import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

TOPIC = "Cubes and Cube Roots"
SUBJECT = "Mathematics"

random.seed(42)

EASY = [
    ("What is the cube of 2?", "8", ["4", "6", "12"]),
    ("What is the cube of 3?", "27", ["9", "18", "36"]),
    ("What is the cube of 4?", "64", ["16", "32", "48"]),
    ("What is the cube of 5?", "125", ["25", "100", "150"]),
    ("What is the cube of 6?", "216", ["36", "126", "256"]),
    ("What is the cube of 7?", "343", ["49", "243", "441"]),
    ("What is the cube of 8?", "512", ["64", "256", "5120"]),
    ("What is the cube of 9?", "729", ["81", "243", "629"]),
    ("What is the cube of 10?", "1000", ["100", "500", "10000"]),
    ("What is the cube root of 8?", "2", ["4", "3", "8"]),
    ("What is the cube root of 27?", "3", ["6", "9", "2"]),
    ("What is the cube root of 64?", "4", ["8", "6", "2"]),
    ("What is the cube root of 125?", "5", ["25", "15", "4"]),
    ("What is the cube root of 216?", "6", ["12", "8", "9"]),
    ("What is the cube root of 343?", "7", ["6", "8", "9"]),
    ("What is the cube root of 512?", "8", ["4", "6", "9"]),
    ("What is the cube root of 729?", "9", ["7", "8", "10"]),
    ("What is the cube root of 1000?", "10", ["5", "20", "100"]),
    ("Which of these is a perfect cube?", "64", ["50", "72", "90"]),
    ("Which of these is a perfect cube?", "216", ["200", "220", "250"]),
    ("What is 1 cubed?", "1", ["0", "2", "3"]),
    ("What is the cube of 11?", "1331", ["121", "1111", "1221"]),
    ("What is the cube of 12?", "1728", ["144", "1228", "1828"]),
    ("What is the cube root of 1000000?", "100", ["10", "1000", "10000"]),
    ("What is the cube of 0?", "0", ["1", "3", "9"]),
    ("What is the cube root of 1?", "1", ["0", "2", "3"]),
    ("What is the cube of 15?", "3375", ["225", "337", "3275"]),
    ("What is the cube root of 1331?", "11", ["10", "12", "13"]),
    ("What is the cube of 20?", "8000", ["400", "2000", "6000"]),
    ("What is the cube root of 1728?", "12", ["10", "11", "14"]),
]

MEDIUM = [
    ("Find the cube of 13.", "2197", ["169", "1997", "2297"]),
    ("Find the cube of 14.", "2744", ["196", "2644", "2844"]),
    ("Find the cube of 15.", "3375", ["225", "3275", "3475"]),
    ("Find the cube of 16.", "4096", ["256", "3096", "4196"]),
    ("Find the cube of 17.", "4913", ["289", "4813", "5013"]),
    ("Find the cube of 18.", "5832", ["324", "5732", "5932"]),
    ("Find the cube of 19.", "6859", ["361", "6759", "6959"]),
    ("Find the cube of 21.", "9261", ["441", "9161", "9361"]),
    ("Find the cube root of 2197.", "13", ["11", "12", "14"]),
    ("Find the cube root of 2744.", "14", ["12", "13", "15"]),
    ("Find the cube root of 3375.", "15", ["13", "14", "16"]),
    ("Find the cube root of 4096.", "16", ["14", "15", "17"]),
    ("Find the cube root of 4913.", "17", ["15", "16", "18"]),
    ("Find the cube root of 5832.", "18", ["16", "17", "19"]),
    ("Find the cube root of 6859.", "19", ["17", "18", "20"]),
    ("Find the cube root of 9261.", "21", ["19", "20", "22"]),
    ("Find the cube of 25.", "15625", ["625", "12500", "16625"]),
    ("Find the cube root of 15625.", "25", ["15", "20", "30"]),
    ("Find the cube of 30.", "27000", ["900", "2700", "30000"]),
    ("Find the cube root of 27000.", "30", ["20", "25", "40"]),
    ("What is the value of 4³ + 3³?", "91", ["81", "64", "100"]),
    ("What is the value of 5³ - 4³?", "61", ["51", "71", "81"]),
    ("What is the cube root of 8000?", "20", ["10", "15", "25"]),
    ("What is the cube root of 64000?", "40", ["20", "30", "50"]),
    ("Which of these is a perfect cube?", "1000", ["900", "1100", "1200"]),
    ("Find the cube of 22.", "10648", ["484", "10448", "11648"]),
    ("Find the cube root of 10648.", "22", ["20", "21", "24"]),
    ("What is the cube of 24?", "13824", ["576", "12824", "14824"]),
    ("Find the cube root of 13824.", "24", ["22", "23", "26"]),
    ("What is the cube of 2.5?", "15.625", ["6.25", "12.5", "25"]),
]

HARD = [
    ("Find the smallest number by which 72 must be multiplied to make it a perfect cube.", "3", ["2", "4", "6"]),
    ("Find the smallest number by which 108 must be multiplied to make it a perfect cube.", "2", ["3", "4", "6"]),
    ("Find the smallest number by which 500 must be multiplied to make it a perfect cube.", "2", ["3", "5", "10"]),
    ("Find the smallest number by which 256 must be divided to make it a perfect cube.", "4", ["2", "8", "16"]),
    ("Find the smallest number by which 675 must be multiplied to make it a perfect cube.", "5", ["2", "3", "10"]),
    ("Find the cube root of 0.000125.", "0.05", ["0.5", "0.005", "0.25"]),
    ("Find the cube root of 0.027.", "0.3", ["0.03", "0.9", "0.09"]),
    ("A cube has a volume of 729 cm³. Find its side.", "9 cm", ["8 cm", "7 cm", "10 cm"]),
    ("Find the volume of a cube whose side is 12 cm.", "1728 cm³", ["144 cm³", "1440 cm³", "172 cm³"]),
    ("Find the side of a cube whose volume is 4096 cm³.", "16 cm", ["14 cm", "15 cm", "18 cm"]),
    ("Find the smallest number by which 675 must be divided to make it a perfect cube.", "25", ["5", "15", "45"]),
    ("What is the cube root of 110592?", "48", ["46", "47", "49"]),
    ("Find the cube of 35.", "42875", ["1225", "41875", "43875"]),
    ("What is the value of 15³ + 10³?", "4375", ["3375", "4275", "4475"]),
    ("What is the value of 20³ - 10³?", "7000", ["6000", "8000", "9000"]),
    ("Find the smallest perfect cube divisible by 12 and 18.", "216", ["108", "144", "432"]),
    ("Find the smallest perfect cube divisible by 6, 10 and 15.", "27000", ["900", "3000", "13500"]),
    ("Find the cube root of 250047.", "63", ["61", "62", "64"]),
    ("A cubical tank has a volume of 8000 litres. Find its side in decimetres.", "20 dm", ["10 dm", "15 dm", "25 dm"]),
    ("If the side of a cube is doubled, how many times does its volume increase?", "8 times", ["2 times", "4 times", "6 times"]),
    ("If the side of a cube is tripled, how many times does its volume increase?", "27 times", ["3 times", "9 times", "18 times"]),
    ("Find the cube root of 0.000216.", "0.06", ["0.6", "0.006", "0.12"]),
    ("Find the smallest number by which 6750 must be multiplied to make it a perfect cube.", "4", ["2", "3", "5"]),
    ("Find the cube root of 157464.", "54", ["52", "53", "56"]),
    ("A cube has a volume of 15625 cm³. Find its side.", "25 cm", ["15 cm", "20 cm", "30 cm"]),
    ("Find the cube root of 373248.", "72", ["70", "71", "74"]),
    ("What is the value of 12³ + 8³?", "2240", ["2000", "2140", "2340"]),
    ("Find the smallest number by which 2000 must be divided to make it a perfect cube.", "2", ["4", "5", "10"]),
    ("Find the cube root of 512000.", "80", ["60", "70", "90"]),
    ("A cubical box has a volume of 27000 cm³. Find its side.", "30 cm", ["20 cm", "25 cm", "40 cm"]),
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