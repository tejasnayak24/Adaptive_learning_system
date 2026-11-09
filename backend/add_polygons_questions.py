
import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"
TOPIC = "Polygons"
SUBJECT = "Mathematics"

random.seed(42)

EASY = [
    ("What is a polygon?", "A closed plane figure made of straight line segments", ["A curved figure", "An open figure", "A three-dimensional figure"]),
    ("How many sides does a triangle have?", "3", ["4", "5", "6"]),
    ("How many sides does a pentagon have?", "5", ["4", "6", "7"]),
    ("How many sides does a hexagon have?", "6", ["5", "7", "8"]),
    ("How many sides does an octagon have?", "8", ["6", "7", "9"]),
    ("How many sides does a decagon have?", "10", ["8", "9", "12"]),
    ("What is a polygon with four sides called?", "Quadrilateral", ["Pentagon", "Hexagon", "Triangle"]),
    ("What is a polygon with seven sides called?", "Heptagon", ["Hexagon", "Octagon", "Nonagon"]),
    ("What is a polygon with nine sides called?", "Nonagon", ["Octagon", "Decagon", "Heptagon"]),
    ("What is a regular polygon?", "A polygon with all sides and angles equal", ["A polygon with unequal sides", "An open figure", "A figure with curved sides"]),
    ("How many sides does a square have?", "4", ["3", "5", "6"]),
    ("How many sides does a regular hexagon have?", "6", ["5", "7", "8"]),
    ("Which polygon has the fewest possible sides?", "Triangle", ["Square", "Pentagon", "Hexagon"]),
    ("How many diagonals does a triangle have?", "0", ["1", "2", "3"]),
    ("What is the sum of the interior angles of a triangle?", "180°", ["90°", "270°", "360°"]),
    ("What is the sum of the interior angles of a quadrilateral?", "360°", ["180°", "270°", "540°"]),
    ("How many diagonals does a quadrilateral have?", "2", ["1", "3", "4"]),
    ("Which polygon has eight sides?", "Octagon", ["Hexagon", "Heptagon", "Decagon"]),
    ("Which polygon has ten sides?", "Decagon", ["Nonagon", "Octagon", "Hexagon"]),
    ("What is the perimeter of a polygon?", "Sum of all its side lengths", ["Sum of its angles", "Area inside it", "Number of vertices"]),
    ("What is the sum of exterior angles of any convex polygon?", "360°", ["180°", "270°", "540°"]),
    ("How many vertices does a pentagon have?", "5", ["4", "6", "7"]),
    ("What is a diagonal of a polygon?", "A line segment joining two non-adjacent vertices", ["A side of the polygon", "A curved line", "An exterior angle"]),
    ("Which of these is not a polygon?", "Circle", ["Triangle", "Square", "Pentagon"]),
    ("How many sides does a hexagon have?", "6", ["4", "5", "8"]),
    ("What is a polygon with twelve sides called?", "Dodecagon", ["Decagon", "Nonagon", "Octagon"]),
    ("How many diagonals does a pentagon have?", "5", ["4", "6", "7"]),
    ("What is the measure of each exterior angle of a regular hexagon?", "60°", ["45°", "90°", "120°"]),
    ("What is the measure of each interior angle of a regular triangle?", "60°", ["45°", "90°", "120°"]),
    ("Which polygon has all sides and all interior angles equal?", "Regular polygon", ["Irregular polygon", "Open polygon", "Concave polygon"]),
]

MEDIUM = [
    ("Find the sum of interior angles of a pentagon.", "540°", ["360°", "720°", "900°"]),
    ("Find the sum of interior angles of a hexagon.", "720°", ["540°", "900°", "1080°"]),
    ("Find the sum of interior angles of an octagon.", "1080°", ["720°", "900°", "1260°"]),
    ("Find each interior angle of a regular pentagon.", "108°", ["90°", "120°", "135°"]),
    ("Find each interior angle of a regular hexagon.", "120°", ["90°", "108°", "135°"]),
    ("Find each exterior angle of a regular pentagon.", "72°", ["60°", "90°", "108°"]),
    ("Find each exterior angle of a regular octagon.", "45°", ["30°", "60°", "90°"]),
    ("How many diagonals does a hexagon have?", "9", ["6", "8", "12"]),
    ("How many diagonals does a heptagon have?", "14", ["7", "12", "21"]),
    ("How many diagonals does an octagon have?", "20", ["16", "18", "24"]),
    ("The sum of interior angles of a polygon is 900°. How many sides does it have?", "7", ["6", "8", "9"]),
    ("The sum of interior angles of a polygon is 1260°. Find its number of sides.", "9", ["8", "10", "12"]),
    ("Each exterior angle of a regular polygon is 40°. How many sides does it have?", "9", ["8", "10", "12"]),
    ("Each exterior angle of a regular polygon is 30°. Find its number of sides.", "12", ["10", "11", "15"]),
    ("Find the perimeter of a regular hexagon with side 7 cm.", "42 cm", ["35 cm", "49 cm", "56 cm"]),
    ("Find the perimeter of a regular octagon with side 5 cm.", "40 cm", ["30 cm", "35 cm", "45 cm"]),
    ("A regular pentagon has a perimeter of 60 cm. Find its side length.", "12 cm", ["10 cm", "15 cm", "20 cm"]),
    ("Find each interior angle of a regular octagon.", "135°", ["120°", "140°", "150°"]),
    ("Find each exterior angle of a regular decagon.", "36°", ["30°", "40°", "45°"]),
    ("How many diagonals can be drawn from one vertex of a hexagon?", "3", ["2", "4", "5"]),
    ("How many diagonals can be drawn from one vertex of a decagon?", "7", ["6", "8", "9"]),
    ("The interior angle sum of a polygon is 1800°. Find the number of sides.", "12", ["10", "11", "14"]),
    ("The exterior angle of a regular polygon is 24°. Find the number of sides.", "15", ["12", "14", "18"]),
    ("Find the sum of interior angles of a decagon.", "1440°", ["1080°", "1260°", "1620°"]),
    ("A regular polygon has 8 sides. Find the sum of its exterior angles.", "360°", ["180°", "720°", "1080°"]),
    ("A regular hexagon has a perimeter of 72 cm. Find its side length.", "12 cm", ["10 cm", "14 cm", "16 cm"]),
    ("How many diagonals does a decagon have?", "35", ["30", "40", "45"]),
    ("A polygon has 11 sides. Find the sum of its interior angles.", "1620°", ["1440°", "1800°", "1980°"]),
    ("Each interior angle of a regular polygon is 150°. Find the number of sides.", "12", ["10", "11", "15"]),
    ("Find each interior angle of a regular decagon.", "144°", ["135°", "150°", "120°"]),
]

HARD = [
    ("The interior angle sum of a polygon is 1980°. Find the number of sides.", "13", ["12", "14", "15"]),
    ("Each interior angle of a regular polygon is 160°. Find the number of sides.", "18", ["16", "20", "24"]),
    ("Each exterior angle of a regular polygon is 15°. Find the number of sides.", "24", ["20", "18", "30"]),
    ("The number of diagonals in a polygon is 35. Find the number of sides.", "10", ["8", "9", "12"]),
    ("A polygon has 54 diagonals. Find its number of sides.", "12", ["10", "11", "14"]),
    ("The number of diagonals of a polygon is 3 times its number of sides. Find the number of sides.", "9", ["8", "10", "12"]),
    ("The interior angle sum of a polygon is 4 times 180°. Find the number of sides.", "6", ["5", "7", "8"]),
    ("Each interior angle of a regular polygon is 5 times its exterior angle. Find the number of sides.", "12", ["10", "15", "18"]),
    ("The exterior angle of a regular polygon is one-fifth of its interior angle. Find the number of sides.", "12", ["10", "15", "20"]),
    ("The interior angle sum of a polygon is 900° more than the interior angle sum of a pentagon. Find the number of sides.", "12", ["10", "11", "13"]),
    ("A polygon has 27 diagonals. Find the number of sides.", "9", ["8", "10", "12"]),
    ("A regular polygon has 15 sides. Find each interior angle.", "156°", ["150°", "160°", "144°"]),
    ("A regular polygon has 20 sides. Find each exterior angle.", "18°", ["15°", "20°", "24°"]),
    ("The number of diagonals of a polygon is 44. Find its number of sides.", "11", ["10", "12", "13"]),
    ("The sum of interior angles of a polygon is 2340°. Find the number of sides.", "15", ["14", "16", "18"]),
    ("Each interior angle of a regular polygon is 165°. Find the number of sides.", "24", ["20", "18", "30"]),
    ("A polygon has 14 sides. Find the number of diagonals from one vertex.", "11", ["10", "12", "13"]),
    ("A regular polygon has an exterior angle of 12°. Find its number of sides.", "30", ["24", "28", "36"]),
    ("The number of diagonals of a polygon is 5 times its number of sides. Find the number of sides.", "13", ["11", "12", "14"]),
    ("The interior angle sum of a polygon is 2520°. Find its number of sides.", "16", ["15", "17", "18"]),
    ("A regular polygon has 18 sides. Find the sum of its interior angles.", "2880°", ["2700°", "3060°", "3240°"]),
    ("The interior angle of a regular polygon is 8 times its exterior angle. Find its number of sides.", "18", ["16", "20", "24"]),
    ("A polygon has 90 diagonals. Find the number of sides.", "15", ["14", "16", "18"]),
    ("The sum of interior angles of a polygon is 2700°. Find each interior angle if it is regular.", "150°", ["144°", "156°", "160°"]),
    ("A regular polygon has 36 sides. Find each exterior angle.", "10°", ["12°", "15°", "18°"]),
    ("A polygon has 17 sides. Find its total number of diagonals.", "119", ["102", "136", "144"]),
    ("The number of diagonals of a polygon is 7 times its number of sides. Find the number of sides.", "16", ["14", "15", "18"]),
    ("A regular polygon has an interior angle of 140°. Find its number of sides.", "9", ["8", "10", "12"]),
    ("The interior angle sum of a polygon is 3060°. Find its number of sides.", "19", ["18", "20", "21"]),
    ("A regular polygon has 25 sides. Find the sum of its interior angles.", "4140°", ["3960°", "4320°", "4500°"]),
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
                f"{difficulty} must contain 30 questions. Found {len(data)}"
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
