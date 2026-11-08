
import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

TOPIC = "Lines and Angles"
SUBJECT = "Mathematics"

random.seed(42)

# Format: (question, correct answer, [three wrong answers])

EASY = [
    ("How many degrees are there in a right angle?", "90°", ["45°", "180°", "360°"]),
    ("How many degrees are there in a straight angle?", "180°", ["90°", "270°", "360°"]),
    ("What is the measure of a complete angle?", "360°", ["180°", "90°", "270°"]),
    ("An angle less than 90° is called what?", "Acute angle", ["Obtuse angle", "Right angle", "Straight angle"]),
    ("An angle greater than 90° but less than 180° is called what?", "Obtuse angle", ["Acute angle", "Right angle", "Reflex angle"]),
    ("An angle measuring exactly 90° is called what?", "Right angle", ["Acute angle", "Obtuse angle", "Straight angle"]),
    ("An angle measuring 180° is called what?", "Straight angle", ["Right angle", "Reflex angle", "Acute angle"]),
    ("What is the sum of angles on a straight line?", "180°", ["90°", "270°", "360°"]),
    ("What is the sum of angles around a point?", "360°", ["180°", "90°", "270°"]),
    ("What is the complement of 30°?", "60°", ["30°", "150°", "90°"]),
    ("What is the complement of 45°?", "45°", ["90°", "135°", "55°"]),
    ("What is the supplement of 60°?", "120°", ["30°", "60°", "90°"]),
    ("What is the supplement of 100°?", "80°", ["100°", "90°", "180°"]),
    ("Two angles whose sum is 90° are called what?", "Complementary angles", ["Supplementary angles", "Adjacent angles", "Vertically opposite angles"]),
    ("Two angles whose sum is 180° are called what?", "Supplementary angles", ["Complementary angles", "Acute angles", "Reflex angles"]),
    ("What are angles opposite each other when two lines intersect called?", "Vertically opposite angles", ["Adjacent angles", "Complementary angles", "Corresponding angles"]),
    ("What is the measure of vertically opposite angles if one is 70°?", "70°", ["110°", "90°", "120°"]),
    ("How many endpoints does a line segment have?", "2", ["0", "1", "3"]),
    ("How many endpoints does a ray have?", "1", ["0", "2", "3"]),
    ("How many endpoints does a line have?", "0", ["1", "2", "3"]),
    ("Lines that never meet are called what?", "Parallel lines", ["Intersecting lines", "Perpendicular lines", "Curved lines"]),
    ("Lines meeting at 90° are called what?", "Perpendicular lines", ["Parallel lines", "Intersecting lines", "Curved lines"]),
    ("What is the measure of an angle equal to half a right angle?", "45°", ["30°", "60°", "90°"]),
    ("What is the measure of an angle equal to twice a right angle?", "180°", ["90°", "120°", "360°"]),
    ("What is the reflex angle of 90°?", "270°", ["180°", "90°", "360°"]),
    ("Which instrument is used to measure angles?", "Protractor", ["Ruler", "Compass", "Divider"]),
    ("What is the angle between perpendicular lines?", "90°", ["45°", "180°", "360°"]),
    ("If one angle is 40°, what is its complementary angle?", "50°", ["40°", "140°", "60°"]),
    ("If one angle is 125°, what is its supplementary angle?", "55°", ["65°", "125°", "45°"]),
    ("How many degrees are there in a full rotation?", "360°", ["90°", "180°", "270°"]),
]

MEDIUM = [
    ("Two angles on a straight line are 65° and x°. Find x.", "115°", ["105°", "125°", "95°"]),
    ("Two complementary angles are 35° and x°. Find x.", "55°", ["45°", "65°", "145°"]),
    ("Two supplementary angles are 110° and x°. Find x.", "70°", ["60°", "80°", "110°"]),
    ("If one of two vertically opposite angles is 85°, find the other.", "85°", ["95°", "180°", "90°"]),
    ("Two adjacent angles on a straight line are (x + 20)° and 100°. Find x.", "60°", ["50°", "70°", "80°"]),
    ("Two complementary angles are (x + 10)° and 40°. Find x.", "40°", ["30°", "50°", "60°"]),
    ("Two supplementary angles are (2x)° and 60°. Find x.", "60°", ["30°", "90°", "120°"]),
    ("If an angle is 3 times its complement, find the angle.", "67.5°", ["60°", "45°", "75°"]),
    ("If an angle is twice its supplement, find the angle.", "120°", ["60°", "90°", "150°"]),
    ("Two angles are in the ratio 2:3 and are complementary. Find the smaller angle.", "36°", ["30°", "45°", "54°"]),
    ("Two angles are in the ratio 1:2 and are supplementary. Find the smaller angle.", "60°", ["45°", "90°", "120°"]),
    ("If two vertically opposite angles are (3x + 10)° and 100°, find x.", "30", ["20", "40", "50"]),
    ("If two adjacent angles on a straight line are (2x + 10)° and 70°, find x.", "50", ["40", "60", "70"]),
    ("Two angles around a point are 90°, 120° and x°. Find x.", "150°", ["140°", "160°", "180°"]),
    ("Three angles around a point are 100°, 80° and x°. Find x.", "180°", ["160°", "170°", "200°"]),
    ("If an angle is 25°, find its reflex angle.", "335°", ["315°", "325°", "345°"]),
    ("If an angle is 140°, find its reflex angle.", "220°", ["200°", "240°", "260°"]),
    ("Two complementary angles are in the ratio 4:5. Find the larger angle.", "50°", ["40°", "45°", "60°"]),
    ("Two supplementary angles are in the ratio 4:5. Find the smaller angle.", "80°", ["90°", "100°", "70°"]),
    ("If one angle is 15° more than its complement, find the angle.", "52.5°", ["45°", "60°", "37.5°"]),
    ("If one angle is 20° less than its supplement, find the angle.", "80°", ["70°", "90°", "100°"]),
    ("Two lines intersect. If one angle is 115°, find an adjacent angle.", "65°", ["115°", "75°", "55°"]),
    ("Two lines intersect. If one angle is 40°, find the vertically opposite angle.", "40°", ["140°", "90°", "180°"]),
    ("A pair of corresponding angles are formed by parallel lines. If one is 75°, find the other.", "75°", ["105°", "90°", "115°"]),
    ("A pair of alternate interior angles are formed by parallel lines. If one is 110°, find the other.", "110°", ["70°", "90°", "180°"]),
    ("A pair of co-interior angles are formed by parallel lines. If one is 120°, find the other.", "60°", ["120°", "90°", "80°"]),
    ("If two parallel lines are cut by a transversal, what is the sum of co-interior angles?", "180°", ["90°", "360°", "270°"]),
    ("If two corresponding angles are (2x + 10)° and 90°, find x.", "40", ["30", "50", "60"]),
    ("If alternate interior angles are (3x)° and 120°, find x.", "40", ["30", "50", "60"]),
    ("If co-interior angles are 2x° and 60°, find x.", "60", ["30", "45", "90"]),
]

HARD = [
    ("Two angles are in the ratio 3:5 and are supplementary. Find the larger angle.", "112.5°", ["67.5°", "100°", "120°"]),
    ("Two angles are in the ratio 2:7 and are complementary. Find the larger angle.", "70°", ["20°", "60°", "80°"]),
    ("An angle is 4 times its complement. Find the angle.", "72°", ["60°", "75°", "80°"]),
    ("An angle is 5 times its supplement. Find the angle.", "150°", ["120°", "135°", "160°"]),
    ("Two supplementary angles differ by 40°. Find the larger angle.", "110°", ["100°", "120°", "70°"]),
    ("Two complementary angles differ by 18°. Find the larger angle.", "54°", ["36°", "45°", "60°"]),
    ("Two angles on a straight line are (3x + 10)° and (2x + 20)°. Find x.", "30", ["20", "40", "50"]),
    ("Vertically opposite angles are (4x - 10)° and (2x + 30)°. Find x.", "20", ["10", "30", "40"]),
    ("Two adjacent angles on a straight line are (3x - 5)° and (2x + 10)°. Find x.", "35", ["25", "30", "40"]),
    ("Three angles around a point are x°, 2x° and 3x°. Find x.", "60°", ["30°", "45°", "90°"]),
    ("Four angles around a point are x°, 2x°, 3x° and 4x°. Find the largest angle.", "144°", ["90°", "120°", "160°"]),
    ("Two supplementary angles are in the ratio 7:11. Find the smaller angle.", "70°", ["80°", "110°", "90°"]),
    ("Two complementary angles are in the ratio 7:8. Find the smaller angle.", "42°", ["40°", "48°", "54°"]),
    ("An angle is 30° more than its complement. Find the angle.", "60°", ["45°", "75°", "90°"]),
    ("An angle is 50° less than its supplement. Find the angle.", "65°", ["55°", "75°", "85°"]),
    ("Two parallel lines are cut by a transversal. If one corresponding angle is 3x° and the other is 120°, find x.", "40", ["30", "50", "60"]),
    ("Two alternate interior angles are (2x + 20)° and 100°. Find x.", "40", ["30", "50", "60"]),
    ("Two co-interior angles are (3x + 10)° and 80°. Find x.", "30", ["20", "40", "50"]),
    ("One angle of a linear pair is 4 times the other. Find the smaller angle.", "36°", ["45°", "30°", "40°"]),
    ("One angle of a linear pair is 5 times the other. Find the larger angle.", "150°", ["120°", "135°", "160°"]),
    ("Two intersecting lines form an angle of 65°. Find the sum of the other three angles.", "295°", ["180°", "245°", "315°"]),
    ("If one angle formed by two intersecting lines is 3x° and its adjacent angle is 2x°, find x.", "36", ["30", "40", "45"]),
    ("Three angles around a point are (x + 20)°, (2x + 10)° and 90°. Find x.", "80", ["60", "70", "90"]),
    ("Four angles around a point are 2x°, 3x°, 4x° and x°. Find the smallest angle.", "36°", ["18°", "45°", "72°"]),
    ("Two parallel lines are cut by a transversal. If one co-interior angle is 3 times the other, find the larger angle.", "135°", ["90°", "120°", "150°"]),
    ("Two angles are supplementary. One is 24° greater than the other. Find the smaller angle.", "78°", ["68°", "82°", "90°"]),
    ("Two complementary angles are such that the larger is twice the smaller. Find the larger angle.", "60°", ["30°", "45°", "75°"]),
    ("An angle is 3 times its adjacent angle on a straight line. Find the larger angle.", "135°", ["90°", "120°", "150°"]),
    ("Two vertically opposite angles are (5x - 15)° and (3x + 25)°. Find the value of x.", "20", ["15", "25", "30"]),
    ("Two co-interior angles are (4x + 20)° and (2x + 40)°. Find the larger angle.", "100°", ["80°", "120°", "140°"]),
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
