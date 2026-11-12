from conftest import heartbeat, register_and_login, start_monitoring

# lesson_with_quiz creates two questions; correct answers are B then A.
ALL_CORRECT = ["B", "A"]


def _answers(client, headers, quiz_id, letters):
    questions = client.get(f"/quiz/{quiz_id}", headers=headers).json()["data"]["questions"]
    return {str(q["id"]): letter for q, letter in zip(questions, letters)}


import pytest

_SESSIONS = {}


@pytest.fixture(autouse=True)
def _fresh_sessions():
    _SESSIONS.clear()
    yield
    _SESSIONS.clear()


def _monitoring(client, headers):
    key = headers["Authorization"]
    if key not in _SESSIONS:
        _SESSIONS[key] = start_monitoring(client, headers)
    return _SESSIONS[key]


def _submit(client, headers, quiz_id, letters=ALL_CORRECT, camera=None, **overrides):
    """Submit answers; ``camera`` is a list of heartbeat dicts sent first."""
    monitoring = _monitoring(client, headers)
    me = client.get("/profile", headers=headers).json()["data"]["id"]
    client.post(f"/attention/{me}/reset", headers=headers)
    for beat in camera or []:
        assert heartbeat(client, monitoring, **beat).status_code == 200
    body = {
        "quiz_id": quiz_id,
        "monitoring_session_id": monitoring["session_id"],
        "answers": _answers(client, headers, quiz_id, letters),
        "response_time": 42,
    }
    body.update(overrides)
    return client.post("/quiz/submit", json=body, headers=headers)


def test_quiz_delivery_never_exposes_answers(client, auth, lesson_with_quiz):
    headers, _ = auth
    quiz_id = lesson_with_quiz["quiz_id"]

    for response in (
        client.get(f"/quiz/{quiz_id}", headers=headers),
        client.post("/quiz/start", json={"quiz_id": quiz_id}, headers=headers),
    ):
        assert response.status_code == 200
        questions = response.json()["data"]["questions"]
        assert len(questions) == 2
        assert all("correct_answer" not in q for q in questions)

    assert client.get(f"/quiz/{quiz_id}").status_code == 401


def test_server_grades_answers_and_ignores_client_score(client, auth, lesson_with_quiz):
    headers, profile = auth
    response = _submit(client, headers, lesson_with_quiz["quiz_id"], letters=["B", "C"], quiz_score=100)

    assert response.status_code == 200, response.text
    data = response.json()["data"]
    assert data["grading"]["score"] == 50.0
    assert data["grading"]["correct_count"] == 1
    assert data["grading"]["total_questions"] == 2
    # Correct answers are revealed only after submission.
    assert [r["correct_answer"] for r in data["grading"]["results"]] == ["B", "A"]

    progress = data["progress"]
    assert progress["student_id"] == profile["id"]
    assert progress["quiz_id"] == lesson_with_quiz["quiz_id"]
    assert progress["quiz_score"] == 50.0
    assert progress["difficulty"] == "EASY"
    assert progress["created_at"] is not None


def test_incomplete_or_invalid_answers_rejected(client, auth, lesson_with_quiz):
    headers, _ = auth
    quiz_id = lesson_with_quiz["quiz_id"]
    answers = _answers(client, headers, quiz_id, ALL_CORRECT)
    first_id = next(iter(answers))

    session_id = _monitoring(client, headers)["session_id"]
    partial = {"quiz_id": quiz_id, "monitoring_session_id": session_id, "answers": {first_id: "B"}, "response_time": 5}
    response = client.post("/quiz/submit", json=partial, headers=headers)
    assert response.status_code == 422 and "Unanswered" in response.text

    foreign = {**partial, "answers": {**answers, "999999": "A"}}
    response = client.post("/quiz/submit", json=foreign, headers=headers)
    assert response.status_code == 422 and "not in this quiz" in response.text

    bad_letter = {**partial, "answers": {**answers, first_id: "E"}}
    response = client.post("/quiz/submit", json=bad_letter, headers=headers)
    assert response.status_code == 422 and "A, B, C or D" in response.text

    assert client.post("/quiz/submit", json={**partial, "quiz_id": 424242}, headers=headers).status_code == 404


def test_submission_without_telemetry_is_saved_as_null(client, auth, lesson_with_quiz):
    headers, _ = auth
    data = _submit(client, headers, lesson_with_quiz["quiz_id"]).json()["data"]

    assert data["progress"]["attention_score"] is None
    assert data["progress"]["yawning"] is None
    assert data["progress"]["telemetry_available"] is False
    assert data["recommendation"] is None
    assert data["recommendation_status"] == "telemetry_unavailable"


def test_submission_with_telemetry_stores_recommendation(client, auth, lesson_with_quiz):
    headers, _ = auth
    data = _submit(
        client,
        headers,
        lesson_with_quiz["quiz_id"],
        camera=[{"attention_score": 0.80}, {"attention_score": 0.84}],
        hints_used=1,
    ).json()["data"]

    assert data["progress"]["attention_score"] == 0.82  # server-side average of the heartbeats
    assert data["progress"]["hints_used"] == 1
    assert data["recommendation_status"] == "available"
    rec = data["recommendation"]
    assert isinstance(rec["action"], str)
    assert rec["policy"] in ("q_learning", "q_learning_nearest_state", "fallback")
    assert rec["model_version"].startswith("v3-")
    assert rec["confidence_kind"] == "heuristic_decision_strength"
    assert rec["action"] not in (rec["blocked_actions"] or {})

    latest = client.get("/recommendations/latest", headers=headers).json()["data"]
    assert latest["status"] == "available"
    assert latest["recommendation"]["id"] == rec["id"]
    assert latest["attempt"]["lesson_title"] == "Cell Biology"

    history = client.get("/recommendations", headers=headers).json()["data"]
    assert [row["id"] for row in history] == [rec["id"]]


def test_next_attempt_records_reward_for_previous_recommendation(client, auth, lesson_with_quiz, db_session):
    from app.models.recommendation import RecommendationHistory
    from app.models.reward import RewardHistory

    headers, _ = auth
    quiz_id = lesson_with_quiz["quiz_id"]
    first = _submit(client, headers, quiz_id, letters=["C", "C"], camera=[{"attention_score": 0.5}]).json()["data"]
    second = _submit(client, headers, quiz_id, letters=ALL_CORRECT, camera=[{"attention_score": 0.9}]).json()["data"]

    rows = db_session.query(RewardHistory).all()
    assert len(rows) == 1
    reward = rows[0]
    assert reward.recommendation_id == first["recommendation"]["id"]
    assert reward.progress_id == second["progress"]["id"]
    assert reward.action == first["recommendation"]["action"]
    # Reward version 2 (rl_engine.training.rewards.observed_reward), same lesson
    # and difficulty, 0% -> 100%: learning gain +3.0 (clipped), engagement
    # 2*(0.9-0.5) = +0.8, step cost -0.5  ->  3.3
    assert reward.reward == 3.3
    assert reward.reward_version == 2
    import json as _json

    detail = _json.loads(reward.reward_detail)
    assert detail["learning_gain"] == 3.0 and detail["engagement_change"] == 0.8
    # Same lesson and same quiz level: consistent with same-lesson actions,
    # not observable for break/real-world/challenge.
    expected_followed = {
        "REPEAT_LESSON": True, "PRACTICE_QUIZ": True, "SHOW_WORKED_EXAMPLE": True, "PROVIDE_HINT": True,
        "DECREASE_DIFFICULTY": False, "INCREASE_DIFFICULTY": False,
        "FOCUS_RECOVERY": None, "SHOW_REAL_WORLD_APPLICATION": None, "QUICK_CHALLENGE": None,
    }
    assert reward.followed == expected_followed[reward.action]

    closed = db_session.get(RecommendationHistory, first["recommendation"]["id"])
    assert closed.outcome_progress_id == second["progress"]["id"]


def test_latest_recommendation_states(client, auth, lesson_with_quiz):
    headers, _ = auth
    empty = client.get("/recommendations/latest", headers=headers).json()["data"]
    assert empty["status"] == "no_attempts"

    _submit(client, headers, lesson_with_quiz["quiz_id"])
    no_camera = client.get("/recommendations/latest", headers=headers).json()["data"]
    assert no_camera["status"] == "telemetry_unavailable"
    assert no_camera["recommendation"] is None
    assert no_camera["attempt"]["telemetry_available"] is False


def test_submission_is_always_recorded_for_token_owner(client, auth, lesson_with_quiz):
    headers, profile = auth
    _, other = register_and_login(client, email="other@example.com")

    forged = _submit(client, headers, lesson_with_quiz["quiz_id"], student_id=other["id"])
    assert forged.status_code == 403

    same = _submit(client, headers, lesson_with_quiz["quiz_id"], student_id=profile["id"])
    assert same.status_code == 200


def test_progress_is_owner_only(client, auth, lesson_with_quiz):
    headers, profile = auth
    _submit(client, headers, lesson_with_quiz["quiz_id"], camera=[{"attention_score": 0.7}])

    own = client.get(f"/progress/{profile['id']}", headers=headers)
    assert own.status_code == 200
    rows = own.json()["data"]
    assert len(rows) == 1
    assert rows[0]["attention_score"] == 0.7

    other_headers, _ = register_and_login(client, email="peer@example.com")
    assert client.get(f"/progress/{profile['id']}", headers=other_headers).status_code == 403
    assert client.get(f"/progress/{profile['id']}").status_code == 401

    progress_id = rows[0]["id"]
    update = {
        "quiz_score": 90,
        "response_time": 30,
        "attention_score": None,
        "difficulty": "hard",
        "completed": True,
    }
    assert client.put(f"/progress/{progress_id}", json=update, headers=other_headers).status_code == 403
    updated = client.put(f"/progress/{progress_id}", json=update, headers=headers)
    assert updated.status_code == 200
    assert updated.json()["data"]["difficulty"] == "HARD"


def test_lesson_progress_returns_latest_attempt(client, auth, lesson_with_quiz):
    headers, profile = auth
    lesson_id = lesson_with_quiz["lesson_id"]
    _submit(client, headers, lesson_with_quiz["quiz_id"], letters=["C", "C"])
    _submit(client, headers, lesson_with_quiz["quiz_id"], letters=ALL_CORRECT)

    latest = client.get(f"/progress/{profile['id']}/{lesson_id}", headers=headers).json()["data"]
    assert latest["quiz_score"] == 100.0
