# Schema do Banco de Dados

## Visao Geral

Este documento define a estrutura completa do banco de dados do Sistema de Gestao Escolar.

**Banco de dados:** SQLite

---

## Diagrama ER (Resumo)

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

## Tabelas

### 1. usuarios

Tabela central de autenticacao. Todos os acessos ao sistema passam por aqui.

| Coluna | Tipo | Constraints | Descricao |
|--------|------|-------------|-----------|
| id | INTEGER | PK, AUTOINCREMENT | Identificador unico |
| email | VARCHAR(255) | NOT NULL, UNIQUE | Email para login |
| senha_hash | VARCHAR(255) | NOT NULL | Hash bcrypt da senha |
| tipo | VARCHAR(20) | NOT NULL, CHECK (tipo IN ('admin', 'professor', 'responsavel')) | Tipo de usuario |
| ativo | BOOLEAN | NOT NULL, DEFAULT true | Se o usuario pode acessar o sistema |
| criado_em | TIMESTAMP | NOT NULL, DEFAULT NOW() | Data de criacao |
| atualizado_em | TIMESTAMP | NOT NULL, DEFAULT NOW() | Data da ultima atualizacao |

**Indices:**
- `idx_usuarios_email` - UNIQUE em `email`
- `idx_usuarios_tipo` - em `tipo`

---

### 2. professores

Dados especificos dos professores.

| Coluna | Tipo | Constraints | Descricao |
|--------|------|-------------|-----------|
| id | INTEGER | PK, AUTOINCREMENT | Identificador unico |
| usuario_id | INTEGER | NOT NULL, UNIQUE, FK -> usuarios(id) ON DELETE CASCADE | Vinculo com usuario |
| nome | VARCHAR(255) | NOT NULL | Nome completo |
| matricula | VARCHAR(50) | NOT NULL, UNIQUE | Matricula institucional |
| criado_em | TIMESTAMP | NOT NULL, DEFAULT NOW() | Data de criacao |
| atualizado_em | TIMESTAMP | NOT NULL, DEFAULT NOW() | Data da ultima atualizacao |

**Indices:**
- `idx_professores_usuario_id` - UNIQUE em `usuario_id`
- `idx_professores_matricula` - UNIQUE em `matricula`

---

### 3. responsaveis

Pais ou responsaveis legais dos alunos.

| Coluna | Tipo | Constraints | Descricao |
|--------|------|-------------|-----------|
| id | INTEGER | PK, AUTOINCREMENT | Identificador unico |
| usuario_id | INTEGER | NOT NULL, UNIQUE, FK -> usuarios(id) ON DELETE CASCADE | Vinculo com usuario |
| nome | VARCHAR(255) | NOT NULL | Nome completo |
| cpf | VARCHAR(11) | NOT NULL, UNIQUE | CPF (apenas numeros) |
| telefone | VARCHAR(20) | NULL | Telefone para contato |
| criado_em | TIMESTAMP | NOT NULL, DEFAULT NOW() | Data de criacao |
| atualizado_em | TIMESTAMP | NOT NULL, DEFAULT NOW() | Data da ultima atualizacao |

**Indices:**
- `idx_responsaveis_usuario_id` - UNIQUE em `usuario_id`
- `idx_responsaveis_cpf` - UNIQUE em `cpf`

---

### 4. turmas

Turmas/classes da escola.

| Coluna | Tipo | Constraints | Descricao |
|--------|------|-------------|-----------|
| id | INTEGER | PK, AUTOINCREMENT | Identificador unico |
| nome | VARCHAR(50) | NOT NULL | Nome da turma (ex: "5A", "3B") |
| ano | INTEGER | NOT NULL | Ano letivo (ex: 2025) |
| serie | VARCHAR(20) | NOT NULL | Serie/ano escolar (ex: "5º ano", "3ª serie") |
| turno | VARCHAR(20) | NOT NULL, CHECK (turno IN ('matutino', 'vespertino', 'noturno')) | Periodo de aulas |
| ativa | BOOLEAN | NOT NULL, DEFAULT true | Se a turma esta ativa |
| criado_em | TIMESTAMP | NOT NULL, DEFAULT NOW() | Data de criacao |
| atualizado_em | TIMESTAMP | NOT NULL, DEFAULT NOW() | Data da ultima atualizacao |

**Indices:**
- `idx_turmas_ano` - em `ano`
- `idx_turmas_ativa` - em `ativa`
- `idx_turmas_unique_nome_ano` - UNIQUE em `(nome, ano)`

---

### 5. alunos

Dados dos alunos matriculados.

| Coluna | Tipo | Constraints | Descricao |
|--------|------|-------------|-----------|
| id | INTEGER | PK, AUTOINCREMENT | Identificador unico |
| responsavel_id | INTEGER | NOT NULL, FK -> responsaveis(id) ON DELETE RESTRICT | Responsavel legal |
| turma_id | INTEGER | NULL, FK -> turmas(id) ON DELETE SET NULL | Turma atual (NULL se nao matriculado) |
| nome | VARCHAR(255) | NOT NULL | Nome completo |
| matricula | VARCHAR(50) | NOT NULL, UNIQUE | Matricula do aluno |
| data_nascimento | DATE | NOT NULL | Data de nascimento |
| ativo | BOOLEAN | NOT NULL, DEFAULT true | Se o aluno esta ativo |
| criado_em | TIMESTAMP | NOT NULL, DEFAULT NOW() | Data de criacao |
| atualizado_em | TIMESTAMP | NOT NULL, DEFAULT NOW() | Data da ultima atualizacao |

**Indices:**
- `idx_alunos_responsavel_id` - em `responsavel_id`
- `idx_alunos_turma_id` - em `turma_id`
- `idx_alunos_matricula` - UNIQUE em `matricula`

---

### 6. disciplinas

Disciplinas/materias oferecidas.

| Coluna | Tipo | Constraints | Descricao |
|--------|------|-------------|-----------|
| id | INTEGER | PK, AUTOINCREMENT | Identificador unico |
| nome | VARCHAR(100) | NOT NULL, UNIQUE | Nome da disciplina |
| carga_horaria | INTEGER | NOT NULL | Carga horaria semanal em horas |
| criado_em | TIMESTAMP | NOT NULL, DEFAULT NOW() | Data de criacao |
| atualizado_em | TIMESTAMP | NOT NULL, DEFAULT NOW() | Data da ultima atualizacao |

**Indices:**
- `idx_disciplinas_nome` - UNIQUE em `nome`

---

### 7. professor_disciplina

Relacao N:N entre professores e disciplinas que lecionam.

| Coluna | Tipo | Constraints | Descricao |
|--------|------|-------------|-----------|
| id | INTEGER | PK, AUTOINCREMENT | Identificador unico |
| professor_id | INTEGER | NOT NULL, FK -> professores(id) ON DELETE CASCADE | Professor |
| disciplina_id | INTEGER | NOT NULL, FK -> disciplinas(id) ON DELETE CASCADE | Disciplina |
| criado_em | TIMESTAMP | NOT NULL, DEFAULT NOW() | Data de criacao |

**Indices:**
- `idx_professor_disciplina_unique` - UNIQUE em `(professor_id, disciplina_id)`

---

### 8. professor_turma

Relacao N:N entre professores e turmas que lecionam.

| Coluna | Tipo | Constraints | Descricao |
|--------|------|-------------|-----------|
| id | INTEGER | PK, AUTOINCREMENT | Identificador unico |
| professor_id | INTEGER | NOT NULL, FK -> professores(id) ON DELETE CASCADE | Professor |
| turma_id | INTEGER | NOT NULL, FK -> turmas(id) ON DELETE CASCADE | Turma |
| disciplina_id | INTEGER | NOT NULL, FK -> disciplinas(id) ON DELETE CASCADE | Disciplina lecionada nesta turma |
| criado_em | TIMESTAMP | NOT NULL, DEFAULT NOW() | Data de criacao |

**Indices:**
- `idx_professor_turma_unique` - UNIQUE em `(professor_id, turma_id, disciplina_id)`

---

### 9. chamadas

Registro de chamada/presenca por aula.

| Coluna | Tipo | Constraints | Descricao |
|--------|------|-------------|-----------|
| id | INTEGER | PK, AUTOINCREMENT | Identificador unico |
| turma_id | INTEGER | NOT NULL, FK -> turmas(id) ON DELETE RESTRICT | Turma da chamada |
| professor_id | INTEGER | NOT NULL, FK -> professores(id) ON DELETE RESTRICT | Professor que fez a chamada |
| disciplina_id | INTEGER | NOT NULL, FK -> disciplinas(id) ON DELETE RESTRICT | Disciplina da aula |
| data | DATE | NOT NULL | Data da aula |
| observacoes | TEXT | NULL | Observacoes gerais |
| criado_em | TIMESTAMP | NOT NULL, DEFAULT NOW() | Data de criacao |
| atualizado_em | TIMESTAMP | NOT NULL, DEFAULT NOW() | Data da ultima atualizacao |

**Indices:**
- `idx_chamadas_turma_id` - em `turma_id`
- `idx_chamadas_professor_id` - em `professor_id`
- `idx_chamadas_data` - em `data`
- `idx_chamadas_unique` - UNIQUE em `(turma_id, disciplina_id, data)`

---

### 10. presencas

Presenca individual de cada aluno em uma chamada.

| Coluna | Tipo | Constraints | Descricao |
|--------|------|-------------|-----------|
| id | INTEGER | PK, AUTOINCREMENT | Identificador unico |
| chamada_id | INTEGER | NOT NULL, FK -> chamadas(id) ON DELETE CASCADE | Chamada relacionada |
| aluno_id | INTEGER | NOT NULL, FK -> alunos(id) ON DELETE CASCADE | Aluno |
| presente | BOOLEAN | NOT NULL | Se o aluno estava presente |
| justificativa | TEXT | NULL | Justificativa de falta (se houver) |
| criado_em | TIMESTAMP | NOT NULL, DEFAULT NOW() | Data de criacao |
| atualizado_em | TIMESTAMP | NOT NULL, DEFAULT NOW() | Data da ultima atualizacao |

**Indices:**
- `idx_presencas_chamada_id` - em `chamada_id`
- `idx_presencas_aluno_id` - em `aluno_id`
- `idx_presencas_unique` - UNIQUE em `(chamada_id, aluno_id)`

---

### 11. avaliacoes

Provas, trabalhos e outras avaliacoes.

| Coluna | Tipo | Constraints | Descricao |
|--------|------|-------------|-----------|
| id | INTEGER | PK, AUTOINCREMENT | Identificador unico |
| turma_id | INTEGER | NOT NULL, FK -> turmas(id) ON DELETE RESTRICT | Turma avaliada |
| disciplina_id | INTEGER | NOT NULL, FK -> disciplinas(id) ON DELETE RESTRICT | Disciplina da avaliacao |
| professor_id | INTEGER | NOT NULL, FK -> professores(id) ON DELETE RESTRICT | Professor responsavel |
| titulo | VARCHAR(255) | NOT NULL | Titulo da avaliacao |
| descricao | TEXT | NULL | Descricao/instrucoes |
| tipo | VARCHAR(50) | NOT NULL, CHECK (tipo IN ('prova', 'trabalho', 'exercicio', 'outro')) | Tipo de avaliacao |
| valor_maximo | DECIMAL(5,2) | NOT NULL, DEFAULT 10.00 | Nota maxima possivel |
| data | DATE | NOT NULL | Data da avaliacao |
| bimestre | INTEGER | NOT NULL, CHECK (bimestre BETWEEN 1 AND 4) | Bimestre da avaliacao |
| criado_em | TIMESTAMP | NOT NULL, DEFAULT NOW() | Data de criacao |
| atualizado_em | TIMESTAMP | NOT NULL, DEFAULT NOW() | Data da ultima atualizacao |

**Indices:**
- `idx_avaliacoes_turma_id` - em `turma_id`
- `idx_avaliacoes_disciplina_id` - em `disciplina_id`
- `idx_avaliacoes_professor_id` - em `professor_id`
- `idx_avaliacoes_data` - em `data`
- `idx_avaliacoes_bimestre` - em `bimestre`

---

### 12. notas

Notas individuais dos alunos nas avaliacoes.

| Coluna | Tipo | Constraints | Descricao |
|--------|------|-------------|-----------|
| id | INTEGER | PK, AUTOINCREMENT | Identificador unico |
| avaliacao_id | INTEGER | NOT NULL, FK -> avaliacoes(id) ON DELETE CASCADE | Avaliacao relacionada |
| aluno_id | INTEGER | NOT NULL, FK -> alunos(id) ON DELETE CASCADE | Aluno |
| valor | DECIMAL(5,2) | NULL | Nota obtida (NULL se nao avaliado) |
| observacoes | TEXT | NULL | Observacoes sobre o desempenho |
| criado_em | TIMESTAMP | NOT NULL, DEFAULT NOW() | Data de criacao |
| atualizado_em | TIMESTAMP | NOT NULL, DEFAULT NOW() | Data da ultima atualizacao |

**Indices:**
- `idx_notas_avaliacao_id` - em `avaliacao_id`
- `idx_notas_aluno_id` - em `aluno_id`
- `idx_notas_unique` - UNIQUE em `(avaliacao_id, aluno_id)`

---

## Constraints Adicionais

### Validacoes de Negocio

1. **Nota nao pode exceder valor maximo:**
```sql
ALTER TABLE notas ADD CONSTRAINT chk_nota_valor
CHECK (valor IS NULL OR valor >= 0);

-- Trigger para validar contra valor_maximo da avaliacao
CREATE OR REPLACE FUNCTION validar_nota_maxima()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.valor IS NOT NULL THEN
        IF NEW.valor > (SELECT valor_maximo FROM avaliacoes WHERE id = NEW.avaliacao_id) THEN
            RAISE EXCEPTION 'Nota excede o valor maximo da avaliacao';
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

2. **Aluno deve pertencer a turma da chamada:**
```sql
CREATE OR REPLACE FUNCTION validar_aluno_turma_chamada()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM alunos a
        JOIN chamadas c ON c.turma_id = a.turma_id
        WHERE a.id = NEW.aluno_id AND c.id = NEW.chamada_id
    ) THEN
        RAISE EXCEPTION 'Aluno nao pertence a turma desta chamada';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

3. **Aluno deve pertencer a turma da avaliacao:**
```sql
CREATE OR REPLACE FUNCTION validar_aluno_turma_avaliacao()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM alunos a
        JOIN avaliacoes av ON av.turma_id = a.turma_id
        WHERE a.id = NEW.aluno_id AND av.id = NEW.avaliacao_id
    ) THEN
        RAISE EXCEPTION 'Aluno nao pertence a turma desta avaliacao';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

---

## Triggers para Atualizacao Automatica

```sql
-- Funcao generica para atualizar campo atualizado_em
CREATE OR REPLACE FUNCTION atualizar_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.atualizado_em = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Aplicar em todas as tabelas com atualizado_em
CREATE TRIGGER trg_usuarios_updated BEFORE UPDATE ON usuarios
FOR EACH ROW EXECUTE FUNCTION atualizar_timestamp();

CREATE TRIGGER trg_professores_updated BEFORE UPDATE ON professores
FOR EACH ROW EXECUTE FUNCTION atualizar_timestamp();

-- ... (repetir para todas as tabelas)
```

---

## Script de Criacao

O script SQL completo para criar o banco esta em: `backend/src/database/migrations/001_initial_schema.sql`
