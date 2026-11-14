"""Curriculum browsing: Grade -> Subject -> Unit -> Topic -> Lesson."""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_student
from app.database.connection import get_db
from app.models.lesson import Lesson
from app.models.student import Student
from app.services import curriculum_service as cs

router = APIRouter(tags=["Curriculum"])


@router.get("/curriculum/grades")
def grades(
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student),
) -> dict[str, Any]:
    """Lesson counts for every grade and subject (used for grade selection)."""
    return {"success": True, "data": cs.grade_overview(db)}


@router.get("/curriculum")
def curriculum(
    subject: str | None = Query(default=None),
    grade: int | None = Query(default=None),
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student),
) -> dict[str, Any]:
    """The student's grade curriculum, optionally for one subject.

    Students always get their own grade (409 ``grade_required`` if not
    chosen yet; 403 for another grade). Teachers/admins may pass ``grade``.
    Each lesson includes its quizzes and the student's attempts/best score.
    """
    visible = cs.visible_grade(student, grade)
    return {"success": True, "data": cs.curriculum_tree(db, student, visible, subject)}


@router.get("/curriculum/lessons/{lesson_id}/navigation")
def lesson_navigation(
    lesson_id: int,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student),
) -> dict[str, Any]:
    lesson = db.get(Lesson, lesson_id)
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    cs.check_lesson_access(student, lesson)
    return {"success": True, "data": cs.navigation(db, lesson)}
