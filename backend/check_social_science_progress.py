import os
import logging
from pathlib import Path

logging.disable(logging.CRITICAL)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "adaptive_learning.db"

os.environ["DATABASE_URL"] = (
    f"sqlite:///{DATABASE_PATH.as_posix()}"
)

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
    lessons = (
        db.query(Lesson)
        .filter(Lesson.topic == "Social Science")
        .order_by(Lesson.id)
        .all()
    )

    total_questions = 0

    print("\n========== SOCIAL SCIENCE PROGRESS ==========\n")

    for lesson in lessons:
        print(f"\n{lesson.title}")

        lesson_total = 0

        for difficulty in ["Easy", "Medium", "Hard"]:
            quiz = (
                db.query(Quiz)
                .filter(
                    Quiz.lesson_id == lesson.id,
                    Quiz.difficulty == difficulty,
                )
                .first()
            )

            count = (
                db.query(Question)
                .filter(Question.quiz_id == quiz.id)
                .count()
                if quiz
                else 0
            )

            lesson_total += count
            print(f"  {difficulty}: {count}/30")

        total_questions += lesson_total
        print(f"  Lesson total: {lesson_total}/90")

    print("\n========== FINAL TOTALS ==========")
    print(f"Lessons found: {len(lessons)}/40")
    print(f"Questions found: {total_questions}/3600")

    if len(lessons) == 40 and total_questions == 3600:
        print("\nSUCCESS: All 40 lessons contain 3,600 questions!")
    else:
        print("\nSome lessons or questions may still be missing.")

finally:
    db.close()