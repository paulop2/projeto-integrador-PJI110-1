# Phase 3: Painel Admin - Context

**Gathered:** 2026-04-27
**Status:** Ready for planning

<domain>
## Phase Boundary

Admin-only CRUD panel to build and maintain the school's full structure — students, classes, subjects, teacher accounts, guardian accounts, and the links between them. No data entry from teachers or guardians happens here. Role-based access and auth are Phase 2; reports and dashboards are Phase 6.

</domain>

<decisions>
## Implementation Decisions

### Navigation & structure
- Sidebar nav (persistent left sidebar with links to each entity section)
- Admin lands on a Dashboard home with summary counts (e.g. "23 alunos, 4 turmas, 2 professores")
- Sidebar order: Dashboard → Alunos → Turmas → Disciplinas → Professores → Responsáveis
- Sidebar collapse behavior: Claude's discretion (prototype scope)

### List & table design
- Pagination: 25 rows per page with prev/next navigation
- Text search on name for every list
- Row actions: Edit button + Deactivate button (no hard delete)
- Deactivated records: Claude's discretion (hidden by default vs grayed out)
- Alunos table columns: Nome, Matrícula, Turma, Status — other entities follow similar logic (Claude decides columns per entity)

### Association flows
- Professor → Turma/Disciplina: managed **from the Turma form** using repeating rows of [Disciplina dropdown] + [Professor dropdown]. Admin adds/removes rows as needed.
- Responsável → Aluno: linkable **from both sides** — Responsável form has a multi-select of alunos; Aluno form has a responsável picker.
- Initial password for professor/responsável accounts: admin sets manually during account creation (no email flow at creation time).

### Form presentation
- All create/edit forms open as **modal dialogs** (overlay on list page)
- Success feedback: toast notification ("Aluno criado com sucesso", disappears after 3s)
- Deactivate action requires a **confirmation dialog** ("Desativar [Nome]? Esta ação pode ser revertida.") with Confirm/Cancel

### Claude's Discretion
- Sidebar collapse/expand behavior (icon-only mode or always expanded)
- Deactivated record visibility default (hidden with toggle vs grayed out always visible)
- Column selection for Turmas, Disciplinas, Professores, Responsáveis tables

</decisions>

<specifics>
## Specific Ideas

- No specific UI references given — open to standard admin panel patterns
- Matrícula is explicitly required as a column in the Alunos table

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 03-painel-admin*
*Context gathered: 2026-04-27*
