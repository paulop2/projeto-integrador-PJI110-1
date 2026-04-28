# Phase 7: Deploy - Context

**Gathered:** 2026-04-28
**Status:** Ready for planning

<domain>
## Phase Boundary

Configurar infraestrutura de produção: backend FastAPI no Render (Web Service), frontend React no Cloudflare Pages, ambos com auto-deploy nativo via integração GitHub. Banco de dados permanece SQLite (efêmero — zerado a cada deploy) com seed de demonstração rico.

</domain>

<decisions>
## Implementation Decisions

### Banco de Dados em Produção
- **D-01:** Manter SQLite sem Render Disk. Banco zerado a cada deploy — comportamento aceitável para protótipo acadêmico.
- **D-02:** Expandir seed nas migrations Alembic com dados de demonstração suficientes para avaliação: turmas, alunos, disciplinas, professores, responsáveis, notas e chamadas. Admin executa o seed automaticamente no primeiro `alembic upgrade head`.

### Frontend Hosting
- **D-03:** Cloudflare Pages — integração nativa com GitHub, CDN global, free tier sem expiração. Build: `npm run build` (dentro de `frontend/`), output: `dist/`.
- **D-04:** Adicionar arquivo `public/_redirects` com `/* /index.html 200` para suporte a client-side routing (React Router) no Cloudflare Pages.

### CI/CD
- **D-05:** Usar CD nativo das plataformas: Render auto-deploy + Cloudflare Pages auto-deploy, ambos conectados diretamente ao repo GitHub via integração nativa. Push para `master` aciona os dois deploys automaticamente.
- **D-06:** Criar `.github/workflows/deploy.yml` minimal — apenas documenta o fluxo e serve como evidência para o relatório de que "deploy automático via GitHub Actions" está configurado. O workflow real é executado via webhooks nativos das plataformas.

### Migrations em Produção
- **D-07:** Usar `preDeployCommand` no Render: `cd backend && alembic upgrade head`. Se migrations falharem, o deploy é cancelado automaticamente sem derrubar o serviço ativo.

### Variáveis de Ambiente em Produção
Configurar no Render Dashboard (nunca commitadas):
- `DATABASE_URL` → `sqlite:///./escola.db`
- `SECRET_KEY` → string aleatória 32+ chars
- `CORS_ORIGINS` → `["https://<projeto>.pages.dev"]` (URL do Cloudflare Pages)
- `FRONTEND_URL` → `https://<projeto>.pages.dev`
- `ENVIRONMENT` → `production`
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `SMTP_SENDER` → Mailtrap (sandbox — demo apenas)

Configurar no Cloudflare Pages Dashboard:
- `VITE_API_URL` → `https://<projeto>.onrender.com`

### Claude's Discretion
- Estrutura exata do `render.yaml` (usar arquivo ou apenas configuração via dashboard)
- Conteúdo específico do seed de demonstração (nomes, quantidades de alunos/turmas)
- Nome dos serviços no Render e Cloudflare Pages (gerados durante a configuração)
- Se usar `render.yaml` ou configuração manual via dashboard (ambos funcionam)

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Configuração do Backend
- `backend/src/config.py` — Settings pydantic-settings; todas as env vars lidas aqui; CORS_ORIGINS é lista JSON
- `backend/.env.example` — Lista completa de variáveis a configurar no Render
- `backend/requirements.txt` — Dependências atuais; verificar se `uvicorn[standard]` está presente (necessário para Render)
- `backend/alembic.ini` — Configuração do Alembic; `script_location` e `sqlalchemy.url`
- `backend/alembic/env.py` — env.py com batch mode (Phase 1); base para preDeployCommand
- `backend/src/main.py` — CORS config via `settings.CORS_ORIGINS`; CORS deve aceitar URL do Cloudflare Pages

### Seed de Demonstração
- `backend/alembic/versions/` — Migrations existentes; novo seed vai em migration adicional ou extensão da 0001

### Frontend Build
- `frontend/vite.config.ts` — Build config; output padrão em `dist/`
- `frontend/package.json` — Scripts: `build` deve ser `tsc -b && vite build`
- `frontend/src/services/api.ts` — Usa `import.meta.env.VITE_API_URL` como baseURL

### Referência de deploy
- `.planning/ROADMAP.md` §Phase 7 — Goal e Success Criteria do deploy
- `.planning/PROJECT.md` §Constraints — Stack fixada: FastAPI + React + SQLite

No external ADRs — all deploy requirements captured above.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `backend/src/config.py`: pydantic-settings já lê de env vars — zero mudança de código para produção, só precisa das env vars configuradas no Render
- `backend/alembic/` (batch mode): migrations já têm `render_as_batch=True` — compatível com SQLite em qualquer ambiente
- `frontend/src/services/api.ts`: já usa `import.meta.env.VITE_API_URL` — só precisa configurar a env var no Cloudflare Pages

### Established Patterns
- CORS configurado via `CORS_ORIGINS` em `settings` — nunca hardcoded; basta mudar env var no Render para adicionar a URL do Cloudflare Pages
- `ENVIRONMENT=production` permite habilitar/desabilitar comportamentos (ex: docs Swagger) sem mudança de código

### Integration Points
- `preDeployCommand` no Render → `cd backend && alembic upgrade head` (seed já está nas migrations)
- Cloudflare Pages: detecta `npm run build` automaticamente no diretório `frontend/`
- `_redirects` em `frontend/public/` para garantir que React Router funciona no Cloudflare Pages (sem 404 em refresh)

</code_context>

<specifics>
## Specific Ideas

- Seed de demonstração deve ter dados suficientes para mostrar o sistema funcionando: pelo menos 2 turmas, 3 disciplinas, 5-10 alunos por turma, notas e chamadas lançadas para todos os bimestres — para o avaliador ver o dashboard com dados reais
- GitHub Actions workflow é principalmente para documentação/evidência do relatório — as plataformas fazem o deploy real

</specifics>

<deferred>
## Deferred Ideas

None — discussão ficou dentro do escopo da fase.

</deferred>

---

*Phase: 07-deploy*
*Context gathered: 2026-04-28*
