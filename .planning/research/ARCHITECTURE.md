# Architecture Research

**Domain:** School management web application (SPA + REST API)
**Researched:** 2026-04-26
**Confidence:** HIGH — based on existing project documentation in `docs/` (api-architecture.md, database-schema.md, frontend-architecture.md, projeto-visao-geral.md)

---

## Standard Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        BROWSER (SPA)                            │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │
│  │  Admin   │  │ Professor│  │Responsavel│  │  Auth / Login │  │
│  │  Pages   │  │  Pages   │  │  Pages   │  │               │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └───────┬───────┘  │
│       │             │             │                 │          │
│  ┌────┴─────────────┴─────────────┴─────────────────┴──────┐   │
│  │           React Router + Role-based Guards              │   │
│  └────────────────────────────┬────────────────────────────┘   │
│                               │                                 │
│  ┌────────────────────────────┴────────────────────────────┐   │
│  │    React Query (server state) + Context (auth/ui)       │   │
│  └────────────────────────────┬────────────────────────────┘   │
│                               │ HTTP + JWT Bearer               │
└───────────────────────────────┼─────────────────────────────────┘
                                │
┌───────────────────────────────┼─────────────────────────────────┐
│                        BACKEND (FastAPI)                         │
│                               │                                 │
│  ┌────────────────────────────┴────────────────────────────┐   │
│  │              Auth Middleware (JWT verification)          │   │
│  └────────────────────────────┬────────────────────────────┘   │
│                               │                                 │
│  ┌──────────┐  ┌──────────┐  ┌┴─────────┐  ┌──────────────┐  │
│  │  /auth   │  │ /turmas  │  │ /alunos  │  │  /chamadas   │  │
│  │  router  │  │  router  │  │  router  │  │    router    │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └──────┬───────┘  │
│       │             │             │                │           │
│  ┌────┴─────────────┴─────────────┴────────────────┴──────┐   │
│  │              Service Layer (business rules)             │   │
│  └────────────────────────────┬────────────────────────────┘   │
│                               │                                 │
│  ┌────────────────────────────┴────────────────────────────┐   │
│  │              SQLAlchemy ORM / Raw SQL queries            │   │
│  └────────────────────────────┬────────────────────────────┘   │
│                               │                                 │
└───────────────────────────────┼─────────────────────────────────┘
                                │
┌───────────────────────────────┼─────────────────────────────────┐
│                        DATA LAYER                                │
│                               │                                 │
│              ┌────────────────┴────────────────┐               │
│              │          SQLite file             │               │
│              │   escola.db (single file, local) │               │
│              └─────────────────────────────────┘               │
└─────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Communicates With |
|-----------|---------------|-------------------|
| React SPA | UI rendering, routing, form handling, token storage | FastAPI via HTTP |
| React Router | Route protection by auth status and user role | Auth Context |
| Auth Context | Holds JWT token and decoded user (id, email, tipo) in memory | React Query, all pages |
| React Query | Server state cache, auto-invalidation, loading/error states | FastAPI REST endpoints |
| FastAPI App | HTTP request handling, response formatting, CORS | Auth middleware, routers |
| Auth Middleware | JWT verification on every protected request, injects current_user | All protected routers |
| API Routers | Route definitions grouped by resource | Service layer |
| Service Layer | Business logic, ownership checks (professor owns turma?, responsavel owns filho?) | ORM/queries |
| ORM / queries | SQL generation, transaction management | SQLite file |
| SQLite | Data persistence (single file, no server process needed) | Nothing |

---

## Recommended Project Structure

### Backend (FastAPI)

```
backend/
├── src/
│   ├── main.py               # FastAPI app init, CORS, router registration
│   ├── config.py             # Settings (SECRET_KEY, DB_URL, TOKEN_EXPIRE)
│   ├── database.py           # SQLAlchemy engine and session factory
│   ├── dependencies.py       # get_db(), get_current_user(), role guards
│   │
│   ├── auth/
│   │   ├── router.py         # POST /auth/login, POST /auth/logout
│   │   ├── service.py        # verify_password(), create_access_token()
│   │   └── schemas.py        # LoginRequest, TokenResponse
│   │
│   ├── usuarios/
│   │   ├── router.py         # GET/POST/PUT/DELETE /usuarios
│   │   ├── service.py        # create_usuario(), list_usuarios()
│   │   ├── schemas.py        # UsuarioCreate, UsuarioResponse
│   │   └── models.py         # SQLAlchemy Usuario model
│   │
│   ├── professores/
│   │   ├── router.py
│   │   ├── service.py
│   │   ├── schemas.py
│   │   └── models.py
│   │
│   ├── responsaveis/
│   │   ├── router.py
│   │   ├── service.py
│   │   ├── schemas.py
│   │   └── models.py
│   │
│   ├── alunos/
│   │   ├── router.py
│   │   ├── service.py
│   │   ├── schemas.py
│   │   └── models.py
│   │
│   ├── turmas/
│   │   ├── router.py
│   │   ├── service.py
│   │   ├── schemas.py
│   │   └── models.py
│   │
│   ├── disciplinas/
│   │   ├── router.py
│   │   ├── service.py
│   │   ├── schemas.py
│   │   └── models.py
│   │
│   ├── chamadas/
│   │   ├── router.py         # POST /chamadas, GET /chamadas/:id, etc.
│   │   ├── service.py        # Business rule: professor must own turma
│   │   ├── schemas.py
│   │   └── models.py         # Chamada + Presenca models
│   │
│   ├── avaliacoes/
│   │   ├── router.py         # POST /avaliacoes, GET /avaliacoes, etc.
│   │   ├── service.py        # Business rule: nota <= valor_maximo
│   │   ├── schemas.py
│   │   └── models.py         # Avaliacao + Nota models
│   │
│   └── database/
│       └── migrations/
│           └── 001_initial_schema.sql
│
├── tests/
│   ├── test_auth.py
│   ├── test_chamadas.py
│   └── test_notas.py
│
├── requirements.txt
└── .env
```

### Frontend (React)

```
frontend/
├── src/
│   ├── main.jsx              # ReactDOM.render, QueryClientProvider
│   ├── App.jsx               # Router setup, route definitions
│   │
│   ├── contexts/
│   │   ├── AuthContext.jsx   # JWT storage, login(), logout(), currentUser
│   │   └── UIContext.jsx     # Sidebar open/closed, toast notifications
│   │
│   ├── hooks/
│   │   ├── useAuth.js        # Consumes AuthContext
│   │   ├── useAlunos.js      # React Query hooks for alunos API
│   │   ├── useChamadas.js
│   │   └── useNotas.js
│   │
│   ├── services/
│   │   └── api.js            # Axios instance with base URL + auth header interceptor
│   │
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Layout.jsx    # Sidebar + Header + content slot
│   │   │   ├── Sidebar.jsx   # Nav links filtered by user role
│   │   │   └── Header.jsx    # User name, logout button
│   │   ├── guards/
│   │   │   ├── PrivateRoute.jsx   # Redirect to /login if no token
│   │   │   └── RoleRoute.jsx     # Redirect to dashboard if wrong role
│   │   └── ui/
│   │       ├── Table.jsx         # Generic sortable/paginated table
│   │       ├── Card.jsx
│   │       ├── Button.jsx
│   │       ├── Input.jsx
│   │       ├── Select.jsx
│   │       ├── Loading.jsx
│   │       └── EmptyState.jsx
│   │
│   ├── pages/
│   │   ├── auth/
│   │   │   └── Login.jsx
│   │   ├── admin/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Usuarios.jsx
│   │   │   ├── Professores.jsx
│   │   │   ├── Responsaveis.jsx
│   │   │   ├── Alunos.jsx
│   │   │   ├── Turmas.jsx
│   │   │   └── Disciplinas.jsx
│   │   ├── professor/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Chamada.jsx      # Take attendance
│   │   │   ├── Avaliacoes.jsx   # List/create assessments
│   │   │   └── LancarNotas.jsx  # Enter grades
│   │   └── responsavel/
│   │       ├── Dashboard.jsx
│   │       ├── Filhos.jsx
│   │       ├── Boletim.jsx
│   │       └── Frequencia.jsx
│   │
│   └── utils/
│       ├── jwt.js             # decodeToken(), isTokenExpired()
│       └── formatters.js      # formatDate(), formatNota()
│
├── index.html
├── vite.config.js
└── package.json
```

### Structure Rationale

- **Feature-based modules (backend):** Each domain entity (alunos, chamadas, etc.) owns its own router, service, schemas, and models. This maps directly to team member assignments and avoids merge conflicts.
- **Role-based page directories (frontend):** `pages/admin/`, `pages/professor/`, `pages/responsavel/` make it obvious which pages each role sees and which team members own which screens.
- **services/api.js centralized:** Single Axios instance means the auth header injection is defined once. Every API call picks it up automatically.
- **hooks/ separates data fetching from rendering:** React Query hooks live in `hooks/`, pages stay clean and focused on display logic.

---

## Architectural Patterns

### Pattern 1: Ownership Check in Service Layer

**What:** Before any read or write on sensitive data (aluno grades, chamada records), the service function verifies the requesting user has permission via the ownership rules defined in `api-architecture.md`.

**When to use:** Every endpoint that touches aluno, chamada, presenca, avaliacao, nota data.

**Trade-offs:** Adds one extra query per request. Acceptable at this scale; avoids an entire class of authorization bugs.

**Example:**
```python
# backend/src/chamadas/service.py
def get_chamada(db, chamada_id: int, current_user: dict):
    chamada = db.query(Chamada).filter(Chamada.id == chamada_id).first()
    if not chamada:
        raise HTTPException(404, "Chamada nao encontrada")

    if current_user["tipo"] == "admin":
        return chamada
    if current_user["tipo"] == "professor":
        professor = db.query(Professor).filter(
            Professor.usuario_id == current_user["id"]
        ).first()
        if chamada.professor_id != professor.id:
            raise HTTPException(403, "Sem permissao")
    # responsavel: chamadas are not accessible
    raise HTTPException(403, "Sem permissao")
```

### Pattern 2: JWT Stored in Memory (AuthContext), Fallback to localStorage

**What:** On app load, token is read from localStorage into React Context. All API calls read from Context. On logout, both are cleared.

**When to use:** Single-tab school use case. localStorage survives page refresh (important for teachers doing chamada on shared computers).

**Trade-offs:** localStorage is XSS-vulnerable. For this project scope (intranet-like, single school), acceptable. Mitigation: short 8-hour expiry as specified.

### Pattern 3: React Query for All Server State

**What:** Every API call goes through a `useQuery` or `useMutation` hook. No `useEffect` + `useState` for data fetching.

**When to use:** All pages that display or modify backend data.

**Trade-offs:** Adds React Query as a dependency, but eliminates race conditions, double-fetch bugs, and stale data issues that are common when teams use raw `useEffect`.

---

## Data Flow

### Request Flow: Teacher Takes Attendance

```
Professor clicks "Salvar Chamada"
    ↓
ChamadaForm.jsx calls useMutation (chamadas)
    ↓
api.js POST /api/chamadas  [Authorization: Bearer <jwt>]
    ↓
FastAPI auth middleware validates JWT → injects current_user
    ↓
chamadas/router.py → chamadas/service.py
    ↓
Service: verify professor owns turma_id (professor_turma table)
    ↓
Insert into chamadas + batch insert into presencas
    ↓
Return 201 { success: true, data: { chamada_id, ... } }
    ↓
React Query invalidates ["chamadas"] cache
    ↓
ChamadaForm shows success state, redirects to /chamada history
```

### Request Flow: Parent Views Child's Grades

```
Responsavel navigates to /filhos/:id/notas
    ↓
Boletim.jsx mounts → useQuery(["notas", alunoId])
    ↓
api.js GET /api/notas/:alunoId  [Authorization: Bearer <jwt>]
    ↓
FastAPI: notas/router.py → notas/service.py
    ↓
Service: verify responsavel_id on alunos table matches current_user.id
    ↓
JOIN notas + avaliacoes + disciplinas
    ↓
Return grouped by bimestre + disciplina
    ↓
Boletim.jsx renders BoletimView component with grouped data
```

### Authentication Flow

```
/login form submit
    ↓
POST /api/auth/login { email, senha }
    ↓
FastAPI: verify hash with bcrypt → if valid, create JWT
JWT payload: { sub: user_id, email, tipo, exp: 8h }
    ↓
Return { token: "<jwt>" }
    ↓
AuthContext stores token in localStorage + state
    ↓
React Router redirects based on tipo:
  admin       → /admin
  professor   → /professor
  responsavel → /responsavel
```

### State Management

```
AuthContext (global)
  ├── token (string | null)
  ├── currentUser { id, email, tipo }
  ├── login(token) → decode + store
  └── logout() → clear storage + state

React Query Cache (server state)
  ├── ["alunos"]           → list of alunos
  ├── ["aluno", id]        → single aluno
  ├── ["chamadas"]         → list of chamadas
  ├── ["notas", alunoId]   → notas grouped by bimestre
  └── auto-invalidated on mutation success

Local State (per component)
  ├── Form field values
  ├── Pagination page number
  ├── Filter/search strings
  └── Loading/error UI flags
```

---

## Core Data Models

### Entity Relationships

```
usuarios (authentication)
   |
   ├─── professores (1:1 via usuario_id)
   │        |
   │        ├─── professor_turma (N:N with turmas + disciplinas)
   │        ├─── chamadas (professor who took attendance)
   │        └─── avaliacoes (professor who created assessment)
   |
   └─── responsaveis (1:1 via usuario_id)
            |
            └─── alunos (1:N — one responsavel, multiple children)
                     |
                     ├─── turmas (N:1 — aluno belongs to one turma)
                     ├─── presencas (via chamadas)
                     └─── notas (via avaliacoes)

turmas
   ├─── alunos (1:N)
   ├─── chamadas (1:N)
   └─── avaliacoes (1:N)

disciplinas
   ├─── professor_disciplina (N:N with professores)
   ├─── professor_turma (N:N context: which discipline in which class)
   ├─── chamadas (each chamada is for a specific disciplina)
   └─── avaliacoes (each assessment belongs to a disciplina)

chamadas (one roll call session)
   └─── presencas (one row per aluno per chamada: present/absent)

avaliacoes (one assessment definition)
   └─── notas (one row per aluno per avaliacao: score)
```

### Key Model Constraints (enforce in service layer)

| Rule | Tables Involved | Enforcement Point |
|------|----------------|-------------------|
| nota.valor <= avaliacao.valor_maximo | notas, avaliacoes | Service before INSERT |
| presenca.aluno_id must be in chamada.turma_id | presencas, chamadas, alunos | Service before INSERT |
| nota.aluno_id must be in avaliacao.turma_id | notas, avaliacoes, alunos | Service before INSERT |
| professor can only create chamada for owned turma | chamadas, professor_turma | Service ownership check |
| responsavel can only read own filhos | alunos | Service ownership check |

**Note:** The database-schema.md shows these as PostgreSQL triggers but the stack uses SQLite. Enforce these constraints in the Python service layer instead of triggers — SQLite trigger support is limited and harder to debug.

---

## API Endpoint Groups

### Group 1: Auth
```
POST   /api/auth/login        Public — returns JWT
POST   /api/auth/logout       Authenticated — (stateless: client discards token)
GET    /api/auth/me           Authenticated — returns current_user info
```

### Group 2: Usuarios (Admin only)
```
GET    /api/usuarios          List all users
POST   /api/usuarios          Create user (any type)
GET    /api/usuarios/:id      Get user by ID
PUT    /api/usuarios/:id      Update user
DELETE /api/usuarios/:id      Deactivate user (soft delete via ativo=false)
```

### Group 3: Professores (Admin only for write)
```
GET    /api/professores       Admin: all; Professor: own profile
GET    /api/professores/:id   Admin + self
PUT    /api/professores/:id   Admin + self (own profile edit)
```

### Group 4: Responsaveis (Admin only for write)
```
GET    /api/responsaveis      Admin: all
GET    /api/responsaveis/:id  Admin + self
PUT    /api/responsaveis/:id  Admin + self
```

### Group 5: Alunos
```
GET    /api/alunos            Admin: all; Professor: own turmas; Responsavel: own filhos
POST   /api/alunos            Admin only
GET    /api/alunos/:id        Admin + Professor (own turma) + Responsavel (own filho)
PUT    /api/alunos/:id        Admin only
```

### Group 6: Turmas (Admin manages; Professor reads own)
```
GET    /api/turmas            Admin: all; Professor: assigned turmas
POST   /api/turmas            Admin only
GET    /api/turmas/:id        Admin + Professor (assigned)
PUT    /api/turmas/:id        Admin only
GET    /api/turmas/:id/alunos Admin + Professor (assigned)
```

### Group 7: Disciplinas (Admin manages)
```
GET    /api/disciplinas       All authenticated
POST   /api/disciplinas       Admin only
PUT    /api/disciplinas/:id   Admin only
```

### Group 8: Chamadas (Professor creates; Admin views all)
```
POST   /api/chamadas                   Professor (own turma)
GET    /api/chamadas                   Admin: all; Professor: own turmas
GET    /api/chamadas/:id               Admin + Professor (owner)
PUT    /api/chamadas/:id               Admin + Professor (owner)
GET    /api/alunos/:id/presencas       Admin + Professor (own turma) + Responsavel (own filho)
```

### Group 9: Avaliacoes + Notas
```
POST   /api/avaliacoes                 Professor (own turma+disciplina)
GET    /api/avaliacoes                 Admin: all; Professor: own; Responsavel: filhos' turmas
GET    /api/avaliacoes/:id             Admin + Professor (owner) + Responsavel (filho turma)
PUT    /api/avaliacoes/:id             Admin + Professor (owner)
GET    /api/avaliacoes/:id/notas       Admin + Professor (owner)
PUT    /api/avaliacoes/:id/notas       Professor (owner) — batch update all scores at once
GET    /api/alunos/:id/notas           Admin + Professor (own turma) + Responsavel (own filho)
```

---

## Frontend Route Structure

```
/                     → redirect based on role
/login                → Login.jsx (public)

/admin                → admin/Dashboard.jsx
/admin/usuarios       → admin/Usuarios.jsx
/admin/usuarios/novo  → admin/UsuarioForm.jsx
/admin/professores    → admin/Professores.jsx
/admin/responsaveis   → admin/Responsaveis.jsx
/admin/alunos         → admin/Alunos.jsx
/admin/alunos/novo    → admin/AlunoForm.jsx
/admin/turmas         → admin/Turmas.jsx
/admin/disciplinas    → admin/Disciplinas.jsx

/professor            → professor/Dashboard.jsx
/professor/chamada    → professor/Chamada.jsx (select turma + mark attendance)
/professor/chamadas/:id → professor/ChamadaDetail.jsx (edit past chamada)
/professor/avaliacoes → professor/Avaliacoes.jsx
/professor/avaliacoes/nova → professor/AvaliacaoForm.jsx
/professor/avaliacoes/:id/notas → professor/LancarNotas.jsx

/responsavel          → responsavel/Dashboard.jsx
/responsavel/filhos   → responsavel/Filhos.jsx
/responsavel/filhos/:id → responsavel/FilhoDetail.jsx
/responsavel/filhos/:id/boletim → responsavel/Boletim.jsx
/responsavel/filhos/:id/frequencia → responsavel/Frequencia.jsx

/perfil               → shared/Perfil.jsx (all roles)
```

---

## Build Order (Component Dependencies)

Build in this sequence to avoid blocking team members:

### Layer 0: Foundation (no external dependencies)
1. Database schema + migrations (`001_initial_schema.sql`)
2. FastAPI project skeleton (`main.py`, `database.py`, `config.py`, `dependencies.py`)
3. React project skeleton (Vite, React Router, Axios instance, AuthContext shell)

### Layer 1: Authentication (everything else depends on this)
4. Backend: `auth/` module — login endpoint, JWT creation, `get_current_user` dependency
5. Frontend: Login page + AuthContext complete + PrivateRoute + RoleRoute guards

### Layer 2: Admin CRUD (no business logic, just data management)
6. Backend: `usuarios/`, `professores/`, `responsaveis/`, `disciplinas/` routers + services
7. Backend: `turmas/` + `alunos/` (depends on responsaveis existing)
8. Frontend: Admin pages for all of the above (can be built in parallel with backend)

### Layer 3: Core Academic Operations (depends on Layer 2 data)
9. Backend: `chamadas/` + presence recording (depends on turmas + alunos + professor_turma)
10. Backend: `avaliacoes/` + `notas/` (depends on turmas + alunos + disciplinas)
11. Frontend: Professor attendance flow (`/professor/chamada`)
12. Frontend: Professor grades flow (`/professor/avaliacoes` → `/notas`)

### Layer 4: Parent View (depends on Layer 3 data existing)
13. Frontend: Responsavel pages — Boletim + Frequencia (read-only, query Layer 3 data)

### Layer 5: Polish
14. Dashboard summaries, charts (FrequenciaChart, grade averages)
15. Error boundaries, loading states, empty states throughout
16. PDF export for Boletim (optional differentiator)

---

## Scaling Considerations

| Scale | Architecture Adjustments |
|-------|--------------------------|
| 0-500 users (1 school) | Current monolith is fine. SQLite handles this easily. Single process. |
| 500-5k users (multiple schools) | Keep monolith. Switch to PostgreSQL. Add connection pooling. |
| 5k+ users | Introduce caching layer (Redis), consider splitting read-heavy endpoints. |

**First bottleneck for this project:** SQLite write concurrency — only one writer at a time. Not a problem for a single school with 50 concurrent users. If load increases, migrate to PostgreSQL (SQLAlchemy makes this a config change).

**Second bottleneck:** The `GET /alunos/:id/notas` aggregation query joins notas + avaliacoes + disciplinas. Add a database index on `notas.aluno_id` and `avaliacoes.turma_id` (already planned in schema). This covers the responsavel's most-used query.

---

## Anti-Patterns

### Anti-Pattern 1: Authorization Logic in Routers

**What people do:** Put `if current_user.tipo == "admin"` checks directly in the router function.

**Why it's wrong:** Business rules scatter across the codebase. When the rule changes (e.g., "coordinators can also see all chamadas"), you update it in 5 places and miss one.

**Do this instead:** Put ownership checks in the service layer. The router only extracts request data and calls the service. The service raises `HTTPException(403)` if the check fails.

### Anti-Pattern 2: Fetching All Data Then Filtering in Python

**What people do:** `db.query(Chamada).all()` then loop in Python to filter by professor ownership.

**Why it's wrong:** Loads entire table into memory. At 1000 chamadas it's slow; at 50000 it breaks.

**Do this instead:** Filter at the query level: `db.query(Chamada).filter(Chamada.professor_id == professor.id)`.

### Anti-Pattern 3: useEffect for Every API Call in React

**What people do:** `useEffect(() => { fetch(...).then(setData) }, [])` on every page component.

**Why it's wrong:** No caching, race conditions on fast navigation, stale data shown after mutations, duplicated loading/error state management across 15 pages.

**Do this instead:** React Query `useQuery` hook. One definition, automatic caching, background refetch, invalidation on mutation.

### Anti-Pattern 4: Storing JWT in React state only (lost on refresh)

**What people do:** `const [token, setToken] = useState(null)` — token is gone on page refresh.

**Why it's wrong:** Teachers doing chamada lose their session every time they refresh the page on shared computers.

**Do this instead:** Write to `localStorage` on login, read from `localStorage` on app init in AuthContext. Clear on logout.

### Anti-Pattern 5: PostgreSQL-style Triggers in SQLite

**What people do:** Copy the trigger SQL from database-schema.md (written in PL/pgSQL) and run it in SQLite.

**Why it's wrong:** SQLite does not support PL/pgSQL. The trigger syntax is different and limited.

**Do this instead:** Enforce those same business rules in the Python service layer before INSERT/UPDATE statements.

---

## Integration Points

### Internal Boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| React SPA ↔ FastAPI | HTTP REST, JSON, JWT in Authorization header | CORS must be configured in FastAPI for localhost:5173 in dev |
| FastAPI ↔ SQLite | SQLAlchemy ORM, single connection pool | Use `check_same_thread=False` for SQLite in FastAPI |
| AuthContext ↔ React Query | AuthContext provides token; React Query's `api.js` reads it via interceptor | Token change triggers re-fetch of user-specific queries |

### External Services (future / optional)

| Service | Integration Pattern | Notes |
|---------|---------------------|-------|
| Email (SMTP) | FastAPI background task on grade/absence event | Use Python `smtplib` or `fastapi-mail`. Do not block the request. |
| PDF generation | Server-side `reportlab` or client-side `jsPDF` | Client-side is simpler for v1; no server load |

---

## Sources

- `docs/api-architecture.md` — Endpoint definitions, JWT format, permission matrix (HIGH confidence — team-authored)
- `docs/database-schema.md` — Full entity schema with constraints and indices (HIGH confidence — team-authored)
- `docs/frontend-architecture.md` — Route table, state management strategy, component inventory (HIGH confidence — team-authored)
- `docs/projeto-visao-geral.md` — Module list, user flows, feature priorities (HIGH confidence — team-authored)
- `.planning/PROJECT.md` — Confirmed stack (FastAPI + React + SQLite), constraints, team structure

---

*Architecture research for: Sistema Web de Registro Escolar (UNIVESP PJI110)*
*Researched: 2026-04-26*
