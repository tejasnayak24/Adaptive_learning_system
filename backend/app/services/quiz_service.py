from sqlalchemy.orm import Session

from app.models.quiz import Quiz
from app.models.question import Question
from app.models.progress import Progress


class QuizService:

    @staticmethod
    def start_quiz(db: Session, quiz_id: int):
        quiz = (
            db.query(Quiz)
            .filter(Quiz.id == quiz_id)
            .first()
        )

        if quiz is None:
            return None

        questions = (
            db.query(Question)
            .filter(Question.quiz_id == quiz_id)
            .order_by(Question.id)
            .all()
        )

        return {
            "quiz": quiz,
            "questions": questions,
        }

    @staticmethod
    def get_quizzes_by_lesson(db: Session, lesson_id: int):
        return (
            db.query(Quiz)
            .filter(Quiz.lesson_id == lesson_id)
            .order_by(Quiz.id)
            .all()
        )

    @staticmethod
    def submit_quiz(
        db: Session,
        student_id: int,
        lesson_id: int,
        quiz_score: float,
        response_time: float,
        attention_score: float,
        difficulty: str,
    ):
        progress = Progress(
            student_id=student_id,
            lesson_id=lesson_id,
            quiz_score=quiz_score,
            response_time=response_time,
            attention_score=attention_score,
            difficulty=difficulty,
            completed=True,
        )

        try:
            db.add(progress)
            db.commit()
            db.refresh(progress)
            return progress

        except Exception:
            db.rollback()
            raise