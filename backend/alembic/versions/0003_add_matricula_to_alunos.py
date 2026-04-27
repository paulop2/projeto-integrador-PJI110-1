"""add matricula to alunos

Revision ID: 0003
Revises: 0002
Create Date: 2026-04-27 00:00:00.000000

Adiciona coluna matricula (String 20, unique) à tabela alunos.
Geração automática pelo service layer: MAT{ano}{id:05d}.
"""

from alembic import op
import sqlalchemy as sa

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("alunos", schema=None) as batch_op:
        batch_op.add_column(sa.Column("matricula", sa.String(length=20), nullable=True))
        batch_op.create_unique_constraint("uq_alunos_matricula", ["matricula"])


def downgrade() -> None:
    with op.batch_alter_table("alunos", schema=None) as batch_op:
        batch_op.drop_constraint("uq_alunos_matricula", type_="unique")
        batch_op.drop_column("matricula")
