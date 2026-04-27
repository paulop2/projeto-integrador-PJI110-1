from sqlalchemy import Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base

class Nota(Base):
    __tablename__ = "notas"
    __table_args__ = (UniqueConstraint("avaliacao_id", "aluno_id", name="uq_notas_avaliacao_id_aluno_id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    avaliacao_id: Mapped[int] = mapped_column(ForeignKey("avaliacoes.id", ondelete="CASCADE"))
    aluno_id: Mapped[int] = mapped_column(ForeignKey("alunos.id", ondelete="CASCADE"))
    valor: Mapped[float] = mapped_column(Float, nullable=False)
