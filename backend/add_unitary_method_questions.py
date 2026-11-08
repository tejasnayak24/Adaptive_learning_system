
import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

# Exact title stored in your database
TOPIC = "Unitary Method"
SUBJECT = "Mathematics"

random.seed(42)

EASY = [
    ("If 2 pens cost Rs. 10, find the cost of 1 pen.", 5),
    ("If 3 books cost Rs. 30, find the cost of 1 book.", 10),
    ("If 4 pencils cost Rs. 20, find the cost of 6 pencils.", 30),
    ("If 5 chocolates cost Rs. 25, find the cost of 1 chocolate.", 5),
    ("If 2 kg of rice costs Rs. 100, find the cost of 1 kg.", 50),
    ("If 3 notebooks cost Rs. 45, find the cost of 5 notebooks.", 75),
    ("If 4 oranges cost Rs. 40, find the cost of 8 oranges.", 80),
    ("If 6 bananas cost Rs. 30, find the cost of 1 banana.", 5),
    ("If 5 metres of cloth cost Rs. 100, find the cost of 1 metre.", 20),
    ("If 2 toys cost Rs. 80, find the cost of 3 toys.", 120),
    ("If 4 pens cost Rs. 60, find the cost of 8 pens.", 120),
    ("If 10 eggs cost Rs. 60, find the cost of 5 eggs.", 30),
    ("If 3 kg of apples cost Rs. 150, find the cost of 2 kg.", 100),
    ("If 5 litres of milk cost Rs. 250, find the cost of 1 litre.", 50),
    ("If 2 shirts cost Rs. 800, find the cost of 1 shirt.", 400),
    ("If 4 workers earn Rs. 2000, find the earning of 1 worker.", 500),
    ("If 6 packets cost Rs. 90, find the cost of 4 packets.", 60),
    ("If 8 pencils cost Rs. 40, find the cost of 12 pencils.", 60),
    ("If 3 chairs cost Rs. 900, find the cost of 5 chairs.", 1500),
    ("If 5 kg of sugar costs Rs. 250, find the cost of 3 kg.", 150),
    ("If 2 metres of ribbon cost Rs. 30, find the cost of 6 metres.", 90),
    ("If 4 tickets cost Rs. 200, find the cost of 7 tickets.", 350),
    ("If 3 bottles cost Rs. 75, find the cost of 4 bottles.", 100),
    ("If 10 pens cost Rs. 100, find the cost of 7 pens.", 70),
    ("If 5 toys cost Rs. 500, find the cost of 2 toys.", 200),
    ("If 2 kg of potatoes cost Rs. 40, find the cost of 5 kg.", 100),
    ("If 6 books cost Rs. 300, find the cost of 2 books.", 100),
    ("If 4 cups cost Rs. 120, find the cost of 3 cups.", 90),
    ("If 3 metres of wire cost Rs. 60, find the cost of 9 metres.", 180),
    ("If 8 mangoes cost Rs. 160, find the cost of 5 mangoes.", 100)
]

MEDIUM = [
    ("If 8 workers complete a job in 12 days, how many days will 16 workers take?", 6),
    ("If 5 machines produce 100 items, how many items will 8 machines produce?", 160),
    ("If 12 men earn Rs. 6000, how much will 8 men earn?", 4000),
    ("If 6 taps fill a tank in 10 hours, how long will 3 taps take?", 20),
    ("If 15 workers complete a task in 8 days, how many days will 10 workers take?", 12),
    ("If 4 kg of rice costs Rs. 240, find the cost of 7 kg.", 420),
    ("If 9 books cost Rs. 450, find the cost of 14 books.", 700),
    ("If 12 metres of cloth cost Rs. 720, find the cost of 5 metres.", 300),
    ("If 6 workers earn Rs. 9000, find the earning of 10 workers.", 15000),
    ("If 20 people consume food in 15 days, how many days will it last for 10 people?", 30),
    ("If 8 pumps empty a tank in 6 hours, how long will 4 pumps take?", 12),
    ("If 10 workers finish a job in 18 days, how many workers are needed to finish it in 9 days?", 20),
    ("If 5 machines make 250 products in a day, how many will 12 machines make?", 600),
    ("If 16 men complete a job in 15 days, how many days will 20 men take?", 12),
    ("If 7 kg of apples cost Rs. 350, find the cost of 11 kg.", 550),
    ("If 3 litres of paint cover 45 square metres, how much area will 8 litres cover?", 120),
    ("If 6 pencils cost Rs. 42, find the cost of 15 pencils.", 105),
    ("If 12 workers build a wall in 20 days, how many workers are needed in 15 days?", 16),
    ("If 4 cars use 40 litres of fuel, how much fuel will 7 similar cars use?", 70),
    ("If 18 people complete a task in 10 days, how many days will 15 people take?", 12),
    ("If 5 packets contain 60 biscuits, how many biscuits are in 9 packets?", 108),
    ("If 8 metres of fabric cost Rs. 560, find the cost of 13 metres.", 910),
    ("If 24 workers complete a job in 5 days, how many workers are needed in 10 days?", 12),
    ("If 6 taps fill a tank in 8 hours, how long will 12 taps take?", 4),
    ("If 15 books cost Rs. 1200, find the cost of 8 books.", 640),
    ("If 9 machines produce 450 items, how many items will 4 machines produce?", 200),
    ("If 25 workers finish a task in 12 days, how many days will 15 workers take?", 20),
    ("If 4 kg of sugar costs Rs. 180, find the cost of 10 kg.", 450),
    ("If 7 people consume 21 kg of rice, how much rice will 12 people consume?", 36),
    ("If 14 workers earn Rs. 9800, find the earning of 9 workers.", 6300)
]

HARD = [
    ("If 18 workers complete a project in 24 days, how many days will 27 workers take?", 16),
    ("If 24 machines produce 1200 items in 5 hours, how many items will 36 machines produce in 5 hours?", 1800),
    ("If 15 men can complete a job in 20 days, how many men are required to complete it in 12 days?", 25),
    ("If 20 workers complete a task in 15 days working 8 hours daily, how many days will 30 workers take working 10 hours daily?", 8),
    ("If 12 pumps fill a tank in 15 hours, how long will 20 pumps take?", 9),
    ("If 16 workers build 80 metres of road in 10 days, how many metres will 24 workers build in 15 days?", 180),
    ("If 25 workers earn Rs. 75000 in 30 days, how much will 40 workers earn in 20 days?", 80000),
    ("If 18 machines produce 5400 items in 6 days, how many items will 25 machines produce in 8 days?", 10000),
    ("If 30 people consume 450 kg of food in 15 days, how much food will 20 people consume in 12 days?", 240),
    ("If 24 men finish a job in 18 days, how many days will 36 men take to finish the same job?", 12),
    ("If 8 taps fill a tank in 12 hours, how long will 6 taps take?", 16),
    ("If 15 workers complete 60 units in 8 days, how many units will 20 workers complete in 12 days?", 120),
    ("If 12 machines produce 720 items in 6 hours, how many items will 15 machines produce in 8 hours?", 1200),
    ("If 40 workers complete a project in 25 days, how many workers are needed to complete it in 20 days?", 50),
    ("If 16 men complete a job in 30 days working 6 hours daily, how many days will 24 men take working 8 hours daily?", 15),
    ("If 5 vehicles carry 200 tonnes of goods, how many tonnes can 12 vehicles carry?", 480),
    ("If 18 workers earn Rs. 54000 in 15 days, how much will 25 workers earn in 12 days?", 60000),
    ("If 20 machines produce 8000 items in 10 days, how many items will 15 machines produce in 12 days?", 7200),
    ("If 36 workers complete a task in 20 days, how many workers are required to finish it in 15 days?", 48),
    ("If 12 printers print 3600 pages in 5 hours, how many pages will 20 printers print in 8 hours?", 9600),
    ("If 25 men build 100 metres of wall in 12 days, how many metres will 30 men build in 15 days?", 150),
    ("If 16 workers complete a job in 24 days, how many days will 32 workers take?", 12),
    ("If 10 pumps empty a reservoir in 18 hours, how many pumps are required to empty it in 6 hours?", 30),
    ("If 24 people consume 360 kg of food in 10 days, how much food will 40 people consume in 15 days?", 900),
    ("If 15 machines manufacture 3000 products in 4 days, how many products will 25 machines manufacture in 6 days?", 7500),
    ("If 45 workers complete a job in 16 days, how many days will 30 workers take?", 24),
    ("If 8 workers working 6 hours daily complete a job in 15 days, how many days will 12 workers take working 10 hours daily?", 6),
    ("If 20 cows consume 600 kg of fodder in 15 days, how much fodder will 30 cows consume in 12 days?", 720),
    ("If 14 workers complete 70 units in 10 days, how many units will 21 workers complete in 15 days?", 157.5),
    ("If 18 machines produce 2700 items in 5 days, how many days will 30 machines take to produce 5400 items?", 6)
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
