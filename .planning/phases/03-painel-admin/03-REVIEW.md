---
phase: 03-painel-admin
reviewed: 2025-04-29T00:00:00Z
depth: standard
files_reviewed: 29
files_reviewed_list:
  - backend/requirements.txt
  - backend/src/admin/__init__.py
  - backend/src/admin/router.py
  - backend/src/admin/schemas.py
  - backend/src/admin/service.py
  - backend/src/main.py
  - backend/src/models/__init__.py
  - backend/src/models/aluno.py
  - backend/src/models/disciplina.py
  - backend/src/models/professor.py
  - backend/src/models/professor_turma.py
  - backend/src/models/responsavel.py
  - backend/src/models/turma.py
  - backend/tests/__init__.py
  - backend/tests/conftest.py
  - backend/tests/test_admin.py
  - frontend/src/App.tsx
  - frontend/src/components/admin/AdminLayout.tsx
  - frontend/src/components/admin/ConfirmDialog.tsx
  - frontend/src/components/admin/EntityTable.tsx
  - frontend/src/components/admin/Modal.tsx
  - frontend/src/components/admin/Sidebar.tsx
  - frontend/src/index.css
  - frontend/src/main.tsx
  - frontend/src/pages/admin/AdminDashboard.tsx
  - frontend/src/pages/admin/AlunosPage.tsx
  - frontend/src/pages/admin/DisciplinasPage.tsx
  - frontend/src/pages/admin/ProfessoresPage.tsx
  - frontend/src/pages/admin/ResponsaveisPage.tsx
  - frontend/src/pages/admin/TurmasPage.tsx
findings:
  critical: 3
  warning: 11
  info: 3
  total: 17
status: issues_found
---

# Phase 03: Code Review Report

**Reviewed:** 2025-04-29
**Depth:** standard
**Files Reviewed:** 29
**Status:** issues_found

## Summary

Reviewed the full Phase 03 admin panel implementation (backend CRUD service + router, SQLAlchemy models, frontend React pages and components, and pytest test suite). The code follows the project's established patterns (SQLAlchemy 1.x query style, Pydantic v2 schemas, React Query + react-hook-form + zod on the frontend). However, three **critical** issues were found: a security vulnerability exposing password hashes via an unprotected endpoint, and two data-loss bugs in frontend edit modals that fail to pre-populate relational data. Several warnings around type safety, UX, deprecated APIs, and duplicate error handling were also identified.

---

## Critical Issues

### CR-01: `deactivate_usuario` endpoint exposes `senha_hash` (security vulnerability)

**File:** `backend/src/admin/router.py:231-237`
**Issue:** The `POST /admin/usuarios/{usuario_id}/deactivate` endpoint has **no `response_model`**. It returns the raw SQLAlchemy `Usuario` model from `service.deactivate_usuario()`. Since `Usuario` contains `senha_hash`, `email`, `tipo`, and `reset_tokens`, FastAPI's default serialization will include the hashed password in the JSON response. This is a credential-exposure vulnerability.
**Fix:** Add a dedicated `UsuarioOut` schema (or reuse an existing one) that explicitly excludes `senha_hash` and relationships:
```python
class UsuarioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: str
    tipo: str
    ativo: bool

@router.post("/usuarios/{usuario_id}/deactivate", response_model=UsuarioOut)
def deactivate_usuario(...):
    ...
```

### CR-02: Editing a Turma wipes all existing `professor_turma` assignments (data loss)

**File:** `frontend/src/pages/admin/TurmasPage.tsx:106-112`
**Issue:** When the `TurmaModal` opens in edit mode, the `useEffect` resets the form with `professor_turma: []` (hardcoded empty array). The modal never fetches existing professor/disciplina assignments for the turma. When the admin saves the edit, the backend's `update_turma` receives the empty array and calls `_sync_professor_turma`, which deletes all existing rows and inserts nothing. All professor–disciplina links for that turma are silently lost.
**Fix:** Fetch the existing `professor_turma` rows for the turma (e.g., add a backend endpoint or include them in the `TurmaOut` response) and populate the `useFieldArray` with that data on edit:
```tsx
useEffect(() => {
  reset(
    initial
      ? { nome: initial.nome, ano: initial.ano, serie: initial.serie, turno: initial.turno,
          professor_turma: initial.professor_turma ?? [] }
      : defaultValues
  )
}, [initial, reset, open])
```

### CR-03: Editing a Responsavel wipes all existing `aluno_ids` links (data loss)

**File:** `frontend/src/pages/admin/ResponsaveisPage.tsx:109-117`
**Issue:** The `ResponsavelModal` resets `selectedAlunoIds` to an empty array in the `useEffect` regardless of whether the modal is in edit mode. The `initial` responsavel's linked alunos are never loaded. On save, the backend `update_responsavel` receives `aluno_ids: []` and clears all existing links. This silently orphans previously linked students.
**Fix:** Fetch the responsavel's linked alunos (e.g., include `aluno_ids` in `ResponsavelOut` or add a dedicated endpoint) and populate `selectedAlunoIds` when editing:
```tsx
useEffect(() => {
  const ids = initial?.aluno_ids ?? []
  setSelectedAlunoIds(ids)
  reset(
    initial
      ? { ..., aluno_ids: ids }
      : { ..., aluno_ids: [] }
  )
}, [initial, reset, open])
```

---

## Warnings

### WR-01: Backend does not validate foreign-key existence on Aluno create/update

**File:** `backend/src/admin/service.py:174-188, 190-198`
**Issue:** `create_aluno` and `update_aluno` accept `turma_id` and `responsavel_id` from the request body without verifying that the referenced `Turma` or `Responsavel` rows exist. If invalid IDs are sent, the database may store orphaned foreign keys (especially on SQLite with FK enforcement disabled).
**Fix:** Add existence checks before assignment:
```python
if body.turma_id is not None:
    if not db.query(Turma).filter(Turma.id == body.turma_id).first():
        raise HTTPException(status_code=400, detail="Turma não encontrada")
```

### WR-02: Deprecated `datetime.utcnow()` usage

**File:** `backend/src/admin/service.py:12, 184`
**Issue:** `datetime.utcnow()` is deprecated in Python 3.12+ and will be removed in a future version.
**Fix:** Use `datetime.now(timezone.utc)` instead:
```python
from datetime import timezone
aluno.matricula = _generate_matricula(datetime.now(timezone.utc).year, aluno.id)
```

### WR-03: Duplicate error toasts for failed API calls

**File:** `frontend/src/services/api.ts:51-54`, and all admin page mutation `onError` handlers (e.g., `frontend/src/pages/admin/AlunosPage.tsx:73-74`)
**Issue:** The Axios response interceptor already calls `toast.error(msg)` for any non-401 error. Each mutation's `onError` handler also calls `toast.error(...)`. This results in two identical toast notifications for every API error.
**Fix:** Remove the `onError` toast from individual mutations and let the interceptor handle it globally, or disable the interceptor toast for mutations:
```typescript
// In api.ts, remove or gate the toast for mutation endpoints
// Or in mutations, just log instead of toast:
onError: (err) => console.error(err)
```

### WR-04: `@tailwind` directives nested inside `@media` block (CSS parsing issue)

**File:** `frontend/src/index.css:33-37`
**Issue:** The `@tailwind base;`, `@tailwind components;`, and `@tailwind utilities;` directives are placed inside `@media (prefers-color-scheme: dark) { ... }`. Tailwind directives must be at the top level of the stylesheet; nesting them inside a media query causes PostCSS/Tailwind to skip processing them, which can break dark-mode utility generation.
**Fix:** Move the directives to the top level, before any selectors:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@media (prefers-color-scheme: dark) {
  :root { ... }
}
```

### WR-05: EntityTable shows non-functional "Desativar" button for Disciplinas and Turmas

**File:** `frontend/src/components/admin/EntityTable.tsx:108-115`
**Issue:** The deactivate button is shown when `row.ativo === true || row.ativo === undefined`. `Disciplina` and `Turma` models have no `ativo` field, so `row.ativo` is `undefined`, and the button renders. `DisciplinasPage.tsx:130` and `TurmasPage.tsx:231` pass `onDeactivate={() => {}}`, making the button clickable but non-functional. This is confusing UX.
**Fix:** Either (a) add `ativo` fields to `Disciplina` and `Turma` models and implement soft-delete endpoints, or (b) hide the button when no `onDeactivate` callback is provided by changing the condition:
```tsx
{onDeactivate && (row.ativo === true || row.ativo === undefined) && (
  <button ...>Desativar</button>
)}
```

### WR-06: `alunos_em_risco` over-counts when a Turma has no disciplines

**File:** `backend/src/admin/service.py:113-128`
**Issue:** When a turma has no linked disciplines (`disciplina_ids` is empty), every student in that turma is marked as "at risk" because `aprovado_em_todas` is forced to `False`. This produces misleading dashboard metrics.
**Fix:** Skip the turma entirely or set `aprovado_em_todas = True` (or `None`) when no disciplines exist:
```python
if not disciplina_ids:
    aprovado_em_todas = None  # or skip counting
```

### WR-07: Unsafe TypeScript type assertions (`as unknown as`) in page components

**File:** `frontend/src/pages/admin/AlunosPage.tsx:237-238`, and similar lines in `DisciplinasPage.tsx`, `ProfessoresPage.tsx`, `ResponsaveisPage.tsx`, `TurmasPage.tsx`
**Issue:** `EntityTable` passes `Record<string, unknown>` rows, and every page casts them to specific types with `as unknown as AlunoOut`. This bypasses TypeScript's type safety and could mask runtime type mismatches if the API response shape changes.
**Fix:** Make `EntityTable` generic so each page can specify the row type:
```typescript
interface EntityTableProps<T> {
  rows: T[]
  onEdit: (row: T) => void
  ...
}
```

### WR-08: `service.py` imports unused SQLAlchemy v2 constructs

**File:** `backend/src/admin/service.py:13-14`
**Issue:** `from sqlalchemy import select, func` are imported but never used; the file uses the 1.x `db.query()` style throughout. Dead imports reduce clarity.
**Fix:** Remove the unused imports.

### WR-09: Frontend modals reset form state on every `open` change

**File:** `frontend/src/pages/admin/AlunosPage.tsx:123-134`, `ResponsaveisPage.tsx:109-117`, `TurmasPage.tsx:106-112`, `ProfessoresPage.tsx:88-93`, `DisciplinasPage.tsx:66-68`
**Issue:** Each modal's `useEffect` depends on `[initial, reset, open]`. If the modal is toggled rapidly or if a parent re-renders with the same `open=true`, the form resets, potentially wiping user input.
**Fix:** Remove `open` from the dependency array and gate the reset logic:
```tsx
useEffect(() => {
  if (!open) return
  reset(...)
}, [initial, reset])  // omit open
```

### WR-10: Outdated comment in test file

**File:** `backend/tests/test_admin.py:4-6`
**Issue:** The docstring states "backend module (src/admin/) does not exist yet" and "All tests will FAIL with 404/422/ImportError until Plan 02 implements the backend." The backend module now exists, making this comment misleading.
**Fix:** Remove or update the comment to reflect current state.

### WR-11: Admin can deactivate any user account (including other admins)

**File:** `backend/src/admin/router.py:231-237`, `backend/src/admin/service.py:437-447`
**Issue:** `deactivate_usuario` only prevents self-deactivation. There is no guard against an admin deactivating another admin account. Depending on business rules, this may be intentional, but it creates a single-admin-takeover risk.
**Fix:** Consider adding a check:
```python
if usuario.tipo.value == "admin":
    raise HTTPException(status_code=400, detail="Não é permitido desativar outro administrador")
```

---

## Info

### IN-01: Hardcoded year range in Turma Zod schema

**File:** `frontend/src/pages/admin/TurmasPage.tsx:36`
**Issue:** `ano: z.number().int().min(2000).max(2099)` uses magic numbers.
**Fix:** Extract to constants:
```typescript
const MIN_ANO = 2000
const MAX_ANO = new Date().getFullYear() + 10
```

### IN-02: Redundant `python-multipart` in requirements

**File:** `backend/requirements.txt:9`
**Issue:** `fastapi[standard]` already includes `python-multipart` as a dependency. Listing it separately is redundant.
**Fix:** Remove the standalone `python-multipart` line or keep it pinned only if a specific version is required.

### IN-03: `requirements.txt` missing `email-validator` for Pydantic `EmailStr`

**File:** `backend/requirements.txt`
**Issue:** Pydantic's `EmailStr` requires the `email-validator` package. It is not listed in `requirements.txt`. While it may be pulled in transitively by `pydantic-settings` or `fastapi`, explicit declaration is safer.
**Fix:** Add `email-validator>=2.0.0` to `requirements.txt`.

---

_Reviewed: 2025-04-29_
_Reviewer: gsd-code-reviewer_
_Depth: standard_
