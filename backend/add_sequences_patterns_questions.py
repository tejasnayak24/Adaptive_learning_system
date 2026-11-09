
import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

TOPIC = "Sequences and Patterns"
SUBJECT = "Mathematics"

random.seed(42)

# Format: (question, correct answer, [three wrong answers])

EASY = [
    ("Find the next number: 2, 4, 6, 8, __.", "10", ["9", "11", "12"]),
    ("Find the next number: 5, 10, 15, 20, __.", "25", ["22", "24", "30"]),
    ("Find the next number: 3, 6, 9, 12, __.", "15", ["14", "16", "18"]),
    ("Find the next number: 1, 2, 3, 4, __.", "5", ["6", "7", "8"]),
    ("Find the next number: 10, 20, 30, 40, __.", "50", ["45", "55", "60"]),
    ("Find the next number: 2, 4, 8, 16, __.", "32", ["24", "30", "36"]),
    ("Find the next number: 1, 3, 5, 7, __.", "9", ["8", "10", "11"]),
    ("Find the next number: 10, 9, 8, 7, __.", "6", ["5", "7", "4"]),
    ("Find the next number: 100, 90, 80, 70, __.", "60", ["65", "55", "50"]),
    ("Find the next number: 1, 4, 9, 16, __.", "25", ["20", "24", "36"]),
    ("Find the next number: 1, 8, 27, 64, __.", "125", ["100", "120", "144"]),
    ("Find the next number: 2, 5, 8, 11, __.", "14", ["13", "15", "16"]),
    ("Find the next number: 7, 14, 21, 28, __.", "35", ["32", "36", "42"]),
    ("Find the next number: 50, 45, 40, 35, __.", "30", ["25", "32", "28"]),
    ("Find the next number: 3, 9, 27, 81, __.", "243", ["162", "180", "324"]),
    ("Find the next number: 4, 8, 12, 16, __.", "20", ["18", "22", "24"]),
    ("Find the next number: 11, 22, 33, 44, __.", "55", ["50", "54", "66"]),
    ("Find the next number: 2, 3, 5, 8, 12, __.", "17", ["15", "16", "18"]),
    ("Find the next number: 1, 1, 2, 3, 5, __.", "8", ["7", "9", "10"]),
    ("Find the next number: 20, 18, 16, 14, __.", "12", ["10", "13", "11"]),
    ("How many terms are there in the sequence 2, 4, 6, 8, 10?", "5", ["4", "6", "10"]),
    ("What is the common difference in 4, 7, 10, 13, ...?", "3", ["2", "4", "5"]),
    ("What is the common ratio in 2, 6, 18, 54, ...?", "3", ["2", "4", "6"]),
    ("Which number comes next: 6, 12, 18, 24, __?", "30", ["28", "32", "36"]),
    ("Find the next number: 81, 27, 9, 3, __.", "1", ["0", "2", "6"]),
    ("Find the next number: 1, 4, 7, 10, __.", "13", ["12", "14", "15"]),
    ("Find the next number: 5, 15, 45, 135, __.", "405", ["270", "300", "540"]),
    ("Find the next number: 64, 32, 16, 8, __.", "4", ["2", "6", "12"]),
    ("What is the 5th term of 3, 6, 9, 12, ...?", "15", ["12", "18", "21"]),
    ("What is the first term of the sequence 7, 14, 21, 28, ...?", "7", ["14", "21", "28"]),
]

MEDIUM = [
    ("Find the 10th term of 2, 4, 6, 8, ...", "20", ["18", "22", "24"]),
    ("Find the 8th term of 5, 10, 15, 20, ...", "40", ["35", "45", "50"]),
    ("Find the common difference of 12, 17, 22, 27, ...", "5", ["4", "6", "7"]),
    ("Find the common ratio of 3, 9, 27, 81, ...", "3", ["2", "4", "6"]),
    ("Find the 6th term of 4, 8, 12, 16, ...", "24", ["20", "28", "32"]),
    ("Find the 7th term of 2, 6, 10, 14, ...", "26", ["24", "28", "30"]),
    ("Find the 5th term of 3, 6, 12, 24, ...", "48", ["36", "42", "54"]),
    ("Find the 6th term of 1, 4, 9, 16, ...", "36", ["25", "30", "49"]),
    ("Find the 5th term of 1, 8, 27, 64, ...", "125", ["100", "144", "216"]),
    ("Find the 12th term of 5, 10, 15, 20, ...", "60", ["55", "65", "70"]),
    ("Which term of 3, 6, 9, 12, ... is 30?", "10th", ["8th", "9th", "12th"]),
    ("Which term of 5, 10, 15, 20, ... is 50?", "10th", ["8th", "9th", "12th"]),
    ("Find the missing number: 4, 9, 14, __, 24.", "19", ["18", "20", "21"]),
    ("Find the missing number: 2, 6, __, 54, 162.", "18", ["12", "24", "36"]),
    ("Find the missing number: 1, 4, 9, __, 25.", "16", ["12", "18", "20"]),
    ("Find the sum of the first 5 natural numbers.", "15", ["10", "20", "25"]),
    ("Find the sum of the first 5 even numbers.", "30", ["25", "35", "40"]),
    ("Find the sum of the first 5 odd numbers.", "25", ["20", "30", "35"]),
    ("Find the 10th term of an AP with first term 3 and common difference 4.", "39", ["35", "40", "43"]),
    ("Find the 8th term of an AP with first term 7 and common difference 3.", "28", ["25", "30", "31"]),
    ("Find the 6th term of a GP with first term 2 and common ratio 2.", "64", ["32", "48", "128"]),
    ("Find the 5th term of a GP with first term 3 and common ratio 3.", "243", ["81", "162", "729"]),
    ("What is the next number: 2, 5, 10, 17, 26, __?", "37", ["35", "36", "39"]),
    ("What is the next number: 1, 2, 6, 24, __?", "120", ["48", "96", "144"]),
    ("Find the next number: 4, 7, 13, 22, 34, __.", "49", ["46", "48", "52"]),
    ("Find the 15th term of 2, 5, 8, 11, ...", "44", ["41", "45", "47"]),
    ("Find the 20th term of 1, 3, 5, 7, ...", "39", ["37", "40", "41"]),
    ("How many terms are there in 4, 8, 12, ..., 40?", "10", ["8", "9", "12"]),
    ("Find the sum of the first 10 natural numbers.", "55", ["45", "50", "60"]),
    ("Find the sum of the first 10 even numbers.", "110", ["100", "105", "120"]),
]

HARD = [
    ("Find the 20th term of an AP with first term 5 and common difference 3.", "62", ["59", "60", "65"]),
    ("Find the 15th term of an AP with first term 8 and common difference 5.", "78", ["73", "80", "83"]),
    ("Find the 12th term of an AP with first term 4 and common difference 6.", "70", ["64", "68", "76"]),
    ("Find the 10th term of a GP with first term 2 and common ratio 3.", "39366", ["19683", "59049", "6561"]),
    ("Find the 6th term of a GP with first term 5 and common ratio 2.", "160", ["80", "120", "320"]),
    ("Find the sum of the first 10 terms of the AP 2, 4, 6, 8, ...", "110", ["100", "120", "90"]),
    ("Find the sum of the first 10 terms of the AP 3, 6, 9, 12, ...", "165", ["150", "180", "135"]),
    ("Find the sum of the first 10 natural numbers.", "55", ["50", "60", "65"]),
    ("Find the sum of the first 20 natural numbers.", "210", ["200", "220", "190"]),
    ("Find the sum of the first 15 odd numbers.", "225", ["215", "230", "250"]),
    ("Find the sum of the first 12 even numbers.", "156", ["144", "150", "168"]),
    ("Which term of the AP 7, 11, 15, 19, ... is 63?", "15th", ["14th", "16th", "17th"]),
    ("Which term of the AP 5, 8, 11, 14, ... is 50?", "16th", ["15th", "17th", "18th"]),
    ("Which term of the AP 4, 9, 14, 19, ... is 79?", "16th", ["14th", "15th", "17th"]),
    ("An AP has first term 6 and common difference 4. Find its 25th term.", "102", ["98", "100", "106"]),
    ("An AP has first term 10 and common difference 2. Find its 30th term.", "68", ["60", "66", "70"]),
    ("Find the missing term: 3, 8, 13, __, 23, 28.", "18", ["16", "17", "19"]),
    ("Find the missing term: 2, 6, 18, __, 162.", "54", ["36", "48", "72"]),
    ("Find the next number: 1, 4, 10, 20, 35, __.", "56", ["50", "55", "60"]),
    ("Find the next number: 2, 3, 5, 8, 13, 21, __.", "34", ["31", "32", "35"]),
    ("Find the next number: 1, 2, 6, 24, 120, __.", "720", ["600", "500", "840"]),
    ("Find the next number: 3, 8, 15, 24, 35, __.", "48", ["45", "46", "49"]),
    ("Find the sum of the first 20 terms of an AP with first term 2 and common difference 3.", "610", ["600", "620", "630"]),
    ("Find the sum of the first 15 terms of an AP with first term 4 and common difference 2.", "270", ["250", "260", "280"]),
    ("Find the 10th term of the sequence defined by a(n) = 3n + 2.", "32", ["30", "31", "33"]),
    ("Find the 8th term of the sequence defined by a(n) = n^2 + 1.", "65", ["64", "63", "72"]),
    ("Find the 12th term of the sequence defined by a(n) = 2n - 1.", "23", ["21", "24", "25"]),
    ("An AP has 5th term 18 and common difference 3. Find its first term.", "6", ["5", "7", "9"]),
    ("An AP has first term 4 and 10th term 31. Find its common difference.", "3", ["2", "4", "5"]),
    ("Find the sum of the first 8 terms of a GP with first term 1 and common ratio 2.", "255", ["127", "256", "128"]),
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
