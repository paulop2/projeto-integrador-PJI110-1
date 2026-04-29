---
phase: 06-dashboard-e-polish
reviewed: 2026-04-29T12:00:00Z
depth: standard
files_reviewed: 16
files_reviewed_list:
  - backend/src/admin/router.py
  - backend/src/admin/schemas.py
  - backend/src/admin/service.py
  - backend/src/professor/schemas.py
  - backend/src/professor/service.py
  - backend/tests/test_admin.py
  - backend/tests/test_professor.py
  - frontend/src/components/SkeletonCard.tsx
  - frontend/src/components/SkeletonRow.tsx
  - frontend/src/components/SkeletonTable.tsx
  - frontend/src/components/admin/EntityTable.tsx
  - frontend/src/components/professor/TurmaCard.tsx
  - frontend/src/pages/admin/AdminDashboard.tsx
  - frontend/src/pages/professor/ProfessorLandingPage.tsx
  - frontend/src/pages/responsavel/ResponsavelBoletimPage.tsx
  - frontend/src/services/api.ts
findings:
  critical: 2
  warning: 8
  info: 8
  total: 18
status: issues_found
---

# Phase 06: Code Review Report

**Reviewed:** 2026-04-29
**Depth:** standard
**Files Reviewed:** 16
**Status:** issues_found

## Summary

The phase adds admin dashboard aggregation, professor landing metrics, and UI skeletons/polish. The backend service layer is functionally sound but contains **two critical security/correctness issues**: a raw `Usuario` object returned without a response model (leaking `senha_hash`) and a type-mismatch in the professor chamada service that triggers a 500 error when no attendance record exists. Several warnings around silent data-validation failures, missing input sanitisation, and unhandled edge cases were also found. The frontend components are clean, but error-state handling is incomplete on a few pages. Tests are well-structured and do not contain reliability defects.

## Critical Issues

### CR-01: Raw `Usuario` object returned without response model leaks password hash

**File:** `backend/src/admin/router.py:231-237`
**Issue:** The `POST /admin/usuarios/{usuario_id}/deactivate` endpoint lacks a `response_model`. It returns the raw SQLAlchemy `Usuario` instance from `service.deactivate_usuario()`. The `Usuario` model contains `senha_hash` (and potentially other sensitive fields), so FastAPI serialises and leaks the hashed password to the admin caller.
**Fix:** Add a safe response schema or return a minimal dict:
```python
@router.post("/usuarios/{usuario_id}/deactivate", response_model=schemas.UsuarioOut)
def deactivate_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    caller: Usuario = Depends(require_role("admin")),
):
    return service.deactivate_usuario(db, target_id=usuario_id, caller_id=caller.id)
```
(If no `UsuarioOut` exists yet, define one that exposes only `id`, `email`, `ativo`, and `tipo`.)

### CR-02: `get_chamada` returns `None` for non-optional `id` field

**File:** `backend/src/professor/service.py:160`
**Issue:** When no `Chamada` exists, the function returns `{"id": None, "data": date_str, "presencas": []}`. The `ChamadaOut` schema defines `id: int`, so `None` violates the contract. If the router declares `response_model=schemas.ChamadaOut`, FastAPI/Pydantic raises a validation error and the endpoint crashes with 500 on a normal "not found" case.
**Fix:** Make `id` optional in the schema to match the service contract:
```python
class ChamadaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
    data: date
    presencas: List[PresencaOut] = []
```

## Warnings

### WR-01: `create_responsavel` silently ignores invalid `aluno_ids`

**File:** `backend/src/admin/service.py:392-395`
**Issue:** When linking alunos to a new responsável, if an `aluno_id` does not exist the loop simply skips it. The API still returns 201, misleading the caller into believing all links were created.
**Fix:**
```python
for aluno_id in body.aluno_ids:
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=400, detail=f"Aluno {aluno_id} não encontrado")
    aluno.responsavel_id = responsavel.id
```

### WR-02: `update_responsavel` silently ignores invalid `aluno_ids`

**File:** `backend/src/admin/service.py:412-415`
**Issue:** Same silent-skip behaviour as WR-01 when updating a responsável's linked alunos.
**Fix:** Raise `HTTPException(400, ...)` when `aluno` is `None`, identical to WR-01.

### WR-03: `get_chamada` crashes on malformed date strings

**File:** `backend/src/professor/service.py:153`
**Issue:** `datetime.strptime(date_str, "%Y-%m-%d")` raises an unhandled `ValueError` for invalid formats, causing a 500 Internal Server Error instead of a 422 Unprocessable Entity.
**Fix:**
```python
try:
    target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
except ValueError:
    raise HTTPException(status_code=422, detail="Data inválida, use o formato YYYY-MM-DD")
```

### WR-04: `upsert_chamada` allows presencas for students outside the turma

**File:** `backend/src/professor/service.py:189-190`
**Issue:** The service never verifies that each `aluno_id` in `payload.presencas` belongs to the requested `turma_id`. A buggy or malicious request can create attendance records for arbitrary students.
**Fix:** Validate against the turma roster before inserting:
```python
allowed = {a.id for a in db.query(Aluno).filter(Aluno.turma_id == turma_id, Aluno.ativo == True).all()}
for p in payload.presencas:
    if p.aluno_id not in allowed:
        raise HTTPException(status_code=422, detail=f"Aluno {p.aluno_id} não pertence à turma")
    db.add(Presenca(chamada_id=chamada.id, aluno_id=p.aluno_id, presente=p.presente))
```

### WR-05: `upsert_notas` allows grades for students outside the turma

**File:** `backend/src/professor/service.py:221-252`
**Issue:** Similar to WR-04, `grade.aluno_id` is not validated against the turma roster, permitting grades to be assigned to students who are not enrolled in the class.
**Fix:** Query the turma's active alunos once at the start of the function and reject any `grade.aluno_id` not in the allowed set.

### WR-06: Password creation schemas lack minimum length validation

**File:** `backend/src/admin/schemas.py:125, 157`
**Issue:** `ProfessorCreate.senha` and `ResponsavelCreate.senha` accept empty strings or trivial passwords, weakening account security.
**Fix:**
```python
from pydantic import Field

class ProfessorCreate(BaseModel):
    ...
    senha: str = Field(..., min_length=8)
```
(Apply the same to `ResponsavelCreate`.)

### WR-07: `_sync_professor_turma` does not validate foreign-key targets

**File:** `backend/src/admin/service.py:224-232`
**Issue:** The function blindly inserts `professor_turma` rows. If `professor_id` or `disciplina_id` does not exist, the database raises an `IntegrityError`, which bubbles up as an unhandled 500.
**Fix:** Validate existence before insert:
```python
for row in rows:
    if not db.query(Professor).filter(Professor.id == row.professor_id).first():
        raise HTTPException(status_code=400, detail=f"Professor {row.professor_id} não encontrado")
    if not db.query(Disciplina).filter(Disciplina.id == row.disciplina_id).first():
        raise HTTPException(status_code=400, detail=f"Disciplina {row.disciplina_id} não encontrada")
    db.add(ProfessorTurma(turma_id=turma_id, disciplina_id=row.disciplina_id, professor_id=row.professor_id))
```

### WR-08: AdminDashboard hides desempenho errors silently

**File:** `frontend/src/pages/admin/AdminDashboard.tsx:51-136`
**Issue:** `useAdminDesempenho` is not destructured for `isError`. If the request fails, `desempenho` is undefined and the entire "Desempenho por Turma" section disappears without any feedback to the user.
**Fix:**
```tsx
const { data: desempenho, isLoading: desempenhoLoading, isError: desempenhoError } = useAdminDesempenho()
...
{desempenhoError && (
  <div className="mb-4 p-3 bg-red-50 text-red-700 text-sm rounded-md border border-red-200">
    Erro ao carregar desempenho.
  </div>
)}
```

## Info

### IN-01: Unused SQLAlchemy imports in admin service

**File:** `backend/src/admin/service.py:14`
**Issue:** `select` and `func` are imported from `sqlalchemy` but never used.
**Fix:** Remove the unused imports.

### IN-02: Unused SQLAlchemy import in professor service

**File:** `backend/src/professor/service.py:13`
**Issue:** `func` is imported from `sqlalchemy` but never used.
**Fix:** Remove the unused import.

### IN-03: Deprecated `datetime.utcnow()` usage

**File:** `backend/src/admin/service.py:184`
**Issue:** `datetime.utcnow()` is deprecated since Python 3.12.
**Fix:** Replace with `datetime.now(timezone.utc).year` (and import `timezone` from `datetime`).

### IN-04: Incorrect ordinal indicator in bimestre title

**File:** `backend/src/professor/service.py:234`
**Issue:** `f"{grade.bimestre}o Bimestre"` uses a plain letter "o". The correct Portuguese ordinal indicator is "º".
**Fix:** `f"{grade.bimestre}º Bimestre"`

### IN-05: Toast may display `[object Object]` on validation errors

**File:** `frontend/src/services/api.ts:52`
**Issue:** Pydantic validation errors return `detail` as an array of objects. Passing an array directly to `toast.error()` produces poor user-facing output.
**Fix:** Normalise the message before toasting:
```ts
const raw = error.response?.data?.detail
const msg = Array.isArray(raw)
  ? raw.map((d: any) => d.msg || String(d)).join(', ')
  : (raw || 'Erro no servidor. Tente novamente em instantes.')
toast.error(msg)
```

### IN-06: Missing error state in ProfessorLandingPage

**File:** `frontend/src/pages/professor/ProfessorLandingPage.tsx:25`
**Issue:** `useMinhasTurmas` error state is ignored. A network failure renders the "Nenhuma turma vinculada" empty state, which is misleading.
**Fix:** Destructure `isError` from the hook and render an error banner when true.

### IN-07: Missing error states in ResponsavelBoletimPage

**File:** `frontend/src/pages/responsavel/ResponsavelBoletimPage.tsx:48, 58`
**Issue:** Both `useMeusFilhos` and `useBoletim` error states are ignored. API failures display empty/skeleton states instead of error feedback.
**Fix:** Destructure `isError` for each query and render appropriate error messages.

### IN-08: Duplicate aprovado-calculation logic

**File:** `backend/src/admin/service.py:51-87` and `backend/src/professor/service.py:47-83`
**Issue:** `_calcular_media_freq_aprovado` and `_calcular_aprovado` are nearly identical. Divergence between the two could lead to inconsistent LDB metrics.
**Fix:** Extract a shared helper (e.g., `src/shared/calcular_aprovado.py`) and reuse it in both services.

---

_Reviewed: 2026-04-29_
_Reviewer: gsd-code-reviewer_
_Depth: standard_
