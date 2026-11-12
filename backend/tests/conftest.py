"""Shared fixtures for backend tests.

Tests never touch the real PostgreSQL database: environment variables are
pointed at a throwaway SQLite file *before* the app is imported, and the
``get_db`` dependency is overridden with a session bound to an in-memory
SQLite engine whose schema is built from the models.
"""

import os
import sys
import tempfile
from pathlib import Path

import pytest

BACKEND_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BACKEND_DIR.parent

for path in (BACKEND_DIR, PROJECT_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

_TMP_DIR = tempfile.mkdtemp(prefix="aegis-tests-")
os.environ["DATABASE_URL"] = f"sqlite:///{Path(_TMP_DIR) / 'unused.db'}"
os.environ["SECRET_KEY"] = "test-secret-key-not-for-production"
os.environ["ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"
os.environ["DEBUG"] = "False"

from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402

from app.database.connection import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402
from app.models.lesson import Lesson  # noqa: E402
from app.models.question import Question  # noqa: E402
from app.models.quiz import Quiz  # noqa: E402
from app.services import telemetry_service  # noqa: E402


@pytest.fixture()
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = TestingSession()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


@pytest.fixture()
def client(db_session):
    def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    telemetry_service.clear_all()
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    telemetry_service.clear_all()


@pytest.fixture()
def lesson_with_quiz(db_session):
    lesson = Lesson(
        title="Cell Biology",
        topic="Cell Biology",
        difficulty="MIXED",
        content="Cells are the basic unit of life.",
    )
    db_session.add(lesson)
    db_session.flush()

    quiz = Quiz(lesson_id=lesson.id, title="Cell Biology - Easy Quiz", difficulty="EASY")
    db_session.add(quiz)
    db_session.flush()

    db_session.add_all(
        [
            Question(
                quiz_id=quiz.id,
                question="What is the basic unit of life?",
                option_a="Organ",
                option_b="Cell",
                option_c="Tissue",
                option_d="Atom",
                correct_answer="B",
            ),
            Question(
                quiz_id=quiz.id,
                question="Which organelle makes proteins?",
                option_a="Ribosome",
                option_b="Nucleus",
                option_c="Vacuole",
                option_d="Wall",
                correct_answer="A",
            ),
        ]
    )
    db_session.commit()
    return {"lesson_id": lesson.id, "quiz_id": quiz.id}


def register_and_login(client, email="student@example.com", password="Passw0rd!", name="Asha Rao", age=14):
    response = client.post(
        "/register",
        json={"name": name, "email": email, "password": password, "age": age},
    )
    assert response.status_code == 200, response.text
    token = client.post("/login", json={"email": email, "password": password}).json()[
        "access_token"
    ]
    profile = client.get("/profile", headers={"Authorization": f"Bearer {token}"}).json()["data"]
    return {"Authorization": f"Bearer {token}"}, profile


@pytest.fixture()
def auth(client):
    """Register a student and return (headers, profile)."""
    return register_and_login(client)
