from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base

class Presenca(Base):
    __tablename__ = "presencas"
    __table_args__ = (UniqueConstraint("chamada_id", "aluno_id", name="uq_presencas_chamada_id_aluno_id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    chamada_id: Mapped[int] = mapped_column(ForeignKey("chamadas.id", ondelete="CASCADE"))
    aluno_id: Mapped[int] = mapped_column(ForeignKey("alunos.id", ondelete="CASCADE"))
    presente: Mapped[bool] = mapped_column(Boolean, nullable=False)
    justificativa: Mapped[str | None] = mapped_column(String(500), nullable=True)
