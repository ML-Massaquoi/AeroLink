from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select

from app.api.deps import CurrentUser, DbSession, require_permission
from app.core.security import hash_password
from app.models import AuditEvent, Role, User
from app.schemas.auth import (
    AuditEventList,
    AuditEventOut,
    RoleOut,
    UserCreate,
    UserList,
    UserOut,
)
from app.services.audit import record_event
from app.services.serialize import role_out, user_out

router = APIRouter(tags=["users"])


@router.get("/users", response_model=UserList)
def list_users(
    db: DbSession,
    user: User = Depends(require_permission("admin.users.read")),
    limit: int = 100,
    offset: int = 0,
) -> UserList:
    total = db.scalar(select(func.count()).select_from(User)) or 0
    rows = db.scalars(select(User).order_by(User.id).limit(limit).offset(offset)).all()
    return UserList(items=[user_out(u) for u in rows], total=total)


@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    db: DbSession,
    actor: User = Depends(require_permission("admin.users.manage")),
) -> UserOut:
    email = payload.email.lower().strip()
    if db.scalar(select(User).where(User.email == email)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    role = db.get(Role, payload.role_id)
    if role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    new_user = User(
        email=email,
        full_name=payload.full_name.strip(),
        password_hash=hash_password(payload.password),
        role_id=role.id,
        is_active=True,
    )
    db.add(new_user)
    db.flush()
    record_event(
        db,
        action="user.created",
        entity_type="user",
        entity_id=new_user.id,
        user_id=actor.id,
        new_state={"email": email, "full_name": new_user.full_name, "role": role.name},
    )
    db.commit()
    db.refresh(new_user)
    return user_out(new_user)


@router.get("/roles", response_model=list[RoleOut])
def list_roles(db: DbSession, user: CurrentUser) -> list[RoleOut]:
    roles = db.scalars(select(Role).order_by(Role.id)).all()
    return [role_out(r) for r in roles]


@router.get("/audit", response_model=AuditEventList)
def list_audit(
    db: DbSession,
    user: User = Depends(require_permission("audit.read")),
    limit: int = 50,
    offset: int = 0,
) -> AuditEventList:
    total = db.scalar(select(func.count()).select_from(AuditEvent)) or 0
    rows = db.scalars(
        select(AuditEvent).order_by(AuditEvent.id.desc()).limit(limit).offset(offset)
    ).all()
    return AuditEventList(items=[AuditEventOut.model_validate(r) for r in rows], total=total)
