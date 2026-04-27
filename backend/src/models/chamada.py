from datetime import date, datetime
from sqlalchemy import Date, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from src.database import Base

class Chamada(Base):
    __tablename__ = "chamadas"
    id: Mapped[int] = mapped_column(primary_key=True)
    turma_id: Mapped[int] = mapped_column(ForeignKey("turmas.id", ondelete="CASCADE"))
    disciplina_id: Mapped[int] = mapped_column(ForeignKey("disciplinas.id", ondelete="CASCADE"))
    professor_id: Mapped[int] = mapped_column(ForeignKey("professores.id", ondelete="CASCADE"))
    data: Mapped[date] = mapped_column(Date, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
