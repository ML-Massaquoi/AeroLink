# AeroLink

**Airport Network Infrastructure Management System** — a digital source of
truth for Freetown International Airport's (FIA) physical and logical IT
infrastructure: locations, racks, switches, ports, patch panels, cables,
fiber, endpoints, and the connections between them.

See [docs/DECISIONS.md](docs/DECISIONS.md) for architecture decisions and
[docs/ROADMAP.md](docs/ROADMAP.md) for current status.

## Technology stack

| Layer | Choice |
|---|---|
| Frontend | Next.js (App Router), TypeScript, Tailwind CSS, shadcn/ui, Lucide |
| Backend | Python, FastAPI, Pydantic, SQLAlchemy 2, Alembic |
| Database | PostgreSQL 16+ |
| Infra | Docker Compose, environment-based config, health checks |

## Repository layout

```
aerolink/
├── frontend/           Next.js application
├── backend/            FastAPI application + Alembic migrations
├── infrastructure/     Docker files and helper scripts
├── docs/               Architecture, decisions, roadmap
├── docker-compose.yml  Local/pilot stack
└── .env.example        Documented environment variables
```

## Quick start (Docker)

```bash
cp .env.example .env        # edit secrets for your environment
docker compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000 (docs at `/docs`)
- Postgres: localhost:5432 (persistent volume)

On first boot the backend runs migrations and seeds the default roles and
the initial administrator from `SEED_ADMIN_EMAIL` / `SEED_ADMIN_PASSWORD`.

## Local development without Docker

Requires Python 3.12+, Node 20+, and a reachable PostgreSQL 16+
(set `DATABASE_URL` accordingly).

```bash
# backend
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload

# frontend
cd frontend
npm install
npm run dev
```

## Environment configuration

All configuration is environment-based; see [.env.example](.env.example).
Never commit real secrets.

## Testing & quality

```bash
# backend
cd backend && pytest

# frontend
cd frontend && npm run lint && npm run typecheck && npm test
```

## Design

Light interface, off-white background, forest-green primary accent, neutral
borders, restrained status colors (green/amber/red). Calm, precise,
information-dense. No fabricated data — empty states are real empty states.

## Security

Server-side RBAC (UI hiding is not authorization), hashed passwords,
httpOnly session cookies, input validation via Pydantic/Zod, audit logging
for infrastructure changes, secrets only via environment. See
[docs/SECURITY.md](docs/SECURITY.md).
