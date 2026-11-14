"""Session-integrity report: factual, own records only, no scores."""

import json
from datetime import datetime, timedelta

import pytest
from conftest import heartbeat, register_and_login, start_monitoring

from app.models.monitoring import MonitoringConsent
from app.services import monitoring_service as ms
from app.services import quiz_attempt_service as qa

PAGE = "page-report-aaaa"
PAGE2 = "page-report-bbbb"


class Clock:
    def __init__(self):
        self.now = datetime.utcnow()

    def advance(self, seconds):
        self.now += timedelta(seconds=seconds)


@pytest.fixture()
def clock(monkeypatch):
    c = Clock()
    monkeypatch.setattr(qa, "_utcnow", lambda: c.now)
    return c


def _start(client, headers, quiz_id):
    response = client.post("/quiz/start", json={"quiz_id": quiz_id}, headers=headers)
    assert response.status_code == 200, response.text
    return response.json()["data"]["attempt"]["id"]


def _ev(client, headers, attempt_id, page, *events):
    response = client.post(f"/quiz/attempts/{attempt_id}/events", json={"page_id": page, "events": list(events)}, headers=headers)
    assert response.status_code == 200, response.text


def _report(client, headers):
    response = client.get("/integrity/report", headers=headers)
    assert response.status_code == 200, response.text
    return response.json()["data"]


def test_report_lists_incidents_with_measured_times_and_outcomes(client, auth, lesson_with_quiz, clock):
    headers, _ = auth
    attempt_id = _start(client, headers, lesson_with_quiz["quiz_id"])
    _ev(client, headers, attempt_id, PAGE, {"seq": 1, "kind": "blur"}, {"seq": 2, "kind": "focus"})
    _ev(client, headers, attempt_id, PAGE, {"seq": 3, "kind": "hidden"})
    clock.advance(4)
    _ev(client, headers, attempt_id, PAGE, {"seq": 4, "kind": "visible", "hidden_ms": 3800})
    clock.advance(30)
    _ev(client, headers, attempt_id, PAGE, {"seq": 5, "kind": "hidden"})

    report = _report(client, headers)
    [attempt] = report["attempts"]
    assert attempt["status"] == "terminated" and attempt["graded"] is False
    assert attempt["tab_switch_incidents"] == 2
    first, second = attempt["incidents"]
    assert first["away_seconds"] == 3.8 and first["away_measured"] is True
    assert "warning given" in first["result"]
    assert second["away_seconds"] is None  # ended at once: no time away to measure
    assert "second time" in second["result"]
    assert attempt["window_focus_changes"] == 1
    assert report["totals"]["tab_switch_incidents"] == 2
    assert report["totals"]["attempts_terminated"] == 1


def test_report_shows_unverified_periods_and_network_delays(client, auth, lesson_with_quiz, clock):
    headers, _ = auth
    attempt_id = _start(client, headers, lesson_with_quiz["quiz_id"])
    _ev(client, headers, attempt_id, PAGE, {"seq": 1, "kind": "hidden"})
    clock.advance(30)
    client.get(f"/quiz/attempts/{attempt_id}", headers=headers)  # deadline passes -> unverified
    clock.advance(10)
    _ev(client, headers, attempt_id, PAGE, {"seq": 2, "kind": "visible", "hidden_ms": 4000, "delivery_failures": 5})

    [attempt] = _report(client, headers)["attempts"]
    [incident] = attempt["incidents"]
    assert incident["unverified"] is True
    assert "delayed by the network" in incident["result"]
    [period] = attempt["unverified_periods"]
    assert period["seconds"] == 10.0
    assert attempt["reports_delayed_by_network"] == 1
    assert attempt["status"] == "in_progress"


def test_reload_is_listed_but_not_counted_as_a_tab_switch(client, auth, lesson_with_quiz, clock):
    headers, _ = auth
    attempt_id = _start(client, headers, lesson_with_quiz["quiz_id"])
    _ev(client, headers, attempt_id, PAGE, {"seq": 1, "kind": "pagehide"})
    clock.advance(1)
    _ev(client, headers, attempt_id, PAGE2, {"seq": 1, "kind": "resume", "reload": True, "hidden_ms": 900})
    report = _report(client, headers)
    [attempt] = report["attempts"]
    assert attempt["tab_switch_incidents"] == 0
    assert attempt["incidents"][0]["kind"] == "page_reloaded"
    assert report["totals"]["reloads"] == 1


def test_report_includes_multiple_face_episodes_with_times(client, auth, lesson_with_quiz, monkeypatch):
    headers, _ = auth
    mon = start_monitoring(client, headers)
    attempt_id = _start(client, headers, lesson_with_quiz["quiz_id"])
    heartbeat(client, mon, face_count=2, multiple_faces=True)
    heartbeat(client, mon, face_count=1, multiple_faces=False)
    report = _report(client, headers)
    assert report["totals"]["multiple_face_episodes"] == 1
    [episode] = report["attempts"][0]["multiple_face_episodes"]
    assert episode["peak_face_count"] == 2 and episode["end_reason"] == "cleared"
    assert episode["started_at"].endswith("Z") and episode["seconds"] is not None
    [session] = report["sessions"]
    assert session["monitoring_session_id"] == mon["session_id"]
    assert report["attempts"][0]["attempt_id"] == attempt_id


def test_report_is_factual_and_private(client, auth, lesson_with_quiz, clock):
    headers, _ = auth
    attempt_id = _start(client, headers, lesson_with_quiz["quiz_id"])
    _ev(client, headers, attempt_id, PAGE, {"seq": 1, "kind": "visible", "hidden_ms": 60000})

    other, _ = register_and_login(client, email="someone.else@example.com")
    assert _report(client, other)["attempts"] == []
    assert client.get("/integrity/report").status_code == 401

    text = json.dumps(_report(client, headers)).lower()
    for word in ("cheat", "probability", "suspicious", "misconduct score", "risk"):
        assert word not in text.replace("not proof of misconduct", "")


def test_consent_v1_must_be_given_again_for_the_new_monitoring(client, auth, db_session):
    headers, profile = auth
    db_session.add(
        MonitoringConsent(
            student_id=profile["id"], consent_version="2026-11-v1", is_minor=True,
            guardian_authorization_confirmed=True, school_authorization_confirmed=True,
        )
    )
    db_session.commit()
    view = client.get("/monitoring/consent", headers=headers).json()["data"]
    assert view["valid"] is False and view["required_version"] == ms.CONSENT_VERSION == "2026-11-v2"
    assert client.post("/monitoring/sessions", json={"lesson_id": None}, headers=headers).status_code == 403
