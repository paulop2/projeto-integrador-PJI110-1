---
phase: 06-dashboard-e-polish
fixed_at: 2026-04-29T12:00:00Z
review_path: /Users/pvs/projetos/projeto-integrador-PJI110-1/.planning/phases/06-dashboard-e-polish/06-REVIEW.md
iteration: 1
findings_in_scope: 10
fixed: 6
skipped: 4
status: partial
---

# Phase 06: Code Review Fix Report

**Fixed at:** 2026-04-29T12:00:00Z
**Source review:** /Users/pvs/projetos/projeto-integrador-PJI110-1/.planning/phases/06-dashboard-e-polish/06-REVIEW.md
**Iteration:** 1

**Summary:**
- Findings in scope: 10
- Fixed: 6
- Skipped: 4

## Fixed Issues

### CR-02: `get_chamada` returns `None` for non-optional `id` field

**Files modified:** `backend/src/professor/schemas.py`
**Commit:** 6839a09
**Applied fix:** Changed `ChamadaOut.id` from `int` to `Optional[int] = None` so the schema accepts the service's `{"id": None, ...}` response when no attendance record exists.

### WR-01: `create_responsavel` silently ignores invalid `aluno_ids`

**Files modified:** `backend/src/admin/service.py`
**Commit:** 4770ebe
**Applied fix:** Replaced the silent `if aluno:` skip with an explicit `HTTPException(status_code=400, detail=f"Aluno {aluno_id} não encontrado")` when the aluno does not exist.

### WR-02: `update_responsavel` silently ignores invalid `aluno_ids`

**Files modified:** `backend/src/admin/service.py`
**Commit:** 78c0f78
**Applied fix:** Same pattern as WR-01 — raises `HTTPException(400)` when an `aluno_id` in the update payload does not exist.

### WR-06: Password creation schemas lack minimum length validation

**Files modified:** `backend/src/admin/schemas.py`
**Commit:** e24e0b2
**Applied fix:** Added `Field(..., min_length=8)` to `ProfessorCreate.senha` and `ResponsavelCreate.senha`, and added `Field` to the pydantic imports.

### WR-07: `_sync_professor_turma` does not validate foreign-key targets

**Files modified:** `backend/src/admin/service.py`
**Commit:** f9f0396
**Applied fix:** Added existence checks for `Professor` and `Disciplina` before inserting `ProfessorTurma` rows, raising `HTTPException(400)` with a descriptive message if either is missing.

### WR-08: AdminDashboard hides desempenho errors silently

**Files modified:** `frontend/src/pages/admin/AdminDashboard.tsx`
**Commit:** d710d25
**Applied fix:** Destructured `isError: desempenhoError` from `useAdminDesempenho()` and rendered a red error banner when `desempenhoError` is true, matching the existing dashboard error pattern.

## Skipped Issues

### CR-01: Raw `Usuario` object returned without response model leaks password hash

**File:** `backend/src/admin/router.py:231-237`
**Reason:** Code context differs from review — the endpoint already declares `response_model=schemas.UsuarioOut` and the `UsuarioOut` schema only exposes `id`, `email`, `tipo`, and `ativo` (no `senha_hash`). No fix was required.

### WR-03: `get_chamada` crashes on malformed date strings

**File:** `backend/src/professor/service.py:153`
**Reason:** Code context differs from review — the current implementation no longer calls `datetime.strptime`. The router uses FastAPI's native `date` query-parameter parsing (`date: date = Query(...)`), which returns a 422 for malformed strings automatically. No fix was required.

### WR-04: `upsert_chamada` allows presencas for students outside the turma

**File:** `backend/src/professor/service.py:189-190`
**Reason:** Already fixed in current codebase — the function queries active alunos for the turma into `allowed_aluno_ids` and raises `HTTPException(422)` for any `aluno_id` not in the set.

### WR-05: `upsert_notas` allows grades for students outside the turma

**File:** `backend/src/professor/service.py:221-252`
**Reason:** Already fixed in current codebase — the function queries active alunos for the turma into `allowed_aluno_ids` and raises `HTTPException(422)` for any `grade.aluno_id` not in the set.

---

_Fixed: 2026-04-29T12:00:00Z_
_Fixer: the agent (gsd-code-fixer)_
_Iteration: 1_
