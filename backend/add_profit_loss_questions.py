
import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

TOPIC = "Profit and Loss"
SUBJECT = "Mathematics"

random.seed(42)

EASY = [
    ("An item is bought for Rs. 100 and sold for Rs. 120. Find the profit.", 20),
    ("An item is bought for Rs. 200 and sold for Rs. 180. Find the loss.", 20),
    ("CP = Rs. 500 and SP = Rs. 600. Find the profit.", 100),
    ("CP = Rs. 300 and SP = Rs. 250. Find the loss.", 50),
    ("An item bought for Rs. 50 is sold for Rs. 70. Find the profit.", 20),
    ("An item bought for Rs. 400 is sold for Rs. 350. Find the loss.", 50),
    ("Find the profit percentage if CP = Rs. 100 and profit = Rs. 20.", 20),
    ("Find the loss percentage if CP = Rs. 200 and loss = Rs. 40.", 20),
    ("CP = Rs. 500 and profit = Rs. 50. Find SP.", 550),
    ("CP = Rs. 800 and loss = Rs. 100. Find SP.", 700),
    ("SP = Rs. 150 and profit = Rs. 30. Find CP.", 120),
    ("SP = Rs. 400 and loss = Rs. 50. Find CP.", 450),
    ("An article costs Rs. 250 and is sold for Rs. 300. Find profit percentage.", 20),
    ("An article costs Rs. 400 and is sold for Rs. 360. Find loss percentage.", 10),
    ("An item is bought for Rs. 1000 and sold for Rs. 1100. Find profit percentage.", 10),
    ("An item is bought for Rs. 500 and sold for Rs. 450. Find loss percentage.", 10),
    ("Find 10% profit on a cost price of Rs. 200.", 20),
    ("Find 20% loss on a cost price of Rs. 300.", 60),
    ("An item costing Rs. 600 is sold at 10% profit. Find SP.", 660),
    ("An item costing Rs. 800 is sold at 10% loss. Find SP.", 720),
    ("An item is sold for Rs. 240 at a profit of Rs. 40. Find CP.", 200),
    ("An item is sold for Rs. 180 at a loss of Rs. 20. Find CP.", 200),
    ("A shopkeeper buys a bag for Rs. 400 and sells it for Rs. 500. Find profit percentage.", 25),
    ("A toy bought for Rs. 250 is sold for Rs. 200. Find loss percentage.", 20),
    ("Find the selling price of an item costing Rs. 1000 at 5% profit.", 1050),
    ("Find the selling price of an item costing Rs. 600 at 5% loss.", 570),
    ("If CP = Rs. 100 and SP = Rs. 100, find the profit or loss.", 0),
    ("An article is bought for Rs. 750 and sold for Rs. 900. Find the profit.", 150),
    ("An article is bought for Rs. 900 and sold for Rs. 810. Find the loss.", 90),
    ("Find the profit percentage when CP = Rs. 400 and SP = Rs. 500.", 25)
]

MEDIUM = [
    ("An article is bought for Rs. 1200 and sold at 15% profit. Find SP.", 1380),
    ("An article costing Rs. 800 is sold at 12.5% loss. Find SP.", 700),
    ("A shopkeeper buys an item for Rs. 1500 and sells it for Rs. 1800. Find profit percentage.", 20),
    ("An item bought for Rs. 2000 is sold for Rs. 1700. Find loss percentage.", 15),
    ("An article is sold for Rs. 960 at 20% profit. Find CP.", 800),
    ("An article is sold for Rs. 850 at 15% loss. Find CP.", 1000),
    ("A trader earns Rs. 240 profit on an item costing Rs. 1200. Find profit percentage.", 20),
    ("A trader loses Rs. 150 on an item costing Rs. 750. Find loss percentage.", 20),
    ("Find SP if CP is Rs. 2500 and profit is 18%.", 2950),
    ("Find SP if CP is Rs. 1600 and loss is 25%.", 1200),
    ("An item is sold for Rs. 1440 at 20% profit. Find CP.", 1200),
    ("An item is sold for Rs. 680 at 15% loss. Find CP.", 800),
    ("A bicycle bought for Rs. 4000 is sold for Rs. 4600. Find profit percentage.", 15),
    ("A phone bought for Rs. 12000 is sold for Rs. 10800. Find loss percentage.", 10),
    ("A shopkeeper sells an item for Rs. 750 and gains 25%. Find CP.", 600),
    ("A shopkeeper sells an item for Rs. 900 and loses 10%. Find CP.", 1000),
    ("An article costs Rs. 2400. At what price should it be sold to gain 25%?", 3000),
    ("An article costs Rs. 1800. At what price should it be sold to lose 15%?", 1530),
    ("A trader buys 10 pens for Rs. 100 and sells each pen for Rs. 12. Find total profit.", 20),
    ("A shopkeeper buys 20 notebooks for Rs. 400 and sells each for Rs. 18. Find total loss.", 40),
    ("A man buys an article for Rs. 500 and spends Rs. 50 on repairs. He sells it for Rs. 660. Find profit.", 110),
    ("A chair costs Rs. 1000 and Rs. 100 is spent on transport. It is sold for Rs. 1320. Find profit percentage.", 20),
    ("An article is sold for Rs. 540 at a loss of 10%. Find CP.", 600),
    ("An article is sold for Rs. 1260 at a profit of 5%. Find CP.", 1200),
    ("A shopkeeper gains 30% by selling an item for Rs. 1300. Find CP.", 1000),
    ("A trader loses 20% by selling an item for Rs. 1600. Find CP.", 2000),
    ("An item costing Rs. 750 is sold at 16% profit. Find profit amount.", 120),
    ("An item costing Rs. 1250 is sold at 8% loss. Find loss amount.", 100),
    ("A trader buys an item for Rs. 2500 and sells it for Rs. 2875. Find profit percentage.", 15),
    ("A shopkeeper buys an article for Rs. 3600 and sells it for Rs. 3240. Find loss percentage.", 10)
]

HARD = [
    ("An article is sold at 20% profit for Rs. 1440. Find its cost price.", 1200),
    ("An article is sold at 25% loss for Rs. 1500. Find its cost price.", 2000),
    ("A trader sells two articles for Rs. 1200 each. On one he gains 20% and on the other he loses 20%. Find the total loss.", 80),
    ("A shopkeeper sells an article at 10% profit. If CP is Rs. 2500, find SP.", 2750),
    ("A trader buys an article for Rs. 4000 and spends Rs. 500 on repairs. He sells it at 10% profit. Find SP.", 4950),
    ("An article is sold for Rs. 1800 at 20% loss. At what price should it be sold to gain 20%?", 2700),
    ("A man sells an item for Rs. 960 and gains 20%. Find the selling price required for a 30% profit.", 1040),
    ("A trader sells an article for Rs. 720 at a loss of 10%. Find the selling price for a 20% profit.", 960),
    ("A shopkeeper buys 50 articles for Rs. 2000. He sells each for Rs. 50. Find total profit.", 500),
    ("A trader buys 40 items for Rs. 2400 and sells each for Rs. 55. Find total loss.", 200),
    ("An article is marked at Rs. 2000 and sold at 10% profit on its cost price of Rs. 1500. Find SP.", 1650),
    ("A trader buys an item for Rs. 800 and sells it at 15% profit. Find SP.", 920),
    ("A man sells an article at 10% loss. If he had sold it for Rs. 120 more, he would have gained 5%. Find CP.", 800),
    ("A trader sells an article at 20% profit. If the selling price were Rs. 100 less, the profit would be 10%. Find CP.", 1000),
    ("A shopkeeper buys 12 articles for Rs. 960 and sells 10 articles for Rs. 900. Find profit percentage.", 12.5),
    ("A trader buys 15 items for Rs. 1200 and sells 12 items for Rs. 1080. Find profit percentage.", 12.5),
    ("An article is sold at 25% profit. If its cost price increases by Rs. 100 and selling price remains Rs. 500, the profit becomes 0%. Find original CP.", 400),
    ("A trader sells an article for Rs. 1500 and gains 25%. Find the loss if it were sold for Rs. 1080.", 120),
    ("A shopkeeper sells an item for Rs. 920 at 15% profit. Find CP.", 800),
    ("An item is sold for Rs. 1530 at 15% loss. Find CP.", 1800),
    ("A trader buys goods for Rs. 5000 and spends Rs. 500 on transport. He sells them for Rs. 6600. Find profit percentage.", 20),
    ("A person buys 100 articles for Rs. 5000. He sells 80 articles for Rs. 60 each and the rest for Rs. 40 each. Find total profit.", 1200),
    ("A trader sells two items for Rs. 600 each. He gains 20% on one and loses 20% on the other. Find total loss.", 50),
    ("An article is sold at 10% profit. If both CP and SP increase by Rs. 100, the profit becomes 8%. Find original CP.", 400),
    ("A shopkeeper sells an article at 25% loss for Rs. 900. Find the selling price for a 20% profit.", 1440),
    ("A trader buys an article for Rs. 2400 and sells it at a 12.5% profit. Find SP.", 2700),
    ("A merchant sells goods at 20% profit. If he had bought them for 10% less and sold them for Rs. 50 less, his profit would be 30%. Find original CP.", 500),
    ("A trader buys an article for Rs. 1500. At what price should he sell it to gain 16%?", 1740),
    ("An article is sold for Rs. 1875 at a profit of 25%. Find the cost price.", 1500),
    ("A trader sells an item at 5% loss for Rs. 950. Find the selling price for a 10% profit.", 1100)
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
