"""
Responsavel service layer — boletim and frequencia business logic (read-only).

Security:
- _get_responsavel() resolves responsavel.id from current_user (Usuario) on every call
- _assert_responsavel_owns_aluno() ownership check called at start of every aluno-specific function
  - Returns 403 (NOT 404) when aluno does not belong to current responsavel — IDOR prevention
  - Never filter chamadas by professor_id — count ALL chamadas for (turma_id, disciplina_id)
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.models.usuario import Usuario
from src.models.responsavel import Responsavel
from src.models.aluno import Aluno
from src.models.turma import Turma
from src.models.disciplina import Disciplina
from src.models.professor_turma import ProfessorTurma
from src.models.chamada import Chamada
from src.models.presenca import Presenca
from src.models.avaliacao import Avaliacao
from src.models.nota import Nota


def _get_responsavel(db: Session, usuario: Usuario) -> Responsavel:
    """Resolve responsavel.id from current_user (Usuario). Raises 404 if profile not found."""
    resp = db.query(Responsavel).filter(Responsavel.usuario_id == usuario.id).first()
    if not resp:
        raise HTTPException(status_code=404, detail="Perfil de responsável não encontrado")
    return resp


def _assert_responsavel_owns_aluno(db: Session, responsavel_id: int, aluno_id: int) -> Aluno:
    """
    Raises 403 if the aluno is not linked to this responsavel.
    Returns the aluno on success (avoids a second query).
    CRITICAL: Returns 403 (not 404) — 404 leaks aluno existence.
    """
    aluno = db.query(Aluno).filter(
        Aluno.id == aluno_id,
        Aluno.responsavel_id == responsavel_id,
    ).first()
    if not aluno:
        raise HTTPException(status_code=403, detail="Acesso negado a este aluno")
    return aluno


def get_meus_filhos(db: Session, current_user: Usuario) -> list:
    resp = _get_responsavel(db, current_user)
    alunos = db.query(Aluno).filter(
        Aluno.responsavel_id == resp.id,
        Aluno.ativo == True,
    ).all()
    result = []
    for aluno in alunos:
        turma_nome = None
        if aluno.turma_id:
            turma = db.query(Turma).filter(Turma.id == aluno.turma_id).first()
            turma_nome = turma.nome if turma else None
        result.append({"id": aluno.id, "nome": aluno.nome, "turma_nome": turma_nome})
    return result


def get_boletim(db: Session, current_user: Usuario, aluno_id: int) -> list:
    resp = _get_responsavel(db, current_user)
    aluno = _assert_responsavel_owns_aluno(db, resp.id, aluno_id)

    if not aluno.turma_id:
        return []  # aluno not enrolled in any turma

    # Step 1: Discover all disciplinas taught in aluno's turma via professor_turma
    disciplina_ids = (
        db.query(ProfessorTurma.disciplina_id)
        .filter(ProfessorTurma.turma_id == aluno.turma_id)
        .distinct()
        .all()
    )
    disciplina_ids = [row[0] for row in disciplina_ids]

    result = []
    for disc_id in disciplina_ids:
        disciplina = db.query(Disciplina).filter(Disciplina.id == disc_id).first()
        if not disciplina:
            continue

        # Step 2: Notas — one entry per bimestre (1-4)
        avaliacoes = db.query(Avaliacao).filter(
            Avaliacao.turma_id == aluno.turma_id,
            Avaliacao.disciplina_id == disc_id,
        ).all()
        BIMESTRES = {1, 2, 3, 4}
        notas_por_bimestre: dict = {b: None for b in BIMESTRES}
        for av in avaliacoes:
            if av.bimestre not in BIMESTRES:
                continue
            nota = db.query(Nota).filter(
                Nota.avaliacao_id == av.id,
                Nota.aluno_id == aluno.id,
            ).first()
            if nota:
                notas_por_bimestre[av.bimestre] = nota.valor
        existing_values = [v for v in notas_por_bimestre.values() if v is not None]
        media = sum(existing_values) / len(existing_values) if existing_values else None

        # Step 3: Frequência — ALL chamadas for (turma_id, disciplina_id), NO professor_id filter
        chamadas = db.query(Chamada).filter(
            Chamada.turma_id == aluno.turma_id,
            Chamada.disciplina_id == disc_id,
        ).all()
        total_aulas = len(chamadas)
        chamada_ids = [c.id for c in chamadas]
        if total_aulas == 0:
            total_presentes = 0
            freq_pct = None  # no classes registered yet — cannot calculate
        else:
            total_presentes = db.query(Presenca).filter(
                Presenca.aluno_id == aluno.id,
                Presenca.chamada_id.in_(chamada_ids),
                Presenca.presente == True,
            ).count()
            freq_pct = (total_presentes / total_aulas) * 100.0

        # Step 4: Status — only "aprovado"/"reprovado" when all 4 bimestres are graded
        todos_bimestres = all(v is not None for v in notas_por_bimestre.values())
        if not todos_bimestres:
            status = "em_andamento"
        elif media is not None and media >= 5.0 and freq_pct is not None and freq_pct >= 75.0:
            status = "aprovado"
        else:
            status = "reprovado"

        result.append({
            "disciplina_id": disc_id,
            "disciplina_nome": disciplina.nome,
            "bim1": notas_por_bimestre[1],
            "bim2": notas_por_bimestre[2],
            "bim3": notas_por_bimestre[3],
            "bim4": notas_por_bimestre[4],
            "media": media,
            "total_aulas": total_aulas,
            "total_presentes": total_presentes,
            "freq_pct": freq_pct,
            "status": status,
        })
    return result
