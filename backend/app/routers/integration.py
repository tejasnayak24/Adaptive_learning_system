"""Facial-analysis telemetry endpoints.

* ``POST /attention`` -- called by the local camera agent once per second.
* ``GET /attention/{student_id}`` and ``POST /attention/{student_id}/reset``
  -- called by the signed-in student's browser; owner-only.

The former ``POST /recommend`` placeholder was removed: recommendations are
served by ``/rl/recommend`` and ``/recommendations/latest``.
"""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.auth.dependencies import get_current_student
from app.models.student import Student
from app.services.telemetry_service import (
    get_telemetry,
    reset_telemetry,
    update_telemetry,
)

router = APIRouter(tags=["Facial Analysis Telemetry"])


class AttentionSample(BaseModel):
    """One reading from the camera agent. Extra fields are ignored."""

    student_id: int
    attention_score: float = Field(ge=0.0, le=1.0)
    yawning: bool = False
    looking_away: bool = False


def _require_self(student_id: int, student: Student) -> None:
    if student_id != student.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own telemetry",
        )


@router.post("/attention")
def attention(sample: AttentionSample) -> dict[str, Any]:
    update_telemetry(
        student_id=sample.student_id,
        attention_score=sample.attention_score,
        yawning=sample.yawning,
        looking_away=sample.looking_away,
    )

    return {
        "success": True,
        "message": "Attention score received",
        "data": sample.model_dump(),
    }


@router.get("/attention/{student_id}")
def get_attention(
    student_id: int,
    student: Student = Depends(get_current_student),
) -> dict[str, Any]:
    _require_self(student_id, student)

    return {
        "success": True,
        "message": "Latest attention telemetry fetched",
        "data": get_telemetry(student_id),
    }


@router.post("/attention/{student_id}/reset")
def reset_attention(
    student_id: int,
    student: Student = Depends(get_current_student),
) -> dict[str, Any]:
    _require_self(student_id, student)
    reset_telemetry(student_id)

    return {
        "success": True,
        "message": "Quiz telemetry reset",
        "data": get_telemetry(student_id),
    }
