
import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

TOPIC = "Simplification"
SUBJECT = "Mathematics"

random.seed(42)

EASY = [
    "10 + 5", "20 - 8", "6 * 4", "36 / 6", "15 + 12",
    "30 - 14", "8 * 5", "48 / 8", "25 + 17", "50 - 23",
    "9 * 7", "72 / 9", "40 + 35", "80 - 45", "12 * 6",
    "100 / 10", "18 + 24", "65 - 28", "7 * 8", "81 / 9",
    "45 + 36", "90 - 55", "11 * 9", "96 / 12", "125 - 50",
    "14 * 5", "144 / 12", "55 + 29", "100 - 37", "13 * 6"
]

MEDIUM = [
    "10 + 5 * 2", "(20 + 10) / 5", "40 - 6 * 4",
    "8 * 5 + 12", "100 / 5 - 8", "25 + 36 / 6",
    "(15 + 9) * 2", "80 - 24 / 4", "12 * 3 - 15",
    "96 / 8 + 17", "50 + 5 * 6", "(60 - 20) / 4",
    "7 * 8 + 16", "120 / 6 - 5", "45 - 3 * 9",
    "(18 + 12) / 3", "9 * 7 - 23", "150 / 5 + 12",
    "64 / 8 * 3", "100 - 8 * 7", "15 + 45 / 9",
    "(35 + 25) / 5", "11 * 6 - 18", "144 / 12 + 28",
    "90 - 5 * 12", "16 * 4 - 25", "200 / 10 + 15",
    "(72 - 24) / 6", "13 * 5 + 20", "180 / 9 - 7"
]

HARD = [
    "120 - (15 + 5) * 4", "240 / (8 * 3) + 15",
    "45 + 6 * (18 - 10)", "(150 - 30) / 5 + 12",
    "200 - 8 * (12 + 3)", "360 / 12 + 7 * 5",
    "(80 + 40) / 6 * 3", "500 - (25 * 8 + 40)",
    "18 * (15 - 7) + 24", "420 / (7 * 5) + 16",
    "300 / 10 - 4 * 6", "(125 + 75) / 8 + 10",
    "15 * 4 + 180 / 9", "600 - 12 * (25 + 5)",
    "(96 / 8 + 14) * 3", "250 / 5 - 6 * 7",
    "32 * 5 - (120 / 4)", "480 / (12 + 8) * 5",
    "75 + 9 * (20 - 12)", "(400 - 100) / 15 + 8",
    "24 * 6 - 144 / 8", "700 / 10 - (8 * 4)",
    "(45 + 35) * 2 / 8", "900 - 15 * (20 + 10)",
    "16 * (30 - 18) + 50", "540 / 9 - 7 * 6",
    "(200 + 100) / 12 * 4", "85 + 5 * (40 - 22)",
    "1000 / 20 + 12 * 3", "600 - (240 / 6 + 35)"
]


def generate_questions(expressions):
    questions = []

    for expression in expressions:
        answer = eval(expression)

        if isinstance(answer, float) and answer.is_integer():
            answer = int(answer)

        if not isinstance(answer, int):
            raise ValueError(f"Non-integer answer: {expression}")

        wrong_options = []
        candidates = [
            answer + 1,
            answer - 1,
            answer + 2,
            answer - 2,
            answer + 10,
            answer * 2,
            answer + 5,
            answer - 5
        ]

        for candidate in candidates:
            if candidate != answer and candidate not in wrong_options:
                wrong_options.append(candidate)

            if len(wrong_options) == 3:
                break

        options = [answer] + wrong_options
        random.shuffle(options)

        correct_answer = ["A", "B", "C", "D"][options.index(answer)]

        questions.append((
            f"Simplify: {expression}",
            str(options[0]),
            str(options[1]),
            str(options[2]),
            str(options[3]),
            correct_answer
        ))

    return questions


def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM lessons WHERE title = ? AND topic = ?",
        (TOPIC, SUBJECT)
    )

    lesson = cursor.fetchone()

    if not lesson:
        print(f"Lesson not found: {TOPIC}")
        conn.close()
        return

    lesson_id = lesson[0]

    difficulty_data = {
        "Easy": EASY,
        "Medium": MEDIUM,
        "Hard": HARD
    }

    total_inserted = 0

    for difficulty, expressions in difficulty_data.items():

        cursor.execute("""
            SELECT id FROM quizzes
            WHERE lesson_id = ?
            AND LOWER(difficulty) = LOWER(?)
        """, (lesson_id, difficulty))

        quiz = cursor.fetchone()

        if not quiz:
            print(f"{difficulty} quiz not found!")
            continue

        quiz_id = quiz[0]
        questions = generate_questions(expressions)

        inserted = 0

        for question in questions:

            cursor.execute("""
                SELECT 1 FROM questions
                WHERE quiz_id = ? AND question = ?
            """, (quiz_id, question[0]))

            if cursor.fetchone():
                continue

            cursor.execute("""
                INSERT INTO questions
                (
                    quiz_id,
                    question,
                    option_a,
                    option_b,
                    option_c,
                    option_d,
                    correct_answer
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (quiz_id, *question))

            inserted += 1

        total_inserted += inserted

        print(f"{difficulty}: {inserted} questions inserted.")

    conn.commit()
    conn.close()

    print(f"\nCompleted! Total new questions inserted: {total_inserted}")


if __name__ == "__main__":
    main()
