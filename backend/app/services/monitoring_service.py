"""Monitored learning sessions: consent, agent pairing, heartbeats, status.

Pairing protocol
----------------
1. The signed-in student's browser creates a session (requires current
   consent). The backend returns a random, single-use pairing token that
   expires after ``PAIRING_TTL_SECONDS``; only its SHA-256 hash is stored.
2. The browser hands the token to the local camera agent
   (http://127.0.0.1:8765) in a POST body.
3. The agent exchanges it at ``/monitoring/sessions/{id}/claim`` for an
   agent token bound to that student and session. The pairing token is
   consumed and can never be used again.
4. The agent sends heartbeats with the agent token. The student identity
   always comes from the token's session -- never from the agent.

Reconnecting issues a new pairing token for the same session and revokes
the previous agent token, so the student never has to log in again.

A session ends when the student ends it, starts another one, or stops
polling its status for ``CLIENT_TIMEOUT_SECONDS`` (e.g. the tab was
closed). Heartbeats for an ended session are rejected, which makes the
agent release the webcam.
"""

import hashlib
import hmac
import secrets
import time
from datetime import datetime, timedelta
from typing import Any

from sqlalchemy.orm import Session

from app.models.monitoring import MonitoringConsent, MonitoringSession
from app.models.student import Student
from app.services import telemetry_service

CONSENT_VERSION = "2026-11-v1"
ADULT_AGE = 18

PAIRING_TTL_SECONDS = 120
AGENT_TOKEN_TTL_SECONDS = 8 * 3600
CLIENT_TIMEOUT_SECONDS = 60
HEARTBEAT_INTERVAL_SECONDS = 1.0
MAX_CAPTURE_AGE_SECONDS = 3.0  # a measurement older than this is not "live"

PENDING = "pending"
ACTIVE = "active"
ENDED = "ended"


class MonitoringError(Exception):
    def __init__(self, status_code: int, detail: str):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail


def _utcnow() -> datetime:
    return datetime.utcnow()


def _hash(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _matches(token: str, digest: str | None) -> bool:
    return digest is not None and hmac.compare_digest(_hash(token), digest)


# ---------------------------------------------------------------------------
# Consent
# ---------------------------------------------------------------------------


def is_minor(student: Student) -> bool:
    return student.age < ADULT_AGE


def current_consent(db: Session, student: Student) -> MonitoringConsent | None:
    return (
        db.query(MonitoringConsent)
        .filter(
            MonitoringConsent.student_id == student.id,
            MonitoringConsent.consent_version == CONSENT_VERSION,
            MonitoringConsent.withdrawn_at.is_(None),
        )
        .order_by(MonitoringConsent.id.desc())
        .first()
    )


def consent_view(db: Session, student: Student) -> dict[str, Any]:
    consent = current_consent(db, student)
    return {
        "required_version": CONSENT_VERSION,
        "is_minor": is_minor(student),
        "valid": consent is not None,
        "consent": None
        if consent is None
        else {
            "version": consent.consent_version,
            "accepted_at": consent.accepted_at,
            "guardian_authorization_confirmed": consent.guardian_authorization_confirmed,
            "school_authorization_confirmed": consent.school_authorization_confirmed,
        },
    }


def give_consent(
    db: Session,
    student: Student,
    *,
    guardian_authorization_confirmed: bool,
    school_authorization_confirmed: bool,
) -> MonitoringConsent:
    minor = is_minor(student)
    if minor and not (guardian_authorization_confirmed and school_authorization_confirmed):
        raise MonitoringError(
            400,
            "Students under 18 need confirmation that a parent or guardian and "
            "their school have authorised camera-based monitoring.",
        )

    for old in db.query(MonitoringConsent).filter(
        MonitoringConsent.student_id == student.id, MonitoringConsent.withdrawn_at.is_(None)
    ):
        old.withdrawn_at = _utcnow()

    consent = MonitoringConsent(
        student_id=student.id,
        consent_version=CONSENT_VERSION,
        is_minor=minor,
        guardian_authorization_confirmed=bool(guardian_authorization_confirmed),
        school_authorization_confirmed=bool(school_authorization_confirmed),
    )
    db.add(consent)
    db.commit()
    return consent


def withdraw_consent(db: Session, student: Student) -> None:
    for consent in db.query(MonitoringConsent).filter(
        MonitoringConsent.student_id == student.id, MonitoringConsent.withdrawn_at.is_(None)
    ):
        consent.withdrawn_at = _utcnow()
    for session in _open_sessions(db, student.id):
        _end(session, "consent_withdrawn")
    db.commit()


# ---------------------------------------------------------------------------
# Sessions
# ---------------------------------------------------------------------------


def _open_sessions(db: Session, student_id: int):
    return (
        db.query(MonitoringSession)
        .filter(MonitoringSession.student_id == student_id, MonitoringSession.status != ENDED)
        .all()
    )


def _end(session: MonitoringSession, reason: str) -> None:
    if session.status == ENDED:
        return
    session.status = ENDED
    session.ended_at = _utcnow()
    session.end_reason = reason
    session.pairing_token_hash = None
    session.agent_token_hash = None


def _issue_pairing_token(session: MonitoringSession) -> str:
    token = secrets.token_urlsafe(32)
    session.pairing_token_hash = _hash(token)
    session.pairing_expires_at = _utcnow() + timedelta(seconds=PAIRING_TTL_SECONDS)
    return token


def create_session(db: Session, student: Student, lesson_id: int | None) -> tuple[MonitoringSession, str]:
    if current_consent(db, student) is None:
        raise MonitoringError(403, "Camera monitoring consent is required before starting a lesson.")

    for session in _open_sessions(db, student.id):
        _end(session, "replaced_by_new_session")

    session = MonitoringSession(
        id="ms_" + secrets.token_urlsafe(18),
        student_id=student.id,
        lesson_id=lesson_id,
        status=PENDING,
        last_client_seen_at=_utcnow(),
        last_sequence=0,
        heartbeat_count=0,
        reconnect_count=0,
    )
    token = _issue_pairing_token(session)
    db.add(session)
    db.commit()
    telemetry_service.forget_student(student.id)
    return session, token


def owned_session(db: Session, student: Student, session_id: str) -> MonitoringSession:
    session = db.get(MonitoringSession, session_id)
    if session is None:
        raise MonitoringError(404, "Monitoring session not found")
    if session.student_id != student.id:
        raise MonitoringError(403, "This monitoring session belongs to another student")
    return session


def _expire_if_abandoned(session: MonitoringSession) -> None:
    if session.status == ENDED:
        return
    seen = session.last_client_seen_at or session.created_at
    if _utcnow() - seen > timedelta(seconds=CLIENT_TIMEOUT_SECONDS):
        _end(session, "client_inactive")


def reissue_pairing(db: Session, student: Student, session_id: str) -> tuple[MonitoringSession, str]:
    """New pairing token for reconnection; revokes the current agent token."""
    session = owned_session(db, student, session_id)
    _expire_if_abandoned(session)
    if session.status == ENDED:
        db.commit()
        raise MonitoringError(409, "This monitoring session has ended; start a new one")

    session.agent_token_hash = None
    session.agent_token_expires_at = None
    session.status = PENDING
    session.reconnect_count += 1
    session.last_client_seen_at = _utcnow()
    token = _issue_pairing_token(session)
    db.commit()
    return session, token


def claim(db: Session, session_id: str, pairing_token: str) -> tuple[MonitoringSession, str]:
    """Agent exchanges a single-use pairing token for an agent token."""
    session = db.get(MonitoringSession, session_id)
    # Same error for every failure so the endpoint cannot be used to probe.
    rejected = MonitoringError(401, "Invalid, expired or already used pairing token")

    if session is None or session.status == ENDED:
        raise rejected
    if not _matches(pairing_token, session.pairing_token_hash):
        raise rejected
    if session.pairing_expires_at is None or session.pairing_expires_at < _utcnow():
        session.pairing_token_hash = None
        db.commit()
        raise rejected

    agent_token = secrets.token_urlsafe(32)
    now = _utcnow()
    session.pairing_token_hash = None  # single use
    session.pairing_expires_at = None
    session.agent_token_hash = _hash(agent_token)
    session.agent_token_expires_at = now + timedelta(seconds=AGENT_TOKEN_TTL_SECONDS)
    session.status = ACTIVE
    session.claimed_at = now
    session.last_sequence = 0
    db.commit()
    return session, agent_token


def session_for_agent(db: Session, agent_token: str) -> MonitoringSession:
    session = (
        db.query(MonitoringSession)
        .filter(MonitoringSession.agent_token_hash == _hash(agent_token))
        .first()
    )
    if session is None or session.status != ACTIVE:
        raise MonitoringError(401, "Agent token is not valid for an active session")
    if session.agent_token_expires_at is None or session.agent_token_expires_at < _utcnow():
        raise MonitoringError(401, "Agent token expired")

    _expire_if_abandoned(session)
    if session.status == ENDED:
        db.commit()
        raise MonitoringError(410, "The learning session has ended")
    return session


def heartbeat(db: Session, session: MonitoringSession, sample: dict[str, Any]) -> dict[str, Any]:
    sequence = int(sample["sequence"])
    if sequence <= session.last_sequence:
        raise MonitoringError(409, "Out-of-order or replayed heartbeat")

    server_now = time.time()
    captured_at = sample.get("captured_at")
    measurement = dict(sample)
    # A measurement the agent captured too long ago is not live data.
    if captured_at is None or abs(server_now - float(captured_at)) > MAX_CAPTURE_AGE_SECONDS:
        if sample.get("camera_ok"):
            measurement["camera_error"] = "stale_measurement"
        measurement["camera_ok"] = False

    session.last_sequence = sequence
    session.heartbeat_count += 1
    session.last_heartbeat_at = _utcnow()

    telemetry_service.record_heartbeat(session.student_id, session.id, measurement)
    view = status_view(session)
    if view["state"] == "verified" and session.first_verified_at is None:
        session.first_verified_at = _utcnow()
    db.commit()
    return view


def agent_stopped(db: Session, session: MonitoringSession, reason: str) -> None:
    """The agent shut down: the session waits for a (re)connection."""
    session.agent_token_hash = None
    session.agent_token_expires_at = None
    if session.status == ACTIVE:
        session.status = PENDING
    db.commit()


def touch_client(db: Session, session: MonitoringSession) -> None:
    _expire_if_abandoned(session)
    if session.status != ENDED:
        session.last_client_seen_at = _utcnow()
    db.commit()


def end_session(db: Session, session: MonitoringSession, reason: str = "ended_by_student") -> None:
    _end(session, reason)
    db.commit()


def status_view(session: MonitoringSession) -> dict[str, Any]:
    """Combined monitoring state shown to the student's browser.

    States: ``awaiting_agent`` (not paired yet / agent stopped),
    ``stale`` (paired but no fresh heartbeat), ``camera_unavailable``,
    ``no_face``, ``verifying`` (face seen, not yet stable), ``verified``
    and ``ended``.
    """
    telemetry = telemetry_service.get_telemetry(session.student_id)
    same_session = telemetry["session_id"] == session.id

    if session.status == ENDED:
        state = "ended"
    elif session.status == PENDING:
        state = "awaiting_agent"
    elif not same_session or telemetry["status"] in ("no_data", "stale"):
        state = "stale"
    elif telemetry["status"] == "camera_unavailable":
        state = "camera_unavailable"
    elif telemetry["status"] == "no_face":
        state = "no_face"
    elif not telemetry["face_stable"]:
        state = "verifying"
    else:
        state = "verified"

    return {
        "session_id": session.id,
        "status": session.status,
        "state": state,
        "verified": state == "verified",
        "end_reason": session.end_reason,
        "heartbeat_age_seconds": telemetry["age_seconds"] if same_session else None,
        "camera_error": telemetry["camera_error"] if same_session else None,
        "lighting_ok": telemetry["lighting_ok"] if same_session else None,
        "possible_drowsiness": telemetry["possible_drowsiness"] if same_session else None,
        "attention_score": telemetry["attention_score"] if same_session else None,
        "stale_after_seconds": telemetry_service.STALE_AFTER_SECONDS,
    }
