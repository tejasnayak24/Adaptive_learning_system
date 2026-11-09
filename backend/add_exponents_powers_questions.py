import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

TOPIC = "Exponents and Powers"
SUBJECT = "Mathematics"

random.seed(42)

EASY = [
    ("What is 2 raised to the power 3?", "8", ["6", "9", "12"]),
    ("What is 3 raised to the power 2?", "9", ["6", "8", "12"]),
    ("What is 5²?", "25", ["10", "15", "20"]),
    ("What is 10³?", "1000", ["100", "300", "10000"]),
    ("What is 4²?", "16", ["8", "12", "24"]),
    ("What is 2⁴?", "16", ["8", "12", "32"]),
    ("What is 6²?", "36", ["12", "18", "30"]),
    ("What is 3³?", "27", ["9", "18", "36"]),
    ("What is 7²?", "49", ["14", "21", "42"]),
    ("What is 1⁵?", "1", ["5", "0", "10"]),
    ("What is 9²?", "81", ["18", "72", "99"]),
    ("What is 10²?", "100", ["10", "20", "1000"]),
    ("What is 2⁵?", "32", ["16", "25", "64"]),
    ("What is 8²?", "64", ["16", "32", "48"]),
    ("What is 5³?", "125", ["25", "75", "100"]),
    ("What is 4³?", "64", ["16", "32", "48"]),
    ("What is 3⁴?", "81", ["27", "64", "12"]),
    ("What is 10⁴?", "10000", ["100", "1000", "100000"]),
    ("What is the base in 5³?", "5", ["3", "15", "8"]),
    ("What is the exponent in 7⁴?", "4", ["7", "28", "11"]),
    ("What is 12¹?", "12", ["1", "0", "24"]),
    ("What is 15⁰?", "1", ["0", "15", "15⁰"]),
    ("What is 2⁰?", "1", ["0", "2", "4"]),
    ("What is 6³?", "216", ["36", "108", "126"]),
    ("What is 11²?", "121", ["22", "111", "131"]),
    ("What is 12²?", "144", ["124", "134", "154"]),
    ("What is 2⁶?", "64", ["32", "16", "128"]),
    ("What is 3⁵?", "243", ["81", "125", "729"]),
    ("What is 7³?", "343", ["49", "147", "441"]),
    ("What is 1⁰?", "1", ["0", "10", "Undefined"]),
]

MEDIUM = [
    ("Simplify 2³ × 2².", "32", ["16", "64", "128"]),
    ("Simplify 3² × 3³.", "243", ["81", "729", "27"]),
    ("Simplify 5⁴ ÷ 5².", "25", ["125", "625", "5"]),
    ("Simplify 2⁶ ÷ 2³.", "8", ["4", "16", "32"]),
    ("Simplify 4² × 4³.", "1024", ["256", "512", "2048"]),
    ("Simplify 10⁵ ÷ 10².", "1000", ["100", "10000", "100000"]),
    ("What is the value of (2³)²?", "64", ["16", "32", "128"]),
    ("What is the value of (3²)³?", "729", ["81", "243", "6561"]),
    ("Simplify 7⁴ ÷ 7².", "49", ["343", "2401", "7"]),
    ("Simplify 6² × 6¹.", "216", ["36", "72", "1296"]),
    ("Express 1000 as a power of 10.", "10³", ["10²", "10⁴", "10⁵"]),
    ("Express 81 as a power of 3.", "3⁴", ["3²", "3³", "3⁵"]),
    ("Express 64 as a power of 2.", "2⁶", ["2⁴", "2⁵", "2⁷"]),
    ("Simplify 5³ × 5⁰.", "125", ["25", "625", "1"]),
    ("Simplify 9⁴ ÷ 9³.", "9", ["81", "729", "1"]),
    ("What is the value of 2³ + 3²?", "17", ["15", "18", "25"]),
    ("What is the value of 5² - 2³?", "17", ["15", "18", "21"]),
    ("Simplify 3⁴ × 3².", "729", ["243", "81", "2187"]),
    ("Simplify 8³ ÷ 8².", "8", ["64", "512", "1"]),
    ("What is the value of (5²)²?", "625", ["125", "100", "250"]),
    ("Express 125 as a power of 5.", "5³", ["5²", "5⁴", "5⁵"]),
    ("Express 256 as a power of 4.", "4⁴", ["4²", "4³", "4⁵"]),
    ("Simplify 2⁴ × 2³ ÷ 2².", "32", ["16", "64", "128"]),
    ("Simplify 10³ × 10².", "100000", ["1000", "10000", "1000000"]),
    ("What is the value of 4³ + 2⁴?", "80", ["64", "72", "96"]),
    ("What is the value of 3³ × 2²?", "108", ["81", "96", "120"]),
    ("Simplify 11³ ÷ 11².", "11", ["121", "1331", "1"]),
    ("What is the value of (2 × 3)²?", "36", ["12", "18", "24"]),
    ("Simplify 4⁵ ÷ 4³.", "16", ["4", "64", "256"]),
    ("What is the value of 2⁴ + 2⁵?", "48", ["32", "40", "64"]),
]

HARD = [
    ("Simplify 2⁵ × 2³ ÷ 2⁴.", "16", ["8", "32", "64"]),
    ("Simplify 3⁶ ÷ 3² × 3¹.", "243", ["81", "729", "27"]),
    ("Simplify (2³ × 2²)².", "1024", ["256", "512", "2048"]),
    ("Simplify (5²)³ ÷ 5⁴.", "25", ["125", "625", "5"]),
    ("Find the value of 2⁴ × 3².", "144", ["96", "128", "162"]),
    ("Find the value of 5³ + 2⁵.", "157", ["145", "165", "175"]),
    ("Find the value of 3⁴ - 2⁵.", "49", ["41", "51", "59"]),
    ("Simplify 10⁶ ÷ 10³ × 10².", "100000", ["10000", "1000000", "1000"]),
    ("If 2ˣ = 32, find x.", "5", ["4", "6", "8"]),
    ("If 3ˣ = 81, find x.", "4", ["3", "5", "6"]),
    ("If 5ˣ = 625, find x.", "4", ["2", "3", "5"]),
    ("If 10ˣ = 100000, find x.", "5", ["3", "4", "6"]),
    ("Simplify (3²)² × 3.", "243", ["81", "729", "27"]),
    ("Simplify 4³ × 2².", "256", ["128", "64", "512"]),
    ("Simplify 2⁷ ÷ 2³ × 2².", "64", ["16", "32", "128"]),
    ("Find the value of (2² + 3²)².", "169", ["81", "121", "196"]),
    ("Simplify 6⁴ ÷ 6² × 6.", "216", ["36", "1296", "72"]),
    ("Express 729 as a power of 3.", "3⁶", ["3⁴", "3⁵", "3⁷"]),
    ("Express 1024 as a power of 2.", "2¹⁰", ["2⁸", "2⁹", "2¹¹"]),
    ("Simplify (2⁴)³ ÷ 2⁸.", "256", ["64", "128", "512"]),
    ("Find the value of 7² × 7³ ÷ 7⁴.", "7", ["49", "343", "1"]),
    ("Find the value of 2⁵ + 3³ × 2.", "86", ["72", "80", "96"]),
    ("Simplify 5⁶ ÷ (5² × 5²).", "25", ["5", "125", "625"]),
    ("If 4ˣ = 256, find x.", "4", ["3", "5", "6"]),
    ("Find the value of (10²)³ ÷ 10⁴.", "100", ["10", "1000", "10000"]),
    ("Simplify 3³ × 9².", "2187", ["729", "6561", "243"]),
    ("Simplify 2⁸ ÷ 4².", "16", ["8", "32", "64"]),
    ("Find the value of 5² × 2³.", "200", ["100", "150", "250"]),
    ("Simplify (3 × 2)³.", "216", ["36", "108", "512"]),
    ("Find the value of 2⁶ + 4³ - 3².", "119", ["109", "127", "135"]),
]


def make_questions(data):
    questions = []

    for question, answer, wrong_answers in data:
        options = [answer] + wrong_answers[:]
        random.shuffle(options)

        correct_answer = ["A", "B", "C", "D"][options.index(answer)]

        questions.append((
            question,
            options[0],
            options[1],
            options[2],
            options[3],
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
    total_inserted = 0

    difficulty_data = {
        "Easy": EASY,
        "Medium": MEDIUM,
        "Hard": HARD
    }

    for difficulty, data in difficulty_data.items():
        cursor.execute(
            """
            SELECT id FROM quizzes
            WHERE lesson_id = ? AND LOWER(difficulty) = LOWER(?)
            """,
            (lesson_id, difficulty)
        )

        quiz = cursor.fetchone()

        if not quiz:
            print(f"{difficulty} quiz not found for {TOPIC}")
            continue

        quiz_id = quiz[0]
        questions = make_questions(data)
        inserted = 0

        for q in questions:
            cursor.execute(
                "SELECT 1 FROM questions WHERE quiz_id = ? AND question = ?",
                (quiz_id, q[0])
            )

            if cursor.fetchone():
                continue

            cursor.execute(
                """
                INSERT INTO questions
                (quiz_id, question, option_a, option_b,
                 option_c, option_d, correct_answer)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (quiz_id, *q)
            )

            inserted += 1

        total_inserted += inserted
        print(f"{difficulty}: {inserted} questions inserted.")

    conn.commit()
    conn.close()

    print(f"\nCompleted! Total new questions inserted: {total_inserted}")


if __name__ == "__main__":
    main()