import logging
from pathlib import Path
import os

logging.disable(logging.CRITICAL)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "adaptive_learning.db"

os.environ["DATABASE_URL"] = f"sqlite:///{DATABASE_PATH.as_posix()}"

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
                Lesson.title == "Understanding Diversity",
                Lesson.topic == "Social Science",
            )
            .first()
        )

        if lesson is None:
            print("Understanding Diversity lesson not found.")
            return

        total = 0

        for difficulty in ["Easy", "Medium", "Hard"]:
            quiz = (
                db.query(Quiz)
                .filter(
                    Quiz.lesson_id == lesson.id,
                    Quiz.title == f"Understanding Diversity - {difficulty}",
                )
                .first()
            )

            if quiz is None:
                print(f"{difficulty}: QUIZ NOT FOUND")
                continue

            count = (
                db.query(Question)
                .filter(Question.quiz_id == quiz.id)
                .count()
            )

            total += count
            print(f"{difficulty}: {count}/30 questions")

        print("------------------------------")
        print(f"TOTAL: {total}/90 questions")

    finally:
        db.close()


if __name__ == "__main__":
    main()