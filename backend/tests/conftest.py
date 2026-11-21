import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import get_db
from app.main import create_app
from app.models import Base
from app.seed import seed


@pytest.fixture()
def db_session_factory():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    Base.metadata.create_all(engine)
    TestingSession = sessionmaker(
        bind=engine, autoflush=False, autocommit=False, expire_on_commit=False
    )
    with TestingSession() as session:
        seed(session)
        _create_admin(session)
    yield TestingSession
    engine.dispose()


def _create_admin(session) -> None:
    from sqlalchemy import select

    from app.core.security import hash_password
    from app.models import Role, User

    if session.scalar(select(User).where(User.email == "admin@aerolink.dev")):
        return
    role = session.scalar(select(Role).where(Role.name == "System Administrator"))
    session.add(
        User(
            email="admin@aerolink.dev",
            full_name="Test Admin",
            password_hash=hash_password("AdminPass123!"),
            role_id=role.id,
            is_active=True,
        )
    )
    session.commit()


@pytest.fixture()
def client(db_session_factory):
    app = create_app()

    def override_get_db():
        session = db_session_factory()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def admin_client(client, db_session_factory):
    """Logged-in client with System Administrator permissions."""
    r = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@aerolink.dev", "password": "AdminPass123!"},
    )
    assert r.status_code == 200, r.text
    return client


@pytest.fixture()
def seed_users(db_session_factory):
    """Create one user per role for RBAC tests. Returns {role_name: email}."""
    from sqlalchemy import select

    from app.core.security import hash_password
    from app.models import Role, User

    passwords = "TechnicianPass1!"
    emails: dict[str, str] = {}
    with db_session_factory() as session:
        roles = session.scalars(select(Role)).all()
        for role in roles:
            slug = role.name.lower().replace(" / ", "-").replace(" ", "-")
            email = f"{slug}@aerolink.dev"
            session.add(
                User(
                    email=email,
                    full_name=role.name,
                    password_hash=hash_password(passwords),
                    role_id=role.id,
                    is_active=True,
                )
            )
            emails[role.name] = email
        session.commit()
    return {"emails": emails, "password": passwords}
