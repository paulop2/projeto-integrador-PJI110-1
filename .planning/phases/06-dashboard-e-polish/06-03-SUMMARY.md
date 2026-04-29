# 06-03 Summary: Dashboard e Polish — Wire Frontend Dashboards

## What Was Built

Connected the frontend dashboards to the new backend aggregated endpoints and added polished UI for displaying performance metrics.

### Task 1: AdminDashboard — Alert Card & Performance Table
- Added `useAdminDesempenho` hook that queries `GET /admin/dashboard/desempenho`.
- Integrated the hook into `AdminDashboard` component.
- Added a **Desempenho por Turma** section below the count cards.
- Implemented loading state using `<SkeletonTable rows={5} columns={5} />`.
- Added an **alert card** that shows:
  - Green card with check icon when `alunos_em_risco === 0`.
  - Yellow card with warning icon when `alunos_em_risco > 0`, including descriptive subtext about risk criteria.
- Added a **responsive data table** with columns: Turma, Alunos, Média Geral, % Aprovados, Status.
  - Uses `StatusBadge` component (imported from `../../components/responsavel/StatusBadge`) to indicate turma health based on `pct_aprovados >= 60`.
  - Follows existing `EntityTable` styling pattern (`min-w-full`, `divide-y`, `bg-gray-50` header).
- Handles empty state with "Nenhuma turma cadastrada." message.

### Task 2: TurmaCard & ProfessorLandingPage — Enriched Metrics
- Extended `TurmaCard` prop interface to include `media_geral` and `pct_aprovados`.
- Added a metrics row below the student count displaying:
  - **Média geral** — formatted to 1 decimal place or em-dash if absent.
  - **% Aprovados** — formatted to 0 decimals with `%` suffix or em-dash if absent.
- Extended `ProfessorLandingPage`'s `Turma` interface to include the same optional fields.
- The existing `<TurmaCard turma={t} ... />` invocation automatically passes through the new fields.
- Skeleton loading state from Plan 02 is preserved (no regression to text loading).

## Key Files Changed

| File | Change |
|------|--------|
| `frontend/src/pages/admin/AdminDashboard.tsx` | Added `useAdminDesempenho` hook, alert card, performance table with `StatusBadge`, `SkeletonTable` loading state |
| `frontend/src/components/professor/TurmaCard.tsx` | Extended props, added metrics row for `media_geral` and `pct_aprovados` |
| `frontend/src/pages/professor/ProfessorLandingPage.tsx` | Extended `Turma` interface with optional `media_geral` and `pct_aprovados` |

## Build Results

```
$ node node_modules/.bin/tsc -b
(no output — 0 errors)
```

TypeScript compilation passes cleanly with zero errors.

## Commits

- `7921887` — `feat(06-03): add admin dashboard alert card and performance table`
- `e59de84` — `feat(06-03): enrich TurmaCard with media_geral and pct_aprovados metrics`

## Deviations from Plan

None. All requirements from Plan 06-03 were implemented as specified.
