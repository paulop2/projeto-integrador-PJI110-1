# Roadmap: Sistema Web de Registro Escolar

## Overview

O sistema parte do zero e entrega um protótipo funcional até 24/05/2026. A ordem de execução é ditada por dependências rígidas: infraestrutura antes de qualquer feature, autenticação antes de qualquer tela protegida, entidades cadastrais antes de transações, portal do professor antes do portal do responsável. Cada fase entrega uma capacidade verificável — nenhuma fase bloqueia a próxima sem motivo. O eixo central do projeto é o core value: pais acompanhando desempenho escolar dos filhos sem precisar ir à escola.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Infraestrutura** - Esqueleto backend + frontend funcionando com banco, migrations e CORS
- [x] **Phase 2: Autenticação** - Login JWT com três perfis e rotas protegidas por papel
- [x] **Phase 3: Painel Admin** - CRUD completo de alunos, turmas, disciplinas, professores e responsáveis
- [x] **Phase 4: Portal do Professor** - Registro de chamada e lançamento de notas por turma/bimestre
- [x] **Phase 5: Portal do Responsável** - Boletim e frequência do filho com cálculos automáticos
- [x] **Phase 6: Dashboard e Polish** - Dashboard agregado, alertas LDB e estados de erro/loading
- [ ] **Phase 7: Deploy** - Sistema está rodando em produção no Render com deploy automático via GitHub Actions

## Phase Details

### Phase 1: Infraestrutura
**Goal**: Equipe tem um ambiente local funcional onde backend e frontend se comunicam, banco persiste dados com schema correto e padrões de código estão estabelecidos
**Depends on**: Nothing (first phase)
**Requirements**: INFRA-01, INFRA-02, INFRA-03, INFRA-04, INFRA-05
**Success Criteria** (what must be TRUE):
  1. Backend FastAPI responde em localhost:8000 e frontend React responde em localhost:5173 sem erros
  2. Uma requisição do frontend para o backend retorna dados (endpoint de referência funciona via CORS)
  3. Migrations Alembic criam o schema completo do zero com `alembic upgrade head` sem erros
  4. Variáveis de ambiente são lidas de `.env` (não commitado); `.env.example` documenta todas as variáveis necessárias
  5. SQLite opera em WAL mode com PRAGMA foreign_keys=ON confirmado por teste manual
**Plans**: 3 plans

Plans:
- [x] 01-01-PLAN.md — Backend skeleton: FastAPI config, database.py com WAL+FK event listener, main.py com CORS, /health endpoint
- [x] 01-02-PLAN.md — Alembic schema: env.py com batch mode, migration inicial com 11 tabelas + indexes + seed admin
- [x] 01-03-PLAN.md — Frontend scaffold: Vite React-TS, React Router 6, TanStack Query 5, api.ts axios, Makefile

### Phase 2: Autenticação
**Goal**: Qualquer usuário com credenciais válidas consegue entrar no sistema e vê apenas as telas do seu perfil
**Depends on**: Phase 1
**Requirements**: AUTH-01, AUTH-02, AUTH-03, AUTH-04, AUTH-05, AUTH-06
**Success Criteria** (what must be TRUE):
  1. Usuário faz login com email/senha e recebe JWT com claim de perfil (`tipo`)
  2. Admin, professor e responsável são redirecionados para dashboards diferentes após login
  3. Acessar uma rota protegida sem token (ou com token expirado) redireciona automaticamente para /login
  4. Token é armazenado em `localStorage` (verificável via DevTools) e persiste entre abas; prazo de 7 dias com renovação automática
  5. Usuário com senha esquecida recebe link de recuperação por e-mail
**Plans**: 6 plans

Plans:
- [x] 02-01-PLAN.md — Backend foundation: Alembic migration 0002 (reset_tokens), Usuario model, auth module (login endpoint, JWT, get_current_user, require_role)
- [x] 02-02-PLAN.md — Backend password reset: forgot-password + reset-password endpoints, smtplib email, single-use opaque tokens
- [x] 02-03-PLAN.md — Frontend auth infra: AuthContext with localStorage persistence, api.ts interceptors (Bearer token + 401 redirect + X-New-Token renewal)
- [x] 02-04-PLAN.md — Frontend auth pages: LoginPage (split-screen), ForgotPasswordPage, ResetPasswordPage
- [x] 02-05-PLAN.md — Frontend routing: ProtectedRoute, AppLayout with logout dropdown, 3 placeholder dashboards, App.tsx rewrite
- [x] 02-06-PLAN.md — Verification: smoke tests + human verification of complete auth flow

### Phase 3: Painel Admin
**Goal**: Admin consegue cadastrar e gerenciar toda a estrutura da escola — usuários, alunos, turmas, disciplinas e vínculos professor/turma
**Depends on**: Phase 2
**Requirements**: ADMIN-01, ADMIN-02, ADMIN-03, ADMIN-04, ADMIN-05, ADMIN-06
**Success Criteria** (what must be TRUE):
  1. Admin cria, edita, lista e desativa alunos pelo painel sem usar banco diretamente
  2. Admin cria turmas, disciplinas e vincula um professor a uma turma/disciplina (professor_turma)
  3. Admin cria contas de professores e responsáveis; responsável aparece vinculado ao(s) aluno(s) correto(s)
  4. Dados cadastrados pelo admin são imediatamente visíveis nas listas do painel sem refresh manual
**Plans**: 5 plans

Plans:
- [x] 03-01-PLAN.md — Foundations: migration 0003 (matricula), pytest + test stubs, Tailwind v3 install + config, npm packages (sonner/react-hook-form/zod), fix #root width
- [x] 03-02-PLAN.md — Backend admin module: ORM models (6 entities), admin schemas + service + router, main.py registration, test suite green
- [x] 03-03-PLAN.md — Frontend admin layout: AdminLayout + Sidebar, Modal + ConfirmDialog + EntityTable shared components, AdminDashboard, App.tsx routes
- [x] 03-04-PLAN.md — Frontend CRUD pages: AlunosPage, TurmasPage (professor_turma rows), DisciplinasPage, ProfessoresPage, ResponsaveisPage
- [x] 03-05-PLAN.md — Verification: full pytest suite + human verification of all 5 entity CRUD flows

### Phase 4: Portal do Professor
**Goal**: Professor registra presença e notas das suas turmas, e apenas das suas turmas
**Depends on**: Phase 3
**Requirements**: PROF-01, PROF-02, PROF-03, PROF-04, PROF-05
**Success Criteria** (what must be TRUE):
  1. Professor vê apenas as turmas às quais está vinculado (outras turmas não aparecem e não são acessíveis por URL direta)
  2. Professor registra chamada de uma turma/data e o sistema persiste presença/falta para cada aluno em uma única operação
  3. Professor lança nota por aluno, disciplina e bimestre (1º ao 4º); nota lançada aparece no histórico
  4. Professor edita chamada ou nota já registrada e a alteração é refletida imediatamente
  5. Professor visualiza resumo de frequência da turma com percentual de presença por aluno
**Plans**: 4 plans

Plans:
**Wave 1**
- [x] 04-01-PLAN.md — Foundations: 4 ORM models (Chamada/Presenca/Avaliacao/Nota), professor module scaffold (router/service/schemas), test stubs

**Wave 2** *(blocked on Wave 1 completion — 04-02 and 04-03 run in parallel)*
- [x] 04-02-PLAN.md — Backend professor API: full service logic (get_minhas_turmas, upsert_chamada, upsert_notas, get_frequencia), all tests green
- [x] 04-03-PLAN.md — Frontend professor portal: ProfessorLandingPage, ProfessorTurmaPage (3 tabs), TurmaCard/TabNav/AttendanceToggle/GradeTable/FrequencyTable, App.tsx routes

**Wave 3** *(blocked on Wave 2 completion)*
- [x] 04-04-PLAN.md — Verification: full pytest suite + TypeScript build + human browser verification of PROF-01 through PROF-05

Cross-cutting constraints:
- `_get_professor(db, usuario_id)` helper required in every service function (JWT returns usuario.id, not professor.id)
- No new Alembic migrations — schema for chamadas/presencas/avaliacoes/notas already in migration 0001
- Ownership check (`_assert_professor_owns_turma`) must be called in every endpoint

### Phase 5: Portal do Responsável
**Goal**: Responsável visualiza boletim e frequência do filho com cálculos automáticos, sem acesso a dados de outros alunos
**Depends on**: Phase 4
**Requirements**: RESP-01, RESP-02, RESP-03, RESP-04, RESP-05, RESP-06
**Success Criteria** (what must be TRUE):
  1. Responsável vê boletim do filho com notas organizadas por disciplina e bimestre (1º ao 4º)
  2. Sistema calcula e exibe média por disciplina/bimestre automaticamente (sem entrada manual)
  3. Responsável vê percentual de presença do filho por disciplina
  4. Sistema exibe alerta visual destacado quando frequência está abaixo de 75% (regra LDB)
  5. Responsável logado com filho A não consegue acessar dados do filho B de outro responsável (nem por URL direta)
  6. Sistema exibe status de aprovação/reprovação com base na média calculada
**Plans**: 3 plans

Plans:
**Wave 1**
- [x] 05-01-PLAN.md — Backend module + test scaffold: responsavel/ package (schemas, router, service), conftest fixtures (responsavel_user + responsavel_headers), test_responsavel.py (RESP-01 through RESP-06 + access control), main.py registration

**Wave 2** *(blocked on Wave 1 — 05-02 runs after 05-01)*
- [x] 05-02-PLAN.md — Frontend responsavel portal: ResponsavelBoletimPage, 5 components (ChildSelector, SummaryCard, BoletimTable, StatusBadge, EmptyState), App.tsx import swap

**Wave 3** *(blocked on Wave 2 completion)*
- [x] 05-03-PLAN.md — Verification: full pytest suite + TypeScript build + human browser verification of RESP-01 through RESP-06

Cross-cutting constraints:
- `_get_responsavel(db, usuario)` helper required in every service function
- No new Alembic migrations — all 11 tables exist from migration 0001
- Ownership check (`_assert_responsavel_owns_aluno`) must return 403 (NOT 404) — IDOR prevention
- Frequência query must NOT filter by professor_id — count ALL chamadas for (turma_id, disciplina_id)
- Approval rule server-enforced: media >= 5.0 AND freq_pct >= 75.0 (both required; LDB art. 24, VI)

### Phase 6: Dashboard e Polish
**Goal**: Admin e professor têm dashboard com visão agregada de desempenho; sistema está estável para demonstração
**Depends on**: Phase 5
**Requirements**: DASH-01
**Success Criteria** (what must be TRUE):
  1. Admin e professor veem dashboard com médias e frequência agregadas por turma
  2. Erros de API exibem mensagem amigável em português (não stack trace ou tela em branco)
  3. Requisições lentas exibem estado de loading (spinner ou skeleton) sem travar a interface
**Plans**: 4 plans

Plans:
**Wave 1** *(01 and 02 run in parallel)*
- [ ] 06-01-PLAN.md — Backend dashboard APIs: /admin/dashboard/desempenho + enriched /professor/minhas-turmas with LDB metrics
- [ ] 06-02-PLAN.md — Skeleton components + global error handling: reusable SkeletonCard/Row/Table, toast.error() in api.ts interceptor, replace all loading text

**Wave 2** *(blocked on Wave 1)*
- [ ] 06-03-PLAN.md — Frontend dashboard polish: AdminDashboard alert card + performance table, TurmaCard with metrics

**Wave 3** *(blocked on Wave 2)*
- [ ] 06-04-PLAN.md — Verification: full pytest suite + TypeScript build + human browser verification

### Phase 7: Deploy
**Goal**: Sistema está rodando em produção no Render com deploy automático via GitHub Actions
**Depends on**: Phase 6
**Requirements**: DEPLOY-01
**Success Criteria** (what must be TRUE):
  1. Backend FastAPI acessível em URL pública no Render
  2. Frontend React acessível em URL pública (Render static site ou Cloudflare Pages)
  3. Push para `master` dispara deploy automático via GitHub Actions
  4. Variáveis de ambiente (JWT secret, DATABASE_URL) configuradas via Render dashboard, não commitadas
**Plans**: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5 → 6

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Infraestrutura | 3/3 | ✓ Complete | 2026-04-26 |
| 2. Autenticação | 6/6 | ✓ Complete (verification deferred) | 2026-04-27 |
| 3. Painel Admin | 5/5 | ✓ Complete | 2026-04-27 |
| 4. Portal do Professor | 4/4 | ✓ Complete (verification deferred) | 2026-04-27 |
| 5. Portal do Responsável | 3/3 | ✓ Complete (verification deferred) | 2026-04-27 |
| 6. Dashboard e Polish | 4/4 | ✓ Complete (verification deferred) | 2026-04-28 |
| 7. Deploy | 0/? | Not started | - |
