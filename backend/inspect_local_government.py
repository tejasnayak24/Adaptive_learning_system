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
            Lesson.title == "Local Government",
            Lesson.topic == "Social Science"
        )
        .first()
    )

    if not lesson:
        print("Lesson not found.")
    else:
        print(f"Lesson ID: {lesson.id}")
        print(f"Lesson title: {lesson.title}")

        quizzes = (
            db.query(Quiz)
            .filter(Quiz.lesson_id == lesson.id)
            .all()
        )

        print(f"\nTotal quizzes: {len(quizzes)}")

        for quiz in quizzes:
            count = (
                db.query(Question)
                .filter(Question.quiz_id == quiz.id)
                .count()
            )

            print(
                f"Quiz ID: {quiz.id} | "
                f"Title: {quiz.title} | "
                f"Difficulty: {quiz.difficulty} | "
                f"Questions: {count}"
            )

finally:
    db.close()