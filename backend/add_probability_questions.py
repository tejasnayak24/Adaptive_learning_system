
import sqlite3
import random
from pathlib import Path

random.seed(42)

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

TOPIC = "Probability"
SUBJECT = "Mathematics"


def make_questions(data):
    questions = []

    for question, answer, wrong_answers in data:
        options = [str(answer)] + [str(x) for x in wrong_answers]

        if len(options) != 4 or len(set(options)) != 4:
            raise ValueError(
                f"Invalid or duplicate options: {question} | {options}"
            )

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


EASY = [
    ("What is the probability of getting a head when a fair coin is tossed?",
     "1/2", ["1/4", "1/3", "1"]),

    ("What is the probability of getting a tail when a fair coin is tossed?",
     "1/2", ["1/4", "1/3", "0"]),

    ("What is the probability of getting a 3 when a fair six-sided die is rolled?",
     "1/6", ["1/3", "1/2", "1/4"]),

    ("What is the probability of getting an even number on a fair die?",
     "1/2", ["1/6", "1/3", "2/3"]),

    ("What is the probability of getting an odd number on a fair die?",
     "1/2", ["1/6", "1/3", "1/4"]),

    ("What is the probability of getting a number greater than 4 on a fair die?",
     "1/3", ["1/2", "1/6", "2/3"]),

    ("What is the probability of getting a number less than 3 on a fair die?",
     "1/3", ["1/2", "1/6", "2/3"]),

    ("A bag contains 3 red balls and 2 blue balls. What is the probability of picking a red ball?",
     "3/5", ["2/5", "1/5", "1/2"]),

    ("A bag contains 4 green balls and 6 yellow balls. What is the probability of picking a yellow ball?",
     "3/5", ["2/5", "1/5", "1/2"]),

    ("A box contains 5 white balls and 5 black balls. What is the probability of picking a white ball?",
     "1/2", ["1/5", "1/4", "2/5"]),

    ("What is the probability of getting a number 7 when a standard six-sided die is rolled?",
     "0", ["1/6", "1/2", "1"]),

    ("What is the probability of getting a number from 1 to 6 on a standard die?",
     "1", ["0", "1/2", "1/6"]),

    ("A card is drawn from cards numbered 1 to 10. What is the probability of drawing 5?",
     "1/10", ["1/5", "1/2", "1/4"]),

    ("A card is drawn from cards numbered 1 to 8. What is the probability of drawing an even number?",
     "1/2", ["1/4", "1/8", "3/4"]),

    ("A card is drawn from cards numbered 1 to 10. What is the probability of drawing a number greater than 7?",
     "3/10", ["7/10", "1/10", "1/2"]),

    ("A spinner has 4 equal sections numbered 1, 2, 3 and 4. What is the probability of landing on 2?",
     "1/4", ["1/2", "1/3", "1/5"]),

    ("A spinner has 5 equal sections, one of which is red. What is the probability of landing on red?",
     "1/5", ["1/2", "1/4", "1/3"]),

    ("What is the probability of an impossible event?",
     "0", ["1", "1/2", "1/4"]),

    ("What is the probability of a certain event?",
     "1", ["0", "1/2", "1/4"]),

    ("If an event has 2 favourable outcomes out of 5 equally likely outcomes, what is its probability?",
     "2/5", ["3/5", "1/5", "1/2"]),

    ("A bag contains 2 red, 3 blue and 5 green balls. What is the probability of picking a blue ball?",
     "3/10", ["2/10", "5/10", "1/2"]),

    ("A bag contains 7 red balls and 3 blue balls. What is the probability of not picking a red ball?",
     "3/10", ["7/10", "1/10", "1/2"]),

    ("What is the probability of getting heads twice when a fair coin is tossed twice?",
     "1/4", ["1/2", "3/4", "1/8"]),

    ("What is the probability of getting at least one head when a fair coin is tossed once?",
     "1/2", ["1/4", "1", "0"]),

    ("A die is rolled. What is the probability of getting a number divisible by 3?",
     "1/3", ["1/2", "1/6", "2/3"]),

    ("A die is rolled. What is the probability of getting a number less than 5?",
     "2/3", ["1/3", "1/2", "5/6"]),

    ("A card is drawn from cards numbered 1 to 5. What is the probability of drawing 1 or 2?",
     "2/5", ["1/5", "3/5", "1/2"]),

    ("A bag contains 8 red balls and 2 green balls. What is the probability of picking a green ball?",
     "1/5", ["4/5", "1/2", "2/5"]),

    ("What is the probability of getting a number greater than 2 on a fair six-sided die?",
     "2/3", ["1/3", "1/2", "5/6"]),

    ("A coin is tossed once. How many possible outcomes are there?",
     "2", ["1", "3", "4"])
]


MEDIUM = [
    ("Two fair coins are tossed. What is the probability of getting exactly one head?",
     "1/2", ["1/4", "3/4", "1/3"]),

    ("Two fair coins are tossed. What is the probability of getting two tails?",
     "1/4", ["1/2", "3/4", "1/3"]),

    ("Two fair coins are tossed. What is the probability of getting at least one head?",
     "3/4", ["1/4", "1/2", "1/3"]),

    ("Two fair dice are rolled. What is the probability that their sum is 7?",
     "1/6", ["1/12", "1/3", "1/4"]),

    ("Two fair dice are rolled. What is the probability that their sum is 2?",
     "1/36", ["1/6", "1/12", "1/18"]),

    ("Two fair dice are rolled. What is the probability that their sum is 12?",
     "1/36", ["1/6", "1/12", "1/18"]),

    ("Two fair dice are rolled. What is the probability that their sum is 8?",
     "5/36", ["1/6", "1/9", "1/4"]),

    ("Two fair dice are rolled. What is the probability of getting the same number on both dice?",
     "1/6", ["1/3", "1/12", "1/36"]),

    ("Two fair dice are rolled. What is the probability that both show even numbers?",
     "1/4", ["1/2", "1/3", "1/6"]),

    ("A card is drawn from a standard deck of 52 cards. What is the probability of drawing an ace?",
     "1/13", ["1/4", "1/52", "4/13"]),

    ("A card is drawn from a standard deck of 52 cards. What is the probability of drawing a heart?",
     "1/4", ["1/13", "1/2", "1/3"]),

    ("A card is drawn from a standard deck of 52 cards. What is the probability of drawing a king?",
     "1/13", ["1/4", "1/52", "4/13"]),

    ("A card is drawn from a standard deck of 52 cards. What is the probability of drawing a red card?",
     "1/2", ["1/4", "1/13", "3/4"]),

    ("A bag contains 4 red and 6 blue balls. Two balls are drawn without replacement. What is the probability that both are red?",
     "2/15", ["4/15", "1/5", "1/3"]),

    ("A bag contains 3 red and 7 blue balls. Two balls are drawn without replacement. What is the probability that both are blue?",
     "7/15", ["1/2", "2/5", "3/10"]),

    ("A bag contains 5 red and 5 blue balls. Two balls are drawn without replacement. What is the probability that the first is red and the second is blue?",
     "5/18", ["1/4", "1/2", "5/36"]),

    ("A bag contains 2 red, 3 blue and 5 green balls. What is the probability of not picking a green ball?",
     "1/2", ["1/5", "3/10", "2/5"]),

    ("A number is selected randomly from 1 to 20. What is the probability that it is a multiple of 5?",
     "1/5", ["1/4", "1/2", "1/10"]),

    ("A number is selected randomly from 1 to 30. What is the probability that it is a prime number?",
     "1/3", ["1/2", "1/5", "2/3"]),

    ("A number is selected randomly from 1 to 12. What is the probability that it is a factor of 12?",
     "1/3", ["1/2", "1/4", "1/6"]),

    ("A spinner has 8 equal sections numbered 1 to 8. What is the probability of landing on a prime number?",
     "1/2", ["1/4", "3/8", "5/8"]),

    ("A fair coin is tossed three times. What is the probability of getting three heads?",
     "1/8", ["1/4", "3/8", "1/2"]),

    ("A fair coin is tossed three times. What is the probability of getting exactly two heads?",
     "3/8", ["1/8", "1/4", "1/2"]),

    ("A fair coin is tossed three times. What is the probability of getting no heads?",
     "1/8", ["1/4", "3/8", "1/2"]),

    ("A die is rolled twice. What is the probability of getting a 6 on both rolls?",
     "1/36", ["1/6", "1/12", "1/18"]),

    ("A die is rolled twice. What is the probability of getting an even number on both rolls?",
     "1/4", ["1/2", "1/3", "1/6"]),

    ("A card is drawn from cards numbered 1 to 15. What is the probability of selecting a multiple of 3?",
     "1/3", ["1/5", "1/2", "2/3"]),

    ("A bag contains 6 white and 4 black balls. One ball is drawn. What is the probability that it is white?",
     "3/5", ["2/5", "1/2", "4/5"]),

    ("Two fair dice are rolled. What is the probability that the sum is less than 4?",
     "1/12", ["1/6", "1/9", "1/18"]),

    ("Two fair dice are rolled. What is the probability that the sum is greater than 10?",
     "1/12", ["1/6", "1/9", "1/18"])
]


HARD = [
    ("A bag contains 4 red and 6 blue balls. Two balls are drawn without replacement. What is the probability that both are blue?",
     "1/3", ["2/5", "1/2", "1/5"]),

    ("A bag contains 4 red and 6 blue balls. Two balls are drawn without replacement. What is the probability of getting one red and one blue in any order?",
     "8/15", ["2/5", "1/3", "1/2"]),

    ("A bag contains 5 red and 3 blue balls. Two balls are drawn without replacement. What is the probability that both are red?",
     "5/14", ["1/2", "3/14", "5/8"]),

    ("A bag contains 3 white and 2 black balls. Two balls are drawn without replacement. What is the probability that both are white?",
     "3/10", ["1/2", "1/5", "2/5"]),

    ("A bag contains 3 white and 2 black balls. Two balls are drawn without replacement. What is the probability of getting one ball of each colour?",
     "3/5", ["2/5", "1/2", "1/5"]),

    ("Two fair dice are rolled. What is the probability that their sum is a prime number?",
     "5/12", ["1/2", "1/3", "7/12"]),

    ("Two fair dice are rolled. What is the probability that their sum is an even number?",
     "1/2", ["1/3", "1/4", "2/3"]),

    ("Two fair dice are rolled. What is the probability that their product is even?",
     "3/4", ["1/2", "1/4", "2/3"]),

    ("Two fair dice are rolled. What is the probability that at least one die shows a 6?",
     "11/36", ["1/6", "1/3", "5/36"]),

    ("Two fair dice are rolled. What is the probability that neither die shows a 6?",
     "25/36", ["5/6", "1/2", "11/36"]),

    ("A fair coin is tossed four times. What is the probability of getting exactly two heads?",
     "3/8", ["1/4", "1/2", "5/8"]),

    ("A fair coin is tossed four times. What is the probability of getting at least one head?",
     "15/16", ["1/16", "7/8", "3/4"]),

    ("A fair coin is tossed four times. What is the probability of getting exactly three tails?",
     "1/4", ["1/8", "3/8", "1/2"]),

    ("A card is drawn from a standard deck of 52 cards. What is the probability of drawing a face card?",
     "3/13", ["1/13", "1/4", "4/13"]),

    ("A card is drawn from a standard deck of 52 cards. What is the probability of drawing a black king?",
     "1/26", ["1/13", "1/52", "1/4"]),

    ("Two cards are drawn from a standard deck without replacement. What is the probability that both are aces?",
     "1/221", ["1/169", "1/52", "1/26"]),

    ("Two cards are drawn from a standard deck without replacement. What is the probability that both are red?",
     "25/102", ["1/4", "1/2", "13/51"]),

    ("A number is selected randomly from 1 to 50. What is the probability that it is divisible by both 2 and 3?",
     "4/25", ["1/5", "3/25", "1/6"]),

    ("A number is selected randomly from 1 to 100. What is the probability that it is divisible by 4 or 5?",
     "2/5", ["1/2", "1/5", "3/5"]),

    ("A number is selected randomly from 1 to 40. What is the probability that it is a perfect square?",
     "3/20", ["1/5", "1/10", "1/4"]),

    ("A box contains 5 defective and 15 good bulbs. One bulb is selected. What is the probability that it is good?",
     "3/4", ["1/4", "1/2", "2/5"]),

    ("A box contains 5 defective and 15 good bulbs. Two bulbs are selected without replacement. What is the probability that both are good?",
     "21/38", ["3/4", "9/20", "7/19"]),

    ("A box contains 5 defective and 15 good bulbs. Two bulbs are selected without replacement. What is the probability that both are defective?",
     "1/19", ["1/20", "1/10", "1/4"]),

    ("A class has 12 boys and 8 girls. One student is selected randomly. What is the probability of selecting a girl?",
     "2/5", ["3/5", "1/2", "1/5"]),

    ("A class has 12 boys and 8 girls. Two students are selected without replacement. What is the probability that both are girls?",
     "14/95", ["2/5", "4/25", "7/20"]),

    ("A fair die is rolled. Given that the result is even, what is the probability that it is 4?",
     "1/3", ["1/6", "1/2", "2/3"]),

    ("A card is drawn from cards numbered 1 to 20. Given that the number is even, what is the probability that it is divisible by 4?",
     "1/2", ["1/4", "1/5", "2/5"]),

    ("A bag contains 4 red and 6 blue balls. Two balls are drawn without replacement. Given that the first ball is red, what is the probability that the second is blue?",
     "2/3", ["3/5", "1/2", "1/3"]),

    ("A fair die is rolled. What is the probability of not getting a prime number?",
     "1/2", ["1/3", "1/6", "2/3"]),

    ("Two fair dice are rolled. What is the probability that the sum is 9 or 10?",
     "7/36", ["1/6", "5/36", "1/4"])
]


def seed_questions():
    conn = None
    total_inserted = 0

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM lessons WHERE title = ? AND topic = ?",
            (TOPIC, SUBJECT)
        )

        lesson = cursor.fetchone()

        if not lesson:
            print(f"Lesson '{TOPIC}' not found in the database.")
            return

        lesson_id = lesson[0]

        difficulty_data = {
            "Easy": EASY,
            "Medium": MEDIUM,
            "Hard": HARD
        }

        for difficulty, data in difficulty_data.items():

            if len(data) != 30:
                raise ValueError(
                    f"{difficulty} must contain exactly 30 questions. "
                    f"Found: {len(data)}"
                )

            cursor.execute("""
                SELECT id FROM quizzes
                WHERE lesson_id = ?
                AND LOWER(difficulty) = LOWER(?)
            """, (lesson_id, difficulty))

            quiz = cursor.fetchone()

            if not quiz:
                print(f"{difficulty} quiz not found. Skipping.")
                continue

            quiz_id = quiz[0]
            formatted_questions = make_questions(data)
            inserted = 0

            for item in formatted_questions:
                question = item[0]

                cursor.execute("""
                    SELECT 1 FROM questions
                    WHERE quiz_id = ? AND question = ?
                """, (quiz_id, question))

                if cursor.fetchone():
                    continue

                cursor.execute("""
                    INSERT INTO questions (
                        quiz_id,
                        question,
                        option_a,
                        option_b,
                        option_c,
                        option_d,
                        correct_answer
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (quiz_id, *item))

                inserted += 1

            total_inserted += inserted

            print(
                f"{difficulty}: {inserted} new questions inserted."
            )

        conn.commit()

        print("\nProbability seeding completed!")
        print(f"Total new questions inserted: {total_inserted}")

        for difficulty in ["Easy", "Medium", "Hard"]:
            cursor.execute("""
                SELECT COUNT(*)
                FROM questions q
                JOIN quizzes qz ON q.quiz_id = qz.id
                WHERE qz.lesson_id = ?
                AND LOWER(qz.difficulty) = LOWER(?)
            """, (lesson_id, difficulty))

            count = cursor.fetchone()[0]

            print(
                f"{difficulty} total questions in database: {count}"
            )

    except Exception as error:
        if conn:
            conn.rollback()

        print("Error while inserting questions:", error)

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    seed_questions()
