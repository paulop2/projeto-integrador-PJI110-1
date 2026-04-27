# Requirements: Sistema Web de Registro Escolar

**Defined:** 2026-04-26
**Core Value:** Pais acompanham o desempenho escolar dos filhos — notas e presença — sem precisar ir até a escola.

## v1 Requirements

### Infrastructure

- [ ] **INFRA-01**: Projeto backend FastAPI configurado com SQLAlchemy 2.0, Alembic e SQLite (WAL mode + foreign_keys pragma)
- [ ] **INFRA-02**: Projeto frontend React 18 + Vite + TypeScript configurado com React Router 6 e TanStack Query 5
- [ ] **INFRA-03**: CORS configurado corretamente entre backend (port 8000) e frontend (port 5173)
- [ ] **INFRA-04**: Variáveis de ambiente via `.env` (não commitado) com `.env.example` documentado
- [ ] **INFRA-05**: Pipeline de migração do banco via Alembic com schema completo (batch mode para SQLite)

### Authentication

- [ ] **AUTH-01**: Usuário pode fazer login com email e senha, recebendo JWT com claim de perfil (`tipo`)
- [ ] **AUTH-02**: Sistema distingue três perfis: `admin`, `professor`, `responsavel` — cada um vê telas diferentes
- [ ] **AUTH-03**: Rotas do frontend protegidas por perfil (guard redirect para login se não autenticado)
- [ ] **AUTH-04**: JWT armazenado em `sessionStorage` (não `localStorage`) para mitigar risco XSS
- [ ] **AUTH-05**: Token expirado redireciona para login automaticamente
- [ ] **AUTH-06**: Usuário pode recuperar senha via link enviado por e-mail

### Admin

- [ ] **ADMIN-01**: Admin pode cadastrar, editar, listar e desativar alunos
- [ ] **ADMIN-02**: Admin pode cadastrar, editar e listar turmas
- [ ] **ADMIN-03**: Admin pode cadastrar, editar e listar disciplinas
- [ ] **ADMIN-04**: Admin pode vincular professor a uma turma/disciplina (`professor_turma`)
- [ ] **ADMIN-05**: Admin pode criar contas de professores (perfil `professor`)
- [ ] **ADMIN-06**: Admin pode criar contas de responsáveis (perfil `responsavel`) e vinculá-los a aluno(s)

### Professor

- [ ] **PROF-01**: Professor pode registrar chamada (lista de presença/falta) por turma e data
- [ ] **PROF-02**: Professor só vê turmas às quais está vinculado (ownership check)
- [ ] **PROF-03**: Professor pode lançar notas por aluno, disciplina e bimestre (1º ao 4º)
- [ ] **PROF-04**: Professor pode editar notas e presenças já registradas
- [ ] **PROF-05**: Professor pode visualizar resumo de frequência por turma (% de presença por aluno)

### Responsável (Pai/Mãe)

- [ ] **RESP-01**: Responsável vê boletim do filho: notas por disciplina organizadas por bimestre
- [ ] **RESP-02**: Sistema calcula e exibe média por disciplina/bimestre automaticamente
- [ ] **RESP-03**: Responsável vê frequência do filho: percentual de presença por disciplina
- [ ] **RESP-04**: Sistema exibe alerta visual quando frequência está abaixo de 75% (regra LDB art. 24, VI)
- [ ] **RESP-05**: Sistema exibe status de aprovação/reprovação com base na média calculada
- [ ] **RESP-06**: Responsável só vê dados dos seus próprios filhos (ownership check)

### Dashboard

- [ ] **DASH-01**: Admin/Professor pode ver dashboard com resumo de desempenho por turma (médias e frequência agregadas)

## v2 Requirements

### Notificações

- **NOTF-01**: Notificação automática por e-mail quando nota é lançada
- **NOTF-02**: Alerta por e-mail quando frequência cai abaixo de 75%
- **NOTF-03**: Responsável configura preferências de notificação

### Mobile

- **MOB-01**: Interface responsiva para mobile (PWA)
- **MOB-02**: App nativo (React Native) — v3+

### Relatórios Avançados

- **REL-01**: Exportação de boletim em PDF
- **REL-02**: Histórico de desempenho entre bimestres (gráfico de evolução)
- **REL-03**: Comparativo de desempenho por turma para diretoria

## Out of Scope

| Feature | Reason |
|---------|--------|
| Chat / mensagens em tempo real | Alta complexidade, não é o foco do v1 |
| Multi-escola / multi-tenant | Projeto é para uma escola específica |
| Login do aluno | Apenas admin, professor e responsável têm perfis |
| Pagamentos / mensalidades | Fora do escopo educacional do projeto |
| App mobile nativo | Web-first; mobile é v3+ |
| Integração com sistemas externos (SED-SP, etc.) | Complexidade de integração fora do prazo |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| INFRA-01 | Phase 1 | Pending |
| INFRA-02 | Phase 1 | Pending |
| INFRA-03 | Phase 1 | Pending |
| INFRA-04 | Phase 1 | Pending |
| INFRA-05 | Phase 1 | Pending |
| AUTH-01 | Phase 2 | Pending |
| AUTH-02 | Phase 2 | Pending |
| AUTH-03 | Phase 2 | Pending |
| AUTH-04 | Phase 2 | Pending |
| AUTH-05 | Phase 2 | Pending |
| AUTH-06 | Phase 2 | Pending |
| ADMIN-01 | Phase 3 | Pending |
| ADMIN-02 | Phase 3 | Pending |
| ADMIN-03 | Phase 3 | Pending |
| ADMIN-04 | Phase 3 | Pending |
| ADMIN-05 | Phase 3 | Pending |
| ADMIN-06 | Phase 3 | Pending |
| PROF-01 | Phase 4 | Pending |
| PROF-02 | Phase 4 | Pending |
| PROF-03 | Phase 4 | Pending |
| PROF-04 | Phase 4 | Pending |
| PROF-05 | Phase 4 | Pending |
| RESP-01 | Phase 5 | Pending |
| RESP-02 | Phase 5 | Pending |
| RESP-03 | Phase 5 | Pending |
| RESP-04 | Phase 5 | Pending |
| RESP-05 | Phase 5 | Pending |
| RESP-06 | Phase 5 | Pending |
| DASH-01 | Phase 6 | Pending |

**Coverage:**
- v1 requirements: 29 total
- Mapped to phases: 29
- Unmapped: 0 ✓

---
*Requirements defined: 2026-04-26*
*Last updated: 2026-04-26 after initial definition*
