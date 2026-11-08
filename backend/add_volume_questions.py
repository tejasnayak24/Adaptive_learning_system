
import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"
TOPIC = "Volume"
SUBJECT = "Mathematics"

random.seed(42)

EASY = [
    ("What is the formula for the volume of a cube?", "a³", ["6a²", "4a²", "a²"]),
    ("Find the volume of a cube with side 3 cm.", "27 cm³", ["9 cm³", "18 cm³", "36 cm³"]),
    ("What is the formula for the volume of a cuboid?", "Length × Breadth × Height", ["Length × Breadth", "2(lb + bh + hl)", "Length + Breadth + Height"]),
    ("Find the volume of a cuboid measuring 4 cm × 3 cm × 2 cm.", "24 cm³", ["12 cm³", "18 cm³", "36 cm³"]),
    ("Find the volume of a cube with side 5 cm.", "125 cm³", ["25 cm³", "100 cm³", "150 cm³"]),
    ("Which unit is used to measure volume?", "Cubic metre", ["Square metre", "Metre", "Kilogram"]),
    ("Find the volume of a cuboid with length 5 cm, breadth 4 cm and height 3 cm.", "60 cm³", ["20 cm³", "40 cm³", "50 cm³"]),
    ("Find the volume of a cube with side 2 cm.", "8 cm³", ["4 cm³", "6 cm³", "12 cm³"]),
    ("How many dimensions are used to calculate the volume of a cuboid?", "3", ["1", "2", "4"]),
    ("Find the volume of a cuboid measuring 6 cm × 2 cm × 3 cm.", "36 cm³", ["12 cm³", "24 cm³", "30 cm³"]),
    ("Find the volume of a cube with side 4 cm.", "64 cm³", ["16 cm³", "32 cm³", "48 cm³"]),
    ("What is the formula for the volume of a cylinder?", "πr²h", ["2πrh", "πrh", "2πr²"]),
    ("Find the volume of a cuboid measuring 7 cm × 2 cm × 3 cm.", "42 cm³", ["21 cm³", "35 cm³", "49 cm³"]),
    ("Find the volume of a cube with side 6 cm.", "216 cm³", ["36 cm³", "108 cm³", "180 cm³"]),
    ("What is the volume of a cube with side 1 cm?", "1 cm³", ["2 cm³", "3 cm³", "6 cm³"]),
    ("Find the volume of a cuboid with length 8 cm, breadth 5 cm and height 2 cm.", "80 cm³", ["40 cm³", "60 cm³", "100 cm³"]),
    ("What is the volume of a cube with side 10 cm?", "1000 cm³", ["100 cm³", "600 cm³", "500 cm³"]),
    ("How many cubic centimetres make one litre?", "1000 cm³", ["100 cm³", "10 cm³", "10000 cm³"]),
    ("Find the volume of a cuboid measuring 10 cm × 3 cm × 2 cm.", "60 cm³", ["30 cm³", "50 cm³", "90 cm³"]),
    ("Find the volume of a cube with side 7 cm.", "343 cm³", ["49 cm³", "147 cm³", "294 cm³"]),
    ("What is the volume of a cuboid with dimensions 3 cm, 3 cm and 3 cm?", "27 cm³", ["9 cm³", "18 cm³", "36 cm³"]),
    ("Find the volume of a cylinder with radius 1 cm and height 7 cm. Use π = 22/7.", "22 cm³", ["44 cm³", "11 cm³", "154 cm³"]),
    ("Find the volume of a cuboid measuring 9 cm × 2 cm × 4 cm.", "72 cm³", ["36 cm³", "54 cm³", "90 cm³"]),
    ("What is the volume of a cube with side 8 cm?", "512 cm³", ["64 cm³", "256 cm³", "128 cm³"]),
    ("Which solid has six equal square faces?", "Cube", ["Cuboid", "Cylinder", "Cone"]),
    ("Find the volume of a cuboid with length 12 cm, breadth 2 cm and height 2 cm.", "48 cm³", ["24 cm³", "36 cm³", "60 cm³"]),
    ("Find the volume of a cube with side 9 cm.", "729 cm³", ["81 cm³", "243 cm³", "648 cm³"]),
    ("What happens to the volume of a cube when its side increases?", "It increases", ["It decreases", "It remains the same", "It becomes zero"]),
    ("Find the volume of a cuboid measuring 5 cm × 5 cm × 2 cm.", "50 cm³", ["25 cm³", "40 cm³", "60 cm³"]),
    ("Find the volume of a cylinder with radius 7 cm and height 1 cm. Use π = 22/7.", "154 cm³", ["44 cm³", "77 cm³", "308 cm³"])
]

MEDIUM = [
    ("Find the volume of a cube with side 12 cm.", "1728 cm³", ["144 cm³", "864 cm³", "1296 cm³"]),
    ("Find the volume of a cuboid measuring 12 cm × 8 cm × 5 cm.", "480 cm³", ["240 cm³", "400 cm³", "500 cm³"]),
    ("A cuboid has volume 360 cm³, length 12 cm and breadth 5 cm. Find its height.", "6 cm", ["5 cm", "8 cm", "10 cm"]),
    ("Find the volume of a cylinder with radius 7 cm and height 10 cm. Use π = 22/7.", "1540 cm³", ["770 cm³", "440 cm³", "3080 cm³"]),
    ("A cube has a volume of 729 cm³. Find its side.", "9 cm", ["8 cm", "10 cm", "12 cm"]),
    ("Find the volume of a cuboid measuring 15 cm × 10 cm × 4 cm.", "600 cm³", ["300 cm³", "450 cm³", "750 cm³"]),
    ("A cuboid has volume 720 cm³, length 12 cm and height 10 cm. Find its breadth.", "6 cm", ["5 cm", "8 cm", "12 cm"]),
    ("Find the volume of a cylinder with radius 3.5 cm and height 8 cm. Use π = 22/7.", "308 cm³", ["154 cm³", "616 cm³", "220 cm³"]),
    ("Find the volume of a cube with side 15 cm.", "3375 cm³", ["225 cm³", "1125 cm³", "3000 cm³"]),
    ("A cuboid measures 20 cm × 8 cm × 5 cm. Find its volume.", "800 cm³", ["400 cm³", "600 cm³", "1000 cm³"]),
    ("A cube has a volume of 1000 cm³. Find its side.", "10 cm", ["20 cm", "15 cm", "5 cm"]),
    ("Find the volume of a cylinder with radius 7 cm and height 5 cm. Use π = 22/7.", "770 cm³", ["385 cm³", "154 cm³", "440 cm³"]),
    ("A cuboid has volume 540 cm³, length 15 cm and breadth 6 cm. Find its height.", "6 cm", ["5 cm", "8 cm", "10 cm"]),
    ("Find the volume of a cube with side 11 cm.", "1331 cm³", ["121 cm³", "726 cm³", "1000 cm³"]),
    ("Find the volume of a cuboid measuring 18 cm × 10 cm × 6 cm.", "1080 cm³", ["540 cm³", "900 cm³", "1200 cm³"]),
    ("A cylinder has radius 14 cm and height 5 cm. Find its volume using π = 22/7.", "3080 cm³", ["1540 cm³", "616 cm³", "4400 cm³"]),
    ("A cuboid has volume 960 cm³, breadth 8 cm and height 10 cm. Find its length.", "12 cm", ["10 cm", "15 cm", "20 cm"]),
    ("Find the volume of a cube with side 13 cm.", "2197 cm³", ["169 cm³", "676 cm³", "2028 cm³"]),
    ("Find the volume of a cylinder with radius 7 cm and height 12 cm. Use π = 22/7.", "1848 cm³", ["924 cm³", "1540 cm³", "3696 cm³"]),
    ("A cuboid has dimensions 25 cm × 12 cm × 4 cm. Find its volume.", "1200 cm³", ["600 cm³", "1000 cm³", "1500 cm³"]),
    ("A cube has a volume of 1728 cm³. Find its side.", "12 cm", ["10 cm", "14 cm", "16 cm"]),
    ("A cuboid has volume 840 cm³, length 14 cm and breadth 10 cm. Find its height.", "6 cm", ["5 cm", "7 cm", "8 cm"]),
    ("Find the volume of a cylinder with radius 3 cm and height 14 cm. Use π = 22/7.", "396 cm³", ["198 cm³", "264 cm³", "462 cm³"]),
    ("Find the volume of a cuboid measuring 16 cm × 9 cm × 5 cm.", "720 cm³", ["360 cm³", "600 cm³", "800 cm³"]),
    ("Find the volume of a cube with side 14 cm.", "2744 cm³", ["196 cm³", "1372 cm³", "2400 cm³"]),
    ("A cylinder has radius 7 cm and height 20 cm. Find its volume using π = 22/7.", "3080 cm³", ["1540 cm³", "4400 cm³", "6160 cm³"]),
    ("A cuboid has volume 1500 cm³, length 15 cm and height 10 cm. Find its breadth.", "10 cm", ["5 cm", "15 cm", "20 cm"]),
    ("Find the volume of a cuboid measuring 30 cm × 10 cm × 6 cm.", "1800 cm³", ["900 cm³", "1200 cm³", "2000 cm³"]),
    ("A cube has volume 4096 cm³. Find its side.", "16 cm", ["14 cm", "18 cm", "20 cm"]),
    ("Find the volume of a cylinder with radius 14 cm and height 10 cm. Use π = 22/7.", "6160 cm³", ["3080 cm³", "1540 cm³", "8800 cm³"])
]

HARD = [
    ("A rectangular tank is 5 m long, 4 m wide and 3 m high. Find its capacity.", "60 m³", ["20 m³", "40 m³", "80 m³"]),
    ("A cube has a volume of 8000 cm³. Find its side.", "20 cm", ["10 cm", "30 cm", "40 cm"]),
    ("A cylindrical tank has radius 7 m and height 10 m. Find its volume using π = 22/7.", "1540 m³", ["770 m³", "3080 m³", "440 m³"]),
    ("A cuboid has volume 2400 cm³, length 20 cm and breadth 12 cm. Find its height.", "10 cm", ["8 cm", "12 cm", "15 cm"]),
    ("The side of a cube is doubled. By what factor does its volume increase?", "8 times", ["2 times", "4 times", "6 times"]),
    ("A water tank measures 4 m × 3 m × 2 m. How many cubic metres of water can it hold?", "24 m³", ["12 m³", "18 m³", "36 m³"]),
    ("A cylinder has diameter 14 cm and height 20 cm. Find its volume using π = 22/7.", "3080 cm³", ["1540 cm³", "6160 cm³", "4400 cm³"]),
    ("A cuboid has volume 3600 cm³, length 30 cm and height 10 cm. Find its breadth.", "12 cm", ["10 cm", "15 cm", "20 cm"]),
    ("A cube has a volume of 15625 cm³. Find its side.", "25 cm", ["15 cm", "20 cm", "30 cm"]),
    ("A cylindrical container has radius 3.5 cm and height 20 cm. Find its volume using π = 22/7.", "770 cm³", ["385 cm³", "1540 cm³", "440 cm³"]),
    ("A rectangular swimming pool is 25 m long, 10 m wide and 2 m deep. Find its volume.", "500 m³", ["250 m³", "400 m³", "600 m³"]),
    ("A cuboid has dimensions 24 cm × 15 cm × 10 cm. Find its volume.", "3600 cm³", ["1800 cm³", "3000 cm³", "4000 cm³"]),
    ("A cube has volume 27000 cm³. Find its side.", "30 cm", ["20 cm", "25 cm", "40 cm"]),
    ("A cylinder has radius 14 cm and height 15 cm. Find its volume using π = 22/7.", "9240 cm³", ["4620 cm³", "6160 cm³", "12320 cm³"]),
    ("A cuboid has volume 5040 cm³, breadth 12 cm and height 14 cm. Find its length.", "30 cm", ["25 cm", "35 cm", "40 cm"]),
    ("If each dimension of a cuboid is doubled, how many times does its volume become?", "8 times", ["2 times", "4 times", "6 times"]),
    ("A cylindrical tank has radius 7 m and height 5 m. Find its capacity in cubic metres using π = 22/7.", "770 m³", ["385 m³", "1540 m³", "440 m³"]),
    ("A cuboid measures 40 cm × 25 cm × 12 cm. Find its volume.", "12000 cm³", ["6000 cm³", "10000 cm³", "15000 cm³"]),
    ("A cube has volume 64000 cm³. Find its side.", "40 cm", ["20 cm", "30 cm", "50 cm"]),
    ("A cylinder has diameter 28 cm and height 15 cm. Find its volume using π = 22/7.", "9240 cm³", ["4620 cm³", "6160 cm³", "12320 cm³"]),
    ("A water tank measures 6 m × 5 m × 4 m. Find its capacity in litres.", "120000 litres", ["12000 litres", "1200 litres", "100000 litres"]),
    ("A cuboid has volume 7200 cm³, length 24 cm and breadth 15 cm. Find its height.", "20 cm", ["15 cm", "25 cm", "30 cm"]),
    ("A cube has side 25 cm. Find its volume.", "15625 cm³", ["625 cm³", "12500 cm³", "15000 cm³"]),
    ("A cylinder has radius 10.5 cm and height 8 cm. Find its volume using π = 22/7.", "2772 cm³", ["1386 cm³", "5544 cm³", "1848 cm³"]),
    ("A cuboid has dimensions 35 cm × 20 cm × 15 cm. Find its volume.", "10500 cm³", ["7000 cm³", "9000 cm³", "12000 cm³"]),
    ("A cube has volume 91125 cm³. Find its side.", "45 cm", ["35 cm", "40 cm", "50 cm"]),
    ("A cylindrical drum has radius 14 cm and height 25 cm. Find its volume using π = 22/7.", "15400 cm³", ["7700 cm³", "12320 cm³", "17600 cm³"]),
    ("A cuboid has volume 9600 cm³, length 40 cm and height 8 cm. Find its breadth.", "30 cm", ["20 cm", "25 cm", "40 cm"]),
    ("A tank is 10 m long, 5 m wide and 3 m deep. How many litres can it hold?", "150000 litres", ["15000 litres", "50000 litres", "100000 litres"]),
    ("A cylinder has radius 21 cm and height 10 cm. Find its volume using π = 22/7.", "13860 cm³", ["6930 cm³", "9240 cm³", "15400 cm³"])
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
