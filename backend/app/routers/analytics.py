"""Learning analytics for the signed-in student (Phase 6).

``GET /analytics/summary`` returns the dashboard / progress figures for the
authenticated student only -- there is no student id parameter, so one
student can never read another student's analytics.
"""

from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_student
from app.database.connection import get_db
from app.models.student import Student
from app.services import analytics_service

router = APIRouter(tags=["Analytics"])


@router.get("/analytics/summary")
def analytics_summary(
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student),
) -> dict[str, Any]:
    return {
        "success": True,
        "message": "Learning analytics fetched",
        "data": analytics_service.student_summary(db, student),
    }
