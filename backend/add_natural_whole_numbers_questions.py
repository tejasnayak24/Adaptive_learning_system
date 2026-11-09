import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

TOPIC = "Natural Numbers and Whole Numbers"
SUBJECT = "Mathematics"

random.seed(42)


def create_question(question, answer, wrong_answers):
    options = [str(answer)] + [str(x) for x in wrong_answers]
    random.shuffle(options)

    correct_answer = ["A", "B", "C", "D"][options.index(str(answer))]

    return (
        question,
        options[0],
        options[1],
        options[2],
        options[3],
        correct_answer
    )


def easy_questions():
    data = [
        ("What is the smallest natural number?", "1", ["0", "-1", "2"]),
        ("What is the smallest whole number?", "0", ["1", "-1", "2"]),
        ("Which of these is a natural number?", "8", ["-3", "2.5", "-1"]),
        ("Which of these is a whole number?", "0", ["-2", "-1", "1.5"]),
        ("What is the successor of 25?", "26", ["24", "27", "20"]),
        ("What is the predecessor of 40?", "39", ["41", "38", "40"]),
        ("What is the successor of 99?", "100", ["98", "101", "90"]),
        ("What is the predecessor of 100?", "99", ["101", "98", "90"]),
        ("What is 12 + 8?", "20", ["18", "22", "16"]),
        ("What is 35 - 15?", "20", ["15", "25", "30"]),
        ("What is 7 × 6?", "42", ["36", "48", "40"]),
        ("What is 56 ÷ 8?", "7", ["6", "8", "9"]),
        ("Which number comes immediately after 49?", "50", ["48", "51", "59"]),
        ("Which number comes immediately before 75?", "74", ["76", "73", "70"]),
        ("Which is the greatest number?", "45", ["32", "28", "41"]),
        ("Which is the smallest number?", "12", ["21", "18", "15"]),
        ("How many natural numbers are there?", "Infinitely many", ["10", "100", "1000"]),
        ("Is zero a natural number under the usual school convention?", "No", ["Yes", "Sometimes always", "None"]),
        ("Is zero a whole number?", "Yes", ["No", "Only sometimes", "None"]),
        ("What is the additive identity of whole numbers?", "0", ["1", "10", "-1"]),
        ("What is the multiplicative identity of whole numbers?", "1", ["0", "2", "10"]),
        ("What is 0 + 15?", "15", ["0", "1", "16"]),
        ("What is 1 × 25?", "25", ["1", "0", "26"]),
        ("What is 25 × 0?", "0", ["25", "1", "5"]),
        ("Which number is even?", "18", ["13", "15", "21"]),
        ("Which number is odd?", "17", ["12", "14", "20"]),
        ("Which of these is a two-digit whole number?", "56", ["8", "105", "7.5"]),
        ("How many digits are there in 100?", "3", ["1", "2", "4"]),
        ("What is the place value of 4 in 245?", "40", ["4", "400", "5"]),
        ("What is the sum of the first three natural numbers?", "6", ["3", "5", "9"]),
    ]

    return [create_question(q, a, w) for q, a, w in data]


def medium_questions():
    data = [
        ("What is the sum of the first 10 natural numbers?", "55", ["45", "50", "60"]),
        ("What is the sum of the first 10 whole numbers?", "45", ["55", "50", "40"]),
        ("How many natural numbers are there from 1 to 20?", "20", ["19", "21", "18"]),
        ("How many whole numbers are there from 0 to 20?", "21", ["20", "19", "22"]),
        ("What is the difference between the largest two-digit and smallest two-digit natural numbers?", "89", ["90", "88", "91"]),
        ("What is the product of the first four natural numbers?", "24", ["12", "16", "20"]),
        ("What is the value of 125 + 275?", "400", ["350", "450", "500"]),
        ("What is the value of 500 - 275?", "225", ["235", "215", "250"]),
        ("What is the value of 24 × 15?", "360", ["340", "350", "380"]),
        ("What is the value of 840 ÷ 12?", "70", ["60", "80", "75"]),
        ("Which property is shown by 8 + 5 = 5 + 8?", "Commutative property", ["Associative property", "Distributive property", "Closure property"]),
        ("Which property is shown by (2 + 3) + 4 = 2 + (3 + 4)?", "Associative property", ["Commutative property", "Distributive property", "Identity property"]),
        ("Which property is shown by 5 × (3 + 2) = 5 × 3 + 5 × 2?", "Distributive property", ["Commutative property", "Identity property", "Closure property"]),
        ("What is the additive identity in whole numbers?", "0", ["1", "2", "10"]),
        ("What is the multiplicative identity in natural numbers?", "1", ["0", "2", "10"]),
        ("Which operation is not closed in whole numbers?", "Subtraction", ["Addition", "Multiplication", "None of these"]),
        ("Which operation is closed in natural numbers?", "Multiplication", ["Subtraction", "Division", "None of these"]),
        ("What is the predecessor of the smallest natural number?", "Not a natural number", ["0", "1", "2"]),
        ("What is the successor of 999?", "1000", ["998", "999", "1001"]),
        ("What is the predecessor of 1000?", "999", ["1001", "998", "990"]),
        ("What is the value of 15 + 25 × 2?", "65", ["80", "50", "40"]),
        ("What is the value of (15 + 25) × 2?", "80", ["65", "70", "90"]),
        ("What is the value of 144 ÷ 12 + 8?", "20", ["12", "18", "24"]),
        ("What is the value of 100 - 5 × 8?", "60", ["760", "40", "80"]),
        ("Which number is divisible by both 2 and 5?", "40", ["32", "45", "27"]),
        ("What is the smallest three-digit natural number?", "100", ["99", "101", "110"]),
        ("What is the greatest two-digit natural number?", "99", ["100", "98", "90"]),
        ("How many whole numbers lie between 5 and 10?", "4", ["5", "3", "6"]),
        ("What is the average of 10, 20 and 30?", "20", ["15", "25", "30"]),
        ("If 5 is added to a number, the result is 18. Find the number.", "13", ["12", "14", "15"]),
    ]

    return [create_question(q, a, w) for q, a, w in data]


def hard_questions():
    data = [
        ("What is the sum of the first 20 natural numbers?", "210", ["200", "190", "220"]),
        ("What is the sum of the first 20 whole numbers?", "190", ["200", "210", "180"]),
        ("What is the sum of the first 50 natural numbers?", "1275", ["1250", "1225", "1300"]),
        ("What is the sum of the first 50 whole numbers?", "1225", ["1275", "1200", "1250"]),
        ("How many natural numbers are there between 100 and 200?", "99", ["100", "101", "98"]),
        ("How many whole numbers are there from 50 to 100, inclusive?", "51", ["50", "49", "52"]),
        ("What is the difference between the sum of the first 10 natural numbers and the first 10 whole numbers?", "10", ["5", "15", "20"]),
        ("A number multiplied by 8 gives 456. Find the number.", "57", ["56", "58", "59"]),
        ("The sum of two consecutive natural numbers is 51. Find the smaller number.", "25", ["24", "26", "27"]),
        ("The sum of three consecutive natural numbers is 72. Find the middle number.", "24", ["23", "25", "26"]),
        ("The product of two consecutive natural numbers is 56. Find the smaller number.", "7", ["6", "8", "9"]),
        ("A number divided by 12 gives quotient 15 and remainder 7. Find the number.", "187", ["180", "182", "192"]),
        ("What is the value of 250 × 4 + 150 ÷ 5?", "1030", ["1000", "1060", "980"]),
        ("Evaluate: 500 - (25 × 8) + 40", "340", ["300", "360", "380"]),
        ("Evaluate: 120 ÷ 6 × 5 + 10", "110", ["30", "100", "120"]),
        ("Which property is used in 12 × (10 + 5) = 12 × 10 + 12 × 5?", "Distributive property", ["Associative property", "Commutative property", "Identity property"]),
        ("Which of the following is not a whole number?", "-4", ["0", "12", "100"]),
        ("Which of the following is not a natural number?", "0", ["1", "5", "20"]),
        ("If a + 0 = 75, find a.", "75", ["0", "1", "74"]),
        ("If a × 1 = 125, find a.", "125", ["1", "0", "126"]),
        ("A shop has 125 boxes with 24 pencils in each. How many pencils are there?", "3000", ["2500", "2800", "3200"]),
        ("A factory produces 250 items daily. How many items does it produce in 28 days?", "7000", ["6500", "6800", "7500"]),
        ("A number is increased by 125 and becomes 500. Find the original number.", "375", ["350", "400", "425"]),
        ("The product of two numbers is 720. If one number is 24, find the other.", "30", ["25", "35", "40"]),
        ("What is the smallest whole number that must be added to 995 to get 1000?", "5", ["4", "6", "10"]),
        ("How many multiples of 5 are there from 1 to 100?", "20", ["19", "21", "25"]),
        ("How many even natural numbers are there from 1 to 50?", "25", ["24", "26", "50"]),
        ("What is the value of 999 × 9?", "8991", ["9000", "8990", "9091"]),
        ("A number is divided by 9 and gives quotient 12 and remainder 5. Find the number.", "113", ["108", "110", "115"]),
        ("The sum of two numbers is 100. One number is 37. Find the other.", "63", ["53", "67", "73"]),
    ]

    return [create_question(q, a, w) for q, a, w in data]


def main():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        # Find lesson
        cursor.execute(
            """
            SELECT id
            FROM lessons
            WHERE title = ? AND topic = ?
            """,
            (TOPIC, SUBJECT)
        )

        lesson = cursor.fetchone()

        if not lesson:
            raise RuntimeError(
                f"{TOPIC} lesson was not found."
            )

        lesson_id = lesson[0]

        print(f"Found lesson: {TOPIC} (ID: {lesson_id})")

        question_banks = {
            "Easy": easy_questions(),
            "Medium": medium_questions(),
            "Hard": hard_questions()
        }

        total_inserted = 0

        for difficulty, questions in question_banks.items():

            cursor.execute(
                """
                SELECT id
                FROM quizzes
                WHERE lesson_id = ?
                AND LOWER(difficulty) = LOWER(?)
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
                    """
                    SELECT id
                    FROM questions
                    WHERE quiz_id = ? AND question = ?
                    """,
                    (quiz_id, question[0])
                )

                if cursor.fetchone():
                    continue

                cursor.execute(
                    """
                    INSERT INTO questions (
                        quiz_id,
                        question,
                        option_a,
                        option_b,
                        option_c,
                        option_d,
                        correct_answer
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (quiz_id, *question)
                )

                inserted += 1

            total_inserted += inserted

            print(
                f"{difficulty}: {inserted} questions inserted "
                f"into Quiz ID {quiz_id}"
            )

        connection.commit()

        print("\n--------------------------------")
        print("NATURAL NUMBERS SEEDING COMPLETED")
        print("--------------------------------")
        print(f"Total new questions inserted: {total_inserted}")

    except Exception as error:
        connection.rollback()
        print("ERROR:", error)
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()