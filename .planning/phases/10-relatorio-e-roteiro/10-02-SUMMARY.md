---
phase: 10-relatorio-e-roteiro
plan: 02
subsystem: docs
tags: [roteiro, video, ava, univesp, pji110]

# Dependency graph
requires:
  - phase: 07-deploy
    provides: production URLs (https://projeto-integrador.pages.dev, https://projeto-integrador-pji110-1.onrender.com) used in Slot 7
  - phase: 10-relatorio-e-roteiro
    provides: CONTEXT.md decisions D-09 (team list), D-10 (slot structure), D-11 (AVA criteria), D-04 (Ficha Tecnica); RESEARCH.md Video Script Architecture section
provides:
  - "docs/roteiro-video.md — complete 8-slot video script with speaker assignments, estimated times, screen instructions, and suggested speeches in natural Portuguese"
  - "AVA criteria mapping table covering all 6 evaluation criteria (a-f)"
  - "250-word Ficha Tecnica description block ready to copy into docs/Modelo-Ficha_Tecnica_do_video.docx"
affects: [video recording, ficha tecnica, relatorio-final]

# Tech tracking
tech-stack:
  added: []
  patterns: ["Slot-based video script format: speaker + time + screen + speech + transition"]

key-files:
  created:
    - docs/roteiro-video.md
  modified: []

key-decisions:
  - "Script content matches plan spec exactly — no deviations; all 8 slots written with complete speeches in natural Portuguese"
  - "Intentional placeholders: [INSERIR LINK DO YOUTUBE APÓS UPLOAD] at lines 4 and 150 — video not yet recorded; expected per plan"
  - "Demo credentials referenced as seed demo (admin@escola.dev/admin123) — no real production credentials in script"

patterns-established:
  - "Video script slot format: ## Slot N — Name (~Xs) with Criterio AVA, O que mostrar, Fala sugerida, Transicao"

requirements-completed:
  - ENTREGA-01

# Metrics
duration: 1min
completed: 2026-05-13
---

# Phase 10 Plan 02: Roteiro de Vídeo Summary

**Roteiro completo de 8 slots em português natural para vídeo de demonstração (~8 min), cobrindo os 6 critérios AVA e incluindo bloco de 250 palavras para a Ficha Técnica do vídeo**

## Performance

- **Duration:** ~1 min
- **Started:** 2026-05-13T14:04:59Z
- **Completed:** 2026-05-13T14:06:00Z
- **Tasks:** 1
- **Files modified:** 1

## Accomplishments
- Created `docs/roteiro-video.md` with 8 named speaker slots, each with: name, estimated time, screen instructions, full suggested speech in natural Portuguese, and transition cue
- AVA criteria mapping table at document top explicitly maps all 6 criteria (a-f) to specific slots
- Slot 7 uses verified production URL `https://projeto-integrador.pages.dev` (not localhost)
- Ficha Tecnica description block (~250 words) at end of document, ready to copy into `docs/Modelo-Ficha_Tecnica_do_video.docx`
- Recording instructions section with 6 practical guidelines for the team

## Task Commits

Each task was committed atomically:

1. **Task 1: Escrever roteiro com 8 slots de fala e cobertura dos critérios AVA** - `6155f39` (feat)

**Plan metadata:** (committed with SUMMARY.md below)

## Files Created/Modified
- `docs/roteiro-video.md` — Complete 8-slot video script, 150 lines, ~8 min estimated total runtime

## Decisions Made
- Plan provided complete content spec in `<action>` block — executed exactly as specified with no structural changes needed
- Included all contextual detail from RESEARCH.md Video Script Architecture section and CONTEXT.md D-09/D-10/D-11

## Deviations from Plan

None - plan executed exactly as written.

## Known Stubs

| Stub | File | Line | Reason |
|------|------|------|--------|
| `[INSERIR LINK DO YOUTUBE APÓS UPLOAD]` | docs/roteiro-video.md | 4, 150 | Video not yet recorded; intentional per plan; equipe insere após upload |

These stubs do NOT prevent the plan's goal — the script is complete and usable for recording. The YouTube link is only known after the team records and uploads the video.

## Issues Encountered

None.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness
- `docs/roteiro-video.md` is ready for team use immediately
- Team should: (1) rehearse and time the full script before recording, (2) verify seed demo data is present on Render before recording, (3) insert YouTube link in lines 4 and 150 after upload
- Plan 10-01 (`docs/relatorio-final.md`) is the sibling deliverable for the same ENTREGA-01 deadline (2026-05-19 23:59)

---
*Phase: 10-relatorio-e-roteiro*
*Completed: 2026-05-13*
