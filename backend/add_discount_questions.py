
import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

TOPIC = "Discount"
SUBJECT = "Mathematics"

random.seed(42)

EASY = [
    ("Find 10% discount on Rs. 100.", 10),
    ("Find 20% discount on Rs. 200.", 40),
    ("Find 50% discount on Rs. 500.", 250),
    ("Find 25% discount on Rs. 400.", 100),
    ("Find 10% discount on Rs. 800.", 80),
    ("Find 5% discount on Rs. 200.", 10),
    ("Find 15% discount on Rs. 200.", 30),
    ("Find 20% discount on Rs. 500.", 100),
    ("Find 30% discount on Rs. 300.", 90),
    ("Find 40% discount on Rs. 100.", 40),
    ("Marked price is Rs. 500 and discount is Rs. 50. Find selling price.", 450),
    ("Marked price is Rs. 800 and discount is Rs. 100. Find selling price.", 700),
    ("Marked price is Rs. 1000 and discount is Rs. 200. Find selling price.", 800),
    ("Marked price is Rs. 600 and discount is Rs. 60. Find selling price.", 540),
    ("Marked price is Rs. 400 and discount is Rs. 100. Find selling price.", 300),
    ("Find the discount percentage if MP = Rs. 100 and discount = Rs. 10.", 10),
    ("Find the discount percentage if MP = Rs. 200 and discount = Rs. 40.", 20),
    ("Find the discount percentage if MP = Rs. 500 and discount = Rs. 100.", 20),
    ("Find the discount percentage if MP = Rs. 400 and discount = Rs. 80.", 20),
    ("Find the discount percentage if MP = Rs. 1000 and discount = Rs. 250.", 25),
    ("An item marked at Rs. 200 is sold at 10% discount. Find SP.", 180),
    ("An item marked at Rs. 500 is sold at 20% discount. Find SP.", 400),
    ("An item marked at Rs. 800 is sold at 25% discount. Find SP.", 600),
    ("An item marked at Rs. 600 is sold at 50% discount. Find SP.", 300),
    ("An item marked at Rs. 1000 is sold at 10% discount. Find SP.", 900),
    ("Find the marked price if SP = Rs. 90 after a 10% discount.", 100),
    ("Find the marked price if SP = Rs. 160 after a 20% discount.", 200),
    ("Find the marked price if SP = Rs. 300 after a 25% discount.", 400),
    ("Find the marked price if SP = Rs. 450 after a 10% discount.", 500),
    ("Find the marked price if SP = Rs. 600 after a 40% discount.", 1000)
]

MEDIUM = [
    ("A shirt marked at Rs. 1200 is sold at 15% discount. Find SP.", 1020),
    ("A bag marked at Rs. 2000 is sold at 20% discount. Find SP.", 1600),
    ("A watch marked at Rs. 1500 is sold at 10% discount. Find SP.", 1350),
    ("A book marked at Rs. 800 is sold at 25% discount. Find SP.", 600),
    ("A phone marked at Rs. 5000 is sold at 12% discount. Find SP.", 4400),
    ("Find the discount amount on an item marked at Rs. 2400 with 15% discount.", 360),
    ("Find the discount amount on Rs. 1600 at 12.5% discount.", 200),
    ("Find the discount amount on Rs. 3000 at 20% discount.", 600),
    ("Find the discount amount on Rs. 800 at 15% discount.", 120),
    ("Find the discount amount on Rs. 2500 at 8% discount.", 200),
    ("An item is sold for Rs. 720 after a 10% discount. Find MP.", 800),
    ("An item is sold for Rs. 680 after a 15% discount. Find MP.", 800),
    ("An item is sold for Rs. 900 after a 25% discount. Find MP.", 1200),
    ("An item is sold for Rs. 850 after a 15% discount. Find MP.", 1000),
    ("An item is sold for Rs. 1440 after a 20% discount. Find MP.", 1800),
    ("An article marked at Rs. 2500 is sold for Rs. 2000. Find discount percentage.", 20),
    ("An article marked at Rs. 1200 is sold for Rs. 900. Find discount percentage.", 25),
    ("An article marked at Rs. 800 is sold for Rs. 720. Find discount percentage.", 10),
    ("An article marked at Rs. 1500 is sold for Rs. 1200. Find discount percentage.", 20),
    ("An article marked at Rs. 2000 is sold for Rs. 1700. Find discount percentage.", 15),
    ("A shop offers 10% discount on Rs. 1000. Find the amount paid.", 900),
    ("A shop offers 30% discount on Rs. 1500. Find the amount paid.", 1050),
    ("A dress marked at Rs. 2400 is sold at 25% discount. Find the amount paid.", 1800),
    ("A table marked at Rs. 4000 is sold at 15% discount. Find the amount paid.", 3400),
    ("A laptop marked at Rs. 50000 is sold at 10% discount. Find the amount paid.", 45000),
    ("An item gets successive discounts of 10% and 10% on Rs. 1000. Find final price.", 810),
    ("An item marked at Rs. 2000 gets a discount of 10% followed by 20%. Find final price.", 1440),
    ("Find the single equivalent discount for successive discounts of 10% and 20%.", 28),
    ("Find the single equivalent discount for successive discounts of 20% and 25%.", 40),
    ("Find the single equivalent discount for successive discounts of 10% and 30%.", 37)
]

HARD = [
    ("An item marked at Rs. 4000 is sold after successive discounts of 10% and 20%. Find SP.", 2880),
    ("An article marked at Rs. 5000 receives successive discounts of 20% and 10%. Find SP.", 3600),
    ("A product marked at Rs. 8000 receives discounts of 25% and 20%. Find SP.", 4800),
    ("A watch marked at Rs. 6000 receives successive discounts of 10% and 15%. Find SP.", 4590),
    ("A product marked at Rs. 10000 receives discounts of 30% and 10%. Find SP.", 6300),
    ("Find the equivalent single discount for successive discounts of 15% and 20%.", 32),
    ("Find the equivalent single discount for successive discounts of 25% and 10%.", 32.5),
    ("Find the equivalent single discount for successive discounts of 20% and 30%.", 44),
    ("Find the equivalent single discount for successive discounts of 10% and 40%.", 46),
    ("Find the equivalent single discount for successive discounts of 30% and 20%.", 44),
    ("An article is sold for Rs. 1530 after a 15% discount. Find its marked price.", 1800),
    ("An article is sold for Rs. 2040 after a 15% discount. Find its marked price.", 2400),
    ("An article is sold for Rs. 2550 after a 15% discount. Find its marked price.", 3000),
    ("An item is sold for Rs. 1680 after a 30% discount. Find its marked price.", 2400),
    ("An item is sold for Rs. 2250 after a 25% discount. Find its marked price.", 3000),
    ("A shopkeeper gives 20% discount on Rs. 2500. Find the discount amount.", 500),
    ("A shopkeeper gives 12.5% discount on Rs. 4000. Find the discount amount.", 500),
    ("A product marked at Rs. 3600 is sold for Rs. 3060. Find discount percentage.", 15),
    ("A product marked at Rs. 5000 is sold for Rs. 4250. Find discount percentage.", 15),
    ("An item marked at Rs. 8000 is sold for Rs. 6000. Find discount percentage.", 25),
    ("An article is sold for Rs. 1800 after a 10% discount. Find the amount of discount.", 200),
    ("An item marked at Rs. 6000 is sold after successive discounts of 15% and 10%. Find total discount.", 1410),
    ("An item marked at Rs. 4000 receives successive discounts of 20% and 15%. Find total discount.", 1280),
    ("A shop offers 10% discount followed by 5% discount on Rs. 2000. Find final price.", 1710),
    ("An item marked at Rs. 5000 is sold for Rs. 3600 after two successive discounts. If the first discount is 10%, find the second discount percentage.", 20),
    ("A shopkeeper offers a 20% discount and then another 10% discount. Find the total discount percentage.", 28),
    ("A product marked at Rs. 2500 is sold after a 12% discount. Find the selling price.", 2200),
    ("An article marked at Rs. 4000 is sold at a discount of 17.5%. Find SP.", 3300),
    ("A product marked at Rs. 12000 is sold after successive discounts of 25% and 10%. Find SP.", 8100),
    ("An item marked at Rs. 7500 is sold after successive discounts of 20% and 20%. Find SP.", 4800)
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
