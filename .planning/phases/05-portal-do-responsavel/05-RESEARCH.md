# Phase 5: Portal do Responsável — Research

**Researched:** 2026-04-27
**Domain:** FastAPI read-only service layer + React data-display page
**Confidence:** HIGH — all findings verified against codebase; no new libraries or external services needed

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- Layout: tabela clássica — disciplinas nas linhas, bimestres nas colunas; coluna de média calculada automaticamente na mesma linha
- Frequência: exibida por disciplina (não percentual geral único); mesmo linha do boletim; formato "82% (15/18)"
- Alertas: frequência < 75% → linha/célula em vermelho (bg-red-50 / text-red-700); badge colorido por linha (Aprovado/Reprovado)
- Regra de aprovação: média >= 5.0 **E** frequência >= 75% (regra LDB completa)
- Resumo geral no topo: card indicando "X disciplina(s) em risco de reprovação" ou "Aprovado em todas as disciplinas"
- Múltiplos filhos: seletor dropdown no topo da página; troca de filho sem sair da página
- Página única: /responsavel (sem sub-rotas)
- AppLayout: mesmo header/logout do portal do professor
- Portal read-only: sem criação, edição ou ações destrutivas

### Claude's Discretion
- Layout visual exato do boletim (tabela, espaçamento, tipografia) — UI-SPEC aprovado resolve isso
- Fluxo pós-login (direto ao boletim)
- Navegação por período letivo (ano atual — sem seletor)
- Impressão/PDF — não é requisito do protótipo

### Deferred Ideas (OUT OF SCOPE)
- Histórico de anos letivos anteriores
- Notificações por e-mail/push quando frequência cair abaixo de 75%
- Exportar boletim como PDF
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| RESP-01 | Responsável vê boletim do filho: notas por disciplina organizadas por bimestre | GET /responsavel/boletim?aluno_id=X — query avaliacoes+notas for aluno's turma, grouped by disciplina |
| RESP-02 | Sistema calcula e exibe média por disciplina/bimestre automaticamente | Python: avg(nota.valor) per disciplina for available bimestres; frontend renders calculated value |
| RESP-03 | Responsável vê frequência do filho: percentual de presença por disciplina | Query chamadas per (turma_id, disciplina_id) → count presencas where aluno_id = filho.id |
| RESP-04 | Sistema exibe alerta visual quando frequência está abaixo de 75% | Frontend: bg-red-50 row + text-red-700 on frequência cell when pct < 75 |
| RESP-05 | Sistema exibe status de aprovação/reprovação com base na média calculada | Frontend: StatusBadge rendered from `aprovado` bool in API response (média >= 5.0 AND freq >= 75%) |
| RESP-06 | Responsável só vê dados dos seus próprios filhos (ownership check) | `_assert_responsavel_owns_aluno()` called in every endpoint; 403 if aluno.responsavel_id != responsavel.id |
</phase_requirements>

---

## Summary

Phase 5 is the final feature phase before polish. All schema infrastructure required is already in place from Phase 1 (migration 0001): `responsaveis`, `alunos`, `avaliacoes`, `notas`, `chamadas`, `presencas`, and `disciplinas` tables are fully created. No new Alembic migrations are needed.

The key architectural insight is that the aluno-to-responsavel link is a **direct foreign key on the alunos table** (`alunos.responsavel_id` → `responsaveis.id`), not a junction table. This simplifies the ownership check dramatically: query `Aluno.responsavel_id == responsavel.id`. The frequency calculation follows the same pattern as `professor/service.py::get_frequencia` but scoped to a single aluno instead of all alunos in a turma.

The boletim aggregation requires Python-level grouping (not SQL aggregates) matching the existing service style: for each disciplina taught in the aluno's turma, collect up to 4 bimestre notes, compute the mean of those that exist, and separately count chamadas/presencas per disciplina.

On the frontend, the stub `ResponsavelDashboard.tsx` at `/responsavel` (index route) is replaced by a new page file. The routing in `App.tsx` already has `AppLayout` wired and requires zero changes. No new npm or pip packages are needed.

**Primary recommendation:** Mirror `professor/service.py` and `professor/router.py` exactly. Create `src/responsavel/{router.py,service.py,schemas.py}`. The boletim endpoint returns a single structured response with a `filhos` list (for the selector) and a `boletim` list of per-disciplina rows. Frontend is one page: `ResponsavelBoletimPage.tsx` replacing the current stub.

---

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Ownership check (RESP-06) | API / Backend | — | JWT user → responsavel → aluno.responsavel_id; must be server-enforced, never frontend-only |
| Boletim aggregation — notas by disciplina/bimestre (RESP-01, RESP-02) | API / Backend | — | Joins avaliacoes+notas+disciplinas; mean calculation in Python; returns structured JSON |
| Frequência aggregation per disciplina (RESP-03) | API / Backend | — | Joins chamadas+presencas for aluno's turma; count logic in Python |
| Approval rule (média >= 5.0 AND freq >= 75%) (RESP-05) | API / Backend | — | Rule encoded in Python, boolean `aprovado` sent to frontend — eliminates client-side rule drift |
| Alert visual highlight (RESP-04) | Browser / Client | — | Read-only conditional Tailwind class based on `aprovado` / `freq_pct` values from API |
| Child selector (multiple filhos) | Browser / Client | — | React state; `filhos` list returned by API; changing selection triggers new query |
| Summary card (risk count) | Browser / Client | — | Derived from boletim rows: count rows where `aprovado == false`; no separate API call |

---

## Critical Schema Facts

**Verified from `backend/alembic/versions/0001_initial_schema.py` and ORM models.** [VERIFIED: codebase]

### Responsavel-to-Aluno Link

There is **no junction table** for responsavel-to-aluno. The link is a direct FK column on alunos:

```
alunos.responsavel_id  →  responsaveis.id  (ondelete=SET NULL, nullable)
```

One responsavel can have **multiple alunos** (query: `Aluno.responsavel_id == responsavel.id`).
One aluno has **at most one responsavel** (1:N, not N:M).

### Aluno-to-Turma Link

```
alunos.turma_id  →  turmas.id  (ondelete=SET NULL, nullable)
```

The aluno carries `turma_id` directly. No junction table. This is the turma context needed to find relevant chamadas and avaliacoes.

### Notas Join Chain

```
avaliacoes (turma_id, disciplina_id, bimestre)
    ↓ avaliacoes.id
notas (avaliacao_id, aluno_id, valor)
```

To get all notas for a given aluno in a given turma:
1. Query `Avaliacao` where `turma_id == aluno.turma_id`
2. For each Avaliacao, query `Nota` where `avaliacao_id == av.id AND aluno_id == aluno.id`

### Disciplinas in a Turma

There is no direct `turma_disciplinas` table. Disciplinas taught in a turma are discovered via `ProfessorTurma` (the professor_turma junction: `professor_id, turma_id, disciplina_id`). To enumerate all disciplinas for a turma: `SELECT DISTINCT disciplina_id FROM professor_turma WHERE turma_id = X`.

### Frequência Join Chain

```
chamadas (turma_id, disciplina_id, data)
    ↓ chamadas.id
presencas (chamada_id, aluno_id, presente)
```

For a given aluno in a given turma + disciplina:
- Total aulas = `COUNT(chamadas) WHERE turma_id = aluno.turma_id AND disciplina_id = D`
- Presentes = `COUNT(presencas) WHERE aluno_id = aluno.id AND chamada_id IN (chamada_ids for that disciplina) AND presente = True`

### Avaliacao.valor_maximo

Notas are stored as raw float values (e.g., 8.5 out of 10.0). The mean calculation for the boletim divides by `valor_maximo` if scores are not already on a 0-10 scale. However, the professor service always creates avaliacoes with `valor_maximo=10.0`. **Mean is computed as `sum(nota.valor) / count(notas_that_exist)`** — a simple average of the raw values (which are all on the same 0-10 scale). [VERIFIED: professor/service.py upsert_notas]

---

## Standard Stack

### Core — already installed, no new packages needed

| Component | Library | Version | Source |
|-----------|---------|---------|--------|
| Backend framework | FastAPI + Uvicorn | installed | [VERIFIED: backend runs on port 8000] |
| ORM | SQLAlchemy 2.0 (sync) | installed | [VERIFIED: all models use Mapped[] syntax] |
| Schema validation | Pydantic v2 | installed | [VERIFIED: professor/schemas.py uses ConfigDict] |
| Auth dependency | require_role("responsavel") | existing | [VERIFIED: src/auth/dependencies.py] |
| HTTP client | axios via `api` instance | installed | [VERIFIED: frontend/package.json] |
| Data fetching | TanStack Query 5 | ^5.100.5 | [VERIFIED: frontend/package.json] |
| Styling | Tailwind CSS 3 | ^3.4.19 | [VERIFIED: frontend/package.json devDependencies] |
| Routing | react-router-dom 7 | ^7.14.2 | [VERIFIED: frontend/package.json] |

**Installation needed:** None. All libraries already installed in both backend and frontend.

---

## Architecture Patterns

### System Architecture Diagram

```
Browser (responsavel user)
        |
        | GET /responsavel/meus-filhos          → returns [{id, nome, turma_nome}]
        | GET /responsavel/boletim?aluno_id=X   → returns boletim rows
        |
[FastAPI /responsavel router]
        |
        ├─ require_role("responsavel")   ← JWT → usuario → tipo check
        ├─ _get_responsavel()            ← usuario.id → responsaveis.id
        ├─ _assert_responsavel_owns_aluno() ← aluno.responsavel_id == responsavel.id
        |
        ├─ [meus-filhos] SELECT alunos WHERE responsavel_id = R
        |
        └─ [boletim] 
               ├─ get disciplinas for turma (via professor_turma DISTINCT)
               ├─ for each disciplina:
               │     notas: avaliacoes → notas WHERE aluno_id = A
               │     calc média (Python avg of existing bimestre values)
               │     frequencia: chamadas for (turma, disciplina) → presencas WHERE aluno_id = A
               │     aprovado: média >= 5.0 AND freq_pct >= 75.0
               └─ return list[DisciplinaBoletimRow]
```

### Recommended Project Structure — New Files

```
backend/
└── src/
    └── responsavel/
        ├── __init__.py        # empty
        ├── router.py          # APIRouter prefix="/responsavel"
        ├── service.py         # _get_responsavel, _assert_owns, get_meus_filhos, get_boletim
        └── schemas.py         # FilhoOut, DisciplinaBoletimRow, BoletimOut

backend/tests/
└── test_responsavel.py        # RESP-01 through RESP-06 test cases

frontend/src/
├── pages/
│   └── responsavel/
│       └── ResponsavelBoletimPage.tsx   # replaces ResponsavelDashboard stub
└── components/
    └── responsavel/
        ├── ChildSelector.tsx
        ├── SummaryCard.tsx
        ├── BoletimTable.tsx
        └── StatusBadge.tsx
```

**App.tsx change:** Replace `ResponsavelDashboard` import with `ResponsavelBoletimPage`. The route structure itself (`/responsavel` → `AppLayout` → index) is already correct and requires no changes.

---

### Pattern 1: _get_responsavel() helper

Mirror of `_get_professor()` in professor/service.py. [VERIFIED: codebase]

```python
# Source: mirrors backend/src/professor/service.py::_get_professor
from src.models.responsavel import Responsavel

def _get_responsavel(db: Session, usuario: Usuario) -> Responsavel:
    """Resolve responsavel.id from current_user (Usuario). Raises 404 if profile not found."""
    resp = db.query(Responsavel).filter(
        Responsavel.usuario_id == usuario.id
    ).first()
    if not resp:
        raise HTTPException(status_code=404, detail="Perfil de responsável não encontrado")
    return resp
```

---

### Pattern 2: Ownership check

```python
# Source: codebase analysis — alunos.responsavel_id FK verified in migration 0001
def _assert_responsavel_owns_aluno(
    db: Session, responsavel_id: int, aluno_id: int
) -> Aluno:
    """
    Raises 403 if the aluno is not linked to this responsavel.
    Returns the aluno on success (avoids a second query later).
    """
    aluno = db.query(Aluno).filter(
        Aluno.id == aluno_id,
        Aluno.responsavel_id == responsavel_id,
    ).first()
    if not aluno:
        raise HTTPException(status_code=403, detail="Acesso negado a este aluno")
    return aluno
```

**Critical:** This check must be called for every aluno-specific endpoint. Accepting `aluno_id` from URL/query params without this check is a direct IDOR vulnerability.

---

### Pattern 3: get_meus_filhos service function

```python
# Source: codebase analysis — Aluno.responsavel_id, Turma.nome verified
from src.models.turma import Turma

def get_meus_filhos(db: Session, current_user: Usuario) -> list:
    resp = _get_responsavel(db, current_user)
    alunos = db.query(Aluno).filter(
        Aluno.responsavel_id == resp.id,
        Aluno.ativo == True,
    ).all()
    result = []
    for aluno in alunos:
        turma_nome = None
        if aluno.turma_id:
            turma = db.query(Turma).filter(Turma.id == aluno.turma_id).first()
            turma_nome = turma.nome if turma else None
        result.append({
            "id": aluno.id,
            "nome": aluno.nome,
            "turma_nome": turma_nome,
        })
    return result
```

---

### Pattern 4: get_boletim service function — the core query

```python
# Source: codebase analysis — joins verified against migration 0001 schema
from src.models.professor_turma import ProfessorTurma
from src.models.disciplina import Disciplina
from src.models.avaliacao import Avaliacao
from src.models.nota import Nota
from src.models.chamada import Chamada
from src.models.presenca import Presenca

def get_boletim(db: Session, current_user: Usuario, aluno_id: int) -> list:
    resp = _get_responsavel(db, current_user)
    aluno = _assert_responsavel_owns_aluno(db, resp.id, aluno_id)

    if not aluno.turma_id:
        return []  # aluno not enrolled in any turma → empty boletim

    # Step 1: Discover all disciplinas taught in the aluno's turma
    disciplina_ids = (
        db.query(ProfessorTurma.disciplina_id)
        .filter(ProfessorTurma.turma_id == aluno.turma_id)
        .distinct()
        .all()
    )
    disciplina_ids = [row[0] for row in disciplina_ids]

    result = []
    for disc_id in disciplina_ids:
        disciplina = db.query(Disciplina).filter(Disciplina.id == disc_id).first()
        if not disciplina:
            continue

        # Step 2: Notas — one entry per bimestre
        avaliacoes = db.query(Avaliacao).filter(
            Avaliacao.turma_id == aluno.turma_id,
            Avaliacao.disciplina_id == disc_id,
        ).all()

        notas_por_bimestre: dict[int, float | None] = {1: None, 2: None, 3: None, 4: None}
        for av in avaliacoes:
            nota = db.query(Nota).filter(
                Nota.avaliacao_id == av.id,
                Nota.aluno_id == aluno.id,
            ).first()
            if nota:
                notas_por_bimestre[av.bimestre] = nota.valor

        existing_values = [v for v in notas_por_bimestre.values() if v is not None]
        media = sum(existing_values) / len(existing_values) if existing_values else None

        # Step 3: Frequência — chamadas for this turma+disciplina → presencas for this aluno
        chamadas = db.query(Chamada).filter(
            Chamada.turma_id == aluno.turma_id,
            Chamada.disciplina_id == disc_id,
        ).all()
        total_aulas = len(chamadas)
        chamada_ids = [c.id for c in chamadas]

        if total_aulas == 0:
            total_presentes = 0
            freq_pct = None   # no classes registered yet
        else:
            total_presentes = db.query(Presenca).filter(
                Presenca.aluno_id == aluno.id,
                Presenca.chamada_id.in_(chamada_ids),
                Presenca.presente == True,
            ).count()
            freq_pct = (total_presentes / total_aulas) * 100.0

        # Step 4: Approval rule (LDB completa)
        aprovado = (
            media is not None and media >= 5.0
            and freq_pct is not None and freq_pct >= 75.0
        )

        result.append({
            "disciplina_id": disc_id,
            "disciplina_nome": disciplina.nome,
            "bim1": notas_por_bimestre[1],
            "bim2": notas_por_bimestre[2],
            "bim3": notas_por_bimestre[3],
            "bim4": notas_por_bimestre[4],
            "media": media,
            "total_aulas": total_aulas,
            "total_presentes": total_presentes,
            "freq_pct": freq_pct,
            "aprovado": aprovado,
        })

    return result
```

**Note on `aprovado` when data is incomplete:** When media or freq_pct is None (no data entered yet), `aprovado` is False. This is conservative — the UI should show status badges only when at least one value exists. The planner may choose to add an `has_data` flag or check `media is not None` on the frontend before rendering the badge.

---

### Pattern 5: Pydantic response schemas

```python
# Source: mirrors backend/src/professor/schemas.py pattern
from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, ConfigDict


class FilhoOut(BaseModel):
    id: int
    nome: str
    turma_nome: Optional[str] = None


class DisciplinaBoletimRow(BaseModel):
    disciplina_id: int
    disciplina_nome: str
    bim1: Optional[float] = None
    bim2: Optional[float] = None
    bim3: Optional[float] = None
    bim4: Optional[float] = None
    media: Optional[float] = None
    total_aulas: int
    total_presentes: int
    freq_pct: Optional[float] = None
    aprovado: bool
```

---

### Pattern 6: Router endpoints

```python
# Source: mirrors backend/src/professor/router.py pattern
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from src.database import get_db
from src.auth.dependencies import require_role
from src.models.usuario import Usuario
from . import schemas, service

router = APIRouter(prefix="/responsavel", tags=["responsavel"])
responsavel_required = Depends(require_role("responsavel"))


@router.get("/meus-filhos", response_model=list[schemas.FilhoOut])
def get_meus_filhos(
    db: Session = Depends(get_db),
    current_user: Usuario = responsavel_required,
):
    return service.get_meus_filhos(db, current_user)


@router.get("/boletim", response_model=list[schemas.DisciplinaBoletimRow])
def get_boletim(
    aluno_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user: Usuario = responsavel_required,
):
    return service.get_boletim(db, current_user, aluno_id)
```

---

### Pattern 7: main.py registration

```python
# Add after professor_router import:
from src.responsavel.router import router as responsavel_router
# Add after app.include_router(professor_router):
app.include_router(responsavel_router)
```

---

### Pattern 8: Frontend — useBoletim hook

```typescript
// Source: mirrors frontend/src/pages/professor/ProfessorLandingPage.tsx useQuery pattern
import { useQuery } from '@tanstack/react-query'
import { api } from '../../services/api'

interface FilhoOut {
  id: number
  nome: string
  turma_nome: string | null
}

interface DisciplinaBoletimRow {
  disciplina_id: number
  disciplina_nome: string
  bim1: number | null
  bim2: number | null
  bim3: number | null
  bim4: number | null
  media: number | null
  total_aulas: number
  total_presentes: number
  freq_pct: number | null
  aprovado: boolean
}

function useMeusFilhos() {
  return useQuery<FilhoOut[]>({
    queryKey: ['meus-filhos'],
    queryFn: () => api.get('/responsavel/meus-filhos').then((r) => r.data),
  })
}

function useBoletim(alunoId: number | null) {
  return useQuery<DisciplinaBoletimRow[]>({
    queryKey: ['boletim', alunoId],
    queryFn: () =>
      api.get('/responsavel/boletim', { params: { aluno_id: alunoId } }).then((r) => r.data),
    enabled: alunoId !== null,
  })
}
```

**Key:** `enabled: alunoId !== null` prevents the query firing before the child selector resolves.

---

### Anti-Patterns to Avoid

- **Encoding approval logic in the frontend only:** The `aprovado` boolean must be computed in Python service and sent to the frontend. Doing it only in TypeScript risks rule drift if the Python rule ever changes.
- **Querying all chamadas by professor_id for frequência:** The professor ownership context does not apply to the responsavel module. Chamadas must be filtered by `turma_id` and `disciplina_id` only — not by `professor_id` — because multiple professors may have registered chamadas for the same turma/disciplina.
- **Not calling `_assert_responsavel_owns_aluno` for every aluno_id param:** Any endpoint accepting `aluno_id` must call the ownership check, even on GET endpoints. IDOR is the primary attack surface of this phase.
- **Returning 404 instead of 403 for unauthorized aluno access:** Use 403, not 404. Returning 404 for an aluno that exists (but belongs to another responsavel) leaks information about whether the aluno exists.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| JWT validation | Custom token parsing | `require_role("responsavel")` from `src/auth/dependencies.py` | Already tested, handles expiry + tipo check |
| Ownership check helper | Ad-hoc inline query | `_assert_responsavel_owns_aluno()` function — the same pattern as `_assert_professor_owns_turma()` | Consistent; easier to audit |
| HTTP request handling | Raw fetch | `api` axios instance from `src/services/api.ts` | Handles Bearer token injection + 401 redirect automatically |
| Data fetching + caching | useEffect + useState | TanStack Query `useQuery` | Handles loading, error, refetch; already installed |
| Tailwind classes | Custom CSS | Tailwind utility classes per UI-SPEC | Design system is locked; custom CSS breaks consistency |

**Key insight:** The complexity in this phase is in the SQL join chain, not in framework choices. All framework infrastructure is re-used from Phases 3–4.

---

## Common Pitfalls

### Pitfall 1: IDOR via aluno_id query parameter
**What goes wrong:** Responsável A crafts a request `GET /responsavel/boletim?aluno_id=99` for a child linked to Responsável B, and receives data.
**Why it happens:** Ownership check omitted on GET endpoints (mistakenly treated as read-only = safe).
**How to avoid:** `_assert_responsavel_owns_aluno()` called as the FIRST thing in `get_boletim()`, before any data query.
**Warning signs:** Test case: request boletim for an aluno_id not linked to current responsavel → must return 403, not 200.

### Pitfall 2: Empty disciplinas list when turma has no professor_turma rows
**What goes wrong:** Boletim returns empty list `[]` because no `professor_turma` rows exist for the turma yet, even though the aluno is enrolled.
**Why it happens:** Disciplinas are discovered via `professor_turma` DISTINCT query. A newly created turma with no professor assignments has no rows.
**How to avoid:** This is correct behavior — the boletim is genuinely empty when no professor has been assigned. Frontend must handle the empty state with the "Boletim não disponível" EmptyState component (per UI-SPEC).
**Warning signs:** QA: create aluno in a new turma with no professor_turma rows → boletim returns `[]` → frontend shows EmptyState, not an error.

### Pitfall 3: División por zero in média when no notas exist
**What goes wrong:** `sum(values) / len(values)` raises ZeroDivisionError when no notas are recorded for a disciplina.
**Why it happens:** `existing_values = [v for v in notas_por_bimestre.values() if v is not None]` — if no notes exist, list is empty.
**How to avoid:** `media = sum(existing_values) / len(existing_values) if existing_values else None` — guard already shown in Pattern 4.
**Warning signs:** Test with aluno who has no notas → media should be None, not an error.

### Pitfall 4: freq_pct None vs 0.0 — approval rule must not false-positive
**What goes wrong:** freq_pct is None (no classes registered), and the approval logic incorrectly marks aprovado=True because the None check is missing.
**Why it happens:** `None >= 75.0` raises TypeError in Python; if wrapped carelessly, defaults to True.
**How to avoid:** Explicit `freq_pct is not None and freq_pct >= 75.0` in the approval condition.
**Warning signs:** Test: aluno with notas (média >= 5.0) but zero chamadas registered → aprovado must be False.

### Pitfall 5: Frontend queryKey stale data after child selector change
**What goes wrong:** Switching the child selector dropdown does not refetch boletim — old data persists.
**Why it happens:** TanStack Query `queryKey` doesn't include `alunoId`, so Query treats both requests as the same.
**How to avoid:** `queryKey: ['boletim', alunoId]` — alunoId in key ensures cache-miss on switch.
**Warning signs:** Change dropdown from child A to child B → boletim should reflect child B's data, not child A's.

### Pitfall 6: Using professor_id filter when querying chamadas for the responsavel portal
**What goes wrong:** Service copied from professor module includes `Chamada.professor_id == prof.id` filter, which omits chamadas from other professors in the same turma/disciplina.
**Why it happens:** The professor frequency endpoint filters by professor_id to limit to their own chamadas. For the responsavel, we want ALL chamadas for the turma/disciplina.
**How to avoid:** Filter only on `turma_id` and `disciplina_id`, never `professor_id`, in the responsavel boletim query.

---

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest |
| Config file | backend/pytest.ini (or implicit from pyproject.toml) |
| Quick run command | `cd backend && python -m pytest tests/test_responsavel.py -x -q` |
| Full suite command | `cd backend && python -m pytest -x -q` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| RESP-01 | boletim endpoint returns notas organized by disciplina/bimestre | integration | `pytest tests/test_responsavel.py::test_boletim_notas -x` | Wave 0 |
| RESP-02 | média calculated correctly for existing bimestres | unit (via integration) | `pytest tests/test_responsavel.py::test_media_calculation -x` | Wave 0 |
| RESP-03 | frequência returned per disciplina with correct pct | integration | `pytest tests/test_responsavel.py::test_frequencia_per_disciplina -x` | Wave 0 |
| RESP-04 | low frequência flag present in response (freq_pct < 75) | unit (via integration) | `pytest tests/test_responsavel.py::test_freq_below_threshold -x` | Wave 0 |
| RESP-05 | aprovado=False when média < 5.0 OR freq < 75% | unit (via integration) | `pytest tests/test_responsavel.py::test_approval_rule -x` | Wave 0 |
| RESP-06 | responsavel cannot access aluno owned by another responsavel | security | `pytest tests/test_responsavel.py::test_ownership_idor_blocked -x` | Wave 0 |

Additional security tests:
- Unauthenticated → 401
- Professor JWT on /responsavel endpoint → 403
- Admin JWT on /responsavel endpoint → 403

### Sampling Rate
- **Per task commit:** `cd backend && python -m pytest tests/test_responsavel.py -x -q`
- **Per wave merge:** `cd backend && python -m pytest -x -q`
- **Phase gate:** Full suite green + TypeScript build clean before `/gsd-verify-work`

### Wave 0 Gaps
- [ ] `backend/tests/test_responsavel.py` — covers RESP-01 through RESP-06 + security
- [ ] `backend/src/responsavel/__init__.py` — empty init
- [ ] `backend/src/responsavel/router.py`, `service.py`, `schemas.py` — module scaffold

**conftest.py gap:** No `responsavel_headers` fixture exists in `conftest.py`. It must be added, mirroring `professor_headers`. A `responsavel_user` fixture (creates `Usuario` with `tipo=TipoUsuario.responsavel`) is also needed.

---

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | yes | `require_role("responsavel")` — JWT validated on every request |
| V3 Session Management | no | JWT stateless; session handled in Phase 2 |
| V4 Access Control | yes | `_assert_responsavel_owns_aluno()` — IDOR prevention; 403 on unauthorized aluno |
| V5 Input Validation | yes | `aluno_id: int` typed in Query param; Pydantic validates response schemas |
| V6 Cryptography | no | No new crypto operations in Phase 5 |

### Known Threat Patterns

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| IDOR on aluno_id query param | Information Disclosure | `_assert_responsavel_owns_aluno()` in every endpoint; return 403 (not 404) |
| Role escalation — professor JWT accessing /responsavel | Elevation of Privilege | `require_role("responsavel")` rejects professor JWT with 403 |
| Unauthenticated boletim access | Spoofing | `OAuth2PasswordBearer` dependency → 401 if no token |

**Security note on 403 vs 404:** For RESP-06, when the aluno_id does not belong to the current responsavel, always return 403 ("Acesso negado a este aluno") — not 404. A 404 response leaks the fact that an aluno with that ID exists in the system, which is an information disclosure issue.

---

## Environment Availability

Step 2.6: SKIPPED — Phase 5 is purely code changes (new backend module + frontend page). No external tools, services, CLIs, databases, or runtimes beyond what already runs the project are required. SQLite is the database and is already operational.

---

## Open Questions (RESOLVED)

1. **What if a responsavel has zero alunos linked?**
   - What we know: `alunos.responsavel_id` is nullable; admin may create a responsavel account before linking alunos
   - What's unclear: Should `GET /responsavel/meus-filhos` return `[]` (and frontend shows EmptyState) or should the service return 404?
   - Recommendation: Return `[]` with HTTP 200; frontend renders "Nenhum aluno vinculado" EmptyState (per UI-SPEC copy). This is consistent with professor returning `[]` for zero turmas.

2. **Media calculation when bimestre has multiple avaliacoes**
   - What we know: The schema allows multiple `Avaliacao` rows per (turma_id, disciplina_id, bimestre) — there is no unique constraint on (turma_id, disciplina_id, bimestre). The professor upsert creates one avaliacao per bimestre via find-or-create, but theoretically multiple could exist.
   - What's unclear: Should the boletim average the notas across all avaliacoes in a bimestre, or take the most recent?
   - Recommendation: For Phase 5, query avaliacoes per bimestre and aggregate all notas in that bimestre via a simple average. In practice, the professor service creates exactly one avaliacao per bimestre, so this edge case does not occur in the prototype.

3. **Nota values normalized vs raw**
   - What we know: `Nota.valor` stores the raw score (e.g., 8.5). `Avaliacao.valor_maximo` is always 10.0 (professor service hardcodes it). The boletim display uses raw values.
   - Recommendation: Display `nota.valor` directly without normalization. If `valor_maximo` differs from 10.0 in future, a normalization factor `(valor / valor_maximo * 10)` would be needed — flag as a note in code.

---

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | All avaliacoes have `valor_maximo = 10.0` (professor service hardcodes this) | get_boletim Pattern 4 | If a teacher created an avaliacao with different valor_maximo, raw nota values would be on different scales, distorting the mean. Low risk for prototype. |
| A2 | There is exactly one avaliacao per (turma, disciplina, bimestre) in practice | Open Questions #2 | Multiple avaliacoes per bimestre would cause the mean to be computed across all sub-scores in a bimestre rather than per-bimestre grade. Low risk given professor service find-or-create logic. |

---

## Sources

### Primary (HIGH confidence)
- `backend/alembic/versions/0001_initial_schema.py` — full schema verified; all table columns and FK constraints confirmed
- `backend/src/models/*.py` — ORM model definitions confirmed; `alunos.responsavel_id` FK to `responsaveis.id` confirmed
- `backend/src/professor/service.py` — service patterns (helper, ownership check, aggregation) verified
- `backend/src/professor/schemas.py` — Pydantic v2 schema patterns verified
- `backend/src/auth/dependencies.py` — `require_role()` and `get_current_user()` patterns verified
- `backend/src/main.py` — router registration pattern verified
- `backend/tests/conftest.py` — fixture inventory: `professor_headers` exists; `responsavel_headers` does NOT exist
- `frontend/src/App.tsx` — `/responsavel` route already has `AppLayout` + index; no route changes needed
- `frontend/package.json` — all required packages confirmed installed

### Secondary (MEDIUM confidence)
- None — all critical findings are verified directly from codebase

### Tertiary (LOW confidence)
- None

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all packages verified in package.json / backend runtime
- Architecture: HIGH — schema fully verified from migration files + ORM models
- Pitfalls: HIGH — derived from direct code inspection of identical patterns in professor module
- Security: HIGH — IDOR pattern is the only material attack surface; mitigation pattern exists in professor module

**Research date:** 2026-04-27
**Valid until:** 2026-05-27 (stable schema; no moving parts)
