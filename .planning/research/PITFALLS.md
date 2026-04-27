# Pitfalls Research

**Domain:** School management web app (FastAPI + React + SQLite, team of students)
**Researched:** 2026-04-26
**Confidence:** HIGH (critical pitfalls verified against official docs and multiple sources)

---

## Critical Pitfalls

### Pitfall 1: PostgreSQL Trigger Syntax in the SQLite Schema

**What goes wrong:**
The current `database-schema.md` document defines triggers using PostgreSQL PL/pgSQL syntax:
`RETURNS TRIGGER AS $$ ... $$ LANGUAGE plpgsql`. This syntax does not exist in SQLite.
SQLite uses: `CREATE TRIGGER name BEFORE|AFTER INSERT|UPDATE|DELETE ON table BEGIN ... END`.
If anyone copies those trigger definitions into SQLite migrations, they will fail to run entirely
and the business-rule validations (nota excede valor, aluno pertence à turma) will silently not exist.

**Why it happens:**
Documentation was written with PostgreSQL patterns in mind but the chosen database is SQLite.
Common in student projects where different team members write different parts without cross-checking.

**How to avoid:**
Rewrite all trigger definitions in SQLite syntax before implementation begins. In SQLite, cross-table
validation triggers look like:

```sql
CREATE TRIGGER trg_validate_nota_maxima
BEFORE INSERT ON notas
BEGIN
    SELECT CASE
        WHEN NEW.valor > (SELECT valor_maximo FROM avaliacoes WHERE id = NEW.avaliacao_id)
        THEN RAISE(ABORT, 'Nota excede o valor maximo da avaliacao')
    END;
END;
```

Also enable foreign key enforcement explicitly — SQLite does NOT enforce foreign keys by default:
`PRAGMA foreign_keys = ON;` must be executed on every new connection.

**Warning signs:**
- Trigger definitions containing `LANGUAGE plpgsql`, `RETURNS TRIGGER`, or `$$` delimiters
- No `PRAGMA foreign_keys = ON` in the SQLAlchemy engine setup
- Tests passing for invalid data (child of wrong class, grade above max)

**Phase to address:** Database / Backend setup — first sprint, before any feature work.

---

### Pitfall 2: SQLite Concurrency — "database is locked" Under FastAPI

**What goes wrong:**
FastAPI runs in an async event loop but synchronous SQLAlchemy sessions block the event loop when
they execute queries. SQLite allows only one writer at a time. Under concurrent requests (e.g., a
teacher submitting attendance while the admin is saving a student), SQLite returns `OperationalError:
database is locked`. Without `busy_timeout`, this failure is instant with no retry.

**Why it happens:**
- `check_same_thread=False` is used to avoid the "SQLite objects created in a thread can only be used
  in that same thread" error, but this does not solve write serialization.
- Synchronous SQLAlchemy in async FastAPI route handlers runs DB calls in a threadpool — multiple
  threads competing to write trigger the lock.
- No `busy_timeout` configured, so the lock fails immediately rather than waiting.

**How to avoid:**
Configure the engine with WAL mode and a busy timeout:

```python
from sqlalchemy import create_engine, event

engine = create_engine(
    "sqlite:///./escola.db",
    connect_args={"check_same_thread": False},
)

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA busy_timeout=5000")  # wait up to 5s before giving up
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
```

For the prototype scale (one school, few simultaneous users), this is sufficient. Do not use async
SQLAlchemy with SQLite — `aiosqlite` introduces additional complexity without real benefit at this scale.

**Warning signs:**
- `OperationalError: database is locked` appearing in logs during testing
- No `busy_timeout` pragma in engine setup
- Multiple background tasks or concurrent test requests triggering lock errors

**Phase to address:** Backend infrastructure setup — before any endpoint implementation.

---

### Pitfall 3: RBAC Bypass — Authorization Checked Only at the Route Level

**What goes wrong:**
The permission matrix is well-defined in `api-architecture.md`, but a common implementation mistake
is enforcing role checks only at the FastAPI route decorator level (e.g., via `Depends(get_current_user)`)
without also verifying data ownership in the query. A teacher who knows a `chamada_id` belonging to
another teacher can hit `GET /chamadas/{id}` and receive data if the route only checks "is a teacher"
rather than "is THIS teacher's chamada". Similarly, a parent who knows a child's `aluno_id` that is
not theirs can query `/notas/{alunoId}` if the query does not filter by `responsavel_id`.

**Why it happens:**
Students split frontend/backend work. The person writing the route focuses on "does the user have a
valid token and the right role?" but forgets "does this user own this resource?". The frontend never
shows unauthorized data, so the bug is invisible during manual testing.

**How to avoid:**
Every query for a resource that belongs to a specific user must include an ownership filter:

```python
# WRONG — role only
@router.get("/notas/{aluno_id}")
async def get_notas(aluno_id: int, user=Depends(get_current_user), db=Depends(get_db)):
    return db.query(Nota).filter(Nota.aluno_id == aluno_id).all()

# CORRECT — role + ownership
@router.get("/notas/{aluno_id}")
async def get_notas(aluno_id: int, user=Depends(get_current_user), db=Depends(get_db)):
    if user.tipo == "responsavel":
        aluno = db.query(Aluno).filter(
            Aluno.id == aluno_id,
            Aluno.responsavel_id == user.responsavel_id  # ownership check
        ).first()
        if not aluno:
            raise HTTPException(status_code=403, detail="Acesso negado")
    elif user.tipo == "professor":
        # verify student belongs to one of professor's classes
        ...
    return db.query(Nota).filter(Nota.aluno_id == aluno_id).all()
```

Create a shared `verify_aluno_access(aluno_id, user, db)` utility used by every endpoint that touches
student data. Test each endpoint with the wrong user's token explicitly.

**Warning signs:**
- Routes that accept `aluno_id` as a path parameter without querying against the authenticated user's profile
- No tests that verify a teacher cannot access another teacher's data using a known ID
- Authorization logic duplicated per-route rather than extracted into a shared function

**Phase to address:** Backend — auth and permission layer, before implementing chamadas/notas endpoints.

---

### Pitfall 4: JWT Stored in localStorage — XSS Vulnerability

**What goes wrong:**
`frontend-architecture.md` specifies storing the JWT in `localStorage` or `sessionStorage`. Both are
accessible to any JavaScript running on the page. If a single dependency or third-party script has an
XSS vulnerability, the token can be stolen and the attacker impersonates any user (including admin).

**Why it happens:**
localStorage is the simplest approach and is universally shown in tutorials. The security implication
is not obvious until a specific attack is demonstrated.

**How to avoid:**
For this prototype, using `sessionStorage` (not `localStorage`) is the minimum improvement: the token
disappears when the browser tab closes. For production-grade security, store the access token in memory
(React state/context) and use an `HttpOnly` cookie for the refresh token. Given the academic context
and prototype scope, `sessionStorage` + short token expiry (the current 8h is acceptable for school
hours but could be reduced) is a reasonable pragmatic tradeoff.

At minimum, never use `dangerouslySetInnerHTML` with user-supplied content anywhere in the app. The main
XSS vector in this codebase would be teacher-entered observacoes or justificativa fields rendered as HTML.

**Warning signs:**
- `localStorage.setItem('token', ...)` in auth code
- Any `dangerouslySetInnerHTML` usage in components that render user input (student names, observations)
- Dependencies with known XSS vulnerabilities (`npm audit` warnings)

**Phase to address:** Frontend auth implementation — first auth sprint.

---

### Pitfall 5: CORS Misconfiguration Blocking Frontend-Backend Integration

**What goes wrong:**
React dev server runs on `localhost:5173` (Vite default), FastAPI on `localhost:8000`. Without correct
CORS headers, every browser request is blocked. The common mistake is either:
- `allow_origins=["*"]` combined with `allow_credentials=True` — browsers reject this combination
- `allow_origins=["http://localhost:3000"]` when Vite serves on port `5173`
- Forgetting to add CORS middleware before other custom middleware in FastAPI

**Why it happens:**
CORS is counterintuitive. Students often cargo-cult configurations from Stack Overflow that use a
different port or framework version.

**How to avoid:**
Set CORS explicitly from the start:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Add CORS middleware first, before any other middleware. Use environment variables for origins so the
same config works in development and production. Alternatively, configure a Vite proxy so all `/api`
calls are proxied to the backend — this eliminates CORS entirely during development.

**Warning signs:**
- "Access-Control-Allow-Origin" errors in browser console on first integration attempt
- Frontend team and backend team testing independently without integration test
- No integration tested until late in the project

**Phase to address:** Project setup — day one, before any feature work begins.

---

### Pitfall 6: Scope Creep from Real School Stakeholder

**What goes wrong:**
The project has a real community partner (professora Elizabete). After initial validation, stakeholders
tend to request additions once they see a working prototype: "Can teachers also message parents?", "Can
we export the grade report as PDF?", "Can the admin schedule classes?". Each addition sounds small but
can consume 2-3 development days, and with an 8-person team under a fixed May 24 deadline, even two
scope additions can derail delivery.

**Why it happens:**
The team wants to be responsive to the real user, which is the right instinct. But in an academic
project with a hard deadline, any feature not in the agreed scope is a risk.

**How to avoid:**
Define and freeze scope in writing before development. The current `PROJECT.md` out-of-scope list is
good — reference it explicitly in every stakeholder interaction. Use the phrase "version 2" for every
new request. Assign one team member as scope guardian who has explicit authority to say "this goes in
the backlog, not this sprint."

**Warning signs:**
- Stakeholder meetings producing new feature requests after Week 2
- Any sprint containing a feature not in the original requirements list
- Team members saying "it's just a small addition" for something not in scope

**Phase to address:** Project kickoff — establish scope document and stakeholder communication protocol.

---

### Pitfall 7: Mixed Technical Levels Leading to Inconsistent Code and Integration Failures

**What goes wrong:**
With 8 students of varying technical backgrounds, the risk is that two people implement the same pattern
differently: one uses Pydantic v1 style, another uses v2; one returns raw dicts, another returns Pydantic
models; one uses `Session` directly, another uses dependency injection. The frontend team builds against
assumed API contracts that differ from the actual implementation, causing integration bugs discovered late.

**Why it happens:**
Without a shared conventions document reviewed by everyone, each developer defaults to tutorials they
found individually. FastAPI is used by people at different stages — some follow older v0.x docs.

**How to avoid:**
Establish a coding conventions document in Week 1 covering:
- Pydantic version (use v2 — current default with FastAPI 0.100+)
- Response schema (all endpoints use the standard success/error envelope from `api-architecture.md`)
- SQLAlchemy session pattern (always via `Depends(get_db)`, never instantiated directly)
- Error handling (always raise `HTTPException`, never return error dicts)
- Frontend API calls (all via a central `apiClient` instance, never raw `fetch` or `axios` calls inline)

Define one complete endpoint end-to-end (e.g., `GET /alunos`) as a reference implementation that the
whole team reviews before splitting work.

**Warning signs:**
- Different endpoints returning different response shapes
- Frontend making requests to hardcoded URLs instead of a central API config
- "It works on my machine" reports during team integration sessions
- Pydantic validation errors on previously tested endpoints after a merge

**Phase to address:** Project setup and first feature implementation.

---

## Technical Debt Patterns

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| `check_same_thread=False` without WAL + busy_timeout | Avoids thread error | "database is locked" crashes in demo | Never — always pair with WAL pragma |
| Hardcoded `SECRET_KEY` in source code | Fewer env var concerns | Any token is forgeable once code is public | Never — use `.env` from day one |
| Role check only, no ownership check in queries | Faster to implement | IDOR vulnerability exposing all students' data | Never for data-access routes |
| `allow_origins=["*"]` in CORS | Quick fix for CORS errors | Incompatible with credentials; security risk | Development only, never commit |
| No SQLAlchemy migrations (recreate DB on change) | Simpler early on | Data loss on every schema change | Acceptable until first real data; then use Alembic |
| Skipping input validation on grade/attendance forms | Faster UI | Corrupt data (negative grades, future attendance) | Never — validate both frontend and backend |

---

## Integration Gotchas

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| React + FastAPI auth | Storing JWT in `localStorage` | Use `sessionStorage` for prototype; HttpOnly cookie for production |
| Vite + FastAPI | Hardcoding `http://localhost:8000` in every component | Central `axios` instance with `baseURL` from env var (`VITE_API_URL`) |
| SQLAlchemy + SQLite | Using async SQLAlchemy (`aiosqlite`) expecting better perf | Use sync SQLAlchemy with WAL + busy_timeout; async adds complexity without benefit at this scale |
| React Router + FastAPI | React Router routes returning 404 on page refresh in production | Configure the server to serve `index.html` for all non-API routes |
| JWT expiry + React | Token expires silently; user gets 401 with no explanation | Axios interceptor catches 401, clears token, redirects to `/login` |
| SQLite + Foreign Keys | Assuming FK constraints are enforced | Explicitly run `PRAGMA foreign_keys = ON` on every connection via SQLAlchemy event |

---

## Performance Traps

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| N+1 query on chamada listing | Attendance page slow; each student's name is a separate query | Use `joinedload` or explicit JOIN in SQLAlchemy | 20+ students per class |
| Fetching all notas without pagination | Boletim page loads all historical grades | Add `limit/offset` pagination from the start (already in API spec) | Multiple school years of data |
| No database indexes on `aluno_id`, `turma_id` | Slow queries when filtering by class or student | Indexes defined in schema — verify they are created in migrations | 100+ students |
| Frontend loading all classes to populate a select | Slow turma dropdown | Add server-side filtering/search for dropdowns | 20+ classes |

Scale note: this is a single school prototype. The performance traps above are relevant even at small
scale if the demo runs slowly — a slow demo loses credibility with the academic evaluator.

---

## Security Mistakes

| Mistake | Risk | Prevention |
|---------|------|------------|
| PostgreSQL trigger syntax in SQLite | Business rules silently not enforced; invalid grades can be stored | Rewrite all triggers in SQLite syntax; add unit tests that verify constraints |
| No `PRAGMA foreign_keys = ON` | Orphaned records (notas without valid aluno); data integrity failure | Set via SQLAlchemy connect event |
| Parent can query any student's grades by guessing ID | Data breach — child privacy | Always filter by authenticated user's `responsavel_id` |
| Teacher can modify another teacher's attendance by guessing ID | Data tampering | Always filter by authenticated user's `professor_id` |
| JWT secret in `.env` committed to git | Any token forgeable by anyone with repo access | Add `.env` to `.gitignore` from day one; use `.env.example` with placeholder values |
| No rate limiting on `/auth/login` | Brute force password attacks | For prototype: acceptable; note it as known limitation in documentation |

---

## UX Pitfalls

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| Teacher must select turma, then disciplina, then date on separate steps to take attendance | Friction reduces teacher adoption | Single-page chamada form: select turma + disciplina + date, then list of students appears |
| Parent sees raw attendance numbers (12/20) without context | Parent doesn't know if it's good or bad | Show percentage and highlight when below 75% (LDB minimum) |
| No loading states on form submissions | Teacher double-submits attendance; duplicate chamada constraint violation | Disable submit button immediately on first click; show spinner |
| Generic error messages ("Erro interno") | User cannot self-recover | Map backend error codes to user-friendly Portuguese messages |
| Admin must create `usuario` + `professor` records separately | Confusing two-step flow | Admin form creates both in a single transaction |

---

## "Looks Done But Isn't" Checklist

- [ ] **Attendance:** Form submits but no check whether a chamada already exists for this turma+disciplina+date — verify the unique constraint error is caught and shown as a friendly message.
- [ ] **Grades:** Teacher can enter a grade value above `valor_maximo` if frontend validation is skipped — verify the backend rejects it with a clear error.
- [ ] **Role protection:** Parent visiting `/alunos` in the URL bar should redirect to their dashboard, not show a 403 JSON response — verify `RoleRoute` redirects, not just blocks.
- [ ] **Token expiry:** After 8 hours, all API calls return 401 — verify the Axios interceptor catches this and redirects to `/login` rather than showing a cryptic error.
- [ ] **SQLite FK enforcement:** After setup, insert a `presenca` with an invalid `aluno_id` — verify it is rejected. If not, `PRAGMA foreign_keys = ON` is not running.
- [ ] **Admin creates user:** Creating a professor user should also create a `professores` record — verify both rows exist after the form submission.
- [ ] **Inactive user:** A user with `ativo = false` can still log in if the login endpoint only checks email/password — verify `ativo` is checked before issuing the JWT.

---

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Wrong trigger syntax discovered late | MEDIUM | Rewrite triggers in SQLite syntax; add tests; no data loss if caught before real data |
| RBAC bypass discovered after data entry | HIGH | Audit all queries; add ownership filters; review all exposed data; potentially notify affected parties |
| Database locked errors in demo | MEDIUM | Enable WAL + busy_timeout; run a quick smoke test sequence before the demo |
| Scope crept past deadline | HIGH | Revert uncommitted features; deliver core MVP; document deferred features in relatorio-final |
| JWT secret committed to git | HIGH | Rotate secret immediately (invalidates all active sessions); revoke git history or rotate credentials |
| CORS blocking integration mid-sprint | LOW | Add correct CORS config (30-minute fix); unblocks entire frontend team |

---

## Pitfall-to-Phase Mapping

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| PostgreSQL trigger syntax in SQLite | Phase 1 — Database setup | Run migration; attempt invalid grade insert; verify rejection |
| SQLite concurrency (database is locked) | Phase 1 — Backend infrastructure | Run concurrent write test with `pytest-asyncio` |
| RBAC bypass (ownership not checked) | Phase 2 — Auth and permissions layer | Run auth test matrix: each role accessing another's data |
| JWT in localStorage | Phase 2 — Frontend auth | Code review: no `localStorage.setItem('token'...)` |
| CORS misconfiguration | Phase 1 — Project setup | First frontend-backend integration call succeeds |
| Scope creep | Phase 1 — Project kickoff | Scope document signed off before development begins |
| Inconsistent code patterns | Phase 1 — Conventions + reference implementation | Code review checklist applied on first PR |

---

## Sources

- FastAPI official security docs: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
- FastAPI CORS docs: https://fastapi.tiangolo.com/tutorial/cors/
- SQLite official quirks and gotchas: https://sqlite.org/quirks.html
- SQLite WAL mode: https://sqlite.org/wal.html
- SQLite concurrent writes analysis: https://tenthousandmeters.com/blog/sqlite-concurrent-writes-and-database-is-locked-errors/
- FastAPI + SQLAlchemy thread safety discussion: https://github.com/fastapi/fastapi/discussions/5199
- JWT localStorage vs cookies security: https://nulldog.com/jwt-in-localstorage-with-react-security-risks-best-practices
- FastAPI RBAC implementation patterns: https://www.permit.io/blog/fastapi-rbac-full-implementation-tutorial
- FastAPI best practices (community): https://github.com/zhanymkanov/fastapi-best-practices
- Scope creep prevention: https://asana.com/resources/what-is-scope-creep

---
*Pitfalls research for: Sistema Web de Registro Escolar (FastAPI + React + SQLite)*
*Researched: 2026-04-26*
