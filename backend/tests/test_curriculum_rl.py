"""Phase 5 milestone E: RL recommendations resolve to the student's own grade and subject."""

import pytest

from conftest import heartbeat, register_and_login, start_monitoring
from curriculum.importer import import_curriculum
from curriculum_fixtures import curriculum_file

ACTIONS = [
    "NEXT_LESSON",
    "REPEAT_LESSON",
    "INCREASE_DIFFICULTY",
    "DECREASE_DIFFICULTY",
    "PRACTICE_QUIZ",
    "QUICK_CHALLENGE",
    "SHOW_WORKED_EXAMPLE",
    "PROVIDE_HINT",
    "FOCUS_RECOVERY",
    "SHOW_REAL_WORLD_APPLICATION",
    "SKIP_TO_ADVANCED_TOPIC",
]


@pytest.fixture()
def two_grades(db_session):
    files = [
        curriculum_file(8, "Mathematics", "g8m"),
        curriculum_file(8, "Science", "g8s"),
        curriculum_file(9, "Mathematics", "g9m"),
    ]
    import_curriculum(db_session, files, require_complete=False)
    db_session.commit()


def _lesson(db_session, slug):
    from app.models.lesson import Lesson

    return db_session.query(Lesson).filter_by(slug=slug).one()


def _quiz(lesson, level):
    return next(q for q in lesson.quizzes if q.difficulty == level)


@pytest.mark.parametrize("action", ACTIONS)
def test_every_action_has_a_target_inside_the_same_grade_and_subject(db_session, two_grades, action):
    from app.models.lesson import Lesson
    from app.models.quiz import Quiz
    from app.services.curriculum_service import recommendation_next_step

    lesson = _lesson(db_session, "g8m-t1-l0")  # 3rd of 6 Grade 8 Mathematics lessons
    step = recommendation_next_step(db_session, lesson, _quiz(lesson, "MEDIUM"), action)
    assert step is not None and step["kind"] in ("lesson", "quiz", "break")

    if step["kind"] == "lesson":
        target = db_session.get(Lesson, step["lesson_id"])
        assert (target.grade, target.subject) == (8, "Mathematics")
    if step["kind"] == "quiz":
        target = db_session.get(Quiz, step["quiz_id"])
        assert target.lesson_id == lesson.id


def test_pacing_targets_follow_curriculum_order(db_session, two_grades):
    from app.services.curriculum_service import recommendation_next_step

    lesson = _lesson(db_session, "g8m-t1-l0")
    quiz = _quiz(lesson, "MEDIUM")
    assert recommendation_next_step(db_session, lesson, quiz, "NEXT_LESSON")["lesson_id"] == _lesson(db_session, "g8m-t1-l1").id
    assert recommendation_next_step(db_session, lesson, quiz, "SKIP_TO_ADVANCED_TOPIC")["lesson_id"] == _lesson(db_session, "g8m-t2-l0").id
    assert recommendation_next_step(db_session, lesson, quiz, "INCREASE_DIFFICULTY")["difficulty"] == "HARD"
    assert recommendation_next_step(db_session, lesson, quiz, "DECREASE_DIFFICULTY")["difficulty"] == "EASY"
    assert recommendation_next_step(db_session, lesson, quiz, "QUICK_CHALLENGE")["mode"] == "challenge"
    assert recommendation_next_step(db_session, lesson, quiz, "SHOW_WORKED_EXAMPLE")["section"] == "worked-examples"


def test_last_lesson_never_jumps_to_another_grade_or_subject(db_session, two_grades):
    from app.services.curriculum_service import recommendation_next_step

    last = _lesson(db_session, "g8m-t2-l1")  # final Grade 8 Mathematics lesson
    for action in ("NEXT_LESSON", "SKIP_TO_ADVANCED_TOPIC"):
        step = recommendation_next_step(db_session, last, _quiz(last, "HARD"), action)
        assert step == {"kind": "subject_complete", "grade": 8, "subject": "Mathematics"}
    hard = recommendation_next_step(db_session, last, _quiz(last, "HARD"), "INCREASE_DIFFICULTY")
    assert hard["kind"] == "quiz" and hard["mode"] == "practice"  # already at HARD


def test_submit_returns_next_step_within_grade_and_subject(client, db_session, two_grades):
    from app.models.lesson import Lesson

    headers, _ = register_and_login(client, email="rl8@example.com")
    client.put("/profile/grade", json={"grade": 8}, headers=headers)
    lesson = _lesson(db_session, "g8m-t0-l0")
    quiz_id = _quiz(lesson, "EASY").id
    monitoring = start_monitoring(client, headers)
    heartbeat(client, monitoring, attention_score=0.85)
    questions = client.get(f"/quiz/{quiz_id}", headers=headers).json()["data"]["questions"]
    answers = {str(q["id"]): "A" for q in questions}
    data = client.post(
        "/quiz/submit",
        json={"quiz_id": quiz_id, "monitoring_session_id": monitoring["session_id"], "answers": answers, "response_time": 40},
        headers=headers,
    ).json()["data"]

    assert data["recommendation"] is not None
    step = data["next_step"]
    assert step is not None
    if step["kind"] == "lesson":
        target = db_session.get(Lesson, step["lesson_id"])
        assert (target.grade, target.subject) == (8, "Mathematics")

    latest = client.get("/recommendations/latest", headers=headers).json()["data"]
    assert latest["next_step"] == step
