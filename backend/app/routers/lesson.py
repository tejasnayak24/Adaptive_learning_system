from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_student, require_curriculum_manager
from app.database.connection import get_db
from app.models.lesson import Lesson
from app.models.student import Student
from app.services import curriculum_service as cs
from app.schemas.lesson import LessonCreate, LessonUpdate
from app.services.lesson_service import LessonService

router = APIRouter(tags=["Lessons"])


def _lesson_summary(lesson: Lesson) -> dict[str, Any]:
    return {
        "id": lesson.id,
        "title": lesson.title,
        "topic": lesson.topic,
        "difficulty": lesson.difficulty,
        "grade": lesson.grade,
        "subject": lesson.subject,
        "topic_id": lesson.topic_id,
        "position": lesson.position,
        "created_at": lesson.created_at,
    }


@router.get("/lessons")
def get_lessons(
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student),
) -> dict[str, Any]:
    """Lessons of the student's grade in curriculum order (all for teachers).

    A student who has not chosen a grade yet gets an empty list.
    """
    query = db.query(Lesson)
    if not cs.is_manager(student):
        query = query.filter(Lesson.grade == student.grade) if student.grade else query.filter(False)
    lessons = query.order_by(Lesson.grade, Lesson.subject, Lesson.position, Lesson.id).all()

    return {
        "success": True,
        "message": "Lessons fetched successfully",
        "data": jsonable_encoder([_lesson_summary(lesson) for lesson in lessons]),
    }


@router.get("/lesson/{lesson_id}")
def get_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student),
) -> dict[str, Any]:
    lesson = LessonService.get_lesson_by_id(db, lesson_id)

    if lesson is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found",
        )
    cs.check_lesson_access(student, lesson)

    quizzes = [
        {
            "id": quiz.id,
            "lesson_id": quiz.lesson_id,
            "title": quiz.title,
            "difficulty": quiz.difficulty,
        }
        for quiz in lesson.quizzes
    ]

    return {
        "success": True,
        "message": "Lesson fetched successfully",
        "data": {
            "id": lesson.id,
            "title": lesson.title,
            "topic": lesson.topic,
            "content": lesson.content,
            "difficulty": lesson.difficulty,
            "created_at": lesson.created_at,
            "quizzes": quizzes,
            "material": cs.lesson_material(lesson),
            "navigation": cs.navigation(db, lesson),
            **cs.placement(lesson),
        },
    }


@router.post("/lesson")
def create_lesson(
    lesson: LessonCreate,
    db: Session = Depends(get_db),
    manager=Depends(require_curriculum_manager),
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
    manager=Depends(require_curriculum_manager),
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
    manager=Depends(require_curriculum_manager),
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