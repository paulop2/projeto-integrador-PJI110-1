---
phase: 01-infraestrutura
reviewed: 2026-04-29T00:00:00Z
depth: standard
files_reviewed: 14
files_reviewed_list:
  - .env.example
  - .gitignore
  - backend/.env.example
  - backend/alembic.ini
  - backend/alembic/README
  - backend/alembic/env.py
  - backend/alembic/script.py.mako
  - backend/alembic/versions/0001_initial_schema.py
  - backend/pyproject.toml
  - backend/requirements.txt
  - backend/src/__init__.py
  - backend/src/config.py
  - backend/src/database.py
  - backend/src/main.py
  - backend/src/models/__init__.py
findings:
  critical: 1
  warning: 9
  info: 3
  total: 13
status: issues_found
---

# Phase 01: Code Review Report

**Reviewed:** 2026-04-29
**Depth:** standard
**Files Reviewed:** 14
**Status:** issues_found

## Summary

This review covers the initial infrastructure and backend scaffolding for the Sistema Escolar API. The codebase establishes a solid FastAPI + SQLAlchemy + Alembic foundation, but contains **one critical security vulnerability** (a hardcoded admin backdoor in a migration) and several warnings related to configuration robustness, inconsistent database URLs between Alembic offline/online modes, and missing defensive error handling in middleware.

## Critical Issues

### CR-01: Hardcoded Admin Backdoor in Production Migration

**File:** `backend/alembic/versions/0001_initial_schema.py:346-356`
**Issue:** The initial schema migration unconditionally seeds a default admin user (`admin@escola.dev`) with a pre-computed bcrypt hash for the known weak password `Admin@123`. Because this lives in a migration script, it will execute in **every** environment (development, staging, production) where `alembic upgrade head` is run, creating a predictable backdoor account. The hash and email are visible in source control, allowing anyone to authenticate as admin.
**Fix:** Remove the seed from the migration. Use a standalone seed script or management command that is gated by environment checks (e.g., only run in development), and generate the hash at runtime rather than hardcoding it.

```python
# Remove this block from the migration:
op.execute(
    """
    INSERT INTO usuarios (email, senha_hash, tipo, ativo)
    VALUES (
        'admin@escola.dev',
        '$2b$12$1mKwUZ5aHQg.DHcmI0KbcuTVrXlC15/dZ6s4SOmUpj/p82q1jeKEe',
        'admin',
        1
    )
    """
)
```

## Warnings

### WR-01: Missing try/finally for Foreign Key Pragma in Alembic

**File:** `backend/alembic/env.py:46-60`
**Issue:** `run_migrations_online()` disables foreign key enforcement (`PRAGMA foreign_keys=OFF`) before running migrations, but if `context.run_migrations()` raises an exception, the code that re-enables foreign keys (`PRAGMA foreign_keys=ON`) is never reached. While the connection will be closed, this is brittle and violates the fail-safe principle.
**Fix:** Wrap the migration execution in a `try/finally` block to guarantee FK enforcement is restored.

```python
def run_migrations_online() -> None:
    with engine.connect() as connection:
        connection.execute(text("PRAGMA foreign_keys=OFF"))
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,
            naming_convention=NAMING_CONVENTION,
        )
        try:
            with context.begin_transaction():
                context.run_migrations()
            connection.commit()
        finally:
            connection.execute(text("PRAGMA foreign_keys=ON"))
```

### WR-02: Inconsistent Database URL Between Offline and Online Migrations

**File:** `backend/alembic/env.py:30` and `backend/alembic.ini:89`
**Issue:** `run_migrations_offline()` reads the database URL from `alembic.ini` (`sqlite:///./escola.db`), while `run_migrations_online()` uses the `engine` object imported from `src.database`, which is configured from `settings.DATABASE_URL`. If `DATABASE_URL` is overridden (e.g., in a test environment or via environment variables), offline migration SQL generation (`alembic revision --autogenerate --sql`) will target a different database than online migrations.
**Fix:** Unify the source of truth. Either read the URL from settings in both modes, or programmatically inject `settings.DATABASE_URL` into the Alembic config at runtime in `env.py`:

```python
from src.config import settings
# In env.py, before run_migrations_offline:
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
```

### WR-03: Relative sys.path in Alembic env.py

**File:** `backend/alembic/env.py:8`
**Issue:** `sys.path.insert(0, ".")` depends on the current working directory. If Alembic is invoked from a directory other than `backend/`, the import `from src.database import Base, engine` will fail because `"src"` won't be found on the path.
**Fix:** Use an absolute path derived from the file's location:

```python
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
```

### WR-04: Relative .env Path in Pydantic Settings

**File:** `backend/src/config.py:7`
**Issue:** `env_file=".env"` is relative to the process's current working directory. If the application is started from outside the `backend/` directory (e.g., `uvicorn backend.src.main:app` from the project root), the `.env` file is not found and the application silently falls back to default values.
**Fix:** Resolve the path relative to the config module file:

```python
from pathlib import Path

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent / ".env",
        env_file_encoding="utf-8",
    )
```

### WR-05: SQLite PRAGMA Event Listener Without Dialect Check

**File:** `backend/src/database.py:13-20`
**Issue:** `set_sqlite_pragmas` executes SQLite-specific `PRAGMA` statements on every new connection without verifying the underlying database dialect. If `DATABASE_URL` is switched to PostgreSQL or MySQL, the event listener will crash on connection because those dialects do not support `PRAGMA journal_mode`.
**Fix:** Guard the pragma execution with a dialect check:

```python
@event.listens_for(engine, "connect")
def set_sqlite_pragmas(dbapi_conn, connection_record):
    if "sqlite" not in str(engine.url):
        return
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA busy_timeout=5000")
    cursor.close()
```

### WR-06: Unprotected Token Renewal in Middleware

**File:** `backend/src/main.py:42`
**Issue:** `maybe_renew_token(token)` is called directly inside `TokenRenewalMiddleware.dispatch` without any exception handling. If the renewal logic raises an exception (e.g., database error, decryption failure, unexpected token format), the middleware will crash and return a 500 Internal Server Error for a request that otherwise succeeded.
**Fix:** Wrap the renewal call in a broad `try/except` to prevent a secondary failure from breaking the response:

```python
class TokenRenewalMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: StarletteRequest, call_next):
        response = await call_next(request)
        if 200 <= response.status_code < 300:
            auth_header = request.headers.get("Authorization", "")
            match = re.match(r"^Bearer\s+(.+)$", auth_header, re.IGNORECASE)
            if match:
                token = match.group(1)
                try:
                    new_token = maybe_renew_token(token)
                    if new_token:
                        response.headers["X-New-Token"] = new_token
                except Exception:
                    pass  # Silently skip renewal on failure
        return response
```

### WR-07: Weak Default SECRET_KEY

**File:** `backend/src/config.py:12`
**Issue:** The `SECRET_KEY` field has a default value of `"dev-secret-key-change-in-production"`. If the application is deployed without explicitly setting `SECRET_KEY` in the environment, JWT tokens will be signed with a publicly known, predictable key, allowing token forgery and authentication bypass.
**Fix:** Remove the default value and require the secret to be provided at startup. For development-only convenience, use a separate `EnvSettings` subclass or explicit environment detection:

```python
SECRET_KEY: str  # No default — pydantic will raise if missing from env
```

### WR-08: Outdated Root .env.example Documentation

**File:** `.env.example:7` and `backend/.env.example:4`
**Issue:** The root `.env.example` references `ACCESS_TOKEN_EXPIRE_MINUTES=480`, while the actual codebase uses `ACCESS_TOKEN_EXPIRE_DAYS=7` (in `backend/.env.example` and `backend/src/config.py`). This inconsistency is confusing for developers setting up the project.
**Fix:** Update the root `.env.example` to match the real configuration key and value:

```
# Backend (backend/.env)
# ACCESS_TOKEN_EXPIRE_DAYS=7
```

### WR-09: SQLite-Specific connect_args Tightly Coupled to Engine

**File:** `backend/src/database.py:8-10`
**Issue:** `create_engine` passes `connect_args={"check_same_thread": False}`, which is a SQLite-only parameter. If the database backend is changed to PostgreSQL, this parameter will be passed to `psycopg2.connect()`, which will raise `TypeError: connect() got an unexpected keyword argument 'check_same_thread'`.
**Fix:** Conditionally set `connect_args` based on the URL dialect, or centralize engine creation logic to handle dialect differences.

## Info

### IN-01: Redundant Unique Index on usuarios.email

**File:** `backend/alembic/versions/0001_initial_schema.py:41,43`
**Issue:** Both a `UniqueConstraint("email")` and a `unique=True` index (`ix_usuarios_email`) are created on the same column. A unique constraint already creates an implicit index in SQLite; the explicit unique index is redundant.
**Fix:** Remove the redundant explicit index:

```python
# Remove this line:
# op.create_index("ix_usuarios_email", "usuarios", ["email"], unique=True)
```

### IN-02: Redundant Unique Index on reset_tokens.token

**File:** `backend/alembic/versions/0001_initial_schema.py:62,71`
**Issue:** Same redundancy as IN-01: a `UniqueConstraint("token")` and a `unique=True` index (`ix_reset_tokens_token`) are both defined.
**Fix:** Remove the redundant explicit index.

### IN-03: @lru_cache Called Without Parentheses

**File:** `backend/src/config.py:28`
**Issue:** `@lru_cache` is used without parentheses (`@lru_cache` instead of `@lru_cache()`). While this shorthand is accepted in Python 3.8+, using the explicit call form is clearer and avoids ambiguity.
**Fix:** Add parentheses:

```python
@lru_cache()
def get_settings() -> Settings:
    return Settings()
```

---

_Reviewed: 2026-04-29_
_Reviewer: gsd-code-reviewer_
_Depth: standard_
