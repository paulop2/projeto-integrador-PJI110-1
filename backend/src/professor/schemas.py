"""
Pydantic v2 schemas for professor endpoints.
All *Out schemas use model_config = ConfigDict(from_attributes=True) for SQLAlchemy -> Pydantic.
"""
from __future__ import annotations
from datetime import date
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


# --- Turma schemas ---

class TurmaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    disciplinas: List[str] = []
    num_alunos: int = 0
    media_geral: Optional[float] = None
    pct_aprovados: Optional[float] = None


# --- Chamada schemas ---

class PresencaIn(BaseModel):
    aluno_id: int
    presente: bool

class ChamadaCreate(BaseModel):
    disciplina_id: int
    data: date
    presencas: List[PresencaIn]

class PresencaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    aluno_id: int
    presente: bool

class ChamadaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    data: date
    presencas: List[PresencaOut] = []


# --- Notas schemas ---

class GradeIn(BaseModel):
    aluno_id: int
    bimestre: int
    valor: float

class NotasCreate(BaseModel):
    disciplina_id: int
    grades: List[GradeIn]

class NoteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    aluno_id: int
    bimestre: int
    valor: float

class NotasOut(BaseModel):
    aluno_id: int
    nome: str
    notas: List[NoteOut] = []


# --- Frequencia schemas ---

class FrequenciaRow(BaseModel):
    aluno_id: int
    nome: str
    total_aulas: int
    total_presentes: int
    percentual: float
