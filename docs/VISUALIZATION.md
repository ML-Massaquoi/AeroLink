# AeroLink — Visualization Engineering Requirements

Authoritative spec for all interactive infrastructure visualizations.
Adopted 2026-11-21. Applies from Stage 2 (registry) onward; foundation
stages must keep the architecture ready for it (see DECISIONS.md D7).

## Mandatory technologies

- **React Flow (`@xyflow/react`)** — interactive topology, device
  relationships, cable tracing, infrastructure graphs.
- **Custom SVG + React** — switch front panels, individual ports, patch
  panels, fiber/ODF panels, rack elevations, physical infrastructure.
- **Lucide React** — consistent interface icons.
- **D3.js (optional)** — advanced graph layout for large topologies only
  when React Flow layout is insufficient.

Forbidden: static images, placeholder illustrations, generic cards as
substitutes for real diagrams; hardcoded port counts or states; fabricated
links; fake topology data in production. Empty infrastructure shows a
professional empty state, never a fake diagram.

## 1. Switch visualization

Reusable interactive components rendering the actual registered switch model
and port configuration from backend records.

- Configurable port counts (8/16/24/48 and others).
- Copper RJ45 ports; SFP/SFP+ and fiber uplink ports.
- Port numbering matching physical numbering.
- Port status visualization; clickable; hover info; selection/inspection.
- Connection info, VLAN/interface info when documented.
- Fault and reservation states; port history.

## 2. Interactive port management

Every port is a database-backed entity. Visual states must distinguish:
**Available, Occupied, Reserved, Faulty, Disabled, Unknown**.

Selecting a port opens a detail inspector: connected cable, endpoint, patch
panel, VLAN, configuration, status, history, permitted actions. Actions must
update the backend, respect permissions, validate connections, and generate
audit records.

## 3. Rack elevation (SVG/React)

- Rack units from actual rack capacity; equipment rendered by recorded
  U-height and position (multi-U devices included).
- Switches, patch panels, servers, UPS and other rack devices.
- Occupied vs. available space; equipment inspection.
- Overlap prevention (backend validation is authoritative).
- Reflects actual database state. No static rack photographs as UI.

## 4. Patch panel visualization (SVG/React)

Configurable port counts, accurate numbering, copper and fiber panel types,
port states, cable IDs, connected switch ports, connected outlets/endpoints,
port inspection, connection history.

## 5. Fiber / ODF visualization

ODF frames, fiber trays, fiber cables, individual cores/strands, termination
points, splices, fiber port assignments; states: available, occupied,
reserved, faulty, unknown. Connectivity from actual relationships only.

## 6. Interactive network topology (React Flow)

Meaningful nodes: core/distribution/access switches, routers, firewalls,
APs, servers, endpoints, patch panels where relevant. Edges = documented
relationships only.

Support: zoom, pan, node selection, detail panels, connection inspection,
search, filtering, grouping, connection highlighting, navigation to the
underlying record. Verified vs. unverified/discovered links must be visually
distinguished. Never fabricate links.

## 7. Connection tracing

Backend-powered path derivation, frontend visualization:

`Endpoint → Outlet → Cable → Patch Panel → Patch Panel Port → Cable → Switch → Switch Port → Uplink → Next Device`

Path comes from database relationships, never frontend guessing. Incomplete
paths clearly indicate where the trace stops and what is missing.

## 8. Visualization architecture

Dedicated visualization layer — no diagram logic inside dashboard pages:

```
src/components/visualizations/
├── network-topology/
├── switch/
├── switch-ports/
├── rack-elevation/
├── patch-panel/
├── fiber-odf/
└── connection-trace/
```

Separate rendering, data fetching, interaction handling, validation and
business logic. Components reusable across pages.

## 9. Data integrity

All diagrams generated from real database records. Any diagram-performed
action must: (1) validate server-side, (2) respect authorization,
(3) preserve DB integrity, (4) update records, (5) generate audit record,
(6) refresh the affected visualization.

## 10. Quality standard

Professional enterprise network-management behavior: no placeholder boxes,
decorative lines, generic device icons standing in for physical devices,
oversized ports, cluttered layouts or nonfunctional interactions.
Technically accurate, interactive, database-connected, clear, maintainable.
