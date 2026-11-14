"""Session-integrity report: a factual activity summary for one student.

Built only from the student's own records:

* quiz attempts and the page events reported for them (tab-switch rule);
* multiple-face episodes recorded from the camera agent's heartbeats.

The report lists what was measured, when, and how precisely. It contains
no score, probability or verdict: a hidden tab or a second face is not
evidence of misconduct, and the wording says so.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from app.models.lesson import Lesson
from app.models.monitoring import MonitoringSession
from app.models.quiz import Quiz
from app.models.quiz_attempt import ABANDONED, AWAY, SUBMITTED, TERMINATED, UNVERIFIED, QuizAttempt, QuizAttemptEvent
from app.models.session_event import MULTIPLE_FACES, SessionEvent
from app.models.student import Student

END_LABELS = {
    "submitted": "Submitted and graded",
    "grace_expired": "Ended: the quiz page was hidden for more than 10 seconds",
    "second_tab_switch": "Ended: the quiz page was hidden a second time after the warning",
    "left_quiz": "Closed: the student left the quiz for another page",
    "no_contact": "Closed: no activity for 30 minutes",
    "unverified_no_measurement": "Closed: the return to the quiz could not be verified (not a violation)",
    "reload_not_verified": "Closed: a reload could not be verified in time (not a violation)",
}

RETURN_LABELS = {
    "strike": "Came back within 10 seconds: warning given",
    "strike_network_delayed": "Came back within 10 seconds: warning given (the report was delayed by the network)",
    "reload_recovered": "Page reloaded and came back in time: no warning",
    "abandoned_unverified": "Return could not be verified: attempt closed (not a violation)",
}

NOTES = [
    "Times away are measured by the student's own browser; the server checks them against its own clock.",
    "A tab-switch incident means the quiz page was hidden (another tab, a minimised window, a locked screen). "
    "Aegis does not know which tab, website or app was used.",
    "Window focus changes (for example clicking the camera agent's window) are counted for diagnostics only "
    "and never count as a tab switch.",
    "Multiple-face episodes start after about 3 seconds of two or more faces and end about 2 seconds after; "
    "the recorded times are when the server received those signals. A second face is not proof of misconduct "
    "(for example a parent helping).",
    "Network problems are never counted as a tab switch. Periods that could not be verified are shown separately.",
]

MAX_ATTEMPTS = 50


def _iso(moment: datetime | None) -> str | None:
    return moment.isoformat() + "Z" if moment else None


def _seconds(start: datetime | None, end: datetime | None) -> float | None:
    if start is None or end is None:
        return None
    return round(max(0.0, (end - start).total_seconds()), 1)


def _incidents(attempt: QuizAttempt, events: list[QuizAttemptEvent], now: datetime) -> tuple[list, list, int, int]:
    """Absences, unverified periods, focus changes and delayed reports of one attempt."""
    incidents: list[dict[str, Any]] = []
    unverified: list[dict[str, Any]] = []
    focus_changes = 0
    delayed_reports = 0
    current = None
    open_unverified = None

    def close_unverified(at):
        nonlocal open_unverified
        if open_unverified is not None:
            open_unverified["to"] = _iso(at)
            open_unverified["seconds"] = _seconds(open_unverified["_from"], at)
            open_unverified = None

    for ev in events:
        outcome = ev.outcome
        if (ev.delivery_failures or 0) > 0:
            delayed_reports += 1
        if ev.kind == "blur":
            focus_changes += 1
            continue

        if ev.kind in ("hidden", "pagehide", "hidden_tick") and outcome in ("grace_started", "terminated") and (
            current is None or outcome == "grace_started"
        ):
            current = {
                "at": _iso(ev.received_at),
                "kind": "page_closed_or_reloaded" if ev.kind == "pagehide" else "page_hidden",
                "away_seconds": None,
                "away_measured": False,
                "result": None,
                "unverified": False,
            }
            incidents.append(current)
            if outcome == "terminated":
                current["result"] = END_LABELS.get(attempt.end_reason, "Ended")
                current = None
            continue

        if ev.kind == "deadline_passed" and outcome == "unverified":
            if current is not None:
                current["unverified"] = True
            open_unverified = {"from": _iso(ev.received_at), "to": None, "seconds": None, "_from": ev.received_at}
            unverified.append(open_unverified)
            continue

        if ev.kind == "hidden_tick" and outcome == "terminated" and current is not None:
            current["away_seconds"] = round((ev.hidden_ms or 0) / 1000, 1)
            current["away_measured"] = ev.hidden_ms is not None
            current["result"] = END_LABELS.get(attempt.end_reason, "Ended")
            close_unverified(ev.received_at)
            current = None
            continue

        if ev.kind in ("visible", "resume") and outcome in (
            "strike", "strike_network_delayed", "terminated", "reload_recovered", "abandoned_unverified"
        ):
            incident = current
            if incident is None:
                # The "hidden" report never arrived; the return carried the measurement.
                incident = {
                    "at": _iso(ev.received_at),
                    "kind": "page_hidden",
                    "away_seconds": None,
                    "away_measured": False,
                    "result": None,
                    "unverified": False,
                }
                incidents.append(incident)
            if ev.hidden_ms is not None:
                incident["away_seconds"] = round(ev.hidden_ms / 1000, 1)
                incident["away_measured"] = True
            if outcome == "reload_recovered":
                incident["kind"] = "page_reloaded"
            incident["result"] = (
                END_LABELS.get(attempt.end_reason, "Ended") if outcome == "terminated" else RETURN_LABELS[outcome]
            )
            close_unverified(ev.received_at)
            current = None

    if current is not None and current["result"] is None:
        if attempt.status in (AWAY, UNVERIFIED):
            current["result"] = "Waiting for the return to be confirmed"
        else:
            current["result"] = END_LABELS.get(attempt.end_reason, "No return was reported")
    if open_unverified is not None:
        close_unverified(attempt.ended_at or now)
    for period in unverified:
        period.pop("_from", None)
    return incidents, unverified, focus_changes, delayed_reports


def _episode_view(ep: SessionEvent, now: datetime) -> dict[str, Any]:
    return {
        "started_at": _iso(ep.started_at),
        "ended_at": _iso(ep.ended_at),
        "seconds": _seconds(ep.started_at, ep.ended_at),
        "ongoing": ep.ended_at is None,
        "peak_face_count": ep.peak_count,
        "end_reason": ep.end_reason,
    }


def build_report(db: Session, student: Student, limit: int = 20, now: datetime | None = None) -> dict[str, Any]:
    now = now or datetime.utcnow()
    limit = max(1, min(int(limit), MAX_ATTEMPTS))

    attempts = (
        db.query(QuizAttempt)
        .filter(QuizAttempt.student_id == student.id)
        .order_by(QuizAttempt.started_at.desc(), QuizAttempt.id.desc())
        .limit(limit)
        .all()
    )
    episodes = (
        db.query(SessionEvent)
        .filter(SessionEvent.student_id == student.id, SessionEvent.kind == MULTIPLE_FACES)
        .order_by(SessionEvent.started_at.desc())
        .limit(200)
        .all()
    )

    quiz_ids = {a.quiz_id for a in attempts if a.quiz_id}
    quizzes = {q.id: q for q in db.query(Quiz).filter(Quiz.id.in_(quiz_ids)).all()} if quiz_ids else {}
    lesson_ids = {q.lesson_id for q in quizzes.values()}
    session_ids = {e.monitoring_session_id for e in episodes}
    sessions = (
        {s.id: s for s in db.query(MonitoringSession).filter(MonitoringSession.id.in_(session_ids)).all()}
        if session_ids
        else {}
    )
    lesson_ids |= {s.lesson_id for s in sessions.values() if s.lesson_id}
    lessons = {l.id: l for l in db.query(Lesson).filter(Lesson.id.in_(lesson_ids)).all()} if lesson_ids else {}

    attempt_ids = [a.id for a in attempts]
    events_by_attempt: dict[int, list[QuizAttemptEvent]] = {i: [] for i in attempt_ids}
    if attempt_ids:
        for ev in (
            db.query(QuizAttemptEvent)
            .filter(QuizAttemptEvent.attempt_id.in_(attempt_ids))
            .order_by(QuizAttemptEvent.id)
            .all()
        ):
            events_by_attempt[ev.attempt_id].append(ev)

    attempt_views = []
    totals = {
        "attempts": len(attempts),
        "tab_switch_incidents": 0,
        "reloads": 0,
        "attempts_terminated": 0,
        "attempts_abandoned": 0,
        "attempts_graded": 0,
        "unverified_periods": 0,
        "reports_delayed_by_network": 0,
        "window_focus_changes": 0,
        "multiple_face_episodes": len(episodes),
        "multiple_face_seconds": round(sum(_seconds(e.started_at, e.ended_at) or 0.0 for e in episodes), 1),
    }

    for attempt in attempts:
        incidents, unverified, focus_changes, delayed = _incidents(attempt, events_by_attempt[attempt.id], now)
        switches = [i for i in incidents if i["kind"] != "page_reloaded"]
        quiz = quizzes.get(attempt.quiz_id)
        lesson = lessons.get(quiz.lesson_id) if quiz else None
        window_end = attempt.ended_at or now
        overlapping = [
            _episode_view(e, now)
            for e in episodes
            if e.started_at <= window_end and (e.ended_at or now) >= attempt.started_at
        ]
        attempt_views.append(
            {
                "attempt_id": attempt.id,
                "quiz_id": attempt.quiz_id,
                "quiz_title": quiz.title if quiz else None,
                "difficulty": quiz.difficulty if quiz else None,
                "lesson_id": lesson.id if lesson else None,
                "lesson_title": lesson.title if lesson else None,
                "mode": attempt.mode,
                "protected": attempt.protected,
                "status": attempt.status,
                "graded": attempt.status == SUBMITTED,
                "outcome": END_LABELS.get(attempt.end_reason) or (
                    "In progress" if attempt.status not in (TERMINATED, ABANDONED, SUBMITTED) else attempt.status
                ),
                "end_reason": attempt.end_reason,
                "started_at": _iso(attempt.started_at),
                "ended_at": _iso(attempt.ended_at),
                "tab_switch_incidents": len(switches),
                "incidents": incidents,
                "unverified_periods": unverified,
                "window_focus_changes": focus_changes,
                "reports_delayed_by_network": delayed,
                "multiple_face_episodes": overlapping,
            }
        )
        totals["tab_switch_incidents"] += len(switches)
        totals["reloads"] += len(incidents) - len(switches)
        totals["attempts_terminated"] += attempt.status == TERMINATED
        totals["attempts_abandoned"] += attempt.status == ABANDONED
        totals["attempts_graded"] += attempt.status == SUBMITTED
        totals["unverified_periods"] += len(unverified)
        totals["reports_delayed_by_network"] += delayed
        totals["window_focus_changes"] += focus_changes

    session_views = []
    for session_id in sorted(session_ids, key=lambda sid: sessions[sid].created_at if sid in sessions else now, reverse=True):
        session = sessions.get(session_id)
        own = [e for e in episodes if e.monitoring_session_id == session_id]
        lesson = lessons.get(session.lesson_id) if session and session.lesson_id else None
        session_views.append(
            {
                "monitoring_session_id": session_id,
                "lesson_title": lesson.title if lesson else None,
                "started_at": _iso(session.created_at) if session else None,
                "ended_at": _iso(session.ended_at) if session else None,
                "multiple_face_episodes": [_episode_view(e, now) for e in sorted(own, key=lambda e: e.started_at)],
            }
        )

    return {
        "generated_at": _iso(now),
        "notes": NOTES,
        "totals": totals,
        "attempts": attempt_views,
        "sessions": session_views,
    }
