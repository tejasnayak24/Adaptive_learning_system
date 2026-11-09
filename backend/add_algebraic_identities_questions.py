
import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

TOPIC = "Algebraic Identities"
SUBJECT = "Mathematics"

random.seed(42)

# Format: (question, correct answer, [three wrong answers])

EASY = [
    ("What is the expansion of (a + b)^2?", "a^2 + 2ab + b^2", ["a^2 + b^2", "a^2 - 2ab + b^2", "a^2 + ab + b^2"]),
    ("What is the expansion of (a - b)^2?", "a^2 - 2ab + b^2", ["a^2 + 2ab + b^2", "a^2 - b^2", "a^2 + b^2"]),
    ("What is the identity for (a + b)(a - b)?", "a^2 - b^2", ["a^2 + b^2", "a^2 - 2ab + b^2", "a^2 + 2ab + b^2"]),
    ("Expand (x + 3)^2.", "x^2 + 6x + 9", ["x^2 + 3x + 9", "x^2 + 9", "x^2 - 6x + 9"]),
    ("Expand (x - 2)^2.", "x^2 - 4x + 4", ["x^2 + 4x + 4", "x^2 - 4", "x^2 - 2x + 4"]),
    ("Expand (x + 4)(x - 4).", "x^2 - 16", ["x^2 + 16", "x^2 - 8x + 16", "x^2 + 8x + 16"]),
    ("What is the square of 5?", "25", ["10", "15", "20"]),
    ("What is the value of (a + 0)^2?", "a^2", ["a", "2a", "0"]),
    ("What is the value of (x - 0)^2?", "x^2", ["2x", "x", "0"]),
    ("Expand (y + 2)^2.", "y^2 + 4y + 4", ["y^2 + 2y + 4", "y^2 - 4y + 4", "y^2 + 4"]),
    ("Expand (y - 5)^2.", "y^2 - 10y + 25", ["y^2 + 10y + 25", "y^2 - 25", "y^2 - 5y + 25"]),
    ("Expand (a + 6)(a - 6).", "a^2 - 36", ["a^2 + 36", "a^2 - 12a + 36", "a^2 + 12a + 36"]),
    ("What is the middle term in (a + b)^2?", "2ab", ["ab", "a^2", "b^2"]),
    ("What is the middle term in (a - b)^2?", "-2ab", ["2ab", "-ab", "0"]),
    ("What is the identity for (x + y)^2?", "x^2 + 2xy + y^2", ["x^2 + y^2", "x^2 - 2xy + y^2", "x^2 - y^2"]),
    ("What is the identity for (x - y)^2?", "x^2 - 2xy + y^2", ["x^2 + 2xy + y^2", "x^2 - y^2", "x^2 + y^2"]),
    ("Expand (m + 1)^2.", "m^2 + 2m + 1", ["m^2 + m + 1", "m^2 - 2m + 1", "m^2 + 1"]),
    ("Expand (m - 1)^2.", "m^2 - 2m + 1", ["m^2 + 2m + 1", "m^2 - 1", "m^2 + 1"]),
    ("Expand (p + 2)(p - 2).", "p^2 - 4", ["p^2 + 4", "p^2 - 4p + 4", "p^2 + 4p + 4"]),
    ("What is (10 + 2)^2?", "144", ["124", "100", "104"]),
    ("What is (10 - 2)^2?", "64", ["96", "80", "60"]),
    ("What is 7^2 - 3^2?", "40", ["10", "49", "16"]),
    ("What is (a + b)^2 when a = 2 and b = 3?", "25", ["13", "20", "10"]),
    ("What is (a - b)^2 when a = 5 and b = 2?", "9", ["21", "49", "7"]),
    ("Expand (x + 1)(x - 1).", "x^2 - 1", ["x^2 + 1", "x^2 - 2x + 1", "x^2 + 2x + 1"]),
    ("Which identity is used to expand (a + b)^2?", "a^2 + 2ab + b^2", ["a^2 - b^2", "a^2 - 2ab + b^2", "a^2 + b^2"]),
    ("What is the square of (x + 5)?", "x^2 + 10x + 25", ["x^2 + 5x + 25", "x^2 - 10x + 25", "x^2 + 25"]),
    ("What is the square of (x - 3)?", "x^2 - 6x + 9", ["x^2 + 6x + 9", "x^2 - 9", "x^2 - 3x + 9"]),
    ("Find 12^2 using an identity.", "144", ["124", "142", "122"]),
    ("Find 9^2 using an identity.", "81", ["72", "90", "99"]),
]

MEDIUM = [
    ("Expand (2x + 3)^2.", "4x^2 + 12x + 9", ["4x^2 + 6x + 9", "4x^2 - 12x + 9", "2x^2 + 12x + 9"]),
    ("Expand (3x - 2)^2.", "9x^2 - 12x + 4", ["9x^2 + 12x + 4", "9x^2 - 4", "3x^2 - 12x + 4"]),
    ("Expand (2a + 5)(2a - 5).", "4a^2 - 25", ["4a^2 + 25", "4a^2 - 20a + 25", "2a^2 - 25"]),
    ("Expand (3y + 4)^2.", "9y^2 + 24y + 16", ["9y^2 + 12y + 16", "9y^2 - 24y + 16", "3y^2 + 24y + 16"]),
    ("Expand (4x - 3)^2.", "16x^2 - 24x + 9", ["16x^2 + 24x + 9", "16x^2 - 9", "4x^2 - 24x + 9"]),
    ("Expand (5a + 2)(5a - 2).", "25a^2 - 4", ["25a^2 + 4", "25a^2 - 20a + 4", "5a^2 - 4"]),
    ("Find (x + 7)^2 - x^2.", "14x + 49", ["7x + 49", "14x + 7", "x^2 + 14x + 49"]),
    ("Find (x - 4)^2 - x^2.", "-8x + 16", ["8x + 16", "-8x - 16", "x^2 - 8x + 16"]),
    ("Simplify (a + b)^2 - 2ab.", "a^2 + b^2", ["a^2 - b^2", "a^2 + 2ab + b^2", "a^2 - 2ab + b^2"]),
    ("Simplify (x + 3)^2 - (x - 3)^2.", "12x", ["6x", "12x + 18", "6x + 9"]),
    ("Find 21 × 19 using an identity.", "399", ["389", "401", "409"]),
    ("Find 32 × 28 using an identity.", "896", ["886", "906", "8960"]),
    ("Find 103^2 using an identity.", "10609", ["10606", "10306", "10906"]),
    ("Find 98^2 using an identity.", "9604", ["9804", "9406", "9608"]),
    ("Evaluate (2x + 1)^2 when x = 2.", "25", ["21", "16", "36"]),
    ("Evaluate (3a - 2)^2 when a = 2.", "16", ["20", "25", "36"]),
    ("Expand (x + 2y)^2.", "x^2 + 4xy + 4y^2", ["x^2 + 2xy + 4y^2", "x^2 - 4xy + 4y^2", "x^2 + 4y^2"]),
    ("Expand (2a - 3b)^2.", "4a^2 - 12ab + 9b^2", ["4a^2 + 12ab + 9b^2", "4a^2 - 9b^2", "2a^2 - 12ab + 9b^2"]),
    ("Expand (3p + 2q)(3p - 2q).", "9p^2 - 4q^2", ["9p^2 + 4q^2", "9p^2 - 12pq + 4q^2", "3p^2 - 4q^2"]),
    ("Simplify (x + 5)^2 - 10x.", "x^2 + 25", ["x^2 + 10x + 25", "x^2 - 25", "x^2 + 5"]),
    ("Simplify (a - 4)^2 + 8a.", "a^2 + 16", ["a^2 - 16", "a^2 - 8a + 16", "a^2 + 8a + 16"]),
    ("Find (x + 6)(x - 6) + 36.", "x^2", ["x^2 + 36", "x^2 - 36", "2x^2"]),
    ("Expand (2m + 1)^2.", "4m^2 + 4m + 1", ["4m^2 + 2m + 1", "4m^2 - 4m + 1", "2m^2 + 4m + 1"]),
    ("Expand (5x - 1)^2.", "25x^2 - 10x + 1", ["25x^2 + 10x + 1", "25x^2 - 1", "5x^2 - 10x + 1"]),
    ("Simplify (a + b)^2 + (a - b)^2.", "2a^2 + 2b^2", ["2a^2 - 2b^2", "a^2 + b^2", "4ab"]),
    ("Find 49 × 51 using an identity.", "2499", ["2501", "2409", "2599"]),
    ("Find 105 × 95 using an identity.", "9975", ["9875", "10025", "9970"]),
    ("Expand (x + 2)(x - 2) + 4.", "x^2", ["x^2 + 4", "x^2 - 4", "2x^2"]),
    ("Simplify (2x + 3)^2 - 4x^2.", "12x + 9", ["12x - 9", "4x^2 + 12x + 9", "6x + 9"]),
    ("Simplify (3a - 2)^2 - 9a^2.", "-12a + 4", ["12a + 4", "-12a - 4", "9a^2 - 12a + 4"]),
]

HARD = [
    ("Expand (2x + 3y)^2.", "4x^2 + 12xy + 9y^2", ["4x^2 + 6xy + 9y^2", "4x^2 - 12xy + 9y^2", "2x^2 + 12xy + 9y^2"]),
    ("Expand (3a - 4b)^2.", "9a^2 - 24ab + 16b^2", ["9a^2 + 24ab + 16b^2", "9a^2 - 16b^2", "3a^2 - 24ab + 16b^2"]),
    ("Expand (5p + 2q)(5p - 2q).", "25p^2 - 4q^2", ["25p^2 + 4q^2", "25p^2 - 20pq + 4q^2", "5p^2 - 4q^2"]),
    ("Simplify (x + y)^2 - (x - y)^2.", "4xy", ["2xy", "2x^2 + 2y^2", "4x^2"]),
    ("Simplify (a + b)^2 + 2ab.", "a^2 + 4ab + b^2", ["a^2 + b^2", "a^2 + 2ab + b^2", "a^2 - 2ab + b^2"]),
    ("Find 1002^2 using an identity.", "1004004", ["1002004", "1004000", "1004040"]),
    ("Find 997^2 using an identity.", "994009", ["993009", "997009", "994900"]),
    ("Find 1005 × 995 using an identity.", "999975", ["999925", "1000025", "999750"]),
    ("Find 1008 × 992 using an identity.", "999936", ["9999360", "999836", "1000036"]),
    ("Simplify (2x + 5)^2 - (2x - 5)^2.", "40x", ["20x", "40x + 50", "20x + 25"]),
    ("Expand (3x + 2y)^2 - (3x - 2y)^2.", "24xy", ["12xy", "18x^2 + 8y^2", "24x^2y"]),
    ("Simplify (a + 3b)^2 - 6ab.", "a^2 + 9b^2", ["a^2 + 3b^2", "a^2 - 3b^2", "a^2 + 6ab + 9b^2"]),
    ("Find (x + 4)^2 + (x - 4)^2.", "2x^2 + 32", ["2x^2 - 32", "2x^2 + 16", "x^2 + 32"]),
    ("Simplify (2a + b)^2 + (2a - b)^2.", "8a^2 + 2b^2", ["8a^2 - 2b^2", "4a^2 + 2b^2", "8ab"]),
    ("Evaluate (x + 2)^2 - (x - 2)^2 when x = 5.", "40", ["20", "36", "44"]),
    ("If a + b = 10 and ab = 21, find a^2 + b^2.", "58", ["79", "42", "100"]),
    ("If a - b = 4 and ab = 5, find a^2 + b^2.", "26", ["16", "21", "36"]),
    ("If x + y = 8 and xy = 12, find (x - y)^2.", "16", ["40", "64", "24"]),
    ("If x - y = 6 and xy = 8, find (x + y)^2.", "68", ["36", "52", "44"]),
    ("Find 203^2 using an identity.", "41209", ["40609", "41200", "41309"]),
    ("Find 1001^2 using an identity.", "1002001", ["1001001", "1002000", "1002010"]),
    ("Simplify (3x + 4)^2 - 9x^2.", "24x + 16", ["24x - 16", "9x^2 + 24x + 16", "12x + 16"]),
    ("Simplify (4a - 3)^2 - 16a^2.", "-24a + 9", ["24a + 9", "-24a - 9", "16a^2 - 24a + 9"]),
    ("Find (2x + 3y)^2 + (2x - 3y)^2.", "8x^2 + 18y^2", ["8x^2 - 18y^2", "4x^2 + 18y^2", "24xy"]),
    ("If x + y = 12 and x - y = 4, find xy.", "32", ["24", "16", "36"]),
    ("If a + b = 9 and a - b = 3, find a^2 + b^2.", "45", ["36", "54", "81"]),
    ("Find 48^2 using the identity (50 - 2)^2.", "2304", ["2404", "2204", "2306"]),
    ("Find 102^2 using the identity (100 + 2)^2.", "10404", ["10204", "10400", "10408"]),
    ("Simplify (x + 7)^2 - (x^2 + 14x).", "49", ["14", "7", "x^2 + 49"]),
    ("Simplify (3a + 2b)^2 - (9a^2 + 4b^2).", "12ab", ["6ab", "12a^2b^2", "9ab"]),
]


def make_questions(data):
    questions = []

    for question, answer, wrong_answers in data:
        options = [str(answer)] + [str(x) for x in wrong_answers]

        if len(set(options)) != 4:
            raise ValueError(f"Duplicate options found: {question}")

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
