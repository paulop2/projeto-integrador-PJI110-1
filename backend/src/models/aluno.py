from datetime import date
from sqlalchemy import String, Boolean, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class Aluno(Base):
    __tablename__ = "alunos"

    id: Mapped[int] = mapped_column(primary_key=True)
    matricula: Mapped[str | None] = mapped_column(String(20), unique=True, nullable=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    data_nascimento: Mapped[date | None] = mapped_column(Date, nullable=True)
    responsavel_id: Mapped[int | None] = mapped_column(
        ForeignKey("responsaveis.id", ondelete="SET NULL"), nullable=True
    )
    turma_id: Mapped[int | None] = mapped_column(
        ForeignKey("turmas.id", ondelete="SET NULL"), nullable=True
    )
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
