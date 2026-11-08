import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

TOPIC = "Fractions"
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
        ("What is a fraction?", "A part of a whole", ["A whole number", "A negative number", "A decimal only"]),
        ("What is the numerator in 3/5?", "3", ["5", "8", "2"]),
        ("What is the denominator in 7/9?", "9", ["7", "16", "2"]),
        ("Which fraction represents one-half?", "1/2", ["1/3", "1/4", "2/3"]),
        ("Which of these is a proper fraction?", "3/5", ["5/3", "7/4", "9/2"]),
        ("Which of these is an improper fraction?", "7/4", ["2/5", "3/8", "1/4"]),
        ("Which fraction is equivalent to 1/2?", "2/4", ["1/3", "3/5", "2/5"]),
        ("What is 1/4 + 1/4?", "1/2", ["1/4", "2/3", "3/4"]),
        ("What is 2/5 + 1/5?", "3/5", ["3/10", "1/5", "2/5"]),
        ("What is 4/7 - 2/7?", "2/7", ["6/7", "2/14", "1/7"]),
        ("What is 3/8 + 2/8?", "5/8", ["5/16", "1/8", "6/8"]),
        ("What is 5/9 - 2/9?", "3/9", ["7/9", "3/18", "2/9"]),
        ("Which fraction is greater?", "3/4", ["1/4", "1/2", "1/3"]),
        ("Which fraction is smaller?", "1/5", ["3/5", "4/5", "2/5"]),
        ("What is 1/2 of 10?", "5", ["2", "10", "20"]),
        ("What is 1/4 of 20?", "5", ["4", "10", "8"]),
        ("What is 2/3 of 12?", "8", ["6", "4", "9"]),
        ("Convert 1 1/2 into an improper fraction.", "3/2", ["2/3", "4/2", "5/2"]),
        ("Convert 5/2 into a mixed number.", "2 1/2", ["1 1/2", "2 1/3", "3 1/2"]),
        ("What is the reciprocal of 2/3?", "3/2", ["2/3", "3/4", "1/2"]),
        ("What is the reciprocal of 5?", "1/5", ["5/1", "1/10", "5/2"]),
        ("What is 1/3 × 3?", "1", ["1/3", "3", "2"]),
        ("What is 1/2 × 1/2?", "1/4", ["1/2", "1/3", "2/4"]),
        ("What is 2/3 × 3/4?", "1/2", ["5/7", "6/7", "2/4"]),
        ("What is 1/2 ÷ 1/2?", "1", ["1/4", "2", "1/2"]),
        ("Which fraction has numerator 1?", "1/7", ["2/7", "3/7", "4/7"]),
        ("What is the simplest form of 2/4?", "1/2", ["2/2", "1/4", "2/3"]),
        ("What is the simplest form of 6/9?", "2/3", ["3/4", "1/3", "2/9"]),
        ("How many quarters make one whole?", "4", ["2", "3", "5"]),
        ("Which fraction represents a whole?", "4/4", ["1/4", "2/4", "3/4"]),
    ]

    return [create_question(q, a, w) for q, a, w in data]


def medium_questions():
    data = [
        ("Simplify 12/18.", "2/3", ["3/4", "4/5", "1/3"]),
        ("Simplify 15/25.", "3/5", ["2/5", "5/6", "1/5"]),
        ("Simplify 24/36.", "2/3", ["3/4", "4/9", "1/2"]),
        ("What is 2/3 + 1/6?", "5/6", ["3/9", "1/2", "4/6"]),
        ("What is 3/4 + 1/8?", "7/8", ["4/12", "5/8", "1"]),
        ("What is 5/6 - 1/3?", "1/2", ["2/3", "4/3", "1/3"]),
        ("What is 7/10 - 2/5?", "3/10", ["5/10", "1/2", "2/10"]),
        ("What is 2/5 + 3/10?", "7/10", ["5/15", "1/2", "6/10"]),
        ("What is 3/4 × 2/5?", "3/10", ["6/9", "5/20", "2/5"]),
        ("What is 4/7 × 7/8?", "1/2", ["4/8", "7/15", "2/7"]),
        ("What is 5/6 × 3/10?", "1/4", ["15/16", "1/2", "3/5"]),
        ("What is 2/3 ÷ 4/5?", "5/6", ["8/15", "6/5", "2/5"]),
        ("What is 3/4 ÷ 1/2?", "3/2", ["3/8", "2/3", "1/2"]),
        ("Convert 17/5 into a mixed number.", "3 2/5", ["2 3/5", "3 1/5", "4 2/5"]),
        ("Convert 4 2/3 into an improper fraction.", "14/3", ["12/3", "10/3", "13/3"]),
        ("Which fraction is equivalent to 4/7?", "12/21", ["8/14", "6/14", "10/21"]),
        ("Which is the greatest fraction?", "5/6", ["3/4", "2/3", "1/2"]),
        ("Arrange 1/2, 1/4 and 3/4 in ascending order.", "1/4, 1/2, 3/4", ["3/4, 1/2, 1/4", "1/2, 1/4, 3/4", "1/4, 3/4, 1/2"]),
        ("What fraction of an hour is 15 minutes?", "1/4", ["1/2", "1/3", "3/4"]),
        ("What fraction of a day is 6 hours?", "1/4", ["1/2", "1/3", "1/6"]),
        ("A pizza is divided into 8 equal slices. If 3 are eaten, what fraction remains?", "5/8", ["3/8", "4/8", "6/8"]),
        ("Ravi reads 2/5 of a book. What fraction is left unread?", "3/5", ["2/5", "1/5", "4/5"]),
        ("What is 3/5 of 40?", "24", ["20", "18", "30"]),
        ("What is 5/8 of 64?", "40", ["32", "48", "36"]),
        ("What is the missing numerator in ?/12 = 2/3?", "8", ["6", "4", "9"]),
        ("What is the missing denominator in 3/? = 1/4?", "12", ["9", "8", "6"]),
        ("What is the difference between 5/6 and 1/3?", "1/2", ["2/3", "1/3", "4/6"]),
        ("What is 1 1/2 + 2 1/2?", "4", ["3", "3 1/2", "4 1/2"]),
        ("What is 3 1/4 - 1 1/4?", "2", ["1", "2 1/2", "3"]),
        ("What is 2 1/2 × 2?", "5", ["4", "3", "6"]),
    ]

    return [create_question(q, a, w) for q, a, w in data]


def hard_questions():
    data = [
        ("Evaluate: 2/3 + 3/4.", "17/12", ["5/7", "6/12", "13/12"]),
        ("Evaluate: 5/6 - 2/9.", "11/18", ["3/3", "7/18", "13/18"]),
        ("Evaluate: 7/8 - 1/3.", "13/24", ["6/5", "11/24", "5/24"]),
        ("Evaluate: 3/5 + 7/10 - 1/2.", "4/5", ["3/5", "1/2", "9/10"]),
        ("Evaluate: 2/3 × 9/10 × 5/6.", "1/2", ["2/3", "3/5", "5/6"]),
        ("Evaluate: 5/8 ÷ 15/16.", "2/3", ["3/2", "5/6", "1/3"]),
        ("Evaluate: 3/4 ÷ 9/16.", "4/3", ["3/4", "2/3", "9/12"]),
        ("Evaluate: 1 1/2 + 2 2/3.", "4 1/6", ["3 5/6", "4 2/3", "3 1/6"]),
        ("Evaluate: 5 1/4 - 2 2/3.", "2 7/12", ["3 1/12", "2 5/12", "3 7/12"]),
        ("Evaluate: 2 1/2 × 1 1/5.", "3", ["2 1/2", "3 1/2", "4"]),
        ("Evaluate: 3 1/3 ÷ 1 2/3.", "2", ["1", "3", "2 1/2"]),
        ("Find 7/12 of 144.", "84", ["72", "96", "108"]),
        ("Find 5/9 of 162.", "90", ["81", "72", "99"]),
        ("A tank is 3/5 full. If its capacity is 200 litres, how much water is inside?", "120 litres", ["100 litres", "150 litres", "80 litres"]),
        ("A student completes 3/8 of a project on Monday and 1/4 on Tuesday. What fraction is completed?", "5/8", ["4/12", "3/8", "7/8"]),
        ("A rope is 15 metres long. If 2/5 is cut off, how much remains?", "9 metres", ["6 metres", "10 metres", "12 metres"]),
        ("A person spends 2/7 of their money and has Rs. 500 left. What was the original amount?", "Rs. 700", ["Rs. 600", "Rs. 750", "Rs. 800"]),
        ("If 3/4 of a number is 48, find the number.", "64", ["60", "56", "72"]),
        ("If 5/6 of a number is 50, find the number.", "60", ["55", "65", "75"]),
        ("Which fraction is greater: 7/12 or 5/8?", "5/8", ["7/12", "Both are equal", "Cannot be determined"]),
        ("Find the fraction between 1/3 and 1/2 with denominator 12.", "5/12", ["4/12", "6/12", "7/12"]),
        ("What is the sum of the reciprocals of 2/3 and 3/4?", "17/6", ["17/12", "13/6", "5/6"]),
        ("Evaluate: (2/5 + 1/10) ÷ 1/2.", "1", ["1/2", "2", "3/2"]),
        ("Evaluate: (3/4 × 8/9) + 1/3.", "1", ["2/3", "5/6", "4/3"]),
        ("A container has 5/6 litre of juice. If 1/3 litre is consumed, how much remains?", "1/2 litre", ["2/3 litre", "1/3 litre", "5/9 litre"]),
        ("A class has 40 students. If 3/5 are girls, how many are boys?", "16", ["24", "20", "18"]),
        ("A farmer uses 2/5 of his land for rice and 1/4 for wheat. What fraction remains unused?", "7/20", ["13/20", "3/20", "9/20"]),
        ("A water tank is 2/3 full. After adding 20 litres, it becomes 5/6 full. Find its capacity.", "120 litres", ["100 litres", "90 litres", "150 litres"]),
        ("Find x if x/15 = 4/5.", "12", ["10", "9", "15"]),
        ("Find x if 3/8 of x = 27.", "72", ["64", "81", "96"]),
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
            raise RuntimeError("Fractions lesson was not found.")

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
        print("FRACTIONS SEEDING COMPLETED")
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