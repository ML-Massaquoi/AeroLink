# AeroLink — Database

PostgreSQL is the source of truth. Migrations are managed with Alembic
(`backend/migrations/versions/`). Physical connectivity and logical network
relationships are modeled separately (logical models arrive with later
stages).

## Current schema (0001_initial)

### permissions
| column | type | notes |
|---|---|---|
| id | int PK | |
| codename | varchar(64) unique | e.g. `infra.read`, `admin.users.manage` |
| description | varchar(255) | |

### roles
| column | type | notes |
|---|---|---|
| id | int PK | |
| name | varchar(64) unique | System Administrator, IT Manager, … |
| description | varchar(255) | |
| created_at / updated_at | timestamptz | |

### role_permissions (M:N)
`role_id` → roles, `permission_id` → permissions; both FKs, composite PK,
cascade on delete.

### users
| column | type | notes |
|---|---|---|
| id | int PK | |
| email | varchar(255) unique indexed | lowercased on write |
| full_name | varchar(128) | |
| password_hash | varchar(255) | argon2id |
| is_active | bool | inactive users cannot log in |
| last_login_at | timestamptz nullable | |
| role_id | int FK → roles | single role per user (MVP) |

### sessions
Server-side sessions. `token_hash` (varchar 64, unique, indexed) is the
SHA-256 of the cookie token — raw tokens are never stored. `expires_at`
enforces lifetime; `revoked_at` supports logout. FK → users (cascade).

### audit_events
Append-only history: `user_id` (FK, SET NULL), `action`, `entity_type`,
`entity_id` (string — polymorphic), `previous_state`/`new_state` (JSONB on
PostgreSQL), `reason`, `created_at` indexed. No update/delete API exists.

## Conventions

- Integer surrogate PKs; unique business identifiers (location codes, asset
  tags) modeled as unique columns.
- `TIMESTAMPTZ` everywhere; server defaults via `func.now()`.
- Deletion of infrastructure will use archival flags (e.g. `is_archived`)
  so history and relationships survive; hard deletes reserved for users/
  sessions only.
- JSONB reserved for audit snapshots and future observation payloads — not
  a substitute for relational modeling of connections.

## Planned entities (stages 1–2)

Location (tree, unique code), Rack (+ U placements), Equipment, Switch
(+ auto-generated SwitchPort), PatchPanel (+ ports), Cable, FiberCable/
FiberCore/ODF, Outlet, Endpoint, Connection (FK-based, validated,
transactional allocation), VLAN, WorkOrder, MaintenanceRecord.

Connection integrity rules: ports cannot hold conflicting active
allocations; placements must respect rack capacity; endpoints must exist;
traversal only follows recorded relationships. See PRD §21.
