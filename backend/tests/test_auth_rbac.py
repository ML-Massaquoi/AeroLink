def test_login_requires_valid_credentials(client):
    r = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@aerolink.dev", "password": "wrong-password"},
    )
    assert r.status_code == 401

    r = client.post(
        "/api/v1/auth/login",
        json={"email": "nobody@aerolink.dev", "password": "whatever123"},
    )
    assert r.status_code == 401


def test_login_and_me_roundtrip(client, seed_users):
    r = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@aerolink.dev", "password": "AdminPass123!"},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["email"] == "admin@aerolink.dev"
    assert body["role"]["name"] == "System Administrator"
    assert "infra.read" in body["role"]["permissions"]
    assert "admin.users.manage" in body["role"]["permissions"]

    r = client.get("/api/v1/auth/me")
    assert r.status_code == 200
    assert r.json()["email"] == "admin@aerolink.dev"


def test_me_requires_authentication(client):
    r = client.get("/api/v1/auth/me")
    assert r.status_code == 401


def test_logout_revokes_session(client):
    r = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@aerolink.dev", "password": "AdminPass123!"},
    )
    assert r.status_code == 200

    r = client.post("/api/v1/auth/logout")
    assert r.status_code == 200

    r = client.get("/api/v1/auth/me")
    assert r.status_code == 401


def test_rbac_enforced_on_users_endpoint(client, seed_users):
    # unauthenticated
    assert client.get("/api/v1/users").status_code == 401

    emails = seed_users["emails"]
    password = seed_users["password"]

    # Read-only auditor lacks admin.users.read
    r = client.post(
        "/api/v1/auth/login",
        json={"email": emails["Read-only / Auditor"], "password": password},
    )
    assert r.status_code == 200
    r = client.get("/api/v1/users")
    assert r.status_code == 403
    client.post("/api/v1/auth/logout")

    # System Administrator can list users
    r = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@aerolink.dev", "password": "AdminPass123!"},
    )
    assert r.status_code == 200
    r = client.get("/api/v1/users")
    assert r.status_code == 200
    assert r.json()["total"] >= 6  # admin + 5 seeded role users


def test_create_user_requires_manage_permission(client, seed_users):
    emails = seed_users["emails"]
    password = seed_users["password"]

    # IT Technician cannot create users
    r = client.post(
        "/api/v1/auth/login",
        json={"email": emails["IT Technician"], "password": password},
    )
    assert r.status_code == 200
    r = client.post(
        "/api/v1/users",
        json={
            "email": "new@aerolink.dev",
            "full_name": "New User",
            "password": "StrongPass123!",
            "role_id": 1,
        },
    )
    assert r.status_code == 403
    client.post("/api/v1/auth/logout")

    # Admin can create users
    r = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@aerolink.dev", "password": "AdminPass123!"},
    )
    assert r.status_code == 200

    # fetch roles to find IT Technician role id
    roles = client.get("/api/v1/roles").json()
    tech_role_id = next(r["id"] for r in roles if r["name"] == "IT Technician")

    r = client.post(
        "/api/v1/users",
        json={
            "email": "new@aerolink.dev",
            "full_name": "New User",
            "password": "StrongPass123!",
            "role_id": tech_role_id,
        },
    )
    assert r.status_code == 201, r.text
    assert r.json()["email"] == "new@aerolink.dev"

    # duplicate email rejected
    r = client.post(
        "/api/v1/users",
        json={
            "email": "new@aerolink.dev",
            "full_name": "Duplicate",
            "password": "StrongPass123!",
            "role_id": tech_role_id,
        },
    )
    assert r.status_code == 409


def test_audit_log_records_login_events(client):
    client.post(
        "/api/v1/auth/login",
        json={"email": "admin@aerolink.dev", "password": "AdminPass123!"},
    )
    r = client.get("/api/v1/audit")
    assert r.status_code == 200
    actions = [e["action"] for e in r.json()["items"]]
    assert "auth.login" in actions


def test_inactive_user_cannot_login(client, db_session_factory):
    from sqlalchemy import select

    from app.core.security import hash_password
    from app.models import Role, User

    with db_session_factory() as session:
        role = session.scalar(select(Role).where(Role.name == "IT Technician"))
        session.add(
            User(
                email="inactive@aerolink.dev",
                full_name="Inactive User",
                password_hash=hash_password("SomePass123!"),
                role_id=role.id,
                is_active=False,
            )
        )
        session.commit()

    r = client.post(
        "/api/v1/auth/login",
        json={"email": "inactive@aerolink.dev", "password": "SomePass123!"},
    )
    assert r.status_code == 401
