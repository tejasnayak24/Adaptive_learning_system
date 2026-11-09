
import sqlite3
from pathlib import Path
from collections import Counter

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

START_ID = 161
END_ID = 200

EXPECTED_LESSONS = 40
EXPECTED_PER_DIFFICULTY = 30
EXPECTED_TOTAL = 3600

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

    print(f"GK lessons found: {len(lessons)}/{EXPECTED_LESSONS}\n")

    total_questions = 0
    incomplete = []
    duplicate_issues = []
    invalid_answers = []
    invalid_options = []
    missing_quizzes = []

    for lesson_id, title in lessons:

        # Get quiz difficulty from the quizzes table.
        cursor.execute("""
            SELECT id, difficulty
            FROM quizzes
            WHERE lesson_id = ?
        """, (lesson_id,))

        quizzes = cursor.fetchall()

        difficulty_counts = Counter()
        all_questions = []

        for quiz_id, difficulty in quizzes:

            cursor.execute("""
                SELECT
                    id,
                    question,
                    option_a,
                    option_b,
                    option_c,
                    option_d,
                    correct_answer
                FROM questions
                WHERE quiz_id = ?
            """, (quiz_id,))

            questions = cursor.fetchall()

            difficulty_counts[difficulty] += len(questions)
            total_questions += len(questions)

            for row in questions:

                all_questions.append(row)

                question_id, question, a, b, c, d, answer = row

                # Validate correct answer
                if answer not in ("A", "B", "C", "D"):
                    invalid_answers.append(
                        (lesson_id, question_id, answer)
                    )

                # Validate options
                options = [a, b, c, d]

                if (
                    any(not option for option in options)
                    or len(set(options)) != 4
                ):
                    invalid_options.append(
                        (lesson_id, question_id)
                    )

        if not quizzes:
            missing_quizzes.append((lesson_id, title))

        lesson_ok = True

        # Check exactly 30 questions per difficulty
        for difficulty in DIFFICULTIES:

            count = difficulty_counts[difficulty]

            if count != EXPECTED_PER_DIFFICULTY:

                lesson_ok = False

                incomplete.append(
                    (lesson_id, title, difficulty, count)
                )

        # Check duplicate question text within each lesson
        normalized_questions = [
            row[1].strip().lower()
            for row in all_questions
            if row[1]
        ]

        duplicates = [
            question
            for question, count in Counter(
                normalized_questions
            ).items()
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

    # Final summary
    print("\n================ FINAL SUMMARY ================\n")

    print(f"Total GK lessons: {len(lessons)}")
    print(f"Expected GK lessons: {EXPECTED_LESSONS}")

    print(f"Total questions: {total_questions}")
    print(f"Expected questions: {EXPECTED_TOTAL}")

    print(
        f"Incomplete difficulty counts: {len(incomplete)}"
    )

    print(
        f"Duplicate question groups: {len(duplicate_issues)}"
    )

    print(
        f"Invalid correct answers: {len(invalid_answers)}"
    )

    print(
        f"Invalid options: {len(invalid_options)}"
    )

    print(
        f"Lessons without quizzes: {len(missing_quizzes)}"
    )

    # Display problems
    if incomplete:

        print("\nINCOMPLETE TOPICS:")

        for item in incomplete:
            print(item)

    if duplicate_issues:

        print("\nDUPLICATE QUESTIONS:")

        for lesson_id, title, duplicates in duplicate_issues:

            print(f"\nLesson {lesson_id} - {title}:")

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

    if missing_quizzes:

        print("\nLESSONS WITHOUT QUIZZES:")

        for item in missing_quizzes:
            print(item)

    # Final validation
    success = (
        len(lessons) == EXPECTED_LESSONS
        and total_questions == EXPECTED_TOTAL
        and not incomplete
        and not duplicate_issues
        and not invalid_answers
        and not invalid_options
        and not missing_quizzes
    )

    print("\n================================================")

    if success:

        print("\nSUCCESS! GK QUESTION BANK PASSED ALL CHECKS.")

        print("40 topics verified.")
        print("1200 Easy questions verified.")
        print("1200 Medium questions verified.")
        print("1200 Hard questions verified.")
        print("3600 total questions verified.")

        print("No duplicate questions.")
        print("No invalid answers.")
        print("No invalid options.")

    else:

        print("\nVERIFICATION FAILED.")
        print("Please check the issues displayed above.")

    conn.close()


if __name__ == "__main__":
    main()
