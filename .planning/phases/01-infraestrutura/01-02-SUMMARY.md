---
phase: 01-infraestrutura
plan: "02"
subsystem: database

tags: [alembic, sqlalchemy, sqlite, migration, batch-mode]

requires:
  - phase: 01-infraestrutura
    provides: "Backend FastAPI skeleton with database.py (Base, engine, get_db)"
provides:
  - Alembic configuration with batch mode for SQLite
  - Complete database schema with 11 tables
  - Performance indexes on foreign key and query columns
  - Admin seed user for development
  - downgrade/upgrade round-trip capability
affects:
  - 02-* (all feature phases depend on this schema)
  - 03-* (auth endpoints depend on usuarios table)

tech-stack:
  added:
    - alembic>=1.13.0 (already in requirements.txt from 01-01)
  patterns:
    - "Schema managed exclusively via Alembic migrations (no Base.metadata.create_all)"
    - "Manual migration files for definitive schema"
    - "Pre-computed bcrypt hashes in migrations to avoid runtime dependencies"
    - "Explicit connection.commit() after migrations for SQLAlchemy 2.0 + SQLite"

key-files:
  created:
    - backend/alembic.ini
    - backend/alembic/env.py
    - backend/alembic/script.py.mako
    - backend/alembic/README
    - backend/alembic/versions/0001_initial_schema.py
  modified:
    - backend/alembic/env.py (added explicit connection.commit() fix)

key-decisions:
  - "Added explicit connection.commit() after context.run_migrations() in env.py to fix SQLAlchemy 2.0 + SQLite transaction behavior where DDL implicit commits prevent DML persistence"

patterns-established:
  - "Alembic env.py: PRAGMA foreign_keys=OFF during migration, ON after, with explicit commit"
  - "render_as_batch=True in both offline and online modes for SQLite ALTER TABLE support"
  - "NAMING_CONVENTION for consistent constraint/index naming across the schema"
  - "Seed data via op.execute() with hardcoded bcrypt hash (no runtime passlib dependency)"

duration: 6min
completed: 2026-04-26
---

# Phase 1 Plan 2: Alembic Schema Migration Summary

**Complete school database schema with 11 tables, performance indexes, check constraints, and admin seed user, managed via Alembic with SQLite batch mode and explicit commit for SQLAlchemy 2.0 compatibility.**

## Performance

- **Duration:** 6 min
- **Started:** 2026-04-26T22:25:19Z
- **Completed:** 2026-04-26T22:31:32Z
- **Tasks:** 2
- **Files modified:** 5

## Accomplishments
- Initialized Alembic in backend/ with custom env.py importing src.database Base/engine
- Configured render_as_batch=True in both offline and online migration modes
- Added PRAGMA foreign_keys=OFF/ON wrapper and naming convention for constraints
- Created 0001_initial_schema.py with all 11 system tables and their relationships
- Added performance indexes on: notas.avaliacao_id, notas.aluno_id, presencas.chamada_id, presencas.aluno_id, alunos.responsavel_id, alunos.turma_id, professor_turma.professor_id, chamadas.turma_id, chamadas.data, avaliacoes.turma_id, avaliacoes.bimestre
- Added check constraints: bimestre IN (1,2,3,4) and valor_maximo > 0
- Inserted admin seed user (admin@escola.dev / admin123) with pre-computed bcrypt hash
- Verified FK enforcement rejects invalid references with IntegrityError
- Verified clean downgrade/upgrade round-trip

## Task Commits

Each task was committed atomically:

1. **Task 1: Inicializar Alembic e configurar env.py com batch mode** — `180ab71` (chore)
2. **Task 2: Criar migration inicial com schema completo (11 tabelas) e seed admin** — `fdf592a` (feat)

**Plan metadata:** _(to be committed after summary creation)_

## Files Created/Modified
- `backend/alembic.ini` — Alembic configuration with SQLite URL and script locations
- `backend/alembic/env.py` — Custom environment with batch mode, explicit commit, FK pragma handling, naming convention
- `backend/alembic/script.py.mako` — Migration template (Alembic default)
- `backend/alembic/README` — Alembic README (default)
- `backend/alembic/versions/0001_initial_schema.py` — Complete schema migration with 11 tables, indexes, constraints, and admin seed

## Decisions Made
- Added explicit `connection.commit()` after `context.run_migrations()` in `env.py` because SQLAlchemy 2.0 + SQLite requires it for DML (INSERT, alembic_version updates) to persist after DDL statements cause implicit commits.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] DML not persisting after DDL in SQLAlchemy 2.0 + SQLite**
- **Found during:** Task 2 (running alembic upgrade head)
- **Issue:** Migration reported success and created all 11 tables, but `alembic_version` table was empty and admin seed INSERT was missing. This occurred because DDL statements (CREATE TABLE) in SQLite cause implicit transaction commits, leaving subsequent DML (INSERT, alembic_version update) in an uncommitted state that gets rolled back when the SQLAlchemy 2.0 connection context manager exits.
- **Fix:** Added `connection.commit()` immediately after `context.run_migrations()` in `env.py`'s `run_migrations_online()` function.
- **Files modified:** `backend/alembic/env.py`
- **Verification:** After fix, `alembic upgrade head` correctly populates `alembic_version` with `0001` and inserts the admin seed. Downgrade/upgrade round-trip confirmed clean.
- **Committed in:** `fdf592a` (Task 2 commit)

---

**Total deviations:** 1 auto-fixed (1 bug)
**Impact on plan:** Fix is essential for correct Alembic operation with SQLAlchemy 2.0 and SQLite. No scope creep.

## Issues Encountered
- SQLAlchemy 2.0 connection behavior with SQLite implicit DDL commits caused DML to be silently lost. Resolved by adding explicit `connection.commit()` in env.py.

## User Setup Required
None — no external service configuration required.

## Next Phase Readiness
- Database schema is complete and managed via Alembic
- Ready for **Plan 03** (Frontend Scaffold) — backend data layer is solid
- Ready for **Phase 2** (Autenticação) — `usuarios` table with admin seed is available
- Ready for **Phase 3-6** — all required tables (alunos, turmas, disciplinas, notas, presencas, etc.) are in place

## Self-Check: PASSED

- [x] All 5 key files exist on disk
- [x] Commit `180ab71` found in git history
- [x] Commit `fdf592a` found in git history
- [x] `alembic current` returns `0001 (head)`
- [x] 11 system tables exist in escola.db
- [x] Admin seed present in usuarios table
- [x] FK enforcement rejects invalid references
- [x] `alembic downgrade base && alembic upgrade head` completes cleanly

---
*Phase: 01-infraestrutura*
*Completed: 2026-04-26*
