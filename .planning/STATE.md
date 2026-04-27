# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-04-26)

**Core value:** Pais acompanham o desempenho escolar dos filhos — notas e presença — sem precisar ir até a escola.
**Current focus:** Phase 3 - Painel Admin

## Current Position

Phase: 3 of 6 (Painel Admin)
Plan: 4 of 5 in current phase
Status: Executing — Plan 4 complete, ready for Plan 5
Last activity: 2026-04-27 — 03-04 completed

Progress: [████████████████████████░░] 45%

## Performance Metrics

**Velocity:**
- Total plans completed: 5
- Average duration: 6 min
- Total execution time: 0.5 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 01-infraestrutura | 3 | 3 | 5 min |
| 02-autentica-o | 4 | 4 | 7 min |

**Recent Trend:**
- Last 5 plans: 02-04 (10 min), 02-03 (2 min), 02-01 (10 min), 01-01 (4 min), 01-03 (completed)
- Trend: stable

*Updated after each plan completion*
| Phase 03-painel-admin P04 | 18min | 2 tasks | 6 files |
| Phase 03-painel-admin P03 | 12min | 2 tasks | 7 files |
| Phase 03-painel-admin P02 | 20min | 2 tasks | 11 files |
| Phase 03-painel-admin P01 | 15min | 3 tasks | 11 files |
| Phase 02-autentica-o P04 | 10min | 2 tasks | 3 files |
| Phase 02-autentica-o P03 | 2min | 2 tasks | 2 files |
| Phase 02-autentica-o P02 | 5min | 2 tasks | 5 files |
| Phase 02-autentica-o P05 | 5min | 2 tasks | 7 files |

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
- [Phase 02-autentica-o]: Used timezone-aware datetime comparison with fallback for naive SQLite datetimes to prevent runtime TypeError during token expiration check — SQLite stores naive datetimes; comparing offset-naive and offset-aware datetimes raises TypeError. Added tzinfo check in validate_and_consume_token to replace naive with UTC timezone before comparison.
- [Phase 02-autentica-o]: AuthProvider wraps RouterProvider so useAuth() works inside route components

### Pending Todos

- [ ] Human verification of Phase 2 auth flow (02-06 Task 2) — scheduled for 2026-04-28
  - Verification steps saved in `.planning/phases/02-autentica-o/02-06-PLAN.md`
  - Servers: start backend (`cd backend && uvicorn src.main:app --reload`) and frontend (`cd frontend && npm run dev`)
  - Open http://localhost:5173 and follow 25 verification steps in plan file

### Blockers/Concerns

- Ambiente de deploy para avaliação não especificado — confirmar antes do fim da Phase 5

### Resolved

- Threshold de aprovação: **média >= 5.0** (confirmado 2026-04-26)
- SMTP para recuperação de senha: **Mailtrap** (desenvolvimento/demo) — usar `mailtrap-python` ou SMTP direto via `fastapi-mail`

## Session Continuity

Last session: 2026-04-27
Stopped at: 02-06-PLAN.md checkpoint — Task 1 (smoke tests) complete, Task 2 (human verification) pending
Resume file: .planning/phases/02-autentica-o/02-06-PLAN.md

**To resume:** Run `/gsd-execute-phase 02` — discovers 5 completed SUMMARYs, resumes from 02-06 checkpoint.
