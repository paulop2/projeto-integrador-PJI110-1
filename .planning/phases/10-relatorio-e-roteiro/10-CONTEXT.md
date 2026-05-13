# Phase 10: Relatório e Roteiro - Context

**Gathered:** 2026-05-13
**Status:** Ready for planning

<domain>
## Phase Boundary

Dois documentos de entrega acadêmica, ambos prontos até 2026-05-19 23:59:

1. **`docs/relatorio-final.md`** — rascunho completo do Relatório Técnico-Científico seguindo o template UNIVESP (`docs/Modelo_Relatorio_Final.docx`), para a equipe transferir ao Word e exportar como PDF
2. **`docs/roteiro-video.md`** — roteiro de demonstração em vídeo (5-10 min, YouTube) com falas divididas entre os 8 integrantes + resumo de 250 palavras para preencher a Ficha Técnica (`docs/Modelo-Ficha_Tecnica_do_video.docx`)

Sem mudanças no código — fase é puramente documental. O planner lê os artefatos GSD (SUMMARY.md, CONTEXT.md, DISCUSSION-LOG.md das phases 1-8) e os docs existentes em `/docs` como fonte primária de conteúdo.

</domain>

<decisions>
## Implementation Decisions

### Template e formato de entrega

- **D-01:** Relatório segue o template oficial UNIVESP (`docs/Modelo_Relatorio_Final.docx`). Seções obrigatórias (em ordem): Capa, Folha de rosto, Ficha catalográfica, Resumo (250 palavras) + Palavras-chave, Sumário, **1 Introdução**, **2 Desenvolvimento** (2.1 Objetivos · 2.2 Justificativa e delimitação do problema · 2.3 Fundamentação teórica · 2.4 Aplicação das disciplinas · 2.5 Metodologia), **3 Resultados: solução final**, **4 Considerações finais**, Referências.
- **D-02:** Rascunho entregue como `docs/relatorio-final.md` (Markdown). Formatação Word (Times New Roman 12, margens ABNT 3/2cm, espaçamento 1,5) é responsabilidade da equipe ao copiar para o `.docx`.
- **D-03:** Vídeo: postado no YouTube (link obrigatório na capa do relatório + postado no AVA). Duração: mínimo 5 minutos, máximo 10 minutos. Prazo: **2026-05-19 23:59**. Entrega no AVA como PDF — apenas um integrante envia pelo grupo.
- **D-04:** Ficha Técnica (`docs/Modelo-Ficha_Tecnica_do_video.docx`) preenchida com: nomes/RAs dos integrantes, polo (Valinhos), curso, disciplina (Projeto Integrador em Computação I), orientador (Edson Ricardo Nunes Nascimento), título, link YouTube, descrição do protótipo (250 palavras). O roteiro inclui um bloco "Descrição para Ficha Técnica" pronto para copiar.
- **D-05:** A correção do relatório final está vinculada à entrega do vídeo — ambos devem ser entregues juntos até 19/05.

### Conteúdo gerado vs esqueleto

- **D-06:** Planner gera **rascunho completo** do relatório — texto de todas as seções elaborado a partir dos artefatos GSD, pronto para revisar. Não usar placeholders genéricos. A fonte primária é: SUMMARY.md das phases 1-8, CONTEXT.md de cada phase, DISCUSSION-LOG.md, STATE.md, PROJECT.md.
- **D-07:** Fundamentação teórica (2.3): planner sugere fontes relevantes com citações formatadas em **NBR:10520:2023** (sem caixa alta nas citações — ex: `(Fielding, 2000)` e não `(FIELDING, 2000)`). Temas: sistemas de informação escolar, REST APIs, React/SPAs, LDB art. 24 (frequência 75%), metodologia ágil/Scrum.
- **D-08:** Seção 2.4 (Aplicação das disciplinas): planner infere as disciplinas mais prováveis para o curso de Computação UNIVESP (Algoritmos e Programação, Banco de Dados, Engenharia de Software, IHC/Interação Humano-Computador, Programação para Web) e relaciona cada uma ao que foi construído. Equipe valida e ajusta.

### Roteiro de vídeo e divisão entre integrantes

- **D-09:** Integrantes confirmados (do README):
  1. Luiz Eduardo Rodrigues Firmino
  2. Thalita Fernanda Rospendowski Mazzini
  3. Rafael Gustavo Leite
  4. Luiz Henrique de Toledo
  5. Diego Miguel Mafra
  6. Nicholas Prado de Sousa Medeiros
  7. Paulo Vitor de Souza
  8. Leonardo Matheus Anselmo Matiazzo

- **D-10:** Planner propõe divisão equilibrada de 8 slots de fala (não por fase, não por perfil pré-definido). Estrutura sugerida: Apresentação do grupo e problema (1-2 pessoas) → Arquitetura técnica (1 pessoa) → Demo perfil Admin (1 pessoa) → Demo perfil Professor (1 pessoa) → Demo perfil Responsável + alertas Phase 9 (1 pessoa) → Deploy e acesso em produção (1 pessoa) → Considerações finais e impacto (1-2 pessoas). Cada slot com falas aproximadas, tempo estimado, e o que mostrar na tela.
- **D-11:** Critérios de avaliação do vídeo a cobrir explicitamente no roteiro: (a) identificação do grupo, (b) apresentação do problema e relevância comunitária, (c) solução em funcionamento, (d) implementação e impacto na comunidade externa, (e) uso de slides/imagens/recursos, (f) respeito ao tempo 5-10min.

### Profundidade técnica do relatório

- **D-12:** Sem código-fonte no corpo do relatório — usar **diagramas de arquitetura** como figuras: (a) Diagrama ER do banco de dados (já existe em `docs/database-schema.md`), (b) Fluxo de autenticação JWT (diagrama de sequência simples). Planner inclui o Markdown dos diagramas como sugestão de conteúdo visual.
- **D-13:** Screenshots estratégicos na seção **3 Resultados** — planner indica quais telas capturar (sugestão: tela de login, painel admin, registro de chamada do professor, boletim do responsável, painel de alertas Phase 9). Equipe captura as telas e insere no Word como Figuras numeradas.

### Feedback do professor a corrigir (nota 8,5/10)

- **D-14:** A **Introdução** DEVE descrever o contexto escolar específico: escola pública municipal, Valinhos SP; entrevista realizada em 08/03/2026 com Elizabete Ap. Godoy de Toledo (professora da rede municipal); mencionar como o registro é feito atualmente (e.g., cadernetas/papel, dificuldade de acesso dos pais). Sem essa contextualização a justificativa fica genérica.
- **D-15:** A **Justificativa** (2.2) deve responder: como a comunicação escola-responsável acontece hoje? Como o PI melhora especificamente essa realidade da escola parceira? Evitar afirmações genéricas sem dados contextuais.
- **D-16:** A seção **3 Resultados** deve ter conteúdo real (não texto do template). Incluir: funcionalidades implementadas por fase, capturas de tela, métricas (ex: 8 fases implementadas, N endpoints, deploy ativo em produção).
- **D-17:** **Referências** em formato NBR:10520:2023 (não ABNT 2002 como no template de 2021). Citações no texto sem caixa alta.

### Claude's Discretion

- Título exato do trabalho (TBD pela equipe — planner usa como placeholder)
- Número de páginas total esperado (planner estima 15-25 páginas)
- Número de Registro Acadêmico (RA) de cada integrante (planner deixa `[RA]` como placeholder)
- Fonte exata das referências bibliográficas — planner sugere, equipe confirma quais têm acesso
- Tempo exato de cada seção no roteiro de vídeo (planner distribui os 7-8 min proporcionalmente)

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Templates de entrega (fonte da estrutura)
- `docs/Modelo_Relatorio_Final.docx` — Template oficial UNIVESP; seções obrigatórias, formatação ABNT, ficha catalográfica, referências
- `docs/Modelo-Ficha_Tecnica_do_video.docx` — Ficha técnica do vídeo: campos obrigatórios (grupo, polo, curso, orientador, link, descrição 250 palavras)

### Feedback do professor (pontos a corrigir)
- `docs/feedback_professor_relatorio_parcial.md` — Feedback completo do tutor (nota 8,5/10): falta de contexto escolar, justificativa frágil, Resultados e Referências com texto template. **LEITURA OBRIGATÓRIA** para o planner antes de escrever qualquer seção.

### Artefatos GSD — fonte primária de conteúdo
- `.planning/phases/01-infraestrutura/01-01-SUMMARY.md` até `01-03-SUMMARY.md` — o que foi construído na infra
- `.planning/phases/02-autentica-o/` — auth, JWT, reset de senha, decisões de design
- `.planning/phases/03-painel-admin/` — CRUD admin completo
- `.planning/phases/04-portal-do-professor/` — chamada e notas; contexto e SUMMARY
- `.planning/phases/05-portal-do-responsavel/` — boletim, frequência, regra LDB
- `.planning/phases/06-dashboard-e-polish/` — dashboard, skeletons, error handling
- `.planning/phases/07-deploy/07-CONTEXT.md` — Render + Cloudflare Pages, variáveis de ambiente, seed
- `.planning/phases/08-ux-polish/08-CONTEXT.md` — sidebar colapsável, UserMenu, responsividade
- `.planning/STATE.md` — decisões acumuladas do projeto

### Documentação existente (conteúdo aproveitável)
- `docs/api-architecture.md` — Arquitetura da API RESTful; padrões de response
- `docs/database-schema.md` — Schema ER completo do banco; fonte para o diagrama
- `docs/frontend-architecture.md` — Arquitetura do frontend
- `docs/projeto-visao-geral.md` — Visão geral dos módulos (boa fonte para seção de Resultados)
- `docs/Ata 01_02 - Reunião PI Turma 19.md` — Ata inicial com contexto de problema e requisitos iniciais

### Contexto do projeto
- `.planning/PROJECT.md` — Core value, equipe, tutor, polo, contexto acadêmico, decisões chave
- `.planning/ROADMAP.md` — Todas as 10 fases, goals, success criteria, planos executados

</canonical_refs>

<code_context>
## Existing Code Insights

### Sem mudanças no código
Esta fase não altera código-fonte. O planner lê os artefatos GSD como fonte de conteúdo.

### Assets reutilizáveis para o relatório
- `docs/database-schema.md` — Diagrama ER textual já existente; pode ser convertido em figura para o relatório
- `.planning/ROADMAP.md §Progress table` — Tabela de fases completas com datas; útil na seção de Resultados
- `README.md §Equipe` — Lista canônica dos 8 integrantes com nomes completos

### Integration Points
- O conteúdo de `docs/relatorio-final.md` e `docs/roteiro-video.md` (gerados nesta phase) não afeta nenhum sistema em execução — são documentos estáticos no repositório

</code_context>

<specifics>
## Specific Ideas

- O roteiro do vídeo deve cobrir explicitamente os 6 critérios de avaliação do AVA: identificação do grupo, apresentação do problema, apresentação da solução em funcionamento, implementação na comunidade externa, uso de recursos (slides/imagens), respeito ao tempo 5-10 minutos
- A descrição de 250 palavras para a Ficha Técnica deve ser derivada do conteúdo do roteiro (não repetir o resumo do relatório — são documentos separados)
- Entrevista com Elizabete Ap. Godoy de Toledo (professora rede municipal, 08/03/2026, Valinhos SP) deve aparecer na Introdução como evidência de validação da necessidade real do sistema
- O relatório final está **vinculado** à entrega do vídeo — a nota do relatório depende que o vídeo exista no YouTube no momento da correção

</specifics>

<deferred>
## Deferred Ideas

- Conversão automática do Markdown para Word/PDF com formatação ABNT (pandoc + template) — plausível mas complexidade extra desnecessária dado o prazo de 6 dias
- Vídeo editado com narração de tela automatizada — fora do escopo do GSD; é trabalho da equipe gravar e editar

</deferred>

---

*Phase: 10-relatorio-e-roteiro*
*Context gathered: 2026-05-13*
