# AeroLink — System Architecture

## Overview

Modular monolith: a **Next.js** frontend and a **FastAPI** backend sharing a
**PostgreSQL** database. No direct database access from the frontend; every
data operation goes through the REST API with server-side authorization.

```
Browser ──► Next.js (App Router, port 3000)
              │  same-origin /api/v1/* rewrite
              ▼
           FastAPI (port 8000/8010)
              │  SQLAlchemy sessions, service layer
              ▼
           PostgreSQL 16+
```

In Docker, Next.js rewrites `/api/*` to `http://backend:8000`; in local
development to `BACKEND_API_URL`. This keeps session cookies first-party and
removes CORS from the dev loop.

## Frontend responsibilities

- Rendering, navigation, forms (React Hook Form + Zod client validation).
- Server-side session check in `(app)/layout.tsx` (redirects to `/login`).
- `src/lib/api.ts` — single typed fetch client (`apiFetch`), error mapping.
- `src/components/visualizations/` — dedicated diagram layer (see
  docs/VISUALIZATION.md). No diagram logic inside dashboard pages.
- UI hiding of unauthorized controls is **cosmetic**; enforcement is backend.

## Backend responsibilities

- `app/api/routes/` — HTTP layer only: validation, status codes, serialization.
- `app/services/` — business logic (auth, audit, serialize; domain services
  grow here: locations, racks, switches, tracing…).
- `app/models/` — SQLAlchemy 2.0 models; `app/schemas/` — Pydantic contracts.
- `app/core/` — settings (pydantic-settings, env-only), DB engine/session,
  security primitives (argon2, session tokens).
- Permission checks via `require_permission("codename")` dependency on every
  mutating/sensitive route.

## Session & auth flow

1. `POST /auth/login` verifies argon2 hash, creates a `sessions` row storing
   only the SHA-256 of a random token; sets httpOnly, SameSite=Lax cookie.
2. Every request resolves the cookie → session row → user + role permissions.
3. `POST /auth/logout` revokes (soft) the session server-side.
4. Expiry enforced by `expires_at`; inactive users rejected at resolution.

## Auditing

`services/audit.record_event()` appends `audit_events` rows (user, action,
entity, previous/new state, reason). Ordinary users have no API path to alter
or delete audit rows.

## Background work (future)

Discovery jobs, reconciliation and report generation will run as background
tasks behind the same service layer (FastAPI BackgroundTasks now; dedicated
worker when discovery lands). Protocol logic stays isolated from routes;
vendor specifics live in adapters.

## Module boundaries

Stages and module map: docs/ROADMAP.md · Decisions: docs/DECISIONS.md ·
Visualization: docs/VISUALIZATION.md.
