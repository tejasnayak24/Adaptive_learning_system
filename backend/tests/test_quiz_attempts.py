"""Server-side quiz attempts and the two-strike tab-switch rule.

The server clock is controlled (``clock`` fixture), so every timing rule
is tested exactly: 10 s grace measured by the browser, 2 s delivery
allowance on the server side, unverified absences, reloads, cooldown.
"""

from datetime import datetime, timedelta

import pytest

from app.models.progress import Progress
from app.models.quiz_attempt import QuizAttempt, QuizAttemptEvent
from app.models.recommendation import RecommendationHistory
from app.models.reward import RewardHistory
from app.services import quiz_attempt_service as qa
from conftest import heartbeat, register_and_login, start_monitoring

PAGE_A = "page-aaaaaaaa"
PAGE_B = "page-bbbbbbbb"


class Clock:
    def __init__(self):
        self.now = datetime(2026, 11, 14, 10, 0, 0)

    def advance(self, seconds):
        self.now += timedelta(seconds=seconds)


@pytest.fixture()
def clock(monkeypatch):
    c = Clock()
    monkeypatch.setattr(qa, "_utcnow", lambda: c.now)
    return c


def _start(client, headers, quiz_id, **extra):
    return client.post("/quiz/start", json={"quiz_id": quiz_id, **extra}, headers=headers)


def _attempt(client, headers, quiz_id, **extra):
    response = _start(client, headers, quiz_id, **extra)
    assert response.status_code == 200, response.text
    return response.json()["data"]


def _events(client, headers, attempt_id, page, *events):
    response = client.post(
        f"/quiz/attempts/{attempt_id}/events",
        json={"page_id": page, "events": list(events)},
        headers=headers,
    )
    assert response.status_code == 200, response.text
    return response.json()["data"]


def _state(client, headers, attempt_id):
    response = client.get(f"/quiz/attempts/{attempt_id}", headers=headers)
    assert response.status_code == 200, response.text
    return response.json()["data"]


def _all_answers(data, letter="A"):
    return {str(q["id"]): letter for q in data["questions"]}


def _submit(client, headers, quiz_id, answers, monitoring, **extra):
    heartbeat(client, monitoring, attention_score=0.8)
    body = {
        "quiz_id": quiz_id,
        "monitoring_session_id": monitoring["session_id"],
        "answers": answers,
        "response_time": 30,
        **extra,
    }
    return client.post("/quiz/submit", json=body, headers=headers)


@pytest.fixture()
def quiz(client, auth, lesson_with_quiz, clock):
    headers, profile = auth
    return {"headers": headers, "profile": profile, "quiz_id": lesson_with_quiz["quiz_id"]}


def _new_attempt(client, quiz):
    data = _attempt(client, quiz["headers"], quiz["quiz_id"])
    return data, data["attempt"]["id"]


# ---------------------------------------------------------------- start / resume / answers


def test_start_creates_attempt_and_resume_returns_it(client, quiz, clock):
    data, attempt_id = _new_attempt(client, quiz)
    attempt = data["attempt"]
    assert attempt["status"] == "in_progress" and attempt["strikes"] == 0
    assert attempt["protected"] is True and attempt["graded"] is False
    assert attempt["grace_seconds"] == 10.0
    assert data["resumed"] is False
    assert all("correct_answer" not in q for q in data["questions"])

    again = _attempt(client, quiz["headers"], quiz["quiz_id"])
    assert again["attempt"]["id"] == attempt_id
    assert again["resumed"] is True


def test_answers_are_saved_validated_and_restored(client, quiz, clock):
    data, attempt_id = _new_attempt(client, quiz)
    first = str(data["questions"][0]["id"])
    url = f"/quiz/attempts/{attempt_id}/answers"
    headers = quiz["headers"]

    saved = client.put(url, json={"answers": {first: "b"}, "draft_state": {"current": 1}}, headers=headers)
    assert saved.status_code == 200
    assert saved.json()["data"]["answers"] == {first: "B"}

    assert client.put(url, json={"answers": {"999999": "A"}}, headers=headers).status_code == 422
    assert client.put(url, json={"answers": {first: "E"}}, headers=headers).status_code == 422

    resumed = _attempt(client, headers, quiz["quiz_id"])["attempt"]
    assert resumed["answers"] == {first: "B"}
    assert resumed["draft_state"] == {"current": 1}


# ---------------------------------------------------------------- first incident


def test_return_within_grace_gives_one_strike_and_warning(client, quiz, clock):
    _, attempt_id = _new_attempt(client, quiz)
    h = quiz["headers"]
    state = _events(client, h, attempt_id, PAGE_A, {"seq": 1, "kind": "hidden"})
    assert state["status"] == "away"

    clock.advance(11.9)  # 9.9 s away + 2 s for the report to arrive
    state = _events(client, h, attempt_id, PAGE_A, {"seq": 2, "kind": "visible", "hidden_ms": 9900})
    assert state["status"] == "in_progress"
    assert state["strikes"] == 1 and state["warning"] is True


def test_more_than_ten_seconds_by_browser_clock_terminates(client, quiz, clock):
    _, attempt_id = _new_attempt(client, quiz)
    h = quiz["headers"]
    _events(client, h, attempt_id, PAGE_A, {"seq": 1, "kind": "hidden"})
    clock.advance(10.2)
    state = _events(client, h, attempt_id, PAGE_A, {"seq": 2, "kind": "visible", "hidden_ms": 10100})
    assert state["status"] == "terminated"
    assert state["end_reason"] == "grace_expired"
    assert state["graded"] is False


def test_delivery_allowance_never_adds_grace_time(client, quiz, clock):
    """A prompt report arriving after 10 + 2 s is not accepted, even if the browser says 9 s."""
    _, attempt_id = _new_attempt(client, quiz)
    h = quiz["headers"]
    _events(client, h, attempt_id, PAGE_A, {"seq": 1, "kind": "hidden"})
    clock.advance(12.5)
    state = _events(
        client, h, attempt_id, PAGE_A,
        {"seq": 2, "kind": "visible", "hidden_ms": 9000, "delivery_failures": 0, "queued_ms": 0},
    )
    assert state["status"] == "terminated" and state["end_reason"] == "grace_expired"


def test_hidden_heartbeats_terminate_while_still_away(client, quiz, clock):
    """Throttled timers cannot help: the still-hidden page reports its own measurement."""
    _, attempt_id = _new_attempt(client, quiz)
    h = quiz["headers"]
    _events(client, h, attempt_id, PAGE_A, {"seq": 1, "kind": "hidden"})
    clock.advance(4)
    assert _events(client, h, attempt_id, PAGE_A, {"seq": 2, "kind": "hidden_tick", "hidden_ms": 4000})["status"] == "away"
    clock.advance(6.6)
    state = _events(client, h, attempt_id, PAGE_A, {"seq": 3, "kind": "hidden_tick", "hidden_ms": 10600})
    assert state["status"] == "terminated" and state["end_reason"] == "grace_expired"


# ---------------------------------------------------------------- second incident


def test_second_switch_terminates_immediately(client, quiz, clock):
    _, attempt_id = _new_attempt(client, quiz)
    h = quiz["headers"]
    _events(client, h, attempt_id, PAGE_A, {"seq": 1, "kind": "hidden"})
    clock.advance(3)
    _events(client, h, attempt_id, PAGE_A, {"seq": 2, "kind": "visible", "hidden_ms": 3000})
    clock.advance(60)
    state = _events(client, h, attempt_id, PAGE_A, {"seq": 3, "kind": "hidden"})
    assert state["status"] == "terminated"
    assert state["end_reason"] == "second_tab_switch"
    assert state["strikes"] == 2


def test_lost_hidden_report_is_recovered_from_the_return(client, quiz, clock):
    _, attempt_id = _new_attempt(client, quiz)
    h = quiz["headers"]
    state = _events(client, h, attempt_id, PAGE_A, {"seq": 2, "kind": "visible", "hidden_ms": 3000})
    assert state["strikes"] == 1 and state["status"] == "in_progress"
    state = _events(client, h, attempt_id, PAGE_A, {"seq": 4, "kind": "visible", "hidden_ms": 2000})
    assert state["status"] == "terminated" and state["end_reason"] == "second_tab_switch"


# ---------------------------------------------------------------- network and unverified


def test_no_report_after_grace_locks_attempt_as_unverified_not_violation(client, quiz, clock):
    data, attempt_id = _new_attempt(client, quiz)
    h = quiz["headers"]
    _events(client, h, attempt_id, PAGE_A, {"seq": 1, "kind": "hidden"})
    clock.advance(13)
    state = _state(client, h, attempt_id)
    assert state["status"] == "unverified"
    assert state["end_reason"] is None and state["strikes"] == 0

    # Locked: cannot be submitted, but answers are still saved.
    monitoring = start_monitoring(client, h)
    response = _submit(client, h, quiz["quiz_id"], _all_answers(data), monitoring)
    assert response.status_code == 409
    assert client.put(
        f"/quiz/attempts/{attempt_id}/answers", json={"answers": _all_answers(data)}, headers=h
    ).status_code == 200


def test_network_delayed_return_is_not_a_violation(client, quiz, clock):
    _, attempt_id = _new_attempt(client, quiz)
    h = quiz["headers"]
    _events(client, h, attempt_id, PAGE_A, {"seq": 1, "kind": "hidden"})
    clock.advance(45)  # the report could not be delivered for a while
    assert _state(client, h, attempt_id)["status"] == "unverified"
    state = _events(
        client, h, attempt_id, PAGE_A,
        {"seq": 2, "kind": "visible", "hidden_ms": 5000, "delivery_failures": 3, "queued_ms": 40000},
    )
    assert state["status"] == "in_progress" and state["strikes"] == 1
    assert state["end_reason"] is None


def test_unverified_absence_without_measurement_is_abandoned_not_terminated(client, quiz, clock):
    _, attempt_id = _new_attempt(client, quiz)
    h = quiz["headers"]
    _events(client, h, attempt_id, PAGE_A, {"seq": 1, "kind": "pagehide"})
    clock.advance(120)
    # The tab was closed and the quiz opened again in a new tab: no measurement.
    resumed = _attempt(client, h, quiz["quiz_id"])["attempt"]
    assert resumed["id"] == attempt_id and resumed["status"] == "unverified"
    state = _events(client, h, attempt_id, PAGE_B, {"seq": 1, "kind": "resume"})
    assert state["status"] == "abandoned"
    assert state["end_reason"] == "unverified_no_measurement"
    assert state["strikes"] == 0


def test_attempt_without_any_contact_is_abandoned(client, quiz, clock):
    _, attempt_id = _new_attempt(client, quiz)
    clock.advance(31 * 60)
    state = _state(client, quiz["headers"], attempt_id)
    assert state["status"] == "abandoned" and state["end_reason"] == "no_contact"


# ---------------------------------------------------------------- reload
# A confirmed reload (the browser's prompt accepted -> pagehide) is a
# tab-switch incident. A cancelled reload sends nothing.


def test_confirmed_reload_is_the_first_incident_and_keeps_the_attempt(client, quiz, db_session, clock):
    data, attempt_id = _new_attempt(client, quiz)
    h = quiz["headers"]
    first = str(data["questions"][0]["id"])
    client.put(f"/quiz/attempts/{attempt_id}/answers", json={"answers": {first: "B"}}, headers=h)

    assert _events(client, h, attempt_id, PAGE_A, {"seq": 1, "kind": "pagehide"})["status"] == "away"
    clock.advance(1.5)
    resumed = _attempt(client, h, quiz["quiz_id"])
    assert resumed["attempt"]["id"] == attempt_id
    assert resumed["attempt"]["answers"] == {first: "B"}
    state = _events(client, h, attempt_id, PAGE_B, {"seq": 1, "kind": "resume", "reload": True, "hidden_ms": 1400})
    assert state["status"] == "in_progress"
    assert state["strikes"] == 1 and state["warning"] is True
    outcomes = [e.outcome for e in db_session.query(QuizAttemptEvent).filter_by(attempt_id=attempt_id).order_by(QuizAttemptEvent.id)]
    assert outcomes == ["grace_started", "reload_strike"]


def test_confirmed_reload_after_strike_terminates_immediately(client, quiz, clock):
    data, attempt_id = _new_attempt(client, quiz)
    h = quiz["headers"]
    first = str(data["questions"][0]["id"])
    client.put(f"/quiz/attempts/{attempt_id}/answers", json={"answers": {first: "C"}}, headers=h)
    _events(client, h, attempt_id, PAGE_A, {"seq": 1, "kind": "hidden"})
    clock.advance(2)
    _events(client, h, attempt_id, PAGE_A, {"seq": 2, "kind": "visible", "hidden_ms": 2000})
    clock.advance(30)

    state = _events(client, h, attempt_id, PAGE_A, {"seq": 3, "kind": "pagehide"})
    assert state["status"] == "terminated"
    assert state["end_reason"] == "second_tab_switch"
    assert state["strikes"] == 2
    assert state["answers"] == {first: "C"}  # preserved
    # The reloaded page finds the ended attempt; a new one waits for the cooldown.
    blocked = _start(client, h, quiz["quiz_id"])
    assert blocked.status_code == 429
    assert blocked.json()["detail"]["previous_attempt"]["end_reason"] == "second_tab_switch"


def test_cancelled_reload_is_not_an_incident(client, quiz, clock):
    """Cancelling the browser's prompt sends no event: nothing changes."""
    _, attempt_id = _new_attempt(client, quiz)
    h = quiz["headers"]
    _events(client, h, attempt_id, PAGE_A, {"seq": 1, "kind": "visible", "hidden_ms": 1000})  # strike 1
    clock.advance(20)
    state = _state(client, h, attempt_id)
    assert state["status"] == "in_progress" and state["strikes"] == 1


def test_reload_strike_history_survives_several_reload_pages(client, quiz, clock):
    _, attempt_id = _new_attempt(client, quiz)
    h = quiz["headers"]
    _events(client, h, attempt_id, PAGE_A, {"seq": 1, "kind": "pagehide"})
    clock.advance(1)
    _events(client, h, attempt_id, PAGE_B, {"seq": 1, "kind": "resume", "reload": True, "hidden_ms": 900})
    clock.advance(40)
    # The reloaded page (B) is reloaded again: second incident.
    state = _events(client, h, attempt_id, PAGE_B, {"seq": 2, "kind": "pagehide"})
    assert state["status"] == "terminated" and state["end_reason"] == "second_tab_switch"


def test_slow_reload_follows_the_ten_second_rule(client, quiz, clock):
    _, attempt_id = _new_attempt(client, quiz)
    h = quiz["headers"]
    _events(client, h, attempt_id, PAGE_A, {"seq": 1, "kind": "pagehide"})
    clock.advance(16)
    state = _events(client, h, attempt_id, PAGE_B, {"seq": 1, "kind": "resume", "reload": True, "hidden_ms": 15500})
    assert state["status"] == "terminated" and state["end_reason"] == "grace_expired"


def test_reload_delayed_by_the_network_is_a_warning_not_a_termination(client, quiz, clock):
    _, attempt_id = _new_attempt(client, quiz)
    h = quiz["headers"]
    _events(client, h, attempt_id, PAGE_A, {"seq": 1, "kind": "pagehide"})
    clock.advance(30)
    state = _events(
        client, h, attempt_id, PAGE_B,
        {"seq": 1, "kind": "resume", "reload": True, "hidden_ms": 2500, "delivery_failures": 4},
    )
    assert state["status"] == "in_progress" and state["strikes"] == 1


# ---------------------------------------------------------------- diagnostics and duplicates


def test_blur_focus_and_network_events_never_strike(client, quiz, db_session, clock):
    _, attempt_id = _new_attempt(client, quiz)
    h = quiz["headers"]
    state = _events(
        client, h, attempt_id, PAGE_A,
        {"seq": 1, "kind": "blur"},  # e.g. the camera agent's preview window
        {"seq": 2, "kind": "focus"},
        {"seq": 3, "kind": "offline"},
        {"seq": 4, "kind": "online"},
    )
    assert state["status"] == "in_progress" and state["strikes"] == 0
    outcomes = {e.outcome for e in db_session.query(QuizAttemptEvent).filter_by(attempt_id=attempt_id)}
    assert outcomes == {"diagnostic"}


def test_duplicate_and_replayed_events_are_ignored(client, quiz, db_session, clock):
    _, attempt_id = _new_attempt(client, quiz)
    h = quiz["headers"]
    _events(client, h, attempt_id, PAGE_A, {"seq": 1, "kind": "hidden"})
    clock.advance(2)
    _events(client, h, attempt_id, PAGE_A, {"seq": 2, "kind": "visible", "hidden_ms": 2000})
    # A retry of the same batch must not become a second switch.
    state = _events(
        client, h, attempt_id, PAGE_A,
        {"seq": 1, "kind": "hidden"},
        {"seq": 2, "kind": "visible", "hidden_ms": 2000},
    )
    assert state["status"] == "in_progress" and state["strikes"] == 1
    assert db_session.query(QuizAttemptEvent).filter_by(attempt_id=attempt_id, page_id=PAGE_A).count() == 2


def test_event_outcomes_record_network_delay(client, quiz, db_session, clock):
    _, attempt_id = _new_attempt(client, quiz)
    h = quiz["headers"]
    _events(client, h, attempt_id, PAGE_A, {"seq": 1, "kind": "hidden"})
    clock.advance(20)
    _events(client, h, attempt_id, PAGE_A, {"seq": 2, "kind": "visible", "hidden_ms": 4000, "delivery_failures": 2})
    rows = db_session.query(QuizAttemptEvent).filter_by(attempt_id=attempt_id).order_by(QuizAttemptEvent.id).all()
    assert [(r.kind, r.outcome) for r in rows] == [
        ("hidden", "grace_started"),
        ("deadline_passed", "unverified"),
        ("visible", "strike_network_delayed"),
    ]


# ---------------------------------------------------------------- submission, grading, cooldown


def test_terminated_attempt_is_ungraded_and_counts_nowhere(client, quiz, db_session, clock):
    data, attempt_id = _new_attempt(client, quiz)
    h = quiz["headers"]
    answers = _all_answers(data, "B")
    client.put(f"/quiz/attempts/{attempt_id}/answers", json={"answers": answers}, headers=h)
    _events(client, h, attempt_id, PAGE_A, {"seq": 1, "kind": "hidden"})
    clock.advance(11)
    _events(client, h, attempt_id, PAGE_A, {"seq": 2, "kind": "hidden_tick", "hidden_ms": 11000})

    monitoring = start_monitoring(client, h)
    response = _submit(client, h, quiz["quiz_id"], answers, monitoring, attempt_id=attempt_id)
    assert response.status_code == 409

    # Answers preserved, frozen; nothing graded or recorded anywhere.
    attempt = db_session.get(QuizAttempt, attempt_id)
    assert attempt.answers == answers and attempt.progress_id is None
    assert client.put(f"/quiz/attempts/{attempt_id}/answers", json={"answers": {}}, headers=h).status_code == 409
    assert db_session.query(Progress).count() == 0
    assert db_session.query(RecommendationHistory).count() == 0
    assert db_session.query(RewardHistory).count() == 0
    summary = client.get("/analytics/summary", headers=h).json()["data"]
    assert summary["overview"]["quiz_attempts"] == 0
    assert summary["overview"]["lessons_completed"] == 0
    assert summary["overview"]["average_score"] is None


def test_cooldown_after_termination_then_new_attempt(client, quiz, clock):
    _, attempt_id = _new_attempt(client, quiz)
    h = quiz["headers"]
    _events(client, h, attempt_id, PAGE_A, {"seq": 1, "kind": "visible", "hidden_ms": 50000})

    clock.advance(60)
    blocked = _start(client, h, quiz["quiz_id"])
    assert blocked.status_code == 429
    assert blocked.headers["Retry-After"] == "240"
    assert blocked.json()["detail"]["retry_after_seconds"] == 240

    clock.advance(241)
    fresh = _attempt(client, h, quiz["quiz_id"])["attempt"]
    assert fresh["id"] != attempt_id and fresh["strikes"] == 0


def test_confirmed_departure_abandons_with_cooldown(client, quiz, clock):
    _, attempt_id = _new_attempt(client, quiz)
    h = quiz["headers"]
    state = client.post(f"/quiz/attempts/{attempt_id}/abandon", headers=h).json()["data"]
    assert state["status"] == "abandoned" and state["end_reason"] == "left_quiz"
    assert state["strikes"] == 0 and state["retry_after_seconds"] == 300
    assert _start(client, h, quiz["quiz_id"]).status_code == 429


def test_submission_marks_attempt_and_allows_immediate_retake(client, quiz, db_session, clock):
    data, attempt_id = _new_attempt(client, quiz)
    h = quiz["headers"]
    monitoring = start_monitoring(client, h)
    response = _submit(client, h, quiz["quiz_id"], _all_answers(data), monitoring, attempt_id=attempt_id)
    assert response.status_code == 200, response.text
    body = response.json()["data"]
    assert body["attempt"]["status"] == "submitted" and body["attempt"]["graded"] is True
    assert db_session.get(QuizAttempt, attempt_id).progress_id == body["progress"]["id"]

    again = _submit(client, h, quiz["quiz_id"], _all_answers(data), monitoring, attempt_id=attempt_id)
    assert again.status_code == 409
    retake = _attempt(client, h, quiz["quiz_id"])["attempt"]
    assert retake["id"] != attempt_id


def test_submit_requires_started_attempt_and_confirmed_return(client, quiz, clock):
    h = quiz["headers"]
    monitoring = start_monitoring(client, h)
    questions = client.get(f"/quiz/{quiz['quiz_id']}", headers=h).json()["data"]
    answers = _all_answers(questions)
    assert _submit(client, h, quiz["quiz_id"], answers, monitoring).status_code == 409

    _, attempt_id = _new_attempt(client, quiz)
    _events(client, h, attempt_id, PAGE_A, {"seq": 1, "kind": "hidden"})
    pending = _submit(client, h, quiz["quiz_id"], answers, monitoring)
    assert pending.status_code == 409
    assert "not been confirmed" in pending.json()["detail"]["message"]


def test_attempts_are_private(client, quiz, clock):
    _, attempt_id = _new_attempt(client, quiz)
    other, _ = register_and_login(client, email="other@example.com")
    assert client.get(f"/quiz/attempts/{attempt_id}", headers=other).status_code == 404
    assert client.put(f"/quiz/attempts/{attempt_id}/answers", json={"answers": {}}, headers=other).status_code == 404
    assert client.post(
        f"/quiz/attempts/{attempt_id}/events",
        json={"page_id": PAGE_A, "events": [{"seq": 1, "kind": "hidden"}]},
        headers=other,
    ).status_code == 404
    assert client.post(f"/quiz/attempts/{attempt_id}/abandon", headers=other).status_code == 404
    assert client.get(f"/quiz/attempts/{attempt_id}").status_code == 401
    # Unchanged by the other student's attempts.
    assert _state(client, quiz["headers"], attempt_id)["status"] == "in_progress"


def test_start_rejects_foreign_monitoring_session(client, quiz, clock):
    other, _ = register_and_login(client, email="other2@example.com")
    foreign = start_monitoring(client, other)
    response = _start(client, quiz["headers"], quiz["quiz_id"], monitoring_session_id=foreign["session_id"])
    assert response.status_code == 403


def test_unprotected_mode_records_but_never_terminates(client, quiz, monkeypatch, clock):
    """Hook for an explicitly ungraded practice mode (none exists yet)."""
    monkeypatch.setattr(qa, "PROTECTED_MODES", frozenset({"standard"}))
    attempt = _attempt(client, quiz["headers"], quiz["quiz_id"], mode="practice")["attempt"]
    assert attempt["protected"] is False
    state = _events(client, quiz["headers"], attempt["id"], PAGE_A, {"seq": 1, "kind": "visible", "hidden_ms": 60000})
    assert state["status"] == "in_progress" and state["strikes"] == 0


def test_event_payload_is_validated(client, quiz, clock):
    _, attempt_id = _new_attempt(client, quiz)
    url = f"/quiz/attempts/{attempt_id}/events"
    h = quiz["headers"]
    assert client.post(url, json={"page_id": "x", "events": [{"seq": 1, "kind": "hidden"}]}, headers=h).status_code == 422
    assert client.post(url, json={"page_id": PAGE_A, "events": [{"seq": 1, "kind": "screenshot"}]}, headers=h).status_code == 422
    assert client.post(url, json={"page_id": PAGE_A, "events": []}, headers=h).status_code == 422


def test_concurrent_starts_resume_the_same_attempt(client, quiz, monkeypatch, clock):
    """Two simultaneous starts (StrictMode, two tabs): one attempt, no 500."""
    _, attempt_id = _new_attempt(client, quiz)
    real = qa._open_attempt
    calls = {"n": 0}

    def racing(db, student_id, quiz_id):
        # The first lookup misses the attempt the "other request" just created.
        calls["n"] += 1
        return None if calls["n"] == 1 else real(db, student_id, quiz_id)

    monkeypatch.setattr(qa, "_open_attempt", racing)
    again = _start(client, quiz["headers"], quiz["quiz_id"])
    assert again.status_code == 200, again.text
    assert again.json()["data"]["attempt"]["id"] == attempt_id
    assert again.json()["data"]["resumed"] is True
