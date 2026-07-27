from sqlalchemy.orm import Session

from app.models.progress import StudentProgress
from app.schemas.progress import ProgressUpdate


class ProgressService:

    @staticmethod
    def get_student_progress(
        db: Session,
        student_id: int,
    ):
        return (
            db.query(StudentProgress)
            .filter(StudentProgress.student_id == student_id)
            .all()
        )

    @staticmethod
    def get_lesson_progress(
        db: Session,
        student_id: int,
        lesson_id: int,
    ):
        return (
            db.query(StudentProgress)
            .filter(
                StudentProgress.student_id == student_id,
                StudentProgress.lesson_id == lesson_id,
            )
            .first()
        )

    @staticmethod
    def update_progress(
        db: Session,
        progress_id: int,
        progress: ProgressUpdate,
    ):
        existing = (
            db.query(StudentProgress)
            .filter(StudentProgress.id == progress_id)
            .first()
        )

        if not existing:
            return None

        existing.quiz_score = progress.quiz_score
        existing.response_time = progress.response_time
        existing.attention_score = progress.attention_score
        existing.difficulty = progress.difficulty
        existing.completed = progress.completed

        db.commit()
        db.refresh(existing)

        return existing