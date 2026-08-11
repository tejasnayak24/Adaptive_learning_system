from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.connection import get_db
from app.schemas.lesson import LessonCreate, LessonUpdate
from app.services.lesson_service import LessonService


def serialize_lesson(lesson):
    return {
        "id": lesson.id,
        "title": lesson.title,
        "topic": lesson.topic,
        "difficulty": lesson.difficulty,
        "content": lesson.content,
        "created_at": lesson.created_at,
        "quizzes": [
            {
                "id": quiz.id,
                "lesson_id": quiz.lesson_id,
                "title": quiz.title,
                "difficulty": quiz.difficulty,
                "question_count": len(quiz.questions),
            }
            for quiz in sorted(lesson.quizzes, key=lambda q: (q.difficulty, q.id))
        ],
    }

router = APIRouter(tags=["Lessons"])


@router.get("/lessons")
def get_lessons(
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    lessons = LessonService.get_all_lessons(db)

    return {
        "success": True,
        "message": "Lessons fetched successfully",
        "data": [serialize_lesson(lesson) for lesson in lessons],
    }


@router.get("/lesson/{lesson_id}")
def get_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    lesson = LessonService.get_lesson_by_id(db, lesson_id)

    if lesson is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found",
        )

    return {
        "success": True,
        "message": "Lesson fetched successfully",
        "data": serialize_lesson(lesson),
    }


@router.post("/lesson")
def create_lesson(
    lesson: LessonCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    new_lesson = LessonService.create_lesson(db, lesson)

    return {
        "success": True,
        "message": "Lesson created successfully",
        "data": jsonable_encoder(new_lesson),
    }


@router.put("/lesson/{lesson_id}")
def update_lesson(
    lesson_id: int,
    lesson: LessonUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    updated = LessonService.update_lesson(
        db,
        lesson_id,
        lesson,
    )

    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found",
        )

    return {
        "success": True,
        "message": "Lesson updated successfully",
        "data": jsonable_encoder(updated),
    }


@router.delete("/lesson/{lesson_id}")
def delete_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    deleted = LessonService.delete_lesson(db, lesson_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found",
        )

    return {
        "success": True,
        "message": "Lesson deleted successfully",
        "data": {},
    }