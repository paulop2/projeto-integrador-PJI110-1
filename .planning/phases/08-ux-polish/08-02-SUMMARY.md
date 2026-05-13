---
phase: 08-ux-polish
plan: "08-02"
subsystem: ui
tags: [react, tailwind, component-extraction, accessibility]

# Dependency graph
requires:
  - phase: 08-ux-polish
    provides: "AdminLayout refactor with sidebar collapse (08-01)"
provides:
  - "Reusable UserMenu component with avatar initials and dropdown"
  - "AppLayout refactored to delegate dropdown logic to UserMenu"
  - "Consistent user menu across AppLayout and AdminLayout"
affects:
  - "08-03 responsividade"

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Component extraction: inline dropdown logic → reusable UserMenu"
    - "ARIA best practices: aria-haspopup, aria-expanded, aria-controls, role=menu, role=menuitem"
    - "Click-outside and Escape key handling in React component"

key-files:
  created:
    - frontend/src/components/UserMenu.tsx
  modified:
    - frontend/src/components/AppLayout.tsx

key-decisions:
  - "Named export UserMenu (not default) for clarity and tree-shaking"
  - "Avatar initials computed from first two words of user.nome, matching Sidebar pattern"
  - "Dropdown width increased from w-40 to w-48 to accommodate name + tipo comfortably"

patterns-established:
  - "UserMenu: reusable avatar+dropdown component for all layouts"
  - "ARIA attributes on dropdown: aria-haspopup, aria-expanded, aria-controls, role=menu, role=menuitem"

# Metrics
duration: 3min
completed: 2026-05-13
---

# Phase 8 Plan 02: UserMenu Component Extraction Summary

**Reusable UserMenu component with indigo avatar initials, identity dropdown, and ARIA accessibility — AppLayout refactored from 128 lines to ~25 lines**

## Performance

- **Duration:** 3 min
- **Started:** 2026-05-13T00:58:31Z
- **Completed:** 2026-05-13T01:01:35Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- Created UserMenu.tsx with avatar circle (indigo-500/20 background, indigo-400 text), initials computation, dropdown panel with identity row and logout button
- Extracted all dropdown logic (state, refs, click-outside, Escape key, logout handler) from AppLayout into UserMenu
- Refactored AppLayout.tsx from 128 lines to ~25 lines — thin shell delegating user menu to UserMenu component
- Full ARIA compliance: aria-haspopup, aria-expanded, aria-controls, role=menu, role=menuitem

## Task Commits

Each task was committed atomically:

1. **Task 1: Create UserMenu component** — `7448f72` (feat)
2. **Task 2: Update AppLayout to use UserMenu** — `65c22a4` (refactor)

**Plan metadata:** `TBD` (docs: complete plan)

## Files Created/Modified
- `frontend/src/components/UserMenu.tsx` — New reusable component: avatar initials in indigo circle, dropdown with nome/tipo identity and "Sair" logout button, click-outside and Escape handlers, proper ARIA
- `frontend/src/components/AppLayout.tsx` — Refactored to use `<UserMenu />`, removed all inline dropdown logic (state, effects, handlers, tipoLabelMap)

## Decisions Made
- Named export `UserMenu` instead of default export for clarity and better tree-shaking
- Avatar initials computed from first two words of `user.nome` (matching existing Sidebar.tsx pattern)
- Dropdown width `w-48` (192px) instead of original `w-40` (160px) to comfortably fit name + tipo

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- UserMenu component ready for use in AdminLayout (08-01 already references it)
- AppLayout fully refactored and delegating user menu logic
- Ready for 08-03 responsividade plan

## Self-Check: PASSED

- [x] `frontend/src/components/UserMenu.tsx` exists
- [x] `frontend/src/components/AppLayout.tsx` contains `<UserMenu />`
- [x] TypeScript compilation passes (`npx tsc --noEmit -p tsconfig.app.json` exits 0)
- [x] Commits exist: `7448f72`, `65c22a4`

---
*Phase: 08-ux-polish*
*Completed: 2026-05-13*
