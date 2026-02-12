**Resumo do Projeto**  
Um sistema web básico de registro de presença e notas de alunos. Esse sistema seria separado em frontend e backend para faciltiar desenvolvimento em grupo e separação das responsabilidades do sistema.

Esse sistema teria três tipos de acessos/credenciais: Responsável, Professor e Admin.

**Diagrama de Relacionamentos**

usuarios (1) ──── (1) professores  
usuarios (1) ──── (1) responsaveis  
responsaveis (1) ──── (N) alunos  
turmas (1) ──── (N) alunos  
turmas (1) ──── (N) chamadas  
turmas (1) ──── (N) avaliacoes  
professores (1) ──── (N) chamadas  
professores (1) ──── (N) avaliacoes  
chamadas (1) ──── (N) presencas  
avaliacoes (1) ──── (N) notas  
alunos (1) ──── (N) presencas  
alunos (1) ──── (N) notas  
disciplinas (1) ──── (N) avaliacoes

**Endpoints**

## **Autenticação e Usuários**

Endpoints básicos para entrada no sistema.

* POST /auth/login: Realiza o login e retorna o token de acesso (JWT).  
  \- Publico  
  \- Retorna JWT  
* POST /admin/users: (Apenas Admin) Cria novos usuários (aluno, professor ou responsável).  
  \- Autenticado  
* POST /admin/refresh: Refresh do token JWT do user  
  \- Autenticado  
  \- Retorna perfil do usuário logado 

## **Endpoints por Perfil**

### 1\. Administrador (admin)

O "mestre" do sistema. Ele gerencia a estrutura e tem poder de correção.

* POST /alunos: Cadastra um novo aluno e vincula a um responsável.  
* POST /professores: Cadastra novo professor.  
* PUT /notas/{id}: Edita uma nota já lançada (correção de erros).

### 2\. Professor (professor)

Focado na rotina de sala de aula.

* GET /turmas/{turma\_id}/alunos: Lista os alunos de uma turma específica.  
* POST /chamada: Registra a presença diária (lista de IDs de alunos e status).  
* POST /notas: Lança as notas de uma avaliação para a turma.

### 3\. Responsável (responsavel)

Apenas leitura dos dados dos alunos vinculados.

* GET /meus\_alunos: Lista os alunos vinculados ao perfil do responsável.  
* GET /alunos/{id}/boletim: Visualiza o boletim (notas e faltas) de um aluno específico.

**Stack**

Não foi definida nenhuma stack, pensamos a princípio em Python ou Javascript para o backend, não definimos o frontend se será react ou html,css e javascript puro.  
Precisamos definir um banco de dados também.   
Leonardo comentou de usar um NoSQL local que seja um arquivo simples.