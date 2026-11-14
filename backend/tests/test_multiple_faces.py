"""Multiple-face episodes recorded from the camera agent's heartbeats."""

from datetime import datetime, timedelta

from conftest import heartbeat, start_monitoring

from app.models.session_event import SessionEvent
from app.services import monitoring_service as ms


def _episodes(db_session, session_id):
    return (
        db_session.query(SessionEvent)
        .filter_by(monitoring_session_id=session_id)
        .order_by(SessionEvent.id)
        .all()
    )


def test_sustained_signal_opens_one_episode_and_clearing_closes_it(client, auth, db_session):
    headers, _ = auth
    mon = start_monitoring(client, headers)
    heartbeat(client, mon, face_count=1, multiple_faces=False)
    view = heartbeat(client, mon, face_count=2, multiple_faces=True).json()["data"]
    assert view["multiple_faces"] is True
    heartbeat(client, mon, face_count=3, multiple_faces=True)
    heartbeat(client, mon, face_count=2, multiple_faces=True)
    view = heartbeat(client, mon, face_count=1, multiple_faces=False).json()["data"]
    assert view["multiple_faces"] is False

    [episode] = _episodes(db_session, mon["session_id"])
    assert episode.kind == "multiple_faces"
    assert episode.peak_count == 3
    assert episode.end_reason == "cleared"
    assert episode.ended_at >= episode.started_at


def test_status_shows_the_live_signal_to_the_browser(client, auth):
    headers, _ = auth
    mon = start_monitoring(client, headers)
    heartbeat(client, mon, face_count=2, multiple_faces=True)
    status = client.get(f"/monitoring/sessions/{mon['session_id']}", headers=headers).json()["data"]
    assert status["multiple_faces"] is True
    # Learning is not locked by it: the student's own face is still verified.
    assert status["state"] == "verified"


def test_unmeasured_sample_ends_an_episode_as_not_measured(client, auth, db_session):
    headers, _ = auth
    mon = start_monitoring(client, headers)
    heartbeat(client, mon, face_count=2, multiple_faces=True)
    heartbeat(client, mon, face_count=None, multiple_faces=None)
    [episode] = _episodes(db_session, mon["session_id"])
    assert episode.end_reason == "not_measured"


def test_camera_failure_is_not_counted_as_multiple_faces(client, auth, db_session):
    headers, _ = auth
    mon = start_monitoring(client, headers)
    view = heartbeat(client, mon, camera_ok=False, face_detected=False, face_count=2, multiple_faces=True).json()["data"]
    assert view["multiple_faces"] is None
    assert _episodes(db_session, mon["session_id"]) == []


def test_stale_measurement_is_not_counted(client, auth, db_session):
    import time

    headers, _ = auth
    mon = start_monitoring(client, headers)
    heartbeat(client, mon, captured_at=time.time() - 600, face_count=2, multiple_faces=True)
    assert _episodes(db_session, mon["session_id"]) == []


def test_gap_in_heartbeats_closes_the_episode_at_the_last_one(client, auth, db_session, monkeypatch):
    headers, _ = auth
    mon = start_monitoring(client, headers)
    t0 = datetime.utcnow()
    clock = {"now": t0}
    monkeypatch.setattr(ms, "_utcnow", lambda: clock["now"])
    r = heartbeat(client, mon, face_count=2, multiple_faces=True)
    assert r.status_code == 200, r.text
    clock["now"] = t0 + timedelta(seconds=1)
    heartbeat(client, mon, face_count=2, multiple_faces=True)
    clock["now"] = t0 + timedelta(seconds=40)  # agent was gone for a while
    heartbeat(client, mon, face_count=2, multiple_faces=True)

    first, second = _episodes(db_session, mon["session_id"])
    assert first.end_reason == "heartbeats_stopped"
    assert first.ended_at == t0 + timedelta(seconds=1)
    assert second.started_at == t0 + timedelta(seconds=40) and second.ended_at is None


def test_ending_the_session_closes_an_open_episode(client, auth, db_session):
    headers, _ = auth
    mon = start_monitoring(client, headers)
    heartbeat(client, mon, face_count=2, multiple_faces=True)
    client.post(f"/monitoring/sessions/{mon['session_id']}/end", headers=headers)
    [episode] = _episodes(db_session, mon["session_id"])
    assert episode.end_reason == "session_ended" and episode.ended_at is not None


def test_multiple_faces_never_changes_attention_or_quiz_records(client, auth, lesson_with_quiz):
    headers, _ = auth
    mon = start_monitoring(client, headers)
    quiz_id = lesson_with_quiz["quiz_id"]
    data = client.post("/quiz/start", json={"quiz_id": quiz_id}, headers=headers).json()["data"]
    heartbeat(client, mon, attention_score=0.8, face_count=2, multiple_faces=True)
    answers = {str(q["id"]): "A" for q in data["questions"]}
    result = client.post(
        "/quiz/submit",
        json={"quiz_id": quiz_id, "monitoring_session_id": mon["session_id"], "answers": answers, "response_time": 10},
        headers=headers,
    )
    assert result.status_code == 200, result.text
    body = result.json()["data"]
    assert body["progress"]["attention_score"] == 0.8
    assert body["attempt"]["status"] == "submitted"  # not terminated by it


def test_face_count_is_validated(client, auth):
    headers, _ = auth
    mon = start_monitoring(client, headers)
    assert heartbeat(client, mon, face_count=99).status_code == 422
    assert heartbeat(client, mon, face_count=-1).status_code == 422
