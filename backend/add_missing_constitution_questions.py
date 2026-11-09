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


NEW_QUESTIONS = [
    {
        "question": "Which document contains the basic rules for governing India?",
        "option_a": "The Constitution",
        "option_b": "A school textbook",
        "option_c": "A newspaper",
        "option_d": "A travel guide",
        "correct_answer": "A",
    },
    {
        "question": "What is the national law-making body of India called?",
        "option_a": "Election Commission",
        "option_b": "Parliament",
        "option_c": "Supreme Court",
        "option_d": "Planning Commission",
        "correct_answer": "B",
    },
    {
        "question": "Which of these is a fundamental right guaranteed by the Indian Constitution?",
        "option_a": "The right to ignore all laws",
        "option_b": "The right to avoid every tax",
        "option_c": "The right to equality",
        "option_d": "The right to make personal laws for everyone",
        "correct_answer": "C",
    },
]


def add_missing_questions():
    db = SessionLocal()

    try:
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

        quiz = (
            db.query(Quiz)
            .filter(
                Quiz.lesson_id == lesson.id,
                Quiz.title == "Indian Constitution - Easy",
            )
            .first()
        )

        if quiz is None:
            print("Easy quiz not found.")
            return

        existing_count = (
            db.query(Question)
            .filter(Question.quiz_id == quiz.id)
            .count()
        )

        print(f"Existing Easy questions: {existing_count}/30")

        if existing_count >= 30:
            print("Easy quiz already has 30 questions. Nothing added.")
            return

        added = 0

        for item in NEW_QUESTIONS:
            if existing_count + added >= 30:
                break

            # Prevent duplicate question text within this quiz.
            duplicate = (
                db.query(Question)
                .filter(
                    Question.quiz_id == quiz.id,
                    Question.question == item["question"],
                )
                .first()
            )

            if duplicate:
                continue

            question = Question(
                quiz_id=quiz.id,
                question=item["question"],
                option_a=item["option_a"],
                option_b=item["option_b"],
                option_c=item["option_c"],
                option_d=item["option_d"],
                correct_answer=item["correct_answer"],
            )

            db.add(question)
            added += 1

        db.commit()

        final_count = (
            db.query(Question)
            .filter(Question.quiz_id == quiz.id)
            .count()
        )

        print(f"Questions added: {added}")
        print(f"Final Easy count: {final_count}/30")

    except Exception as error:
        db.rollback()
        print(f"Error: {error}")

    finally:
        db.close()


if __name__ == "__main__":
    add_missing_questions()