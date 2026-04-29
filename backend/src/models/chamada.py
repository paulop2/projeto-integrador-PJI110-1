from datetime import date, datetime
from sqlalchemy import Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from src.database import Base

class Chamada(Base):
    __tablename__ = "chamadas"
    __table_args__ = (
        UniqueConstraint("turma_id", "disciplina_id", "professor_id", "data", name="uq_chamadas_turma_disc_prof_data"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    turma_id: Mapped[int] = mapped_column(ForeignKey("turmas.id", ondelete="CASCADE"))
    disciplina_id: Mapped[int] = mapped_column(ForeignKey("disciplinas.id", ondelete="CASCADE"))
    professor_id: Mapped[int] = mapped_column(ForeignKey("professores.id", ondelete="CASCADE"))
    data: Mapped[date] = mapped_column(Date, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
