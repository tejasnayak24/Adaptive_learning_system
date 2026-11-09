
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"
TARGET_QUESTIONS = 30

def main():
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DATABASE_PATH}")

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    try:
        # Original 5 lessons and 35 additional lessons.
        cursor.execute("""
            SELECT id, title
            FROM lessons
            WHERE id BETWEEN 2 AND 6
               OR id BETWEEN 46 AND 80
            ORDER BY id
        """)
        lessons = cursor.fetchall()

        total_questions = 0
        complete_lessons = 0
        problems = []

        print(f"Science lessons found: {len(lessons)}")
        print("=" * 70)

        for lesson_id, title in lessons:
            cursor.execute("""
                SELECT q.id, q.difficulty, COUNT(questions.id)
                FROM quizzes AS q
                LEFT JOIN questions ON questions.quiz_id = q.id
                WHERE q.lesson_id = ?
                GROUP BY q.id, q.difficulty
            """, (lesson_id,))

            quiz_rows = cursor.fetchall()
            counts = {}

            for quiz_id, difficulty, count in quiz_rows:
                counts.setdefault(difficulty, []).append(count)
                total_questions += count

            lesson_ok = True

            print(f"\n[{lesson_id}] {title}")

            for difficulty in ("Easy", "Medium", "Hard"):
                matching = counts.get(difficulty, [])

                if len(matching) == 1 and matching[0] == TARGET_QUESTIONS:
                    print(f"  {difficulty}: {matching[0]}/30 [OK]")
                else:
                    lesson_ok = False

                    if not matching:
                        message = f"{difficulty} quiz is missing"
                    elif len(matching) > 1:
                        message = f"{difficulty} has {len(matching)} quizzes"
                    else:
                        message = (
                            f"{difficulty} has {matching[0]} questions "
                            f"(expected 30)"
                        )

                    problems.append(f"{title}: {message}")
                    print(f"  {message} [CHECK]")

            if lesson_ok:
                complete_lessons += 1

        print("\n" + "=" * 70)
        print("FINAL SUMMARY")
        print(f"Lessons found: {len(lessons)}/40")
        print(f"Complete lessons: {complete_lessons}/{len(lessons)}")
        print(f"Total questions: {total_questions}")
        print(f"Expected total: {40 * 3 * TARGET_QUESTIONS}")

        if len(lessons) == 40 and complete_lessons == 40:
            print("\nSUCCESS! All 40 Science lessons are complete.")
        else:
            print("\nSome lessons need checking.")

        if problems:
            print("\nISSUES FOUND:")
            for problem in problems:
                print(f"- {problem}")

    finally:
        conn.close()

if __name__ == "__main__":
    main()
