"""FastAPI router exposing the RL recommendation endpoints.

* ``POST /rl/recommend`` -- stateless recommendation for a supplied state.
* ``GET /rl/model`` -- which offline-trained Q-table is loaded.
* ``GET /recommendations/latest`` -- the signed-in student's most recent
  stored recommendation (generated server-side when a quiz is graded).
* ``GET /recommendations`` -- the signed-in student's recommendation history.

All endpoints require authentication.
"""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_student
from app.database.connection import get_db
from app.models.progress import Progress
from app.models.recommendation import RecommendationHistory
from app.models.student import Student
from app.schemas.rl import RecommendationRequest
from app.services.recommendation_service import (
    has_camera_telemetry,
    recommendation_to_dict,
)
from app.services.rl_service import get_rl_service

router = APIRouter(tags=["Reinforcement Learning"])


@router.post("/rl/recommend")
def recommend(
    request: RecommendationRequest,
    student: Student = Depends(get_current_student),
) -> dict[str, Any]:
    """Return the RL agent's recommendation for a supplied student state.

    Returns:
        A mapping with ``action`` (or ``None``), ``confidence`` (a heuristic
        decision-strength indicator, not a probability, or ``None``),
        ``explanation``, ``policy``, the Q-values of the eligible actions,
        the blocked actions with reasons, and ``telemetry_available``.
        When real camera telemetry is missing no recommendation is
        generated.

    Raises:
        HTTPException: 422 if the RL engine rejects the state, 500 if the
            recommendation fails for any other reason.
    """
    if not request.telemetry_available:
        return {
            "action": None,
            "confidence": None,
            "explanation": (
                "Camera telemetry was unavailable for this attempt, so an "
                "adaptive recommendation was not generated."
            ),
            "policy": None,
            "telemetry_available": False,
        }

    try:
        decision = get_rl_service().decide(request.model_dump())
    except (ValueError, KeyError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail="Failed to generate a recommendation."
        ) from exc

    detail = decision.detail
    return {
        "action": decision.recommendation.action.name,
        "confidence": decision.recommendation.confidence,
        "confidence_kind": "heuristic_decision_strength",
        "explanation": decision.recommendation.explanation,
        "policy": decision.policy,
        "model_version": decision.model_version,
        "state_key": list(decision.state_key),
        "state_features": detail.get("state_features"),
        "q_values": detail.get("q_values"),
        "runner_up": detail.get("runner_up"),
        "margin": detail.get("margin"),
        "blocked_actions": detail.get("blocked_actions"),
        "untested_actions": detail.get("untested_actions"),
        "state_visits": detail.get("state_visits"),
        "telemetry_available": True,
    }


@router.get("/rl/model")
def model_info(student: Student = Depends(get_current_student)) -> dict[str, Any]:
    """Which trained Q-table is loaded (offline-trained; not updated online)."""
    return {
        "success": True,
        "data": {**get_rl_service().model_info, "training": "offline_simulation", "online_updates": False},
    }


def _attempt_summary(progress: Progress | None) -> dict[str, Any] | None:
    if progress is None:
        return None
    return {
        "progress_id": progress.id,
        "lesson_id": progress.lesson_id,
        "quiz_id": progress.quiz_id,
        "lesson_title": progress.lesson.title if progress.lesson else None,
        "topic": progress.lesson.topic if progress.lesson else None,
        "quiz_score": progress.quiz_score,
        "difficulty": progress.difficulty,
        "attention_score": progress.attention_score,
        "telemetry_available": has_camera_telemetry(progress),
        "created_at": progress.created_at,
    }


@router.get("/recommendations/latest")
def latest_recommendation(
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student),
) -> dict[str, Any]:
    """The recommendation for the student's most recent attempt.

    ``recommendation`` is ``None`` when the student has no attempts yet
    (``status = "no_attempts"``) or when the latest attempt had no camera
    telemetry (``status = "telemetry_unavailable"``).
    """
    latest_attempt = (
        db.query(Progress)
        .filter(Progress.student_id == student.id)
        .order_by(Progress.id.desc())
        .first()
    )

    if latest_attempt is None:
        return {
            "success": True,
            "message": "No quiz attempts yet",
            "data": {"status": "no_attempts", "recommendation": None, "attempt": None},
        }

    row = (
        db.query(RecommendationHistory)
        .filter(
            RecommendationHistory.student_id == student.id,
            RecommendationHistory.progress_id == latest_attempt.id,
        )
        .order_by(RecommendationHistory.id.desc())
        .first()
    )

    if row is None:
        status = (
            "telemetry_unavailable"
            if not has_camera_telemetry(latest_attempt)
            else "not_generated"
        )
    else:
        status = "available"

    return {
        "success": True,
        "message": "Latest recommendation fetched",
        "data": {
            "status": status,
            "recommendation": recommendation_to_dict(row),
            "attempt": _attempt_summary(latest_attempt),
        },
    }


@router.get("/recommendations")
def recommendation_history(
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student),
) -> dict[str, Any]:
    rows = (
        db.query(RecommendationHistory)
        .filter(RecommendationHistory.student_id == student.id)
        .order_by(RecommendationHistory.id.desc())
        .all()
    )

    return {
        "success": True,
        "message": "Recommendation history fetched",
        "data": [recommendation_to_dict(row) for row in rows],
    }
