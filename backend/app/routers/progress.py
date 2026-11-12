from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_student
from app.database.connection import get_db
from app.models.student import Student
from app.schemas.progress import ProgressUpdate
from app.services.progress_service import ProgressService
from app.utils.response import progress_to_dict

router = APIRouter(tags=["Student Progress"])


def _require_self(student_id: int, student: Student) -> None:
    """Students may only read or change their own progress."""
    if student_id != student.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own progress",
        )


@router.get("/progress/{student_id}")
def get_student_progress(
    student_id: int,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student),
) -> dict[str, Any]:
    _require_self(student_id, student)

    progress = ProgressService.get_student_progress(
        db,
        student_id,
    )

    return {
        "success": True,
        "message": "Student progress fetched successfully",
        "data": [progress_to_dict(item) for item in progress],
    }


@router.get("/progress/{student_id}/{lesson_id}")
def get_lesson_progress(
    student_id: int,
    lesson_id: int,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student),
) -> dict[str, Any]:
    _require_self(student_id, student)

    progress = ProgressService.get_lesson_progress(
        db,
        student_id,
        lesson_id,
    )

    if progress is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progress not found",
        )

    return {
        "success": True,
        "message": "Lesson progress fetched successfully",
        "data": progress_to_dict(progress),
    }


@router.put("/progress/{progress_id}")
def update_progress(
    progress_id: int,
    progress: ProgressUpdate,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student),
) -> dict[str, Any]:

    existing = ProgressService.get_progress_by_id(db, progress_id)

    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progress not found",
        )

    _require_self(existing.student_id, student)

    updated = ProgressService.update_progress(
        db,
        progress_id,
        progress,
    )

    return {
        "success": True,
        "message": "Progress updated successfully",
        "data": progress_to_dict(updated),
    }
