import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

TOPIC = "HCF and LCM"
SUBJECT = "Mathematics"

random.seed(42)

EASY = [
    ("Find the HCF of 12 and 18.", "6", ["3", "9", "12"]),
    ("Find the LCM of 4 and 6.", "12", ["6", "18", "24"]),
    ("Find the HCF of 8 and 16.", "8", ["4", "16", "2"]),
    ("Find the LCM of 3 and 5.", "15", ["8", "10", "30"]),
    ("Find the HCF of 10 and 15.", "5", ["10", "15", "3"]),
    ("Find the LCM of 2 and 7.", "14", ["7", "9", "21"]),
    ("Find the HCF of 20 and 30.", "10", ["5", "15", "20"]),
    ("Find the LCM of 5 and 10.", "10", ["5", "15", "20"]),
    ("Find the HCF of 9 and 27.", "9", ["3", "18", "27"]),
    ("Find the LCM of 6 and 8.", "24", ["12", "18", "48"]),
    ("Find the HCF of 14 and 21.", "7", ["14", "3", "21"]),
    ("Find the LCM of 4 and 10.", "20", ["10", "14", "40"]),
    ("Find the HCF of 16 and 24.", "8", ["4", "12", "16"]),
    ("Find the LCM of 3 and 9.", "9", ["3", "18", "27"]),
    ("Find the HCF of 25 and 35.", "5", ["10", "7", "15"]),
    ("Find the LCM of 7 and 14.", "14", ["7", "21", "28"]),
    ("Find the HCF of 18 and 24.", "6", ["3", "9", "12"]),
    ("Find the LCM of 8 and 12.", "24", ["12", "36", "48"]),
    ("Find the HCF of 6 and 9.", "3", ["6", "9", "2"]),
    ("Find the LCM of 2 and 9.", "18", ["9", "11", "27"]),
    ("Find the HCF of 30 and 45.", "15", ["5", "10", "30"]),
    ("Find the LCM of 6 and 10.", "30", ["15", "20", "60"]),
    ("Find the HCF of 21 and 28.", "7", ["14", "21", "4"]),
    ("Find the LCM of 5 and 8.", "40", ["20", "30", "80"]),
    ("Find the HCF of 32 and 40.", "8", ["4", "16", "10"]),
    ("Find the LCM of 9 and 12.", "36", ["18", "24", "48"]),
    ("Find the HCF of 15 and 20.", "5", ["10", "15", "4"]),
    ("Find the LCM of 7 and 10.", "70", ["35", "17", "77"]),
    ("Find the HCF of 36 and 48.", "12", ["6", "18", "24"]),
    ("Find the LCM of 4 and 9.", "36", ["18", "27", "45"]),
]

MEDIUM = [
    ("Find the HCF of 48 and 60.", "12", ["6", "15", "24"]),
    ("Find the LCM of 12 and 15.", "60", ["30", "45", "90"]),
    ("Find the HCF of 72 and 90.", "18", ["9", "12", "36"]),
    ("Find the LCM of 8, 12 and 16.", "48", ["24", "36", "96"]),
    ("Find the HCF of 54 and 81.", "27", ["9", "18", "36"]),
    ("Find the LCM of 10, 15 and 20.", "60", ["30", "40", "120"]),
    ("Find the HCF of 84 and 126.", "42", ["21", "14", "63"]),
    ("Find the LCM of 6, 9 and 12.", "36", ["18", "24", "72"]),
    ("Find the HCF of 96 and 144.", "48", ["24", "36", "72"]),
    ("Find the LCM of 14 and 21.", "42", ["28", "35", "84"]),
    ("Find the HCF of 105 and 140.", "35", ["15", "20", "70"]),
    ("Find the LCM of 16 and 20.", "80", ["40", "60", "100"]),
    ("Find the HCF of 64 and 80.", "16", ["8", "32", "20"]),
    ("Find the LCM of 18 and 24.", "72", ["36", "48", "96"]),
    ("Find the HCF of 90 and 150.", "30", ["15", "45", "60"]),
    ("Find the LCM of 15, 20 and 30.", "60", ["30", "90", "120"]),
    ("Find the HCF of 108 and 180.", "36", ["18", "54", "72"]),
    ("Find the LCM of 9, 15 and 18.", "90", ["45", "60", "180"]),
    ("Find the HCF of 120 and 168.", "24", ["12", "36", "48"]),
    ("Find the LCM of 12 and 18.", "36", ["24", "48", "72"]),
    ("Find the HCF of 132 and 176.", "44", ["22", "33", "66"]),
    ("Find the LCM of 20 and 25.", "100", ["50", "75", "125"]),
    ("Find the HCF of 144 and 216.", "72", ["36", "48", "108"]),
    ("Find the LCM of 24 and 36.", "72", ["48", "60", "144"]),
    ("Find the HCF of 75 and 125.", "25", ["5", "15", "50"]),
    ("Find the LCM of 25 and 30.", "150", ["75", "100", "300"]),
    ("Find the HCF of 56 and 98.", "14", ["7", "28", "42"]),
    ("Find the LCM of 21 and 28.", "84", ["42", "56", "112"]),
    ("Find the HCF of 160 and 200.", "40", ["20", "50", "80"]),
    ("Find the LCM of 16, 24 and 32.", "96", ["48", "64", "192"]),
]

HARD = [
    ("The HCF of two numbers is 6 and their LCM is 180. If one number is 30, find the other.", "36", ["24", "42", "48"]),
    ("The product of two numbers is 720 and their HCF is 6. Find their LCM.", "120", ["60", "90", "180"]),
    ("Find the smallest number divisible by 12, 15 and 20.", "60", ["30", "45", "120"]),
    ("Find the greatest number that divides 45, 75 and 105 exactly.", "15", ["5", "10", "25"]),
    ("Two bells ring every 12 and 18 minutes. After how many minutes will they ring together again?", "36", ["24", "30", "48"]),
    ("Find the smallest number that leaves no remainder when divided by 8, 12 and 18.", "72", ["36", "48", "96"]),
    ("The HCF of 24 and 36 is 12. Find their LCM.", "72", ["48", "60", "96"]),
    ("Find the greatest length of a ribbon that can measure exactly 48 cm and 60 cm.", "12 cm", ["6 cm", "10 cm", "15 cm"]),
    ("Three lights flash every 6, 8 and 12 seconds. When will they flash together again?", "24 seconds", ["18 seconds", "36 seconds", "48 seconds"]),
    ("Find the smallest 3-digit number divisible by 12 and 15.", "120", ["105", "135", "150"]),
    ("Find the greatest 2-digit number divisible by both 6 and 8.", "96", ["72", "84", "88"]),
    ("Two numbers have HCF 8 and LCM 96. If one number is 24, find the other.", "32", ["16", "40", "48"]),
    ("Find the HCF of 144, 180 and 216.", "36", ["18", "24", "72"]),
    ("Find the LCM of 8, 10 and 15.", "120", ["60", "90", "150"]),
    ("Two runners complete a lap in 20 and 30 seconds. After how many seconds will they meet at the starting point?", "60 seconds", ["40 seconds", "50 seconds", "90 seconds"]),
    ("Find the greatest number that divides 65 and 117 leaving the same remainder in each case.", "26", ["13", "17", "52"]),
    ("The product of two numbers is 2400 and their HCF is 10. Find their LCM.", "240", ["120", "200", "300"]),
    ("Find the smallest number divisible by 16, 24 and 40.", "240", ["120", "160", "320"]),
    ("Find the greatest number that divides 98 and 122 leaving a remainder of 2 in each case.", "24", ["12", "20", "30"]),
    ("Two traffic lights change every 45 and 60 seconds. When will they change together again?", "180 seconds", ["90 seconds", "120 seconds", "150 seconds"]),
    ("The HCF of two numbers is 9 and their LCM is 108. If one number is 27, find the other.", "36", ["18", "45", "54"]),
    ("Find the smallest 4-digit number divisible by 18.", "1008", ["1002", "1010", "1026"]),
    ("Find the greatest number that divides 125, 175 and 225 exactly.", "25", ["15", "35", "50"]),
    ("Find the LCM of 18, 24 and 30.", "360", ["180", "240", "720"]),
    ("Two machines complete a cycle every 16 and 24 minutes. When will their cycles coincide?", "48 minutes", ["32 minutes", "40 minutes", "72 minutes"]),
    ("Find the smallest number which when divided by 6, 8 and 12 leaves no remainder.", "24", ["36", "48", "72"]),
    ("The HCF of two numbers is 5 and their LCM is 150. If one number is 25, find the other.", "30", ["20", "35", "45"]),
    ("Find the greatest number that divides 84, 120 and 156 exactly.", "12", ["6", "18", "24"]),
    ("Find the smallest number divisible by 14, 21 and 35.", "210", ["105", "140", "280"]),
    ("The product of two numbers is 3600 and their LCM is 300. Find their HCF.", "12", ["10", "15", "20"]),
]


def make_questions(data):
    questions = []

    for question, answer, wrong_answers in data:
        options = [answer] + wrong_answers[:]
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
    total_inserted = 0

    difficulty_data = {
        "Easy": EASY,
        "Medium": MEDIUM,
        "Hard": HARD
    }

    for difficulty, data in difficulty_data.items():
        cursor.execute(
            """
            SELECT id FROM quizzes
            WHERE lesson_id = ? AND LOWER(difficulty) = LOWER(?)
            """,
            (lesson_id, difficulty)
        )

        quiz = cursor.fetchone()

        if not quiz:
            print(f"{difficulty} quiz not found for {TOPIC}")
            continue

        quiz_id = quiz[0]
        questions = make_questions(data)
        inserted = 0

        for q in questions:
            cursor.execute(
                "SELECT 1 FROM questions WHERE quiz_id = ? AND question = ?",
                (quiz_id, q[0])
            )

            if cursor.fetchone():
                continue

            cursor.execute(
                """
                INSERT INTO questions
                (quiz_id, question, option_a, option_b,
                 option_c, option_d, correct_answer)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (quiz_id, *q)
            )

            inserted += 1

        total_inserted += inserted
        print(f"{difficulty}: {inserted} questions inserted.")

    conn.commit()
    conn.close()

    print(f"\nCompleted! Total new questions inserted: {total_inserted}")


if __name__ == "__main__":
    main()