# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-04-26)

**Core value:** Pais acompanham o desempenho escolar dos filhos — notas e presença — sem precisar ir até a escola.
**Current focus:** Phase 1 - Infraestrutura

## Current Position

Phase: 1 of 6 (Infraestrutura)
Plan: 2 of 3 in current phase
Status: In progress
Last activity: 2026-04-26 — Completed 01-03 (Frontend Scaffold)

Progress: [██████░░░░] 66%

## Performance Metrics

**Velocity:**
- Total plans completed: 2
- Average duration: 4 min
- Total execution time: 0.07 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 01-infraestrutura | 2 | 3 | 4 min |

**Recent Trend:**
- Last 5 plans: 01-01 (4 min), 01-03 (completed)
- Trend: -

*Updated after each plan completion*

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- Setup: FastAPI + React + SQLite stack fixado; SQLAlchemy sync (não async) para evitar problemas de lock no SQLite
- Setup: JWT armazenado em sessionStorage (não localStorage) — mitigação XSS mínima para protótipo
- Setup: Business rules (nota <= max, aluno pertence à turma) aplicadas na service layer Python, não em triggers SQLite

### Pending Todos

None yet.

### Blockers/Concerns

- Ambiente de deploy para avaliação não especificado — confirmar antes do fim da Phase 5

### Resolved

- Threshold de aprovação: **média >= 5.0** (confirmado 2026-04-26)
- SMTP para recuperação de senha: **Mailtrap** (desenvolvimento/demo) — usar `mailtrap-python` ou SMTP direto via `fastapi-mail`

## Session Continuity

Last session: 2026-04-26
Stopped at: Completed 01-03-PLAN.md (Frontend Scaffold). Next: Wave 2 (01-02 Alembic Schema)
Resume file: None
