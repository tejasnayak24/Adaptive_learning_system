
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

LESSONS = [
    "Solar System",
    "Stars and Galaxies",
    "Rocks and Minerals",
    "Water Cycle",
    "Natural Disasters and Preparedness",
]

conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

try:
    for lesson in LESSONS:
        cursor.execute(
            """
            SELECT id, title
            FROM lessons
            WHERE LOWER(TRIM(title)) = LOWER(TRIM(?))
            """,
            (lesson,),
        )

        lesson_row = cursor.fetchone()

        if not lesson_row:
            print(f"\n{lesson}: LESSON NOT FOUND")
            continue

        lesson_id, lesson_title = lesson_row

        print(f"\n{'=' * 55}")
        print(lesson_title)

        cursor.execute(
            """
            SELECT q.difficulty, COUNT(questions.id)
            FROM quizzes AS q
            LEFT JOIN questions
                ON questions.quiz_id = q.id
            WHERE q.lesson_id = ?
            GROUP BY q.id, q.difficulty
            ORDER BY q.difficulty
            """,
            (lesson_id,),
        )

        results = cursor.fetchall()

        for difficulty, count in results:
            status = "OK" if count == 30 else "CHECK"
            print(f"{difficulty}: {count}/30 questions [{status}]")

        if len(results) != 3:
            print(f"WARNING: Expected 3 quizzes, found {len(results)}")

finally:
    conn.close()
