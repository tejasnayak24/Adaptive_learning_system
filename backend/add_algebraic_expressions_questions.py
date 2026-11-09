
import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

TOPIC = "Algebraic Expressions"
SUBJECT = "Mathematics"

random.seed(42)

# Each question: (question, correct answer, [three wrong answers])

EASY = [
    ("How many terms are there in 3x + 5?", "2", ["1", "3", "5"]),
    ("What is the coefficient of x in 7x + 4?", "7", ["4", "11", "1"]),
    ("What is the constant term in 5x + 9?", "9", ["5", "x", "14"]),
    ("Which of the following is a variable?", "x", ["5", "+", "10"]),
    ("What is the coefficient of y in 8y - 3?", "8", ["-3", "3", "11"]),
    ("Which pair contains like terms?", "3x and 7x", ["3x and 7y", "x and x²", "2x and 2y"]),
    ("What is the value of x + 4 when x = 3?", "7", ["6", "8", "9"]),
    ("Simplify: 2x + 3x", "5x", ["6x", "5x²", "x"]),
    ("Simplify: 7a - 2a", "5a", ["9a", "5", "14a"]),
    ("How many terms are in 4x + 3y + 7?", "3", ["2", "4", "1"]),
    ("What is the constant term in 6a - 11?", "-11", ["6", "11", "a"]),
    ("What is the coefficient of p in -5p + 2?", "-5", ["5", "2", "-2"]),
    ("Evaluate 2x when x = 4.", "8", ["6", "4", "10"]),
    ("Simplify: 4m + 2m", "6m", ["8m", "6m²", "2m"]),
    ("Which expression represents 5 more than x?", "x + 5", ["5x", "x - 5", "x/5"]),
    ("Which expression represents twice a number y?", "2y", ["y + 2", "y²", "y/2"]),
    ("What is the variable in 9a + 6?", "a", ["9", "6", "15"]),
    ("Simplify: 8x - 3x", "5x", ["11x", "5", "24x"]),
    ("Evaluate a + b when a = 2 and b = 5.", "7", ["10", "3", "25"]),
    ("What is the coefficient of x in x + 8?", "1", ["8", "0", "-1"]),
    ("How many variables are in 3x + 2y?", "2", ["1", "3", "4"]),
    ("Simplify: 5p + p", "6p", ["5p", "5p²", "4p"]),
    ("Evaluate 3a + 2 when a = 2.", "8", ["7", "10", "6"]),
    ("Which is a numerical expression?", "5 + 8", ["3x + 2", "a - 4", "2y"]),
    ("What is the coefficient of y in y - 6?", "1", ["-6", "6", "0"]),
    ("Simplify: 9b - 4b", "5b", ["13b", "5", "36b"]),
    ("What is the constant term in 2x + 3y + 8?", "8", ["2", "3", "x"]),
    ("Evaluate x - 2 when x = 9.", "7", ["11", "6", "9"]),
    ("Which expression represents 3 times x?", "3x", ["x + 3", "x³", "x/3"]),
    ("Simplify: 2a + 4a + a", "7a", ["6a", "8a", "7a²"]),
]

MEDIUM = [
    ("Simplify: 3x + 5x - 2x", "6x", ["10x", "8x", "6x²"]),
    ("Simplify: 4a + 3b + 2a - b", "6a + 2b", ["6a + 4b", "2a + 2b", "6a - 2b"]),
    ("Evaluate 2x + 3y when x = 2 and y = 4.", "16", ["14", "12", "18"]),
    ("Simplify: 5p - 2q + 3p + q", "8p - q", ["8p + 3q", "2p - q", "8p - 3q"]),
    ("Expand: 3(x + 4)", "3x + 12", ["3x + 4", "x + 12", "7x"]),
    ("Expand: 2(a - 5)", "2a - 10", ["2a - 5", "2a + 10", "a - 10"]),
    ("Simplify: 7x + 3 - 2x + 5", "5x + 8", ["9x + 8", "5x - 2", "5x + 2"]),
    ("Evaluate 4a - 3b when a = 5 and b = 2.", "14", ["16", "20", "10"]),
    ("Simplify: 6m + 4n - 2m + 3n", "4m + 7n", ["8m + 7n", "4m + n", "4m + 5n"]),
    ("Expand: 5(2x + 3)", "10x + 15", ["10x + 3", "7x + 15", "10x + 8"]),
    ("Simplify: 8a - 3a + 2a", "7a", ["13a", "7a²", "5a"]),
    ("Evaluate x² + 2x when x = 3.", "15", ["12", "18", "9"]),
    ("Simplify: 3x + 2y - x + 5y", "2x + 7y", ["4x + 7y", "2x + 3y", "2x - 7y"]),
    ("Expand: 4(3a - 2)", "12a - 8", ["12a - 2", "7a - 8", "12a + 8"]),
    ("Simplify: 2(x + 3) + x", "3x + 6", ["2x + 6", "3x + 3", "4x + 6"]),
    ("Evaluate 5p + 2q - 3 when p = 2 and q = 4.", "15", ["17", "13", "19"]),
    ("Simplify: 9x - 4 + 2x + 7", "11x + 3", ["7x + 3", "11x - 3", "11x + 11"]),
    ("Expand: 3(2y - 4)", "6y - 12", ["6y - 4", "5y - 12", "6y + 12"]),
    ("Simplify: 4a + 2b - a + 5b", "3a + 7b", ["5a + 7b", "3a + 3b", "3a - 7b"]),
    ("Evaluate 2x² + 3 when x = 4.", "35", ["19", "32", "36"]),
    ("Simplify: 5(x + 2) - 2x", "3x + 10", ["7x + 10", "3x + 2", "5x + 10"]),
    ("Expand: 2(3a + 4b)", "6a + 8b", ["5a + 6b", "6a + 4b", "3a + 8b"]),
    ("Simplify: 7p + 2q - 3p - 5q", "4p - 3q", ["10p - 3q", "4p + 7q", "4p - 7q"]),
    ("Evaluate 3a² - 2 when a = 3.", "25", ["21", "27", "19"]),
    ("Simplify: 2x + 3(x + 4)", "5x + 12", ["5x + 4", "6x + 12", "2x + 12"]),
    ("Expand: 6(2m - 3)", "12m - 18", ["12m - 3", "8m - 18", "12m + 18"]),
    ("Simplify: 10a - 4b - 3a + 6b", "7a + 2b", ["13a + 2b", "7a - 2b", "7a + 10b"]),
    ("Evaluate 2x + y² when x = 3 and y = 4.", "22", ["20", "16", "28"]),
    ("Simplify: 4( x + 2) + 3x", "7x + 8", ["7x + 2", "4x + 8", "7x + 6"]),
    ("Expand: 3(2p - q + 4)", "6p - 3q + 12", ["6p - q + 12", "5p - 3q + 12", "6p + 3q + 12"]),
]

HARD = [
    ("Simplify: 3(2x + 5) - 2(x - 4)", "4x + 23", ["4x + 7", "8x + 23", "4x + 13"]),
    ("Simplify: 5a - 2(3a - 4) + 7a", "6a + 8", ["6a - 8", "12a + 8", "6a + 4"]),
    ("Expand and simplify: 4(2x - 3) + 3(x + 5)", "11x + 3", ["11x - 3", "8x + 3", "11x + 12"]),
    ("Simplify: 2(3a + 4b) - 3(a - 2b)", "3a + 14b", ["3a + 2b", "9a + 14b", "3a + 8b"]),
    ("Evaluate 2x² - 3x + 4 when x = -2.", "18", ["10", "14", "20"]),
    ("Simplify: 7x - [3x - (2x + 5)]", "6x + 5", ["2x + 5", "6x - 5", "12x + 5"]),
    ("Expand: (x + 3)(x + 2)", "x² + 5x + 6", ["x² + 6x + 5", "x² + 5x + 5", "x² + x + 6"]),
    ("Expand: (a + 4)(a + 2)", "a² + 6a + 8", ["a² + 8a + 6", "a² + 6a + 6", "a² + 2a + 8"]),
    ("Simplify: 3x² + 5x - 2x² + 4x", "x² + 9x", ["5x² + 9x", "x² + x", "x² + 9"]),
    ("Evaluate 3a² - 2ab + b² when a = 2 and b = 3.", "9", ["15", "21", "12"]),
    ("Simplify: 2(3x - 4) - 3(2x + 5)", "-23", ["-7", "23", "-13"]),
    ("Expand: (x - 5)(x + 2)", "x² - 3x - 10", ["x² + 3x - 10", "x² - 7x + 10", "x² - 3x + 10"]),
    ("Simplify: 4a - 2[3a - (a - 5)]", "-5", ["5", "-1", "-9"]),
    ("Evaluate x³ - 2x² + 3x when x = 2.", "6", ["8", "4", "10"]),
    ("Expand: (2x + 3)(x + 4)", "2x² + 11x + 12", ["2x² + 8x + 12", "2x² + 11x + 7", "2x² + 5x + 12"]),
    ("Simplify: 5(2p - 3q) - 2(3p + q)", "4p - 17q", ["16p - 13q", "4p - 13q", "4p - 17"]),
    ("Expand: (a - 3)(a - 2)", "a² - 5a + 6", ["a² + 5a + 6", "a² - a + 6", "a² - 5a - 6"]),
    ("Simplify: 2x² + 3x - (x² - 4x + 5)", "x² + 7x - 5", ["3x² + 7x - 5", "x² - x - 5", "x² + 7x + 5"]),
    ("Evaluate 2a² + 3b² - ab when a = 3 and b = 2.", "20", ["22", "26", "18"]),
    ("Expand: (3x - 2)(x + 5)", "3x² + 13x - 10", ["3x² + 15x - 10", "3x² + 13x + 10", "3x² - 13x - 10"]),
    ("Simplify: 4[2x - (3x - 5)] + x", "-3x + 20", ["3x + 20", "-3x + 5", "5x + 20"]),
    ("Expand: (2a + 1)(a - 3)", "2a² - 5a - 3", ["2a² - 6a - 3", "2a² + 5a - 3", "2a² - 5a + 3"]),
    ("Simplify: 3(x² + 2x) - 2(x² - x)", "x² + 8x", ["5x² + 4x", "x² + 4x", "x² + 8"]),
    ("Evaluate 2x²y - 3xy² when x = 2 and y = -1.", "-10", ["10", "-6", "-14"]),
    ("Expand: (x + 6)²", "x² + 12x + 36", ["x² + 6x + 36", "x² + 36", "x² + 12x + 12"]),
    ("Simplify: 2a(3a - 4) + 5a(a + 2)", "11a² + 2a", ["11a² - 2a", "6a² + 2a", "11a² + 10a"]),
    ("Expand: (2x - 3)²", "4x² - 12x + 9", ["4x² - 9", "4x² + 12x + 9", "2x² - 12x + 9"]),
    ("Simplify: 5x - 2[3x - 4( x - 2)]", "7x - 16", ["-x - 16", "7x + 16", "5x - 16"]),
    ("Expand: (a + 5)(a - 5)", "a² - 25", ["a² + 25", "a² - 10a + 25", "a² - 5"]),
    ("Simplify: (2x + 3)(x - 2) - 2x(x + 1)", "-3x - 6", ["3x - 6", "-3x + 6", "2x² - 3x - 6"]),
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
