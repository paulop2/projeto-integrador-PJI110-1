# Phase 6: Dashboard e Polish - Context

**Gathered:** 2026-04-28
**Status:** Ready for planning

<domain>
## Phase Boundary

Admin e professor têm dashboards com visão agregada de desempenho por turma (médias e % aprovados). Sistema exibe erros de API com mensagens amigáveis em português via toast global. Estados de loading padronizados com skeleton components em todas as telas.

</domain>

<decisions>
## Implementation Decisions

### Dashboard do Admin
- **D-01:** Mostrar card de alerta global + tabela de turmas com desempenho — padrão análogo ao portal do responsável (SummaryCard + tabela).
- **D-02:** Card de alerta usa regra LDB completa (mesma da Phase 5): aluno em risco = reprovado em pelo menos uma disciplina (média < 5.0 OU frequência < 75%).
- **D-03:** Tabela de turmas mostra: nome da turma, média geral, % aprovados.
- **D-04:** Dados pedagógicos expostos por novo endpoint separado `/admin/dashboard/desempenho` — mantém o `/admin/dashboard` existente leve (só contagens).

### Dashboard do Professor
- **D-05:** Métricas agregadas integradas no TurmaCard existente na ProfessorLandingPage — professor vê tudo sem navegar para outra tela.
- **D-06:** TurmaCard exibe: média geral da turma + % alunos aprovados (consistente com admin dashboard).

### Tratamento de Erros
- **D-07:** Toast automático global via interceptor do axios em `api.ts` para todos os erros 4xx/5xx (exceto 401, que já redireciona para /login).
- **D-08:** Mensagem do toast: usar `error.response?.data?.detail` se disponível; fallback para mensagem genérica ("Erro no servidor. Tente novamente em instantes.") para erros sem detail legível.
- **D-09:** Toast usa `toast.error()` do Sonner — já montado em `main.tsx` com `richColors`.

### Loading Visual
- **D-10:** Padrão: skeleton components reutilizáveis em TODAS as telas do sistema.
- **D-11:** Criar componentes genéricos em `frontend/src/components/` — ex: `<SkeletonRow />`, `<SkeletonCard />` — reaproveitados em todas as telas.
- **D-12:** Substituir texto "Carregando..." em ProfessorLandingPage e qualquer outro texto inline de loading por skeleton.

### Claude's Discretion
- Estrutura visual exata dos skeleton components (número de linhas, proporções)
- Layout preciso da tabela de desempenho do admin (colunas, ordenação)
- Endpoint separado para desempenho do admin: `/admin/dashboard/desempenho`

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Fase anterior — Portal do Responsável (padrões a reutilizar)
- `.planning/phases/05-portal-do-responsavel/05-CONTEXT.md` — Regra LDB, padrão de card de alerta (SummaryCard), cálculo de aprovação
- `frontend/src/components/responsavel/SummaryCard.tsx` — Componente de alerta global (alunos em risco) — reutilizar lógica visual
- `frontend/src/components/responsavel/StatusBadge.tsx` — Badge verde/vermelho aprovado/reprovado — reutilizar

### Backend existente
- `backend/src/responsavel/service.py` — Lógica LDB completa (média >= 5.0 AND freq >= 75%) — replicar cálculo no novo endpoint admin
- `backend/src/admin/router.py` — Onde adicionar novo endpoint `/admin/dashboard/desempenho`
- `backend/src/professor/service.py` — Dados de turmas, chamadas, notas — base para cálculo agregado do professor

### Frontend existente
- `frontend/src/pages/professor/ProfessorLandingPage.tsx` — TurmaCard a ser enriquecido com métricas
- `frontend/src/components/professor/TurmaCard.tsx` — Componente a modificar
- `frontend/src/pages/admin/AdminDashboard.tsx` — Já tem count cards + isError banner; adicionar seção pedagógica
- `frontend/src/services/api.ts` — Interceptor axios — onde adicionar toast global de erro

### Infraestrutura
- `frontend/src/main.tsx` — Toaster do Sonner já montado com `richColors position="top-right"`

No external ADRs or specs — all requirements captured above.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `SummaryCard.tsx`: card de alerta "X em risco" — reutilizar lógica e visual no dashboard admin
- `StatusBadge.tsx`: badge aprovado/reprovado — reutilizar na tabela de turmas
- `TurmaCard.tsx`: já exibe nome, disciplinas, num_alunos — adicionar média + % aprovados
- `AdminDashboard.tsx` (`pages/admin/`): já tem grid de count cards + isError inline — adicionar seção abaixo dos cards
- Sonner `toast` já disponível globalmente — importar e chamar `toast.error()` no interceptor

### Established Patterns
- TanStack Query com `isLoading` / `isError` / `data` — padrão consistente em todas as telas
- `useQuery` com `queryKey` tipado — seguir mesmo padrão para os novos endpoints
- Backend service layer + router pattern — novo endpoint segue `admin/service.py` + `admin/router.py`
- `require_role("admin")` / `require_role("professor")` via Depends — obrigatório nos novos endpoints

### Integration Points
- Novo endpoint `/admin/dashboard/desempenho`: admin router + service — calcula por turma cruzando Aluno, Nota, Avaliacao, Chamada, Presenca
- TurmaCard enriquecido: professor landing page já chama `/professor/minhas-turmas` — novo endpoint de métricas agrega por turma_id
- Interceptor de erro em `api.ts` response handler (bloco `(error) =>`) — adicionar toast antes de `return Promise.reject(error)`

</code_context>

<specifics>
## Specific Ideas

- Padrão visual admin: card de alerta (alunos em risco) no topo → tabela de turmas abaixo — análogo ao portal do responsável
- Toast de erro deve usar `error.response?.data?.detail` quando disponível (mensagens do FastAPI são em português e descritivas)
- Skeleton components como componentes genéricos reutilizáveis (`<SkeletonRow />`, `<SkeletonCard />`) em `frontend/src/components/`
- Substituir texto "Carregando..." em ProfessorLandingPage e em qualquer outro lugar do sistema

</specifics>

<deferred>
## Deferred Ideas

None — discussão ficou dentro do escopo da fase.

</deferred>

---

*Phase: 06-dashboard-e-polish*
*Context gathered: 2026-04-28*
