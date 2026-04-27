# Phase 4: Portal do Professor - Research

**Researched:** 2026-04-27
**Domain:** FastAPI professor module + React professor portal (attendance, grades, frequency)
**Confidence:** HIGH — all claims verified against the live codebase

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **Navigation:** Landing page shows cards of linked turmas. Card: nome da turma, disciplina(s) vinculada(s), nº alunos. Inside turma: three tabs — Chamada | Notas | Frequencia. Breadcrumb `Minhas Turmas > Turma A`.
- **Chamada:** Default date = today. Toggle Presente/Falta per student. Initial state for new (unsaved) chamada: all Presente. Saved chamadas are editable, with warning. Feedback: toast/snackbar on save.
- **Notas:** Flow: professor picks turma + disciplina first, then a students-x-bimesters grid opens. Grade/table format — alunos em linhas, 1o ao 4o bimestre em colunas. Inline error validation (red border, prevents save). Explicit "Salvar" button.
- **Frequencia:** Third tab. Shows percentual + count per student (e.g., 85% — 17/20 aulas). Visual highlight for < 75% (red row + badge). Period: ano letivo acumulado (Claude's simplest option for prototype).

### Claude's Discretion
- How the professor accesses chamadas from previous dates (date selector vs. paginated history)
- Period shown in frequency summary (ano letivo vs. filterable by bimestre)
- Detailed design of the Presente/Falta toggle
- Keyboard navigation between grade cells (Tab, Enter, etc.)

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope.

</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| PROF-01 | Professor pode registrar chamada (lista de presença/falta) por turma e data | `chamadas` + `presencas` tables confirmed in migration 0001; no ORM models exist yet — must create |
| PROF-02 | Professor só vê turmas às quais está vinculado (ownership check) | `professor_turma` table confirmed: (professor_id, turma_id, disciplina_id) composite PK; `require_role("professor")` pattern from `auth/dependencies.py` |
| PROF-03 | Professor pode lançar notas por aluno, disciplina e bimestre (1o ao 4o) | `avaliacoes` + `notas` tables confirmed; complex — notas are linked via an intermediate `avaliacao` record; see Architecture Patterns section |
| PROF-04 | Professor pode editar notas e presenças já registradas | Upsert pattern on presencas (unique constraint on chamada_id+aluno_id); avaliacoes use upsert on notas (unique constraint on avaliacao_id+aluno_id) |
| PROF-05 | Professor pode visualizar resumo de frequência da turma (% de presença por aluno) | Aggregation query across `presencas` + `chamadas` for a given turma_id filtered to professor's linked turmas |

</phase_requirements>

---

## Summary

Phase 4 implements the professor portal on top of the existing schema, auth, and admin module. The database schema was declared complete in migration 0001 — all five tables needed for this phase already exist: `professor_turma`, `chamadas`, `presencas`, `avaliacoes`, and `notas`. No new migrations are expected.

What does NOT exist yet: ORM models for chamadas, presencas, avaliacoes, and notas; a professor API module (`src/professor/`); professor-specific frontend pages. The existing `ProfessorDashboard` is a stub (6 lines, no data). The entire business logic for this phase is greenfield within a well-patterned codebase.

The critical architectural decision already in the schema is that grades use a two-level structure: an `avaliacao` row (which represents a bimestre's evaluation context per turma+disciplina) is created first, and then `notas` are attached to that avaliacao per student. The UI contract from CONTEXT.md — a flat grade grid (students × 4 bimesters) — must be backed by upsert logic that finds-or-creates the avaliacao for each bimestre, then upserts the nota.

**Primary recommendation:** Mirror the admin module pattern exactly. Create `src/professor/` with router + service + schemas. Add four ORM models (Chamada, Presenca, Avaliacao, Nota). Wire into main.py. Build professor frontend pages under `src/pages/professor/`.

---

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Ownership check (professor sees own turmas only) | API / Backend | — | Security rule must be enforced server-side; client filter alone is insufficient for PROF-02 |
| Chamada create/upsert | API / Backend | — | Atomic write across chamadas + presencas tables |
| Notas upsert (find-or-create avaliacao + upsert nota) | API / Backend | — | Business logic involving two tables; client cannot safely orchestrate |
| Frequencia aggregation (% per aluno) | API / Backend | — | SQL aggregation is more efficient than client-side calculation over paginated data |
| Professor landing page (turma cards) | Frontend (React) | — | Read-only display; consumes API response |
| Chamada UI (toggle Presente/Falta) | Frontend (React) | — | Local state until save |
| Grade table (students × bimesters) | Frontend (React) | — | Local state + inline validation until save |
| Frequencia display (highlights < 75%) | Frontend (React) | — | Pure rendering logic based on API data |
| Auth / route guard | Frontend (React) | API / Backend | Frontend redirects; API enforces with require_role("professor") |

---

## Standard Stack

### Core (all already installed — no new packages needed)

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| FastAPI | >=0.115.0 [VERIFIED: requirements.txt] | Backend router + dependency injection | Project standard |
| SQLAlchemy 2.0 (sync) | >=2.0.0 [VERIFIED: requirements.txt] | ORM + query builder | Project standard — sync specifically to avoid SQLite WAL lock issues |
| Pydantic v2 | bundled with FastAPI | Request/response schema validation | Project standard |
| React 18 + TypeScript | ^19.2.5 (react) [VERIFIED: package.json] | Frontend framework | Note: package.json shows react@^19.2.5 — the runtime is React 19, not 18 |
| TanStack Query | ^5.100.5 [VERIFIED: package.json] | Server state, cache invalidation | Project standard |
| sonner | ^2.0.7 [VERIFIED: package.json] | Toast notifications | Already installed in Phase 3 |
| react-hook-form + zod | ^7.74.0 / ^4.3.6 [VERIFIED: package.json] | Form handling + validation | Already installed in Phase 3 — NOT needed for professor portal (no modals with forms; grade table uses controlled inputs, not RHF) |
| axios | ^1.15.2 [VERIFIED: package.json] | HTTP client | Project standard via `services/api.ts` |
| Tailwind CSS v3 | ^3.4.19 [VERIFIED: package.json] | Styling | Project standard |

### No New Packages Required

The professor portal needs no new npm or pip packages. All required libraries are installed. [VERIFIED: package.json, requirements.txt]

---

## Architecture Patterns

### System Architecture Diagram

```
[Browser: /professor]
        |
  ProtectedRoute (allowedRole="professor")
        |
    AppLayout (no sidebar — header only, pt-16 offset)
        |
  ProfessorLandingPage (/professor)
        |
    GET /professor/minhas-turmas
        |
  [API: professor router]
        |
  professor_turma (WHERE professor_id = current_user.professor.id)
        |--- turmas (join)
        |--- disciplinas (join)
        |--- alunos count (subquery)
        |
  ProfessorTurmaPage (/professor/turmas/:id) [tab state: chamada|notas|frequencia]
        |
        |-- [Chamada tab]
        |     GET /professor/turmas/:id/chamada?date=YYYY-MM-DD
        |         |-- chamadas (WHERE turma_id + data)
        |         |-- presencas (WHERE chamada_id)
        |     POST /professor/turmas/:id/chamada  { date, presencas: [{aluno_id, presente}] }
        |         |-- find-or-create chamada row
        |         |-- delete+insert presencas (replace-all within chamada)
        |
        |-- [Notas tab]
        |     GET /professor/turmas/:id/notas?disciplina_id=X
        |         |-- avaliacoes (WHERE turma_id + disciplina_id, grouped by bimestre)
        |         |-- notas (WHERE avaliacao_id IN (...) + aluno_id)
        |     POST /professor/turmas/:id/notas  { disciplina_id, grades: [{aluno_id, bimestre, valor}] }
        |         |-- find-or-create avaliacao per bimestre
        |         |-- upsert nota per (avaliacao_id, aluno_id)
        |
        |-- [Frequencia tab]
              GET /professor/turmas/:id/frequencia
                  |-- chamadas (WHERE turma_id filtered to professor ownership)
                  |-- presencas (aggregate: COUNT total, COUNT presente per aluno_id)
                  |-- returns: [{aluno_id, nome, total_aulas, total_presentes, percentual}]
```

### Recommended Project Structure

```
backend/src/
├── professor/           # new module (mirrors admin/)
│   ├── __init__.py
│   ├── router.py        # /professor prefix, require_role("professor")
│   ├── service.py       # all business logic
│   └── schemas.py       # Pydantic v2 in/out schemas
├── models/
│   ├── chamada.py       # new ORM model
│   ├── presenca.py      # new ORM model
│   ├── avaliacao.py     # new ORM model
│   └── nota.py          # new ORM model

frontend/src/
├── pages/professor/
│   ├── ProfessorLandingPage.tsx    # /professor — replaces ProfessorDashboard stub
│   └── ProfessorTurmaPage.tsx      # /professor/turmas/:id — tabs
├── components/professor/
│   ├── TurmaCard.tsx
│   ├── AttendanceToggle.tsx
│   ├── GradeTable.tsx
│   ├── FrequencyTable.tsx
│   ├── TabNav.tsx
│   └── Breadcrumb.tsx
```

### Pattern 1: require_role dependency (auth guard)

The professor router uses the identical pattern as admin — a module-level `Depends` applied to every endpoint.

```python
# Source: backend/src/admin/router.py (verified in codebase)
from src.auth.dependencies import require_role
from src.models.usuario import Usuario

router = APIRouter(prefix="/professor", tags=["professor"])
professor_required = Depends(require_role("professor"))

@router.get("/minhas-turmas")
def get_minhas_turmas(
    db: Session = Depends(get_db),
    current_user: Usuario = professor_required,
):
    return service.get_minhas_turmas(db, current_user)
```

### Pattern 2: Resolving professor_id from current_user

The JWT carries `usuario_id` (the `sub` claim). The `professores` table has a `usuario_id` FK. Every professor service function must resolve `professor.id` from `current_user.id`.

```python
# Source: backend/src/admin/service.py pattern + migration 0001 schema (verified)
from src.models.professor import Professor

def _get_professor(db: Session, usuario: Usuario) -> Professor:
    prof = db.query(Professor).filter(Professor.usuario_id == usuario.id).first()
    if not prof:
        raise HTTPException(status_code=404, detail="Perfil de professor não encontrado")
    return prof
```

### Pattern 3: Ownership check on turma access

Every endpoint that takes a `turma_id` path parameter must verify the professor is linked via `professor_turma`.

```python
# Source: database schema (migration 0001, professor_turma table verified)
def _assert_professor_owns_turma(db: Session, professor_id: int, turma_id: int) -> None:
    link = db.query(ProfessorTurma).filter(
        ProfessorTurma.professor_id == professor_id,
        ProfessorTurma.turma_id == turma_id,
    ).first()
    if not link:
        raise HTTPException(status_code=403, detail="Acesso negado a esta turma")
```

### Pattern 4: Chamada upsert (find-or-create + replace presencas)

The `chamadas` table has `(turma_id, disciplina_id, professor_id, data)` — no unique constraint on (turma_id, data) alone. The service must find an existing chamada for (turma_id, disciplina_id, data) owned by the professor, or create one. Then replace all `presencas` for that chamada_id.

```python
# Source: migration 0001 schema (verified), pattern mirrors _sync_professor_turma in admin/service.py
def upsert_chamada(db, professor_id, turma_id, disciplina_id, data, presencas_data):
    chamada = db.query(Chamada).filter(
        Chamada.turma_id == turma_id,
        Chamada.disciplina_id == disciplina_id,
        Chamada.professor_id == professor_id,
        Chamada.data == data,
    ).first()
    if not chamada:
        chamada = Chamada(turma_id=turma_id, disciplina_id=disciplina_id,
                          professor_id=professor_id, data=data)
        db.add(chamada)
        db.flush()
    # Replace-all pattern (same as _sync_professor_turma)
    db.query(Presenca).filter(Presenca.chamada_id == chamada.id).delete(synchronize_session=False)
    for p in presencas_data:
        db.add(Presenca(chamada_id=chamada.id, aluno_id=p.aluno_id, presente=p.presente))
    db.commit()
    return chamada
```

### Pattern 5: Notas upsert (find-or-create avaliacao per bimestre)

The UI sends a flat array of `{aluno_id, bimestre, valor}`. The service finds-or-creates an `avaliacao` for each `(turma_id, disciplina_id, bimestre)` combo, then upserts notas. The `notas` table has a unique constraint on `(avaliacao_id, aluno_id)`.

```python
# Source: migration 0001 schema (verified)
# avaliacao: unique constraint NOT on (turma_id, disciplina_id, bimestre) — no constraint declared
# Therefore service must query first before inserting
def upsert_notas(db, professor_id, turma_id, disciplina_id, grades):
    for grade in grades:
        avaliacao = db.query(Avaliacao).filter(
            Avaliacao.turma_id == turma_id,
            Avaliacao.disciplina_id == disciplina_id,
            Avaliacao.professor_id == professor_id,
            Avaliacao.bimestre == grade.bimestre,
        ).first()
        if not avaliacao:
            avaliacao = Avaliacao(
                turma_id=turma_id, disciplina_id=disciplina_id,
                professor_id=professor_id, bimestre=grade.bimestre,
                titulo=f"{grade.bimestre}o Bimestre", valor_maximo=10.0,
            )
            db.add(avaliacao)
            db.flush()
        # Upsert nota
        nota = db.query(Nota).filter(
            Nota.avaliacao_id == avaliacao.id,
            Nota.aluno_id == grade.aluno_id,
        ).first()
        if nota:
            nota.valor = grade.valor
        else:
            db.add(Nota(avaliacao_id=avaliacao.id, aluno_id=grade.aluno_id, valor=grade.valor))
    db.commit()
```

### Pattern 6: TanStack Query mutation with toast — AlunosPage pattern

```typescript
// Source: frontend/src/pages/admin/AlunosPage.tsx (verified in codebase)
function useSaveChamada() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (body: ChamadaPayload) =>
      api.post(`/professor/turmas/${body.turma_id}/chamada`, body).then((r) => r.data),
    onSuccess: async () => {
      await qc.invalidateQueries({ queryKey: ['chamada', turmaId] })
      toast.success('Chamada salva com sucesso.')
    },
    onError: () => toast.error('Erro ao salvar chamada. Tente novamente.'),
  })
}
```

### Pattern 7: Route structure for professor portal

The professor routes in App.tsx already have `ProtectedRoute allowedRole="professor"` wrapping `AppLayout`. Phase 4 replaces the `ProfessorDashboard` stub with real pages and adds a nested `:id` route.

```typescript
// Source: frontend/src/App.tsx (verified in codebase) — current structure:
{
  path: '/professor',
  element: <ProtectedRoute allowedRole="professor" />,
  children: [
    {
      element: <AppLayout />,
      children: [{ index: true, element: <ProfessorDashboard /> }],
    },
  ],
}

// Phase 4 extension — add turma detail route:
children: [
  { index: true, element: <ProfessorLandingPage /> },         // replaces stub
  { path: 'turmas/:id', element: <ProfessorTurmaPage /> },    // new
],
```

### Anti-Patterns to Avoid

- **Lazy ownership check:** Never rely only on the frontend to filter turmas — the `/professor/turmas/:id` endpoint MUST check `professor_turma` FK or a URL-direct access bypasses PROF-02.
- **Avaliacao duplication:** Never insert a new `avaliacao` without querying first — there is no unique constraint on (turma_id, disciplina_id, bimestre), so duplicates silently accumulate if you always insert.
- **React Hook Form for grade table:** The grade table is a controlled-input grid, not a traditional form. Use React state (`useState` with a map of `{aluno_id, bimestre} -> value`) rather than RHF — RHF's register pattern does not compose well with dynamically keyed table cells.
- **Direct `db.delete()` on presencas:** Use `db.query(Presenca).filter(...).delete(synchronize_session=False)` for the replace-all — identical to how `_sync_professor_turma` works in admin service.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Toast notifications | Custom toast component | `sonner` (already installed) | Already used in all admin pages; consistent UX |
| Auth guard for professor routes | Custom role check component | `ProtectedRoute` (already exists) | Phase 3 component handles it exactly; just pass `allowedRole="professor"` |
| Modal component | New modal | `Modal.tsx` from admin components | Already built, portal-based, ESC/backdrop close — UI-SPEC explicitly says reuse it |
| ConfirmDialog | New confirm UI | `ConfirmDialog.tsx` from admin components | UI-SPEC says reuse for overwrite-attendance confirmation |
| Percentage calculation client-side | JS map/reduce over presencas | Backend aggregation endpoint | Avoids N+1 data fetching; frequency tab is read-only display |
| Tab state management | URL params or router state | Local `useState` in `ProfessorTurmaPage` | Tabs are UI state only, no deep-link requirement in CONTEXT.md |

---

## Critical Schema Facts

### Tables That Already Exist (migration 0001) [VERIFIED: codebase]

**`chamadas`** — one row per "attendance session":
- `id`, `turma_id` (FK turmas), `disciplina_id` (FK disciplinas), `professor_id` (FK professores), `data` (Date), `criado_em`
- Indexes: `ix_chamadas_turma_id`, `ix_chamadas_data`
- No unique constraint on (turma_id, disciplina_id, data) — service must query-first to avoid duplicates

**`presencas`** — one row per student per chamada:
- `id`, `chamada_id` (FK chamadas CASCADE), `aluno_id` (FK alunos CASCADE), `presente` (Boolean), `justificativa` (nullable)
- Unique constraint: `(chamada_id, aluno_id)` — enforces one record per student per session
- Indexes: `ix_presencas_chamada_id`, `ix_presencas_aluno_id`

**`avaliacoes`** — defines an evaluation context per turma/disciplina/bimestre:
- `id`, `turma_id`, `disciplina_id`, `professor_id`, `titulo` (String 255), `bimestre` (Integer 1-4), `valor_maximo` (Float, default 10.0), `data` (nullable)
- Check constraints: `bimestre IN (1,2,3,4)`, `valor_maximo > 0`
- Indexes: `ix_avaliacoes_turma_id`, `ix_avaliacoes_bimestre`
- No unique constraint on (turma_id, disciplina_id, bimestre) — service must find-or-create

**`notas`** — grade per student per avaliacao:
- `id`, `avaliacao_id` (FK avaliacoes CASCADE), `aluno_id` (FK alunos CASCADE), `valor` (Float), `criado_em`
- Unique constraint: `(avaliacao_id, aluno_id)` — enforces one grade per student per evaluation
- Indexes: `ix_notas_avaliacao_id`, `ix_notas_aluno_id`

**`professor_turma`** — ownership junction:
- Composite PK: `(professor_id, turma_id, disciplina_id)` — a professor can be linked to the same turma for multiple disciplines
- Index: `ix_professor_turma_professor_id`
- Implication for Notas tab: if a professor teaches two disciplines in the same turma, the UI must show a discipline selector (confirmed in UI-SPEC screen contract section 4)

### ORM Models That Do NOT Exist Yet [VERIFIED: codebase ls]

Files missing from `backend/src/models/`: `chamada.py`, `presenca.py`, `avaliacao.py`, `nota.py`

These four ORM model files must be created in Wave 0 / Plan 1 of Phase 4.

---

## Common Pitfalls

### Pitfall 1: professor_id Resolution
**What goes wrong:** Endpoints receive `current_user` (a `Usuario` row), but `chamadas`, `presencas`, and `avaliacoes` all require `professores.id` (not `usuarios.id`).
**Why it happens:** The auth dependency returns `Usuario`, not `Professor`. The two IDs are different (separate tables with separate auto-increment PKs).
**How to avoid:** Every service function resolves `professor = db.query(Professor).filter(Professor.usuario_id == current_user.id).first()` before any business logic. Create a `_get_professor()` helper reused across all service functions.
**Warning signs:** 500 errors on FKs if you accidentally pass `usuario.id` where `professor_id` is expected.

### Pitfall 2: Duplicate Avaliacoes
**What goes wrong:** Calling "save notas" multiple times creates duplicate `avaliacao` rows for the same (turma, disciplina, bimestre) combination, producing a duplicated grade history.
**Why it happens:** Unlike `presencas`, the `avaliacoes` table has NO unique constraint on (turma_id, disciplina_id, bimestre). SQLAlchemy will happily insert duplicates.
**How to avoid:** Always `db.query(Avaliacao).filter(...).first()` before inserting; only insert if result is None.
**Warning signs:** Growing duplicate rows in `avaliacoes`; frequencia tab showing unexpected counts.

### Pitfall 3: Ownership Bypass via Direct URL
**What goes wrong:** A professor accesses `/professor/turmas/99` where turma 99 belongs to another professor — they can read students and submit grades.
**Why it happens:** If the ownership check only filters the landing page list, turma detail page endpoints are unprotected.
**How to avoid:** `_assert_professor_owns_turma(db, professor_id, turma_id)` called at the start of every endpoint that receives a `turma_id` path parameter.
**Warning signs:** PROF-02 test fails if ownership check is missing.

### Pitfall 4: Grade Table as React Hook Form
**What goes wrong:** Using `useForm` + `register` for the grade table results in dynamic field names and complex RHF array logic; validation errors are difficult to target to specific cells.
**Why it happens:** RHF is the project standard for forms (admin modals), so it might be reflexively applied.
**How to avoid:** Use a `Map<string, string>` state keyed by `${aluno_id}-${bimestre}` for cell values; validate inline on `onChange`. Save collects state and transforms to API payload.
**Warning signs:** Complex RHF field array setup for a 2D table is a clear signal to use plain state.

### Pitfall 5: Frequency Calculation in Frontend
**What goes wrong:** Fetching all chamadas+presencas for a turma client-side and calculating percentages in JavaScript — this fetches unbounded data and breaks for large classes with long attendance history.
**Why it happens:** Simpler to get all data and compute in React.
**How to avoid:** The `/professor/turmas/:id/frequencia` endpoint returns pre-aggregated data: `{aluno_id, nome, total_aulas, total_presentes, percentual}`. The frontend only renders.
**Warning signs:** useQuery fetching full chamadas list instead of a dedicated aggregation endpoint.

### Pitfall 6: React 19 vs React 18 Imports
**What goes wrong:** Code examples using React 18 patterns (e.g., `import React from 'react'` for JSX) may produce lint warnings since the project runs React 19.
**Why it happens:** package.json shows `react@^19.2.5` — not 18 as stated in the tech stack summary.
**How to avoid:** Use React 19 patterns already established in the codebase (no explicit React import needed; functional components only; no class components).
**Warning signs:** TypeScript errors on React types if using @types/react v18 patterns — but @types/react is already at v19 in devDependencies.

---

## Code Examples

### New ORM Models (to be created)

```python
# backend/src/models/chamada.py
# Source: migration 0001 schema (verified in codebase)
from datetime import date
from sqlalchemy import Date, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from src.database import Base

class Chamada(Base):
    __tablename__ = "chamadas"
    id: Mapped[int] = mapped_column(primary_key=True)
    turma_id: Mapped[int] = mapped_column(ForeignKey("turmas.id", ondelete="CASCADE"))
    disciplina_id: Mapped[int] = mapped_column(ForeignKey("disciplinas.id", ondelete="CASCADE"))
    professor_id: Mapped[int] = mapped_column(ForeignKey("professores.id", ondelete="CASCADE"))
    data: Mapped[date] = mapped_column(Date, nullable=False)
```

```python
# backend/src/models/presenca.py
# Source: migration 0001 schema (verified in codebase)
from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base

class Presenca(Base):
    __tablename__ = "presencas"
    __table_args__ = (UniqueConstraint("chamada_id", "aluno_id", name="uq_presencas_chamada_id_aluno_id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    chamada_id: Mapped[int] = mapped_column(ForeignKey("chamadas.id", ondelete="CASCADE"))
    aluno_id: Mapped[int] = mapped_column(ForeignKey("alunos.id", ondelete="CASCADE"))
    presente: Mapped[bool] = mapped_column(Boolean, nullable=False)
    justificativa: Mapped[str | None] = mapped_column(String(500), nullable=True)
```

```python
# backend/src/models/avaliacao.py
# Source: migration 0001 schema (verified in codebase)
from datetime import date
from sqlalchemy import CheckConstraint, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base

class Avaliacao(Base):
    __tablename__ = "avaliacoes"
    __table_args__ = (
        CheckConstraint("bimestre IN (1, 2, 3, 4)", name="ck_avaliacoes_bimestre"),
        CheckConstraint("valor_maximo > 0", name="ck_avaliacoes_valor_maximo"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    turma_id: Mapped[int] = mapped_column(ForeignKey("turmas.id", ondelete="CASCADE"))
    disciplina_id: Mapped[int] = mapped_column(ForeignKey("disciplinas.id", ondelete="CASCADE"))
    professor_id: Mapped[int] = mapped_column(ForeignKey("professores.id", ondelete="CASCADE"))
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    bimestre: Mapped[int] = mapped_column(Integer, nullable=False)
    valor_maximo: Mapped[float] = mapped_column(Float, nullable=False, default=10.0)
    data: Mapped[date | None] = mapped_column(Date, nullable=True)
```

```python
# backend/src/models/nota.py
# Source: migration 0001 schema (verified in codebase)
from sqlalchemy import Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base

class Nota(Base):
    __tablename__ = "notas"
    __table_args__ = (UniqueConstraint("avaliacao_id", "aluno_id", name="uq_notas_avaliacao_id_aluno_id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    avaliacao_id: Mapped[int] = mapped_column(ForeignKey("avaliacoes.id", ondelete="CASCADE"))
    aluno_id: Mapped[int] = mapped_column(ForeignKey("alunos.id", ondelete="CASCADE"))
    valor: Mapped[float] = mapped_column(Float, nullable=False)
```

### AttendanceToggle Component

```tsx
// Source: UI-SPEC screen contract section 3 (verified in 04-UI-SPEC.md)
interface AttendanceToggleProps {
  presente: boolean
  onChange: (presente: boolean) => void
}

function AttendanceToggle({ presente, onChange }: AttendanceToggleProps) {
  return (
    <div className="flex rounded-md shadow-sm" role="group">
      <button
        type="button"
        aria-pressed={presente}
        onClick={() => onChange(true)}
        className={`px-3 py-1 text-xs font-medium rounded-l-md border ${
          presente
            ? 'bg-green-100 text-green-800 border-green-200'
            : 'bg-white text-gray-500 border-gray-300 hover:bg-gray-50'
        }`}
      >
        Presente
      </button>
      <button
        type="button"
        aria-pressed={!presente}
        onClick={() => onChange(false)}
        className={`px-3 py-1 text-xs font-medium rounded-r-md border -ml-px ${
          !presente
            ? 'bg-red-100 text-red-800 border-red-200'
            : 'bg-white text-gray-500 border-gray-300 hover:bg-gray-50'
        }`}
      >
        Falta
      </button>
    </div>
  )
}
```

### TabNav Component

```tsx
// Source: UI-SPEC screen contract section 2 (verified in 04-UI-SPEC.md)
type Tab = 'chamada' | 'notas' | 'frequencia'

interface TabNavProps {
  active: Tab
  onChange: (tab: Tab) => void
}

function TabNav({ active, onChange }: TabNavProps) {
  const tabs: { key: Tab; label: string }[] = [
    { key: 'chamada', label: 'Chamada' },
    { key: 'notas', label: 'Notas' },
    { key: 'frequencia', label: 'Frequencia' },
  ]
  return (
    <div className="border-b border-gray-200 mb-6" role="tablist">
      <div className="flex gap-6">
        {tabs.map((t) => (
          <button
            key={t.key}
            role="tab"
            aria-selected={active === t.key}
            onClick={() => onChange(t.key)}
            className={`px-1 py-3 text-sm font-medium border-b-2 ${
              active === t.key
                ? 'text-indigo-600 border-indigo-600'
                : 'text-gray-500 hover:text-gray-700 border-transparent'
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>
    </div>
  )
}
```

### Frequency Row Background Logic

```tsx
// Source: UI-SPEC screen contract section 5 (verified in 04-UI-SPEC.md)
// Row class: bg-red-50 when below 75%, standard otherwise
const rowClass = percentual < 75 ? 'bg-red-50 hover:bg-red-100' : 'hover:bg-gray-50'
const percentClass = percentual < 75 ? 'text-red-700' : 'text-gray-700'
```

---

## State of the Art

| Old Approach | Current Approach | Notes |
|--------------|------------------|-------|
| Class components | Functional components + hooks | React 19 — codebase uses this already |
| Context for server state | TanStack Query v5 | Codebase uses this already |
| `useQuery` result `.isLoading` | `.isLoading` still valid in TQ v5 | No change needed |
| `keepPreviousData: true` option | `placeholderData: keepPreviousData` import | Already used in AlunosPage — follow same pattern |

---

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | The `avaliacao` auto-title for the grade table can be `"Xo Bimestre"` (e.g., "1o Bimestre") when created by the professor portal | Architecture Patterns — Notas upsert | Low — titulo is required by schema but not displayed in the professor portal UI; Phase 5 (responsavel) renders it to parents, so any string is acceptable for the prototype |
| A2 | Frequencia aggregation covers "ano letivo completo" (all chamadas for the turma, no date filter) | Architecture Patterns — system diagram | Medium — CONTEXT.md says "probably ano letivo for prototype simplicity" (Claude's Discretion) — if the user wants bimestre filter, a `?bimestre=` query param can be added later without breaking the endpoint |

---

## Open Questions (RESOLVED)

1. **Disciplina selector in Notas tab**
   - What we know: A professor can be linked to the same turma for multiple disciplinas (professor_turma composite PK includes disciplina_id). The UI-SPEC says show a disciplina selector if multiple exist.
   - What's unclear: The GET endpoint for notas needs `disciplina_id` — what does the API return when no disciplina is selected? Probably nothing until selection is made.
   - Recommendation: The Notas tab should initialize with the first disciplina in the list automatically (if only one, no selector needed; if multiple, show select).
   - RESOLVED: Plan 04-03 Task 2 implements this — first disciplina auto-selected, selector shown when professor teaches multiple disciplines in the turma.

2. **Chamada and disciplina_id**
   - What we know: `chamadas` table requires `disciplina_id` — a chamada is per turma+disciplina+date.
   - What's unclear: The Chamada tab in CONTEXT.md doesn't mention choosing a disciplina before taking attendance. If a professor teaches two disciplines in the same turma, there would be two separate chamadas per day.
   - Recommendation: Mirror the Notas tab behavior — show a disciplina selector in the Chamada tab when the professor teaches multiple disciplines in the turma.
   - RESOLVED: Plan 04-03 Task 2 mirrors the Notas tab pattern — disciplina selector in Chamada tab when multiple disciplinas exist; defaults to first disciplina when only one.

---

## Environment Availability

Step 2.6: SKIPPED — no new external dependencies. All required tools (Python, Node, pytest, npm) were confirmed operational in Phase 3.

---

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest 8.x [VERIFIED: requirements.txt] |
| Config file | none — pytest discovers `tests/` automatically |
| Quick run command | `cd backend && python -m pytest tests/test_professor.py -x -q` |
| Full suite command | `cd backend && python -m pytest tests/ -q` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| PROF-01 | POST chamada creates chamada + presencas rows | unit | `pytest tests/test_professor.py::test_create_chamada -x` | ❌ Wave 0 |
| PROF-02 | GET minhas-turmas only returns linked turmas; direct URL to unlinked turma returns 403 | unit | `pytest tests/test_professor.py::test_ownership_check -x` | ❌ Wave 0 |
| PROF-03 | POST notas creates/updates avaliacoes and notas rows | unit | `pytest tests/test_professor.py::test_upsert_notas -x` | ❌ Wave 0 |
| PROF-04 | POST chamada over existing date replaces presencas; POST notas over existing values updates them | unit | `pytest tests/test_professor.py::test_edit_chamada_and_notas -x` | ❌ Wave 0 |
| PROF-05 | GET frequencia returns correct percentual per aluno | unit | `pytest tests/test_professor.py::test_frequencia_aggregation -x` | ❌ Wave 0 |
| AUTH | Unauthenticated → 401; admin/responsavel → 403 | unit | `pytest tests/test_professor.py::test_access_control -x` | ❌ Wave 0 |

### Sampling Rate

- **Per task commit:** `cd backend && python -m pytest tests/test_professor.py -x -q`
- **Per wave merge:** `cd backend && python -m pytest tests/ -q`
- **Phase gate:** Full suite (all tests including Phase 3 tests) green before `/gsd-verify-work`

### Wave 0 Gaps

- [ ] `backend/tests/test_professor.py` — covers PROF-01 through PROF-05 + access control
- [ ] `backend/src/models/chamada.py` — ORM model (required for tests to import)
- [ ] `backend/src/models/presenca.py` — ORM model (required for tests to import)
- [ ] `backend/src/models/avaliacao.py` — ORM model (required for tests to import)
- [ ] `backend/src/models/nota.py` — ORM model (required for tests to import)
- [ ] `backend/src/professor/__init__.py` — module package
- [ ] `backend/src/professor/router.py` — routes under `/professor`
- [ ] `backend/src/professor/service.py` — business logic
- [ ] `backend/src/professor/schemas.py` — Pydantic schemas

The conftest.py fixtures (`test_db`, `client`, `professor_headers`) already exist and work for professor-role JWT — no conftest changes needed. [VERIFIED: backend/tests/conftest.py]

---

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | yes | JWT via existing `require_role("professor")` — no new auth code needed |
| V3 Session Management | no | Handled by Phase 2; no session changes in Phase 4 |
| V4 Access Control | yes | `_assert_professor_owns_turma()` on every turma-specific endpoint; professor_turma FK check |
| V5 Input Validation | yes | Pydantic v2 schemas on all POST bodies; `bimestre IN (1,2,3,4)` check constraint in DB; `valor` range 0–10 enforced in service layer |
| V6 Cryptography | no | No new crypto; existing JWT signing is unchanged |

### Known Threat Patterns for This Stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Insecure Direct Object Reference (turma_id in URL) | Elevation of Privilege | `_assert_professor_owns_turma()` at every endpoint start |
| Grade injection (valor outside 0–10) | Tampering | Service layer validates `0 <= valor <= avaliacao.valor_maximo` before insert; backend rejects, not just frontend |
| JWT impersonation (professor using admin token) | Spoofing | `require_role("professor")` dependency enforced on every professor endpoint |
| Bulk presencas replace without ownership | Tampering | Ownership check before replace-all — can't replace presencas for a turma you don't own |

---

## Sources

### Primary (HIGH confidence)

- Codebase: `backend/alembic/versions/0001_initial_schema.py` — complete DB schema, all 11 tables
- Codebase: `backend/src/admin/router.py`, `service.py`, `schemas.py` — module pattern to mirror
- Codebase: `backend/src/auth/dependencies.py` — `require_role` and `get_current_user` patterns
- Codebase: `backend/src/models/professor.py`, `professor_turma.py`, `aluno.py`, `turma.py` — ORM model patterns
- Codebase: `frontend/src/App.tsx` — existing routing structure for professor portal
- Codebase: `frontend/src/components/AppLayout.tsx` — shared layout (no sidebar for professor)
- Codebase: `frontend/src/pages/admin/AlunosPage.tsx` — TanStack Query mutation + toast pattern
- Codebase: `frontend/src/components/admin/Modal.tsx`, `EntityTable.tsx` — reusable component patterns
- Codebase: `frontend/package.json`, `backend/requirements.txt` — installed package versions
- Codebase: `.planning/phases/04-portal-do-professor/04-UI-SPEC.md` — screen contracts and component specs
- Codebase: `backend/tests/conftest.py` — existing test fixture patterns

### Secondary (MEDIUM confidence)

None needed — all required facts are directly verified in the codebase.

---

## Metadata

**Confidence breakdown:**

- Standard stack: HIGH — verified against package.json and requirements.txt
- Database schema: HIGH — verified line-by-line in migration 0001
- Architecture patterns: HIGH — derived directly from existing codebase (admin module is the template)
- Component patterns: HIGH — verified in AppLayout, Modal, EntityTable, AlunosPage source
- Pitfalls: HIGH — derived from schema constraints (no unique on avaliacoes) and auth model (usuario_id vs professor_id)
- Test patterns: HIGH — conftest.py verified; test file doesn't exist yet (wave 0 gap)

**Research date:** 2026-04-27
**Valid until:** 2026-05-27 (stable schema; no external dependencies to change)
