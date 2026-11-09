
import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"
TOPIC = "Rational Numbers"
SUBJECT = "Mathematics"

random.seed(42)


def make_questions(data):
    result = []
    for q, answer, wrong in data:
        options = [str(answer)] + [str(x) for x in wrong]
        random.shuffle(options)
        correct = ["A", "B", "C", "D"][options.index(str(answer))]
        result.append((q, *options, correct))
    return result


EASY = [
    ("Which of these is a rational number?", "1/2", ["√2", "π", "√3"]),
    ("Which number can be written as p/q, where q is not zero?", "Rational number", ["Irrational number", "Natural number only", "Prime number"]),
    ("Is 5 a rational number?", "Yes", ["No", "Only sometimes", "Cannot be determined"]),
    ("Which is a negative rational number?", "-3/4", ["3/4", "0", "5/2"]),
    ("What is the numerator of 7/9?", "7", ["9", "16", "2"]),
    ("What is the denominator of 5/8?", "8", ["5", "13", "3"]),
    ("Which fraction is equivalent to 1/2?", "2/4", ["1/3", "3/5", "2/5"]),
    ("What is the simplest form of 4/8?", "1/2", ["2/3", "1/4", "4/4"]),
    ("What is the additive inverse of 3/5?", "-3/5", ["3/5", "5/3", "0"]),
    ("What is the additive inverse of -7/9?", "7/9", ["-7/9", "9/7", "0"]),
    ("What is the reciprocal of 2/3?", "3/2", ["2/3", "-3/2", "1/3"]),
    ("What is the reciprocal of 5?", "1/5", ["5", "-5", "0"]),
    ("Which rational number is equal to zero?", "0/5", ["5/0", "1/5", "5/1"]),
    ("What is 1/4 + 1/4?", "1/2", ["1/4", "2/8", "3/4"]),
    ("What is 2/5 + 1/5?", "3/5", ["3/10", "1/5", "2/5"]),
    ("What is 5/7 - 2/7?", "3/7", ["7/7", "3/14", "2/7"]),
    ("What is 1/2 × 1/3?", "1/6", ["2/5", "1/5", "2/6"]),
    ("What is 2/3 × 3/4?", "1/2", ["5/7", "6/7", "2/3"]),
    ("What is 1/2 ÷ 1/2?", "1", ["1/4", "2", "1/2"]),
    ("What is 3/4 ÷ 1/2?", "3/2", ["3/8", "2/3", "1/2"]),
    ("Which is greater: 2/3 or 1/3?", "2/3", ["1/3", "Both equal", "Cannot say"]),
    ("Which is smaller: -1/2 or 1/2?", "-1/2", ["1/2", "Both equal", "0"]),
    ("Is every integer a rational number?", "Yes", ["No", "Only positive integers", "Only negative integers"]),
    ("What is the standard form of 6/9?", "2/3", ["3/4", "1/3", "2/9"]),
    ("Which fraction represents a positive rational number?", "4/7", ["-4/7", "-2/3", "-1/5"]),
    ("What is -2/5 + 2/5?", "0", ["4/5", "-4/5", "2/5"]),
    ("What is 3/8 + 2/8?", "5/8", ["5/16", "1/8", "6/8"]),
    ("What is 7/10 - 3/10?", "2/5", ["4/5", "4/10", "3/10"]),
    ("Which of these is not a rational number?", "√5", ["2/3", "0.5", "-4"]),
    ("What is the reciprocal of -4/7?", "-7/4", ["7/4", "-4/7", "4/7"]),
]

MEDIUM = [
    ("Simplify 18/24.", "3/4", ["2/3", "4/5", "1/4"]),
    ("Simplify 21/35.", "3/5", ["2/5", "4/7", "1/5"]),
    ("Evaluate: 2/3 + 1/6.", "5/6", ["3/9", "1/2", "4/6"]),
    ("Evaluate: 3/4 - 1/8.", "5/8", ["2/8", "4/8", "7/8"]),
    ("Evaluate: 5/6 - 1/3.", "1/2", ["2/3", "1/3", "4/3"]),
    ("Evaluate: 2/5 + 3/10.", "7/10", ["5/15", "1/2", "6/10"]),
    ("Evaluate: -2/3 + 1/3.", "-1/3", ["1/3", "-3/3", "2/3"]),
    ("Evaluate: -3/4 + 1/2.", "-1/4", ["1/4", "-5/4", "1/2"]),
    ("Evaluate: 3/5 × 10/9.", "2/3", ["3/4", "1/3", "5/9"]),
    ("Evaluate: 4/7 × 14/8.", "1", ["2", "1/2", "4/7"]),
    ("Evaluate: 5/6 ÷ 10/9.", "3/4", ["4/3", "5/9", "2/3"]),
    ("Evaluate: 2/3 ÷ 4/5.", "5/6", ["8/15", "6/5", "2/5"]),
    ("Convert 17/4 into a mixed number.", "4 1/4", ["3 1/4", "4 2/4", "5 1/4"]),
    ("Convert 3 2/5 into an improper fraction.", "17/5", ["15/5", "13/5", "16/5"]),
    ("Which is greater: 5/8 or 2/3?", "2/3", ["5/8", "Both equal", "Cannot determine"]),
    ("Arrange -1/2, 1/4 and 3/4 in ascending order.", "-1/2, 1/4, 3/4", ["1/4, -1/2, 3/4", "3/4, 1/4, -1/2", "-1/2, 3/4, 1/4"]),
    ("Find the rational number halfway between 2/5 and 4/5.", "3/5", ["2/5", "4/5", "1/5"]),
    ("What is the additive inverse of -11/13?", "11/13", ["-11/13", "13/11", "0"]),
    ("What is the multiplicative inverse of -3/8?", "-8/3", ["8/3", "-3/8", "3/8"]),
    ("Evaluate: (-2/5) × (-3/4).", "3/10", ["-3/10", "5/9", "6/9"]),
    ("Evaluate: (-3/7) ÷ (6/14).", "-1", ["1", "-2", "2"]),
    ("Evaluate: 1/2 + 2/3 - 1/6.", "1", ["5/6", "2/3", "7/6"]),
    ("Evaluate: 3/4 × 2/3 + 1/2.", "1", ["3/4", "1/2", "5/4"]),
    ("What is 3/5 of 45?", "27", ["25", "30", "15"]),
    ("If 2/3 of a number is 18, find the number.", "27", ["24", "30", "36"]),
    ("What is the decimal form of 3/8?", "0.375", ["0.35", "0.38", "0.625"]),
    ("What is the fraction form of 0.6 in simplest form?", "3/5", ["6/5", "1/6", "2/5"]),
    ("Find x if x/12 = 3/4.", "9", ["8", "6", "10"]),
    ("Find the difference between 5/6 and 1/4.", "7/12", ["4/12", "2/3", "1/2"]),
    ("Evaluate: (-5/8) + (3/4).", "1/8", ["-1/8", "2/8", "8/8"]),
]

HARD = [
    ("Evaluate: 2/3 + 5/8.", "31/24", ["7/11", "29/24", "13/24"]),
    ("Evaluate: 7/9 - 5/12.", "13/36", ["2/3", "12/36", "17/36"]),
    ("Evaluate: 3/4 + 2/5 - 1/10.", "21/20", ["19/20", "11/10", "17/20"]),
    ("Evaluate: (-2/3) + (5/6) - 1/4.", "-1/12", ["1/12", "-5/12", "5/12"]),
    ("Evaluate: 4/5 × 15/16 × 2/3.", "1/2", ["2/3", "3/4", "1/4"]),
    ("Evaluate: 7/9 ÷ 14/27.", "3/2", ["2/3", "7/6", "1/2"]),
    ("Evaluate: (-5/6) ÷ (10/9).", "-3/4", ["3/4", "-4/3", "4/3"]),
    ("Evaluate: (2/3 + 1/6) ÷ 5/6.", "1", ["5/6", "2/3", "3/2"]),
    ("Evaluate: (3/4 × 8/9) - 1/6.", "1/2", ["2/3", "1/3", "5/6"]),
    ("Evaluate: 2 1/2 + 3 2/3.", "6 1/6", ["5 5/6", "6 2/3", "5 1/6"]),
    ("Evaluate: 5 1/4 - 2 2/3.", "2 7/12", ["3 1/12", "2 5/12", "3 7/12"]),
    ("Evaluate: 1 1/2 × 2 2/3.", "4", ["3", "5", "4 1/2"]),
    ("Evaluate: 3 1/3 ÷ 1 2/3.", "2", ["1", "3", "2 1/2"]),
    ("Find 7/12 of 180.", "105", ["95", "100", "115"]),
    ("If 5/8 of a number is 40, find the number.", "64", ["56", "60", "72"]),
    ("A tank is 3/4 full. After using 30 litres, it is half full. Find its capacity.", "120 litres", ["100 litres", "90 litres", "150 litres"]),
    ("A person spends 2/5 of their money and has Rs. 600 left. Find the original amount.", "Rs. 1000", ["Rs. 800", "Rs. 1200", "Rs. 1500"]),
    ("A student completes 2/7 of a task on Monday and 3/7 on Tuesday. What fraction remains?", "2/7", ["5/7", "3/7", "1/7"]),
    ("A rope is 24 metres long. If 5/8 is used, how much remains?", "9 metres", ["15 metres", "12 metres", "8 metres"]),
    ("Find x if 3/5 of x is 42.", "70", ["65", "75", "80"]),
    ("Which is greater: 7/10 or 5/7?", "5/7", ["7/10", "Both equal", "Cannot determine"]),
    ("Find a rational number between 1/3 and 1/2.", "5/12", ["1/4", "2/3", "3/4"]),
    ("Evaluate: (5/6 - 1/3) × 9/5.", "9/10", ["3/5", "1/2", "6/5"]),
    ("Evaluate: [(-3/4) + (1/2)] ÷ (-1/4).", "1", ["-1", "2", "-2"]),
    ("Evaluate: 2/5 ÷ 4/15 + 1/2.", "2", ["3/2", "1", "5/2"]),
    ("The sum of two rational numbers is 5/6. One number is 1/3. Find the other.", "1/2", ["2/3", "1/3", "1/6"]),
    ("The product of two rational numbers is 3/8. One number is 3/4. Find the other.", "1/2", ["1/4", "2/3", "3/2"]),
    ("If x + 2/5 = 7/10, find x.", "3/10", ["1/10", "5/10", "9/10"]),
    ("If x - 3/4 = 1/2, find x.", "5/4", ["1/4", "3/4", "7/4"]),
    ("Evaluate: (1/2 + 1/3) × (3/5).", "1/2", ["2/5", "3/4", "5/6"]),
]


def main():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT id FROM lessons WHERE title = ? AND topic = ?",
            (TOPIC, SUBJECT)
        )
        lesson = cursor.fetchone()

        if not lesson:
            raise RuntimeError("Rational Numbers lesson was not found.")

        lesson_id = lesson[0]
        print(f"Found lesson: {TOPIC} (ID: {lesson_id})")

        banks = {
            "Easy": make_questions(EASY),
            "Medium": make_questions(MEDIUM),
            "Hard": make_questions(HARD)
        }

        total = 0

        for difficulty, questions in banks.items():
            cursor.execute(
                """
                SELECT id FROM quizzes
                WHERE lesson_id = ? AND LOWER(difficulty) = LOWER(?)
                """,
                (lesson_id, difficulty)
            )
            quiz = cursor.fetchone()

            if not quiz:
                print(f"WARNING: {difficulty} quiz not found.")
                continue

            quiz_id = quiz[0]
            inserted = 0

            for question in questions:
                cursor.execute(
                    "SELECT id FROM questions WHERE quiz_id = ? AND question = ?",
                    (quiz_id, question[0])
                )

                if cursor.fetchone():
                    continue

                cursor.execute(
                    """
                    INSERT INTO questions
                    (quiz_id, question, option_a, option_b, option_c,
                     option_d, correct_answer)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (quiz_id, *question)
                )
                inserted += 1

            total += inserted
            print(f"{difficulty}: {inserted} questions inserted into Quiz ID {quiz_id}")

        connection.commit()
        print("\n--------------------------------")
        print("RATIONAL NUMBERS SEEDING COMPLETED")
        print("--------------------------------")
        print(f"Total new questions inserted: {total}")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
