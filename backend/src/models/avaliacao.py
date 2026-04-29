from datetime import date
from sqlalchemy import CheckConstraint, Date, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base

class Avaliacao(Base):
    __tablename__ = "avaliacoes"
    __table_args__ = (
        CheckConstraint("bimestre IN (1, 2, 3, 4)", name="ck_avaliacoes_bimestre"),
        CheckConstraint("valor_maximo > 0", name="ck_avaliacoes_valor_maximo"),
        UniqueConstraint("turma_id", "disciplina_id", "professor_id", "bimestre", name="uq_avaliacoes_turma_disc_prof_bimestre"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    turma_id: Mapped[int] = mapped_column(ForeignKey("turmas.id", ondelete="CASCADE"))
    disciplina_id: Mapped[int] = mapped_column(ForeignKey("disciplinas.id", ondelete="CASCADE"))
    professor_id: Mapped[int] = mapped_column(ForeignKey("professores.id", ondelete="CASCADE"))
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    bimestre: Mapped[int] = mapped_column(Integer, nullable=False)
    valor_maximo: Mapped[float] = mapped_column(Float, nullable=False, default=10.0)
    data: Mapped[date | None] = mapped_column(Date, nullable=True)
