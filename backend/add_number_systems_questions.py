import sqlite3
import random
from pathlib import Path

# Database path
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

TOPIC = "Number Systems"
SUBJECT = "Mathematics"

random.seed(42)


def create_question(question, answer, wrong_answers):
    """
    Creates an MCQ with four options and a correct answer.
    """

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

    questions = []

    data = [
        ("Which of the following is a natural number?", "1", ["0", "-2", "-5"]),
        ("Which is the smallest whole number?", "0", ["1", "-1", "2"]),
        ("Which of these is an integer?", "-5", ["2.5", "1/2", "3.7"]),
        ("What is the successor of 99?", "100", ["98", "101", "90"]),
        ("What is the predecessor of 50?", "49", ["51", "48", "52"]),
        ("Which number is an even number?", "24", ["15", "17", "21"]),
        ("Which number is an odd number?", "13", ["12", "18", "20"]),
        ("Which of these is a prime number?", "7", ["9", "15", "21"]),
        ("Which of these is a composite number?", "12", ["2", "3", "5"]),
        ("What is the place value of 5 in 352?", "50", ["5", "500", "2"]),
        ("Which number is divisible by 2?", "48", ["35", "51", "73"]),
        ("Which number is divisible by 5?", "65", ["42", "33", "71"]),
        ("Which number is divisible by 10?", "90", ["25", "43", "67"]),
        ("What is the Roman numeral for 10?", "X", ["V", "L", "C"]),
        ("Which is a negative integer?", "-8", ["8", "0", "4"]),
        ("What is the absolute value of -6?", "6", ["-6", "0", "12"]),
        ("Which is a fraction?", "3/4", ["5", "8", "-2"]),
        ("Which is a decimal number?", "2.5", ["4", "7", "-3"]),
        ("What is 5 + 7?", "12", ["10", "11", "13"]),
        ("What is 15 - 8?", "7", ["6", "8", "9"]),
        ("What is 6 × 4?", "24", ["20", "22", "26"]),
        ("What is 20 ÷ 5?", "4", ["2", "5", "10"]),
        ("Which number is a multiple of 3?", "12", ["14", "16", "20"]),
        ("Which number is a factor of 12?", "4", ["5", "7", "9"]),
        ("What is the smallest prime number?", "2", ["1", "0", "3"]),
        ("Which number is neither prime nor composite?", "1", ["2", "4", "6"]),
        ("Which is a rational number?", "1/2", ["√2", "π", "√3"]),
        ("What is the value of 2³?", "8", ["6", "9", "12"]),
        ("What is the square of 5?", "25", ["10", "15", "20"]),
        ("What is the cube of 3?", "27", ["9", "18", "12"]),
    ]

    for q, a, wrong in data:
        questions.append(create_question(q, a, wrong))

    return questions


def medium_questions():

    questions = []

    data = [
        ("Which of the following is an irrational number?", "√5", ["1/2", "0.25", "4"]),
        ("What is the prime factorisation of 36?", "2 × 2 × 3 × 3", ["2 × 3 × 6", "4 × 9", "3 × 12"]),
        ("What is the HCF of 18 and 24?", "6", ["3", "9", "12"]),
        ("What is the LCM of 8 and 12?", "24", ["12", "16", "48"]),
        ("Which number is divisible by 9?", "729", ["725", "731", "734"]),
        ("What is the value of (-8) + 5?", "-3", ["3", "-13", "13"]),
        ("What is the value of (-6) × (-4)?", "24", ["-24", "10", "-10"]),
        ("What is the value of 45 ÷ (-9)?", "-5", ["5", "-4", "4"]),
        ("What is the square root of 144?", "12", ["10", "14", "16"]),
        ("What is the cube root of 216?", "6", ["4", "8", "9"]),
        ("What is the value of 2⁴?", "16", ["8", "12", "32"]),
        ("What is the value of 3² + 4²?", "25", ["24", "49", "14"]),
        ("Which fraction is equivalent to 3/4?", "6/8", ["3/8", "4/6", "5/8"]),
        ("Convert 0.75 into a fraction.", "3/4", ["1/2", "2/5", "4/5"]),
        ("What is the decimal form of 1/4?", "0.25", ["0.5", "0.75", "0.1"]),
        ("What is the successor of -1?", "0", ["-2", "1", "-3"]),
        ("What is the predecessor of 0?", "-1", ["1", "2", "-2"]),
        ("Which is the greatest integer?", "0", ["-1", "-5", "-10"]),
        ("What is the sum of the first five natural numbers?", "15", ["10", "20", "25"]),
        ("How many factors does 16 have?", "5", ["4", "6", "8"]),
        ("What is the prime factorisation of 60?", "2 × 2 × 3 × 5", ["2 × 3 × 10", "3 × 4 × 5", "2 × 5 × 6"]),
        ("Which of these is a perfect square?", "169", ["150", "170", "180"]),
        ("What is the square of 12?", "144", ["124", "132", "154"]),
        ("What is the cube of 4?", "64", ["16", "32", "48"]),
        ("What is the value of 5⁰?", "1", ["0", "5", "10"]),
        ("Which number lies between 1 and 2?", "√2", ["3", "4", "5"]),
        ("What is the absolute value of -15?", "15", ["-15", "0", "30"]),
        ("What is the remainder when 47 is divided by 5?", "2", ["1", "3", "4"]),
        ("Which is the smallest composite number?", "4", ["1", "2", "3"]),
        ("What is the sum of -12 and 20?", "8", ["-8", "32", "-32"]),
    ]

    for q, a, wrong in data:
        questions.append(create_question(q, a, wrong))

    return questions


def hard_questions():

    questions = []

    data = [
        ("Which of the following is a non-terminating, non-repeating decimal?", "√3", ["0.5", "0.25", "0.75"]),
        ("What is the HCF of 48 and 72?", "24", ["12", "18", "36"]),
        ("What is the LCM of 18 and 30?", "90", ["60", "120", "180"]),
        ("What is the smallest number divisible by 12, 15 and 20?", "60", ["30", "45", "120"]),
        ("What is the greatest four-digit number divisible by 9?", "9999", ["9998", "9996", "9990"]),
        ("What is the smallest four-digit number divisible by 8?", "1000", ["1008", "1016", "1024"]),
        ("What is the value of (-12) × (-3) + (-8)?", "28", ["20", "36", "-28"]),
        ("What is the value of (-2)³ + 5²?", "17", ["-17", "33", "9"]),
        ("Evaluate: 36 ÷ (-6) + 14", "8", ["20", "-8", "10"]),
        ("What is the value of 2⁵ × 2³?", "256", ["64", "128", "512"]),
        ("Simplify: 3⁴ ÷ 3²", "9", ["3", "27", "81"]),
        ("What is the value of (2³)²?", "64", ["16", "32", "128"]),
        ("What is the square root of 2025?", "45", ["35", "40", "55"]),
        ("What is the cube root of 1728?", "12", ["10", "14", "16"]),
        ("What is the prime factorisation of 180?", "2² × 3² × 5", ["2 × 3² × 5", "2² × 3 × 5", "2 × 3 × 5²"]),
        ("What is the HCF of 84 and 126?", "42", ["21", "14", "28"]),
        ("What is the LCM of 24 and 36?", "72", ["48", "96", "108"]),
        ("What is the value of (-15) + 25 - 18?", "-8", ["-2", "2", "8"]),
        ("Which fraction has a terminating decimal expansion?", "7/20", ["1/3", "2/7", "5/6"]),
        ("Which of the following is an irrational number?", "√7", ["√49", "0.125", "3/8"]),
        ("What is the sum of the first 10 natural numbers?", "55", ["45", "50", "60"]),
        ("How many prime numbers are there between 1 and 20?", "8", ["7", "9", "10"]),
        ("What is the smallest prime factor of 91?", "7", ["3", "5", "13"]),
        ("What is the remainder when 2⁵ is divided by 5?", "2", ["1", "3", "4"]),
        ("If a number is divisible by both 6 and 8, it must be divisible by?", "24", ["12", "16", "18"]),
        ("What is the value of 10³ - 5²?", "975", ["950", "985", "1000"]),
        ("Which number is a perfect cube?", "343", ["324", "350", "400"]),
        ("What is the product of the HCF and LCM of 12 and 18?", "216", ["108", "144", "324"]),
        ("What is the value of (-3)² × (-2)³?", "-72", ["72", "-36", "36"]),
        ("What is the least number that must be added to 100 to make it divisible by 9?", "8", ["5", "7", "9"]),
    ]

    for q, a, wrong in data:
        questions.append(create_question(q, a, wrong))

    return questions


def main():

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:

        # Find the Mathematics lesson
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
            raise RuntimeError("Number Systems lesson was not found.")

        lesson_id = lesson[0]

        print(f"Found lesson: {TOPIC} (ID: {lesson_id})")

        question_banks = {
            "Easy": easy_questions(),
            "Medium": medium_questions(),
            "Hard": hard_questions()
        }

        total_inserted = 0

        for difficulty, questions in question_banks.items():

            # Find the corresponding quiz
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
                print(f"WARNING: {difficulty} quiz not found. Skipping.")
                continue

            quiz_id = quiz[0]

            inserted = 0

            for question in questions:

                q_text = question[0]

                # Avoid duplicate questions
                cursor.execute(
                    """
                    SELECT id
                    FROM questions
                    WHERE quiz_id = ? AND question = ?
                    """,
                    (quiz_id, q_text)
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
                f"{difficulty}: {inserted} new questions inserted "
                f"into Quiz ID {quiz_id}"
            )

        connection.commit()

        print("\n--------------------------------")
        print("NUMBER SYSTEMS SEEDING COMPLETED")
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