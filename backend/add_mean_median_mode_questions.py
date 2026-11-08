
import sqlite3
import random
from pathlib import Path

random.seed(42)

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

TOPIC = "Mean, Median and Mode"
SUBJECT = "Mathematics"


# Format: (question, correct_answer, [wrong1, wrong2, wrong3])


EASY = [
    ("What is the mean?", "Average of the values", ["Middle value", "Most frequent value", "Difference between values"]),
    ("What is the median?", "Middle value of ordered data", ["Average value", "Most frequent value", "Largest value"]),
    ("What is the mode?", "Most frequently occurring value", ["Middle value", "Average value", "Smallest value"]),
    ("Find the mean of 2, 4, 6.", "4", ["2", "6", "12"]),
    ("Find the median of 3, 5, 7.", "5", ["3", "7", "15"]),
    ("Find the mode of 2, 2, 3, 4.", "2", ["3", "4", "4.5"]),
    ("Find the mean of 5, 5, 5.", "5", ["3", "10", "15"]),
    ("Find the median of 1, 3, 5, 7, 9.", "5", ["3", "7", "9"]),
    ("Find the mode of 4, 5, 5, 6, 7.", "5", ["4", "6", "7"]),
    ("Find the mean of 10, 20, 30.", "20", ["10", "30", "60"]),
    ("Find the median of 2, 4, 6, 8, 10.", "6", ["4", "8", "10"]),
    ("Find the mode of 1, 2, 2, 3, 3, 3.", "3", ["1", "2", "4"]),
    ("What is the mean of 8 and 12?", "10", ["8", "12", "20"]),
    ("Find the median of 4, 8, 12.", "8", ["4", "12", "24"]),
    ("Find the mean of 3, 6, 9.", "6", ["3", "9", "18"]),
    ("Find the median of 5, 10, 15, 20, 25.", "15", ["10", "20", "25"]),
    ("Find the mode of 7, 8, 8, 9, 10.", "8", ["7", "9", "10"]),
    ("Which measure represents the average?", "Mean", ["Median", "Mode", "Range"]),
    ("Which measure is affected by extreme values?", "Mean", ["Median", "Mode", "None"]),
    ("Which measure identifies the most common value?", "Mode", ["Mean", "Median", "Range"]),
    ("How many values are there in 2, 4, 6, 8?", "4", ["2", "3", "5"]),
    ("Find the sum of 2, 3, 4.", "9", ["7", "8", "10"]),
    ("Find the mean of 4, 6, 8.", "6", ["4", "8", "18"]),
    ("Find the median of 1, 2, 3, 4, 5.", "3", ["2", "4", "5"]),
    ("Find the mode of 6, 6, 7, 8, 9.", "6", ["7", "8", "9"]),
    ("What is the median of 10, 20, 30, 40?", "25", ["20", "30", "40"]),
    ("Find the mean of 1, 2, 3, 4, 5.", "3", ["2", "4", "5"]),
    ("If all values are equal to 7, what is their mean?", "7", ["0", "1", "14"]),
    ("If all values are equal to 5, what is their median?", "5", ["0", "10", "15"]),
    ("If a value occurs most frequently, it is called the:", "Mode", ["Mean", "Median", "Range"]),
]


MEDIUM = [
    ("Find the mean of 12, 15, 18, 21.", "16.5", ["15", "17", "18"]),
    ("Find the median of 4, 8, 10, 12, 16.", "10", ["8", "12", "16"]),
    ("Find the mode of 3, 5, 5, 7, 7, 7, 9.", "7", ["5", "9", "3"]),
    ("Find the mean of 6, 8, 10, 12, 14.", "10", ["8", "12", "14"]),
    ("Find the median of 2, 5, 7, 9, 11, 13.", "8", ["7", "9", "11"]),
    ("Find the mean of 15, 20, 25, 30, 35.", "25", ["20", "30", "35"]),
    ("Find the median of 3, 6, 9, 12, 15, 18, 21.", "12", ["9", "15", "18"]),
    ("Find the mode of 4, 4, 5, 6, 6, 6, 7, 8.", "6", ["4", "5", "7"]),
    ("The mean of 5 numbers is 12. Find their sum.", "60", ["50", "55", "65"]),
    ("The sum of 8 observations is 96. Find the mean.", "12", ["10", "14", "16"]),
    ("The mean of 4 numbers is 15. Three numbers are 10, 15 and 20. Find the fourth number.", "15", ["10", "20", "25"]),
    ("The mean of 5 numbers is 20. Four numbers total 70. Find the fifth number.", "30", ["20", "25", "35"]),
    ("Find the median of 10, 15, 20, 25, 30, 35.", "22.5", ["20", "25", "30"]),
    ("Find the mean of 2, 4, 6, 8, 10, 12.", "7", ["6", "8", "9"]),
    ("Find the mode of 10, 12, 12, 14, 14, 14, 16.", "14", ["12", "16", "10"]),
    ("The mean of 6 values is 10. What is their total?", "60", ["50", "70", "80"]),
    ("The average of 5 numbers is 18. Their total is:", "90", ["80", "85", "100"]),
    ("Find the median of 1, 4, 7, 10, 13, 16, 19, 22.", "11.5", ["10", "13", "16"]),
    ("Find the mean of 20, 25, 30, 35, 40.", "30", ["25", "35", "40"]),
    ("Find the mode of 2, 3, 4, 4, 5, 5, 5, 6.", "5", ["4", "6", "3"]),
    ("If each observation is increased by 5, how does the mean change?", "It increases by 5", ["It decreases by 5", "It remains unchanged", "It doubles"]),
    ("If every observation is multiplied by 3, the mean is:", "Multiplied by 3", ["Divided by 3", "Unchanged", "Increased by 3"]),
    ("The mean of 10 observations is 8. If one observation is removed, the total becomes 72. What was the removed value?", "8", ["6", "10", "12"]),
    ("Find the median of 6, 8, 10, 12, 14, 16.", "11", ["10", "12", "14"]),
    ("Find the mean of 7, 9, 11, 13, 15.", "11", ["9", "12", "13"]),
    ("The mean of 3 numbers is 14. Two numbers are 10 and 12. Find the third number.", "20", ["16", "18", "22"]),
    ("Find the median of 5, 9, 12, 15, 18, 20, 25.", "15", ["12", "18", "20"]),
    ("Find the mode of 1, 1, 2, 3, 3, 3, 4, 4.", "3", ["1", "2", "4"]),
    ("The mean of 4 numbers is 25. If one number is 40, find the sum of the remaining three.", "60", ["50", "70", "80"]),
    ("Find the median of 2, 6, 8, 10, 14, 18, 20.", "10", ["8", "14", "18"]),
]


HARD = [
    ("The mean of 6 numbers is 15. Five numbers are 10, 12, 14, 16 and 18. Find the sixth number.", "20", ["18", "22", "24"]),
    ("The mean of 8 observations is 25. If one observation is removed, the mean of the remaining 7 is 24. Find the removed observation.", "32", ["25", "30", "35"]),
    ("The average of 5 numbers is 24. If one number is 30, find the average of the remaining four.", "22.5", ["20", "24", "25"]),
    ("The mean of 10 numbers is 20. If each number is increased by 4, find the new mean.", "24", ["20", "22", "28"]),
    ("The mean of 5 numbers is 16. If one number is replaced by 26 instead of 16, what is the new mean?", "18", ["16", "17", "20"]),
    ("The average of 6 numbers is 12. If each number is doubled, what is the new average?", "24", ["12", "18", "36"]),
    ("The mean of 7 numbers is 18. Their total sum is:", "126", ["116", "120", "136"]),
    ("The median of 3, 5, 7, x, 11, 13, 15 is 9. Find x.", "9", ["7", "11", "13"]),
    ("Find the median of 4, 7, 9, 12, 15, 18, 20, 24, 27.", "15", ["12", "18", "20"]),
    ("Find the mean of 12, 14, 16, 18, 20, 22, 24, 26.", "19", ["18", "20", "21"]),
    ("The mean of 5 numbers is 30. Four numbers are 20, 25, 35 and 40. Find the fifth number.", "30", ["25", "35", "40"]),
    ("The average of 4 numbers is 18. If a fifth number 28 is added, find the new average.", "20", ["18", "19", "22"]),
    ("The mean of 9 values is 14. If one value of 20 is removed, find the new mean.", "13.25", ["13", "14", "15"]),
    ("The mean of 5 values is 10. If four values total 36, find the fifth value.", "14", ["10", "12", "16"]),
    ("The mean of 6 numbers is 15. If one number is 25, find the mean of the remaining five.", "13", ["12", "14", "15"]),
    ("Find the mode of 5, 7, 7, 8, 8, 8, 9, 9, 10.", "8", ["7", "9", "10"]),
    ("Find the median of 11, 13, 15, 17, 19, 21, 23, 25.", "18", ["17", "19", "21"]),
    ("The mean of 4 numbers is 20. If three numbers are 15, 18 and 22, find the fourth.", "25", ["20", "22", "28"]),
    ("The average age of 5 students is 16 years. A new student aged 22 joins. Find the new average age.", "17 years", ["16 years", "18 years", "19 years"]),
    ("The average of 10 numbers is 12. If each number is reduced by 2, what is the new average?", "10", ["8", "12", "14"]),
    ("The mean of 5 consecutive integers is 18. Find the largest integer.", "20", ["18", "19", "21"]),
    ("The mean of 7 consecutive integers is 15. Find the smallest integer.", "12", ["13", "14", "11"]),
    ("The average of 4 numbers is 16. If one number is 10 and another is 18, find the sum of the remaining two.", "36", ["30", "32", "40"]),
    ("The mean of 6 values is 20. Five values total 95. Find the sixth value.", "25", ["20", "30", "35"]),
    ("The mean of 3 numbers is 15. If the first two are 12 and 18, find the third.", "15", ["12", "18", "20"]),
    ("The mean of 8 numbers is 10. If one number is 18, find the mean of the remaining seven.", "58/7", ["8", "9", "10"]),
    ("The mean of 5 numbers is 14. If each number is multiplied by 2 and then increased by 3, what is the new mean?", "31", ["28", "30", "34"]),
    ("The mean of 4 numbers is 12. If one number is increased by 8, what is the new mean?", "14", ["12", "13", "16"]),
    ("Find the median of 2, 5, 8, 11, 14, 17, 20, 23, 26, 29.", "15.5", ["14", "17", "20"]),
    ("The mean of 6 numbers is 18. If one number 24 is replaced by 36, find the new mean.", "20", ["18", "19", "22"]),
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

        print("\nMean, Median and Mode seeding completed!")
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
