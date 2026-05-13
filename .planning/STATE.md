# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-04-26)

**Core value:** Pais acompanham o desempenho escolar dos filhos — notas e presença — sem precisar ir até a escola.
**Current focus:** Phase 8 - UX Polish

## Current Position

Phase: 8 of 10 (UX Polish)
Plan: 1 of 3 in current phase
Status: In Progress
Last activity: 2026-05-13 — Completed 08-01 sidebar collapse + AdminLayout header

Progress: [████████████████████░░░░░░░░░░] 70%

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
| 03-painel-admin | 5 | 5 | 15 min |
| 04-portal-do-professor | 4 | 4 | 15 min |

**Recent Trend:**
- Last 5 plans: 05-03 (5 min), 05-02 (12 min), 05-01 (15 min), 04-04 (verification), 04-03 (frontend)
- Trend: stable

| Phase 05-portal-do-responsavel P03 | 5min | 2 tasks | 1 file |
| Phase 05-portal-do-responsavel P02 | 12min | 2 tasks | 7 files |
| Phase 05-portal-do-responsavel P01 | 15min | 2 tasks | 7 files |

*Updated after each plan completion*
| Phase 04-portal-do-professor P04 | 10min | 2 tasks | 3 files |
| Phase 04-portal-do-professor P03 | 15min | 2 tasks | 8 files |
| Phase 04-portal-do-professor P02 | 12min | 2 tasks | 2 files |
| Phase 04-portal-do-professor P01 | 10min | 2 tasks | 11 files |
| Phase 03-painel-admin P05 | 10min | 2 tasks | 1 file |
| Phase 03-painel-admin P04 | 18min | 2 tasks | 6 files |
| Phase 03-painel-admin P03 | 12min | 2 tasks | 7 files |
| Phase 03-painel-admin P02 | 20min | 2 tasks | 11 files |
| Phase 03-painel-admin P01 | 15min | 2 tasks | 11 files |
| Phase 02-autentica-o P04 | 10min | 2 tasks | 3 files |
| Phase 02-autentica-o P03 | 2min | 2 tasks | 2 files |
| Phase 02-autentica-o P02 | 5min | 2 tasks | 5 files |
| Phase 02-autentica-o P05 | 5min | 2 tasks | 7 files |
| Phase 08-ux-polish P01 | 2min | 2 tasks | 2 files |
| Phase 08-ux-polish P08-02 | 3min | 2 tasks | 2 files |

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
- [Phase 08-ux-polish]: Named export UserMenu (not default) for clarity and tree-shaking
- [Phase 08-ux-polish]: Avatar initials computed from first two words of user.nome, matching Sidebar pattern

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

Last session: 2026-05-13
Stopped at: Completed 08-01-PLAN.md
Resume file: None

### UI-SPEC Approved
- Phase 4 UI design contract approved on 2026-04-27
- 6/6 dimensions passed (Copywriting, Visuals, Color, Typography, Spacing, Registry Safety)
- File: `.planning/phases/04-portal-do-professor/04-UI-SPEC.md`

**To resume:** Proceed to Phase 4 planning — `/gsd-plan-phase 04` or `/gsd-discuss-phase 04`.
