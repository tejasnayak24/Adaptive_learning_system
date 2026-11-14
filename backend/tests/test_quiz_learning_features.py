"""Phase 5 milestone C: hints, secure answer review, practice/hint/challenge modes, retry."""

from conftest import heartbeat, register_and_login, start_monitoring
from curriculum.importer import import_curriculum
from curriculum_fixtures import curriculum_file


def _setup(client, db_session):
    import_curriculum(db_session, [curriculum_file(8, "Mathematics", "g8m")], require_complete=False)
    db_session.commit()
    headers, _ = register_and_login(client, email="learner@example.com")
    client.put("/profile/grade", json={"grade": 8}, headers=headers)
    lesson = client.get("/curriculum?subject=Mathematics", headers=headers).json()["data"]["subjects"][0]["units"][0]["topics"][0]["lessons"][0]
    quiz_id = next(q["id"] for q in lesson["quizzes"] if q["difficulty"] == "MEDIUM")
    return headers, lesson, quiz_id


def _submit(client, headers, monitoring, quiz_id, letters, **extra):
    heartbeat(client, monitoring, attention_score=0.8)
    questions = client.post("/quiz/start", json={"quiz_id": quiz_id}, headers=headers).json()["data"]["questions"]
    answers = {str(q["id"]): letter for q, letter in zip(questions, letters)}
    body = {
        "quiz_id": quiz_id,
        "monitoring_session_id": monitoring["session_id"],
        "answers": answers,
        "response_time": 50,
        **extra,
    }
    return client.post("/quiz/submit", json=body, headers=headers)


def test_questions_carry_hints_but_never_answers_or_explanations(client, db_session):
    headers, _, quiz_id = _setup(client, db_session)
    for path in (f"/quiz/{quiz_id}",):
        questions = client.get(path, headers=headers).json()["data"]["questions"]
        assert len(questions) == 4
        for q in questions:
            assert q["hint"]
            assert "correct_answer" not in q and "explanation" not in q
    started = client.post("/quiz/start", json={"quiz_id": quiz_id}, headers=headers).json()["data"]["questions"]
    assert all("correct_answer" not in q for q in started)


def test_answer_review_reveals_answers_and_explanations_after_submission(client, db_session):
    headers, _, quiz_id = _setup(client, db_session)
    monitoring = start_monitoring(client, headers)
    data = _submit(client, headers, monitoring, quiz_id, ["A", "A", "A", "A"]).json()["data"]
    review = data["grading"]["results"]
    assert len(review) == 4
    assert all(r["correct_answer"] in "ABCD" and r["explanation"] for r in review)
    # The fixture's MEDIUM answers rotate B, C, D, A, so exactly one 'A' is right.
    assert data["grading"]["correct_count"] == 1
    assert data["progress"]["attempt_mode"] == "standard"


def test_modes_are_recorded_and_retry_creates_new_attempts(client, db_session):
    from app.models.progress import Progress

    headers, lesson, quiz_id = _setup(client, db_session)
    monitoring = start_monitoring(client, headers)
    modes = ["practice", "hints", "challenge"]
    for mode in modes:
        response = _submit(client, headers, monitoring, quiz_id, ["B", "C", "D", "A"], mode=mode, hints_used=2)
        assert response.status_code == 200
        assert response.json()["data"]["progress"]["attempt_mode"] == mode
        assert response.json()["data"]["grading"]["score"] == 100.0

    attempts = db_session.query(Progress).filter_by(quiz_id=quiz_id).order_by(Progress.id).all()
    assert [a.attempt_mode for a in attempts] == modes
    assert all(a.hints_used == 2 for a in attempts)

    bad = _submit(client, headers, monitoring, quiz_id, ["B", "C", "D", "A"], mode="cheat")
    assert bad.status_code == 422


def test_progress_persists_in_curriculum_tree(client, db_session):
    headers, lesson, quiz_id = _setup(client, db_session)
    monitoring = start_monitoring(client, headers)
    _submit(client, headers, monitoring, quiz_id, ["B", "C", "D", "B"])
    _submit(client, headers, monitoring, quiz_id, ["B", "C", "D", "A"], mode="practice")

    tree = client.get("/curriculum?subject=Mathematics", headers=headers).json()["data"]
    first = tree["subjects"][0]["units"][0]["topics"][0]["lessons"][0]
    assert first["id"] == lesson["id"]
    assert first["attempts"] == 2
    assert first["best_score"] == 100.0
    assert tree["subjects"][0]["lessons_attempted"] == 1


def test_difficulty_levels_are_separate_quizzes(client, db_session):
    headers, lesson, _ = _setup(client, db_session)
    levels = {q["difficulty"]: q["id"] for q in lesson["quizzes"]}
    assert set(levels) == {"EASY", "MEDIUM", "HARD"}
    texts = {
        level: {q["question"] for q in client.get(f"/quiz/{qid}", headers=headers).json()["data"]["questions"]}
        for level, qid in levels.items()
    }
    assert all(level in next(iter(texts[level])) for level in levels)
    assert not (texts["EASY"] & texts["HARD"])
