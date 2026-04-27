# Phase 4: Portal do Professor - Pattern Map

**Mapped:** 2026-04-27
**Files analyzed:** 16 new/modified files
**Analogs found:** 16 / 16

---

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `backend/src/models/chamada.py` | model | CRUD | `backend/src/models/professor_turma.py` + `aluno.py` | exact |
| `backend/src/models/presenca.py` | model | CRUD | `backend/src/models/aluno.py` (UniqueConstraint pattern) | exact |
| `backend/src/models/avaliacao.py` | model | CRUD | `backend/src/models/aluno.py` + professor.py | exact |
| `backend/src/models/nota.py` | model | CRUD | `backend/src/models/professor_turma.py` (FK + UniqueConstraint) | exact |
| `backend/src/professor/__init__.py` | config | — | `backend/src/admin/__init__.py` | exact |
| `backend/src/professor/router.py` | route | request-response | `backend/src/admin/router.py` | exact |
| `backend/src/professor/service.py` | service | CRUD + batch | `backend/src/admin/service.py` | exact |
| `backend/src/professor/schemas.py` | model | request-response | `backend/src/admin/schemas.py` | exact |
| `backend/tests/test_professor.py` | test | request-response | `backend/tests/test_admin.py` | exact |
| `frontend/src/pages/professor/ProfessorLandingPage.tsx` | component | request-response | `frontend/src/pages/admin/AlunosPage.tsx` (page shell) | role-match |
| `frontend/src/pages/professor/ProfessorTurmaPage.tsx` | component | request-response | `frontend/src/pages/admin/AlunosPage.tsx` | role-match |
| `frontend/src/components/professor/TurmaCard.tsx` | component | request-response | `frontend/src/components/admin/EntityTable.tsx` (card-in-table row) | partial |
| `frontend/src/components/professor/TabNav.tsx` | component | event-driven | no direct analog — UI-SPEC + RESEARCH.md pattern | UI-SPEC |
| `frontend/src/components/professor/AttendanceToggle.tsx` | component | event-driven | no direct analog — UI-SPEC pattern | UI-SPEC |
| `frontend/src/components/professor/GradeTable.tsx` | component | CRUD | `frontend/src/components/admin/EntityTable.tsx` (table structure) | role-match |
| `frontend/src/components/professor/FrequencyTable.tsx` | component | request-response | `frontend/src/components/admin/EntityTable.tsx` (table structure) | role-match |

---

## Pattern Assignments

### `backend/src/models/chamada.py` (model, CRUD)

**Analog:** `backend/src/models/aluno.py` + `backend/src/models/professor_turma.py`

**Imports + ORM declaration pattern** (`aluno.py` lines 1-7, `professor_turma.py` lines 1-4):
```python
from datetime import date
from sqlalchemy import Date, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from src.database import Base
```

**Core model pattern** — `mapped_column` + FK with cascade (`professor_turma.py` lines 6-17):
```python
class Chamada(Base):
    __tablename__ = "chamadas"
    id: Mapped[int] = mapped_column(primary_key=True)
    turma_id: Mapped[int] = mapped_column(ForeignKey("turmas.id", ondelete="CASCADE"))
    disciplina_id: Mapped[int] = mapped_column(ForeignKey("disciplinas.id", ondelete="CASCADE"))
    professor_id: Mapped[int] = mapped_column(ForeignKey("professores.id", ondelete="CASCADE"))
    data: Mapped[date] = mapped_column(Date, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
```

**Key fact:** No `__table_args__` needed — no unique constraint on (turma_id, disciplina_id, data). Service must query-first to avoid duplicates.

---

### `backend/src/models/presenca.py` (model, CRUD)

**Analog:** `backend/src/models/aluno.py` (Boolean column) + `professor_turma.py` (FK pattern)

**UniqueConstraint + Boolean pattern** — `aluno.py` lines 1-21 plus `professor_turma.py` FK style:
```python
from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base

class Presenca(Base):
    __tablename__ = "presencas"
    __table_args__ = (UniqueConstraint("chamada_id", "aluno_id", name="uq_presencas_chamada_id_aluno_id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    chamada_id: Mapped[int] = mapped_column(ForeignKey("chamadas.id", ondelete="CASCADE"))
    aluno_id: Mapped[int] = mapped_column(ForeignKey("alunos.id", ondelete="CASCADE"))
    presente: Mapped[bool] = mapped_column(Boolean, nullable=False)
    justificativa: Mapped[str | None] = mapped_column(String(500), nullable=True)
```

**Key fact:** `__table_args__` is a tuple — the trailing comma on the `UniqueConstraint` line is mandatory.

---

### `backend/src/models/avaliacao.py` (model, CRUD)

**Analog:** `backend/src/models/aluno.py` (multi-column model) + `professor.py` (String + Float columns)

**CheckConstraint + Float column pattern**:
```python
from datetime import date
from sqlalchemy import CheckConstraint, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base

class Avaliacao(Base):
    __tablename__ = "avaliacoes"
    __table_args__ = (
        CheckConstraint("bimestre IN (1, 2, 3, 4)", name="ck_avaliacoes_bimestre"),
        CheckConstraint("valor_maximo > 0", name="ck_avaliacoes_valor_maximo"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    turma_id: Mapped[int] = mapped_column(ForeignKey("turmas.id", ondelete="CASCADE"))
    disciplina_id: Mapped[int] = mapped_column(ForeignKey("disciplinas.id", ondelete="CASCADE"))
    professor_id: Mapped[int] = mapped_column(ForeignKey("professores.id", ondelete="CASCADE"))
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    bimestre: Mapped[int] = mapped_column(Integer, nullable=False)
    valor_maximo: Mapped[float] = mapped_column(Float, nullable=False, default=10.0)
    data: Mapped[date | None] = mapped_column(Date, nullable=True)
```

**Key fact:** No unique constraint on (turma_id, disciplina_id, bimestre) — service must `db.query(Avaliacao).filter(...).first()` before every insert.

---

### `backend/src/models/nota.py` (model, CRUD)

**Analog:** `backend/src/models/professor_turma.py` (composite FK) + `presenca.py` (UniqueConstraint)

```python
from sqlalchemy import Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base

class Nota(Base):
    __tablename__ = "notas"
    __table_args__ = (UniqueConstraint("avaliacao_id", "aluno_id", name="uq_notas_avaliacao_id_aluno_id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    avaliacao_id: Mapped[int] = mapped_column(ForeignKey("avaliacoes.id", ondelete="CASCADE"))
    aluno_id: Mapped[int] = mapped_column(ForeignKey("alunos.id", ondelete="CASCADE"))
    valor: Mapped[float] = mapped_column(Float, nullable=False)
```

---

### `backend/src/models/__init__.py` (modified — add 4 new imports)

**Analog:** `backend/src/models/__init__.py` lines 1-13 (current file — extend it)

**Current pattern** (`__init__.py` lines 1-13):
```python
from src.models.usuario import Usuario, ResetToken, TipoUsuario
from src.models.aluno import Aluno
# ... existing imports ...
from src.models.professor_turma import ProfessorTurma

__all__ = [
    "Usuario", "ResetToken", "TipoUsuario",
    "Aluno", "Turma", "Disciplina",
    "Professor", "Responsavel", "ProfessorTurma",
]
```

**Add these four lines** (same pattern — one import per model file):
```python
from src.models.chamada import Chamada
from src.models.presenca import Presenca
from src.models.avaliacao import Avaliacao
from src.models.nota import Nota
```
And extend `__all__` with `"Chamada", "Presenca", "Avaliacao", "Nota"`.

---

### `backend/src/professor/__init__.py` (config)

**Analog:** `backend/src/admin/__init__.py` (empty file — just package marker)

```python
# empty — package marker only, same as src/admin/__init__.py
```

---

### `backend/src/professor/router.py` (route, request-response)

**Analog:** `backend/src/admin/router.py` — mirror exactly

**Module docstring + imports + role guard pattern** (`admin/router.py` lines 1-18):
```python
"""
Professor API router — all endpoints require professor JWT.

Security:
- professor_required = Depends(require_role("professor")) applied to every endpoint
- Ownership check via _assert_professor_owns_turma on all turma-specific endpoints
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.database import get_db
from src.auth.dependencies import require_role
from src.models.usuario import Usuario
from . import schemas, service

router = APIRouter(prefix="/professor", tags=["professor"])
professor_required = Depends(require_role("professor"))
```

**Endpoint signature pattern** (`admin/router.py` lines 25-27 — dashboard style):
```python
@router.get("/minhas-turmas", response_model=list[schemas.TurmaOut])
def get_minhas_turmas(
    db: Session = Depends(get_db),
    current_user: Usuario = professor_required,
):
    return service.get_minhas_turmas(db, current_user)
```

**Path-param endpoint pattern** (`admin/router.py` lines 53-60 — update style):
```python
@router.get("/turmas/{turma_id}/chamada", response_model=schemas.ChamadaOut)
def get_chamada(
    turma_id: int,
    date: str = Query(...),
    db: Session = Depends(get_db),
    current_user: Usuario = professor_required,
):
    return service.get_chamada(db, current_user, turma_id, date)
```

**main.py registration** — add after `admin_router` (`main.py` lines 10-13 + 50):
```python
from src.professor.router import router as professor_router
# ...
app.include_router(professor_router)
```

---

### `backend/src/professor/service.py` (service, CRUD + batch)

**Analog:** `backend/src/admin/service.py`

**Module docstring + imports pattern** (`admin/service.py` lines 1-25):
```python
"""
Professor service layer — chamada, notas, and frequencia business logic.

Patterns:
- _get_professor() helper resolves professor_id from current_user (Usuario) on every call
- _assert_professor_owns_turma() ownership check called at start of every turma-specific function
- db.query() style consistent with admin/service.py
- Chamada: find-or-create + delete+insert presencas (replace-all)
- Notas: find-or-create avaliacao per bimestre + upsert nota
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException

from src.models.usuario import Usuario
from src.models.professor import Professor
from src.models.professor_turma import ProfessorTurma
from src.models.turma import Turma
from src.models.disciplina import Disciplina
from src.models.aluno import Aluno
from src.models.chamada import Chamada
from src.models.presenca import Presenca
from src.models.avaliacao import Avaliacao
from src.models.nota import Nota
from . import schemas
```

**_get_professor helper** (mirrors `_generate_matricula` helper style in `admin/service.py` line 51):
```python
def _get_professor(db: Session, usuario: Usuario) -> Professor:
    prof = db.query(Professor).filter(Professor.usuario_id == usuario.id).first()
    if not prof:
        raise HTTPException(status_code=404, detail="Perfil de professor não encontrado")
    return prof
```

**Ownership check** (mirrors `deactivate_usuario` guard style in `admin/service.py` lines 337-347):
```python
def _assert_professor_owns_turma(db: Session, professor_id: int, turma_id: int) -> None:
    link = db.query(ProfessorTurma).filter(
        ProfessorTurma.professor_id == professor_id,
        ProfessorTurma.turma_id == turma_id,
    ).first()
    if not link:
        raise HTTPException(status_code=403, detail="Acesso negado a esta turma")
```

**Replace-all delete pattern** (mirrors `_sync_professor_turma` in `admin/service.py` lines 124-132):
```python
# From admin/service.py lines 124-132 — replace-all pattern:
def _sync_professor_turma(db: Session, turma_id: int, rows: list) -> None:
    db.query(ProfessorTurma).filter(ProfessorTurma.turma_id == turma_id).delete(synchronize_session=False)
    for row in rows:
        db.add(ProfessorTurma(...))

# Professor service applies this same pattern for presencas:
db.query(Presenca).filter(Presenca.chamada_id == chamada.id).delete(synchronize_session=False)
for p in presencas_data:
    db.add(Presenca(chamada_id=chamada.id, aluno_id=p.aluno_id, presente=p.presente))
```

**db.flush() before db.commit()** (mirrors `create_aluno` in `admin/service.py` lines 74-87):
```python
# admin/service.py lines 82-84:
db.add(aluno)
db.flush()  # assigns aluno.id before commit
aluno.matricula = _generate_matricula(...)
db.commit()
db.refresh(aluno)

# professor/service.py: same flush pattern for chamada find-or-create:
if not chamada:
    chamada = Chamada(...)
    db.add(chamada)
    db.flush()  # get chamada.id for presenca FK
```

**HTTPException 404 pattern** (mirrors `update_aluno` in `admin/service.py` lines 90-98):
```python
# admin/service.py line 92-93:
if not aluno:
    raise HTTPException(status_code=404, detail="Aluno não encontrado")
```

---

### `backend/src/professor/schemas.py` (model, request-response)

**Analog:** `backend/src/admin/schemas.py`

**Module docstring + imports pattern** (`admin/schemas.py` lines 1-9):
```python
"""
Pydantic v2 schemas for professor endpoints.
All *Out schemas use model_config = ConfigDict(from_attributes=True) for SQLAlchemy -> Pydantic.
"""
from __future__ import annotations
from datetime import date
from typing import List, Optional
from pydantic import BaseModel, ConfigDict
```

**Out schema with from_attributes** (`admin/schemas.py` lines 29-39 — AlunoOut pattern):
```python
class TurmaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    disciplinas: List[str] = []
    num_alunos: int = 0
```

**Input schema with Optional fields** (`admin/schemas.py` lines 15-19 — AlunoCreate style):
```python
class PresencaIn(BaseModel):
    aluno_id: int
    presente: bool

class ChamadaCreate(BaseModel):
    disciplina_id: int
    data: date
    presencas: List[PresencaIn]
```

**List[nested] pattern** (`admin/schemas.py` lines 58-63 — TurmaCreate professor_turma list):
```python
# admin/schemas.py lines 58-63:
class TurmaCreate(BaseModel):
    nome: str
    professor_turma: List[ProfessorTurmaRow] = []

# professor/schemas.py mirrors:
class NotasCreate(BaseModel):
    disciplina_id: int
    grades: List[GradeIn]
```

---

### `backend/tests/test_professor.py` (test, request-response)

**Analog:** `backend/tests/test_admin.py`

**Docstring + access control tests pattern** (`test_admin.py` lines 1-26):
```python
"""
Professor endpoint tests — Phase 4.

Tests cover PROF-01 through PROF-05 plus access control.
Run: cd backend && python -m pytest tests/test_professor.py -x -q
"""
import pytest


def test_unauthenticated_gets_401(client):
    """Unauthenticated request to any /professor endpoint returns 401."""
    response = client.get("/professor/minhas-turmas")
    assert response.status_code == 401


def test_professor_role_required(client, admin_headers):
    """Admin JWT receives 403 on /professor endpoints."""
    response = client.get("/professor/minhas-turmas", headers=admin_headers)
    assert response.status_code == 403
```

**Setup fixtures from conftest** — all needed fixtures already exist (`conftest.py` lines 75-100):
```python
# Available from conftest.py — no new fixtures needed:
# - test_db   (function scope, in-memory SQLite)
# - client    (get_db override)
# - professor_user  (Usuario with tipo=professor)
# - professor_headers  (Bearer JWT for professor)
# - admin_headers  (Bearer JWT for admin, for 403 tests)
```

**Inline data setup pattern** (`test_admin.py` lines 119-138 — inline model creation):
```python
# test_admin.py pattern — create test data inline before assertion:
from src.models.usuario import Usuario, TipoUsuario
from src.auth.service import hash_password

u = Usuario(email="prof2@test.com", senha_hash=hash_password("pass"), tipo=TipoUsuario.professor, ativo=True)
test_db.add(u)
test_db.flush()
from src.models.professor import Professor
p = Professor(usuario_id=u.id, nome="Prof Teste")
test_db.add(p)
test_db.commit()
```

**Assertion pattern** (`test_admin.py` lines 36-42):
```python
assert response.status_code == 201
data = response.json()
assert "id" in data
assert data["nome"] == "João Silva"
```

---

### `frontend/src/pages/professor/ProfessorLandingPage.tsx` (component, request-response)

**Analog:** `frontend/src/pages/admin/AlunosPage.tsx` — page shell with useQuery + loading/empty states

**Imports pattern** (`AlunosPage.tsx` lines 1-10):
```typescript
import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { api } from '../../services/api'
```

**useQuery hook pattern** (`AlunosPage.tsx` lines 41-48):
```typescript
function useMinhasTurmas() {
  return useQuery({
    queryKey: ['minhas-turmas'],
    queryFn: () => api.get('/professor/minhas-turmas').then((r) => r.data),
  })
}
```

**Loading + empty state pattern** (`EntityTable.tsx` lines 59-62):
```typescript
// EntityTable.tsx — reuse these exact Tailwind classes:
{isLoading ? (
  <div className="text-center py-12 text-gray-400 text-sm">Carregando turmas...</div>
) : rows.length === 0 ? (
  <div className="text-center py-12 text-gray-400 text-sm">Nenhuma turma vinculada.</div>
) : (
  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mt-6">
    {turmas.map((t) => <TurmaCard key={t.id} turma={t} onClick={() => navigate(`/professor/turmas/${t.id}`)} />)}
  </div>
)}
```

**Page heading pattern** (`AlunosPage.tsx` line 249):
```typescript
// AlunosPage.tsx line 249 — reuse exact heading style:
<h1 className="text-2xl font-semibold text-gray-900 mb-6">Alunos</h1>
// ProfessorLandingPage:
<h1 className="text-2xl font-bold text-gray-900">Minhas Turmas</h1>
<p className="text-sm text-gray-500 mt-1">Selecione uma turma para registrar chamada ou lancar notas</p>
```

**Page wrapper** (`AlunosPage.tsx` line 248):
```typescript
// AlunosPage.tsx line 248:
<div className="p-8">
```

---

### `frontend/src/pages/professor/ProfessorTurmaPage.tsx` (component, request-response)

**Analog:** `frontend/src/pages/admin/AlunosPage.tsx` — page with state + multiple sub-components

**Tab state management** — use `useState`, NOT URL params (RESEARCH.md anti-pattern note):
```typescript
// Pattern: local state only (no useSearchParams), same as AlunosPage local modal state
const [activeTab, setActiveTab] = useState<'chamada' | 'notas' | 'frequencia'>('chamada')
```

**Route params pattern** (`App.tsx` lines 56-59 — `useParams` from react-router-dom):
```typescript
import { useParams, Link } from 'react-router-dom'

export default function ProfessorTurmaPage() {
  const { id } = useParams<{ id: string }>()
  const turmaId = Number(id)
  // ...
}
```

**Breadcrumb** — uses `Link` from react-router-dom (`AppLayout.tsx` lines 51-55 — Link style):
```typescript
// AppLayout.tsx Link pattern (lines 51-55):
<Link to={`/${user?.tipo ?? ''}`} className="text-xl font-bold text-indigo-600 hover:text-indigo-700">
// ProfessorTurmaPage breadcrumb:
<nav className="flex items-center gap-2 text-sm mb-6">
  <Link to="/professor" className="text-indigo-600 hover:text-indigo-800 font-medium">Minhas Turmas</Link>
  <span className="text-gray-400">/</span>
  <span className="text-gray-500">{turma?.nome}</span>
</nav>
```

**Conditional tab rendering** (mirrors AlunosPage conditional modal render pattern):
```typescript
{activeTab === 'chamada' && <ChamadaTab turmaId={turmaId} disciplinas={disciplinas} />}
{activeTab === 'notas' && <NotasTab turmaId={turmaId} disciplinas={disciplinas} />}
{activeTab === 'frequencia' && <FrequencyTable turmaId={turmaId} />}
```

---

### `frontend/src/components/professor/TurmaCard.tsx` (component, request-response)

**Analog:** `frontend/src/components/admin/EntityTable.tsx` — row rendering pattern, badge-style display

**TypeScript interface pattern** (`AlunosPage.tsx` lines 15-25):
```typescript
interface TurmaCardProps {
  turma: {
    id: number
    nome: string
    disciplinas: string[]
    num_alunos: number
  }
  onClick: () => void
}
```

**Card container** (UI-SPEC section 1 — TurmaCard):
```typescript
export function TurmaCard({ turma, onClick }: TurmaCardProps) {
  return (
    <div
      onClick={onClick}
      className="bg-white rounded-lg border border-gray-200 p-4 hover:border-indigo-300 hover:shadow-md transition-all cursor-pointer"
    >
      <h2 className="text-xl font-semibold text-gray-900">{turma.nome}</h2>
      <p className="text-sm text-gray-500 mt-1">{turma.disciplinas.join(', ')}</p>
      <p className="text-sm text-gray-700 mt-2">{turma.num_alunos} alunos</p>
    </div>
  )
}
```

---

### `frontend/src/components/professor/TabNav.tsx` (component, event-driven)

**No direct analog** — closest structural pattern is the admin Sidebar active-link pattern (`AdminLayout`), but TabNav is simpler. Use UI-SPEC section 2 + RESEARCH.md Pattern 6 excerpt directly.

**Full component from UI-SPEC / RESEARCH.md** (verified against existing indigo-600 active-state convention):
```typescript
type Tab = 'chamada' | 'notas' | 'frequencia'

interface TabNavProps {
  active: Tab
  onChange: (tab: Tab) => void
}

export function TabNav({ active, onChange }: TabNavProps) {
  const tabs: { key: Tab; label: string }[] = [
    { key: 'chamada', label: 'Chamada' },
    { key: 'notas', label: 'Notas' },
    { key: 'frequencia', label: 'Frequencia' },
  ]
  return (
    <div className="border-b border-gray-200 mb-6" role="tablist">
      <div className="flex gap-6">
        {tabs.map((t) => (
          <button
            key={t.key}
            role="tab"
            aria-selected={active === t.key}
            onClick={() => onChange(t.key)}
            className={`px-1 py-3 text-sm font-medium border-b-2 ${
              active === t.key
                ? 'text-indigo-600 border-indigo-600'
                : 'text-gray-500 hover:text-gray-700 border-transparent'
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>
    </div>
  )
}
```

---

### `frontend/src/components/professor/AttendanceToggle.tsx` (component, event-driven)

**No direct analog** — toggle pattern. Use UI-SPEC section 3 + RESEARCH.md Pattern 6 excerpt. Consistent with `bg-green-100 text-green-800` and `bg-red-100 text-red-800` used in `EntityTable.tsx` lines 87-90 for status badges.

**Badge color reference** (`EntityTable.tsx` lines 87-90):
```typescript
// EntityTable.tsx lines 87-90 — same green/red semantic colors:
className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
  row[col.key] ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
}`}
```

**Full component** (UI-SPEC section 3, verified consistent with EntityTable badge colors):
```typescript
interface AttendanceToggleProps {
  presente: boolean
  onChange: (presente: boolean) => void
}

export function AttendanceToggle({ presente, onChange }: AttendanceToggleProps) {
  return (
    <div className="flex rounded-md shadow-sm" role="group">
      <button
        type="button"
        aria-pressed={presente}
        onClick={() => onChange(true)}
        className={`px-3 py-1 text-xs font-medium rounded-l-md border ${
          presente
            ? 'bg-green-100 text-green-800 border-green-200'
            : 'bg-white text-gray-500 border-gray-300 hover:bg-gray-50'
        }`}
      >
        Presente
      </button>
      <button
        type="button"
        aria-pressed={!presente}
        onClick={() => onChange(false)}
        className={`px-3 py-1 text-xs font-medium rounded-r-md border -ml-px ${
          !presente
            ? 'bg-red-100 text-red-800 border-red-200'
            : 'bg-white text-gray-500 border-gray-300 hover:bg-gray-50'
        }`}
      >
        Falta
      </button>
    </div>
  )
}
```

---

### `frontend/src/components/professor/GradeTable.tsx` (component, CRUD)

**Analog:** `frontend/src/components/admin/EntityTable.tsx` — table structure, thead/tbody, cell classes

**Table skeleton** (`EntityTable.tsx` lines 64-119 — div > table > thead > tbody):
```typescript
// EntityTable.tsx lines 64-119 — use this exact table skeleton:
<div className="overflow-x-auto">
  <table className="min-w-full divide-y divide-gray-200">
    <thead className="bg-gray-50">
      <tr>
        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
          Aluno
        </th>
        {[1, 2, 3, 4].map((b) => (
          <th key={b} className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            {b}o Bimestre
          </th>
        ))}
      </tr>
    </thead>
    <tbody className="bg-white divide-y divide-gray-200">
      {alunos.map((aluno) => (
        <tr key={aluno.id} className="hover:bg-gray-50">
          <td className="px-4 py-3 text-sm font-medium text-gray-900 whitespace-nowrap">
            {aluno.nome}
          </td>
          {[1, 2, 3, 4].map((b) => (
            <td key={b} className="px-2 py-2">
              <input
                type="text"
                value={grades[`${aluno.id}-${b}`] ?? ''}
                onChange={(e) => handleChange(aluno.id, b, e.target.value)}
                placeholder="—"
                aria-invalid={isInvalid(aluno.id, b)}
                className={`w-20 px-2 py-1 border rounded-md text-sm text-center focus:outline-none focus:ring-2 ${
                  isInvalid(aluno.id, b)
                    ? 'border-red-500 focus:ring-red-500 bg-red-50'
                    : 'border-gray-300 focus:ring-indigo-500'
                }`}
              />
            </td>
          ))}
        </tr>
      ))}
    </tbody>
  </table>
</div>
```

**State pattern** — Map keyed by `${aluno_id}-${bimestre}` (NOT react-hook-form — RESEARCH.md anti-pattern):
```typescript
// Do NOT use useForm/register. Use plain state:
const [grades, setGrades] = useState<Record<string, string>>({})
const handleChange = (alunoId: number, bimestre: number, value: string) => {
  setGrades((prev) => ({ ...prev, [`${alunoId}-${bimestre}`]: value }))
}
const isInvalid = (alunoId: number, bimestre: number): boolean => {
  const v = grades[`${alunoId}-${bimestre}`]
  if (v === '' || v === undefined) return false
  const num = parseFloat(v)
  return isNaN(num) || num < 0 || num > 10
}
```

**useMutation + toast pattern** (`AlunosPage.tsx` lines 65-75):
```typescript
// AlunosPage.tsx lines 65-75 — exact mutation + toast pattern:
function useSaveNotas(turmaId: number) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (body: NotasPayload) =>
      api.post(`/professor/turmas/${turmaId}/notas`, body).then((r) => r.data),
    onSuccess: async () => {
      await qc.invalidateQueries({ queryKey: ['notas', turmaId] })
      toast.success('Notas salvas com sucesso.')
    },
    onError: () => toast.error('Erro ao salvar notas. Verifique os valores e tente novamente.'),
  })
}
```

**Save button pattern** (`AlunosPage.tsx` lines 196-209 — disabled + loading label):
```typescript
// AlunosPage.tsx lines 200-208:
<button
  type="submit"
  disabled={isPending}
  className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md hover:bg-indigo-700 disabled:opacity-50"
>
  {isPending ? 'Salvando...' : 'Salvar'}
</button>
// GradeTable:
<div className="mt-4 flex justify-end">
  <button
    onClick={handleSave}
    disabled={saveMutation.isPending || hasErrors}
    className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md hover:bg-indigo-700 disabled:opacity-50"
  >
    {saveMutation.isPending ? 'Salvando...' : 'Salvar notas'}
  </button>
</div>
```

---

### `frontend/src/components/professor/FrequencyTable.tsx` (component, request-response)

**Analog:** `frontend/src/components/admin/EntityTable.tsx` — read-only table, no actions column

**Table structure** (same skeleton as EntityTable — `EntityTable.tsx` lines 64-119, minus actions column):
```typescript
<div className="overflow-x-auto">
  <table className="min-w-full divide-y divide-gray-200">
    <thead className="bg-gray-50">
      <tr>
        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Aluno</th>
        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Presenca</th>
        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Aulas</th>
      </tr>
    </thead>
    <tbody className="bg-white divide-y divide-gray-200">
      {rows.map((row) => {
        const atRisk = row.percentual < 75
        return (
          <tr key={row.aluno_id} className={atRisk ? 'bg-red-50 hover:bg-red-100' : 'hover:bg-gray-50'}>
            <td className="px-4 py-3 text-sm font-medium text-gray-900 whitespace-nowrap">
              {row.nome}
            </td>
            <td className="px-4 py-3 text-sm whitespace-nowrap">
              <span className={atRisk ? 'text-red-700 font-medium' : 'text-gray-700 font-medium'}>
                {row.percentual.toFixed(0)}%
              </span>
              {atRisk && (
                <span className="ml-2 inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-red-100 text-red-800">
                  ⚠ Abaixo de 75%
                </span>
              )}
            </td>
            <td className="px-4 py-3 text-sm text-gray-500 whitespace-nowrap">
              {row.total_presentes}/{row.total_aulas} aulas
            </td>
          </tr>
        )
      })}
    </tbody>
  </table>
</div>
```

**Badge pattern** (`EntityTable.tsx` lines 86-91 — same `inline-flex items-center px-2 py-0.5 rounded text-xs font-medium` pattern):
```typescript
// EntityTable.tsx lines 86-91:
<span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
  row[col.key] ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
}`}>
// FrequencyTable uses same pattern with bg-red-100 text-red-800 for at-risk badge
```

**useQuery hook** (`AlunosPage.tsx` lines 41-47 pattern):
```typescript
function useFrequencia(turmaId: number) {
  return useQuery({
    queryKey: ['frequencia', turmaId],
    queryFn: () => api.get(`/professor/turmas/${turmaId}/frequencia`).then((r) => r.data),
  })
}
```

---

### `frontend/src/App.tsx` (modified — add professor routes)

**Analog:** `frontend/src/App.tsx` itself — extend existing professor block (lines 67-75)

**Current professor block** (`App.tsx` lines 67-75):
```typescript
{
  path: '/professor',
  element: <ProtectedRoute allowedRole="professor" />,
  children: [
    {
      element: <AppLayout />,
      children: [{ index: true, element: <ProfessorDashboard /> }],
    },
  ],
},
```

**Phase 4 replacement** — replace `ProfessorDashboard` stub with two routes:
```typescript
{
  path: '/professor',
  element: <ProtectedRoute allowedRole="professor" />,
  children: [
    {
      element: <AppLayout />,
      children: [
        { index: true, element: <ProfessorLandingPage /> },
        { path: 'turmas/:id', element: <ProfessorTurmaPage /> },
      ],
    },
  ],
},
```

**Import pattern** (`App.tsx` lines 9-16 — named imports):
```typescript
// Follow existing import style — one import per page, default imports:
import ProfessorLandingPage from './pages/professor/ProfessorLandingPage'
import ProfessorTurmaPage from './pages/professor/ProfessorTurmaPage'
// Remove: import ProfessorDashboard from './pages/dashboards/ProfessorDashboard'
```

---

## Shared Patterns

### Authentication Guard (backend)
**Source:** `backend/src/auth/dependencies.py` lines 37-45
**Apply to:** All endpoints in `professor/router.py`
```python
# dependencies.py lines 37-45 — require_role returns a checker closure:
def require_role(role: str):
    def checker(user: Annotated[Usuario, Depends(get_current_user)]):
        if user.tipo.value != role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado")
        return user
    return checker

# Usage in router (same as admin/router.py lines 17-18):
professor_required = Depends(require_role("professor"))
```

### DB Session Dependency
**Source:** `backend/src/admin/router.py` lines 9, 26-27
**Apply to:** All endpoint functions in `professor/router.py`
```python
from src.database import get_db
# Every endpoint signature:
db: Session = Depends(get_db),
current_user: Usuario = professor_required,
```

### db.query() style (sync SQLAlchemy)
**Source:** `backend/src/admin/service.py` lines 33-43
**Apply to:** All functions in `professor/service.py`
```python
# admin/service.py lines 33-36 — db.query() style (NOT select()):
alunos = db.query(Aluno).filter(Aluno.ativo == True).count()
# professor/service.py uses same style:
prof = db.query(Professor).filter(Professor.usuario_id == usuario.id).first()
```

### Toast Notifications (frontend)
**Source:** `frontend/src/pages/admin/AlunosPage.tsx` lines 6, 69-74
**Apply to:** All mutation hooks in professor frontend files
```typescript
import { toast } from 'sonner'
// onSuccess:
toast.success('Chamada salva com sucesso.')
// onError:
toast.error('Erro ao salvar chamada. Tente novamente.')
```

### TanStack Query mutation pattern
**Source:** `frontend/src/pages/admin/AlunosPage.tsx` lines 65-75
**Apply to:** `useSaveChamada`, `useSaveNotas` hooks in professor components
```typescript
const qc = useQueryClient()
return useMutation({
  mutationFn: (body) => api.post(url, body).then((r) => r.data),
  onSuccess: async () => {
    await qc.invalidateQueries({ queryKey: [...] })
    toast.success('...')
  },
  onError: () => toast.error('...'),
})
```

### Primary button style
**Source:** `frontend/src/pages/admin/AlunosPage.tsx` lines 200-208
**Apply to:** All save buttons in professor components
```typescript
className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md hover:bg-indigo-700 disabled:opacity-50"
```

### Input field style
**Source:** `frontend/src/pages/admin/AlunosPage.tsx` lines 152-155
**Apply to:** Date selector input in ChamadaTab, select dropdown for disciplinas
```typescript
className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
```

### Modal reuse (attendance overwrite confirmation)
**Source:** `frontend/src/components/admin/Modal.tsx` + `ConfirmDialog.tsx`
**Apply to:** Overwrite-attendance confirmation in ChamadaTab
```typescript
// ConfirmDialog.tsx is already built — import and use with custom title/message:
import { ConfirmDialog } from '../../components/admin/ConfirmDialog'
// Or use Modal directly for custom content:
import { Modal } from '../../components/admin/Modal'
```

### Pydantic ConfigDict(from_attributes=True)
**Source:** `backend/src/admin/schemas.py` lines 30-31
**Apply to:** All `*Out` schemas in `professor/schemas.py`
```python
class TurmaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
```

---

## No Analog Found

| File | Role | Data Flow | Reason |
|------|------|-----------|--------|
| `frontend/src/components/professor/TabNav.tsx` | component | event-driven | No tab navigation component exists in codebase; AdminLayout has sidebar nav (different pattern). Use UI-SPEC section 2 directly. |
| `frontend/src/components/professor/AttendanceToggle.tsx` | component | event-driven | No toggle/switch component exists. Use UI-SPEC section 3 directly. Color tokens match EntityTable badge colors. |
| `frontend/src/components/professor/Breadcrumb.tsx` | component | — | No breadcrumb component exists. Simple `<nav>` with `Link` from react-router-dom + UI-SPEC section 2 styling. |

---

## Metadata

**Analog search scope:** `backend/src/`, `backend/tests/`, `frontend/src/`
**Files scanned:** 23 Python files, 22 TypeScript files
**Pattern extraction date:** 2026-04-27

**Critical patterns confirmed:**
- `db.query()` style (sync) throughout — not `select()` style
- `db.flush()` before `db.commit()` when inserting rows that need their auto-id
- `synchronize_session=False` on bulk `.delete()` calls (same as `_sync_professor_turma`)
- `model_config = ConfigDict(from_attributes=True)` on all Out schemas
- `useQueryClient` + `invalidateQueries` after every mutation
- `keepPreviousData` import from `@tanstack/react-query` (not option flag — TQ v5 style, see `AlunosPage.tsx` line 2)
- React 19 — no `import React from 'react'` needed; functional components only
- No `react-hook-form` for grade table — plain `useState<Record<string, string>>`
