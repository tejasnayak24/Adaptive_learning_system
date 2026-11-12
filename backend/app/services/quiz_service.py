from sqlalchemy.orm import Session

from app.models.attempt_answer import AttemptAnswer
from app.models.progress import Progress
from app.models.question import Question
from app.models.quiz import Quiz
from app.services.grading_service import GradingResult, grade_answers


def question_to_public_dict(question: Question) -> dict:
    """A question as delivered to students: never includes the answer."""
    return {
        "id": question.id,
        "quiz_id": question.quiz_id,
        "question": question.question,
        "option_a": question.option_a,
        "option_b": question.option_b,
        "option_c": question.option_c,
        "option_d": question.option_d,
    }


def quiz_to_dict(quiz: Quiz) -> dict:
    return {
        "id": quiz.id,
        "lesson_id": quiz.lesson_id,
        "title": quiz.title,
        "difficulty": quiz.difficulty,
    }


class QuizService:

    @staticmethod
    def get_quiz_by_id(
        db: Session,
        quiz_id: int,
    ):
        return db.get(Quiz, quiz_id)

    @staticmethod
    def get_quizzes_by_lesson(
        db: Session,
        lesson_id: int,
    ):
        return (
            db.query(Quiz)
            .filter(Quiz.lesson_id == lesson_id)
            .order_by(Quiz.id)
            .all()
        )

    @staticmethod
    def get_questions_by_quiz(
        db: Session,
        quiz_id: int,
    ):
        return (
            db.query(Question)
            .filter(Question.quiz_id == quiz_id)
            .order_by(Question.id)
            .all()
        )

    @staticmethod
    def start_quiz(
        db: Session,
        quiz_id: int,
    ):
        """Return the quiz and its questions *without* correct answers."""
        quiz = QuizService.get_quiz_by_id(db, quiz_id)

        if not quiz:
            return None

        questions = QuizService.get_questions_by_quiz(db, quiz_id)

        return {
            "quiz": quiz_to_dict(quiz),
            "questions": [question_to_public_dict(q) for q in questions],
        }

    @staticmethod
    def grade_and_record(
        db: Session,
        *,
        student_id: int,
        quiz: Quiz,
        answers: dict[int, str],
        response_time: float,
        hints_used: int,
        attention_score: float | None,
        yawning: bool | None,
        looking_away: bool | None,
        drowsy: bool | None,
    ) -> tuple[Progress, GradingResult]:
        """Grade the answers on the server and store the attempt.

        Raises ``GradingError`` if the answers do not match the quiz.
        The caller commits the transaction.
        """
        questions = QuizService.get_questions_by_quiz(db, quiz.id)
        grading = grade_answers(questions, answers)

        progress = Progress(
            student_id=student_id,
            lesson_id=quiz.lesson_id,
            quiz_id=quiz.id,
            quiz_score=grading.score,
            correct_count=grading.correct_count,
            total_questions=grading.total_questions,
            hints_used=hints_used,
            response_time=response_time,
            attention_score=attention_score,
            yawning=yawning,
            looking_away=looking_away,
            drowsy=drowsy,
            difficulty=quiz.difficulty,
            completed=True,
        )
        db.add(progress)
        db.flush()

        for result in grading.results:
            db.add(
                AttemptAnswer(
                    progress_id=progress.id,
                    question_id=result.question_id,
                    selected_answer=result.selected_answer,
                    correct_answer=result.correct_answer,
                    is_correct=result.is_correct,
                )
            )

        return progress, grading
