
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

TOPIC = "Integers"
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
        ("Which of the following is a negative integer?", "-5", ["5", "0", "2"]),
        ("Which of the following is a positive integer?", "8", ["-8", "0", "-3"]),
        ("What is the additive inverse of 7?", "-7", ["7", "0", "1"]),
        ("What is the additive inverse of -9?", "9", ["-9", "0", "1"]),
        ("What is the absolute value of -12?", "12", ["-12", "0", "24"]),
        ("What is the absolute value of 15?", "15", ["-15", "0", "30"]),
        ("What is (-5) + 3?", "-2", ["2", "-8", "8"]),
        ("What is 8 + (-3)?", "5", ["11", "-5", "-11"]),
        ("What is (-4) + (-6)?", "-10", ["10", "-2", "2"]),
        ("What is 9 - 5?", "4", ["14", "-4", "5"]),
        ("What is 5 - 9?", "-4", ["4", "14", "-14"]),
        ("What is (-3) - 4?", "-7", ["7", "1", "-1"]),
        ("What is (-6) × 2?", "-12", ["12", "-8", "8"]),
        ("What is (-5) × (-3)?", "15", ["-15", "8", "-8"]),
        ("What is 24 ÷ (-6)?", "-4", ["4", "-6", "6"]),
        ("What is (-20) ÷ (-5)?", "4", ["-4", "5", "-5"]),
        ("Which integer is greater: -2 or -5?", "-2", ["-5", "Both are equal", "0"]),
        ("Which integer is smaller: -8 or -3?", "-8", ["-3", "Both are equal", "0"]),
        ("What is the successor of -4?", "-3", ["-5", "4", "3"]),
        ("What is the predecessor of 6?", "5", ["7", "-5", "-6"]),
        ("What is the opposite of 10?", "-10", ["10", "0", "1"]),
        ("Which integer represents 5 degrees below zero?", "-5", ["5", "0", "10"]),
        ("Which integer represents a gain of Rs. 100?", "100", ["-100", "0", "-10"]),
        ("What is the result of (-2) × 5?", "-10", ["10", "-7", "7"]),
        ("What is 0 × (-15)?", "0", ["15", "-15", "1"]),
        ("What is (-18) + 18?", "0", ["18", "-18", "36"]),
        ("What is (-7) + 0?", "-7", ["7", "0", "-1"]),
        ("What is the value of (-1) × (-1)?", "1", ["-1", "0", "2"]),
        ("Which integer lies between -3 and -1?", "-2", ["-4", "0", "1"]),
        ("What is the sum of -10 and 4?", "-6", ["6", "-14", "14"]),
    ]

    return [create_question(q, a, w) for q, a, w in data]


def medium_questions():
    data = [
        ("Evaluate: (-15) + 8", "-7", ["7", "-23", "23"]),
        ("Evaluate: 25 + (-17)", "8", ["42", "-8", "-42"]),
        ("Evaluate: (-12) + (-18)", "-30", ["30", "-6", "6"]),
        ("Evaluate: (-20) - (-8)", "-12", ["-28", "12", "28"]),
        ("Evaluate: 15 - (-9)", "24", ["6", "-6", "-24"]),
        ("Evaluate: (-14) - 6", "-20", ["20", "-8", "8"]),
        ("Evaluate: (-7) × 8", "-56", ["56", "-15", "15"]),
        ("Evaluate: (-9) × (-6)", "54", ["-54", "15", "-15"]),
        ("Evaluate: 72 ÷ (-8)", "-9", ["9", "-8", "8"]),
        ("Evaluate: (-96) ÷ (-12)", "8", ["-8", "12", "-12"]),
        ("Evaluate: (-5) × 4 + 10", "-10", ["10", "-30", "30"]),
        ("Evaluate: 20 + (-4) × 3", "8", ["48", "-8", "12"]),
        ("Evaluate: (-18) ÷ 3 + 7", "1", ["-1", "13", "-13"]),
        ("Evaluate: 30 - 5 × 8", "-10", ["10", "200", "40"]),
        ("Evaluate: (-6) × (-3) - 10", "8", ["28", "-8", "18"]),
        ("What is the absolute value of -25 + 10?", "15", ["-15", "35", "25"]),
        ("Which is the greatest integer among -12, -5, -20 and -1?", "-1", ["-5", "-12", "-20"]),
        ("Which is the smallest integer among 8, -3, 0 and -10?", "-10", ["-3", "0", "8"]),
        ("What is the distance between -5 and 7 on a number line?", "12", ["2", "10", "13"]),
        ("What is the distance between -8 and -2?", "6", ["10", "4", "8"]),
        ("The temperature rises from -4°C to 9°C. What is the increase?", "13°C", ["5°C", "9°C", "12°C"]),
        ("A person owes Rs. 250 and pays Rs. 100. What is the remaining debt?", "Rs. 150", ["Rs. 350", "Rs. 100", "Rs. 250"]),
        ("What is the additive inverse of -35?", "35", ["-35", "0", "1"]),
        ("What is the product of three negative integers?", "Negative", ["Positive", "Zero", "Cannot be determined"]),
        ("What is the sign of (-2) × (-3) × 4?", "Positive", ["Negative", "Zero", "Cannot be determined"]),
        ("Evaluate: (-4)²", "16", ["-16", "8", "-8"]),
        ("Evaluate: -4²", "-16", ["16", "8", "-8"]),
        ("What is (-3)³?", "-27", ["27", "-9", "9"]),
        ("Evaluate: (-2)⁴", "16", ["-16", "8", "-8"]),
        ("What is the value of 45 ÷ (-5) × 2?", "-18", ["18", "-9", "9"]),
    ]

    return [create_question(q, a, w) for q, a, w in data]


def hard_questions():
    data = [
        ("Evaluate: (-25) + 18 - 12", "-19", ["19", "-31", "31"]),
        ("Evaluate: 40 - (-15) + (-25)", "30", ["60", "-30", "20"]),
        ("Evaluate: (-12) × 5 + 20", "-40", ["40", "-80", "80"]),
        ("Evaluate: (-8) × (-7) - 60", "-4", ["4", "116", "-116"]),
        ("Evaluate: 144 ÷ (-12) + 25", "13", ["-13", "37", "-37"]),
        ("Evaluate: (-96) ÷ 8 - 15", "-27", ["27", "-3", "3"]),
        ("Evaluate: (-15) × (-4) ÷ 10", "6", ["-6", "60", "-60"]),
        ("Evaluate: 50 - [(-5) × 8]", "90", ["10", "-90", "40"]),
        ("Evaluate: (-3) × [8 + (-12)]", "12", ["-12", "60", "-60"]),
        ("Evaluate: 72 ÷ [(-3) × 4]", "-6", ["6", "-9", "9"]),
        ("Evaluate: (-5)² + (-3)²", "34", ["-34", "16", "64"]),
        ("Evaluate: (-4)³ + 20", "-44", ["44", "-84", "84"]),
        ("Evaluate: (-2)⁵ × (-2)", "64", ["-64", "32", "-32"]),
        ("Evaluate: (-3)² × (-2)³", "-72", ["72", "-36", "36"]),
        ("Evaluate: (-6)² - 5 × 8", "-4", ["4", "64", "76"]),
        ("The sum of two integers is -15. One integer is 8. Find the other.", "-23", ["23", "-7", "7"]),
        ("The difference between two integers is 12. If the smaller integer is -5, find the larger integer.", "7", ["-17", "17", "-7"]),
        ("The product of two integers is -72. If one integer is 9, find the other.", "-8", ["8", "-9", "9"]),
        ("The quotient of two integers is -7. If the divisor is 5, find the dividend.", "-35", ["35", "-12", "12"]),
        ("A submarine is 120 metres below sea level and rises 45 metres. What is its new position?", "-75 metres", ["75 metres", "-165 metres", "165 metres"]),
        ("The temperature is -8°C. It decreases by 7°C and then increases by 12°C. Find the final temperature.", "-3°C", ["3°C", "-27°C", "11°C"]),
        ("A bank account has a balance of -Rs. 500. A deposit of Rs. 800 is made. Find the new balance.", "Rs. 300", ["-Rs. 300", "Rs. 1300", "-Rs. 1300"]),
        ("A lift is on the 4th floor and moves down 9 floors. Which floor does it reach?", "-5", ["5", "-13", "13"]),
        ("Find the integer whose product with -12 is 144.", "-12", ["12", "-24", "24"]),
        ("If x + (-18) = -7, find x.", "11", ["-11", "25", "-25"]),
        ("If x - 15 = -22, find x.", "-7", ["7", "-37", "37"]),
        ("If -6x = 54, find x.", "-9", ["9", "-48", "48"]),
        ("Evaluate: [(-40) + 16] ÷ (-4)", "6", ["-6", "14", "-14"]),
        ("Evaluate: (-7) × [(-5) + 9] - 12", "-40", ["-16", "16", "40"]),
        ("Evaluate: 100 ÷ (-5) + (-6) × 4", "-44", ["44", "-4", "4"]),
    ]

    return [create_question(q, a, w) for q, a, w in data]


def main():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
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
            raise RuntimeError("Integers lesson was not found.")

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
        print("INTEGERS SEEDING COMPLETED")
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
