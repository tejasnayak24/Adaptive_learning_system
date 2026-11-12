from conftest import register_and_login


def _submit(client, headers, lesson_id, **overrides):
    body = {
        "lesson_id": lesson_id,
        "quiz_score": 80,
        "response_time": 42,
        "difficulty": "Easy",
    }
    body.update(overrides)
    return client.post("/quiz/submit", json=body, headers=headers)


def test_submission_without_telemetry_is_saved_as_null(client, auth, lesson_with_quiz):
    headers, profile = auth
    response = _submit(client, headers, lesson_with_quiz["lesson_id"])

    assert response.status_code == 200, response.text
    data = response.json()["data"]
    assert data["student_id"] == profile["id"]
    assert data["attention_score"] is None
    assert data["yawning"] is None
    assert data["looking_away"] is None
    assert data["telemetry_available"] is False


def test_submission_with_telemetry_is_saved(client, auth, lesson_with_quiz):
    headers, _ = auth
    response = _submit(
        client,
        headers,
        lesson_with_quiz["lesson_id"],
        attention_score=0.82,
        yawning=False,
        looking_away=True,
    )
    data = response.json()["data"]
    assert data["attention_score"] == 0.82
    assert data["looking_away"] is True
    assert data["telemetry_available"] is True


def test_difficulty_is_normalised_to_uppercase(client, auth, lesson_with_quiz):
    headers, _ = auth
    data = _submit(client, headers, lesson_with_quiz["lesson_id"], difficulty=" medium ").json()["data"]
    assert data["difficulty"] == "MEDIUM"


def test_invalid_difficulty_and_scores_rejected(client, auth, lesson_with_quiz):
    headers, _ = auth
    lesson_id = lesson_with_quiz["lesson_id"]
    assert _submit(client, headers, lesson_id, difficulty="MIXED").status_code == 422
    assert _submit(client, headers, lesson_id, quiz_score=140).status_code == 422
    assert _submit(client, headers, lesson_id, attention_score=1.5).status_code == 422


def test_submission_is_always_recorded_for_token_owner(client, auth, lesson_with_quiz):
    headers, profile = auth
    _, other = register_and_login(client, email="other@example.com")

    forged = _submit(client, headers, lesson_with_quiz["lesson_id"], student_id=other["id"])
    assert forged.status_code == 403

    same = _submit(client, headers, lesson_with_quiz["lesson_id"], student_id=profile["id"])
    assert same.status_code == 200


def test_submission_requires_auth_and_existing_lesson(client, auth, lesson_with_quiz):
    headers, _ = auth
    assert _submit(client, {}, lesson_with_quiz["lesson_id"]).status_code == 401
    assert _submit(client, headers, 99999).status_code == 404


def test_progress_is_owner_only(client, auth, lesson_with_quiz):
    headers, profile = auth
    _submit(client, headers, lesson_with_quiz["lesson_id"], attention_score=0.7, yawning=False, looking_away=False)

    own = client.get(f"/progress/{profile['id']}", headers=headers)
    assert own.status_code == 200
    rows = own.json()["data"]
    assert len(rows) == 1
    assert rows[0]["attention_score"] == 0.7

    other_headers, other = register_and_login(client, email="peer@example.com")
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
    _submit(client, headers, lesson_id, quiz_score=40)
    _submit(client, headers, lesson_id, quiz_score=95)

    latest = client.get(f"/progress/{profile['id']}/{lesson_id}", headers=headers).json()["data"]
    assert latest["quiz_score"] == 95
