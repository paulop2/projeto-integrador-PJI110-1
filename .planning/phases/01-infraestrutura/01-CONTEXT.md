# Phase 1: Infraestrutura - Context

**Gathered:** 2026-04-26
**Status:** Ready for planning

<domain>
## Phase Boundary

Estabelecer ambiente local funcional: backend FastAPI (localhost:8000) e frontend React (localhost:5173) se comunicam via CORS, banco SQLite persiste dados com schema completo via Alembic, e padrões de código estão configurados. Nenhuma feature de negócio nesta phase — só infraestrutura.

</domain>

<decisions>
## Implementation Decisions

### Schema do banco
- Schema completo criado na Phase 1 via Alembic: todas as entidades (users, alunos, turmas, disciplinas, notas, chamadas) e todas as tabelas de vínculo (professor_turma, responsavel_aluno) + indexes
- Zero migrations adicionais nas phases seguintes — phases 2-6 focam só em código
- SQLite em WAL mode com `PRAGMA foreign_keys=ON` configurado na inicialização

### Seed data
- Migration da Phase 1 insere um usuário admin padrão com credenciais de desenvolvimento (ex: admin@escola.dev / admin123)
- Elimina setup manual para validar as phases seguintes

### Gerenciamento de dependências Python
- venv + requirements.txt (sem Poetry)
- `python -m venv venv && pip install -r requirements.txt` para setup local

### Claude's Discretion
- Estrutura de pastas: monorepo com `/backend` e `/frontend` na raiz
- Workflow de desenvolvimento: dois terminais separados ou Makefile com targets `make backend` / `make frontend` / `make dev`
- Python tooling: Black + Ruff
- Frontend tooling: ESLint + Prettier, npm como package manager
- Credenciais exatas do admin seed (seguir padrão seguro de dev)

</decisions>

<specifics>
## Specific Ideas

- SQLite WAL mode e foreign_keys já são requisito explícito do success criteria da phase
- `.env.example` deve documentar todas as variáveis necessárias (JWT secret, DB path, CORS origins)

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 01-infraestrutura*
*Context gathered: 2026-04-26*
