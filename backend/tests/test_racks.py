"""Racks module: inventory, location rules, U height, RBAC, audit."""


def _login(client, email):
    r = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "AdminPass123!"},
    )
    assert r.status_code == 200, r.text
    return r.json()


def _create_location(client, code, name, type_, parent_id=None):
    r = client.post(
        "/api/v1/locations",
        json={"code": code, "name": name, "type": type_, "parent_id": parent_id},
    )
    assert r.status_code == 201, r.text
    return r.json()


def _create_rack(client, code, name, location_id, height_u=42, status="active", description=None):
    return client.post(
        "/api/v1/racks",
        json={
            "code": code,
            "name": name,
            "location_id": location_id,
            "height_u": height_u,
            "status": status,
            "description": description,
        },
    )


def _tech_room(client, suffix="01"):
    building = _create_location(client, f"FIA-RK-BLD-{suffix}", f"Terminal {suffix}", "building")
    floor = _create_location(
        client, f"FIA-RK-FL-{suffix}", f"Level {suffix}", "floor", building["id"]
    )
    room = _create_location(
        client, f"FIA-RK-TR-{suffix}", f"Telecom Room {suffix}", "technical_room", floor["id"]
    )
    return room


def test_create_rack_in_technical_room(admin_client):
    room = _tech_room(admin_client)

    r = _create_rack(admin_client, "FIA-RACK-01", "Core Rack A", room["id"], height_u=42)
    assert r.status_code == 201, r.text
    rack = r.json()
    assert rack["code"] == "FIA-RACK-01"
    assert rack["height_u"] == 42
    assert rack["status"] == "active"
    assert rack["location"]["code"] == room["code"]

    # detail fetch works
    detail = admin_client.get(f"/api/v1/racks/{rack['id']}").json()
    assert detail["name"] == "Core Rack A"


def test_rack_requires_room_or_technical_room(admin_client):
    building = _create_location(admin_client, "FIA-RK-BLD-X", "Tower X", "building")
    floor = _create_location(admin_client, "FIA-RK-FL-X", "Floor X", "floor", building["id"])

    # building rejected
    r = _create_rack(admin_client, "RACK-BAD-1", "Bad Rack", building["id"])
    assert r.status_code == 422

    # floor rejected
    r = _create_rack(admin_client, "RACK-BAD-2", "Bad Rack", floor["id"])
    assert r.status_code == 422

    # plain room allowed
    room = _create_location(admin_client, "FIA-RK-RM-X", "Office X", "room", floor["id"])
    r = _create_rack(admin_client, "RACK-OK-RM", "Office Rack", room["id"], height_u=12)
    assert r.status_code == 201, r.text


def test_height_and_status_validation(admin_client):
    room = _tech_room(admin_client, "H")

    r = _create_rack(admin_client, "RACK-H-0", "Zero U", room["id"], height_u=0)
    assert r.status_code == 422

    r = _create_rack(admin_client, "RACK-H-99", "Huge", room["id"], height_u=99)
    assert r.status_code == 422

    r = _create_rack(admin_client, "RACK-H-ST", "Bad Status", room["id"], status="on_fire")
    assert r.status_code == 422

    # unknown location
    r = admin_client.post(
        "/api/v1/racks",
        json={"code": "RACK-LOC-404", "name": "Ghost", "location_id": 99999, "height_u": 42},
    )
    assert r.status_code == 404


def test_duplicate_rack_codes_rejected(admin_client):
    room = _tech_room(admin_client, "D")
    assert _create_rack(admin_client, "RACK-DUP", "First", room["id"]).status_code == 201
    r = _create_rack(admin_client, "RACK-DUP", "Second", room["id"])
    assert r.status_code == 409
    r = _create_rack(admin_client, "rack-dup", "Third", room["id"])
    assert r.status_code == 409


def test_update_rack_and_audit(admin_client):
    room = _tech_room(admin_client, "U")
    rack = _create_rack(admin_client, "RACK-UPD", "Old Name", room["id"]).json()

    r = admin_client.patch(f"/api/v1/racks/{rack['id']}", json={"name": "New Name", "height_u": 47})
    assert r.status_code == 200
    body = r.json()
    assert body["name"] == "New Name"
    assert body["height_u"] == 47

    audit = admin_client.get("/api/v1/audit").json()
    actions = [e["action"] for e in audit["items"]]
    assert "rack.created" in actions
    assert "rack.updated" in actions


def test_archive_rack(admin_client):
    room = _tech_room(admin_client, "A")
    rack = _create_rack(admin_client, "RACK-ARCH", "Archivable", room["id"]).json()

    assert admin_client.post(f"/api/v1/racks/{rack['id']}/archive").status_code == 200
    active = admin_client.get("/api/v1/racks", params={"q": "Archivable"}).json()
    assert active["total"] == 0
    with_archived = admin_client.get(
        "/api/v1/racks", params={"q": "Archivable", "include_archived": True}
    ).json()
    assert with_archived["total"] == 1

    assert admin_client.post(f"/api/v1/racks/{rack['id']}/unarchive").status_code == 200
    assert admin_client.get("/api/v1/racks", params={"q": "Archivable"}).json()["total"] == 1


def test_rbac_racks(client, admin_client, seed_users):
    # admin_client is the same client logged in as admin — create fixtures, then log out
    room = _tech_room(admin_client, "RB")
    admin_client.post("/api/v1/auth/logout")

    # unauthenticated
    assert client.get("/api/v1/racks").status_code == 401

    emails = seed_users["emails"]
    password = seed_users["password"]

    # Auditor: read yes, write no
    client.post(
        "/api/v1/auth/login",
        json={"email": emails["Read-only / Auditor"], "password": password},
    )
    assert client.get("/api/v1/racks").status_code == 200
    r = _create_rack(client, "AUD-RACK", "Auditor Try", room["id"])
    assert r.status_code == 403
    client.post("/api/v1/auth/logout")

    # Technician: write allowed
    client.post(
        "/api/v1/auth/login",
        json={"email": emails["IT Technician"], "password": password},
    )
    r = _create_rack(client, "TECH-RACK", "Tech Rack", room["id"], height_u=24)
    assert r.status_code == 201, r.text
    client.post("/api/v1/auth/logout")


def test_search_and_location_filter(admin_client):
    room = _tech_room(admin_client, "S")
    other = _tech_room(admin_client, "T")

    _create_rack(admin_client, "RACK-S-1", "Searchable Alpha", room["id"])
    _create_rack(admin_client, "RACK-S-2", "Searchable Beta", room["id"])
    _create_rack(admin_client, "RACK-S-3", "Other Rack", other["id"])

    assert admin_client.get("/api/v1/racks", params={"q": "Searchable"}).json()["total"] == 2
    assert (
        admin_client.get("/api/v1/racks", params={"location_id": room["id"]}).json()["total"]
        == 2
    )
    assert admin_client.get("/api/v1/racks", params={"status": "active"}).json()["total"] >= 3
    assert admin_client.get("/api/v1/racks", params={"status": "on_fire"}).status_code == 422
