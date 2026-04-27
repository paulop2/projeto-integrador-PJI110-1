from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class Disciplina(Base):
    __tablename__ = "disciplinas"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    carga_horaria: Mapped[int | None] = mapped_column(Integer, nullable=True)
