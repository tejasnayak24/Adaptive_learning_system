from sqlalchemy.orm import Session

from app.models.progress import Progress
from app.schemas.progress import ProgressUpdate


class ProgressService:

    @staticmethod
    def get_student_progress(db: Session, student_id: int):
        return (
            db.query(Progress)
            .filter(Progress.student_id == student_id)
            .all()
        )

    @staticmethod
    def get_lesson_progress(
        db: Session,
        student_id: int,
        lesson_id: int,
    ):
        return (
            db.query(Progress)
            .filter(
                Progress.student_id == student_id,
                Progress.lesson_id == lesson_id,
            )
            .first()
        )

    @staticmethod
    def update_progress(
        db: Session,
        progress_id: int,
        progress: ProgressUpdate,
    ):
        db_progress = (
            db.query(Progress)
            .filter(Progress.id == progress_id)
            .first()
        )

        if db_progress is None:
            return None

        db_progress.quiz_score = progress.quiz_score
        db_progress.response_time = progress.response_time
        db_progress.attention_score = progress.attention_score
        db_progress.difficulty = progress.difficulty
        db_progress.completed = progress.completed

        db.commit()
        db.refresh(db_progress)

        return db_progress