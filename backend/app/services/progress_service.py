from sqlalchemy.orm import Session

from app.models.progress import Progress
from app.schemas.progress import ProgressUpdate


class ProgressService:

    @staticmethod
    def get_progress_by_id(db: Session, progress_id: int):
        return db.get(Progress, progress_id)

    @staticmethod
    def get_student_progress(db: Session, student_id: int):
        return (
            db.query(Progress)
            .filter(Progress.student_id == student_id)
            .order_by(Progress.id)
            .all()
        )

    @staticmethod
    def get_lesson_progress(
        db: Session,
        student_id: int,
        lesson_id: int,
    ):
        # Most recent attempt for the lesson.
        return (
            db.query(Progress)
            .filter(
                Progress.student_id == student_id,
                Progress.lesson_id == lesson_id,
            )
            .order_by(Progress.id.desc())
            .first()
        )

    @staticmethod
    def update_progress(
        db: Session,
        progress_id: int,
        progress: ProgressUpdate,
    ):
        db_progress = ProgressService.get_progress_by_id(db, progress_id)

        if db_progress is None:
            return None

        db_progress.quiz_score = progress.quiz_score
        db_progress.response_time = progress.response_time
        db_progress.attention_score = progress.attention_score
        db_progress.yawning = progress.yawning
        db_progress.looking_away = progress.looking_away
        db_progress.difficulty = progress.difficulty
        db_progress.completed = progress.completed

        db.commit()
        db.refresh(db_progress)

        return db_progress
