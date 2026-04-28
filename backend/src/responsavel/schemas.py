from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, ConfigDict


class FilhoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    turma_nome: Optional[str] = None


class DisciplinaBoletimRow(BaseModel):
    disciplina_id: int
    disciplina_nome: str
    bim1: Optional[float] = None
    bim2: Optional[float] = None
    bim3: Optional[float] = None
    bim4: Optional[float] = None
    media: Optional[float] = None
    total_aulas: int
    total_presentes: int
    freq_pct: Optional[float] = None
    aprovado: bool
