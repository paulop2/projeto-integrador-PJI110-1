"""
Admin CRUD endpoint tests — Phase 3.

Stubs: tests are written in full but backend module (src/admin/) does not exist yet.
All tests will FAIL with 404/422/ImportError until Plan 02 implements the backend.
Run after Plan 02 to confirm green.
"""
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
