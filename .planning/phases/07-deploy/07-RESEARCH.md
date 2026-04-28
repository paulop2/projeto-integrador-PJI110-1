# Phase 7: Deploy - Research

**Researched:** 2026-04-28
**Domain:** Render Web Service (Python FastAPI) + Cloudflare Pages (React/Vite) + GitHub Actions
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** Manter SQLite sem Render Disk. Banco zerado a cada deploy — comportamento aceitável para protótipo acadêmico.
- **D-02:** Expandir seed nas migrations Alembic com dados de demonstração suficientes para avaliação: turmas, alunos, disciplinas, professores, responsáveis, notas e chamadas. Admin executa o seed automaticamente no primeiro `alembic upgrade head`.
- **D-03:** Cloudflare Pages — integração nativa com GitHub, CDN global, free tier sem expiração. Build: `npm run build` (dentro de `frontend/`), output: `dist/`.
- **D-04:** Adicionar arquivo `frontend/public/_redirects` com `/* /index.html 200` para suporte a client-side routing (React Router) no Cloudflare Pages.
- **D-05:** Usar CD nativo das plataformas: Render auto-deploy + Cloudflare Pages auto-deploy, ambos conectados diretamente ao repo GitHub via integração nativa. Push para `master` aciona os dois deploys automaticamente.
- **D-06:** Criar `.github/workflows/deploy.yml` minimal — apenas documenta o fluxo e serve como evidência para o relatório de que "deploy automático via GitHub Actions" está configurado. O workflow real é executado via webhooks nativos das plataformas.
- **D-07:** Usar `preDeployCommand` no Render: `cd backend && alembic upgrade head`. Se migrations falharem, o deploy é cancelado automaticamente sem derrubar o serviço ativo.

### Variáveis de Ambiente em Produção
Configurar no Render Dashboard:
- `DATABASE_URL` → `sqlite:///./escola.db`
- `SECRET_KEY` → string aleatória 32+ chars
- `CORS_ORIGINS` → `["https://<projeto>.pages.dev"]`
- `FRONTEND_URL` → `https://<projeto>.pages.dev`
- `ENVIRONMENT` → `production`
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `SMTP_SENDER` → Mailtrap (sandbox)

Configurar no Cloudflare Pages Dashboard:
- `VITE_API_URL` → `https://<projeto>.onrender.com`

### Claude's Discretion
- Estrutura exata do `render.yaml` (usar arquivo ou apenas configuração via dashboard)
- Conteúdo específico do seed de demonstração (nomes, quantidades de alunos/turmas)
- Nome dos serviços no Render e Cloudflare Pages (gerados durante a configuração)
- Se usar `render.yaml` ou configuração manual via dashboard (ambos funcionam)

### Deferred Ideas (OUT OF SCOPE)
None — discussão ficou dentro do escopo da fase.

</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| DEPLOY-01 | Deploy em produção (Render + GitHub Actions) | Covered by: Render render.yaml config, Cloudflare Pages build settings, GitHub Actions workflow structure, seed migration pattern, env var configuration via dashboards |

</phase_requirements>

---

## Summary

This phase creates all infrastructure artifacts needed to deploy the project. The backend FastAPI runs as a Render Web Service (free tier, Python runtime) with auto-deploy from GitHub. The frontend React/Vite app runs on Cloudflare Pages (free tier) with auto-deploy from GitHub. All code is already production-ready: `config.py` reads from env vars, `api.ts` uses `VITE_API_URL`, CORS is configurable via env. The main work is creating new files and running a seed migration.

**Critical discovered constraint:** `preDeployCommand` is **NOT available on Render's free tier**. [VERIFIED: render.com/docs/deploys] This overrides the locked decision D-07. The alternative is to chain `alembic upgrade head` in the `startCommand` via a shell compound command: `bash -c "alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port $PORT"`. This approach is widely used for free-tier Render deployments and achieves the same safety guarantee (startup fails if migrations fail).

The seed migration (D-02) is a new Alembic migration file `0002_seed_demo.py` that inserts demonstration data after the schema exists. It must be idempotent-safe (INSERT OR IGNORE) because the DB is ephemeral and rebuilt on every deploy.

**Primary recommendation:** Create 4 files + 1 migration. No existing application code changes required.

---

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Backend API serving | Render Web Service (Python) | — | FastAPI + uvicorn process |
| Database persistence | Render ephemeral filesystem | — | SQLite file, wiped on redeploy |
| Seed data | Alembic migration (runs at startup) | — | `alembic upgrade head` in startCommand |
| Frontend serving | Cloudflare Pages (CDN/Static) | — | Static assets built from Vite |
| Client-side routing | Cloudflare Pages (_redirects) | — | Falls back to index.html |
| Auto-deploy (backend) | Render native GitHub integration | — | Webhook on push to master |
| Auto-deploy (frontend) | Cloudflare Pages native GitHub | — | Webhook on push to master |
| CI documentation | GitHub Actions workflow | — | Evidence file only, no actual deploy |
| Env var injection | Render Dashboard / CF Pages Dashboard | — | Never committed to git |

---

## Standard Stack

### Core

| Library/Tool | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Render Web Service | Free tier | Host FastAPI backend | Simple Python runtime, auto-deploy, free |
| Cloudflare Pages | Free tier | Host React frontend | CDN, free, no expiry, native GitHub integration |
| uvicorn[standard] | >=0.30.0 | ASGI server | Already in requirements.txt [VERIFIED: codebase] |
| alembic | >=1.13.0 | Run migrations at startup | Already in requirements.txt [VERIFIED: codebase] |
| GitHub Actions | — | CI documentation file | Required for report evidence (D-06) |

**Version verification:** `uvicorn[standard]>=0.30.0` already present in `backend/requirements.txt` — no version changes needed. [VERIFIED: codebase read]

### Files to CREATE (all new)

| File | Purpose |
|------|---------|
| `render.yaml` | IaC config for Render Web Service — optional but useful as documentation |
| `.github/workflows/deploy.yml` | GitHub Actions workflow — documentation evidence (D-06) |
| `frontend/public/_redirects` | Cloudflare Pages SPA routing fallback (D-04) |
| `backend/alembic/versions/0002_seed_demo.py` | Alembic migration with rich demo data (D-02) |

### Files with NO CHANGES NEEDED

| File | Reason |
|------|---------|
| `backend/src/config.py` | Already reads all needed env vars from environment — zero changes |
| `backend/src/main.py` | CORS already uses `settings.CORS_ORIGINS` — zero changes |
| `backend/requirements.txt` | `uvicorn[standard]` already present — zero changes |
| `frontend/src/services/api.ts` | Already uses `import.meta.env.VITE_API_URL` — zero changes |
| `backend/alembic/env.py` | `run_migrations_online()` + batch mode already set up correctly |

---

## Architecture Patterns

### System Architecture Diagram

```
GitHub (master branch)
        |
        +---> Render (native webhook) ---> Render Web Service
        |         build: pip install -r requirements.txt
        |         start: alembic upgrade head && uvicorn src.main:app
        |         env: DATABASE_URL, SECRET_KEY, CORS_ORIGINS, FRONTEND_URL...
        |                    |
        |              SQLite escola.db (ephemeral, seeded on every boot)
        |
        +---> Cloudflare Pages (native webhook) ---> CDN Edge
                  root: frontend/
                  build: npm run build
                  output: dist/
                  env: VITE_API_URL=https://<service>.onrender.com
                           |
                     React SPA + _redirects
                           |
                    Browser --> GET /api/* --> Render URL (CORS)
```

### Recommended Project Structure (new files only)

```
/
├── render.yaml                              # NEW: Render IaC config
├── .github/
│   └── workflows/
│       └── deploy.yml                       # NEW: CI documentation
├── frontend/
│   └── public/
│       └── _redirects                       # NEW: SPA routing fallback
└── backend/
    └── alembic/
        └── versions/
            └── 0002_seed_demo.py            # NEW: Demo data migration
```

### Pattern 1: render.yaml Web Service with monorepo rootDir

**What:** Render Blueprint IaC file declaring the Python web service configuration.
**When to use:** Checked into repo root — serves as documentation and enables "Deploy to Render" button. For this project, using `rootDir: backend` so commands run relative to the `backend/` directory.

**Key constraint:** `preDeployCommand` requires a paid instance. Use `startCommand` compound instead.

```yaml
# Source: render.com/docs/blueprint-spec + render.com/docs/monorepo-support
services:
  - type: web
    name: escola-api
    runtime: python
    plan: free
    rootDir: backend
    buildCommand: pip install -r requirements.txt
    startCommand: bash -c "alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port $PORT"
    autoDeploy: true
    envVars:
      - key: DATABASE_URL
        value: sqlite:///./escola.db
      - key: ENVIRONMENT
        value: production
      - key: SECRET_KEY
        generateValue: true    # Render generates a random value on first deploy
      - key: CORS_ORIGINS
        sync: false            # Must be set manually in dashboard (URL not known until CF Pages deployed)
      - key: FRONTEND_URL
        sync: false
      - key: SMTP_HOST
        sync: false
      - key: SMTP_PORT
        sync: false
      - key: SMTP_USER
        sync: false
      - key: SMTP_PASS
        sync: false
      - key: SMTP_SENDER
        sync: false
```

**Important:** `sync: false` means "this var must be set manually in the Render dashboard; it is not auto-synced from this file." [CITED: render.com/docs/blueprint-spec]

### Pattern 2: GitHub Actions "Documentation" Workflow

**What:** A minimal workflow that runs on push to master and echoes deploy status. It does NOT perform the actual deploy (that is done by Render + CF native webhooks). Its purpose is to appear in the GitHub Actions tab as evidence for the academic report.

```yaml
# Source: github.com/actions/checkout docs
name: Deploy

on:
  push:
    branches: [master]

jobs:
  deploy:
    name: Deploy to production
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Notify deploy triggered
        run: |
          echo "Push to master detected."
          echo "Render auto-deploy: backend (FastAPI) will be deployed via Render native webhook."
          echo "Cloudflare Pages auto-deploy: frontend (React) will be deployed via CF native webhook."
          echo "Both deploys are triggered automatically without this workflow needing to act."
```

### Pattern 3: frontend/public/_redirects for SPA routing

**What:** A single-line file in the Cloudflare Pages `public/` directory (which Vite copies verbatim to `dist/`) that makes all paths serve `index.html`. This ensures React Router handles `/dashboard`, `/login`, etc. without 404s on direct URL access or page refresh.

**Context:** Cloudflare Pages documentation states: "If your project does not include a top-level 404.html file, Pages assumes that you are deploying a SPA and matches all incoming paths to root (/)" — meaning in theory `_redirects` may not be strictly required. However, the locked decision D-04 requires this file. Adding it is safe and explicit. [CITED: developers.cloudflare.com/pages/configuration/serving-pages/]

```
# Source: developers.cloudflare.com/pages/configuration/redirects
/*    /index.html   200
```

**Note:** Cloudflare Pages native SPA fallback already handles this case when no 404.html is present. The `_redirects` file makes it explicit and consistent regardless of Cloudflare's default behavior.

### Pattern 4: Alembic Demo Seed Migration (0002)

**What:** A new Alembic migration file chained after `0001`. It inserts all demo data in the correct FK dependency order.

**Idempotency:** Since the DB is ephemeral (wiped on redeploy per D-01), each deploy runs migrations from scratch. `alembic upgrade head` runs 0001 (schema) then 0002 (seed). No need for INSERT OR IGNORE — the DB is always empty before migrations run.

**Down_revision:** Must be `"0001"` — chains from the initial schema migration.

**Recommended seed data (per CONTEXT.md D-02 and specifics):**
- 2 turmas: "Turma A - 9º Ano" and "Turma B - 8º Ano"
- 3 disciplinas: Matemática, Português, Ciências
- 2 professores (with their usuario accounts, senha "Prof@123")
- 2 responsáveis (with their usuario accounts, senha "Resp@123")
- 8 alunos: 4 per turma, each linked to a responsável
- professor_turma links: each professor teaches all 3 disciplines in one turma
- 12 chamadas: each professor, 2 dates per turma/disciplina combo, with presencas for all alunos
- avaliacoes + notas: all 4 bimestres, all alunos, all disciplina+turma combos, with varied grades

**BCrypt pre-computed hashes:** Hashes must be pre-computed (like the admin seed in 0001) — Alembic migrations cannot import application code to call bcrypt at migration time. Use Python offline to generate:
```python
# Run once locally to get hash for "Prof@123"
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
print(pwd_context.hash("Prof@123"))
```

**Migration skeleton:**
```python
# Source: [ASSUMED] pattern from existing 0001_initial_schema.py in this codebase
revision = "0002"
down_revision = "0001"

def upgrade() -> None:
    # 1. Insert usuarios for professors (tipo='professor')
    # 2. Insert professores rows (linking usuario_id)
    # 3. Insert usuarios for responsaveis (tipo='responsavel')
    # 4. Insert responsaveis rows
    # 5. Insert turmas
    # 6. Insert disciplinas
    # 7. Insert alunos (linking responsavel_id and turma_id)
    # 8. Insert professor_turma links
    # 9. Insert chamadas + presencas
    # 10. Insert avaliacoes + notas
    pass

def downgrade() -> None:
    # Delete in reverse FK order
    pass
```

### Anti-Patterns to Avoid

- **Hardcoding CORS origins in code:** `main.py` already reads from `settings.CORS_ORIGINS`. Never hardcode the Cloudflare URL directly.
- **Committing secrets:** Never put `SECRET_KEY`, SMTP credentials, or `DATABASE_URL` in `render.yaml` values (use `sync: false` and set in dashboard).
- **Using `preDeployCommand` on free tier:** This will silently fail or cause deployment errors — use compound `startCommand` instead.
- **Running bcrypt at migration time:** Alembic migrations run with only SQLAlchemy available (not necessarily the full app stack). Pre-compute hashes offline.
- **`/* /index.html 200` causing infinite loop:** This is a concern on some platforms but Cloudflare Pages handles it correctly — the rule is an HTTP rewrite (status 200), not a redirect.
- **Not setting `rootDir`:** Without `rootDir: backend` in render.yaml, all commands run from repo root and must be prefixed with `cd backend &&`.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| SPA routing on Cloudflare Pages | Custom 404.html or JS redirect hack | `_redirects` file with `/* /index.html 200` | Native platform support, one line |
| Migrations at startup | Manual SQL in main.py startup | `alembic upgrade head` in startCommand compound | Already have Alembic, idempotent, chains correctly |
| Secret generation | Manual random string in render.yaml | `generateValue: true` in render.yaml envVars | Render generates a secure random value on first deploy |
| Auto-deploy | Custom GitHub Actions deploy steps | Render + Cloudflare native GitHub integration | Zero config, no secrets needed in GitHub, per D-05 |

---

## Common Pitfalls

### Pitfall 1: preDeployCommand Not Available on Free Tier
**What goes wrong:** Adding `preDeployCommand: alembic upgrade head` to render.yaml on a free service — deploy will fail or the field will be ignored.
**Why it happens:** Render restricts this feature to paid instances. [VERIFIED: render.com/docs/deploys]
**How to avoid:** Use compound startCommand: `bash -c "alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port $PORT"`. If migrations fail, uvicorn never starts and the deploy fails safely.
**Warning signs:** Render dashboard shows "preDeployCommand not available" or the feature is greyed out.

### Pitfall 2: alembic.ini sqlalchemy.url Overrides DATABASE_URL Env Var
**What goes wrong:** Alembic reads `sqlalchemy.url` from `alembic.ini` (hardcoded as `sqlite:///./escola.db`) and ignores the `DATABASE_URL` environment variable set in Render dashboard.
**Why it happens:** `alembic/env.py` uses `src.database.engine` which reads from `settings.DATABASE_URL` — this IS correct and picks up the env var. BUT `alembic.ini` has `sqlalchemy.url = sqlite:///./escola.db` as a fallback. Since env.py uses the engine from `src.database`, the `DATABASE_URL` env var IS honored. [VERIFIED: codebase read of alembic/env.py]
**How to avoid:** No change needed — the current `env.py` already uses `from src.database import Base, engine` which calls `settings.DATABASE_URL`. The `alembic.ini` value is only used in offline mode.
**Warning signs:** Alembic writes to a different path than expected.

### Pitfall 3: CORS Misconfiguration in Production
**What goes wrong:** Frontend gets CORS error on production because `CORS_ORIGINS` env var on Render does not include the Cloudflare Pages URL.
**Why it happens:** The default value is `["http://localhost:5173"]`. The env var must be set to the CF Pages URL, formatted as a JSON array string: `["https://escola-pi.pages.dev"]`.
**How to avoid:** Set `CORS_ORIGINS` in Render dashboard AFTER Cloudflare Pages URL is known. `config.py` uses `list[str]` type which pydantic-settings parses JSON strings. [VERIFIED: codebase read of config.py]
**Warning signs:** Browser console shows "No 'Access-Control-Allow-Origin' header" errors in production.

### Pitfall 4: Free Tier Cold Start Delay
**What goes wrong:** First request after 15 minutes of inactivity takes 30-60 seconds (service spinning up from sleep).
**Why it happens:** Render free tier spins down idle services after 15 minutes. [VERIFIED: render.com/docs/free]
**How to avoid:** This is accepted behavior for a prototype/demo. Brief the evaluator that first load may be slow. No mitigation needed unless demo availability is critical.
**Warning signs:** All other requests work; only the very first request after a long idle is slow.

### Pitfall 5: Working Directory for alembic upgrade head
**What goes wrong:** `alembic upgrade head` fails with "Can't find 'alembic.ini'" if run from repo root.
**Why it happens:** Alembic needs to find `alembic.ini` which is in `backend/`. With `rootDir: backend` in render.yaml, commands run from `backend/` so `alembic upgrade head` works directly.
**How to avoid:** With `rootDir: backend` set, both `alembic upgrade head` and `uvicorn src.main:app` work without any `cd` prefix.
**Warning signs:** Alembic error: "No such file or directory: alembic.ini".

### Pitfall 6: VITE_API_URL Not Set → All API Calls Fail Silently
**What goes wrong:** Frontend builds successfully but all API calls go to `undefined` (baseURL becomes "undefined/auth/login").
**Why it happens:** `import.meta.env.VITE_API_URL` is `undefined` if not set in Cloudflare Pages environment variables.
**How to avoid:** Set `VITE_API_URL` in Cloudflare Pages Dashboard > Settings > Environment variables BEFORE the first deploy (or trigger a redeploy after setting it). [VERIFIED: codebase read of api.ts]
**Warning signs:** API calls in browser network tab show requests to `undefined/...` or just `/...`.

---

## Code Examples

### render.yaml (full recommended content)

```yaml
# Source: render.com/docs/blueprint-spec + render.com/docs/monorepo-support
# Place at repository root: /render.yaml
services:
  - type: web
    name: escola-api
    runtime: python
    plan: free
    rootDir: backend
    buildCommand: pip install -r requirements.txt
    startCommand: bash -c "alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port $PORT"
    autoDeploy: true
    envVars:
      - key: DATABASE_URL
        value: sqlite:///./escola.db
      - key: ENVIRONMENT
        value: production
      - key: SECRET_KEY
        generateValue: true
      - key: CORS_ORIGINS
        sync: false
      - key: FRONTEND_URL
        sync: false
      - key: SMTP_HOST
        sync: false
      - key: SMTP_PORT
        sync: false
      - key: SMTP_USER
        sync: false
      - key: SMTP_PASS
        sync: false
      - key: SMTP_SENDER
        sync: false
```

### .github/workflows/deploy.yml (documentation only)

```yaml
# Source: docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions
# This workflow serves as documentation evidence for the academic report.
# Actual deploys are triggered natively by Render and Cloudflare Pages via GitHub webhooks.
name: Deploy

on:
  push:
    branches: [master]

jobs:
  deploy:
    name: Deploy to production
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Report deploy trigger
        run: |
          echo "=== Deploy triggered by push to master ==="
          echo "Backend (FastAPI): Render auto-deploy webhook active."
          echo "  Service: escola-api (render.com)"
          echo "  Runtime: Python, rootDir: backend/"
          echo "  Start: alembic upgrade head && uvicorn src.main:app"
          echo ""
          echo "Frontend (React/Vite): Cloudflare Pages auto-deploy webhook active."
          echo "  Project: escola-pi (pages.dev)"
          echo "  Root dir: frontend/"
          echo "  Build: npm run build, Output: dist/"
          echo ""
          echo "Both deploys execute independently via platform native webhooks."
          echo "No credentials needed here — deploys are handled by the platforms."
```

### frontend/public/_redirects

```
# Source: developers.cloudflare.com/pages/configuration/redirects
# Enables React Router client-side routing — all paths fall back to index.html
/*    /index.html   200
```

### Alembic Migration 0002 — seed structure

```python
# Source: pattern from backend/alembic/versions/0001_initial_schema.py [VERIFIED: codebase]
"""seed demo data

Revision ID: 0002
Revises: 0001
Create Date: 2026-04-28

Dados de demonstração para avaliação acadêmica.
Inclui: 2 turmas, 3 disciplinas, 2 professores, 2 responsáveis,
8 alunos, professor_turma links, chamadas, presenças, avaliações e notas.
"""

from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Pre-computed bcrypt hashes (cost=12):
    # "Prof@123"  → compute with passlib before writing migration
    # "Resp@123"  → compute with passlib before writing migration

    # Insert in FK dependency order:
    # 1. usuarios (tipo='professor') x2
    # 2. professores x2 (linking usuario_id)
    # 3. usuarios (tipo='responsavel') x2
    # 4. responsaveis x2
    # 5. turmas x2
    # 6. disciplinas x3
    # 7. alunos x8 (4 per turma, linked to responsavel and turma)
    # 8. professor_turma (each professor -> all 3 disciplines in their turma)
    # 9. chamadas x12 (2 dates × 2 turmas × 3 disciplinas)
    # 10. presencas (all alunos per chamada)
    # 11. avaliacoes (4 bimestres × 3 disciplinas × 2 turmas = 24)
    # 12. notas (all alunos × all avaliacoes)
    pass


def downgrade() -> None:
    # Delete in reverse FK dependency order
    op.execute("DELETE FROM notas")
    op.execute("DELETE FROM avaliacoes")
    op.execute("DELETE FROM presencas")
    op.execute("DELETE FROM chamadas")
    op.execute("DELETE FROM professor_turma")
    op.execute("DELETE FROM alunos")
    op.execute("DELETE FROM disciplinas")
    op.execute("DELETE FROM turmas")
    op.execute("DELETE FROM responsaveis")
    op.execute("DELETE FROM professores")
    # Delete seeded usuarios (keep admin from 0001)
    op.execute("DELETE FROM usuarios WHERE email != 'admin@escola.dev'")
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `preDeployCommand` for migrations | Compound `startCommand` on free tier | Render free tier restriction | Must chain alembic in startCommand |
| Manual Heroku Procfile | render.yaml blueprint IaC | ~2021 | Declarative, version-controlled config |
| Cloudflare Pages requires `_redirects` for SPA | Native SPA fallback (auto, if no 404.html) | CF Pages 2022+ | `_redirects` still works but may not be strictly needed |

---

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | `bash -c "..."` syntax works in Render startCommand for compound commands | Pattern 1 / render.yaml | Command might need `sh -c` or a separate shell script; fallback: create `start.sh` script |
| A2 | Cloudflare Pages with `rootDir: frontend` (set in dashboard) correctly sets build working directory | Architecture Patterns | Frontend build might fail; workaround: prefix build command with `cd frontend && npm run build` and change output to `frontend/dist` |
| A3 | Alembic migrations run correctly when working dir is `backend/` with `rootDir: backend` | Pitfall 5 | Already confirmed from env.py using relative `sys.path.insert(0, ".")` which resolves to `backend/` |
| A4 | Pre-computed bcrypt hashes in migration survive across Python/bcrypt version upgrades | Seed migration | Hash from `bcrypt>=4.0.1` (pinned) should be stable; same library used for login verification |

**Notes on A3:** The `backend/alembic/env.py` uses `sys.path.insert(0, ".")` and `from src.database import Base, engine` — when Alembic runs from `backend/` directory, `.` resolves to `backend/` and `src.database` imports correctly. [VERIFIED: codebase read]

---

## Open Questions

1. **Whether render.yaml is used vs. manual dashboard configuration**
   - What we know: Both work. `render.yaml` at repo root enables "Connect via Blueprint"; manual dashboard setup also works.
   - What's unclear: D-07 mentions `preDeployCommand` but this is unavailable on free tier — the plan must use the compound startCommand approach instead.
   - Recommendation: Create `render.yaml` for documentation value (IaC as evidence for report) but use compound startCommand instead of preDeployCommand.

2. **CORS_ORIGINS format validation**
   - What we know: `config.py` declares `CORS_ORIGINS: list[str]`. Pydantic-settings parses JSON strings from environment variables. Set as `["https://escola-pi.pages.dev"]` in Render dashboard.
   - What's unclear: Whether the Render dashboard accepts multi-line JSON or if the JSON must be on a single line.
   - Recommendation: Use single-line JSON array string in Render dashboard: `["https://projeto.pages.dev"]`.

---

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python 3 | Render build | ✓ (Render provides) | Latest 3.x | — |
| uvicorn[standard] | Render startCommand | ✓ | >=0.30.0 [VERIFIED: requirements.txt] | — |
| alembic | Render startCommand | ✓ | >=1.13.0 [VERIFIED: requirements.txt] | — |
| Node.js | Cloudflare Pages build | ✓ (CF provides) | Latest LTS | — |
| npm run build | Cloudflare Pages | ✓ | package.json "build": "tsc -b && vite build" [VERIFIED: package.json] | — |
| Render account | Backend hosting | ✗ (must create) | — | — |
| Cloudflare account | Frontend hosting | ✗ (must create) | — | — |
| GitHub repo | Auto-deploy trigger | ✓ (already exists) | — | — |

**Missing dependencies with no fallback:**
- Render account (free) — must be created at render.com before execution
- Cloudflare account (free) — must be created at cloudflare.com before execution

---

## Validation Architecture

> workflow.nyquist_validation is not set to false in config.json — treating as enabled.

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest (backend) |
| Config file | `backend/pyproject.toml` (ruff only; pytest config inline) |
| Quick run command | `cd backend && python -m pytest tests/ -x -q` |
| Full suite command | `cd backend && python -m pytest tests/ -v` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| DEPLOY-01 | Backend health endpoint returns 200 at public URL | smoke/manual | `curl https://<service>.onrender.com/health` | Manual — URL not known until deploy |
| DEPLOY-01 | Frontend loads at Cloudflare Pages URL | smoke/manual | Browser: `https://<project>.pages.dev` | Manual — URL not known until deploy |
| DEPLOY-01 | `/login` works with admin@escola.dev / Admin@123 | smoke/manual | Browser login test | Manual — requires live URL |
| DEPLOY-01 | Seed data present (turmas, alunos visible in admin panel) | smoke/manual | Browser: Admin dashboard | Manual — requires live URL |
| DEPLOY-01 | Push to master triggers deploy (GitHub Actions tab shows run) | smoke/manual | GitHub Actions tab | Manual — requires push |

### Sampling Rate

- **Per task commit:** `cd backend && python -m pytest tests/ -x -q` (regression protection)
- **Per wave merge:** `cd backend && python -m pytest tests/ -v && cd frontend && npm run build`
- **Phase gate:** Live URL smoke test before `/gsd-verify-work`

### Wave 0 Gaps

None — existing test infrastructure covers all automated checks. The deploy-specific verification is manual (requires live URLs).

---

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | yes | JWT already implemented (Phase 2) |
| V3 Session Management | yes | localStorage + 7-day expiry (Phase 2 decision) |
| V4 Access Control | yes | Role guards already implemented |
| V5 Input Validation | yes | Pydantic schemas already in place |
| V6 Cryptography | yes | bcrypt for passwords, PyJWT for tokens |

### Deploy-Specific Security Checklist

| Control | Standard | Status |
|---------|----------|--------|
| SECRET_KEY in env, not git | Render dashboard env var | Configured via dashboard |
| CORS restricted to known origin | `CORS_ORIGINS` env var | Set to CF Pages URL only |
| HTTPS | Render + CF provide TLS automatically | Free, automatic |
| No `.env` file committed | `.gitignore` should include `.env` | [ASSUMED] — verify .gitignore |
| `ENVIRONMENT=production` | Disables debug behavior if used | Set in Render dashboard |

---

## Sources

### Primary (HIGH confidence)
- `render.com/docs/deploys` — preDeployCommand availability and restrictions (paid only)
- `render.com/docs/blueprint-spec` — render.yaml field reference, envVars syntax, `sync: false`
- `render.com/docs/monorepo-support` — `rootDir` field behavior and affected commands
- `developers.cloudflare.com/pages/configuration/serving-pages/` — SPA fallback behavior
- `developers.cloudflare.com/pages/get-started/git-integration/` — root dir for monorepos, env vars
- `github.com/render-examples/fastapi/blob/main/render.yaml` — reference render.yaml for FastAPI
- Codebase (all files read): `backend/requirements.txt`, `backend/src/config.py`, `backend/src/main.py`, `backend/alembic/env.py`, `backend/alembic/versions/0001_initial_schema.py`, `frontend/package.json`, `frontend/src/services/api.ts`, `frontend/vite.config.ts`

### Secondary (MEDIUM confidence)
- Multiple community sources confirming compound startCommand as free-tier migration alternative

### Tertiary (LOW confidence)
- None

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — verified from official Render docs + codebase
- Architecture: HIGH — all components verified, critical preDeployCommand constraint confirmed
- Pitfalls: HIGH — preDeployCommand restriction confirmed via render.com/docs/deploys
- Seed migration pattern: MEDIUM — structure matches existing 0001, FK ordering assumed correct

**Research date:** 2026-04-28
**Valid until:** 2026-05-28 (Render/CF Pages APIs are stable; free tier policies rarely change)
