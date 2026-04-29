---
phase: 03-painel-admin
reviewed: 2025-04-29T00:00:00Z
fixed_at: 2025-04-29
depth: standard
fix_scope: critical_warning
findings_in_scope: 14
fixed: 14
skipped: 0
info_skipped: 3
status: all_fixed
iteration: 1
---

# Phase 03: Code Review Fix Report

**Fix Scope:** critical + warning (default)  
**Findings in Scope:** 14  
**Fixed:** 14  
**Skipped:** 0  
**Status:** all_fixed  

---

## Critical Issues Fixed

### CR-01: `deactivate_usuario` endpoint exposes `senha_hash`
- **Status:** Fixed
- **Files changed:** `backend/src/admin/schemas.py`, `backend/src/admin/router.py`
- **Fix:** Added `UsuarioOut` schema excluding `senha_hash` and applied `response_model=schemas.UsuarioOut` to the `deactivate_usuario` endpoint.

### CR-02: Editing a Turma wipes all existing `professor_turma` assignments
- **Status:** Fixed
- **Files changed:** `backend/src/admin/schemas.py`, `backend/src/admin/service.py`, `frontend/src/pages/admin/TurmasPage.tsx`
- **Fix:** Added `professor_turma` field to `TurmaOut` schema; populated it in `list_turmas` service; updated frontend `TurmaOut` interface and modal `useEffect` to pre-populate existing professor/disciplina assignments on edit.

### CR-03: Editing a Responsavel wipes all existing `aluno_ids` links
- **Status:** Fixed
- **Files changed:** `backend/src/admin/schemas.py`, `backend/src/admin/service.py`, `frontend/src/pages/admin/ResponsaveisPage.tsx`
- **Fix:** Added `aluno_ids` field to `ResponsavelOut` schema; populated it in `list_responsaveis` service; updated frontend `ResponsavelOut` interface and modal `useEffect` to pre-populate linked alunos on edit.

---

## Warnings Fixed

### WR-01: Backend does not validate foreign-key existence on Aluno create/update
- **Status:** Fixed
- **Files changed:** `backend/src/admin/service.py`
- **Fix:** Added existence checks for `turma_id` and `responsavel_id` in both `create_aluno` and `update_aluno`, raising `HTTPException(400)` if not found.

### WR-02: Deprecated `datetime.utcnow()` usage
- **Status:** Fixed
- **Files changed:** `backend/src/admin/service.py`
- **Fix:** Replaced `datetime.utcnow()` with `datetime.now(timezone.utc)` and updated import.

### WR-03: Duplicate error toasts for failed API calls
- **Status:** Fixed
- **Files changed:** `frontend/src/pages/admin/AlunosPage.tsx`, `frontend/src/pages/admin/DisciplinasPage.tsx`, `frontend/src/pages/admin/ProfessoresPage.tsx`, `frontend/src/pages/admin/ResponsaveisPage.tsx`, `frontend/src/pages/admin/TurmasPage.tsx`
- **Fix:** Removed `onError` toast handlers from all mutations; the global Axios interceptor already handles error toasts for non-401 responses.

### WR-04: `@tailwind` directives nested inside `@media` block
- **Status:** Fixed
- **Files changed:** `frontend/src/index.css`
- **Fix:** Moved `@tailwind base;`, `@tailwind components;`, `@tailwind utilities;` to the top level of the stylesheet, before any selectors.

### WR-05: EntityTable shows non-functional "Desativar" button for Disciplinas and Turmas
- **Status:** Fixed
- **Files changed:** `frontend/src/components/admin/EntityTable.tsx`, `frontend/src/pages/admin/DisciplinasPage.tsx`
- **Fix:** Made `onDeactivate` prop optional in `EntityTable`; the deactivate button now only renders when `onDeactivate` is provided. Removed the empty `onDeactivate={() => {}}` from `DisciplinasPage`.

### WR-06: `alunos_em_risco` over-counts when a Turma has no disciplines
- **Status:** Fixed
- **Files changed:** `backend/src/admin/service.py`
- **Fix:** Changed logic so that when a turma has no linked disciplines, students are not counted as "at risk".

### WR-07: Unsafe TypeScript type assertions (`as unknown as`) in page components
- **Status:** Fixed
- **Files changed:** `frontend/src/components/admin/EntityTable.tsx`, `frontend/src/pages/admin/AlunosPage.tsx`, `frontend/src/pages/admin/DisciplinasPage.tsx`, `frontend/src/pages/admin/ProfessoresPage.tsx`, `frontend/src/pages/admin/ResponsaveisPage.tsx`, `frontend/src/pages/admin/TurmasPage.tsx`
- **Fix:** Made `EntityTable` generic with type parameter `<T>`; each page now specifies its row type (e.g., `EntityTable<AlunoOut>`) and removed unsafe `as unknown as` casts from `onEdit`/`onDeactivate` handlers.

### WR-08: `service.py` imports unused SQLAlchemy v2 constructs
- **Status:** Fixed
- **Files changed:** `backend/src/admin/service.py`
- **Fix:** Removed unused `select` and `func` imports from SQLAlchemy.

### WR-09: Frontend modals reset form state on every `open` change
- **Status:** Fixed
- **Files changed:** `frontend/src/pages/admin/AlunosPage.tsx`, `frontend/src/pages/admin/DisciplinasPage.tsx`, `frontend/src/pages/admin/ProfessoresPage.tsx`, `frontend/src/pages/admin/ResponsaveisPage.tsx`, `frontend/src/pages/admin/TurmasPage.tsx`
- **Fix:** Removed `open` from `useEffect` dependency arrays in all modal components; added an early-return guard (`if (!open) return`) to prevent resetting closed modals.

### WR-10: Outdated comment in test file
- **Status:** Fixed
- **Files changed:** `backend/tests/test_admin.py`
- **Fix:** Removed the misleading docstring stating the backend module does not exist yet.

### WR-11: Admin can deactivate any user account (including other admins)
- **Status:** Fixed
- **Files changed:** `backend/src/admin/service.py`
- **Fix:** Added a guard in `deactivate_usuario` to reject deactivation of accounts with `tipo == "admin"`.

---

## Info Findings (Skipped — fix scope = critical_warning)

- **IN-01:** Hardcoded year range in Turma Zod schema
- **IN-02:** Redundant `python-multipart` in requirements
- **IN-03:** `requirements.txt` missing `email-validator`

---

_Fix report generated: 2025-04-29_  
_Fixer: gsd-code-fixer_  
_Iteration: 1/1_  
