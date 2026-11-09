import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"
TOPIC = "Factors and Multiples"
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
    ("What is a factor of 12?", "3", ["5", "7", "8"]),
    ("Which of these is a factor of 10?", "5", ["3", "4", "6"]),
    ("Which number is a multiple of 4?", "16", ["10", "14", "18"]),
    ("What is the smallest factor of every positive integer?", "1", ["0", "2", "10"]),
    ("What is the greatest factor of 15?", "15", ["5", "3", "1"]),
    ("Which number is a factor of 20?", "4", ["3", "6", "7"]),
    ("Which number is a multiple of 5?", "35", ["32", "33", "37"]),
    ("Is 24 a multiple of 6?", "Yes", ["No", "Only sometimes", "Cannot say"]),
    ("How many factors does 7 have?", "2", ["1", "3", "4"]),
    ("Which is a factor of 18?", "6", ["5", "7", "8"]),
    ("Which is a multiple of 3?", "21", ["20", "22", "25"]),
    ("What is the first positive multiple of 8?", "8", ["0", "4", "16"]),
    ("Which number is a factor of 16?", "8", ["3", "5", "6"]),
    ("Which number is NOT a factor of 12?", "5", ["2", "3", "4"]),
    ("What are the first three positive multiples of 2?", "2, 4, 6", ["1, 2, 3", "2, 3, 4", "4, 6, 8"]),
    ("Which number is a common factor of 8 and 12?", "4", ["5", "7", "9"]),
    ("Which number is a common multiple of 2 and 3?", "6", ["4", "8", "10"]),
    ("Is 1 a factor of 25?", "Yes", ["No", "Only for even numbers", "Cannot say"]),
    ("Which number has only two factors?", "Prime number", ["Composite number", "Even number", "Multiple"]),
    ("Which number is a composite number?", "9", ["2", "3", "5"]),
    ("What is the smallest prime number?", "2", ["1", "0", "3"]),
    ("What is the smallest composite number?", "4", ["1", "2", "3"]),
    ("Which number is divisible by 2?", "18", ["15", "21", "25"]),
    ("Which number is divisible by 10?", "50", ["45", "33", "27"]),
    ("What is a common factor of 10 and 15?", "5", ["4", "6", "8"]),
    ("Which is a multiple of 9?", "27", ["25", "28", "32"]),
    ("How many factors does 1 have?", "1", ["0", "2", "3"]),
    ("Is 36 a multiple of 9?", "Yes", ["No", "Only sometimes", "Cannot say"]),
    ("Which number is a factor of both 6 and 9?", "3", ["2", "4", "5"]),
    ("Which number is a multiple of both 3 and 4?", "12", ["6", "8", "9"]),
]

MEDIUM = [
    ("Find all factors of 12.", "1, 2, 3, 4, 6, 12", ["1, 2, 4, 8, 12", "2, 3, 6, 9", "1, 3, 5, 12"]),
    ("How many factors does 24 have?", "8", ["6", "7", "9"]),
    ("Find the first five positive multiples of 7.", "7, 14, 21, 28, 35", ["7, 14, 20, 28, 35", "7, 21, 28, 35, 42", "14, 21, 28, 35, 42"]),
    ("Which is the greatest common factor of 12 and 18?", "6", ["3", "9", "12"]),
    ("Find the common factors of 16 and 24.", "1, 2, 4, 8", ["1, 2, 4", "2, 4, 6, 8", "1, 3, 8"]),
    ("Which is the least common multiple of 4 and 6?", "12", ["6", "18", "24"]),
    ("Find the LCM of 5 and 8.", "40", ["20", "25", "45"]),
    ("Find the HCF of 20 and 30.", "10", ["5", "15", "20"]),
    ("Is 51 a prime or composite number?", "Composite", ["Prime", "Neither", "Both"]),
    ("Which pair consists of co-prime numbers?", "8 and 15", ["6 and 9", "10 and 20", "12 and 18"]),
    ("What is the prime factorisation of 12?", "2 × 2 × 3", ["2 × 3", "3 × 3 × 2", "2 × 2 × 2"]),
    ("What is the prime factorisation of 18?", "2 × 3 × 3", ["2 × 2 × 3", "3 × 3", "2 × 9"]),
    ("Find the HCF of 24 and 36.", "12", ["6", "18", "24"]),
    ("Find the LCM of 6 and 9.", "18", ["9", "27", "36"]),
    ("Which number is a common multiple of 4 and 10?", "20", ["12", "16", "18"]),
    ("How many factors does 36 have?", "9", ["6", "8", "10"]),
    ("Which of these is a factor of 48?", "12", ["10", "14", "18"]),
    ("Find the greatest common factor of 15, 25 and 35.", "5", ["10", "15", "25"]),
    ("Find the least common multiple of 3, 4 and 6.", "12", ["6", "18", "24"]),
    ("Which number is divisible by both 6 and 8?", "48", ["24", "32", "40"]),
    ("Find the prime factors of 30.", "2, 3, 5", ["2, 5, 10", "3, 5, 6", "2, 3, 10"]),
    ("Which number has exactly three factors?", "4", ["6", "8", "10"]),
    ("Find the HCF of 45 and 60.", "15", ["5", "10", "20"]),
    ("Find the LCM of 7 and 14.", "14", ["7", "21", "28"]),
    ("Which pair has an HCF of 1?", "9 and 16", ["8 and 12", "10 and 15", "14 and 21"]),
    ("What is the smallest common multiple of 8 and 12?", "24", ["12", "36", "48"]),
    ("Find the missing number: 6 × ? = 54.", "9", ["8", "7", "6"]),
    ("Which is the greatest factor of 42 other than 42?", "21", ["14", "7", "6"]),
    ("What is the prime factorisation of 60?", "2 × 2 × 3 × 5", ["2 × 3 × 10", "3 × 4 × 5", "2 × 2 × 15"]),
    ("Find the HCF of 32 and 48.", "16", ["8", "12", "24"]),
]

HARD = [
    ("Find the HCF of 72 and 120.", "24", ["12", "18", "36"]),
    ("Find the LCM of 18 and 24.", "72", ["36", "48", "96"]),
    ("Find the HCF of 84, 126 and 210.", "42", ["21", "28", "63"]),
    ("Find the LCM of 8, 12 and 15.", "120", ["60", "90", "180"]),
    ("What is the prime factorisation of 180?", "2 × 2 × 3 × 3 × 5", ["2 × 3 × 3 × 10", "2 × 2 × 5 × 9", "3 × 3 × 20"]),
    ("Find the smallest number divisible by 12, 15 and 20.", "60", ["30", "45", "120"]),
    ("Find the greatest number that divides 48 and 72 exactly.", "24", ["12", "18", "36"]),
    ("Two bells ring every 12 and 18 minutes. If they ring together now, after how many minutes will they ring together again?", "36 minutes", ["24 minutes", "30 minutes", "48 minutes"]),
    ("Three lights flash every 6, 8 and 12 seconds. When will they flash together again?", "24 seconds", ["12 seconds", "18 seconds", "36 seconds"]),
    ("Find the smallest 3-digit number divisible by 8.", "104", ["100", "108", "112"]),
    ("Find the greatest 2-digit number divisible by 7.", "98", ["91", "95", "99"]),
    ("Find the smallest number that leaves no remainder when divided by 5, 6 and 8.", "120", ["60", "90", "240"]),
    ("The HCF of two numbers is 6 and their LCM is 72. If one number is 18, find the other.", "24", ["12", "30", "36"]),
    ("The product of two numbers is 216 and their HCF is 6. Find their LCM.", "36", ["24", "42", "48"]),
    ("Find the number of factors of 72.", "12", ["10", "8", "14"]),
    ("How many factors does 100 have?", "9", ["8", "10", "12"]),
    ("Find the HCF of 96 and 144 using prime factorisation.", "48", ["24", "36", "72"]),
    ("Find the LCM of 16, 20 and 24.", "240", ["120", "180", "360"]),
    ("Two ropes of lengths 84 m and 126 m are cut into equal pieces of maximum length. Find the length of each piece.", "42 m", ["21 m", "28 m", "63 m"]),
    ("Three runners complete a lap in 40, 50 and 60 seconds. After how many seconds will they meet at the starting point together?", "600 seconds", ["300 seconds", "400 seconds", "500 seconds"]),
    ("Find the smallest number which is divisible by 9, 12 and 15.", "180", ["90", "120", "150"]),
    ("Find the greatest 3-digit number divisible by 12.", "996", ["984", "990", "999"]),
    ("Find the smallest 4-digit number divisible by 15.", "1005", ["1000", "1010", "1020"]),
    ("The HCF of 36 and x is 12. Which of these could be x?", "24", ["25", "30", "35"]),
    ("Two numbers are in the ratio 2:3 and their HCF is 5. Find their LCM.", "30", ["15", "25", "45"]),
    ("Find the number of distinct prime factors of 210.", "4", ["3", "5", "6"]),
    ("Find the sum of all factors of 12.", "28", ["24", "30", "32"]),
    ("Find the product of the HCF and LCM of 12 and 18.", "216", ["108", "180", "240"]),
    ("Find the smallest number that must be added to 85 to make it divisible by 9.", "5", ["4", "6", "8"]),
    ("Find the smallest number that must be subtracted from 100 to make it divisible by 7.", "2", ["1", "3", "5"]),
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
            raise RuntimeError("Factors and Multiples lesson was not found.")

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
        print("FACTORS AND MULTIPLES SEEDING COMPLETED")
        print("--------------------------------")
        print(f"Total new questions inserted: {total}")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()