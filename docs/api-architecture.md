# Arquitetura da API

## Visao Geral

API RESTful para o Sistema de Gestao Escolar.

**Banco de dados:** SQLite
**Base URL:** `/api`

---

## Padrao de Responses

### Sucesso

```json
{
  "success": true,
  "data": { ... },
  "message": "Operacao realizada com sucesso"
}
```

**Para listas com paginacao:**
```json
{
  "success": true,
  "data": [ ... ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "totalPages": 8
  }
}
```

### Erro

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Dados invalidos",
    "details": [
      {
        "field": "email",
        "message": "Email invalido"
      }
    ]
  }
}
```

### Codigos de Erro

| Codigo | HTTP Status | Descricao |
|--------|-------------|-----------|
| VALIDATION_ERROR | 400 | Dados de entrada invalidos |
| UNAUTHORIZED | 401 | Token ausente ou invalido |
| FORBIDDEN | 403 | Sem permissao para a acao |
| NOT_FOUND | 404 | Recurso nao encontrado |
| CONFLICT | 409 | Conflito (ex: email duplicado) |
| INTERNAL_ERROR | 500 | Erro interno do servidor |

---

## Formato do JWT

### Payload (Claims)

| Campo | Tipo | Descricao |
|-------|------|-----------|
| sub | string | ID do usuario (UUID) |
| email | string | Email do usuario |
| tipo | string | 'admin', 'professor' ou 'responsavel' |
| iat | number | Timestamp de emissao |
| exp | number | Timestamp de expiracao |

### Configuracao

- **Algoritmo:** HS256
- **Expiracao:** 8 horas
- **Header:** `Authorization: Bearer <token>`

---

## Regras de Permissao por Tipo de Usuario

### Admin

Acesso total ao sistema.

| Recurso | Permissoes |
|---------|------------|
| Usuarios | CRUD completo |
| Professores | CRUD completo |
| Responsaveis | CRUD completo |
| Alunos | CRUD completo |
| Turmas | CRUD completo |
| Disciplinas | CRUD completo |
| Chamadas | Visualizar todas |
| Avaliacoes | Visualizar todas |
| Notas | Visualizar todas |

### Professor

Acesso as suas turmas e alunos.

| Recurso | Permissoes |
|---------|------------|
| Perfil | Ver e editar proprio |
| Turmas | Ver apenas as suas |
| Alunos | Ver apenas das suas turmas |
| Chamadas | CRUD das suas turmas |
| Avaliacoes | CRUD das suas disciplinas/turmas |
| Notas | CRUD das suas avaliacoes |

### Responsavel

Acesso apenas aos dados dos seus filhos.

| Recurso | Permissoes |
|---------|------------|
| Perfil | Ver e editar proprio |
| Alunos | Ver apenas seus filhos |
| Presencas | Ver apenas dos filhos |
| Notas | Ver apenas dos filhos |
| Avaliacoes | Ver apenas das turmas dos filhos |

---

## Matriz de Permissoes por Endpoint

| Endpoint | Admin | Professor | Responsavel |
|----------|-------|-----------|-------------|
| POST /auth/login | Publico | Publico | Publico |
| GET /usuarios | Sim | Nao | Nao |
| GET /professores | Sim | Nao | Nao |
| GET /turmas | Sim | Suas turmas | Nao |
| GET /alunos | Sim | Seus alunos | Seus filhos |
| POST /chamadas | Sim | Suas turmas | Nao |
| GET /presencas/:alunoId | Sim | Seus alunos | Seus filhos |
| POST /avaliacoes | Sim | Suas turmas | Nao |
| GET /notas/:alunoId | Sim | Seus alunos | Seus filhos |

---

## Logica de Verificacao de Propriedade

Para endpoints que acessam dados de alunos, o sistema deve verificar:

1. **Admin:** Sempre permitido
2. **Professor:** Verificar se o aluno pertence a uma turma que o professor leciona
3. **Responsavel:** Verificar se o aluno e filho (responsavel_id) do usuario logado
