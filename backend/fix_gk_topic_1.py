
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 161

OLD_QUESTION = (
    "which union territory has kavaratti as its capital?"
)

NEW_QUESTION = (
    "Which Union Territory has Port Blair as its capital?"
)

OPTIONS = [
    "Andaman and Nicobar Islands",
    "Lakshadweep",
    "Chandigarh",
    "Puducherry"
]

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT q.id, q.question
            FROM questions q
            JOIN quizzes qu ON q.quiz_id = qu.id
            WHERE qu.lesson_id = ?
              AND LOWER(TRIM(q.question)) = ?
            ORDER BY q.id
        """, (LESSON_ID, OLD_QUESTION))

        duplicates = cursor.fetchall()

        if len(duplicates) < 2:
            print("No duplicate found to replace.")
            return

        # Keep the first question and replace the second.
        question_id = duplicates[1][0]

        cursor.execute("""
            UPDATE questions
            SET question = ?,
                option_a = ?,
                option_b = ?,
                option_c = ?,
                option_d = ?,
                correct_answer = ?
            WHERE id = ?
        """, (
            NEW_QUESTION,
            OPTIONS[0],
            OPTIONS[1],
            OPTIONS[2],
            OPTIONS[3],
            "A",
            question_id
        ))

        conn.commit()

        print("SUCCESS! Topic 1 duplicate replaced.")
        print("New question:", NEW_QUESTION)
        print("Correct answer: A")

    except Exception as e:
        conn.rollback()
        print("ERROR:", e)

    finally:
        conn.close()


if __name__ == "__main__":
    main()
