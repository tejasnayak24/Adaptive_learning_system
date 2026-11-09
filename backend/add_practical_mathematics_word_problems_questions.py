
import sqlite3
import random
import re
from pathlib import Path

random.seed(42)

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

TOPIC = "Practical Mathematics and Word Problems"
SUBJECT = "Mathematics"


# ============================================================
# QUESTION CREATION WITH AUTOMATIC DUPLICATE CORRECTION
# ============================================================

def create_question(question, answer, wrong1, wrong2, wrong3):
    answer = str(answer)
    wrong_answers = [str(wrong1), str(wrong2), str(wrong3)]

    options = [answer]

    for wrong in wrong_answers:
        if wrong not in options:
            options.append(wrong)
            continue

        # Automatically generate a different numerical distractor.
        match = re.fullmatch(r"([^0-9-]*)(-?\d+(?:\.\d+)?)(.*)", answer)

        if match:
            prefix, number, suffix = match.groups()
            number = float(number)

            if number.is_integer():
                number = int(number)

            offset = 7
            while True:
                candidate = f"{prefix}{number + offset}{suffix}"

                if candidate not in options:
                    options.append(candidate)
                    break

                offset += 7
        else:
            index = 1
            while f"{wrong} (Option {index})" in options:
                index += 1

            options.append(f"{wrong} (Option {index})")

    return (question, answer, options[1:])


def make_questions(data):
    questions = []

    for question, answer, wrong_answers in data:
        options = [str(answer)] + [str(x) for x in wrong_answers]

        if len(options) != 4 or len(set(options)) != 4:
            raise ValueError(
                f"Invalid options: {question} | {options}"
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


# ============================================================
# EASY QUESTIONS - 30
# ============================================================

EASY = []

# Shopping calculations
for price, quantity in [
    (10, 3), (15, 4), (20, 5), (25, 2), (12, 6)
]:
    total = price * quantity

    EASY.append(create_question(
        f"A notebook costs Rs.{price}. What is the cost of {quantity} notebooks?",
        total,
        total + price,
        total - price,
        total + 20
    ))

# Change calculations
for paid, cost in [
    (100, 65), (200, 125), (500, 350),
    (100, 75), (200, 160)
]:
    change = paid - cost

    EASY.append(create_question(
        f"A customer pays Rs.{paid} for an item costing Rs.{cost}. How much change should be returned?",
        change,
        change + 10,
        change - 10,
        change + 20
    ))

# Distance calculations
for speed, hours in [
    (40, 2), (50, 3), (60, 2), (30, 4), (45, 2)
]:
    distance = speed * hours

    EASY.append(create_question(
        f"A vehicle travels at {speed} km/h for {hours} hours. How far does it travel?",
        f"{distance} km",
        f"{distance + 10} km",
        f"{distance - 10} km",
        f"{distance + 20} km"
    ))

# Time calculations
for start_hour, duration in [
    (9, 2), (10, 3), (13, 2), (14, 4), (8, 5)
]:
    total_hour = start_hour + duration

    answer_hour = total_hour % 12
    if answer_hour == 0:
        answer_hour = 12

    answer_period = "PM" if total_hour % 24 >= 12 else "AM"
    answer = f"{answer_hour}:00 {answer_period}"

    wrong1 = f"{answer_hour}:00 {'AM' if answer_period == 'PM' else 'PM'}"
    wrong2 = f"{(answer_hour % 12) + 1}:00 {answer_period}"
    wrong3 = f"{((answer_hour + 10) % 12) + 1}:00 {answer_period}"

    EASY.append(create_question(
        f"A journey starts at {start_hour}:00 and takes {duration} hours. When does it end?",
        answer,
        wrong1,
        wrong2,
        wrong3
    ))

# Percentage calculations
for value, percentage in [
    (100, 10), (200, 25), (400, 50), (300, 20), (500, 10)
]:
    result = value * percentage // 100

    EASY.append(create_question(
        f"What is {percentage}% of {value}?",
        result,
        result + 10,
        result - 10,
        result + 15
    ))

# Unit conversions
for km in [2, 3, 5, 7, 10]:
    EASY.append(create_question(
        f"Convert {km} kilometres into metres.",
        f"{km * 1000} metres",
        f"{km * 100} metres",
        f"{km * 10} metres",
        f"{km * 10000} metres"
    ))


# ============================================================
# MEDIUM QUESTIONS - 30
# ============================================================

MEDIUM = []

# Discount calculations
for price, discount in [
    (1000, 10), (800, 25), (1200, 20),
    (1500, 10), (2000, 15)
]:
    final_price = price - price * discount // 100

    MEDIUM.append(create_question(
        f"A product costs Rs.{price} and has a discount of {discount}%. What is its selling price after discount?",
        f"Rs.{final_price}",
        f"Rs.{price * discount // 100}",
        f"Rs.{price - 10}",
        f"Rs.{price + price * discount // 100}"
    ))

# Profit calculations
for cost, profit_percent in [
    (500, 20), (800, 25), (600, 10),
    (1000, 15), (400, 50)
]:
    selling = cost + cost * profit_percent // 100

    MEDIUM.append(create_question(
        f"An article costs Rs.{cost} and is sold at a profit of {profit_percent}%. Find its selling price.",
        f"Rs.{selling}",
        f"Rs.{cost - cost * profit_percent // 100}",
        f"Rs.{cost + profit_percent}",
        f"Rs.{selling + 100}"
    ))

# Simple interest
for principal, rate, years in [
    (1000, 5, 2), (2000, 10, 3), (1500, 4, 2),
    (3000, 5, 2), (2500, 8, 1)
]:
    interest = principal * rate * years // 100

    MEDIUM.append(create_question(
        f"Find the simple interest on Rs.{principal} at {rate}% per annum for {years} years.",
        f"Rs.{interest}",
        f"Rs.{interest + 50}",
        f"Rs.{interest - 50}",
        f"Rs.{principal + interest}"
    ))

# Average calculations
for numbers in [
    [10, 20, 30, 40],
    [15, 25, 35, 45],
    [12, 18, 24, 30],
    [20, 30, 40, 50],
    [5, 15, 25, 35]
]:
    average = sum(numbers) // len(numbers)

    MEDIUM.append(create_question(
        f"Find the average of {', '.join(map(str, numbers))}.",
        average,
        average + 5,
        average - 5,
        sum(numbers)
    ))

# Work and time
for workers, days in [
    (2, 12), (3, 15), (4, 20), (5, 10), (6, 18)
]:
    total_work = workers * days
    new_workers = workers * 2
    new_days = total_work // new_workers

    MEDIUM.append(create_question(
        f"If {workers} workers complete a job in {days} days, how many days will {new_workers} workers take at the same rate?",
        f"{new_days} days",
        f"{days} days",
        f"{new_days + 2} days",
        f"{total_work} days"
    ))

# Speed calculations
for distance, time in [
    (120, 2), (180, 3), (240, 4),
    (150, 5), (300, 6)
]:
    speed = distance // time

    MEDIUM.append(create_question(
        f"A car covers {distance} km in {time} hours. Find its average speed.",
        f"{speed} km/h",
        f"{speed + 10} km/h",
        f"{speed - 10} km/h",
        f"{speed + 20} km/h"
    ))


# ============================================================
# HARD QUESTIONS - 30
# ============================================================

HARD = []

# Successive discounts
for price, first, second in [
    (2000, 10, 20), (1500, 20, 10),
    (3000, 10, 10), (2500, 20, 20),
    (4000, 25, 10)
]:
    after_first = price * (100 - first) // 100
    final_price = after_first * (100 - second) // 100

    HARD.append(create_question(
        f"An item costs Rs.{price}. It receives successive discounts of {first}% and {second}%. Find the final price.",
        f"Rs.{final_price}",
        f"Rs.{price - price * (first + second) // 100}",
        f"Rs.{after_first}",
        f"Rs.{final_price + 100}"
    ))

# Profit and loss
for cost, selling in [
    (800, 1000), (1200, 1000), (1500, 1800),
    (2000, 1600), (500, 600)
]:
    difference = abs(selling - cost)
    percentage = difference * 100 // cost

    description = "profit" if selling > cost else "loss"

    HARD.append(create_question(
        f"An article is purchased for Rs.{cost} and sold for Rs.{selling}. What is the {description} percentage?",
        f"{percentage}%",
        f"{percentage + 5}%",
        f"{percentage + 10}%",
        f"{percentage + 15}%"
    ))

# Combined work
for a, b in [
    (10, 15), (12, 12), (8, 24), (6, 12), (9, 18)
]:
    combined = (a * b) // (a + b)

    HARD.append(create_question(
        f"A can complete a job in {a} days and B can complete it in {b} days. How many days will they take working together?",
        f"{combined} days",
        f"{a + b} days",
        f"{combined + 1} days",
        f"{max(a, b)} days"
    ))

# Ratio sharing
for total, first, second in [
    (120, 2, 4), (180, 2, 7), (240, 3, 5),
    (160, 3, 5), (200, 2, 3)
]:
    share = total * first // (first + second)

    HARD.append(create_question(
        f"Rs.{total} is divided between two people in the ratio {first}:{second}. How much does the first person receive?",
        f"Rs.{share}",
        f"Rs.{total - share}",
        f"Rs.{share + 10}",
        f"Rs.{share + 20}"
    ))

# Distance and time
for distance, speed in [
    (240, 60), (300, 50), (360, 60),
    (420, 70), (480, 80)
]:
    hours = distance // speed

    HARD.append(create_question(
        f"A vehicle travels {distance} km at an average speed of {speed} km/h. How long does the journey take?",
        f"{hours} hours",
        f"{hours + 1} hours",
        f"{hours + 2} hours",
        f"{hours + 3} hours"
    ))

# Percentage increase
for original, increase in [
    (500, 20), (800, 25), (1000, 15),
    (1200, 10), (2000, 5)
]:
    new_value = original + original * increase // 100

    HARD.append(create_question(
        f"The price of an item is Rs.{original}. It increases by {increase}%. What is the new price?",
        f"Rs.{new_value}",
        f"Rs.{original - original * increase // 100}",
        f"Rs.{original + increase}",
        f"Rs.{new_value + 100}"
    ))


# ============================================================
# VALIDATE QUESTIONS
# ============================================================

def validate_questions():

    difficulty_data = {
        "Easy": EASY,
        "Medium": MEDIUM,
        "Hard": HARD
    }

    for difficulty, data in difficulty_data.items():

        if len(data) != 30:
            raise ValueError(
                f"{difficulty} must contain 30 questions. Found {len(data)}"
            )

        question_texts = [item[0] for item in data]

        if len(set(question_texts)) != 30:
            raise ValueError(
                f"Duplicate questions found in {difficulty}!"
            )

        for question, answer, wrong_answers in data:

            options = [str(answer)] + [str(x) for x in wrong_answers]

            if len(set(options)) != 4:
                raise ValueError(
                    f"Duplicate options in {difficulty}: {question} | {options}"
                )

    print("Question validation successful!")


# ============================================================
# DATABASE INSERTION
# ============================================================

def seed_questions():

    conn = None
    total_inserted = 0

    try:
        validate_questions()

        difficulty_data = {
            "Easy": EASY,
            "Medium": MEDIUM,
            "Hard": HARD
        }

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM lessons WHERE title = ? AND topic = ?",
            (TOPIC, SUBJECT)
        )

        lesson = cursor.fetchone()

        if not lesson:
            print(f"Lesson '{TOPIC}' not found in database.")
            return

        lesson_id = lesson[0]

        for difficulty, data in difficulty_data.items():

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

        print("\nPractical Mathematics and Word Problems seeding completed!")
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
