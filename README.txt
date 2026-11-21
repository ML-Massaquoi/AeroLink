# MASTER BUILD PROMPT — AEROLINK
## Airport Network Infrastructure Management System

You are acting as a **Principal Software Architect, Senior Full-Stack Engineer, UI/UX Designer, Network Infrastructure Engineer, and Security Engineer** responsible for building AeroLink.

Your task is to build a production-minded, professional airport network infrastructure management platform for **Freetown International Airport (FIA)**.

You are not here merely to design screens, generate mockups, or produce a development plan. You are here to **actively develop the application, implement the functionality, connect the frontend to the backend, build the database, test your work, and continuously move the project toward a working product**.

---

# 1. PRODUCT CONTEXT

## Product name

AeroLink

## Product description

AeroLink is an Airport Network Infrastructure Management System designed to digitally document, organize, manage, trace, and monitor the physical and logical IT infrastructure of Freetown International Airport.

The system will eventually serve as the airport's digital infrastructure twin, providing IT personnel with a reliable, centralized view of network infrastructure across buildings, offices, technical rooms, cabinets, racks, switches, patch panels, ports, cables, fiber connections, endpoints, and network services.

The system must eliminate dependence on:

- Manual cable tracing.
- Outdated spreadsheets.
- Unreliable handwritten labels.
- Technicians' memory.
- Fragmented infrastructure records.
- Unstructured port assignments.
- Guesswork during network troubleshooting.

AeroLink must help IT staff answer questions such as:

- Where is this switch physically located?
- What is connected to this switch port?
- Where does this cable terminate?
- Which patch panel is involved?
- Which ports are free?
- Which ports are occupied, reserved, or faulty?
- Where does this fiber link terminate?
- Which endpoint depends on this connection?
- What infrastructure may be affected if this connection is changed?
- Who last modified this infrastructure?
- What is the documented physical path from an endpoint to a network switch?

AeroLink must become a trusted infrastructure source of truth.

---

# 2. PRODUCT PRINCIPLES

These principles are non-negotiable.

### 2.1 Accuracy over appearance
The system must manage real infrastructure records. Never invent physical connections, cable paths, switch configurations, endpoints, or infrastructure statistics.

### 2.2 Security first
Airport network infrastructure information is sensitive. Authentication, authorization, data protection, validation, and auditability must be built into the architecture.

### 2.3 Simplicity
The application must be intuitive enough for an IT technician to use while working in a technical room.

### 2.4 Professional design
The application must look like a mature enterprise infrastructure management product, not a generic admin dashboard or AI-generated template.

### 2.5 Real functionality
Buttons, forms, filters, tables, actions, search, navigation, and status changes must actually work.

### 2.6 Modular architecture
The system must be organized into maintainable modules. Future functionality must be added without unnecessarily rewriting existing features.

### 2.7 Data integrity
Invalid connections, duplicate allocations, nonexistent infrastructure relationships, and conflicting port assignments must be prevented.

### 2.8 Progressive development
Build a strong foundation first, then expand. Do not attempt to build every advanced feature simultaneously.

---

# 3. TECHNOLOGY STACK

Use the following technology stack unless an existing project contains a deliberate, functional implementation that should be preserved.

## Frontend

- Next.js
- TypeScript
- App Router
- Tailwind CSS
- Reusable component architecture
- Responsive layouts
- Modern accessible UI patterns
- Lucide icons
- Server and client components appropriately
- React Hook Form for complex forms where appropriate
- Zod for client-side validation

## Backend

- Python
- FastAPI
- REST API
- Pydantic
- SQLAlchemy
- Alembic database migrations
- Modular service architecture

## Database

- PostgreSQL

## Infrastructure

- Docker
- Docker Compose
- Environment-based configuration
- Health checks
- Persistent database volumes

## Future integrations

Architecture should allow future integration with:

- SNMP
- LLDP
- Managed switch APIs
- MAC address tables
- Network monitoring
- Network device discovery

Do not implement risky network scanning or network configuration modifications during the initial development phase.

---

# 4. DESIGN DIRECTION

The visual experience is extremely important.

AeroLink must feel like a premium enterprise infrastructure product designed for aviation, network operations, and critical infrastructure management.

## Visual identity

- Light interface.
- Off-white background.
- White content surfaces.
- Neutral grey borders.
- Dark charcoal typography.
- Restrained blue accent colors.
- Subtle green for healthy or verified states.
- Amber for warnings.
- Red for faults and critical conditions.
- Generous spacing.
- Refined typography.
- Clean and consistent alignment.
- Minimal shadows.
- Subtle transitions.
- High-quality data visualization.

Avoid:

- Generic AI dashboard layouts.
- Excessive gradient backgrounds.
- Neon colors.
- Unnecessary glassmorphism.
- Oversized cards.
- Too many KPI cards.
- Excessive rounded corners.
- Cluttered interfaces.
- Decorative charts that communicate nothing.
- Dark dashboards as the default theme.
- Unnecessary animations.
- Excessive nested containers.
- Making everything look like a card.

## Design philosophy

The product should feel like a combination of:

- Modern enterprise software.
- Network infrastructure management.
- Airport operations technology.
- Professional engineering tools.

It must be visually calm, precise, structured, and information-dense without being overwhelming.

## Frontend requirement

Use **Next.js with TypeScript**. Do not replace it with Vite or standalone React.

The frontend must have a coherent design system with reusable components, consistent typography, spacing, colors, statuses, buttons, forms, tables, drawers, modals, and navigation.

---

# 5. APPLICATION STRUCTURE

Create a well-organized application with the following primary modules.

## Main navigation

### Overview
Operational infrastructure dashboard.

### Infrastructure Map
Airport infrastructure navigation and graphical infrastructure representation.

### Locations
- Buildings
- Floors
- Areas
- Rooms
- Technical rooms

### Racks & Cabinets
- Rack inventory
- Rack elevation
- Rack equipment
- U-position management

### Network Devices
- Network equipment inventory
- Routers
- Switches
- Firewalls
- Network hardware

### Switches & Ports
- Switch inventory
- Port grid
- Port status
- Port assignments
- Port history

### Patch Panels
- Patch panel inventory
- Patch panel port management
- Patch panel connections

### Cables
- Copper cable management
- Cable identifiers
- Terminations
- Cable paths
- Cable status

### Fiber
- Fiber cable inventory
- Fiber cores
- ODF management
- Splices
- Fiber connections

### Endpoints
- Computers
- CCTV cameras
- Access points
- IP phones
- Printers
- Kiosks
- Passenger information displays
- Servers
- Other connected devices

### Connections
- Physical connections
- Connection tracing
- Connectivity relationships
- Connection verification

### Work Orders
- New installations
- Moves
- Repairs
- Disconnections
- Troubleshooting
- Infrastructure modifications

### Maintenance
- Fault records
- Maintenance history
- Repairs
- Preventive maintenance

### Reports
- Infrastructure inventory
- Port utilization
- Cable utilization
- Available ports
- Fault reports
- Work order reports
- Maintenance reports

### Audit Log
- Infrastructure changes
- User activity
- Connection modifications
- Administrative actions

### Settings
- Users
- Roles
- Permissions
- Application settings
- Infrastructure naming standards

Organize the navigation thoughtfully. Do not simply place every module into a long unstructured sidebar.

---

# 6. INFRASTRUCTURE HIERARCHY

The data model and UI must support the following hierarchy:

Airport Campus
→ Buildings
→ Floors / Areas
→ Rooms / Technical Rooms
→ Racks / Cabinets
→ Equipment
→ Switches / Patch Panels / ODF
→ Ports / Fiber Cores
→ Cables / Connections
→ Endpoints / Services

Users must be able to navigate between these levels naturally.

For example:

Airport
→ Main Terminal
→ Ground Floor
→ Telecom Room 01
→ Rack A
→ Switch SW-01
→ Port 24
→ Connected Cable
→ Patch Panel
→ Office Outlet
→ Immigration Workstation

Infrastructure relationships must be based on actual database records, not hardcoded visual representations.

---

# 7. MVP FEATURES TO BUILD

Focus on these core modules first.

## Module A — Authentication & Authorization

Implement:

- Login.
- Logout.
- Secure session handling.
- User management.
- Role management.
- Permission management.
- Protected routes.
- Backend authorization.
- Password security.
- Authentication error handling.

Roles:

- System Administrator.
- IT Manager.
- Network Administrator.
- IT Technician.
- Read-only / Auditor.

Permissions must be enforced by the backend, not only by hiding frontend controls.

---

## Module B — Infrastructure Locations

Implement:

- Buildings.
- Floors.
- Areas.
- Rooms.
- Technical rooms.

Users must be able to:

- Create locations.
- Edit locations.
- View location details.
- Archive locations.
- Search locations.
- Navigate parent/child relationships.
- View infrastructure contained within a location.

Each location must have a unique identifier.

---

## Module C — Rack & Cabinet Management

Implement:

- Rack inventory.
- Rack dimensions.
- Rack height in U.
- Rack location.
- Rack status.
- Equipment placement.
- Rack elevation visualization.

Users must be able to:

- Create racks.
- Assign racks to technical rooms.
- Define rack height.
- Place equipment into U positions.
- View occupied positions.
- View available space.
- Move equipment.
- Prevent invalid or conflicting equipment placements.

Create a useful graphical rack elevation. Do not settle for a simple table if a visual rack representation can materially improve the experience.

---

## Module D — Equipment Inventory

Manage infrastructure equipment, including:

- Switches.
- Routers.
- Firewalls.
- Servers.
- Patch panels.
- ODFs.
- UPS units.
- Other network infrastructure.

Equipment records should support:

- Equipment ID.
- Name.
- Category.
- Manufacturer.
- Model.
- Serial number.
- Asset tag.
- Management IP where applicable.
- MAC address where applicable.
- Location.
- Rack.
- Rack position.
- Status.
- Installation date.
- Warranty information if available.
- Notes.
- Maintenance history.

---

## Module E — Switch Management

Implement switch registration and management.

Switch information:

- Switch ID.
- Hostname.
- Manufacturer.
- Model.
- Serial number.
- Management IP.
- MAC address.
- Location.
- Rack.
- Rack position.
- Role.
- Firmware version.
- Number of physical ports.
- Status.
- Notes.

Switch roles:

- Access.
- Distribution.
- Core.
- CCTV.
- Wireless.
- Security.
- Other.

When a switch is created, the system must generate its port records based on its configured port capacity.

For example:

A 48-port switch must automatically create Port 1 through Port 48.

Do not manually create each port individually.

---

## Module F — Port Management

This is one of the most important features.

Implement an interactive port visualization for switches.

Each port must have a status:

- Available.
- Occupied.
- Reserved.
- Faulty.
- Disabled.
- Unknown.

The port grid must be visually understandable and responsive.

Users should be able to:

- Inspect all switch ports.
- Click a port.
- View port details.
- Assign a connection.
- Reserve a port.
- Release a port.
- Mark a port faulty.
- Disable a port where appropriate.
- Update descriptions.
- View connection details.
- View port history.

Port details should include:

- Switch.
- Port number.
- Port label.
- Speed.
- VLAN.
- Administrative status.
- Operational status, if known.
- Connected cable.
- Patch panel.
- Connected endpoint.
- MAC address.
- IP address, if documented.
- Description.
- Last verification.
- History.

Prevent conflicting active assignments.

Port allocation and release operations must use backend validation and database transactions.

---

## Module G — Patch Panel Management

Implement:

- Patch panel inventory.
- Patch panel identification.
- Rack assignment.
- Rack position.
- Port capacity.
- Individual port records.
- Port status.
- Cable mapping.
- Switch connection mapping.
- Endpoint connection mapping.

Users must be able to inspect a patch panel visually and select individual ports.

---

## Module H — Cable Management

Implement a cable registry.

Cable information:

- Cable ID.
- Cable type.
- Category.
- Label.
- Origin.
- Destination.
- Length.
- Route.
- Installation date.
- Technician.
- Status.
- Notes.
- Verification status.

Cable types should include:

- Ethernet copper.
- Fiber optic.
- Coaxial.
- Other.

Cable statuses:

- Active.
- Spare.
- Reserved.
- Faulty.
- Disconnected.
- Retired.

Users must be able to:

- Register cables.
- Search cables.
- View cable details.
- Record cable terminations.
- Link cables to infrastructure.
- Record cable routes.
- Verify connections.
- Track maintenance.
- Generate identifiers.
- Generate QR codes.
- Print labels.

---

## Module I — Fiber Management

Implement fiber infrastructure records.

Support:

- Fiber cable.
- Fiber count.
- Individual fiber cores.
- Fiber ID.
- Fiber type.
- Origin.
- Destination.
- Route.
- ODF.
- ODF ports.
- Splice points.
- Status.
- Verification.
- Testing records where available.

Users must be able to trace documented fiber connections.

Do not assume a fiber core is active or connected unless the data confirms it.

---

## Module J — Endpoint Management

Implement endpoint inventory.

Endpoint types:

- Desktop.
- Laptop.
- CCTV camera.
- Wireless access point.
- IP phone.
- Printer.
- Passenger information display.
- Server.
- Kiosk.
- Access control equipment.
- Network terminal.
- Other.

Endpoint details:

- Endpoint ID.
- Name.
- Type.
- Manufacturer.
- Model.
- Serial number.
- MAC address.
- IP address.
- Department.
- Location.
- Responsible party.
- Connected switch.
- Switch port.
- Patch panel.
- Patch panel port.
- Cable.
- VLAN.
- Status.
- Last verified.
- Notes.

Endpoint records must support searching by name, ID, IP, MAC, location, type, and department.

---

## Module K — Connection Tracing

Implement a connection tracing engine.

Users must be able to trace:

Endpoint
→ Outlet
→ Cable
→ Patch Panel
→ Patch Panel Port
→ Cable
→ Switch
→ Switch Port

The system must also support tracing in reverse.

The trace page must show:

- Every known path component.
- Connection direction.
- Component locations.
- Cable IDs.
- Port identifiers.
- Switch names.
- Endpoints.
- VLAN and IP information where documented.
- Verification status.
- Missing or incomplete links.

The trace must be generated from real persisted relationships.

If the path is incomplete, display where it ends and why.

Never fabricate missing connection information.

---

## Module L — Work Orders

Implement work order management.

Work order categories:

- New connection.
- Device installation.
- Port allocation.
- Cable installation.
- Cable replacement.
- Network relocation.
- Infrastructure modification.
- Fault investigation.
- Preventive maintenance.
- Disconnection.
- Decommissioning.

Statuses:

- Requested.
- Assigned.
- In Progress.
- Completed.
- Verified.
- Closed.
- Cancelled.

Priorities:

- Low.
- Normal.
- High.
- Critical.

Work orders should support:

- Reference number.
- Title.
- Description.
- Category.
- Priority.
- Related infrastructure.
- Requester.
- Assigned technician.
- Dates.
- Status.
- Attachments.
- Resolution.
- Verification.
- Audit history.

---

## Module M — Maintenance

Implement:

- Fault registration.
- Maintenance records.
- Repairs.
- Equipment inspections.
- Port repairs.
- Cable repairs.
- Fiber repairs.
- Preventive maintenance.
- Maintenance history.

Every maintenance record must be linked to the relevant infrastructure where possible.

---

## Module N — Audit & Change Management

Record important infrastructure modifications.

Audit events must include:

- User.
- Action.
- Entity.
- Entity ID.
- Previous state.
- New state.
- Timestamp.
- Reason.
- Related work order.

Ordinary users must not be able to alter or delete historical audit records.

---

## Module O — QR Identification

Implement QR code generation for:

- Racks.
- Cabinets.
- Switches.
- Patch panels.
- Cables.
- Technical rooms.
- Other infrastructure.

QR codes must reference unique identifiers and open the corresponding authenticated AeroLink record.

QR codes must not expose sensitive infrastructure details.

---

## Module P — Search

Build a useful global search experience.

Search by:

- Asset ID.
- Switch name.
- Management IP.
- Port.
- Cable ID.
- MAC address.
- IP address.
- Endpoint name.
- Serial number.
- Rack.
- Patch panel.
- Location.
- Fiber ID.

Search results must display:

- Entity type.
- Name or identifier.
- Location.
- Status.
- Relevant connection information.

---

# 8. DASHBOARD

Build a clean, professional, informative infrastructure dashboard.

Do not overload it with unnecessary cards.

Prioritize the following:

### KPIs

- Total infrastructure assets.
- Total switches.
- Total patch panels.
- Total ports.
- Occupied ports.
- Available ports.
- Reserved ports.
- Faulty ports.
- Documented cables.
- Fiber infrastructure.
- Endpoints.
- Open work orders.

### Dashboard content

- Infrastructure summary.
- Port utilization.
- Infrastructure by building.
- Recent infrastructure changes.
- Open and critical work orders.
- Faults.
- Infrastructure verification progress.
- Recently added assets.
- Quick actions.

Use meaningful visualizations where they improve comprehension.

The dashboard must be connected to real backend data.

If the database is empty, display a genuine empty state with an explanation and appropriate actions. Never insert fake statistics to make the dashboard appear populated.

---

# 9. DATABASE & DATA INTEGRITY

Build a proper relational database.

Expected initial entities include:

- Users.
- Roles.
- Permissions.
- Buildings.
- Floors.
- Areas.
- Rooms.
- Racks.
- Rack positions.
- Equipment.
- Switches.
- Switch ports.
- Patch panels.
- Patch panel ports.
- Cables.
- Fiber cables.
- Fiber cores.
- ODFs.
- Endpoints.
- Outlets.
- Connections.
- VLANs.
- Work orders.
- Maintenance records.
- Audit logs.
- Attachments.
- Discovery jobs.
- Discovery results.

Use:

- Primary keys.
- Foreign keys.
- Unique constraints.
- Indexes.
- Validation.
- Transactions.
- Migrations.

Avoid overly generic schemas that make infrastructure relationships difficult to enforce.

Connections must be modeled explicitly.

Physical connectivity and logical network relationships must be separate concepts, while still allowing them to be related.

Do not create an unnecessarily complicated database. Build a strong, understandable foundation that can scale.

---

# 10. SECURITY REQUIREMENTS

Treat AeroLink as a sensitive airport IT system.

Implement:

- Secure authentication.
- Secure password hashing.
- Server-side RBAC.
- Protected API endpoints.
- Input validation.
- SQL injection prevention.
- XSS protection.
- Secure session handling.
- Rate limiting where appropriate.
- Safe error handling.
- Audit logging.
- Environment-based secrets.
- HTTPS-ready deployment.
- Database backups.
- Secure configuration.
- Least-privilege principles.

Never:

- Hardcode passwords.
- Commit secrets.
- Expose database credentials.
- Expose network credentials in UI.
- Return sensitive information unnecessarily.
- Trust frontend authorization.
- Allow unvalidated infrastructure changes.
- Perform unauthorized network scanning.
- Automatically modify network devices during the MVP.

---

# 11. PROJECT STRUCTURE

Maintain a clean, modular structure.

A recommended starting structure:

aerolink/
├── frontend/
│   ├── app/
│   ├── components/
│   │   ├── ui/
│   │   ├── layout/
│   │   ├── infrastructure/
│   │   ├── network/
│   │   └── shared/
│   ├── features/
│   │   ├── dashboard/
│   │   ├── locations/
│   │   ├── racks/
│   │   ├── equipment/
│   │   ├── switches/
│   │   ├── ports/
│   │   ├── patch-panels/
│   │   ├── cables/
│   │   ├── fiber/
│   │   ├── endpoints/
│   │   ├── connections/
│   │   ├── work-orders/
│   │   └── reports/
│   ├── lib/
│   ├── hooks/
│   ├── types/
│   └── styles/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── repositories/
│   │   ├── integrations/
│   │   ├── tasks/
│   │   └── utils/
│   ├── migrations/
│   └── tests/
│
├── infrastructure/
│   ├── docker/
│   └── scripts/
│
├── docs/
│
├── docker-compose.yml
├── .env.example
└── README.md

You may adapt the structure to the project, but maintain separation of concerns and modularity.

Do not create unnecessary folders simply to make the structure look sophisticated.

---

# 12. DEVELOPMENT WORKFLOW

You must follow this workflow.

## STEP 1 — INSPECT THE PROJECT

Before writing code:

- Inspect the repository.
- Identify the current framework.
- Inspect existing files.
- Identify existing components.
- Check installed dependencies.
- Check database configuration.
- Identify existing functionality.
- Identify broken functionality.
- Determine whether the project is empty or partially implemented.

Do not destroy existing working code.

Do not blindly replace existing project configuration.

If an existing architecture is already established, evaluate it and preserve good decisions.

## STEP 2 — ESTABLISH THE FOUNDATION

Build or verify:

- Frontend application.
- Backend application.
- Database connection.
- Docker environment.
- Environment configuration.
- Health endpoints.
- Database migrations.
- Authentication.
- Authorization.
- Base design system.
- Application layout.
- Navigation.
- Logging.

Ensure both frontend and backend can start successfully.

## STEP 3 — BUILD THE PRODUCT IN MODULES

Develop in this order:

1. Foundation and authentication.
2. Dashboard shell and design system.
3. Locations.
4. Racks and cabinets.
5. Equipment inventory.
6. Switch management.
7. Port management.
8. Patch panels.
9. Cables.
10. Endpoints.
11. Fiber.
12. Connections and tracing.
13. Work orders.
14. Maintenance.
15. Audit.
16. QR codes.
17. Reporting.
18. Infrastructure map.

Dependencies may justify adjustments to this order.

## STEP 4 — IMPLEMENT FULL FUNCTIONALITY

Every module must include the necessary:

- Backend models.
- Database migrations.
- API endpoints.
- Business logic.
- Validation.
- Frontend pages.
- Forms.
- Loading states.
- Error states.
- Empty states.
- Search.
- Filters.
- Pagination where needed.
- Permissions.
- Audit logging.

Do not create frontend-only features.

Do not leave buttons that do nothing.

Do not simulate successful API calls.

Do not use hardcoded records to imitate a connected backend.

## STEP 5 — VERIFY YOUR WORK

After every meaningful implementation:

- Run the frontend.
- Run the backend.
- Run migrations.
- Check for errors.
- Run linting.
- Run type checking.
- Run tests.
- Test API endpoints.
- Verify frontend/backend integration.
- Fix problems before proceeding.

Do not knowingly leave broken functionality behind.

---

# 13. DEVELOPMENT RULES FOR AI AGENTS

If you have access to terminal, filesystem, code execution, browser, testing, or subagents, use them appropriately.

You are expected to actively work.

### Do not:

- Stop after writing a plan.
- Give me instructions to do the coding myself.
- Generate only a landing page.
- Build a static dashboard.
- Create fake API responses.
- Use fake production data.
- Leave core functions as TODOs.
- Leave buttons without actions.
- Ignore backend development.
- Ignore database migrations.
- Ignore authentication.
- Ignore security.
- Create unnecessary complexity.
- Rewrite the entire codebase without justification.
- Ask me to approve every small technical decision.

### Do:

- Make reasonable engineering decisions independently.
- Inspect the existing project first.
- Build in manageable increments.
- Keep the application running.
- Maintain documentation.
- Test the work.
- Fix issues you discover.
- Explain decisions briefly when they matter.
- Continue implementing the next logical task without waiting for me after every step.

If a requirement cannot be implemented because of a real external dependency, clearly identify the limitation and continue with everything else that can be implemented.

---

# 14. TESTING REQUIREMENTS

Build tests for critical business logic.

Priority tests:

- Authentication.
- Permissions.
- Location hierarchy.
- Rack capacity.
- Equipment placement conflicts.
- Switch port creation.
- Port allocation.
- Port release.
- Duplicate port assignments.
- Cable termination validation.
- Connection integrity.
- Connection tracing.
- Work order lifecycle.
- Audit event creation.

Port allocation must be concurrency-safe.

Infrastructure deletion must be handled carefully. Use archival or decommissioning workflows when historical relationships must be preserved.

---

# 15. DOCUMENTATION

Create and maintain:

### README.md
- Project overview.
- Features.
- Technology stack.
- Setup instructions.
- Development instructions.
- Environment configuration.
- Startup commands.

### docs/ARCHITECTURE.md
- System architecture.
- Frontend/backend responsibilities.
- Database architecture.
- Module boundaries.
- API design.
- Integration architecture.

### docs/DATABASE.md
- Entity definitions.
- Relationships.
- Constraints.
- Connection model.

### docs/SECURITY.md
- Authentication.
- Authorization.
- Security controls.
- Secrets management.
- Deployment considerations.

### docs/ROADMAP.md
- Implemented features.
- Current stage.
- Remaining features.
- Known issues.
- Next development priorities.

Keep documentation aligned with the actual implementation.

---

# 16. INITIAL IMPLEMENTATION TARGET

Your first development milestone is:

## AeroLink Foundation + Core Infrastructure Registry

Complete the following before moving into advanced features:

### Foundation

- [ ] Repository inspected.
- [ ] Architecture established.
- [ ] Next.js frontend operational.
- [ ] FastAPI backend operational.
- [ ] PostgreSQL connected.
- [ ] Docker setup working.
- [ ] Environment configuration.
- [ ] Health checks.
- [ ] Database migrations.
- [ ] Authentication.
- [ ] RBAC.
- [ ] Base design system.
- [ ] Responsive application layout.

### Initial functional modules

- [ ] Dashboard connected to backend.
- [ ] Buildings.
- [ ] Floors / areas.
- [ ] Rooms / technical rooms.
- [ ] Racks.
- [ ] Equipment.
- [ ] Switch inventory.
- [ ] Automatic switch port generation.
- [ ] Switch port visualization.
- [ ] Port status management.
- [ ] Patch panel inventory.

### Quality

- [ ] API validation.
- [ ] Database constraints.
- [ ] Error handling.
- [ ] Loading states.
- [ ] Empty states.
- [ ] Responsive layout.
- [ ] Tests.
- [ ] Documentation.
- [ ] No fabricated production data.

---

# 17. UI IMPLEMENTATION EXPECTATIONS

The first interface must establish the final AeroLink design language.

Build:

## Application shell

- Refined sidebar.
- AeroLink branding.
- Logical navigation.
- Breadcrumbs.
- Top bar.
- Global search.
- Notifications area if appropriate.
- User profile menu.
- Responsive sidebar.

## Dashboard

A clean overview with:

- Infrastructure summary.
- Port utilization.
- Infrastructure health.
- Open work orders.
- Recent changes.
- Building overview.
- Quick actions.

## Infrastructure pages

Use consistent patterns for:

- Page headers.
- Titles.
- Descriptions.
- Action buttons.
- Search.
- Filter bars.
- Tables.
- Detail panels.
- Drawers.
- Forms.
- Empty states.

## Switch detail page

Must contain:

- Switch identity.
- Status.
- Location.
- Management IP.
- Model.
- Port capacity.
- Port utilization.
- Visual port grid.
- Port filtering.
- Port details.
- Connected device information.
- Connection trace entry point.
- History.

The port visualization must be one of the strongest UX elements of AeroLink.

---

# 18. FUTURE DEVELOPMENT — DO NOT BUILD PREMATURELY

Design the architecture so these can be introduced later:

## Automated Network Discovery

- SNMP.
- LLDP.
- MAC address discovery.
- Switch interface discovery.
- VLAN discovery.
- Device discovery.

## Monitoring

- Port status.
- Traffic statistics.
- Errors.
- Device availability.
- Alerts.

## Digital Infrastructure Twin

- Airport map.
- Building navigation.
- Floor plans.
- Technical room visualization.
- Rack visualization.
- Network topology.
- Connection visualization.
- Infrastructure dependency mapping.

## Intelligent Infrastructure

Potential future integration with intelligent patch panels or hardware capable of detecting physical patch changes.

These future features must not compromise the reliability of the core infrastructure registry.

---

# 19. DEFINITION OF DONE

A feature is not considered complete merely because its UI exists.

A feature is complete only when:

1. Its interface is implemented.
2. Its backend logic exists.
3. Its database schema is correct.
4. Its API is functional.
5. Validation is implemented.
6. Authorization is enforced.
7. Errors are handled.
8. Loading states exist.
9. Empty states exist.
10. Data is persisted.
11. Frontend and backend are connected.
12. Critical tests pass.
13. The feature has been verified.
14. Documentation is updated where necessary.

---

# 20. YOUR FIRST TASK — START NOW

Do not respond with another architecture proposal.

Do not simply restate this prompt.

Do not stop at planning.

Begin by inspecting the project repository and identifying its current state.

Then:

1. Establish the project structure.
2. Confirm the frontend, backend, and database strategy.
3. Implement the application foundation.
4. Build the AeroLink design system and application shell.
5. Establish authentication and permissions.
6. Implement the first real infrastructure modules.
7. Connect them to the backend and database.
8. Test the implementation.
9. Fix errors.
10. Continue progressing through the MVP.

Maintain a brief development log showing:

- What has been implemented.
- Files or modules created.
- Decisions made.
- Tests performed.
- Problems discovered.
- Remaining tasks.

At the end of each work session, report:

**Completed**
What is genuinely implemented.

**Verified**
What has actually been tested and confirmed working.

**Outstanding**
What remains incomplete.

**Next**
The next task you will begin.

If you have sufficient execution time and tools, continue working beyond the first milestone instead of stopping prematurely.

---

# FINAL INSTRUCTION

Build AeroLink as if it will be used by real airport IT technicians to manage infrastructure that supports airport operations.

Prioritize engineering quality, security, data accuracy, maintainability, exceptional usability, and a professional interface.

I do not want a template.

I do not want a static dashboard.

I do not want a demo full of fake data.

I want a properly engineered, functional, extensible Airport Network Infrastructure Management System.

**Inspect the repository and start building AeroLink now.**
