# Project Research Summary

**Project:** Sistema Web de Registro Escolar — UNIVESP PJI110, Polo Valinhos
**Domain:** Brazilian K-12 school management web application (SIS)
**Researched:** 2026-04-26
**Confidence:** HIGH

## Executive Summary

This is a school information system (SIS) for a single Brazilian K-12 institution with three distinct user roles: admin, professor, and responsavel (parent/guardian). The canonical approach for this domain is a layered SPA + REST API architecture — React frontend talking to a FastAPI backend over JWT-authenticated HTTP, with SQLite as the data store. The Brazilian educational context imposes two non-negotiable domain requirements: grades structured by bimestre (4 per year) and frequency tracking against the LDB 25% absence ceiling. Every design decision should serve one of three core user journeys: admin configuring the institution, teachers recording daily attendance and grades, and parents reading their child's report card.

The recommended implementation path is FastAPI (Python 3.12, SQLAlchemy 2.0, Alembic, PyJWT) on the backend and React 18 + TypeScript + Vite + TanStack Query on the frontend. The stack is well-matched to a student team of 8: it is fully documented in the project's existing docs/ files, the library choices minimize footguns (PyJWT over the abandoned python-jose, Alembic over schema drift, React Query over raw useEffect), and the feature-per-module backend structure maps directly onto team member assignments. The architecture is already specified in detail in docs/api-architecture.md, docs/database-schema.md, and docs/frontend-architecture.md, which means the research phase is primarily validation rather than discovery.

The dominant risks are not technical complexity but execution risks: PostgreSQL trigger syntax in a SQLite database (business rules will silently not exist), RBAC checks that verify role but not resource ownership (IDOR vulnerability across student data), SQLite write locks under FastAPI's async threading, and scope creep from a real stakeholder. All four are preventable in Week 1 if the team sets up the infrastructure correctly before building features. The hard deadline of 24 May 2026 makes scope discipline non-negotiable.

## Key Findings

### Recommended Stack

The backend is FastAPI 0.136 with SQLAlchemy 2.0 (sync, not async, with WAL-mode SQLite), Alembic for migrations, PyJWT for JWT, and passlib[bcrypt] for password hashing. The uv package manager and Ruff linter are the recommended dev tooling for team velocity. The frontend is React 18 + TypeScript + Vite 5, with React Router 6 for routing, TanStack Query 5 for all server state, Axios for HTTP (with an interceptor-based auth header), React Hook Form + Zod for form validation, and Tailwind CSS 3 + shadcn/ui for UI components.

**Core technologies:**
- Python 3.12 + FastAPI 0.136: async REST framework with automatic OpenAPI docs, Pydantic v2 integration
- SQLAlchemy 2.0 (sync) + WAL mode SQLite: sync session is simpler and sufficient for one school; avoid aiosqlite
- Alembic 1.13 with render_as_batch=True: required for SQLite column migrations; never use create_all()
- PyJWT 2.x: JWT creation/validation — python-jose is abandoned and has an unpatched CVE
- React 18 + Vite 5 + TypeScript 5: stable, fast build tooling; avoid CRA (deprecated) and React 19 (too new)
- TanStack Query 5: eliminates race conditions and stale-data bugs endemic in student projects using raw useEffect
- Tailwind CSS 3: keep on v3; v4 breaks all existing patterns and shadcn/ui compatibility is not yet established

### Expected Features

The MVP (deadline 24/05/2026) is fully enumerated in FEATURES.md. The three user journeys map to clean feature groups with clear dependency ordering.

**Must have (table stakes) — v1 by 24/05/2026:**
- Authentication + JWT + role-based routing (root dependency for everything)
- Admin CRUD: usuarios, professores, responsaveis, alunos, turmas, disciplinas
- Admin: teacher-class-subject assignment (professor_turma junction) — commonly underscoped, causes access failures if skipped
- Teacher: attendance registration (chamada) — bulk mark present/absent per class session
- Teacher: assessment creation (avaliacoes) and grade entry (notas) by bimestre
- Teacher: correction of past attendance records
- Parent: boletim (report card with computed media per disciplina per bimestre)
- Parent: frequencia (attendance percentage per subject)
- Admin and teacher dashboards (simple counts/navigation, not analytics)

**Should have (competitive) — v1.x post-validation:**
- Passing/failing status indicator on boletim (requires school to confirm passing threshold)
- Absence alert when student exceeds LDB 25% limit (legal compliance for real deployment)
- PDF boletim export (needed for parent-teacher meetings)
- Password recovery via email

**Defer (v2+):**
- Email/WhatsApp notifications — high infra cost, defer until parent dashboard is validated
- Multi-year grade history, multi-school support, student login, mobile app

**Brazilian context requirements that affect schema and display (non-negotiable):**
- 4-bimestre grading cycle — all grade views must aggregate by bimestre
- LDB 25% absence rule — frequency percentage must be prominently displayed
- CPF as identity anchor for adults (already in schema)
- Turno (shift) on turmas must be visible to teachers to avoid attendance on the wrong shift

### Architecture Approach

The system is a standard layered monolith: React SPA communicates over HTTP with FastAPI, which applies JWT authentication middleware, routes requests through domain-specific modules (each with router, service, schemas, models), enforces ownership rules in the service layer, and persists data in a single SQLite file. Both backend and frontend are organized by domain feature rather than by file type, enabling parallel team development with minimal merge conflicts.

**Major components:**
1. React SPA (AuthContext + React Query + Role-based Router): handles all UI, token storage, and API state caching
2. FastAPI Auth Middleware + Domain Routers: validates JWT on every protected request, routes to the correct module
3. Service Layer (ownership checks + business rules): the single location where "does this user own this resource?" is enforced — must not be bypassed
4. SQLAlchemy ORM + SQLite (WAL mode, busy_timeout, foreign_keys ON): data persistence with write serialization protection

The build order is strict: Foundation (skeleton + DB migrations) → Authentication → Admin CRUD → Core academic operations (chamadas + notas) → Parent read-only views → Polish. No layer can be built before its dependencies exist.

### Critical Pitfalls

1. **PostgreSQL trigger syntax in SQLite schema** — The existing database-schema.md uses PL/pgSQL trigger syntax that is invalid in SQLite. If copied into migrations, business rules (nota exceeds max, aluno not in turma) will silently not exist. Rewrite all triggers in SQLite syntax (BEGIN...END), add PRAGMA foreign_keys = ON to every connection via SQLAlchemy event listener, and add unit tests that verify constraint enforcement before any feature work begins.

2. **RBAC bypass via missing ownership checks** — Checking "is the user a teacher?" at the route level is not enough. Any endpoint that takes a resource ID (chamada_id, aluno_id) must also verify the requesting user owns that resource. A parent who guesses another student's aluno_id gets their grades if the query does not filter by responsavel_id. Build a shared verify_aluno_access() utility and use it everywhere. Write explicit cross-user access tests.

3. **SQLite "database is locked" under FastAPI concurrency** — FastAPI's threadpool + SQLite's single-writer model produces lock errors under concurrent write requests. Prevention: configure PRAGMA journal_mode=WAL and PRAGMA busy_timeout=5000 via SQLAlchemy connect event. Use sync SQLAlchemy, not async (aiosqlite adds complexity without benefit at this scale).

4. **JWT stored in localStorage (XSS risk)** — Minimum mitigation for prototype: use sessionStorage (token disappears on tab close) and keep the 8-hour expiry. Never use dangerouslySetInnerHTML on user-supplied text fields. Add an Axios interceptor to catch 401 responses and redirect to /login automatically.

5. **CORS misconfiguration blocking integration** — Vite runs on localhost:5173, FastAPI on localhost:8000. Set CORSMiddleware explicitly with allow_origins=["http://localhost:5173"] as the first middleware on day one. Alternatively, configure a Vite proxy for /api to eliminate CORS in development entirely.

## Implications for Roadmap

Based on research, the build order is driven by strict feature dependencies (auth before everything, CRUD entities before transactions, transactions before parent read views) and a hard 24 May 2026 deadline that requires scope discipline. The architecture is already well-specified, so phases are execution-focused rather than discovery-focused.

### Phase 1: Foundation and Infrastructure

**Rationale:** Every feature depends on a working database schema, backend skeleton, and frontend scaffold. Pitfalls 1, 2, 3, and 5 (trigger syntax, RBAC pattern, SQLite concurrency, CORS) must all be prevented here, before any feature work begins. A reference endpoint (e.g., GET /alunos) should be built end-to-end in this phase so the whole team reviews the patterns before splitting work — this is the most effective prevention for inconsistent code patterns across 8 developers.
**Delivers:** Running FastAPI app with SQLite (WAL + FK pragma), Alembic migrations with correct SQLite trigger syntax, React + Vite project with Axios instance + AuthContext shell + CORS working, coding conventions document, one reference endpoint reviewed by the full team.
**Addresses:** Infrastructure prerequisites
**Avoids:** PostgreSQL trigger syntax bug, SQLite lock errors, CORS integration failures, inconsistent team patterns

### Phase 2: Authentication and Role-Based Access

**Rationale:** Authentication is the root dependency for all features. It must be complete and tested before any other module is built. The ownership-check pattern established here (service layer, not router) becomes the template for every subsequent module.
**Delivers:** POST /auth/login returning JWT, get_current_user dependency with role in payload, React Login page, AuthContext complete, PrivateRoute + RoleRoute guards, role-based redirect on login.
**Uses:** PyJWT 2.x, passlib[bcrypt], pydantic-settings, React Router 6 data router API
**Avoids:** RBAC bypass — ownership check template is established here as the team standard

### Phase 3: Admin CRUD — Entity Setup

**Rationale:** All core academic operations (attendance, grades) require foundational entities to exist first: turmas, disciplinas, alunos, professores, responsaveis, and the teacher-class-subject assignment. The professor_turma junction is commonly underscoped in student projects — it must be treated as a first-class deliverable in this phase.
**Delivers:** Full CRUD for usuarios, professores, responsaveis, alunos, turmas, disciplinas via admin portal. Teacher-class-subject assignment (professor_turma). Admin dashboard with entity totals.
**Implements:** Feature-based backend modules (router/service/schemas/models per domain), Admin page directory in frontend
**Avoids:** Missing professor_turma assignment causing access failures in Phase 4

### Phase 4: Core Academic Operations (Teacher Portal)

**Rationale:** With entities in place, the teacher's two primary workflows become buildable. These are the most complex modules due to ownership checks, bulk operations, and business rule enforcement (nota <= valor_maximo, student must belong to turma). Each service function must enforce ownership against the professor_turma table.
**Delivers:** Teacher dashboard (minhas turmas), chamada registration (bulk present/absent per class session), chamada history editing, avaliacao creation, notas entry per student per assessment. All with correct ownership enforcement in the service layer.
**Uses:** SQLAlchemy joinedload to avoid N+1 queries on student listings; batch insert for presencas in a single transaction
**Avoids:** RBAC bypass on chamadas/notas endpoints; N+1 query trap on student attendance listings

### Phase 5: Parent Read-Only Views

**Rationale:** The parent portal depends on Phase 4 data existing. It is read-only but requires non-trivial query logic: grouping notas by bimestre + disciplina and computing averages, and computing frequency percentage per disciplina. These queries must filter strictly by authenticated responsavel's filhos.
**Delivers:** Responsavel dashboard, filhos list, boletim (grades per bimestre with computed media), frequencia (attendance percentage per disciplina). All filtered by responsavel_id ownership.
**Implements:** GET /alunos/:id/notas and GET /alunos/:id/presencas with ownership guard, computed aggregation at query time grouped by bimestre (4 per year, per Brazilian standard)
**Avoids:** Parent able to query any student's data by guessing aluno_id

### Phase 6: Polish, Validation, and v1.x Differentiators

**Rationale:** Once core flows are functional, add value before submission: passing/failing indicators, the LDB 25% absence alert (legal compliance for real deployment), error and loading states throughout, and demo stability. PDF export and password recovery are v1.x additions if time permits. Scope guardian must enforce that anything not on this list goes to the v2 backlog.
**Delivers:** Passing/failing indicator on boletim, absence alert highlighting (>25% per LDB), error boundaries, loading states, friendly Portuguese error messages, Axios 401 interceptor redirect. Optionally: PDF export, absence justification UI in parent dashboard.
**Avoids:** Scope creep from stakeholder requests — all new requests go to v2 backlog

### Phase Ordering Rationale

- Auth before everything because it is the root dependency (confirmed by FEATURES.md dependency tree)
- CRUD entities before transactions because chamadas/notas reference turmas/alunos/disciplinas via foreign keys
- Teacher portal before parent portal because the parent reads data the teacher writes (data dependency)
- Infrastructure pitfall prevention in Phase 1 because it costs 10x less to set up correctly on day one than to diagnose and fix after data exists
- Differentiators in Phase 6 because they enhance a working core; building them early risks shipping polish with no core and missing the deadline

### Research Flags

Phases with well-documented patterns (skip research-phase):
- **Phase 1:** FastAPI + SQLite + Alembic setup is fully documented in official sources and in the project's existing docs/ files
- **Phase 2:** JWT auth with FastAPI is covered by official docs (updated to PyJWT in PR #11589); React Router protected routes are standard patterns
- **Phase 3:** Admin CRUD is straightforward with no novel patterns

Phases likely needing deeper planning attention before implementation:
- **Phase 4:** The chamada bulk-insert pattern (one chamada + N presencas in a single transaction) and the notas batch-update endpoint have performance and constraint implications worth designing explicitly before implementation begins
- **Phase 5:** The boletim aggregation query (JOIN notas + avaliacoes + disciplinas, GROUP BY bimestre) should be designed and tested against sample data before frontend work begins — the schema must be confirmed correct for the 4-bimestre grouping

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Official docs confirmed; FastAPI PR #11589 confirms PyJWT; version compatibility matrix verified against official release notes |
| Features | HIGH | Scope confirmed by team meeting notes; bimestre grading and LDB rules are statutory requirements, not opinions |
| Architecture | HIGH | Based directly on team-authored docs (api-architecture.md, database-schema.md, frontend-architecture.md) — not inferred from external sources |
| Pitfalls | HIGH | Critical pitfalls verified against official SQLite docs, FastAPI GitHub issues, and SQLAlchemy threading discussions |

**Overall confidence:** HIGH

### Gaps to Address

- **Passing threshold for boletim:** The school's passing grade (media >= 5.0 or 6.0?) is not confirmed in any document. The boletim can show computed averages without this, but the passing/failing indicator (v1.x) requires the school to confirm it. Assign one team member to ask professora Elizabete before Phase 6.
- **SMTP provider for password recovery:** The email provider for password recovery (v1.x) is unspecified. Confirm whether this is needed before submission or deferred to real deployment. If needed, a free SMTP service (e.g., Brevo free tier) should be selected during Phase 6 planning.
- **Business rule enforcement strategy:** Research recommends enforcing rules (nota <= valor_maximo, student belongs to turma) in the Python service layer rather than SQLite triggers. This must be an explicit team decision documented in Week 1 conventions so no developer accidentally relies on DB-level enforcement that does not exist.
- **Deployment environment for evaluation:** The project docs do not specify where the prototype will be hosted for the 24 May evaluation. If a public URL is needed (e.g., for professora Elizabete to test remotely), a deployment plan (Railway, Render, or local demo) must be confirmed before Phase 5 ends.

## Sources

### Primary (HIGH confidence)
- docs/api-architecture.md — endpoint definitions, JWT format, permission matrix (team-authored)
- docs/database-schema.md — full entity schema with constraints (team-authored)
- docs/frontend-architecture.md — route table, state management, component inventory (team-authored)
- docs/projeto-visao-geral.md — module list, user flows, priorities (team-authored)
- https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/ — official JWT auth guide (updated to PyJWT)
- https://github.com/fastapi/fastapi/pull/11589 — PR confirming PyJWT replaces python-jose in FastAPI docs
- https://sqlite.org/wal.html — WAL mode official documentation
- https://sqlite.org/quirks.html — SQLite official quirks and gotchas

### Secondary (MEDIUM confidence)
- https://chaoticengineer.hashnode.dev/fastapi-sqlalchemy — SQLAlchemy 2.0 + FastAPI patterns
- https://www.robinwieruch.de/react-libraries/ — React Libraries 2025 annual guide
- https://blog.greeden.me/en/2025/08/12/no-fail-guide-getting-started-with-database-migrations-fastapi-x-sqlalchemy-x-alembic/ — Alembic + SQLite WAL + batch mode
- https://tenthousandmeters.com/blog/sqlite-concurrent-writes-and-database-is-locked-errors/ — SQLite concurrent write analysis
- https://nulldog.com/jwt-in-localstorage-with-react-security-risks-best-practices — JWT storage security tradeoffs
- Secretaria Escolar Digital SP (sed.educacao.sp.gov.br) — Brazilian SIS feature reference
- Diário Escola / Activesoft — Brazilian SIS feature reference

### Tertiary (LOW confidence / inferred)
- Deployment target unconfirmed — assumed local demo or simple cloud host for academic evaluation

---
*Research completed: 2026-04-26*
*Ready for roadmap: yes*
