# Phase 8: UX Polish - Context

**Gathered:** 2026-05-12
**Status:** Ready for planning

<domain>
## Phase Boundary

Responsividade e padronização visual do frontend — sidebar do admin colapsável com hamburger button, UserMenu com avatar padronizado em todos os perfis, tabelas legíveis no mobile, layout das páginas de professor e responsável ajustado para telas pequenas. Sem mudanças no backend; apenas frontend React com classes Tailwind existentes.

</domain>

<decisions>
## Implementation Decisions

### Sidebar collapse (AdminLayout)

- **D-01:** Desktop: sidebar colapsa para ícones apenas (~56px de largura) ao clicar no hamburger. Estado expanded/collapsed gerenciado por useState.
- **D-02:** Mobile (< 768px): sidebar oculta por padrão. Hamburger abre drawer overlay que aparece sobre o conteúdo principal com backdrop semitransparente escuro. Toque/clique no backdrop fecha o drawer.
- **D-03:** Botão hamburger fica no topo da própria sidebar. Quando colapsada, o ícone hamburger substitui o logo no topo.
- **D-04:** No estado colapsado (desktop), apenas os ícones SVG dos itens de navegação são visíveis (sem labels). Hover sobre ícone pode mostrar tooltip com label.

### UserMenu padronizado

- **D-05:** AppLayout (professor e responsável): substituir o botão textual atual por `[avatar círculo com iniciais] Nome (Tipo) ▼`. Avatar é círculo com cor indigo e iniciais do nome. Dropdown expandido mostra: nome completo, tipo de perfil (Professor / Responsável), e botão "Sair".
- **D-06:** AdminLayout: adicionar header fixo no topo (similar ao AppLayout) com logo à esquerda e UserMenu à direita (avatar + nome + tipo + dropdown com Sair). O header coexiste com a sidebar.
- **D-07:** Seção de usuário no rodapé da Sidebar do admin: manter o avatar com iniciais + nome/email + hover-logout existente (sidebar continua tendo esse footer user section). O header é adicionado acima sem remover o footer.
- **D-08:** Criar componente `UserMenu` reutilizável (iniciais, nome, tipo, dropdown com Sair) usado tanto no AppLayout quanto no header do AdminLayout.

### Tabelas no mobile

- **D-09:** EntityTable, BoletimTable e GradeTable: envolver cada tabela em `<div className="overflow-x-auto">`. Estrutura HTML da tabela preservada. Sem transformação para cards — scroll horizontal é suficiente para Phase 8.

### Breakpoints e layout geral

- **D-10:** Mobile < 768px no AdminLayout: sidebar completamente oculta por padrão (display: none ou translate-x negativo). Main ocupa 100% da largura. Hamburger no header (ou topo da sidebar) abre o drawer overlay.
- **D-11:** AppLayout (professor e responsável): ajustar padding horizontal das páginas para mobile (usar `px-4 sm:px-6 lg:px-8`) e revisar espaçamento interno das páginas ProfessorTurmaPage e ResponsavelBoletimPage para telas pequenas.

### Claude's Discretion

- Animação de transição da sidebar (CSS transition na largura vs translate)
- Exata implementação do backdrop overlay (portal vs posicionamento absoluto)
- Tooltip nos ícones da sidebar colapsada (implementar apenas se não complicar o estado)
- Cores do avatar (manter indigo-500/20 com texto indigo-400 — consistente com sidebar atual)
- Exato conteúdo do dropdown (mínimo: nome, tipo, Sair)

</decisions>

<specifics>
## Specific Ideas

- Sidebar collapse deve se comportar como Linear/Notion: ícones visíveis quando colapsado, labels somem
- Header do AdminLayout deve ser visualmente consistente com AppLayout (mesmo estilo de header branco com shadow)
- AppLayout já tem a lógica de dropdown funcional (click outside, Escape, aria) — reusar essa lógica no componente UserMenu compartilhado

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Layouts existentes
- `frontend/src/components/AppLayout.tsx` — Layout de professor e responsável; já tem dropdown implementado com click-outside, Escape, aria-haspopup/expanded; base para UserMenu component
- `frontend/src/components/admin/AdminLayout.tsx` — Layout admin atual (sem header, sem collapse); alvo das mudanças de sidebar e header
- `frontend/src/components/admin/Sidebar.tsx` — Sidebar atual com navItems, icons, seção de usuário no rodapé; alvo do collapse e hamburger

### Tabelas a adaptar
- `frontend/src/components/admin/EntityTable.tsx` — Tabela admin com CRUD; adicionar overflow-x-auto wrapper
- `frontend/src/components/responsavel/BoletimTable.tsx` — Tabela de boletim; adicionar overflow-x-auto wrapper
- `frontend/src/components/professor/GradeTable.tsx` — Tabela de notas; adicionar overflow-x-auto wrapper

### Páginas a revisar para mobile
- `frontend/src/pages/professor/ProfessorTurmaPage.tsx` — Revisar padding e espaçamento para mobile
- `frontend/src/pages/responsavel/ResponsavelBoletimPage.tsx` — Revisar padding e espaçamento para mobile

### Referências do projeto
- `.planning/ROADMAP.md` §Phase 8 — Goal, Success Criteria e Cross-cutting constraints
- `.planning/phases/06-dashboard-e-polish/06-CONTEXT.md` — Decisões de UI polish anteriores

No external ADRs — all UX decisions captured above.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `AppLayout.tsx`: dropdown logic (useState, useRef, click-outside, Escape listener, aria-haspopup/expanded) — extrair para `UserMenu` component reutilizável
- `Sidebar.tsx`: lógica de iniciais (`user.nome.split(' ').slice(0,2).map(n=>n[0]).join('').toUpperCase()`) — copiar para UserMenu
- `Sidebar.tsx`: navItems array com icons inline — pode receber prop `collapsed` para conditional rendering das labels

### Established Patterns
- Tailwind classes para dark sidebar: `bg-gray-950 text-white border-gray-800` — manter no estado colapsado
- Tailwind responsivo: projeto usa `sm:`, `lg:` prefixes — usar `md:` como breakpoint para sidebar collapse
- Transições existentes: `transition-colors` em vários componentes — usar `transition-all` ou `transition-transform` para animate sidebar
- `useAuth()` hook retorna `user.nome`, `user.tipo`, `logout()` — disponível em qualquer componente autenticado

### Integration Points
- `AdminLayout.tsx`: adicionar `useState(collapsed)` + header JSX + wrapper para drawer overlay
- `App.tsx`: rotas de admin usam `<AdminLayout>` — mudanças em AdminLayout afetam todas as páginas admin automaticamente
- `AppLayout.tsx`: header atual tem `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8` — padrão de padding a aplicar nas páginas de professor/responsável

</code_context>

<deferred>
## Deferred Ideas

- **Admin escolhe cores da escola** — feature com persistência (banco ou localStorage) + UI de configuração no painel admin + aplicação dinâmica de palette Tailwind. Nova capacidade que pertence a fase própria (ex: Phase 11 ou backlog). Capturado para não perder a ideia.
- **Cards adaptados por linha no mobile** — EntityTable/BoletimTable/GradeTable virando cards no mobile seria melhor UX mas complexidade maior; scroll horizontal é suficiente para entrega de 24/05. Reavaliar em versão futura.

</deferred>

---

*Phase: 08-ux-polish*
*Context gathered: 2026-05-12*
