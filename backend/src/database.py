from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from src.config import settings


engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},  # Obrigatório para SQLite no FastAPI
)


@event.listens_for(engine, "connect")
def set_sqlite_pragmas(dbapi_conn, connection_record):
    """Configura pragmas SQLite em toda nova conexão — WAL mode + FK enforcement."""
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")   # WAL mode para leituras concorrentes
    cursor.execute("PRAGMA foreign_keys=ON")     # Enforça constraints de FK
    cursor.execute("PRAGMA busy_timeout=5000")   # Aguarda até 5s em write lock
    cursor.close()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """FastAPI dependency que fornece sessão de banco e fecha ao finalizar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
