---
phase: 02-autentica-o
plan: "02"
subsystem: auth
tags: [fastapi, sqlalchemy, smtplib, mailtrap, password-reset, opaque-tokens]

requires:
  - phase: 02-autentica-o
    provides: "Usuario model, JWT auth service, database with reset_tokens migration"
provides:
  - "POST /auth/forgot-password endpoint — generates single-use opaque token, sends email via Mailtrap SMTP"
  - "POST /auth/reset-password endpoint — validates token, updates password, returns JWT for auto-login"
  - "Password reset service with generate_reset_token, send_reset_email, validate_and_consume_token, update_password"
affects:
  - 02-autentica-o
  - frontend (will consume /auth/forgot-password and /auth/reset-password)

tech-stack:
  added: []
  patterns:
    - "Opaque tokens for password reset (not JWTs) enabling true invalidation and single-use semantics"
    - "Email existence hiding — identical 200 response for known and unknown emails"
    - "Dev fallback: prints reset link to stdout when SMTP not configured"

key-files:
  created:
    - backend/src/password_reset/__init__.py
    - backend/src/password_reset/schemas.py
    - backend/src/password_reset/service.py
    - backend/src/password_reset/router.py
  modified:
    - backend/src/main.py

key-decisions:
  - "Used timezone-aware datetime comparison with fallback for naive SQLite datetimes to prevent runtime TypeError"

patterns-established:
  - "Service layer handles token lifecycle (generate, validate, consume, invalidate)"
  - "Router delegates to service, returns consistent responses to prevent information leakage"

# Metrics
duration: 5min
completed: 2026-04-27
---

# Phase 02 Plan 02: Password Reset Flow Summary

**Password reset with single-use opaque tokens, Mailtrap SMTP integration, and auto-login JWT issuance upon successful reset**

## Performance

- **Duration:** 5 min
- **Started:** 2026-04-27T00:04:50Z
- **Completed:** 2026-04-27T00:09:52Z
- **Tasks:** 2
- **Files modified:** 5

## Accomplishments
- Secure forgot-password endpoint that does not reveal email existence
- Single-use opaque reset tokens with 24-hour expiration stored in reset_tokens table
- Automatic invalidation of previous unused tokens when requesting a new reset
- Reset-password endpoint validates token, updates hash, and issues JWT for immediate auto-login
- Dev fallback prints reset link to stdout when SMTP credentials are not configured

## Task Commits

Each task was committed atomically:

1. **Task 1: Password reset service + schemas** — `a9300fa` (feat)
2. **Task 2: Password reset router + main.py wiring** — `9cc6d2b` (feat)

**Plan metadata:** `[to be committed]` (docs: complete plan)

## Self-Check: PASSED
- All created files exist on disk
- All commits verified in git log

## Files Created/Modified
- `backend/src/password_reset/__init__.py` — Package init
- `backend/src/password_reset/schemas.py` — Pydantic schemas for forgot/reset password requests and responses
- `backend/src/password_reset/service.py` — Token generation, SMTP email sending, token validation/consumption, password update
- `backend/src/password_reset/router.py` — FastAPI routes for POST /auth/forgot-password and POST /auth/reset-password
- `backend/src/main.py` — Wired reset_router under /auth prefix

## Decisions Made
- Fixed timezone-aware vs naive datetime comparison for SQLite compatibility during token expiration check

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed timezone-aware datetime comparison with naive SQLite datetimes**
- **Found during:** Task 1 (Password reset service + schemas)
- **Issue:** `reset_token.expira_em < datetime.now(timezone.utc)` raised `TypeError: can't compare offset-naive and offset-aware datetimes` because SQLite stores naive datetimes
- **Fix:** Added tzinfo check in `validate_and_consume_token`: if `expira_em.tzinfo is None`, replace with `timezone.utc` before comparison
- **Files modified:** backend/src/password_reset/service.py
- **Verification:** Service verification script passed after fix (token generated, valid, reuse blocked)
- **Committed in:** a9300fa (Task 1 commit)

---

**Total deviations:** 1 auto-fixed (1 bug)
**Impact on plan:** Necessary fix for SQLite compatibility. No scope creep.

## Issues Encountered
- None beyond the datetime comparison issue which was auto-fixed

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- Password reset flow is complete and ready for frontend integration
- Frontend will need pages for /redefinir-senha?token=<token> and forgot-password form

---
*Phase: 02-autentica-o*
*Completed: 2026-04-27*
