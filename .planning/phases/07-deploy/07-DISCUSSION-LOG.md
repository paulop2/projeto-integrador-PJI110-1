# Phase 7: Deploy - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-28
**Phase:** 07-deploy
**Areas discussed:** Banco em produção, Frontend hosting, GitHub Actions workflow, Migrations em produção

---

## Banco em Produção

| Option | Description | Selected |
|--------|-------------|----------|
| SQLite + Render Disk | Volume persistente no Render (~$0.25/GB/mês). Sem mudança de código. | |
| SQLite sem persistência | Dados zerados a cada deploy. OK para protótipo acadêmico com seed manual. | |
| Migrar para PostgreSQL | Neon ou Supabase free tier. Requer psycopg2, ajustes no Alembic. | |

**User's choice:** Freeform — "continuar com SQLite por enquanto, com seed inicial grande com todos os dados pra testes"
**Notes:** Projeto é protótipo acadêmico; avaliador verá o sistema via seed. Persistência não é requisito crítico.

---

## Frontend Hosting

| Option | Description | Selected |
|--------|-------------|----------|
| Render Static Site | Mesma plataforma do backend. Config simples, auto-deploy junto. | |
| Cloudflare Pages | CDN global gratuita, build mais rápido, free tier sem expiração. | ✓ |

**User's choice:** Cloudflare Pages
**Notes:** Nenhuma. Escolha direta.

---

## GitHub Actions Workflow

| Option | Description | Selected |
|--------|-------------|----------|
| Só deploy | Push no master aciona deploy via CD nativo das plataformas. | ✓ |
| Tests + deploy | Roda pytest antes de subir. Se falhar, cancela deploy. | |
| Lint + build + tests + deploy | Pipeline completo. | |

**User's choice:** Só deploy (Recomendado)
**Notes:** CD nativo do Render + Cloudflare Pages via integração GitHub. Workflow no GitHub Actions serve como evidência para relatório.

---

## Migrations em Produção

| Option | Description | Selected |
|--------|-------------|----------|
| preDeployCommand | Render roda alembic upgrade head antes de trocar instância. Cancela deploy se falhar. | ✓ |
| Startup command | alembic upgrade head && uvicorn ... Mais simples, mas derruba serviço em caso de erro. | |

**User's choice:** preDeployCommand (Recomendado)
**Notes:** Nenhuma. Escolha direta pela opção mais robusta.

---

## Claude's Discretion

- Estrutura exata do `render.yaml` (usar arquivo ou dashboard)
- Conteúdo específico do seed de demonstração (nomes, quantidades)
- Nome dos serviços no Render e Cloudflare Pages
- Estrutura do workflow `.github/workflows/deploy.yml`

## Deferred Ideas

None — discussão ficou dentro do escopo da fase.
