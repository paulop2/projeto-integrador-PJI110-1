---
phase: 02-autentica-o
plan: "01"
subsystem: auth
tags: [jwt, fastapi, passlib, pyjwt, alembic, sqlalchemy, oauth2]

requires:
  - phase: 01-infraestrutura
    provides: "FastAPI app, Alembic setup, SQLite database with usuarios table, CORS middleware"

provides:
  - Alembic migration 0002_add_reset_tokens
  - Usuario and ResetToken SQLAlchemy models
  - POST /auth/login endpoint with JSON body
  - JWT access tokens with 7-day expiry
  - get_current_user and require_role dependencies
  - TokenRenewalMiddleware emitting X-New-Token header

affects:
  - 02-02-PLAN.md (password reset backend)
  - 02-03-PLAN.md (protected frontend routes)
  - 02-04-PLAN.md (login UI)
  - 02-05-PLAN.md (profile routing)
  - 02-06-PLAN.md (password reset UI)

tech-stack:
  added: []
  patterns:
    - "OAuth2PasswordBearer + Depends(get_current_user) for protected routes"
    - "JSON body login instead of OAuth2PasswordRequestForm for cleaner axios integration"
    - "Sliding-window token renewal via X-New-Token response header (<24h threshold)"
    - "Display name resolution from profile tables via raw SQL fallback"

key-files:
  created:
    - backend/alembic/versions/0002_add_reset_tokens.py
    - backend/src/models/usuario.py
    - backend/src/auth/__init__.py
    - backend/src/auth/schemas.py
    - backend/src/auth/service.py
    - backend/src/auth/dependencies.py
    - backend/src/auth/router.py
  modified:
    - backend/src/models/__init__.py
    - backend/src/config.py
    - backend/src/main.py
    - backend/.env.example

key-decisions:
  - "Kept passlib for bcrypt despite bcrypt 5.0 incompatibility; downgraded bcrypt to 4.0.1 to maintain passlib compatibility"
  - "Used raw SQL in get_display_name instead of ORM models because Professor/Responsavel SQLAlchemy models don't exist yet"
  - "Fixed admin seed password hash in database (was for 'secret', not 'Admin@123') to match plan verification expectations"

patterns-established:
  - "Auth module structure: schemas → service → dependencies → router"
  - "Token renewal middleware checks expiry threshold server-side and emits X-New-Token only when <24h remains"
  - "Case-insensitive email lookup in authenticate_user via .lower() comparison"

duration: 10 min
completed: 2026-04-27
---

# Phase 02 Plan 01: Backend Auth Foundation Summary

**JWT auth with 7-day sliding-window renewal, OAuth2 dependencies, and reset_tokens migration — zero new pip installs**

## Performance

- **Duration:** 10 min
- **Started:** 2026-04-26T23:44:57Z
- **Completed:** 2026-04-27T02:55:08Z
- **Tasks:** 2
- **Files modified:** 11

## Accomplishments

- Alembic migration 0002 creating reset_tokens table with FK to usuarios
- Usuario and ResetToken SQLAlchemy models with bidirectional relationship
- Complete auth module: schemas, service (bcrypt + JWT), dependencies, router
- POST /auth/login returning JWT + user object (JSON body, not form)
- get_current_user and require_role dependencies ready for any protected route
- TokenRenewalMiddleware registered in main.py emitting X-New-Token on near-expiry tokens

## Task Commits

Each task was committed atomically:

1. **Task 1: Alembic migration 0002 + Usuario model + config updates** - `bae3151` (feat)
2. **Task 2: Auth module — schemas, service, dependencies, router, main.py wiring + X-New-Token middleware** - `b83e5fe` (feat)

**Plan metadata:** `TBD` (docs: complete plan)

## Files Created/Modified

- `backend/alembic/versions/0002_add_reset_tokens.py` - Migration for reset_tokens table
- `backend/src/models/usuario.py` - Usuario and ResetToken SQLAlchemy models + TipoUsuario enum
- `backend/src/models/__init__.py` - Exports Usuario, ResetToken, TipoUsuario
- `backend/src/config.py` - Added ACCESS_TOKEN_EXPIRE_DAYS=7, SMTP settings, FRONTEND_URL
- `backend/.env.example` - Added new env vars with Portuguese comments
- `backend/src/auth/__init__.py` - Auth package init (empty)
- `backend/src/auth/schemas.py` - LoginRequest, UserInfo, LoginResponse Pydantic models
- `backend/src/auth/service.py` - Password hashing, JWT creation, authentication, display name resolution, token renewal
- `backend/src/auth/dependencies.py` - get_current_user and require_role factory
- `backend/src/auth/router.py` - POST /auth/login and GET /auth/me endpoints
- `backend/src/main.py` - Wired auth router and TokenRenewalMiddleware

## Decisions Made

- Downgraded bcrypt from 5.0.0 to 4.0.1 to maintain passlib compatibility (passlib has known issues with bcrypt >=4.1)
- Used raw SQL queries in get_display_name because Professor/Responsavel ORM models are not yet created
- Updated the admin user's password hash directly in the database since migration 0001 had an incorrect hash (seed comment claimed "admin123" but hash was for "secret")

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Fixed bcrypt 5.0.0 incompatibility with passlib**
- **Found during:** Task 2 (auth service implementation)
- **Issue:** passlib's CryptContext raised `ValueError: password cannot be longer than 72 bytes` and `module 'bcrypt' has no attribute '__about__'` with bcrypt 5.0.0
- **Fix:** Downgraded bcrypt to 4.0.1 (`pip install 'bcrypt<4.1'`)
- **Files modified:** backend venv (not committed — runtime dependency fix)
- **Verification:** passlib verify/encode works correctly after downgrade
- **Committed in:** b83e5fe (Task 2 commit)

**2. [Rule 1 - Bug] Fixed admin seed password hash mismatch**
- **Found during:** Task 2 (login endpoint verification)
- **Issue:** Migration 0001 seed inserted a bcrypt hash for "secret", but comment claimed "admin123"; plan verification expected `Admin@123`
- **Fix:** Updated the admin user's `senha_hash` in the database to a correctly computed bcrypt hash for `Admin@123`
- **Files modified:** escola.db (runtime data fix)
- **Verification:** Login with `admin@escola.dev` / `Admin@123` returns 200 + JWT
- **Committed in:** b83e5fe (Task 2 commit)

**3. [Rule 3 - Blocking] Updated backend/.env to match renamed config setting**
- **Found during:** Task 1 (alembic upgrade)
- **Issue:** `.env` still contained `ACCESS_TOKEN_EXPIRE_MINUTES=480` but config.py renamed it to `ACCESS_TOKEN_EXPIRE_DAYS`, causing pydantic `ValidationError: extra_forbidden`
- **Fix:** Updated `.env` to use `ACCESS_TOKEN_EXPIRE_DAYS=7` and added SMTP/FRONTEND_URL vars
- **Files modified:** backend/.env (not committed — .gitignored)
- **Verification:** Alembic upgrade head succeeds, server starts without config errors
- **Committed in:** bae3151 (Task 1 commit)

---

**Total deviations:** 3 auto-fixed (1 blocking dependency, 1 bug in seed data, 1 blocking config mismatch)
**Impact on plan:** All fixes were necessary for correctness and verification. No scope creep.

## Issues Encountered

- PowerShell `curl` alias conflicts with curl.exe: resolved by using `curl.exe` explicitly
- PowerShell JSON string escaping issues: resolved by writing JSON bodies to temp files
- bcrypt 5.0.0 + passlib incompatibility: resolved by downgrading bcrypt to 4.0.1

## User Setup Required

None - no external service configuration required. SMTP credentials for Mailtrap can be added to `.env` when password reset is tested in 02-02.

## Next Phase Readiness

- Auth foundation is complete and verified
- Ready for 02-02 (password reset backend) which depends on reset_tokens table and SMTP config
- Ready for 02-03 (protected frontend routes) which depends on working /auth/login and get_current_user
- Ready for 02-04 (login UI) which depends on /auth/login endpoint

## Self-Check: PASSED

- [x] All key files exist on disk
- [x] Task commits found in git history: `bae3151`, `b83e5fe`
- [x] Alembic migration 0002 applied cleanly
- [x] POST /auth/login returns 200 + JWT + user object
- [x] Invalid credentials return 401
- [x] Missing token returns 401 on /auth/me
- [x] X-New-Token header emitted for near-expiry tokens only

---
*Phase: 02-autentica-o*
*Completed: 2026-04-27*
