"""
Admin API router — all endpoints require admin JWT.

Security:
- admin_required = Depends(require_role("admin")) applied to every endpoint (T-03-01)
- Plaintext passwords never returned in responses
- Soft delete only — no hard DELETE operations
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.database import get_db
from src.auth.dependencies import require_role
from src.models.usuario import Usuario
from . import schemas, service

router = APIRouter(prefix="/admin", tags=["admin"])
admin_required = Depends(require_role("admin"))


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

@router.get("/dashboard", response_model=schemas.DashboardCounts)
def dashboard(db: Session = Depends(get_db), _: Usuario = admin_required):
    return service.get_dashboard_counts(db)


# ---------------------------------------------------------------------------
# Alunos
# ---------------------------------------------------------------------------

@router.get("/alunos", response_model=schemas.PaginatedAlunos)
def list_alunos(
    page: int = Query(1, ge=1),
    search: str = Query(""),
    db: Session = Depends(get_db),
    _: Usuario = admin_required,
):
    return service.list_alunos(db, page=page, per_page=25, search=search)


@router.post("/alunos", response_model=schemas.AlunoOut, status_code=201)
def create_aluno(
    body: schemas.AlunoCreate,
    db: Session = Depends(get_db),
    _: Usuario = admin_required,
):
    return service.create_aluno(db, body)


@router.put("/alunos/{aluno_id}", response_model=schemas.AlunoOut)
def update_aluno(
    aluno_id: int,
    body: schemas.AlunoUpdate,
    db: Session = Depends(get_db),
    _: Usuario = admin_required,
):
    return service.update_aluno(db, aluno_id, body)


@router.post("/alunos/{aluno_id}/deactivate", response_model=schemas.AlunoOut)
def deactivate_aluno(
    aluno_id: int,
    db: Session = Depends(get_db),
    _: Usuario = admin_required,
):
    return service.deactivate_aluno(db, aluno_id)


# ---------------------------------------------------------------------------
# Turmas
# ---------------------------------------------------------------------------

@router.get("/turmas", response_model=schemas.PaginatedTurmas)
def list_turmas(
    page: int = Query(1, ge=1),
    search: str = Query(""),
    db: Session = Depends(get_db),
    _: Usuario = admin_required,
):
    return service.list_turmas(db, page=page, per_page=25, search=search)


@router.post("/turmas", response_model=schemas.TurmaOut, status_code=201)
def create_turma(
    body: schemas.TurmaCreate,
    db: Session = Depends(get_db),
    _: Usuario = admin_required,
):
    return service.create_turma(db, body)


@router.put("/turmas/{turma_id}", response_model=schemas.TurmaOut)
def update_turma(
    turma_id: int,
    body: schemas.TurmaUpdate,
    db: Session = Depends(get_db),
    _: Usuario = admin_required,
):
    return service.update_turma(db, turma_id, body)


# ---------------------------------------------------------------------------
# Disciplinas
# ---------------------------------------------------------------------------

@router.get("/disciplinas", response_model=schemas.PaginatedDisciplinas)
def list_disciplinas(
    page: int = Query(1, ge=1),
    search: str = Query(""),
    db: Session = Depends(get_db),
    _: Usuario = admin_required,
):
    return service.list_disciplinas(db, page=page, per_page=25, search=search)


@router.post("/disciplinas", response_model=schemas.DisciplinaOut, status_code=201)
def create_disciplina(
    body: schemas.DisciplinaCreate,
    db: Session = Depends(get_db),
    _: Usuario = admin_required,
):
    return service.create_disciplina(db, body)


@router.put("/disciplinas/{disc_id}", response_model=schemas.DisciplinaOut)
def update_disciplina(
    disc_id: int,
    body: schemas.DisciplinaUpdate,
    db: Session = Depends(get_db),
    _: Usuario = admin_required,
):
    return service.update_disciplina(db, disc_id, body)


# ---------------------------------------------------------------------------
# Professores
# ---------------------------------------------------------------------------

@router.get("/professores", response_model=schemas.PaginatedProfessores)
def list_professores(
    page: int = Query(1, ge=1),
    search: str = Query(""),
    db: Session = Depends(get_db),
    _: Usuario = admin_required,
):
    return service.list_professores(db, page=page, per_page=25, search=search)


@router.post("/professores", response_model=schemas.ProfessorOut, status_code=201)
def create_professor(
    body: schemas.ProfessorCreate,
    db: Session = Depends(get_db),
    _: Usuario = admin_required,
):
    return service.create_professor(db, body)


@router.put("/professores/{prof_id}", response_model=schemas.ProfessorOut)
def update_professor(
    prof_id: int,
    body: schemas.ProfessorUpdate,
    db: Session = Depends(get_db),
    _: Usuario = admin_required,
):
    return service.update_professor(db, prof_id, body)


@router.post("/professores/{prof_id}/deactivate", response_model=schemas.ProfessorOut)
def deactivate_professor(
    prof_id: int,
    db: Session = Depends(get_db),
    _: Usuario = admin_required,
):
    return service.deactivate_professor(db, prof_id)


# ---------------------------------------------------------------------------
# Responsaveis
# ---------------------------------------------------------------------------

@router.get("/responsaveis", response_model=schemas.PaginatedResponsaveis)
def list_responsaveis(
    page: int = Query(1, ge=1),
    search: str = Query(""),
    db: Session = Depends(get_db),
    _: Usuario = admin_required,
):
    return service.list_responsaveis(db, page=page, per_page=25, search=search)


@router.post("/responsaveis", response_model=schemas.ResponsavelOut, status_code=201)
def create_responsavel(
    body: schemas.ResponsavelCreate,
    db: Session = Depends(get_db),
    _: Usuario = admin_required,
):
    return service.create_responsavel(db, body)


@router.put("/responsaveis/{resp_id}", response_model=schemas.ResponsavelOut)
def update_responsavel(
    resp_id: int,
    body: schemas.ResponsavelUpdate,
    db: Session = Depends(get_db),
    _: Usuario = admin_required,
):
    return service.update_responsavel(db, resp_id, body)


@router.post("/responsaveis/{resp_id}/deactivate", response_model=schemas.ResponsavelOut)
def deactivate_responsavel(
    resp_id: int,
    db: Session = Depends(get_db),
    _: Usuario = admin_required,
):
    return service.deactivate_responsavel(db, resp_id)


# ---------------------------------------------------------------------------
# Usuario deactivation (T-03-03: self-deactivation guard)
# ---------------------------------------------------------------------------

@router.post("/usuarios/{usuario_id}/deactivate")
def deactivate_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    caller: Usuario = Depends(require_role("admin")),
):
    return service.deactivate_usuario(db, target_id=usuario_id, caller_id=caller.id)
