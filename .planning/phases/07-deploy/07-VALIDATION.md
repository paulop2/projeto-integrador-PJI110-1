---
phase: 7
slug: deploy
status: draft
nyquist_compliant: false
wave_0_complete: true
created: 2026-04-28
---

# Phase 7 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest (backend) |
| **Config file** | `backend/pyproject.toml` (ruff only; pytest config inline) |
| **Quick run command** | `cd backend && python -m pytest tests/ -x -q` |
| **Full suite command** | `cd backend && python -m pytest tests/ -v` |
| **Estimated runtime** | ~10 seconds |

---

## Sampling Rate

- **After every task commit:** Run `cd backend && python -m pytest tests/ -x -q`
- **After every plan wave:** Run `cd backend && python -m pytest tests/ -v && cd frontend && npm run build`
- **Before `/gsd-verify-work`:** Full suite must be green + live URL smoke test
- **Max feedback latency:** ~10 seconds (automated) + manual smoke test after deploy

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Secure Behavior | Test Type | Automated Command | Status |
|---------|------|------|-------------|-----------------|-----------|-------------------|--------|
| 07-01-01 | 01 | 1 | DEPLOY-01 | Seed uses bcrypt hashes (not plaintext) | unit/build | `cd backend && python -m pytest tests/ -x -q` | ⬜ pending |
| 07-01-02 | 01 | 1 | DEPLOY-01 | _redirects prevents 404 on SPA routes | build | `cd frontend && npm run build` | ⬜ pending |
| 07-01-03 | 01 | 1 | DEPLOY-01 | GitHub Actions YAML valid, no secrets in workflow | build | `cd frontend && npm run build` | ⬜ pending |
| 07-02-01 | 02 | 2 | DEPLOY-01 | Backend health 200 at public URL | smoke/manual | `curl https://<service>.onrender.com/health` | ⬜ pending |
| 07-02-02 | 02 | 2 | DEPLOY-01 | Frontend loads at Cloudflare Pages URL | smoke/manual | Browser: `https://<project>.pages.dev` | ⬜ pending |
| 07-02-03 | 02 | 2 | DEPLOY-01 | Login works with admin@escola.dev / Admin@123 | smoke/manual | Browser login test | ⬜ pending |
| 07-02-04 | 02 | 2 | DEPLOY-01 | Seed data visible in admin panel | smoke/manual | Browser: Admin dashboard | ⬜ pending |
| 07-02-05 | 02 | 2 | DEPLOY-01 | Push to master triggers GitHub Actions run | smoke/manual | GitHub Actions tab | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

Existing infrastructure covers all automated phase requirements.

*No new test stubs or framework installs needed — pytest suite and TypeScript build are already operational.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Backend accessible at Render URL | DEPLOY-01 | URL not known until deploy | `curl https://<service>.onrender.com/health` → 200 |
| Frontend accessible at Cloudflare Pages URL | DEPLOY-01 | URL not known until deploy | Open `https://<project>.pages.dev` in browser |
| Login works in production | DEPLOY-01 | Requires live env vars | Login with `admin@escola.dev` / `Admin@123` |
| Seed data visible | DEPLOY-01 | Requires live DB | Check Admin panel shows turmas, alunos, notas |
| Push triggers auto-deploy | DEPLOY-01 | Requires real git push to master | Check GitHub Actions tab after push |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s (automated tasks)
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
