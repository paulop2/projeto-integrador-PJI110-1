"""
Shared pytest fixtures for Phase 3 admin tests.

Uses an in-memory SQLite database for each test — no production DB touched.
Overrides the FastAPI `get_db` dependency so every request uses the test session.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database import Base, get_db
from src.main import app
from src.models.usuario import Usuario, TipoUsuario
from src.auth.service import hash_password, create_access_token


TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def test_db():
    """In-memory SQLite engine + tables created fresh per test function."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db):
    """FastAPI TestClient with get_db overridden to use in-memory test_db."""
    def override_get_db():
        try:
            yield test_db
        finally:
            pass  # test_db fixture handles close

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def admin_user(test_db):
    """Creates an admin Usuario in the test DB and returns it."""
    user = Usuario(
        email="admin@test.com",
        senha_hash=hash_password("adminpass"),
        tipo=TipoUsuario.admin,
        ativo=True,
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture(scope="function")
def professor_user(test_db):
    """Creates a professor Usuario in the test DB and returns it."""
    user = Usuario(
        email="prof@test.com",
        senha_hash=hash_password("profpass"),
        tipo=TipoUsuario.professor,
        ativo=True,
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture(scope="function")
def admin_headers(admin_user):
    """Authorization headers for an admin user JWT."""
    token = create_access_token({"sub": str(admin_user.id), "tipo": "admin"})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def professor_headers(professor_user):
    """Authorization headers for a professor user JWT (used to test 403)."""
    token = create_access_token({"sub": str(professor_user.id), "tipo": "professor"})
    return {"Authorization": f"Bearer {token}"}
