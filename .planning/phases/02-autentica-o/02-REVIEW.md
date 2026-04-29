---
phase: 02-autentica-o
reviewed: 2026-04-29T12:00:00Z
depth: standard
files_reviewed: 22
files_reviewed_list:
  - backend/.env.example
  - backend/src/auth/__init__.py
  - backend/src/auth/dependencies.py
  - backend/src/auth/router.py
  - backend/src/auth/schemas.py
  - backend/src/auth/service.py
  - backend/src/config.py
  - backend/src/main.py
  - backend/src/models/__init__.py
  - backend/src/models/usuario.py
  - backend/src/password_reset/__init__.py
  - backend/src/password_reset/router.py
  - backend/src/password_reset/schemas.py
  - backend/src/password_reset/service.py
  - frontend/src/App.tsx
  - frontend/src/components/AppLayout.tsx
  - frontend/src/components/ProtectedRoute.tsx
  - frontend/src/contexts/AuthContext.tsx
  - frontend/src/main.tsx
  - frontend/src/pages/ForgotPasswordPage.tsx
  - frontend/src/pages/LoginPage.tsx
  - frontend/src/pages/ResetPasswordPage.tsx
  - frontend/src/pages/dashboards/AdminDashboard.tsx
  - frontend/src/pages/dashboards/ProfessorDashboard.tsx
  - frontend/src/pages/dashboards/ResponsavelDashboard.tsx
  - frontend/src/services/api.ts
findings:
  critical: 3
  warning: 2
  info: 4
  total: 9
status: issues_found
---

# Phase 02: Code Review Report

**Reviewed:** 2026-04-29T12:00:00Z
**Depth:** standard
**Files Reviewed:** 22
**Status:** issues_found

## Summary

Reviewed the authentication and password-reset implementation across the FastAPI backend and React frontend. Found **3 critical issues** that must be fixed before shipping: a JWT parsing crash that leaks 500 errors, an expired-token resurrection vulnerability in the auto-renew middleware, and unhandled SMTP exceptions in the password-reset flow. Additionally identified 2 warnings and 4 info-level items.

## Critical Issues

### CR-01: Unhandled ValueError on malformed JWT `sub` claim causes 500 instead of 401

**File:** `backend/src/auth/dependencies.py:31`
**Issue:** `get_current_user` calls `int(user_id)` on the `sub` claim extracted from the JWT payload. If a token is crafted with a non-numeric `sub` (e.g., `"abc"`), `int()` raises `ValueError`, which is not caught by the surrounding `try/except jwt.InvalidTokenError`. This bubbles up as an HTTP 500, leaking internal server state and bypassing the intended 401 Unauthorized response.
**Fix:**
```python
try:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    user_id_int = int(user_id)
except (jwt.InvalidTokenError, ValueError):
    raise credentials_exception
user = db.get(Usuario, user_id_int)
```

### CR-02: Auto-renew middleware resurrects expired tokens on public endpoints

**File:** `backend/src/auth/service.py:55-66`
**Issue:** `maybe_renew_token` decodes the JWT with `options={"verify_exp": False}`. It then checks whether `(exp - now) < 86400`. For any **already-expired** token, `exp - now` is negative, so the condition is `True`, and a brand-new valid token is issued. Because the `TokenRenewalMiddleware` in `main.py` runs on **every** 2xx response—including public endpoints such as `/health` and `/auth/forgot-password`—an attacker who possesses an expired token can send it to a public endpoint and receive a fresh, valid `X-New-Token` header without any credentials.
**Fix:** Verify expiration before renewing:
```python
def maybe_renew_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return None
    exp = payload.get("exp")
    if not exp:
        return None
    now = datetime.now(timezone.utc).timestamp()
    if exp < now:
        return None  # already expired — do NOT renew
    if (exp - now) < 86400:  # less than 24 h remaining
        new_data = {"sub": payload.get("sub"), "tipo": payload.get("tipo")}
        return create_access_token(new_data)
    return None
```

### CR-03: Unhandled SMTP exceptions in password-reset email cause 500 errors

**File:** `backend/src/password_reset/service.py:61-64`
**Issue:** `send_reset_email` performs SMTP connection, TLS handshake, authentication, and message sending without any exception handling. If the SMTP server is unreachable, credentials are invalid, or the network is down, `smtplib` raises `SMTPException` subclasses that propagate uncaught, resulting in a 500 Internal Server Error for the `/auth/forgot-password` endpoint.
**Fix:** Wrap SMTP operations in a try/except block and raise a domain-specific exception or return gracefully so the router can return a controlled error response:
```python
from smtplib import SMTPException

def send_reset_email(to_email: str, token: str) -> None:
    ...
    if not settings.SMTP_USER:
        print(f"[DEV] Reset link: {reset_url}")
        return

    msg = MIMEMultipart("alternative")
    ...
    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASS)
            server.sendmail(settings.SMTP_SENDER, to_email, msg.as_string())
    except SMTPException as exc:
        # Log the error and re-raise a custom exception or handle gracefully
        raise RuntimeError(f"Failed to send reset email: {exc}") from exc
```

## Warnings

### WR-01: Deprecated `datetime.utcnow` used for SQLAlchemy defaults

**File:** `backend/src/models/usuario.py:26,45`
**Issue:** `datetime.utcnow` is deprecated in Python 3.12+ and returns a **naive** datetime. Mixing naive and timezone-aware datetimes (used elsewhere in the codebase such as `datetime.now(timezone.utc)`) can lead to subtle comparison bugs and future compatibility issues with SQLAlchemy 2.0.
**Fix:** Replace `default=datetime.utcnow` with `default=lambda: datetime.now(timezone.utc)` or use `sqlalchemy.func.now()`.

### WR-02: Weak default `SECRET_KEY` in settings

**File:** `backend/src/config.py:12`
**Issue:** The `Settings` class defines `SECRET_KEY: str = "dev-secret-key-change-in-production"`. If the application is deployed without an explicit `.env` file (a common ops mistake), JWTs are signed with a publicly known, trivially guessable secret, allowing token forgery.
**Fix:** Either remove the default (force env-provided value) or add a startup guard that aborts when `ENVIRONMENT != "development"` and the default secret is still in use.

## Info

### IN-01: `EyeIcon` component duplicated across login and reset pages

**File:** `frontend/src/pages/LoginPage.tsx:7-34` and `frontend/src/pages/ResetPasswordPage.tsx:7-34`
**Issue:** The `EyeIcon` SVG component is defined identically in two separate files. This violates DRY and increases maintenance cost.
**Fix:** Extract `EyeIcon` into a shared component (e.g., `frontend/src/components/icons/EyeIcon.tsx`) and import it in both pages.

### IN-02: Dashboard components in `pages/dashboards/` appear unused

**File:** `frontend/src/pages/dashboards/AdminDashboard.tsx`, `frontend/src/pages/dashboards/ProfessorDashboard.tsx`, `frontend/src/pages/dashboards/ResponsavelDashboard.tsx`
**Issue:** `App.tsx` imports `AdminDashboard` from `./pages/admin/AdminDashboard` and does not import `ProfessorDashboard` or `ResponsavelDashboard` at all. The three files under `pages/dashboards/` are not referenced in the reviewed source tree, suggesting they are dead code.
**Fix:** Remove the unused files or update `App.tsx` to import from the `dashboards/` directory if that is the intended location.

### IN-03: `/auth/me` endpoint lacks explicit response model

**File:** `backend/src/auth/router.py:35-41`
**Issue:** The `me` endpoint returns an inline dictionary. Without a Pydantic response model, the OpenAPI schema is incomplete and there is no runtime validation or documentation of the returned fields.
**Fix:** Add a `response_model=UserInfo` (or a dedicated `MeResponse` schema) to the route decorator.

### IN-04: Untyped `dict` used in password-reset response schema

**File:** `backend/src/password_reset/schemas.py:20`
**Issue:** `ResetPasswordResponse.user` is typed as `dict`, losing all type safety and schema documentation for the nested user object.
**Fix:** Replace `dict` with the existing `UserInfo` schema from `src.auth.schemas`.

---

_Reviewed: 2026-04-29T12:00:00Z_
_Reviewer: gsd-code-reviewer_
_Depth: standard_
