# Arquitetura do Frontend

## Visao Geral

SPA (Single Page Application) construida com React.

---

## Estrutura de Rotas

### Rotas Publicas

| Rota | Pagina | Descricao |
|------|--------|-----------|
| /login | Login | Tela de autenticacao |

### Rotas Protegidas (requerem autenticacao)

| Rota | Pagina | Permissao | Descricao |
|------|--------|-----------|-----------|
| / | Dashboard | Todos | Visao geral (conteudo varia por tipo) |
| /usuarios | Lista Usuarios | Admin | Gerenciar usuarios |
| /usuarios/novo | Novo Usuario | Admin | Cadastrar usuario |
| /professores | Lista Professores | Admin | Gerenciar professores |
| /professores/:id | Detalhe Professor | Admin | Ver/editar professor |
| /responsaveis | Lista Responsaveis | Admin | Gerenciar responsaveis |
| /responsaveis/:id | Detalhe Responsavel | Admin | Ver/editar responsavel |
| /alunos | Lista Alunos | Admin, Professor | Gerenciar/ver alunos |
| /alunos/:id | Detalhe Aluno | Todos | Ver/editar aluno |
| /turmas | Lista Turmas | Admin, Professor | Gerenciar/ver turmas |
| /turmas/:id | Detalhe Turma | Admin, Professor | Ver alunos da turma |
| /disciplinas | Lista Disciplinas | Admin | Gerenciar disciplinas |
| /chamada | Nova Chamada | Professor | Registrar presenca |
| /chamada/:id | Editar Chamada | Professor | Alterar presencas |
| /avaliacoes | Lista Avaliacoes | Admin, Professor | Ver avaliacoes |
| /avaliacoes/nova | Nova Avaliacao | Professor | Criar avaliacao |
| /avaliacoes/:id | Lancar Notas | Professor | Registrar notas |
| /filhos | Meus Filhos | Responsavel | Lista de filhos |
| /filhos/:id | Detalhe Filho | Responsavel | Boletim e frequencia |
| /filhos/:id/notas | Notas | Responsavel | Notas por disciplina |
| /filhos/:id/frequencia | Frequencia | Responsavel | Historico de presencas |
| /perfil | Meu Perfil | Todos | Ver/editar perfil proprio |

---

## Gerenciamento de Estado

### Estado Global (Context ou Zustand)

| Estado | Descricao |
|--------|-----------|
| auth | Usuario logado, token JWT, tipo de usuario |
| ui | Sidebar aberta/fechada, tema, notificacoes |

### Estado Local (useState/useReducer)

- Formularios
- Dados de listagens
- Filtros e paginacao
- Estados de loading

### Estado do Servidor (React Query ou SWR)

- Cache de requisicoes
- Invalidacao automatica
- Refetch em foco

---

## Componentes Principais

### Layout

| Componente | Descricao |
|------------|-----------|
| Layout | Container principal com sidebar e header |
| Sidebar | Menu lateral de navegacao |
| Header | Barra superior com usuario e logout |
| PrivateRoute | Proteção de rotas por autenticacao |
| RoleRoute | Proteção de rotas por tipo de usuario |

### Formularios

| Componente | Descricao |
|------------|-----------|
| Input | Campo de texto padrao |
| Select | Campo de selecao |
| DatePicker | Seletor de data |
| Form | Container de formulario com validacao |
| Button | Botao com variantes |

### Dados

| Componente | Descricao |
|------------|-----------|
| Table | Tabela com ordenacao e paginacao |
| Card | Cartao para exibicao de informacoes |
| List | Lista simples |
| EmptyState | Estado vazio |
| Loading | Indicador de carregamento |
| ErrorState | Exibicao de erros |

### Especificos do Dominio

| Componente | Descricao |
|------------|-----------|
| AlunoCard | Cartao com info do aluno |
| TurmaSelect | Seletor de turma |
| DisciplinaSelect | Seletor de disciplina |
| ChamadaForm | Formulario de presenca |
| NotasTable | Tabela de lancamento de notas |
| BoletimView | Visualizacao do boletim |
| FrequenciaChart | Grafico de frequencia |

---

## Fluxo de Autenticacao

1. Usuario acessa `/login`
2. Envia credenciais para `POST /api/auth/login`
3. Recebe JWT no response
4. Armazena JWT no localStorage/sessionStorage
5. Redireciona para dashboard baseado no tipo:
   - admin → `/admin`
   - professor → `/professor`
   - responsavel → `/responsavel`
6. Todas as requisicoes incluem header `Authorization: Bearer <token>`
7. Se token expirar (401), redireciona para `/login`

---

## Protecao de Rotas

### Por Autenticacao

Rotas que requerem login verificam:
- Token existe no storage
- Token nao expirou (validacao local do exp)

### Por Tipo de Usuario

Cada rota define quais tipos de usuario podem acessa-la (ver tabela de rotas).
Se usuario tentar acessar rota nao autorizada → redireciona para dashboard.

---

## Tratamento de Erros

### Erros de Requisicao

| Status | Acao |
|--------|------|
| 400 | Exibir mensagens de validacao nos campos |
| 401 | Limpar auth e redirecionar para login |
| 403 | Exibir mensagem "Sem permissao" |
| 404 | Exibir pagina "Nao encontrado" |
| 500 | Exibir mensagem generica de erro |

### Erros de Rede

- Exibir mensagem "Sem conexao"
- Oferecer botao para tentar novamente
