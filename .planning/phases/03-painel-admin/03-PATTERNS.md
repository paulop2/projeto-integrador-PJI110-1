# Phase 3: Painel Admin - Pattern Map

**Mapped:** 2026-04-27
**Files analyzed:** 27 (13 backend, 14 frontend)
**Analogs found:** 24 / 27

---

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `backend/src/models/aluno.py` | model | CRUD | `backend/src/models/usuario.py` | exact |
| `backend/src/models/turma.py` | model | CRUD | `backend/src/models/usuario.py` | exact |
| `backend/src/models/disciplina.py` | model | CRUD | `backend/src/models/usuario.py` | exact |
| `backend/src/models/professor.py` | model | CRUD | `backend/src/models/usuario.py` | exact |
| `backend/src/models/responsavel.py` | model | CRUD | `backend/src/models/usuario.py` | exact |
| `backend/src/models/__init__.py` | config | — | `backend/src/models/__init__.py` | exact (modify) |
| `backend/src/admin/__init__.py` | config | — | `backend/src/auth/__init__.py` | exact |
| `backend/src/admin/router.py` | route | request-response | `backend/src/auth/router.py` | role-match |
| `backend/src/admin/schemas.py` | model | request-response | `backend/src/auth/schemas.py` | role-match |
| `backend/src/admin/service.py` | service | CRUD | `backend/src/password_reset/service.py` | role-match |
| `backend/alembic/versions/0003_add_matricula_to_alunos.py` | migration | — | `backend/alembic/versions/0002_add_reset_tokens.py` | role-match |
| `backend/src/main.py` | config | — | `backend/src/main.py` | exact (modify) |
| `backend/tests/__init__.py` | config | — | `backend/src/auth/__init__.py` | role-match |
| `backend/tests/conftest.py` | test | request-response | — | no analog |
| `backend/tests/test_admin.py` | test | request-response | — | no analog |
| `frontend/src/components/admin/AdminLayout.tsx` | component | request-response | `frontend/src/components/AppLayout.tsx` | role-match |
| `frontend/src/components/admin/Sidebar.tsx` | component | request-response | `frontend/src/components/AppLayout.tsx` | partial-match |
| `frontend/src/components/admin/EntityTable.tsx` | component | CRUD | `frontend/src/pages/LoginPage.tsx` | partial-match |
| `frontend/src/components/admin/Modal.tsx` | component | request-response | `frontend/src/components/AppLayout.tsx` | partial-match |
| `frontend/src/components/admin/ConfirmDialog.tsx` | component | request-response | `frontend/src/components/AppLayout.tsx` | partial-match |
| `frontend/src/pages/admin/AdminDashboard.tsx` | component | request-response | `frontend/src/pages/dashboards/AdminDashboard.tsx` | exact (replace) |
| `frontend/src/pages/admin/AlunosPage.tsx` | component | CRUD | `frontend/src/pages/LoginPage.tsx` | partial-match |
| `frontend/src/pages/admin/TurmasPage.tsx` | component | CRUD | `frontend/src/pages/LoginPage.tsx` | partial-match |
| `frontend/src/pages/admin/DisciplinasPage.tsx` | component | CRUD | `frontend/src/pages/LoginPage.tsx` | partial-match |
| `frontend/src/pages/admin/ProfessoresPage.tsx` | component | CRUD | `frontend/src/pages/LoginPage.tsx` | partial-match |
| `frontend/src/pages/admin/ResponsaveisPage.tsx` | component | CRUD | `frontend/src/pages/LoginPage.tsx` | partial-match |
| `frontend/src/App.tsx` | config | — | `frontend/src/App.tsx` | exact (modify) |

---

## Pattern Assignments

### `backend/src/models/aluno.py` (model, CRUD)

**Analog:** `backend/src/models/usuario.py`

**Imports pattern** (lines 1-8):
```python
import enum
from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
```

**Core model pattern** (lines 17-31):
```python
class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    tipo: Mapped[TipoUsuario] = mapped_column(nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
```

**FK + relationship pattern** (lines 29-31, 34-41):
```python
    reset_tokens: Mapped[List["ResetToken"]] = relationship(
        "ResetToken", back_populates="usuario"
    )

# FK column pattern from ResetToken:
    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False
    )
```

**Adaptation notes for Aluno:**
- Use `ForeignKey("responsaveis.id", ondelete="SET NULL")` and `ForeignKey("turmas.id", ondelete="SET NULL")` — both nullable
- Add `matricula: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)` after `id`
- Add `data_nascimento: Mapped[date | None] = mapped_column(Date, nullable=True)`
- `ativo` column is already present in DB schema (migration 0001) — copy directly from Usuario pattern

---

### `backend/src/models/turma.py`, `disciplina.py` (model, CRUD)

**Analog:** `backend/src/models/usuario.py`

Same `Mapped`/`mapped_column` pattern. These models have no FK columns — simple flat tables:

- `Turma`: `id`, `nome` (String 100), `ano` (Integer), `serie` (String 50), `turno` (String 20)
- `Disciplina`: `id`, `nome` (String 100), `carga_horaria` (Integer, nullable)

Match the `__tablename__` exactly to the migration: `"turmas"` and `"disciplinas"`.

---

### `backend/src/models/professor.py`, `responsavel.py` (model, CRUD)

**Analog:** `backend/src/models/usuario.py` (ResetToken sub-model portion)

These are profile tables with a 1:1 FK to `usuarios.id`:

```python
# FK pattern from ResetToken (lines 36-40):
    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False
    )
    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="reset_tokens")
```

**Adaptation:**
- `Professor.__tablename__ = "professores"` — fields: `id`, `usuario_id`, `nome` (String 255), `cpf` (String 14, nullable)
- `Responsavel.__tablename__ = "responsaveis"` — fields: `id`, `usuario_id`, `nome` (String 255), `cpf` (String 14, nullable), `telefone` (String 20, nullable)
- `UniqueConstraint` on `usuario_id` (already in migration, must mirror in model)

---

### `backend/src/models/__init__.py` (config, modify)

**Analog:** `backend/src/models/__init__.py` (lines 1-3)

Current content:
```python
from src.models.usuario import Usuario, ResetToken, TipoUsuario

__all__ = ["Usuario", "ResetToken", "TipoUsuario"]
```

**Modification:** Add imports for all new models so Alembic autogenerate can detect them:
```python
from src.models.usuario import Usuario, ResetToken, TipoUsuario
from src.models.aluno import Aluno
from src.models.turma import Turma
from src.models.disciplina import Disciplina
from src.models.professor import Professor
from src.models.responsavel import Responsavel

__all__ = ["Usuario", "ResetToken", "TipoUsuario", "Aluno", "Turma", "Disciplina", "Professor", "Responsavel"]
```

---

### `backend/src/admin/__init__.py` (config)

**Analog:** `backend/src/auth/__init__.py`

The auth `__init__.py` is an empty package marker. The admin one should be too:
```python
# empty — package marker
```

---

### `backend/src/admin/schemas.py` (model, request-response)

**Analog:** `backend/src/auth/schemas.py`

**Imports pattern** (lines 1-2):
```python
from pydantic import BaseModel, EmailStr
```

**Schema pattern** (lines 4-19):
```python
class LoginRequest(BaseModel):
    email: EmailStr
    senha: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserInfo
```

**Adaptation for admin schemas:**
- All schemas use `BaseModel` only — no `model_config` needed unless reading from ORM, in which case add `model_config = ConfigDict(from_attributes=True)` to `Out` classes (Pydantic v2 pattern replacing `orm_mode`)
- Pattern: `XxxCreate`, `XxxUpdate` (all fields `Optional`), `XxxOut` (includes computed fields like `turma_nome`), `PaginatedXxx` (wraps list with `total`, `page`, `per_page`)
- Import `from typing import Optional` and `from datetime import date` as needed

**Critical Pydantic v2 detail — ORM output schemas:**
```python
from pydantic import BaseModel, ConfigDict
from typing import Optional

class AlunoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # replaces orm_mode=True

    id: int
    matricula: str
    nome: str
    ativo: bool
    # ... other fields
```

---

### `backend/src/admin/router.py` (route, request-response)

**Analog:** `backend/src/auth/router.py`

**Imports pattern** (lines 1-9):
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.auth.schemas import LoginRequest, LoginResponse, UserInfo
from src.auth.service import authenticate_user, create_access_token, get_display_name
from src.auth.dependencies import get_current_user
from src.database import get_db
from src.models.usuario import Usuario

router = APIRouter(prefix="/auth", tags=["auth"])
```

**Route handler pattern** (lines 13-32):
```python
@router.post("/login", response_model=LoginResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, body.email, body.senha)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
        )
    ...
    return LoginResponse(...)
```

**Adaptation for admin router:**
- `router = APIRouter(prefix="/admin", tags=["admin"])`
- Auth guard pattern: `admin_required = Depends(require_role("admin"))` — import `require_role` from `src.auth.dependencies`
- Query params via `Query` import from fastapi: `page: int = Query(1, ge=1)`, `search: str = Query("")`
- Use `status_code=201` on POST create endpoints
- HTTPException for not-found: `raise HTTPException(status_code=404, detail="Não encontrado")`

**second analog** — `backend/src/password_reset/router.py` shows the same session injection pattern but for a different module, confirming `db: Session = Depends(get_db)` is the consistent pattern.

---

### `backend/src/admin/service.py` (service, CRUD)

**Analog:** `backend/src/password_reset/service.py`

**Imports pattern** (lines 1-12):
```python
import secrets
import smtplib
from datetime import datetime, timedelta, timezone
...
from sqlalchemy.orm import Session

from src.auth.service import hash_password
from src.config import settings
from src.models.usuario import Usuario, ResetToken
```

**Session usage pattern** (lines 14-34):
```python
def generate_reset_token(db: Session, email: str) -> str | None:
    user = db.query(Usuario).filter(Usuario.email == email.lower()).first()
    if not user:
        return None
    # Delete existing...
    db.query(ResetToken).filter_by(usuario_id=user.id, usado=False).delete()
    # Add new...
    reset_token = ResetToken(...)
    db.add(reset_token)
    db.commit()
    return token
```

**Password hash reuse** (line 9):
```python
from src.auth.service import hash_password
```

**update_password pattern** (lines 84-86):
```python
def update_password(db: Session, user: Usuario, nova_senha: str) -> None:
    user.senha_hash = hash_password(nova_senha)
    db.commit()
```

**Adaptation for admin service:**
- Use `db.query(Model)` style (legacy 1.x style — consistent with existing codebase) rather than `db.scalars(select(Model))` style
- `db.add()` + `db.commit()` for creates/updates
- `db.flush()` before `db.commit()` when creating Professor/Responsavel atomically (need `usuario.id` before inserting profile row)
- Soft delete: `record.ativo = False; db.commit()` — never `db.delete()`
- Pagination: `offset = (page - 1) * per_page` then `.offset(offset).limit(per_page)` on the query
- Password hashing: `from src.auth.service import hash_password` — reuse, do not redefine

---

### `backend/alembic/versions/0003_add_matricula_to_alunos.py` (migration)

**Analog:** `backend/alembic/versions/0002_add_reset_tokens.py`

**Migration header pattern** (lines 1-12):
```python
"""add reset_tokens

Revision ID: 0002
Revises: 0001
Create Date: 2026-04-26 00:00:00.000000
...
"""

from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None
```

**Batch mode pattern** — confirmed in `env.py` (lines 36 and 52):
```python
render_as_batch=True,  # CRÍTICO: suporte a ALTER TABLE no SQLite
```

**Adaptation for migration 0003:**
```python
revision = "0003"
down_revision = "0002"

def upgrade() -> None:
    with op.batch_alter_table("alunos") as batch_op:
        batch_op.add_column(sa.Column("matricula", sa.String(20), nullable=True))
        batch_op.create_unique_constraint("uq_alunos_matricula", ["matricula"])

def downgrade() -> None:
    with op.batch_alter_table("alunos") as batch_op:
        batch_op.drop_constraint("uq_alunos_matricula", type_="unique")
        batch_op.drop_column("matricula")
```

Note: `render_as_batch=True` is already set in `env.py` (verified lines 36 and 52) — no change needed there.

---

### `backend/src/main.py` (config, modify)

**Analog:** `backend/src/main.py` (lines 1-55)

**Router registration pattern** (lines 9-12, 47-48):
```python
from src.auth.router import router as auth_router
from src.password_reset.router import router as reset_router

app.include_router(auth_router)
app.include_router(reset_router, prefix="/auth")
```

**Modification:** Add two lines — one import and one `include_router`:
```python
# Add import (after existing router imports):
from src.admin.router import router as admin_router

# Add registration (after existing include_router calls):
app.include_router(admin_router)
```

The admin router already has `prefix="/admin"` in its own definition, so no `prefix=` argument needed here.

---

### `frontend/src/components/admin/AdminLayout.tsx` (component, request-response)

**Analog:** `frontend/src/components/AppLayout.tsx`

**Imports pattern** (lines 1-3):
```typescript
import { useState, useEffect, useRef, useMemo } from 'react'
import { Outlet, Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
```

**Layout wrapper pattern** (lines 46-102):
```typescript
export default function AppLayout() {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <header className="fixed top-0 left-0 right-0 z-50 bg-white shadow-sm border-b border-gray-200">
        ...
      </header>
      <main className="flex-1 pt-16">
        <Outlet />
      </main>
    </div>
  )
}
```

**Adaptation for AdminLayout:**
- Replace `flex-col` wrapper with `flex h-screen` (horizontal split: sidebar + content)
- Import `NavLink` from `react-router-dom` (for active-state styling) instead of `Link`
- Keep `useAuth` for user info and logout in sidebar footer
- `useNavigate` for post-logout redirect
- `<Outlet />` goes in the right-side `<main>` panel

**NavLink active pattern** (copy from RESEARCH.md Pattern 10):
```typescript
<NavLink
  to={item.to}
  end={item.end}
  className={({ isActive }) =>
    `block px-3 py-2 rounded text-sm ${isActive ? 'bg-indigo-600' : 'hover:bg-gray-700'}`
  }
>
```

---

### `frontend/src/components/admin/Sidebar.tsx` (component, request-response)

**Analog:** `frontend/src/components/AppLayout.tsx` (nav portion, lines 48-94)

The `<aside>` / nav section can be extracted into a standalone `Sidebar` component. It receives no props (reads nav items from a local constant array). `AdminLayout` imports and renders it.

**Logout button pattern** (lines 39-44 in AppLayout):
```typescript
const handleLogout = () => {
  setDropdownOpen(false)
  logout()
  navigate('/login', { replace: true })
}
```

**User display pattern** (lines 65 in AppLayout):
```typescript
{user?.nome} ({tipoLabel})
```

---

### `frontend/src/components/admin/Modal.tsx` (component, request-response)

**Analog:** `frontend/src/components/AppLayout.tsx` (overlay/dropdown pattern)

The dropdown overlay in AppLayout (lines 82-92) shows the CSS pattern for overlays:
```typescript
{dropdownOpen && (
  <div className="absolute right-0 mt-2 w-40 bg-white rounded-md shadow-lg border border-gray-200 py-1 z-50">
    ...
  </div>
)}
```

**Adaptation for Modal:** Use `createPortal` to render into `document.body`. Add `fixed inset-0 z-50` backdrop. Use `role="dialog"` and `aria-modal="true"`. Attach keydown listener for ESC key via `useEffect` (pattern exists in AppLayout lines 26-37):
```typescript
useEffect(() => {
  function handleClickOutside(event: MouseEvent) {
    if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
      setDropdownOpen(false)
    }
  }
  if (dropdownOpen) {
    document.addEventListener('mousedown', handleClickOutside)
  }
  return () => {
    document.removeEventListener('mousedown', handleClickOutside)
  }
}, [dropdownOpen])
```

Import `useEffect` from React (already in AppLayout line 1). Import `createPortal` from `react-dom`.

---

### `frontend/src/components/admin/ConfirmDialog.tsx` (component, request-response)

**Analog:** `frontend/src/components/admin/Modal.tsx` (the file being created above)

ConfirmDialog is a thin wrapper over Modal with two buttons (Confirm + Cancel). Copy the Modal component pattern, but:
- Props: `open`, `onClose`, `onConfirm`, `entityName` (to render "Desativar [Nome]? Esta ação pode ser revertida.")
- Two buttons: Cancel (`onClick={onClose}`) and Confirm (`onClick={onConfirm}`, styled red)

---

### `frontend/src/components/admin/EntityTable.tsx` (component, CRUD)

**Analog:** `frontend/src/pages/LoginPage.tsx` (form + submission pattern)

The closest pattern for a data table with loading state is the mutation loading pattern in LoginPage (lines 47-57):
```typescript
const mutation = useMutation({
  mutationFn: (body: ...) => api.post(...).then((r) => r.data),
  onSuccess: (data) => { ... },
  onError: () => { ... },
})
// disabled={mutation.isPending} on the submit button
```

EntityTable is a reusable component receiving:
- `columns: { key: string; label: string }[]`
- `rows: Record<string, unknown>[]`
- `total: number`, `page: number`, `perPage: number`
- `onPageChange: (p: number) => void`
- `onSearch: (q: string) => void`
- `onEdit: (row) => void`, `onDeactivate: (row) => void`
- `isLoading: boolean`

No analog exists for a paginated table — use the RESEARCH.md Pattern 5 (TanStack Query paginated list) in the consuming page components, not inside EntityTable.

---

### `frontend/src/pages/admin/AdminDashboard.tsx` (component, request-response)

**Analog:** `frontend/src/pages/dashboards/AdminDashboard.tsx` (replace/supersede)

Current file (lines 1-11):
```typescript
import { useAuth } from '../../contexts/AuthContext'

export default function AdminDashboard() {
  const { user } = useAuth()
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold">Bem-vindo, {user?.nome}!</h1>
      <p className="text-gray-500 mt-2">Painel do administrador — em breve.</p>
    </div>
  )
}
```

**Adaptation:** The new `AdminDashboard` at `src/pages/admin/AdminDashboard.tsx` replaces this placeholder. It uses `useQuery` to fetch `/admin/dashboard` counts:
```typescript
import { useQuery } from '@tanstack/react-query'
import { api } from '../../services/api'

function useAdminDashboard() {
  return useQuery({
    queryKey: ['admin-dashboard'],
    queryFn: () => api.get('/admin/dashboard').then(r => r.data),
  })
}
```

**`api` import pattern** from `frontend/src/pages/LoginPage.tsx` (line 5):
```typescript
import { api } from '../services/api'
```

**`useMutation` import pattern** from `frontend/src/pages/LoginPage.tsx` (line 3):
```typescript
import { useMutation } from '@tanstack/react-query'
```

---

### `frontend/src/pages/admin/AlunosPage.tsx` et al. (component, CRUD)

**Analog:** `frontend/src/pages/LoginPage.tsx` (mutation + api call + loading state)

All five entity pages (Alunos, Turmas, Disciplinas, Professores, Responsaveis) follow the same structure. The closest existing analog is LoginPage for the mutation + api pattern.

**Api call pattern** (lines 47-57 in LoginPage):
```typescript
const mutation = useMutation({
  mutationFn: (body: { email: string; senha: string }) =>
    api.post('/auth/login', body).then((r) => r.data),
  onSuccess: (data) => {
    login(data.access_token, data.user)
    navigate(`/${data.user.tipo}`, { replace: true })
  },
  onError: () => {
    setLoginError('Email ou senha incorretos')
  },
})
```

**isPending disable pattern** (line 176):
```typescript
disabled={mutation.isPending}
```

**Adaptation for entity pages:**
- Replace `useMutation` for login with `useQuery` for list (import `useQuery, keepPreviousData` from `@tanstack/react-query`)
- Add `useState` for `page` and `search` local state
- `queryKey: ['alunos', { page, search }]` with `placeholderData: keepPreviousData` (v5 API — not `keepPreviousData: true`)
- `useMutation` for create/update/deactivate with `onSuccess: () => { queryClient.invalidateQueries(...); toast.success(...) }`
- `useQueryClient` from `@tanstack/react-query` for cache invalidation
- `toast` from `sonner` for success/error feedback

---

### `frontend/src/App.tsx` (config, modify)

**Analog:** `frontend/src/App.tsx` (lines 1-89)

**Current admin route structure** (lines 44-51):
```typescript
{
  path: '/admin',
  element: <ProtectedRoute allowedRole="admin" />,
  children: [
    {
      element: <AppLayout />,
      children: [{ index: true, element: <AdminDashboard /> }],
    },
  ],
},
```

**Modification:** Replace `AppLayout` with `AdminLayout` for the admin subtree and add child routes:
```typescript
{
  path: '/admin',
  element: <ProtectedRoute allowedRole="admin" />,
  children: [
    {
      element: <AdminLayout />,
      children: [
        { index: true, element: <AdminDashboard /> },
        { path: 'alunos', element: <AlunosPage /> },
        { path: 'turmas', element: <TurmasPage /> },
        { path: 'disciplinas', element: <DisciplinasPage /> },
        { path: 'professores', element: <ProfessoresPage /> },
        { path: 'responsaveis', element: <ResponsaveisPage /> },
      ],
    },
  ],
},
```

Keep `professor` and `responsavel` routes unchanged — they continue to use `AppLayout`.

**Import pattern** (lines 1-10):
```typescript
import { createBrowserRouter, RouterProvider, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import LoginPage from './pages/LoginPage'
// ... existing imports
import AdminLayout from './components/admin/AdminLayout'
import AdminDashboard from './pages/admin/AdminDashboard'
import AlunosPage from './pages/admin/AlunosPage'
// ... other admin page imports
```

---

### `frontend/src/index.css` (config, modify)

**Analog:** `frontend/src/index.css` (lines 1-112)

**Modification:** Prepend three Tailwind directives at the very top of the file:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

These must come before all existing `:root { ... }` content. The existing custom CSS properties and styles remain unchanged below.

---

### `frontend/tailwind.config.js` (config, new)

No analog exists. Use the standard Tailwind v3 ESM config (required since `package.json` has `"type": "module"`, verified line 4):
```js
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: { extend: {} },
  plugins: [],
}
```

Note: `export default` (ESM) not `module.exports =` (CJS) — because `"type": "module"` is set in `package.json`.

---

### `frontend/package.json` (config, modify)

**Analog:** `frontend/package.json` (lines 1-34)

**Modification:** Add to `devDependencies`:
```json
"tailwindcss": "3.4.19",
"postcss": "^8.4.0",
"autoprefixer": "^10.4.0"
```

Add to `dependencies`:
```json
"sonner": "^2.0.7",
"react-hook-form": "^7.74.0",
"zod": "^4.3.6",
"@hookform/resolvers": "^3.9.0"
```

Note: These are added by running the install commands from RESEARCH.md, not by manually editing package.json. The planner should issue the npm install commands; package.json updates automatically.

---

### `backend/tests/__init__.py` (config)

**Analog:** `backend/src/auth/__init__.py`

Empty package marker file. Content: empty (0 bytes) or a single comment.

---

### `backend/tests/conftest.py` (test, request-response)

**No analog in codebase.** No tests directory exists yet.

Use pytest + httpx `TestClient` pattern from FastAPI docs. Key fixtures needed:
- `test_db` — in-memory SQLite engine + session override
- `client` — `TestClient(app)` with DB override
- `admin_headers` — dict with `Authorization: Bearer <token>` for admin user
- `professor_headers` — same for professor role

Reference RESEARCH.md Validation Architecture section for fixture structure.

---

### `backend/tests/test_admin.py` (test, request-response)

**No analog in codebase.** No existing test files.

Test structure follows FastAPI TestClient pattern:
```python
def test_create_aluno(client, admin_headers):
    response = client.post("/admin/alunos", json={...}, headers=admin_headers)
    assert response.status_code == 201
    assert "matricula" in response.json()
```

Reference RESEARCH.md Validation Architecture section for the full test case list.

---

## Shared Patterns

### Authentication Guard (Admin Role)
**Source:** `backend/src/auth/dependencies.py` (lines 37-45)
**Apply to:** All endpoint functions in `backend/src/admin/router.py`

```python
def require_role(role: str):
    def checker(user: Annotated[Usuario, Depends(get_current_user)]):
        if user.tipo.value != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado",
            )
        return user
    return checker
```

Usage in admin router:
```python
from src.auth.dependencies import require_role
admin_required = Depends(require_role("admin"))

# On every endpoint:
@router.get("/alunos", ...)
def list_alunos(db: Session = Depends(get_db), _=admin_required):
    ...
```

### Password Hashing (for Professor/Responsavel creation)
**Source:** `backend/src/auth/service.py` (lines 10, 17-18)
**Apply to:** `backend/src/admin/service.py` (create_professor, create_responsavel functions)

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)
```

Import from auth service — do not redefine:
```python
from src.auth.service import hash_password
```

### Session / DB Dependency
**Source:** `backend/src/database.py` (lines 23-36) + `backend/src/auth/router.py` (lines 7-14)
**Apply to:** All functions in `backend/src/admin/router.py`

```python
# database.py pattern:
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Usage in router:
from src.database import get_db
from sqlalchemy.orm import Session

def some_endpoint(db: Session = Depends(get_db)):
    ...
```

### HTTP Error Handling
**Source:** `backend/src/auth/router.py` (lines 14-21) + `backend/src/password_reset/router.py` (lines 36-38)
**Apply to:** All endpoint functions in `backend/src/admin/router.py`

```python
# 401 pattern (auth):
raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Email ou senha incorretos",
)

# 400 pattern (validation):
raise HTTPException(status_code=400, detail="Senha deve ter pelo menos 8 caracteres")
```

For admin CRUD, the common case is 404:
```python
raise HTTPException(status_code=404, detail="Registro não encontrado")
```

### API Client (Frontend)
**Source:** `frontend/src/services/api.ts` (lines 1-52)
**Apply to:** All frontend page components that call the backend

```typescript
import { api } from '../../services/api'

// GET with params:
api.get('/admin/alunos', { params: { page, search } }).then(r => r.data)

// POST:
api.post('/admin/alunos', body).then(r => r.data)

// PUT:
api.put(`/admin/alunos/${id}`, body).then(r => r.data)

// POST deactivate:
api.post(`/admin/alunos/${id}/deactivate`).then(r => r.data)
```

The `api` instance auto-attaches `Authorization: Bearer <token>` via the request interceptor (lines 11-17 in api.ts). No manual header needed in page components.

### TanStack Query — useMutation pattern
**Source:** `frontend/src/pages/LoginPage.tsx` (lines 47-57)
**Apply to:** All create/update/deactivate operations in admin pages

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { toast } from 'sonner'

const queryClient = useQueryClient()

const mutation = useMutation({
  mutationFn: (body) => api.post('/admin/alunos', body).then(r => r.data),
  onSuccess: async () => {
    await queryClient.invalidateQueries({ queryKey: ['alunos'] })
    toast.success('Aluno criado com sucesso')
  },
  onError: () => {
    toast.error('Erro ao criar aluno')
  },
})

// Disable submit button while pending:
disabled={mutation.isPending}
```

### React Router NavLink (active state)
**Source:** `frontend/src/components/AppLayout.tsx` (lines 51-56) — uses `Link`, but NavLink pattern is similar
**Apply to:** `frontend/src/components/admin/Sidebar.tsx`

```typescript
// AppLayout uses Link; Sidebar uses NavLink for active state:
import { NavLink } from 'react-router-dom'

<NavLink
  to="/admin/alunos"
  className={({ isActive }) =>
    `block px-3 py-2 rounded text-sm ${isActive ? 'bg-indigo-600 text-white' : 'hover:bg-gray-700 text-gray-300'}`
  }
>
  Alunos
</NavLink>
```

### useAuth Hook (Frontend)
**Source:** `frontend/src/contexts/AuthContext.tsx` (lines 81-87)
**Apply to:** `AdminLayout.tsx`, `Sidebar.tsx`, any page that needs user info or logout

```typescript
import { useAuth } from '../../contexts/AuthContext'

const { user, logout } = useAuth()
// user.nome, user.tipo, user.email available
// logout() clears token + user from localStorage + state
```

---

## No Analog Found

| File | Role | Data Flow | Reason |
|---|---|---|---|
| `backend/tests/conftest.py` | test | request-response | No test infrastructure exists in the project yet — no conftest.py or pytest fixtures anywhere |
| `backend/tests/test_admin.py` | test | request-response | No test files exist in the project |
| `frontend/tailwind.config.js` | config | — | Tailwind not installed; no existing config |

---

## Key Observations for Planner

1. **Alembic `render_as_batch=True` is confirmed** in `env.py` at lines 36 and 52. Migration 0003 can use `op.batch_alter_table` without any env.py changes.

2. **`db.query()` (legacy) style is used throughout** `password_reset/service.py` — this is the consistent codebase style. New admin service should match this style even though SQLAlchemy 2.0 style (`db.scalars(select(...))`) also works.

3. **`hash_password` function name** in `auth/service.py` is `hash_password` (line 17), but `authenticate_user` calls it as `hash_password`. The RESEARCH.md calls it `get_password_hash` — the real function name is `hash_password`. Use `from src.auth.service import hash_password`.

4. **`package.json` has `"type": "module"`** (line 4) — `tailwind.config.js` must use `export default {}` syntax (ESM), not `module.exports = {}`.

5. **Existing `AdminDashboard` at `pages/dashboards/AdminDashboard.tsx`** is a placeholder. The new one goes at `pages/admin/AdminDashboard.tsx`. The App.tsx route must be updated to import from the new path. The old file can remain or be deleted — planner should decide.

6. **The `#root` div in `index.css`** has `width: 1126px; max-width: 100%; margin: 0 auto;` which constrains the full-width admin layout. The Tailwind directives prepended to `index.css` don't fix this conflict. The planner should note that `#root` styles may need to be reset for the admin sidebar layout (e.g., override with `max-w-none` or remove the `width` constraint for admin routes).

---

## Metadata

**Analog search scope:** `backend/src/`, `backend/alembic/`, `frontend/src/`
**Files scanned:** 19
**Pattern extraction date:** 2026-04-27
