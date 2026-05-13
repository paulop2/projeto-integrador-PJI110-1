# Phase 10: Relatório e Roteiro - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-13
**Phase:** 10-relatorio-e-roteiro
**Areas discussed:** Template e formato de entrega, Conteúdo gerado vs esqueleto, Divisão do roteiro entre integrantes, Profundidade técnica do relatório

---

## Template e formato de entrega

| Option | Description | Selected |
|--------|-------------|----------|
| Sim, tem template específico | URL ou arquivo do template | ✓ |
| Não, estrutura livre | Apenas os critérios de sucesso | |
| Não sei / verificar com tutor | Criar estrutura e confirmar depois | |

**User's choice:** Tem template específico — `docs/Modelo_Relatorio_Final.docx`

---

| Option | Description | Selected |
|--------|-------------|----------|
| Google Docs | Criado e entregue no Google Docs | |
| PDF a partir de Word/Docs | Documento Word exportado como PDF | ✓ |
| Markdown no repositório | Relatório como arquivo .md no repo | |

**User's choice:** PDF a partir de Word/Docs

---

| Option | Description | Selected |
|--------|-------------|----------|
| Sim, vou compartilhar o link | Template acessível para referência | |
| Não tenho, mas sei as seções | Ditar seções obrigatórias | |
| Usar seções dos critérios de sucesso | Planner organiza baseado nos critérios | |

**User's choice (free text):** "Acabei de adicionar relatorio_final e ficha técnica do video no /docs. estão em formato docx"
**Notes:** Templates encontrados em `docs/Modelo_Relatorio_Final.docx` e `docs/Modelo-Ficha_Tecnica_do_video.docx`. Estrutura extraída: Resumo (250 palavras), 1 Introdução, 2 Desenvolvimento (2.1-2.5), 3 Resultados, 4 Considerações finais, Referências.

**Informação adicional (final da discussão):** User compartilhou os requisitos do AVA para entrega do vídeo (Q7). Prazo: 2026-05-19 23:59. Vídeo postado no YouTube, link na capa do relatório + AVA. Entrega PDF via AVA (um integrante envia). Critérios: identificação do grupo, apresentação do problema, solução em funcionamento, implementação/impacto, recursos, tempo 5-10 min.

---

## Conteúdo gerado vs esqueleto

| Option | Description | Selected |
|--------|-------------|----------|
| Rascunho completo pronto para revisar | Texto de todas as seções dos artefatos GSD | ✓ |
| Esqueleto detalhado com prompts | Seções com instruções para cada integrante | |
| Só Introdução + Resultados, resto placeholder | Seções difíceis geradas; resto placeholder | |

**User's choice:** Rascunho completo

---

| Option | Description | Selected |
|--------|-------------|----------|
| Markdown no repositório | `docs/relatorio-final.md` | ✓ |
| Diretamente no template Word | Equipe insere manualmente | |
| Google Docs | Colaborativo, copiado para Doc | |

**User's choice:** Markdown no repositório (`docs/relatorio-final.md`)

---

| Option | Description | Selected |
|--------|-------------|----------|
| Markdown no repo | `docs/roteiro-video.md` | |
| Preencher direto na Ficha Técnica | Conteúdo transferido para .docx | |
| Ambos (Markdown detalhado + resumo na Ficha) | Script completo + descrição sintética | ✓ |

**User's choice:** Ambos — `docs/roteiro-video.md` com script completo + resumo de 250 palavras para Ficha Técnica

---

| Option | Description | Selected |
|--------|-------------|----------|
| Tenho fontes definidas | Referências já definidas | |
| Planner sugere fontes relevantes | Sugestões em NBR:10520:2023 | ✓ |
| Seção mínima / espaço reservado | Placeholder para equipe preencher | |

**User's choice:** Planner sugere fontes relevantes (sistemas web escolares, React/FastAPI, LDB, metodologia ágil) em formato NBR:10520:2023

---

## Divisão do roteiro entre integrantes

| Option | Description | Selected |
|--------|-------------|----------|
| Sim, compartilho agora | Nomes + papéis definidos | |
| Não, só somos 8 | Slots genéricos, equipe distribui | |
| Tenho parte, compartilho o que sei | Alguns nomes confirmados | |

**User's choice (free text):** "Os integrantes estão no relatório. transforma o pdf em markdown. os nomes das pessoas no projeto também estão no readme."
**Notes:** PDF do relatório parcial estava comprimido (ilegível por CLI). Nomes encontrados no README: 8 integrantes listados com nomes completos. Tutor: Edson Ricardo Nunes Nascimento.

---

| Option | Description | Selected |
|--------|-------------|----------|
| Por perfil funcional | Admin/Professor/Responsável/Infra | |
| Por fase do projeto | Cada um apresenta as phases que trabalhou | |
| Planner decide divisão equilibrada | Baseado nos 8 nomes e funcionalidades | ✓ |

**User's choice:** Planner decide divisão equilibrada

---

## Profundidade técnica do relatório

| Option | Description | Selected |
|--------|-------------|----------|
| Sim, trechos-chave como exemplos | Código ilustrativo | |
| Não, só descrição textual | Texto sobre decisões técnicas | |
| Diagrama de arquitetura em vez de código | ER do banco + fluxo de autenticação | ✓ |

**User's choice:** Diagramas de arquitetura (ER + fluxo JWT)

---

| Option | Description | Selected |
|--------|-------------|----------|
| Tenho fontes definidas | Listar disciplinas agora | |
| Não sei de cor, verificar | Placeholder para equipe | |
| Usar as óbvias do projeto | Planner infere, equipe valida | ✓ |

**User's choice:** Planner infere disciplinas (BD, Prog. Web, Algoritmos, Eng. Software, IHC)

---

| Option | Description | Selected |
|--------|-------------|----------|
| Sim, screenshots como figuras | Indicar telas a capturar na seção Resultados | ✓ |
| Não, só descrever as telas por texto | Relatório mais leve | |
| Planner decide estratégia | 3-4 screenshots estratégicos | |

**User's choice:** Sim, screenshots como figuras na seção Resultados

---

## Claude's Discretion

- Título exato do trabalho (equipe define)
- Número de páginas total estimado
- RAs dos integrantes (planner deixa `[RA]` como placeholder)
- Fontes bibliográficas específicas (planner sugere, equipe confirma acesso)
- Distribuição de tempo por seção no roteiro de vídeo

## Deferred Ideas

- Conversão automática Markdown → Word com pandoc e template ABNT — complexidade extra desnecessária para o prazo
- Vídeo com narração automatizada — responsabilidade da equipe gravar/editar
