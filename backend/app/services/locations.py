"""Location domain logic: hierarchy validation, CRUD, archive, tree."""

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import ALLOWED_PARENTS, LOCATION_TYPES, Location
from app.schemas.location import LocationCreate, LocationTreeNode, LocationUpdate
from app.services.audit import record_event


def _get_or_404(db: Session, location_id: int) -> Location:
    location = db.get(Location, location_id)
    if location is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")
    return location


def get_location(db: Session, location_id: int) -> Location:
    return _get_or_404(db, location_id)


def _validate_parent(db: Session, location_type: str, parent_id: int | None) -> Location | None:
    allowed = ALLOWED_PARENTS[location_type]
    if not allowed:
        if parent_id is not None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f"A {location_type} must be a root-level location (no parent)",
            )
        return None
    if parent_id is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"A {location_type} requires a parent of type: {', '.join(allowed)}",
        )
    parent = db.get(Location, parent_id)
    if parent is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Parent location not found"
        )
    if parent.type not in allowed:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"Parent of type '{parent.type}' cannot contain a '{location_type}'",
        )
    if parent.is_archived:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Parent location is archived",
        )
    return parent


def _ensure_code_free(db: Session, code: str, exclude_id: int | None = None) -> None:
    query = select(Location).where(func.lower(Location.code) == code.lower())
    if exclude_id is not None:
        query = query.where(Location.id != exclude_id)
    if db.scalar(query) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"Location code '{code}' already exists"
        )


def create_location(db: Session, payload: LocationCreate, actor_id: int) -> Location:
    _ensure_code_free(db, payload.code)
    _validate_parent(db, payload.type, payload.parent_id)

    location = Location(
        code=payload.code,
        name=payload.name.strip(),
        type=payload.type,
        parent_id=payload.parent_id,
        description=payload.description,
        is_archived=False,
    )
    db.add(location)
    db.flush()
    record_event(
        db,
        action="location.created",
        entity_type="location",
        entity_id=location.id,
        user_id=actor_id,
        new_state={
            "code": location.code,
            "name": location.name,
            "type": location.type,
            "parent_id": location.parent_id,
        },
    )
    db.commit()
    db.refresh(location)
    return location


def update_location(
    db: Session, location_id: int, payload: LocationUpdate, actor_id: int
) -> Location:
    location = _get_or_404(db, location_id)
    changes: dict[str, object] = {}
    previous = {"code": location.code, "name": location.name, "description": location.description}

    if payload.code is not None and payload.code.lower() != location.code.lower():
        _ensure_code_free(db, payload.code, exclude_id=location.id)
        location.code = payload.code
        changes["code"] = payload.code
    if payload.name is not None and payload.name.strip() != location.name:
        location.name = payload.name.strip()
        changes["name"] = location.name
    if payload.description is not None and payload.description != location.description:
        location.description = payload.description
        changes["description"] = location.description

    if changes:
        db.add(location)
        record_event(
            db,
            action="location.updated",
            entity_type="location",
            entity_id=location.id,
            user_id=actor_id,
            previous_state=previous,
            new_state=changes,
        )
        db.commit()
        db.refresh(location)
    return location


def archive_location(
    db: Session, location_id: int, actor_id: int, archived: bool = True
) -> Location:
    location = _get_or_404(db, location_id)

    if archived:
        active_children = db.scalar(
            select(func.count())
            .select_from(Location)
            .where(Location.parent_id == location.id, Location.is_archived.is_(False))
        )
        if active_children:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Cannot archive: location still has active child locations",
            )

    if location.is_archived != archived:
        location.is_archived = archived
        db.add(location)
        record_event(
            db,
            action="location.archived" if archived else "location.unarchived",
            entity_type="location",
            entity_id=location.id,
            user_id=actor_id,
            new_state={"code": location.code, "is_archived": archived},
        )
        db.commit()
        db.refresh(location)
    return location


def list_locations(
    db: Session,
    *,
    type_filter: str | None = None,
    parent_id: int | None = None,
    q: str | None = None,
    include_archived: bool = False,
    limit: int = 100,
    offset: int = 0,
) -> tuple[list[Location], int]:
    query = select(Location)
    if type_filter:
        if type_filter not in LOCATION_TYPES:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f"Unknown location type: {type_filter}",
            )
        query = query.where(Location.type == type_filter)
    if parent_id is not None:
        query = query.where(Location.parent_id == parent_id)
    if q:
        pattern = f"%{q.strip()}%"
        query = query.where(Location.name.ilike(pattern) | Location.code.ilike(pattern))
    if not include_archived:
        query = query.where(Location.is_archived.is_(False))

    total = db.scalar(select(func.count()).select_from(query.subquery())) or 0
    rows = db.scalars(
        query.order_by(Location.type, Location.name).limit(limit).offset(offset)
    ).all()
    return list(rows), total


def get_location_tree(db: Session, include_archived: bool = False) -> list[LocationTreeNode]:
    query = select(Location)
    if not include_archived:
        query = query.where(Location.is_archived.is_(False))
    locations = db.scalars(query.order_by(Location.name)).all()

    nodes = {
        loc.id: LocationTreeNode(
            id=loc.id,
            code=loc.code,
            name=loc.name,
            type=loc.type,
            is_archived=loc.is_archived,
            children=[],
        )
        for loc in locations
    }
    roots: list[LocationTreeNode] = []
    for loc in locations:
        node = nodes[loc.id]
        if loc.parent_id is not None and loc.parent_id in nodes:
            nodes[loc.parent_id].children.append(node)
        else:
            roots.append(node)
    return roots
