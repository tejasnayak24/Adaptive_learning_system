import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

TOPIC = "Decimals"
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
        ("What is the decimal form of 1/10?", "0.1", ["0.01", "1.0", "0.001"]),
        ("What is the decimal form of 1/2?", "0.5", ["0.2", "0.25", "0.75"]),
        ("What is the decimal form of 1/4?", "0.25", ["0.5", "0.4", "0.75"]),
        ("How many decimal places are there in 2.35?", "2", ["1", "3", "4"]),
        ("What is the place value of 5 in 3.56?", "0.05", ["0.5", "5", "0.005"]),
        ("What is the place value of 7 in 4.72?", "0.7", ["0.07", "7", "0.007"]),
        ("Which is the greatest decimal?", "0.9", ["0.5", "0.7", "0.3"]),
        ("Which is the smallest decimal?", "0.12", ["0.21", "0.5", "0.8"]),
        ("What is 0.5 + 0.2?", "0.7", ["0.3", "0.6", "0.8"]),
        ("What is 0.8 - 0.3?", "0.5", ["0.4", "0.6", "0.7"]),
        ("What is 1.2 + 2.3?", "3.5", ["3.4", "2.5", "4.5"]),
        ("What is 5.6 - 2.1?", "3.5", ["3.4", "4.5", "2.5"]),
        ("What is 0.5 × 2?", "1.0", ["0.5", "2.5", "1.5"]),
        ("What is 0.4 × 10?", "4", ["0.4", "40", "0.04"]),
        ("What is 25.5 ÷ 5?", "5.1", ["5.5", "4.1", "6.1"]),
        ("What is 3.5 + 1.5?", "5", ["4", "6", "5.5"]),
        ("How many tenths make one whole?", "10", ["5", "100", "2"]),
        ("How many hundredths make one whole?", "100", ["10", "50", "1000"]),
        ("Which fraction is equal to 0.75?", "3/4", ["1/4", "1/2", "2/5"]),
        ("Which fraction is equal to 0.2?", "1/5", ["1/2", "1/4", "2/5"]),
        ("Convert 3/10 into a decimal.", "0.3", ["0.03", "3.0", "0.003"]),
        ("Convert 7/100 into a decimal.", "0.07", ["0.7", "7.0", "0.007"]),
        ("What is 2.5 × 10?", "25", ["2.5", "250", "0.25"]),
        ("What is 45.6 ÷ 10?", "4.56", ["45.06", "456", "0.456"]),
        ("Which decimal represents five and six tenths?", "5.6", ["5.06", "56.0", "0.56"]),
        ("What is the value of 0.01?", "One hundredth", ["One tenth", "One whole", "One thousandth"]),
        ("Round 4.6 to the nearest whole number.", "5", ["4", "6", "4.5"]),
        ("Round 7.2 to the nearest whole number.", "7", ["8", "6", "7.5"]),
        ("How is 0.50 written as a simplified fraction?", "1/2", ["1/5", "5/10", "1/4"]),
        ("What is 10.0 + 0.5?", "10.5", ["10.05", "10.0", "11.5"]),
    ]

    return [create_question(q, a, w) for q, a, w in data]


def medium_questions():
    data = [
        ("What is 12.45 + 7.35?", "19.80", ["19.70", "20.80", "18.80"]),
        ("What is 25.60 - 8.45?", "17.15", ["17.25", "16.15", "18.15"]),
        ("What is 3.25 × 4?", "13", ["12", "13.5", "14"]),
        ("What is 2.5 × 1.2?", "3", ["2.5", "3.5", "4"]),
        ("What is 4.8 ÷ 0.6?", "8", ["6", "7", "9"]),
        ("What is 7.5 ÷ 0.5?", "15", ["10", "12", "20"]),
        ("Convert 0.625 into a fraction in simplest form.", "5/8", ["3/8", "1/2", "7/8"]),
        ("Convert 0.375 into a fraction in simplest form.", "3/8", ["1/4", "5/8", "3/4"]),
        ("Convert 7/20 into a decimal.", "0.35", ["0.7", "0.25", "0.75"]),
        ("Convert 13/25 into a decimal.", "0.52", ["0.25", "0.13", "0.65"]),
        ("Which is greater: 0.65 or 0.605?", "0.65", ["0.605", "Both are equal", "Cannot be determined"]),
        ("Arrange 0.4, 0.04 and 0.44 in ascending order.", "0.04, 0.4, 0.44", ["0.4, 0.04, 0.44", "0.44, 0.4, 0.04", "0.04, 0.44, 0.4"]),
        ("Round 8.746 to two decimal places.", "8.75", ["8.74", "8.70", "8.76"]),
        ("Round 12.348 to one decimal place.", "12.3", ["12.4", "12.35", "12.0"]),
        ("What is 0.25 × 0.4?", "0.1", ["1.0", "0.01", "0.5"]),
        ("What is 1.25 × 0.8?", "1", ["0.1", "10", "1.5"]),
        ("What is 6.72 ÷ 0.8?", "8.4", ["0.84", "84", "7.4"]),
        ("What is 15.75 ÷ 2.5?", "6.3", ["6.5", "5.3", "7.3"]),
        ("What is 3.45 + 2.7 + 1.05?", "7.2", ["7.0", "6.2", "8.2"]),
        ("What is 20 - 3.75?", "16.25", ["17.25", "16.75", "15.25"]),
        ("What is the value of 0.6²?", "0.36", ["0.12", "0.6", "0.06"]),
        ("What is 0.3 × 0.3 × 10?", "0.9", ["0.09", "9", "0.03"]),
        ("A pencil costs Rs. 4.50. What is the cost of 6 pencils?", "Rs. 27", ["Rs. 24", "Rs. 26", "Rs. 30"]),
        ("A ribbon of 5.5 metres is cut into 5 equal pieces. Find the length of each piece.", "1.1 metres", ["1.5 metres", "0.11 metres", "2.1 metres"]),
        ("A bottle contains 1.5 litres of water. How much water is there in 4 bottles?", "6 litres", ["5 litres", "4.5 litres", "7 litres"]),
        ("A person has Rs. 100 and spends Rs. 37.50. How much remains?", "Rs. 62.50", ["Rs. 63.50", "Rs. 72.50", "Rs. 52.50"]),
        ("What is the place value of 8 in 12.084?", "0.08", ["0.8", "0.008", "8"]),
        ("How many thousandths are there in 0.125?", "125", ["12.5", "25", "100"]),
        ("What is 0.09 × 100?", "9", ["0.9", "90", "0.009"]),
        ("What is 56.7 ÷ 100?", "0.567", ["5.67", "56.07", "0.0567"]),
    ]

    return [create_question(q, a, w) for q, a, w in data]


def hard_questions():
    data = [
        ("Evaluate: 12.5 + 3.75 - 4.8.", "11.45", ["10.45", "12.45", "11.55"]),
        ("Evaluate: 5.6 × 2.5.", "14", ["12", "13", "15"]),
        ("Evaluate: 8.4 ÷ 0.07.", "120", ["12", "60", "140"]),
        ("Evaluate: 0.125 × 0.64.", "0.08", ["0.8", "0.008", "0.16"]),
        ("Evaluate: 15.75 ÷ 0.25.", "63", ["6.3", "62", "75"]),
        ("Evaluate: (2.5 + 1.75) × 4.", "17", ["16", "18", "15"]),
        ("Evaluate: 20.5 - (3.25 × 4).", "7.5", ["8.5", "6.5", "9.5"]),
        ("Evaluate: 4.8 × 0.25 + 1.6.", "2.8", ["2.4", "3.2", "4.0"]),
        ("Evaluate: 18.9 ÷ 0.3 - 12.5.", "50.5", ["49.5", "51.5", "52.5"]),
        ("Evaluate: (6.4 ÷ 0.8) × 1.25.", "10", ["8", "9", "12"]),
        ("Convert 0.875 into a fraction in simplest form.", "7/8", ["5/8", "3/4", "9/8"]),
        ("Convert 0.0625 into a fraction in simplest form.", "1/16", ["1/8", "1/12", "1/32"]),
        ("Convert 17/40 into a decimal.", "0.425", ["0.45", "0.375", "0.475"]),
        ("What is the difference between 0.8 and 0.008?", "0.792", ["0.78", "0.802", "0.72"]),
        ("Round 45.6789 to three decimal places.", "45.679", ["45.678", "45.68", "45.670"]),
        ("A car travels 12.5 km per litre. How far will it travel using 8 litres?", "100 km", ["90 km", "110 km", "80 km"]),
        ("A shopkeeper buys 2.5 kg of rice at Rs. 48.50 per kg. Find the total cost.", "Rs. 121.25", ["Rs. 120.25", "Rs. 122.50", "Rs. 125.25"]),
        ("A tank contains 25.5 litres of water. If 8.75 litres are removed, how much remains?", "16.75 litres", ["17.75 litres", "15.75 litres", "16.25 litres"]),
        ("A wire of 18.6 metres is divided into 6 equal pieces. Find each piece's length.", "3.1 metres", ["3.6 metres", "2.1 metres", "4.1 metres"]),
        ("A student scores 78.5, 85.5 and 91 marks. Find the average.", "85", ["84", "86", "87"]),
        ("A shirt costs Rs. 750.50 and a pair of trousers costs Rs. 925.75. Find their total cost.", "Rs. 1676.25", ["Rs. 1675.25", "Rs. 1686.25", "Rs. 1576.25"]),
        ("A person earns Rs. 1250.75 and spends Rs. 875.50. Find the savings.", "Rs. 375.25", ["Rs. 385.25", "Rs. 374.25", "Rs. 475.25"]),
        ("If 0.4 of a number is 18, find the number.", "45", ["40", "42", "50"]),
        ("If 2.5 times a number is 37.5, find the number.", "15", ["12", "25", "18"]),
        ("What is the value of 0.2 × 0.02 × 0.002?", "0.000008", ["0.0008", "0.00008", "0.008"]),
        ("Evaluate: 0.75 ÷ 0.015.", "50", ["5", "25", "75"]),
        ("Evaluate: (12.6 - 4.8) ÷ 0.6.", "13", ["12", "14", "15"]),
        ("A container holds 3.75 litres. How many such containers are needed to hold 30 litres?", "8", ["6", "7", "9"]),
        ("A shopkeeper sells an item for Rs. 125.50 after making a profit of Rs. 25.75. Find its cost price.", "Rs. 99.75", ["Rs. 100.75", "Rs. 101.25", "Rs. 98.75"]),
        ("Evaluate: 2.4 × (3.5 - 1.25) + 0.6.", "6", ["5.4", "6.6", "5.8"]),
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
            raise RuntimeError("Decimals lesson was not found.")

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
        print("DECIMALS SEEDING COMPLETED")
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