---
phase: 04-portal-do-professor
reviewed: 2026-04-29T03:00:00Z
depth: standard
files_reviewed: 19
files_reviewed_list:
  - backend/src/main.py
  - backend/src/models/__init__.py
  - backend/src/models/avaliacao.py
  - backend/src/models/chamada.py
  - backend/src/models/nota.py
  - backend/src/models/presenca.py
  - backend/src/professor/__init__.py
  - backend/src/professor/router.py
  - backend/src/professor/schemas.py
  - backend/src/professor/service.py
  - backend/tests/test_professor.py
  - frontend/src/App.tsx
  - frontend/src/components/professor/AttendanceToggle.tsx
  - frontend/src/components/professor/FrequencyTable.tsx
  - frontend/src/components/professor/GradeTable.tsx
  - frontend/src/components/professor/TabNav.tsx
  - frontend/src/components/professor/TurmaCard.tsx
  - frontend/src/pages/professor/ProfessorLandingPage.tsx
  - frontend/src/pages/professor/ProfessorTurmaPage.tsx
findings:
  critical: 3
  warning: 6
  info: 2
  total: 11
status: issues_found
---

# Phase 04: Portal do Professor — Code Review Report

**Reviewed:** 2026-04-29T03:00:00Z
**Depth:** standard
**Files Reviewed:** 19
**Status:** issues_found

## Summary

This phase introduces the professor portal with backend endpoints for attendance (chamada), grades (notas), and frequency (frequencia), plus corresponding React frontend components. The implementation follows the established patterns (SQLAlchemy ORM, FastAPI routers, TanStack Query, Tailwind) and has good test coverage.

However, three **BLOCKER** issues were found:

1. **Ambiguous chamada retrieval**: `GET /professor/turmas/{id}/chamada` does not accept or filter by `disciplina_id`. Since `Chamada` is stored per `(turma, disciplina, professor, date)`, the endpoint returns a non-deterministic record when a professor teaches multiple disciplines in the same turma, causing the frontend to display and potentially overwrite the wrong attendance data.

2. **Attendance state corruption on edit**: The `effectivePresencas` computed value in `ProfessorTurmaPage.tsx` returns only the delta state when any student is toggled. All non-toggled students default to `true` (Presente) in the UI, **losing their previously loaded server state**.

3. **Missing discipline-level authorization**: `_assert_professor_owns_turma` only verifies `(professor, turma)` linkage, not `(professor, turma, disciplina)`. A professor who teaches Math in a turma can create/update Chamada and Avaliacao records for Physics in the same turma via direct API calls.

Additionally, several **WARNING** issues affect robustness and type safety, including unvalidated date parsing causing 500 errors, missing `aluno_id` ownership validation in write endpoints, UTC-vs-local date bugs in the frontend, missing TypeScript generics, and background refetch overwriting unsaved user edits.

---

## Critical Issues

### CR-01: `get_chamada` lacks discipline filter, returns arbitrary record for multi-discipline turmas

**File:** `backend/src/professor/service.py:150–166`, `backend/src/professor/router.py:46–53`
**Issue:** The `GET /professor/turmas/{turma_id}/chamada` endpoint accepts `date` but not `disciplina_id`. The `Chamada` table stores one row per `(turma_id, disciplina_id, professor_id, data)`. When a professor teaches multiple disciplines in the same turma, `service.get_chamada` queries `.filter(Chamada.turma_id == turma_id, Chamada.professor_id == prof.id, Chamada.data == target_date).first()` — this is **non-deterministic** because multiple rows can match. The frontend (`useChamada`) calls this without discipline, so the user may see the wrong attendance data and unknowingly overwrite a different discipline's chamada when saving.
**Fix:**
- Add `disciplina_id: int = Query(...)` to the `get_chamada` router endpoint.
- Pass `disciplina_id` to `service.get_chamada` and add `Chamada.disciplina_id == disciplina_id` to the query filter.
- Update the frontend `useChamada` hook to include `effectiveDisciplinaId` in the query key and API call.

```python
# backend/src/professor/router.py
@router.get("/turmas/{turma_id}/chamada")
def get_chamada(
    turma_id: int,
    date: str = Query(...),
    disciplina_id: int = Query(...),  # add this
    db: Session = Depends(get_db),
    current_user: Usuario = professor_required,
):
    return service.get_chamada(db, current_user, turma_id, date, disciplina_id)
```

```typescript
// frontend/src/pages/professor/ProfessorTurmaPage.tsx
function useChamada(turmaId: number, dateStr: string, disciplinaId: number) {
  return useQuery<ChamadaData>({
    queryKey: ['chamada', turmaId, dateStr, disciplinaId],
    queryFn: () =>
      api.get(`/professor/turmas/${turmaId}/chamada?date=${dateStr}&disciplina_id=${disciplinaId}`).then((r) => r.data),
    enabled: disciplinaId > 0,
  })
}
```

---

### CR-02: `effectivePresencas` loses loaded server state on user edit

**File:** `frontend/src/pages/professor/ProfessorTurmaPage.tsx:117–132`
**Issue:** The `effectivePresencas` IIFE returns the raw `presencas` delta state when `Object.keys(presencas).length > 0`. This means after the user toggles even a single student, all other students disappear from the map and the UI defaults them to `true` via `effectivePresencas[aluno.id] ?? true`. For example, if the server loaded Student 1 as absent (`false`) and Student 2 as present (`true`), and the user toggles Student 2 to absent, Student 1 will erroneously display as present on the next render because `presencas` only contains `{2: false}`.
**Fix:** Always build the base state from `chamadaData` or `alunos`, then merge user edits on top. Remove the early `return presencas` guard.

```typescript
const effectivePresencas: Record<number, boolean> = (() => {
  const base: Record<number, boolean> = {}
  if (chamadaData?.presencas?.length > 0) {
    for (const p of chamadaData.presencas) {
      base[p.aluno_id] = p.presente
    }
  } else {
    for (const a of alunos ?? []) {
      base[a.id] = true
    }
  }
  // Merge user edits on top of loaded state
  for (const [alunoId, presente] of Object.entries(presencas)) {
    base[Number(alunoId)] = presente
  }
  return base
})()
```

---

### CR-03: Missing discipline-level authorization in write endpoints

**File:** `backend/src/professor/service.py:37–44`, `backend/src/professor/router.py:56–83`
**Issue:** `_assert_professor_owns_turma` validates only that the professor is linked to the turma via `ProfessorTurma`, but it does **not** check that the professor is linked to the specific `disciplina_id` in the payload. The `ProfessorTurma` composite primary key is `(professor_id, turma_id, disciplina_id)`, explicitly modeling per-discipline assignments. A professor who teaches Math in Turma 1 can send a crafted request with `disciplina_id=<physics_id>` to create/update Chamada or Avaliacao/Nota records for Physics, polluting the database with unauthorized discipline records.
**Fix:** Add a discipline ownership check and call it in `upsert_chamada`, `get_notas`, `upsert_notas`, and `get_chamada` (after adding discipline to that endpoint).

```python
# backend/src/professor/service.py
def _assert_professor_owns_disciplina(db: Session, professor_id: int, turma_id: int, disciplina_id: int) -> None:
    link = db.query(ProfessorTurma).filter(
        ProfessorTurma.professor_id == professor_id,
        ProfessorTurma.turma_id == turma_id,
        ProfessorTurma.disciplina_id == disciplina_id,
    ).first()
    if not link:
        raise HTTPException(status_code=403, detail="Acesso negado a esta disciplina")

# Then call it in upsert_chamada, upsert_notas, get_notas, get_chamada
_assert_professor_owns_turma(db, prof.id, turma_id)
_assert_professor_owns_disciplina(db, prof.id, turma_id, payload.disciplina_id)
```

---

## Warnings

### WR-01: Malformed date string causes HTTP 500 instead of 422

**File:** `backend/src/professor/service.py:153`
**Issue:** `get_chamada` calls `datetime.strptime(date_str, "%Y-%m-%d").date()` directly. If `date_str` is malformed (e.g., `"2024-13-01"` or `"not-a-date"`), `strptime` raises `ValueError`, which FastAPI turns into an unhandled 500 error. The router parameter is typed as `str = Query(...)` with no Pydantic `date` validation.
**Fix:** Change the router parameter to `date: date = Query(...)` (Pydantic will validate the format and return 422), or wrap `strptime` in a try/except and raise `HTTPException(status_code=422, detail="...")`.

```python
# backend/src/professor/router.py
from datetime import date

@router.get("/turmas/{turma_id}/chamada")
def get_chamada(
    turma_id: int,
    date: date = Query(...),  # Pydantic validates format
    ...
):
    return service.get_chamada(db, current_user, turma_id, date)
```

---

### WR-02: Write endpoints don't validate that `aluno_id`s belong to the turma

**File:** `backend/src/professor/service.py:169–192`, `218–254`
**Issue:** `upsert_chamada` and `upsert_notas` iterate over `payload.presencas` / `payload.grades` and use the provided `aluno_id`s directly without verifying that those students are actually enrolled in `turma_id`. A malicious professor could post attendance or grades for students from other turmas. The foreign key constraint on `alunos.id` will not prevent this because the student exists, just in the wrong turma.
**Fix:** Before processing, query the active alunos for the turma and reject any `aluno_id` not in the allowed set.

```python
allowed_aluno_ids = {
    a.id for a in db.query(Aluno).filter(Aluno.turma_id == turma_id, Aluno.ativo == True).all()
}
for p in payload.presencas:
    if p.aluno_id not in allowed_aluno_ids:
        raise HTTPException(status_code=422, detail=f"Aluno {p.aluno_id} nao pertence a esta turma")
```

---

### WR-03: Frontend default date uses UTC instead of local timezone

**File:** `frontend/src/pages/professor/ProfessorTurmaPage.tsx:94–96`
**Issue:** `new Date().toISOString().split('T')[0]` produces the **UTC** date. In timezones west of UTC (e.g., Brazil UTC-3), during evening hours the displayed default date can be one day ahead of the actual local date, causing professors to record attendance for the wrong day.
**Fix:** Use a local-timezone date formatter.

```typescript
const [selectedDate, setSelectedDate] = useState<string>(
  new Date().toLocaleDateString('en-CA') // YYYY-MM-DD in local time
)
```

---

### WR-04: Missing TypeScript generics on `useQuery` hooks

**File:** `frontend/src/components/professor/GradeTable.tsx:15–20`, `frontend/src/pages/professor/ProfessorTurmaPage.tsx:66–72`
**Issue:** `useQuery` is called without generic type parameters, so `notasData` and `chamadaData` are inferred as `unknown` (or `any` depending on tsconfig). This bypasses compile-time type safety and forces explicit `unknown` annotations in callback signatures (e.g., `(_: unknown, idx: number)`). In strict TypeScript projects, this is a type-safety regression.
**Fix:** Add explicit generics to `useQuery` calls.

```typescript
// GradeTable.tsx
interface NotasData {
  aluno_id: number
  nome: string
  notas: { bimestre: number; valor: number }[]
}

const { data: notasData, isLoading } = useQuery<NotasData[]>({...})

// ProfessorTurmaPage.tsx
interface ChamadaData {
  id: number | null
  data: string
  presencas: { aluno_id: number; presente: boolean }[]
}

function useChamada(turmaId: number, dateStr: string) {
  return useQuery<ChamadaData>({...})
}
```

---

### WR-05: Background refetch overwrites unsaved grade edits

**File:** `frontend/src/components/professor/GradeTable.tsx:23–32`
**Issue:** The `useEffect` that populates `grades` from `notasData` has no guard against overwriting user edits. If React Query refetches in the background (window focus, network reconnect, stale-while-revalidate), `notasData` updates, the effect fires, and any unsaved values the user typed are lost.
**Fix:** Only initialize `grades` once per `disciplinaId` change, or use a ref to track whether initialization has occurred. Alternatively, use `keepPreviousData: true` and only reset when `disciplinaId` changes.

```typescript
useEffect(() => {
  if (!notasData) return
  const initial: Record<string, string> = {}
  for (const row of notasData) {
    for (const n of row.notas ?? []) {
      initial[`${row.aluno_id}-${n.bimestre}`] = String(n.valor)
    }
  }
  setGrades(initial)
}, [disciplinaId]) // only reset when discipline changes, not on every data update
```

---

### WR-06: No database unique constraints on Chamada / Avaliacao composite keys

**File:** `backend/src/models/chamada.py:7–14`, `backend/src/models/avaliacao.py:6–19`
**Issue:** Neither `Chamada` nor `Avaliacao` defines a `UniqueConstraint` on their natural composite keys (`(turma_id, disciplina_id, professor_id, data)` and `(turma_id, disciplina_id, professor_id, bimestre)`). Race conditions in `upsert_chamada` and `upsert_notas` can create duplicate rows because the Python-level `.first()` + `if not:` pattern is not atomic. Duplicate Chamada rows cause `get_chamada` to behave non-deterministically; duplicate Avaliacao rows break the nota upsert logic.
**Fix:** Add `__table_args__` with unique constraints.

```python
# chamada.py
__table_args__ = (
    UniqueConstraint("turma_id", "disciplina_id", "professor_id", "data", name="uq_chamadas_turma_disc_prof_data"),
)

# avaliacao.py
__table_args__ = (
    CheckConstraint("bimestre IN (1, 2, 3, 4)", name="ck_avaliacoes_bimestre"),
    CheckConstraint("valor_maximo > 0", name="ck_avaliacoes_valor_maximo"),
    UniqueConstraint("turma_id", "disciplina_id", "professor_id", "bimestre", name="uq_avaliacoes_turma_disc_prof_bimestre"),
)
```

---

## Info

### IN-01: Unused Pydantic schema classes

**File:** `backend/src/professor/schemas.py:39–44`, `57–67`
**Issue:** `ChamadaOut`, `PresencaOut`, `NotasOut`, and `NoteOut` are defined but never referenced as `response_model` in `router.py`. `get_chamada`, `upsert_chamada`, `get_notas`, and `upsert_notas` all return raw dicts without response models. This dead code should either be wired up or removed to reduce maintenance surface.
**Fix:** Either attach `response_model=...` to the relevant router endpoints, or delete the unused classes.

---

### IN-02: Inconsistent `model_config` on `NotasOut`

**File:** `backend/src/professor/schemas.py:63–66`
**Issue:** `NotasOut` is the only `*Out` schema that omits `model_config = ConfigDict(from_attributes=True)`. If it is ever used to wrap SQLAlchemy objects directly (e.g., as a response model), Pydantic v2 will raise validation errors. Since it is currently unused (see IN-01), this is low priority but inconsistent with the established pattern.
**Fix:** Add `model_config = ConfigDict(from_attributes=True)` to `NotasOut` for consistency, or remove the class entirely if it remains unused.

---

_Reviewed: 2026-04-29T03:00:00Z_  
_Reviewer: gsd-code-reviewer_  
_Depth: standard_
