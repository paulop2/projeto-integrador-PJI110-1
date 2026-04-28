"""
Responsavel endpoint tests — Phase 5.

Tests cover RESP-01 through RESP-06 plus access control.
Run: cd backend && python3 -m pytest tests/test_responsavel.py -x -q
"""
import pytest
from datetime import date

from src.models.responsavel import Responsavel
from src.models.turma import Turma
from src.models.disciplina import Disciplina
from src.models.aluno import Aluno
from src.models.professor_turma import ProfessorTurma
from src.models.chamada import Chamada
from src.models.presenca import Presenca
from src.models.avaliacao import Avaliacao
from src.models.nota import Nota
from src.models.usuario import Usuario, TipoUsuario
from src.auth.service import hash_password, create_access_token


def _setup_responsavel_with_filho(test_db, responsavel_user):
    """
    Create Responsavel profile, Turma, Disciplina, Aluno (linked via responsavel_id),
    and ProfessorTurma link (required for boletim disciplina discovery).
    Returns (resp, turma, disciplina, aluno).
    """
    resp = Responsavel(usuario_id=responsavel_user.id, nome="Resp Teste")
    test_db.add(resp)
    test_db.flush()

    turma = Turma(nome="7A", ano=2026, serie="7", turno="manha")
    test_db.add(turma)
    disciplina = Disciplina(nome="Matematica")
    test_db.add(disciplina)
    test_db.flush()

    aluno = Aluno(
        nome="Filho Teste",
        matricula="MAT9001",
        ativo=True,
        turma_id=turma.id,
        responsavel_id=resp.id,
    )
    test_db.add(aluno)
    test_db.flush()

    # ProfessorTurma link needed so boletim can discover disciplinas via professor_turma DISTINCT query
    # We use a dummy professor_id=1 here — the service does not check professor ownership
    prof_user = Usuario(email="prof_fixture@test.com", senha_hash=hash_password("x"), tipo=TipoUsuario.professor, ativo=True)
    test_db.add(prof_user)
    test_db.flush()
    from src.models.professor import Professor
    prof = Professor(usuario_id=prof_user.id, nome="Prof Fixture", cpf="99999999999")
    test_db.add(prof)
    test_db.flush()

    link = ProfessorTurma(professor_id=prof.id, turma_id=turma.id, disciplina_id=disciplina.id)
    test_db.add(link)
    test_db.commit()

    return resp, turma, disciplina, aluno, prof


# ---------------------------------------------------------------------------
# Access control tests (run without full boletim data — test role guard only)
# ---------------------------------------------------------------------------

def test_unauthenticated_meus_filhos_gets_401(client):
    """Unauthenticated request to /responsavel/meus-filhos returns 401 (T-05-03)."""
    response = client.get("/responsavel/meus-filhos")
    assert response.status_code == 401


def test_unauthenticated_boletim_gets_401(client):
    """Unauthenticated request to /responsavel/boletim returns 401 (T-05-03)."""
    response = client.get("/responsavel/boletim?aluno_id=1")
    assert response.status_code == 401


def test_professor_role_rejected_on_meus_filhos(client, professor_headers):
    """Professor JWT receives 403 on /responsavel/meus-filhos (T-05-02)."""
    response = client.get("/responsavel/meus-filhos", headers=professor_headers)
    assert response.status_code == 403


def test_professor_role_rejected_on_boletim(client, professor_headers):
    """Professor JWT receives 403 on /responsavel/boletim (T-05-02)."""
    response = client.get("/responsavel/boletim?aluno_id=1", headers=professor_headers)
    assert response.status_code == 403


def test_admin_role_rejected_on_meus_filhos(client, admin_headers):
    """Admin JWT receives 403 on /responsavel/meus-filhos (T-05-02)."""
    response = client.get("/responsavel/meus-filhos", headers=admin_headers)
    assert response.status_code == 403


# ---------------------------------------------------------------------------
# RESP-06: Ownership / IDOR tests
# ---------------------------------------------------------------------------

def test_ownership_idor_blocked(client, test_db, responsavel_user, responsavel_headers):
    """
    Responsavel cannot access boletim of aluno belonging to another responsavel.
    Must return 403 (NOT 404) — 404 leaks aluno existence (T-05-01, RESP-06).
    """
    # Create owner responsavel and linked aluno
    owner_user = Usuario(
        email="owner@test.com",
        senha_hash=hash_password("ownerpass"),
        tipo=TipoUsuario.responsavel,
        ativo=True,
    )
    test_db.add(owner_user)
    test_db.flush()
    owner_resp = Responsavel(usuario_id=owner_user.id, nome="Owner Resp")
    test_db.add(owner_resp)
    test_db.flush()
    other_aluno = Aluno(nome="Filho de Outro", matricula="MAT9002", ativo=True, responsavel_id=owner_resp.id)
    test_db.add(other_aluno)

    # Current responsavel_user must also have a Responsavel profile (for _get_responsavel)
    current_resp = Responsavel(usuario_id=responsavel_user.id, nome="Current Resp")
    test_db.add(current_resp)
    test_db.commit()

    # Try to access other_aluno's boletim as current responsavel
    response = client.get(f"/responsavel/boletim?aluno_id={other_aluno.id}", headers=responsavel_headers)
    assert response.status_code == 403
    assert "Acesso negado" in response.json()["detail"]


# ---------------------------------------------------------------------------
# RESP-01, RESP-02: Boletim notas and media calculation
# ---------------------------------------------------------------------------

def test_boletim_notas(client, test_db, responsavel_user, responsavel_headers):
    """
    GET /responsavel/boletim?aluno_id=X returns boletim with notas organized by disciplina/bimestre (RESP-01).
    """
    resp, turma, disciplina, aluno, prof = _setup_responsavel_with_filho(test_db, responsavel_user)

    # Create avaliacao + nota for bimestre 1
    av = Avaliacao(turma_id=turma.id, disciplina_id=disciplina.id, professor_id=prof.id, titulo="Prova", bimestre=1, valor_maximo=10.0)
    test_db.add(av)
    test_db.flush()
    nota = Nota(avaliacao_id=av.id, aluno_id=aluno.id, valor=8.0)
    test_db.add(nota)
    test_db.commit()

    response = client.get(f"/responsavel/boletim?aluno_id={aluno.id}", headers=responsavel_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    row = data[0]
    assert row["disciplina_id"] == disciplina.id
    assert row["disciplina_nome"] == "Matematica"
    assert row["bim1"] == pytest.approx(8.0)
    assert row["bim2"] is None
    assert row["bim3"] is None
    assert row["bim4"] is None


def test_media_calculation(client, test_db, responsavel_user, responsavel_headers):
    """
    Media is computed as average of existing bimestre notas only (RESP-02).
    Missing bimestres (None) are excluded from calculation.
    """
    resp, turma, disciplina, aluno, prof = _setup_responsavel_with_filho(test_db, responsavel_user)

    # Add notas for bimestre 1 and 3 only (bim2 and bim4 absent)
    for bim, valor in [(1, 6.0), (3, 8.0)]:
        av = Avaliacao(turma_id=turma.id, disciplina_id=disciplina.id, professor_id=prof.id, titulo="Prova", bimestre=bim, valor_maximo=10.0)
        test_db.add(av)
        test_db.flush()
        nota = Nota(avaliacao_id=av.id, aluno_id=aluno.id, valor=valor)
        test_db.add(nota)
    test_db.commit()

    response = client.get(f"/responsavel/boletim?aluno_id={aluno.id}", headers=responsavel_headers)
    assert response.status_code == 200
    row = response.json()[0]
    assert row["media"] == pytest.approx(7.0)  # (6.0 + 8.0) / 2


def test_media_none_when_no_notas(client, test_db, responsavel_user, responsavel_headers):
    """When no notas exist, media is None (not 0 or ZeroDivisionError)."""
    resp, turma, disciplina, aluno, prof = _setup_responsavel_with_filho(test_db, responsavel_user)
    test_db.commit()

    response = client.get(f"/responsavel/boletim?aluno_id={aluno.id}", headers=responsavel_headers)
    assert response.status_code == 200
    row = response.json()[0]
    assert row["media"] is None


# ---------------------------------------------------------------------------
# RESP-03, RESP-04: Frequência per disciplina
# ---------------------------------------------------------------------------

def test_frequencia_per_disciplina(client, test_db, responsavel_user, responsavel_headers):
    """
    GET /responsavel/boletim returns frequência per disciplina with correct percentual (RESP-03).
    freq_pct = total_presentes / total_aulas * 100. No professor_id filter applied.
    """
    resp, turma, disciplina, aluno, prof = _setup_responsavel_with_filho(test_db, responsavel_user)

    # Add 4 chamadas, aluno present for 3
    for i, presente in enumerate([True, True, True, False]):
        chamada = Chamada(turma_id=turma.id, disciplina_id=disciplina.id, professor_id=prof.id, data=date(2026, 4, i + 1))
        test_db.add(chamada)
        test_db.flush()
        presenca = Presenca(chamada_id=chamada.id, aluno_id=aluno.id, presente=presente)
        test_db.add(presenca)
    test_db.commit()

    response = client.get(f"/responsavel/boletim?aluno_id={aluno.id}", headers=responsavel_headers)
    assert response.status_code == 200
    row = response.json()[0]
    assert row["total_aulas"] == 4
    assert row["total_presentes"] == 3
    assert row["freq_pct"] == pytest.approx(75.0)


def test_freq_below_threshold(client, test_db, responsavel_user, responsavel_headers):
    """
    freq_pct < 75 is captured correctly in the response (RESP-04).
    Response value can be used by frontend to apply red highlight.
    """
    resp, turma, disciplina, aluno, prof = _setup_responsavel_with_filho(test_db, responsavel_user)

    for i, presente in enumerate([True, False, False, False]):
        chamada = Chamada(turma_id=turma.id, disciplina_id=disciplina.id, professor_id=prof.id, data=date(2026, 4, i + 11))
        test_db.add(chamada)
        test_db.flush()
        presenca = Presenca(chamada_id=chamada.id, aluno_id=aluno.id, presente=presente)
        test_db.add(presenca)
    test_db.commit()

    response = client.get(f"/responsavel/boletim?aluno_id={aluno.id}", headers=responsavel_headers)
    assert response.status_code == 200
    row = response.json()[0]
    assert row["freq_pct"] == pytest.approx(25.0)
    assert row["freq_pct"] < 75.0


# ---------------------------------------------------------------------------
# RESP-05: Approval rule
# ---------------------------------------------------------------------------

def test_approval_rule_pass(client, test_db, responsavel_user, responsavel_headers):
    """aprovado=True when media >= 5.0 AND freq_pct >= 75% (RESP-05, LDB rule)."""
    resp, turma, disciplina, aluno, prof = _setup_responsavel_with_filho(test_db, responsavel_user)

    # Nota: 8.0
    av = Avaliacao(turma_id=turma.id, disciplina_id=disciplina.id, professor_id=prof.id, titulo="Prova", bimestre=1, valor_maximo=10.0)
    test_db.add(av)
    test_db.flush()
    test_db.add(Nota(avaliacao_id=av.id, aluno_id=aluno.id, valor=8.0))

    # Frequência: 4/4 = 100%
    for i in range(4):
        chamada = Chamada(turma_id=turma.id, disciplina_id=disciplina.id, professor_id=prof.id, data=date(2026, 5, i + 1))
        test_db.add(chamada)
        test_db.flush()
        test_db.add(Presenca(chamada_id=chamada.id, aluno_id=aluno.id, presente=True))
    test_db.commit()

    response = client.get(f"/responsavel/boletim?aluno_id={aluno.id}", headers=responsavel_headers)
    assert response.json()[0]["aprovado"] is True


def test_approval_rule_fail_low_media(client, test_db, responsavel_user, responsavel_headers):
    """aprovado=False when media < 5.0, even with good frequencia (RESP-05)."""
    resp, turma, disciplina, aluno, prof = _setup_responsavel_with_filho(test_db, responsavel_user)

    av = Avaliacao(turma_id=turma.id, disciplina_id=disciplina.id, professor_id=prof.id, titulo="Prova", bimestre=1, valor_maximo=10.0)
    test_db.add(av)
    test_db.flush()
    test_db.add(Nota(avaliacao_id=av.id, aluno_id=aluno.id, valor=4.0))  # below 5.0

    for i in range(4):
        chamada = Chamada(turma_id=turma.id, disciplina_id=disciplina.id, professor_id=prof.id, data=date(2026, 5, i + 11))
        test_db.add(chamada)
        test_db.flush()
        test_db.add(Presenca(chamada_id=chamada.id, aluno_id=aluno.id, presente=True))
    test_db.commit()

    response = client.get(f"/responsavel/boletim?aluno_id={aluno.id}", headers=responsavel_headers)
    assert response.json()[0]["aprovado"] is False


def test_approval_rule_fail_low_freq(client, test_db, responsavel_user, responsavel_headers):
    """aprovado=False when freq_pct < 75%, even with good media (RESP-05)."""
    resp, turma, disciplina, aluno, prof = _setup_responsavel_with_filho(test_db, responsavel_user)

    av = Avaliacao(turma_id=turma.id, disciplina_id=disciplina.id, professor_id=prof.id, titulo="Prova", bimestre=1, valor_maximo=10.0)
    test_db.add(av)
    test_db.flush()
    test_db.add(Nota(avaliacao_id=av.id, aluno_id=aluno.id, valor=9.0))  # good media

    # Only 1/4 present = 25%
    for i, presente in enumerate([True, False, False, False]):
        chamada = Chamada(turma_id=turma.id, disciplina_id=disciplina.id, professor_id=prof.id, data=date(2026, 5, i + 21))
        test_db.add(chamada)
        test_db.flush()
        test_db.add(Presenca(chamada_id=chamada.id, aluno_id=aluno.id, presente=presente))
    test_db.commit()

    response = client.get(f"/responsavel/boletim?aluno_id={aluno.id}", headers=responsavel_headers)
    assert response.json()[0]["aprovado"] is False


def test_approval_false_when_no_data(client, test_db, responsavel_user, responsavel_headers):
    """aprovado=False when both media and freq_pct are None (no data entered yet)."""
    resp, turma, disciplina, aluno, prof = _setup_responsavel_with_filho(test_db, responsavel_user)
    test_db.commit()

    response = client.get(f"/responsavel/boletim?aluno_id={aluno.id}", headers=responsavel_headers)
    assert response.json()[0]["aprovado"] is False


# ---------------------------------------------------------------------------
# RESP-01: meus-filhos endpoint
# ---------------------------------------------------------------------------

def test_meus_filhos_returns_list(client, test_db, responsavel_user, responsavel_headers):
    """GET /responsavel/meus-filhos returns list with linked alunos (RESP-01)."""
    resp, turma, disciplina, aluno, prof = _setup_responsavel_with_filho(test_db, responsavel_user)

    response = client.get("/responsavel/meus-filhos", headers=responsavel_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == aluno.id
    assert data[0]["nome"] == "Filho Teste"
    assert data[0]["turma_nome"] == "7A"


def test_meus_filhos_empty_when_no_alunos(client, test_db, responsavel_user, responsavel_headers):
    """GET /responsavel/meus-filhos returns [] when responsavel has no linked alunos."""
    resp = Responsavel(usuario_id=responsavel_user.id, nome="Resp Sem Filhos")
    test_db.add(resp)
    test_db.commit()

    response = client.get("/responsavel/meus-filhos", headers=responsavel_headers)
    assert response.status_code == 200
    assert response.json() == []
