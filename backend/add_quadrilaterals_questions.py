
import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"
TOPIC = "Quadrilaterals"
SUBJECT = "Mathematics"

random.seed(42)

# Each question: question, correct answer, three wrong answers

EASY = [
    ("How many sides does a quadrilateral have?", "4", ["3", "5", "6"]),
    ("How many angles does a quadrilateral have?", "4", ["3", "5", "6"]),
    ("What is the sum of the interior angles of a quadrilateral?", "360°", ["180°", "270°", "540°"]),
    ("Which quadrilateral has four equal sides and four right angles?", "Square", ["Rectangle", "Rhombus", "Trapezium"]),
    ("Which quadrilateral has opposite sides equal and four right angles?", "Rectangle", ["Square", "Kite", "Trapezium"]),
    ("Which quadrilateral has all four sides equal?", "Rhombus", ["Rectangle", "Trapezium", "Parallelogram"]),
    ("How many pairs of parallel sides does a parallelogram have?", "2", ["1", "3", "0"]),
    ("Which quadrilateral has exactly one pair of parallel sides in the usual school definition?", "Trapezium", ["Square", "Rectangle", "Rhombus"]),
    ("What is the shape of a standard playing card?", "Rectangle", ["Square", "Rhombus", "Kite"]),
    ("How many diagonals does a quadrilateral have?", "2", ["1", "3", "4"]),
    ("Are opposite sides of a rectangle equal?", "Yes", ["No", "Only one pair", "Only sometimes"]),
    ("What is each angle of a square?", "90°", ["60°", "45°", "120°"]),
    ("Which quadrilateral has two pairs of adjacent equal sides?", "Kite", ["Rectangle", "Trapezium", "Parallelogram"]),
    ("Are opposite angles of a parallelogram equal?", "Yes", ["No", "Only one pair", "Always 90°"]),
    ("How many right angles does a rectangle have?", "4", ["2", "1", "3"]),
    ("Which quadrilateral has all sides equal but angles need not be 90°?", "Rhombus", ["Rectangle", "Trapezium", "Kite"]),
    ("What is a four-sided polygon called?", "Quadrilateral", ["Triangle", "Pentagon", "Hexagon"]),
    ("How many vertices does a quadrilateral have?", "4", ["3", "5", "6"]),
    ("Which quadrilateral has opposite sides parallel and equal?", "Parallelogram", ["Kite", "Trapezium", "Pentagon"]),
    ("Are the diagonals of a rectangle equal?", "Yes", ["No", "Only one is longer", "They are perpendicular always"]),
    ("Which quadrilateral has four right angles?", "Rectangle", ["Rhombus", "Kite", "Trapezium"]),
    ("How many pairs of opposite angles does a quadrilateral have?", "2", ["1", "3", "4"]),
    ("What is the sum of angles in any quadrilateral?", "360°", ["90°", "180°", "270°"]),
    ("Which quadrilateral looks like a diamond shape?", "Rhombus", ["Rectangle", "Square only", "Trapezium"]),
    ("Can a square also be classified as a rectangle?", "Yes", ["No", "Only if tilted", "Only if enlarged"]),
    ("Can a square also be classified as a rhombus?", "Yes", ["No", "Only sometimes", "Only if rotated"]),
    ("How many sides of a square are equal?", "4", ["2", "3", "None"]),
    ("What is the measure of a straight angle?", "180°", ["90°", "270°", "360°"]),
    ("Which quadrilateral has diagonals that bisect each other?", "Parallelogram", ["Trapezium", "Kite only", "Triangle"]),
    ("What is the perimeter of a square with side 5 cm?", "20 cm", ["10 cm", "15 cm", "25 cm"]),
]

MEDIUM = [
    ("Three angles of a quadrilateral are 80°, 90° and 100°. Find the fourth angle.", "90°", ["80°", "100°", "110°"]),
    ("A rectangle has length 12 cm and breadth 5 cm. Find its perimeter.", "34 cm", ["17 cm", "60 cm", "30 cm"]),
    ("Find the perimeter of a square whose side is 9 cm.", "36 cm", ["18 cm", "81 cm", "27 cm"]),
    ("A parallelogram has one angle of 70°. Find its adjacent angle.", "110°", ["70°", "90°", "120°"]),
    ("One angle of a parallelogram is 120°. What is its opposite angle?", "120°", ["60°", "90°", "240°"]),
    ("A rhombus has a side of 8 cm. Find its perimeter.", "32 cm", ["16 cm", "64 cm", "24 cm"]),
    ("The angles of a quadrilateral are 90°, 90°, 90° and x°. Find x.", "90°", ["80°", "100°", "120°"]),
    ("A rectangle has length 15 cm and breadth 7 cm. Find its area.", "105 cm²", ["44 cm²", "22 cm²", "100 cm²"]),
    ("The perimeter of a square is 48 cm. Find its side.", "12 cm", ["8 cm", "16 cm", "24 cm"]),
    ("A parallelogram has adjacent angles x° and 2x°. Find x.", "60°", ["45°", "90°", "120°"]),
    ("One angle of a quadrilateral is 75°. The other three are equal. Find each of them.", "95°", ["90°", "100°", "105°"]),
    ("A rectangle has perimeter 50 cm and length 15 cm. Find its breadth.", "10 cm", ["5 cm", "15 cm", "20 cm"]),
    ("The diagonal of a square divides it into how many triangles?", "2", ["3", "4", "1"]),
    ("A rhombus has one angle of 60°. Find its adjacent angle.", "120°", ["60°", "90°", "150°"]),
    ("Find the area of a square with side 11 cm.", "121 cm²", ["44 cm²", "22 cm²", "100 cm²"]),
    ("A parallelogram has angles 80°, 100°, 80° and x°. Find x.", "100°", ["80°", "90°", "120°"]),
    ("A rectangle has area 72 cm² and length 9 cm. Find its breadth.", "8 cm", ["6 cm", "9 cm", "12 cm"]),
    ("The perimeter of a rectangle is 40 cm. Its length is 12 cm. Find its breadth.", "8 cm", ["6 cm", "10 cm", "12 cm"]),
    ("A square has an area of 64 cm². Find its perimeter.", "32 cm", ["16 cm", "24 cm", "64 cm"]),
    ("Two angles of a quadrilateral are 100° and 80°. The remaining angles are equal. Find each.", "90°", ["80°", "100°", "110°"]),
    ("A parallelogram has sides 10 cm and 6 cm. Find its perimeter.", "32 cm", ["16 cm", "60 cm", "26 cm"]),
    ("The perimeter of a rhombus is 52 cm. Find the length of each side.", "13 cm", ["12 cm", "14 cm", "15 cm"]),
    ("A rectangle has length 18 cm and breadth 4 cm. Find its area.", "72 cm²", ["44 cm²", "36 cm²", "88 cm²"]),
    ("One angle of a parallelogram is 65°. Find the other three angles.", "115°, 65°, 115°", ["65°, 65°, 115°", "90°, 90°, 115°", "115°, 115°, 115°"]),
    ("A square has a perimeter of 100 cm. Find its area.", "625 cm²", ["100 cm²", "250 cm²", "400 cm²"]),
    ("A rectangle's length is twice its breadth. If breadth is 6 cm, find its perimeter.", "36 cm", ["24 cm", "30 cm", "48 cm"]),
    ("The diagonals of a parallelogram bisect each other. If one half is 7 cm, find the full diagonal.", "14 cm", ["7 cm", "21 cm", "28 cm"]),
    ("A quadrilateral has angles 70°, 80°, 110° and x°. Find x.", "100°", ["90°", "110°", "120°"]),
    ("A rectangle has a perimeter of 60 cm and breadth 10 cm. Find its length.", "20 cm", ["15 cm", "25 cm", "30 cm"]),
    ("A square's side increases from 4 cm to 8 cm. What is its new area?", "64 cm²", ["32 cm²", "16 cm²", "48 cm²"]),
]

HARD = [
    ("The angles of a quadrilateral are in the ratio 2:3:4:3. Find the largest angle.", "120°", ["90°", "100°", "110°"]),
    ("The angles of a quadrilateral are x°, 2x°, 3x° and 4x°. Find the smallest angle.", "36°", ["30°", "40°", "45°"]),
    ("The perimeter of a rectangle is 84 cm. Its length is 3 times its breadth. Find its area.", "243 cm²", ["216 cm²", "189 cm²", "252 cm²"]),
    ("The perimeter of a square equals the perimeter of a rectangle measuring 12 cm by 8 cm. Find the square's area.", "100 cm²", ["64 cm²", "81 cm²", "144 cm²"]),
    ("The angles of a quadrilateral are (x+10)°, (x+20)°, (2x)° and (2x+30)°. Find x.", "50°", ["40°", "45°", "60°"]),
    ("A rectangle's length is 5 cm more than its breadth. Its perimeter is 50 cm. Find its area.", "150 cm²", ["144 cm²", "125 cm²", "175 cm²"]),
    ("The diagonals of a rhombus are 16 cm and 12 cm. Find its area.", "96 cm²", ["192 cm²", "48 cm²", "144 cm²"]),
    ("A square has a diagonal of 10√2 cm. Find its area.", "100 cm²", ["50 cm²", "200 cm²", "20 cm²"]),
    ("The adjacent angles of a parallelogram are in the ratio 2:1. Find the larger angle.", "120°", ["90°", "60°", "150°"]),
    ("A rectangle has an area of 180 cm² and length 15 cm. Find its perimeter.", "54 cm", ["45 cm", "60 cm", "48 cm"]),
    ("The angles of a quadrilateral are in the ratio 1:2:3:4. Find the smallest angle.", "36°", ["30°", "40°", "45°"]),
    ("A square and a rectangle have equal areas. The square side is 10 cm and rectangle length is 20 cm. Find rectangle breadth.", "5 cm", ["4 cm", "8 cm", "10 cm"]),
    ("The perimeter of a rhombus is 80 cm. One diagonal is 24 cm. Find the other diagonal.", "32 cm", ["24 cm", "40 cm", "48 cm"]),
    ("The angles of a quadrilateral are (2x+10)°, (2x+20)°, (x+30)° and (x+40)°. Find x.", "43⅓°", ["40°", "45°", "50°"]),
    ("A rectangular field is 25 m long and 15 m wide. Find the cost of fencing at ₹20 per metre.", "₹1,600", ["₹800", "₹1,200", "₹2,000"]),
    ("The length of a rectangle is increased by 20% while breadth remains unchanged. By what percentage does its area increase?", "20%", ["10%", "25%", "40%"]),
    ("The side of a square is increased by 50%. Find the percentage increase in its area.", "125%", ["50%", "100%", "150%"]),
    ("A rectangle has length 24 cm and diagonal 26 cm. Find its breadth.", "10 cm", ["12 cm", "14 cm", "16 cm"]),
    ("A rhombus has diagonals 10 cm and 24 cm. Find the length of one side.", "13 cm", ["12 cm", "14 cm", "15 cm"]),
    ("The perimeter of a rectangle is 100 cm. Its length exceeds its breadth by 10 cm. Find its area.", "600 cm²", ["500 cm²", "625 cm²", "700 cm²"]),
    ("A square has an area of 196 cm². Find the length of its diagonal.", "14√2 cm", ["14 cm", "28 cm", "7√2 cm"]),
    ("The angles of a quadrilateral are in the ratio 3:4:5:6. Find the second-largest angle.", "100°", ["80°", "90°", "120°"]),
    ("A rectangular garden has area 240 m² and breadth 12 m. Find the cost of fencing at ₹15 per metre.", "₹660", ["₹600", "₹720", "₹750"]),
    ("A square and a rectangle have equal perimeters of 40 cm. The rectangle has length 12 cm. Find its area.", "96 cm²", ["100 cm²", "80 cm²", "120 cm²"]),
    ("The diagonals of a rhombus are 18 cm and 24 cm. Find its perimeter.", "60 cm", ["48 cm", "72 cm", "84 cm"]),
    ("A rectangle's length and breadth are in the ratio 5:3. Its perimeter is 64 cm. Find its area.", "240 cm²", ["180 cm²", "200 cm²", "256 cm²"]),
    ("One angle of a parallelogram is 3 times its adjacent angle. Find the smaller angle.", "45°", ["30°", "60°", "90°"]),
    ("The angles of a quadrilateral are (x+5)°, (x+15)°, (2x+10)° and (2x+30)°. Find the largest angle.", "120°", ["100°", "110°", "130°"]),
    ("A square has a perimeter of 64 cm. A rectangle has the same perimeter and length 20 cm. Find the rectangle's area.", "180 cm²", ["160 cm²", "200 cm²", "220 cm²"]),
    ("A rectangle has length 30 cm and breadth 16 cm. Find the length of its diagonal.", "34 cm", ["32 cm", "36 cm", "40 cm"]),
]


def make_questions(data):
    questions = []

    for question, answer, wrong_answers in data:
        options = [str(answer)] + [str(x) for x in wrong_answers]

        if len(options) != 4 or len(set(options)) != 4:
            raise ValueError(f"Invalid or duplicate options: {question}")

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
