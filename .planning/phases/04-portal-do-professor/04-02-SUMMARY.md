---
phase: 04-portal-do-professor
plan: 02
subsystem: backend
status: complete
start_date: 2026-04-27
end_date: 2026-04-27
key_files:
  created: []
  modified:
    - backend/src/professor/service.py
    - backend/tests/test_professor.py
metrics:
  commits: 1
  tasks: 2
  tests_green: 9
---

## Summary

Implemented all professor service functions in service.py, replacing NotImplementedError stubs from Plan 01. All 9 tests in test_professor.py pass green, and full backend test suite (20 tests) shows no regressions.

## Commits

| Commit | Message | Files |
|--------|---------|-------|
| 5a546d9 | feat(04-02): implement professor service logic — chamada, notas, frequencia | 2 files |

## Deviations

- Fixed test file: `Turma` constructor used `ano_letivo` (incorrect) → changed to `ano`, `serie`, `turno` to match migration 0001 schema.
- Fixed test file: `_setup_professor_with_turma` did not set `turma_id` on Aluno, causing `test_frequencia_aggregation` to return empty list (no alunos matched `Aluno.turma_id == turma_id` filter).

## Self-Check

- [x] get_minhas_turmas returns only linked turmas with disciplina names and aluno counts
- [x] upsert_chamada uses delete-replace pattern with synchronize_session=False
- [x] upsert_notas queries Avaliacao before inserting (no duplicate rows)
- [x] Grade valor range validated server-side (0 to valor_maximo)
- [x] get_frequencia filters chamadas by professor_id (no cross-professor leaks)
- [x] All 9 tests in test_professor.py pass
- [x] Full pytest suite (20 tests) exits 0 (no regressions)

## Self-Check: PASSED
