# Phase 6: Dashboard e Polish - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-28
**Phase:** 06-dashboard-e-polish
**Areas discussed:** Dashboard do Admin, Dashboard do Professor, Tratamento de erros, Loading visual

---

## Dashboard do Admin

| Option | Description | Selected |
|--------|-------------|----------|
| Tabela de turmas com médias | Lista de turmas com média geral + % aprovados + % com frequência < 75% | |
| Card de alerta global | Um único card: 'X alunos em risco de reprovação no total' | |
| Ambos: alerta + tabela | Card de resumo no topo + tabela por turma abaixo | ✓ |

**User's choice:** Ambos: alerta + tabela

---

| Option | Description | Selected |
|--------|-------------|----------|
| Média geral + % aprovados | Duas métricas essenciais por turma | ✓ |
| Média + frequência média + % aprovados | Três métricas — mais completo mas mais pesado | |
| Apenas % aprovados por turma | Uma métrica só | |

**User's choice:** Média geral + % aprovados (Recomendado)

---

| Option | Description | Selected |
|--------|-------------|----------|
| Sim, mesma regra LDB | média < 5.0 OU frequência < 75% = em risco — consistente com Phase 5 | ✓ |
| Só frequência < 75% | Alerta apenas para risco de frequência | |

**User's choice:** Sim, mesma regra LDB (Recomendado)

---

| Option | Description | Selected |
|--------|-------------|----------|
| Novo endpoint separado | /admin/dashboard/desempenho — mantém /dashboard leve | |
| Expandir /admin/dashboard | Um endpoint com contagens + dados pedagógicos | |
| Claude decide | — | ✓ |

**User's choice:** Claude decide — decidido: novo endpoint `/admin/dashboard/desempenho`

---

## Dashboard do Professor

| Option | Description | Selected |
|--------|-------------|----------|
| Dentro de cada TurmaCard | Adicionar média e frequência média diretamente no card | ✓ |
| Nova seção em ProfessorTurmaPage | Resumo no topo da página de detalhes da turma | |
| Página separada /professor/dashboard | Tela de dashboard dedicada | |

**User's choice:** Dentro de cada TurmaCard (Recomendado)

---

| Option | Description | Selected |
|--------|-------------|----------|
| Média geral da turma + % alunos aprovados | Duas métricas chave consistentes com admin | ✓ |
| Frequência média + média geral | Foco em presença | |
| Claude decide | — | |

**User's choice:** Média geral da turma + % alunos aprovados (Recomendado)

---

## Tratamento de Erros

| Option | Description | Selected |
|--------|-------------|----------|
| Toast global no interceptor axios | api.ts: qualquer erro 4xx/5xx dispara toast.error() | ✓ |
| Banner por componente | Cada componente detecta isError e exibe banner inline | |
| Híbrido: toast global + banner nos críticos | Interceptor + banners em componentes críticos | |

**User's choice:** Toast global no interceptor axios (Recomendado)

---

| Option | Description | Selected |
|--------|-------------|----------|
| Mensagem genérica fixa | 'Erro no servidor. Tente novamente em instantes.' | |
| Usar detail do JSON de resposta | Se a API retornar {detail: '...'} usar esse texto; fallback para genérico | ✓ |
| Claude decide | — | |

**User's choice:** Usar detail do JSON de resposta

---

## Loading Visual

| Option | Description | Selected |
|--------|-------------|----------|
| Spinner centralizado simples | Componente Spinner com border-spin Tailwind | |
| Skeleton por componente | Blocos cinzas pulsantes no lugar dos dados | ✓ |
| Manter texto 'Carregando...' | Padrão atual do ProfessorLandingPage | |

**User's choice:** Skeleton por componente

---

| Option | Description | Selected |
|--------|-------------|----------|
| Apenas nos dashboards novos | Skeleton só nas novas telas | |
| Dashboards + ProfessorLandingPage | Incluir a landing page existente | |
| Todas as telas do sistema | Padronizar skeleton em todo o app | ✓ |

**User's choice:** Todas as telas do sistema

---

| Option | Description | Selected |
|--------|-------------|----------|
| Componente genérico | `<SkeletonRow />`, `<SkeletonCard />` em frontend/src/components/ | ✓ |
| Inline Tailwind em cada tela | animate-pulse + divs no lugar dos dados | |

**User's choice:** Componente genérico (Recomendado)

---

## Claude's Discretion

- Endpoint de desempenho do admin: `/admin/dashboard/desempenho` (novo endpoint separado)
- Estrutura visual exata dos skeleton components (número de linhas, proporções)
- Layout preciso da tabela de desempenho do admin (colunas, ordenação)

## Deferred Ideas

None — discussão ficou dentro do escopo da fase.
