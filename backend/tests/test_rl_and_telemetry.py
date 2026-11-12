from app.services import telemetry_service as telemetry

BASE_RL = {
    "subject": "Science",
    "topic": "Cell Biology",
    "lesson": "Cell Biology",
    "previous_quiz_score": 60,
    "current_quiz_score": 85,
    "difficulty": "easy",
    "response_time": 30.0,
    "hints_used": 0,
    "lesson_attempts": 1,
    "completed_lessons": 1,
}


def test_rl_reports_unavailable_without_telemetry(client, auth):
    headers, _ = auth
    response = client.post("/rl/recommend", json=BASE_RL, headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body["telemetry_available"] is False
    assert body["action"] is None
    assert body["confidence"] is None


def test_rl_partial_telemetry_is_still_unavailable(client, auth):
    headers, _ = auth
    body = client.post("/rl/recommend", json={**BASE_RL, "attention_score": 0.9}, headers=headers).json()
    assert body["telemetry_available"] is False


def test_rl_recommends_with_real_telemetry(client, auth):
    headers, _ = auth
    response = client.post(
        "/rl/recommend",
        json={**BASE_RL, "attention_score": 0.9, "yawning": False, "looking_away": False},
        headers=headers,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["telemetry_available"] is True
    assert isinstance(body["action"], str)
    assert 0.0 <= body["confidence"] <= 1.0
    assert body["policy"] in ("q_learning", "q_learning_nearest_state", "fallback")
    assert body["confidence_kind"] == "heuristic_decision_strength"
    assert body["state_key"] and len(body["state_key"]) == 8
    assert body["action"] not in body["blocked_actions"]


def test_rl_rejects_invalid_values(client, auth):
    headers, _ = auth
    bad = {**BASE_RL, "attention_score": 0.9, "yawning": False, "looking_away": False}
    assert client.post("/rl/recommend", json={**bad, "difficulty": "MIXED"}, headers=headers).status_code == 422
    assert client.post("/rl/recommend", json={**bad, "current_quiz_score": 101}, headers=headers).status_code == 422


def test_telemetry_without_data_is_unavailable():
    telemetry.clear_all()
    view = telemetry.get_telemetry(1, now=1000.0)
    assert view["available"] is False
    assert view["status"] == "no_data"
    assert view["attention_score"] is None
    assert view["session_average_attention"] is None


def test_stale_telemetry_is_never_reported_as_current():
    telemetry.clear_all()
    telemetry.update_telemetry(7, 0.9, False, False, now=1000.0)

    live = telemetry.get_telemetry(7, now=1002.0)
    assert live["available"] is True
    assert live["status"] == "live"
    assert live["attention_score"] == 0.9

    stale = telemetry.get_telemetry(7, now=1000.0 + telemetry.STALE_AFTER_SECONDS + 1)
    assert stale["available"] is False
    assert stale["status"] == "stale"
    assert stale["attention_score"] is None
    assert stale["session_average_attention"] is None
    assert stale["yawning_observed"] is None


def test_session_aggregates_and_reset():
    telemetry.clear_all()
    telemetry.update_telemetry(3, 0.6, False, False, now=10.0)
    telemetry.update_telemetry(3, 0.8, True, False, now=11.0)

    view = telemetry.get_telemetry(3, now=11.5)
    assert view["session_samples"] == 2
    assert view["session_average_attention"] == 0.7
    assert view["yawning_observed"] is True
    assert view["looking_away_observed"] is False

    telemetry.reset_telemetry(3)
    after = telemetry.get_telemetry(3, now=11.5)
    assert after["available"] is True  # camera still live after a quiz reset
    assert after["session_samples"] == 0
    assert after["session_average_attention"] is None
    assert after["yawning_observed"] is False


def test_telemetry_endpoints(client, auth):
    from conftest import heartbeat, start_monitoring

    headers, profile = auth
    sid = profile["id"]
    heartbeat(client, start_monitoring(client, headers), attention_score=0.75)
    body = client.get(f"/attention/{sid}", headers=headers).json()["data"]
    assert body["available"] is True
    assert body["attention_score"] == 0.75

    reset = client.post(f"/attention/{sid}/reset", headers=headers).json()["data"]
    assert reset["session_samples"] == 0
