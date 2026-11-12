"""Phase 5 milestone A: grade support, hierarchy, access rules, importer."""

import json

import pytest

from conftest import register_and_login
from curriculum.importer import CurriculumError, import_curriculum
from curriculum_fixtures import curriculum_file


@pytest.fixture()
def small_curriculum(db_session):
    from seed_science import seed_into

    seed_into(db_session)
    files = [
        curriculum_file(9, "Science", "g9sci", legacy={"title": "Cell Biology"}),
        curriculum_file(9, "Mathematics", "g9math"),
        curriculum_file(6, "Mathematics", "g6math"),
    ]
    stats = import_curriculum(db_session, files, require_complete=False)
    db_session.commit()
    return files, stats


def _student(client, grade, email):
    headers, profile = register_and_login(client, email=email)
    if grade is not None:
        assert client.put("/profile/grade", json={"grade": grade}, headers=headers).status_code == 200
    return headers


def test_register_with_grade_and_profile_reports_it(client):
    response = client.post(
        "/register",
        json={"name": "Meera", "email": "meera@example.com", "password": "Passw0rd!", "age": 12, "grade": 7},
    )
    assert response.status_code == 200 and response.json()["data"]["grade"] == 7
    token = client.post("/login", json={"email": "meera@example.com", "password": "Passw0rd!"}).json()["access_token"]
    assert client.get("/profile", headers={"Authorization": f"Bearer {token}"}).json()["data"]["grade"] == 7

    bad = client.post(
        "/register",
        json={"name": "X", "email": "x@example.com", "password": "Passw0rd!", "age": 12, "grade": 11},
    )
    assert bad.status_code == 422


def test_existing_account_without_grade_must_choose_one(client, small_curriculum):
    headers, profile = register_and_login(client, email="old@example.com")
    assert profile["grade"] is None
    assert client.get("/curriculum", headers=headers).status_code == 409
    assert client.get("/curriculum", headers=headers).json()["detail"] == "grade_required"
    assert client.get("/lessons", headers=headers).json()["data"] == []
    assert client.put("/profile/grade", json={"grade": 12}, headers=headers).status_code == 422
    assert client.put("/profile/grade", json={"grade": 9}, headers=headers).status_code == 200
    assert client.get("/curriculum", headers=headers).status_code == 200


def test_curriculum_is_filtered_by_grade(client, small_curriculum):
    g9 = _student(client, 9, "g9@example.com")
    g6 = _student(client, 6, "g6@example.com")

    tree9 = client.get("/curriculum", headers=g9).json()["data"]
    assert tree9["grade"] == 9
    assert [s["subject"] for s in tree9["subjects"]] == ["Mathematics", "Science"]
    tree6 = client.get("/curriculum", headers=g6).json()["data"]
    assert [s["subject"] for s in tree6["subjects"]] == ["Mathematics"]

    only_science = client.get("/curriculum?subject=Science", headers=g9).json()["data"]["subjects"]
    assert [s["subject"] for s in only_science] == ["Science"]
    science = only_science[0]
    assert science["lesson_count"] == 6
    topics = science["units"][0]["topics"]
    assert len(topics) == 3 and all(len(t["lessons"]) == 2 for t in topics)

    assert client.get("/curriculum?grade=6", headers=g9).status_code == 403
    assert client.get("/curriculum?subject=Art", headers=g9).status_code == 422

    lessons9 = client.get("/lessons", headers=g9).json()["data"]
    assert len(lessons9) == 12 and {l["grade"] for l in lessons9} == {9}


def test_lesson_detail_material_navigation_and_grade_access(client, small_curriculum, db_session):
    from app.models.lesson import Lesson

    g9 = _student(client, 9, "nav9@example.com")
    g6 = _student(client, 6, "nav6@example.com")
    second = db_session.query(Lesson).filter_by(slug="g9math-t0-l1").one()

    body = client.get(f"/lesson/{second.id}", headers=g9).json()["data"]
    assert body["grade"] == 9 and body["subject"] == "Mathematics"
    assert body["curriculum_topic"]["title"] == "Topic 0" and body["unit"]["title"] == "Unit"
    assert body["material"]["objectives"] and body["material"]["worked"]
    nav = body["navigation"]
    assert nav["index"] == 1 and nav["total"] == 6
    assert nav["previous"]["id"] == db_session.query(Lesson).filter_by(slug="g9math-t0-l0").one().id
    assert nav["next"]["id"] == db_session.query(Lesson).filter_by(slug="g9math-t1-l0").one().id
    assert nav["skip"]["id"] == db_session.query(Lesson).filter_by(slug="g9math-t1-l1").one().id
    assert nav["next_topic"]["id"] == nav["next"]["id"]

    assert client.get(f"/lesson/{second.id}", headers=g6).status_code == 403
    quiz_id = body["quizzes"][0]["id"]
    assert client.get(f"/quiz/{quiz_id}", headers=g6).status_code == 403
    questions = client.get(f"/quiz/{quiz_id}", headers=g9).json()["data"]["questions"]
    assert all(q["hint"] for q in questions)
    assert all("correct_answer" not in q and "explanation" not in q for q in questions)


def test_teacher_can_browse_any_grade(client, small_curriculum, db_session):
    from app.models.student import Student

    headers, profile = register_and_login(client, email="teacher@example.com")
    db_session.get(Student, profile["id"]).role = "teacher"
    db_session.commit()
    assert client.get("/curriculum?grade=6", headers=headers).json()["data"]["grade"] == 6
    assert len(client.get("/lessons", headers=headers).json()["data"]) >= 18


def test_original_science_lesson_is_adopted_not_duplicated(client, small_curriculum, db_session):
    from app.models.lesson import Lesson
    from app.models.question import Question

    files, stats = small_curriculum
    assert stats.adopted_legacy_lessons == 1
    cell = db_session.query(Lesson).filter_by(title="Cell Biology").all()
    assert len(cell) == 1
    cell = cell[0]
    assert cell.slug == "g9sci-legacy" and cell.grade == 9 and cell.subject == "Science"
    assert cell.content.startswith("Cells are the basic structural")  # original text kept
    assert len(cell.quizzes) == 3
    assert sum(len(q.questions) for q in cell.quizzes) == 15  # original questions kept

    noted = db_session.query(Question).filter_by(question="What is the basic structural and functional unit of life?").one()
    assert noted.correct_answer == "B"  # answer unchanged
    assert noted.hint and noted.explanation
    assert json.loads(cell.material)["objectives"]


def test_import_is_idempotent(db_session, small_curriculum):
    from app.models.lesson import Lesson
    from app.models.question import Question

    files, _ = small_curriculum
    before = (db_session.query(Lesson).count(), db_session.query(Question).count())
    again = import_curriculum(db_session, files, require_complete=False)
    db_session.commit()
    assert again.total_created == 0
    assert sum(again.updated.values()) == 0
    assert (db_session.query(Lesson).count(), db_session.query(Question).count()) == before


def test_invalid_content_is_refused(db_session):
    bad = curriculum_file(7, "English", "g7eng")
    bad["units"][0]["topics"][0]["lessons"][0]["intro"] = "Too short."
    bad["units"][0]["topics"][0]["lessons"][0]["sections"] = [["A", "b"], ["C", "d"]]
    with pytest.raises(CurriculumError, match="explanation too short"):
        import_curriculum(db_session, [bad], require_complete=False)
    with pytest.raises(CurriculumError, match="missing grade"):
        import_curriculum(db_session, [curriculum_file(7, "English", "ok")])
