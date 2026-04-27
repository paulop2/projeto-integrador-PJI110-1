from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class Professor(Base):
    __tablename__ = "professores"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    cpf: Mapped[str | None] = mapped_column(String(14), nullable=True)
