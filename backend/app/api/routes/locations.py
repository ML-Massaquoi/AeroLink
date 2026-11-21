from fastapi import APIRouter, Depends, Query, status

from app.api.deps import DbSession, require_permission
from app.models import Location, User
from app.schemas.location import (
    LocationCreate,
    LocationList,
    LocationOut,
    LocationTreeNode,
    LocationUpdate,
)
from app.services import locations as location_service

router = APIRouter(prefix="/locations", tags=["locations"])


def _out(location: Location) -> LocationOut:
    return LocationOut(
        id=location.id,
        code=location.code,
        name=location.name,
        type=location.type,
        parent_id=location.parent_id,
        description=location.description,
        is_archived=location.is_archived,
        created_at=location.created_at.isoformat() if location.created_at else None,
    )


@router.get("", response_model=LocationList)
def list_locations(
    db: DbSession,
    user: User = Depends(require_permission("infra.read")),
    type: str | None = Query(default=None),
    parent_id: int | None = Query(default=None),
    q: str | None = Query(default=None, max_length=128),
    include_archived: bool = Query(default=False),
    limit: int = Query(default=100, le=500),
    offset: int = Query(default=0, ge=0),
) -> LocationList:
    rows, total = location_service.list_locations(
        db,
        type_filter=type,
        parent_id=parent_id,
        q=q,
        include_archived=include_archived,
        limit=limit,
        offset=offset,
    )
    return LocationList(items=[_out(r) for r in rows], total=total)


@router.get("/tree", response_model=list[LocationTreeNode])
def location_tree(
    db: DbSession,
    user: User = Depends(require_permission("infra.read")),
    include_archived: bool = Query(default=False),
) -> list[LocationTreeNode]:
    return location_service.get_location_tree(db, include_archived=include_archived)


@router.get("/{location_id}", response_model=LocationOut)
def get_location(
    location_id: int,
    db: DbSession,
    user: User = Depends(require_permission("infra.read")),
) -> LocationOut:
    location = location_service.get_location(db, location_id)
    return _out(location)


@router.post("", response_model=LocationOut, status_code=status.HTTP_201_CREATED)
def create_location(
    payload: LocationCreate,
    db: DbSession,
    actor: User = Depends(require_permission("infra.write")),
) -> LocationOut:
    location = location_service.create_location(db, payload, actor_id=actor.id)
    return _out(location)


@router.patch("/{location_id}", response_model=LocationOut)
def update_location(
    location_id: int,
    payload: LocationUpdate,
    db: DbSession,
    actor: User = Depends(require_permission("infra.write")),
) -> LocationOut:
    location = location_service.update_location(db, location_id, payload, actor_id=actor.id)
    return _out(location)


@router.post("/{location_id}/archive", response_model=LocationOut)
def archive_location(
    location_id: int,
    db: DbSession,
    actor: User = Depends(require_permission("infra.write")),
) -> LocationOut:
    location = location_service.archive_location(db, location_id, actor_id=actor.id, archived=True)
    return _out(location)


@router.post("/{location_id}/unarchive", response_model=LocationOut)
def unarchive_location(
    location_id: int,
    db: DbSession,
    actor: User = Depends(require_permission("infra.write")),
) -> LocationOut:
    location = location_service.archive_location(db, location_id, actor_id=actor.id, archived=False)
    return _out(location)
