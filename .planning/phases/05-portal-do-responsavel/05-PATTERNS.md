# Phase 5: Portal do Responsável — Pattern Map

**Mapped:** 2026-04-27
**Files analyzed:** 14 (5 new backend, 2 backend modifications, 6 new frontend, 1 frontend modification)
**Analogs found:** 14 / 14

---

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `backend/src/responsavel/__init__.py` | config | — | `backend/src/professor/__init__.py` | exact |
| `backend/src/responsavel/schemas.py` | model/schema | request-response | `backend/src/professor/schemas.py` | exact |
| `backend/src/responsavel/service.py` | service | CRUD (read-only) | `backend/src/professor/service.py` | exact |
| `backend/src/responsavel/router.py` | controller | request-response | `backend/src/professor/router.py` | exact |
| `backend/tests/test_responsavel.py` | test | request-response | `backend/tests/test_professor.py` | exact |
| `backend/src/main.py` (modify) | config | — | `backend/src/main.py` | self |
| `backend/tests/conftest.py` (modify) | test | — | `backend/tests/conftest.py` | self |
| `frontend/src/pages/responsavel/ResponsavelBoletimPage.tsx` | component/page | request-response | `frontend/src/pages/professor/ProfessorLandingPage.tsx` | role-match |
| `frontend/src/components/responsavel/ChildSelector.tsx` | component | event-driven | `frontend/src/pages/admin/AlunosPage.tsx` (select pattern) | partial |
| `frontend/src/components/responsavel/SummaryCard.tsx` | component | transform | `frontend/src/components/AppLayout.tsx` (card layout) | partial |
| `frontend/src/components/responsavel/BoletimTable.tsx` | component | transform | `frontend/src/components/admin/EntityTable.tsx` | role-match |
| `frontend/src/components/responsavel/StatusBadge.tsx` | component | transform | `frontend/src/components/admin/EntityTable.tsx` (badge pattern) | partial |
| `frontend/src/components/responsavel/EmptyState.tsx` | component | — | `frontend/src/pages/professor/ProfessorLandingPage.tsx` (empty branch) | partial |
| `frontend/src/App.tsx` (modify) | config | — | `frontend/src/App.tsx` | self |

---

## Pattern Assignments

### `backend/src/responsavel/__init__.py` (config)

**Analog:** `backend/src/professor/__init__.py`

Empty file — no content needed. Python package marker only.

---

### `backend/src/responsavel/schemas.py` (model/schema, request-response)

**Analog:** `backend/src/professor/schemas.py`

**Imports pattern** (lines 1-8):
```python
from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, ConfigDict
```

**Core schema pattern** (lines 13-75 of analog):
```python
"""
Pydantic v2 schemas for professor endpoints.
All *Out schemas use model_config = ConfigDict(from_attributes=True) for SQLAlchemy -> Pydantic.
"""
from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class TurmaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    disciplinas: List[str] = []
    num_alunos: int = 0


class FrequenciaRow(BaseModel):
    aluno_id: int
    nome: str
    total_aulas: int
    total_presentes: int
    percentual: float
```

**What to replicate for responsavel/schemas.py:**

Use `ConfigDict(from_attributes=True)` on output schemas that come from ORM objects. Use bare `BaseModel` for schemas built from dicts (as in the service layer). Use `Optional[float]` (not `float | None`) for Python 3.9 compatibility, matching the analog.

Schemas needed:
```python
class FilhoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    turma_nome: Optional[str] = None


class DisciplinaBoletimRow(BaseModel):
    disciplina_id: int
    disciplina_nome: str
    bim1: Optional[float] = None
    bim2: Optional[float] = None
    bim3: Optional[float] = None
    bim4: Optional[float] = None
    media: Optional[float] = None
    total_aulas: int
    total_presentes: int
    freq_pct: Optional[float] = None
    aprovado: bool
```

Note: `DisciplinaBoletimRow` does not need `from_attributes=True` because the service returns plain dicts (same pattern as `FrequenciaRow` in the analog, which is built from a dict in `get_frequencia()`).

---

### `backend/src/responsavel/service.py` (service, CRUD read-only)

**Analog:** `backend/src/professor/service.py`

**Module docstring + imports pattern** (lines 1-26):
```python
"""
Professor service layer — chamada, notas, and frequencia business logic.

Patterns:
- _get_professor() helper resolves professor_id from current_user (Usuario) on every call
- _assert_professor_owns_turma() ownership check called at start of every turma-specific function
- db.query() style consistent with admin/service.py
...
"""
from sqlalchemy.orm import Session
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

**Profile resolver helper** (lines 29-34):
```python
def _get_professor(db: Session, usuario: Usuario) -> Professor:
    """Resolve professor.id from current_user (Usuario). Raises 404 if professor profile not found."""
    prof = db.query(Professor).filter(Professor.usuario_id == usuario.id).first()
    if not prof:
        raise HTTPException(status_code=404, detail="Perfil de professor não encontrado")
    return prof
```
Mirror exactly: `_get_responsavel()` resolves `Responsavel` using `Responsavel.usuario_id == usuario.id`. Use 404 status and Portuguese detail string.

**Ownership check helper** (lines 37-44):
```python
def _assert_professor_owns_turma(db: Session, professor_id: int, turma_id: int) -> None:
    """Raises 403 if professor is not linked to the turma via professor_turma."""
    link = db.query(ProfessorTurma).filter(
        ProfessorTurma.professor_id == professor_id,
        ProfessorTurma.turma_id == turma_id,
    ).first()
    if not link:
        raise HTTPException(status_code=403, detail="Acesso negado a esta turma")
```
Mirror: `_assert_responsavel_owns_aluno()` queries `Aluno` directly (no junction table). Returns the `Aluno` on success (avoids a second query). Uses 403, not 404, for IDOR prevention.

**Frequência aggregation core pattern** (lines 182-211):
```python
def get_frequencia(db: Session, current_user: Usuario, turma_id: int) -> list:
    prof = _get_professor(db, current_user)
    _assert_professor_owns_turma(db, prof.id, turma_id)
    chamadas = db.query(Chamada).filter(
        Chamada.turma_id == turma_id,
        Chamada.professor_id == prof.id,   # <-- CRITICAL: DO NOT copy this line to responsavel
    ).all()
    total_aulas = len(chamadas)
    chamada_ids = [c.id for c in chamadas]
    ...
    for aluno in alunos:
        if total_aulas == 0:
            total_presentes = 0
            percentual = 0.0
        else:
            total_presentes = db.query(Presenca).filter(
                Presenca.aluno_id == aluno.id,
                Presenca.chamada_id.in_(chamada_ids),
                Presenca.presente == True,
            ).count()
            percentual = (total_presentes / total_aulas) * 100.0
        result.append({...})
    return result
```
In `responsavel/service.py`, filter chamadas by `turma_id` AND `disciplina_id` only — never `professor_id`. The anti-pattern (copying `professor_id` filter) would under-count aulas.

**List comprehension + dict-based aggregation pattern** (lines 47-72):
```python
def get_minhas_turmas(db: Session, current_user: Usuario) -> list:
    prof = _get_professor(db, current_user)
    links = db.query(ProfessorTurma).filter(
        ProfessorTurma.professor_id == prof.id
    ).all()

    turma_map: dict[int, dict] = {}
    for link in links:
        ...
    return list(turma_map.values())
```
Services return plain Python dicts from `list`. Pydantic validates on exit via `response_model`. No `.model_dump()` call needed in the service.

---

### `backend/src/responsavel/router.py` (controller, request-response)

**Analog:** `backend/src/professor/router.py`

**Full router pattern** (lines 1-75):
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


@router.get("/minhas-turmas", response_model=list[schemas.TurmaOut])
def get_minhas_turmas(
    db: Session = Depends(get_db),
    current_user: Usuario = professor_required,
):
    return service.get_minhas_turmas(db, current_user)


@router.get("/turmas/{turma_id}/chamada")
def get_chamada(
    turma_id: int,
    date: str = Query(...),
    db: Session = Depends(get_db),
    current_user: Usuario = professor_required,
):
    return service.get_chamada(db, current_user, turma_id, date)
```

Adapt to:
- `prefix="/responsavel"`, `tags=["responsavel"]`
- `responsavel_required = Depends(require_role("responsavel"))`
- Two GET-only endpoints: `/meus-filhos` (no path params) and `/boletim` (`aluno_id: int = Query(...)`)
- Import `from . import schemas, service` — same relative import pattern

**Query parameter pattern** (lines 30-35):
```python
@router.get("/turmas/{turma_id}/chamada")
def get_chamada(
    turma_id: int,
    date: str = Query(...),
    db: Session = Depends(get_db),
    current_user: Usuario = professor_required,
):
```
For `/boletim`: `aluno_id: int = Query(...)` — same `Query(...)` required-param pattern.

---

### `backend/src/main.py` (modification)

**Analog:** `backend/src/main.py` (self)

**Current router registration block** (lines 9-13, 49-52):
```python
from src.auth.router import router as auth_router
from src.auth.service import maybe_renew_token
from src.password_reset.router import router as reset_router
from src.admin.router import router as admin_router
from src.professor.router import router as professor_router

...

app.include_router(auth_router)
app.include_router(reset_router, prefix="/auth")
app.include_router(admin_router)
app.include_router(professor_router)
```

Add after `professor_router` import:
```python
from src.responsavel.router import router as responsavel_router
```
Add after `app.include_router(professor_router)`:
```python
app.include_router(responsavel_router)
```

No other changes to `main.py`.

---

### `backend/tests/conftest.py` (modification)

**Analog:** `backend/tests/conftest.py` (self)

**Professor fixture pair to mirror** (lines 75-100):
```python
@pytest.fixture(scope="function")
def professor_user(test_db):
    """Creates a professor Usuario in the test DB and returns it."""
    user = Usuario(
        email="prof@test.com",
        senha_hash=hash_password("profpass"),
        tipo=TipoUsuario.professor,
        ativo=True,
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture(scope="function")
def professor_headers(professor_user):
    """Authorization headers for a professor user JWT."""
    token = create_access_token({"sub": str(professor_user.id), "tipo": "professor"})
    return {"Authorization": f"Bearer {token}"}
```

Add exactly two new fixtures mirroring this pair:
```python
@pytest.fixture(scope="function")
def responsavel_user(test_db):
    """Creates a responsavel Usuario in the test DB and returns it."""
    user = Usuario(
        email="resp@test.com",
        senha_hash=hash_password("resppass"),
        tipo=TipoUsuario.responsavel,
        ativo=True,
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture(scope="function")
def responsavel_headers(responsavel_user):
    """Authorization headers for a responsavel user JWT."""
    token = create_access_token({"sub": str(responsavel_user.id), "tipo": "responsavel"})
    return {"Authorization": f"Bearer {token}"}
```

`TipoUsuario.responsavel` is already importable — `Responsavel` model and `TipoUsuario` enum are already imported in conftest (line 20: `from src.models.responsavel import Responsavel`).

---

### `backend/tests/test_responsavel.py` (test, request-response)

**Analog:** `backend/tests/test_professor.py`

**Module docstring + imports pattern** (lines 1-19):
```python
"""
Professor endpoint tests — Phase 4.

Tests cover PROF-01 through PROF-05 plus access control.
Run: cd backend && python -m pytest tests/test_professor.py -x -q
"""
import pytest
from datetime import date

from src.models.professor import Professor
from src.models.turma import Turma
from src.models.disciplina import Disciplina
from src.models.aluno import Aluno
from src.models.professor_turma import ProfessorTurma
from src.models.chamada import Chamada
from src.models.presenca import Presenca
from src.models.avaliacao import Avaliacao
from src.models.nota import Nota
```

**Setup helper pattern** (lines 25-45):
```python
def _setup_professor_with_turma(test_db, professor_user):
    """Create Professor profile, Turma, Disciplina, Aluno, and professor_turma link."""
    prof = Professor(usuario_id=professor_user.id, nome="Prof Teste", cpf="00000000001")
    test_db.add(prof)
    test_db.flush()

    turma = Turma(nome="7A", ano=2026, serie="7", turno="manha")
    test_db.add(turma)
    disciplina = Disciplina(nome="Matematica")
    test_db.add(disciplina)
    test_db.flush()

    aluno = Aluno(nome="Aluno Um", matricula="MAT0001", ativo=True, turma_id=turma.id)
    test_db.add(aluno)
    test_db.flush()

    link = ProfessorTurma(professor_id=prof.id, turma_id=turma.id, disciplina_id=disciplina.id)
    test_db.add(link)
    test_db.commit()

    return prof, turma, disciplina, aluno
```
Mirror: `_setup_responsavel_with_filho(test_db, responsavel_user)` creates `Responsavel` profile, `Turma`, `Disciplina`, `Aluno` (with `responsavel_id` set), and `ProfessorTurma` link (needed for boletim disciplina discovery). Returns `(resp, turma, disciplina, aluno)`.

**Security test pattern** (lines 52-63):
```python
def test_unauthenticated_gets_401(client):
    """Unauthenticated request to any /professor endpoint returns 401."""
    response = client.get("/professor/minhas-turmas")
    assert response.status_code == 401


def test_admin_role_rejected(client, admin_headers):
    """Admin JWT receives 403 on /professor endpoints (T-04-01)."""
    response = client.get("/professor/minhas-turmas", headers=admin_headers)
    assert response.status_code == 403
```

**Ownership / IDOR test pattern** (lines 68-81):
```python
def test_ownership_check(client, test_db, professor_user, professor_headers):
    """Professor cannot access a turma they are not linked to (PROF-02, T-04-02)."""
    prof = Professor(usuario_id=professor_user.id, nome="Prof Dono", cpf="00000000002")
    test_db.add(prof)
    turma = Turma(nome="9B", ano=2026, serie="9", turno="manha")
    test_db.add(turma)
    test_db.commit()

    response = client.get(
        f"/professor/turmas/{turma.id}/chamada?date=2026-04-27",
        headers=professor_headers,
    )
    assert response.status_code == 403
```
For RESP-06: create two responsavel users, link an aluno to one, then assert the other gets 403 (not 404) on `/responsavel/boletim?aluno_id=X`.

**Aggregation assertion pattern** (lines 236-263):
```python
def test_frequencia_aggregation(client, test_db, professor_user, professor_headers):
    ...
    response = client.get(
        f"/professor/turmas/{turma.id}/frequencia",
        headers=professor_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    row = data[0]
    assert row["aluno_id"] == aluno.id
    assert row["total_aulas"] == 2
    assert row["total_presentes"] == 1
    assert row["percentual"] == pytest.approx(50.0)
```
Use `pytest.approx()` for float comparisons (média, freq_pct). Assert exact field names matching `DisciplinaBoletimRow` schema.

---

### `frontend/src/pages/responsavel/ResponsavelBoletimPage.tsx` (component/page, request-response)

**Analog:** `frontend/src/pages/professor/ProfessorLandingPage.tsx`

**Full analog** (lines 1-53):
```typescript
import { useQuery } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { api } from '../../services/api'
import { TurmaCard } from '../../components/professor/TurmaCard'

interface Turma {
  id: number
  nome: string
  disciplinas: string[]
  num_alunos: number
}

function useMinhasTurmas() {
  return useQuery<Turma[]>({
    queryKey: ['minhas-turmas'],
    queryFn: () => api.get('/professor/minhas-turmas').then((r) => r.data),
  })
}

export default function ProfessorLandingPage() {
  const navigate = useNavigate()
  const { data: turmas, isLoading } = useMinhasTurmas()

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold text-gray-900">Minhas Turmas</h1>
      <p className="text-sm text-gray-500 mt-1">
        Selecione uma turma para registrar chamada ou lancar notas
      </p>

      {isLoading ? (
        <div className="text-center py-12 text-gray-400 text-sm">Carregando turmas...</div>
      ) : !turmas || turmas.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-xl font-medium text-gray-900">Nenhuma turma vinculada</p>
          ...
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mt-6">
          {turmas.map((t) => (
            <TurmaCard key={t.id} turma={t} onClick={() => navigate(`/professor/turmas/${t.id}`)} />
          ))}
        </div>
      )}
    </div>
  )
}
```

**Adapt for ResponsavelBoletimPage:**
- Two `useQuery` hooks: `useMeusFilhos()` and `useBoletim(alunoId)` (see RESEARCH.md Pattern 8)
- `useState<number | null>(null)` for `selectedAlunoId`; auto-select first filho on data load with `useEffect`
- Content area layout: `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8` (replaces `p-8` to match AppLayout + `pt-16` offset)
- Three-branch render: loading → empty (`filhos.length === 0`) → main content (ChildSelector + SummaryCard + BoletimTable)
- No `useNavigate` needed (read-only, no navigation)

**useBoletim enabled guard** (from RESEARCH.md Pattern 8):
```typescript
function useBoletim(alunoId: number | null) {
  return useQuery<DisciplinaBoletimRow[]>({
    queryKey: ['boletim', alunoId],
    queryFn: () =>
      api.get('/responsavel/boletim', { params: { aluno_id: alunoId } }).then((r) => r.data),
    enabled: alunoId !== null,
  })
}
```
`enabled: alunoId !== null` prevents the query from firing before child selection resolves.

---

### `frontend/src/components/responsavel/ChildSelector.tsx` (component, event-driven)

**Analog:** `frontend/src/pages/admin/AlunosPage.tsx` (select element pattern, lines 170-178)

**Native select pattern:**
```typescript
<select
  {...register('turma_id', { setValueAs: (v) => (v === '' ? null : Number(v)) })}
  className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
>
  <option value="">Sem turma</option>
  {(turmasData ?? []).map((t: { id: number; nome: string }) => (
    <option key={t.id} value={t.id}>{t.nome}</option>
  ))}
</select>
```

**Adapt for ChildSelector — uncontrolled native select (no react-hook-form):**
```typescript
interface ChildSelectorProps {
  filhos: FilhoOut[]
  selectedId: number | null
  onChange: (id: number) => void
}

export function ChildSelector({ filhos, selectedId, onChange }: ChildSelectorProps) {
  if (filhos.length <= 1) return null   // visibility rule from UI-SPEC

  return (
    <div className="mb-6">
      <label className="block text-sm font-normal text-gray-700 mb-1">Filho(a)</label>
      <select
        value={selectedId ?? ''}
        onChange={(e) => onChange(Number(e.target.value))}
        className="w-full sm:w-72 border border-gray-300 rounded-md text-sm px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white"
      >
        {filhos.map((f) => (
          <option key={f.id} value={f.id}>
            {f.nome}{f.turma_nome ? ` — ${f.turma_nome}` : ''}
          </option>
        ))}
      </select>
    </div>
  )
}
```

Classes match UI-SPEC exactly: `w-full sm:w-72`, `focus:ring-2 focus:ring-indigo-500`, `bg-white`.

---

### `frontend/src/components/responsavel/SummaryCard.tsx` (component, transform)

**Analog:** `frontend/src/components/AppLayout.tsx` (card/panel layout), `frontend/src/components/admin/EntityTable.tsx` (badge pattern)

**Badge pattern from EntityTable** (lines 87-92):
```typescript
<span
  className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
    row[col.key] ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
  }`}
>
  {row[col.key] ? 'Ativo' : 'Inativo'}
</span>
```

**SummaryCard — three variant pattern (from UI-SPEC):**
```typescript
interface SummaryCardProps {
  rows: DisciplinaBoletimRow[]
}

export function SummaryCard({ rows }: SummaryCardProps) {
  const atRiskCount = rows.filter(r => !r.aprovado).length

  if (atRiskCount === 0) {
    return (
      <div className="bg-green-50 border border-green-200 rounded-lg p-6 mb-6">
        {/* icon aria-hidden="true" */}
        <p className="text-xl font-semibold text-green-800">Aprovado em todas as disciplinas</p>
        <p className="text-sm text-green-700">Média e frequência estão dentro dos limites exigidos.</p>
      </div>
    )
  }

  // at-risk or failed variant
  return (
    <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 mb-6">
      {/* icon aria-hidden="true" */}
      <p className="text-xl font-semibold text-yellow-800">{atRiskCount} disciplina(s) em risco de reprovação</p>
      <p className="text-sm text-yellow-700">Verifique as disciplinas destacadas abaixo...</p>
    </div>
  )
}
```

Icons are inline SVG with `aria-hidden="true"` (UI-SPEC accessibility requirement). Three variants: green (all approved), yellow (at risk), red (confirmed failed). Derive `atRiskCount` from `rows.filter(r => !r.aprovado).length` — no separate API call.

---

### `frontend/src/components/responsavel/BoletimTable.tsx` (component, transform)

**Analog:** `frontend/src/components/admin/EntityTable.tsx`

**Table structure pattern** (lines 64-119):
```typescript
<div className="overflow-x-auto">
  <table className="min-w-full divide-y divide-gray-200">
    <thead className="bg-gray-50">
      <tr>
        {columns.map((col) => (
          <th
            key={col.key}
            className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
          >
            {col.label}
          </th>
        ))}
        <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
          Ações
        </th>
      </tr>
    </thead>
    <tbody className="bg-white divide-y divide-gray-200">
      {rows.map((row, i) => (
        <tr key={(row.id as number) ?? i} className="hover:bg-gray-50">
          {columns.map((col) => (
            <td key={col.key} className="px-4 py-3 text-sm text-gray-700 whitespace-nowrap">
              ...
            </td>
          ))}
        </tr>
      ))}
    </tbody>
  </table>
</div>
```

**Adapt for BoletimTable — key differences from analog:**
- No action column (read-only portal)
- Row highlight: `row.aprovado === false || (row.freq_pct !== null && row.freq_pct < 75) || (row.media !== null && row.media < 5.0)` → `bg-red-50 hover:bg-red-100` instead of `hover:bg-gray-50`
- Cell padding: `px-3 py-2` (more compact than analog's `px-4 py-3`)
- Numeric bimestre cells: `text-center`; missing nota: `text-gray-400` with "—"
- Média cell: conditional `text-red-700 font-semibold` when `media < 5.0`
- Frequência cell: `"${row.freq_pct?.toFixed(0)}% (${row.total_presentes}/${row.total_aulas})"` — conditional `text-red-700 font-semibold` when < 75
- Status column: `<StatusBadge aprovado={row.aprovado} />`
- Table header cell classes: `px-3 py-2 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider` (per UI-SPEC — `font-semibold` not `font-medium`)
- Semantic HTML: `<th scope="col">` on all header cells (accessibility)
- `min-w-[640px]` on table for mobile horizontal scroll

**Loading branch from EntityTable** (lines 59-61):
```typescript
{isLoading ? (
  <div className="text-center py-12 text-gray-400 text-sm">Carregando...</div>
) : rows.length === 0 ? (
  <div className="text-center py-12 text-gray-400 text-sm">Nenhum registro encontrado.</div>
) : (
```

---

### `frontend/src/components/responsavel/StatusBadge.tsx` (component, transform)

**Analog:** `frontend/src/components/admin/EntityTable.tsx` (badge in lines 87-92):
```typescript
<span
  className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
    row[col.key] ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
  }`}
>
  {row[col.key] ? 'Ativo' : 'Inativo'}
</span>
```

**StatusBadge — simple boolean-driven component:**
```typescript
interface StatusBadgeProps {
  aprovado: boolean
}

export function StatusBadge({ aprovado }: StatusBadgeProps) {
  return (
    <span
      className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold ${
        aprovado ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
      }`}
    >
      {aprovado ? 'Aprovado' : 'Reprovado'}
    </span>
  )
}
```

Classes from UI-SPEC: `inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold` (note `font-semibold` — badge typography from UI-SPEC, not `font-medium` from EntityTable). Colors: `bg-green-100 text-green-800` / `bg-red-100 text-red-800`.

---

### `frontend/src/components/responsavel/EmptyState.tsx` (component)

**Analog:** `frontend/src/pages/professor/ProfessorLandingPage.tsx` (empty branch, lines 33-38):
```typescript
) : !turmas || turmas.length === 0 ? (
  <div className="text-center py-12">
    <p className="text-xl font-medium text-gray-900">Nenhuma turma vinculada</p>
    <p className="text-sm text-gray-500 mt-2">
      Entre em contato com a administracao para vincular turmas ao seu perfil.
    </p>
  </div>
)
```

**Adapt for EmptyState — two variant component:**
```typescript
type EmptyStateVariant = 'no-children' | 'no-data'

interface EmptyStateProps {
  variant: EmptyStateVariant
}

export function EmptyState({ variant }: EmptyStateProps) {
  const config = {
    'no-children': {
      heading: 'Nenhum aluno vinculado',
      body: 'Entre em contato com a administração para vincular seu perfil a um aluno.',
    },
    'no-data': {
      heading: 'Boletim não disponível',
      body: 'As notas e frequências ainda não foram lançadas para este aluno.',
    },
  }[variant]

  return (
    <div className="text-center py-12">
      {/* inline SVG icon aria-hidden="true" — 48px, text-gray-300 */}
      <p className="text-xl font-semibold text-gray-900 mt-4">{config.heading}</p>
      <p className="text-sm text-gray-500 mt-2">{config.body}</p>
    </div>
  )
}
```

Icons: inline SVG (`aria-hidden="true"`) at 48px, `text-gray-300`. Heading uses `font-semibold` (UI-SPEC typography for card title), not `font-medium` (analog).

---

### `frontend/src/App.tsx` (modification)

**Analog:** `frontend/src/App.tsx` (self)

**Current responsavel import and route** (lines 17, 81-88):
```typescript
import ResponsavelDashboard from './pages/dashboards/ResponsavelDashboard'

...

{
  path: '/responsavel',
  element: <ProtectedRoute allowedRole="responsavel" />,
  children: [
    {
      element: <AppLayout />,
      children: [{ index: true, element: <ResponsavelDashboard /> }],
    },
  ],
},
```

Change **only** the import line and the index route element:
```typescript
// Remove:
import ResponsavelDashboard from './pages/dashboards/ResponsavelDashboard'
// Add:
import ResponsavelBoletimPage from './pages/responsavel/ResponsavelBoletimPage'

// In router, change:
{ index: true, element: <ResponsavelDashboard /> }
// To:
{ index: true, element: <ResponsavelBoletimPage /> }
```

No other changes to App.tsx. Route structure, ProtectedRoute, and AppLayout wiring are already correct.

---

## Shared Patterns

### Authentication / Role Guard

**Source:** `backend/src/professor/router.py` lines 17, 23-25
**Apply to:** `responsavel/router.py` — every endpoint

```python
professor_required = Depends(require_role("professor"))

@router.get("/minhas-turmas", response_model=list[schemas.TurmaOut])
def get_minhas_turmas(
    db: Session = Depends(get_db),
    current_user: Usuario = professor_required,
):
```

Pattern: define role dependency once as module-level constant (`responsavel_required = Depends(require_role("responsavel"))`), reuse as default value on every endpoint's `current_user` parameter.

### Ownership Check (IDOR Prevention)

**Source:** `backend/src/professor/service.py` lines 37-44
**Apply to:** Every function in `responsavel/service.py` that accepts `aluno_id`

```python
def _assert_professor_owns_turma(db: Session, professor_id: int, turma_id: int) -> None:
    link = db.query(ProfessorTurma).filter(...).first()
    if not link:
        raise HTTPException(status_code=403, detail="Acesso negado a esta turma")
```

Use 403 (not 404) on failure. Must be the FIRST call in any endpoint function, before data queries.

### Profile Resolver Helper

**Source:** `backend/src/professor/service.py` lines 29-34
**Apply to:** `responsavel/service.py` — `_get_responsavel()` called at top of every service function

```python
def _get_professor(db: Session, usuario: Usuario) -> Professor:
    prof = db.query(Professor).filter(Professor.usuario_id == usuario.id).first()
    if not prof:
        raise HTTPException(status_code=404, detail="Perfil de professor não encontrado")
    return prof
```

Use 404 status (profile not found is a legitimate server-side data error, not a client access error).

### TanStack Query useQuery Hook

**Source:** `frontend/src/pages/professor/ProfessorLandingPage.tsx` lines 13-18
**Apply to:** `ResponsavelBoletimPage.tsx` — all data fetching

```typescript
function useMinhasTurmas() {
  return useQuery<Turma[]>({
    queryKey: ['minhas-turmas'],
    queryFn: () => api.get('/professor/minhas-turmas').then((r) => r.data),
  })
}
```

Pattern: define per-file hook functions at module level, above the component. Use typed generics on `useQuery<T>`. Include all dynamic parameters in `queryKey` array (prevents stale cache on selector change).

### Axios `api` Instance

**Source:** `frontend/src/pages/professor/ProfessorLandingPage.tsx` line 3
**Apply to:** All frontend files that fetch data

```typescript
import { api } from '../../services/api'
```

Never use raw `fetch`. The `api` axios instance handles Bearer token injection and 401 redirect automatically.

### Tailwind Loading / Empty State

**Source:** `frontend/src/pages/professor/ProfessorLandingPage.tsx` lines 31-39
**Apply to:** `ResponsavelBoletimPage.tsx` loading and empty branches

```typescript
{isLoading ? (
  <div className="text-center py-12 text-gray-400 text-sm">Carregando turmas...</div>
) : !turmas || turmas.length === 0 ? (
  <div className="text-center py-12">
    ...
  </div>
) : (
  ...
)}
```

Three-branch pattern: loading → empty → content. Use this same top-level structure in `ResponsavelBoletimPage`.

### Table Wrapper + Semantic HTML

**Source:** `frontend/src/components/admin/EntityTable.tsx` lines 64-119
**Apply to:** `BoletimTable.tsx`

```typescript
<div className="overflow-x-auto">
  <table className="min-w-full divide-y divide-gray-200">
    <thead className="bg-gray-50">
      <tr>
        <th scope="col" className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
          ...
        </th>
      </tr>
    </thead>
    <tbody className="bg-white divide-y divide-gray-200">
      ...
    </tbody>
  </table>
</div>
```

Add `scope="col"` on `<th>` (not in analog — required by UI-SPEC accessibility). Wrap in `overflow-x-auto` for mobile scroll.

### pytest Fixture Setup Helper

**Source:** `backend/tests/test_professor.py` lines 25-45
**Apply to:** `test_responsavel.py` — `_setup_responsavel_with_filho()` helper

```python
def _setup_professor_with_turma(test_db, professor_user):
    prof = Professor(usuario_id=professor_user.id, nome="Prof Teste", cpf="00000000001")
    test_db.add(prof)
    test_db.flush()
    ...
    test_db.commit()
    return prof, turma, disciplina, aluno
```

Use `test_db.flush()` after each object before creating dependents (so FK IDs are populated). Use `test_db.commit()` once at the end. Return all created objects for use in test assertions.

---

## No Analog Found

All files have analogs in the codebase. No files require falling back to RESEARCH.md patterns exclusively.

---

## Metadata

**Analog search scope:** `backend/src/professor/`, `backend/src/main.py`, `backend/tests/`, `frontend/src/pages/professor/`, `frontend/src/pages/admin/`, `frontend/src/components/admin/`, `frontend/src/components/AppLayout.tsx`, `frontend/src/App.tsx`
**Files scanned:** 10 source files read directly
**Pattern extraction date:** 2026-04-27
