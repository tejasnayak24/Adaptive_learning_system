"""Camera-monitoring endpoints (consent, sessions, local-agent pairing).

Browser (signed-in student, owner only):
    GET/POST/DELETE /monitoring/consent
    POST /monitoring/sessions                       create + pairing token
    POST /monitoring/sessions/{id}/pairing          reconnect: new token
    GET  /monitoring/sessions/{id}                  combined status
    POST /monitoring/sessions/{id}/end

Local camera agent:
    POST /monitoring/sessions/{id}/claim            pairing token -> agent token
    POST /monitoring/heartbeat                      Bearer agent token
    POST /monitoring/agent/end                      Bearer agent token

Tokens travel only in request bodies or the Authorization header, never
in URLs, and are never logged or stored in clear text.
"""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_student
from app.database.connection import get_db
from app.models.student import Student
from app.services import monitoring_service as ms

router = APIRouter(tags=["Camera Monitoring"])

_agent_bearer = HTTPBearer(auto_error=False)


class ConsentRequest(BaseModel):
    accept: bool
    guardian_authorization_confirmed: bool = False
    school_authorization_confirmed: bool = False


class SessionCreateRequest(BaseModel):
    lesson_id: int | None = None


class ClaimRequest(BaseModel):
    pairing_token: str = Field(min_length=20, max_length=128)


class HeartbeatRequest(BaseModel):
    sequence: int = Field(ge=1)
    sent_at: float | None = None
    captured_at: float | None = None
    camera_ok: bool
    camera_error: str | None = Field(default=None, max_length=64)
    face_detected: bool = False
    face_stable: bool = False
    lighting_ok: bool | None = None
    brightness: float | None = Field(default=None, ge=0, le=255)
    attention_score: float | None = Field(default=None, ge=0.0, le=1.0)
    yawning: bool | None = None
    looking_away: bool | None = None
    eyes_closed: bool | None = None
    possible_drowsiness: bool | None = None
    eyes_closed_seconds: float | None = Field(default=None, ge=0)
    head_direction: str | None = Field(default=None, max_length=16)
    gaze: str | None = Field(default=None, max_length=16)


class AgentEndRequest(BaseModel):
    reason: str = Field(default="agent_stopped", max_length=64)


def _raise(exc: ms.MonitoringError):
    raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc


def _agent_session(
    credentials: HTTPAuthorizationCredentials | None = Depends(_agent_bearer),
    db: Session = Depends(get_db),
):
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Agent token required")
    try:
        return ms.session_for_agent(db, credentials.credentials)
    except ms.MonitoringError as exc:
        _raise(exc)


def _ok(message: str, data: Any) -> dict[str, Any]:
    return {"success": True, "message": message, "data": data}


# -- consent -------------------------------------------------------------


@router.get("/monitoring/consent")
def get_consent(db: Session = Depends(get_db), student: Student = Depends(get_current_student)):
    return _ok("Consent status", ms.consent_view(db, student))


@router.post("/monitoring/consent")
def post_consent(
    request: ConsentRequest,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student),
):
    if not request.accept:
        raise HTTPException(status_code=400, detail="Consent must be explicitly accepted")
    try:
        ms.give_consent(
            db,
            student,
            guardian_authorization_confirmed=request.guardian_authorization_confirmed,
            school_authorization_confirmed=request.school_authorization_confirmed,
        )
    except ms.MonitoringError as exc:
        _raise(exc)
    return _ok("Consent recorded", ms.consent_view(db, student))


@router.delete("/monitoring/consent")
def delete_consent(db: Session = Depends(get_db), student: Student = Depends(get_current_student)):
    ms.withdraw_consent(db, student)
    return _ok("Consent withdrawn", ms.consent_view(db, student))


# -- browser session control --------------------------------------------


def _pairing_payload(session, token):
    return {
        "session_id": session.id,
        "pairing_token": token,
        "pairing_expires_in": ms.PAIRING_TTL_SECONDS,
        **ms.status_view(session),
    }


@router.post("/monitoring/sessions")
def create_session(
    request: SessionCreateRequest,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student),
):
    try:
        session, token = ms.create_session(db, student, request.lesson_id)
    except ms.MonitoringError as exc:
        _raise(exc)
    return _ok("Monitoring session created", _pairing_payload(session, token))


@router.post("/monitoring/sessions/{session_id}/pairing")
def reissue_pairing(
    session_id: str,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student),
):
    try:
        session, token = ms.reissue_pairing(db, student, session_id)
    except ms.MonitoringError as exc:
        _raise(exc)
    return _ok("New pairing token issued", _pairing_payload(session, token))


@router.get("/monitoring/sessions/{session_id}")
def session_status(
    session_id: str,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student),
):
    try:
        session = ms.owned_session(db, student, session_id)
    except ms.MonitoringError as exc:
        _raise(exc)
    ms.touch_client(db, session)
    return _ok("Monitoring status", ms.status_view(session))


@router.post("/monitoring/sessions/{session_id}/end")
def end_session(
    session_id: str,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student),
):
    try:
        session = ms.owned_session(db, student, session_id)
    except ms.MonitoringError as exc:
        _raise(exc)
    ms.end_session(db, session)
    return _ok("Monitoring session ended", ms.status_view(session))


# -- camera agent -------------------------------------------------------


@router.post("/monitoring/sessions/{session_id}/claim")
def claim(session_id: str, request: ClaimRequest, db: Session = Depends(get_db)):
    try:
        session, agent_token = ms.claim(db, session_id, request.pairing_token)
    except ms.MonitoringError as exc:
        _raise(exc)

    first_name = (session.student.name or "").split(" ")[0] if session.student else None
    return _ok(
        "Agent paired",
        {
            "agent_token": agent_token,
            "session_id": session.id,
            "student_name": first_name,
            "heartbeat_interval": ms.HEARTBEAT_INTERVAL_SECONDS,
            "stale_after_seconds": ms.telemetry_service.STALE_AFTER_SECONDS,
        },
    )


@router.post("/monitoring/heartbeat")
def heartbeat(
    request: HeartbeatRequest,
    db: Session = Depends(get_db),
    session=Depends(_agent_session),
):
    try:
        view = ms.heartbeat(db, session, request.model_dump())
    except ms.MonitoringError as exc:
        _raise(exc)
    return _ok("Heartbeat received", view)


@router.post("/monitoring/agent/end")
def agent_end(
    request: AgentEndRequest,
    db: Session = Depends(get_db),
    session=Depends(_agent_session),
):
    ms.agent_stopped(db, session, request.reason)
    return _ok("Agent disconnected", ms.status_view(session))
