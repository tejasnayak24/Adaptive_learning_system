import os
import logging
from pathlib import Path

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

db = SessionLocal()

try:
    lesson = (
        db.query(Lesson)
        .filter(
            Lesson.title == "The Indian Parliament",
            Lesson.topic == "Social Science"
        )
        .first()
    )

    if not lesson:
        print("The Indian Parliament lesson was not found.")
    else:
        print(f"Lesson found: {lesson.title} (ID: {lesson.id})")
        total = 0

        for difficulty in ["Easy", "Medium", "Hard"]:
            quiz = (
                db.query(Quiz)
                .filter(
                    Quiz.lesson_id == lesson.id,
                    Quiz.difficulty == difficulty
                )
                .first()
            )

            count = (
                db.query(Question)
                .filter(Question.quiz_id == quiz.id)
                .count()
                if quiz else 0
            )

            total += count
            print(f"{difficulty}: {count}/30 questions")

        print(f"\nTotal: {total}/90 questions")

finally:
    db.close()