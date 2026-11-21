"""Rack domain logic: placement-capable inventory, validation, archive."""

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.models import Location, Rack
from app.models.rack import MAX_RACK_U, MIN_RACK_U, RACK_LOCATION_TYPES, RACK_STATUSES
from app.schemas.rack import RackCreate, RackUpdate
from app.services.audit import record_event


def _get_or_404(db: Session, rack_id: int) -> Rack:
    rack = db.scalar(
        select(Rack).options(joinedload(Rack.location)).where(Rack.id == rack_id)
    )
    if rack is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rack not found")
    return rack


def _ensure_code_free(db: Session, code: str, exclude_id: int | None = None) -> None:
    query = select(Rack).where(func.lower(Rack.code) == code.lower())
    if exclude_id is not None:
        query = query.where(Rack.id != exclude_id)
    if db.scalar(query) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"Rack code '{code}' already exists"
        )


def _validate_location(db: Session, location_id: int) -> Location:
    location = db.get(Location, location_id)
    if location is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")
    if location.type not in RACK_LOCATION_TYPES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Racks can only be placed in a room or technical room",
        )
    if location.is_archived:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Location is archived",
        )
    return location


def _validate_height(height_u: int) -> None:
    if not (MIN_RACK_U <= height_u <= MAX_RACK_U):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"Rack height must be between {MIN_RACK_U} and {MAX_RACK_U} U",
        )


def create_rack(db: Session, payload: RackCreate, actor_id: int) -> Rack:
    _ensure_code_free(db, payload.code)
    _validate_location(db, payload.location_id)
    _validate_height(payload.height_u)

    rack = Rack(
        code=payload.code,
        name=payload.name.strip(),
        location_id=payload.location_id,
        height_u=payload.height_u,
        status=payload.status,
        description=payload.description,
        is_archived=False,
    )
    db.add(rack)
    db.flush()
    record_event(
        db,
        action="rack.created",
        entity_type="rack",
        entity_id=rack.id,
        user_id=actor_id,
        new_state={
            "code": rack.code,
            "name": rack.name,
            "location_id": rack.location_id,
            "height_u": rack.height_u,
            "status": rack.status,
        },
    )
    db.commit()
    return _get_or_404(db, rack.id)


def update_rack(db: Session, rack_id: int, payload: RackUpdate, actor_id: int) -> Rack:
    rack = _get_or_404(db, rack_id)
    changes: dict[str, object] = {}
    previous = {
        "code": rack.code,
        "name": rack.name,
        "location_id": rack.location_id,
        "height_u": rack.height_u,
        "status": rack.status,
        "description": rack.description,
    }

    if payload.code is not None and payload.code.lower() != rack.code.lower():
        _ensure_code_free(db, payload.code, exclude_id=rack.id)
        rack.code = payload.code
        changes["code"] = rack.code
    if payload.name is not None and payload.name.strip() != rack.name:
        rack.name = payload.name.strip()
        changes["name"] = rack.name
    if payload.location_id is not None and payload.location_id != rack.location_id:
        _validate_location(db, payload.location_id)
        rack.location_id = payload.location_id
        changes["location_id"] = rack.location_id
    if payload.height_u is not None and payload.height_u != rack.height_u:
        _validate_height(payload.height_u)
        rack.height_u = payload.height_u
        changes["height_u"] = rack.height_u
    if payload.status is not None and payload.status != rack.status:
        rack.status = payload.status
        changes["status"] = rack.status
    if payload.description is not None and payload.description != rack.description:
        rack.description = payload.description
        changes["description"] = rack.description

    if changes:
        db.add(rack)
        record_event(
            db,
            action="rack.updated",
            entity_type="rack",
            entity_id=rack.id,
            user_id=actor_id,
            previous_state=previous,
            new_state=changes,
        )
        db.commit()
        return _get_or_404(db, rack.id)
    return rack


def archive_rack(db: Session, rack_id: int, actor_id: int, archived: bool = True) -> Rack:
    rack = _get_or_404(db, rack_id)

    if rack.is_archived != archived:
        rack.is_archived = archived
        db.add(rack)
        record_event(
            db,
            action="rack.archived" if archived else "rack.unarchived",
            entity_type="rack",
            entity_id=rack.id,
            user_id=actor_id,
            new_state={"code": rack.code, "is_archived": archived},
        )
        db.commit()
        return _get_or_404(db, rack.id)
    return rack


def get_rack(db: Session, rack_id: int) -> Rack:
    return _get_or_404(db, rack_id)


def list_racks(
    db: Session,
    *,
    location_id: int | None = None,
    status_filter: str | None = None,
    q: str | None = None,
    include_archived: bool = False,
    limit: int = 100,
    offset: int = 0,
) -> tuple[list[Rack], int]:
    query = select(Rack).options(joinedload(Rack.location))
    if location_id is not None:
        query = query.where(Rack.location_id == location_id)
    if status_filter:
        if status_filter not in RACK_STATUSES:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f"Unknown rack status: {status_filter}",
            )
        query = query.where(Rack.status == status_filter)
    if q:
        pattern = f"%{q.strip()}%"
        query = query.where(Rack.name.ilike(pattern) | Rack.code.ilike(pattern))
    if not include_archived:
        query = query.where(Rack.is_archived.is_(False))

    total = db.scalar(select(func.count()).select_from(query.subquery())) or 0
    rows = db.scalars(query.order_by(Rack.code).limit(limit).offset(offset)).all()
    return list(rows), total
