---
phase: 03-painel-admin
plan: 02
subsystem: backend
tags: [orm, crud, fastapi, sqlalchemy, pytest, admin]
requires:
  - 03-01
provides:
  - "6 SQLAlchemy ORM models for admin entities"
  - "Consolidated admin module (schemas + service + router)"
  - "15 protected /admin/* endpoints with require_role('admin')"
  - "Green pytest suite (11/11 tests passing)"
affects:
  - backend/src/models/aluno.py
  - backend/src/models/turma.py
  - backend/src/models/disciplina.py
  - backend/src/models/professor.py
  - backend/src/models/responsavel.py
  - backend/src/models/professor_turma.py
  - backend/src/models/__init__.py
  - backend/src/admin/__init__.py
  - backend/src/admin/schemas.py
  - backend/src/admin/service.py
  - backend/src/admin/router.py
  - backend/src/main.py
  - backend/tests/conftest.py
  - backend/requirements.txt
key-files.created:
  - backend/src/models/aluno.py
  - backend/src/models/turma.py
  - backend/src/models/disciplina.py
  - backend/src/models/professor.py
  - backend/src/models/responsavel.py
  - backend/src/models/professor_turma.py
  - backend/src/admin/__init__.py
  - backend/src/admin/schemas.py
  - backend/src/admin/service.py
  - backend/src/admin/router.py
key-files.modified:
  - backend/src/models/__init__.py
  - backend/src/main.py
  - backend/tests/conftest.py
  - backend/requirements.txt
key-decisions:
  - "Used db.query() style in service layer to match existing password_reset/service.py codebase"
  - "ProfessorTurma modeled with composite PK (professor_id, turma_id, disciplina_id) — no surrogate id"
  - "professor_turma sync uses replace-all strategy (delete + re-insert) for simplicity and atomicity"
  - "Matricula auto-generated as MAT{year}{id:05d} after db.flush() in same transaction"
  - "Professor/Responsavel creation is atomic: Usuario row flushed first, then profile row, then commit"
  - "Self-deactivation guard (T-03-03) returns 400 when caller tries to deactivate themselves"
  - "Pinned bcrypt <5.0 in requirements.txt to avoid passlib incompatibility"
requirements-completed:
  - ADMIN-01
  - ADMIN-02
  - ADMIN-03
  - ADMIN-04
  - ADMIN-05
  - ADMIN-06
duration: 20min
completed: 2026-04-27
---

# 03-02 Summary: Backend Admin Module

## One-liner
Implemented the complete backend admin module — six ORM models, consolidated schemas/service/router, and main.py registration — delivering 15 protected `/admin/*` endpoints and a green pytest suite.

## What was built

### Task 1: SQLAlchemy ORM models for all 6 entities
- Created `backend/src/models/aluno.py` with `matricula` column (String(20), unique, nullable)
- Created `backend/src/models/turma.py` with nome/ano/serie/turno
- Created `backend/src/models/disciplina.py` with nome/carga_horaria
- Created `backend/src/models/professor.py` with usuario_id FK (CASCADE, unique)
- Created `backend/src/models/responsavel.py` with usuario_id FK (CASCADE, unique)
- Created `backend/src/models/professor_turma.py` with composite PK (professor_id, turma_id, disciplina_id)
- Updated `backend/src/models/__init__.py` to export all models for Alembic autogenerate
- Verified all models import cleanly with `python3 -c "from src.models import ..."`

### Task 2: Admin module — schemas + service + router + main.py registration
- Created `backend/src/admin/schemas.py` with Pydantic v2 schemas for all 6 entities:
  - Create/Update/Out/Paginated for Alunos, Turmas, Disciplinas, Professores, Responsaveis
  - DashboardCounts for summary endpoint
  - ProfessorTurmaRow for junction table sync
- Created `backend/src/admin/service.py` with full CRUD business logic:
  - Dashboard counts (active alunos, turmas, disciplinas, active professores/responsaveis)
  - Aluno CRUD with auto-generated matricula (`MAT{year}{id:05d}`)
  - Turma CRUD with `_sync_professor_turma` replace-all strategy
  - Disciplina CRUD
  - Professor CRUD with atomic Usuario+Professor creation
  - Responsavel CRUD with atomic Usuario+Responsavel creation + aluno linking
  - Self-deactivation guard (`deactivate_usuario` refuses if target == caller)
  - Soft delete only (`ativo = False`); zero hard `db.delete()` calls
- Created `backend/src/admin/router.py` with 15 endpoints:
  - Every endpoint protected by `admin_required = Depends(require_role("admin"))`
  - `/admin/dashboard`, `/admin/alunos/*`, `/admin/turmas/*`, `/admin/disciplinas/*`, `/admin/professores/*`, `/admin/responsaveis/*`, `/admin/usuarios/{id}/deactivate`
- Updated `backend/src/main.py` to `include_router(admin_router)`
- Fixed `backend/tests/conftest.py`:
  - Added imports for all 6 new models so `Base.metadata.create_all()` creates their tables
  - Switched test engine to `StaticPool` to prevent SQLite in-memory connection issues with `TestClient`'s threaded execution

## Outcome
- All 11 tests in `tests/test_admin.py` pass green (exit 0)
- 15 admin endpoints registered in OpenAPI schema
- Every endpoint returns 401 for unauthenticated and 403 for non-admin JWT
- POST `/admin/alunos` returns 201 with auto-generated matricula starting with "MAT"
- POST `/admin/professores` creates both Usuario and Professor atomically (verified by test)
- PUT `/admin/turmas/{id}` replaces professor_turma rows atomically (verified by test)
- POST `/admin/usuarios/{id}/deactivate` returns 400 for self-deactivation (verified by test)

## Deviations
- **bcrypt version conflict**: Environment had bcrypt 5.0.0 installed, which breaks passlib's CryptContext (raises `ValueError: password cannot be longer than 72 bytes` even for short passwords, plus `AttributeError: module 'bcrypt' has no attribute '__about__'`). Downgraded to bcrypt 4.3.0 and added `bcrypt<5.0,>=4.0.1` pin to `requirements.txt` to prevent recurrence. This is a dependency fix, not an architectural change.
- **conftest.py model imports + StaticPool**: The existing conftest.py from Plan 01 only imported `Usuario`; new models needed explicit imports before `Base.metadata.create_all()` to create their tables. Additionally, `TestClient` executes requests in a worker thread, causing SQLite in-memory `SingletonThreadPool` to provide a fresh empty connection. Switched to `StaticPool` so all threads share the same in-memory database connection. These are test infrastructure fixes, not architectural changes.

## Next step
Proceed to **03-03-PLAN.md** — Frontend admin layout: AdminLayout + Sidebar, Modal + ConfirmDialog + EntityTable shared components, AdminDashboard, App.tsx routes.
