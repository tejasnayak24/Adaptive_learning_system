
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

def main():
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DATABASE_PATH}")

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT
                l.id,
                l.title,
                q.difficulty,
                COUNT(questions.id)
            FROM lessons AS l
            JOIN quizzes AS q ON q.lesson_id = l.id
            LEFT JOIN questions ON questions.quiz_id = q.id
            WHERE l.id BETWEEN 2 AND 6
               OR l.id BETWEEN 46 AND 80
            GROUP BY l.id, l.title, q.id, q.difficulty
            ORDER BY l.id, q.difficulty
        """)

        rows = cursor.fetchall()

        print("SCIENCE QUESTION BANK SUMMARY")
        print("=" * 65)

        total = 0

        for lesson_id, title, difficulty, count in rows:
            total += count
            print(
                f"Lesson {lesson_id}: {title} | "
                f"{difficulty} | {count} questions"
            )

        print("=" * 65)
        print(f"Total quiz records: {len(rows)}")
        print(f"Total questions: {total}")

        # Check that every correct_answer is A, B, C or D.
        cursor.execute("""
            SELECT
                l.title,
                q.difficulty,
                questions.id,
                questions.question,
                questions.correct_answer
            FROM questions
            JOIN quizzes AS q ON q.id = questions.quiz_id
            JOIN lessons AS l ON l.id = q.lesson_id
            WHERE (
                l.id BETWEEN 2 AND 6
                OR l.id BETWEEN 46 AND 80
            )
            AND UPPER(TRIM(questions.correct_answer))
                NOT IN ('A', 'B', 'C', 'D')
            ORDER BY l.id, q.difficulty
        """)

        invalid = cursor.fetchall()

        print("\nINVALID ANSWER KEY CHECK")
        print("=" * 65)

        if invalid:
            for title, difficulty, question_id, question, answer in invalid:
                print(
                    f"{title} | {difficulty} | Question ID {question_id}\n"
                    f"Question: {question}\n"
                    f"Stored answer: {answer}\n"
                )
            print(f"Found {len(invalid)} invalid answer keys.")
        else:
            print("All stored answer keys use A, B, C or D.")

        print("\nNote: Valid letters do not guarantee that the answers are correct.")

    finally:
        conn.close()

if __name__ == "__main__":
    main()
