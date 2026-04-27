---
phase: 03-painel-admin
plan: 03
subsystem: frontend
tags: [react, tailwind, layout, components, routing]
requires:
  - 03-01
  - 03-02
provides:
  - "AdminLayout + Sidebar with 6 nav links"
  - "Reusable Modal, ConfirmDialog, EntityTable components"
  - "AdminDashboard page fetching /admin/dashboard counts"
  - "App.tsx admin route tree with AdminLayout and 5 placeholder child routes"
affects:
  - frontend/src/components/admin/AdminLayout.tsx
  - frontend/src/components/admin/Sidebar.tsx
  - frontend/src/components/admin/Modal.tsx
  - frontend/src/components/admin/ConfirmDialog.tsx
  - frontend/src/components/admin/EntityTable.tsx
  - frontend/src/pages/admin/AdminDashboard.tsx
  - frontend/src/App.tsx
key-files.created:
  - frontend/src/components/admin/AdminLayout.tsx
  - frontend/src/components/admin/Sidebar.tsx
  - frontend/src/components/admin/Modal.tsx
  - frontend/src/components/admin/ConfirmDialog.tsx
  - frontend/src/components/admin/EntityTable.tsx
  - frontend/src/pages/admin/AdminDashboard.tsx
key-files.modified:
  - frontend/src/App.tsx
key-decisions:
  - "Sidebar is always expanded (no collapse toggle) to keep prototype simple"
  - "Modal uses createPortal + native ESC key handler; no extra dependency"
  - "EntityTable shows 'Ativo'/'Inativo' badge for ativo column and hides Deactivate button when inactive"
  - "Placeholder pages for Alunos/Turmas/Disciplinas/Professores/Responsáveis keep routes functional until Plan 04"
  - "AppLayout import kept because /professor and /responsavel routes still use it"
requirements-completed:
  - ADMIN-01 (partial - UI shell)
  - ADMIN-02 (partial - UI shell)
  - ADMIN-03 (partial - UI shell)
  - ADMIN-04 (partial - UI shell)
  - ADMIN-05 (partial - UI shell)
  - ADMIN-06 (partial - UI shell)
duration: 12min
completed: 2026-04-27
---

# 03-03 Summary: Frontend Admin Layout and Shared Components

## One-liner
Built the admin layout shell — sidebar navigation, reusable Modal/ConfirmDialog/EntityTable components, AdminDashboard with live API count cards, and wired all admin routes in App.tsx with placeholder entity pages.

## What was built

### Task 1: AdminLayout, Sidebar, and shared UI components
- Created `frontend/src/components/admin/` directory with 5 files:
  - **Sidebar.tsx**: persistent left nav with 6 `NavLink` items (Dashboard → Responsáveis), active link highlighted with `bg-indigo-600`, logout button at bottom using `useAuth()`
  - **AdminLayout.tsx**: flex layout with Sidebar + `<Outlet>` for admin routes
  - **Modal.tsx**: portal-based modal with ESC close, backdrop click close, `max-w-lg`, `max-h-[90vh]` scroll
  - **ConfirmDialog.tsx**: wraps Modal for deactivate confirmations; shows entity name + Cancel/Desativar buttons
  - **EntityTable.tsx**: reusable table with search input, pagination (prev/next + page/total), Edit/Deactivate row actions, loading and empty states

### Task 2: AdminDashboard page + App.tsx route update
- Created `frontend/src/pages/admin/AdminDashboard.tsx`:
  - Fetches `/admin/dashboard` via TanStack Query (`queryKey: ['admin-dashboard']`)
  - Displays 5 count cards (Alunos, Turmas, Disciplinas, Professores, Responsáveis) with color-coded borders
  - Shows loading dashes and API error banner
- Updated `frontend/src/App.tsx`:
  - Replaced `AppLayout` with `AdminLayout` inside `/admin` protected route
  - Added 5 placeholder child routes (`alunos`, `turmas`, `disciplinas`, `professores`, `responsaveis`)
  - Kept `/professor` and `/responsavel` routes using `AppLayout` unchanged

## Outcome
- Frontend builds successfully (`npm run build` exit 0) with Node 22.11.0
- TypeScript compiles clean (`tsc --noEmit` 0 errors)
- Admin routes render inside sidebar layout; non-admin routes keep top-header layout
- Dashboard count cards fetch real data from backend endpoint implemented in Plan 02
- All 11 backend admin tests remain green

## Deviations
- **Manual browser verification deferred**: Steps 5–7 of plan verification (visual confirmation of sidebar, count cards, placeholder pages, and professor layout unchanged) require a browser. In this headless environment, we verified inclusion of UI strings in the production bundle and confirmed route wiring via TypeScript + build. Human verification should be done before Phase 3 completion.

## Next step
Proceed to **03-04-PLAN.md** — Frontend CRUD pages: AlunosPage, TurmasPage (with professor_turma rows), DisciplinasPage, ProfessoresPage, ResponsaveisPage.
