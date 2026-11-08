
import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

TOPIC = "Introduction to Polynomials"
SUBJECT = "Mathematics"

random.seed(42)

# Format: (question, correct answer, [three wrong answers])

EASY = [
    ("How many terms are there in 3x + 5?", "2", ["1", "3", "5"]),
    ("What is the degree of 5x^3 + 2x + 1?", "3", ["1", "2", "5"]),
    ("What is the coefficient of x in 7x + 4?", "7", ["4", "11", "1"]),
    ("What is the constant term in 4x^2 + 3x + 9?", "9", ["4", "3", "0"]),
    ("Which of the following is a polynomial?", "x^2 + 3x + 2", ["1/x + 2", "√x + 3", "x^-2 + 1"]),
    ("What is the degree of 8x^2 + 5?", "2", ["1", "5", "8"]),
    ("How many terms are in x^2 + 3x + 7?", "3", ["2", "4", "1"]),
    ("What is the coefficient of x^2 in 6x^2 + 4x + 1?", "6", ["4", "1", "11"]),
    ("What is the degree of the polynomial 9x^4?", "4", ["9", "3", "1"]),
    ("Which is a constant polynomial?", "7", ["x + 7", "x^2", "3x"]),
    ("What is the degree of a non-zero constant polynomial?", "0", ["1", "2", "Undefined"]),
    ("What is the leading coefficient of 5x^3 + 2x + 1?", "5", ["2", "1", "3"]),
    ("Is 3x^2 + 2x + 1 a trinomial?", "Yes", ["No", "Monomial", "Binomial"]),
    ("How many terms are in 8x^2 - 3x?", "2", ["1", "3", "4"]),
    ("What is the coefficient of x^3 in 4x^3 - 2x + 5?", "4", ["-2", "5", "3"]),
    ("What is the degree of 6x^5 + 2x^2?", "5", ["2", "6", "7"]),
    ("Which is a monomial?", "5x^2", ["x + 2", "x^2 + x + 1", "x - 3"]),
    ("Which is a binomial?", "x + 5", ["x^2 + x + 1", "7x^2", "x + y + 2"]),
    ("What is the constant term in 3x^2 - 5x + 8?", "8", ["3", "-5", "0"]),
    ("Evaluate x + 5 when x = 2.", "7", ["5", "6", "8"]),
    ("Evaluate 2x when x = 4.", "8", ["6", "4", "10"]),
    ("What is the degree of 2x^3 + 4x^2 + x + 6?", "3", ["2", "4", "6"]),
    ("Which expression has degree 1?", "4x + 3", ["x^2 + 1", "x^3 + 2", "5"]),
    ("What is the coefficient of x in 9x - 4?", "9", ["-4", "4", "1"]),
    ("How many terms are in 5x^3 + 2x^2 + 7x + 1?", "4", ["3", "5", "2"]),
    ("What is the leading term of 3x^4 + 5x^2 + 2?", "3x^4", ["5x^2", "2", "3x"]),
    ("Which is a zero polynomial?", "0", ["5", "x", "x + 1"]),
    ("What is the degree of x^6 + 3x^2 + 4?", "6", ["2", "3", "4"]),
    ("Evaluate x^2 when x = 3.", "9", ["6", "12", "3"]),
    ("What is the coefficient of x^2 in x^2 + 5x + 7?", "1", ["5", "7", "0"]),
]

MEDIUM = [
    ("Simplify: (3x + 2) + (2x + 5)", "5x + 7", ["5x + 3", "x + 7", "6x + 7"]),
    ("Subtract (2x + 3) from (5x + 8).", "3x + 5", ["7x + 11", "3x + 11", "7x + 5"]),
    ("Simplify: 4x^2 + 3x^2", "7x^2", ["12x^2", "7x^4", "x^2"]),
    ("Find the degree of 5x^4 + 3x^2 + 2x + 1.", "4", ["3", "2", "5"]),
    ("Evaluate 2x^2 + 3x when x = 2.", "14", ["10", "12", "16"]),
    ("Simplify: (6x + 4) - (2x + 1)", "4x + 3", ["8x + 5", "4x + 5", "8x + 3"]),
    ("Add: (x^2 + 2x + 1) + (2x^2 + 3x + 4)", "3x^2 + 5x + 5", ["3x^2 + 5x + 3", "2x^2 + 5x + 5", "3x^2 + x + 5"]),
    ("Subtract: (x^2 + 5x + 6) - (x^2 + 2x + 3)", "3x + 3", ["3x + 9", "2x + 3", "3x - 3"]),
    ("Multiply: 3x × 4x", "12x^2", ["7x^2", "12x", "12x^3"]),
    ("Multiply: 5x × 2", "10x", ["7x", "10x^2", "5x"]),
    ("Find the value of x^2 + 2x + 1 when x = 3.", "16", ["14", "12", "18"]),
    ("What is the degree of 7x^3 - 4x^2 + 9?", "3", ["2", "4", "9"]),
    ("Simplify: 2x^2 + 5x - x^2 + 3x", "x^2 + 8x", ["3x^2 + 8x", "x^2 + 2x", "x^2 + 8"]),
    ("Multiply: 2x(x + 3)", "2x^2 + 6x", ["2x^2 + 3x", "2x + 6", "2x^2 + 5x"]),
    ("Add: (3a + 2b) + (4a - 5b)", "7a - 3b", ["7a + 7b", "a - 3b", "7a - 7b"]),
    ("Subtract (2a - 3b) from (5a + 4b).", "3a + 7b", ["7a + b", "3a + b", "7a + 7b"]),
    ("Multiply: (x + 2) × 3", "3x + 6", ["x + 6", "3x + 2", "5x"]),
    ("Evaluate 3x^2 - 2x when x = 2.", "8", ["10", "12", "6"]),
    ("What is the coefficient of x^3 in 8x^3 - 4x + 7?", "8", ["-4", "7", "3"]),
    ("Simplify: 5x^2 - 2x^2 + 4x^2", "7x^2", ["11x^2", "7x^4", "3x^2"]),
    ("Multiply: (x + 3) × 2x", "2x^2 + 6x", ["2x^2 + 3x", "2x + 6", "2x^2 + 5x"]),
    ("Find the degree of 4x^5 + 3x^3 - 2x + 1.", "5", ["3", "4", "6"]),
    ("Simplify: (4x^2 + 3x) + (x^2 - 2x)", "5x^2 + x", ["5x^2 + 5x", "3x^2 + x", "5x^2 - x"]),
    ("Subtract: (5x^2 + 4x) - (2x^2 + x)", "3x^2 + 3x", ["7x^2 + 5x", "3x^2 + 5x", "7x^2 + 3x"]),
    ("Multiply: 4a^2 × 3a", "12a^3", ["7a^3", "12a^2", "12a^4"]),
    ("Evaluate 2x^3 when x = 3.", "54", ["18", "27", "36"]),
    ("Simplify: 3(x^2 + 2x)", "3x^2 + 6x", ["3x^2 + 2x", "x^2 + 6x", "5x^2"]),
    ("What is the leading coefficient of 9x^5 - 3x^2 + 1?", "9", ["5", "-3", "1"]),
    ("Multiply: (2x + 3) × 2", "4x + 6", ["4x + 3", "2x + 6", "4x + 5"]),
    ("Evaluate x^2 - 4x + 5 when x = 3.", "2", ["4", "5", "1"]),
]

HARD = [
    ("Expand: (x + 2)(x + 3)", "x^2 + 5x + 6", ["x^2 + 6x + 5", "x^2 + 5x + 5", "x^2 + x + 6"]),
    ("Expand: (x - 4)(x + 2)", "x^2 - 2x - 8", ["x^2 + 2x - 8", "x^2 - 6x + 8", "x^2 - 2x + 8"]),
    ("Expand: (2x + 3)(x + 4)", "2x^2 + 11x + 12", ["2x^2 + 8x + 12", "2x^2 + 11x + 7", "2x^2 + 5x + 12"]),
    ("Simplify: 3x^2 + 5x - 2x^2 + 4x - 7", "x^2 + 9x - 7", ["x^2 + x - 7", "5x^2 + 9x - 7", "x^2 + 9x + 7"]),
    ("Expand: (x + 5)^2", "x^2 + 10x + 25", ["x^2 + 5x + 25", "x^2 + 25", "x^2 + 10x + 10"]),
    ("Expand: (2x - 3)(x - 2)", "2x^2 - 7x + 6", ["2x^2 - 5x + 6", "2x^2 + 7x + 6", "2x^2 - 7x - 6"]),
    ("Simplify: 2x(3x + 4) - 3x(x - 2)", "3x^2 + 14x", ["9x^2 + 2x", "3x^2 + 2x", "3x^2 + 14"]),
    ("Expand: (3x + 2)(x - 1)", "3x^2 - x - 2", ["3x^2 + 5x - 2", "3x^2 - x + 2", "3x^2 - 2x - 2"]),
    ("Subtract (2x^2 - 3x + 4) from (5x^2 + x - 2).", "3x^2 + 4x - 6", ["7x^2 - 2x + 2", "3x^2 - 2x - 6", "3x^2 + 4x + 6"]),
    ("Expand: (x - 3)^2", "x^2 - 6x + 9", ["x^2 - 9", "x^2 + 6x + 9", "x^2 - 6x - 9"]),
    ("Multiply: (2x + 1)(2x - 1)", "4x^2 - 1", ["4x^2 + 1", "4x^2 - 4x + 1", "2x^2 - 1"]),
    ("Simplify: 4(x^2 + 2x) - 2(x^2 - 3x)", "2x^2 + 14x", ["6x^2 + 2x", "2x^2 + 2x", "2x^2 + 14"]),
    ("Expand: (x + 4)(x - 5)", "x^2 - x - 20", ["x^2 + x - 20", "x^2 - 9x + 20", "x^2 - x + 20"]),
    ("Evaluate 2x^2 - 3x + 4 when x = -2.", "18", ["10", "14", "20"]),
    ("Expand: (3x - 2)(2x + 5)", "6x^2 + 11x - 10", ["6x^2 + 15x - 10", "6x^2 + 11x + 10", "6x^2 - 11x - 10"]),
    ("Simplify: 5x(x + 2) - 2x(2x - 3)", "x^2 + 16x", ["9x^2 + 4x", "x^2 + 4x", "x^2 + 16"]),
    ("Expand: (2a + 3)(a + 4)", "2a^2 + 11a + 12", ["2a^2 + 8a + 12", "2a^2 + 11a + 7", "2a^2 + 5a + 12"]),
    ("Simplify: (3x^2 + 2x - 1) + (x^2 - 5x + 4)", "4x^2 - 3x + 3", ["4x^2 + 7x + 3", "2x^2 - 3x + 3", "4x^2 - 3x - 3"]),
    ("Expand: (x + 2)(x - 2)", "x^2 - 4", ["x^2 + 4", "x^2 - 4x + 4", "x^2 - 2"]),
    ("Multiply: (x^2 + 2x + 1) × 2", "2x^2 + 4x + 2", ["2x^2 + 2x + 1", "x^2 + 4x + 2", "2x^2 + 4x + 1"]),
    ("Expand: (2x - 5)^2", "4x^2 - 20x + 25", ["4x^2 - 25", "4x^2 + 20x + 25", "2x^2 - 20x + 25"]),
    ("Simplify: 3(x^2 + 2x - 1) - 2(x^2 - x + 4)", "x^2 + 8x - 11", ["5x^2 + 4x - 11", "x^2 + 4x - 11", "x^2 + 8x + 11"]),
    ("Expand: (3a - 4)(a + 2)", "3a^2 + 2a - 8", ["3a^2 + 6a - 8", "3a^2 + 2a + 8", "3a^2 - 2a - 8"]),
    ("Evaluate x^3 - 2x^2 + 3x - 1 when x = 2.", "5", ["7", "3", "9"]),
    ("Expand: (x + 3)(x^2 + 2x + 1)", "x^3 + 5x^2 + 7x + 3", ["x^3 + 5x^2 + 5x + 3", "x^3 + 6x^2 + 7x + 3", "x^3 + 5x^2 + 7x - 3"]),
    ("Simplify: (2x^2 + 3x - 5) - (x^2 - 4x + 2)", "x^2 + 7x - 7", ["3x^2 - x - 3", "x^2 - x - 7", "x^2 + 7x + 7"]),
    ("Expand: (2x + 3)(x^2 - x + 4)", "2x^3 + x^2 + 5x + 12", ["2x^3 - x^2 + 5x + 12", "2x^3 + x^2 + 8x + 12", "2x^3 + x^2 + 5x - 12"]),
    ("Simplify: 4x^2 - 3x + 2 + 5x^2 + 7x - 8", "9x^2 + 4x - 6", ["9x^2 - 10x - 6", "x^2 + 4x - 6", "9x^2 + 4x + 6"]),
    ("Expand: (x - 2)(x^2 + 2x + 4)", "x^3 - 8", ["x^3 + 8", "x^3 - 2x^2 + 4", "x^3 - 4"]),
    ("Expand: (2x + 1)(x^2 + 3x - 2)", "2x^3 + 7x^2 - x - 2", ["2x^3 + 6x^2 - x - 2", "2x^3 + 7x^2 + x - 2", "2x^3 + 7x^2 - x + 2"]),
]


def make_questions(data):
    questions = []

    for question, answer, wrong_answers in data:
        options = [str(answer)] + [str(x) for x in wrong_answers]

        random.shuffle(options)

        correct_answer = ["A", "B", "C", "D"][options.index(str(answer))]

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
