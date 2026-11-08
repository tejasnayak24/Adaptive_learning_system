
import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

TOPIC = "Ratio and Proportion"
SUBJECT = "Mathematics"

random.seed(42)

EASY = [
    ("Simplify the ratio 4:8",  "1:2"),
    ("Simplify the ratio 6:9",  "2:3"),
    ("Simplify the ratio 10:15", "2:3"),
    ("Simplify the ratio 12:16", "3:4"),
    ("Simplify the ratio 15:20", "3:4"),
    ("Simplify the ratio 18:24", "3:4"),
    ("Simplify the ratio 5:10", "1:2"),
    ("Simplify the ratio 21:28", "3:4"),
    ("Simplify the ratio 8:12", "2:3"),
    ("Simplify the ratio 14:21", "2:3"),
    ("Find the equivalent ratio of 2:3 when multiplied by 2", "4:6"),
    ("Find the equivalent ratio of 3:4 when multiplied by 3", "9:12"),
    ("Find the equivalent ratio of 5:6 when multiplied by 2", "10:12"),
    ("Find the equivalent ratio of 4:7 when multiplied by 2", "8:14"),
    ("Find the equivalent ratio of 2:5 when multiplied by 4", "8:20"),
    ("If there are 2 boys and 3 girls, what is the ratio of boys to girls?", "2:3"),
    ("If there are 5 red balls and 10 blue balls, find the ratio of red to blue balls.", "1:2"),
    ("Divide 20 in the ratio 1:1. What is the first share?", "10"),
    ("Divide 30 in the ratio 1:2. What is the first share?", "10"),
    ("Divide 40 in the ratio 1:3. What is the second share?", "30"),
    ("If 2 pens cost Rs. 10, what is the cost of 1 pen?", "5"),
    ("If 3 notebooks cost Rs. 30, what is the cost of 1 notebook?", "10"),
    ("Find the missing number: 2:4 = 3:?", "6"),
    ("Find the missing number: 3:6 = 4:?", "8"),
    ("Find the missing number: 5:10 = 7:?", "14"),
    ("Are the ratios 2:4 and 3:6 equivalent? Enter 1 for Yes.", "1"),
    ("Are the ratios 2:5 and 4:10 equivalent? Enter 1 for Yes.", "1"),
    ("Simplify the ratio 20:25", "4:5"),
    ("Simplify the ratio 9:12", "3:4"),
    ("Simplify the ratio 16:20", "4:5")
]

MEDIUM = [
    ("Divide 60 in the ratio 2:3. Find the first share.", "24"),
    ("Divide 80 in the ratio 3:5. Find the second share.", "50"),
    ("Divide 100 in the ratio 2:3. Find the first share.", "40"),
    ("Divide 120 in the ratio 5:7. Find the first share.", "50"),
    ("Divide 90 in the ratio 4:5. Find the second share.", "50"),
    ("Divide 150 in the ratio 2:3. Find the first share.", "60"),
    ("Divide 200 in the ratio 3:7. Find the second share.", "140"),
    ("Divide 72 in the ratio 5:4. Find the first share.", "40"),
    ("Divide 96 in the ratio 3:5. Find the second share.", "60"),
    ("Divide 180 in the ratio 4:5. Find the first share.", "80"),
    ("If 5 pens cost Rs. 40, find the cost of 8 pens.", "64"),
    ("If 4 books cost Rs. 100, find the cost of 6 books.", "150"),
    ("If 6 workers complete a task in 10 days, how many days will 12 workers take?", "5"),
    ("If 3 kg of rice costs Rs. 150, find the cost of 5 kg.", "250"),
    ("If 8 metres of cloth cost Rs. 400, find the cost of 12 metres.", "600"),
    ("Find x: 4:5 = x:20", "16"),
    ("Find x: 3:7 = 12:x", "28"),
    ("Find x: 5:8 = 15:x", "24"),
    ("Find x: 6:9 = x:15", "10"),
    ("Find x: 2:3 = 10:x", "15"),
    ("The ratio of boys to girls is 3:2. If there are 30 boys, how many girls are there?", "20"),
    ("The ratio of red to blue balls is 4:5. If there are 20 red balls, how many blue balls are there?", "25"),
    ("The ratio of ages of A and B is 2:3. If A is 12 years old, find B's age.", "18"),
    ("The ratio of two numbers is 5:6. If the first number is 25, find the second.", "30"),
    ("The ratio of sugar to flour is 1:4. If sugar is 5 kg, find the flour required.", "20"),
    ("Simplify the ratio 45:60", "3:4"),
    ("Simplify the ratio 72:90", "4:5"),
    ("Simplify the ratio 84:126", "2:3"),
    ("Find the fourth proportional to 2, 4 and 6.", "12"),
    ("Find the fourth proportional to 3, 5 and 9.", "15")
]

HARD = [
    ("Divide 360 in the ratio 2:3:4. Find the largest share.", "160"),
    ("Divide 420 in the ratio 3:4:5. Find the smallest share.", "105"),
    ("Divide 600 in the ratio 2:3:5. Find the second share.", "180"),
    ("Divide 720 in the ratio 4:5:7. Find the largest share.", "315"),
    ("Divide 540 in the ratio 3:5:7. Find the first share.", "108"),
    ("The ratio of A:B is 3:4 and B:C is 2:5. Find A:C.", "3:10"),
    ("The ratio of A:B is 2:3 and B:C is 4:5. Find A:C.", "8:15"),
    ("The ratio of boys to girls is 5:4. If the total is 81, find the number of boys.", "45"),
    ("The ratio of two numbers is 7:9. Their sum is 128. Find the smaller number.", "56"),
    ("The ratio of two numbers is 4:7. Their difference is 30. Find the smaller number.", "40"),
    ("The present ages of A and B are in the ratio 3:5. If their total age is 64, find A's age.", "24"),
    ("The ages of two people are in the ratio 4:7. If their age difference is 15, find the younger age.", "20"),
    ("A sum of Rs. 840 is divided among three people in the ratio 2:3:7. Find the largest share.", "490"),
    ("If 15 workers complete a job in 12 days, how many days will 20 workers take?", "9"),
    ("If 8 machines produce 400 items in a day, how many items will 12 machines produce?", "600"),
    ("A car travels 180 km in 3 hours. How far will it travel in 5 hours at the same speed?", "300"),
    ("If 12 men finish a job in 15 days, how many men are needed to finish it in 9 days?", "20"),
    ("If 5 taps fill a tank in 12 hours, how long will 10 similar taps take?", "6"),
    ("Find the third proportional to 4 and 8.", "16"),
    ("Find the fourth proportional to 4, 6 and 8.", "12"),
    ("If x:y = 5:7 and y:z = 14:9, find x:z.", "10:9"),
    ("The ratio of milk to water is 5:2. If the mixture contains 35 litres, find the quantity of milk.", "25"),
    ("A mixture contains milk and water in the ratio 7:3. If there are 60 litres of mixture, find the water quantity.", "18"),
    ("The ratio of income to expenditure is 5:4. If income is Rs. 25,000, find savings.", "5000"),
    ("Two numbers are in the ratio 8:11. If their sum is 171, find the larger number.", "99"),
    ("The ratio of two numbers is 9:5. If their difference is 32, find their sum.", "112"),
    ("A map scale is 1:100000. If the map distance is 5 cm, find the actual distance in km.", "5"),
    ("If 18 workers build a wall in 20 days, how many days will 24 workers take?", "15"),
    ("The ratio of the sides of a rectangle is 3:5. If its perimeter is 64 cm, find its longer side.", "20"),
    ("A and B share Rs. 900 in the ratio 7:8. Find B's share.", "480")
]


def make_questions(data):
    questions = []

    for question, answer in data:
        if ":" in answer:
            a, b = map(int, answer.split(":"))
            wrong_options = [
                f"{a + 1}:{b}",
                f"{a}:{b + 1}",
                f"{a + 2}:{b + 1}"
            ]
        else:
            value = int(answer)
            wrong_options = [
                str(value + 1),
                str(value - 1),
                str(value + 2)
            ]

        options = [answer] + wrong_options
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
        print(f"{difficulty}: {inserted} questions inserted.")

    conn.commit()
    conn.close()

    print(f"\nCompleted! Total new questions inserted: {total_inserted}")


if __name__ == "__main__":
    main()
