# Phase 8: UX Polish - Discussion Log

**Session:** 2026-05-12
**Areas discussed:** Sidebar collapse, UserMenu padronizado, Tabelas no mobile, Breakpoints e layout geral

---

## Area: Sidebar collapse

**Q1: Comportamento desktop do hamburger**
- Options: Colapsa para ícones / Some completamente / Claude decide
- Selected: **Colapsa para ícones (~56px)**

**Q2: Comportamento mobile (< 768px)**
- Options: Overlay/drawer / Sempre colapsada / Claude decide
- Selected: **Overlay/drawer com backdrop**

**Q3: Localização do hamburger**
- Options: No topo da sidebar / Header fixo no conteúdo
- Selected: **No topo da sidebar**

---

## Area: UserMenu padronizado

**Q1: Avatar/dropdown no AppLayout (professor/responsável)**
- Options: Avatar com iniciais + dropdown / Manter texto, melhorar dropdown
- Selected: **Ambos — avatar com iniciais + manter texto "Nome (Tipo)" + dropdown melhorado**

**Q2: Rodapé da sidebar do admin**
- Options: Dropdown no rodapé / Manter hover-logout
- Selected: **Manter hover-logout simples + adicionar header para manter coerência estética**

**Q3: Header fixo no AdminLayout**
- Options: Não / Sim, adicionar header
- Selected: **Sim — adicionar header com avatar/dropdown ao AdminLayout**

---

## Area: Tabelas no mobile

**Q1: Estratégia para mobile**
- Options: Scroll horizontal com wrapper / Cards por linha / Claude decide
- Selected: **Scroll horizontal com overflow-x-auto**

---

## Area: Breakpoints e layout geral

**Q1: Sidebar mobile por padrão**
- Options: Escondida, abre como overlay / Colapsada para ícones
- Selected: **Escondida por padrão, abre como overlay**

**Q2: AppLayout além do UserMenu**
- Options: Só UserMenu / Também ajustar padding e conteúdo
- Selected: **Ajustar padding e conteúdo das páginas de professor e responsável**

---

## Deferred Ideas

- **Admin escolhe cores da escola** — nova feature com persistência + UI de configuração. Pertence a fase própria.
- **Cards adaptados por linha** — melhor UX mas fora de escopo para entrega de 24/05.

---

## Claude's Discretion

- Animação de transição da sidebar
- Implementação do backdrop overlay
- Tooltip nos ícones da sidebar colapsada
- Cores do avatar (manter padrão indigo)
