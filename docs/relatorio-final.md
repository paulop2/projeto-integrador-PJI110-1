# Sistema Web de Registro Escolar: Uma Solução para Acompanhamento de Desempenho por Responsáveis

> **Nota:** A equipe deve definir o título final antes da impressão. A sugestão acima pode ser ajustada.

---

## Identificação

**Instituição:** Universidade Virtual do Estado de São Paulo — UNIVESP
**Curso:** Bacharelado em Ciência da Computação
**Disciplina:** Projeto Integrador em Computação I (PJI110) — Turma 004
**Polo:** Valinhos — SP
**Orientador:** Edson Ricardo Nunes Nascimento
**Período:** 1º semestre de 2026
**Prazo de entrega:** 2026-05-19

> **Link do vídeo:** [INSERIR LINK YOUTUBE APÓS UPLOAD]

---

## Integrantes

| Nome | RA |
|------|----|
| Luiz Eduardo Rodrigues Firmino | [RA] |
| Thalita Fernanda Rospendowski Mazzini | [RA] |
| Rafael Gustavo Leite | [RA] |
| Luiz Henrique de Toledo | [RA] |
| Diego Miguel Mafra | [RA] |
| Nicholas Prado de Sousa Medeiros | [RA] |
| Paulo Vitor de Souza | [RA] |
| Leonardo Matheus Anselmo Matiazzo | [RA] |

> **Nota:** A equipe deve preencher os Registros Acadêmicos (RA) antes da submissão no AVA.

---

## Resumo

Este trabalho apresenta o desenvolvimento de um sistema web de registro escolar voltado ao acompanhamento do desempenho acadêmico por responsáveis. O problema foi identificado por meio de entrevista realizada em 08 de março de 2026 com a professora Elizabete Ap. Godoy de Toledo, docente da rede municipal de ensino de Valinhos-SP, que revelou que o acesso dos responsáveis a notas e frequência dos alunos ocorre exclusivamente por meio de boletins impressos entregues bimestralmente, cadernetas de papel e bilhetes transportados pelos próprios alunos, sem qualquer canal digital sistemático. Para pais que precisam verificar dados fora do período de entrega de boletim, a única alternativa é comparecer presencialmente à escola. O sistema desenvolvido oferece três portais de acesso — administrador, professor e responsável — acessíveis de qualquer dispositivo com navegador, permitindo que os responsáveis acompanhem notas por bimestre e percentual de frequência dos filhos sem necessidade de deslocamento. O desenvolvimento foi conduzido de forma iterativa em 10 fases sequenciais, com commits atômicos por tarefa, testes automatizados com pytest no backend, verificação de compilação TypeScript no frontend e deploy contínuo via integração entre GitHub, Render e Cloudflare Pages. O sistema está disponível em produção em https://projeto-integrador.pages.dev desde 12 de maio de 2026. Como limitações do protótipo, destacam-se o uso do banco de dados SQLite — adequado para demonstração, mas sem suporte a alta concorrência — e o comportamento efêmero do banco no Render free tier, em que os dados são recriados a cada novo deploy. O impacto esperado é reduzir a dependência de deslocamentos e da intermediação dos alunos para que pais e responsáveis acompanhem o progresso escolar dos filhos de forma contínua e acessível.

**Palavras-chave:** sistema de informação escolar; desenvolvimento web; React; FastAPI; acompanhamento escolar.

---

## Sumário

1. Introdução
2. Desenvolvimento
   - 2.1 Objetivos
   - 2.2 Justificativa e Delimitação do Problema
   - 2.3 Fundamentação Teórica
   - 2.4 Aplicação das Disciplinas
   - 2.5 Metodologia
3. Resultados: Solução Final
4. Considerações Finais
5. Referências

---

## 1 Introdução

O presente projeto integrador foi desenvolvido em parceria com uma escola pública da rede municipal de ensino de Valinhos-SP. Para identificar as necessidades reais da comunidade escolar, a equipe realizou, em 08 de março de 2026, uma entrevista semiestruturada com a professora Elizabete Ap. Godoy de Toledo, docente da rede municipal de Valinhos-SP. A entrevista revelou que o registro acadêmico — notas e frequência dos alunos — é gerenciado por meio de cadernetas de papel preenchidas pelos professores, sendo os dados compilados em boletins impressos entregues aos responsáveis a cada bimestre. [A equipe deve inserir o nome da escola e o número aproximado de alunos matriculados quando disponíveis — usar "[NOME DA ESCOLA]" e "[NÚMERO DE ALUNOS]" como referência.]

O estado atual da comunicação entre a escola e os responsáveis pelos alunos é caracterizado pela ausência de um canal digital sistemático. As informações acadêmicas são transmitidas primordialmente por três meios: boletins impressos entregues bimestralmente, cadernetas de papel consultadas no ambiente escolar e bilhetes transportados pelos próprios alunos. Pais que desejam verificar notas ou frequência dos filhos fora do período de entrega do boletim precisam comparecer pessoalmente à escola ou aguardar o próximo ciclo bimestral. Não existe mecanismo de comunicação digital que permita consulta remota e assíncrona por parte dos responsáveis.

Esse cenário apresenta fragilidades identificadas durante a análise de necessidades: em primeiro lugar, a baixa visibilidade em tempo real sobre a frequência escolar — um aluno pode acumular faltas suficientes para reprovação (abaixo de 75%, conforme o art. 24, VI, da Lei n.º 9.394, de 1996) sem que o responsável seja alertado em tempo hábil para intervir. Em segundo lugar, a intermediação dos próprios alunos como canal de comunicação entre escola e responsáveis introduz risco de perda ou não entrega das informações. Em terceiro lugar, a correção de um erro de nota exige que o responsável compareça presencialmente à instituição, tornando o processo moroso e dependente de disponibilidade de horário.

Com o objetivo de atender às demandas identificadas na entrevista, este projeto desenvolveu um sistema web de registro escolar com três portais de acesso distintos: o portal do administrador, para gerenciamento da estrutura da escola (alunos, turmas, disciplinas, professores e responsáveis); o portal do professor, para registro de chamada e lançamento de notas por turma e bimestre; e o portal do responsável, para consulta de boletim e frequência dos filhos de qualquer dispositivo com acesso à internet, sem necessidade de deslocamento até a escola. O sistema está disponível publicamente em https://projeto-integrador.pages.dev, com auto-deploy configurado a partir do repositório GitHub da equipe.

Este relatório está organizado da seguinte forma: a seção 2 apresenta os objetivos, a justificativa, a fundamentação teórica, a aplicação das disciplinas do curso e a metodologia de desenvolvimento adotada. A seção 3 descreve os resultados obtidos — funcionalidades implementadas por fase, métricas do sistema e indicações de capturas de tela para inserção na versão Word. A seção 4 traz as considerações finais, incluindo limitações do protótipo e perspectivas de trabalhos futuros. As referências bibliográficas encerram o documento.

---

## 2 Desenvolvimento

### 2.1 Objetivos

O objetivo geral deste projeto é desenvolver um sistema web de registro escolar que permita a pais e responsáveis acompanhar o desempenho acadêmico dos filhos — notas por bimestre e frequência por disciplina — sem necessidade de deslocamento até a escola, utilizando qualquer dispositivo com acesso à internet.

Os objetivos específicos foram organizados a partir dos 29 requisitos v1 levantados durante a análise de necessidades:

a) **Painel administrativo:** implementar CRUD completo para gestão de alunos, turmas, disciplinas, professores, responsáveis e vínculos entre professor e turma, permitindo ao administrador escolar manter a estrutura da escola sem acesso direto ao banco de dados (ADMIN-01 a ADMIN-06);

b) **Portal do professor:** implementar funcionalidades de registro de chamada por turma e data, lançamento de notas por aluno, disciplina e bimestre (1º ao 4º), e visualização de resumo de frequência por turma, com controle de acesso restrito às turmas vinculadas ao professor autenticado (PROF-01 a PROF-05);

c) **Portal do responsável:** implementar visualização de boletim com notas organizadas por disciplina e bimestre, cálculo automático de média, percentual de frequência e alerta visual quando a frequência cai abaixo de 75%, conforme o limiar estabelecido pelo art. 24, VI, da Lei de Diretrizes e Bases da Educação Nacional (RESP-01 a RESP-06);

d) **Infraestrutura e deploy:** configurar o ambiente de desenvolvimento com backend FastAPI, frontend React, banco de dados SQLite e migrations Alembic, e realizar o deploy do sistema em infraestrutura de nuvem com acesso público e redesploy automático via integração contínua com o repositório GitHub (INFRA-01 a INFRA-05, DEPLOY-01).

---

### 2.2 Justificativa e Delimitação do Problema

A comunicação entre escola e responsáveis na escola parceira de Valinhos-SP ocorre, segundo a entrevista realizada com a professora Elizabete Ap. Godoy de Toledo, por meio de três canais principais: cadernetas de papel preenchidas pelos professores com registros de notas e observações; boletins impressos entregues bimestralmente aos alunos para que levem aos responsáveis; e bilhetes avulsos transportados pelos próprios alunos para comunicar eventos, ocorrências ou solicitações específicas. Ligações telefônicas ocorrem esporadicamente para situações urgentes, mas não há qualquer canal digital sistemático de comunicação ou consulta remota de dados acadêmicos.

Esse modelo apresenta três fragilidades fundamentais que este projeto pretende mitigar. A primeira é a falta de visibilidade em tempo real sobre a frequência escolar: entre uma entrega de boletim e a próxima, um aluno pode acumular faltas suficientes para atingir o limite de reprovação estabelecido pelo art. 24, VI, da Lei n.º 9.394/1996 — que exige frequência mínima de 75% do total de horas letivas — sem que o responsável seja informado em tempo hábil para tomar alguma medida. A segunda fragilidade é a dependência da intermediação do próprio aluno como canal de transmissão de informações: bilhetes podem não chegar ao destinatário, seja por esquecimento, extravio ou omissão deliberada. A terceira é a necessidade de deslocamento presencial para verificar ou contestar uma nota, o que impõe ônus de tempo e deslocamento a responsáveis com rotinas de trabalho que não coincidem com o horário de atendimento escolar.

A delimitação do sistema desenvolvido é intencional e reflete as necessidades identificadas na escola parceira: o sistema atende a uma escola específica (sem suporte a múltiplas escolas no mesmo banco de dados), com foco nos perfis de administrador, professor e responsável — alunos não possuem login no sistema. O acesso é web-first, sem aplicativo móvel nativo (escopo de versões futuras). A modalidade de ensino atendida é o [Ensino Fundamental — a equipe deve confirmar a modalidade exata com a escola parceira].

O sistema resolve cada fragilidade identificada de forma direta: o portal do responsável disponibiliza acesso 24 horas por dia, 7 dias por semana, a notas e frequência atualizadas, sem necessidade de comparecimento à escola; o alerta visual automático é exibido quando a frequência de qualquer disciplina cai abaixo de 75% (RESP-04), permitindo intervenção antes do fim do período letivo; o dashboard do professor exibe resumo de frequência por turma (PROF-05), facilitando a identificação de alunos em risco; e o administrador pode corrigir notas diretamente pelo painel (ADMIN-01), sem que o responsável precise ir à escola para registrar a solicitação de correção.

---

### 2.3 Fundamentação Teórica

Os sistemas de informação para gestão escolar — conhecidos como SIEs (Sistemas de Informação Educacional) — são ferramentas de software que centralizam e automatizam o registro, a consulta e o processamento de dados acadêmicos em instituições de ensino. Conforme apontam Laudon e Laudon (2020), sistemas de informação gerenciais têm como finalidade coletar, processar e distribuir informações que apoiem a tomada de decisão em organizações. No contexto escolar, esses sistemas substituem registros manuais em papel por interfaces digitais que tornam os dados acessíveis a múltiplos atores — professores, administradores e responsáveis — de forma simultânea e remota.

A arquitetura do backend foi concebida seguindo os princípios da Transferência de Estado Representacional (REST), definidos por Fielding (2000) em sua tese de doutoramento como um estilo arquitetural para sistemas de hipermídia distribuídos. Nessa abordagem, cada recurso do domínio (alunos, turmas, chamadas, notas) é identificado por uma URI única, e as operações sobre esses recursos são mapeadas nos verbos HTTP padrão (GET para leitura, POST para criação, PUT para atualização, DELETE para remoção). O uso de REST permite que frontend e backend sejam desenvolvidos e implantados de forma independente, e que a API possa ser consumida por qualquer cliente HTTP, incluindo futuros aplicativos móveis.

O frontend foi construído com React, biblioteca JavaScript de código aberto mantida pela Meta Open Source (2024) para a construção de interfaces de usuário baseadas em componentes reutilizáveis. O padrão de Single Page Application (SPA) adotado permite que a interface responda a interações do usuário sem recarregamentos completos da página, proporcionando uma experiência mais fluida. O gerenciamento de estado de servidor foi implementado com TanStack Query 5, que abstrai o cache de requisições HTTP e a invalidação automática de dados após mutações.

A Lei de Diretrizes e Bases da Educação Nacional estabelece, em seu art. 24, VI, que "será exigida a frequência mínima de setenta e cinco por cento do total de horas letivas para aprovação" (Brasil, 1996). Esse critério legal é o fundamento direto do requisito RESP-04, que exige a exibição de alerta visual quando a frequência do aluno em qualquer disciplina cai abaixo desse limiar. O sistema calcula o percentual de frequência como a razão entre o número de presenças registradas e o total de chamadas realizadas para a turma na disciplina, e exibe um badge de alerta no portal do responsável quando o valor calculado é inferior a 75%.

A autenticação do sistema utiliza o padrão JSON Web Token (JWT), especificado na RFC 7519 por Jones et al. (2015), que define um formato compacto e autocontido para transmissão segura de declarações entre partes como um objeto JSON assinado. O token é gerado no login com um prazo de expiração de 7 dias, armazenado no localStorage do navegador e incluído automaticamente em todas as requisições subsequentes via cabeçalho Authorization. O mecanismo de renovação automática — implementado por meio de um interceptor no cliente HTTP — renova o token ao detectar um cabeçalho X-New-Token na resposta, sem exigir que o usuário faça login novamente. O desenvolvimento iterativo adotado neste projeto segue os princípios do desenvolvimento ágil descritos por Schwaber e Sutherland (2020) no Scrum Guide, com entregas incrementais verificáveis ao final de cada fase do ciclo de desenvolvimento.

---

### 2.4 Aplicação das Disciplinas

O desenvolvimento deste projeto integrador mobilizou conhecimentos de diversas disciplinas do curso de Bacharelado em Ciência da Computação da UNIVESP, demonstrando na prática a integração entre fundamentos teóricos e aplicação técnica em um sistema funcional. O quadro a seguir relaciona cada disciplina às decisões de implementação e às fases do projeto em que os conhecimentos foram aplicados.

> **Nota para a equipe:** revisar esta tabela — remover disciplinas não cursadas pelo grupo e adicionar as que faltarem. A lista foi elaborada com base nas disciplinas do currículo de Computação UNIVESP verificadas publicamente.

| Disciplina UNIVESP | Como aplicada no PI | Fase(s) |
|---|---|---|
| Algoritmos e Programação de Computadores | Lógica de negócio em Python: cálculo de média por bimestre (aprovado se média >= 5,0), percentual de frequência (presenças / total de chamadas × 100), renovação automática de JWT por janela deslizante | 2, 4, 5 |
| Banco de Dados | Modelagem ER com 11 tabelas, constraints de chave estrangeira, índices UNIQUE para integridade referencial, migrations versionadas com Alembic, consultas via SQLAlchemy 2.0 (síncrono); regras de negócio na service layer, não em triggers | 1, 2, 3, 4, 5 |
| Programação para Web | Backend FastAPI (Python 3.12), Frontend React 19 + TypeScript + Vite + Tailwind CSS v3; SPA com React Router 6 para navegação client-side; TanStack Query 5 para cache e sincronização de estado de servidor | 1–8 |
| Engenharia de Software | Processo iterativo em 10 fases com dependências explícitas; controle de versão Git com commits atômicos por tarefa; testes automatizados com pytest (backend); verificação de build TypeScript (frontend); CI/CD com GitHub Actions + Render + Cloudflare Pages; documentação de requisitos e arquitetura | Todas |
| Interação Humano-Computador (IHC) | Mensagens de erro em português via toasts Sonner; skeleton loading em todas as telas para feedback de carregamento; sidebar admin colapsável com hamburger button para uso em dispositivos móveis; alertas visuais de risco LDB com role="alert"; componente UserMenu com avatar de iniciais e dropdown acessível em todos os perfis | 6, 8, 9 |
| Projeto Integrador em Computação I | Integração de todas as disciplinas em um sistema funcional real, validado junto a membro da comunidade escolar (entrevista com Elizabete Ap. Godoy de Toledo, professora da rede municipal de Valinhos-SP, em 08/03/2026) | Todas |

---

### 2.5 Metodologia

O desenvolvimento do sistema foi conduzido de forma iterativa, organizado em 10 fases sequenciais com dependências explícitas entre si: infraestrutura de código → autenticação → entidades cadastrais (painel admin) → portal do professor → portal do responsável → dashboard e polish → deploy em produção → UX polish → notificações → documentação e relatório. Cada fase foi precedida por uma etapa de pesquisa e levantamento de decisões de implementação, seguida pelo planejamento em tarefas atômicas, execução com commits individuais por tarefa e verificação dos critérios de conclusão. Esse processo é análogo ao ciclo de sprints do Scrum (Schwaber; Sutherland, 2020), com a diferença de que o critério de passagem para a fase seguinte é baseado em critérios de sucesso técnicos verificáveis, e não em iterações de tempo fixo.

O controle de versão foi realizado com Git, com todos os commits armazenados em repositório GitHub público. Cada tarefa de desenvolvimento gerou um commit atômico com mensagem padronizada no formato `tipo(fase-plano): descrição concisa`, permitindo rastreabilidade direta entre código e plano de execução. O backend foi validado por testes automatizados escritos com pytest, cobrindo os endpoints de cada perfil de usuário, as regras de controle de acesso (IDOR prevention — retorno 403 para dados de outro aluno) e os cálculos de média e frequência. O frontend passou por verificação de compilação TypeScript (`tsc -b && vite build`) após cada fase, garantindo ausência de erros de tipo antes do deploy. O deploy contínuo foi configurado para disparar automaticamente a cada push para o branch `master`: o frontend via GitHub Actions com `cloudflare/wrangler-action@v3`, e o backend via webhook nativo do Render.

A coleta de requisitos utilizou como técnica primária a entrevista semiestruturada com a professora Elizabete Ap. Godoy de Toledo, realizada em 08 de março de 2026, em Valinhos-SP. A entrevista identificou os principais pontos de dor do modelo atual de comunicação escola-responsável e validou a relevância de um sistema digital como solução. A análise das informações coletadas resultou em 29 requisitos v1 organizados em 7 grupos funcionais: INFRA (infraestrutura), AUTH (autenticação), ADMIN (painel administrativo), PROF (portal do professor), RESP (portal do responsável), DASH (dashboard) e DEPLOY (implantação em produção). Todos os 29 requisitos v1 foram implementados no ciclo de desenvolvimento descrito neste relatório.

As métricas de execução do projeto, registradas no arquivo STATE.md do repositório, indicam: 10 fases planejadas, sendo 8 concluídas até a data de produção deste relatório (fases 9 e 10 em andamento); aproximadamente 24 planos de execução realizados; 11 tabelas no banco de dados; 3 perfis de usuário distintos; deploy ativo em dois ambientes de produção desde 12 de maio de 2026.

---

## 3 Resultados: Solução Final

O sistema web de registro escolar foi implementado em sua totalidade e encontra-se disponível em produção desde 12 de maio de 2026, acessível publicamente pelo endereço https://projeto-integrador.pages.dev. O backend FastAPI está hospedado no Render Web Service (https://projeto-integrador-pji110-1.onrender.com), e o frontend React está hospedado no Cloudflare Pages, com redesploy automático configurado para ambas as plataformas a cada push para o branch `master` do repositório GitHub.

As subseções a seguir detalham as funcionalidades entregues em cada fase, as métricas do sistema e as indicações de capturas de tela para inserção na versão Word do relatório.

### 3.1 Funcionalidades Implementadas por Fase

| Fase | Período | Funcionalidade Entregue | Requisitos |
|------|---------|------------------------|------------|
| 1 — Infraestrutura | 2026-04-26 | Backend FastAPI configurado com SQLAlchemy 2.0 + SQLite (WAL mode, foreign keys ON); Frontend React 19 + TypeScript + Vite + Tailwind CSS; 11 tabelas criadas via migrations Alembic; CORS configurado; seed de admin; Makefile de desenvolvimento | INFRA-01 a INFRA-05 |
| 2 — Autenticação | 2026-04-27 | Login JWT com 3 perfis (admin, professor, responsável); token armazenado em localStorage com prazo de 7 dias e renovação automática via cabeçalho X-New-Token; recuperação de senha por e-mail (Mailtrap sandbox); redirecionamento automático por perfil após login | AUTH-01 a AUTH-06 |
| 3 — Painel Admin | 2026-04-27 | CRUD completo de 6 entidades: alunos, turmas, disciplinas, professores, responsáveis e vínculo professor/turma; modais de criação e edição; confirmação de desativação; suite de testes pytest verde | ADMIN-01 a ADMIN-06 |
| 4 — Portal do Professor | 2026-04-27 | Registro de chamada por turma/data com toggles de presença/falta; lançamento de notas por aluno/disciplina/bimestre (1º ao 4º); resumo de frequência por turma com percentual por aluno; controle de acesso por turma vinculada (ownership check) | PROF-01 a PROF-05 |
| 5 — Portal do Responsável | 2026-04-27 | Boletim com notas por disciplina/bimestre; cálculo automático de média; percentual de frequência; alerta visual LDB quando frequência < 75%; badge de status Aprovado/Reprovado; verificação de IDOR (retorno 403 para dados de outro aluno) | RESP-01 a RESP-06 |
| 6 — Dashboard e Polish | 2026-04-28 | Dashboard com médias e frequência agregadas por turma para admin e professor; skeleton loading em todas as telas; toast de erros em português via Sonner; alertas LDB visuais destacados | DASH-01 |
| 7 — Deploy | 2026-05-12 | Backend no Render Web Service (free tier); frontend no Cloudflare Pages; redesploy automático via GitHub Actions (frontend) e webhook nativo Render (backend); seed de dados de demonstração criado via migration Alembic | DEPLOY-01 |
| 8 — UX Polish | 2026-05-12 | Sidebar admin colapsável com hamburger button; componente UserMenu reutilizável (avatar com iniciais + nome + tipo + botão de logout) padronizado em todos os perfis; tabelas com scroll horizontal para legibilidade em dispositivos móveis | UX-01 |

### 3.2 Métricas do Sistema

- **10 fases** planejadas; 8 implementadas e verificadas até a data deste relatório (fases 9 e 10 em andamento)
- **29 requisitos v1** mapeados e implementados
- **11 tabelas** no banco de dados: `usuarios`, `professores`, `responsaveis`, `alunos`, `turmas`, `disciplinas`, `professor_turma`, `chamadas`, `presencas`, `avaliacoes`, `notas`
- **3 perfis de acesso** com controle baseado em claims do JWT (`tipo`: admin, professor, responsavel)
- **2 ambientes de produção** ativos desde 2026-05-12:
  - Backend: https://projeto-integrador-pji110-1.onrender.com
  - Frontend: https://projeto-integrador.pages.dev
- **Auto-deploy** configurado: push para o branch `master` dispara redesploy automático em ambas as plataformas

### 3.3 Capturas de Tela (Figuras)

As figuras a seguir devem ser inseridas no documento Word como Figuras numeradas, com legenda abaixo de cada imagem seguindo o formato "Figura N — Descrição (Fonte: elaborado pelos autores, 2026)".

> **Figura 1** — Tela de login em https://projeto-integrador.pages.dev/login — ponto de entrada único para os três perfis de usuário (admin, professor, responsável).
>
> [Equipe: capturar screenshot da tela de login e inserir aqui no Word]

> **Figura 2** — Painel administrativo — listagem de alunos com botões de edição e desativação via modal de confirmação.
>
> [Equipe: capturar screenshot do painel admin em /admin]

> **Figura 3** — Portal do professor — aba de chamada com toggles de presença/falta por aluno, seletor de turma e data.
>
> [Equipe: capturar screenshot da aba Chamada no portal do professor]

> **Figura 4** — Portal do responsável — boletim com notas por disciplina/bimestre, médias calculadas automaticamente e badges de status (Aprovado/Reprovado/Em risco).
>
> [Equipe: capturar screenshot do boletim em /responsavel]

> **Figura 5** — Painel de alertas — banner de risco de reprovação por frequência abaixo de 75%, exibido no topo do portal do responsável.
>
> [Equipe: capturar screenshot do painel de alertas no portal do responsável]

> **Figura 6** — Diagrama de arquitetura ER — estrutura das 11 tabelas do banco de dados e seus relacionamentos:

```
usuarios
    |
    +--< professores
    |
    +--< responsaveis --< alunos
                              |
turmas >------------------+   |
    |                         |
    +--< chamadas --< presencas
    |         |
    |         +-- professor_id
    |
    +--< avaliacoes --< notas
              |
              +-- disciplina_id
              +-- professor_id

disciplinas (independente)
```

---

## 4 Considerações Finais

O sistema web de registro escolar desenvolvido neste projeto integrador cumpre o objetivo central estabelecido desde a análise de necessidades realizada junto à escola parceira de Valinhos-SP: pais e responsáveis podem acompanhar o desempenho acadêmico dos filhos — notas por bimestre e percentual de frequência por disciplina — sem precisar se deslocar até a escola. Todos os 29 requisitos v1 foram implementados e verificados, e o sistema está acessível em produção pública desde 12 de maio de 2026. A entrevista com a professora Elizabete Ap. Godoy de Toledo, em 08 de março de 2026, forneceu a evidência empírica de que o problema identificado é real e relevante para a comunidade escolar de Valinhos-SP.

O protótipo apresenta limitações documentadas que são aceitáveis para o contexto acadêmico e de demonstração, mas que deveriam ser endereçadas em uma versão de produção real: (a) o banco de dados SQLite foi adotado pela simplicidade de configuração, mas não oferece suporte adequado a alta concorrência de leituras e escritas simultâneas — em um ambiente com muitos professores registrando chamadas ao mesmo tempo, o mecanismo de lock do SQLite pode introduzir latência; (b) o Render free tier não possui disco persistente, o que significa que o banco de dados é recriado a cada novo deploy a partir do seed de demonstração (`migration 0002_seed_demo_data.py`) — dados inseridos manualmente entre deploys são perdidos; (c) o serviço de e-mail está configurado com o Mailtrap sandbox, que não entrega e-mails reais em produção — para uso real, seria necessário configurar um servidor SMTP de produção (SendGrid, Amazon SES ou similar).

Os trabalhos futuros mais relevantes, mapeados nos requisitos v2 do projeto, incluem: exportação do boletim em PDF diretamente pelo portal do responsável (REL-01); notificações por e-mail automáticas quando a frequência de um aluno cai abaixo de 75%, enviadas ao responsável sem que ele precise verificar o portal ativamente (NOTF-02); desenvolvimento de uma interface mobile nativa (MOB-01); e suporte a múltiplas escolas no mesmo banco de dados (multi-tenant), atualmente fora do escopo por exigir mudanças arquiteturais significativas.

O projeto demonstrou que é possível, dentro do período de uma disciplina de Projeto Integrador, conceber, implementar, testar e publicar em produção um sistema web funcional com múltiplos perfis de acesso, autenticação JWT, testes automatizados e integração contínua — integrando na prática os conhecimentos de Algoritmos e Programação, Banco de Dados, Programação para Web, Engenharia de Software e Interação Humano-Computador adquiridos ao longo do curso de Bacharelado em Ciência da Computação da UNIVESP. O contato com a comunidade escolar por meio da entrevista com a professora Elizabete reforça que o desenvolvimento de software, quando ancorado em um problema real identificado junto aos usuários finais, tem maior potencial de gerar impacto positivo fora do ambiente acadêmico.

---

## Referências

BRASIL. *Lei de Diretrizes e Bases da Educação Nacional*. Lei n.º 9.394, de 20 de dezembro de 1996. Brasília: Presidência da República, 1996. Disponível em: https://portal.mec.gov.br/seesp/arquivos/pdf/lei9394_ldbn1.pdf. Acesso em: 13 maio 2026.

DATE, Christopher J. *Introdução a Sistemas de Banco de Dados*. 8. ed. Rio de Janeiro: Elsevier, 2004. (verificar acesso)

FIELDING, Roy Thomas. *Architectural Styles and the Design of Network-based Software Architectures*. Tese (Doutorado em Informática) — University of California, Irvine, 2000. Disponível em: https://ics.uci.edu/~fielding/pubs/dissertation/top.htm. Acesso em: 13 maio 2026.

JONES, Michael et al. *JSON Web Token (JWT)*. RFC 7519. Internet Engineering Task Force (IETF), 2015. Disponível em: https://tools.ietf.org/html/rfc7519. Acesso em: 13 maio 2026.

LAUDON, Kenneth C.; LAUDON, Jane P. *Sistemas de informação gerenciais*. 14. ed. São Paulo: Pearson Education do Brasil, 2020. (verificar acesso)

META OPEN SOURCE. *React: A JavaScript library for building user interfaces*. Documentação oficial. Disponível em: https://react.dev. Acesso em: 13 maio 2026.

PRESSMAN, Roger S. *Engenharia de software: uma abordagem profissional*. 8. ed. Porto Alegre: AMGH, 2016. (verificar acesso)

RAMÍREZ, Sebastián. *FastAPI: Modern, fast (high-performance), web framework for building APIs with Python*. Documentação oficial. Disponível em: https://fastapi.tiangolo.com. Acesso em: 13 maio 2026.

SCHWABER, Ken; SUTHERLAND, Jeff. *The Scrum Guide*. Scrum.org, 2020. Disponível em: https://scrumguides.org/docs/scrumguide/v2020/2020-Scrum-Guide-PortugueseBR.pdf. Acesso em: 13 maio 2026.

---

> **Nota:** As referências marcadas com "(verificar acesso)" acima são obras canônicas nas respectivas áreas. Caso a equipe não tenha acesso à edição mencionada, substituir por material disponível no Portal CAPES Periódicos ou pela edição disponível na biblioteca digital da UNIVESP.
