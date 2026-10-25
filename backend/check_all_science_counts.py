
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"
TARGET_QUESTIONS = 30
EXPECTED_DIFFICULTIES = {"Easy", "Medium", "Hard"}

def main():
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DATABASE_PATH}")

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    try:
        # Check the 35 additional Science lessons (IDs 46–80).
        cursor.execute(
            """
            SELECT id, title
            FROM lessons
            WHERE id BETWEEN 46 AND 80
            ORDER BY id
            """
        )
        lessons = cursor.fetchall()

        if not lessons:
            print("No lessons found with IDs 46–80.")
            return

        print(f"Checking {len(lessons)} additional Science lessons...")
        print("=" * 75)

        total_questions = 0
        complete_lessons = 0
        incomplete_lessons = []

        for lesson_id, title in lessons:
            cursor.execute(
                """
                SELECT q.id, q.difficulty, COUNT(questions.id)
                FROM quizzes AS q
                LEFT JOIN questions ON questions.quiz_id = q.id
                WHERE q.lesson_id = ?
                GROUP BY q.id, q.difficulty
                """,
                (lesson_id,),
            )

            quiz_rows = cursor.fetchall()
            counts = {}
            issues = []

            for quiz_id, difficulty, count in quiz_rows:
                counts[difficulty] = counts.get(difficulty, 0) + 1
                total_questions += count

                if count != TARGET_QUESTIONS:
                    issues.append(
                        f"{difficulty}: {count}/{TARGET_QUESTIONS} questions"
                    )

            for difficulty in EXPECTED_DIFFICULTIES:
                if difficulty not in counts:
                    issues.append(f"{difficulty}: quiz missing")
                elif counts[difficulty] > 1:
                    issues.append(f"{difficulty}: duplicate quizzes found")

            print(f"\n[{lesson_id}] {title}")

            for difficulty in ("Easy", "Medium", "Hard"):
                matching = [
                    count
                    for _, quiz_difficulty, count in quiz_rows
                    if quiz_difficulty == difficulty
                ]

                if len(matching) == 1:
                    count = matching[0]
                    status = "OK" if count == TARGET_QUESTIONS else "CHECK"
                    print(f"  {difficulty}: {count}/30 [{status}]")
                elif len(matching) == 0:
                    print(f"  {difficulty}: MISSING QUIZ")
                else:
                    print(f"  {difficulty}: {len(matching)} QUIZZES FOUND")

            if not issues:
                complete_lessons += 1
            else:
                incomplete_lessons.append((lesson_id, title, issues))

        print("\n" + "=" * 75)
        print("FINAL SUMMARY")
        print(f"Lessons found: {len(lessons)}/35")
        print(f"Complete lessons: {complete_lessons}/{len(lessons)}")
        print(f"Total questions across these lessons: {total_questions}")
        print(f"Expected if all 35 lessons have 90 questions: {35 * 90}")

        if not incomplete_lessons and len(lessons) == 35:
            print("\nSUCCESS! All 35 lessons have 30 Easy, 30 Medium and 30 Hard questions.")
        else:
            print("\nLessons needing attention:")
            for lesson_id, title, issues in incomplete_lessons:
                print(f"\n{lesson_id}: {title}")
                for issue in issues:
                    print(f"  - {issue}")

            if len(lessons) != 35:
                print("WARNING: Expected 35 lessons with IDs 46–80.")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
