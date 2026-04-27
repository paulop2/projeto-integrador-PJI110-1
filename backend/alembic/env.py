import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import text

# Adicionar backend/src ao path para imports funcionarem
sys.path.insert(0, ".")

from src.database import Base, engine  # noqa: E402
import src.models  # noqa: F401, E402 — importar todos os models para Alembic detectar

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

NAMING_CONVENTION = {
    "ix": "ix_%(table_name)s_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


def run_migrations_offline() -> None:
    """Modo offline: gera SQL sem conexão ao banco."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,  # CRÍTICO: suporte a ALTER TABLE no SQLite
        naming_convention=NAMING_CONVENTION,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Modo online: conecta ao banco e executa migrations."""
    with engine.connect() as connection:
        # Desabilitar FK enforcement durante a migration (obrigatório para batch mode no SQLite)
        connection.execute(text("PRAGMA foreign_keys=OFF"))
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,  # CRÍTICO: suporte a ALTER TABLE no SQLite
            naming_convention=NAMING_CONVENTION,
        )
        with context.begin_transaction():
            context.run_migrations()
        # Reabilitar FK enforcement após migration
        connection.execute(text("PRAGMA foreign_keys=ON"))


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
