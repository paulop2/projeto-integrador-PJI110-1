---
phase: 03-painel-admin
plan: 01
type: execute
subsystem: backend+frontend
tags: [alembic, migration, pytest, tailwind, foundations]
requires: []
provides:
  - "matricula column on alunos table"
  - "pytest test infrastructure with 11 admin test stubs"
  - "Tailwind CSS v3 configured and working"
  - "Sonner Toaster mounted at app root"
  - "react-hook-form + zod + @hookform/resolvers installed"
affects:
  - backend/alembic/versions/0003_add_matricula_to_alunos.py
  - backend/requirements.txt
  - backend/tests/__init__.py
  - backend/tests/conftest.py
  - backend/tests/test_admin.py
  - frontend/package.json
  - frontend/package-lock.json
  - frontend/tailwind.config.js
  - frontend/postcss.config.js
  - frontend/src/index.css
  - frontend/src/main.tsx
key-files.created:
  - backend/alembic/versions/0003_add_matricula_to_alunos.py
  - backend/tests/__init__.py
  - backend/tests/conftest.py
  - backend/tests/test_admin.py
  - frontend/tailwind.config.js
  - frontend/postcss.config.js
key-files.modified:
  - backend/requirements.txt
  - frontend/package.json
  - frontend/package-lock.json
  - frontend/src/index.css
  - frontend/src/main.tsx
key-decisions:
  - "Used python3 -m pip install and python3 -m alembic since pip/alembic not on PATH"
  - "Reinstalled frontend node_modules with Node 22.11.0 to resolve Vite 8 / rolldown native binding issue"
  - "Removed @rolldown/binding-darwin-arm64 from package.json devDependencies to keep project cross-platform"
requirements-completed:
  - ADMIN-01 (partial - schema + tests)
  - ADMIN-02 (partial - tests)
  - ADMIN-03 (partial - tests)
  - ADMIN-04 (partial - tests)
  - ADMIN-05 (partial - tests)
  - ADMIN-06 (partial - tests)
duration: 15min
completed: 2026-04-27
---

# 03-01 Summary: Foundations for Painel Admin

## One-liner
Installed and configured all foundational infrastructure that every other plan in Phase 3 depends on: Alembic migration 0003 (matricula), pytest test suite with stubs, Tailwind v3 + new npm packages.

## What was built

### Task 1: Alembic migration 0003 — add matricula to alunos + apply
- Created `backend/alembic/versions/0003_add_matricula_to_alunos.py` with `batch_alter_table` adding `matricula` String(20) nullable + unique constraint `uq_alunos_matricula`
- Applied migration with `alembic upgrade head`; verified `PRAGMA table_info(alunos)` shows matricula column
- `alembic current` confirms `0003 (head)`

### Task 2: pytest + httpx install + test infrastructure
- Added `pytest>=8.0.0` and `httpx>=0.27.0` to `backend/requirements.txt`
- Installed dependencies with `python3 -m pip install -r requirements.txt`
- Created `backend/tests/__init__.py` (empty package marker)
- Created `backend/tests/conftest.py` with 6 fixtures: `test_db`, `client`, `admin_user`, `professor_user`, `admin_headers`, `professor_headers`
- Created `backend/tests/test_admin.py` with 11 test stubs covering all ADMIN-01..06 requirements plus security tests (401/403/self-deactivation)
- Verified `pytest --collect-only` collects 11 tests with 0 import errors

### Task 3: Tailwind v3 install + config + index.css directives + npm packages + fix #root
- Installed `tailwindcss@3`, `postcss`, `autoprefixer` as devDependencies
- Installed `sonner`, `react-hook-form`, `zod`, `@hookform/resolvers` as dependencies
- Generated `tailwind.config.js` and `postcss.config.js` with ESM `export default` syntax
- Updated `tailwind.config.js` content to `['./index.html', './src/**/*.{js,ts,jsx,tsx}']`
- Prepended `@tailwind base/components/utilities` to `frontend/src/index.css`
- Removed `#root` width constraint (`width: 1126px`, `margin: 0 auto`, `text-align: center`, `border-inline`) to support full-screen sidebar layout
- Added `<Toaster richColors position="top-right" />` to `frontend/src/main.tsx`
- Verified `npm run build` exits 0 with Node 22.11.0

## Outcome
- Migration 0003 applied successfully; alunos table now has matricula column
- pytest collects 11 tests without errors (tests will be red until Plan 02 implements backend)
- Frontend builds without PostCSS/Tailwind errors
- All new npm packages present in node_modules and package.json

## Deviations
- **Node version / build environment**: The existing project used Vite 8 with Node 16, which is incompatible. To satisfy the `npm run build` acceptance criterion, reinstalled `node_modules` using Node 22.11.0 and explicitly added the `@rolldown/binding-darwin-arm64` package (subsequently removed from `package.json` to keep the project cross-platform; it remains in `package-lock.json`). Build now succeeds. This is an environment fix, not an architectural change.

## Next step
Proceed to **03-02-PLAN.md** — Backend admin module: ORM models (6 entities), admin schemas + service + router, main.py registration, test suite green.
