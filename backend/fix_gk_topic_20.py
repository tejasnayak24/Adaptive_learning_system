
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 180

OLD_QUESTION = (
    "who was the first indian woman to become the president "
    "of the indian national congress?"
)

NEW_QUESTION = (
    "Who founded the Arya Samaj in 1875?"
)

OPTIONS = [
    "Swami Dayanand Saraswati",
    "Swami Vivekananda",
    "Raja Ram Mohan Roy",
    "Ishwar Chandra Vidyasagar"
]


def main():
    if not DB_PATH.exists():
        print("ERROR: Database not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT q.id
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

        # Keep the first occurrence; replace the second.
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

        print("SUCCESS! Topic 20 duplicate replaced.")
        print("New question:", NEW_QUESTION)
        print("Correct answer: A - Swami Dayanand Saraswati")

    except Exception as error:
        conn.rollback()
        print("ERROR:", error)

    finally:
        conn.close()


if __name__ == "__main__":
    main()
