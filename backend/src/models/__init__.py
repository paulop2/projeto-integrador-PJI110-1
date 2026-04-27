from src.models.usuario import Usuario, ResetToken, TipoUsuario
from src.models.aluno import Aluno
from src.models.turma import Turma
from src.models.disciplina import Disciplina
from src.models.professor import Professor
from src.models.responsavel import Responsavel
from src.models.professor_turma import ProfessorTurma

__all__ = [
    "Usuario", "ResetToken", "TipoUsuario",
    "Aluno", "Turma", "Disciplina",
    "Professor", "Responsavel", "ProfessorTurma",
]
