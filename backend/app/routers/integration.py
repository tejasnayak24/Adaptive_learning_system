"""Facial-analysis telemetry endpoints.

* ``GET /attention/{student_id}`` and ``POST /attention/{student_id}/reset``
  -- called by the signed-in student's browser; owner-only.

Measurements arrive only as authenticated heartbeats from the paired
camera agent (``POST /monitoring/heartbeat``). The former unauthenticated
``POST /attention`` (which trusted a student id sent by the camera) and
the ``POST /recommend`` placeholder were removed.
"""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependencies import get_current_student
from app.models.student import Student
from app.services.telemetry_service import (
    get_telemetry,
    reset_telemetry,
)

router = APIRouter(tags=["Facial Analysis Telemetry"])


def _require_self(student_id: int, student: Student) -> None:
    if student_id != student.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own telemetry",
        )


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
