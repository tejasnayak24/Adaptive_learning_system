
import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

TOPIC = "Percentages"
SUBJECT = "Mathematics"

random.seed(42)

EASY = [
    ("Find 10% of 100.", 10),
    ("Find 20% of 200.", 40),
    ("Find 50% of 80.", 40),
    ("Find 25% of 100.", 25),
    ("Find 10% of 500.", 50),
    ("Find 5% of 200.", 10),
    ("Find 50% of 150.", 75),
    ("Find 20% of 50.", 10),
    ("Find 25% of 200.", 50),
    ("Find 10% of 90.", 9),
    ("Find 30% of 100.", 30),
    ("Find 40% of 50.", 20),
    ("Find 75% of 100.", 75),
    ("Find 50% of 300.", 150),
    ("Find 15% of 200.", 30),
    ("Find 5% of 100.", 5),
    ("Find 20% of 150.", 30),
    ("Find 25% of 80.", 20),
    ("Find 10% of 250.", 25),
    ("Find 60% of 100.", 60),
    ("Convert 1/2 into a percentage.", 50),
    ("Convert 1/4 into a percentage.", 25),
    ("Convert 3/4 into a percentage.", 75),
    ("Convert 1/5 into a percentage.", 20),
    ("Convert 1/10 into a percentage.", 10),
    ("Convert 0.5 into a percentage.", 50),
    ("Convert 0.25 into a percentage.", 25),
    ("Convert 0.75 into a percentage.", 75),
    ("Convert 0.2 into a percentage.", 20),
    ("Convert 0.1 into a percentage.", 10)
]

MEDIUM = [
    ("Find 15% of 400.", 60),
    ("Find 35% of 200.", 70),
    ("Find 12% of 500.", 60),
    ("Find 45% of 300.", 135),
    ("Find 18% of 250.", 45),
    ("Find 65% of 400.", 260),
    ("Find 32% of 250.", 80),
    ("Find 8% of 750.", 60),
    ("Find 22% of 500.", 110),
    ("Find 16% of 600.", 96),
    ("A shirt costs Rs. 800. Find its price after a 10% discount.", 720),
    ("A book costs Rs. 500. Find its price after a 20% discount.", 400),
    ("A student scores 80 out of 100. Find the percentage.", 80),
    ("A student scores 45 out of 60. Find the percentage.", 75),
    ("Find 125% of 80.", 100),
    ("Find 150% of 200.", 300),
    ("Increase 100 by 20%.", 120),
    ("Increase 250 by 10%.", 275),
    ("Decrease 200 by 25%.", 150),
    ("Decrease 400 by 15%.", 340),
    ("What percentage of 200 is 50?", 25),
    ("What percentage of 500 is 100?", 20),
    ("What percentage of 80 is 20?", 25),
    ("What percentage of 300 is 90?", 30),
    ("A price of Rs. 600 increases by 10%. Find the new price.", 660),
    ("A population of 1000 decreases by 5%. Find the new population.", 950),
    ("Convert 3/5 into a percentage.", 60),
    ("Convert 7/10 into a percentage.", 70),
    ("Convert 0.35 into a percentage.", 35),
    ("Convert 1.25 into a percentage.", 125)
]

HARD = [
    ("A number is increased by 20% and becomes 240. Find the original number.", 200),
    ("A number is decreased by 25% and becomes 300. Find the original number.", 400),
    ("The price of an item increases from Rs. 400 to Rs. 500. Find the percentage increase.", 25),
    ("The price decreases from Rs. 800 to Rs. 600. Find the percentage decrease.", 25),
    ("A student scores 360 marks out of 450. Find the percentage.", 80),
    ("A student scores 420 marks out of 600. Find the percentage.", 70),
    ("The population of a town is 5000. It increases by 10%. Find the new population.", 5500),
    ("A population of 8000 decreases by 15%. Find the new population.", 6800),
    ("An item costing Rs. 1200 is sold at a 15% discount. Find the selling price.", 1020),
    ("An item costing Rs. 2000 is sold at a 12% discount. Find the selling price.", 1760),
    ("A salary of Rs. 25000 is increased by 12%. Find the new salary.", 28000),
    ("A salary of Rs. 40000 is reduced by 10%. Find the new salary.", 36000),
    ("A number is 40% of 500. Find the number.", 200),
    ("If 35% of a number is 140, find the number.", 400),
    ("If 60% of a number is 180, find the number.", 300),
    ("If 75% of a number is 225, find the number.", 300),
    ("An article is sold for Rs. 900 after a 10% discount. Find its marked price.", 1000),
    ("An article is sold for Rs. 680 after a 15% discount. Find its marked price.", 800),
    ("A number increases from 200 to 260. Find the percentage increase.", 30),
    ("A number decreases from 500 to 350. Find the percentage decrease.", 30),
    ("A student gets 72% marks in an exam of 500 marks. Find the marks obtained.", 360),
    ("A person spends 65% of Rs. 20000. Find the amount saved.", 7000),
    ("A shopkeeper gives two successive discounts of 10% and 20% on Rs. 1000. Find the final price.", 720),
    ("The price of an item increases by 10% and then decreases by 10%. Find the final price if the original price was Rs. 1000.", 990),
    ("In a class of 80 students, 55% are girls. Find the number of boys.", 36),
    ("A candidate gets 48% of 500 votes. Find the number of votes received.", 240),
    ("A number is increased by 25% and then by 20%. Find the overall percentage increase.", 50),
    ("A number is decreased by 20% and then by 25%. Find the overall percentage decrease.", 40),
    ("The cost of an item rises from Rs. 250 to Rs. 300. Find the percentage increase.", 20),
    ("A student needs 40% marks to pass an exam of 600 marks. If the student scores 210, how many more marks are needed to pass?", 30)
]


def make_questions(data):
    questions = []

    for question, answer in data:
        wrong_options = [
            answer + 1,
            answer - 1,
            answer + 2
        ]

        options = [answer] + wrong_options
        random.shuffle(options)

        correct_answer = ["A", "B", "C", "D"][options.index(answer)]

        questions.append((
            question,
            str(options[0]),
            str(options[1]),
            str(options[2]),
            str(options[3]),
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
                    quiz_id, question,
                    option_a, option_b,
                    option_c, option_d,
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
