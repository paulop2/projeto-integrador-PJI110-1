"""
Admin CRUD endpoint tests — Phase 3.
"""
from datetime import date
import pytest


# ---------------------------------------------------------------------------
# Security / access control tests
# ---------------------------------------------------------------------------

def test_unauthenticated_gets_401(client):
    """Unauthenticated request to any /admin endpoint returns 401."""
    response = client.get("/admin/alunos")
    assert response.status_code == 401


def test_admin_role_required_for_professor(client, professor_headers):
    """Professor JWT receives 403 on all /admin endpoints (T-03-01)."""
    response = client.get("/admin/alunos", headers=professor_headers)
    assert response.status_code == 403


# ---------------------------------------------------------------------------
# ADMIN-01: Alunos CRUD
# ---------------------------------------------------------------------------

def test_create_aluno(client, admin_headers):
    """POST /admin/alunos creates aluno and returns 201 with matricula."""
    response = client.post(
        "/admin/alunos",
        json={"nome": "João Silva", "turma_id": None, "responsavel_id": None},
        headers=admin_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert "matricula" in data
    assert data["matricula"].startswith("MAT")
    assert data["nome"] == "João Silva"
    assert data["ativo"] is True


def test_list_alunos(client, admin_headers):
    """GET /admin/alunos returns paginated result with items/total/page."""
    # Create one aluno first
    client.post(
        "/admin/alunos",
        json={"nome": "Maria Souza"},
        headers=admin_headers,
    )
    response = client.get("/admin/alunos?page=1&search=", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert data["page"] == 1
    assert len(data["items"]) >= 1


def test_deactivate_aluno(client, admin_headers):
    """POST /admin/alunos/{id}/deactivate sets ativo=False (soft delete)."""
    create_resp = client.post(
        "/admin/alunos",
        json={"nome": "Pedro Costa"},
        headers=admin_headers,
    )
    assert create_resp.status_code == 201
    aluno_id = create_resp.json()["id"]

    deactivate_resp = client.post(
        f"/admin/alunos/{aluno_id}/deactivate",
        headers=admin_headers,
    )
    assert deactivate_resp.status_code == 200
    assert deactivate_resp.json()["ativo"] is False


# ---------------------------------------------------------------------------
# ADMIN-02: Turmas CRUD
# ---------------------------------------------------------------------------

def test_create_turma(client, admin_headers):
    """POST /admin/turmas creates turma and returns 201."""
    response = client.post(
        "/admin/turmas",
        json={"nome": "9A", "ano": 2026, "serie": "9º ano", "turno": "manhã"},
        headers=admin_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "9A"
    assert data["ano"] == 2026


# ---------------------------------------------------------------------------
# ADMIN-03: Disciplinas CRUD
# ---------------------------------------------------------------------------

def test_create_disciplina(client, admin_headers):
    """POST /admin/disciplinas creates disciplina and returns 201."""
    response = client.post(
        "/admin/disciplinas",
        json={"nome": "Matemática", "carga_horaria": 120},
        headers=admin_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "Matemática"


# ---------------------------------------------------------------------------
# ADMIN-04: professor_turma sync
# ---------------------------------------------------------------------------

def test_sync_professor_turma(client, admin_headers, test_db):
    """PUT /admin/turmas/{id} replaces all professor_turma rows atomically."""
    from src.models.usuario import Usuario, TipoUsuario
    from src.auth.service import hash_password

    # Create a professor user + profile to have valid FK targets
    u = Usuario(
        email="prof2@test.com",
        senha_hash=hash_password("pass"),
        tipo=TipoUsuario.professor,
        ativo=True,
    )
    test_db.add(u)
    test_db.flush()
    from src.models.professor import Professor
    p = Professor(usuario_id=u.id, nome="Prof Teste")
    test_db.add(p)
    test_db.commit()
    test_db.refresh(p)

    # Create disciplina
    disc_resp = client.post(
        "/admin/disciplinas",
        json={"nome": "Física", "carga_horaria": 80},
        headers=admin_headers,
    )
    assert disc_resp.status_code == 201
    disc_id = disc_resp.json()["id"]

    # Create turma with professor_turma rows
    turma_resp = client.post(
        "/admin/turmas",
        json={
            "nome": "8B",
            "ano": 2026,
            "serie": "8º ano",
            "turno": "tarde",
            "professor_turma": [
                {"disciplina_id": disc_id, "professor_id": p.id}
            ],
        },
        headers=admin_headers,
    )
    assert turma_resp.status_code == 201
    turma_id = turma_resp.json()["id"]

    # Update with empty professor_turma should remove the row
    update_resp = client.put(
        f"/admin/turmas/{turma_id}",
        json={
            "nome": "8B",
            "ano": 2026,
            "serie": "8º ano",
            "turno": "tarde",
            "professor_turma": [],
        },
        headers=admin_headers,
    )
    assert update_resp.status_code == 200


# ---------------------------------------------------------------------------
# ADMIN-05: Professor account creation (atomic T-03-02)
# ---------------------------------------------------------------------------

def test_create_professor(client, admin_headers):
    """POST /admin/professores creates Usuario(tipo=professor) + Professor atomically."""
    response = client.post(
        "/admin/professores",
        json={
            "nome": "Ana Lima",
            "email": "ana@escola.com",
            "senha": "senha123",
            "cpf": None,
        },
        headers=admin_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "Ana Lima"
    assert "id" in data
    # Verify no plaintext password in response
    assert "senha" not in data
    assert "senha_hash" not in data


# ---------------------------------------------------------------------------
# ADMIN-06: Responsavel account + aluno link
# ---------------------------------------------------------------------------

def test_create_responsavel(client, admin_headers):
    """POST /admin/responsaveis creates Usuario(tipo=responsavel) + Responsavel + links alunos."""
    # Create aluno first
    aluno_resp = client.post(
        "/admin/alunos",
        json={"nome": "Filho Teste"},
        headers=admin_headers,
    )
    assert aluno_resp.status_code == 201
    aluno_id = aluno_resp.json()["id"]

    response = client.post(
        "/admin/responsaveis",
        json={
            "nome": "Pai Teste",
            "email": "pai@escola.com",
            "senha": "senha123",
            "cpf": None,
            "telefone": None,
            "aluno_ids": [aluno_id],
        },
        headers=admin_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "Pai Teste"
    assert "senha" not in data


def test_admin_self_deactivation_blocked(client, admin_headers, admin_user):
    """Admin cannot deactivate their own account (T-03-03)."""
    response = client.post(
        f"/admin/usuarios/{admin_user.id}/deactivate",
        headers=admin_headers,
    )
    # Must return 400 (business rule) or 403 — NOT 200
    assert response.status_code in (400, 403)


# ---------------------------------------------------------------------------
# ADMIN-07: Dashboard desempenho aggregation
# ---------------------------------------------------------------------------

def test_admin_dashboard_desempenho(client, admin_headers, test_db):
    """GET /admin/dashboard/desempenho returns aggregated LDB metrics per turma."""
    from src.models.usuario import Usuario, TipoUsuario
    from src.models.professor import Professor
    from src.models.turma import Turma
    from src.models.disciplina import Disciplina
    from src.models.aluno import Aluno
    from src.models.professor_turma import ProfessorTurma
    from src.models.avaliacao import Avaliacao
    from src.models.nota import Nota
    from src.models.chamada import Chamada
    from src.models.presenca import Presenca
    from src.auth.service import hash_password

    # Create professor
    u = Usuario(
        email="prof_dash@test.com",
        senha_hash=hash_password("pass"),
        tipo=TipoUsuario.professor,
        ativo=True,
    )
    test_db.add(u)
    test_db.flush()
    prof = Professor(usuario_id=u.id, nome="Prof Dash")
    test_db.add(prof)
    test_db.flush()

    # Create turma, disciplina, aluno
    turma = Turma(nome="8A", ano=2026, serie="8", turno="manha")
    test_db.add(turma)
    disciplina = Disciplina(nome="Matematica")
    test_db.add(disciplina)
    test_db.flush()

    aluno = Aluno(nome="Aluno A", matricula="MAT001", ativo=True, turma_id=turma.id)
    test_db.add(aluno)
    test_db.flush()

    # Link professor to turma
    link = ProfessorTurma(professor_id=prof.id, turma_id=turma.id, disciplina_id=disciplina.id)
    test_db.add(link)
    test_db.flush()

    # Create avaliacao, nota, chamada, presenca for passing student
    av = Avaliacao(
        turma_id=turma.id,
        disciplina_id=disciplina.id,
        professor_id=prof.id,
        bimestre=1,
        titulo="AV1",
        valor_maximo=10.0,
    )
    test_db.add(av)
    test_db.flush()

    nota = Nota(avaliacao_id=av.id, aluno_id=aluno.id, valor=8.0)
    test_db.add(nota)

    chamada = Chamada(
        turma_id=turma.id,
        disciplina_id=disciplina.id,
        professor_id=prof.id,
        data=date(2026, 4, 1),
    )
    test_db.add(chamada)
    test_db.flush()

    presenca = Presenca(chamada_id=chamada.id, aluno_id=aluno.id, presente=True)
    test_db.add(presenca)
    test_db.commit()

    # First check — passing student → 0 at risk
    response = client.get("/admin/dashboard/desempenho", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert "turmas" in data
    assert "alunos_em_risco" in data
    assert data["alunos_em_risco"] == 0
    assert len(data["turmas"]) == 1
    turma_data = data["turmas"][0]
    assert turma_data["turma_id"] == turma.id
    assert turma_data["num_alunos"] == 1
    assert turma_data["media_geral"] == pytest.approx(8.0)
    assert turma_data["pct_aprovados"] == pytest.approx(100.0)

    # Add failing student
    aluno_fail = Aluno(nome="Aluno B", matricula="MAT002", ativo=True, turma_id=turma.id)
    test_db.add(aluno_fail)
    test_db.flush()

    nota_fail = Nota(avaliacao_id=av.id, aluno_id=aluno_fail.id, valor=4.0)
    test_db.add(nota_fail)

    presenca_fail = Presenca(chamada_id=chamada.id, aluno_id=aluno_fail.id, presente=True)
    test_db.add(presenca_fail)
    test_db.commit()

    # Second check — one failing → 1 at risk, 50% approval
    response = client.get("/admin/dashboard/desempenho", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["alunos_em_risco"] == 1
    turma_data = data["turmas"][0]
    assert turma_data["num_alunos"] == 2
    assert turma_data["media_geral"] == pytest.approx(6.0)
    assert turma_data["pct_aprovados"] == pytest.approx(50.0)
