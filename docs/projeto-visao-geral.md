# Projeto Integrador - Visao Geral

## O que e o sistema?

Sistema web de registro de presenca e notas para escolas, com tres tipos de acesso:
- **Admin**: Gerencia usuarios, turmas, disciplinas
- **Professor**: Faz chamada e lanca notas
- **Responsavel**: Consulta boletim e frequencia dos filhos

---

## Modulos a Implementar

### 1. Autenticacao (Auth)

| Item | Descricao |
|------|-----------|
| Login | Tela de login com email/senha |
| JWT | Gerar e validar tokens |
| Refresh Token | Renovar sessao sem relogar |
| Logout | Invalidar sessao |
| Protecao de rotas | Verificar token em cada request |
| Controle de permissao | Verificar tipo de usuario |

### 2. Telas do Admin

| Tela | Funcionalidade |
|------|----------------|
| Dashboard | Resumo do sistema (totais, graficos) |
| Usuarios | CRUD de usuarios |
| Professores | CRUD de professores |
| Responsaveis | CRUD de responsaveis |
| Alunos | CRUD de alunos + vincular a turma/responsavel |
| Turmas | CRUD de turmas |
| Disciplinas | CRUD de disciplinas |

### 3. Telas do Professor

| Tela | Funcionalidade |
|------|----------------|
| Dashboard | Suas turmas, chamadas pendentes |
| Minhas Turmas | Lista de turmas que leciona |
| Fazer Chamada | Selecionar turma, marcar presencas |
| Historico Chamadas | Ver/editar chamadas anteriores |
| Avaliacoes | Criar provas/trabalhos |
| Lancar Notas | Inserir notas por avaliacao |

### 4. Telas do Responsavel

| Tela | Funcionalidade |
|------|----------------|
| Dashboard | Resumo dos filhos |
| Meus Filhos | Lista de alunos vinculados |
| Boletim | Notas por disciplina/bimestre |
| Frequencia | Presencas e faltas |

### 5. Componentes Compartilhados

| Componente | Descricao |
|------------|-----------|
| Layout | Sidebar + header + conteudo |
| Tabela | Com paginacao, busca, ordenacao |
| Formularios | Inputs, selects, validacao |
| Modais | Confirmacao, alertas |
| Loading/Error states | Feedback visual |

---

## Funcionalidades Extras (Sugestoes)

### Prioridade Alta (recomendado)

| Feature | Descricao | Beneficio |
|---------|-----------|-----------|
| Notificacoes por Email | Enviar email quando nota for lancada ou falta registrada | Responsavel fica informado |
| Exportar Boletim PDF | Gerar PDF do boletim para impressao | Responsavel pode imprimir |
| Busca Global | Buscar aluno/professor por nome em qualquer tela | Facilita navegacao |

### Prioridade Media (diferencial)

| Feature | Descricao | Beneficio |
|---------|-----------|-----------|
| Integracao WhatsApp | Enviar notificacoes via WhatsApp (API oficial ou Twilio) | Comunicacao instantanea |
| Dashboard com Graficos | Graficos de frequencia, medias, evolucao | Visualizacao de dados |
| Relatorios | Relatorio de faltas, alunos em risco | Gestao escolar |
| Recuperacao de Senha | Enviar link por email para redefinir senha | Autonomia do usuario |

### Prioridade Baixa (futuro)

| Feature | Descricao | Beneficio |
|---------|-----------|-----------|
| Integracao Telegram | Bot para consultar notas/frequencia | Alternativa ao WhatsApp |
| App Mobile | App nativo ou PWA | Acesso mobile |
| Multi-escola | Suporte a varias escolas no mesmo sistema | Escalabilidade |
| Historico de Anos | Manter dados de anos anteriores | Historico academico |
| FAQ/Ajuda | Secao de perguntas frequentes | Suporte ao usuario |

---

## Decisoes Tecnicas Pendentes

| Decisao | Opcoes | Impacto |
|---------|--------|---------|
| Backend Framework | FastAPI (Python) vs Express (Node) | Stack do time |
| ORM/Query Builder | SQLAlchemy vs raw SQL | Produtividade |
| Frontend State | Context API vs Zustand vs Redux | Complexidade |
| Estilizacao | Tailwind vs CSS Modules vs styled-components | Produtividade |
| Validacao Forms | React Hook Form vs Formik | DX |
| Testes | Jest + Testing Library vs Vitest | Velocidade |

---

## Fluxos Principais

### Fluxo do Professor - Fazer Chamada

1. Login
2. Dashboard → Ver turmas do dia
3. Selecionar turma
4. Ver lista de alunos
5. Marcar presente/ausente para cada um
6. Salvar chamada
7. (Sistema notifica responsaveis de faltas)

### Fluxo do Professor - Lancar Notas

1. Login
2. Avaliacoes → Criar nova avaliacao
3. Preencher: turma, disciplina, tipo, data, valor maximo
4. Salvar avaliacao
5. Lancar Notas → Selecionar avaliacao
6. Inserir nota para cada aluno
7. Salvar notas
8. (Sistema notifica responsaveis)

### Fluxo do Responsavel - Ver Boletim

1. Login
2. Dashboard → Ver resumo dos filhos
3. Selecionar filho
4. Ver boletim (notas por disciplina)
5. Ver frequencia (presencas/faltas)
6. (Opcional) Exportar PDF

---

## Proximos Passos

1. [ ] Definir stack do backend (Python FastAPI ou Node Express)
2. [ ] Definir bibliotecas do frontend (state, forms, estilo)
3. [ ] Criar estrutura inicial do projeto (pastas, configs)
4. [ ] Implementar autenticacao (login + JWT)
5. [ ] Implementar CRUD basico (usuarios, turmas, alunos)
6. [ ] Implementar chamada e notas
7. [ ] Implementar telas do responsavel
8. [ ] Adicionar features extras
