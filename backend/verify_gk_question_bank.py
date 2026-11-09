
import sqlite3
from pathlib import Path
from collections import Counter

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

START_ID = 161
END_ID = 200
EXPECTED_PER_DIFFICULTY = 30
DIFFICULTIES = ["Easy", "Medium", "Hard"]

def main():
    if not DB_PATH.exists():
        print("ERROR: Database not found:", DB_PATH)
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("\n========== GK QUESTION BANK VERIFICATION ==========\n")

    cursor.execute("""
        SELECT id, title
        FROM lessons
        WHERE id BETWEEN ? AND ?
        ORDER BY id
    """, (START_ID, END_ID))

    lessons = cursor.fetchall()

    print(f"GK lessons found: {len(lessons)}/40")

    if len(lessons) != 40:
        print("ERROR: Expected exactly 40 lessons.")

    total_questions = 0
    incomplete = []
    duplicate_issues = []
    invalid_answers = []
    invalid_options = []

    for lesson_id, title in lessons:
        cursor.execute("""
            SELECT q.difficulty, qu.id
            FROM quizzes qu
            JOIN lessons q ON q.id = qu.lesson_id
            WHERE qu.lesson_id = ?
        """, (lesson_id,))

        quizzes = cursor.fetchall()

        difficulty_counts = Counter()
        all_questions = []

        for difficulty, quiz_id in quizzes:
            cursor.execute("""
                SELECT id, question, option_a, option_b,
                       option_c, option_d, correct_answer
                FROM questions
                WHERE quiz_id = ?
            """, (quiz_id,))

            questions = cursor.fetchall()
            difficulty_counts[difficulty] += len(questions)
            total_questions += len(questions)

            for row in questions:
                all_questions.append((difficulty, row))

                question_id, question, a, b, c, d, answer = row

                if answer not in ("A", "B", "C", "D"):
                    invalid_answers.append(
                        (lesson_id, question_id, answer)
                    )

                options = [a, b, c, d]

                if any(not option for option in options) or len(
                    set(options)
                ) != 4:
                    invalid_options.append(
                        (lesson_id, question_id)
                    )

        lesson_ok = True

        for difficulty in DIFFICULTIES:
            count = difficulty_counts[difficulty]

            if count != EXPECTED_PER_DIFFICULTY:
                lesson_ok = False
                incomplete.append(
                    (lesson_id, title, difficulty, count)
                )

        # Check duplicate question text within the lesson
        normalized = [
            row[1][1].strip().lower()
            for row in all_questions
        ]

        duplicates = [
            question for question, count
            in Counter(normalized).items()
            if count > 1
        ]

        if duplicates:
            duplicate_issues.append(
                (lesson_id, title, duplicates)
            )

        status = "PASS" if lesson_ok else "FAIL"

        print(
            f"{status} | ID {lesson_id} | {title} | "
            f"Easy: {difficulty_counts['Easy']} | "
            f"Medium: {difficulty_counts['Medium']} | "
            f"Hard: {difficulty_counts['Hard']}"
        )

    print("\n================ FINAL SUMMARY ================\n")
    print(f"Total GK lessons: {len(lessons)}")
    print(f"Total questions: {total_questions}")
    print(f"Expected questions: {40 * 90}")
    print(f"Incomplete difficulty counts: {len(incomplete)}")
    print(f"Duplicate question groups: {len(duplicate_issues)}")
    print(f"Invalid correct answers: {len(invalid_answers)}")
    print(f"Invalid options: {len(invalid_options)}")

    if incomplete:
        print("\nINCOMPLETE TOPICS:")
        for item in incomplete:
            print(item)

    if duplicate_issues:
        print("\nDUPLICATE QUESTIONS:")
        for lesson_id, title, duplicates in duplicate_issues:
            print(f"Lesson {lesson_id} - {title}:")
            for question in duplicates:
                print("  ", question)

    if invalid_answers:
        print("\nINVALID ANSWERS:")
        for item in invalid_answers:
            print(item)

    if invalid_options:
        print("\nINVALID OPTIONS:")
        for item in invalid_options:
            print(item)

    success = (
        len(lessons) == 40
        and total_questions == 3600
        and not incomplete
        and not duplicate_issues
        and not invalid_answers
        and not invalid_options
    )

    print("\n================================================")

    if success:
        print("SUCCESS! GK QUESTION BANK PASSED ALL CHECKS.")
        print("All 40 topics contain exactly 90 questions.")
    else:
        print("VERIFICATION FAILED. CHECK THE ISSUES ABOVE.")

    conn.close()


if __name__ == "__main__":
    main()
