"""
Admin service layer — all CRUD business logic.

Patterns:
- db.query() style (matches existing codebase in password_reset/service.py)
- hash_password imported from src.auth.service — never redefined
- Soft delete: record.ativo = False — never db.delete()
- Atomic creates: db.flush() before db.commit() to get auto-id for profile rows
- professor_turma: replace-all strategy (delete existing + insert fresh)
- Matricula generation: MAT{year}{id:05d} — generated after db.flush()
"""
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from fastapi import HTTPException

from src.models.usuario import Usuario, TipoUsuario
from src.models.aluno import Aluno
from src.models.turma import Turma
from src.models.disciplina import Disciplina
from src.models.professor import Professor
from src.models.responsavel import Responsavel
from src.models.professor_turma import ProfessorTurma
from src.auth.service import hash_password
from . import schemas


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

def get_dashboard_counts(db: Session) -> dict:
    alunos = db.query(Aluno).filter(Aluno.ativo == True).count()
    turmas = db.query(Turma).count()
    disciplinas = db.query(Disciplina).count()
    professores = db.query(Professor).join(Usuario, Professor.usuario_id == Usuario.id).filter(Usuario.ativo == True).count()
    responsaveis = db.query(Responsavel).join(Usuario, Responsavel.usuario_id == Usuario.id).filter(Usuario.ativo == True).count()
    return {
        "alunos": alunos,
        "turmas": turmas,
        "disciplinas": disciplinas,
        "professores": professores,
        "responsaveis": responsaveis,
    }


# ---------------------------------------------------------------------------
# Alunos
# ---------------------------------------------------------------------------

def _generate_matricula(year: int, aluno_id: int) -> str:
    return f"MAT{year}{aluno_id:05d}"


def list_alunos(db: Session, page: int, per_page: int, search: str) -> dict:
    q = db.query(Aluno).filter(Aluno.ativo == True)
    if search:
        q = q.filter(Aluno.nome.ilike(f"%{search}%"))
    total = q.count()
    items = q.order_by(Aluno.nome).offset((page - 1) * per_page).limit(per_page).all()
    # Enrich with turma_nome
    result = []
    for aluno in items:
        turma_nome = None
        if aluno.turma_id:
            turma = db.query(Turma).filter(Turma.id == aluno.turma_id).first()
            turma_nome = turma.nome if turma else None
        out = schemas.AlunoOut.model_validate(aluno)
        out.turma_nome = turma_nome
        result.append(out)
    return {"items": result, "total": total, "page": page, "per_page": per_page}


def create_aluno(db: Session, body: schemas.AlunoCreate) -> Aluno:
    aluno = Aluno(
        nome=body.nome,
        data_nascimento=body.data_nascimento,
        turma_id=body.turma_id,
        responsavel_id=body.responsavel_id,
        ativo=True,
    )
    db.add(aluno)
    db.flush()  # assigns aluno.id before commit
    aluno.matricula = _generate_matricula(datetime.utcnow().year, aluno.id)
    db.commit()
    db.refresh(aluno)
    return aluno


def update_aluno(db: Session, aluno_id: int, body: schemas.AlunoUpdate) -> Aluno:
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(aluno, field, value)
    db.commit()
    db.refresh(aluno)
    return aluno


def deactivate_aluno(db: Session, aluno_id: int) -> Aluno:
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    aluno.ativo = False
    db.commit()
    db.refresh(aluno)
    return aluno


# ---------------------------------------------------------------------------
# Turmas
# ---------------------------------------------------------------------------

def list_turmas(db: Session, page: int, per_page: int, search: str) -> dict:
    q = db.query(Turma)
    if search:
        q = q.filter(Turma.nome.ilike(f"%{search}%"))
    total = q.count()
    items = q.order_by(Turma.nome).offset((page - 1) * per_page).limit(per_page).all()
    return {"items": items, "total": total, "page": page, "per_page": per_page}


def _sync_professor_turma(db: Session, turma_id: int, rows: list) -> None:
    """Replace-all: delete all existing professor_turma rows for this turma, insert fresh."""
    db.query(ProfessorTurma).filter(ProfessorTurma.turma_id == turma_id).delete(synchronize_session=False)
    for row in rows:
        db.add(ProfessorTurma(
            turma_id=turma_id,
            disciplina_id=row.disciplina_id,
            professor_id=row.professor_id,
        ))


def create_turma(db: Session, body: schemas.TurmaCreate) -> Turma:
    turma = Turma(nome=body.nome, ano=body.ano, serie=body.serie, turno=body.turno)
    db.add(turma)
    db.flush()  # assigns turma.id
    _sync_professor_turma(db, turma.id, body.professor_turma)
    db.commit()
    db.refresh(turma)
    return turma


def update_turma(db: Session, turma_id: int, body: schemas.TurmaUpdate) -> Turma:
    turma = db.query(Turma).filter(Turma.id == turma_id).first()
    if not turma:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    for field, value in body.model_dump(exclude_unset=True, exclude={"professor_turma"}).items():
        setattr(turma, field, value)
    if body.professor_turma is not None:
        _sync_professor_turma(db, turma_id, body.professor_turma)
    db.commit()
    db.refresh(turma)
    return turma


# ---------------------------------------------------------------------------
# Disciplinas
# ---------------------------------------------------------------------------

def list_disciplinas(db: Session, page: int, per_page: int, search: str) -> dict:
    q = db.query(Disciplina)
    if search:
        q = q.filter(Disciplina.nome.ilike(f"%{search}%"))
    total = q.count()
    items = q.order_by(Disciplina.nome).offset((page - 1) * per_page).limit(per_page).all()
    return {"items": items, "total": total, "page": page, "per_page": per_page}


def create_disciplina(db: Session, body: schemas.DisciplinaCreate) -> Disciplina:
    d = Disciplina(nome=body.nome, carga_horaria=body.carga_horaria)
    db.add(d)
    db.commit()
    db.refresh(d)
    return d


def update_disciplina(db: Session, disc_id: int, body: schemas.DisciplinaUpdate) -> Disciplina:
    d = db.query(Disciplina).filter(Disciplina.id == disc_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(d, field, value)
    db.commit()
    db.refresh(d)
    return d


# ---------------------------------------------------------------------------
# Professores
# ---------------------------------------------------------------------------

def list_professores(db: Session, page: int, per_page: int, search: str) -> dict:
    q = db.query(Professor)
    if search:
        q = q.filter(Professor.nome.ilike(f"%{search}%"))
    total = q.count()
    items = q.order_by(Professor.nome).offset((page - 1) * per_page).limit(per_page).all()
    # Enrich with email from usuario
    result = []
    for prof in items:
        usuario = db.query(Usuario).filter(Usuario.id == prof.usuario_id).first()
        out = schemas.ProfessorOut.model_validate(prof)
        out.email = usuario.email if usuario else None
        result.append(out)
    return {"items": result, "total": total, "page": page, "per_page": per_page}


def create_professor(db: Session, body: schemas.ProfessorCreate) -> Professor:
    existing = db.query(Usuario).filter(Usuario.email == body.email.lower()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    usuario = Usuario(
        email=body.email.lower(),
        senha_hash=hash_password(body.senha),
        tipo=TipoUsuario.professor,
        ativo=True,
    )
    db.add(usuario)
    db.flush()  # assigns usuario.id — both rows committed together (T-03-02)
    professor = Professor(usuario_id=usuario.id, nome=body.nome, cpf=body.cpf)
    db.add(professor)
    db.commit()
    db.refresh(professor)
    return professor


def update_professor(db: Session, prof_id: int, body: schemas.ProfessorUpdate) -> Professor:
    prof = db.query(Professor).filter(Professor.id == prof_id).first()
    if not prof:
        raise HTTPException(status_code=404, detail="Professor não encontrado")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(prof, field, value)
    db.commit()
    db.refresh(prof)
    return prof


def deactivate_professor(db: Session, prof_id: int) -> Professor:
    prof = db.query(Professor).filter(Professor.id == prof_id).first()
    if not prof:
        raise HTTPException(status_code=404, detail="Professor não encontrado")
    usuario = db.query(Usuario).filter(Usuario.id == prof.usuario_id).first()
    if usuario:
        usuario.ativo = False
    db.commit()
    db.refresh(prof)
    return prof


# ---------------------------------------------------------------------------
# Responsaveis
# ---------------------------------------------------------------------------

def list_responsaveis(db: Session, page: int, per_page: int, search: str) -> dict:
    q = db.query(Responsavel)
    if search:
        q = q.filter(Responsavel.nome.ilike(f"%{search}%"))
    total = q.count()
    items = q.order_by(Responsavel.nome).offset((page - 1) * per_page).limit(per_page).all()
    result = []
    for resp in items:
        usuario = db.query(Usuario).filter(Usuario.id == resp.usuario_id).first()
        out = schemas.ResponsavelOut.model_validate(resp)
        out.email = usuario.email if usuario else None
        result.append(out)
    return {"items": result, "total": total, "page": page, "per_page": per_page}


def create_responsavel(db: Session, body: schemas.ResponsavelCreate) -> Responsavel:
    existing = db.query(Usuario).filter(Usuario.email == body.email.lower()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    usuario = Usuario(
        email=body.email.lower(),
        senha_hash=hash_password(body.senha),
        tipo=TipoUsuario.responsavel,
        ativo=True,
    )
    db.add(usuario)
    db.flush()  # assigns usuario.id — both rows committed together (T-03-02)
    responsavel = Responsavel(
        usuario_id=usuario.id,
        nome=body.nome,
        cpf=body.cpf,
        telefone=body.telefone,
    )
    db.add(responsavel)
    db.flush()  # assigns responsavel.id so we can link alunos
    # Link alunos — update responsavel_id FK on each aluno
    for aluno_id in body.aluno_ids:
        aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
        if aluno:
            aluno.responsavel_id = responsavel.id
    db.commit()
    db.refresh(responsavel)
    return responsavel


def update_responsavel(db: Session, resp_id: int, body: schemas.ResponsavelUpdate) -> Responsavel:
    resp = db.query(Responsavel).filter(Responsavel.id == resp_id).first()
    if not resp:
        raise HTTPException(status_code=404, detail="Responsável não encontrado")
    for field, value in body.model_dump(exclude_unset=True, exclude={"aluno_ids"}).items():
        setattr(resp, field, value)
    if body.aluno_ids is not None:
        # Remove existing links for this responsavel
        db.query(Aluno).filter(Aluno.responsavel_id == resp_id).update(
            {"responsavel_id": None}, synchronize_session=False
        )
        for aluno_id in body.aluno_ids:
            aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
            if aluno:
                aluno.responsavel_id = resp_id
    db.commit()
    db.refresh(resp)
    return resp


def deactivate_responsavel(db: Session, resp_id: int) -> Responsavel:
    resp = db.query(Responsavel).filter(Responsavel.id == resp_id).first()
    if not resp:
        raise HTTPException(status_code=404, detail="Responsável não encontrado")
    usuario = db.query(Usuario).filter(Usuario.id == resp.usuario_id).first()
    if usuario:
        usuario.ativo = False
    db.commit()
    db.refresh(resp)
    return resp


# ---------------------------------------------------------------------------
# Admin self-deactivation guard (T-03-03)
# ---------------------------------------------------------------------------

def deactivate_usuario(db: Session, target_id: int, caller_id: int) -> Usuario:
    """Deactivate a usuario account. Refuses if target is the caller themselves."""
    if target_id == caller_id:
        raise HTTPException(status_code=400, detail="Admin não pode desativar a própria conta")
    usuario = db.query(Usuario).filter(Usuario.id == target_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    usuario.ativo = False
    db.commit()
    db.refresh(usuario)
    return usuario
