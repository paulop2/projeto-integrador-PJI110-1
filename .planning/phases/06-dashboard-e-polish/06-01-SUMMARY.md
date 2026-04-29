# 06-01 Summary: Dashboard e Polish — Backend Aggregation Endpoints

## What Was Built

1. **Admin Dashboard Desempenho Endpoint** (`GET /admin/dashboard/desempenho`)
   - Returns per-turma aggregated metrics (`media_geral`, `pct_aprovados`, `num_alunos`)
   - Returns global `alunos_em_risco` count (students not approved in all disciplines)
   - Uses LDB calculation logic: `media >= 5.0 AND freq_pct >= 75%`
   - Frequência counts ALL chamadas for `(turma_id, disciplina_id)` without professor filter

2. **Professor Minhas-Turmas Enrichment** (`GET /professor/minhas-turmas`)
   - Each turma now includes `media_geral` (average of all student-discipline averages) and `pct_aprovados` (percentage of students approved in all disciplines)
   - Extracted reusable helper `_calcular_aprovado(db, aluno_id, turma_id, disciplina_id)` in `professor/service.py`

3. **Backend Tests**
   - `test_admin_dashboard_desempenho`: verifies aggregated metrics and `alunos_em_risco` for passing vs failing students
   - `test_professor_minhas_turmas_with_metrics`: verifies `media_geral ≈ 8.0` and `pct_aprovados ≈ 100.0`

## Key Files Changed

| File | Change |
|------|--------|
| `backend/src/admin/schemas.py` | Added `TurmaDesempenhoOut` and `DashboardDesempenho` schemas |
| `backend/src/admin/service.py` | Added `_calcular_media_freq_aprovado()` helper and `get_dashboard_desempenho()` service |
| `backend/src/admin/router.py` | Added `GET /admin/dashboard/desempenho` endpoint |
| `backend/src/professor/schemas.py` | Added optional `media_geral` and `pct_aprovados` to `TurmaOut` |
| `backend/src/professor/service.py` | Extracted `_calcular_aprovado()` helper; enriched `get_minhas_turmas()` with LDB metrics |
| `backend/tests/test_admin.py` | Added `test_admin_dashboard_desempenho` |
| `backend/tests/test_professor.py` | Added `test_professor_minhas_turmas_with_metrics` |

## Test Results

```
$ cd backend && python3 -m pytest tests/ -x -q
39 passed, 1 warning in 12.30s
```

All existing tests continue to pass. No regressions introduced.

## Deviations from Plan

None. All requirements from the plan were implemented as specified.
