import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

TOPIC = "Squares and Square Roots"
SUBJECT = "Mathematics"

random.seed(42)

EASY = [
    ("What is the square of 5?", "25", ["10", "15", "20"]),
    ("What is the square of 8?", "64", ["16", "32", "48"]),
    ("What is the square of 10?", "100", ["20", "50", "90"]),
    ("What is the square of 12?", "144", ["124", "124", "164"]),
    ("What is the square root of 25?", "5", ["4", "6", "10"]),
    ("What is the square root of 49?", "7", ["6", "8", "9"]),
    ("What is the square root of 81?", "9", ["7", "8", "10"]),
    ("What is the square root of 100?", "10", ["5", "20", "15"]),
    ("What is the square of 6?", "36", ["12", "18", "30"]),
    ("What is the square of 9?", "81", ["18", "27", "72"]),
    ("What is the square root of 64?", "8", ["6", "7", "9"]),
    ("What is the square root of 121?", "11", ["10", "12", "13"]),
    ("What is the square of 4?", "16", ["8", "12", "20"]),
    ("What is the square of 7?", "49", ["14", "21", "42"]),
    ("What is the square root of 36?", "6", ["4", "5", "7"]),
    ("What is the square root of 144?", "12", ["10", "11", "14"]),
    ("What is the square of 3?", "9", ["6", "12", "18"]),
    ("What is the square of 11?", "121", ["111", "101", "131"]),
    ("What is the square root of 169?", "13", ["11", "12", "14"]),
    ("What is the square of 15?", "225", ["125", "215", "250"]),
    ("Which of these is a perfect square?", "64", ["50", "70", "90"]),
    ("Which number has a square root of 4?", "16", ["8", "12", "20"]),
    ("What is the square of 2?", "4", ["2", "6", "8"]),
    ("What is the square root of 196?", "14", ["12", "13", "15"]),
    ("What is the square of 13?", "169", ["139", "159", "179"]),
    ("What is the square root of 225?", "15", ["13", "14", "16"]),
    ("What is the square of 20?", "400", ["200", "300", "500"]),
    ("What is the square root of 400?", "20", ["10", "15", "25"]),
    ("What is the square of 14?", "196", ["186", "194", "204"]),
    ("What is the square root of 289?", "17", ["15", "16", "18"]),
]

MEDIUM = [
    ("Find the square of 18.", "324", ["314", "334", "344"]),
    ("Find the square of 25.", "625", ["525", "600", "650"]),
    ("Find the square root of 256.", "16", ["14", "15", "18"]),
    ("Find the square root of 324.", "18", ["16", "17", "20"]),
    ("Find the square of 16.", "256", ["246", "266", "276"]),
    ("Find the square root of 625.", "25", ["20", "24", "30"]),
    ("Find the square of 19.", "361", ["341", "351", "371"]),
    ("Find the square root of 441.", "21", ["19", "20", "22"]),
    ("Find the square of 22.", "484", ["464", "474", "494"]),
    ("Find the square root of 529.", "23", ["21", "22", "24"]),
    ("Find the square of 24.", "576", ["566", "586", "596"]),
    ("Find the square root of 729.", "27", ["25", "26", "28"]),
    ("Find the square of 30.", "900", ["600", "800", "1000"]),
    ("Find the square root of 900.", "30", ["20", "25", "35"]),
    ("Find the square of 17.", "289", ["279", "299", "309"]),
    ("Find the square root of 784.", "28", ["26", "27", "29"]),
    ("Find the square of 26.", "676", ["656", "666", "686"]),
    ("Find the square root of 1024.", "32", ["30", "31", "34"]),
    ("Find the square of 35.", "1225", ["1125", "1205", "1325"]),
    ("Find the square root of 1156.", "34", ["32", "33", "36"]),
    ("Find the square of 32.", "1024", ["924", "1004", "1044"]),
    ("Find the square root of 1600.", "40", ["30", "35", "45"]),
    ("What is the value of 15² + 10²?", "325", ["300", "350", "375"]),
    ("What is the value of 20² - 12²?", "256", ["144", "200", "288"]),
    ("What is the square root of 2025?", "45", ["40", "42", "50"]),
    ("What is the square of 28?", "784", ["764", "774", "794"]),
    ("Which is the smallest perfect square greater than 100?", "121", ["110", "120", "144"]),
    ("How many natural numbers are between 5² and 6²?", "10", ["9", "11", "12"]),
    ("What is the square root of 1764?", "42", ["40", "41", "44"]),
    ("Find the value of 12² + 8².", "208", ["200", "216", "224"]),
]

HARD = [
    ("Find the smallest number by which 72 must be multiplied to make it a perfect square.", "2", ["3", "6", "8"]),
    ("Find the smallest number by which 180 must be multiplied to make it a perfect square.", "5", ["2", "3", "10"]),
    ("Find the smallest number by which 48 must be divided to make it a perfect square.", "3", ["2", "4", "6"]),
    ("Find the smallest number by which 98 must be multiplied to make it a perfect square.", "2", ["3", "7", "14"]),
    ("Find the square root of 0.0009.", "0.03", ["0.3", "0.003", "0.09"]),
    ("Find the square root of 2.25.", "1.5", ["1.25", "2.5", "0.15"]),
    ("A square has an area of 625 cm². Find its side.", "25 cm", ["20 cm", "30 cm", "35 cm"]),
    ("Find the perimeter of a square whose area is 256 cm².", "64 cm", ["32 cm", "48 cm", "80 cm"]),
    ("What is the smallest number that must be added to 80 to make it a perfect square?", "1", ["2", "4", "9"]),
    ("What is the smallest number that must be subtracted from 90 to make it a perfect square?", "9", ["5", "10", "16"]),
    ("Find the square root of 4096.", "64", ["62", "63", "66"]),
    ("Find the square of 45.", "2025", ["2005", "2015", "2045"]),
    ("What is the value of 25² - 15²?", "400", ["350", "450", "500"]),
    ("Find the square root of 0.0081.", "0.09", ["0.9", "0.009", "0.81"]),
    ("A square garden has an area of 900 m². Find its perimeter.", "120 m", ["90 m", "100 m", "150 m"]),
    ("Find the smallest number by which 200 must be divided to make it a perfect square.", "2", ["4", "5", "10"]),
    ("Find the square root of 3136.", "56", ["54", "55", "58"]),
    ("What is the value of 35² + 15²?", "1450", ["1250", "1350", "1550"]),
    ("Find the smallest perfect square divisible by 6, 8 and 12.", "144", ["72", "96", "288"]),
    ("How many numbers are there between 10² and 11²?", "20", ["19", "21", "22"]),
    ("The area of a square is 1225 cm². Find its diagonal approximately.", "49.5 cm", ["35 cm", "45 cm", "50 cm"]),
    ("Find the square root of 5625.", "75", ["65", "70", "80"]),
    ("What is the smallest number that must be added to 150 to make it a perfect square?", "19", ["14", "20", "25"]),
    ("What is the smallest number that must be subtracted from 200 to make it a perfect square?", "4", ["5", "9", "16"]),
    ("Find the square root of 0.0625.", "0.25", ["0.5", "0.025", "0.75"]),
    ("A square has a perimeter of 80 cm. Find its area.", "400 cm²", ["200 cm²", "300 cm²", "500 cm²"]),
    ("Find the smallest number by which 150 must be multiplied to make it a perfect square.", "6", ["2", "3", "5"]),
    ("Find the square root of 7744.", "88", ["86", "87", "89"]),
    ("What is the value of 48² - 32²?", "1280", ["1200", "1240", "1320"]),
    ("Find the smallest perfect square divisible by 15 and 20.", "900", ["300", "600", "1200"]),
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