
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

EXPECTED = 30
DIFFICULTIES = ["Easy", "Medium", "Hard"]


def main():
    if not DB_PATH.exists():
        print("ERROR: Database file not found:", DB_PATH)
        return

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    cur.execute("""
        SELECT id, title
        FROM lessons
        WHERE topic = 'English'
        ORDER BY id
    """)

    lessons = cur.fetchall()

    if not lessons:
        print("No English lessons found.")
        con.close()
        return

    incomplete = []
    total_questions = 0

    print("\n========== ENGLISH QUESTION BANK VERIFICATION ==========\n")

    for lesson_id, title in lessons:
        print(f"\nLesson {lesson_id}: {title}")

        lesson_counts = {}

        for difficulty in DIFFICULTIES:
            cur.execute("""
                SELECT q.id, COUNT(questions.id)
                FROM quizzes q
                LEFT JOIN questions ON questions.quiz_id = q.id
                WHERE q.lesson_id = ?
                AND q.difficulty = ?
                GROUP BY q.id
            """, (lesson_id, difficulty))

            quiz_results = cur.fetchall()

            if not quiz_results:
                count = 0
            else:
                count = sum(row[1] for row in quiz_results)

            lesson_counts[difficulty] = count
            total_questions += count

            status = "PASS" if count == EXPECTED else "INCOMPLETE"

            print(f"  {difficulty}: {count}/30 - {status}")

        if all(lesson_counts[d] == EXPECTED for d in DIFFICULTIES):
            print("  RESULT: COMPLETE")
        else:
            print("  RESULT: NEEDS ATTENTION")
            incomplete.append((lesson_id, title, lesson_counts))

    print("\n================ FINAL SUMMARY ================\n")
    print("Total English lessons:", len(lessons))
    print("Total questions counted:", total_questions)
    print("Expected questions:", len(lessons) * 90)
    print("Incomplete lessons:", len(incomplete))

    if incomplete:
        print("\nTopics that need attention:")
        for lesson_id, title, counts in incomplete:
            print(f"\n{lesson_id} - {title}")
            for difficulty, count in counts.items():
                if count != EXPECTED:
                    print(f"  {difficulty}: {count}/30")
    else:
        print("\nSUCCESS! Every English lesson has exactly 90 questions!")
        print("30 Easy + 30 Medium + 30 Hard.")

    con.close()


if __name__ == "__main__":
    main()
