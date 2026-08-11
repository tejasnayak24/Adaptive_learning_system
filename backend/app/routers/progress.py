from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.connection import get_db
from app.schemas.progress import ProgressUpdate
from app.services.progress_service import ProgressService

router = APIRouter(tags=["Student Progress"])


def progress_to_dict(progress):
    return {
        "id": progress.id,
        "student_id": progress.student_id,
        "lesson_id": progress.lesson_id,
        "quiz_score": progress.quiz_score,
        "response_time": progress.response_time,
        "attention_score": progress.attention_score,
        "difficulty": progress.difficulty,
        "completed": progress.completed,
    }


@router.get("/progress/{student_id}")
def get_student_progress(
    student_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:

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
    current_user=Depends(get_current_user),
) -> dict[str, Any]:

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
    current_user=Depends(get_current_user),
) -> dict[str, Any]:

    updated = ProgressService.update_progress(
        db,
        progress_id,
        progress,
    )

    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progress not found",
        )

    return {
        "success": True,
        "message": "Progress updated successfully",
        "data": progress_to_dict(updated),
    }