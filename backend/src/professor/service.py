"""
Professor service layer — chamada, notas, and frequencia business logic.

Patterns:
- _get_professor() helper resolves professor_id from current_user (Usuario) on every call
- _assert_professor_owns_turma() ownership check called at start of every turma-specific function
- db.query() style consistent with admin/service.py
- Chamada: find-or-create + delete+insert presencas (replace-all)
- Notas: find-or-create avaliacao per bimestre + upsert nota
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException

from src.models.usuario import Usuario
from src.models.professor import Professor
from src.models.professor_turma import ProfessorTurma
from src.models.turma import Turma
from src.models.disciplina import Disciplina
from src.models.aluno import Aluno
from src.models.chamada import Chamada
from src.models.presenca import Presenca
from src.models.avaliacao import Avaliacao
from src.models.nota import Nota
from . import schemas


def _get_professor(db: Session, usuario: Usuario) -> Professor:
    """Resolve professor.id from current_user (Usuario). Raises 404 if professor profile not found."""
    prof = db.query(Professor).filter(Professor.usuario_id == usuario.id).first()
    if not prof:
        raise HTTPException(status_code=404, detail="Perfil de professor não encontrado")
    return prof


def _assert_professor_owns_turma(db: Session, professor_id: int, turma_id: int) -> None:
    """Raises 403 if professor is not linked to the turma via professor_turma."""
    link = db.query(ProfessorTurma).filter(
        ProfessorTurma.professor_id == professor_id,
        ProfessorTurma.turma_id == turma_id,
    ).first()
    if not link:
        raise HTTPException(status_code=403, detail="Acesso negado a esta turma")


def get_minhas_turmas(db: Session, current_user: Usuario) -> list:
    raise NotImplementedError("Wave 2: implement in Plan 02")


def get_chamada(db: Session, current_user: Usuario, turma_id: int, date_str: str):
    raise NotImplementedError("Wave 2: implement in Plan 02")


def upsert_chamada(db: Session, current_user: Usuario, turma_id: int, payload: schemas.ChamadaCreate):
    raise NotImplementedError("Wave 2: implement in Plan 02")


def get_notas(db: Session, current_user: Usuario, turma_id: int, disciplina_id: int) -> list:
    raise NotImplementedError("Wave 2: implement in Plan 02")


def upsert_notas(db: Session, current_user: Usuario, turma_id: int, payload: schemas.NotasCreate):
    raise NotImplementedError("Wave 2: implement in Plan 02")


def get_frequencia(db: Session, current_user: Usuario, turma_id: int) -> list:
    raise NotImplementedError("Wave 2: implement in Plan 02")
