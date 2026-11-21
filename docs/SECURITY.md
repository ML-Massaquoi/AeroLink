# AeroLink — Security

AeroLink holds sensitive airport infrastructure data. Controls below apply
from the foundation; discovery-stage additions are marked accordingly.

## Authentication

- **argon2id** password hashing (argon2-cffi); automatic rehash on login when
  parameters change.
- Server-side sessions: random 256-bit token in an **httpOnly, SameSite=Lax**
  cookie (`Secure` in production); only the SHA-256 hash is persisted.
- Login failures return a generic 401 and are written to the audit log
  (`auth.login_failed`).
- Session lifetime configurable (`SESSION_MAX_AGE_SECONDS`, default 8 h);
  logout revokes server-side.
- Inactive accounts cannot authenticate or resolve from existing sessions.

## Authorization (RBAC)

- Five seeded roles (PRD §6): System Administrator, IT Manager, Network
  Administrator, IT Technician, Read-only/Auditor.
- Permission codenames stored relationally; checked server-side via the
  `require_permission()` dependency on each route.
- **UI hiding is not authorization** — the frontend masks controls the user
  lacks, but the API independently rejects with 403.

## Data protection

- Secrets only via environment (`pydantic-settings`); `.env` git-ignored;
  `.env.example` contains placeholders.
- CORS restricted to configured origins with credentials allowed.
- Passwords never logged, never returned by the API.
- Session tokens never stored in plaintext; audit rows contain no secrets.
- Input validated with Pydantic on every endpoint (types, lengths, formats).

## Audit

- `audit_events` append-only; no API path modifies or deletes them.
- Captured: logins (success/failure), logouts, user creation, and — as
  modules land — every infrastructure mutation with previous/new state.

## Application hardening

- Parameterized SQL through SQLAlchemy (injection-safe by construction).
- React escaping by default; no `dangerouslySetInnerHTML` in the codebase.
- Structured, generic error responses — no stack traces leaked to clients.
- Dependencies pinned by lockfiles; frontend lint/build gates in CI-ready
  scripts; backend `ruff` + `pytest` gate.

## Deployment

- Docker Compose for pilot; internal network only; HTTPS via reverse proxy
  in production (cookie `Secure` flag activates with `APP_ENV=production`).
- Postgres bound to the compose network; credentials from environment.
- Database backups are an operational requirement before airport rollout
  (see ROADMAP Stage 5).

## Out of scope (MVP, per PRD)

MFA (future), SNMPv3 credential vault (discovery stage), rate limiting
middleware (add before exposure beyond the pilot network).
