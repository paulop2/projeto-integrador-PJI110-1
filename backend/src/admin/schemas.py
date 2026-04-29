"""
Pydantic v2 schemas for admin CRUD endpoints.
All *Out schemas use model_config = ConfigDict(from_attributes=True) for SQLAlchemy → Pydantic.
All *Create/*Update schemas use default extra="ignore" (Pydantic v2 default).
"""
from __future__ import annotations
from datetime import date
from typing import List, Optional
from pydantic import BaseModel, EmailStr, ConfigDict


# ---------------------------------------------------------------------------
# Alunos
# ---------------------------------------------------------------------------
class AlunoCreate(BaseModel):
    nome: str
    data_nascimento: Optional[date] = None
    turma_id: Optional[int] = None
    responsavel_id: Optional[int] = None


class AlunoUpdate(BaseModel):
    nome: Optional[str] = None
    data_nascimento: Optional[date] = None
    turma_id: Optional[int] = None
    responsavel_id: Optional[int] = None


class AlunoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    matricula: Optional[str]
    nome: str
    data_nascimento: Optional[date]
    turma_id: Optional[int]
    turma_nome: Optional[str] = None
    responsavel_id: Optional[int]
    ativo: bool


class PaginatedAlunos(BaseModel):
    items: List[AlunoOut]
    total: int
    page: int
    per_page: int


# ---------------------------------------------------------------------------
# Turmas
# ---------------------------------------------------------------------------
class ProfessorTurmaRow(BaseModel):
    """One row in the professor_turma junction for create/update."""
    disciplina_id: int
    professor_id: int


class TurmaCreate(BaseModel):
    nome: str
    ano: int
    serie: str
    turno: str
    professor_turma: List[ProfessorTurmaRow] = []


class TurmaUpdate(BaseModel):
    nome: Optional[str] = None
    ano: Optional[int] = None
    serie: Optional[str] = None
    turno: Optional[str] = None
    professor_turma: Optional[List[ProfessorTurmaRow]] = None


class TurmaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    ano: int
    serie: str
    turno: str
    professor_turma: List[ProfessorTurmaRow] = []


class PaginatedTurmas(BaseModel):
    items: List[TurmaOut]
    total: int
    page: int
    per_page: int


# ---------------------------------------------------------------------------
# Disciplinas
# ---------------------------------------------------------------------------
class DisciplinaCreate(BaseModel):
    nome: str
    carga_horaria: Optional[int] = None


class DisciplinaUpdate(BaseModel):
    nome: Optional[str] = None
    carga_horaria: Optional[int] = None


class DisciplinaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    carga_horaria: Optional[int]


class PaginatedDisciplinas(BaseModel):
    items: List[DisciplinaOut]
    total: int
    page: int
    per_page: int


# ---------------------------------------------------------------------------
# Professores (creates Usuario + Professor atomically)
# ---------------------------------------------------------------------------
class ProfessorCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    cpf: Optional[str] = None


class ProfessorUpdate(BaseModel):
    nome: Optional[str] = None
    cpf: Optional[str] = None


class ProfessorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    cpf: Optional[str]
    usuario_id: int
    email: Optional[str] = None


class PaginatedProfessores(BaseModel):
    items: List[ProfessorOut]
    total: int
    page: int
    per_page: int


# ---------------------------------------------------------------------------
# Responsaveis (creates Usuario + Responsavel + links alunos)
# ---------------------------------------------------------------------------
class ResponsavelCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    cpf: Optional[str] = None
    telefone: Optional[str] = None
    aluno_ids: List[int] = []


class ResponsavelUpdate(BaseModel):
    nome: Optional[str] = None
    cpf: Optional[str] = None
    telefone: Optional[str] = None
    aluno_ids: Optional[List[int]] = None


class ResponsavelOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    cpf: Optional[str]
    telefone: Optional[str]
    usuario_id: int
    email: Optional[str] = None
    aluno_ids: List[int] = []


class PaginatedResponsaveis(BaseModel):
    items: List[ResponsavelOut]
    total: int
    page: int
    per_page: int


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------
class DashboardCounts(BaseModel):
    alunos: int
    turmas: int
    disciplinas: int
    professores: int
    responsaveis: int


class TurmaDesempenhoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    turma_id: int
    turma_nome: str
    num_alunos: int
    media_geral: Optional[float] = None
    pct_aprovados: Optional[float] = None


class UsuarioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    tipo: str
    ativo: bool


class DashboardDesempenho(BaseModel):
    turmas: List[TurmaDesempenhoOut]
    alunos_em_risco: int
