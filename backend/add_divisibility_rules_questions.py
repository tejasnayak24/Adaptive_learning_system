import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

TOPIC = "Divisibility Rules"
SUBJECT = "Mathematics"

random.seed(42)

EASY = [
    ("Which digit makes 42_ divisible by 2?", "0", ["3", "5", "7"]),
    ("Which number is divisible by 5?", "125", ["123", "127", "128"]),
    ("A number is divisible by 10 if its last digit is:", "0", ["2", "5", "8"]),
    ("Which of these numbers is divisible by 3?", "123", ["124", "125", "127"]),
    ("Which number is divisible by 2?", "246", ["135", "157", "221"]),
    ("Which number is divisible by 5?", "340", ["342", "343", "347"]),
    ("A number is divisible by 3 if the sum of its digits is divisible by:", "3", ["2", "5", "10"]),
    ("Which number is divisible by 10?", "450", ["451", "455", "458"]),
    ("Is 728 divisible by 2?", "Yes", ["No", "Only by 5", "Cannot be determined"]),
    ("Which number is divisible by both 2 and 5?", "60", ["32", "45", "27"]),
    ("Which of these numbers is divisible by 3?", "111", ["112", "113", "115"]),
    ("Which number is divisible by 5?", "275", ["271", "272", "273"]),
    ("Which number is divisible by 2 and 10?", "80", ["42", "55", "65"]),
    ("What is the last digit of a number divisible by 10?", "0", ["1", "5", "9"]),
    ("Which number is divisible by 3?", "222", ["221", "224", "226"]),
    ("Is 999 divisible by 3?", "Yes", ["No", "Only by 2", "Only by 5"]),
    ("Which number is divisible by 2?", "864", ["863", "865", "867"]),
    ("Which number is divisible by 5?", "515", ["511", "512", "514"]),
    ("Which number is divisible by 10?", "120", ["121", "125", "128"]),
    ("Which number is divisible by 3?", "321", ["322", "323", "325"]),
    ("A number ending in an even digit is divisible by:", "2", ["3", "5", "10"]),
    ("Which number is divisible by both 3 and 5?", "135", ["132", "134", "137"]),
    ("Is 450 divisible by 5?", "Yes", ["No", "Only by 2", "Cannot be determined"]),
    ("Which number is divisible by 2?", "1002", ["1001", "1003", "1005"]),
    ("Which number is divisible by 10?", "670", ["671", "675", "678"]),
    ("Which number is divisible by 3?", "456", ["457", "458", "460"]),
    ("Which number is divisible by 5?", "890", ["891", "892", "893"]),
    ("What is the divisibility rule for 2?", "Last digit is even", ["Last digit is 5", "Sum of digits is 2", "Last digit is 0"]),
    ("What is the divisibility rule for 10?", "Last digit is 0", ["Last digit is even", "Sum of digits is 10", "Last digit is 5"]),
    ("Which number is divisible by both 2 and 3?", "126", ["125", "127", "131"]),
]

MEDIUM = [
    ("Is 234 divisible by 6?", "Yes", ["No", "Only by 3", "Only by 2"]),
    ("Which number is divisible by 9?", "729", ["728", "731", "734"]),
    ("Which number is divisible by 4?", "316", ["315", "317", "319"]),
    ("A number is divisible by 8 if its last three digits are divisible by:", "8", ["4", "6", "10"]),
    ("Which number is divisible by 11?", "121", ["123", "125", "127"]),
    ("Is 1,248 divisible by 8?", "Yes", ["No", "Only by 4", "Only by 6"]),
    ("Which number is divisible by 6?", "132", ["133", "135", "137"]),
    ("Which number is divisible by 9?", "567", ["568", "569", "571"]),
    ("Which number is divisible by 4?", "524", ["525", "526", "527"]),
    ("Which number is divisible by 11?", "242", ["243", "245", "247"]),
    ("Is 3,456 divisible by 8?", "Yes", ["No", "Only by 4", "Only by 6"]),
    ("Which number is divisible by both 4 and 6?", "120", ["122", "124", "126"]),
    ("Which number is divisible by 9?", "891", ["892", "893", "895"]),
    ("Is 1,452 divisible by 11?", "Yes", ["No", "Only by 3", "Only by 5"]),
    ("Which number is divisible by 8?", "1,016", ["1,014", "1,015", "1,017"]),
    ("Which number is divisible by 6?", "246", ["245", "247", "249"]),
    ("What is the divisibility rule for 9?", "Sum of digits is divisible by 9", ["Last digit is 9", "Last two digits are divisible by 9", "Number is even"]),
    ("What is the divisibility rule for 4?", "Last two digits are divisible by 4", ["Last digit is even", "Sum of digits is divisible by 4", "Last three digits are divisible by 4"]),
    ("Which number is divisible by both 8 and 10?", "1,120", ["1,122", "1,125", "1,128"]),
    ("Is 5,184 divisible by 9?", "Yes", ["No", "Only by 3", "Only by 8"]),
    ("Which number is divisible by 11?", "363", ["364", "365", "367"]),
    ("Which number is divisible by 4?", "1,236", ["1,237", "1,239", "1,241"]),
    ("Which number is divisible by 6?", "318", ["319", "320", "323"]),
    ("Is 2,016 divisible by 8?", "Yes", ["No", "Only by 4", "Only by 6"]),
    ("Which number is divisible by 9?", "1,458", ["1,457", "1,459", "1,461"]),
    ("Which number is divisible by both 3 and 11?", "132", ["133", "134", "136"]),
    ("Which number is divisible by 8?", "2,048", ["2,046", "2,047", "2,049"]),
    ("Is 726 divisible by 11?", "Yes", ["No", "Only by 3", "Only by 6"]),
    ("Which number is divisible by 6 but not by 9?", "114", ["126", "144", "162"]),
    ("Which number is divisible by both 4 and 9?", "144", ["142", "146", "148"]),
]

HARD = [
    ("Find the digit x if 47x is divisible by 3.", "1", ["2", "3", "5"]),
    ("Find the smallest digit x if 52x is divisible by 9.", "2", ["3", "4", "5"]),
    ("Which digit should replace x in 63x2 to make it divisible by 4?", "1", ["2", "3", "5"]),
    ("Find the digit x if 8x4 is divisible by 9.", "6", ["5", "7", "8"]),
    ("Which digit x makes 35x divisible by 5 and 3?", "5", ["2", "4", "7"]),
    ("Find the smallest digit x that makes 72x divisible by 6.", "0", ["1", "2", "3"]),
    ("Find the digit x if 4x8 is divisible by 11.", "2", ["1", "3", "4"]),
    ("Which digit x makes 12x4 divisible by 8?", "0", ["1", "2", "3"]),
    ("Find the smallest digit x if 56x is divisible by 9.", "7", ["5", "6", "8"]),
    ("Which digit x makes 7x5 divisible by 3?", "1", ["2", "3", "5"]),
    ("Find the digit x if 3x6 is divisible by 11.", "0", ["1", "2", "3"]),
    ("Which digit x makes 24x divisible by both 2 and 3?", "0", ["1", "2", "5"]),
    ("Find the smallest digit x if 91x is divisible by 3.", "2", ["1", "3", "4"]),
    ("Which digit x makes 5x32 divisible by 4?", "0", ["1", "2", "3"]),
    ("Find the digit x if 6x3 is divisible by 9.", "3", ["2", "4", "5"]),
    ("Which digit x makes 42x divisible by 11?", "1", ["2", "3", "4"]),
    ("Find the smallest digit x if 38x is divisible by 6.", "4", ["2", "5", "6"]),
    ("Which digit x makes 1x24 divisible by 8?", "0", ["1", "2", "3"]),
    ("Find the digit x if 2x5 is divisible by 5 and 3.", "2", ["1", "3", "4"]),
    ("Which digit x makes 73x2 divisible by 4 and 3?", "1", ["2", "3", "5"]),
    ("Find the smallest digit x if 64x is divisible by 9.", "8", ["6", "7", "9"]),
    ("Which digit x makes 8x1 divisible by 11?", "9", ["7", "8", "6"]),
    ("Find the digit x if 15x6 is divisible by 9.", "6", ["4", "5", "7"]),
    ("Which digit x makes 32x divisible by 6?", "4", ["1", "2", "5"]),
    ("Find the smallest digit x if 7x2 is divisible by 9.", "0", ["1", "2", "3"]),
    ("Which digit x makes 4x56 divisible by 8?", "0", ["1", "2", "3"]),
    ("Find the digit x if 9x9 is divisible by 11.", "0", ["1", "2", "3"]),
    ("Which digit x makes 25x divisible by 9?", "2", ["1", "3", "4"]),
    ("Find the smallest digit x if 83x is divisible by 6.", "4", ["2", "3", "5"]),
    ("Which digit x makes 6x12 divisible by 9?", "0", ["1", "2", "3"]),
]


def make_questions(data):
    questions = []

    for question, answer, wrong_answers in data:
        options = [answer] + wrong_answers[:]
        random.shuffle(options)

        correct_answer = ["A", "B", "C", "D"][options.index(answer)]

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
    total_inserted = 0

    difficulty_data = {
        "Easy": EASY,
        "Medium": MEDIUM,
        "Hard": HARD
    }

    for difficulty, data in difficulty_data.items():
        cursor.execute(
            """
            SELECT id FROM quizzes
            WHERE lesson_id = ? AND LOWER(difficulty) = LOWER(?)
            """,
            (lesson_id, difficulty)
        )

        quiz = cursor.fetchone()

        if not quiz:
            print(f"{difficulty} quiz not found for {TOPIC}")
            continue

        quiz_id = quiz[0]
        questions = make_questions(data)
        inserted = 0

        for q in questions:
            cursor.execute(
                "SELECT 1 FROM questions WHERE quiz_id = ? AND question = ?",
                (quiz_id, q[0])
            )

            if cursor.fetchone():
                continue

            cursor.execute(
                """
                INSERT INTO questions
                (quiz_id, question, option_a, option_b,
                 option_c, option_d, correct_answer)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (quiz_id, *q)
            )

            inserted += 1

        total_inserted += inserted
        print(f"{difficulty}: {inserted} questions inserted.")

    conn.commit()
    conn.close()

    print(f"\nCompleted! Total new questions inserted: {total_inserted}")


if __name__ == "__main__":
    main()