# Roteiro do Vídeo de Demonstração
## Sistema Web de Registro Escolar — PJI110 Turma 004 — UNIVESP Polo Valinhos

**Link do vídeo:** [INSERIR LINK DO YOUTUBE APÓS UPLOAD]
**Duração estimada:** ~8 minutos (dentro do limite de 5 a 10 minutos)
**Plataforma:** YouTube (não listado ou público — decisão da equipe)

---

## Mapeamento dos Critérios de Avaliação AVA

| Critério AVA | Slot que cobre | Status |
|---|---|---|
| (a) Identificação do grupo | Slot 1 — Luiz Eduardo | ✓ |
| (b) Apresentação do problema e relevância comunitária | Slot 2 — Thalita | ✓ |
| (c) Solução em funcionamento | Slots 4, 5, 6 — Luiz Henrique, Diego, Nicholas | ✓ |
| (d) Implementação e impacto na comunidade externa | Slot 7 — Paulo Vitor | ✓ |
| (e) Uso de slides/imagens/recursos | Slot 1 (slide grupo), Slot 3 (diagrama arquitetura) | ✓ |
| (f) Respeito ao tempo 5-10 min | Distribuição ~8 min total (ver tempos por slot) | ✓ |

> **Instrução à equipe:** ensaiar o roteiro completo e cronometrar antes de gravar. Cada integrante deve ler sua fala em voz alta no ritmo natural de apresentação. Ajuste os textos conforme necessário — o roteiro é um ponto de partida, não uma leitura literal.

---

## Slot 1 — Luiz Eduardo Rodrigues Firmino (~45 segundos)
**Critério AVA coberto:** (a) Identificação do grupo | (e) Uso de recursos visuais

**O que mostrar na tela:**
Slide de apresentação do grupo com: nome do projeto, lista dos 8 integrantes (com foto opcional), polo Valinhos, disciplina PJI110 Turma 004, UNIVESP.

**Fala sugerida:**
> "Olá, bom dia! Somos o grupo da Turma 004 da disciplina Projeto Integrador em Computação I da UNIVESP, Polo Valinhos. Nosso grupo é formado por Luiz Eduardo Rodrigues Firmino, Thalita Fernanda Rospendowski Mazzini, Rafael Gustavo Leite, Luiz Henrique de Toledo, Diego Miguel Mafra, Nicholas Prado de Sousa Medeiros, Paulo Vitor de Souza e Leonardo Matheus Anselmo Matiazzo. Nosso projeto é o Sistema Web de Registro Escolar — uma solução para que pais e responsáveis acompanhem o desempenho escolar dos filhos sem precisar ir até a escola. Vou passar a palavra para a Thalita, que vai apresentar o problema que nos motivou."

**Transição:** Thalita assume o microfone ou narração.

---

## Slot 2 — Thalita Fernanda Rospendowski Mazzini (~60 segundos)
**Critério AVA coberto:** (b) Apresentação do problema e relevância comunitária

**O que mostrar na tela:**
Câmera voltada para a apresentadora, ou slide com: foto ou ícone de escola pública, legenda "Escola Municipal — Valinhos, SP", e bullets com o problema atual (cadernetas, bilhetes, boletim bimestral).

**Fala sugerida:**
> "O projeto surgiu de uma necessidade real identificada em uma escola pública municipal da rede de ensino de Valinhos. Em março de 2026, entrevistamos a professora Elizabete Ap. Godoy de Toledo, docente da rede municipal, para entender como funciona o registro escolar hoje. O que descobrimos é que as notas são registradas em cadernetas de papel, os boletins são entregues impressos apenas uma vez por bimestre, e a comunicação com os pais acontece principalmente por bilhetes levados pelos próprios alunos. Isso significa que um aluno pode acumular faltas suficientes para ser reprovado — a lei exige presença mínima de 75% — sem que o responsável saiba a tempo de agir. Nosso projeto resolve exatamente isso."

**Transição:** Rafael assume para apresentar a arquitetura técnica.

---

## Slot 3 — Rafael Gustavo Leite (~60 segundos)
**Critério AVA coberto:** (e) Uso de slides e recursos visuais — diagrama de arquitetura

**O que mostrar na tela:**
Slide com o diagrama de arquitetura do sistema: três camadas — Frontend (React + Vite + Tailwind, hospedado no Cloudflare Pages), Backend (FastAPI + Python, hospedado no Render), Banco de Dados (SQLite com 11 tabelas). Mostrar as setas de comunicação REST API + JWT.

**Fala sugerida:**
> "Tecnicamente, o sistema é dividido em duas partes: um backend construído com Python e FastAPI, que expõe uma API REST, e um frontend em React com TypeScript, que consome essa API. A autenticação usa tokens JWT com três perfis de acesso: administrador, professor e responsável. O banco de dados é SQLite com onze tabelas, gerenciadas com o ORM SQLAlchemy e migrations Alembic. O sistema está em produção: o backend roda no Render e o frontend no Cloudflare Pages, com deploy automático a cada atualização no GitHub. Agora o Luiz Henrique vai mostrar o sistema funcionando ao vivo pelo perfil de administrador."

**Transição:** Luiz Henrique abre o navegador na URL de produção.

---

## Slot 4 — Luiz Henrique de Toledo (~75 segundos)
**Critério AVA coberto:** (c) Solução em funcionamento — demo perfil Admin

**O que mostrar na tela:**
Navegador aberto em https://projeto-integrador.pages.dev/login. Fazer login como admin (usar credenciais do seed demo — admin@escola.dev / admin123 ou conforme configurado). Navegar para o painel admin e mostrar: lista de alunos, criar ou editar uma turma em modal, mostrar listagem de disciplinas.

**Fala sugerida:**
> "Aqui estou no sistema em produção. Vou entrar com o perfil de administrador. [faz login] Após o login, o sistema me direciona automaticamente para o painel de administração. Aqui posso gerenciar toda a estrutura da escola: cadastrar alunos, criar turmas, adicionar disciplinas e vincular professores às turmas. [mostra a lista de alunos] Por exemplo, vou abrir o modal de edição de um aluno para mostrar que os dados podem ser atualizados diretamente pelo painel, sem precisar acessar o banco de dados. [demonstra o modal] O administrador também cria as contas de professores e responsáveis e faz os vínculos entre responsáveis e seus filhos. Vou agora passar para o Diego, que vai mostrar o portal do professor."

**Transição:** Diego faz login com credenciais de professor.

---

## Slot 5 — Diego Miguel Mafra (~75 segundos)
**Critério AVA coberto:** (c) Solução em funcionamento — demo perfil Professor

**O que mostrar na tela:**
Navegador em https://projeto-integrador.pages.dev/login. Fazer login como professor (usar credenciais do seed demo). Navegar para portal do professor: mostrar lista de turmas vinculadas, entrar em uma turma, mostrar a aba de Chamada com toggles de presença, depois mostrar a aba de Notas com lançamento por bimestre.

**Fala sugerida:**
> "Agora vou demonstrar o portal do professor. [faz login como professor] Após o login como professor, vejo apenas as turmas às quais estou vinculado — professores não têm acesso a outras turmas. [clica em uma turma] Dentro da turma, tenho três abas: Chamada, Notas e Frequência. [abre aba Chamada] Na chamada, marco presença ou falta para cada aluno clicando nos botões — o sistema registra a data automaticamente. [abre aba Notas] Para lançar notas, seleciono o bimestre e insiro a nota de cada aluno por disciplina. O sistema valida que a nota está dentro do limite máximo. [abre aba Frequência] Na aba de frequência, vejo o percentual de presença de cada aluno — isso me ajuda a identificar quem está em risco de reprovação. O sistema calcula tudo automaticamente. Passo agora para o Nicholas, que vai mostrar como o responsável vê essas informações."

**Transição:** Nicholas faz login como responsável.

---

## Slot 6 — Nicholas Prado de Sousa Medeiros (~60 segundos)
**Critério AVA coberto:** (c) Solução em funcionamento — demo perfil Responsável + alerta LDB

**O que mostrar na tela:**
Navegador em https://projeto-integrador.pages.dev/login. Fazer login como responsável (usar credenciais do seed demo). Mostrar o boletim do filho: tabela de notas por disciplina/bimestre com médias calculadas e badges Aprovado/Reprovado. Se disponível após Phase 9, mostrar o painel de alertas de frequência.

**Fala sugerida:**
> "Agora vou mostrar o portal do responsável — a peça central do projeto. [faz login como responsável] Ao entrar, vejo o boletim do meu filho com as notas organizadas por disciplina e bimestre. O sistema calcula a média automaticamente — não preciso fazer nada manualmente. [aponta para as colunas] Aqui está a frequência em percentual. Se a frequência de alguma disciplina estiver abaixo de setenta e cinco por cento, o sistema exibe um alerta destacado — isso implementa a regra da Lei de Diretrizes e Bases, artigo 24. O responsável recebe essa informação em tempo real, sem precisar ir à escola. O sistema também mostra o status de aprovado ou reprovado com base na média calculada. Passo para o Paulo Vitor, que vai falar sobre o deploy e o impacto do projeto."

**Transição:** Paulo Vitor assume.

---

## Slot 7 — Paulo Vitor de Souza (~60 segundos)
**Critério AVA coberto:** (d) Implementação e impacto na comunidade externa | (c) Sistema em funcionamento — produção

**O que mostrar na tela:**
Navegador mostrando a URL pública https://projeto-integrador.pages.dev (não localhost). Depois mostrar rapidamente o repositório GitHub com o histórico de commits ou o log do GitHub Actions com o deploy automático.

**Fala sugerida:**
> "O sistema que acabamos de demonstrar não está rodando localmente — está em produção pública, acessível a partir de qualquer dispositivo com internet. O frontend está hospedado no Cloudflare Pages, em projeto-integrador.pages.dev, e o backend está no Render. Cada vez que fazemos um commit no GitHub, o deploy é feito automaticamente — aqui no GitHub Actions você pode ver o histórico de deploys. [mostra o log] O impacto para a comunidade escolar é direto: a escola parceira de Valinhos pode adotar o sistema e os responsáveis passam a ter acesso às informações dos filhos de qualquer lugar, a qualquer hora, sem depender de bilhetes ou visitas presenciais. Passo a palavra para o Leonardo, que vai fechar com as considerações finais."

**Transição:** Leonardo assume para encerramento.

---

## Slot 8 — Leonardo Matheus Anselmo Matiazzo (~45 segundos)
**Critério AVA coberto:** (f) Respeito ao tempo — encerramento dentro dos 10 minutos

**O que mostrar na tela:**
Slide de encerramento com: nome do projeto, equipe, logotipo UNIVESP, agradecimentos, link do YouTube (inserir após upload) e e-mail ou contato para dúvidas (opcional).

**Fala sugerida:**
> "Para encerrar, o Sistema Web de Registro Escolar entregou todas as funcionalidades planejadas para o v1: administração completa, registro de chamada e notas pelo professor, e acompanhamento de boletim e frequência pelo responsável — tudo em produção e acessível publicamente. As limitações do protótipo incluem o banco de dados SQLite, adequado para demonstração mas não para alta escala, e o envio de e-mail via ambiente de sandbox. Como próximos passos, planejamos exportação de boletim em PDF e notificações por e-mail reais. Agradecemos ao nosso orientador Edson Ricardo Nunes Nascimento e ao Polo Valinhos pelo suporte durante o desenvolvimento. Obrigado!"

---

## Instruções de Gravação

1. **Ensaio obrigatório:** cronometrar o roteiro completo antes de gravar. O tempo total não deve ultrapassar 10 minutos.
2. **Credenciais de demo:** usar as credenciais do seed demo (migration 0002_seed_demo_data.py). O banco é recriado a cada deploy no Render free tier — verificar se os dados estão presentes antes de gravar.
3. **URL de produção:** usar sempre https://projeto-integrador.pages.dev (não localhost) para os slots de demo.
4. **Qualidade de vídeo:** resolução mínima 1080p, som claro sem ruído de fundo.
5. **Upload:** postar no YouTube como público ou não listado. Inserir o link na capa do relatório e na Ficha Técnica antes de entregar no AVA.
6. **Entrega no AVA:** apenas um integrante envia o PDF do relatório pelo grupo, até 2026-05-19 23:59.

---

## Descrição para Ficha Técnica do Vídeo (~250 palavras)

> **Instrução:** copiar este bloco para o campo "Descrição do protótipo" da Ficha Técnica (`docs/Modelo-Ficha_Tecnica_do_video.docx`). Este texto NÃO é o mesmo do Resumo do relatório — descreve especificamente o vídeo e o protótipo demonstrado.

Este vídeo apresenta o Sistema Web de Registro Escolar, desenvolvido como Projeto Integrador em Computação I (PJI110) pela Turma 004 da UNIVESP, Polo Valinhos, sob orientação do professor Edson Ricardo Nunes Nascimento.

O projeto foi motivado por uma necessidade identificada em escola pública municipal da rede de Valinhos-SP, por meio de entrevista com a professora Elizabete Ap. Godoy de Toledo em março de 2026. O problema central é a falta de visibilidade dos responsáveis sobre o desempenho escolar dos filhos: notas e frequência são comunicadas por boletins impressos bimestrais e bilhetes levados pelos próprios alunos, sem canal digital sistemático.

A solução desenvolvida é uma aplicação web com três portais de acesso distintos. O administrador gerencia toda a estrutura da escola: alunos, turmas, disciplinas, professores e responsáveis. O professor registra chamada e lança notas por turma e bimestre, com controle de acesso restrito às suas turmas. O responsável visualiza o boletim do filho com notas por disciplina organizadas por bimestre, médias calculadas automaticamente, percentual de frequência e alerta visual quando a presença cai abaixo de setenta e cinco por cento — limite mínimo estabelecido pela Lei de Diretrizes e Bases, artigo 24, inciso VI.

O sistema foi construído com Python e FastAPI no backend, React e TypeScript no frontend, SQLite como banco de dados, e autenticação por tokens JWT. O deploy foi realizado no Render (backend) e Cloudflare Pages (frontend), com integração contínua via GitHub Actions. O protótipo está em produção pública em projeto-integrador.pages.dev e demonstra, ao vivo, todos os três perfis de usuário.

**Link do vídeo:** [INSERIR LINK YOUTUBE APÓS UPLOAD]
