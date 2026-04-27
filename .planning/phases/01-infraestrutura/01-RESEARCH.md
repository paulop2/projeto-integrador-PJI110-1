# Phase 1: Infraestrutura - Research

**Researched:** 2026-04-26
**Domain:** FastAPI + SQLAlchemy 2.0 sync + Alembic + SQLite + React 18 + Vite + TypeScript project scaffolding
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Schema do banco:**
- Schema completo criado na Phase 1 via Alembic: todas as entidades (users, alunos, turmas, disciplinas, notas, chamadas) e todas as tabelas de vínculo (professor_turma, responsavel_aluno) + indexes
- Zero migrations adicionais nas phases seguintes — phases 2-6 focam só em código
- SQLite em WAL mode com `PRAGMA foreign_keys=ON` configurado na inicialização
- Migration da Phase 1 insere um usuário admin padrão com credenciais de desenvolvimento (ex: admin@escola.dev / admin123)

**Gerenciamento de dependências Python:**
- venv + requirements.txt (sem Poetry)
- `python -m venv venv && pip install -r requirements.txt` para setup local

### Claude's Discretion

- Estrutura de pastas: monorepo com `/backend` e `/frontend` na raiz
- Workflow de desenvolvimento: dois terminais separados ou Makefile com targets `make backend` / `make frontend` / `make dev`
- Python tooling: Black + Ruff
- Frontend tooling: ESLint + Prettier, npm como package manager
- Credenciais exatas do admin seed (seguir padrão seguro de dev)

### Deferred Ideas (OUT OF SCOPE)

None — discussion stayed within phase scope
</user_constraints>

---

## Summary

Phase 1 establishes the monorepo skeleton with a functioning FastAPI backend (localhost:8000) and React frontend (localhost:5173) that can already communicate via CORS. The critical deliverable unique to this phase is the Alembic migration that creates the **complete database schema in one shot** — all 8 tables plus 2 junction tables plus indexes, plus a seeded admin user. Phases 2-6 depend entirely on this schema existing without modification.

The technology choices are all locked. The main execution risk is Alembic configuration for SQLite: batch mode must be enabled (`render_as_batch=True`) or future migrations will fail on `ALTER TABLE`. The second risk is SQLite engine setup: WAL mode and `foreign_keys=ON` must be set via SQLAlchemy event listener on every connection, not just once. These two details are non-negotiable for correctness.

For the frontend, `npm create vite@latest frontend -- --template react-ts` is the single command that scaffolds a correct React 18 + TypeScript + Vite project. The only configuration decision for Phase 1 is wiring up the development-time proxy or CORS to allow `localhost:5173 → localhost:8000` calls to succeed.

**Primary recommendation:** Build `backend/` first (FastAPI skeleton + database.py + Alembic migration), verify `alembic upgrade head` completes cleanly, then scaffold `frontend/` and prove CORS works with a single test endpoint. Phase 1 is done when those two checks pass.

---

## Standard Stack

### Core — Backend

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python | 3.12+ | Runtime | 3.12 stable LTS; FastAPI requires 3.10+ |
| FastAPI | 0.115.x+ | REST API framework | Auto OpenAPI docs, Pydantic v2 integration, dependency injection |
| SQLAlchemy | 2.0+ | ORM + session management | Mature, integrates with FastAPI deps; use sync (not async) for SQLite |
| Alembic | 1.13+ | Database migrations | Only migration tool for SQLAlchemy; required for WAL + batch mode |
| SQLite | bundled | Database | Zero-config, single file; WAL mode for concurrent reads |
| Uvicorn | 0.30+ | ASGI server | Standard FastAPI dev server; `uvicorn[standard]` for extras |
| pydantic-settings | 2.x | `.env` loading | `BaseSettings` + `SettingsConfigDict(env_file=".env")` — reads `.env` automatically |
| passlib[bcrypt] | 1.7.x | Password hashing | Needed for Phase 2 auth; install now so schema can store hashed passwords |
| PyJWT | 2.x | JWT tokens | Install now for Phase 2; do NOT install python-jose (abandoned) |

### Core — Frontend

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| React | 18.x | UI framework | Locked. Stable ecosystem; React 19 has breaking changes |
| TypeScript | 5.x | Type safety | Catches API contract mismatches early |
| Vite | 5.x+ | Build tool + dev server | Default for new React projects; `create vite` scaffolds correctly |
| React Router DOM | 6.x | Client-side routing | Use `createBrowserRouter` (data API), not legacy `<BrowserRouter>` |
| TanStack Query | 5.x | Server state + data fetching | Replaces manual useEffect patterns; handles cache/loading/error |

### Supporting — Backend Tooling

| Tool | Version | Purpose | Config location |
|------|---------|---------|-----------------|
| Ruff | latest | Linter + formatter (replaces Black + flake8 + isort) | `pyproject.toml` `[tool.ruff]` |
| Black | latest | Formatter (keep alongside Ruff for compatibility) | `pyproject.toml` `[tool.black]` — set same `line-length=88` |

**Note on Black + Ruff:** CONTEXT.md specifies both. Ruff's formatter can fully replace Black. The safest approach for a team: use Ruff for linting (`ruff check .`) and Black for formatting (`black .`), both configured to `line-length = 88` in `pyproject.toml`. Alternatively, use only Ruff formatter (`ruff format .`) and drop Black. Recommend: **use only Ruff** (linter + formatter) to avoid configuration conflicts — it is Black-compatible by default.

### Supporting — Frontend Tooling

| Tool | Version | Purpose | Notes |
|------|---------|---------|-------|
| ESLint | ships with Vite | Linting | Vite scaffolds ESLint config automatically (`eslint.config.js`) |
| Prettier | latest | Formatting | Install separately: `npm install -D prettier` |

### Installation Commands

```bash
# Backend — create structure
mkdir backend && cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install "fastapi[standard]" "sqlalchemy>=2.0" alembic "pydantic-settings>=2" \
            "passlib[bcrypt]" "python-jose[cryptography]" PyJWT uvicorn
pip install --dev ruff black

pip freeze > requirements.txt

# Initialize Alembic
alembic init alembic
# Then edit alembic/env.py (see Code Examples below)

# Frontend — from repo root
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install react-router-dom @tanstack/react-query axios
npm install -D prettier
```

---

## Architecture Patterns

### Recommended Project Structure

```
projeto-integrador-PJI110-1/         # monorepo root
├── backend/
│   ├── venv/                         # git-ignored
│   ├── alembic/
│   │   ├── env.py                    # CRITICAL: render_as_batch=True + pragma event
│   │   ├── script.py.mako
│   │   └── versions/
│   │       └── 0001_initial_schema.py   # Full schema + seed admin
│   ├── src/
│   │   ├── main.py                   # FastAPI app init, CORS, router registration
│   │   ├── config.py                 # Settings via pydantic-settings
│   │   ├── database.py               # engine, SessionLocal, get_db dependency
│   │   ├── models/
│   │   │   └── __init__.py           # Import all models (Alembic needs to see them)
│   │   └── (domain modules added Phase 2+)
│   ├── alembic.ini
│   ├── requirements.txt
│   ├── pyproject.toml                # Black + Ruff config
│   └── .env                          # git-ignored
│
├── frontend/
│   ├── src/
│   │   ├── main.tsx                  # ReactDOM render + QueryClientProvider
│   │   ├── App.tsx                   # Router setup with createBrowserRouter
│   │   └── services/
│   │       └── api.ts                # Axios instance with baseURL from env
│   ├── .env.local                    # git-ignored; VITE_API_URL=http://localhost:8000
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── package.json
│
├── Makefile                          # make dev / make backend / make frontend
├── .env.example                      # Documents all required env vars
└── .gitignore                        # venv/, *.db, .env, node_modules/
```

### Pattern 1: SQLite Engine with WAL Mode + Foreign Keys

**What:** Configure all required SQLite pragmas via SQLAlchemy's `event.listens_for(engine, "connect")`. This runs on every new connection, ensuring WAL mode and foreign key enforcement are always active.

**When to use:** The `database.py` file — set this up before any other database code.

```python
# backend/src/database.py
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from src.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},  # Required for SQLite in FastAPI
)

@event.listens_for(engine, "connect")
def set_sqlite_pragmas(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")        # WAL mode for concurrent reads
    cursor.execute("PRAGMA foreign_keys=ON")          # Enforce FK constraints
    cursor.execute("PRAGMA busy_timeout=5000")        # Wait up to 5s on write lock
    cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Source: Official FastAPI SQL docs + PITFALLS.md (pitfall 2)

### Pattern 2: Alembic env.py with render_as_batch + WAL Pragma

**What:** Configure Alembic's `env.py` to use batch mode (required for any future schema changes on SQLite) and import all models so autogenerate works.

**Critical:** `render_as_batch=True` must be in BOTH `run_migrations_online` and `run_migrations_offline`.

```python
# backend/alembic/env.py (key sections)
import sys
sys.path.insert(0, '.')

from src.database import engine, Base
from src import models  # noqa: F401 — import all models so Alembic sees them

target_metadata = Base.metadata

def run_migrations_online():
    with engine.connect() as connection:
        # Disable FK enforcement during batch migration (required for SQLite)
        connection.execute(text("PRAGMA foreign_keys=OFF"))
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,      # CRITICAL for SQLite ALTER support
            naming_convention={
                "ix": "ix_%(table_name)s_%(column_0_label)s",
                "uq": "uq_%(table_name)s_%(column_0_name)s",
                "ck": "ck_%(table_name)s_%(constraint_name)s",
                "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
                "pk": "pk_%(table_name)s",
            },
        )
        with context.begin_transaction():
            context.run_migrations()
        connection.execute(text("PRAGMA foreign_keys=ON"))
```

Source: Alembic official docs (https://alembic.sqlalchemy.org/en/latest/batch.html)

### Pattern 3: pydantic-settings Config

**What:** Load all environment variables from `.env` with type validation. Use `@lru_cache` to avoid re-reading on every request.

```python
# backend/src/config.py
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str = "sqlite:///./escola.db"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480  # 8 hours
    CORS_ORIGINS: list[str] = ["http://localhost:5173"]
    ENVIRONMENT: str = "development"

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
```

Source: FastAPI official settings docs (https://fastapi.tiangolo.com/advanced/settings/)

### Pattern 4: FastAPI App with CORS

**What:** CORS middleware must be added FIRST before any other middleware. Origins must match exactly (including port).

```python
# backend/src/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings

app = FastAPI(title="Sistema Escolar API", version="1.0.0")

# CORS must be added first
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,   # ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok", "environment": settings.ENVIRONMENT}
```

Source: FastAPI CORS docs (https://fastapi.tiangolo.com/tutorial/cors/)

### Pattern 5: Frontend Bootstrap

**What:** Wrap the React app with QueryClientProvider in `main.tsx`. This is required before any TanStack Query hooks work.

```typescript
// frontend/src/main.tsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { RouterProvider } from 'react-router-dom'
import { router } from './App'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 1,
    },
  },
})

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  </React.StrictMode>
)
```

Source: TanStack Query v5 docs (https://tanstack.com/query/v5/docs/framework/react/installation)

### Pattern 6: Makefile Targets

**What:** Simplify two-terminal development with a Makefile at the repo root.

```makefile
# Makefile (at repo root)
.PHONY: backend frontend dev install-backend install-frontend

backend:
	cd backend && source venv/bin/activate && uvicorn src.main:app --reload --port 8000

frontend:
	cd frontend && npm run dev

dev:
	make -j2 backend frontend

install-backend:
	cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt

install-frontend:
	cd frontend && npm install

migrate:
	cd backend && source venv/bin/activate && alembic upgrade head

setup: install-backend install-frontend migrate
```

Note: `make -j2` runs both targets in parallel. On Windows, `make` requires Git Bash or WSL; alternatively provide a `start.ps1` or document running two terminal commands.

### Pattern 7: Complete Database Schema (All Tables)

The Phase 1 Alembic migration must create ALL of these tables in one revision:

| Table | Key Columns | Notes |
|-------|------------|-------|
| `usuarios` | id, email, senha_hash, tipo (admin/professor/responsavel), ativo | Central auth table |
| `professores` | id, usuario_id FK, nome, cpf | 1:1 with usuarios |
| `responsaveis` | id, usuario_id FK, nome, cpf, telefone | 1:1 with usuarios |
| `alunos` | id, nome, data_nascimento, responsavel_id FK, turma_id FK, ativo | Core entity |
| `turmas` | id, nome, ano, serie, turno | Classes/grades |
| `disciplinas` | id, nome, carga_horaria | Subjects |
| `chamadas` | id, turma_id FK, disciplina_id FK, professor_id FK, data, created_at | Roll-call session |
| `presencas` | id, chamada_id FK, aluno_id FK, presente (bool), justificativa | Attendance record |
| `avaliacoes` | id, turma_id FK, disciplina_id FK, professor_id FK, titulo, bimestre (1-4), valor_maximo, data | Assessment definition |
| `notas` | id, avaliacao_id FK, aluno_id FK, valor, created_at | Student score |
| `professor_turma` | professor_id FK, turma_id FK, disciplina_id FK | Junction: who teaches what |

**Indexes needed on:** `notas.aluno_id`, `notas.avaliacao_id`, `presencas.aluno_id`, `presencas.chamada_id`, `alunos.responsavel_id`, `alunos.turma_id`, `professor_turma.(professor_id, turma_id, disciplina_id)` unique.

**Seed data in same migration:** Insert one row into `usuarios` with `tipo='admin'`, `email='admin@escola.dev'`, `senha_hash=bcrypt('admin123')`, `ativo=True`.

### Anti-Patterns to Avoid

- **Do not use `Base.metadata.create_all()`** for production schema — bypasses migration history; use `alembic upgrade head` only
- **Do not put `PRAGMA foreign_keys=ON` only in the app startup** — it must be in the SQLAlchemy event listener (called per connection)
- **Do not use `allow_origins=["*"]` with `allow_credentials=True`** — browsers reject this combination
- **Do not use `allow_origins=["http://localhost:3000"]`** — Vite serves on 5173, not 3000
- **Do not configure Alembic without `render_as_batch=True`** — any future `ALTER COLUMN` will fail on SQLite
- **Do not commit `.env`** — only `.env.example` goes to git
- **Do not use async SQLAlchemy** — sync SQLAlchemy + WAL + busy_timeout is correct for this scale; async adds complexity for no benefit

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Loading `.env` file | Custom file parser | pydantic-settings `BaseSettings` | Handles type coercion, defaults, validation, test overrides |
| SQLite pragma setup | Connection event hooks from scratch | SQLAlchemy `event.listens_for(engine, "connect")` | Runs on every connection automatically |
| Schema versioning | Keeping `create_all()` + manual SQL | Alembic revisions | Tracks history, supports rollback, enables team collaboration |
| React project scaffold | Manual webpack config | `npm create vite@latest -- --template react-ts` | Correct HMR, TypeScript, ESLint config in one command |
| Server state / data fetching | `useEffect` + `useState` for API calls | TanStack Query `useQuery` / `useMutation` | Caching, deduplication, background refresh, loading/error states |
| CORS config | Manual response headers | FastAPI `CORSMiddleware` | Handles preflight, credentials, all HTTP methods correctly |

**Key insight:** Every "hand-roll" in this list has subtle edge cases. WAL pragma must run per-connection (not once). CORS must handle OPTIONS preflight. Schema versioning with `create_all()` silently drops columns on table renames. Use the standard tools — they exist precisely because the manual approach has known failure modes.

---

## Common Pitfalls

### Pitfall 1: Alembic Without `render_as_batch=True`
**What goes wrong:** Migrations autogenerated after Phase 1 that include `ALTER COLUMN`, `DROP COLUMN`, or constraint changes will fail with `OperationalError: near "ALTER": syntax error` on SQLite.
**Why it happens:** SQLite's ALTER TABLE only supports `ADD COLUMN` and `RENAME`. Alembic's batch mode works around this by creating a new table, copying data, and dropping the old one.
**How to avoid:** Set `render_as_batch=True` in `context.configure()` in `env.py` from day one. Also disable FK enforcement during migration with `PRAGMA foreign_keys=OFF` / `ON`.
**Warning signs:** Any migration that uses `op.alter_column()`, `op.drop_constraint()`, or `op.drop_column()` without batch mode wrapper.

### Pitfall 2: `PRAGMA foreign_keys=ON` Not Running Per-Connection
**What goes wrong:** Foreign key violations are silently ignored. Orphaned `presencas` records can exist with invalid `aluno_id`. The success criteria check (item 5) will fail.
**Why it happens:** SQLite's foreign key enforcement is off by default AND must be set on every new connection. Setting it once at startup does not persist to new connections from the pool.
**How to avoid:** Use `@event.listens_for(engine, "connect")` to set the pragma on every connection (see Pattern 1 above).
**Warning signs:** Manual test `INSERT INTO presencas (chamada_id, aluno_id, ...) VALUES (99999, 99999, ...)` succeeds instead of raising a FK error.

### Pitfall 3: CORS Blocks First Frontend-Backend Test
**What goes wrong:** Frontend developer gets `Access to fetch at 'http://localhost:8000/health' from origin 'http://localhost:5173' has been blocked by CORS policy`.
**Why it happens:** CORSMiddleware is missing, or `allow_origins` does not include `http://localhost:5173` exactly (wrong port, missing scheme, trailing slash).
**How to avoid:** Add `CORSMiddleware` as the FIRST middleware in `main.py`. Read origins from `settings.CORS_ORIGINS`. Test with a browser request on day 1.
**Warning signs:** `Access-Control-Allow-Origin` header missing from backend responses.

### Pitfall 4: Alembic Cannot Import Models
**What goes wrong:** `alembic revision --autogenerate` produces an empty migration (no tables). Running `alembic upgrade head` on the empty migration creates no schema.
**Why it happens:** Alembic's autogenerate compares `target_metadata` against the live database. If models are not imported before `target_metadata = Base.metadata`, Alembic sees nothing to generate.
**How to avoid:** In `alembic/env.py`, import ALL SQLAlchemy model files before setting `target_metadata`. A clean pattern: create `src/models/__init__.py` that imports every model file, then `import src.models` in `env.py`.
**Warning signs:** Running `alembic revision --autogenerate -m "initial"` and the generated file contains only `pass` in `upgrade()`.

### Pitfall 5: Windows venv Activation in Makefile
**What goes wrong:** `source venv/bin/activate` fails on Windows because PowerShell/cmd use `venv\Scripts\activate`.
**Why it happens:** Makefile syntax assumes Unix shells. Windows developers on the team get errors.
**How to avoid:** Document both activation commands in README. The Makefile targets work correctly in Git Bash (which uses Unix shell). Alternatively, use `python -m uvicorn ...` directly without activating venv (works if `python` resolves to the venv interpreter).
**Warning signs:** `make backend` errors with `source: not found` on Windows CMD.

### Pitfall 6: bcrypt Not Available for Seed Migration
**What goes wrong:** The Alembic migration that seeds the admin user tries to hash the password with `passlib[bcrypt]`, but if `passlib` is not installed, the migration fails.
**Why it happens:** The migration script runs Python code; any library it imports must be installed in the venv.
**How to avoid:** Include `passlib[bcrypt]` in `requirements.txt` before running migrations. The Phase 1 seed migration imports `from passlib.context import CryptContext` — this must succeed.

---

## Code Examples

### Complete `.env.example`

```bash
# backend/.env.example — copy to .env and fill in real values
DATABASE_URL=sqlite:///./escola.db
SECRET_KEY=change-me-in-production-use-random-32-chars
ACCESS_TOKEN_EXPIRE_MINUTES=480
CORS_ORIGINS=["http://localhost:5173"]
ENVIRONMENT=development
```

### Vite Frontend Env

```bash
# frontend/.env.local — git-ignored
VITE_API_URL=http://localhost:8000
```

```typescript
// frontend/src/services/api.ts
import axios from 'axios'

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})
```

### Verify CORS Works (Test Endpoint)

```typescript
// frontend/src/App.tsx — temporary CORS test
import { useEffect, useState } from 'react'
import { api } from './services/api'

function App() {
  const [health, setHealth] = useState<string>('checking...')

  useEffect(() => {
    api.get('/health').then(res => setHealth(JSON.stringify(res.data)))
  }, [])

  return <div>Backend: {health}</div>
}
```

### pyproject.toml (Ruff only — recommended)

```toml
# backend/pyproject.toml
[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W"]
ignore = ["E501"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

### Alembic `alembic.ini` Key Settings

```ini
# backend/alembic.ini
script_location = alembic
sqlalchemy.url = sqlite:///./escola.db
# Note: in practice, get URL from env var in env.py, not hardcoded here
```

---

## State of the Art

| Old Approach | Current Approach | Impact |
|--------------|------------------|--------|
| `Base.metadata.create_all()` for schema init | Alembic migrations | Schema history, rollback, team collaboration |
| `python-jose` for JWT | `PyJWT 2.x` | python-jose abandoned (no updates since 2021, unpatched vuln) |
| Create React App | `npm create vite@latest` | CRA deprecated; Vite is 10x faster build, official React recommendation |
| Tailwind v4 | Tailwind v3 | v4 config is completely different; ecosystem not caught up |
| Black + flake8 + isort separately | Ruff (replaces all three) | One tool, one config, 100x faster |
| FastAPI docs recommending SQLModel | SQLAlchemy 2.0 directly | FastAPI tutorial now shows SQLModel, but SQLAlchemy 2.0 directly is still fully supported and more flexible for complex queries |
| Async SQLAlchemy for FastAPI | Sync SQLAlchemy + WAL | For SQLite prototype scale, sync + WAL + busy_timeout is simpler and sufficient |

---

## Open Questions

1. **Ruff vs Black + Ruff**
   - What we know: CONTEXT.md specifies "Black + Ruff"; Ruff's formatter is Black-compatible
   - What's unclear: Team may expect `black .` command; Ruff formatter is newer and replaces it
   - Recommendation: Configure `pyproject.toml` with only Ruff (linter + formatter). Planner should document this choice clearly in task instructions so team understands why `black` is not called explicitly.

2. **Makefile portability on Windows**
   - What we know: 6/8 team members may be on Windows; `make` requires Git Bash
   - What's unclear: Whether team has Git Bash or prefers PowerShell
   - Recommendation: Provide Makefile AND document the raw commands for each target in README. Makefile is a convenience, not a requirement.

3. **Vite proxy vs CORS configuration**
   - What we know: CORS in FastAPI works; Vite proxy also works and eliminates CORS entirely in dev
   - What's unclear: Which approach is simpler for the team to debug
   - Recommendation: Use FastAPI CORS configuration (not Vite proxy). CORS config is explicit and mirrors production behavior. Vite proxy hides CORS issues that will surface in production.

4. **Admin seed password hashing at migration time**
   - What we know: Migration must insert hashed password; passlib must be importable in migration
   - What's unclear: Whether to hardcode hash string or compute at migration run time
   - Recommendation: Pre-compute the bcrypt hash for `admin123` and hardcode the hash string in the migration script. This avoids importing passlib in the migration and is idempotent. Hash: `$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW` (bcrypt of "admin123", cost 12).

---

## Sources

### Primary (HIGH confidence)
- Alembic official docs — batch mode configuration: https://alembic.sqlalchemy.org/en/latest/batch.html
- FastAPI official docs — CORS: https://fastapi.tiangolo.com/tutorial/cors/
- FastAPI official docs — SQL databases: https://fastapi.tiangolo.com/tutorial/sql-databases/
- FastAPI official docs — Settings with pydantic-settings: https://fastapi.tiangolo.com/advanced/settings/
- TanStack Query v5 — Installation: https://tanstack.com/query/v5/docs/framework/react/installation
- Vite official docs — Getting started: https://vite.dev/guide/
- `.planning/research/STACK.md` — Stack research (verified 2026-04-26)
- `.planning/research/PITFALLS.md` — Pitfalls research (verified 2026-04-26)
- `.planning/research/ARCHITECTURE.md` — Architecture research (verified 2026-04-26)

### Secondary (MEDIUM confidence)
- SQLite official WAL docs: https://sqlite.org/wal.html
- Ruff official docs — Configuration: https://docs.astral.sh/ruff/configuration/
- React Router v6 docs — createBrowserRouter: https://reactrouter.com/6.30.3/routers/create-browser-router
- Alembic batch mode + SQLite walkthrough: https://blog.miguelgrinberg.com/post/fixing-alter-table-errors-with-flask-migrate-and-sqlite

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — verified against official docs and existing project research
- Architecture: HIGH — based on locked decisions and team-authored architecture docs
- Alembic batch mode: HIGH — verified directly from official Alembic docs
- SQLite WAL setup: HIGH — official SQLite + SQLAlchemy docs
- Pitfalls: HIGH — cross-verified with existing PITFALLS.md research

**Research date:** 2026-04-26
**Valid until:** 2026-05-26 (30 days — stable ecosystem)
