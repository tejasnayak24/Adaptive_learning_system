from sqlalchemy.orm import Session

from app.models.quiz import Quiz
from app.models.question import Question
from app.models.progress import StudentProgress


class QuizService:

    @staticmethod
    def get_quiz_by_id(
        db: Session,
        quiz_id: int,
    ):
        return (
            db.query(Quiz)
            .filter(Quiz.id == quiz_id)
            .first()
        )

    @staticmethod
    def get_questions_by_quiz(
        db: Session,
        quiz_id: int,
    ):
        return (
            db.query(Question)
            .filter(Question.quiz_id == quiz_id)
            .all()
        )

    @staticmethod
    def start_quiz(
        db: Session,
        quiz_id: int,
    ):
        quiz = QuizService.get_quiz_by_id(
            db,
            quiz_id,
        )

        if not quiz:
            return None

        questions = QuizService.get_questions_by_quiz(
            db,
            quiz_id,
        )

        return {
            "quiz": quiz,
            "questions": questions,
        }

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
        progress = StudentProgress(
            student_id=student_id,
            lesson_id=lesson_id,
            quiz_score=quiz_score,
            response_time=response_time,
            attention_score=attention_score,
            difficulty=difficulty,
            completed=True,
        )

        db.add(progress)
        db.commit()
        db.refresh(progress)

        return progress