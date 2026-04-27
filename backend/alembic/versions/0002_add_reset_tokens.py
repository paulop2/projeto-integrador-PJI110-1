"""add reset_tokens

Revision ID: 0002
Revises: 0001
Create Date: 2026-04-26 00:00:00.000000

Tabela reset_tokens para tokens de redefinição de senha (24h TTL, single-use).
"""

from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "reset_tokens",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("usuario_id", sa.Integer(), nullable=False),
        sa.Column("token", sa.String(length=128), nullable=False),
        sa.Column("expira_em", sa.DateTime(), nullable=False),
        sa.Column("usado", sa.Boolean(), nullable=False, server_default="0"),
        sa.Column(
            "criado_em",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.current_timestamp(),
        ),
        sa.PrimaryKeyConstraint("id", name="pk_reset_tokens"),
        sa.UniqueConstraint("token", name="uq_reset_tokens_token"),
        sa.ForeignKeyConstraint(
            ["usuario_id"],
            ["usuarios.id"],
            name="fk_reset_tokens_usuario_id_usuarios",
            ondelete="CASCADE",
        ),
    )
    op.create_index("ix_reset_tokens_usuario_id", "reset_tokens", ["usuario_id"])
    op.create_index("ix_reset_tokens_token", "reset_tokens", ["token"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_reset_tokens_token", table_name="reset_tokens")
    op.drop_index("ix_reset_tokens_usuario_id", table_name="reset_tokens")
    op.drop_table("reset_tokens")
