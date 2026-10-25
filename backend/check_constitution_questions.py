import logging
from pathlib import Path
import os

# Disable detailed SQLAlchemy logs
logging.disable(logging.CRITICAL)

# Set the project root and database path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "adaptive_learning.db"

os.environ["DATABASE_URL"] = f"sqlite:///{DATABASE_PATH.as_posix()}"

# Import database and models
from app.database.connection import SessionLocal
from app.models.student import Student
from app.models.lesson import Lesson
from app.models.quiz import Quiz
from app.models.question import Question
from app.models.progress import Progress
from app.models.session import LearningSession
from app.models.reward import RewardHistory


def check_constitution_questions():
    db = SessionLocal()

    try:
        # Find the Indian Constitution lesson
        lesson = (
            db.query(Lesson)
            .filter(
                Lesson.title == "Indian Constitution",
                Lesson.topic == "Social Science",
            )
            .first()
        )

        if lesson is None:
            print("Indian Constitution lesson not found.")
            return

        total_questions = 0

        print("\n========== INDIAN CONSTITUTION QUESTION CHECK ==========\n")

        # Check each difficulty level
        for difficulty in ["Easy", "Medium", "Hard"]:
            quiz_title = f"Indian Constitution - {difficulty}"

            quiz = (
                db.query(Quiz)
                .filter(
                    Quiz.lesson_id == lesson.id,
                    Quiz.title == quiz_title,
                )
                .first()
            )

            if quiz is None:
                print(f"{difficulty}: QUIZ NOT FOUND")
                continue

            question_count = (
                db.query(Question)
                .filter(Question.quiz_id == quiz.id)
                .count()
            )

            total_questions += question_count

            print(f"{difficulty}: {question_count}/30 questions")

        print("-----------------------------------------")
        print(f"TOTAL: {total_questions}/90 questions")
        print("=========================================\n")

    except Exception as error:
        print(f"Error checking questions: {error}")

    finally:
        db.close()


if __name__ == "__main__":
    check_constitution_questions()