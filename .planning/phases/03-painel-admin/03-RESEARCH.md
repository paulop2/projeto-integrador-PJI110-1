# Phase 3: Painel Admin - Research

**Researched:** 2026-04-27
**Domain:** FastAPI CRUD routers, SQLAlchemy 2.0 ORM models, React admin panel with sidebar nav, TanStack Query v5 pagination + mutations, modal dialogs, toast notifications
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

#### Navigation & structure
- Sidebar nav (persistent left sidebar with links to each entity section)
- Admin lands on a Dashboard home with summary counts (e.g. "23 alunos, 4 turmas, 2 professores")
- Sidebar order: Dashboard → Alunos → Turmas → Disciplinas → Professores → Responsáveis

#### List & table design
- Pagination: 25 rows per page with prev/next navigation
- Text search on name for every list
- Row actions: Edit button + Deactivate button (no hard delete)
- Alunos table columns: Nome, Matrícula, Turma, Status — other entities follow similar logic (Claude decides columns per entity)

#### Association flows
- Professor → Turma/Disciplina: managed **from the Turma form** using repeating rows of [Disciplina dropdown] + [Professor dropdown]. Admin adds/removes rows as needed.
- Responsável → Aluno: linkable **from both sides** — Responsável form has a multi-select of alunos; Aluno form has a responsável picker.
- Initial password for professor/responsável accounts: admin sets manually during account creation (no email flow at creation time).

#### Form presentation
- All create/edit forms open as **modal dialogs** (overlay on list page)
- Success feedback: toast notification ("Aluno criado com sucesso", disappears after 3s)
- Deactivate action requires a **confirmation dialog** ("Desativar [Nome]? Esta ação pode ser revertida.") with Confirm/Cancel

### Claude's Discretion
- Sidebar collapse/expand behavior (icon-only mode or always expanded)
- Deactivated record visibility default (hidden with toggle vs grayed out always visible)
- Column selection for Turmas, Disciplinas, Professores, Responsáveis tables

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope.
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| ADMIN-01 | Admin pode cadastrar, editar, listar e desativar alunos | Backend: Aluno model + CRUD endpoints with `ativo` flag. Frontend: Alunos list page with pagination, search, edit modal, deactivate confirm |
| ADMIN-02 | Admin pode cadastrar, editar e listar turmas | Backend: Turma model + endpoints. Frontend: Turmas list + create/edit modal with embedded professor_turma rows |
| ADMIN-03 | Admin pode cadastrar, editar e listar disciplinas | Backend: Disciplina model + endpoints. Frontend: Disciplinas list + create/edit modal |
| ADMIN-04 | Admin pode vincular professor a uma turma/disciplina (professor_turma) | Backend: professor_turma junction managed via Turma PUT/POST. Frontend: repeating rows inside Turma form |
| ADMIN-05 | Admin pode criar contas de professores (perfil `professor`) | Backend: creates Usuario(tipo=professor) + Professores profile row atomically. Frontend: Professores list + create/edit modal with manual password field |
| ADMIN-06 | Admin pode criar contas de responsáveis (perfil `responsavel`) e vinculá-los a aluno(s) | Backend: creates Usuario(tipo=responsavel) + Responsaveis profile + updates alunos.responsavel_id. Frontend: Responsáveis list + create/edit modal with aluno multi-select |
</phase_requirements>

---

## Summary

Phase 3 adds the complete admin CRUD panel on top of the working auth foundation from Phase 2. The backend needs six new FastAPI modules (one per entity: alunos, turmas, disciplinas, professores, responsaveis, and a dashboard summary endpoint), each following the established `schemas → service → router` pattern already proven in the auth module. The frontend needs a sidebar layout replacing the current top-only header, six section pages (each with a paginated list + search + modals), and two new npm packages: Sonner (toast) and React Hook Form + Zod (form validation in modals).

**Critical gap discovered:** The `alunos` table has no `matricula` column even though CONTEXT.md explicitly requires it in the table display. [VERIFIED: codebase grep of 0001_initial_schema.py] The initial migration comment claimed the schema was "complete," but `matricula` was omitted. Phase 3 Wave 0 must add Alembic migration 0003 adding `matricula` as a unique string column with auto-generation logic.

**Critical gap discovered:** Tailwind CSS is used throughout existing frontend components (AppLayout.tsx, LoginPage.tsx, etc.) via utility class names but is **not installed as an npm package** and has no config file. [VERIFIED: package.json, package-lock.json, directory listing] Wave 0 must install Tailwind CSS v3 and configure it before any frontend work proceeds.

**Primary recommendation:** Follow the existing module pattern (`auth/`, `password_reset/`) for all six backend modules. Use `require_role("admin")` dependency on every new endpoint. On the frontend, add a `<Sidebar>` component inside `AppLayout` (or a dedicated `AdminLayout`) that renders for admin routes only.

---

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| List/search/paginate entities | API / Backend | — | Filtering and counting happen at the DB layer via SQLAlchemy queries with LIKE + LIMIT/OFFSET |
| CRUD form state | Browser / Client | — | React Hook Form manages local form state; API call on submit |
| Toast notifications | Browser / Client | — | Sonner renders in DOM; triggered by TanStack Query mutation callbacks |
| Modal dialogs | Browser / Client | — | React portal-based overlays; no server involvement |
| `professor_turma` association sync | API / Backend | Browser / Client | Backend receives full list of [disciplina, professor] pairs and replaces junction rows atomically; frontend sends the array |
| `responsavel_id` on alunos | API / Backend | — | FK column; set during create/edit of both Aluno and Responsavel |
| Summary counts (dashboard) | API / Backend | — | Aggregated COUNT queries; single endpoint returns all counts |
| Deactivation (soft delete) | API / Backend | — | `ativo=False` on the record; no hard DELETE used |
| Password hashing for new accounts | API / Backend | — | `passlib.CryptContext` already wired in auth.service; reused here |
| Admin-only access enforcement | API / Backend | — | `Depends(require_role("admin"))` on every new router |

---

## Standard Stack

### Core — Already Installed (Backend)
| Library | Version | Purpose | Notes |
|---------|---------|---------|-------|
| FastAPI | 0.136+ | Router, request parsing, DI | Already configured with CORS + middleware |
| SQLAlchemy | 2.0+ | ORM models, queries | Sync session pattern established |
| Alembic | 1.13+ | Schema migrations | Batch mode for SQLite already configured in env.py |
| passlib[bcrypt] | 1.7.4 | Password hashing for new accounts | Reuse `CryptContext` from auth.service |
| Pydantic | v2 (via FastAPI) | Request/response schemas | Already in use |

### Core — Already Installed (Frontend)
| Library | Version | Purpose | Notes |
|---------|---------|---------|-------|
| @tanstack/react-query | 5.100.5 | Server state, pagination, mutations | `useQuery` with `keepPreviousData` for paginated lists; `useMutation` + `invalidateQueries` for CRUD |
| axios | 1.15.2 | HTTP client | Pre-configured with auth interceptor in api.ts |
| react-router-dom | 7.14.2 | Routing | Nested routes already established |

### New Dependencies Required (Frontend)
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| tailwindcss | 3.4.19 | Utility-first CSS | Already used in all existing components; must be installed to work. Lock on v3 — v4 breaks existing class patterns [VERIFIED: npm registry] |
| postcss | (peer) | Required by Tailwind | Tailwind v3 peer dependency |
| autoprefixer | (peer) | Required by Tailwind | Tailwind v3 peer dependency |
| sonner | 2.0.7 | Toast notifications | Minimal API: `<Toaster />` once at root, `toast("message")` anywhere. Preferred over react-hot-toast for simpler integration [VERIFIED: npm registry] |
| react-hook-form | 7.74.0 | Form state in modals | Uncontrolled inputs, minimal re-renders, reset() on modal close; standard for complex forms [VERIFIED: npm registry] |
| zod | 4.3.6 | Schema validation | Pairs with react-hook-form via `@hookform/resolvers/zod`; Portuguese error messages via `.min(1, "Nome é obrigatório")` [VERIFIED: npm registry] |
| @hookform/resolvers | latest | Bridge between zod and react-hook-form | Required adapter package [ASSUMED] |

**Installation:**
```bash
cd frontend
npm install -D tailwindcss@3 postcss autoprefixer
npx tailwindcss init -p
npm install sonner react-hook-form zod @hookform/resolvers
```

**Tailwind configuration (tailwind.config.js):**
```js
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: { extend: {} },
  plugins: [],
}
```

**Add to src/index.css (prepend these three lines):**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### New Dependencies Required (Backend)
None. All required libraries are already installed.

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| sonner | react-hot-toast | react-hot-toast is older; sonner has cleaner API and better TypeScript support |
| react-hook-form + zod | Controlled inputs with useState | State-per-field approach causes re-renders on every keystroke in modals; react-hook-form is the industry standard |
| Tailwind v3 | Tailwind v4 | v4 has completely different config format (CSS-first, no tailwind.config.js); existing components were written against v3 class API — upgrading would break everything |
| Custom modal with `<dialog>` | @radix-ui/react-dialog or @headlessui/react | For a prototype, a simple CSS-based modal avoids extra dependencies; native `<dialog>` handles focus trapping and ESC — viable alternative if keeping dependencies minimal |

---

## Architecture Patterns

### System Architecture Diagram

```
Browser (Admin user)
       |
       | HTTP (Bearer JWT)
       v
FastAPI (port 8000)
  ├── POST/GET/PUT /admin/alunos         → AlunoService → Session → SQLite
  ├── POST/GET/PUT /admin/turmas         → TurmaService → Session → SQLite
  ├── POST/GET/PUT /admin/disciplinas    → DisciplinaService → Session → SQLite
  ├── POST/GET/PUT /admin/professores    → ProfessorService → Session → SQLite
  ├── POST/GET/PUT /admin/responsaveis   → ResponsavelService → Session → SQLite
  └── GET          /admin/dashboard      → DashboardService → Session → SQLite

React (port 5173)
  ├── AdminLayout (sidebar + outlet)
  │   ├── /admin            → AdminDashboard (summary counts)
  │   ├── /admin/alunos     → AlunosPage (list + modal)
  │   ├── /admin/turmas     → TurmasPage (list + modal with professor_turma rows)
  │   ├── /admin/disciplinas → DisciplinasPage (list + modal)
  │   ├── /admin/professores → ProfessoresPage (list + modal)
  │   └── /admin/responsaveis → ResponsaveisPage (list + modal)
  │
  └── TanStack Query cache
      ├── ['alunos', {page, search}]    → staleTime 5min
      ├── ['turmas', {page, search}]
      ├── ['disciplinas', {page, search}]
      ├── ['professores', {page, search}]
      ├── ['responsaveis', {page, search}]
      └── ['admin-dashboard']
```

### Recommended Project Structure

**Backend additions:**
```
backend/src/
├── models/
│   ├── usuario.py        # existing — Usuario, ResetToken
│   ├── aluno.py          # NEW — Aluno SQLAlchemy model
│   ├── turma.py          # NEW — Turma model
│   ├── disciplina.py     # NEW — Disciplina model
│   ├── professor.py      # NEW — Professor model
│   ├── responsavel.py    # NEW — Responsavel model
│   └── __init__.py       # export all models (needed for Alembic autogenerate)
├── admin/
│   ├── __init__.py
│   ├── router.py         # one file — all admin APIRouter, prefix="/admin"
│   ├── schemas.py        # all Pydantic In/Out schemas for admin entities
│   └── service.py        # all service functions (CRUD logic)
└── main.py               # include_router(admin_router)
```

**Alternative:** One sub-module per entity (alunos/, turmas/, etc.). Given prototype scope, the single `admin/` module is simpler and keeps the planner's task count low.

**Frontend additions:**
```
frontend/src/
├── pages/
│   └── admin/
│       ├── AdminDashboard.tsx      # summary counts (replaces placeholder)
│       ├── AlunosPage.tsx          # list + AlunoModal
│       ├── TurmasPage.tsx          # list + TurmaModal (with professor_turma rows)
│       ├── DisciplinasPage.tsx     # list + DisciplinaModal
│       ├── ProfessoresPage.tsx     # list + ProfessorModal
│       └── ResponsaveisPage.tsx    # list + ResponsavelModal
├── components/
│   ├── admin/
│   │   ├── Sidebar.tsx             # persistent left nav
│   │   ├── AdminLayout.tsx         # sidebar + outlet wrapper
│   │   ├── EntityTable.tsx         # reusable: columns, pagination, search bar
│   │   ├── ConfirmDialog.tsx       # reusable deactivate confirm
│   │   └── Modal.tsx               # reusable modal shell (open/close/title)
│   ├── AppLayout.tsx               # existing — keep for professor/responsavel
│   └── ProtectedRoute.tsx          # existing
└── App.tsx                         # add /admin/* subroutes
```

### Pattern 1: Backend CRUD Module (schemas → service → router)
**What:** The established pattern from `auth/` — schemas define API shapes, service contains business logic, router maps HTTP verbs.
**When to use:** Every entity module follows this pattern.

```python
# Source: established in backend/src/auth/ (Phase 2)
# backend/src/admin/schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import date

class AlunoCreate(BaseModel):
    nome: str
    data_nascimento: Optional[date] = None
    turma_id: Optional[int] = None
    responsavel_id: Optional[int] = None

class AlunoUpdate(BaseModel):
    nome: Optional[str] = None
    data_nascimento: Optional[date] = None
    turma_id: Optional[int] = None
    responsavel_id: Optional[int] = None

class AlunoOut(BaseModel):
    id: int
    matricula: str
    nome: str
    data_nascimento: Optional[date]
    turma_id: Optional[int]
    turma_nome: Optional[str]   # joined from turmas
    responsavel_id: Optional[int]
    ativo: bool

    class Config:
        from_attributes = True  # SQLAlchemy 2.0 — replaces orm_mode
```

```python
# backend/src/admin/router.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src.database import get_db
from src.auth.dependencies import require_role
from . import schemas, service

router = APIRouter(prefix="/admin", tags=["admin"])
admin_required = Depends(require_role("admin"))

@router.get("/alunos", response_model=schemas.PaginatedAlunos)
def list_alunos(
    page: int = Query(1, ge=1),
    search: str = Query(""),
    db: Session = Depends(get_db),
    _: None = admin_required,
):
    return service.list_alunos(db, page=page, per_page=25, search=search)

@router.post("/alunos", response_model=schemas.AlunoOut, status_code=201)
def create_aluno(body: schemas.AlunoCreate, db: Session = Depends(get_db), _=admin_required):
    return service.create_aluno(db, body)

@router.put("/alunos/{aluno_id}", response_model=schemas.AlunoOut)
def update_aluno(aluno_id: int, body: schemas.AlunoUpdate, db: Session = Depends(get_db), _=admin_required):
    return service.update_aluno(db, aluno_id, body)

@router.post("/alunos/{aluno_id}/deactivate", response_model=schemas.AlunoOut)
def deactivate_aluno(aluno_id: int, db: Session = Depends(get_db), _=admin_required):
    return service.deactivate_aluno(db, aluno_id)
```

### Pattern 2: SQLAlchemy 2.0 ORM Model
**What:** Mapped column style, consistent with existing `Usuario` model.

```python
# Source: [VERIFIED: backend/src/models/usuario.py — established pattern]
# backend/src/models/aluno.py
from sqlalchemy import String, Boolean, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

class Aluno(Base):
    __tablename__ = "alunos"

    id: Mapped[int] = mapped_column(primary_key=True)
    matricula: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    data_nascimento: Mapped[date | None] = mapped_column(Date, nullable=True)
    responsavel_id: Mapped[int | None] = mapped_column(ForeignKey("responsaveis.id", ondelete="SET NULL"), nullable=True)
    turma_id: Mapped[int | None] = mapped_column(ForeignKey("turmas.id", ondelete="SET NULL"), nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
```

### Pattern 3: Pagination with SQLAlchemy 2.0
**What:** Server-side LIMIT/OFFSET with total count for prev/next buttons.

```python
# Source: [ASSUMED — standard SQLAlchemy 2.0 select pattern]
# backend/src/admin/service.py
from sqlalchemy import select, func

def list_alunos(db, page: int, per_page: int, search: str):
    offset = (page - 1) * per_page
    base_q = select(Aluno).where(Aluno.ativo == True)
    if search:
        base_q = base_q.where(Aluno.nome.ilike(f"%{search}%"))

    total = db.scalar(select(func.count()).select_from(base_q.subquery()))
    rows = db.scalars(base_q.order_by(Aluno.nome).offset(offset).limit(per_page)).all()

    return {
        "items": rows,
        "total": total,
        "page": page,
        "per_page": per_page,
    }
```

### Pattern 4: professor_turma Sync (replace-all)
**What:** On Turma create/update, the frontend sends the complete list of `[{disciplina_id, professor_id}]` rows. Backend deletes all existing rows for that turma and re-inserts the new list atomically.

```python
# Source: [ASSUMED — standard junction table pattern]
# backend/src/admin/service.py
from src.models.professor_turma import ProfessorTurma  # junction model

def sync_professor_turma(db, turma_id: int, rows: list[dict]):
    # Delete all existing assignments for this turma
    db.query(ProfessorTurma).filter(ProfessorTurma.turma_id == turma_id).delete()
    # Insert fresh rows
    for row in rows:
        db.add(ProfessorTurma(
            turma_id=turma_id,
            disciplina_id=row["disciplina_id"],
            professor_id=row["professor_id"],
        ))
    db.commit()
```

**Why replace-all instead of diff:** With small numbers of assignments (5-15 per turma typical), diff is unnecessary complexity. Replace-all is transactionally safe and idempotent.

### Pattern 5: TanStack Query v5 — Paginated List
**What:** `useQuery` with page in queryKey + `keepPreviousData` (renamed to `placeholderData: keepPreviousData` in v5).

```typescript
// Source: [CITED: tanstack.com/query/v5/docs/framework/react/guides/paginated-queries]
import { useQuery, keepPreviousData } from '@tanstack/react-query'
import { api } from '../../services/api'

function useAlunos(page: number, search: string) {
  return useQuery({
    queryKey: ['alunos', { page, search }],
    queryFn: () =>
      api.get('/admin/alunos', { params: { page, search } }).then(r => r.data),
    placeholderData: keepPreviousData,  // v5 API — NOT keepPreviousData: true
  })
}
```

### Pattern 6: TanStack Query v5 — Mutation with Invalidation
**What:** `useMutation` with `onSuccess` invalidating the list query so the table refreshes automatically.

```typescript
// Source: [CITED: tanstack.com/query/v5/docs/react/guides/invalidations-from-mutations]
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { toast } from 'sonner'

function useCreateAluno() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (body: AlunoCreate) =>
      api.post('/admin/alunos', body).then(r => r.data),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ['alunos'] })
      toast.success('Aluno criado com sucesso')
    },
    onError: () => {
      toast.error('Erro ao criar aluno')
    },
  })
}
```

### Pattern 7: Modal Shell Component
**What:** Reusable modal using native `<dialog>` element (focus trapping, ESC to close, backdrop built-in — no library needed). Alternatively, a simple CSS overlay with React portal.
**Recommendation:** Simple CSS-based overlay with portal for this prototype — avoids introducing another dependency while remaining accessible with `role="dialog"` and `aria-modal`.

```typescript
// Source: [ASSUMED — standard React pattern]
import { useEffect } from 'react'
import { createPortal } from 'react-dom'

interface ModalProps {
  open: boolean
  title: string
  onClose: () => void
  children: React.ReactNode
}

export function Modal({ open, title, onClose, children }: ModalProps) {
  useEffect(() => {
    if (!open) return
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && onClose()
    document.addEventListener('keydown', onKey)
    return () => document.removeEventListener('keydown', onKey)
  }, [open, onClose])

  if (!open) return null

  return createPortal(
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/40"
      onClick={onClose}
      role="dialog"
      aria-modal="true"
    >
      <div
        className="bg-white rounded-lg shadow-xl w-full max-w-lg p-6"
        onClick={e => e.stopPropagation()}
      >
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold">{title}</h2>
          <button onClick={onClose} aria-label="Fechar">&times;</button>
        </div>
        {children}
      </div>
    </div>,
    document.body
  )
}
```

### Pattern 8: Sonner Toast Setup
**What:** One `<Toaster />` at app root, `toast.success("msg")` / `toast.error("msg")` anywhere.

```typescript
// Source: [CITED: github.com/emilkowalski/sonner]
// In main.tsx or App.tsx, add <Toaster /> once:
import { Toaster } from 'sonner'

// Inside JSX tree (at root level):
<Toaster richColors position="top-right" />

// In any mutation callback:
import { toast } from 'sonner'
toast.success('Aluno criado com sucesso')  // auto-dismisses after ~4s
```

### Pattern 9: React Hook Form in Modal
**What:** `useForm` with zod resolver. `reset()` when modal closes to clear stale values.

```typescript
// Source: [ASSUMED — react-hook-form standard pattern]
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const alunoSchema = z.object({
  nome: z.string().min(1, 'Nome é obrigatório'),
  turma_id: z.number().nullable().optional(),
})
type AlunoFormData = z.infer<typeof alunoSchema>

function AlunoModal({ open, onClose, initial }: Props) {
  const { register, handleSubmit, reset, formState: { errors } } = useForm<AlunoFormData>({
    resolver: zodResolver(alunoSchema),
    defaultValues: initial ?? { nome: '', turma_id: null },
  })

  // Reset form when modal closes or initial data changes
  useEffect(() => { reset(initial ?? { nome: '', turma_id: null }) }, [initial, reset])

  const mutation = useCreateAluno()

  const onSubmit = (data: AlunoFormData) => {
    mutation.mutate(data, { onSuccess: onClose })
  }

  return (
    <Modal open={open} onClose={onClose} title={initial ? 'Editar Aluno' : 'Novo Aluno'}>
      <form onSubmit={handleSubmit(onSubmit)}>
        <label>Nome</label>
        <input {...register('nome')} />
        {errors.nome && <p>{errors.nome.message}</p>}
        <button type="submit" disabled={mutation.isPending}>Salvar</button>
      </form>
    </Modal>
  )
}
```

### Pattern 10: Admin Sidebar Layout
**What:** Replace the top-only `AppLayout` for admin routes with a sidebar-first layout. The existing `AppLayout` stays in use for professor/responsavel routes.

```typescript
// Source: [ASSUMED — standard admin panel layout]
// frontend/src/components/admin/AdminLayout.tsx
import { NavLink, Outlet } from 'react-router-dom'

const navItems = [
  { to: '/admin', label: 'Dashboard', end: true },
  { to: '/admin/alunos', label: 'Alunos' },
  { to: '/admin/turmas', label: 'Turmas' },
  { to: '/admin/disciplinas', label: 'Disciplinas' },
  { to: '/admin/professores', label: 'Professores' },
  { to: '/admin/responsaveis', label: 'Responsáveis' },
]

export default function AdminLayout() {
  return (
    <div className="flex h-screen">
      <aside className="w-56 bg-gray-900 text-white flex flex-col">
        {/* logo area */}
        <nav className="flex-1 p-4 space-y-1">
          {navItems.map(item => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) =>
                `block px-3 py-2 rounded text-sm ${isActive ? 'bg-indigo-600' : 'hover:bg-gray-700'}`
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
        {/* user/logout at bottom */}
      </aside>
      <main className="flex-1 overflow-auto">
        <Outlet />
      </main>
    </div>
  )
}
```

**App.tsx changes:** Add `/admin/alunos`, `/admin/turmas`, etc. as child routes under the existing `/admin` route group, using `AdminLayout` instead of `AppLayout` for the admin outlet.

### Anti-Patterns to Avoid
- **Hard DELETE on entities:** All deactivation must set `ativo=False`, not `db.delete()`. Future phases query active records and deactivated records must remain for audit.
- **Storing professor_turma as a relationship collection on Turma:** Use direct delete + re-insert. SQLAlchemy cascade on many-to-many through-table with association objects can cause silent data loss when the relationship collection is cleared.
- **Hashing passwords in the router:** Always hash in the service layer using the same `CryptContext` from `auth.service`. Never pass plaintext to the model.
- **Re-creating models that already exist:** `usuarios`, `professores`, `responsaveis`, `turmas`, `disciplinas`, `alunos`, `professor_turma` tables were created in migration 0001. Do NOT re-create them in Alembic — only ADD the missing `matricula` column in migration 0003.
- **Using `keepPreviousData: true` option:** This is the v4 API. In v5, it's `placeholderData: keepPreviousData` (import `keepPreviousData` from `@tanstack/react-query`).
- **Tailwind v4 install:** Running `npm install tailwindcss` without `@3` gives v4 which has a completely different config format and breaks existing class patterns.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Toast notifications | Custom toast with setTimeout + CSS | `sonner` | Accessibility, stacking, promise handling, auto-dismiss — all handled |
| Form validation in modals | `useState` + manual error strings per field | `react-hook-form` + `zod` | Re-render performance, touched/dirty tracking, schema reuse, reset() |
| Password hashing | `hashlib.sha256` or plain bcrypt | `passlib.CryptContext` from `auth.service` | Already installed, already configured, handles bcrypt cost factor |
| Pagination math | Manual page calculation | Standard LIMIT/OFFSET in service layer | Trivial to get off-by-one wrong; formula is `offset = (page-1)*per_page` |
| Query cache invalidation | Manually refetching via `useState` trigger | `queryClient.invalidateQueries` | Handles stale-time, race conditions, background updates |

---

## Schema Gap: Matricula Column (Migration 0003)

The `alunos` table (created in migration 0001) has no `matricula` column. CONTEXT.md explicitly requires "Matrícula" as a table column. [VERIFIED: grep of 0001_initial_schema.py]

**Resolution:** Wave 0 of Phase 3 must add Alembic migration 0003:

```python
# backend/alembic/versions/0003_add_matricula_to_alunos.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    with op.batch_alter_table("alunos") as batch_op:
        batch_op.add_column(sa.Column("matricula", sa.String(20), nullable=True))
        batch_op.create_unique_constraint("uq_alunos_matricula", ["matricula"])

def downgrade():
    with op.batch_alter_table("alunos") as batch_op:
        batch_op.drop_constraint("uq_alunos_matricula", type_="unique")
        batch_op.drop_column("matricula")
```

**Matricula format:** Auto-generated by the service layer on create. Recommended pattern: `f"MAT{year}{id:05d}"` e.g. `MAT202600001`. The `id` is available after `db.flush()` (before `db.commit()`), allowing the generated matricula to be written back to the row in the same transaction.

**Why nullable in migration:** Existing rows (if any) cannot have a unique non-null value generated retroactively in a SQLite batch migration without a data migration step. Set nullable, backfill in the migration, then optionally alter to not-null in the same migration.

---

## Common Pitfalls

### Pitfall 1: ProfessorTurma is a junction table with composite PK, not a standard model
**What goes wrong:** Treating `professor_turma` as a regular ORM model with `id` primary key fails because the table has a composite PK `(professor_id, turma_id, disciplina_id)`.
**Why it happens:** Developers assume every table has an `id` column.
**How to avoid:** Create a `ProfessorTurma` model mirroring the exact composite PK from the migration. Use `db.query(ProfessorTurma).filter(ProfessorTurma.turma_id == x).delete()` for cleanup.
**Warning signs:** `IntegrityError` with "UNIQUE constraint failed" when trying to re-insert after a failed delete.

### Pitfall 2: Tailwind v4 vs v3 config incompatibility
**What goes wrong:** Running `npm install tailwindcss` (without version pin) installs v4. v4 uses CSS-based config (`@theme {}` in CSS file) instead of `tailwind.config.js`. The `npx tailwindcss init -p` command behavior changes, and existing `className="..."` patterns may not work.
**Why it happens:** npm defaults to latest version.
**How to avoid:** Always install `tailwindcss@3` explicitly.
**Warning signs:** `tailwind.config.js` generates with different structure, or PostCSS errors about unknown plugins.

### Pitfall 3: SQLAlchemy batch mode required for column addition in SQLite
**What goes wrong:** `op.add_column()` on SQLite fails with "Cannot add a column with a UNIQUE constraint to an existing table" without batch mode.
**Why it happens:** SQLite does not support `ALTER TABLE ADD COLUMN` with constraints.
**How to avoid:** Always use `with op.batch_alter_table("alunos") as batch_op:` for any SQLite column additions or constraint changes. Alembic env.py already has `render_as_batch=True` configured. [VERIFIED: Phase 1 RESEARCH.md confirms batch mode set up]
**Warning signs:** `OperationalError: Cannot add a column with constraints`.

### Pitfall 4: React Hook Form `reset()` not called on modal close
**What goes wrong:** Opening the edit modal for record A, closing without saving, then opening for record B still shows record A's data.
**Why it happens:** `useForm` maintains its own internal state; closing the modal does not reset it.
**How to avoid:** Call `reset(initialData)` in a `useEffect` keyed on `[initial, reset]` or when `open` becomes `true`.
**Warning signs:** Pre-filled form data from previous edit appearing in a new create/edit modal.

### Pitfall 5: `keepPreviousData` v4 API used in v5
**What goes wrong:** `useQuery({ ..., keepPreviousData: true })` is silently ignored in TanStack Query v5 — the option was removed.
**Why it happens:** Training data or examples reference v4 API.
**How to avoid:** Use `placeholderData: keepPreviousData` where `keepPreviousData` is imported from `@tanstack/react-query`.
**Warning signs:** Table flickers or shows empty state briefly on page changes.

### Pitfall 6: Admin creates Professor/Responsavel account — must create two rows atomically
**What goes wrong:** Creating `Usuario` succeeds but `Professor`/`Responsavel` profile row insert fails. The orphan `Usuario` row causes a login error ("could not resolve display name").
**Why it happens:** Two separate `db.add()` calls without a transaction wrapper.
**How to avoid:** Create both rows within the same session before `db.commit()`. SQLAlchemy sync sessions auto-wrap in a transaction — as long as both adds happen before `db.commit()`, they are atomic.
**Warning signs:** Professor can log in but auth service returns empty `nome`.

### Pitfall 7: Deactivating a Responsavel does not deactivate linked Alunos
**What goes wrong:** Deactivating a responsavel via `ativo=False` does not affect their linked alunos. A future query for "active alunos" may still return children of a deactivated responsavel.
**Why it happens:** The FK relationship uses `ondelete="SET NULL"` on `alunos.responsavel_id`, not cascade deactivation.
**How to avoid:** When deactivating a responsavel, the admin panel should display a warning that linked alunos remain active. Deactivate alunos separately if needed. Document this as a UI decision (out of Phase 3 scope to auto-cascade deactivation).

---

## Code Examples

### Dashboard Summary Endpoint
```python
# Source: [ASSUMED — SQLAlchemy 2.0 func.count() pattern]
@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), _=admin_required):
    from sqlalchemy import select, func
    counts = {
        "alunos": db.scalar(select(func.count()).where(Aluno.ativo == True).select_from(Aluno)),
        "turmas": db.scalar(select(func.count()).select_from(Turma)),
        "disciplinas": db.scalar(select(func.count()).select_from(Disciplina)),
        "professores": db.scalar(select(func.count()).where(Usuario.ativo == True).join(Professor).select_from(Professor)),
        "responsaveis": db.scalar(select(func.count()).where(Usuario.ativo == True).join(Responsavel).select_from(Responsavel)),
    }
    return counts
```

### Create Professor Account (atomic)
```python
# Source: [ASSUMED — SQLAlchemy 2.0 session pattern]
def create_professor(db: Session, body: ProfessorCreate) -> Professor:
    from src.auth.service import get_password_hash
    if db.scalar(select(Usuario).where(Usuario.email == body.email)):
        raise HTTPException(400, "Email já cadastrado")
    usuario = Usuario(email=body.email, senha_hash=get_password_hash(body.senha), tipo=TipoUsuario.professor, ativo=True)
    db.add(usuario)
    db.flush()  # assigns usuario.id without committing
    professor = Professor(usuario_id=usuario.id, nome=body.nome, cpf=body.cpf)
    db.add(professor)
    db.commit()
    db.refresh(professor)
    return professor
```

### Alunos List with Turma Name (joined query)
```python
# Source: [ASSUMED — SQLAlchemy 2.0 join pattern]
stmt = (
    select(Aluno, Turma.nome.label("turma_nome"))
    .outerjoin(Turma, Aluno.turma_id == Turma.id)
    .where(Aluno.ativo == True)
    .order_by(Aluno.nome)
    .offset(offset)
    .limit(per_page)
)
rows = db.execute(stmt).all()
# rows is list of Row(Aluno, turma_nome)
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `keepPreviousData: true` option | `placeholderData: keepPreviousData` import | TanStack Query v5 | Must use new import; old option silently ignored |
| `orm_mode = True` in Pydantic model | `from_attributes = True` in `model_config` | Pydantic v2 | Any SQLAlchemy → Pydantic serialization needs this |
| `db.query(Model)` (legacy) | `db.scalars(select(Model))` (v2 style) | SQLAlchemy 2.0 | Both work in 2.0 but v2 style is forward-compatible |
| `tailwind.config.js` (CommonJS) | `tailwind.config.js` (ESM export) | Tailwind v3.3+ | Use `export default {}` if package.json has `"type": "module"` |

**Deprecated/outdated:**
- `keepPreviousData: true` in useQuery options: removed in TanStack Query v5; replaced by `placeholderData: keepPreviousData`
- `orm_mode = True`: replaced by `model_config = ConfigDict(from_attributes=True)` in Pydantic v2

---

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | SQLAlchemy `select(func.count())` scalar pattern works for dashboard counts | Code Examples | Minor — fallback is `len(db.scalars(...).all())` but less efficient |
| A2 | Replace-all strategy for professor_turma (delete + re-insert) is safe under SQLite WAL mode | Pattern 4 | Low — SQLite WAL serializes writes; no concurrent admin writes expected |
| A3 | `db.flush()` assigns auto-incremented `id` before commit in SQLite sync mode | Pattern 9 (create professor) | Medium — if flush doesn't assign id, the professor profile row has NULL user_id; test in Wave 0 |
| A4 | Tailwind config file should use ESM (`export default`) since package.json has `"type": "module"` | Standard Stack | Low — CommonJS `module.exports = {}` also works but triggers ESM warning |
| A5 | `@hookform/resolvers` latest version is compatible with react-hook-form 7.74.0 and zod 4.x | Standard Stack | Low — check version compatibility on install; resolver package tracks hook-form major versions |
| A6 | The Alembic env.py `render_as_batch=True` is already set from Phase 1 | Pitfall 3 | Medium — if not set, migration 0003 column add will fail on SQLite |

---

## Open Questions (RESOLVED)

1. **Matricula uniqueness across years**
   - What we know: `matricula` must display in the table per CONTEXT.md
   - What's unclear: Is `MAT{year}{id:05d}` the right format, or does the school have a pre-existing format?
   - Recommendation: Use `MAT{year}{id:05d}` as default; admin can edit the field if they have an override format. Mark `matricula` as an editable field in the modal.
   - RESOLVED: Use `MAT{year}{id:05d}` format as default (e.g., MAT202600001). Field is editable in modal so admin can override if school has a different format. Plan 02 service layer generates this on create via `db.flush()` to get the id before commit.

2. **Tailwind CSS not installed**
   - What we know: All existing Phase 2 components use Tailwind classes. Tailwind is not in package.json.
   - What's unclear: Did the agent that wrote those components expect Tailwind to be installed later, or is there a CDN load somewhere?
   - Recommendation: Install `tailwindcss@3` as Wave 0 of Phase 3. This unblocks all UI work.
   - RESOLVED: Plan 01 Task 3 installs `tailwindcss@3 postcss autoprefixer` via npm, creates `tailwind.config.js` with ESM export default (required by package.json `"type": "module"`), and adds `@tailwind base/components/utilities` to `index.css`.

3. **Alembic env.py batch mode verification**
   - What we know: Phase 1 research recommends batch mode; Phase 1 plan configures it.
   - What's unclear: Did the Phase 1 execution actually write `render_as_batch=True` to env.py?
   - Recommendation: Read `backend/alembic/env.py` at the start of Wave 0 and confirm the flag before running migration 0003.
   - RESOLVED: Pattern mapper verified `render_as_batch=True` is present in `alembic/env.py` lines 36 and 52. Plan 01 Task 1 reads env.py as a `read_first` prerequisite before running migration 0003 to confirm the flag is active.

---

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python 3.x | Backend runtime | Yes | 3.11.7 | — |
| pip | Backend deps | Yes | 23.3.1 | — |
| Node.js (npm) | Frontend build | Yes (implied by existing package-lock.json) | Unknown | — |
| tailwindcss v3 | Frontend CSS | No (not installed) | — | Must install Wave 0 |
| sonner | Toast notifications | No (not installed) | — | Must install Wave 0 |
| react-hook-form | Form validation | No (not installed) | — | Must install Wave 0 |
| zod | Schema validation | No (not installed) | — | Must install Wave 0 |
| SQLite DB file | Migration 0003 | Yes (exists from Phase 1) | — | — |

**Missing dependencies with no fallback:**
- `tailwindcss@3` — required for all existing and new UI components to render correctly
- `sonner` — required for toast feedback (locked decision)
- `react-hook-form` + `zod` + `@hookform/resolvers` — required for modal forms

---

## Validation Architecture

> `workflow.nyquist_validation` is absent from config.json — treated as enabled.

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest (not yet configured for this project) |
| Config file | none — Wave 0 gap |
| Quick run command | `cd backend && python -m pytest tests/ -x -q` |
| Full suite command | `cd backend && python -m pytest tests/ -v` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| ADMIN-01 | Create aluno returns 201 with matricula | integration | `pytest tests/test_admin.py::test_create_aluno -x` | No — Wave 0 |
| ADMIN-01 | List alunos returns paginated result | integration | `pytest tests/test_admin.py::test_list_alunos -x` | No — Wave 0 |
| ADMIN-01 | Deactivate aluno sets ativo=False | integration | `pytest tests/test_admin.py::test_deactivate_aluno -x` | No — Wave 0 |
| ADMIN-02 | Create turma + sync professor_turma rows | integration | `pytest tests/test_admin.py::test_create_turma -x` | No — Wave 0 |
| ADMIN-04 | Update turma replaces all professor_turma rows | integration | `pytest tests/test_admin.py::test_sync_professor_turma -x` | No — Wave 0 |
| ADMIN-05 | Create professor creates Usuario + Professor atomically | integration | `pytest tests/test_admin.py::test_create_professor -x` | No — Wave 0 |
| ADMIN-06 | Create responsavel links to aluno(s) | integration | `pytest tests/test_admin.py::test_create_responsavel -x` | No — Wave 0 |
| ADMIN-* | Non-admin JWT gets 403 on all /admin endpoints | integration | `pytest tests/test_admin.py::test_admin_role_required -x` | No — Wave 0 |
| ADMIN-* | Unauthenticated request gets 401 on all /admin endpoints | integration | `pytest tests/test_admin.py::test_unauthenticated -x` | No — Wave 0 |

### Sampling Rate
- **Per task commit:** `cd backend && python -m pytest tests/test_admin.py -x -q`
- **Per wave merge:** `cd backend && python -m pytest tests/ -v`
- **Phase gate:** Full suite green before `/gsd-verify-work`

### Wave 0 Gaps
- [ ] `backend/tests/__init__.py` — package init
- [ ] `backend/tests/conftest.py` — shared fixtures (test DB, auth headers for admin/professor)
- [ ] `backend/tests/test_admin.py` — all Phase 3 test cases
- [ ] Framework install: `pip install pytest httpx` (httpx for FastAPI TestClient async support)
- [ ] Alembic migration 0003 (matricula column)
- [ ] Tailwind CSS v3 install + config in frontend

---

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | Yes — new accounts created | `passlib.CryptContext` for password hashing; same pattern as Phase 2 |
| V3 Session Management | No — JWT already handled in Phase 2 | — |
| V4 Access Control | Yes — admin-only endpoints | `require_role("admin")` dependency on every /admin/* route |
| V5 Input Validation | Yes — all POST/PUT bodies | Pydantic schemas with field constraints |
| V6 Cryptography | Yes — password hashing for new users | `passlib[bcrypt]` — already installed, do not hand-roll |

### Known Threat Patterns for FastAPI + SQLAlchemy

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Privilege escalation (non-admin calling /admin endpoints) | Elevation of Privilege | `require_role("admin")` on every admin router; verified by test_admin_role_required |
| Mass assignment (extra fields in POST body) | Tampering | Pydantic schemas reject extra fields by default in v2 (`extra="forbid"` optional) |
| Horizontal privilege (admin deactivating themselves) | Elevation of Privilege | Service layer check: refuse deactivation of the caller's own account |
| SQL injection | Tampering | SQLAlchemy ORM parameterized queries only; no raw SQL string formatting |
| Plaintext password storage | Information Disclosure | Always hash with passlib before storing; never store body.senha |
| IDOR (accessing aluno by guessing ID without ownership) | Information Disclosure | Admin role has full access by design; no IDOR concern for admin panel |

---

## Sources

### Primary (HIGH confidence)
- `backend/src/models/usuario.py` — SQLAlchemy 2.0 mapped_column pattern [VERIFIED: codebase]
- `backend/alembic/versions/0001_initial_schema.py` — Full schema; confirmed absence of matricula [VERIFIED: codebase]
- `frontend/package.json` + `package-lock.json` — Confirmed Tailwind not installed [VERIFIED: codebase]
- `frontend/src/components/AppLayout.tsx`, `LoginPage.tsx` — Confirmed Tailwind classes in use [VERIFIED: codebase]
- `backend/requirements.txt` — Confirmed all backend deps [VERIFIED: codebase]

### Secondary (MEDIUM confidence)
- [TanStack Query v5 Paginated Queries](https://tanstack.com/query/v5/docs/framework/react/guides/paginated-queries) — `placeholderData: keepPreviousData` confirmed as v5 API
- [TanStack Query v5 Invalidation from Mutations](https://tanstack.com/query/v5/docs/react/guides/invalidations-from-mutations) — `queryClient.invalidateQueries` pattern confirmed
- [Sonner GitHub](https://github.com/emilkowalski/sonner) — `<Toaster />` + `toast()` setup pattern confirmed
- npm registry — tailwindcss@3 latest = 3.4.19, tailwindcss@latest = 4.2.4 (v4 confirmed as breaking change) [VERIFIED: npm view]

### Tertiary (LOW confidence — assumed from training)
- SQLAlchemy 2.0 `select(func.count())` scalar pattern for dashboard
- `db.flush()` assigns auto-id before commit
- Replace-all for professor_turma junction table

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — packages verified via npm registry; backend deps verified from requirements.txt
- Architecture: HIGH — follows established project patterns (auth module structure)
- Schema gap (matricula): HIGH — verified absence in migration file
- Tailwind gap: HIGH — verified not in package.json or package-lock.json
- Pitfalls: MEDIUM — most from training knowledge, some verified against docs
- Test patterns: MEDIUM — pytest/httpx standard; specific file names assumed

**Research date:** 2026-04-27
**Valid until:** 2026-05-27 (30 days; stable libraries)
