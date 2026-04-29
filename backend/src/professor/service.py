"""
Professor service layer — chamada, notas, and frequencia business logic.

Patterns:
- _get_professor() helper resolves professor_id from current_user (Usuario) on every call
- _assert_professor_owns_turma() ownership check called at start of every turma-specific function
- db.query() style consistent with admin/service.py
- Chamada: find-or-create + delete+insert presencas (replace-all)
- Notas: find-or-create avaliacao per bimestre + upsert nota
"""
from datetime import datetime
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


def _calcular_aprovado(db: Session, aluno_id: int, turma_id: int, disciplina_id: int) -> tuple:
    """Returns (media, freq_pct, aprovado) for a given (aluno, turma, disciplina)."""
    avaliacoes = db.query(Avaliacao).filter(
        Avaliacao.turma_id == turma_id,
        Avaliacao.disciplina_id == disciplina_id,
    ).all()
    notas = []
    for av in avaliacoes:
        nota = db.query(Nota).filter(
            Nota.avaliacao_id == av.id,
            Nota.aluno_id == aluno_id,
        ).first()
        if nota:
            notas.append(nota.valor)
    media = sum(notas) / len(notas) if notas else None

    chamadas = db.query(Chamada).filter(
        Chamada.turma_id == turma_id,
        Chamada.disciplina_id == disciplina_id,
    ).all()
    total_chamadas = len(chamadas)
    if total_chamadas == 0:
        freq_pct = None
    else:
        chamada_ids = [c.id for c in chamadas]
        presentes = db.query(Presenca).filter(
            Presenca.aluno_id == aluno_id,
            Presenca.chamada_id.in_(chamada_ids),
            Presenca.presente == True,
        ).count()
        freq_pct = (presentes / total_chamadas) * 100.0

    aprovado = (
        media is not None and media >= 5.0
        and freq_pct is not None and freq_pct >= 75.0
    )
    return media, freq_pct, aprovado


def get_minhas_turmas(db: Session, current_user: Usuario) -> list:
    prof = _get_professor(db, current_user)
    links = db.query(ProfessorTurma).filter(
        ProfessorTurma.professor_id == prof.id
    ).all()

    # Group by turma_id
    turma_map: dict[int, dict] = {}
    for link in links:
        if link.turma_id not in turma_map:
            turma = db.query(Turma).filter(Turma.id == link.turma_id).first()
            num_alunos = db.query(Aluno).filter(
                Aluno.turma_id == link.turma_id,
                Aluno.ativo == True,
            ).count()
            turma_map[link.turma_id] = {
                "id": link.turma_id,
                "nome": turma.nome if turma else "",
                "disciplinas": [],
                "num_alunos": num_alunos,
            }
        disciplina = db.query(Disciplina).filter(Disciplina.id == link.disciplina_id).first()
        if disciplina:
            turma_map[link.turma_id]["disciplinas"].append(disciplina.nome)

    # Calculate metrics for each turma
    for turma_id, turma_data in turma_map.items():
        alunos = db.query(Aluno).filter(
            Aluno.turma_id == turma_id,
            Aluno.ativo == True,
        ).all()
        disc_ids = (
            db.query(ProfessorTurma.disciplina_id)
            .filter(ProfessorTurma.turma_id == turma_id)
            .distinct()
            .all()
        )
        disc_ids = [row[0] for row in disc_ids]

        all_medias = []
        aprovados_count = 0

        for aluno in alunos:
            aprovado_em_todas = True
            if not disc_ids:
                aprovado_em_todas = False
            for disc_id in disc_ids:
                media, freq_pct, aprovado = _calcular_aprovado(
                    db, aluno.id, turma_id, disc_id
                )
                if media is not None:
                    all_medias.append(media)
                if not aprovado:
                    aprovado_em_todas = False
            if aprovado_em_todas:
                aprovados_count += 1

        num_alunos = len(alunos)
        turma_data["media_geral"] = sum(all_medias) / len(all_medias) if all_medias else None
        turma_data["pct_aprovados"] = (aprovados_count / num_alunos) * 100.0 if num_alunos > 0 else None

    return list(turma_map.values())


def get_chamada(db: Session, current_user: Usuario, turma_id: int, date_str: str):
    prof = _get_professor(db, current_user)
    _assert_professor_owns_turma(db, prof.id, turma_id)
    target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    chamada = db.query(Chamada).filter(
        Chamada.turma_id == turma_id,
        Chamada.professor_id == prof.id,
        Chamada.data == target_date,
    ).first()
    if not chamada:
        return {"id": None, "data": date_str, "presencas": []}
    presencas = db.query(Presenca).filter(Presenca.chamada_id == chamada.id).all()
    return {
        "id": chamada.id,
        "data": str(chamada.data),
        "presencas": [{"aluno_id": p.aluno_id, "presente": p.presente} for p in presencas],
    }


def upsert_chamada(db: Session, current_user: Usuario, turma_id: int, payload: schemas.ChamadaCreate):
    prof = _get_professor(db, current_user)
    _assert_professor_owns_turma(db, prof.id, turma_id)
    chamada = db.query(Chamada).filter(
        Chamada.turma_id == turma_id,
        Chamada.disciplina_id == payload.disciplina_id,
        Chamada.professor_id == prof.id,
        Chamada.data == payload.data,
    ).first()
    if not chamada:
        chamada = Chamada(
            turma_id=turma_id,
            disciplina_id=payload.disciplina_id,
            professor_id=prof.id,
            data=payload.data,
        )
        db.add(chamada)
        db.flush()
    # Replace-all presencas
    db.query(Presenca).filter(Presenca.chamada_id == chamada.id).delete(synchronize_session=False)
    for p in payload.presencas:
        db.add(Presenca(chamada_id=chamada.id, aluno_id=p.aluno_id, presente=p.presente))
    db.commit()
    return {"id": chamada.id, "data": str(chamada.data)}


def get_notas(db: Session, current_user: Usuario, turma_id: int, disciplina_id: int) -> list:
    prof = _get_professor(db, current_user)
    _assert_professor_owns_turma(db, prof.id, turma_id)
    alunos = db.query(Aluno).filter(Aluno.turma_id == turma_id, Aluno.ativo == True).all()
    avaliacoes = db.query(Avaliacao).filter(
        Avaliacao.turma_id == turma_id,
        Avaliacao.disciplina_id == disciplina_id,
        Avaliacao.professor_id == prof.id,
    ).all()
    result = []
    for aluno in alunos:
        notas = []
        for av in avaliacoes:
            nota = db.query(Nota).filter(
                Nota.avaliacao_id == av.id,
                Nota.aluno_id == aluno.id,
            ).first()
            if nota:
                notas.append({"aluno_id": aluno.id, "bimestre": av.bimestre, "valor": nota.valor})
        result.append({"aluno_id": aluno.id, "nome": aluno.nome, "notas": notas})
    return result


def upsert_notas(db: Session, current_user: Usuario, turma_id: int, payload: schemas.NotasCreate):
    prof = _get_professor(db, current_user)
    _assert_professor_owns_turma(db, prof.id, turma_id)
    for grade in payload.grades:
        avaliacao = db.query(Avaliacao).filter(
            Avaliacao.turma_id == turma_id,
            Avaliacao.disciplina_id == payload.disciplina_id,
            Avaliacao.professor_id == prof.id,
            Avaliacao.bimestre == grade.bimestre,
        ).first()
        if not avaliacao:
            avaliacao = Avaliacao(
                turma_id=turma_id,
                disciplina_id=payload.disciplina_id,
                professor_id=prof.id,
                bimestre=grade.bimestre,
                titulo=f"{grade.bimestre}o Bimestre",
                valor_maximo=10.0,
            )
            db.add(avaliacao)
            db.flush()
        # Validate range
        if not (0 <= grade.valor <= avaliacao.valor_maximo):
            raise HTTPException(
                status_code=422,
                detail=f"Valor {grade.valor} fora do intervalo permitido (0 a {avaliacao.valor_maximo})",
            )
        nota = db.query(Nota).filter(
            Nota.avaliacao_id == avaliacao.id,
            Nota.aluno_id == grade.aluno_id,
        ).first()
        if nota:
            nota.valor = grade.valor
        else:
            db.add(Nota(avaliacao_id=avaliacao.id, aluno_id=grade.aluno_id, valor=grade.valor))
    db.commit()
    return {"ok": True}


def get_frequencia(db: Session, current_user: Usuario, turma_id: int) -> list:
    prof = _get_professor(db, current_user)
    _assert_professor_owns_turma(db, prof.id, turma_id)
    chamadas = db.query(Chamada).filter(
        Chamada.turma_id == turma_id,
        Chamada.professor_id == prof.id,
    ).all()
    total_aulas = len(chamadas)
    chamada_ids = [c.id for c in chamadas]
    alunos = db.query(Aluno).filter(Aluno.turma_id == turma_id, Aluno.ativo == True).all()
    result = []
    for aluno in alunos:
        if total_aulas == 0:
            total_presentes = 0
            percentual = 0.0
        else:
            total_presentes = db.query(Presenca).filter(
                Presenca.aluno_id == aluno.id,
                Presenca.chamada_id.in_(chamada_ids),
                Presenca.presente == True,
            ).count()
            percentual = (total_presentes / total_aulas) * 100.0
        result.append({
            "aluno_id": aluno.id,
            "nome": aluno.nome,
            "total_aulas": total_aulas,
            "total_presentes": total_presentes,
            "percentual": percentual,
        })
    return result


def get_turma_alunos(db: Session, current_user: Usuario, turma_id: int) -> list:
    prof = _get_professor(db, current_user)
    _assert_professor_owns_turma(db, prof.id, turma_id)
    alunos = db.query(Aluno).filter(Aluno.turma_id == turma_id, Aluno.ativo == True).all()
    return [{"id": a.id, "nome": a.nome} for a in alunos]


def get_turma_disciplinas(db: Session, current_user: Usuario, turma_id: int) -> list:
    prof = _get_professor(db, current_user)
    _assert_professor_owns_turma(db, prof.id, turma_id)
    links = db.query(ProfessorTurma).filter(
        ProfessorTurma.professor_id == prof.id,
        ProfessorTurma.turma_id == turma_id,
    ).all()
    result = []
    for link in links:
        disciplina = db.query(Disciplina).filter(Disciplina.id == link.disciplina_id).first()
        if disciplina:
            result.append({"id": disciplina.id, "nome": disciplina.nome})
    return result
