
import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"
TOPIC = "Circles"
SUBJECT = "Mathematics"

random.seed(42)

EASY = [
    ("What is the fixed point inside a circle called?", "Centre", ["Radius", "Chord", "Diameter"]),
    ("What is the distance from the centre to the circle called?", "Radius", ["Diameter", "Chord", "Arc"]),
    ("What is the longest chord of a circle?", "Diameter", ["Radius", "Arc", "Tangent"]),
    ("What is the diameter equal to?", "Twice the radius", ["Half the radius", "Three times the radius", "Four times the radius"]),
    ("What is a line segment joining two points on a circle called?", "Chord", ["Radius", "Tangent", "Arc"]),
    ("What is the distance around a circle called?", "Circumference", ["Area", "Diameter", "Radius"]),
    ("Which symbol is commonly used for pi?", "π", ["θ", "α", "β"]),
    ("What is the approximate value of pi?", "3.14", ["2.14", "3.41", "4.13"]),
    ("How many radii can be drawn in a circle?", "Infinitely many", ["One", "Two", "Four"]),
    ("How many diameters can be drawn in a circle?", "Infinitely many", ["One", "Two", "Four"]),
    ("A circle has a radius of 5 cm. Find its diameter.", "10 cm", ["5 cm", "15 cm", "25 cm"]),
    ("A circle has a diameter of 18 cm. Find its radius.", "9 cm", ["18 cm", "36 cm", "6 cm"]),
    ("Which part of a circle is a curved portion of its boundary?", "Arc", ["Chord", "Radius", "Diameter"]),
    ("What is a line touching a circle at exactly one point called?", "Tangent", ["Secant", "Chord", "Diameter"]),
    ("What is a line intersecting a circle at two points called?", "Secant", ["Tangent", "Radius", "Arc"]),
    ("What is the area of a circle with radius r?", "πr²", ["2πr", "πd", "2r"]),
    ("What is the circumference of a circle?", "2πr", ["πr²", "πr", "4πr"]),
    ("If the radius of a circle is 7 cm, what is its diameter?", "14 cm", ["7 cm", "21 cm", "28 cm"]),
    ("What is the radius of a circle with diameter 20 cm?", "10 cm", ["20 cm", "40 cm", "5 cm"]),
    ("Which chord passes through the centre of a circle?", "Diameter", ["Radius", "Tangent", "Arc"]),
    ("What is half of a circle called?", "Semicircle", ["Quadrant", "Chord", "Sector"]),
    ("What is one-fourth of a circle called?", "Quadrant", ["Semicircle", "Diameter", "Segment"]),
    ("Does a radius meet the circumference at a point?", "Yes", ["No", "Only sometimes", "Only at the centre"]),
    ("Are all radii of the same circle equal?", "Yes", ["No", "Only two are equal", "Only opposite radii are equal"]),
    ("A circle has a radius of 3 cm. Find its diameter.", "6 cm", ["3 cm", "9 cm", "12 cm"]),
    ("What is the area measured in?", "Square units", ["Linear units", "Cubic units", "Degrees"]),
    ("What is the circumference measured in?", "Linear units", ["Square units", "Cubic units", "Degrees"]),
    ("What is the angle in a complete circle?", "360°", ["180°", "90°", "270°"]),
    ("What is the angle in a semicircle?", "180°", ["90°", "270°", "360°"]),
    ("What is the angle in a quadrant?", "90°", ["45°", "180°", "360°"]),
]

MEDIUM = [
    ("Find the diameter of a circle with radius 8 cm.", "16 cm", ["8 cm", "24 cm", "32 cm"]),
    ("Find the radius of a circle with diameter 36 cm.", "18 cm", ["36 cm", "72 cm", "12 cm"]),
    ("Find the circumference of a circle with radius 7 cm. Use π = 22/7.", "44 cm", ["22 cm", "154 cm", "88 cm"]),
    ("Find the area of a circle with radius 7 cm. Use π = 22/7.", "154 cm²", ["44 cm²", "77 cm²", "308 cm²"]),
    ("Find the circumference of a circle with diameter 14 cm. Use π = 22/7.", "44 cm", ["22 cm", "88 cm", "154 cm"]),
    ("Find the area of a circle with radius 14 cm. Use π = 22/7.", "616 cm²", ["308 cm²", "88 cm²", "1232 cm²"]),
    ("A circle has a circumference of 88 cm. Find its radius using π = 22/7.", "14 cm", ["7 cm", "28 cm", "21 cm"]),
    ("A circle has an area of 154 cm². Find its radius using π = 22/7.", "7 cm", ["14 cm", "11 cm", "5 cm"]),
    ("Find the circumference of a circle with radius 3.5 cm. Use π = 22/7.", "22 cm", ["11 cm", "44 cm", "77 cm"]),
    ("Find the area of a circle with radius 3.5 cm. Use π = 22/7.", "38.5 cm²", ["22 cm²", "77 cm²", "19.25 cm²"]),
    ("If the radius of a circle is doubled, what happens to its diameter?", "It doubles", ["It becomes half", "It becomes four times", "It remains unchanged"]),
    ("If the radius of a circle is doubled, how does its area change?", "It becomes four times", ["It doubles", "It becomes half", "It remains unchanged"]),
    ("If the diameter of a circle is doubled, how does its circumference change?", "It doubles", ["It becomes four times", "It becomes half", "It remains unchanged"]),
    ("Find the area of a circle with diameter 28 cm. Use π = 22/7.", "616 cm²", ["308 cm²", "1232 cm²", "88 cm²"]),
    ("Find the circumference of a circle with diameter 21 cm. Use π = 22/7.", "66 cm", ["33 cm", "132 cm", "154 cm"]),
    ("A wheel has a radius of 35 cm. Find its circumference using π = 22/7.", "220 cm", ["110 cm", "440 cm", "70 cm"]),
    ("Find the area of a circle with radius 10 cm. Use π = 3.14.", "314 cm²", ["31.4 cm²", "62.8 cm²", "628 cm²"]),
    ("Find the circumference of a circle with radius 10 cm. Use π = 3.14.", "62.8 cm", ["31.4 cm", "314 cm", "125.6 cm"]),
    ("A circle has a diameter of 10 cm. Find its area using π = 3.14.", "78.5 cm²", ["31.4 cm²", "157 cm²", "314 cm²"]),
    ("Find the radius of a circle whose circumference is 132 cm. Use π = 22/7.", "21 cm", ["14 cm", "42 cm", "7 cm"]),
    ("Find the diameter of a circle whose circumference is 44 cm. Use π = 22/7.", "14 cm", ["7 cm", "28 cm", "21 cm"]),
    ("Find the area of a semicircle with radius 7 cm. Use π = 22/7.", "77 cm²", ["154 cm²", "44 cm²", "38.5 cm²"]),
    ("Find the perimeter of a semicircle with radius 7 cm. Use π = 22/7.", "36 cm", ["22 cm", "44 cm", "29 cm"]),
    ("Find the area of a quadrant with radius 14 cm. Use π = 22/7.", "154 cm²", ["616 cm²", "308 cm²", "77 cm²"]),
    ("Find the length of an arc forming a quarter circle of radius 14 cm. Use π = 22/7.", "22 cm", ["44 cm", "11 cm", "88 cm"]),
    ("A circular garden has radius 14 m. Find its area using π = 22/7.", "616 m²", ["308 m²", "88 m²", "1232 m²"]),
    ("A circular track has radius 21 m. Find its circumference using π = 22/7.", "132 m", ["66 m", "264 m", "154 m"]),
    ("Find the area of a circle whose radius is 5 cm. Use π = 3.14.", "78.5 cm²", ["31.4 cm²", "15.7 cm²", "157 cm²"]),
    ("The radius of a circle increases from 4 cm to 8 cm. How many times does its area become?", "4 times", ["2 times", "8 times", "16 times"]),
    ("A circular field has a diameter of 28 m. Find its circumference using π = 22/7.", "88 m", ["44 m", "176 m", "616 m"]),
]

HARD = [
    ("The circumference of a circle is 176 cm. Find its diameter using π = 22/7.", "56 cm", ["28 cm", "44 cm", "88 cm"]),
    ("The area of a circle is 1386 cm². Find its radius using π = 22/7.", "21 cm", ["14 cm", "42 cm", "28 cm"]),
    ("The circumference of a circle is 66 cm. Find its area using π = 22/7.", "346.5 cm²", ["693 cm²", "231 cm²", "154 cm²"]),
    ("The area of a circle is 616 cm². Find its circumference using π = 22/7.", "88 cm", ["44 cm", "176 cm", "132 cm"]),
    ("A circular park has a radius of 21 m. Find the cost of fencing it at ₹10 per metre. Use π = 22/7.", "₹1,320", ["₹660", "₹2,640", "₹1,540"]),
    ("A circular garden has a diameter of 14 m. Find its area using π = 22/7.", "154 m²", ["44 m²", "308 m²", "616 m²"]),
    ("The radius of a circle is increased by 50%. Find the percentage increase in its area.", "125%", ["50%", "100%", "150%"]),
    ("The radius of a circle is reduced by 20%. Find the percentage decrease in its area.", "36%", ["20%", "40%", "16%"]),
    ("The circumference of a circle increases from 44 cm to 88 cm. How does its area change?", "It becomes four times", ["It doubles", "It becomes three times", "It remains unchanged"]),
    ("A wheel of radius 35 cm makes 100 complete revolutions. Find the distance travelled in metres. Use π = 22/7.", "220 m", ["110 m", "440 m", "350 m"]),
    ("A circular track has a diameter of 70 m. Find the distance covered in 5 rounds. Use π = 22/7.", "1100 m", ["550 m", "220 m", "700 m"]),
    ("Find the area of a ring with outer radius 14 cm and inner radius 7 cm. Use π = 22/7.", "462 cm²", ["616 cm²", "154 cm²", "308 cm²"]),
    ("Find the perimeter of a semicircle with diameter 28 cm. Use π = 22/7.", "72 cm", ["44 cm", "56 cm", "88 cm"]),
    ("Find the area of a semicircle with diameter 28 cm. Use π = 22/7.", "308 cm²", ["616 cm²", "154 cm²", "462 cm²"]),
    ("A circular field has radius 14 m. Find the cost of covering it at ₹5 per m². Use π = 22/7.", "₹3,080", ["₹1,540", "₹6,160", "₹2,800"]),
    ("The area of a circle is 154 cm². Find its diameter using π = 22/7.", "14 cm", ["7 cm", "28 cm", "21 cm"]),
    ("The circumference of a circle is 132 cm. Find its area using π = 22/7.", "1386 cm²", ["693 cm²", "616 cm²", "264 cm²"]),
    ("A circular pond has a radius of 7 m. Find the cost of fencing it twice at ₹20 per metre. Use π = 22/7.", "₹1,760", ["₹880", "₹2,640", "₹1,540"]),
    ("The diameter of a circle is increased by 100%. Find the percentage increase in its area.", "300%", ["100%", "200%", "400%"]),
    ("A wheel has a circumference of 220 cm. How many revolutions will it make to cover 110 m?", "50", ["25", "100", "75"]),
    ("Find the area of a quadrant with radius 28 cm. Use π = 22/7.", "616 cm²", ["1232 cm²", "308 cm²", "154 cm²"]),
    ("A circular wire of length 88 cm is bent into a circle. Find its radius using π = 22/7.", "14 cm", ["7 cm", "21 cm", "28 cm"]),
    ("The area of a circle is 2464 cm². Find its diameter using π = 22/7.", "56 cm", ["28 cm", "42 cm", "64 cm"]),
    ("A circular lawn has radius 21 m. Find the area of the lawn using π = 22/7.", "1386 m²", ["693 m²", "132 m²", "1540 m²"]),
    ("A circular table has diameter 2.8 m. Find its circumference using π = 22/7.", "8.8 m", ["4.4 m", "17.6 m", "6.6 m"]),
    ("Find the difference between the areas of two circles with radii 14 cm and 7 cm. Use π = 22/7.", "462 cm²", ["308 cm²", "616 cm²", "154 cm²"]),
    ("A circular path has an outer radius of 14 m and inner radius of 10.5 m. Find its area using π = 22/7.", "269.5 m²", ["154 m²", "462 m²", "308 m²"]),
    ("A wheel of diameter 70 cm makes 200 revolutions. Find the distance travelled in metres. Use π = 22/7.", "440 m", ["220 m", "880 m", "140 m"]),
    ("The radius of a circle is 14 cm. Find the length of a 90° arc using π = 22/7.", "22 cm", ["44 cm", "11 cm", "88 cm"]),
    ("A circular field has a circumference of 352 m. Find its area using π = 22/7.", "9856 m²", ["4928 m²", "2464 m²", "1232 m²"]),
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
