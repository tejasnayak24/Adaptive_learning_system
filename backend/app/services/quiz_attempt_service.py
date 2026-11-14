"""Server-authoritative quiz attempts and the two-strike tab-switch rule.

The browser only *reports* what it observed (page hidden, page visible
again after N ms, still hidden after N ms, focus changes). Every decision
-- warning, termination, "unverified" -- is made here, with the server's
own clock, so throttled or frozen browser timers cannot stretch the rule.

The rule (protected attempts only):

1. The quiz page becomes hidden (0 strikes): a 10-second grace period starts
   at the server's receive time.
2. Back within 10 s: strike 1 and a warning; the quiz continues.
3. Reliable evidence of more than 10 s away: terminated (``grace_expired``).
4. Hidden again after strike 1: terminated at once (``second_tab_switch``).
5. A confirmed reload (the student accepted the browser's "leave / reload"
   prompt, so the page was unloaded: ``pagehide``) is an incident like any
   other: the first one gives strike 1 when the reloaded page is back
   within 10 s; after strike 1 it terminates at once. A cancelled reload
   sends nothing and is not an incident. The attempt, its answers and its
   strike history survive the reload.

Evidence and the 2-second delivery allowance:

* ``hidden_ms`` is the absence measured by the browser's monotonic clock.
  The 10-second limit is applied to it exactly; the allowance never adds
  grace time.
* The allowance only covers the time the "visible" report needs to reach
  the server: a return received more than 10 + 2 s after the absence began
  is accepted only if the browser reports it could not deliver promptly
  (a network problem). Otherwise the attempt is terminated.
* If nothing arrives after the grace period ends, the server cannot tell
  a closed laptop from a network failure: the attempt becomes
  ``unverified`` (locked, not a violation) until a report resolves it.
  A resolution without any measurement abandons the attempt -- it is never
  turned into a violation.

Window blur/focus, online/offline events are recorded for diagnostics only.

Terminated and abandoned attempts are never graded (no ``progress`` row),
and a new attempt at the same quiz is refused for ``COOLDOWN_SECONDS``.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Iterable

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.question import Question
from app.models.quiz import Quiz
from app.models.quiz_attempt import (
    ABANDONED,
    AWAY,
    ENDED_STATUSES,
    IN_PROGRESS,
    OPEN_STATUSES,
    SUBMITTED,
    TERMINATED,
    UNVERIFIED,
    QuizAttempt,
    QuizAttemptEvent,
)
from app.models.student import Student

GRACE_SECONDS = 10.0
DELIVERY_ALLOWANCE_SECONDS = 2.0
COOLDOWN_SECONDS = 300
# An open attempt with no contact at all for this long is abandoned.
NO_CONTACT_ABANDON_SECONDS = 30 * 60
# A report the browser held back for less than this was "sent promptly".
PROMPT_DELIVERY_MS = 1000.0
MAX_EVENTS_PER_ATTEMPT = 2000
MAX_DRAFT_STATE_CHARS = 4000

GRACE_MS = GRACE_SECONDS * 1000.0

# Every current quiz mode is graded, so every mode is protected. An
# explicitly ungraded practice mode, if one is added, would be exempt here.
PROTECTED_MODES = frozenset({"standard", "practice", "hints", "challenge"})

REASON_GRACE_EXPIRED = "grace_expired"
REASON_SECOND_SWITCH = "second_tab_switch"
REASON_LEFT_QUIZ = "left_quiz"
REASON_NO_CONTACT = "no_contact"
REASON_NO_MEASUREMENT = "unverified_no_measurement"

HIDE_KINDS = ("hidden", "pagehide")
RETURN_KINDS = ("visible", "resume")
DIAGNOSTIC_KINDS = ("blur", "focus", "online", "offline")
EVENT_KINDS = HIDE_KINDS + RETURN_KINDS + ("hidden_tick",) + DIAGNOSTIC_KINDS


class AttemptError(Exception):
    def __init__(self, status_code: int, detail: Any, retry_after: int | None = None):
        super().__init__(str(detail))
        self.status_code = status_code
        self.detail = detail
        self.retry_after = retry_after


def _utcnow() -> datetime:
    return datetime.utcnow()


def is_protected(mode: str) -> bool:
    return mode in PROTECTED_MODES


# ----------------------------------------------------------------------
# Lookup and lazy state transitions
# ----------------------------------------------------------------------


def owned_attempt(db: Session, student: Student, attempt_id: int) -> QuizAttempt:
    attempt = db.get(QuizAttempt, attempt_id)
    if attempt is None or attempt.student_id != student.id:
        # Another student's attempt looks exactly like a missing one.
        raise AttemptError(404, "Quiz attempt not found")
    return attempt


def _seconds_since(moment: datetime | None, now: datetime) -> float | None:
    if moment is None:
        return None
    return (now - moment).total_seconds()


def _note(db: Session, attempt: QuizAttempt, kind: str, outcome: str, now: datetime) -> None:
    """A server-side event (no browser page)."""
    seq = (attempt.page_sequences or {}).get("server", 0) + 1
    _set_sequence(attempt, "server", seq)
    db.add(
        QuizAttemptEvent(
            attempt_id=attempt.id, page_id="server", seq=seq, kind=kind, received_at=now, outcome=outcome
        )
    )


def _set_sequence(attempt: QuizAttempt, page_id: str, seq: int) -> None:
    sequences = dict(attempt.page_sequences or {})
    sequences[page_id] = seq
    attempt.page_sequences = sequences  # reassign so the JSON change is saved


def _end(attempt: QuizAttempt, status: str, reason: str, now: datetime) -> None:
    attempt.status = status
    attempt.end_reason = reason
    attempt.ended_at = now


def refresh(db: Session, attempt: QuizAttempt, now: datetime | None = None) -> QuizAttempt:
    """Apply time-based transitions that are due (evaluated lazily)."""
    now = now or _utcnow()
    if attempt.status not in OPEN_STATUSES:
        return attempt

    last_contact = attempt.last_seen_at or attempt.started_at
    if _seconds_since(last_contact, now) > NO_CONTACT_ABANDON_SECONDS:
        _end(attempt, ABANDONED, REASON_NO_CONTACT, now)
        _note(db, attempt, "no_contact", "abandoned", now)
        return attempt

    if attempt.status == AWAY:
        away = _seconds_since(attempt.away_started_at, now)
        if away is not None and away > GRACE_SECONDS + DELIVERY_ALLOWANCE_SECONDS:
            # No report said how the absence ended: neither a return nor
            # "still hidden" -- we cannot tell a closed tab from a network
            # failure. Lock the attempt; this is not a violation.
            attempt.status = UNVERIFIED
            attempt.unverified_since = now
            _note(db, attempt, "deadline_passed", "unverified", now)
    return attempt


def _touch(attempt: QuizAttempt, now: datetime) -> None:
    attempt.last_seen_at = now


# ----------------------------------------------------------------------
# Starting, resuming and saving
# ----------------------------------------------------------------------


def _open_attempt(db: Session, student_id: int, quiz_id: int) -> QuizAttempt | None:
    return (
        db.query(QuizAttempt)
        .filter(
            QuizAttempt.student_id == student_id,
            QuizAttempt.quiz_id == quiz_id,
            QuizAttempt.status.in_(OPEN_STATUSES),
        )
        .order_by(QuizAttempt.id.desc())
        .first()
    )


def _last_ended(db: Session, student_id: int, quiz_id: int) -> QuizAttempt | None:
    return (
        db.query(QuizAttempt)
        .filter(
            QuizAttempt.student_id == student_id,
            QuizAttempt.quiz_id == quiz_id,
            QuizAttempt.status.in_((TERMINATED, ABANDONED)),
            QuizAttempt.ended_at.isnot(None),
        )
        .order_by(QuizAttempt.ended_at.desc())
        .first()
    )


def cooldown_until(db: Session, student_id: int, quiz_id: int, now: datetime | None = None) -> datetime | None:
    """When the student may start this quiz again, if a cooldown applies."""
    now = now or _utcnow()
    last = _last_ended(db, student_id, quiz_id)
    if last is None:
        return None
    until = last.ended_at + timedelta(seconds=COOLDOWN_SECONDS)
    return until if until > now else None


def start_or_resume(
    db: Session,
    student: Student,
    quiz: Quiz,
    mode: str,
    monitoring_session_id: str | None,
    now: datetime | None = None,
) -> tuple[QuizAttempt, bool]:
    """Return the open attempt for this quiz (resumed) or a new one.

    Raises ``AttemptError(429)`` while a cooldown applies.
    """
    now = now or _utcnow()
    attempt = _open_attempt(db, student.id, quiz.id)
    if attempt is not None:
        refresh(db, attempt, now)
        if attempt.status in OPEN_STATUSES:
            _touch(attempt, now)
            if monitoring_session_id:
                # A reload pairs a new monitoring session; the attempt follows it.
                attempt.monitoring_session_id = monitoring_session_id
            return attempt, False
        db.flush()

    until = cooldown_until(db, student.id, quiz.id, now)
    if until is not None:
        retry_after = max(1, int((until - now).total_seconds() + 0.999))
        raise AttemptError(
            429,
            {
                "message": "Your previous attempt at this quiz ended without grading. "
                "You can start a new attempt when the 5-minute cooldown ends.",
                "cooldown_until": until.isoformat() + "Z",
                "retry_after_seconds": retry_after,
                # Why the previous attempt ended (e.g. after a reload page).
                "previous_attempt": view(_last_ended(db, student.id, quiz.id), now),
            },
            retry_after=retry_after,
        )

    attempt = QuizAttempt(
        student_id=student.id,
        quiz_id=quiz.id,
        monitoring_session_id=monitoring_session_id,
        mode=mode,
        protected=is_protected(mode),
        status=IN_PROGRESS,
        strikes=0,
        answers={},
        page_sequences={},
        started_at=now,
        last_seen_at=now,
    )
    try:
        with db.begin_nested():
            db.add(attempt)
            db.flush()
    except IntegrityError:
        # Another request (a second tab, a double click) opened the attempt
        # at the same moment; the unique index kept it to one. Resume it.
        existing = _open_attempt(db, student.id, quiz.id)
        if existing is None:
            raise
        _touch(existing, now)
        return existing, False
    return attempt, True


def _validate_answers(db: Session, quiz_id: int, answers: dict[int, str]) -> dict[str, str]:
    question_ids = {
        qid for (qid,) in db.query(Question.id).filter(Question.quiz_id == quiz_id).all()
    }
    cleaned = {}
    for question_id, option in answers.items():
        if int(question_id) not in question_ids:
            raise AttemptError(422, f"Question {question_id} is not in this quiz")
        letter = str(option).strip().upper()
        if letter not in ("A", "B", "C", "D"):
            raise AttemptError(422, f"Answer for question {question_id} must be A, B, C or D")
        cleaned[str(int(question_id))] = letter
    return cleaned


def save_answers(
    db: Session,
    attempt: QuizAttempt,
    answers: dict[int, str],
    draft_state: dict | None,
    now: datetime | None = None,
) -> QuizAttempt:
    """Save in-progress answers. Allowed in every open state, never after the end."""
    now = now or _utcnow()
    refresh(db, attempt, now)
    if attempt.status not in OPEN_STATUSES:
        raise AttemptError(409, {"message": "This quiz attempt has ended; its answers are frozen.", "attempt": view(attempt, now)})
    attempt.answers = _validate_answers(db, attempt.quiz_id, answers)
    if draft_state is not None:
        attempt.draft_state = draft_state
    _touch(attempt, now)
    return attempt


def abandon(db: Session, attempt: QuizAttempt, now: datetime | None = None) -> QuizAttempt:
    """The student confirmed leaving the quiz for another Aegis page."""
    now = now or _utcnow()
    refresh(db, attempt, now)
    if attempt.status in OPEN_STATUSES:
        _end(attempt, ABANDONED, REASON_LEFT_QUIZ, now)
        _note(db, attempt, "abandon", "abandoned", now)
    return attempt


# ----------------------------------------------------------------------
# Visibility events: the two-strike rule
# ----------------------------------------------------------------------


@dataclass
class ReportedEvent:
    seq: int
    kind: str
    client_ms: float | None = None
    hidden_ms: float | None = None
    delivery_failures: int | None = None
    queued_ms: float | None = None
    # Set by a page that was loaded by reloading the quiz page.
    reload: bool = False


def _clear_absence(attempt: QuizAttempt) -> None:
    attempt.away_started_at = None
    attempt.away_page_id = None
    attempt.away_kind = None
    attempt.unverified_since = None


def _strike(attempt: QuizAttempt) -> None:
    attempt.strikes = 1
    attempt.status = IN_PROGRESS
    _clear_absence(attempt)


def _second_switch(attempt: QuizAttempt, now: datetime) -> str:
    attempt.strikes += 1
    _end(attempt, TERMINATED, REASON_SECOND_SWITCH, now)
    return "terminated"


def _start_absence(attempt: QuizAttempt, page_id: str, kind: str, now: datetime) -> str:
    """The quiz page became hidden, or was unloaded (confirmed reload / close).

    After strike 1 either one terminates at once.
    """
    if attempt.strikes >= 1:
        return _second_switch(attempt, now)
    attempt.status = AWAY
    attempt.away_started_at = now
    attempt.away_page_id = page_id
    attempt.away_kind = "unload" if kind == "pagehide" else "hidden"
    return "grace_started"


def _terminate_grace(attempt: QuizAttempt, now: datetime) -> str:
    attempt.strikes += 1
    _end(attempt, TERMINATED, REASON_GRACE_EXPIRED, now)
    return "terminated"


def _apply(attempt: QuizAttempt, page_id: str, ev: ReportedEvent, now: datetime) -> str:
    if ev.kind in DIAGNOSTIC_KINDS:
        return "diagnostic"
    if not attempt.protected:
        return "diagnostic"
    if attempt.status not in OPEN_STATUSES:
        return "after_end"

    hidden = ev.hidden_ms

    if ev.kind in HIDE_KINDS:
        if attempt.status in (AWAY, UNVERIFIED):
            if ev.kind == "pagehide":
                attempt.away_kind = "unload"
            return "same_absence"
        return _start_absence(attempt, page_id, ev.kind, now)

    if ev.kind == "hidden_tick":
        # The page is still alive and still hidden.
        if attempt.status == IN_PROGRESS:
            # The "hidden" report was lost; this tick opens the absence.
            outcome = _start_absence(attempt, page_id, "hidden", now)
            if outcome == "terminated":
                return outcome
        if attempt.strikes >= 1:
            return _second_switch(attempt, now)
        if hidden is not None and hidden > GRACE_MS:
            return _terminate_grace(attempt, now)
        return "still_hidden"

    return _return(attempt, page_id, ev, now)


def _return(attempt: QuizAttempt, page_id: str, ev: ReportedEvent, now: datetime) -> str:
    """visible / resume: the student is back on the quiz page.

    A page loaded by a reload (``reload``) is judged exactly like any other
    return; its outcome is only labelled as a reload for the report.
    """
    outcome = _judge_return(attempt, ev, now)
    if ev.kind == "resume" and ev.reload and outcome in ("strike", "strike_network_delayed"):
        return f"reload_{outcome}"
    return outcome


def _judge_return(attempt: QuizAttempt, ev: ReportedEvent, now: datetime) -> str:
    hidden = ev.hidden_ms

    if attempt.status == IN_PROGRESS:
        if not hidden:
            return "no_absence"
        # The "hidden" report never arrived; the browser measured the absence.
        if attempt.strikes >= 1:
            return _second_switch(attempt, now)
        if hidden > GRACE_MS:
            return _terminate_grace(attempt, now)
        _strike(attempt)
        return "strike"

    away = _seconds_since(attempt.away_started_at, now) or 0.0
    in_time_by_server = away <= GRACE_SECONDS + DELIVERY_ALLOWANCE_SECONDS
    network_delayed = (ev.delivery_failures or 0) > 0 or (ev.queued_ms or 0.0) > PROMPT_DELIVERY_MS

    if attempt.strikes >= 1:
        # Defensive: an absence after strike 1 is a second incident.
        return _second_switch(attempt, now)

    if hidden is None:
        # No browser measurement (e.g. the tab was closed and reopened).
        if in_time_by_server:
            _strike(attempt)
            return "strike"
        _end(attempt, ABANDONED, REASON_NO_MEASUREMENT, now)
        return "abandoned_unverified"

    if hidden > GRACE_MS:
        return _terminate_grace(attempt, now)
    if in_time_by_server:
        _strike(attempt)
        return "strike"
    if network_delayed:
        # Back in time by the browser's clock; the report was held up by the
        # network. A network problem is never treated as a violation.
        _strike(attempt)
        return "strike_network_delayed"
    # Sent promptly, yet it arrived after the delivery allowance: the
    # allowance never extends the grace period.
    return _terminate_grace(attempt, now)


def report_events(
    db: Session,
    attempt: QuizAttempt,
    page_id: str,
    events: Iterable[ReportedEvent],
    now: datetime | None = None,
) -> QuizAttempt:
    now = now or _utcnow()
    refresh(db, attempt, now)

    stored = db.query(func.count(QuizAttemptEvent.id)).filter(QuizAttemptEvent.attempt_id == attempt.id).scalar()
    last_seq = (attempt.page_sequences or {}).get(page_id, 0)

    for ev in sorted(events, key=lambda e: e.seq):
        if ev.seq <= last_seq:
            continue  # duplicate or replayed
        last_seq = ev.seq
        outcome = _apply(attempt, page_id, ev, now)
        if stored < MAX_EVENTS_PER_ATTEMPT:
            db.add(
                QuizAttemptEvent(
                    attempt_id=attempt.id,
                    page_id=page_id,
                    seq=ev.seq,
                    kind=ev.kind,
                    client_ms=ev.client_ms,
                    hidden_ms=ev.hidden_ms,
                    delivery_failures=ev.delivery_failures,
                    queued_ms=ev.queued_ms,
                    received_at=now,
                    outcome=outcome,
                )
            )
            stored += 1

    _set_sequence(attempt, page_id, last_seq)
    _touch(attempt, now)
    return attempt


# ----------------------------------------------------------------------
# Submission
# ----------------------------------------------------------------------


def attempt_for_submit(
    db: Session, student: Student, quiz: Quiz, attempt_id: int | None, now: datetime | None = None
) -> QuizAttempt:
    """The open attempt a submission belongs to; raises 409 if it cannot be submitted."""
    now = now or _utcnow()
    if attempt_id is not None:
        attempt = owned_attempt(db, student, attempt_id)
        if attempt.quiz_id != quiz.id:
            raise AttemptError(409, "This attempt belongs to a different quiz")
    else:
        attempt = _open_attempt(db, student.id, quiz.id)
        if attempt is None:
            raise AttemptError(409, "Start the quiz before submitting it")

    refresh(db, attempt, now)
    if attempt.status == IN_PROGRESS:
        return attempt
    if attempt.status == AWAY:
        message = "Your return to the quiz has not been confirmed yet. Please try again."
    elif attempt.status == UNVERIFIED:
        message = "This attempt is locked until your return to the quiz is confirmed."
    else:
        message = "This quiz attempt has ended and can no longer be submitted."
    raise AttemptError(409, {"message": message, "attempt": view(attempt, now)})


def mark_submitted(attempt: QuizAttempt, progress_id: int, answers: dict[int, str], now: datetime | None = None) -> None:
    now = now or _utcnow()
    attempt.answers = {str(k): v for k, v in answers.items()}
    attempt.progress_id = progress_id
    _clear_absence(attempt)
    _end(attempt, SUBMITTED, "submitted", now)


# ----------------------------------------------------------------------
# Views
# ----------------------------------------------------------------------


def _iso(moment: datetime | None) -> str | None:
    return moment.isoformat() + "Z" if moment else None


def view(attempt: QuizAttempt, now: datetime | None = None) -> dict[str, Any]:
    """The attempt as the student's browser sees it. Never contains correct answers."""
    now = now or _utcnow()
    cooldown = None
    retry_after = None
    if attempt.status in (TERMINATED, ABANDONED) and attempt.ended_at is not None:
        until = attempt.ended_at + timedelta(seconds=COOLDOWN_SECONDS)
        if until > now:
            cooldown = _iso(until)
            retry_after = max(1, int((until - now).total_seconds() + 0.999))

    return {
        "id": attempt.id,
        "quiz_id": attempt.quiz_id,
        "mode": attempt.mode,
        "protected": attempt.protected,
        "status": attempt.status,
        "graded": attempt.status == SUBMITTED,
        "strikes": attempt.strikes,
        "warning": attempt.status in OPEN_STATUSES and attempt.strikes >= 1,
        "grace_seconds": GRACE_SECONDS,
        "answers": dict(attempt.answers or {}),
        "draft_state": attempt.draft_state,
        "started_at": _iso(attempt.started_at),
        "away_started_at": _iso(attempt.away_started_at),
        "ended_at": _iso(attempt.ended_at),
        "end_reason": attempt.end_reason,
        "progress_id": attempt.progress_id,
        "cooldown_until": cooldown,
        "retry_after_seconds": retry_after,
        "server_time": _iso(now),
    }


def ended(attempt: QuizAttempt) -> bool:
    return attempt.status in ENDED_STATUSES
