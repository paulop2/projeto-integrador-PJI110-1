---
phase: 02-autentica-o
status: all_fixed
findings_in_scope: 5
fixed: 5
skipped: 0
iteration: 1
fix_scope: critical_warning
---

# Phase 02: Code Review Fix Report

**Generated:** 2026-04-29
**Fix Scope:** Critical + Warning only
**Findings In Scope:** 5
**Fixed:** 5
**Skipped:** 0
**Status:** all_fixed

## Summary

All 5 fixable findings (3 Critical, 2 Warning) from `02-REVIEW.md` have been resolved. Each fix was committed atomically.

## Fixes Applied

### Critical

#### CR-01: Unhandled ValueError on malformed JWT `sub` claim
- **File:** `backend/src/auth/dependencies.py`
- **Action:** Wrapped `int(user_id)` inside the existing `try/except` block and added `ValueError` to the exception tuple.
- **Commit:** `fix(02): handle ValueError on malformed JWT sub claim (CR-01)`

#### CR-02: Auto-renew middleware resurrects expired tokens on public endpoints
- **File:** `backend/src/auth/service.py`
- **Action:** Removed `options={"verify_exp": False}` from `jwt.decode` in `maybe_renew_token`. Added explicit `exp < now` check to return `None` for already-expired tokens.
- **Commit:** `fix(02): verify expiration before renewing tokens (CR-02)`

#### CR-03: Unhandled SMTP exceptions in password-reset email cause 500 errors
- **File:** `backend/src/password_reset/service.py`
- **Action:** Wrapped SMTP connection, TLS, auth, and send operations in `try/except SMTPException`. Added 10-second timeout to `smtplib.SMTP()`. Re-raises as `RuntimeError` with context.
- **Commit:** `fix(02): handle SMTP exceptions in password reset (CR-03)`

### Warnings

#### WR-01: Deprecated `datetime.utcnow` used for SQLAlchemy defaults
- **File:** `backend/src/models/usuario.py`
- **Action:** Replaced `default=datetime.utcnow` with `default=lambda: datetime.now(timezone.utc)` for both `Usuario.criado_em` and `ResetToken.criado_em`. Added `timezone` import.
- **Commit:** `fix(02): replace deprecated datetime.utcnow with timezone-aware default (WR-01)`

#### WR-02: Weak default `SECRET_KEY` in settings
- **File:** `backend/src/config.py`
- **Action:** Added a startup guard after `settings` instantiation that raises `RuntimeError` if `ENVIRONMENT != "development"` and the weak default `SECRET_KEY` is still in use.
- **Commit:** `fix(02): add startup guard for weak default SECRET_KEY (WR-02)`

## Info Findings (Out of Scope)

The following 4 Info-level findings were **not** addressed in this pass (scope = Critical + Warning):

- **IN-01:** `EyeIcon` duplicated across login and reset pages — refactor into shared component.
- **IN-02:** Dashboard components in `pages/dashboards/` appear unused — verify and remove dead code.
- **IN-03:** `/auth/me` endpoint lacks explicit response model — add Pydantic response model.
- **IN-04:** Untyped `dict` used in password-reset response schema — replace with `UserInfo` schema.

To include Info findings in a future fix pass, run:
```
/gsd-code-review-fix 02 --all
```

## Next Steps

- `/gsd-verify-work` — Verify phase completion
- `/gsd-code-review 02` — Re-review code if desired

---

_Fixes applied: 2026-04-29_
_Fixer: OpenCode Agent (gsd-code-fixer workflow)_
