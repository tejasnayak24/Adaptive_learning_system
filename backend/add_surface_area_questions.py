
import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"
TOPIC = "Surface Area"
SUBJECT = "Mathematics"

random.seed(42)

EASY = [
    ("What is the formula for the total surface area of a cube?", "6a²", ["4a²", "a²", "12a²"]),
    ("Find the total surface area of a cube with side 2 cm.", "24 cm²", ["8 cm²", "16 cm²", "12 cm²"]),
    ("What is the formula for the lateral surface area of a cube?", "4a²", ["6a²", "2a²", "a²"]),
    ("Find the total surface area of a cube with side 3 cm.", "54 cm²", ["27 cm²", "36 cm²", "18 cm²"]),
    ("What is the formula for the total surface area of a cuboid?", "2(lb + bh + hl)", ["lb + bh + hl", "2(l + b + h)", "l × b × h"]),
    ("Find the total surface area of a cube with side 4 cm.", "96 cm²", ["64 cm²", "48 cm²", "32 cm²"]),
    ("How many square faces does a cube have?", "6", ["4", "8", "12"]),
    ("Find the total surface area of a cube with side 5 cm.", "150 cm²", ["125 cm²", "100 cm²", "75 cm²"]),
    ("What is the shape of each face of a cube?", "Square", ["Rectangle", "Triangle", "Circle"]),
    ("Find the lateral surface area of a cube with side 3 cm.", "36 cm²", ["54 cm²", "27 cm²", "18 cm²"]),
    ("Find the total surface area of a cuboid with length 4 cm, breadth 3 cm and height 2 cm.", "52 cm²", ["24 cm²", "48 cm²", "36 cm²"]),
    ("How many dimensions does a cuboid have?", "3", ["2", "4", "6"]),
    ("Find the total surface area of a cube with side 6 cm.", "216 cm²", ["36 cm²", "144 cm²", "180 cm²"]),
    ("Which unit is suitable for measuring surface area?", "Square metre", ["Metre", "Cubic metre", "Kilogram"]),
    ("Find the total surface area of a cube with side 1 cm.", "6 cm²", ["1 cm²", "4 cm²", "12 cm²"]),
    ("Find the lateral surface area of a cube with side 5 cm.", "100 cm²", ["150 cm²", "125 cm²", "50 cm²"]),
    ("Find the total surface area of a cuboid measuring 5 cm × 4 cm × 3 cm.", "94 cm²", ["60 cm²", "47 cm²", "80 cm²"]),
    ("What is the formula for the curved surface area of a cylinder?", "2πrh", ["πr²", "2πr²", "πrh"]),
    ("What is the formula for the total surface area of a cylinder?", "2πr(r + h)", ["2πrh", "πr²h", "πr(r + h)"]),
    ("Find the curved surface area of a cylinder with radius 7 cm and height 10 cm. Use π = 22/7.", "440 cm²", ["154 cm²", "220 cm²", "880 cm²"]),
    ("Find the area of one square face of a cube with side 8 cm.", "64 cm²", ["32 cm²", "48 cm²", "128 cm²"]),
    ("Find the total surface area of a cuboid with dimensions 6 cm, 4 cm and 2 cm.", "88 cm²", ["48 cm²", "72 cm²", "96 cm²"]),
    ("How many circular faces does a cylinder have?", "2", ["1", "3", "4"]),
    ("Find the total surface area of a cube with side 7 cm.", "294 cm²", ["196 cm²", "343 cm²", "147 cm²"]),
    ("What is the shape of the curved surface of a cylinder when opened flat?", "Rectangle", ["Square", "Triangle", "Circle"]),
    ("Find the lateral surface area of a cuboid with length 5 cm, breadth 3 cm and height 4 cm.", "64 cm²", ["94 cm²", "60 cm²", "40 cm²"]),
    ("Find the total surface area of a cube with side 10 cm.", "600 cm²", ["100 cm²", "400 cm²", "500 cm²"]),
    ("What does TSA stand for in mensuration?", "Total Surface Area", ["Total Solid Area", "Triangle Surface Area", "Total Square Area"]),
    ("Find the total surface area of a cuboid measuring 3 cm × 2 cm × 1 cm.", "22 cm²", ["12 cm²", "18 cm²", "24 cm²"]),
    ("Find the curved surface area of a cylinder with radius 7 cm and height 5 cm. Use π = 22/7.", "220 cm²", ["154 cm²", "110 cm²", "440 cm²"])
]

MEDIUM = [
    ("Find the total surface area of a cube with side 9 cm.", "486 cm²", ["243 cm²", "324 cm²", "729 cm²"]),
    ("Find the total surface area of a cuboid measuring 10 cm × 5 cm × 4 cm.", "220 cm²", ["200 cm²", "180 cm²", "240 cm²"]),
    ("Find the lateral surface area of a cuboid with length 8 cm, breadth 6 cm and height 5 cm.", "140 cm²", ["236 cm²", "120 cm²", "180 cm²"]),
    ("Find the total surface area of a cylinder with radius 7 cm and height 10 cm. Use π = 22/7.", "748 cm²", ["440 cm²", "154 cm²", "594 cm²"]),
    ("Find the total surface area of a cube with side 12 cm.", "864 cm²", ["576 cm²", "144 cm²", "432 cm²"]),
    ("A cuboid has length 12 cm, breadth 8 cm and height 5 cm. Find its total surface area.", "392 cm²", ["300 cm²", "352 cm²", "400 cm²"]),
    ("Find the curved surface area of a cylinder with radius 14 cm and height 8 cm. Use π = 22/7.", "704 cm²", ["616 cm²", "1232 cm²", "352 cm²"]),
    ("Find the total surface area of a cylinder with radius 3 cm and height 7 cm. Use π = 22/7.", "188.57 cm²", ["132 cm²", "66 cm²", "198 cm²"]),
    ("A cube has a side of 11 cm. Find its total surface area.", "726 cm²", ["484 cm²", "121 cm²", "605 cm²"]),
    ("Find the total surface area of a cuboid measuring 15 cm × 10 cm × 6 cm.", "600 cm²", ["450 cm²", "500 cm²", "650 cm²"]),
    ("Find the lateral surface area of a cube with side 8 cm.", "256 cm²", ["384 cm²", "128 cm²", "64 cm²"]),
    ("A cylinder has radius 7 cm and height 14 cm. Find its curved surface area using π = 22/7.", "616 cm²", ["308 cm²", "154 cm²", "924 cm²"]),
    ("Find the total surface area of a cuboid with dimensions 9 cm, 7 cm and 4 cm.", "254 cm²", ["126 cm²", "230 cm²", "280 cm²"]),
    ("Find the total surface area of a cylinder with radius 7 cm and height 7 cm. Use π = 22/7.", "616 cm²", ["308 cm²", "462 cm²", "154 cm²"]),
    ("A cube has a total surface area of 384 cm². Find its side.", "8 cm", ["6 cm", "10 cm", "12 cm"]),
    ("A cuboid has length 10 cm, breadth 6 cm and height 3 cm. Find its total surface area.", "216 cm²", ["180 cm²", "190 cm²", "200 cm²"]),
    ("Find the curved surface area of a cylinder with radius 3.5 cm and height 10 cm. Use π = 22/7.", "220 cm²", ["110 cm²", "154 cm²", "440 cm²"]),
    ("Find the total surface area of a cube with side 15 cm.", "1350 cm²", ["900 cm²", "1125 cm²", "1500 cm²"]),
    ("Find the total surface area of a cuboid measuring 8 cm × 5 cm × 3 cm.", "158 cm²", ["120 cm²", "148 cm²", "180 cm²"]),
    ("A cylinder has radius 14 cm and height 5 cm. Find its total surface area using π = 22/7.", "1672 cm²", ["440 cm²", "616 cm²", "1232 cm²"]),
    ("Find the lateral surface area of a cuboid with length 12 cm, breadth 5 cm and height 7 cm.", "238 cm²", ["358 cm²", "120 cm²", "200 cm²"]),
    ("Find the total surface area of a cube with side 13 cm.", "1014 cm²", ["676 cm²", "845 cm²", "169 cm²"]),
    ("A cuboid has dimensions 20 cm × 10 cm × 5 cm. Find its total surface area.", "700 cm²", ["500 cm²", "600 cm²", "750 cm²"]),
    ("Find the curved surface area of a cylinder with radius 7 cm and height 20 cm. Use π = 22/7.", "880 cm²", ["440 cm²", "154 cm²", "968 cm²"]),
    ("A cube has a total surface area of 600 cm². Find its side.", "10 cm", ["12 cm", "8 cm", "15 cm"]),
    ("Find the total surface area of a cuboid measuring 7 cm × 6 cm × 5 cm.", "214 cm²", ["210 cm²", "180 cm²", "240 cm²"]),
    ("Find the total surface area of a cylinder with radius 3.5 cm and height 7 cm. Use π = 22/7.", "231 cm²", ["154 cm²", "220 cm²", "308 cm²"]),
    ("Find the lateral surface area of a cube with side 14 cm.", "784 cm²", ["1176 cm²", "196 cm²", "392 cm²"]),
    ("A cuboid has dimensions 11 cm, 8 cm and 6 cm. Find its total surface area.", "388 cm²", ["300 cm²", "350 cm²", "420 cm²"]),
    ("Find the total surface area of a cylinder with radius 7 cm and height 3 cm. Use π = 22/7.", "440 cm²", ["132 cm²", "308 cm²", "220 cm²"])
]

HARD = [
    ("A cube has a total surface area of 1350 cm². Find its side.", "15 cm", ["10 cm", "20 cm", "25 cm"]),
    ("A cuboid measures 15 cm × 12 cm × 10 cm. Find its total surface area.", "900 cm²", ["600 cm²", "750 cm²", "850 cm²"]),
    ("A cylinder has radius 14 cm and height 20 cm. Find its total surface area using π = 22/7.", "2992 cm²", ["1760 cm²", "1232 cm²", "3520 cm²"]),
    ("The side of a cube is doubled. By what factor does its total surface area increase?", "4 times", ["2 times", "6 times", "8 times"]),
    ("A cuboid has length 20 cm, breadth 12 cm and height 8 cm. Find its lateral surface area.", "512 cm²", ["832 cm²", "480 cm²", "600 cm²"]),
    ("A cylinder has radius 7 cm and height 15 cm. Find its total surface area using π = 22/7.", "968 cm²", ["660 cm²", "880 cm²", "154 cm²"]),
    ("The total surface area of a cube is 864 cm². Find its side.", "12 cm", ["10 cm", "14 cm", "16 cm"]),
    ("A cuboid has dimensions 18 cm × 12 cm × 9 cm. Find its total surface area.", "972 cm²", ["648 cm²", "900 cm²", "1000 cm²"]),
    ("Find the curved surface area of a cylinder with diameter 28 cm and height 12 cm. Use π = 22/7.", "1056 cm²", ["528 cm²", "1232 cm²", "616 cm²"]),
    ("A cube has side 20 cm. Find its total surface area.", "2400 cm²", ["1200 cm²", "1600 cm²", "800 cm²"]),
    ("A cylindrical tank has radius 3.5 m and height 10 m. Find its curved surface area using π = 22/7.", "220 m²", ["154 m²", "440 m²", "110 m²"]),
    ("A cuboid has length 25 cm, breadth 15 cm and height 10 cm. Find its total surface area.", "1550 cm²", ["1250 cm²", "1500 cm²", "1750 cm²"]),
    ("The total surface area of a cube is 294 cm². Find its side.", "7 cm", ["14 cm", "6 cm", "9 cm"]),
    ("Find the total surface area of a cylinder with diameter 14 cm and height 10 cm. Use π = 22/7.", "748 cm²", ["440 cm²", "308 cm²", "616 cm²"]),
    ("A cuboid has dimensions 30 cm × 20 cm × 10 cm. Find its lateral surface area.", "1000 cm²", ["2200 cm²", "600 cm²", "1200 cm²"]),
    ("If the side of a cube is tripled, its total surface area becomes how many times the original?", "9 times", ["3 times", "6 times", "27 times"]),
    ("A cylinder has radius 14 cm and height 7 cm. Find its total surface area using π = 22/7.", "1848 cm²", ["616 cm²", "1232 cm²", "1540 cm²"]),
    ("A cuboid has length 16 cm, breadth 12 cm and height 10 cm. Find its total surface area.", "944 cm²", ["600 cm²", "800 cm²", "900 cm²"]),
    ("A cube has a total surface area of 1176 cm². Find its side.", "14 cm", ["12 cm", "16 cm", "18 cm"]),
    ("Find the curved surface area of a cylinder with radius 10 cm and height 21 cm. Use π = 22/7.", "1320 cm²", ["660 cm²", "1540 cm²", "440 cm²"]),
    ("A cuboid measures 24 cm × 15 cm × 8 cm. Find its total surface area.", "1344 cm²", ["1000 cm²", "1200 cm²", "1440 cm²"]),
    ("A cylinder has radius 7 cm and height 21 cm. Find its total surface area using π = 22/7.", "1232 cm²", ["924 cm²", "616 cm²", "1540 cm²"]),
    ("The side of a cube increases from 5 cm to 10 cm. Find the increase in total surface area.", "450 cm²", ["300 cm²", "150 cm²", "600 cm²"]),
    ("A cuboid has dimensions 14 cm × 10 cm × 6 cm. Find its lateral surface area.", "288 cm²", ["448 cm²", "240 cm²", "300 cm²"]),
    ("Find the total surface area of a cylinder with radius 10.5 cm and height 14 cm. Use π = 22/7.", "1617 cm²", ["924 cm²", "1386 cm²", "1848 cm²"]),
    ("A cube has a total surface area of 294 cm². What is the area of one face?", "49 cm²", ["98 cm²", "42 cm²", "36 cm²"]),
    ("A cuboid has length 25 cm, breadth 20 cm and height 15 cm. Find its total surface area.", "2350 cm²", ["1500 cm²", "2000 cm²", "2500 cm²"]),
    ("Find the curved surface area of a cylinder with diameter 14 cm and height 25 cm. Use π = 22/7.", "1100 cm²", ["550 cm²", "1540 cm²", "770 cm²"]),
    ("A cube has side 18 cm. Find its lateral surface area.", "1296 cm²", ["1944 cm²", "324 cm²", "648 cm²"]),
    ("A cylinder has radius 21 cm and height 10 cm. Find its total surface area using π = 22/7.", "4092 cm²", ["1320 cm²", "2772 cm²", "3696 cm²"])
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

        if len(data) != 30:
            raise ValueError(
                f"{difficulty} must contain exactly 30 questions. Found {len(data)}"
            )

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
