from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class Turma(Base):
    __tablename__ = "turmas"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    ano: Mapped[int] = mapped_column(Integer, nullable=False)
    serie: Mapped[str] = mapped_column(String(50), nullable=False)
    turno: Mapped[str] = mapped_column(String(20), nullable=False)
