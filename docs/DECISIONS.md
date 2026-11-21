# AeroLink — Architecture Decisions

Working record of decisions made while reconciling the project documents
(`README.txt`, `Sketch.txt`, `AeroLink_Project_Blueprint_v1.pdf`, `AeroLink.pdf`).

Source documents are the PRD (AeroLink.pdf) and the consolidated Blueprint.
Where they conflict, the decision below applies.

---

## D1 — Visual identity: Blueprint palette (with blue as secondary)

**Status:** Accepted · 2026-11-21

The Blueprint's exact tokens are the design system base:

| Token | Value | Use |
|---|---|---|
| `background` | `#F6F5F1` | App background (off-white) |
| `surface` | `#FFFFFF` | Content surfaces |
| `surface-secondary` | `#ECEDE7` | Secondary surfaces |
| `accent-subtle` | `#E5EBE4` | Subtle accent fills |
| `foreground` | `#252923` | Primary text (dark charcoal) |
| `muted` | `#777A73` | Secondary text |
| `forest` | `#526B58` | Primary brand/action color |
| `border` | `#E6E5DF` | Neutral borders |
| `success` | `#487C5A` | Healthy / verified |
| `warning` | `#C48B3A` | Warnings |
| `critical` | `#C6534B` | Faults / critical |

README's "restrained blue accent" is retained only as an **interactive/link
accent** (`--color-link`), never as the primary brand color. The product
identity is forest-on-off-white.

Rationale: Blueprint tokens are deliberate, complete, and match the
"calm, professional airport engineering tool" direction. README described a
mood; Blueprint specified values.

## D2 — Stack finalized as README states

**Status:** Accepted · 2026-11-21

| Layer | Choice |
|---|---|
| Frontend | Next.js (App Router) + TypeScript + Tailwind CSS |
| UI | shadcn/ui primitives + Lucide icons + React Hook Form + Zod |
| Visualization | React Flow (topology), Recharts (reports) as needed |
| Backend | Python 3.12+ + FastAPI + Pydantic |
| ORM / migrations | SQLAlchemy 2.x + Alembic |
| Database | PostgreSQL 16+ |
| Auth | Server-side sessions (httpOnly cookie) + argon2 password hashing |
| Background jobs | FastAPI BackgroundTasks now; dedicated worker/queue later if needed |
| Local dev | Docker Compose (frontend, backend, postgres) |

Rationale: the Blueprint appendix marked these "pending finalization" but
listed FastAPI/PostgreSQL/Docker as the leading (and only) candidates. README
treats them as decided. No competing options exist in the source documents.

Deferred (decide when discovery work starts): SNMP/SSH libraries, job queue
backend (e.g. arq/RQ/Celery), test tooling beyond pytest.

## D3 — Navigation: 10 top-level modules

**Status:** Accepted · 2026-11-21

Sidebar top level (from Blueprint §07), README detail modules mapped inside:

| Top-level nav | Contains (from README module list) |
|---|---|
| Overview | Dashboard |
| Locations | Buildings, floors, areas, rooms, technical rooms |
| Infrastructure | Equipment, Switches & Ports, Patch Panels, Cables, Fiber, Endpoints, Connections |
| Network Discovery | (Phase 3+; hidden until enabled) |
| Topology | Connection tracing, infrastructure map |
| Racks & Cabinets | Rack inventory, elevation, U-position management |
| Cabling & Fiber | Cable registry, fiber cores, ODF (shortcut view into Infrastructure) |
| Operations | Work Orders, Maintenance |
| Reports | Inventory, utilization, fault and work-order reports |
| Settings | Users, roles, permissions, naming standards, audit log |

Rationale: satisfies both documents — README's modules all exist as pages;
Blueprint's nav stays ~10 entries. "Cabling & Fiber" is a curated view; the
authoritative records live under Infrastructure to avoid duplicate CRUD.

## D4 — MVP scope order

**Status:** Accepted · 2026-11-21

Follow README §16 / Blueprint Phase 0–2 first:

1. Foundation (repo, frontend, backend, DB, Docker, auth, RBAC, design system, shell)
2. Dashboard connected to real backend data
3. Locations → Racks → Equipment → Switches (+ auto port generation)
   → Port grid → Patch panels
4. Then: cables, endpoints, fiber, connections/tracing, work orders,
   maintenance, audit, QR, reports, map

Explicitly excluded from MVP (both documents agree): SNMP/LLDP discovery,
topology auto-discovery, digital twin/3D, config changes to devices,
intelligent patching, AI features.

## D5 — Data truthfulness rules

**Status:** Accepted · 2026-11-21

- Never fabricate infrastructure data; empty states are real empty states.
- Physical vs. logical connectivity are separate models.
- Port states are distinct dimensions: admin state, operational state,
  assignment state, inventory/verification state. "Down" ≠ "available".
- Connections reference actual records (FKs), never free text.
- Audit events are append-only for ordinary users.
- Discovery (future) records provenance: source, timestamp, confidence;
  manual entries are distinguishable from discovered values.

## D6 — Repository layout

**Status:** Accepted · 2026-11-21

Per README §11: `frontend/`, `backend/`, `infrastructure/`, `docs/`,
root `docker-compose.yml`, `.env.example`, `README.md`. No empty
"future-proof" folders.

## D7 — Visualization layer architecture

**Status:** Accepted · 2026-11-21

Full requirements: [VISUALIZATION.md](VISUALIZATION.md).

- **React Flow (`@xyflow/react`)** for topology graphs and connection
  tracing; **custom SVG + React** for switch panels, ports, patch panels,
  fiber/ODF and rack elevations; Lucide for icons; D3 optional for advanced
  layout only.
- Dedicated layer at `src/components/visualizations/<domain>/` — rendering,
  data fetching, interaction and validation separated; never inline diagram
  logic in dashboard pages.
- Every diagram derives from database records. Ports are DB entities with
  six visual states (available/occupied/reserved/faulty/disabled/unknown).
  Actions through diagrams are validated server-side, permission-checked,
  audited, and refresh the view.
- Visualization build sequence follows data availability: switch/port grid
  (Stage 1) → patch panel → rack elevation → fiber/ODF → topology →
  connection tracing (Stage 2+).
