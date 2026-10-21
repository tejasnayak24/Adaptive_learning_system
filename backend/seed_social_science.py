import os
from pathlib import Path

# =========================================================
# DATABASE CONFIGURATION
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "adaptive_learning.db"

os.environ["DATABASE_URL"] = (
    f"sqlite:///{DATABASE_PATH.as_posix()}"
)

# =========================================================
# IMPORT ALL MODELS
# Register related models before using SQLAlchemy queries.
# =========================================================

from app.database.connection import SessionLocal
from app.models.student import Student
from app.models.lesson import Lesson
from app.models.quiz import Quiz
from app.models.question import Question
from app.models.progress import Progress
from app.models.session import LearningSession
from app.models.reward import RewardHistory


# =========================================================
# SUBJECT CONFIGURATION
# =========================================================

SUBJECT = "Social Science"

DIFFICULTIES = ["Easy", "Medium", "Hard"]

QUESTIONS_PER_DIFFICULTY = 30

LESSON_TOPICS = [
    "Indian Constitution",
    "Understanding Diversity",
    "Diversity and Discrimination",
    "Government and Its Functions",
    "Local Government",
    "Rural Administration",
    "Urban Administration",
    "Rural Livelihoods",
    "Urban Livelihoods",
    "The Indian Parliament",
    "The Judiciary",
    "Understanding Laws",
    "Fundamental Rights and Duties",
    "Secularism",
    "Parliamentary Government",
    "The State Government",
    "Media and Democracy",
    "Markets Around Us",
    "The National Movement",
    "India After Independence",
    "The Delhi Sultanate",
    "The Mughal Empire",
    "Regional Kingdoms of India",
    "The Revolt of 1857",
    "Colonialism and Tribal Societies",
    "India's Freedom Struggle",
    "Resources and Development",
    "Land, Soil and Water Resources",
    "Agriculture in India",
    "Industries",
    "Human Resources",
    "Our Environment",
    "Maps and Globes",
    "Weather and Climate",
    "The Earth and Its Movements",
    "Physical Features of India",
    "The Indian Monsoon",
    "Population and Settlements",
    "Transport and Communication",
    "Sustainable Development",
]


# =========================================================
# LESSON DESCRIPTION
# =========================================================

def make_lesson_description(topic):
    return (
        f"This lesson introduces {topic} as part of Social Science. "
        "Students can study its key concepts, terminology, relevant "
        "examples, historical background where applicable, and "
        "connections to society and everyday life."
    )


# =========================================================
# CREATE OR FIND A LESSON
# =========================================================

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


# =========================================================
# CREATE OR FIND A QUIZ
# =========================================================

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


# =========================================================
# VALIDATE EXISTING QUESTIONS
# =========================================================

def validate_question(question):
    if not question.question.strip():
        raise ValueError("Question text cannot be empty.")

    options = [
        question.option_a,
        question.option_b,
        question.option_c,
        question.option_d,
    ]

    if any(not option.strip() for option in options):
        raise ValueError(
            f"An option is empty for: {question.question}"
        )

    if question.correct_answer not in {"A", "B", "C", "D"}:
        raise ValueError(
            f"Invalid correct answer for: {question.question}"
        )


# =========================================================
# REPORT QUESTION COUNTS
# =========================================================

def report_quiz(db, quiz):
    questions = (
        db.query(Question)
        .filter(Question.quiz_id == quiz.id)
        .all()
    )

    for question in questions:
        validate_question(question)

    count = len(questions)

    print(
        f"{quiz.title}: {count}/{QUESTIONS_PER_DIFFICULTY} "
        "questions"
    )

    if count < QUESTIONS_PER_DIFFICULTY:
        print(
            "  More verified, lesson-specific questions are needed."
        )

    elif count > QUESTIONS_PER_DIFFICULTY:
        print(
            "  This quiz has more than 30 questions; "
            "no existing questions were deleted."
        )

    return count


# =========================================================
# MAIN SEED FUNCTION
# =========================================================

def seed_social_science():
    db = SessionLocal()

    try:
        print("\nConnecting to database...")
        print(f"Database: {DATABASE_PATH}")
        print(f"Subject: {SUBJECT}")
        print(f"Target lessons: {len(LESSON_TOPICS)}")

        for topic in LESSON_TOPICS:
            lesson = create_or_find_lesson(db, topic)

            for difficulty in DIFFICULTIES:
                quiz = create_or_find_quiz(
                    db,
                    lesson,
                    difficulty,
                )

                # Keep all existing questions.
                # Do not create fake or repeated questions.
                report_quiz(db, quiz)

            db.commit()

        print("\n" + "=" * 55)
        print("SOCIAL SCIENCE SUMMARY")
        print("=" * 55)

        total_lessons = 0
        total_quizzes = 0
        total_questions = 0
        quizzes_below_target = 0

        for topic in LESSON_TOPICS:
            lesson = (
                db.query(Lesson)
                .filter(
                    Lesson.title == topic,
                    Lesson.topic == SUBJECT,
                )
                .first()
            )

            if lesson is None:
                continue

            total_lessons += 1

            for difficulty in DIFFICULTIES:
                quiz_title = f"{topic} - {difficulty}"

                quiz = (
                    db.query(Quiz)
                    .filter(
                        Quiz.lesson_id == lesson.id,
                        Quiz.title == quiz_title,
                    )
                    .first()
                )

                if quiz is None:
                    continue

                total_quizzes += 1

                count = (
                    db.query(Question)
                    .filter(Question.quiz_id == quiz.id)
                    .count()
                )

                total_questions += count

                if count < QUESTIONS_PER_DIFFICULTY:
                    quizzes_below_target += 1

        print(f"Lessons created/found: {total_lessons}/40")
        print(f"Quizzes created/found: {total_quizzes}/120")
        print(f"Existing questions: {total_questions}")
        print(f"Target questions: {40 * 3 * 30}")
        print(f"Quizzes below 30 questions: {quizzes_below_target}")
        print("=" * 55)

        print("\nLesson and quiz setup completed.")

    except Exception as error:
        db.rollback()
        print(f"\nSeeding failed: {error}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_social_science()