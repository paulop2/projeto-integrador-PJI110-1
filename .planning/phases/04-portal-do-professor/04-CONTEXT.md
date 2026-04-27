# Phase 4: Portal do Professor - Context

**Gathered:** 2026-04-27
**Status:** Ready for planning

<domain>
## Phase Boundary

Portal exclusivo do professor para registrar chamada e lançar notas nas turmas às quais está vinculado. Professor não vê nem acessa turmas de outros professores. Cálculos de média e boletim do responsável são fases separadas.

</domain>

<decisions>
## Implementation Decisions

### Navegação entre turmas
- Landing page do professor: lista de cards das turmas vinculadas
- Card mostra: nome da turma, disciplina(s) vinculada(s), número de alunos
- Dentro da turma: três abas — **Chamada | Notas | Frequência**
- Retorno à lista: breadcrumb no topo (`Minhas Turmas > Turma A`)

### Chamada (attendance)
- Data padrão ao abrir chamada: **hoje** (professor pode alterar para registrar datas retroativas)
- Interface: lista de alunos com toggle **Presente / Falta** por aluno
- Estado inicial de chamada nova (sem registros): **todos presentes** — professor só marca quem faltou
- Chamadas já salvas: **editáveis**, mas com aviso de que é uma alteração em registro existente
- Feedback ao salvar: **toast/snackbar** de sucesso

### Lançamento de notas
- Fluxo: professor escolhe **turma + disciplina** primeiro; abre tabela de alunos × bimestres
- Formato de entrada: **grade/tabela** — alunos nas linhas, 1º ao 4º bimestre nas colunas
- Validação: **erro inline** no campo quando nota inválida (acima do máximo, texto) — campo fica vermelho, não deixa salvar enquanto inválido
- Salvamento: **botão "Salvar" explícito** — professor preenche a tabela e confirma

### Resumo de frequência
- Localização: **terceira aba** da turma (Chamada | Notas | Frequência)
- Dados por aluno: **percentual + contagem** (ex: 85% — 17/20 aulas)
- Destaque visual: **linha vermelha** ou badge de alerta ⚠ para alunos abaixo de 75% (regra LDB)
- Período coberto: Claude decide — provavelmente ano letivo acumulado para simplicidade do protótipo

### Claude's Discretion
- Como o professor acessa chamadas de datas anteriores (seletor de data vs. histórico paginado)
- Período exibido no resumo de frequência (ano letivo completo vs. filtrável por bimestre)
- Design detalhado do toggle Presente/Falta (botão, switch, etc.)
- Comportamento de navegação entre células da grade de notas (Tab, Enter, etc.)

</decisions>

<specifics>
## Specific Ideas

- Grade de notas: referência visual confirmada pelo usuário — alunos nas linhas, bimestres (1º–4º) nas colunas
- Cards de turma na landing devem mostrar informação suficiente para o professor identificar a turma sem entrar nela (nome, disciplina, nº alunos)
- Alerta de frequência abaixo de 75% deve ser imediato e visual — professor identifica alunos em risco sem precisar calcular

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 04-portal-do-professor*
*Context gathered: 2026-04-27*
