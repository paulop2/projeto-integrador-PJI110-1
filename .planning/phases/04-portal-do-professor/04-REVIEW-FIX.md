---
phase: 04-portal-do-professor
fixed: 2026-04-29T03:00:00Z
findings_in_scope: 9
fixed_count: 9
skipped_count: 0
info_skipped: 2
status: all_fixed
iteration: 1
scope: critical_warning
---

# Phase 04: Portal do Professor — Code Review Fix Report

**Fixed:** 2026-04-29T03:00:00Z  
**Scope:** Critical + Warning (9 findings)  
**Status:** all_fixed  

## Summary

All 9 Critical and Warning findings from the code review have been addressed. No Info findings were in scope for this fix pass (2 Info items remain documented in the original review for future cleanup).

## Fixes Applied

### Critical Issues (3/3 fixed)

#### CR-01: `get_chamada` lacks discipline filter
**Status:** Fixed  
**Files:** `backend/src/professor/router.py`, `backend/src/professor/service.py`, `frontend/src/pages/professor/ProfessorTurmaPage.tsx`  
**Change:**
- Router now requires `disciplina_id: int = Query(...)` on `GET /professor/turmas/{turma_id}/chamada`
- Router parameter `date` changed from `str` to Pydantic `date` (also fixes WR-01)
- Service `get_chamada` accepts `target_date: date` and `disciplina_id: int`, filtering query by all four dimensions
- Frontend `useChamada` hook updated to accept `disciplinaId` and include it in query key and API call
- Query invalidation in `useSaveChamada` updated to include `disciplina_id`

#### CR-02: `effectivePresencas` loses loaded server state on user edit
**Status:** Fixed  
**File:** `frontend/src/pages/professor/ProfessorTurmaPage.tsx`  
**Change:**
- Removed the early `return presencas` guard that caused non-toggled students to lose their server-loaded state
- `effectivePresencas` now always builds a base state from `chamadaData` or `alunos`, then merges user edits (`presencas` delta) on top

#### CR-03: Missing discipline-level authorization in write endpoints
**Status:** Fixed  
**File:** `backend/src/professor/service.py`  
**Change:**
- Added `_assert_professor_owns_disciplina()` helper that validates `(professor_id, turma_id, disciplina_id)` exists in `ProfessorTurma`
- Called in `get_chamada`, `upsert_chamada`, `get_notas`, and `upsert_notas`
- Coarse `_assert_professor_owns_turma` check is retained as a first line of defense

### Warning Issues (6/6 fixed)

#### WR-01: Malformed date string causes HTTP 500 instead of 422
**Status:** Fixed (co-fixed with CR-01)  
**File:** `backend/src/professor/router.py`  
**Change:** `date` parameter changed from `str = Query(...)` to `date = Query(...)` (Pydantic `date` type). FastAPI now returns 422 for invalid date formats automatically.

#### WR-02: Write endpoints don't validate that `aluno_id`s belong to the turma
**Status:** Fixed  
**File:** `backend/src/professor/service.py`  
**Change:**
- `upsert_chamada` now queries active alunos for the turma and rejects any `aluno_id` not in the allowed set with 422
- `upsert_notas` applies the same validation for `grade.aluno_id`

#### WR-03: Frontend default date uses UTC instead of local timezone
**Status:** Fixed  
**File:** `frontend/src/pages/professor/ProfessorTurmaPage.tsx`  
**Change:** Default `selectedDate` changed from `new Date().toISOString().split('T')[0]` to `new Date().toLocaleDateString('en-CA')`, producing YYYY-MM-DD in local time.

#### WR-04: Missing TypeScript generics on `useQuery` hooks
**Status:** Fixed  
**Files:** `frontend/src/components/professor/GradeTable.tsx`, `frontend/src/pages/professor/ProfessorTurmaPage.tsx`  
**Change:**
- Added `ChamadaData` interface and generic `<ChamadaData>` to `useChamada` in `ProfessorTurmaPage.tsx`
- Added `NotasData` interface and generic `<NotasData[]>` to `useQuery` in `GradeTable.tsx`
- Removed redundant `unknown` type annotations in `GradeTable.tsx` callbacks

#### WR-05: Background refetch overwrites unsaved grade edits
**Status:** Fixed  
**File:** `frontend/src/components/professor/GradeTable.tsx`  
**Change:**
- Introduced `initializedRef` to track whether grades have been seeded from `notasData`
- `useEffect` that populates `grades` now gates on `!initializedRef.current`, preventing background refetch from overwriting user edits
- Separate effect resets `initializedRef` to `false` when `disciplinaId` changes, allowing re-initialization on discipline switch

#### WR-06: No database unique constraints on Chamada / Avaliacao composite keys
**Status:** Fixed  
**Files:** `backend/src/models/chamada.py`, `backend/src/models/avaliacao.py`  
**Change:**
- `Chamada`: added `UniqueConstraint("turma_id", "disciplina_id", "professor_id", "data")`
- `Avaliacao`: added `UniqueConstraint("turma_id", "disciplina_id", "professor_id", "bimestre")`
- **Note:** Existing deployments with duplicate rows must clean data before applying migrations.

### Info Issues (0/2 fixed — out of scope)

| Finding | Status | Reason |
|---------|--------|--------|
| IN-01: Unused Pydantic schema classes | Skipped | Info severity; `--all` not passed |
| IN-02: Inconsistent `model_config` on `NotasOut` | Skipped | Info severity; `--all` not passed |

## Test Results

- **Backend:** `pytest tests/test_professor.py` — 13 passed, 0 failed
- **Frontend:** `tsc --noEmit` — 0 errors

## Commits

| Commit | Message |
|--------|---------|
| `18e7e8e` | fix(04): CR-01 + WR-01 — add disciplina_id filter and Pydantic date validation to get_chamada |
| `bb82d14` | fix(04): CR-03 + WR-02 — add discipline-level authorization and validate aluno_ids in write endpoints |
| `638e9ca` | fix(04): WR-06 — add database unique constraints on Chamada and Avaliacao composite keys |
| `3981e23` | fix(04): CR-02 + WR-03 + WR-04 + WR-05 — fix frontend state corruption, UTC date bug, TypeScript generics, and background refetch overwrite |
| `5669f91` | test(04): update ownership check test for new required disciplina_id query param |

---

_Fixed: 2026-04-29T03:00:00Z_  
_Fixer: gsd-code-fixer_  
_Scope: critical_warning_
