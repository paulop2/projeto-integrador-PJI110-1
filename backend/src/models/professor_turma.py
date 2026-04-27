from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class ProfessorTurma(Base):
    __tablename__ = "professor_turma"

    professor_id: Mapped[int] = mapped_column(
        ForeignKey("professores.id", ondelete="CASCADE"), primary_key=True
    )
    turma_id: Mapped[int] = mapped_column(
        ForeignKey("turmas.id", ondelete="CASCADE"), primary_key=True
    )
    disciplina_id: Mapped[int] = mapped_column(
        ForeignKey("disciplinas.id", ondelete="CASCADE"), primary_key=True
    )
