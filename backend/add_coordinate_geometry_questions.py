
import sqlite3
import random
from pathlib import Path

random.seed(42)

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

TOPIC = "Coordinate Geometry"
SUBJECT = "Mathematics"


# Each question format:
# (question, correct_answer, [wrong1, wrong2, wrong3])


EASY = [
    ("What is the horizontal axis called?", "X-axis", ["Y-axis", "Origin", "Quadrant"]),
    ("What is the vertical axis called?", "Y-axis", ["X-axis", "Origin", "Quadrant"]),
    ("What are the coordinates of the origin?", "(0, 0)", ["(1, 0)", "(0, 1)", "(1, 1)"]),
    ("How many quadrants are there in a Cartesian plane?", "4", ["2", "3", "5"]),
    ("Which coordinate is written first in an ordered pair?", "X-coordinate", ["Y-coordinate", "Z-coordinate", "Origin"]),
    ("Which coordinate is written second in an ordered pair?", "Y-coordinate", ["X-coordinate", "Z-coordinate", "Origin"]),
    ("What is the X-coordinate also called?", "Abscissa", ["Ordinate", "Origin", "Quadrant"]),
    ("What is the Y-coordinate also called?", "Ordinate", ["Abscissa", "Origin", "Axis"]),
    ("In which quadrant are both coordinates positive?", "First quadrant", ["Second quadrant", "Third quadrant", "Fourth quadrant"]),
    ("In which quadrant is X negative and Y positive?", "Second quadrant", ["First quadrant", "Third quadrant", "Fourth quadrant"]),
    ("In which quadrant are both coordinates negative?", "Third quadrant", ["First quadrant", "Second quadrant", "Fourth quadrant"]),
    ("In which quadrant is X positive and Y negative?", "Fourth quadrant", ["First quadrant", "Second quadrant", "Third quadrant"]),
    ("What is the X-coordinate of the point (5, 3)?", "5", ["3", "0", "-5"]),
    ("What is the Y-coordinate of the point (4, 7)?", "7", ["4", "0", "-7"]),
    ("Which point lies on the X-axis?", "(5, 0)", ["(0, 5)", "(3, 4)", "(2, 2)"]),
    ("Which point lies on the Y-axis?", "(0, 6)", ["(6, 0)", "(2, 3)", "(4, 4)"]),
    ("What is the ordinate of the point (8, 2)?", "2", ["8", "0", "-2"]),
    ("What is the abscissa of the point (6, 9)?", "6", ["9", "0", "-6"]),
    ("Which point represents the origin?", "(0, 0)", ["(1, 1)", "(0, 1)", "(1, 0)"]),
    ("What is the sign of both coordinates in the first quadrant?", "Positive, positive", ["Negative, positive", "Negative, negative", "Positive, negative"]),
    ("What is the sign of coordinates in the second quadrant?", "Negative, positive", ["Positive, positive", "Negative, negative", "Positive, negative"]),
    ("What is the sign of coordinates in the third quadrant?", "Negative, negative", ["Positive, positive", "Negative, positive", "Positive, negative"]),
    ("What is the sign of coordinates in the fourth quadrant?", "Positive, negative", ["Positive, positive", "Negative, positive", "Negative, negative"]),
    ("A point on the X-axis has which Y-coordinate?", "0", ["1", "-1", "Any number"]),
    ("A point on the Y-axis has which X-coordinate?", "0", ["1", "-1", "Any number"]),
    ("What is the ordered pair for a point 3 units right and 2 units up from origin?", "(3, 2)", ["(2, 3)", "(-3, 2)", "(3, -2)"]),
    ("What does the origin represent?", "Intersection of X-axis and Y-axis", ["End of X-axis", "End of Y-axis", "Fourth quadrant"]),
    ("How many axes are present in a two-dimensional Cartesian plane?", "2", ["1", "3", "4"]),
    ("Which point is in the first quadrant?", "(2, 5)", ["(-2, 5)", "(-2, -5)", "(2, -5)"]),
    ("Which point is in the third quadrant?", "(-4, -3)", ["(4, 3)", "(-4, 3)", "(4, -3)"]),
]


MEDIUM = [
    ("Find the distance between (0, 0) and (3, 4).", "5 units", ["4 units", "6 units", "7 units"]),
    ("Find the distance between (0, 0) and (6, 8).", "10 units", ["8 units", "12 units", "14 units"]),
    ("Find the midpoint of (2, 4) and (6, 8).", "(4, 6)", ["(3, 6)", "(4, 5)", "(8, 12)"]),
    ("Find the midpoint of (0, 0) and (4, 6).", "(2, 3)", ["(4, 3)", "(2, 6)", "(1, 3)"]),
    ("What is the reflection of (3, 4) across the X-axis?", "(3, -4)", ["(-3, 4)", "(-3, -4)", "(4, 3)"]),
    ("What is the reflection of (5, 2) across the Y-axis?", "(-5, 2)", ["(5, -2)", "(-5, -2)", "(2, 5)"]),
    ("What is the reflection of (2, 3) across the origin?", "(-2, -3)", ["(2, -3)", "(-2, 3)", "(3, 2)"]),
    ("Find the distance between (1, 2) and (4, 6).", "5 units", ["4 units", "6 units", "7 units"]),
    ("Find the distance between (2, 3) and (2, 9).", "6 units", ["5 units", "7 units", "9 units"]),
    ("Find the distance between (-2, 0) and (3, 0).", "5 units", ["3 units", "4 units", "6 units"]),
    ("Find the midpoint of (-2, 4) and (4, 8).", "(1, 6)", ["(2, 6)", "(1, 4)", "(3, 6)"]),
    ("Find the midpoint of (3, 5) and (7, 9).", "(5, 7)", ["(4, 7)", "(5, 6)", "(10, 14)"]),
    ("Which quadrant contains the point (-7, 4)?", "Second quadrant", ["First quadrant", "Third quadrant", "Fourth quadrant"]),
    ("Which quadrant contains the point (6, -8)?", "Fourth quadrant", ["First quadrant", "Second quadrant", "Third quadrant"]),
    ("Find the value of x if the point (x, 5) lies on the Y-axis.", "0", ["5", "1", "-5"]),
    ("Find the value of y if the point (4, y) lies on the X-axis.", "0", ["4", "1", "-4"]),
    ("What is the distance between (0, 0) and (-5, 0)?", "5 units", ["0 units", "10 units", "25 units"]),
    ("Find the distance between (0, 0) and (0, -7).", "7 units", ["0 units", "14 units", "49 units"]),
    ("What is the reflection of (-4, 6) across the X-axis?", "(-4, -6)", ["(4, 6)", "(4, -6)", "(-6, 4)"]),
    ("What is the reflection of (-3, -5) across the Y-axis?", "(3, -5)", ["(-3, 5)", "(3, 5)", "(-5, -3)"]),
    ("Find the midpoint of (4, 2) and (8, 6).", "(6, 4)", ["(5, 4)", "(6, 5)", "(12, 8)"]),
    ("Find the distance between (1, 1) and (4, 5).", "5 units", ["3 units", "4 units", "6 units"]),
    ("Find the distance between (-1, -1) and (2, 3).", "5 units", ["4 units", "6 units", "7 units"]),
    ("Find the midpoint of (-4, -2) and (2, 6).", "(-1, 2)", ["(1, 2)", "(-2, 4)", "(-1, 4)"]),
    ("What is the X-coordinate of the midpoint of (2, 6) and (8, 4)?", "5", ["4", "6", "10"]),
    ("What is the Y-coordinate of the midpoint of (3, 5) and (7, 9)?", "7", ["5", "6", "9"]),
    ("A point is 4 units right and 3 units down from the origin. What are its coordinates?", "(4, -3)", ["(-4, 3)", "(4, 3)", "(-4, -3)"]),
    ("Find the distance between (3, 0) and (0, 4).", "5 units", ["4 units", "6 units", "7 units"]),
    ("Which point is equidistant from (0, 0) and (4, 0) on the X-axis?", "(2, 0)", ["(1, 0)", "(3, 0)", "(4, 0)"]),
    ("Find the midpoint of (1, -3) and (5, 7).", "(3, 2)", ["(2, 2)", "(3, 4)", "(6, 4)"]),
]


HARD = [
    ("Find the distance between (2, 3) and (8, 11).", "10 units", ["8 units", "12 units", "14 units"]),
    ("Find the distance between (-3, 4) and (5, -2).", "10 units", ["8 units", "12 units", "14 units"]),
    ("Find the midpoint of (-5, 7) and (3, -1).", "(-1, 3)", ["(1, 3)", "(-1, 4)", "(-2, 3)"]),
    ("Find the midpoint of (6, -4) and (-2, 8).", "(2, 2)", ["(4, 2)", "(2, 4)", "(2, -2)"]),
    ("Find the area of the triangle with vertices (0, 0), (4, 0), and (0, 3).", "6 square units", ["7 square units", "12 square units", "9 square units"]),
    ("Find the area of the triangle with vertices (0, 0), (6, 0), and (0, 5).", "15 square units", ["11 square units", "30 square units", "20 square units"]),
    ("Find the centroid of a triangle with vertices (0, 0), (6, 0), and (0, 6).", "(2, 2)", ["(3, 3)", "(2, 3)", "(6, 6)"]),
    ("Find the centroid of a triangle with vertices (3, 0), (0, 3), and (0, 0).", "(1, 1)", ["(2, 1)", "(1, 2)", "(3, 3)"]),
    ("Find the distance between (1, 2) and (7, 10).", "10 units", ["8 units", "12 units", "14 units"]),
    ("Find the distance between (-4, -3) and (2, 5).", "10 units", ["6 units", "8 units", "12 units"]),
    ("Find the midpoint of (-6, 4) and (8, -2).", "(1, 1)", ["(2, 1)", "(1, 2)", "(7, 2)"]),
    ("Find the midpoint of (−3, −5) and (7, 9).", "(2, 2)", ["(4, 2)", "(2, 4)", "(5, 2)"]),
    ("If the distance between (0, 0) and (x, 0) is 9 units, what is the positive value of x?", "9", ["3", "18", "81"]),
    ("If the midpoint of (2, 4) and (x, 8) is (5, 6), find x.", "8", ["6", "10", "12"]),
    ("If the midpoint of (4, y) and (8, 6) is (6, 5), find y.", "4", ["2", "6", "8"]),
    ("Find the area of the triangle with vertices (1, 1), (5, 1), and (1, 4).", "6 square units", ["8 square units", "12 square units", "4 square units"]),
    ("Find the area of the triangle with vertices (2, 2), (8, 2), and (2, 6).", "12 square units", ["10 square units", "24 square units", "18 square units"]),
    ("Find the centroid of a triangle with vertices (3, 3), (6, 3), and (3, 6).", "(4, 4)", ["(3, 4)", "(4, 3)", "(5, 5)"]),
    ("What is the distance between (−2, 1) and (4, 9)?", "10 units", ["8 units", "12 units", "14 units"]),
    ("Find the distance between (−1, 2) and (5, 10).", "10 units", ["6 units", "8 units", "12 units"]),
    ("Find the midpoint of (−8, 6) and (4, −2).", "(−2, 2)", ["(2, 2)", "(−2, 4)", "(−4, 2)"]),
    ("Find the area of the triangle with vertices (0, 0), (8, 0), and (0, 4).", "16 square units", ["12 square units", "24 square units", "32 square units"]),
    ("Find the centroid of a triangle with vertices (0, 0), (9, 0), and (0, 9).", "(3, 3)", ["(4, 4)", "(3, 4)", "(9, 9)"]),
    ("If the midpoint of (−2, 4) and (6, y) is (2, 5), find y.", "6", ["4", "5", "8"]),
    ("If the midpoint of (x, 2) and (4, 6) is (3, 4), find x.", "2", ["1", "4", "6"]),
    ("Find the area of the triangle with vertices (1, 2), (7, 2), and (1, 8).", "18 square units", ["12 square units", "24 square units", "36 square units"]),
    ("Find the distance between (−5, −5) and (1, 3).", "10 units", ["8 units", "12 units", "14 units"]),
    ("Find the midpoint of (−4, −6) and (10, 8).", "(3, 1)", ["(2, 1)", "(3, 2)", "(6, 2)"]),
    ("Find the centroid of a triangle with vertices (2, 1), (8, 1), and (2, 7).", "(4, 3)", ["(3, 4)", "(5, 3)", "(4, 4)"]),
    ("Find the area of the triangle with vertices (2, 1), (8, 1), and (2, 5).", "12 square units", ["10 square units", "20 square units", "24 square units"]),
]


def make_questions(data):
    questions = []

    for item in data:
        question = str(item[0])
        answer = str(item[1])
        wrong_answers = [str(x) for x in item[2]]

        options = [answer] + wrong_answers

        if len(options) != 4 or len(set(options)) != 4:
            raise ValueError(
                f"Invalid or duplicate options: {question} | {options}"
            )

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

    try:
        cursor.execute(
            "SELECT id FROM lessons WHERE title = ? AND topic = ?",
            (TOPIC, SUBJECT)
        )

        lesson = cursor.fetchone()

        if not lesson:
            print(f"Lesson not found: {TOPIC}")
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
                    f"{difficulty} must contain exactly 30 questions. "
                    f"Found {len(data)}."
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
                    (
                        quiz_id,
                        question,
                        option_a,
                        option_b,
                        option_c,
                        option_d,
                        correct_answer
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (quiz_id, *question))

                inserted += 1

            total_inserted += inserted

            print(
                f"{difficulty}: {inserted} new questions inserted."
            )

        conn.commit()

        print("\nCoordinate Geometry seeding completed!")
        print(f"Total new questions inserted: {total_inserted}")

        for difficulty in difficulty_data:
            cursor.execute("""
                SELECT COUNT(*)
                FROM questions
                WHERE quiz_id IN (
                    SELECT id FROM quizzes
                    WHERE lesson_id = ?
                    AND LOWER(difficulty) = LOWER(?)
                )
            """, (lesson_id, difficulty))

            count = cursor.fetchone()[0]
            print(f"{difficulty} total questions in database: {count}")

    except Exception as e:
        conn.rollback()
        print(f"\nError: {e}")
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    main()
