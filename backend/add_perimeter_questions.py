
import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"
TOPIC = "Perimeter"
SUBJECT = "Mathematics"

random.seed(42)

EASY = [
    ("What is the perimeter of a shape?", "Total length of its boundary", ["Area inside it", "Number of corners", "Sum of its angles"]),
    ("What is the perimeter of a square with side 5 cm?", "20 cm", ["10 cm", "15 cm", "25 cm"]),
    ("What is the perimeter of a rectangle with length 8 cm and breadth 4 cm?", "24 cm", ["12 cm", "32 cm", "16 cm"]),
    ("Find the perimeter of an equilateral triangle with side 6 cm.", "18 cm", ["12 cm", "24 cm", "36 cm"]),
    ("Find the perimeter of a square with side 7 cm.", "28 cm", ["14 cm", "21 cm", "49 cm"]),
    ("What is the perimeter of a rectangle with length 10 cm and breadth 5 cm?", "30 cm", ["15 cm", "50 cm", "25 cm"]),
    ("Find the perimeter of a triangle with sides 3 cm, 4 cm and 5 cm.", "12 cm", ["10 cm", "15 cm", "20 cm"]),
    ("What is the perimeter of a square with side 9 cm?", "36 cm", ["18 cm", "27 cm", "81 cm"]),
    ("Find the perimeter of a rectangle with length 12 cm and breadth 6 cm.", "36 cm", ["18 cm", "72 cm", "24 cm"]),
    ("What is the unit commonly used to measure perimeter?", "cm", ["cm²", "cm³", "kg"]),
    ("A regular pentagon has sides of 4 cm each. Find its perimeter.", "20 cm", ["16 cm", "24 cm", "12 cm"]),
    ("Find the perimeter of a regular hexagon with side 3 cm.", "18 cm", ["12 cm", "15 cm", "21 cm"]),
    ("A square has a side of 11 cm. Find its perimeter.", "44 cm", ["22 cm", "33 cm", "121 cm"]),
    ("Find the perimeter of a rectangle measuring 15 cm by 5 cm.", "40 cm", ["20 cm", "75 cm", "30 cm"]),
    ("A triangle has sides 7 cm, 8 cm and 9 cm. Find its perimeter.", "24 cm", ["21 cm", "25 cm", "27 cm"]),
    ("Find the perimeter of a square with side 12 m.", "48 m", ["24 m", "36 m", "144 m"]),
    ("A rectangle has length 9 m and breadth 3 m. Find its perimeter.", "24 m", ["12 m", "27 m", "18 m"]),
    ("Find the perimeter of an equilateral triangle with side 10 cm.", "30 cm", ["20 cm", "40 cm", "100 cm"]),
    ("A regular octagon has side 2 cm. Find its perimeter.", "16 cm", ["12 cm", "14 cm", "18 cm"]),
    ("Find the perimeter of a rectangle with length 7 cm and breadth 2 cm.", "18 cm", ["9 cm", "14 cm", "20 cm"]),
    ("A square has a perimeter of 32 cm. Find its side.", "8 cm", ["4 cm", "16 cm", "12 cm"]),
    ("A rectangle has a perimeter of 20 cm. Its length is 6 cm. Find its breadth.", "4 cm", ["5 cm", "6 cm", "8 cm"]),
    ("Find the perimeter of a triangle with sides 5 cm, 5 cm and 8 cm.", "18 cm", ["15 cm", "20 cm", "16 cm"]),
    ("A regular hexagon has a side of 6 m. Find its perimeter.", "36 m", ["30 m", "24 m", "42 m"]),
    ("Find the perimeter of a square with side 2.5 cm.", "10 cm", ["5 cm", "7.5 cm", "12.5 cm"]),
    ("A rectangle measures 20 m by 10 m. Find its perimeter.", "60 m", ["30 m", "200 m", "40 m"]),
    ("Find the perimeter of a triangle with sides 10 cm, 12 cm and 8 cm.", "30 cm", ["20 cm", "28 cm", "32 cm"]),
    ("A square has a side of 15 cm. Find its perimeter.", "60 cm", ["30 cm", "45 cm", "225 cm"]),
    ("Find the perimeter of a regular pentagon with side 8 cm.", "40 cm", ["32 cm", "48 cm", "24 cm"]),
    ("A rectangle has length 14 cm and breadth 7 cm. Find its perimeter.", "42 cm", ["21 cm", "98 cm", "35 cm"]),
]

MEDIUM = [
    ("The perimeter of a square is 64 cm. Find its side.", "16 cm", ["12 cm", "8 cm", "24 cm"]),
    ("The perimeter of a rectangle is 50 cm and its length is 15 cm. Find its breadth.", "10 cm", ["5 cm", "15 cm", "20 cm"]),
    ("A rectangular garden is 25 m long and 15 m wide. Find its perimeter.", "80 m", ["40 m", "375 m", "70 m"]),
    ("The perimeter of an equilateral triangle is 45 cm. Find each side.", "15 cm", ["10 cm", "20 cm", "12 cm"]),
    ("A square has a perimeter of 100 cm. Find its side.", "25 cm", ["20 cm", "50 cm", "10 cm"]),
    ("A rectangle has length 18 cm and perimeter 60 cm. Find its breadth.", "12 cm", ["10 cm", "15 cm", "18 cm"]),
    ("The perimeter of a regular hexagon is 72 cm. Find each side.", "12 cm", ["10 cm", "14 cm", "18 cm"]),
    ("A rectangular field has length 40 m and breadth 20 m. Find the cost of fencing at ₹5 per metre.", "₹600", ["₹300", "₹400", "₹800"]),
    ("A square has a side of 12.5 cm. Find its perimeter.", "50 cm", ["25 cm", "37.5 cm", "62.5 cm"]),
    ("The perimeter of a rectangle is 72 cm. Its breadth is 12 cm. Find its length.", "24 cm", ["18 cm", "30 cm", "36 cm"]),
    ("A triangle has perimeter 50 cm. Two sides are 15 cm and 20 cm. Find the third side.", "15 cm", ["10 cm", "20 cm", "25 cm"]),
    ("A square has a perimeter of 84 m. Find its side.", "21 m", ["14 m", "28 m", "42 m"]),
    ("A rectangle has length 3 times its breadth. If breadth is 5 cm, find its perimeter.", "40 cm", ["20 cm", "30 cm", "45 cm"]),
    ("Find the perimeter of a regular octagon with side 7 cm.", "56 cm", ["49 cm", "63 cm", "42 cm"]),
    ("A rectangular park is 60 m long and 40 m wide. Find the fencing cost at ₹12 per metre.", "₹2,400", ["₹1,200", "₹2,000", "₹3,000"]),
    ("A square has a perimeter of 120 cm. Find its area.", "900 cm²", ["600 cm²", "1200 cm²", "400 cm²"]),
    ("A rectangle has perimeter 100 cm and breadth 20 cm. Find its length.", "30 cm", ["20 cm", "40 cm", "50 cm"]),
    ("The perimeter of a regular pentagon is 75 cm. Find its side length.", "15 cm", ["10 cm", "20 cm", "25 cm"]),
    ("A rectangular field is 35 m long and 25 m wide. Find the distance covered in 3 rounds around it.", "360 m", ["180 m", "240 m", "420 m"]),
    ("The side of a square increases from 8 cm to 12 cm. Find the increase in perimeter.", "16 cm", ["4 cm", "12 cm", "32 cm"]),
    ("A rectangle has length 22 cm and breadth 8 cm. Find its perimeter.", "60 cm", ["30 cm", "176 cm", "44 cm"]),
    ("A wire of length 48 cm is bent into a square. Find its side.", "12 cm", ["8 cm", "16 cm", "24 cm"]),
    ("A wire of length 60 cm is bent into an equilateral triangle. Find each side.", "20 cm", ["15 cm", "30 cm", "10 cm"]),
    ("A rectangular plot has perimeter 140 m and length 40 m. Find its breadth.", "30 m", ["20 m", "40 m", "50 m"]),
    ("A square garden has a perimeter of 200 m. Find the cost of fencing at ₹8 per metre.", "₹1,600", ["₹800", "₹2,000", "₹2,400"]),
    ("A rectangle has length 16 cm and breadth 9 cm. Find its perimeter.", "50 cm", ["25 cm", "144 cm", "45 cm"]),
    ("A regular decagon has each side 6 cm. Find its perimeter.", "60 cm", ["50 cm", "54 cm", "66 cm"]),
    ("The perimeter of a rectangle is 90 cm. Its length is 25 cm. Find its breadth.", "20 cm", ["15 cm", "25 cm", "30 cm"]),
    ("A rectangular field measures 80 m by 50 m. Find the cost of fencing at ₹15 per metre.", "₹3,900", ["₹1,950", "₹3,000", "₹4,500"]),
    ("A square has perimeter 144 cm. Find the length of one side.", "36 cm", ["24 cm", "48 cm", "72 cm"]),
]

HARD = [
    ("The perimeter of a rectangle is 100 cm. Its length is 10 cm more than its breadth. Find its area.", "600 cm²", ["500 cm²", "625 cm²", "700 cm²"]),
    ("The perimeter of a square is equal to the perimeter of a rectangle measuring 20 cm by 10 cm. Find the square's side.", "15 cm", ["10 cm", "20 cm", "30 cm"]),
    ("A rectangular field is 50 m long and 30 m wide. Find the cost of fencing it twice at ₹8 per metre.", "₹1,280", ["₹640", "₹1,000", "₹1,600"]),
    ("The length of a rectangle is twice its breadth. Its perimeter is 72 cm. Find its area.", "288 cm²", ["144 cm²", "216 cm²", "324 cm²"]),
    ("The perimeter of a square is 25% more than 80 cm. Find its side.", "25 cm", ["20 cm", "24 cm", "30 cm"]),
    ("A rectangle has a perimeter of 120 cm. Its length and breadth are in the ratio 2:1. Find its area.", "800 cm²", ["600 cm²", "900 cm²", "1000 cm²"]),
    ("A wire of length 88 cm is bent into a regular hexagon. Find the length of each side.", "14⅔ cm", ["12 cm", "15 cm", "16 cm"]),
    ("A rectangular garden has length 45 m and breadth 30 m. A path is fenced around it twice. Find the total fencing length.", "300 m", ["150 m", "225 m", "360 m"]),
    ("The perimeter of a rectangle is 160 cm. Its length is 3 times its breadth. Find its breadth.", "20 cm", ["15 cm", "25 cm", "30 cm"]),
    ("A square and a rectangle have equal perimeters. The square has side 18 cm and the rectangle has length 24 cm. Find the rectangle's breadth.", "12 cm", ["10 cm", "15 cm", "18 cm"]),
    ("The perimeter of an equilateral triangle is equal to the perimeter of a square of side 9 cm. Find the triangle's side.", "12 cm", ["9 cm", "15 cm", "18 cm"]),
    ("A rectangular plot has perimeter 240 m. Its length is 20 m more than its breadth. Find its length.", "70 m", ["60 m", "80 m", "90 m"]),
    ("The perimeter of a rectangle is 180 cm. Its length is 5 times its breadth. Find its area.", "1125 cm²", ["900 cm²", "1350 cm²", "1500 cm²"]),
    ("A square has a perimeter of 96 cm. If each side is increased by 4 cm, find the new perimeter.", "112 cm", ["100 cm", "108 cm", "120 cm"]),
    ("A rectangular field is 100 m long and 60 m wide. Find the cost of fencing at ₹25 per metre, leaving a 10 m gate.", "₹7,750", ["₹8,000", "₹7,500", "₹9,000"]),
    ("The perimeter of a rectangle is 200 cm. Its length exceeds its breadth by 20 cm. Find its breadth.", "40 cm", ["30 cm", "50 cm", "60 cm"]),
    ("A regular pentagon has a perimeter of 125 cm. Find its side length.", "25 cm", ["20 cm", "30 cm", "35 cm"]),
    ("A rectangular park has perimeter 300 m. Its length is 90 m. Find its breadth.", "60 m", ["50 m", "70 m", "80 m"]),
    ("The perimeter of a square is 20% less than 200 cm. Find its side.", "40 cm", ["35 cm", "45 cm", "50 cm"]),
    ("A rectangle has length 35 cm and perimeter 100 cm. Find its area.", "525 cm²", ["350 cm²", "450 cm²", "600 cm²"]),
    ("A rectangular field is 75 m long and 45 m wide. Find the distance covered by a person walking 4 rounds.", "960 m", ["480 m", "720 m", "1200 m"]),
    ("The perimeter of a square equals 3 times the perimeter of an equilateral triangle with side 8 cm. Find the square's side.", "18 cm", ["12 cm", "16 cm", "24 cm"]),
    ("A rectangle's length is 4 times its breadth. If its perimeter is 100 cm, find its length.", "40 cm", ["20 cm", "30 cm", "50 cm"]),
    ("A rectangular field has perimeter 400 m. Its length and breadth are in the ratio 3:2. Find its breadth.", "80 m", ["60 m", "100 m", "120 m"]),
    ("A square and a regular hexagon have equal perimeters. The square side is 12 cm. Find the hexagon's side.", "8 cm", ["6 cm", "10 cm", "12 cm"]),
    ("A rectangular garden has length 55 m and breadth 35 m. Find the fencing cost at ₹18 per metre, leaving a 10 m entrance.", "₹3,060", ["₹3,240", "₹2,880", "₹3,600"]),
    ("The perimeter of a rectangle is 144 cm. Its length is 8 cm more than twice its breadth. Find its breadth.", "32 cm", ["24 cm", "28 cm", "36 cm"]),
    ("A square has perimeter 160 cm. A rectangle has the same perimeter and breadth 30 cm. Find its length.", "50 cm", ["40 cm", "60 cm", "70 cm"]),
    ("The perimeter of a rectangle is 240 cm. Its length is 1.5 times its breadth. Find its length.", "72 cm", ["60 cm", "80 cm", "90 cm"]),
    ("A rectangular field measures 120 m by 80 m. Find the total cost of fencing it 3 times at ₹10 per metre.", "₹12,000", ["₹4,000", "₹8,000", "₹16,000"]),
]


def make_questions(data):
    questions = []

    for question, answer, wrong_answers in data:
        options = [str(answer)] + [str(x) for x in wrong_answers]

        if len(options) != 4 or len(set(options)) != 4:
            raise ValueError(f"Duplicate or invalid options: {question}")

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
