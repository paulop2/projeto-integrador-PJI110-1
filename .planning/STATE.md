# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-04-26)

**Core value:** Pais acompanham o desempenho escolar dos filhos — notas e presença — sem precisar ir até a escola.
**Current focus:** Phase 2 - Autenticação

## Current Position

Phase: 2 of 6 (Autenticação)
Plan: 3 of 6 in current phase
Status: In progress
Last activity: 2026-04-27 — Completed 02-03 plan (frontend auth infrastructure)

Progress: [████████████████░░░░] 50%

## Performance Metrics

**Velocity:**
- Total plans completed: 4
- Average duration: 6 min
- Total execution time: 0.33 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 01-infraestrutura | 3 | 3 | 5 min |
| 02-autentica-o | 3 | 3 | 7 min |

**Recent Trend:**
- Last 5 plans: 02-03 (2 min), 02-01 (10 min), 01-01 (4 min), 01-03 (completed), 01-02 (6 min)
- Trend: stable

*Updated after each plan completion*
| Phase 02-autentica-o P03 | 2min | 2 tasks | 2 files |

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- Setup: FastAPI + React + SQLite stack fixado; SQLAlchemy sync (não async) para evitar problemas de lock no SQLite
- Setup: JWT armazenado em **localStorage** (decisão Phase 2 discuss: com prazo de 7 dias e renovação automática, sessionStorage era inconveniente sem ganho real de segurança para protótipo)
- Setup: Business rules (nota <= max, aluno pertence à turma) aplicadas na service layer Python, não em triggers SQLite
- Alembic: Explicit `connection.commit()` required after `context.run_migrations()` in SQLAlchemy 2.0 + SQLite because DDL implicit commits leave DML uncommitted
- Auth: Downgraded bcrypt from 5.0.0 to 4.0.1 to maintain passlib compatibility (bcrypt 5.0 breaks passlib's CryptContext)
- Auth: Raw SQL used for display name resolution (Professor/Responsavel ORM models don't exist yet)
- Auth: Admin seed hash fixed in DB (original migration 0001 hash was for "secret", not "admin123" as commented)
- [Phase 02-autentica-o]: localStorage chosen over sessionStorage for token persistence — With 7-day JWT expiry and automatic renewal, sessionStorage offered no real security benefit for prototype

### Pending Todos

None yet.

### Blockers/Concerns

- Ambiente de deploy para avaliação não especificado — confirmar antes do fim da Phase 5

### Resolved

- Threshold de aprovação: **média >= 5.0** (confirmado 2026-04-26)
- SMTP para recuperação de senha: **Mailtrap** (desenvolvimento/demo) — usar `mailtrap-python` ou SMTP direto via `fastapi-mail`

## Session Continuity

Last session: 2026-04-27
Stopped at: Completed 02-03-PLAN.md (frontend auth infrastructure)
Resume file: None
