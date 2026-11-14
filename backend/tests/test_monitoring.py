"""Camera-monitoring sessions: consent, pairing, heartbeats, state, ownership."""

import json
import time
from datetime import datetime, timedelta

import pytest

from app.models.monitoring import MonitoringSession
from app.services import monitoring_service as ms
from app.services import telemetry_service
from conftest import heartbeat, register_and_login, start_monitoring

CONSENT_MINOR = {"accept": True, "guardian_authorization_confirmed": True, "school_authorization_confirmed": True}


def _status(client, headers, session_id):
    response = client.get(f"/monitoring/sessions/{session_id}", headers=headers)
    assert response.status_code == 200, response.text
    return response.json()["data"]


# -- consent ----------------------------------------------------------------


def test_session_requires_consent(client, auth):
    headers, _ = auth
    response = client.post("/monitoring/sessions", json={}, headers=headers)
    assert response.status_code == 403
    assert "consent" in response.json()["detail"].lower()


def test_minor_needs_guardian_and_school_authorisation(client, auth):
    headers, profile = auth
    assert profile["age"] == 14

    view = client.get("/monitoring/consent", headers=headers).json()["data"]
    assert view["is_minor"] is True and view["valid"] is False

    partial = {"accept": True, "guardian_authorization_confirmed": True}
    assert client.post("/monitoring/consent", json=partial, headers=headers).status_code == 400
    assert client.post("/monitoring/consent", json={**CONSENT_MINOR, "accept": False}, headers=headers).status_code == 400

    ok = client.post("/monitoring/consent", json=CONSENT_MINOR, headers=headers)
    assert ok.status_code == 200
    assert ok.json()["data"]["valid"] is True


def test_adult_consent_and_withdrawal_ends_sessions(client):
    headers, _ = register_and_login(client, email="adult@example.com", age=19)
    assert client.post("/monitoring/consent", json={"accept": True}, headers=headers).status_code == 200

    session_id = client.post("/monitoring/sessions", json={}, headers=headers).json()["data"]["session_id"]
    assert client.delete("/monitoring/consent", headers=headers).status_code == 200
    assert _status(client, headers, session_id)["state"] == "ended"
    assert client.post("/monitoring/sessions", json={}, headers=headers).status_code == 403


# -- pairing -------------------------------------------------------------------


def test_pairing_token_is_single_use_and_hashed(client, auth, db_session):
    headers, _ = auth
    client.post("/monitoring/consent", json=CONSENT_MINOR, headers=headers)
    created = client.post("/monitoring/sessions", json={}, headers=headers).json()["data"]
    session_id, token = created["session_id"], created["pairing_token"]
    assert created["state"] == "awaiting_agent"

    stored = db_session.get(MonitoringSession, session_id)
    assert stored.pairing_token_hash != token and len(stored.pairing_token_hash) == 64

    first = client.post(f"/monitoring/sessions/{session_id}/claim", json={"pairing_token": token})
    assert first.status_code == 200
    agent_token = first.json()["data"]["agent_token"]
    assert agent_token != token

    db_session.refresh(stored)
    assert stored.pairing_token_hash is None
    assert stored.agent_token_hash != agent_token

    again = client.post(f"/monitoring/sessions/{session_id}/claim", json={"pairing_token": token})
    assert again.status_code == 401


def test_wrong_or_expired_pairing_token_rejected(client, auth, db_session):
    headers, _ = auth
    client.post("/monitoring/consent", json=CONSENT_MINOR, headers=headers)
    created = client.post("/monitoring/sessions", json={}, headers=headers).json()["data"]
    session_id = created["session_id"]

    wrong = client.post(f"/monitoring/sessions/{session_id}/claim", json={"pairing_token": "x" * 43})
    assert wrong.status_code == 401

    stored = db_session.get(MonitoringSession, session_id)
    stored.pairing_expires_at = datetime.utcnow() - timedelta(seconds=1)
    db_session.commit()
    expired = client.post(f"/monitoring/sessions/{session_id}/claim", json={"pairing_token": created["pairing_token"]})
    assert expired.status_code == 401


def test_heartbeat_requires_valid_agent_token(client):
    body = {"sequence": 1, "camera_ok": True}
    assert client.post("/monitoring/heartbeat", json=body).status_code == 401
    bad = client.post("/monitoring/heartbeat", json=body, headers={"Authorization": "Bearer nope"})
    assert bad.status_code == 401


def test_agent_cannot_choose_student_identity(client, auth):
    headers, profile = auth
    monitoring = start_monitoring(client, headers)
    other_headers, other = register_and_login(client, email="victim@example.com")

    # A student_id in the heartbeat is ignored; telemetry goes to the token's student.
    assert heartbeat(client, monitoring, student_id=other["id"], attention_score=0.33).status_code == 200
    mine = client.get(f"/attention/{profile['id']}", headers=headers).json()["data"]
    theirs = client.get(f"/attention/{other['id']}", headers=other_headers).json()["data"]
    assert mine["attention_score"] == 0.33
    assert theirs["status"] == "no_data"


# -- states ------------------------------------------------------------------


def test_status_transitions(client, auth):
    headers, _ = auth
    monitoring = start_monitoring(client, headers)
    sid = monitoring["session_id"]

    assert _status(client, headers, sid)["state"] == "stale"  # paired, no heartbeat yet

    heartbeat(client, monitoring, camera_ok=False, camera_error="blocked_by_privacy_settings",
              face_detected=False, attention_score=None, captured_at=None)
    status = _status(client, headers, sid)
    assert status["state"] == "camera_unavailable"
    assert status["camera_error"] == "blocked_by_privacy_settings"
    assert status["attention_score"] is None

    heartbeat(client, monitoring, face_detected=False, face_stable=False, attention_score=None)
    assert _status(client, headers, sid)["state"] == "no_face"

    heartbeat(client, monitoring, face_stable=False)
    assert _status(client, headers, sid)["state"] == "verifying"

    heartbeat(client, monitoring)
    status = _status(client, headers, sid)
    assert status["state"] == "verified" and status["verified"] is True


def test_stale_heartbeats_are_never_verified(client, auth, monkeypatch):
    headers, _ = auth
    monitoring = start_monitoring(client, headers)
    heartbeat(client, monitoring)
    assert _status(client, headers, monitoring["session_id"])["verified"] is True

    later = time.time() + telemetry_service.STALE_AFTER_SECONDS + 1
    monkeypatch.setattr(telemetry_service, "_now", lambda: later)
    status = _status(client, headers, monitoring["session_id"])
    assert status["state"] == "stale"
    assert status["verified"] is False
    assert status["attention_score"] is None


def test_old_measurement_in_new_heartbeat_is_not_live(client, auth):
    headers, _ = auth
    monitoring = start_monitoring(client, headers)
    heartbeat(client, monitoring, captured_at=time.time() - 30)
    status = _status(client, headers, monitoring["session_id"])
    assert status["state"] == "camera_unavailable"
    assert status["camera_error"] == "stale_measurement"


def test_replayed_heartbeat_rejected(client, auth):
    headers, _ = auth
    monitoring = start_monitoring(client, headers)
    assert heartbeat(client, monitoring).status_code == 200
    monitoring["sequence"][0] -= 1
    assert heartbeat(client, monitoring).status_code == 409


# -- ownership, reconnection, ending --------------------------------------------


def test_sessions_are_owner_only(client, auth):
    headers, _ = auth
    monitoring = start_monitoring(client, headers)
    other_headers, _ = register_and_login(client, email="intruder@example.com")
    sid = monitoring["session_id"]

    assert client.get(f"/monitoring/sessions/{sid}", headers=other_headers).status_code == 403
    assert client.post(f"/monitoring/sessions/{sid}/end", headers=other_headers).status_code == 403
    assert client.post(f"/monitoring/sessions/{sid}/pairing", headers=other_headers).status_code == 403
    assert client.get(f"/monitoring/sessions/{sid}").status_code == 401


def test_reconnect_reuses_session_and_revokes_old_agent_token(client, auth):
    headers, _ = auth
    monitoring = start_monitoring(client, headers)
    sid = monitoring["session_id"]
    heartbeat(client, monitoring)

    reissued = client.post(f"/monitoring/sessions/{sid}/pairing", headers=headers)
    assert reissued.status_code == 200
    data = reissued.json()["data"]
    assert data["session_id"] == sid and data["state"] == "awaiting_agent"

    assert heartbeat(client, monitoring).status_code == 401  # old agent token revoked

    claimed = client.post(f"/monitoring/sessions/{sid}/claim", json={"pairing_token": data["pairing_token"]})
    assert claimed.status_code == 200
    monitoring["agent_headers"] = {"Authorization": f"Bearer {claimed.json()['data']['agent_token']}"}
    monitoring["sequence"][0] = 0
    assert heartbeat(client, monitoring).status_code == 200
    assert _status(client, headers, sid)["verified"] is True


def test_student_ending_session_stops_agent(client, auth):
    headers, _ = auth
    monitoring = start_monitoring(client, headers)
    assert client.post(f"/monitoring/sessions/{monitoring['session_id']}/end", headers=headers).status_code == 200
    assert heartbeat(client, monitoring).status_code == 401
    assert _status(client, headers, monitoring["session_id"])["state"] == "ended"


def test_new_session_replaces_previous(client, auth):
    headers, _ = auth
    first = start_monitoring(client, headers)
    second = client.post("/monitoring/sessions", json={}, headers=headers).json()["data"]
    assert second["session_id"] != first["session_id"]
    assert _status(client, headers, first["session_id"])["end_reason"] == "replaced_by_new_session"
    assert heartbeat(client, first).status_code == 401


def test_abandoned_session_expires_and_agent_is_told(client, auth, db_session):
    headers, _ = auth
    monitoring = start_monitoring(client, headers)
    stored = db_session.get(MonitoringSession, monitoring["session_id"])
    stored.last_client_seen_at = datetime.utcnow() - timedelta(seconds=ms.CLIENT_TIMEOUT_SECONDS + 5)
    db_session.commit()

    assert heartbeat(client, monitoring).status_code == 410
    db_session.refresh(stored)
    assert stored.status == "ended" and stored.end_reason == "client_inactive"


def test_agent_shutdown_returns_session_to_awaiting(client, auth):
    headers, _ = auth
    monitoring = start_monitoring(client, headers)
    response = client.post("/monitoring/agent/end", json={"reason": "agent_shutdown"}, headers=monitoring["agent_headers"])
    assert response.status_code == 200
    assert _status(client, headers, monitoring["session_id"])["state"] == "awaiting_agent"


# -- quiz submission enforcement -------------------------------------------------


def _answers(client, headers, quiz_id):
    questions = client.post("/quiz/start", json={"quiz_id": quiz_id}, headers=headers).json()["data"]["questions"]
    return {str(q["id"]): "A" for q in questions}


def test_quiz_requires_owned_open_monitoring_session(client, auth, lesson_with_quiz):
    headers, _ = auth
    quiz_id = lesson_with_quiz["quiz_id"]
    body = {"quiz_id": quiz_id, "answers": _answers(client, headers, quiz_id), "response_time": 10}

    assert client.post("/quiz/submit", json=body, headers=headers).status_code == 422  # field required

    other_headers, _ = register_and_login(client, email="owner@example.com")
    foreign = start_monitoring(client, other_headers)
    response = client.post("/quiz/submit", json={**body, "monitoring_session_id": foreign["session_id"]}, headers=headers)
    assert response.status_code == 403

    mine = start_monitoring(client, headers)
    client.post(f"/monitoring/sessions/{mine['session_id']}/end", headers=headers)
    ended = client.post("/quiz/submit", json={**body, "monitoring_session_id": mine["session_id"]}, headers=headers)
    assert ended.status_code == 409


def test_quiz_uses_server_telemetry_and_ignores_client_values(client, auth, lesson_with_quiz, db_session):
    from app.models.recommendation import RecommendationHistory

    headers, profile = auth
    quiz_id = lesson_with_quiz["quiz_id"]
    monitoring = start_monitoring(client, headers)
    client.post(f"/attention/{profile['id']}/reset", headers=headers)

    heartbeat(client, monitoring, attention_score=0.6)
    heartbeat(client, monitoring, attention_score=0.7, possible_drowsiness=True)
    heartbeat(client, monitoring, face_detected=False, attention_score=None)  # absent, not averaged

    body = {
        "quiz_id": quiz_id,
        "monitoring_session_id": monitoring["session_id"],
        "answers": _answers(client, headers, quiz_id),
        "response_time": 10,
        # Forged camera values from the browser are ignored:
        "attention_score": 1.0,
        "drowsy": False,
    }
    data = client.post("/quiz/submit", json=body, headers=headers).json()["data"]
    progress = data["progress"]
    assert progress["attention_score"] == pytest.approx(0.65)
    assert progress["drowsy"] is True
    assert progress["monitoring_session_id"] == monitoring["session_id"]

    rec = db_session.get(RecommendationHistory, data["recommendation"]["id"])
    assert json.loads(rec.state)["drowsy"] is True


def test_tokens_never_appear_in_status_or_urls(client, auth):
    headers, _ = auth
    monitoring = start_monitoring(client, headers)
    status = json.dumps(_status(client, headers, monitoring["session_id"]))
    assert monitoring["pairing_token"] not in status
    assert monitoring["agent_headers"]["Authorization"].split()[1] not in status
