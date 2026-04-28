"""
Responsavel API router — all endpoints require responsavel JWT.

Security:
- responsavel_required = Depends(require_role("responsavel")) applied to every endpoint
- Ownership enforced via _assert_responsavel_owns_aluno in service layer
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.database import get_db
from src.auth.dependencies import require_role
from src.models.usuario import Usuario
from . import schemas, service

router = APIRouter(prefix="/responsavel", tags=["responsavel"])
responsavel_required = Depends(require_role("responsavel"))


@router.get("/meus-filhos", response_model=list[schemas.FilhoOut])
def get_meus_filhos(
    db: Session = Depends(get_db),
    current_user: Usuario = responsavel_required,
):
    return service.get_meus_filhos(db, current_user)


@router.get("/boletim", response_model=list[schemas.DisciplinaBoletimRow])
def get_boletim(
    aluno_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user: Usuario = responsavel_required,
):
    return service.get_boletim(db, current_user, aluno_id)
