# 06-02 Summary — Global Error Handling & Skeleton Loading Components

## What Was Built

### Reusable Skeleton Components
Created three skeleton components to replace raw loading text across the application:

1. **SkeletonCard.tsx** — White rounded card with pulsing gray blocks for title and content rows. Supports `rows` and `className` props. Includes `aria-busy="true"` and `role="status"` for accessibility.
2. **SkeletonRow.tsx** — Horizontal flex row of pulsing gray blocks with varying widths. Supports `columns` and `className` props.
3. **SkeletonTable.tsx** — Composite component stacking SkeletonRow instances inside a bordered container with a slightly darker header row. Supports `rows` and `columns` props.

### Global Toast Error Handling
Enhanced `api.ts` error interceptor to display `toast.error()` notifications for all non-401 API errors, using the backend's `detail` field or a sensible fallback message. The existing 401 handling (logout + redirect) remains unchanged and executes before the toast check.

### Loading Text Replacements
Replaced plain loading text with skeleton components in three locations:
- **EntityTable.tsx** — Uses `<SkeletonTable rows={5} columns={columns.length + 1} />`
- **ProfessorLandingPage.tsx** — Uses a grid of 3 `<SkeletonCard rows={3} />` components
- **ResponsavelBoletimPage.tsx** — Uses `<SkeletonCard rows={2} />` for initial load and `<SkeletonTable rows={4} columns={5} />` for boletim data

## Key Files Changed

| File | Change |
|------|--------|
| `frontend/src/components/SkeletonCard.tsx` | Created |
| `frontend/src/components/SkeletonRow.tsx` | Created |
| `frontend/src/components/SkeletonTable.tsx` | Created |
| `frontend/src/services/api.ts` | Added `sonner` import and toast error interceptor |
| `frontend/src/components/admin/EntityTable.tsx` | Replaced loading div with SkeletonTable |
| `frontend/src/pages/professor/ProfessorLandingPage.tsx` | Replaced loading div with SkeletonCard grid |
| `frontend/src/pages/responsavel/ResponsavelBoletimPage.tsx` | Replaced two loading divs with SkeletonCard and SkeletonTable |

## Build Results

- `cd frontend && npx tsc -b` succeeded with **0 errors** after each task.
- Full `npm run build` could not be executed due to environment Node.js version (16.19.1) being below Vite's requirement (20.19+), but TypeScript compilation confirms type safety.

## Verification

```bash
$ grep -r "Carregando" frontend/src/pages/ --include="*.tsx" -n
frontend/src/pages/LoginPage.tsx:180:              {mutation.isPending ? 'Carregando...' : 'Entrar'}
```

Only the LoginPage button text still contains "Carregando", which is expected and not part of this task's scope.

## Deviations from Plan

None. All tasks were implemented exactly as specified in the plan.

## Commits

1. `140e48b` — feat(06-02): add reusable SkeletonCard, SkeletonRow, SkeletonTable components
2. `6f89770` — feat(06-02): add global toast error handling for non-401 API errors
3. `896c5c7` — feat(06-02): replace loading text with skeleton components across all pages
