"""Phase 7: a monitoring session can only be started for a lesson the student may open."""

from conftest import register_and_login
from curriculum.importer import import_curriculum
from curriculum_fixtures import curriculum_file

from app.models.lesson import Lesson

CONSENT = {"accept": True, "guardian_authorization_confirmed": True, "school_authorization_confirmed": True}


def _setup(client, db_session):
    import_curriculum(
        db_session,
        [curriculum_file(8, "Mathematics", "g8m"), curriculum_file(9, "Mathematics", "g9m")],
        require_complete=False,
    )
    db_session.commit()
    headers, _ = register_and_login(client, email="cam@example.com")
    client.put("/profile/grade", json={"grade": 8}, headers=headers)
    assert client.post("/monitoring/consent", json=CONSENT, headers=headers).status_code == 200
    own = db_session.query(Lesson).filter(Lesson.grade == 8).first()
    other = db_session.query(Lesson).filter(Lesson.grade == 9).first()
    return headers, own, other


def test_session_for_own_grade_lesson_is_created(client, db_session):
    headers, own, _ = _setup(client, db_session)
    response = client.post("/monitoring/sessions", json={"lesson_id": own.id}, headers=headers)
    assert response.status_code == 200, response.text


def test_session_for_another_grade_lesson_is_refused(client, db_session):
    headers, _, other = _setup(client, db_session)
    response = client.post("/monitoring/sessions", json={"lesson_id": other.id}, headers=headers)
    assert response.status_code == 403
    assert "Grade 9" in response.json()["detail"]


def test_session_for_missing_lesson_is_refused(client, db_session):
    headers, _, _ = _setup(client, db_session)
    assert client.post("/monitoring/sessions", json={"lesson_id": 999999}, headers=headers).status_code == 404


def test_session_without_lesson_still_allowed_for_quizzes(client, db_session):
    headers, _, _ = _setup(client, db_session)
    assert client.post("/monitoring/sessions", json={}, headers=headers).status_code == 200
