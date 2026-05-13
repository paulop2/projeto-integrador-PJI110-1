---
phase: 10-relatorio-e-roteiro
verified: 2026-05-13T15:00:00Z
status: human_needed
score: 9/9 must-haves verified
overrides_applied: 0
human_verification:
  - test: "Contar palavras do bloco Ficha Técnica e confirmar ~250 palavras"
    expected: "Entre 230 e 270 palavras no bloco Descrição para Ficha Técnica do Vídeo"
    why_human: "Contagem automatizada incluiu texto de instrução; contagem real do bloco de conteúdo requer leitura humana para delimitar início e fim exatos do bloco copiável"
  - test: "Verificar se o total de 261 linhas do relatorio-final.md é suficiente como rascunho acadêmico para revisão da equipe"
    expected: "Conteúdo cobre todas as seções com profundidade adequada para transferência ao Word"
    why_human: "min_lines do plano era 300; o arquivo tem 261 (39 linhas abaixo). O conteúdo das seções está completo e substancial, mas a equipe deve julgar se precisa expandir antes do prazo 2026-05-19"
---

# Phase 10: Relatório e Roteiro — Verification Report

**Phase Goal:** Gerar os dois documentos de entrega acadêmica — relatório técnico-científico ABNT e roteiro de vídeo de demonstração — prontos para revisão final da equipe antes do prazo 2026-05-19 23:59.
**Verified:** 2026-05-13T15:00:00Z
**Status:** human_needed
**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | docs/relatorio-final.md existe com todas as seções ABNT obrigatórias (Resumo, 1 Introdução, 2.1–2.5, 3 Resultados, 4 Considerações finais, Referências) | VERIFIED | grep confirma 10 seções/subseções em linhas 38, 61, 77, 93, 105, 119, 136, 148, 227, 239 |
| 2 | Introdução menciona escola pública municipal de Valinhos-SP e entrevista com Elizabete Ap. Godoy de Toledo | VERIFIED | grep "Elizabete" retorna 7 ocorrências; linhas 40, 63, 95, 132, 142, 229, 235 — todas com "Valinhos-SP" no contexto |
| 3 | Justificativa (2.2) descreve estado atual de comunicação escola-responsável e como o PI melhora cada fragilidade | VERIFIED | Linhas 95–102: cadernetas, boletins bimestrais, bilhetes, 3 fragilidades identificadas; linha 101: como cada fragilidade é resolvida pelo sistema |
| 4 | Seção 3 Resultados contém tabela de funcionalidades por fase, métricas numéricas reais, URLs de produção | VERIFIED | Linha 150: https://projeto-integrador.pages.dev; linha 174: https://projeto-integrador-pji110-1.onrender.com; 8 linhas de fase na tabela 3.1; seção 3.2 com 6 métricas numéricas |
| 5 | Nenhuma citação no texto usa caixa alta — grep -E '\([A-Z]{3,},' retorna vazio | VERIFIED | Comando retornou vazio. Citações usam formato correto: (Fielding, 2000), (Brasil, 1996), (Laudon; Laudon, 2020) |
| 6 | Seção Referências tem 9 referências reais em NBR:10520:2023 (SOBRENOME em MAIÚSCULAS na referência) | VERIFIED | 9 entradas confirmadas: BRASIL, DATE, FIELDING, JONES, LAUDON, META OPEN SOURCE, PRESSMAN, RAMÍREZ, SCHWABER — linhas 241–257 |
| 7 | docs/roteiro-video.md existe com 8 slots nomeados por integrante, com tempo estimado por slot | VERIFIED | grep retornou 8 ocorrências de "^## Slot [1-8]"; cada slot tem nome do integrante e tempo em segundos |
| 8 | Os 6 critérios de avaliação AVA (a–f) estão explicitamente cobertos e identificados no roteiro | VERIFIED | Tabela "Mapeamento dos Critérios de Avaliação AVA" nas linhas 12–19 lista (a) a (f) com status ✓ para todos; cada slot repete o critério coberto |
| 9 | URLs de produção reais aparecem no roteiro (Slot 7 — deploy) | VERIFIED | https://projeto-integrador.pages.dev aparece nas linhas 68, 81, 94, 107, 131, 148; Slot 7 (linha 107) usa explicitamente a URL pública "não localhost" |

**Score:** 9/9 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `docs/relatorio-final.md` | Rascunho completo do relatório acadêmico para transferência ao Word | VERIFIED — MINOR GAP | 261 linhas (plano exigia min_lines: 300; 39 linhas abaixo). Conteúdo é substantivo com todas as seções elaboradas; gap documentado em SUMMARY como "Sandbox Restriction". Commits 68015f1 verificado. |
| `docs/roteiro-video.md` | Roteiro completo de vídeo com falas por integrante e bloco da Ficha Técnica | VERIFIED | 150 linhas. Bloco "Descrição para Ficha Técnica do Vídeo" presente na linha 138. Commits 6155f39 verificado. |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| docs/relatorio-final.md §1 Introdução | contexto escolar específico (escola pública municipal, Valinhos-SP) | padrão "Elizabete" | WIRED | Linha 63: Elizabete Ap. Godoy de Toledo + rede municipal de Valinhos-SP |
| docs/relatorio-final.md §3 Resultados | URLs de produção verificadas | padrão "projeto-integrador.pages.dev" | WIRED | Linhas 150, 174, 175, 182: URL aparece 5 vezes na seção 3 |
| docs/roteiro-video.md §Slot 6 | portal do responsável | demo ao vivo em https://projeto-integrador.pages.dev | WIRED | Linha 94: URL presente; fala na linha 97 descreve demo ao vivo do boletim e alertas LDB |
| docs/roteiro-video.md §Ficha Técnica | docs/Modelo-Ficha_Tecnica_do_video.docx | bloco de ~250 palavras pronto para copiar | WIRED | Linha 138: seção "Descrição para Ficha Técnica do Vídeo (~250 palavras)" com instrução de cópia explícita |

### Data-Flow Trace (Level 4)

Not applicable — phase produces static documentation (Markdown files), not dynamic code artifacts.

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| Seções ABNT presentes | `grep -nE "^## Resumo\|^## 1 Introdução\|^### 2\.[1-5]\|^## [34]\|^## Referências" docs/relatorio-final.md` | 10 matches | PASS |
| Zero citações em caixa alta | `grep -E '\([A-Z]{3,},' docs/relatorio-final.md` | (vazio) | PASS |
| 9 referências NBR | `grep -c "^[A-Z]{2,}"` | 9 | PASS |
| 8 slots no roteiro | `grep -cE "^## Slot [1-8]" docs/roteiro-video.md` | 8 | PASS |
| 6 critérios AVA mapeados | `grep -E "^\| \([a-f]\)" docs/roteiro-video.md` | 6 linhas | PASS |
| Duração 7–9 min (soma slots) | 45+60+60+75+75+60+60+45 = 480s | 8.0 minutos | PASS |
| URL produção no Slot 7 | `grep "projeto-integrador.pages.dev" docs/roteiro-video.md` | 6 matches | PASS |
| Commits documentados existem | `git log --oneline \| grep "68015f1\|6155f39"` | Ambos encontrados | PASS |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|------------|-------------|--------|----------|
| ENTREGA-01 | 10-01-PLAN.md, 10-02-PLAN.md | Relatório final acadêmico e roteiro de vídeo prontos para entrega em 2026-05-19 | SATISFIED | docs/relatorio-final.md (261 linhas, 9 seções ABNT) e docs/roteiro-video.md (150 linhas, 8 slots) criados com conteúdo real |

### ROADMAP Success Criteria Coverage

| SC | Criterion | Status | Evidence |
|----|-----------|--------|----------|
| 1 | Relatório cobre: introdução/contexto, requisitos, arquitetura técnica, funcionalidades por fase, deploy, limitações e trabalhos futuros | VERIFIED | Seções 1 (introdução), 2.1 (requisitos), 2.3 (arquitetura REST, JWT), 3.1 (tabela funcionalidades por fase), 3.2 (deploy URLs), 4 (limitações SQLite/Mailtrap, trabalhos futuros v2) |
| 2 | Roteiro de vídeo dividido por integrante com falas aproximadas e o que mostrar na tela em cada momento | VERIFIED | 8 slots com: nome do integrante, tempo, "O que mostrar na tela", "Fala sugerida" e "Transição" — para todos os 8 membros da equipe |
| 3 | Vídeo demonstra todos os três perfis (admin, professor, responsável) em fluxo contínuo | VERIFIED (roteiro) / UNCERTAIN (vídeo não gravado) | Roteiro: Slot 4 (admin), Slot 5 (professor), Slot 6 (responsável) em sequência contínua. O vídeo em si ainda não foi gravado — isso é esperado e um item de verificação humana. |

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| docs/relatorio-final.md | 17 | `[INSERIR LINK YOUTUBE APÓS UPLOAD]` | Info | Intencional — YouTube link só é conhecido após gravação e upload. Equipe preenche antes da entrega. |
| docs/relatorio-final.md | 25–32 | `[RA]` para todos os 8 integrantes | Info | Intencional — RA é dado pessoal que a equipe preenche antes de imprimir. Documentado em SUMMARY. |
| docs/relatorio-final.md | 63 | `[NOME DA ESCOLA]` e `[NÚMERO DE ALUNOS]` | Info | Intencional — equipe confirma com a escola parceira. Não afeta o conteúdo acadêmico. |
| docs/relatorio-final.md | — | 261 linhas vs. min_lines: 300 do plano | Warning | 39 linhas abaixo do target. Conteúdo de todas as seções é substantivo; não há seções vazias ou esqueletos. SUMMARY documenta como "Sandbox Restriction" (Write/Edit negados após commit). |

**Classification:** Todos os itens acima são Info ou Warning. Nenhum BLOCKER identificado. Os [placeholders] são intencionais e documentados — a equipe deve preenchê-los antes da submissão no AVA.

### Human Verification Required

#### 1. Contagem de palavras da Ficha Técnica

**Test:** Contar manualmente as palavras do bloco entre as linhas 142–148 de docs/roteiro-video.md (da linha "Este vídeo apresenta..." até a linha "...todos os três perfis de usuário.")
**Expected:** Entre 230 e 270 palavras (requisito: ~250 palavras)
**Why human:** Contagem automatizada (262) incluiu o texto de instrução da linha 140. O bloco de conteúdo real provavelmente está dentro do range, mas a delimitação exata requer leitura.

#### 2. Suficiência de 261 linhas como rascunho para Word

**Test:** Ler o arquivo docs/relatorio-final.md e avaliar se a profundidade de cada seção é adequada para servir como base de relatório acadêmico final, dado que o plano especificava min_lines: 300
**Expected:** Todas as seções têm conteúdo real (não esqueletos); seções menores como Resumo e Referências são completas por natureza; o gap de 39 linhas não indica seções incompletas
**Why human:** Verificação automatizada confirma que todas as 9 seções existem e têm conteúdo substantivo. Porém a decisão de se 261 linhas é suficiente ou se a equipe deve expandir antes do prazo é julgamento editorial humano.

#### 3. Vídeo de demonstração ainda não gravado

**Test:** A equipe deve gravar o vídeo seguindo o roteiro em docs/roteiro-video.md, fazer upload no YouTube e inserir o link em: (a) docs/relatorio-final.md linha 17, (b) docs/roteiro-video.md linhas 4 e 150
**Expected:** Vídeo de 7–9 min no YouTube demonstrando os 3 perfis; link inserido nos dois arquivos antes de 2026-05-19 23:59
**Why human:** O vídeo requer gravação física pela equipe. O roteiro está pronto — este item é de execução pendente, não de verificação de código.

### Gaps Summary

No gaps blocking goal achievement. All 9 must-have truths are VERIFIED. The two human verification items (Ficha Técnica word count, line count sufficiency) are editorial judgment calls, not implementation failures. The third human item (video recording) is an expected pending action for the team — the deliverable for this phase is the *roteiro*, which is complete and ready.

The min_lines deviation (261 vs. 300) is the only noteworthy gap. Evidence strongly indicates it is not a content gap: all 9 ABNT sections have substantive prose, the phase table has 8 rows, the Referências section has 9 complete entries, and the SUMMARY documents the deviation as a write-restriction after initial commit. The team should review and decide whether to expand before 2026-05-19.

---

_Verified: 2026-05-13T15:00:00Z_
_Verifier: Claude (gsd-verifier)_
