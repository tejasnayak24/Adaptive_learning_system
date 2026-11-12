from conftest import heartbeat, register_and_login, start_monitoring

NEW_LESSON = {
    "title": "Photosynthesis",
    "topic": "Plants",
    "difficulty": "MIXED",
    "content": "Plants convert light energy into chemical energy.",
}


def _promote(db_session, student_id, role):
    from app.models.student import Student

    student = db_session.get(Student, student_id)
    student.role = role
    db_session.commit()


def test_new_accounts_are_students(client, auth):
    _, profile = auth
    assert profile["role"] == "student"


def test_students_cannot_modify_lessons(client, auth, lesson_with_quiz):
    headers, _ = auth
    lesson_id = lesson_with_quiz["lesson_id"]

    assert client.post("/lesson", json=NEW_LESSON, headers=headers).status_code == 403
    assert client.put(f"/lesson/{lesson_id}", json={"title": "X"}, headers=headers).status_code == 403
    assert client.delete(f"/lesson/{lesson_id}", headers=headers).status_code == 403
    assert client.post("/lesson", json=NEW_LESSON).status_code == 401

    # Curriculum is untouched. Lesson content now requires signing in.
    assert client.get(f"/lesson/{lesson_id}").status_code == 401
    assert client.get(f"/lesson/{lesson_id}", headers=headers).json()["data"]["title"] == "Cell Biology"


def test_teacher_can_manage_lessons_and_partial_update_keeps_fields(client, db_session, lesson_with_quiz):
    headers, profile = register_and_login(client, email="teacher@example.com")
    _promote(db_session, profile["id"], "teacher")

    created = client.post("/lesson", json=NEW_LESSON, headers=headers)
    assert created.status_code == 200
    lesson_id = created.json()["data"]["id"]

    updated = client.put(f"/lesson/{lesson_id}", json={"title": "Photosynthesis Basics"}, headers=headers)
    assert updated.status_code == 200
    body = updated.json()["data"]
    assert body["title"] == "Photosynthesis Basics"
    assert body["content"] == NEW_LESSON["content"]  # untouched by partial update

    assert client.delete(f"/lesson/{lesson_id}", headers=headers).status_code == 200


def test_telemetry_reads_are_owner_only(client, auth):
    headers, profile = auth
    sid = profile["id"]
    heartbeat(client, start_monitoring(client, headers), attention_score=0.6)

    assert client.get(f"/attention/{sid}", headers=headers).status_code == 200
    assert client.get(f"/attention/{sid}").status_code == 401

    other_headers, _ = register_and_login(client, email="spy@example.com")
    assert client.get(f"/attention/{sid}", headers=other_headers).status_code == 403
    assert client.post(f"/attention/{sid}/reset", headers=other_headers).status_code == 403


def test_unauthenticated_attention_post_was_removed(client):
    # The camera can no longer post telemetry for an arbitrary student id.
    response = client.post("/attention", json={"student_id": 1, "attention_score": 0.4})
    assert response.status_code == 404


def test_rl_endpoint_requires_auth_and_stub_route_removed(client):
    assert client.post("/rl/recommend", json={}).status_code == 401
    assert client.post("/recommend", json={}).status_code == 404
    assert client.get("/recommendations/latest").status_code == 401
