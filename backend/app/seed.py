"""Idempotent seed: permissions, roles, optional initial administrator.

Run with:  python -m app.seed
Called by the Docker entrypoint after migrations.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models import Permission, Role, User

PERMISSIONS: list[tuple[str, str]] = [
    ("infra.read", "View infrastructure records"),
    ("infra.write", "Create and modify infrastructure records"),
    ("ops.write", "Manage work orders and maintenance records"),
    ("audit.read", "View audit history"),
    ("admin.users.read", "View users and roles"),
    ("admin.users.manage", "Create and modify users"),
    ("settings.manage", "Manage application settings"),
    ("reports.export", "Generate and export reports"),
]

ROLES: dict[str, tuple[str, list[str]]] = {
    "System Administrator": (
        "Full access, configuration, user and permission management",
        [c for c, _ in PERMISSIONS],
    ),
    "IT Manager": (
        "Full infrastructure visibility, reports, approvals, oversight",
        [
            "infra.read",
            "infra.write",
            "ops.write",
            "audit.read",
            "admin.users.read",
            "reports.export",
        ],
    ),
    "Network Administrator": (
        "Network assets, switch, port, cable and connectivity management",
        ["infra.read", "infra.write", "ops.write", "audit.read", "reports.export"],
    ),
    "IT Technician": (
        "View infrastructure, perform authorized updates and maintenance",
        ["infra.read", "infra.write", "ops.write"],
    ),
    "Read-only / Auditor": (
        "View records, history, reports and infrastructure maps",
        ["infra.read", "audit.read", "reports.export"],
    ),
}


def seed(db: Session) -> None:
    perm_by_code: dict[str, Permission] = {}
    for codename, description in PERMISSIONS:
        perm = db.scalar(select(Permission).where(Permission.codename == codename))
        if perm is None:
            perm = Permission(codename=codename, description=description)
            db.add(perm)
            db.flush()
        perm_by_code[codename] = perm

    for name, (description, codes) in ROLES.items():
        role = db.scalar(select(Role).where(Role.name == name))
        if role is None:
            role = Role(name=name, description=description)
            db.add(role)
            db.flush()
        role.permissions = [perm_by_code[c] for c in codes]
        db.add(role)

    settings = get_settings()
    if settings.seed_admin_email and settings.seed_admin_password:
        email = settings.seed_admin_email.lower().strip()
        if not db.scalar(select(User).where(User.email == email)):
            admin_role = db.scalar(select(Role).where(Role.name == "System Administrator"))
            assert admin_role is not None
            db.add(
                User(
                    email=email,
                    full_name="System Administrator",
                    password_hash=hash_password(settings.seed_admin_password),
                    role_id=admin_role.id,
                    is_active=True,
                )
            )

    db.commit()


def main() -> None:
    with SessionLocal() as db:
        seed(db)
    print("Seed complete.")


if __name__ == "__main__":
    main()
