---
phase: 3
slug: painel-admin
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-04-27
---

# Phase 3 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest (not yet configured — Wave 0 installs) |
| **Config file** | none — Wave 0 gap |
| **Quick run command** | `cd backend && python -m pytest tests/test_admin.py -x -q` |
| **Full suite command** | `cd backend && python -m pytest tests/ -v` |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** Run `cd backend && python -m pytest tests/test_admin.py -x -q`
- **After every plan wave:** Run `cd backend && python -m pytest tests/ -v`
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** ~30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 03-W0-01 | 01 | 0 | ADMIN-01 | — | — | integration | `pytest tests/test_admin.py::test_create_aluno -x` | ❌ W0 | ⬜ pending |
| 03-W0-02 | 01 | 0 | ADMIN-01 | — | — | integration | `pytest tests/test_admin.py::test_list_alunos -x` | ❌ W0 | ⬜ pending |
| 03-W0-03 | 01 | 0 | ADMIN-01 | — | — | integration | `pytest tests/test_admin.py::test_deactivate_aluno -x` | ❌ W0 | ⬜ pending |
| 03-W0-04 | 02 | 0 | ADMIN-02 | — | — | integration | `pytest tests/test_admin.py::test_create_turma -x` | ❌ W0 | ⬜ pending |
| 03-W0-05 | 02 | 0 | ADMIN-04 | T-03-01 | Require admin JWT | integration | `pytest tests/test_admin.py::test_sync_professor_turma -x` | ❌ W0 | ⬜ pending |
| 03-W0-06 | 03 | 0 | ADMIN-05 | T-03-02 | Atomic user+profile creation | integration | `pytest tests/test_admin.py::test_create_professor -x` | ❌ W0 | ⬜ pending |
| 03-W0-07 | 03 | 0 | ADMIN-06 | — | — | integration | `pytest tests/test_admin.py::test_create_responsavel -x` | ❌ W0 | ⬜ pending |
| 03-sec-01 | all | 0 | ADMIN-* | T-03-03 | Non-admin gets 403 | integration | `pytest tests/test_admin.py::test_admin_role_required -x` | ❌ W0 | ⬜ pending |
| 03-sec-02 | all | 0 | ADMIN-* | T-03-04 | Unauthenticated gets 401 | integration | `pytest tests/test_admin.py::test_unauthenticated -x` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `backend/tests/__init__.py` — package init
- [ ] `backend/tests/conftest.py` — shared fixtures (test DB, auth headers for admin/professor)
- [ ] `backend/tests/test_admin.py` — all Phase 3 test stubs for ADMIN-01 through ADMIN-06 + security tests
- [ ] `pip install pytest httpx` — test framework + FastAPI async test client
- [ ] `backend/alembic/versions/0003_add_matricula_to_alunos.py` — adds matricula column (batch mode)
- [ ] `alembic upgrade head` — apply migration 0003
- [ ] `cd frontend && npm install -D tailwindcss@3 postcss autoprefixer` + `npx tailwindcss init -p` — Tailwind v3 install
- [ ] Add `@tailwind base/components/utilities` to `frontend/src/index.css`
- [ ] `cd frontend && npm install sonner react-hook-form zod @hookform/resolvers` — form and toast packages

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Toast notification displays and disappears after 3s | ADMIN-01..06 | Browser UI behavior; no automated DOM assertion setup | Create any entity in browser, verify toast appears and auto-dismisses |
| Deactivation confirmation dialog appears | ADMIN-01..06 | Browser modal interaction | Click Deactivate on any row, verify dialog with entity name appears |
| Sidebar nav highlights active route | Navigation | CSS active-class behavior | Click each sidebar link, verify it becomes highlighted |
| Modal closes on ESC key | Form UX | Keyboard interaction | Open any modal, press ESC, verify it closes |
| Professor→Turma rows refresh immediately after save | ADMIN-04 | TanStack Query cache invalidation | Add professor_turma rows, save, verify list updates without refresh |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
