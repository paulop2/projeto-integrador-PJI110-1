---
phase: 5
slug: portal-do-responsavel
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-04-27
---

# Phase 5 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x |
| **Config file** | none — pytest discovers `tests/` automatically |
| **Quick run command** | `cd backend && python -m pytest tests/test_responsavel.py -x -q` |
| **Full suite command** | `cd backend && python -m pytest tests/ -q` |
| **Estimated runtime** | ~15 seconds |

---

## Sampling Rate

- **After every task commit:** Run `cd backend && python -m pytest tests/test_responsavel.py -x -q`
- **After every plan wave:** Run `cd backend && python -m pytest tests/ -q`
- **Before `/gsd-verify-work`:** Full suite must be green + TypeScript build clean
- **Max feedback latency:** 20 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 05-01-01 | 01 | 1 | RESP-01..06 | T-05-01 | — | unit | `cd backend && python -m pytest tests/test_responsavel.py -x -q` | ❌ W0 | ⬜ pending |
| 05-02-01 | 02 | 2 | RESP-06 | T-05-01 | Unauthenticated → 401; other role → 403; unlinked aluno → 403 | unit | `cd backend && python -m pytest tests/test_responsavel.py::test_ownership_idor_blocked tests/test_responsavel.py::test_access_control -x` | ❌ W0 | ⬜ pending |
| 05-02-02 | 02 | 2 | RESP-01,02 | — | GET boletim returns notas by disciplina/bimestre; média calculated correctly | unit | `cd backend && python -m pytest tests/test_responsavel.py::test_boletim_notas tests/test_responsavel.py::test_media_calculation -x` | ❌ W0 | ⬜ pending |
| 05-02-03 | 02 | 2 | RESP-03,04 | — | GET boletim returns frequência per disciplina; flag when < 75% | unit | `cd backend && python -m pytest tests/test_responsavel.py::test_frequencia_per_disciplina tests/test_responsavel.py::test_freq_below_threshold -x` | ❌ W0 | ⬜ pending |
| 05-02-04 | 02 | 2 | RESP-05 | — | aprovado=False when média < 5.0 OR freq < 75% | unit | `cd backend && python -m pytest tests/test_responsavel.py::test_approval_rule -x` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `backend/tests/test_responsavel.py` — stubs for RESP-01 through RESP-06 + access control
- [ ] `backend/src/responsavel/__init__.py` — module package
- [ ] `backend/src/responsavel/router.py` — routes under `/responsavel`
- [ ] `backend/src/responsavel/service.py` — business logic
- [ ] `backend/src/responsavel/schemas.py` — Pydantic v2 schemas

**conftest.py gap:** `responsavel_headers` fixture does NOT exist. Wave 0 must add `responsavel_user` + `responsavel_headers` fixtures mirroring `professor_headers`. All ORM models needed (responsavel, aluno, turma, avaliacao, nota, chamada, presenca) already exist.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| ChildSelector renders only when > 1 filho | RESP-01 | Browser UI — conditional render | Login as responsavel with 2 alunos; verify dropdown appears; with 1 aluno verify it's hidden |
| Switching filho in ChildSelector fetches correct data | RESP-01 | Browser UI — state update | Switch between filhos; verify table reloads with different notas |
| At-risk row highlight (bg-red-50) | RESP-04 | Browser UI — CSS class check | Verify disciplina with freq < 75% shows red row background |
| Summary card "em risco" state | RESP-04 | Browser UI — conditional render | Verify yellow warning card appears when any disciplina is at risk |
| Summary card "Aprovado em todas" state | RESP-05 | Browser UI — conditional render | Verify green card appears when all disciplinas pass both thresholds |
| EmptyState — no filhos | RESP-06 | Browser UI — edge case | Login as responsavel with no alunos linked → verify "Nenhum aluno vinculado" message |
| Frequência format "82% (15/18)" | RESP-03 | Browser UI — display format | Verify frequency column shows both percentage and absolute numbers |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 20s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
