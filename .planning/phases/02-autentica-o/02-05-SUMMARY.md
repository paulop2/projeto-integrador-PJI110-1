---
phase: 02-autentica-o
plan: "05"
subsystem: auth
tags: [react-router-dom, createBrowserRouter, protected-routes, frontend]

requires:
  - phase: 02-autentica-o
    provides: AuthContext with useAuth hook, login/logout, token storage
  - phase: 02-autentica-o
    provides: LoginPage, ForgotPasswordPage, ResetPasswordPage

provides:
  - ProtectedRoute guard component (auth + role checks)
  - AppLayout shared layout with header, user dropdown, logout
  - Three placeholder dashboards (Admin, Professor, Responsavel)
  - Complete createBrowserRouter configuration in App.tsx
  - PublicRoute wrapper to redirect authenticated users away from /login

affects:
  - 03-gest-o-de-usu-rios
  - 04-notas-e-frequ-ncia

tech-stack:
  added: []
  patterns:
    - "ProtectedRoute as element in createBrowserRouter with Outlet for nested layouts"
    - "AppLayout wraps Outlet with shared header and logout dropdown"
    - "PublicRoute wrapper for pages that should be inaccessible when authenticated"

key-files:
  created:
    - frontend/src/components/ProtectedRoute.tsx
    - frontend/src/components/AppLayout.tsx
    - frontend/src/pages/dashboards/AdminDashboard.tsx
    - frontend/src/pages/dashboards/ProfessorDashboard.tsx
    - frontend/src/pages/dashboards/ResponsavelDashboard.tsx
  modified:
    - frontend/src/App.tsx
    - frontend/src/main.tsx

key-decisions:
  - "Kept createBrowserRouter (data API) instead of legacy BrowserRouter"
  - "AuthProvider wraps RouterProvider so useAuth() works inside route components"
  - "Dropdown closes on mousedown outside via useEffect + ref"

patterns-established:
  - "ProtectedRoute + AppLayout nesting: route element is ProtectedRoute, children contain AppLayout, which contains Outlet for the actual page"
  - "Tipo label mapping: admin → Admin, professor → Professor, responsavel → Responsável"

duration: 5min
completed: 2026-04-27
---

# Phase 02 Plan 05: Frontend Routing and Protected Routes Summary

**Complete frontend auth flow with role-based route guards, shared AppLayout with logout dropdown, and three placeholder dashboards wired via createBrowserRouter.**

## Performance

- **Duration:** 5 min
- **Started:** 2026-04-27T14:50:00Z (approx)
- **Completed:** 2026-04-27T14:55:00Z (approx)
- **Tasks:** 2
- **Files modified:** 7

## Accomplishments
- ProtectedRoute component blocks unauthenticated access and redirects wrong roles to their own dashboard
- AppLayout provides consistent header with user name, role label, and logout dropdown
- Three placeholder dashboards render "Bem-vindo, [nome]!" using useAuth().user.nome
- App.tsx rewritten with full createBrowserRouter covering login, password reset, role-protected routes, root redirect, and catch-all
- PublicRoute prevents authenticated users from accessing /login

## Task Commits

1. **Task 1: ProtectedRoute + AppLayout + placeholder dashboards** - `29704d2` (feat)
2. **Task 2: Rewrite App.tsx with complete router config + AuthProvider** - `c33d89b` (feat)

**Plan metadata:** [to be committed]

## Files Created/Modified
- `frontend/src/components/ProtectedRoute.tsx` - Route guard checking auth and allowedRole
- `frontend/src/components/AppLayout.tsx` - Shared layout with header, dropdown, logout
- `frontend/src/pages/dashboards/AdminDashboard.tsx` - Admin placeholder dashboard
- `frontend/src/pages/dashboards/ProfessorDashboard.tsx` - Professor placeholder dashboard
- `frontend/src/pages/dashboards/ResponsavelDashboard.tsx` - Responsavel placeholder dashboard
- `frontend/src/App.tsx` - Complete router config with createBrowserRouter
- `frontend/src/main.tsx` - Updated to render `<App />` instead of `<RouterProvider router={router} />`

## Decisions Made
- Kept createBrowserRouter (data API) as specified in previous plans
- AuthProvider wraps RouterProvider so all route components have access to useAuth()
- Dropdown uses mousedown listener on document with cleanup on unmount

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Updated main.tsx to import App instead of router**
- **Found during:** Task 2 (Rewrite App.tsx)
- **Issue:** Old main.tsx imported `router` from App.tsx and wrapped it with QueryClientProvider + RouterProvider. New App.tsx no longer exports `router` and instead exports an App component that wraps AuthProvider around RouterProvider.
- **Fix:** Rewrote main.tsx to import `App` and render `<App />` inside QueryClientProvider, removing the duplicate RouterProvider.
- **Files modified:** frontend/src/main.tsx
- **Verification:** Build succeeds with zero TypeScript errors
- **Committed in:** c33d89b (Task 2 commit)

---

**Total deviations:** 1 auto-fixed (1 blocking)
**Impact on plan:** Necessary adjustment for AuthProvider to wrap RouterProvider correctly. No scope creep.

## Issues Encountered
- None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Frontend auth flow is complete: login → dashboard → logout cycle works end-to-end
- Ready for Phase 3 (user management) to build real dashboard content
- No blockers

## Self-Check: PASSED

- [x] All 7 key files exist on disk
- [x] Task commits 29704d2 and c33d89b exist in git history
- [x] TypeScript compilation passes (`npx tsc --noEmit`)
- [x] Vite production build succeeds

---
*Phase: 02-autentica-o*
*Completed: 2026-04-27*
