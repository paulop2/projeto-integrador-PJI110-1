---
phase: 05-portal-do-responsavel
reviewed: 2026-04-29T00:00:00Z
depth: standard
files_reviewed: 14
files_reviewed_list:
  - backend/src/main.py
  - backend/src/responsavel/__init__.py
  - backend/src/responsavel/router.py
  - backend/src/responsavel/schemas.py
  - backend/src/responsavel/service.py
  - backend/tests/conftest.py
  - backend/tests/test_responsavel.py
  - frontend/src/App.tsx
  - frontend/src/components/responsavel/BoletimTable.tsx
  - frontend/src/components/responsavel/ChildSelector.tsx
  - frontend/src/components/responsavel/EmptyState.tsx
  - frontend/src/components/responsavel/StatusBadge.tsx
  - frontend/src/components/responsavel/SummaryCard.tsx
  - frontend/src/pages/responsavel/ResponsavelBoletimPage.tsx
findings:
  critical: 0
  warning: 2
  info: 2
  total: 4
status: issues_found
---

# Phase 05: Code Review Report

**Reviewed:** 2026-04-29
**Depth:** standard
**Files Reviewed:** 14
**Status:** issues_found

## Summary

Reviewed the full stack of the "Portal do Responsável" phase: FastAPI backend router/service/schemas, integration into main.py, frontend React components, page container, and test suite. The code correctly enforces role-based access and ownership checks (returning 403 on IDOR attempts). However, the boletim notas aggregation logic has two robustness/correctness issues that should be addressed.

## Critical Issues

_None found._

## Warnings

### WR-01: Unhandled KeyError on invalid bimestre values

**File:** `backend/src/responsavel/service.py:91-98`
**Issue:** `notas_por_bimestre` is hardcoded with keys `1, 2, 3, 4`. If an `Avaliacao` record in the database has a `bimestre` value outside this set (e.g., `0`, `5`, or `NULL` converted to an unexpected type), the assignment `notas_por_bimestre[av.bimestre] = nota.valor` raises an unhandled `KeyError`, resulting in HTTP 500 for the end user.
**Fix:**
```python
BIMESTRES = {1, 2, 3, 4}
notas_por_bimestre: dict = {b: None for b in BIMESTRES}
for av in avaliacoes:
    if av.bimestre not in BIMESTRES:
        continue  # or log a warning
    nota = db.query(Nota).filter(...).first()
    if nota:
        notas_por_bimestre[av.bimestre] = nota.valor
```

### WR-02: Silent data loss when multiple avaliacoes exist per bimestre

**File:** `backend/src/responsavel/service.py:91-98`
**Issue:** The loop over `avaliacoes` writes each nota into `notas_por_bimestre[av.bimestre]`. If multiple `Avaliacao` records exist for the same `(turma_id, disciplina_id, bimestre)`, later iterations overwrite earlier ones. The query has no deterministic ordering (`ORDER BY`), so the retained nota is arbitrary. This causes silent data loss when teachers create more than one assessment per bimestre.
**Fix:** Either (a) enforce a unique constraint at the DB level on `(turma_id, disciplina_id, bimestre)` in `Avaliacao`, or (b) accumulate and average notas per bimestre:
```python
from collections import defaultdict

notas_por_bimestre: dict = {1: None, 2: None, 3: None, 4: None}
bim_sums: defaultdict[int, list[float]] = defaultdict(list)
for av in avaliacoes:
    nota = db.query(Nota).filter(...).first()
    if nota and av.bimestre in notas_por_bimestre:
        bim_sums[av.bimestre].append(nota.valor)
for bim, vals in bim_sums.items():
    notas_por_bimestre[bim] = sum(vals) / len(vals)
```

## Info

### IN-01: Conflicting Tailwind utility classes on table

**File:** `frontend/src/components/responsavel/BoletimTable.tsx:39`
**Issue:** The table element declares both `min-w-[640px]` and `min-w-full`. In Tailwind CSS, the latter overrides the former (both set `min-width`). On narrow viewports this may prevent the intended horizontal scroll from activating, squishing table content.
**Fix:** Remove `min-w-full` and keep `min-w-[640px]` (inside the `overflow-x-auto` wrapper):
```tsx
<table className="min-w-[640px] divide-y divide-gray-200">
```

### IN-02: Inline import inside test helper

**File:** `backend/tests/test_responsavel.py:54`
**Issue:** `from src.models.professor import Professor` is imported inside the `_setup_responsavel_with_filho` function body. While functional, this reduces readability and prevents static analysis tools from detecting unused imports or circular dependencies.
**Fix:** Move the import to the top of the file alongside the other model imports.

---

_Reviewed: 2026-04-29_
_Reviewer: gsd-code-reviewer_
_Depth: standard_
