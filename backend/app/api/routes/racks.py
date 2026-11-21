from fastapi import APIRouter, Depends, Query, status

from app.api.deps import DbSession, require_permission
from app.models import Rack, User
from app.schemas.rack import RackCreate, RackList, RackOut, RackUpdate
from app.services import racks as rack_service

router = APIRouter(prefix="/racks", tags=["racks"])


def _out(rack: Rack) -> RackOut:
    return RackOut(
        id=rack.id,
        code=rack.code,
        name=rack.name,
        location_id=rack.location_id,
        height_u=rack.height_u,
        status=rack.status,
        description=rack.description,
        is_archived=rack.is_archived,
        location=rack.location,
        created_at=rack.created_at.isoformat() if rack.created_at else None,
    )


@router.get("", response_model=RackList)
def list_racks(
    db: DbSession,
    user: User = Depends(require_permission("infra.read")),
    location_id: int | None = Query(default=None),
    status: str | None = Query(default=None),
    q: str | None = Query(default=None, max_length=128),
    include_archived: bool = Query(default=False),
    limit: int = Query(default=100, le=500),
    offset: int = Query(default=0, ge=0),
) -> RackList:
    rows, total = rack_service.list_racks(
        db,
        location_id=location_id,
        status_filter=status,
        q=q,
        include_archived=include_archived,
        limit=limit,
        offset=offset,
    )
    return RackList(items=[_out(r) for r in rows], total=total)


@router.get("/{rack_id}", response_model=RackOut)
def get_rack(
    rack_id: int,
    db: DbSession,
    user: User = Depends(require_permission("infra.read")),
) -> RackOut:
    return _out(rack_service.get_rack(db, rack_id))


@router.post("", response_model=RackOut, status_code=status.HTTP_201_CREATED)
def create_rack(
    payload: RackCreate,
    db: DbSession,
    actor: User = Depends(require_permission("infra.write")),
) -> RackOut:
    rack = rack_service.create_rack(db, payload, actor_id=actor.id)
    return _out(rack)


@router.patch("/{rack_id}", response_model=RackOut)
def update_rack(
    rack_id: int,
    payload: RackUpdate,
    db: DbSession,
    actor: User = Depends(require_permission("infra.write")),
) -> RackOut:
    rack = rack_service.update_rack(db, rack_id, payload, actor_id=actor.id)
    return _out(rack)


@router.post("/{rack_id}/archive", response_model=RackOut)
def archive_rack(
    rack_id: int,
    db: DbSession,
    actor: User = Depends(require_permission("infra.write")),
) -> RackOut:
    rack = rack_service.archive_rack(db, rack_id, actor_id=actor.id, archived=True)
    return _out(rack)


@router.post("/{rack_id}/unarchive", response_model=RackOut)
def unarchive_rack(
    rack_id: int,
    db: DbSession,
    actor: User = Depends(require_permission("infra.write")),
) -> RackOut:
    rack = rack_service.archive_rack(db, rack_id, actor_id=actor.id, archived=False)
    return _out(rack)
