
import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

TOPIC = "Linear Equations"
SUBJECT = "Mathematics"

random.seed(42)

# Format: (question, correct answer, [three wrong answers])

EASY = [
    ("Solve: x + 5 = 12", "7", ["5", "6", "8"]),
    ("Solve: x - 4 = 9", "13", ["5", "12", "14"]),
    ("Solve: 2x = 14", "7", ["6", "8", "9"]),
    ("Solve: 3x = 21", "7", ["6", "8", "9"]),
    ("Solve: x/2 = 6", "12", ["10", "8", "14"]),
    ("Solve: x + 8 = 15", "7", ["6", "8", "9"]),
    ("Solve: x - 7 = 5", "12", ["11", "13", "2"]),
    ("Solve: 4x = 20", "5", ["4", "6", "10"]),
    ("Solve: 5x = 35", "7", ["5", "6", "8"]),
    ("Solve: x/3 = 4", "12", ["7", "9", "15"]),
    ("Solve: 2x + 3 = 11", "4", ["3", "5", "7"]),
    ("Solve: 3x - 2 = 13", "5", ["4", "6", "3"]),
    ("Solve: 5x + 5 = 30", "5", ["4", "6", "7"]),
    ("Solve: 4x - 4 = 12", "4", ["3", "5", "6"]),
    ("Solve: x + 10 = 18", "8", ["6", "7", "9"]),
    ("Solve: 6x = 42", "7", ["6", "8", "9"]),
    ("Solve: x/4 = 5", "20", ["15", "16", "25"]),
    ("Solve: 2x - 6 = 10", "8", ["6", "7", "9"]),
    ("Solve: 7x = 49", "7", ["5", "6", "8"]),
    ("Solve: x - 12 = 3", "15", ["9", "14", "16"]),
    ("Solve: 3x + 4 = 19", "5", ["4", "6", "7"]),
    ("Solve: 8x = 64", "8", ["6", "7", "9"]),
    ("Solve: x/5 = 3", "15", ["10", "12", "20"]),
    ("Solve: 4x + 2 = 18", "4", ["3", "5", "6"]),
    ("Solve: 5x - 10 = 15", "5", ["4", "6", "7"]),
    ("Solve: x + 6 = 20", "14", ["12", "13", "15"]),
    ("Solve: 9x = 81", "9", ["7", "8", "10"]),
    ("Solve: 2x + 8 = 20", "6", ["4", "5", "8"]),
    ("Solve: 6x - 3 = 21", "4", ["3", "5", "6"]),
    ("Solve: x/6 = 4", "24", ["18", "20", "30"]),
]

MEDIUM = [
    ("Solve: 3x + 5 = 2x + 12", "7", ["5", "6", "8"]),
    ("Solve: 5x - 4 = 3x + 10", "7", ["6", "8", "9"]),
    ("Solve: 2(x + 3) = 16", "5", ["4", "6", "8"]),
    ("Solve: 3(x - 2) = 15", "7", ["5", "6", "8"]),
    ("Solve: 4(x + 1) = 20", "4", ["3", "5", "6"]),
    ("Solve: 2x + 7 = 5x - 8", "5", ["4", "6", "7"]),
    ("Solve: 6x - 5 = 4x + 9", "7", ["6", "8", "9"]),
    ("Solve: 5(x - 1) = 20", "5", ["4", "6", "7"]),
    ("Solve: 2(x + 4) = 3x + 1", "7", ["5", "6", "8"]),
    ("Solve: 7x + 3 = 4x + 18", "5", ["4", "6", "7"]),
    ("Solve: (x + 5)/2 = 6", "7", ["5", "6", "8"]),
    ("Solve: (2x - 3)/3 = 5", "9", ["6", "8", "10"]),
    ("Solve: 4x + 6 = 2x + 20", "7", ["5", "6", "8"]),
    ("Solve: 3(x + 2) = 2x + 11", "5", ["4", "6", "7"]),
    ("Solve: 8x - 7 = 5x + 8", "5", ["4", "6", "7"]),
    ("Solve: 2(3x - 1) = 16", "3", ["2", "4", "5"]),
    ("Solve: 5(x + 2) = 3x + 18", "4", ["3", "5", "6"]),
    ("Solve: 9x - 4 = 7x + 10", "7", ["6", "8", "9"]),
    ("Solve: (x - 3)/4 = 2", "11", ["7", "9", "12"]),
    ("Solve: 3x + 2 = 2(x + 6)", "10", ["8", "9", "11"]),
    ("Solve: 4(x - 2) = 2x + 6", "7", ["5", "6", "8"]),
    ("Solve: 7(x + 1) = 5x + 17", "5", ["4", "6", "7"]),
    ("Solve: 2x/5 = 6", "15", ["10", "12", "18"]),
    ("Solve: (3x + 2)/2 = 10", "6", ["4", "5", "8"]),
    ("Solve: 6(x - 1) = 3x + 12", "6", ["4", "5", "7"]),
    ("Solve: 5x + 9 = 2x + 24", "5", ["3", "4", "6"]),
    ("Solve: 2(x - 5) + 3 = 9", "8", ["6", "7", "9"]),
    ("Solve: 4x - 3 = 2(x + 5)", "6.5", ["5.5", "6", "7"]),
    ("Solve: 3(x + 4) - 2 = 19", "3", ["4", "5", "6"]),
    ("Solve: 5(2x - 1) = 35", "4", ["3", "5", "6"]),
]

HARD = [
    ("Solve: 3(2x - 5) = 2(x + 7)", "6.5", ["5.5", "6", "7.5"]),
    ("Solve: 4(2x + 3) - 5 = 3x + 20", "3", ["2", "4", "5"]),
    ("Solve: 5(x - 2) + 3 = 2(x + 4)", "5", ["4", "6", "7"]),
    ("Solve: 2(3x + 4) - 5(x - 1) = 14", "1", ["2", "3", "4"]),
    ("Solve: (2x + 3)/5 = 3", "6", ["5", "7", "8"]),
    ("Solve: (3x - 2)/4 = 4", "6", ["5", "7", "8"]),
    ("Solve: 7(x - 2) - 3(x + 1) = 13", "9", ["7", "8", "10"]),
    ("Solve: 5(2x + 1) - 3(x - 4) = 32", "3", ["2", "4", "5"]),
    ("Solve: 3(x + 5) - 2(2x - 1) = 14", "5", ["4", "6", "7"]),
    ("Solve: (x + 2)/3 + 2 = 5", "7", ["6", "8", "9"]),
    ("Solve: (2x - 1)/3 = (x + 2)/2", "8", ["6", "7", "9"]),
    ("Solve: 4x - 2(3x - 5) = 12", " -1", ["1", "2", "-2"]),
    ("Solve: 6(x - 2) + 4 = 2(2x + 1)", "5", ["4", "6", "7"]),
    ("Solve: 3(2x + 1) - 4(x - 2) = 17", "3", ["2", "4", "5"]),
    ("Solve: (x - 4)/2 + (x + 2)/3 = 5", "8", ["6", "7", "9"]),
    ("Solve: 2(4x - 3) = 5(x + 2) + 1", "7", ["5", "6", "8"]),
    ("Solve: 5x - 2(2x + 3) = 9", "15", ["12", "14", "16"]),
    ("Solve: 3(x - 2) + 4(x + 1) = 29", "5", ["4", "6", "7"]),
    ("Solve: (3x + 1)/2 - 2 = 5", "3", ["4", "5", "6"]),
    ("Solve: 4(x + 3) - 2(2x - 1) = 14", "0", ["1", "2", "3"]),
    ("Solve: 2(x + 5)/3 = 8", "7", ["5", "6", "9"]),
    ("Solve: 5(3x - 2) - 4(x + 1) = 24", "6", ["4", "5", "7"]),
    ("Solve: (2x + 5)/3 + (x - 1)/2 = 7", "5", ["4", "6", "7"]),
    ("Solve: 7 - 2(3x - 1) = 3x - 8", "3", ["2", "4", "5"]),
    ("Solve: 4(2x - 1) - 3(x + 2) = 11", "5", ["3", "4", "6"]),
    ("Solve: (x + 3)/4 + (x - 1)/2 = 5", "7", ["5", "6", "8"]),
    ("Solve: 3(2x - 1) + 2(x + 4) = 25", "3", ["2", "4", "5"]),
    ("Solve: 5(x + 2) - 3(2x - 1) = 14", " -1", ["1", "2", "-2"]),
    ("Solve: (3x - 4)/2 = (x + 2)/3", "16/7", ["2", "3", "4"]),
    ("Solve: 2(3x + 4) - 4(x - 2) = 20", "2", ["1", "3", "4"]),
]


def make_questions(data):
    questions = []

    for question, answer, wrong_answers in data:
        options = [str(answer).strip()] + [
            str(x).strip() for x in wrong_answers
        ]

        random.shuffle(options)

        correct_answer = ["A", "B", "C", "D"][
            options.index(str(answer).strip())
        ]

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

    difficulty_data = {
        "Easy": EASY,
        "Medium": MEDIUM,
        "Hard": HARD
    }

    total_inserted = 0

    for difficulty, data in difficulty_data.items():
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
        questions = make_questions(data)
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
                (quiz_id, question, option_a, option_b,
                 option_c, option_d, correct_answer)
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
