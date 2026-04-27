---
phase: 4
slug: portal-do-professor
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-04-27
---

# Phase 4 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x |
| **Config file** | none — pytest discovers `tests/` automatically |
| **Quick run command** | `cd backend && python -m pytest tests/test_professor.py -x -q` |
| **Full suite command** | `cd backend && python -m pytest tests/ -q` |
| **Estimated runtime** | ~15 seconds |

---

## Sampling Rate

- **After every task commit:** Run `cd backend && python -m pytest tests/test_professor.py -x -q`
- **After every plan wave:** Run `cd backend && python -m pytest tests/ -q`
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 20 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 04-01-01 | 01 | 1 | PROF-01,02,03,04,05 | T-04-01 | — | unit | `cd backend && python -m pytest tests/test_professor.py -x -q` | ❌ W0 | ⬜ pending |
| 04-02-01 | 02 | 1 | PROF-01,02 | T-04-01 | Unauthenticated → 401; other role → 403; unlinked turma → 403 | unit | `cd backend && python -m pytest tests/test_professor.py::test_ownership_check tests/test_professor.py::test_access_control -x` | ❌ W0 | ⬜ pending |
| 04-02-02 | 02 | 1 | PROF-01,04 | T-04-01 | POST chamada creates presencas rows; re-POST replaces | unit | `cd backend && python -m pytest tests/test_professor.py::test_create_chamada tests/test_professor.py::test_edit_chamada_and_notas -x` | ❌ W0 | ⬜ pending |
| 04-02-03 | 02 | 1 | PROF-03,04 | T-04-01 | POST notas upserts avaliacao + nota rows | unit | `cd backend && python -m pytest tests/test_professor.py::test_upsert_notas -x` | ❌ W0 | ⬜ pending |
| 04-02-04 | 02 | 1 | PROF-05 | — | GET frequencia returns correct percentual per aluno | unit | `cd backend && python -m pytest tests/test_professor.py::test_frequencia_aggregation -x` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `backend/tests/test_professor.py` — stubs for PROF-01 through PROF-05 + access control
- [ ] `backend/src/models/chamada.py` — ORM model (required for tests to import)
- [ ] `backend/src/models/presenca.py` — ORM model (required for tests to import)
- [ ] `backend/src/models/avaliacao.py` — ORM model (required for tests to import)
- [ ] `backend/src/models/nota.py` — ORM model (required for tests to import)
- [ ] `backend/src/professor/__init__.py` — module package
- [ ] `backend/src/professor/router.py` — routes under `/professor`
- [ ] `backend/src/professor/service.py` — business logic
- [ ] `backend/src/professor/schemas.py` — Pydantic schemas

*conftest.py fixtures (`test_db`, `client`, `professor_headers`) already exist — no conftest changes needed.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Toggle Presente/Falta renders correctly | PROF-01 | Browser UI interaction | Open turma detail → Chamada tab → verify all students default to Presente; click Falta for one student |
| Grade table keyboard navigation (Tab/Enter) | PROF-03 | Browser UI interaction | Open Notas tab → Tab moves to next cell; Enter moves to next row same column |
| Toast feedback on save | PROF-01,03 | Browser UI interaction | Save chamada/notas → verify sonner toast appears |
| Warning banner on existing chamada | PROF-04 | Browser UI interaction | Open chamada for a date that has existing record → verify yellow warning banner appears |
| At-risk row highlight in Frequencia | PROF-05 | Browser UI interaction | Verify students below 75% have `bg-red-50` row and "⚠ Abaixo de 75%" badge |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 20s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
