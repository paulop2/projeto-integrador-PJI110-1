"""
Professor API router — all endpoints require professor JWT.

Security:
- professor_required = Depends(require_role("professor")) applied to every endpoint
- Ownership check via _assert_professor_owns_turma on all turma-specific endpoints
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.database import get_db
from src.auth.dependencies import require_role
from src.models.usuario import Usuario
from . import schemas, service

router = APIRouter(prefix="/professor", tags=["professor"])
professor_required = Depends(require_role("professor"))


@router.get("/minhas-turmas", response_model=list[schemas.TurmaOut])
def get_minhas_turmas(
    db: Session = Depends(get_db),
    current_user: Usuario = professor_required,
):
    return service.get_minhas_turmas(db, current_user)


@router.get("/turmas/{turma_id}/alunos", response_model=list[schemas.AlunoOut])
def get_turma_alunos(
    turma_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = professor_required,
):
    return service.get_turma_alunos(db, current_user, turma_id)


@router.get("/turmas/{turma_id}/disciplinas", response_model=list[schemas.DisciplinaOut])
def get_turma_disciplinas(
    turma_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = professor_required,
):
    return service.get_turma_disciplinas(db, current_user, turma_id)


@router.get("/turmas/{turma_id}/chamada")
def get_chamada(
    turma_id: int,
    date: str = Query(...),
    db: Session = Depends(get_db),
    current_user: Usuario = professor_required,
):
    return service.get_chamada(db, current_user, turma_id, date)


@router.post("/turmas/{turma_id}/chamada", status_code=200)
def upsert_chamada(
    turma_id: int,
    payload: schemas.ChamadaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = professor_required,
):
    return service.upsert_chamada(db, current_user, turma_id, payload)


@router.get("/turmas/{turma_id}/notas")
def get_notas(
    turma_id: int,
    disciplina_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user: Usuario = professor_required,
):
    return service.get_notas(db, current_user, turma_id, disciplina_id)


@router.post("/turmas/{turma_id}/notas", status_code=200)
def upsert_notas(
    turma_id: int,
    payload: schemas.NotasCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = professor_required,
):
    return service.upsert_notas(db, current_user, turma_id, payload)


@router.get("/turmas/{turma_id}/frequencia", response_model=list[schemas.FrequenciaRow])
def get_frequencia(
    turma_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = professor_required,
):
    return service.get_frequencia(db, current_user, turma_id)
