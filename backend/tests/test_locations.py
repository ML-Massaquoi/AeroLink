"""Locations module: hierarchy, unique codes, RBAC, audit."""


def _login(client, email):
    r = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "AdminPass123!"},
    )
    assert r.status_code == 200, r.text
    return r.json()


def _create(client, code, name, type_, parent_id=None, description=None):
    return client.post(
        "/api/v1/locations",
        json={
            "code": code,
            "name": name,
            "type": type_,
            "parent_id": parent_id,
            "description": description,
        },
    )


def test_building_then_floor_then_room_hierarchy(admin_client):
    r = _create(admin_client, "FIA-BLD-01", "Main Terminal", "building")
    assert r.status_code == 201, r.text
    building = r.json()

    # floor under building
    r = _create(admin_client, "FIA-BLD-01-FL-001", "Ground Floor", "floor", building["id"])
    assert r.status_code == 201, r.text
    floor = r.json()

    # room under floor
    r = _create(admin_client, "FIA-ROOM-04", "Immigration Office 04", "room", floor["id"])
    assert r.status_code == 201, r.text

    # technical room under floor
    r = _create(admin_client, "FIA-TR-01", "Telecom Room 01", "technical_room", floor["id"])
    assert r.status_code == 201, r.text

    # tree reflects structure
    tree = admin_client.get("/api/v1/locations/tree").json()
    assert len(tree) == 1
    assert tree[0]["code"] == "FIA-BLD-01"
    assert len(tree[0]["children"]) == 1
    child_codes = {c["code"] for c in tree[0]["children"][0]["children"]}
    assert child_codes == {"FIA-ROOM-04", "FIA-TR-01"}


def test_hierarchy_validation_rejects_invalid_parents(admin_client):
    # floor requires a building parent
    r = _create(admin_client, "BAD-FL", "Orphan Floor", "floor", None)
    assert r.status_code == 422

    building = _create(admin_client, "FIA-BLD-02", "Cargo Terminal", "building").json()

    # building cannot be a child
    r = _create(admin_client, "BAD-BLD", "Nested Building", "building", building["id"])
    assert r.status_code == 422

    # room cannot sit directly under a building (must be floor/area)
    r = _create(admin_client, "BAD-ROOM", "Loose Room", "room", building["id"])
    assert r.status_code == 422

    # unknown type rejected by schema
    r = admin_client.post(
        "/api/v1/locations",
        json={"code": "BAD-TYPE", "name": "X", "type": "hangar", "parent_id": None},
    )
    assert r.status_code == 422

    # nonexistent parent
    r = _create(admin_client, "BAD-PAR", "Ghost Child", "floor", 99999)
    assert r.status_code == 404


def test_duplicate_codes_rejected(admin_client):
    assert _create(admin_client, "FIA-DUP", "First", "building").status_code == 201
    r = _create(admin_client, "FIA-DUP", "Second", "building")
    assert r.status_code == 409
    # case-insensitive duplicate
    r = _create(admin_client, "fia-dup", "Third", "building")
    assert r.status_code == 409


def test_update_and_audit(admin_client):
    building = _create(admin_client, "FIA-BLD-03", "Old Name", "building").json()

    r = admin_client.patch(f"/api/v1/locations/{building['id']}", json={"name": "New Name"})
    assert r.status_code == 200
    assert r.json()["name"] == "New Name"

    audit = admin_client.get("/api/v1/audit").json()
    actions = [e["action"] for e in audit["items"]]
    assert "location.created" in actions
    assert "location.updated" in actions


def test_archive_rules(admin_client):
    building = _create(admin_client, "FIA-BLD-04", "Archivable", "building").json()
    _create(admin_client, "FIA-FL-04", "Floor A", "floor", building["id"])

    # cannot archive while active children exist
    r = admin_client.post(f"/api/v1/locations/{building['id']}/archive")
    assert r.status_code == 422

    # archive child first, then parent
    floor = admin_client.get("/api/v1/locations", params={"parent_id": building["id"]}).json()[
        "items"
    ][0]
    assert admin_client.post(f"/api/v1/locations/{floor['id']}/archive").status_code == 200
    assert admin_client.post(f"/api/v1/locations/{building['id']}/archive").status_code == 200

    # archived hidden by default, visible with flag
    active = admin_client.get("/api/v1/locations", params={"q": "Archivable"}).json()
    assert active["total"] == 0
    with_archived = admin_client.get(
        "/api/v1/locations", params={"q": "Archivable", "include_archived": True}
    ).json()
    assert with_archived["total"] == 1


def test_rbac_locations(client, seed_users):
    # unauthenticated
    assert client.get("/api/v1/locations").status_code == 401

    emails = seed_users["emails"]
    password = seed_users["password"]

    # Auditor: read yes, write no
    client.post(
        "/api/v1/auth/login",
        json={"email": emails["Read-only / Auditor"], "password": password},
    )
    assert client.get("/api/v1/locations").status_code == 200
    r = _create(client, "AUD-BLD", "Auditor Try", "building")
    assert r.status_code == 403
    client.post("/api/v1/auth/logout")

    # Technician: write allowed
    client.post(
        "/api/v1/auth/login",
        json={"email": emails["IT Technician"], "password": password},
    )
    r = _create(client, "TECH-BLD", "Tech Building", "building")
    assert r.status_code == 201, r.text
    client.post("/api/v1/auth/logout")


def test_search_and_filter(admin_client):
    _create(admin_client, "FIA-SEARCH-1", "Searchable Alpha", "building")
    _create(admin_client, "FIA-SEARCH-2", "Searchable Beta", "building")

    r = admin_client.get("/api/v1/locations", params={"q": "Searchable"})
    assert r.json()["total"] == 2

    r = admin_client.get("/api/v1/locations", params={"type": "building", "q": "Searchable"})
    assert r.json()["total"] == 2

    r = admin_client.get("/api/v1/locations", params={"type": "room"})
    assert r.json()["total"] == 0
