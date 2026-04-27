# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-04-26)

**Core value:** Pais acompanham o desempenho escolar dos filhos — notas e presença — sem precisar ir até a escola.
**Current focus:** Phase 2 - Autenticação

## Current Position

Phase: 2 of 6 (Autenticação)
Plan: 0 of ? in current phase
Status: Ready to plan
Last activity: 2026-04-26 — Phase 01 complete, verified 5/5

Progress: [██████████░░░░░░░░░░] 16%

## Performance Metrics

**Velocity:**
- Total plans completed: 3
- Average duration: 5 min
- Total execution time: 0.17 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 01-infraestrutura | 3 | 3 | 5 min |

**Recent Trend:**
- Last 5 plans: 01-01 (4 min), 01-03 (completed), 01-02 (6 min)
- Trend: stable

*Updated after each plan completion*

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- Setup: FastAPI + React + SQLite stack fixado; SQLAlchemy sync (não async) para evitar problemas de lock no SQLite
- Setup: JWT armazenado em **localStorage** (decisão Phase 2 discuss: com prazo de 7 dias e renovação automática, sessionStorage era inconveniente sem ganho real de segurança para protótipo)
- Setup: Business rules (nota <= max, aluno pertence à turma) aplicadas na service layer Python, não em triggers SQLite
- Alembic: Explicit `connection.commit()` required after `context.run_migrations()` in SQLAlchemy 2.0 + SQLite because DDL implicit commits leave DML uncommitted

### Pending Todos

None yet.

### Blockers/Concerns

- Ambiente de deploy para avaliação não especificado — confirmar antes do fim da Phase 5

### Resolved

- Threshold de aprovação: **média >= 5.0** (confirmado 2026-04-26)
- SMTP para recuperação de senha: **Mailtrap** (desenvolvimento/demo) — usar `mailtrap-python` ou SMTP direto via `fastapi-mail`

## Session Continuity

Last session: 2026-04-26
Stopped at: Phase 2 context gathered — auth UX, token storage (localStorage/7d), recovery flow, profile routing.
Resume file: .planning/phases/02-autentica-o/02-CONTEXT.md
