import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "adaptive_learning.db"

os.environ["DATABASE_URL"] = (
    f"sqlite:///{DATABASE_PATH.as_posix()}"
)

from app.database.connection import SessionLocal
from app.models.lesson import Lesson
from app.models.quiz import Quiz
from app.models.question import Question
from app.models.student import Student
from app.models.progress import Progress
from app.models.session import LearningSession
from app.models.reward import RewardHistory

SUBJECT = "Mathematics"

DIFFICULTIES = ["Easy", "Medium", "Hard"]

QUESTIONS_PER_DIFFICULTY = 30

LESSON_TOPICS = [
    "Number Systems",
    "Natural Numbers and Whole Numbers",
    "Integers",
    "Fractions",
    "Decimals",
    "Rational Numbers",
    "Factors and Multiples",
    "HCF and LCM",
    "Divisibility Rules",
    "Squares and Square Roots",
    "Cubes and Cube Roots",
    "Exponents and Powers",
    "Simplification",
    "Ratio and Proportion",
    "Unitary Method",
    "Percentages",
    "Profit and Loss",
    "Discount",
    "Simple Interest",
    "Algebraic Expressions",
    "Linear Equations",
    "Introduction to Polynomials",
    "Algebraic Identities",
    "Sequences and Patterns",
    "Lines and Angles",
    "Triangles",
    "Quadrilaterals",
    "Polygons",
    "Circles",
    "Symmetry",
    "Perimeter",
    "Area of Plane Figures",
    "Surface Area",
    "Volume",
    "Coordinate Geometry",
    "Data Handling",
    "Mean, Median and Mode",
    "Bar Graphs and Pie Charts",
    "Probability",
    "Practical Mathematics and Word Problems",
]


def make_lesson_description(topic):
    return (
        f"This lesson introduces {topic} as part of Mathematics. "
        "Students will learn important mathematical concepts, "
        "formulas, calculations and practical applications."
    )


def create_or_find_lesson(db, topic):
    lesson = (
        db.query(Lesson)
        .filter(
            Lesson.title == topic,
            Lesson.topic == SUBJECT,
        )
        .first()
    )

    if lesson is None:
        lesson = Lesson(
            title=topic,
            topic=SUBJECT,
            difficulty="Easy",
            content=make_lesson_description(topic),
        )

        db.add(lesson)
        db.flush()

        print(f"Created lesson: {topic}")
    else:
        print(f"Lesson already exists: {topic}")

    return lesson


def create_or_find_quiz(db, lesson, difficulty):
    quiz_title = f"{lesson.title} - {difficulty}"

    quiz = (
        db.query(Quiz)
        .filter(
            Quiz.lesson_id == lesson.id,
            Quiz.title == quiz_title,
        )
        .first()
    )

    if quiz is None:
        quiz = Quiz(
            lesson_id=lesson.id,
            title=quiz_title,
            difficulty=difficulty,
        )

        db.add(quiz)
        db.flush()

        print(f"Created quiz: {quiz_title}")

    return quiz


def seed_maths():
    db = SessionLocal()

    try:
        print("\nConnecting to database...")
        print(f"Database: {DATABASE_PATH}")
        print(f"Subject: {SUBJECT}")

        for topic in LESSON_TOPICS:
            lesson = create_or_find_lesson(db, topic)

            for difficulty in DIFFICULTIES:
                create_or_find_quiz(
                    db,
                    lesson,
                    difficulty,
                )

            db.commit()

        total_lessons = (
            db.query(Lesson)
            .filter(Lesson.topic == SUBJECT)
            .count()
        )

        total_quizzes = (
            db.query(Quiz)
            .join(Lesson)
            .filter(Lesson.topic == SUBJECT)
            .count()
        )

        total_questions = (
            db.query(Question)
            .join(Quiz)
            .join(Lesson)
            .filter(Lesson.topic == SUBJECT)
            .count()
        )

        print("\n========== MATHEMATICS SUMMARY ==========")
        print(f"Lessons: {total_lessons}/40")
        print(f"Quizzes: {total_quizzes}/120")
        print(f"Existing questions: {total_questions}")
        print(f"Target questions: {40 * 3 * 30}")
        print("=========================================")

    except Exception as error:
        db.rollback()
        print(f"Seeding failed: {error}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_maths()