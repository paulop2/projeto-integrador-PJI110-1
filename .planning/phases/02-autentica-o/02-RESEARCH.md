# Phase 2: Autenticação - Research

**Researched:** 2026-04-26
**Domain:** JWT authentication, FastAPI security, React Router v7 protected routes, password reset via email
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

#### Login UX
- Layout split screen: lado esquerdo com nome do sistema + tagline em fundo colorido, lado direito com o formulário
- Toggle de visibilidade de senha (ícone de olho dentro do input)
- Validação on blur — cada campo valida quando o usuário sai dele
- Botão de login mostra spinner e fica desabilitado durante a requisição
- Mensagem de erro de autenticação: Claude decide (preferência por mensagem genérica por segurança)
- Posição do link "Esqueci minha senha": Claude decide

#### Recuperação de Senha
- Fluxo: Claude decide (link por email é mais simples para protótipo)
- Após solicitar: confirmação direta — "Email enviado para xxx@xxx.com"
- Validade do token de recuperação: 24 horas
- Após redefinir senha com sucesso: login automático, redireciona para dashboard do perfil

#### Armazenamento e Expiração de Token
- Storage: **localStorage** (mudança deliberada do sessionStorage original — com prazo longo, persistência entre abas faz sentido)
- Prazo do JWT: 7 dias (referência do usuário: 7–30 dias)
- Renovação: automática — cada requisição bem-sucedida estende o prazo
- Quando token expira ou 401 recebido: redirect silencioso para /login, limpando storage
- Tratamento de 401 no frontend: Claude decide (interceptor axios global)

#### Roteamento por Perfil
- Destinos pós-login: Claude decide (provavelmente rotas distintas — /admin, /professor, /responsavel)
- Dashboard desta fase (Phase 2): placeholder com "Bem-vindo, [nome]!" — conteúdo real vem nas fases seguintes
- Acesso a rota de outro perfil por URL direta: redirect silencioso para o dashboard do próprio perfil
- Logout: menu dropdown do usuário (clica no nome/avatar, aparece opção "Sair")
- Layout base: Claude decide (provavelmente compartilhado, menu/links adaptados por perfil)
- Header logado: Nome + tipo de perfil — ex: "João Silva (Professor)"

### Claude's Discretion
- Mensagem exata de erro de credenciais inválidas
- Posicionamento do link "Esqueci minha senha"
- Fluxo exato de recuperação (link ou OTP)
- Rotas específicas por perfil (/admin, /professor, /responsavel ou variantes)
- Layout base compartilhado vs. layouts distintos por perfil
- Tratamento de 401 via interceptor axios
- Skeletons, spinners e estados de loading nas páginas internas

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope.
</user_constraints>

---

## Summary

This phase implements JWT-based authentication on an existing FastAPI + React stack. The backend already has `PyJWT 2.12.1`, `passlib[bcrypt] 1.7.4`, and `python-multipart 0.0.26` installed, plus `email-validator 2.3.0`. The `usuarios` table (with `email`, `senha_hash`, `tipo` enum, `ativo`, `criado_em`) is already migrated. One critical schema gap: `usuarios` has no `nome` column — display names come from joined `professores.nome` or `responsaveis.nome` profile tables. The admin seed user has no profile row, so the backend must either hardcode "Admin" or do a left-join.

The frontend uses React Router v7.14.2 (with `createBrowserRouter` data API), axios 1.15.2, and TanStack Query 5. The auth architecture follows three layers: (1) `AuthContext` storing decoded user + token in localStorage, (2) a global axios response interceptor clearing state on 401 and redirecting to `/login`, and (3) a `ProtectedRoute` component wrapping role-specific route groups with cross-role redirect.

Password reset uses Python's stdlib `secrets.token_urlsafe(32)` (no new dependency) to generate a 64-char opaque token stored in a new `reset_tokens` table, with `smtplib` + `email.mime` (both stdlib) sending the link via Mailtrap SMTP. PyJWT is already used for access tokens — the reset token should be a separate opaque token, NOT a JWT, to enable single-use invalidation after use.

**Primary recommendation:** Use the FastAPI `OAuth2PasswordBearer` + `Depends(get_current_user)` pattern with `passlib.context.CryptContext(schemes=["bcrypt"])` — all dependencies already installed, zero new backend installs needed except SMTP env vars.

---

## Standard Stack

### Already Installed — Backend
| Library | Version | Purpose | Notes |
|---------|---------|---------|-------|
| PyJWT | 2.12.1 | JWT encode/decode | `import jwt` (not `import PyJWT`) |
| passlib[bcrypt] | 1.7.4 | Password hashing | `CryptContext(schemes=["bcrypt"])` |
| python-multipart | 0.0.26 | Form data parsing | Required for `OAuth2PasswordRequestForm` |
| email-validator | 2.3.0 | Email validation | Used via Pydantic `EmailStr` |
| smtplib | stdlib | Send email | No install needed |
| secrets | stdlib | Reset token generation | No install needed |
| fastapi | 0.136.1 | Web framework | Already configured |

### Already Installed — Frontend
| Library | Version | Purpose | Notes |
|---------|---------|---------|-------|
| react-router-dom | 7.14.2 | Routing + guards | Uses `createBrowserRouter` data API |
| axios | 1.15.2 | HTTP client | Needs interceptor added to `api.ts` |
| @tanstack/react-query | 5.100.5 | Server state + mutations | Use for login/reset mutations |
| react | 19.2.5 | UI framework | |

### New Dependencies Required
**Backend:** None. All required libraries are installed.

**Frontend:** None. However, a password visibility toggle requires no library — use a `useState` + `type` toggle on the input.

**Installation:**
```bash
# No new installs needed.
# Ensure .env has SMTP vars for Mailtrap:
# SMTP_HOST=sandbox.smtp.mailtrap.io
# SMTP_PORT=587
# SMTP_USER=<mailtrap_user>
# SMTP_PASS=<mailtrap_pass>
# SMTP_SENDER=noreply@escola.dev
# FRONTEND_URL=http://localhost:5173
```

---

## Architecture Patterns

### Recommended Project Structure

**Backend additions:**
```
backend/src/
├── auth/
│   ├── __init__.py
│   ├── router.py          # POST /auth/login, /auth/refresh, /auth/logout
│   ├── service.py         # authenticate_user, create_access_token, verify_token
│   ├── dependencies.py    # get_current_user, require_role
│   └── schemas.py         # LoginRequest, TokenResponse, PasswordResetRequest
├── password_reset/
│   ├── __init__.py
│   ├── router.py          # POST /auth/forgot-password, POST /auth/reset-password
│   ├── service.py         # generate_token, send_email, validate_token
│   └── schemas.py         # ForgotPasswordRequest, ResetPasswordRequest
├── models/
│   └── usuario.py         # Usuario SQLAlchemy model (+ ResetToken model)
└── main.py                # include_router for auth
```

**Frontend additions:**
```
frontend/src/
├── contexts/
│   └── AuthContext.tsx    # AuthProvider, useAuth hook
├── services/
│   └── api.ts             # axios instance + interceptors (existing, extend)
├── pages/
│   ├── LoginPage.tsx
│   ├── ForgotPasswordPage.tsx
│   ├── ResetPasswordPage.tsx
│   └── dashboards/
│       ├── AdminDashboard.tsx
│       ├── ProfessorDashboard.tsx
│       └── ResponsavelDashboard.tsx
├── components/
│   └── ProtectedRoute.tsx
└── App.tsx                # router config with route groups
```

### Pattern 1: FastAPI JWT Token Creation and Verification
**What:** Create JWT in login endpoint, verify in dependency injected into all protected routes.
**When to use:** Every protected endpoint uses `Depends(get_current_user)`.

```python
# Source: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/ + PyJWT 2.12.1 docs
from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = settings.SECRET_KEY  # from config.py
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=7))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = db.get(Usuario, user_id)
    if user is None or not user.ativo:
        raise credentials_exception
    return user
```

### Pattern 2: Token Renewal on Every Request
**What:** Sliding window — each successful authenticated response issues a fresh token with reset expiry.
**When to use:** Required by locked decision "each successful request extends the deadline."

```python
# In the login router, add a response header or return new token
# Simplest approach: return new token in every authenticated endpoint response header
from fastapi import Response

def renew_token(user: Usuario, response: Response):
    new_token = create_access_token({"sub": user.id, "tipo": user.tipo.value})
    response.headers["X-New-Token"] = new_token
    return new_token
```

**Frontend side:** The axios response interceptor checks for `X-New-Token` header and updates localStorage.

### Pattern 3: Role-Based Route Guard (React Router v7)
**What:** ProtectedRoute component wrapping route groups in `createBrowserRouter`.
**When to use:** All routes under `/admin`, `/professor`, `/responsavel`.

```typescript
// Source: robinwieruch.de/react-router-private-routes + React Router v7 docs
// components/ProtectedRoute.tsx
import { Navigate, Outlet } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

type Props = {
  allowedRole?: 'admin' | 'professor' | 'responsavel'
  redirectTo?: string
}

export function ProtectedRoute({ allowedRole, redirectTo = '/login' }: Props) {
  const { user } = useAuth()

  if (!user) return <Navigate to="/login" replace />

  if (allowedRole && user.tipo !== allowedRole) {
    // Cross-role access: redirect to own dashboard silently
    return <Navigate to={`/${user.tipo}`} replace />
  }

  return <Outlet />
}
```

```typescript
// App.tsx — createBrowserRouter route structure
export const router = createBrowserRouter([
  { path: '/login', element: <LoginPage /> },
  { path: '/esqueci-senha', element: <ForgotPasswordPage /> },
  { path: '/redefinir-senha', element: <ResetPasswordPage /> },
  {
    element: <ProtectedRoute allowedRole="admin" />,
    children: [{ path: '/admin', element: <AdminDashboard /> }],
  },
  {
    element: <ProtectedRoute allowedRole="professor" />,
    children: [{ path: '/professor', element: <ProfessorDashboard /> }],
  },
  {
    element: <ProtectedRoute allowedRole="responsavel" />,
    children: [{ path: '/responsavel', element: <ResponsavelDashboard /> }],
  },
  { path: '/', element: <Navigate to="/login" replace /> },
  { path: '*', element: <Navigate to="/login" replace /> },
])
```

### Pattern 4: AuthContext with localStorage
**What:** React Context holding decoded user info + token, initialized from localStorage on mount.

```typescript
// contexts/AuthContext.tsx
import { createContext, useContext, useState, useEffect, ReactNode } from 'react'

type AuthUser = {
  id: number
  email: string
  tipo: 'admin' | 'professor' | 'responsavel'
  nome: string
}

type AuthContextType = {
  user: AuthUser | null
  token: string | null
  login: (token: string, user: AuthUser) => void
  logout: () => void
}

const AuthContext = createContext<AuthContextType | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(
    () => localStorage.getItem('token')
  )
  const [user, setUser] = useState<AuthUser | null>(() => {
    const raw = localStorage.getItem('user')
    return raw ? JSON.parse(raw) : null
  })

  const login = (newToken: string, newUser: AuthUser) => {
    localStorage.setItem('token', newToken)
    localStorage.setItem('user', JSON.stringify(newUser))
    setToken(newToken)
    setUser(newUser)
  }

  const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setToken(null)
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
```

### Pattern 5: Axios 401 Interceptor
**What:** Global response interceptor that catches 401 errors, clears storage, and redirects to login.
**When to use:** Applied once to the axios instance in `api.ts`.

```typescript
// services/api.ts — extend existing file
import axios from 'axios'

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: { 'Content-Type': 'application/json' },
})

// Request interceptor: attach token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor: handle 401 + token renewal
api.interceptors.response.use(
  (response) => {
    // Token renewal: pick up X-New-Token header if present
    const newToken = response.headers['x-new-token']
    if (newToken) {
      localStorage.setItem('token', newToken)
    }
    return response
  },
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      // Navigate without React Router (outside component tree)
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)
```

### Pattern 6: Password Reset Token (stdlib only)
**What:** Opaque `secrets.token_urlsafe(32)` stored in DB, separate from JWT. Single-use, 24h TTL.
**Why opaque, not JWT:** A JWT reset token cannot be invalidated after use without a denylist. An opaque token stored in a DB column is trivially invalidated by deleting the row.

```python
# models/usuario.py — add ResetToken model
import secrets
from datetime import datetime, timedelta, timezone
from sqlalchemy import Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

class ResetToken(Base):
    __tablename__ = "reset_tokens"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    token: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    used: Mapped[bool] = mapped_column(Boolean, default=False)

def generate_reset_token(db, usuario_id: int) -> str:
    raw = secrets.token_urlsafe(32)
    db_token = ResetToken(
        usuario_id=usuario_id,
        token=raw,
        expires_at=datetime.now(timezone.utc) + timedelta(hours=24),
    )
    db.add(db_token)
    db.commit()
    return raw
```

```python
# Email sending — smtplib, no new dependency
import smtplib
from email.mime.text import MIMEText

def send_reset_email(to_email: str, reset_link: str):
    msg = MIMEText(
        f"Clique no link para redefinir sua senha (válido por 24h):\n\n{reset_link}\n\n"
        "Se não solicitou, ignore este email.",
        "plain",
        "utf-8",
    )
    msg["Subject"] = "Redefinição de senha — Sistema Escolar"
    msg["From"] = settings.SMTP_SENDER
    msg["To"] = to_email

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.sendmail(settings.SMTP_SENDER, to_email, msg.as_string())
```

### Pattern 7: Display Name Resolution
**What:** `usuarios` has no `nome` column. `nome` lives in `professores` or `responsaveis`. Admin has no profile row.
**How to handle:**

```python
# In the login response, resolve nome from joined tables
def get_display_name(db: Session, user: Usuario) -> str:
    if user.tipo.value == "professor":
        prof = db.query(Professor).filter_by(usuario_id=user.id).first()
        return prof.nome if prof else user.email
    elif user.tipo.value == "responsavel":
        resp = db.query(Responsavel).filter_by(usuario_id=user.id).first()
        return resp.nome if resp else user.email
    else:  # admin
        return "Administrador"
```

Include `nome` and `tipo` in the JWT payload AND in the login response body so the frontend can use it without decoding the token.

### Anti-Patterns to Avoid
- **Decoding JWT on the frontend to get user info:** The login response should return `{ access_token, token_type, user: { id, email, tipo, nome } }`. Store the user object explicitly — do not decode the JWT client-side.
- **Using JWT for password reset tokens:** Cannot be invalidated after single use without a denylist. Use opaque DB tokens instead.
- **Storing sensitive state only in Context (not localStorage):** On page refresh, Context resets. Initialize from localStorage in the `useState` initializer function.
- **Redirecting with React Router `navigate()` inside the axios interceptor:** The interceptor runs outside the React component tree. Use `window.location.href = '/login'` for 401 redirects.
- **OAuth2PasswordRequestForm requires `application/x-www-form-urlencoded`:** The default login form in FastAPI OAuth2 expects form data, not JSON. Either keep the form format or use a custom JSON schema — this project should use JSON (`application/json`) with a custom `LoginRequest` Pydantic model for cleaner frontend integration.
- **Missing `reset_tokens` table in migrations:** Phase 1 created all tables but `reset_tokens` was not in scope. A new Alembic migration (0002) is needed for this table.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Password hashing | Custom hash function | `passlib.context.CryptContext(schemes=["bcrypt"])` | bcrypt timing-safe comparison, salt management, upgrade path |
| JWT signing/validation | Custom HMAC/base64 | `PyJWT 2.12.1` — `jwt.encode()` / `jwt.decode()` | Handles `exp`, `iat`, `sub` claims; catches `InvalidTokenError` |
| Reset token generation | UUID or timestamp hash | `secrets.token_urlsafe(32)` | Cryptographically secure, URL-safe, stdlib |
| Email sending | Raw socket SMTP | `smtplib` + `email.mime` (stdlib) | Battle-tested, supports STARTTLS, no new dependency |
| Password visibility toggle | Custom CSS trick | `useState` + `type` attribute toggle | Two lines of React, no library |
| Form validation | Custom regex per field | HTML5 `onBlur` + Pydantic `EmailStr` (backend) | Pydantic validates on server; `email-validator` already installed |

**Key insight:** The entire auth stack — hashing, JWT, email, token generation — is already available through installed or stdlib packages. Zero new `pip install` calls needed.

---

## Common Pitfalls

### Pitfall 1: `ativo=False` Users Can Log In
**What goes wrong:** Query finds the user, password matches, JWT is issued — but user is deactivated.
**Why it happens:** Forgetting to check `user.ativo` in `authenticate_user`.
**How to avoid:** Always check `if not user.ativo: raise 401` after password verification, and again inside `get_current_user` dependency when loading from token.
**Warning signs:** Admin can create users but cannot deactivate them effectively.

### Pitfall 2: `OAuth2PasswordRequestForm` Requires Form Encoding
**What goes wrong:** Frontend sends JSON to `/auth/login`, FastAPI returns 422 Unprocessable Entity.
**Why it happens:** `OAuth2PasswordRequestForm` parses `application/x-www-form-urlencoded`, not `application/json`.
**How to avoid:** Use a custom Pydantic `LoginRequest` schema with JSON body (`email: str, senha: str`) instead of `OAuth2PasswordRequestForm`. The `OAuth2PasswordBearer` scheme (for token extraction) still works fine — it's only the login endpoint body format that differs.

### Pitfall 3: Token Renewal Creates Race Conditions
**What goes wrong:** Multiple parallel requests each receive a new token header; the last one wins in localStorage — some are silently discarded.
**Why it happens:** Sliding-window renewal on every request with parallel requests.
**How to avoid:** For this prototype, issue a new token only when the current one is within 1 day of expiry (server-side check `exp - now < 86400s`). This dramatically reduces renewal frequency without changing the user-facing behavior.

### Pitfall 4: `window.location.href` on 401 Causes Infinite Loop on `/login`
**What goes wrong:** Login endpoint returns 401 for wrong credentials → interceptor redirects → login page tries to load → ...
**Why it happens:** Interceptor is global and fires on all 401 responses including the login call itself.
**How to avoid:** Exclude `/auth/login`, `/auth/forgot-password`, and `/auth/reset-password` URLs from the redirect logic in the response interceptor.

```typescript
// In the 401 handler:
if (error.response?.status === 401) {
  const url = error.config?.url ?? ''
  const isAuthEndpoint = url.includes('/auth/login') || url.includes('/auth/reset')
  if (!isAuthEndpoint) {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    window.location.href = '/login'
  }
}
```

### Pitfall 5: `usuarios` Has No `nome` Column
**What goes wrong:** JWT payload includes `nome` field but it's not on the `usuarios` row; query fails or returns `null`.
**Why it happens:** Schema design separates identity (`usuarios`) from profile (`professores`, `responsaveis`). Admin has no profile row at all.
**How to avoid:** In the login service, LEFT JOIN profile tables and fall back to `"Administrador"` for admin tipo. Return `nome` in both JWT payload and login response body. Never trust the JWT client-side for display — use the stored `user` object from localStorage.

### Pitfall 6: Reset Token Race — Multiple Valid Tokens
**What goes wrong:** User requests reset twice; both tokens are valid and in the DB; attacker with access to email can use either.
**Why it happens:** Each request generates a new token without invalidating previous ones.
**How to avoid:** On new reset request, `DELETE FROM reset_tokens WHERE usuario_id = ? AND used = false` before inserting the new token. Only one active reset per user.

### Pitfall 7: `reset_tokens` Table Missing — Needs New Migration
**What goes wrong:** `ResetToken` model references a table that doesn't exist in the DB.
**Why it happens:** Phase 1 migration only covered the 11 core tables. `reset_tokens` was not in scope.
**How to avoid:** Create `alembic/versions/0002_add_reset_tokens.py` as the first task of this phase.

---

## Code Examples

### Login Endpoint (JSON body, not form)
```python
# Source: FastAPI docs + project conventions
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.auth.schemas import LoginRequest, LoginResponse
from src.auth.service import authenticate_user, create_access_token, get_display_name

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=LoginResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, body.email, body.senha)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",  # generic message per security preference
        )
    token = create_access_token({"sub": user.id, "tipo": user.tipo.value})
    nome = get_display_name(db, user)
    return LoginResponse(
        access_token=token,
        token_type="bearer",
        user=UserInfo(id=user.id, email=user.email, tipo=user.tipo.value, nome=nome),
    )
```

### Protecting an Endpoint by Role
```python
from fastapi import Depends
from src.auth.dependencies import get_current_user, require_role
from src.models.usuario import Usuario

def require_role(role: str):
    def checker(current_user: Usuario = Depends(get_current_user)):
        if current_user.tipo.value != role:
            raise HTTPException(status_code=403, detail="Acesso negado")
        return current_user
    return checker

@router.get("/admin/dashboard")
def admin_dashboard(user: Usuario = Depends(require_role("admin"))):
    return {"message": f"Bem-vindo, Administrador"}
```

### PyJWT encode/decode (verified against PyJWT 2.12.1 docs)
```python
# Source: https://pyjwt.readthedocs.io/en/latest/usage.html
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

# Encode
token = jwt.encode(
    {"sub": 1, "tipo": "admin", "exp": datetime.now(timezone.utc) + timedelta(days=7)},
    SECRET_KEY,
    algorithm="HS256",
)

# Decode
try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
except ExpiredSignatureError:
    # token expired
    raise HTTPException(status_code=401, detail="Token expirado")
except InvalidTokenError:
    # tampered or malformed
    raise HTTPException(status_code=401, detail="Token inválido")
```

### Login mutation with TanStack Query + AuthContext
```typescript
// Source: TanStack Query v5 docs + axios 1.x
import { useMutation } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { api } from '../services/api'
import { useAuth } from '../contexts/AuthContext'

export function useLogin() {
  const { login } = useAuth()
  const navigate = useNavigate()

  return useMutation({
    mutationFn: (body: { email: string; senha: string }) =>
      api.post('/auth/login', body).then((r) => r.data),
    onSuccess: (data) => {
      login(data.access_token, data.user)
      navigate(`/${data.user.tipo}`, { replace: true })
    },
    // onError handled in the component to show inline error message
  })
}
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `python-jose` for JWT | `PyJWT` directly | ~2023 | `python-jose` has unmaintained deps; FastAPI docs now recommend `PyJWT` or `pwdlib` |
| `BrowserRouter` + `Switch` | `createBrowserRouter` data API | React Router v6.4+ | Loaders, actions, and `<Navigate>` replace `<Redirect>` |
| `jwt.decode()` client-side for user info | Store user object from login response | React best practices | Avoids base64 decode dependency in browser |
| Session cookies | localStorage JWT (deliberate choice per CONTEXT.md) | Project decision | Enables tab persistence; accepted tradeoff for a prototype |
| `OAuth2PasswordRequestForm` (form body) | Custom JSON `LoginRequest` Pydantic model | Project convention | Cleaner axios integration; no `application/x-www-form-urlencoded` |

**Deprecated/outdated in this context:**
- `python-jose`: Not installed, not needed — PyJWT 2.12.1 is already present.
- `sessionStorage`: Locked decision to use localStorage.
- `BrowserRouter` (legacy): Project already uses `createBrowserRouter`.

---

## Claude's Discretion — Recommendations

These areas were left to Claude per CONTEXT.md. Concrete recommendations:

### Error Message for Invalid Credentials
Use: `"Email ou senha incorretos"` — generic enough to not reveal whether email exists, but clearer than "Credenciais inválidas" for a Portuguese-language UI.

### "Esqueci minha senha" Link Position
Place it below the senha input field, right-aligned, as a text link. This is the industry-standard position (seen in Gmail, GitHub, etc.) and keeps it contextually close to the password field.

### Password Reset Flow
Use link-by-email (not OTP). Flow:
1. `POST /auth/forgot-password` — validates email exists, generates opaque token, sends email
2. `GET /redefinir-senha?token=<token>` — frontend page extracts token from URL
3. `POST /auth/reset-password` — body: `{ token, nova_senha }` — validates token, updates hash, issues new JWT, returns `{ access_token, user }` for auto-login

### Routes per Perfil
Use: `/admin`, `/professor`, `/responsavel` — direct, no nesting like `/dashboard/admin`.

### Layout Base
Use a **single shared layout** (`AppLayout`) with the header (`Nome + (Tipo)`) and a sidebar/nav that conditionally renders links based on `user.tipo`. Admin sees user management links, professor sees turmas, responsável sees notas/faltas. This avoids duplicating the header/footer in three files.

### 401 Handling
Global axios response interceptor in `api.ts` (Pattern 5 above). Exclude auth endpoints from the redirect loop.

### Loading States
- Login button: `disabled + spinner` during mutation (locked decision).
- Dashboard placeholder page: no skeleton needed — it's a static "Bem-vindo, [nome]!" with no async data.
- Password reset pages: button spinner during submission only.

---

## Open Questions

1. **Token renewal strategy implementation detail**
   - What we know: "cada requisição bem-sucedida estende o prazo" (locked)
   - What's unclear: Issuing a new token on EVERY request creates overhead. Returning it in a response header is cleaner than in the body.
   - Recommendation: Backend checks if token expires in < 24h; if so, sets `X-New-Token` response header. Frontend interceptor picks it up. This satisfies "automatic renewal" without every response being bloated.

2. **Admin display name**
   - What we know: `usuarios` has no `nome`; admin has no row in `professores` or `responsaveis`
   - What's unclear: Should admin have a configurable name in future phases?
   - Recommendation: Hardcode `"Administrador"` for Phase 2. Header shows "Administrador (Admin)". Future phases can add an `admins` profile table if needed.

3. **`reset_tokens` Alembic migration numbering**
   - What we know: Migration `0001_initial_schema.py` exists
   - What's unclear: Whether to create `0002_add_reset_tokens.py` as a separate migration or whether the Phase 1 team left instructions
   - Recommendation: Create `0002_add_reset_tokens.py` as the first backend task in this phase.

---

## Sources

### Primary (HIGH confidence)
- FastAPI official docs — https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/ — JWT + passlib + OAuth2PasswordBearer pattern
- PyJWT 2.12.1 official docs — https://pyjwt.readthedocs.io/en/latest/usage.html — encode/decode API, ExpiredSignatureError
- Installed packages verified directly from project venv: PyJWT 2.12.1, passlib 1.7.4, python-multipart 0.0.26, email-validator 2.3.0, fastapi 0.136.1
- React Router installed version verified from node_modules: 7.14.2
- Alembic migration `0001_initial_schema.py` read directly — confirmed `usuarios` schema (no `nome`, enum `tipo`, `ativo`, `criado_em`)

### Secondary (MEDIUM confidence)
- Robin Wieruch — https://www.robinwieruch.de/react-router-private-routes/ — ProtectedRoute pattern with `isAllowed` + `<Outlet>` (React Router v7, verified against React Router v7.14.2 API)
- LogRocket — https://blog.logrocket.com/authentication-react-router-v7/ — AuthContext + protected routes pattern
- DEV Community (smtplib) — https://dev.to/dillionhuston/adding-smtp-email-notifications-to-fastapi-using-smtplib-and-environment-variables-4mp8 — verified smtplib pattern (stdlib, no install)

### Tertiary (LOW confidence — verify before use)
- Token renewal via `X-New-Token` header pattern: described in multiple blog posts but not in official FastAPI or axios docs. Verify that `response.headers['x-new-token']` lowercase access works in axios 1.x (HTTP/2 headers are lowercased by browsers; axios normalizes them).

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all library versions verified directly from installed venv and node_modules
- Architecture patterns: HIGH — FastAPI patterns from official docs; React Router patterns from verified v7 sources
- Schema details: HIGH — read directly from Alembic migration file
- Password reset flow: MEDIUM — opaque token pattern well-established, smtplib from official Python stdlib; Mailtrap config from secondary source
- Token renewal header pattern: LOW — common practice but not in official docs; flag for validation

**Research date:** 2026-04-26
**Valid until:** 2026-05-26 (stable libraries; React Router v7 minor releases unlikely to break patterns)
