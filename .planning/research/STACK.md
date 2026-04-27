# Stack Research

**Domain:** School management web system (admin + teacher + parent portals)
**Researched:** 2026-04-26
**Confidence:** HIGH (verified against official docs and active community sources)

---

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Python | 3.12+ | Runtime | 3.12 is stable LTS; FastAPI requires 3.10+, but 3.12 gives best performance and type checking support |
| FastAPI | 0.136.x | REST API framework | Built-in async support, Pydantic v2 integration, auto-generates OpenAPI docs; used by 8-person teams without disagreement on conventions |
| Pydantic | 2.7+ | Data validation and serialization | Ships with FastAPI; v2 core is written in Rust (4-17x faster than v1); `model_validate`, `model_dump`, `ConfigDict` are the new API — do not use v1 patterns |
| SQLAlchemy | 2.0+ | ORM / database access layer | Mature, well-documented, integrates directly with FastAPI dependency injection; v2 async API (`AsyncSession`) is the standard for new projects |
| Alembic | 1.13+ | Database migrations | Only tool that tracks schema history for SQLAlchemy models; required even for SQLite to avoid `Base.metadata.create_all()` anti-pattern |
| SQLite | 3.x (bundled) | Database | Already decided; enable WAL mode (`PRAGMA journal_mode=WAL`) for concurrent reads; `check_same_thread=False` required in FastAPI context |
| Uvicorn | 0.30+ | ASGI server | The standard server for FastAPI in development and production; use `uvicorn[standard]` for extras |
| React | 18.x | Frontend UI framework | Stable, mature ecosystem; v19 is available but introduces breaking changes — stick to v18 for team velocity |
| TypeScript | 5.x | Type safety for frontend | Catches contract mismatches between frontend and API early; pair with `strict: true` in tsconfig |
| Vite | 5.x | Frontend build tool | Significantly faster than CRA; official React template: `npm create vite@latest -- --template react-ts` |

### Authentication & Security

| Library | Version | Purpose | Why / Notes |
|---------|---------|---------|-------------|
| PyJWT | 2.x | JWT creation and validation | **Use this, NOT python-jose.** python-jose is abandoned (no release since 2021, unpatched ecdsa vulnerability). FastAPI docs were updated in PR #11589 to recommend PyJWT. `pip install PyJWT` |
| passlib[bcrypt] | 1.7.x | Password hashing | Stable, widely used; bcrypt is secure. Install with `pip install passlib[bcrypt]`. Alternative: `pwdlib[argon2]` for Argon2 algorithm (more modern, but less familiar to team) |
| pydantic-settings | 2.x | Environment config management | Reads `.env` files for `SECRET_KEY`, DB path, etc.; ships as a FastAPI standard dependency |

### Frontend Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| React Router | 6.x | Client-side routing | SPA routing for `/admin`, `/teacher`, `/parent` portals; use `createBrowserRouter` (data router API, not legacy `<BrowserRouter>`) |
| TanStack Query (React Query) | 5.x | Server state / data fetching | Replaces manual `useEffect` + `useState` for API calls; handles caching, background refresh, loading/error states automatically — use for all API calls |
| Axios | 1.x | HTTP client | Better DX than raw `fetch`: interceptors for JWT token injection, centralized error handling, automatic JSON parse; bundle size (~13.5kB gzip) is acceptable for this project size |
| React Hook Form | 7.x | Form state management | Minimal re-renders; pair with Zod resolver for type-safe validation |
| Zod | 3.x | Schema validation (frontend) | TypeScript-first; infer types from schema (`z.infer<typeof schema>`); use same schema on client AND server if sharing types |
| Tailwind CSS | 3.x | Utility-first styling | Fastest path to consistent UI without a design system; v3 is stable (v4 changes config drastically — avoid for team productivity) |
| shadcn/ui | latest | Component library | Unstyled, copy-into-project components built on Radix UI + Tailwind; good for tables, dialogs, forms needed in admin/teacher views. NOT a package — you copy components |

### Backend Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| python-dotenv | 1.x | Load `.env` in development | Only if not using pydantic-settings; pydantic-settings is preferred |
| httpx | 0.27+ | Async HTTP client for tests | Use for testing FastAPI with `AsyncClient`; replaces `requests` in async test context |
| pytest | 8.x | Test runner | Standard Python test runner; use with `pytest-asyncio` for async route tests |
| pytest-asyncio | 0.23+ | Async test support | Required for testing async FastAPI routes and SQLAlchemy async sessions |

### Development Tooling

| Tool | Purpose | Notes |
|------|---------|-------|
| uv | Python package manager + virtualenv | Dramatically faster than pip; replaces `pip + venv`. `uv init`, `uv add fastapi[standard]`. Gaining fast adoption in 2025 |
| Ruff | Python linter + formatter | Replaces flake8 + black + isort in one tool; blazing fast; configure in `pyproject.toml` |
| ESLint + Prettier | JS/TS linter + formatter | Standard frontend tooling; Vite scaffolds ESLint by default |
| Vitest | Frontend unit testing | Vite-native test runner; use instead of Jest for this stack |

---

## Installation

### Backend

```bash
# Recommended: use uv for dependency management
pip install uv
uv init backend
cd backend
uv add "fastapi[standard]" sqlalchemy alembic PyJWT "passlib[bcrypt]" pydantic-settings

# Dev dependencies
uv add --dev pytest pytest-asyncio httpx ruff

# Alternative: traditional pip
pip install "fastapi[standard]" sqlalchemy alembic PyJWT "passlib[bcrypt]" pydantic-settings
```

### Frontend

```bash
# Scaffold React + TypeScript + Vite
npm create vite@latest frontend -- --template react-ts
cd frontend

# Core
npm install react-router-dom @tanstack/react-query axios react-hook-form zod @hookform/resolvers

# Tailwind CSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# shadcn/ui (initialize after Tailwind)
npx shadcn-ui@latest init

# Dev
npm install -D vitest @testing-library/react @testing-library/jest-dom
```

---

## Alternatives Considered

| Category | Recommended | Alternative | When to Use Alternative |
|----------|-------------|-------------|-------------------------|
| JWT library | PyJWT | python-jose | Never — python-jose is abandoned |
| JWT library | PyJWT | Authlib (joserfc) | If you need JWE (token encryption), not just signing; overkill for this project |
| Password hashing | passlib[bcrypt] | pwdlib[argon2] | Argon2 is more modern; use if team knows it. passlib is more familiar and documented |
| ORM | SQLAlchemy 2.0 | SQLModel | SQLModel wraps SQLAlchemy; fine for simple use, but loses flexibility for complex queries. Use raw SQLAlchemy for control |
| DB migrations | Alembic | manual `create_all()` | Never use `create_all()` — it doesn't track history, breaks on schema changes |
| HTTP client | Axios | fetch API | Use fetch for simple one-off requests; Axios for authenticated API with interceptors (this project needs interceptors for JWT) |
| Frontend routing | React Router 6 | TanStack Router | TanStack Router is more type-safe; React Router 6 has better documentation and team familiarity |
| Component library | shadcn/ui + Tailwind | Material UI (MUI) | MUI is heavier; shadcn/ui gives more control and smaller bundle. Avoid MUI unless team already knows it well |
| State management | TanStack Query | Redux / Zustand | Redux is overkill for this app. TanStack Query handles all server state; add Zustand only if complex client-side state emerges |
| Build tool | Vite | Create React App (CRA) | CRA is deprecated and unmaintained. Never use CRA in 2025 |
| CSS approach | Tailwind CSS | CSS Modules | Both are valid; Tailwind is faster for prototyping with a team |

---

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| python-jose | Abandoned library; unpatched ecdsa vulnerability; last release 2021 | PyJWT 2.x |
| Create React App (CRA) | Officially deprecated by React team; unmaintained | Vite (`npm create vite@latest`) |
| `Base.metadata.create_all()` for production | Bypasses migration history; schema changes will break things | Alembic migrations |
| Tailwind CSS v4 | Completely new config format (breaks Tailwind v3 patterns); ecosystem not caught up | Tailwind CSS v3 |
| Redux Toolkit | Overkill for this 3-role app; adds complexity without benefit | TanStack Query for server state + React Context for auth state |
| Django / Django REST Framework | Decided against; heavier, different architecture than FastAPI | FastAPI (already decided) |
| Tortoise ORM / Databases library | Less documentation, smaller community than SQLAlchemy | SQLAlchemy 2.0 |
| flask-jwt-extended | Flask ecosystem, not FastAPI | PyJWT with FastAPI dependency injection |
| Chakra UI | Heavier than shadcn/ui; moved toward paid tier | shadcn/ui + Tailwind CSS |

---

## Stack Patterns by Variant

**For the SQLite + async FastAPI combination:**
- Use `aiosqlite` as the async driver: `uv add aiosqlite`
- Configure SQLAlchemy engine as: `create_async_engine("sqlite+aiosqlite:///./school.db")`
- Enable WAL mode at startup via `PRAGMA journal_mode=WAL` (improves concurrent read performance)
- Always set `connect_args={"check_same_thread": False}` to avoid thread errors in FastAPI

**For JWT authentication with 3 user roles:**
- Store `role` claim in the JWT payload: `{"sub": user_email, "role": "admin"|"teacher"|"parent"}`
- Create a FastAPI dependency `get_current_user(role: str)` that validates the token and checks the role
- Never authorize by role in business logic — always use the dependency injection layer

**For the React multi-portal frontend:**
- Use React Router 6 layouts to nest role-specific routes under protected route wrappers
- One Axios instance per app (not per component); configure `Authorization` header via interceptor from localStorage/context
- Use TanStack Query `queryKey` scoping by role: e.g. `["grades", studentId]` so cache invalidates correctly

**For Alembic + SQLite:**
- Always use `render_as_batch=True` in `alembic/env.py` — SQLite cannot alter columns without batch mode
- Run `alembic upgrade head` on app startup in development (never in production without review)

---

## Version Compatibility

| Package | Compatible With | Notes |
|---------|-----------------|-------|
| FastAPI 0.136.x | Pydantic >= 2.7.0 | FastAPI dropped Pydantic v1 support; do not mix |
| SQLAlchemy 2.0 | Alembic 1.13+ | Alembic 1.13+ required for full SQLAlchemy 2.0 support |
| SQLAlchemy 2.0 async | aiosqlite 0.20+ | Required async SQLite driver |
| React 18.x | React Router 6.x | React Router 7.x targets React 19; stay on 6.x for React 18 |
| TanStack Query 5.x | React 18.x | v5 requires React 18+ (uses `useSyncExternalStore`) |
| Tailwind CSS 3.x | shadcn/ui (current) | shadcn/ui is tested against Tailwind v3; do not upgrade to v4 yet |
| PyJWT 2.x | Python 3.10+ | Works with 3.12 without issue |

---

## Project-Specific Conventions (Team of 8)

- **Backend structure:** Organize by domain, not by file type. Use `app/students/`, `app/grades/`, `app/attendance/`, `app/auth/` — each with `router.py`, `models.py`, `schemas.py`, `crud.py`
- **Frontend structure:** Mirror backend domains: `src/features/grades/`, `src/features/attendance/`, `src/features/admin/`
- **API contract:** Generate OpenAPI types for frontend using `openapi-typescript` or share Zod schemas manually — prevents drift between backend response and frontend expectations
- **Environment config:** Backend reads from `.env` via `pydantic-settings`; Frontend reads from `.env.local` via Vite's `import.meta.env`
- **CORS:** Configure `CORSMiddleware` in FastAPI with explicit `allow_origins` — never use `["*"]` in production

---

## Sources

- https://fastapi.tiangolo.com/tutorial/sql-databases/ — Official FastAPI SQL integration guide (verified)
- https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/ — Official JWT auth guide (updated to PyJWT)
- https://fastapi.tiangolo.com/tutorial/cors/ — CORS configuration (official)
- https://github.com/fastapi/fastapi/pull/11589 — PR confirming PyJWT replaces python-jose in FastAPI docs (HIGH confidence)
- https://github.com/fastapi/fastapi/discussions/11345 — Community discussion on python-jose abandonment (HIGH confidence)
- https://chaoticengineer.hashnode.dev/fastapi-sqlalchemy — SQLAlchemy 2.0 + FastAPI patterns (MEDIUM confidence)
- https://tanstack.com/router/latest — TanStack Router official docs
- https://www.robinwieruch.de/react-libraries/ — React Libraries 2025 guide (MEDIUM confidence, well-maintained annual article)
- https://blog.logrocket.com/axios-vs-fetch-2025/ — Axios vs fetch 2025 comparison (MEDIUM confidence)
- https://zod.dev/ — Zod official docs
- https://react-hook-form.com/get-started — React Hook Form official docs
- https://pypi.org/project/fastapi/ — FastAPI PyPI (version 0.136.x confirmed)
- https://matduggan.com/sqlite-for-a-rest-api-database/ — SQLite for REST APIs analysis (MEDIUM confidence)
- https://blog.greeden.me/en/2025/08/12/no-fail-guide-getting-started-with-database-migrations-fastapi-x-sqlalchemy-x-alembic/ — Alembic + SQLite WAL + batch mode (MEDIUM confidence)

---
*Stack research for: Sistema Web de Registro Escolar (UNIVESP PJI110, Polo Valinhos)*
*Researched: 2026-04-26*
