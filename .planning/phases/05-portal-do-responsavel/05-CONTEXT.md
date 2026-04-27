# Phase 5: Portal do Responsável - Context

**Gathered:** 2026-04-27
**Status:** Ready for planning

<domain>
## Phase Boundary

Responsável visualiza boletim e frequência do filho com cálculos automáticos. Portal é read-only: sem criação ou edição de dados. Acesso restrito estritamente ao(s) filho(s) vinculado(s) ao responsável logado.

</domain>

<decisions>
## Implementation Decisions

### Layout do boletim
- Claude decide o layout de exibição das notas (tabela clássica com disciplinas nas linhas e bimestres nas colunas é o approach natural)
- Coluna de média calculada automaticamente ao lado dos bimestres, na mesma linha da disciplina
- Frequência integrada na mesma página do boletim — responsável não precisa navegar para outra tela
- PDF/impressão: Claude decide (não é requisito explícito do protótipo)

### Frequência e presença
- Frequência exibida por disciplina (não um percentual geral único)
- Percentual de frequência aparece na mesma linha da disciplina no boletim
- Base de cálculo: total de aulas registradas até hoje pelo professor (presençasr / chamadas registradas)
- Exibir percentual + números absolutos: ex. "82% (15/18)"

### Alertas e status
- Frequência < 75%: linha/célula com percentual exibida em vermelho (destaque visual sem banner intrusivo)
- Status aprovado/reprovado: badge colorido na linha da disciplina — verde = Aprovado, vermelho = Reprovado
- Regra de aprovação: média >= 5.0 **E** frequência >= 75% (regra LDB completa)
- Resumo geral no topo da página: card/banner indicando "X disciplina(s) em risco de reprovação" ou "Aprovado em todas as disciplinas"

### Navegação e fluxo
- Após login: Claude decide (ir direto ao boletim é o caminho natural dado que é o único recurso do portal)
- Responsável com múltiplos filhos: seletor de filho no topo da página (dropdown ou abas) — troca de filho sem sair da página
- Período letivo: Claude decide (somente ano letivo atual é suficiente para o protótipo)
- AppLayout: mesmo header/logout do admin e professor — consistência visual entre perfis

### Claude's Discretion
- Layout visual exato do boletim (tabela, espaçamento, tipografia)
- Fluxo pós-login (direto ao boletim ou tela intermediária)
- Navegação por período letivo (ano atual ou seletor — optar pelo mais simples)
- Impressão/PDF

</decisions>

<specifics>
## Specific Ideas

- Frequência deve mostrar números absolutos além do percentual: "82% (15/18)" — o responsável quer entender exatamente quantas aulas foram perdidas
- Status de aprovação usa tanto média quanto frequência (regra LDB completa, não só média)
- Resumo no topo deve dar uma leitura rápida do estado geral do filho antes do responsável entrar no detalhe linha por linha

</specifics>

<deferred>
## Deferred Ideas

- Histórico de anos letivos anteriores — escopo futuro
- Notificações por e-mail/push quando frequência cair abaixo de 75% — possível fase posterior
- Exportar boletim como PDF — não é requisito do protótipo

</deferred>

---

*Phase: 05-portal-do-responsavel*
*Context gathered: 2026-04-27*
