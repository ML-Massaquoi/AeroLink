from app.models import Role, User
from app.schemas.auth import RoleOut, UserOut


def role_out(role: Role) -> RoleOut:
    return RoleOut(
        id=role.id,
        name=role.name,
        description=role.description,
        permissions=sorted(p.codename for p in role.permissions),
    )


def user_out(user: User) -> UserOut:
    return UserOut(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        role=role_out(user.role),
        last_login_at=user.last_login_at,
        created_at=user.created_at,
    )
