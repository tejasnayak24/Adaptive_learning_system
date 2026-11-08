
import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

TOPIC = "Simple Interest"
SUBJECT = "Mathematics"

random.seed(42)

EASY = [
    ("Find SI on Rs. 1000 at 10% for 1 year.", 100),
    ("Find SI on Rs. 2000 at 5% for 1 year.", 100),
    ("Find SI on Rs. 500 at 10% for 2 years.", 100),
    ("Find SI on Rs. 1000 at 5% for 2 years.", 100),
    ("Find SI on Rs. 2000 at 10% for 2 years.", 400),
    ("Find SI on Rs. 5000 at 10% for 1 year.", 500),
    ("Find SI on Rs. 3000 at 5% for 2 years.", 300),
    ("Find SI on Rs. 4000 at 10% for 1 year.", 400),
    ("Find SI on Rs. 1500 at 10% for 2 years.", 300),
    ("Find SI on Rs. 1000 at 8% for 1 year.", 80),
    ("Find SI on Rs. 2000 at 6% for 1 year.", 120),
    ("Find SI on Rs. 3000 at 4% for 2 years.", 240),
    ("Find SI on Rs. 500 at 8% for 2 years.", 80),
    ("Find SI on Rs. 2500 at 10% for 1 year.", 250),
    ("Find SI on Rs. 4000 at 5% for 2 years.", 400),
    ("Find the amount if principal is Rs. 1000 and SI is Rs. 100.", 1100),
    ("Find the amount if principal is Rs. 2000 and SI is Rs. 200.", 2200),
    ("Find the amount if principal is Rs. 500 and SI is Rs. 50.", 550),
    ("Find the amount if principal is Rs. 3000 and SI is Rs. 300.", 3300),
    ("Find the amount if principal is Rs. 1500 and SI is Rs. 150.", 1650),
    ("Find SI on Rs. 1000 at 2% for 3 years.", 60),
    ("Find SI on Rs. 5000 at 4% for 1 year.", 200),
    ("Find SI on Rs. 6000 at 5% for 1 year.", 300),
    ("Find SI on Rs. 800 at 10% for 1 year.", 80),
    ("Find SI on Rs. 1200 at 5% for 2 years.", 120),
    ("Find SI on Rs. 2500 at 4% for 2 years.", 200),
    ("Find SI on Rs. 4000 at 2% for 3 years.", 240),
    ("Find SI on Rs. 10000 at 5% for 1 year.", 500),
    ("Find SI on Rs. 700 at 10% for 2 years.", 140),
    ("Find SI on Rs. 3000 at 10% for 3 years.", 900)
]

MEDIUM = [
    ("Find SI on Rs. 5000 at 8% for 3 years.", 1200),
    ("Find SI on Rs. 4000 at 6% for 5 years.", 1200),
    ("Find SI on Rs. 6000 at 7% for 2 years.", 840),
    ("Find SI on Rs. 8000 at 5% for 3 years.", 1200),
    ("Find SI on Rs. 2500 at 12% for 2 years.", 600),
    ("Find SI on Rs. 7500 at 4% for 5 years.", 1500),
    ("Find SI on Rs. 9000 at 6% for 2 years.", 1080),
    ("Find SI on Rs. 12000 at 5% for 4 years.", 2400),
    ("Find SI on Rs. 3500 at 8% for 3 years.", 840),
    ("Find SI on Rs. 10000 at 7% for 2 years.", 1400),
    ("Find the principal if SI is Rs. 300, rate is 5% and time is 2 years.", 3000),
    ("Find the principal if SI is Rs. 600, rate is 10% and time is 3 years.", 2000),
    ("Find the principal if SI is Rs. 400, rate is 4% and time is 2 years.", 5000),
    ("Find the principal if SI is Rs. 900, rate is 6% and time is 3 years.", 5000),
    ("Find the principal if SI is Rs. 500, rate is 5% and time is 2 years.", 5000),
    ("Find the rate if SI is Rs. 200 on Rs. 1000 for 2 years.", 10),
    ("Find the rate if SI is Rs. 600 on Rs. 3000 for 2 years.", 10),
    ("Find the rate if SI is Rs. 400 on Rs. 2000 for 4 years.", 5),
    ("Find the rate if SI is Rs. 750 on Rs. 5000 for 3 years.", 5),
    ("Find the rate if SI is Rs. 300 on Rs. 2000 for 3 years.", 5),
    ("Find the time if SI is Rs. 400 on Rs. 2000 at 10%.", 2),
    ("Find the time if SI is Rs. 600 on Rs. 3000 at 10%.", 2),
    ("Find the time if SI is Rs. 500 on Rs. 5000 at 5%.", 2),
    ("Find the time if SI is Rs. 900 on Rs. 3000 at 10%.", 3),
    ("Find the time if SI is Rs. 240 on Rs. 2000 at 6%.", 2),
    ("Find the amount on Rs. 5000 at 8% for 2 years.", 5800),
    ("Find the amount on Rs. 4000 at 5% for 3 years.", 4600),
    ("Find the amount on Rs. 6000 at 10% for 2 years.", 7200),
    ("Find the amount on Rs. 8000 at 4% for 5 years.", 9600),
    ("Find the amount on Rs. 2500 at 12% for 2 years.", 3100)
]

HARD = [
    ("A sum amounts to Rs. 6600 in 2 years at 10% SI. Find the principal.", 5500),
    ("A sum amounts to Rs. 7200 in 2 years at 10% SI. Find the principal.", 6000),
    ("A sum amounts to Rs. 5750 in 3 years at 5% SI. Find the principal.", 5000),
    ("A sum amounts to Rs. 8400 in 4 years at 5% SI. Find the principal.", 7000),
    ("A sum amounts to Rs. 9600 in 2 years at 10% SI. Find the principal.", 8000),
    ("At what rate will Rs. 4000 earn Rs. 800 SI in 4 years?", 5),
    ("At what rate will Rs. 5000 earn Rs. 1500 SI in 5 years?", 6),
    ("At what rate will Rs. 6000 earn Rs. 900 SI in 3 years?", 5),
    ("At what rate will Rs. 8000 earn Rs. 1600 SI in 4 years?", 5),
    ("At what rate will Rs. 3000 earn Rs. 900 SI in 5 years?", 6),
    ("In how many years will Rs. 5000 earn Rs. 1000 at 5% SI?", 4),
    ("In how many years will Rs. 4000 earn Rs. 1200 at 10% SI?", 3),
    ("In how many years will Rs. 6000 earn Rs. 1800 at 5% SI?", 6),
    ("In how many years will Rs. 8000 earn Rs. 2400 at 10% SI?", 3),
    ("In how many years will Rs. 2000 earn Rs. 600 at 5% SI?", 6),
    ("A sum doubles itself in 10 years at SI. Find the rate.", 10),
    ("A sum triples itself in 20 years at SI. Find the rate.", 10),
    ("A sum becomes double in 8 years at SI. Find the rate.", 12.5),
    ("A sum becomes three times in 15 years at SI. Find the rate.", 13.33),
    ("A sum becomes double in 5 years at SI. Find the rate.", 20),
    ("Find the difference between SI on Rs. 5000 at 8% for 2 years and 5% for 2 years.", 300),
    ("Find SI on Rs. 8000 at 6% for 9 months.", 360),
    ("Find SI on Rs. 12000 at 5% for 6 months.", 300),
    ("Find SI on Rs. 6000 at 10% for 18 months.", 900),
    ("Find SI on Rs. 4000 at 12% for 9 months.", 360),
    ("A sum of Rs. 10000 earns Rs. 2400 SI in 4 years. Find the rate.", 6),
    ("A sum of Rs. 7500 earns Rs. 1800 SI in 3 years. Find the rate.", 8),
    ("A sum earns Rs. 1200 SI at 5% in 4 years. Find the principal.", 6000),
    ("A sum earns Rs. 1500 SI at 10% in 3 years. Find the principal.", 5000),
    ("A sum of Rs. 8000 becomes Rs. 9200 in 3 years. Find the annual rate.", 5)
]


def make_questions(data):
    questions = []

    for question, answer in data:
        wrong_options = [
            round(answer + 1, 2),
            round(answer - 1, 2),
            round(answer + 2, 2)
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
