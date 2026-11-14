"""Session-integrity report (student's own records only)."""

from typing import Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_student
from app.database.connection import get_db
from app.models.student import Student
from app.services.integrity_report_service import build_report

router = APIRouter(tags=["Session integrity"])


@router.get("/integrity/report")
def integrity_report(
    limit: int = Query(default=20, ge=1, le=50),
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student),
) -> dict[str, Any]:
    """Factual activity summary: tab-switch incidents, unverified periods and
    multiple-face episodes of the signed-in student's recent quiz attempts.
    No score or probability; another student's records are never included."""
    return {"success": True, "message": "Session activity", "data": build_report(db, student, limit)}
