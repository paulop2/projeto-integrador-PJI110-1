"""
Professor endpoint tests — Phase 4.

Tests cover PROF-01 through PROF-05 plus access control.
Run: cd backend && python -m pytest tests/test_professor.py -x -q
"""
import pytest
from datetime import date

from src.models.professor import Professor
from src.models.turma import Turma
from src.models.disciplina import Disciplina
from src.models.aluno import Aluno
from src.models.professor_turma import ProfessorTurma
from src.models.chamada import Chamada
from src.models.presenca import Presenca
from src.models.avaliacao import Avaliacao
from src.models.nota import Nota


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _setup_professor_with_turma(test_db, professor_user):
    """Create Professor profile, Turma, Disciplina, Aluno, and professor_turma link."""
    prof = Professor(usuario_id=professor_user.id, nome="Prof Teste", cpf="00000000001")
    test_db.add(prof)
    test_db.flush()

    turma = Turma(nome="7A", ano=2026, serie="7", turno="manha")
    test_db.add(turma)
    disciplina = Disciplina(nome="Matematica")
    test_db.add(disciplina)
    test_db.flush()

    aluno = Aluno(nome="Aluno Um", matricula="MAT0001", ativo=True, turma_id=turma.id)
    test_db.add(aluno)
    test_db.flush()

    link = ProfessorTurma(professor_id=prof.id, turma_id=turma.id, disciplina_id=disciplina.id)
    test_db.add(link)
    test_db.commit()

    return prof, turma, disciplina, aluno


# ---------------------------------------------------------------------------
# Security / access control tests (these pass as soon as router is registered)
# ---------------------------------------------------------------------------

def test_unauthenticated_gets_401(client):
    """Unauthenticated request to any /professor endpoint returns 401."""
    response = client.get("/professor/minhas-turmas")
    assert response.status_code == 401


def test_admin_role_rejected(client, admin_headers):
    """Admin JWT receives 403 on /professor endpoints (T-04-01)."""
    response = client.get("/professor/minhas-turmas", headers=admin_headers)
    assert response.status_code == 403


# ---------------------------------------------------------------------------
# PROF-02: Ownership check — unlinked turma returns 403
# ---------------------------------------------------------------------------

def test_ownership_check(client, test_db, professor_user, professor_headers):
    """Professor cannot access a turma they are not linked to (PROF-02, T-04-02)."""
    # Create professor profile but do NOT link to any turma
    prof = Professor(usuario_id=professor_user.id, nome="Prof Dono", cpf="00000000002")
    test_db.add(prof)
    turma = Turma(nome="9B", ano=2026, serie="9", turno="manha")
    test_db.add(turma)
    test_db.commit()

    response = client.get(
        f"/professor/turmas/{turma.id}/chamada?date=2026-04-27&disciplina_id=1",
        headers=professor_headers,
    )
    assert response.status_code == 403


# ---------------------------------------------------------------------------
# Turma alunos / disciplinas helpers
# ---------------------------------------------------------------------------

def test_get_turma_alunos(client, test_db, professor_user, professor_headers):
    """GET /professor/turmas/:id/alunos returns alunos for the linked turma."""
    prof, turma, disciplina, aluno = _setup_professor_with_turma(test_db, professor_user)

    response = client.get(
        f"/professor/turmas/{turma.id}/alunos",
        headers=professor_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == aluno.id
    assert data[0]["nome"] == aluno.nome


def test_get_turma_alunos_403_for_unlinked(client, test_db, professor_user, professor_headers):
    """Professor gets 403 for alunos of a turma they do not own."""
    prof = Professor(usuario_id=professor_user.id, nome="Prof Dono", cpf="00000000002")
    test_db.add(prof)
    turma = Turma(nome="9B", ano=2026, serie="9", turno="manha")
    test_db.add(turma)
    test_db.commit()

    response = client.get(
        f"/professor/turmas/{turma.id}/alunos",
        headers=professor_headers,
    )
    assert response.status_code == 403


def test_get_turma_disciplinas(client, test_db, professor_user, professor_headers):
    """GET /professor/turmas/:id/disciplinas returns disciplinas for the linked turma."""
    prof, turma, disciplina, aluno = _setup_professor_with_turma(test_db, professor_user)

    response = client.get(
        f"/professor/turmas/{turma.id}/disciplinas",
        headers=professor_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == disciplina.id
    assert data[0]["nome"] == disciplina.nome


# ---------------------------------------------------------------------------
# PROF-01: Chamada create (PROF-01)
# ---------------------------------------------------------------------------

def test_create_chamada(client, test_db, professor_user, professor_headers):
    """POST /professor/turmas/:id/chamada creates chamada + presencas rows (PROF-01)."""
    prof, turma, disciplina, aluno = _setup_professor_with_turma(test_db, professor_user)

    payload = {
        "disciplina_id": disciplina.id,
        "data": "2026-04-28",
        "presencas": [{"aluno_id": aluno.id, "presente": True}],
    }
    response = client.post(
        f"/professor/turmas/{turma.id}/chamada",
        json=payload,
        headers=professor_headers,
    )
    assert response.status_code == 200

    # Verify rows in DB
    chamada = test_db.query(Chamada).filter(Chamada.turma_id == turma.id).first()
    assert chamada is not None
    presencas = test_db.query(Presenca).filter(Presenca.chamada_id == chamada.id).all()
    assert len(presencas) == 1
    assert presencas[0].presente is True


# ---------------------------------------------------------------------------
# PROF-01 + PROF-02: GET minhas-turmas
# ---------------------------------------------------------------------------

def test_get_minhas_turmas_only_own(client, test_db, professor_user, professor_headers):
    """GET /professor/minhas-turmas returns only turmas linked to the professor (PROF-02)."""
    prof, turma, disciplina, aluno = _setup_professor_with_turma(test_db, professor_user)

    # Create a second turma NOT linked to this professor
    other_turma = Turma(nome="OutraTurma", ano=2026, serie="9", turno="manha")
    test_db.add(other_turma)
    test_db.commit()

    response = client.get("/professor/minhas-turmas", headers=professor_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == turma.id


# ---------------------------------------------------------------------------
# PROF-04: Edit chamada (re-POST replaces presencas)
# ---------------------------------------------------------------------------

def test_edit_chamada_replaces_presencas(client, test_db, professor_user, professor_headers):
    """Re-POSTing chamada for same date replaces all presencas rows (PROF-04)."""
    prof, turma, disciplina, aluno = _setup_professor_with_turma(test_db, professor_user)

    # First POST: aluno presente
    payload = {
        "disciplina_id": disciplina.id,
        "data": "2026-04-28",
        "presencas": [{"aluno_id": aluno.id, "presente": True}],
    }
    client.post(f"/professor/turmas/{turma.id}/chamada", json=payload, headers=professor_headers)

    # Second POST (same date): aluno falta
    payload["presencas"][0]["presente"] = False
    response = client.post(
        f"/professor/turmas/{turma.id}/chamada",
        json=payload,
        headers=professor_headers,
    )
    assert response.status_code == 200

    chamada = test_db.query(Chamada).filter(Chamada.turma_id == turma.id).first()
    presencas = test_db.query(Presenca).filter(Presenca.chamada_id == chamada.id).all()
    assert len(presencas) == 1  # replace-all: still exactly one row
    assert presencas[0].presente is False


# ---------------------------------------------------------------------------
# PROF-03: Notas upsert
# ---------------------------------------------------------------------------

def test_upsert_notas(client, test_db, professor_user, professor_headers):
    """POST /professor/turmas/:id/notas creates avaliacao + nota rows (PROF-03)."""
    prof, turma, disciplina, aluno = _setup_professor_with_turma(test_db, professor_user)

    payload = {
        "disciplina_id": disciplina.id,
        "grades": [{"aluno_id": aluno.id, "bimestre": 1, "valor": 8.5}],
    }
    response = client.post(
        f"/professor/turmas/{turma.id}/notas",
        json=payload,
        headers=professor_headers,
    )
    assert response.status_code == 200

    avaliacao = test_db.query(Avaliacao).filter(
        Avaliacao.turma_id == turma.id,
        Avaliacao.disciplina_id == disciplina.id,
        Avaliacao.bimestre == 1,
    ).first()
    assert avaliacao is not None

    nota = test_db.query(Nota).filter(
        Nota.avaliacao_id == avaliacao.id,
        Nota.aluno_id == aluno.id,
    ).first()
    assert nota is not None
    assert nota.valor == pytest.approx(8.5)


# ---------------------------------------------------------------------------
# PROF-04: Edit nota (re-POST updates value)
# ---------------------------------------------------------------------------

def test_edit_nota_updates_value(client, test_db, professor_user, professor_headers):
    """Re-POSTing notas for same aluno/bimestre updates valor (PROF-04)."""
    prof, turma, disciplina, aluno = _setup_professor_with_turma(test_db, professor_user)

    payload = {
        "disciplina_id": disciplina.id,
        "grades": [{"aluno_id": aluno.id, "bimestre": 2, "valor": 7.0}],
    }
    client.post(f"/professor/turmas/{turma.id}/notas", json=payload, headers=professor_headers)

    # Update to 9.0
    payload["grades"][0]["valor"] = 9.0
    response = client.post(
        f"/professor/turmas/{turma.id}/notas",
        json=payload,
        headers=professor_headers,
    )
    assert response.status_code == 200

    # Should not have duplicated avaliacoes
    count = test_db.query(Avaliacao).filter(
        Avaliacao.turma_id == turma.id,
        Avaliacao.bimestre == 2,
    ).count()
    assert count == 1  # no duplicate avaliacao rows

    nota = test_db.query(Nota).filter(Nota.aluno_id == aluno.id).first()
    assert nota.valor == pytest.approx(9.0)


# ---------------------------------------------------------------------------
# PROF-05: Frequencia aggregation
# ---------------------------------------------------------------------------

def test_frequencia_aggregation(client, test_db, professor_user, professor_headers):
    """GET /professor/turmas/:id/frequencia returns correct percentual per aluno (PROF-05)."""
    prof, turma, disciplina, aluno = _setup_professor_with_turma(test_db, professor_user)

    # Create 2 chamadas: aluno presente in first, falta in second
    c1 = Chamada(turma_id=turma.id, disciplina_id=disciplina.id,
                 professor_id=prof.id, data=date(2026, 4, 1))
    c2 = Chamada(turma_id=turma.id, disciplina_id=disciplina.id,
                 professor_id=prof.id, data=date(2026, 4, 2))
    test_db.add_all([c1, c2])
    test_db.flush()

    test_db.add(Presenca(chamada_id=c1.id, aluno_id=aluno.id, presente=True))
    test_db.add(Presenca(chamada_id=c2.id, aluno_id=aluno.id, presente=False))
    test_db.commit()

    response = client.get(
        f"/professor/turmas/{turma.id}/frequencia",
        headers=professor_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    row = data[0]
    assert row["aluno_id"] == aluno.id
    assert row["total_aulas"] == 2
    assert row["total_presentes"] == 1
    assert row["percentual"] == pytest.approx(50.0)


# ---------------------------------------------------------------------------
# PROF-06: Minhas turmas with LDB metrics
# ---------------------------------------------------------------------------

def test_professor_minhas_turmas_with_metrics(client, test_db, professor_user, professor_headers):
    """GET /professor/minhas-turmas includes media_geral and pct_aprovados."""
    prof, turma, disciplina, aluno = _setup_professor_with_turma(test_db, professor_user)

    # All 4 bimestres graded at 8.0 — required for pct_aprovados to count the student
    for bim in range(1, 5):
        av = Avaliacao(
            turma_id=turma.id,
            disciplina_id=disciplina.id,
            professor_id=prof.id,
            bimestre=bim,
            titulo=f"AV{bim}",
            valor_maximo=10.0,
        )
        test_db.add(av)
        test_db.flush()
        test_db.add(Nota(avaliacao_id=av.id, aluno_id=aluno.id, valor=8.0))

    chamada = Chamada(
        turma_id=turma.id,
        disciplina_id=disciplina.id,
        professor_id=prof.id,
        data=date(2026, 4, 1),
    )
    test_db.add(chamada)
    test_db.flush()
    test_db.add(Presenca(chamada_id=chamada.id, aluno_id=aluno.id, presente=True))
    test_db.commit()

    response = client.get("/professor/minhas-turmas", headers=professor_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    turma_data = data[0]
    assert turma_data["media_geral"] == pytest.approx(8.0)
    assert turma_data["pct_aprovados"] == pytest.approx(100.0)
