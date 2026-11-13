"""Phase 6: student analytics (dashboard, progress, attention, AI Coach history)."""

import time
from datetime import datetime, timedelta

import pytest

from conftest import heartbeat, register_and_login, start_monitoring
from curriculum.importer import import_curriculum
from curriculum_fixtures import curriculum_file

from app.models.lesson import Lesson
from app.models.monitoring import MonitoringSession
from app.models.progress import Progress
from app.services import analytics_service as an

RL_ACTIONS = [
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
def curriculum(db_session):
    files = [
        curriculum_file(8, "Mathematics", "g8m"),
        curriculum_file(8, "Science", "g8s"),
        curriculum_file(9, "English", "g9e"),
    ]
    import_curriculum(db_session, files, require_complete=False)
    db_session.commit()
    return db_session


def _student(client, email="a@example.com", grade=8):
    headers, profile = register_and_login(client, email=email)
    if grade is not None:
        assert client.put("/profile/grade", json={"grade": grade}, headers=headers).status_code == 200
    return headers, profile


def _lessons(db, grade, subject):
    return (
        db.query(Lesson)
        .filter(Lesson.grade == grade, Lesson.subject == subject)
        .order_by(Lesson.position, Lesson.id)
        .all()
    )


def _attempt(db, student_id, lesson, score, *, attention=None, session=None, at=None, yawn=None, away=None, drowsy=None):
    measured = attention is not None
    row = Progress(
        student_id=student_id,
        lesson_id=lesson.id,
        quiz_id=lesson.quizzes[0].id if lesson.quizzes else None,
        quiz_score=score,
        response_time=40,
        hints_used=0,
        attention_score=attention,
        yawning=(yawn if yawn is not None else False) if measured else None,
        looking_away=(away if away is not None else False) if measured else None,
        drowsy=(drowsy if drowsy is not None else False) if measured else None,
        monitoring_session_id=session,
        difficulty="EASY",
        completed=True,
        created_at=at or datetime.utcnow(),
    )
    db.add(row)
    db.commit()
    return row


def _summary(client, headers):
    response = client.get("/analytics/summary", headers=headers)
    assert response.status_code == 200, response.text
    return response.json()["data"]


# ---------------------------------------------------------------- basics


def test_requires_authentication(client):
    assert client.get("/analytics/summary").status_code == 401


def test_new_student_without_grade_gets_empty_honest_summary(client, curriculum):
    headers, profile = _student(client, grade=None)
    data = _summary(client, headers)
    assert data["grade_required"] is True
    assert data["student"]["name"] == profile["name"]
    assert data["subjects"] == [] and data["topics"] == []
    o = data["overview"]
    assert o["quiz_attempts"] == 0 and o["average_score"] is None and o["latest_activity"] is None
    assert data["attention"]["average_attention"] is None
    assert data["attention"]["sufficient_history"] is False
    assert data["activity"] == [] and data["milestones"] == []
    assert o["current_streak_days"] == 0


def test_new_student_with_grade_sees_only_grade_subjects(client, curriculum):
    headers, _ = _student(client, grade=8)
    data = _summary(client, headers)
    assert [s["subject"] for s in data["subjects"]] == ["Mathematics", "Science"]
    assert data["overview"]["subjects_available"] == 2
    assert data["overview"]["lessons_total"] == 12
    assert all(s["average_score"] is None and s["quiz_attempts"] == 0 for s in data["subjects"])
    assert all(t["status"] == "not_started" for t in data["topics"])
    assert len(data["topics"]) == 6


def test_different_grades_see_their_own_curriculum(client, curriculum):
    h9, _ = _student(client, email="nine@example.com", grade=9)
    data = _summary(client, h9)
    assert [s["subject"] for s in data["subjects"]] == ["English"]
    assert data["overview"]["lessons_total"] == 6


# ------------------------------------------------------ statistics/ownership


def test_dashboard_statistics_and_completion_use_pass_mark(client, curriculum):
    headers, me = _student(client)
    db = curriculum
    maths = _lessons(db, 8, "Mathematics")
    science = _lessons(db, 8, "Science")
    _attempt(db, me["id"], maths[0], 25)  # attempted, not passed
    _attempt(db, me["id"], maths[0], 75)  # now passed
    _attempt(db, me["id"], maths[1], 100)
    _attempt(db, me["id"], science[0], 40)  # attempted only

    data = _summary(client, headers)
    o = data["overview"]
    assert o["quiz_attempts"] == 4
    assert o["average_score"] == 60.0
    assert o["lessons_completed"] == 2
    assert o["lessons_attempted"] == 3
    assert o["completion_percent"] == round(2 / 12 * 100, 1)
    assert o["best_score"] == 100.0
    assert o["latest_activity"]["lesson_id"] == science[0].id

    by_subject = {s["subject"]: s for s in data["subjects"]}
    assert by_subject["Mathematics"]["quiz_attempts"] == 3
    assert by_subject["Mathematics"]["average_score"] == round((25 + 75 + 100) / 3, 1)
    assert by_subject["Mathematics"]["lessons_completed"] == 2
    assert by_subject["Mathematics"]["progress_percent"] == round(2 / 6 * 100, 1)
    assert by_subject["Science"]["lessons_completed"] == 0
    assert by_subject["Science"]["lessons_attempted"] == 1


def test_student_only_sees_own_records(client, curriculum):
    h1, me = _student(client, email="one@example.com")
    h2, other = _student(client, email="two@example.com")
    lesson = _lessons(curriculum, 8, "Mathematics")[0]
    _attempt(curriculum, other["id"], lesson, 90, attention=0.9)

    mine = _summary(client, h1)
    assert mine["overview"]["quiz_attempts"] == 0
    assert mine["attention"]["measured_attempts"] == 0
    theirs = _summary(client, h2)
    assert theirs["overview"]["quiz_attempts"] == 1
    assert theirs["student"]["id"] == other["id"]
    # Recommendation history is also scoped to the caller.
    assert client.get("/recommendations", headers=h1).json()["data"] == []


def test_curriculum_tree_marks_completed_by_pass_mark(client, curriculum):
    headers, me = _student(client)
    maths = _lessons(curriculum, 8, "Mathematics")
    _attempt(curriculum, me["id"], maths[0], 20)
    _attempt(curriculum, me["id"], maths[1], 50)
    tree = client.get("/curriculum?subject=Mathematics", headers=headers).json()["data"]
    lessons = {l["id"]: l for u in tree["subjects"][0]["units"] for t in u["topics"] for l in t["lessons"]}
    assert lessons[maths[0].id]["completed"] is False and lessons[maths[0].id]["attempts"] == 1
    assert lessons[maths[1].id]["completed"] is True


# ---------------------------------------------------------------- topics


def test_topic_status_classification():
    assert an.topic_status([]) == "not_started"
    assert an.topic_status([10]) == "insufficient_data"
    assert an.topic_status([100]) == "insufficient_data"
    assert an.topic_status([90, 85]) == "strong"
    assert an.topic_status([30, 40]) == "weak"
    assert an.topic_status([60, 70]) == "needs_revision"
    # Recent attempts matter: early failures followed by mastery.
    assert an.topic_status([0, 10, 90, 90, 95]) == "strong"
    # A high average with a failed latest attempt needs revision.
    assert an.topic_status([100, 100, 40]) == "needs_revision"


def test_topic_performance_never_calls_unattempted_topics_weak(client, curriculum):
    headers, me = _student(client)
    maths = _lessons(curriculum, 8, "Mathematics")  # topic 0: lessons 0,1; topic 1: 2,3; topic 2: 4,5
    _attempt(curriculum, me["id"], maths[0], 90)
    _attempt(curriculum, me["id"], maths[1], 95)
    _attempt(curriculum, me["id"], maths[2], 20)
    _attempt(curriculum, me["id"], maths[3], 30)
    _attempt(curriculum, me["id"], maths[4], 10)  # only one attempt

    topics = [t for t in _summary(client, headers)["topics"] if t["subject"] == "Mathematics"]
    assert [t["status"] for t in topics] == ["strong", "weak", "insufficient_data"]
    assert topics[1]["revise_lesson"]["lesson_id"] == maths[2].id
    assert topics[0]["lessons_completed"] == 2 and topics[0]["next_lesson"] is None
    science = [t for t in _summary(client, headers)["topics"] if t["subject"] == "Science"]
    assert all(t["status"] == "not_started" and t["average_score"] is None for t in science)


# ----------------------------------------------------------------- trend


def test_quiz_trend_is_chronological_with_subject_and_date(client, curriculum):
    headers, me = _student(client)
    maths = _lessons(curriculum, 8, "Mathematics")
    science = _lessons(curriculum, 8, "Science")
    base = datetime(2026, 10, 1, 9, 0)
    _attempt(curriculum, me["id"], maths[0], 40, at=base)
    _attempt(curriculum, me["id"], science[0], 60, at=base + timedelta(days=1))
    _attempt(curriculum, me["id"], maths[0], 80, at=base + timedelta(days=2))

    trend = _summary(client, headers)["trend"]
    assert [p["score"] for p in trend] == [40.0, 60.0, 80.0]
    assert [p["subject"] for p in trend] == ["Mathematics", "Science", "Mathematics"]
    assert trend[0]["at"].startswith("2026-10-01")
    assert trend[0]["passed"] is False and trend[2]["passed"] is True
    assert all(p["topic"] for p in trend)


# ------------------------------------------------------------- attention


def test_attention_average_excludes_null_and_separates_unavailable(client, curriculum, db_session):
    headers, me = _student(client)
    lesson = _lessons(curriculum, 8, "Mathematics")[0]
    db_session.add(MonitoringSession(id="sess-1", student_id=me["id"], status="ended"))
    db_session.commit()
    _attempt(db_session, me["id"], lesson, 70, attention=0.9, session="sess-1", yawn=True)
    _attempt(db_session, me["id"], lesson, 70, attention=0.5, session="sess-1", away=True, drowsy=True)
    _attempt(db_session, me["id"], lesson, 70, attention=None, session="sess-1")  # camera unavailable/stale
    _attempt(db_session, me["id"], lesson, 70, attention=None, session=None)  # before monitoring existed

    att = _summary(client, headers)["attention"]
    assert att["granularity"] == "per_quiz_attempt"
    assert att["attempts_total"] == 4
    assert att["measured_attempts"] == 2
    assert att["average_attention"] == 70.0  # (90 + 50) / 2, NULLs excluded, not (140 / 4)
    assert att["lowest_attention"] == 50.0 and att["highest_attention"] == 90.0
    assert att["unavailable_attempts"] == 1
    assert att["not_monitored_attempts"] == 1
    assert att["yawning"] == {"observed_in": 1, "measured_attempts": 2}
    assert att["looking_away"] == {"observed_in": 1, "measured_attempts": 2}
    assert att["drowsiness"] == {"observed_in": 1, "measured_attempts": 2}
    assert att["sufficient_history"] is False
    trend = _summary(client, headers)["trend"]
    assert [p["telemetry"] for p in trend] == ["measured", "measured", "unavailable", "not_monitored"]
    assert trend[2]["attention"] is None and trend[2]["yawning"] is None


def test_only_null_attention_gives_no_average(client, curriculum):
    headers, me = _student(client)
    lesson = _lessons(curriculum, 8, "Science")[0]
    for _ in range(3):
        _attempt(curriculum, me["id"], lesson, 60)
    att = _summary(client, headers)["attention"]
    assert att["average_attention"] is None and att["measured_attempts"] == 0
    assert att["by_subject"] == []


def test_stale_camera_readings_are_stored_as_unavailable_not_low(client, curriculum):
    headers, me = _student(client)
    lesson = _lessons(curriculum, 8, "Mathematics")[0]
    monitoring = start_monitoring(client, headers, lesson.id)
    # The agent sends a measurement captured long ago: not live data.
    old = time.time() - 600
    heartbeat(client, monitoring, captured_at=old, attention_score=0.1)
    quiz_id = lesson.quizzes[0].id
    questions = client.get(f"/quiz/{quiz_id}", headers=headers).json()["data"]["questions"]
    sub = client.post(
        "/quiz/submit",
        headers=headers,
        json={
            "quiz_id": quiz_id,
            "monitoring_session_id": monitoring["session_id"],
            "answers": {str(q["id"]): "A" for q in questions},
            "response_time": 30,
        },
    )
    assert sub.status_code == 200, sub.text
    assert sub.json()["data"]["progress"]["attention_score"] is None

    data = _summary(client, headers)
    assert data["attention"]["unavailable_attempts"] == 1
    assert data["attention"]["average_attention"] is None
    assert data["trend"][-1]["telemetry"] == "unavailable"


# ------------------------------------------------------ activity/milestones


def test_activity_and_milestones_come_from_saved_attempts(client, curriculum):
    headers, me = _student(client)
    maths = _lessons(curriculum, 8, "Mathematics")
    now = datetime.utcnow()
    for i, lesson in enumerate(maths):
        _attempt(curriculum, me["id"], lesson, 100 if i == 0 else 60, at=now - timedelta(days=len(maths) - i))

    data = _summary(client, headers)
    keys = [m["key"] for m in data["milestones"]]
    assert keys[0] == "first_quiz"
    assert "lessons_completed_1" in keys and "lessons_completed_5" in keys
    assert "first_mastery" in keys and "first_perfect" in keys
    assert "subject_completed_Mathematics" in keys
    assert "subject_completed_Science" not in keys
    types = {e["type"] for e in data["activity"]}
    assert types == {"quiz_attempt", "lesson_completed", "subject_completed"}
    assert data["activity"][0]["type"] == "subject_completed"
    maths_row = next(s for s in data["subjects"] if s["subject"] == "Mathematics")
    assert maths_row["completed"] is True and maths_row["progress_percent"] == 100.0
    # Six consecutive days ending yesterday.
    assert data["overview"]["days_active"] == 6
    assert data["overview"]["current_streak_days"] == 6
    assert data["overview"]["longest_streak_days"] == 6


def test_streak_helper_handles_gaps():
    from datetime import date

    today = date(2026, 11, 13)
    days = {date(2026, 11, 1), date(2026, 11, 2), date(2026, 11, 3), date(2026, 11, 12), date(2026, 11, 13)}
    s = an._streaks(days, today)
    assert s == {"days_active": 5, "current_streak_days": 2, "longest_streak_days": 3, "timezone": "UTC"}
    assert an._streaks({date(2026, 11, 1)}, today)["current_streak_days"] == 0


# ---------------------------------------------------------------- AI Coach


def _submit(client, headers, monitoring, quiz_id, letter="A"):
    heartbeat(client, monitoring, attention_score=0.85)
    questions = client.get(f"/quiz/{quiz_id}", headers=headers).json()["data"]["questions"]
    return client.post(
        "/quiz/submit",
        headers=headers,
        json={
            "quiz_id": quiz_id,
            "monitoring_session_id": monitoring["session_id"],
            "answers": {str(q["id"]): letter for q in questions},
            "response_time": 45,
        },
    )


def test_coach_history_has_context_and_outcome(client, curriculum):
    headers, me = _student(client)
    lesson = _lessons(curriculum, 8, "Mathematics")[0]
    monitoring = start_monitoring(client, headers, lesson.id)
    first = _submit(client, headers, monitoring, lesson.quizzes[0].id).json()["data"]
    assert first["recommendation"]["action"] in RL_ACTIONS

    history = client.get("/recommendations", headers=headers).json()["data"]
    assert len(history) == 1
    item = history[0]
    assert item["context"]["subject"] == "Mathematics" and item["context"]["grade"] == 8
    assert item["context"]["topic"] == "Topic 0"
    assert item["context"]["lesson_id"] == lesson.id
    assert item["outcome"] == {"status": "pending"}
    assert item["policy"] in ("q_learning", "q_learning_nearest_state", "fallback")

    _submit(client, headers, monitoring, lesson.quizzes[0].id, letter="B")
    history = client.get("/recommendations", headers=headers).json()["data"]
    assert len(history) == 2
    older = history[1]
    assert older["outcome"]["status"] == "recorded"
    assert older["outcome"]["same_lesson"] is True
    assert older["outcome"]["score_change"] == round(history[0]["context"]["score"] - older["context"]["score"], 1)
    assert older["outcome"]["reward"] is not None
    assert history[0]["outcome"]["status"] == "pending"

    latest = client.get("/recommendations/latest", headers=headers).json()["data"]
    assert latest["attempt"]["subject"] == "Mathematics"
    assert latest["attempt"]["curriculum_topic"] == "Topic 0"
    assert latest["recommendation"]["id"] == history[0]["id"]


def test_recommendation_history_limit_is_validated(client, curriculum):
    headers, _ = _student(client)
    assert client.get("/recommendations?limit=0", headers=headers).status_code == 422
    assert client.get("/recommendations?limit=5", headers=headers).status_code == 200


@pytest.mark.parametrize("action", RL_ACTIONS)
def test_every_rl_action_resolves_in_coach_and_next_step(client, curriculum, db_session, action):
    """Each of the 11 actions, as stored by the Q-learning service, appears in
    the coach history with context and resolves to a concrete next step."""
    from app.models.recommendation import RecommendationHistory
    from app.services import curriculum_service as cs

    headers, me = _student(client)
    maths = _lessons(curriculum, 8, "Mathematics")
    lesson = maths[2]
    attempt = _attempt(db_session, me["id"], lesson, 65, attention=0.7, session=None)
    db_session.add(
        RecommendationHistory(
            student_id=me["id"],
            progress_id=attempt.id,
            action=action,
            confidence=0.5,
            explanation="test",
            state="{}",
            state_key="[]",
            policy="q_learning",
        )
    )
    db_session.commit()

    item = client.get("/recommendations", headers=headers).json()["data"][0]
    assert item["action"] == action and item["context"]["lesson_id"] == lesson.id

    quiz = next(q for q in lesson.quizzes if q.difficulty == "MEDIUM")
    step = cs.recommendation_next_step(db_session, lesson, quiz, action)
    assert step is not None and step["kind"] in ("lesson", "quiz", "break", "subject_complete")
    if step["kind"] == "lesson":
        target = db_session.get(Lesson, step["lesson_id"])
        assert (target.grade, target.subject) == (8, "Mathematics")

    latest = client.get("/recommendations/latest", headers=headers).json()["data"]
    assert latest["status"] == "available" and latest["recommendation"]["action"] == action
    assert latest["next_step"]["kind"] == step["kind"]
