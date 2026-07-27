from sqlalchemy.orm import Session

from app.models.lesson import Lesson
from app.schemas.lesson import LessonCreate, LessonUpdate


class LessonService:

    @staticmethod
    def get_all_lessons(db: Session):
        return db.query(Lesson).all()

    @staticmethod
    def get_lesson_by_id(
        db: Session,
        lesson_id: int
    ):
        return (
            db.query(Lesson)
            .filter(Lesson.id == lesson_id)
            .first()
        )

    @staticmethod
    def create_lesson(
        db: Session,
        lesson: LessonCreate
    ):
        new_lesson = Lesson(
            title=lesson.title,
            topic=lesson.topic,
            difficulty=lesson.difficulty,
            content=lesson.content,
        )

        db.add(new_lesson)
        db.commit()
        db.refresh(new_lesson)

        return new_lesson

    @staticmethod
    def update_lesson(
        db: Session,
        lesson_id: int,
        lesson: LessonUpdate
    ):
        existing = LessonService.get_lesson_by_id(
            db,
            lesson_id
        )

        if not existing:
            return None

        existing.title = lesson.title
        existing.topic = lesson.topic
        existing.difficulty = lesson.difficulty
        existing.content = lesson.content

        db.commit()
        db.refresh(existing)

        return existing

    @staticmethod
    def delete_lesson(
        db: Session,
        lesson_id: int
    ):
        lesson = LessonService.get_lesson_by_id(
            db,
            lesson_id
        )

        if not lesson:
            return False

        db.delete(lesson)
        db.commit()

        return True