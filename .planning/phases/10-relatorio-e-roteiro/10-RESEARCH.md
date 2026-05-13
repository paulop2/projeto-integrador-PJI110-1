# Phase 10: Relatório e Roteiro - Research

**Researched:** 2026-05-13
**Domain:** Academic report writing (ABNT/UNIVESP) + video script production
**Confidence:** HIGH (all structural findings verified against CONTEXT.md decisions and source files)

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

- D-01: Estrutura obrigatória — Capa, Folha de rosto, Ficha catalográfica, Resumo (250 palavras) + Palavras-chave, Sumário, 1 Introdução, 2 Desenvolvimento (2.1 Objetivos · 2.2 Justificativa · 2.3 Fundamentação teórica · 2.4 Aplicação das disciplinas · 2.5 Metodologia), 3 Resultados, 4 Considerações finais, Referências
- D-02: Output como `docs/relatorio-final.md` (Markdown rascunho); formatação Word é responsabilidade da equipe
- D-03: Vídeo no YouTube, 5-10 min, prazo 2026-05-19 23:59
- D-04: Ficha Técnica inclui nomes/RAs (placeholder [RA]), polo Valinhos, curso, disciplina PJI110, orientador Edson Ricardo Nunes Nascimento, título, link YouTube, descrição 250 palavras
- D-05: Relatório e vídeo entregues juntos no AVA
- D-06: Rascunho COMPLETO — sem placeholders genéricos. Fonte primária: SUMMARY.md phases 1-8, CONTEXT.md, DISCUSSION-LOG.md, STATE.md, PROJECT.md
- D-07: Fundamentação teórica (2.3) com citações NBR:10520:2023 (sem caixa alta: `(Fielding, 2000)`, não `(FIELDING, 2000)`)
- D-08: Seção 2.4 infere disciplinas UNIVESP Computação e relaciona ao que foi construído; equipe valida
- D-09: 8 integrantes confirmados (ver lista em CONTEXT.md)
- D-10: 8 slots de fala equilibrados, estrutura sugerida em CONTEXT.md
- D-11: Critérios de avaliação do vídeo (6 itens) cobertos explicitamente no roteiro
- D-12: Sem código no corpo — usar diagramas de arquitetura como figuras
- D-13: Screenshots estratégicos na seção 3 Resultados — planner indica quais capturar
- D-14: Introdução DEVE descrever contexto escolar: escola pública municipal, Valinhos SP; entrevista 08/03/2026 com Elizabete Ap. Godoy de Toledo
- D-15: Justificativa (2.2) deve responder como comunicação escola-responsável acontece hoje e como o PI melhora isso
- D-16: Seção 3 Resultados com conteúdo real: funcionalidades, screenshots, métricas
- D-17: Referências NBR:10520:2023; citações no texto sem caixa alta

### Claude's Discretion

- Título exato do trabalho (usar placeholder — equipe decide)
- Número de páginas total (estimativa 15-25 páginas)
- RA de cada integrante (usar [RA] como placeholder)
- Fonte exata das referências (planner sugere, equipe confirma acesso)
- Tempo exato de cada seção no roteiro (distribuir 7-8 min proporcionalmente)

### Deferred Ideas (OUT OF SCOPE)

- Conversão automática Markdown → Word/PDF com pandoc
- Vídeo editado com narração automatizada
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| ENTREGA-01 | Relatório final acadêmico e roteiro de vídeo prontos para entrega em 2026-05-19 | Estrutura ABNT verificada, mapeamento artefato→seção documentado, divisão de 8 slots de fala especificada, feedback do professor tratado ponto a ponto |
</phase_requirements>

---

## Summary

Phase 10 é puramente documental: produzir dois arquivos Markdown — `docs/relatorio-final.md` e `docs/roteiro-video.md` — a partir dos artefatos GSD já existentes (SUMMARY.md, CONTEXT.md, STATE.md das phases 1-8). Nenhum código é alterado.

A estrutura do relatório está definida pelo template UNIVESP (`docs/Modelo_Relatorio_Final.docx`), que segue ABNT com seções obrigatórias de Introdução, Desenvolvimento (5 subseções) e Resultados. O feedback do professor (nota 8,5/10) identifica três lacunas críticas: (1) ausência de contextualização da escola parceira, (2) justificativa genérica sem dados sobre o estado atual de comunicação escola-responsável, e (3) seção de Resultados e Referências ainda com texto de template. Cada lacuna tem uma correção determinística mapeada a artefatos existentes.

O roteiro de vídeo segue formato de duas colunas (fala + o que mostrar na tela) com 8 slots distribuídos entre os integrantes, cobrindo os 6 critérios de avaliação do AVA. A duração total é de 7-8 minutos dentro do limite 5-10 min.

**Primary recommendation:** O planner deve gerar o rascunho completo de `docs/relatorio-final.md` mapeando cada seção ABNT a artefatos GSD específicos (tabela abaixo), depois gerar `docs/roteiro-video.md` com slots nomeados por integrante. Zero pesquisa adicional necessária — tudo que o planner precisa já existe nos artefatos do repositório.

---

## Architectural Responsibility Map

Esta fase não tem tiers de software. O mapa abaixo descreve quais artefatos são "donos" de cada seção do relatório.

| Seção do Relatório | Artefato Primário | Artefato Secundário |
|-------------------|-------------------|---------------------|
| 1 Introdução + contexto escolar | `docs/Ata 01_02 - Reunião PI Turma 19.md` + D-14 da CONTEXT.md | README.md §Contexto Acadêmico |
| 2.1 Objetivos | REQUIREMENTS.md §Core Value + v1 Requirements | ROADMAP.md §Overview |
| 2.2 Justificativa e delimitação | `docs/Ata 01_02` + D-15 da CONTEXT.md | feedback_professor_relatorio_parcial.md |
| 2.3 Fundamentação teórica | Referências sugeridas neste RESEARCH.md | STATE.md §Decisions |
| 2.4 Aplicação das disciplinas | Mapeamento disciplinas UNIVESP (neste RESEARCH.md) | REQUIREMENTS.md + ROADMAP.md |
| 2.5 Metodologia | ROADMAP.md §Phases (ordem, dependências, waves) | STATE.md §Performance Metrics |
| 3 Resultados | SUMMARYs de todas as phases + 07-02-SUMMARY.md (URLs produção) | docs/projeto-visao-geral.md |
| 4 Considerações finais | STATE.md + REQUIREMENTS.md §v2 + §Out of Scope | ROADMAP.md §Overview |
| Referências | Lista curada neste RESEARCH.md | D-17 da CONTEXT.md |
| Roteiro vídeo | D-09/D-10/D-11 da CONTEXT.md | 07-02-SUMMARY.md (URLs demo) |

---

## Artifact-to-Section Mapping (deterministic)

Este é o mapa canônico para o planner. Cada seção do relatório tem fonte primária e secundária identificadas com conteúdo específico a extrair.

### Seção 1: Introdução

**O que escrever (requisitos do professor — D-14):**
- Escola parceira: escola pública municipal da rede de Valinhos-SP
- Entrevista em 08/03/2026 com **Elizabete Ap. Godoy de Toledo** (professora da rede municipal, Valinhos SP)
- Estado atual: cadernetas em papel, pais precisam ir à escola para obter notas e frequência, comunicação via bilhetes levados pelos alunos
- Problema: acesso limitado a dados acadêmicos, risco de reprovação por frequência (art. 24, VI, LDB) não comunicado em tempo hábil
- Proposta: sistema web com três portais (admin, professor, responsável) acessível de qualquer dispositivo

**Fontes:**
- `docs/Ata 01_02 - Reunião PI Turma 19.md` — contexto inicial do problema
- `README.md` §Contexto Acadêmico — menção à entrevista com Elizabete
- `docs/feedback_professor_relatorio_parcial.md` — perguntas que a Introdução deve responder (checklist de verificação)

**Métricas para incluir:**
- 8 integrantes, Polo Valinhos, UNIVESP PJI110, Turma 004
- Orientador: Edson Ricardo Nunes Nascimento

---

### Seção 2.1: Objetivos

**O que escrever:**
- Objetivo geral: desenvolver sistema web que permita pais acompanharem notas e frequência dos filhos sem ir à escola
- Objetivos específicos: (a) implementar painel administrativo para CRUD de entidades escolares, (b) portal do professor para registro de chamada e notas, (c) portal do responsável com boletim e alertas LDB, (d) deploy em produção com acesso público

**Fontes:**
- `REQUIREMENTS.md` §Core Value e §v1 Requirements
- `ROADMAP.md` §Overview — lista de phases e goals

---

### Seção 2.2: Justificativa e Delimitação do Problema

**O que escrever (atende ao feedback D-15):**
- Situação atual na escola parceira: registro em cadernetas, notas entregues por boletim impresso bimestral, pais dependem dos alunos para levar bilhetes
- Fragilidades: pais não têm visibilidade em tempo real, alerta de baixa frequência não chega a tempo, correção de erro de nota requer visita à escola
- Delimitação: sistema para uma escola específica (não multi-tenant), Ensino Fundamental, web-first
- Como o PI resolve cada fragilidade: portal do responsável com acesso 24/7, alerta visual de frequência < 75%, dashboard do professor

**Fontes:**
- `docs/Ata 01_02` — resumo do problema original
- `docs/feedback_professor_relatorio_parcial.md` — perguntas 1, 2, 3 do professor (ver p. 1 do doc) são o checklist de validação
- `REQUIREMENTS.md` §Out of Scope — delimita o que NÃO está no escopo

---

### Seção 2.3: Fundamentação Teórica

Ver seção `## Academic References` abaixo com referências completas formatadas em NBR:10520:2023.

**Temas a cobrir:**
1. Sistemas de Informação em Gestão Escolar (SIEs)
2. Arquitetura REST e APIs Web
3. Desenvolvimento Web moderno (SPAs, React)
4. Lei de Diretrizes e Bases (LDB) — art. 24, VI sobre frequência
5. Metodologias ágeis (Scrum)

---

### Seção 2.4: Aplicação das Disciplinas

Ver seção `## UNIVESP Disciplines Mapping` abaixo.

---

### Seção 2.5: Metodologia

**O que escrever:**
- Desenvolvimento iterativo por fases sequenciais (10 fases)
- Cada fase: fase de pesquisa → discussão → planejamento → execução → verificação
- Controle de versão: Git + GitHub (commits atômicos por tarefa)
- Testes: pytest (backend), TypeScript build check (frontend)
- Deploy incremental com CI/CD (GitHub Actions + Render + Cloudflare Pages)
- Coleta de requisitos: entrevista com membro da rede municipal + análise de necessidades

**Fontes:**
- `ROADMAP.md` §Phases — tabela de progresso com datas
- `STATE.md` §Performance Metrics — velocidade de execução (4-20 min por plano, média 6 min)
- `.planning/config.json` — modo de execução (yolo, parallelization)

**Dados concretos para mencionar:**
- 10 fases planejadas, 8 concluídas antes do relatório
- ~24 planos executados no total
- Total de ~0,5 horas de execução automatizada (dado do STATE.md)
- 11 tabelas no banco de dados
- 3 perfis de usuário
- Deploy ativo desde 2026-05-12 em produção pública

---

### Seção 3: Resultados

**O que escrever (atende ao feedback D-16):**

Estruturar como tabela de funcionalidades por fase + screenshots:

| Fase | Funcionalidade Entregue | Requisitos Atendidos |
|------|------------------------|---------------------|
| 1 | Backend FastAPI + frontend React + banco SQLite com 11 tabelas | INFRA-01 a INFRA-05 |
| 2 | Login JWT com 3 perfis + recuperação de senha por email | AUTH-01 a AUTH-06 |
| 3 | CRUD admin: 6 entidades (alunos, turmas, disciplinas, professores, responsáveis, vínculos) | ADMIN-01 a ADMIN-06 |
| 4 | Portal professor: chamada + notas por bimestre + controle de acesso por turma | PROF-01 a PROF-05 |
| 5 | Portal responsável: boletim + frequência + alerta LDB + verificação IDOR | RESP-01 a RESP-06 |
| 6 | Dashboard agregado + skeleton loading + toast de erros | DASH-01 |
| 7 | Deploy Render + Cloudflare Pages + auto-deploy GitHub Actions | DEPLOY-01 |
| 8 | Sidebar colapsável + UserMenu padronizado + tabelas responsivas | UX-01 |

**URLs de produção (verificadas — 07-02-SUMMARY.md):**
- Backend: `https://projeto-integrador-pji110-1.onrender.com`
- Frontend: `https://projeto-integrador.pages.dev`

**Screenshots a indicar (D-13):**
1. Tela de login (`/login`) — mostra ponto de entrada unificado para 3 perfis
2. Painel admin — lista de alunos com CRUD em modal
3. Portal do professor — tab de chamada com toggles presente/ausente
4. Boletim do responsável — tabela com médias e badge de status (aprovado/reprovado)
5. Painel de alertas Phase 9 — banner de risco de reprovação por frequência
6. Dashboard admin — tabela de desempenho por turma

**Fontes:**
- `07-02-SUMMARY.md` — URLs de produção verificadas
- `ROADMAP.md` §Progress — tabela de status de phases
- SUMMARY.md de cada phase — o que foi construído em detalhe

---

### Seção 4: Considerações Finais

**O que escrever:**
- Síntese: sistema funcional atendendo ao core value ("pais acompanham desempenho escolar sem ir à escola")
- 29 requisitos v1 implementados; v2 e mobile fora do escopo do protótipo
- Limitações: SQLite (sem concorrência alta), banco efêmero no Render free tier (seed recriado a cada deploy), email via Mailtrap sandbox (não produção real)
- Trabalhos futuros: exportação PDF do boletim (REL-01), notificações por email reais (NOTF-01), app mobile (MOB-01), multi-escola

**Fontes:**
- `REQUIREMENTS.md` §v2 e §Out of Scope
- `STATE.md` §Resolved e §Blockers/Concerns
- `07-CONTEXT.md` D-01 (banco efêmero — limitação documentada)

---

## Academic References (Seção 2.3)

Referências sugeridas formatadas em NBR:10520:2023. Citações no texto: `(Sobrenome, ano)` — sem caixa alta.

**Regra NBR:10520:2023 [VERIFIED: pucrs.br/biblioteca]:** A partir de 19/07/2023, sobrenome do autor em citações no texto usa apenas a primeira letra maiúscula. Nas **referências** finais o sobrenome permanece em maiúsculas. Exemplos:
- Citação no texto: `(Fielding, 2000, p. 76)`
- Referência final: `FIELDING, Roy Thomas. Architectural Styles...`

### Referências primárias recomendadas

**1. REST / Arquitetura Web**

> FIELDING, Roy Thomas. *Architectural Styles and the Design of Network-based Software Architectures*. Tese (Doutorado) — University of California, Irvine, 2000. Disponível em: https://ics.uci.edu/~fielding/pubs/dissertation/top.htm. Acesso em: 13 maio 2026.

Citação: `(Fielding, 2000)` — [VERIFIED: ics.uci.edu — URL pública, acesso verificado]

**2. LDB — Frequência escolar**

> BRASIL. *Lei de Diretrizes e Bases da Educação Nacional*. Lei n.º 9.394, de 20 de dezembro de 1996. Brasília: Presidência da República, 1996. Disponível em: https://portal.mec.gov.br/seesp/arquivos/pdf/lei9394_ldbn1.pdf. Acesso em: 13 maio 2026.

Citação: `(Brasil, 1996)` — [VERIFIED: portal.mec.gov.br — URL pública]

**3. Sistemas de Informação em Gestão Escolar**

> LAUDON, Kenneth C.; LAUDON, Jane P. *Sistemas de informação gerenciais*. 14. ed. São Paulo: Pearson Education do Brasil, 2020.

Citação: `(Laudon; Laudon, 2020)` — [ASSUMED: obra canônica de SIG; equipe deve confirmar acesso à edição]

**4. Desenvolvimento Web / React**

> META OPEN SOURCE. *React: A JavaScript library for building user interfaces*. Documentação oficial. Disponível em: https://react.dev. Acesso em: 13 maio 2026.

Citação: `(Meta Open Source, 2024)` — [VERIFIED: react.dev — acessível]

**5. FastAPI / Desenvolvimento de APIs Python**

> RAMÍREZ, Sebastián. *FastAPI: Modern, fast (high-performance), web framework for building APIs with Python*. Documentação oficial. Disponível em: https://fastapi.tiangolo.com. Acesso em: 13 maio 2026.

Citação: `(Ramírez, 2024)` — [VERIFIED: fastapi.tiangolo.com — acessível]

**6. Banco de Dados Relacional**

> DATE, Christopher J. *Introdução a Sistemas de Banco de Dados*. 8. ed. Rio de Janeiro: Elsevier, 2004.

Citação: `(Date, 2004)` — [ASSUMED: obra canônica de BD; equipe deve confirmar acesso]

**7. Scrum / Metodologia Ágil**

> SCHWABER, Ken; SUTHERLAND, Jeff. *The Scrum Guide*. Scrum.org, 2020. Disponível em: https://scrumguides.org/docs/scrumguide/v2020/2020-Scrum-Guide-PortugueseBR.pdf. Acesso em: 13 maio 2026.

Citação: `(Schwaber; Sutherland, 2020)` — [VERIFIED: scrumguides.org — PDF oficial em português]

**8. Segurança Web / JWT**

> JONES, Michael et al. *JSON Web Token (JWT)*. RFC 7519. Internet Engineering Task Force (IETF), 2015. Disponível em: https://tools.ietf.org/html/rfc7519. Acesso em: 13 maio 2026.

Citação: `(Jones et al., 2015)` — [VERIFIED: tools.ietf.org — RFC pública]

**9. Engenharia de Software**

> PRESSMAN, Roger S. *Engenharia de software: uma abordagem profissional*. 8. ed. Porto Alegre: AMGH, 2016.

Citação: `(Pressman, 2016)` — [ASSUMED: obra canônica de ES; equipe deve confirmar acesso]

**Nota importante para o planner:** As referências marcadas `[ASSUMED]` são obras canônicas reconhecidas na área. O planner deve incluí-las com a nota "(verificar acesso)" para a equipe confirmar. Caso a equipe não tenha acesso, substituir por material abertamente disponível (e.g., artigos no Google Scholar ou CAPES Periódicos).

---

## UNIVESP Disciplines Mapping (Seção 2.4)

**Contexto:** UNIVESP Computação inclui disciplinas de Algoritmos e Programação, Banco de Dados, Estrutura de Dados, Programação para Web, Engenharia de Software, Interação Humano-Computador, e Projeto Integrador. [VERIFIED: univesp-computacao.github.io/portal-disciplinas/ e assets.univesp.br]

Mapeamento para o que foi construído no PI:

| Disciplina UNIVESP | Como aplicada no PI | Fase(s) |
|-------------------|--------------------|---------| 
| Algoritmos e Programação de Computadores | Lógica de negócio em Python: cálculo de média (>= 5,0), percentual de frequência (count presentes / total chamadas), sliding-window JWT renewal | 2, 4, 5 |
| Banco de Dados | Modelagem ER com 11 tabelas, constraints FK, índices UNIQUE, migrations Alembic, queries SQLAlchemy; sem triggers — regras de negócio na service layer | 1, 2, 3, 4, 5 |
| Programação para Web | Backend FastAPI (Python), Frontend React + TypeScript + Vite + Tailwind; SPA com React Router 6; TanStack Query para cache de servidor | 1, 2, 3, 4, 5, 6, 8 |
| Engenharia de Software | Processo iterativo em fases com dependências explícitas; controle de versão Git; testes automatizados pytest; CI/CD; documentação de requisitos e arquitetura | Todas |
| Interação Humano-Computador (IHC) | Feedback de erro em português (toasts Sonner); skeleton loading; sidebar responsiva com hamburger; alertas visuais LDB; avatar dropdown com acessibilidade (role="alert", aria-live) | 6, 8, 9 |
| Projeto Integrador em Computação I | Integração de todas as disciplinas em sistema real validado com membro da comunidade escolar (entrevista Elizabete, 08/03/2026) | Todas |

**Instrução ao planner:** Incluir na seção 2.4 a tabela acima com parágrafo introdutório explicando que cada disciplina cursada contribuiu para uma ou mais fases do desenvolvimento. A equipe deve revisar e adicionar outras disciplinas que tenha cursado que não aparecem aqui.

---

## Professor Feedback — Checklist de Correção

Cada item do feedback (nota 8,5/10) tem uma correção determinística:

| Ponto do Feedback | Localização no Relatório | Correção Exata |
|------------------|--------------------------|----------------|
| "Qual escola? Pública ou privada? Quantos alunos? Qual modalidade? Onde?" | Introdução (§1) | Inserir: escola pública municipal da rede de Valinhos-SP; entrevista com Elizabete Ap. Godoy de Toledo, professora da rede municipal, em 08/03/2026 |
| "Como o acompanhamento é feito atualmente?" | Introdução (§2) + Justificativa (2.2) | Descrever estado atual: cadernetas, boletins impressos bimestrais, pais buscam informações via alunos ou visitando a escola |
| "Como a comunicação escola-responsável acontece hoje?" | Justificativa (2.2) | Bilhetes levados pelos alunos; ligações pontuais; sem canal digital sistemático |
| "Como o PI melhora isso especificamente?" | Justificativa (2.2) + Resultados (§3) | Portal do responsável: acesso 24/7 a notas e frequência; alerta automático de frequência < 75% (LDB art. 24, VI) |
| "Resultados com texto de template" | Seção 3 | Substituir por conteúdo real (tabela de phases, screenshots, URLs de produção) |
| "Referências com texto de template" | Referências | Substituir por referências reais formatadas em NBR:10520:2023 |
| "Citações em caixa alta (ex: FIELDING, 2000)" | Todo o texto | Usar apenas inicial maiúscula: `(Fielding, 2000)` |
| "Referências no corpo do texto em vez da seção Referências" | Todo o texto | Mover todas as referências para a seção final; usar apenas citações abreviadas no texto |

---

## Video Script Architecture (Seção `docs/roteiro-video.md`)

### Estrutura dos 8 slots (7-8 minutos total)

| Slot | Integrante | Conteúdo | Tela a Mostrar | Tempo estimado |
|------|------------|---------|-----------------|----------------|
| 1 | Luiz Eduardo Rodrigues Firmino | Apresentação do grupo + identificação GID (critério a) | Slide ou câmera — integrantes + polo Valinhos | ~45s |
| 2 | Thalita Fernanda Rospendowski Mazzini | Apresentação do problema e relevância comunitária (critério b) — contexto escola parceira, entrevista Elizabete | Câmera ou slide com foto do contexto | ~60s |
| 3 | Rafael Gustavo Leite | Arquitetura técnica — stack (Python/FastAPI/React/SQLite), diagrama ER simplificado (critério e: uso de recursos visuais) | Slide com diagrama de arquitetura | ~60s |
| 4 | Luiz Henrique de Toledo | Demo perfil Admin — criar turma, cadastrar aluno, vincular professor | Browser em `https://projeto-integrador.pages.dev` — painel admin | ~75s |
| 5 | Diego Miguel Mafra | Demo perfil Professor — registrar chamada, lançar nota | Browser — portal do professor | ~75s |
| 6 | Nicholas Prado de Sousa Medeiros | Demo perfil Responsável — boletim + frequência + alerta LDB (critério c: solução em funcionamento) | Browser — portal do responsável com alerta | ~60s |
| 7 | Paulo Vitor de Souza | Deploy e acesso em produção — mostrar URL pública, auto-deploy GitHub; impacto na comunidade (critério d) | Browser com URL + GitHub Actions log | ~60s |
| 8 | Leonardo Matheus Anselmo Matiazzo | Considerações finais — limitações, trabalhos futuros, respeito ao tempo (critério f) | Câmera ou slide de encerramento | ~45s |

**Total estimado: ~8 minutos 20 segundos** (ajustável — equipe deve cronometrar em ensaio)

### Formato do roteiro por slot

Cada slot no `docs/roteiro-video.md` deve ter:

```markdown
### Slot X — [Nome do Integrante] (~Xs)

**O que mostrar na tela:** [descrição da tela/slide]

**Fala sugerida:**
> "[texto de fala, escrito em português natural]"

**Transição:** "[o que o próximo apresentador deve dizer/mostrar]"
```

### Critérios AVA cobertos explicitamente

| Critério AVA | Slot que cobre |
|-------------|----------------|
| (a) Identificação do grupo | Slot 1 |
| (b) Apresentação do problema e relevância comunitária | Slot 2 |
| (c) Solução em funcionamento | Slots 4, 5, 6 |
| (d) Implementação e impacto na comunidade externa | Slot 7 |
| (e) Uso de slides/imagens/recursos | Slot 3 (diagrama), Slot 1 (slide grupo) |
| (f) Respeito ao tempo 5-10 min | Distribuição ~8 min total |

### Bloco "Descrição para Ficha Técnica" (250 palavras)

O `docs/roteiro-video.md` deve incluir, ao final, um bloco pronto para copiar para a Ficha Técnica:

```markdown
## Descrição para Ficha Técnica do Vídeo (250 palavras)

[texto derivado do roteiro, descrevendo: o problema abordado, a solução desenvolvida,
os perfis demonstrados (admin, professor, responsável), o impacto na comunidade escolar
de Valinhos-SP, e as tecnologias utilizadas — NÃO é o mesmo texto do Resumo do relatório]
```

---

## Don't Hand-Roll

| Problema | Não construir | Usar em vez disso | Por quê |
|----------|--------------|-------------------|---------|
| Diagrama ER | Diagrama do zero | `docs/database-schema.md` já tem diagrama ASCII do ER | Já existe e está correto |
| Lista de integrantes | Pesquisar em outro lugar | `README.md` §Equipe — lista canônica com nomes completos | Fonte de verdade única |
| URLs de produção | Inventar ou buscar | `07-02-SUMMARY.md` — URLs verificadas e ativas | Verificadas em 2026-05-12 |
| Tabela de fases | Escrever do zero | `ROADMAP.md` §Progress — tabela completa com status e datas | Já existe com datas |
| Decisões técnicas | Reconstruir da memória | `STATE.md` §Decisions + `README.md` §Decisões Técnicas | Decisões canônicas |
| Estrutura do relatório | Inferir do zero | `docs/Modelo_Relatorio_Final.docx` + D-01 da CONTEXT.md | Template oficial UNIVESP |

---

## Common Pitfalls

### Pitfall 1: Citações em Caixa Alta
**O que vai errado:** O relatório parcial tinha `(FIELDING, 2000)` — formato NBR:10520:2002 (antigo).
**Por que acontece:** Modelos antigos do Word ou hábito anterior à atualização de julho 2023.
**Como evitar:** Usar sempre `(Sobrenome, ano)` nas citações do texto. Na seção Referências final, o sobrenome vai em MAIÚSCULAS (isso continua igual).
**Sinal de alerta:** Qualquer citação com sobrenome todo em maiúsculas no meio do texto.

### Pitfall 2: Seção 3 Resultados com Conteúdo de Template
**O que vai errado:** Copiar texto do modelo sem substituir pelo conteúdo real do projeto.
**Por que acontece:** A seção de Resultados no template tem texto de exemplo que parece razoável genericamente.
**Como evitar:** A seção 3 DEVE ter: tabela de funcionalidades por fase, métricas numéricas (11 tabelas, 3 perfis, 29 requisitos, 10 phases, 2 URLs de produção), indicações de screenshots, e nenhuma frase que possa se aplicar a outro projeto.

### Pitfall 3: Introdução Genérica (feedback crítico)
**O que vai errado:** "Em muitas escolas, os pais não têm acesso às notas dos filhos..." — sem mencionar a escola específica.
**Por que acontece:** Tendência de generalizar para parecer mais relevante.
**Como evitar:** Primeira menção da escola deve ser específica: escola pública municipal da rede de Valinhos-SP. A entrevista com Elizabete (08/03/2026) deve aparecer como evidência de validação da necessidade.

### Pitfall 4: Referências no Corpo do Texto
**O que vai errado:** Colocar referência bibliográfica completa logo após a citação no parágrafo.
**Por que acontece:** Confusão com notas de rodapé.
**Como evitar:** No texto vai apenas a citação abreviada: `(Fielding, 2000)`. A referência completa vai APENAS na seção "Referências" ao final do documento.

### Pitfall 5: Tempo de Vídeo Estourado
**O que vai errado:** Cada integrante fala mais do que o slot permite e o vídeo passa de 10 minutos.
**Por que acontece:** 8 pessoas × "só mais 30 segundos" = +4 minutos.
**Como evitar:** O roteiro deve incluir tempo estimado por slot. A instrução para a equipe deve dizer: ensaiar e cronometrar antes de gravar. Slots de 45-75 segundos somam ~8 min, deixando 2 min de margem.

### Pitfall 6: Seção 2.4 Inventando Disciplinas
**O que vai errado:** Mencionar disciplinas que o grupo não cursou na UNIVESP.
**Por que acontece:** O planner infere disciplinas prováveis — a equipe deve validar.
**Como evitar:** A seção 2.4 gerada deve ter nota explícita: "A equipe deve revisar e remover disciplinas não cursadas, e adicionar as que faltarem".

---

## State of the Art

| Aspecto | Abordagem Usada no PI | Estado Atual do Mercado | Nota para o Relatório |
|---------|----------------------|------------------------|----------------------|
| Citação ABNT | NBR:10520:2023 (sem caixa alta) | Atualização de julho 2023 | Usar formato novo — verificado |
| JWT Storage | localStorage (7 dias, renovação automática) | Debate ativo (localStorage vs httpOnly cookie) | STATE.md documenta decisão fundamentada para protótipo |
| ORM Approach | SQLAlchemy síncrono | async SQLAlchemy disponível mas com complexidades de lock no SQLite | STATE.md documenta razão da escolha síncrona |
| Frontend State | TanStack Query (servidor) + Context (auth) | Zustand/Jotai também populares; TanStack Query é padrão para cache de servidor | Decisão em 01-03-SUMMARY.md |

---

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Laudon & Laudon (2020) é obra acessível para a equipe | Academic References | Equipe não tem acesso → substituir por artigo disponível no CAPES Periódicos |
| A2 | Pressman (2016) é obra acessível para a equipe | Academic References | Idem → buscar alternativa em acesso aberto |
| A3 | Date (2004) é obra acessível para a equipe | Academic References | Idem → substituir por material do curso COM300 UNIVESP |
| A4 | A escola parceira é de Ensino Fundamental (não Médio ou EJA) | Introdução + Justificativa | Descrição diferente se for outra modalidade — equipe confirma com Elizabete |
| A5 | O estado atual de comunicação é por bilhetes/cadernetas | Introdução + Justificativa | Detalhes reais dependem da entrevista com Elizabete — equipe insere detalhes específicos |
| A6 | As 8 disciplinas UNIVESP listadas foram cursadas por todos ou maioria dos integrantes | Seção 2.4 | Equipe deve revisar — remover as não cursadas, adicionar as faltantes |

---

## Open Questions (RESOLVED)

1. **Título exato do trabalho**
   - O que sabemos: CONTEXT.md D-Claude's Discretion — equipe decide
   - O que falta: decisão da equipe
   - RESOLVED: usar placeholder `[TÍTULO DO TRABALHO]` no rascunho. Sugestão: "Sistema Web de Registro Escolar: Uma Solução para Acompanhamento de Desempenho por Responsáveis"

2. **RA (Registro Acadêmico) de cada integrante**
   - O que sabemos: CONTEXT.md D-04 — usar `[RA]` como placeholder
   - O que falta: equipe preenche na capa e ficha técnica
   - RESOLVED: planner gera tabela com coluna RA vazia para a equipe preencher

3. **Detalhes específicos da escola parceira**
   - O que sabemos: Valinhos-SP, rede municipal, professora Elizabete
   - O que falta: nome da escola, número de alunos, modalidade exata
   - RESOLVED: planner gera com `[NOME DA ESCOLA]`, `[NÚMERO DE ALUNOS]` como placeholders — esses são os únicos placeholders permitidos (não são sobre conteúdo técnico, são dados factuais que só a equipe conhece)

4. **Link do YouTube do vídeo**
   - O que sabemos: vídeo ainda não gravado (fase é simultânea)
   - O que falta: a equipe grava e insere o link
   - RESOLVED: roteiro inclui instrução "[INSERIR LINK YOUTUBE APÓS UPLOAD]" como placeholder na capa do relatório e na Ficha Técnica

5. **Phase 9 (Notificações) concluída antes da entrega?**
   - O que sabemos: STATE.md mostra Phase 9 "Not started" em 2026-05-12; prazo é 2026-05-19
   - O que falta: status real em 2026-05-13
   - RESOLVED: relatorio cobre fases 1-8 como completadas + Phase 9 como "em finalização" se ainda não concluída; planner inclui seção de Resultados que pode ser atualizada para incluir Phase 9 se concluída antes do relatório ser transferido para Word

---

## Environment Availability

Esta fase é puramente documental. Nenhuma dependência externa além do repositório Git.

| Dependência | Requerida por | Disponível | Versão | Fallback |
|-------------|--------------|------------|--------|----------|
| Repositório Git (artefatos GSD) | Fonte de todo conteúdo | ✓ | master | — |
| `docs/Modelo_Relatorio_Final.docx` | Estrutura do relatório | ✓ | — | CONTEXT.md D-01 (estrutura canônica) |
| `docs/Modelo-Ficha_Tecnica_do_video.docx` | Ficha técnica do vídeo | ✓ | — | D-04 da CONTEXT.md |
| `docs/feedback_professor_relatorio_parcial.md` | Checklist de correção | ✓ | — | — |
| URL produção backend | Seção 3 Resultados | ✓ | onrender.com | 07-02-SUMMARY.md |
| URL produção frontend | Seção 3 Resultados | ✓ | pages.dev | 07-02-SUMMARY.md |

**Sem dependências bloqueantes.**

---

## Validation Architecture

`workflow.nyquist_validation` não está definido em `.planning/config.json` — tratado como habilitado.

Esta fase é puramente documental (sem código). Não há testes automatizados. Validação é humana:

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | Arquivo Existe? |
|--------|----------|-----------|-------------------|----------------|
| ENTREGA-01 | `docs/relatorio-final.md` existe e tem todas as seções ABNT | Manual (verificação humana) | `ls docs/relatorio-final.md && grep -c "##" docs/relatorio-final.md` | ❌ Wave 0 |
| ENTREGA-01 | `docs/roteiro-video.md` existe com 8 slots nomeados | Manual | `ls docs/roteiro-video.md && grep -c "Slot" docs/roteiro-video.md` | ❌ Wave 0 |
| ENTREGA-01 | Nenhuma citação em caixa alta no relatório | Semi-automático | `grep -E '\([A-Z]{2,},' docs/relatorio-final.md` (deve retornar vazio) | ❌ Wave 0 |
| ENTREGA-01 | Seção 3 tem conteúdo real (não template) | Manual | Grep por "texto de exemplo" ou "insira aqui" | ❌ Wave 0 |

### Wave 0 Gaps

- [ ] `docs/relatorio-final.md` — a ser criado em 10-01-PLAN.md
- [ ] `docs/roteiro-video.md` — a ser criado em 10-02-PLAN.md

### Sampling Rate

- **Por plano:** verificação manual do arquivo gerado (estrutura de seções, ausência de placeholders genéricos, ausência de citações em caixa alta)
- **Gate do phase:** ambos os arquivos existem + checklist de feedback do professor verificado

---

## Security Domain

`security_enforcement` não configurado em `.planning/config.json` — mas esta fase é puramente documental, sem código. ASVS não aplicável.

---

## Sources

### Primary (HIGH confidence)
- `.planning/phases/10-relatorio-e-roteiro/10-CONTEXT.md` — Decisões canônicas da fase, fonte primária de todos os D-NN
- `.planning/phases/07-deploy/07-02-SUMMARY.md` — URLs de produção verificadas
- `docs/feedback_professor_relatorio_parcial.md` — Feedback do professor, pontos de correção obrigatórios
- `README.md` — Lista canônica da equipe, tutor, polo, stack
- `REQUIREMENTS.md` — Requisitos v1 e v2, rastreabilidade

### Secondary (MEDIUM confidence)
- [Biblioteca PUCRS — NBR:10520:2023 atualização](https://biblioteca.pucrs.br/noticias/atualizacao-da-norma-de-citacoes-da-abnt-nbr-10520-julho-2023/) — mudança de caixa alta para inicial maiúscula
- [UNIVESP Regulamento PI 2023](https://apps.univesp.br/manual-do-aluno/assets/docs/Regulamento_para_o_Projeto_Integrador_jun_2023.pdf) — estrutura de avaliação, peso do relatório (60%)
- [UNIVESP PJI110 plano de ensino](https://assets.univesp.br/blackboard/plano-de-ensino/disciplinas/PJI110.html) — disciplina específica
- [univesp-computacao.github.io/portal-disciplinas](https://univesp-computacao.github.io/portal-disciplinas/) — lista de disciplinas do curso
- [portal.mec.gov.br — LDB Lei 9.394/1996](https://portal.mec.gov.br/seesp/arquivos/pdf/lei9394_ldbn1.pdf) — art. 24, VI, frequência mínima 75%
- [ics.uci.edu — Fielding dissertation 2000](https://ics.uci.edu/~fielding/pubs/dissertation/top.htm) — referência REST canônica, URL verificada

### Tertiary (LOW confidence)
- WebSearch sobre estrutura de roteiro de vídeo — contexto geral, não específico ao AVA UNIVESP

---

## Metadata

**Confidence breakdown:**
- Estrutura ABNT: HIGH — verificada contra CONTEXT.md D-01 e template existente no repositório
- Mapeamento artefato→seção: HIGH — todos os artefatos foram lidos e verificados como existentes
- Referências acadêmicas: MEDIUM — URLs primárias verificadas; obras impressas marcadas [ASSUMED]
- Divisão de vídeo (8 slots): HIGH — nomes confirmados de README.md, critérios AVA de D-11 CONTEXT.md
- Disciplinas UNIVESP 2.4: MEDIUM — lista verificada em univesp-computacao.github.io mas equipe deve validar quais cursou

**Research date:** 2026-05-13
**Valid until:** 2026-05-19 (prazo de entrega — pesquisa não precisa ser renovada)
