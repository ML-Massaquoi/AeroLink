# AeroLink — Roadmap

Maps README §16 (initial milestone), Blueprint Phase 0–14, and PRD Stages 1–7.
Status legend: `todo` · `in-progress` · `done` · `deferred`

## Stage 0 — Foundation (Blueprint Phases 0–1 · PRD Stage 1)

- [x] Repository structure, decisions recorded (this doc, DECISIONS.md)
- [x] Next.js frontend operational
- [x] FastAPI backend operational
- [x] PostgreSQL + Alembic migrations
- [x] Docker Compose with health checks (files ready; untested — no Docker on bootstrap machine)
- [x] Environment configuration (.env.example, pydantic-settings)
- [x] Authentication (login/logout, sessions, password hashing)
- [x] RBAC (roles, permissions, server-side enforcement)
- [x] Base design system (tokens, shadcn-style primitives)
- [x] Application shell (sidebar nav, top bar, breadcrumbs, user menu)
- [x] Audit foundation (audit table + write path)
- [x] Tests: auth, permissions (9 passing); ruff + lint + typecheck green
- [x] README + docs (ARCHITECTURE, DATABASE, SECURITY)
- [x] Visualization engineering requirements recorded (VISUALIZATION.md, D7)

## Stage 1 — Core infrastructure registry (PRD Stage 2)

- [x] Locations: buildings → floors/areas → rooms/technical rooms (CRUD, search, hierarchy, archive) — 7 tests
- [ ] Racks & cabinets: inventory, U height, placement validation
- [ ] **Rack elevation visualization** (SVG, multi-U, overlap-safe) — VISUALIZATION.md §3
- [ ] Equipment inventory: categories, fields per PRD §7.4/D-Module D
- [ ] Switch registration + automatic port generation (48-port → Ports 1–48)
- [ ] **Switch front-panel visualization** (configurable counts, RJ45/SFP, hover, click) — VISUALIZATION.md §1
- [ ] Port grid + **port inspector** with the six states; actions audited — VISUALIZATION.md §2
- [ ] **Patch panel visualization** (copper/fiber, numbering, states) — VISUALIZATION.md §4
- [ ] Dashboard connected to real backend KPIs (real empty states)

## Stage 2 — Ports & connectivity (PRD Stage 3)

- [ ] Cable registry (types, statuses, terminations, routes)
- [ ] Fiber: cables, cores, ODF records + **fiber/ODF visualization** — VISUALIZATION.md §5
- [ ] Endpoint registry (types, search by name/ID/IP/MAC)
- [ ] Connection records with FK integrity + transactional port allocation
- [ ] Connection tracing (endpoint ⇄ outlet ⇄ patch panel ⇄ switch, forward/reverse)
- [ ] **Backend trace engine + trace path visualization** (incomplete-path reporting) — VISUALIZATION.md §7
- [ ] **React Flow topology view** (documented links only, verified/unverified styling) — VISUALIZATION.md §6
- [ ] Verification states (unverified vs. physically verified)

## Stage 3 — Operational management (PRD Stage 4)

- [ ] Work orders (categories, statuses, priorities, assignment)
- [ ] Maintenance / faults linked to infrastructure
- [ ] Change management + audit history UI
- [ ] QR code generation (unique IDs → authenticated record URLs)

## Stage 4 — Dashboard & reporting (PRD Stage 5)

- [ ] KPIs from real data: assets, ports by state, cables, endpoints, open work orders
- [ ] Port utilization, infrastructure-by-building, recent changes, faults
- [ ] Reports + export (inventory, utilization, available ports, faults)
- [ ] Global search across entity types

## Stage 5 — Airport pilot (PRD Stage 6)

- [ ] Survey one technical room at FIA with real data
- [ ] Validate workflows with FIA IT staff
- [ ] Correct issues before wider rollout

## Stage 6 — Discovery & intelligence (Blueprint Phases 3–7, 13 · PRD Stage 7)

Deferred by design — architecture must allow, MVP must not build:

- [ ] Discovery job manager + collector (read-only, scoped, approved targets)
- [ ] SNMPv3 single-device discovery + vendor adapters
- [ ] Dynamic interface registration with provenance
- [ ] Reconciliation (stable identity, change/conflict detection)
- [ ] LLDP/CDP neighbor topology + topology UI (React Flow)
- [ ] Passive infrastructure capture, floor views (Phases 8–10)
- [ ] Reports/completeness (Phase 12), assistive intelligence (Phase 13)
- [ ] Installer, upgrades, hardening (Phase 14 / PRD production)

## Known issues / open questions

- Local dev machine has no Docker/PostgreSQL installed — see README
  "Local development without Docker" for the fallback used during bootstrap.
- Job queue backend undecided (BackgroundTasks until discovery lands).
- Notification system (PRD §16) has no design yet; will ride on audit/events.
