import os
import sys
import logging
from pathlib import Path

logging.disable(logging.CRITICAL)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "adaptive_learning.db"

os.environ["DATABASE_URL"] = f"sqlite:///{DATABASE_PATH.as_posix()}"
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from app.database.connection import SessionLocal
from app.models.student import Student
from app.models.lesson import Lesson
from app.models.quiz import Quiz
from app.models.question import Question
from app.models.progress import Progress
from app.models.session import LearningSession
from app.models.reward import RewardHistory


def main():
    db = SessionLocal()

    try:
        lesson = (
            db.query(Lesson)
            .filter(
                Lesson.title == "Resources and Development",
                Lesson.topic == "Social Science",
            )
            .first()
        )

        if not lesson:
            print("ERROR: Lesson not found.")
            return

        quiz = (
            db.query(Quiz)
            .filter(
                Quiz.lesson_id == lesson.id,
                Quiz.difficulty == "Easy",
            )
            .first()
        )

        if not quiz:
            print("ERROR: Easy quiz not found.")
            return

        existing_count = (
            db.query(Question)
            .filter(Question.quiz_id == quiz.id)
            .count()
        )

        if existing_count >= 30:
            print(f"Easy quiz already contains {existing_count} questions.")
            return

        question_text = (
            "Which practice helps conserve natural resources "
            "while reducing unnecessary waste?"
        )

        duplicate = (
            db.query(Question)
            .filter(
                Question.quiz_id == quiz.id,
                Question.question == question_text,
            )
            .first()
        )

        if not duplicate:
            db.add(
                Question(
                    quiz_id=quiz.id,
                    question=question_text,
                    option_a="Reuse and repair useful items",
                    option_b="Throw away reusable materials",
                    option_c="Leave taps running",
                    option_d="Cut trees without replanting",
                    correct_answer="A",
                )
            )
            db.commit()
            print("Added the missing Easy question.")
        else:
            print("The question already exists; no duplicate added.")

        print("\nFINAL VERIFICATION")

        total = 0

        for difficulty in ["Easy", "Medium", "Hard"]:
            current_quiz = (
                db.query(Quiz)
                .filter(
                    Quiz.lesson_id == lesson.id,
                    Quiz.difficulty == difficulty,
                )
                .first()
            )

            count = (
                db.query(Question)
                .filter(Question.quiz_id == current_quiz.id)
                .count()
                if current_quiz
                else 0
            )

            total += count
            print(f"{difficulty}: {count}/30")

        print(f"TOTAL: {total}/90")

        if total == 90:
            print("SUCCESS: Resources and Development is complete!")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()