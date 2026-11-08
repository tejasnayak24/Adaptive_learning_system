
import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"
TOPIC = "Area of Plane Figures"
SUBJECT = "Mathematics"

random.seed(42)

EASY = [
    ("Find the area of a square with side 5 cm.", "25 cm²", ["20 cm²", "10 cm²", "30 cm²"]),
    ("Find the area of a rectangle with length 8 cm and breadth 4 cm.", "32 cm²", ["24 cm²", "12 cm²", "36 cm²"]),
    ("What is the formula for the area of a square?", "Side × Side", ["4 × Side", "2 × Side", "Length × Breadth"]),
    ("Find the area of a rectangle with length 10 cm and breadth 3 cm.", "30 cm²", ["13 cm²", "26 cm²", "20 cm²"]),
    ("Find the area of a square with side 7 cm.", "49 cm²", ["28 cm²", "14 cm²", "42 cm²"]),
    ("What is the formula for the area of a rectangle?", "Length × Breadth", ["2 × (Length + Breadth)", "Length + Breadth", "Length × Length"]),
    ("Find the area of a triangle with base 6 cm and height 4 cm.", "12 cm²", ["24 cm²", "10 cm²", "18 cm²"]),
    ("Find the area of a rectangle with length 5 cm and breadth 2 cm.", "10 cm²", ["7 cm²", "14 cm²", "20 cm²"]),
    ("Find the area of a square with side 9 cm.", "81 cm²", ["36 cm²", "18 cm²", "72 cm²"]),
    ("What is the unit commonly used to measure area?", "Square centimetre", ["Centimetre", "Kilogram", "Litre"]),
    ("Find the area of a triangle with base 10 cm and height 6 cm.", "30 cm²", ["60 cm²", "16 cm²", "40 cm²"]),
    ("Find the area of a rectangle with length 12 cm and breadth 5 cm.", "60 cm²", ["34 cm²", "50 cm²", "17 cm²"]),
    ("Find the area of a square with side 4 cm.", "16 cm²", ["8 cm²", "12 cm²", "20 cm²"]),
    ("What is half the product of a triangle's base and height called?", "Area of a triangle", ["Perimeter of a triangle", "Area of a square", "Circumference"]),
    ("Find the area of a rectangle with length 7 cm and breadth 3 cm.", "21 cm²", ["10 cm²", "14 cm²", "28 cm²"]),
    ("Find the area of a square with side 6 cm.", "36 cm²", ["24 cm²", "12 cm²", "30 cm²"]),
    ("Find the area of a triangle with base 8 cm and height 5 cm.", "20 cm²", ["40 cm²", "13 cm²", "25 cm²"]),
    ("A rectangle has length 9 cm and breadth 2 cm. Find its area.", "18 cm²", ["11 cm²", "22 cm²", "36 cm²"]),
    ("Find the area of a square with side 3 cm.", "9 cm²", ["6 cm²", "12 cm²", "18 cm²"]),
    ("Which shape has area equal to side multiplied by side?", "Square", ["Triangle", "Circle", "Rectangle"]),
    ("Find the area of a rectangle with length 6 cm and breadth 5 cm.", "30 cm²", ["11 cm²", "22 cm²", "60 cm²"]),
    ("Find the area of a triangle with base 12 cm and height 3 cm.", "18 cm²", ["36 cm²", "15 cm²", "24 cm²"]),
    ("Find the area of a square with side 8 cm.", "64 cm²", ["32 cm²", "16 cm²", "48 cm²"]),
    ("What is the area of a rectangle measuring 4 cm by 4 cm?", "16 cm²", ["8 cm²", "12 cm²", "20 cm²"]),
    ("Find the area of a triangle with base 4 cm and height 7 cm.", "14 cm²", ["28 cm²", "11 cm²", "21 cm²"]),
    ("Find the area of a rectangle with length 15 cm and breadth 2 cm.", "30 cm²", ["17 cm²", "34 cm²", "45 cm²"]),
    ("Find the area of a square with side 10 cm.", "100 cm²", ["40 cm²", "20 cm²", "50 cm²"]),
    ("A rectangle has length 11 cm and breadth 4 cm. Find its area.", "44 cm²", ["30 cm²", "15 cm²", "40 cm²"]),
    ("Find the area of a triangle with base 14 cm and height 2 cm.", "14 cm²", ["28 cm²", "16 cm²", "12 cm²"]),
    ("Which measurement describes the space covered by a flat shape?", "Area", ["Perimeter", "Volume", "Length"])
]

MEDIUM = [
    ("Find the area of a parallelogram with base 12 cm and height 5 cm.", "60 cm²", ["34 cm²", "30 cm²", "120 cm²"]),
    ("Find the area of a trapezium with parallel sides 8 cm and 12 cm and height 5 cm.", "50 cm²", ["100 cm²", "40 cm²", "60 cm²"]),
    ("A square has an area of 144 cm². Find its side.", "12 cm", ["14 cm", "16 cm", "10 cm"]),
    ("A rectangle has an area of 96 cm² and length 12 cm. Find its breadth.", "8 cm", ["6 cm", "10 cm", "12 cm"]),
    ("Find the area of a triangle with base 15 cm and height 8 cm.", "60 cm²", ["120 cm²", "46 cm²", "30 cm²"]),
    ("Find the area of a rhombus with diagonals 10 cm and 8 cm.", "40 cm²", ["80 cm²", "18 cm²", "36 cm²"]),
    ("A parallelogram has base 9 cm and height 7 cm. Find its area.", "63 cm²", ["32 cm²", "56 cm²", "126 cm²"]),
    ("Find the area of a trapezium with parallel sides 6 cm and 10 cm and height 4 cm.", "32 cm²", ["64 cm²", "24 cm²", "40 cm²"]),
    ("A rectangle measures 14 cm by 9 cm. Find its area.", "126 cm²", ["46 cm²", "92 cm²", "112 cm²"]),
    ("A square has an area of 196 cm². Find its side.", "14 cm", ["12 cm", "16 cm", "18 cm"]),
    ("Find the area of a triangle with base 18 cm and height 10 cm.", "90 cm²", ["180 cm²", "28 cm²", "80 cm²"]),
    ("Find the area of a rhombus with diagonals 12 cm and 6 cm.", "36 cm²", ["72 cm²", "18 cm²", "48 cm²"]),
    ("A rectangle has an area of 150 cm² and breadth 10 cm. Find its length.", "15 cm", ["12 cm", "20 cm", "25 cm"]),
    ("Find the area of a parallelogram with base 15 cm and height 8 cm.", "120 cm²", ["60 cm²", "46 cm²", "100 cm²"]),
    ("A trapezium has parallel sides 10 cm and 14 cm and height 6 cm. Find its area.", "72 cm²", ["144 cm²", "60 cm²", "84 cm²"]),
    ("Find the area of a square with diagonal 10 cm.", "50 cm²", ["100 cm²", "25 cm²", "40 cm²"]),
    ("A triangle has area 48 cm² and base 12 cm. Find its height.", "8 cm", ["4 cm", "6 cm", "10 cm"]),
    ("Find the area of a rectangle with length 16 cm and breadth 7 cm.", "112 cm²", ["46 cm²", "96 cm²", "120 cm²"]),
    ("A rhombus has diagonals 16 cm and 10 cm. Find its area.", "80 cm²", ["160 cm²", "60 cm²", "26 cm²"]),
    ("A parallelogram has area 84 cm² and base 12 cm. Find its height.", "7 cm", ["6 cm", "8 cm", "9 cm"]),
    ("Find the area of a triangle with base 20 cm and height 9 cm.", "90 cm²", ["180 cm²", "29 cm²", "100 cm²"]),
    ("A rectangle has length 18 cm and area 216 cm². Find its breadth.", "12 cm", ["10 cm", "14 cm", "16 cm"]),
    ("Find the area of a trapezium with parallel sides 15 cm and 9 cm and height 4 cm.", "48 cm²", ["96 cm²", "36 cm²", "60 cm²"]),
    ("A square has a side of 13 cm. Find its area.", "169 cm²", ["52 cm²", "156 cm²", "144 cm²"]),
    ("Find the area of a parallelogram with base 18 cm and height 6 cm.", "108 cm²", ["48 cm²", "96 cm²", "120 cm²"]),
    ("A triangle has area 75 cm² and height 10 cm. Find its base.", "15 cm", ["10 cm", "12 cm", "20 cm"]),
    ("Find the area of a rectangle measuring 25 cm by 8 cm.", "200 cm²", ["100 cm²", "66 cm²", "225 cm²"]),
    ("A rhombus has diagonals 14 cm and 12 cm. Find its area.", "84 cm²", ["168 cm²", "72 cm²", "26 cm²"]),
    ("Find the area of a triangle with base 16 cm and height 12 cm.", "96 cm²", ["192 cm²", "48 cm²", "112 cm²"]),
    ("A parallelogram has area 150 cm² and height 10 cm. Find its base.", "15 cm", ["10 cm", "20 cm", "25 cm"])
]

HARD = [
    ("A rectangular garden is 25 m long and 18 m wide. Find its area.", "450 m²", ["350 m²", "430 m²", "500 m²"]),
    ("A square park has an area of 625 m². Find the length of one side.", "25 m", ["20 m", "30 m", "35 m"]),
    ("A triangle has a base of 24 cm and an area of 180 cm². Find its height.", "15 cm", ["12 cm", "18 cm", "20 cm"]),
    ("A trapezium has parallel sides 18 cm and 26 cm with height 12 cm. Find its area.", "264 cm²", ["528 cm²", "240 cm²", "300 cm²"]),
    ("A rhombus has an area of 120 cm² and one diagonal is 15 cm. Find the other diagonal.", "16 cm", ["8 cm", "12 cm", "20 cm"]),
    ("A rectangular field is 40 m long and 25 m wide. Find its area.", "1000 m²", ["800 m²", "900 m²", "1200 m²"]),
    ("A square has an area of 324 cm². Find its perimeter.", "72 cm", ["36 cm", "64 cm", "81 cm"]),
    ("A parallelogram has an area of 216 cm² and base 18 cm. Find its height.", "12 cm", ["10 cm", "14 cm", "16 cm"]),
    ("A rectangular floor is 12 m long and 8 m wide. Find the area to be tiled.", "96 m²", ["40 m²", "80 m²", "120 m²"]),
    ("A triangle has an area of 144 cm² and height 16 cm. Find its base.", "18 cm", ["9 cm", "16 cm", "24 cm"]),
    ("A trapezium has parallel sides 20 cm and 30 cm and height 14 cm. Find its area.", "350 cm²", ["700 cm²", "300 cm²", "400 cm²"]),
    ("A square plot has a side of 35 m. Find its area.", "1225 m²", ["140 m²", "1200 m²", "1250 m²"]),
    ("A rectangle has an area of 540 cm² and length 30 cm. Find its breadth.", "18 cm", ["15 cm", "20 cm", "25 cm"]),
    ("A rhombus has diagonals 18 cm and 14 cm. Find its area.", "126 cm²", ["252 cm²", "112 cm²", "144 cm²"]),
    ("A parallelogram has base 24 cm and area 360 cm². Find its height.", "15 cm", ["12 cm", "18 cm", "20 cm"]),
    ("A triangular field has base 50 m and height 32 m. Find its area.", "800 m²", ["1600 m²", "400 m²", "750 m²"]),
    ("A rectangle has length 28 cm and breadth 15 cm. Find its area.", "420 cm²", ["86 cm²", "400 cm²", "450 cm²"]),
    ("A square has an area of 784 cm². Find its side.", "28 cm", ["24 cm", "32 cm", "36 cm"]),
    ("A trapezium has parallel sides 16 cm and 24 cm and height 9 cm. Find its area.", "180 cm²", ["360 cm²", "160 cm²", "200 cm²"]),
    ("A triangle has base 35 cm and height 18 cm. Find its area.", "315 cm²", ["630 cm²", "280 cm²", "350 cm²"]),
    ("A rectangular garden is 45 m long and 30 m wide. Find its area.", "1350 m²", ["1200 m²", "1500 m²", "135 m²"]),
    ("A rhombus has an area of 192 cm² and one diagonal is 24 cm. Find the other diagonal.", "16 cm", ["12 cm", "18 cm", "20 cm"]),
    ("A parallelogram has base 32 cm and height 15 cm. Find its area.", "480 cm²", ["240 cm²", "450 cm²", "500 cm²"]),
    ("A rectangle has area 720 cm² and breadth 24 cm. Find its length.", "30 cm", ["24 cm", "36 cm", "40 cm"]),
    ("A trapezium has parallel sides 25 cm and 35 cm and height 16 cm. Find its area.", "480 cm²", ["960 cm²", "400 cm²", "500 cm²"]),
    ("A triangular board has an area of 210 cm² and base 28 cm. Find its height.", "15 cm", ["12 cm", "18 cm", "20 cm"]),
    ("A square has a diagonal of 14 cm. Find its area.", "98 cm²", ["196 cm²", "49 cm²", "56 cm²"]),
    ("A parallelogram has area 525 cm² and height 21 cm. Find its base.", "25 cm", ["20 cm", "30 cm", "35 cm"]),
    ("A rectangle is 36 m long and 22 m wide. Find its area.", "792 m²", ["792 cm²", "768 m²", "812 m²"]),
    ("A trapezium has parallel sides 32 cm and 18 cm and height 20 cm. Find its area.", "500 cm²", ["1000 cm²", "450 cm²", "520 cm²"])
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
