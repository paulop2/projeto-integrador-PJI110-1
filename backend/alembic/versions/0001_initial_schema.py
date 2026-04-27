"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-04-26 00:00:00.000000

Schema completo do sistema escolar — todas as 11 tabelas + indexes + seed admin.
Este schema é definitivo: fases 2-6 não adicionam migrations.
"""

from alembic import op
import sqlalchemy as sa
from datetime import date

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # -------------------------------------------------------------------------
    # 1. USUARIOS — tabela central de autenticação
    # -------------------------------------------------------------------------
    op.create_table(
        "usuarios",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("senha_hash", sa.String(length=255), nullable=False),
        sa.Column(
            "tipo",
            sa.Enum("admin", "professor", "responsavel", name="tipo_usuario"),
            nullable=False,
        ),
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default="1"),
        sa.Column(
            "criado_em",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.current_timestamp(),
        ),
        sa.PrimaryKeyConstraint("id", name="pk_usuarios"),
        sa.UniqueConstraint("email", name="uq_usuarios_email"),
    )
    op.create_index("ix_usuarios_email", "usuarios", ["email"], unique=True)

    # -------------------------------------------------------------------------
    # 2. PROFESSORES — perfil de professor (1:1 com usuarios)
    # -------------------------------------------------------------------------
    op.create_table(
        "professores",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("usuario_id", sa.Integer(), nullable=False),
        sa.Column("nome", sa.String(length=255), nullable=False),
        sa.Column("cpf", sa.String(length=14), nullable=True),
        sa.ForeignKeyConstraint(
            ["usuario_id"],
            ["usuarios.id"],
            name="fk_professores_usuario_id_usuarios",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_professores"),
        sa.UniqueConstraint("usuario_id", name="uq_professores_usuario_id"),
    )

    # -------------------------------------------------------------------------
    # 3. RESPONSAVEIS — perfil de responsável (1:1 com usuarios)
    # -------------------------------------------------------------------------
    op.create_table(
        "responsaveis",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("usuario_id", sa.Integer(), nullable=False),
        sa.Column("nome", sa.String(length=255), nullable=False),
        sa.Column("cpf", sa.String(length=14), nullable=True),
        sa.Column("telefone", sa.String(length=20), nullable=True),
        sa.ForeignKeyConstraint(
            ["usuario_id"],
            ["usuarios.id"],
            name="fk_responsaveis_usuario_id_usuarios",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_responsaveis"),
        sa.UniqueConstraint("usuario_id", name="uq_responsaveis_usuario_id"),
    )

    # -------------------------------------------------------------------------
    # 4. TURMAS — turmas/classes da escola
    # -------------------------------------------------------------------------
    op.create_table(
        "turmas",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nome", sa.String(length=100), nullable=False),
        sa.Column("ano", sa.Integer(), nullable=False),
        sa.Column("serie", sa.String(length=50), nullable=False),
        sa.Column("turno", sa.String(length=20), nullable=False),  # manhã/tarde/noite
        sa.PrimaryKeyConstraint("id", name="pk_turmas"),
    )

    # -------------------------------------------------------------------------
    # 5. DISCIPLINAS — matérias/subjects
    # -------------------------------------------------------------------------
    op.create_table(
        "disciplinas",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nome", sa.String(length=100), nullable=False),
        sa.Column("carga_horaria", sa.Integer(), nullable=True),  # horas/ano
        sa.PrimaryKeyConstraint("id", name="pk_disciplinas"),
    )

    # -------------------------------------------------------------------------
    # 6. ALUNOS — alunos (depende de responsaveis e turmas)
    # -------------------------------------------------------------------------
    op.create_table(
        "alunos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nome", sa.String(length=255), nullable=False),
        sa.Column("data_nascimento", sa.Date(), nullable=True),
        sa.Column("responsavel_id", sa.Integer(), nullable=True),
        sa.Column("turma_id", sa.Integer(), nullable=True),
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default="1"),
        sa.ForeignKeyConstraint(
            ["responsavel_id"],
            ["responsaveis.id"],
            name="fk_alunos_responsavel_id_responsaveis",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["turma_id"],
            ["turmas.id"],
            name="fk_alunos_turma_id_turmas",
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_alunos"),
    )
    op.create_index("ix_alunos_responsavel_id", "alunos", ["responsavel_id"])
    op.create_index("ix_alunos_turma_id", "alunos", ["turma_id"])

    # -------------------------------------------------------------------------
    # 7. PROFESSOR_TURMA — junction: quem leciona o quê (professor x turma x disciplina)
    # -------------------------------------------------------------------------
    op.create_table(
        "professor_turma",
        sa.Column("professor_id", sa.Integer(), nullable=False),
        sa.Column("turma_id", sa.Integer(), nullable=False),
        sa.Column("disciplina_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["professor_id"],
            ["professores.id"],
            name="fk_professor_turma_professor_id_professores",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["turma_id"],
            ["turmas.id"],
            name="fk_professor_turma_turma_id_turmas",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["disciplina_id"],
            ["disciplinas.id"],
            name="fk_professor_turma_disciplina_id_disciplinas",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "professor_id", "turma_id", "disciplina_id", name="pk_professor_turma"
        ),
    )
    op.create_index(
        "ix_professor_turma_professor_id", "professor_turma", ["professor_id"]
    )

    # -------------------------------------------------------------------------
    # 8. CHAMADAS — sessão de chamada (uma chamada por turma/disciplina/data)
    # -------------------------------------------------------------------------
    op.create_table(
        "chamadas",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("turma_id", sa.Integer(), nullable=False),
        sa.Column("disciplina_id", sa.Integer(), nullable=False),
        sa.Column("professor_id", sa.Integer(), nullable=False),
        sa.Column("data", sa.Date(), nullable=False),
        sa.Column(
            "criado_em",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.current_timestamp(),
        ),
        sa.ForeignKeyConstraint(
            ["turma_id"],
            ["turmas.id"],
            name="fk_chamadas_turma_id_turmas",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["disciplina_id"],
            ["disciplinas.id"],
            name="fk_chamadas_disciplina_id_disciplinas",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["professor_id"],
            ["professores.id"],
            name="fk_chamadas_professor_id_professores",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_chamadas"),
    )
    op.create_index("ix_chamadas_turma_id", "chamadas", ["turma_id"])
    op.create_index("ix_chamadas_data", "chamadas", ["data"])

    # -------------------------------------------------------------------------
    # 9. PRESENCAS — registro de presença por aluno em uma chamada
    # -------------------------------------------------------------------------
    op.create_table(
        "presencas",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("chamada_id", sa.Integer(), nullable=False),
        sa.Column("aluno_id", sa.Integer(), nullable=False),
        sa.Column("presente", sa.Boolean(), nullable=False),
        sa.Column("justificativa", sa.String(length=500), nullable=True),
        sa.ForeignKeyConstraint(
            ["chamada_id"],
            ["chamadas.id"],
            name="fk_presencas_chamada_id_chamadas",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["aluno_id"],
            ["alunos.id"],
            name="fk_presencas_aluno_id_alunos",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_presencas"),
        sa.UniqueConstraint(
            "chamada_id", "aluno_id", name="uq_presencas_chamada_id_aluno_id"
        ),
    )
    op.create_index("ix_presencas_chamada_id", "presencas", ["chamada_id"])
    op.create_index("ix_presencas_aluno_id", "presencas", ["aluno_id"])

    # -------------------------------------------------------------------------
    # 10. AVALIACOES — definição de uma avaliação (prova/trabalho) por bimestre
    # -------------------------------------------------------------------------
    op.create_table(
        "avaliacoes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("turma_id", sa.Integer(), nullable=False),
        sa.Column("disciplina_id", sa.Integer(), nullable=False),
        sa.Column("professor_id", sa.Integer(), nullable=False),
        sa.Column("titulo", sa.String(length=255), nullable=False),
        sa.Column("bimestre", sa.Integer(), nullable=False),  # 1, 2, 3 ou 4
        sa.Column("valor_maximo", sa.Float(), nullable=False, server_default="10.0"),
        sa.Column("data", sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(
            ["turma_id"],
            ["turmas.id"],
            name="fk_avaliacoes_turma_id_turmas",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["disciplina_id"],
            ["disciplinas.id"],
            name="fk_avaliacoes_disciplina_id_disciplinas",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["professor_id"],
            ["professores.id"],
            name="fk_avaliacoes_professor_id_professores",
            ondelete="CASCADE",
        ),
        sa.CheckConstraint("bimestre IN (1, 2, 3, 4)", name="ck_avaliacoes_bimestre"),
        sa.CheckConstraint("valor_maximo > 0", name="ck_avaliacoes_valor_maximo"),
        sa.PrimaryKeyConstraint("id", name="pk_avaliacoes"),
    )
    op.create_index("ix_avaliacoes_turma_id", "avaliacoes", ["turma_id"])
    op.create_index("ix_avaliacoes_bimestre", "avaliacoes", ["bimestre"])

    # -------------------------------------------------------------------------
    # 11. NOTAS — nota de um aluno em uma avaliação
    # -------------------------------------------------------------------------
    op.create_table(
        "notas",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("avaliacao_id", sa.Integer(), nullable=False),
        sa.Column("aluno_id", sa.Integer(), nullable=False),
        sa.Column("valor", sa.Float(), nullable=False),
        sa.Column(
            "criado_em",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.current_timestamp(),
        ),
        sa.ForeignKeyConstraint(
            ["avaliacao_id"],
            ["avaliacoes.id"],
            name="fk_notas_avaliacao_id_avaliacoes",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["aluno_id"],
            ["alunos.id"],
            name="fk_notas_aluno_id_alunos",
            ondelete="CASCADE",
        ),
        sa.UniqueConstraint(
            "avaliacao_id", "aluno_id", name="uq_notas_avaliacao_id_aluno_id"
        ),
        sa.PrimaryKeyConstraint("id", name="pk_notas"),
    )
    op.create_index("ix_notas_avaliacao_id", "notas", ["avaliacao_id"])
    op.create_index("ix_notas_aluno_id", "notas", ["aluno_id"])

    # -------------------------------------------------------------------------
    # SEED: Usuário admin padrão de desenvolvimento
    # Hash pré-computado para "admin123" com bcrypt cost=12
    # NÃO computar o hash em runtime — hardcoded é idempotente e não requer passlib
    # -------------------------------------------------------------------------
    op.execute(
        """
        INSERT INTO usuarios (email, senha_hash, tipo, ativo)
        VALUES (
            'admin@escola.dev',
            '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',
            'admin',
            1
        )
        """
    )


def downgrade() -> None:
    # Remover na ordem inversa de dependência
    op.drop_table("notas")
    op.drop_table("avaliacoes")
    op.drop_table("presencas")
    op.drop_table("chamadas")
    op.drop_table("professor_turma")
    op.drop_table("alunos")
    op.drop_table("disciplinas")
    op.drop_table("turmas")
    op.drop_table("responsaveis")
    op.drop_table("professores")
    op.drop_table("usuarios")
