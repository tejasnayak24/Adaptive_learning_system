
import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"
TOPIC = "Symmetry"
SUBJECT = "Mathematics"

random.seed(42)

EASY = [
    ("What is symmetry?", "A balanced arrangement of parts", ["An irregular arrangement", "A curved line", "An open figure"]),
    ("What is a line of symmetry?", "A line that divides a figure into two matching halves", ["A line joining two corners", "A curved line", "The longest side"]),
    ("How many lines of symmetry does a square have?", "4", ["2", "3", "5"]),
    ("How many lines of symmetry does a rectangle have?", "2", ["1", "3", "4"]),
    ("How many lines of symmetry does an equilateral triangle have?", "3", ["1", "2", "4"]),
    ("How many lines of symmetry does a circle have?", "Infinitely many", ["2", "4", "8"]),
    ("How many lines of symmetry does a regular pentagon have?", "5", ["3", "4", "6"]),
    ("How many lines of symmetry does a regular hexagon have?", "6", ["3", "4", "8"]),
    ("Which letter has vertical line symmetry?", "A", ["F", "G", "R"]),
    ("Which letter has horizontal line symmetry?", "B", ["A", "L", "P"]),
    ("Which shape has no line of symmetry?", "A general scalene triangle", ["Square", "Circle", "Equilateral triangle"]),
    ("How many lines of symmetry does an isosceles triangle have?", "1", ["0", "2", "3"]),
    ("How many lines of symmetry does a regular octagon have?", "8", ["4", "6", "10"]),
    ("What is reflection symmetry also called?", "Line symmetry", ["Rotational symmetry", "Translation", "Scaling"]),
    ("What is rotational symmetry?", "A figure looks unchanged after a rotation", ["A figure is enlarged", "A figure is stretched", "A figure is divided into halves"]),
    ("What is the order of rotational symmetry of a square?", "4", ["2", "3", "8"]),
    ("What is the order of rotational symmetry of a rectangle?", "2", ["1", "3", "4"]),
    ("What is the order of rotational symmetry of an equilateral triangle?", "3", ["1", "2", "4"]),
    ("What is the order of rotational symmetry of a circle?", "Infinite", ["1", "2", "4"]),
    ("Does a non-square rectangle have diagonal lines of symmetry?", "No", ["Yes, one", "Yes, two", "Yes, four"]),
    ("How many lines of symmetry does a rhombus generally have?", "2", ["1", "3", "4"]),
    ("Which shape has exactly one line of symmetry?", "An isosceles triangle", ["A square", "A circle", "A regular hexagon"]),
    ("What is the angle of rotation for a square's smallest non-zero rotation?", "90°", ["45°", "180°", "270°"]),
    ("What is the angle of rotation for an equilateral triangle's smallest non-zero rotation?", "120°", ["60°", "90°", "180°"]),
    ("Which capital letter has vertical symmetry?", "M", ["F", "G", "R"]),
    ("Which capital letter has horizontal symmetry?", "H", ["A", "L", "P"]),
    ("What is the order of rotational symmetry of a regular hexagon?", "6", ["3", "4", "8"]),
    ("How many lines of symmetry does a regular decagon have?", "10", ["5", "8", "12"]),
    ("Does a circle have rotational symmetry?", "Yes", ["No", "Only at 90°", "Only at 180°"]),
    ("What happens when a figure is reflected across its line of symmetry?", "Its two halves match", ["It becomes larger", "It becomes smaller", "It changes its shape"]),
]

MEDIUM = [
    ("Find the order of rotational symmetry of a regular pentagon.", "5", ["2", "3", "4"]),
    ("Find the smallest angle of rotation of a regular hexagon.", "60°", ["45°", "90°", "120°"]),
    ("Find the smallest angle of rotation of a regular octagon.", "45°", ["30°", "60°", "90°"]),
    ("Find the smallest angle of rotation of a regular decagon.", "36°", ["30°", "45°", "60°"]),
    ("A figure has rotational symmetry of order 4. Find its smallest angle of rotation.", "90°", ["45°", "60°", "180°"]),
    ("A figure has rotational symmetry of order 6. Find its smallest angle of rotation.", "60°", ["30°", "90°", "120°"]),
    ("How many lines of symmetry does a regular heptagon have?", "7", ["5", "6", "8"]),
    ("How many lines of symmetry does a regular nonagon have?", "9", ["7", "8", "10"]),
    ("How many lines of symmetry does a regular dodecagon have?", "12", ["6", "10", "14"]),
    ("How many lines of symmetry does a general parallelogram have?", "0", ["1", "2", "4"]),
    ("How many lines of symmetry does a kite generally have?", "1", ["0", "2", "4"]),
    ("What is the order of rotational symmetry of a general parallelogram?", "2", ["1", "3", "4"]),
    ("What is the order of rotational symmetry of a regular octagon?", "8", ["4", "6", "10"]),
    ("What is the smallest angle of rotation of a regular pentagon?", "72°", ["60°", "90°", "108°"]),
    ("A figure has rotational symmetry of order 8. What is its smallest angle of rotation?", "45°", ["30°", "60°", "90°"]),
    ("How many lines of symmetry does a regular triangle have?", "3", ["1", "2", "4"]),
    ("How many lines of symmetry does a regular square-based figure have?", "4", ["2", "3", "8"]),
    ("Which shape has both line symmetry and rotational symmetry of order 2?", "Rectangle", ["A general scalene triangle", "A general trapezium", "A general kite"]),
    ("How many lines of symmetry does a semicircle have?", "1", ["0", "2", "4"]),
    ("What is the order of rotational symmetry of a non-square rectangle?", "2", ["1", "3", "4"]),
    ("A regular polygon has 9 lines of symmetry. How many sides does it have?", "9", ["6", "8", "12"]),
    ("A regular polygon has rotational symmetry of order 12. How many sides does it have?", "12", ["6", "10", "15"]),
    ("Find the smallest angle of rotation of a regular 12-sided polygon.", "30°", ["20°", "45°", "60°"]),
    ("A figure looks unchanged after rotations of 90°, 180°, 270° and 360°. What is its order?", "4", ["2", "3", "5"]),
    ("How many lines of symmetry does a regular 15-sided polygon have?", "15", ["10", "12", "30"]),
    ("Which shape has exactly two lines of symmetry and rotational order 2?", "Non-square rectangle", ["Equilateral triangle", "Regular pentagon", "General kite"]),
    ("What is the smallest angle of rotation of a regular 20-sided polygon?", "18°", ["15°", "20°", "30°"]),
    ("A figure has rotational order 5. How many times does it match itself in one full turn?", "5", ["4", "6", "10"]),
    ("How many lines of symmetry does a regular 4-sided polygon have?", "4", ["2", "3", "8"]),
    ("A figure has 10 lines of symmetry. If it is a regular polygon, how many sides does it have?", "10", ["5", "8", "12"]),
]

HARD = [
    ("A regular polygon has a smallest angle of rotation of 24°. Find its number of sides.", "15", ["12", "18", "20"]),
    ("A regular polygon has a smallest angle of rotation of 18°. Find its number of sides.", "20", ["15", "18", "24"]),
    ("A regular polygon has a smallest angle of rotation of 15°. Find its number of sides.", "24", ["20", "18", "30"]),
    ("A regular polygon has 18 lines of symmetry. Find its smallest angle of rotation.", "20°", ["18°", "30°", "36°"]),
    ("A figure has rotational symmetry of order 12. How many degrees does it rotate between consecutive matching positions?", "30°", ["15°", "45°", "60°"]),
    ("A figure has rotational symmetry of order 15. Find its smallest angle of rotation.", "24°", ["15°", "20°", "30°"]),
    ("A regular polygon has an interior angle of 150°. Find its number of lines of symmetry.", "12", ["10", "15", "18"]),
    ("A regular polygon has an exterior angle of 30°. Find its rotational order.", "12", ["10", "15", "18"]),
    ("A regular polygon has 16 sides. Find its smallest angle of rotation.", "22.5°", ["20°", "24°", "30°"]),
    ("A regular polygon has 24 sides. Find its smallest angle of rotation.", "15°", ["12°", "18°", "24°"]),
    ("A figure has rotational symmetry of order 9. How many matching positions occur in one complete turn?", "9", ["8", "10", "18"]),
    ("A regular polygon has 10 sides. How many lines of symmetry pass through opposite vertices if the number of sides is even?", "5", ["4", "10", "20"]),
    ("A regular polygon has 10 sides. How many lines of symmetry pass through the midpoints of opposite sides?", "5", ["4", "10", "20"]),
    ("A regular polygon has 12 sides. How many lines of symmetry pass through opposite vertices?", "6", ["4", "8", "12"]),
    ("A regular polygon has 12 sides. How many lines of symmetry pass through opposite side midpoints?", "6", ["4", "8", "12"]),
    ("A regular polygon has 14 sides. Find its rotational order.", "14", ["7", "12", "28"]),
    ("A figure has rotational order 20. Find its smallest angle of rotation.", "18°", ["15°", "20°", "24°"]),
    ("A regular polygon has an exterior angle of 20°. Find its number of sides and lines of symmetry.", "18", ["15", "20", "24"]),
    ("A regular polygon has 30 sides. Find its smallest angle of rotation.", "12°", ["10°", "15°", "18°"]),
    ("A figure has rotational symmetry of order 4. How many matching positions are there in 360°?", "4", ["2", "3", "8"]),
    ("A regular polygon has 8 sides. Find the number of lines of symmetry and its rotational order.", "8 and 8", ["4 and 4", "8 and 4", "4 and 8"]),
    ("A regular polygon has 6 sides. Find the number of lines of symmetry and its rotational order.", "6 and 6", ["3 and 3", "6 and 3", "3 and 6"]),
    ("A regular polygon has 9 sides. Find its smallest angle of rotation.", "40°", ["30°", "45°", "60°"]),
    ("A regular polygon has 25 sides. Find its smallest angle of rotation.", "14.4°", ["12°", "15°", "18°"]),
    ("A regular polygon has 36 sides. Find its smallest angle of rotation.", "10°", ["12°", "15°", "18°"]),
    ("A regular polygon has 5 lines of symmetry. Find its smallest angle of rotation.", "72°", ["60°", "90°", "120°"]),
    ("A regular polygon has 7 lines of symmetry. Find its smallest angle of rotation.", "360/7°", ["45°", "60°", "72°"]),
    ("A figure has rotational symmetry of order 3. What is the angle between consecutive matching positions?", "120°", ["60°", "90°", "180°"]),
    ("A regular polygon has 40 sides. Find its smallest angle of rotation.", "9°", ["8°", "10°", "12°"]),
    ("A regular polygon has an exterior angle of 12°. Find its number of lines of symmetry.", "30", ["24", "36", "40"]),
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
