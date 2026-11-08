
import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

TOPIC = "Triangles"
SUBJECT = "Mathematics"

random.seed(42)

# Format: (question, correct answer, [three wrong answers])

EASY = [
    ("How many sides does a triangle have?", "3", ["2", "4", "5"]),
    ("How many angles does a triangle have?", "3", ["2", "4", "5"]),
    ("What is the sum of the interior angles of a triangle?", "180°", ["90°", "270°", "360°"]),
    ("A triangle with all three sides equal is called what?", "Equilateral triangle", ["Isosceles triangle", "Scalene triangle", "Right triangle"]),
    ("A triangle with two equal sides is called what?", "Isosceles triangle", ["Equilateral triangle", "Scalene triangle", "Right triangle"]),
    ("A triangle with all sides unequal is called what?", "Scalene triangle", ["Equilateral triangle", "Isosceles triangle", "Right triangle"]),
    ("A triangle having one angle equal to 90° is called what?", "Right-angled triangle", ["Acute-angled triangle", "Obtuse-angled triangle", "Equilateral triangle"]),
    ("A triangle with all angles less than 90° is called what?", "Acute-angled triangle", ["Obtuse-angled triangle", "Right-angled triangle", "Scalene triangle"]),
    ("A triangle with one angle greater than 90° is called what?", "Obtuse-angled triangle", ["Acute-angled triangle", "Right-angled triangle", "Equilateral triangle"]),
    ("Each angle of an equilateral triangle measures how many degrees?", "60°", ["45°", "90°", "120°"]),
    ("How many equal sides does an isosceles triangle have?", "2", ["1", "3", "0"]),
    ("How many equal sides does an equilateral triangle have?", "3", ["1", "2", "0"]),
    ("What is the longest side of a right-angled triangle called?", "Hypotenuse", ["Base", "Altitude", "Median"]),
    ("What is the side opposite the right angle called?", "Hypotenuse", ["Base", "Height", "Median"]),
    ("What is the sum of two acute angles in a right-angled triangle?", "90°", ["60°", "180°", "120°"]),
    ("Can a triangle have two right angles?", "No", ["Yes", "Always", "Sometimes"]),
    ("Can a triangle have two obtuse angles?", "No", ["Yes", "Always", "Sometimes"]),
    ("What is the perimeter of a triangle with sides 3 cm, 4 cm and 5 cm?", "12 cm", ["10 cm", "11 cm", "15 cm"]),
    ("Find the perimeter of an equilateral triangle with side 6 cm.", "18 cm", ["12 cm", "24 cm", "36 cm"]),
    ("Find the perimeter of a triangle with sides 5 cm, 5 cm and 7 cm.", "17 cm", ["15 cm", "16 cm", "18 cm"]),
    ("What is the area formula for a triangle?", "1/2 × base × height", ["base × height", "2 × base × height", "base + height"]),
    ("Find the area of a triangle with base 10 cm and height 4 cm.", "20 cm²", ["40 cm²", "14 cm²", "24 cm²"]),
    ("How many vertices does a triangle have?", "3", ["2", "4", "5"]),
    ("What is the name of the point where two sides of a triangle meet?", "Vertex", ["Centre", "Midpoint", "Base"]),
    ("What is the sum of the exterior angles of any triangle?", "360°", ["180°", "90°", "270°"]),
    ("How many altitudes can be drawn in a triangle?", "3", ["1", "2", "4"]),
    ("How many medians can be drawn in a triangle?", "3", ["1", "2", "4"]),
    ("Which triangle has angles 90°, 60° and 30°?", "Right-angled triangle", ["Equilateral triangle", "Obtuse-angled triangle", "Acute-angled triangle"]),
    ("Which triangle has angles 70°, 60° and 50°?", "Acute-angled triangle", ["Right-angled triangle", "Obtuse-angled triangle", "Equilateral triangle"]),
    ("What is the perimeter of a triangle with sides 8 cm, 6 cm and 10 cm?", "24 cm", ["20 cm", "22 cm", "26 cm"]),
]

MEDIUM = [
    ("Two angles of a triangle are 50° and 60°. Find the third angle.", "70°", ["60°", "80°", "90°"]),
    ("Two angles of a triangle are 45° and 75°. Find the third angle.", "60°", ["50°", "70°", "80°"]),
    ("Two angles of a triangle are 80° and 40°. Find the third angle.", "60°", ["50°", "70°", "90°"]),
    ("An isosceles triangle has a vertex angle of 40°. Find each base angle.", "70°", ["60°", "80°", "90°"]),
    ("An isosceles triangle has a base angle of 65°. Find the vertex angle.", "50°", ["55°", "60°", "65°"]),
    ("Find the third angle of a triangle if the other two angles are 90° and 35°.", "55°", ["45°", "60°", "65°"]),
    ("Find the perimeter of a triangle with sides 12 cm, 15 cm and 18 cm.", "45 cm", ["40 cm", "42 cm", "48 cm"]),
    ("An equilateral triangle has a perimeter of 36 cm. Find its side.", "12 cm", ["9 cm", "18 cm", "15 cm"]),
    ("An isosceles triangle has equal sides of 8 cm and a base of 6 cm. Find its perimeter.", "22 cm", ["20 cm", "24 cm", "26 cm"]),
    ("Find the area of a triangle with base 12 cm and height 8 cm.", "48 cm²", ["96 cm²", "40 cm²", "56 cm²"]),
    ("Find the area of a triangle with base 15 cm and height 6 cm.", "45 cm²", ["90 cm²", "30 cm²", "60 cm²"]),
    ("A triangle has an area of 30 cm² and a base of 10 cm. Find its height.", "6 cm", ["5 cm", "8 cm", "10 cm"]),
    ("A triangle has an area of 48 cm² and a height of 8 cm. Find its base.", "12 cm", ["10 cm", "14 cm", "16 cm"]),
    ("An exterior angle of a triangle is 120°. One opposite interior angle is 50°. Find the other.", "70°", ["60°", "80°", "90°"]),
    ("An exterior angle of a triangle is 110°. One opposite interior angle is 45°. Find the other.", "65°", ["55°", "75°", "85°"]),
    ("The angles of a triangle are in the ratio 2:3:4. Find the smallest angle.", "40°", ["30°", "45°", "50°"]),
    ("The angles of a triangle are in the ratio 1:2:3. Find the largest angle.", "90°", ["60°", "75°", "120°"]),
    ("The angles of a triangle are in the ratio 3:4:5. Find the middle angle.", "60°", ["45°", "50°", "75°"]),
    ("A triangle has angles x°, 2x° and 3x°. Find x.", "30°", ["20°", "40°", "60°"]),
    ("A triangle has angles (x + 20)°, (x + 30)° and 70°. Find x.", "30°", ["20°", "40°", "50°"]),
    ("Find the hypotenuse of a right triangle with other sides 3 cm and 4 cm.", "5 cm", ["6 cm", "7 cm", "8 cm"]),
    ("Find the hypotenuse of a right triangle with sides 5 cm and 12 cm.", "13 cm", ["11 cm", "14 cm", "15 cm"]),
    ("A right triangle has hypotenuse 10 cm and one side 6 cm. Find the other side.", "8 cm", ["6 cm", "7 cm", "9 cm"]),
    ("A triangle has sides 7 cm, 24 cm and 25 cm. Is it right-angled?", "Yes", ["No", "Equilateral", "Isosceles"]),
    ("Which set of sides can form a triangle?", "5 cm, 6 cm, 8 cm", ["2 cm, 3 cm, 6 cm", "1 cm, 2 cm, 4 cm", "3 cm, 4 cm, 8 cm"]),
    ("Find the perimeter of an isosceles triangle with equal sides 10 cm and base 12 cm.", "32 cm", ["30 cm", "34 cm", "36 cm"]),
    ("An equilateral triangle has a side of 9 cm. Find its perimeter.", "27 cm", ["18 cm", "36 cm", "24 cm"]),
    ("Find the area of a triangle with base 20 cm and height 9 cm.", "90 cm²", ["180 cm²", "80 cm²", "100 cm²"]),
    ("A triangle has area 72 cm² and base 18 cm. Find its height.", "8 cm", ["6 cm", "9 cm", "12 cm"]),
    ("Two angles of an isosceles triangle are 55° each. Find the third angle.", "70°", ["60°", "80°", "90°"]),
]

HARD = [
    ("The angles of a triangle are in the ratio 2:3:5. Find the largest angle.", "90°", ["60°", "75°", "100°"]),
    ("The angles of a triangle are in the ratio 4:5:6. Find the smallest angle.", "48°", ["36°", "54°", "60°"]),
    ("The angles of a triangle are in the ratio 5:6:7. Find the largest angle.", "70°", ["50°", "60°", "80°"]),
    ("The angles of a triangle are (2x + 10)°, (3x - 5)° and (x + 25)°. Find x.", "25", ["20", "30", "35"]),
    ("The angles of a triangle are (x + 10)°, (2x + 20)° and (3x - 30)°. Find the largest angle.", "90°", ["60°", "80°", "100°"]),
    ("An exterior angle is 130°. Its two opposite interior angles are (2x)° and (3x)°. Find x.", "26", ["20", "30", "40"]),
    ("An exterior angle of a triangle is 140°. One opposite interior angle is 65°. Find the other.", "75°", ["65°", "85°", "90°"]),
    ("An isosceles triangle has a vertex angle of 100°. Find each base angle.", "40°", ["30°", "50°", "60°"]),
    ("An isosceles triangle has a base angle of 40°. Find the vertex angle.", "100°", ["80°", "90°", "120°"]),
    ("The perimeter of an equilateral triangle is 54 cm. Find its side length.", "18 cm", ["15 cm", "27 cm", "12 cm"]),
    ("The perimeter of an isosceles triangle is 40 cm. Its base is 10 cm. Find each equal side.", "15 cm", ["10 cm", "20 cm", "12 cm"]),
    ("The area of a triangle is 96 cm² and its base is 16 cm. Find its height.", "12 cm", ["10 cm", "14 cm", "16 cm"]),
    ("The area of a triangle is 150 cm² and its height is 15 cm. Find its base.", "20 cm", ["15 cm", "25 cm", "30 cm"]),
    ("A right triangle has hypotenuse 17 cm and one side 8 cm. Find the other side.", "15 cm", ["12 cm", "14 cm", "16 cm"]),
    ("A right triangle has hypotenuse 25 cm and one side 7 cm. Find the other side.", "24 cm", ["20 cm", "22 cm", "23 cm"]),
    ("Find the hypotenuse of a right triangle whose perpendicular sides are 9 cm and 12 cm.", "15 cm", ["13 cm", "14 cm", "16 cm"]),
    ("A triangle has sides 9 cm, 12 cm and 15 cm. Find its area.", "54 cm²", ["45 cm²", "60 cm²", "72 cm²"]),
    ("A triangle has sides 6 cm, 8 cm and 10 cm. Find its perimeter.", "24 cm", ["20 cm", "22 cm", "26 cm"]),
    ("A triangle has sides 10 cm, 24 cm and 26 cm. Find its area.", "120 cm²", ["100 cm²", "130 cm²", "144 cm²"]),
    ("The angles of a triangle are x°, (x + 20)° and (x + 40)°. Find the largest angle.", "80°", ["60°", "70°", "90°"]),
    ("The angles of a triangle are (2x)°, (3x)° and (4x)°. Find the middle angle.", "60°", ["40°", "50°", "80°"]),
    ("An exterior angle of a triangle is 150°. The opposite interior angles are in the ratio 2:3. Find the larger angle.", "90°", ["60°", "75°", "100°"]),
    ("The angles of a triangle are in the ratio 1:1:4. Find the largest angle.", "120°", ["90°", "100°", "110°"]),
    ("The angles of a triangle are in the ratio 2:2:5. Find the smallest angle.", "40°", ["20°", "30°", "50°"]),
    ("A triangle has perimeter 48 cm. Two sides are 15 cm and 17 cm. Find the third side.", "16 cm", ["14 cm", "18 cm", "20 cm"]),
    ("A triangle has sides 13 cm, 14 cm and 15 cm. Find its perimeter.", "42 cm", ["40 cm", "44 cm", "46 cm"]),
    ("The area of a triangle is 84 cm². If its base is 14 cm, find its height.", "12 cm", ["10 cm", "14 cm", "16 cm"]),
    ("A right triangle has sides 20 cm and 21 cm as perpendicular sides. Find the hypotenuse.", "29 cm", ["28 cm", "30 cm", "31 cm"]),
    ("A right triangle has hypotenuse 13 cm and one side 5 cm. Find the other side.", "12 cm", ["10 cm", "11 cm", "14 cm"]),
    ("The angles of a triangle are (x + 15)°, (2x + 15)° and (3x)°. Find the smallest angle.", "40°", ["30°", "45°", "50°"]),
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
