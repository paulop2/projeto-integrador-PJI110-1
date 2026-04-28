---
phase: 05-portal-do-responsavel
plan: 01
subsystem: api
tags: [fastapi, sqlalchemy, pytest, pydantic]

requires:
  - phase: 04-portal-do-professor
    provides: professor module patterns, test fixture patterns, chamada/presenca models
provides:
  - backend responsavel module (schemas, router, service)
  - responsavel test fixtures (responsavel_user, responsavel_headers)
  - complete test_responsavel.py with 17 tests covering RESP-01 through RESP-06
affects:
  - 05-02 (frontend portal depends on backend API contracts)
  - 05-03 (verification depends on tests passing)

tech-stack:
  added: []
  patterns:
    - "_get_responsavel(db, usuario) helper resolves profile from JWT"
    - "_assert_responsavel_owns_aluno returns 403 (not 404) for IDOR prevention"
    - "Frequência query counts ALL chamadas without professor_id filter"

key-files:
  created:
    - backend/src/responsavel/__init__.py
    - backend/src/responsavel/schemas.py
    - backend/src/responsavel/router.py
    - backend/src/responsavel/service.py
    - backend/tests/test_responsavel.py
  modified:
    - backend/src/main.py
    - backend/tests/conftest.py

key-decisions:
  - "Avaliacao schema requires professor_id and titulo NOT NULL — tests updated to match actual DB constraints"
  - "Chamada schema requires professor_id NOT NULL and data as Python date object — tests updated accordingly"

patterns-established:
  - "Responsavel module mirrors professor/ exactly: schemas → service → router → main.py registration"
  - "Ownership check returns 403 (not 404) to prevent IDOR information leakage"

requirements-completed:
  - RESP-01
  - RESP-02
  - RESP-03
  - RESP-04
  - RESP-05
  - RESP-06

duration: 15min
completed: 2026-04-27
---

# Phase 5 Plan 1: Backend Responsavel Module + Test Scaffold Summary

**Backend responsavel API module with IDOR-safe ownership checks, automatic média/frequência calculations, and 17-test pytest suite covering all RESP requirements**

## Performance

- **Duration:** 15 min
- **Started:** 2026-04-27
- **Completed:** 2026-04-27
- **Tasks:** 2
- **Files modified:** 7

## Accomplishments
- Created `backend/src/responsavel/` package with Pydantic v2 schemas, service layer, and API router
- Implemented `_get_responsavel` and `_assert_responsavel_owns_aluno` helpers with 403-based IDOR prevention
- Built `get_boletim` service function with automatic média calculation, frequência aggregation, and LDB approval rule
- Registered responsavel router in `backend/src/main.py`
- Added `responsavel_user` and `responsavel_headers` fixtures to `backend/tests/conftest.py`
- Created comprehensive `backend/tests/test_responsavel.py` with 17 tests (all green)

## Task Commits

1. **Task 1: Create responsavel backend module (schemas, router, service) and register in main.py** - `e608542` (feat)
2. **Task 2: Add responsavel_user + responsavel_headers fixtures to conftest.py and create test_responsavel.py** - `867ccf9` (test)

## Files Created/Modified
- `backend/src/responsavel/__init__.py` - Python package marker
- `backend/src/responsavel/schemas.py` - `FilhoOut` and `DisciplinaBoletimRow` Pydantic v2 schemas
- `backend/src/responsavel/router.py` - APIRouter with `/meus-filhos` and `/boletim` endpoints
- `backend/src/responsavel/service.py` - Full service logic with ownership enforcement and LDB approval rule
- `backend/tests/test_responsavel.py` - 17 tests covering access control, IDOR, notas, média, frequência, and approval
- `backend/src/main.py` - responsavel_router registration
- `backend/tests/conftest.py` - responsavel_user and responsavel_headers fixtures

## Decisions Made
- Followed professor module pattern exactly for consistency
- Service returns plain dicts for `DisciplinaBoletimRow` (no `from_attributes=True`) matching professor/schemas.py pattern

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Avaliacao and Chamada test setup did not match actual DB schema constraints**
- **Found during:** Task 2 (test_responsavel.py creation)
- **Issue:** Plan's test code created `Avaliacao` without `professor_id` and `titulo`, and `Chamada` without `professor_id` and with string `data` instead of Python `date` object. These caused `IntegrityError` and `TypeError` respectively because the actual models enforce `professor_id NOT NULL`, `titulo NOT NULL`, and `data: Mapped[date]`.
- **Fix:** Updated all `Avaliacao()` instantiations to include `professor_id=prof.id` and `titulo="Prova"`. Updated all `Chamada()` instantiations to include `professor_id=prof.id` and `data=date(YYYY, M, D)`. Added `from datetime import date` import.
- **Files modified:** `backend/tests/test_responsavel.py`
- **Verification:** `python3 -m pytest tests/test_responsavel.py -x -q` → 17 passed
- **Committed in:** `867ccf9` (Task 2 commit)

---

**Total deviations:** 1 auto-fixed (1 bug)
**Impact on plan:** Fix necessary for tests to execute against actual schema. No scope creep.

## Issues Encountered
- None beyond the schema constraint mismatch auto-fixed above.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Backend API contracts are stable and tested
- Frontend portal (05-02) can proceed to consume `/responsavel/meus-filhos` and `/responsavel/boletim`
- All tests green — no blockers for Wave 2

---
*Phase: 05-portal-do-responsavel*
*Completed: 2026-04-27*
