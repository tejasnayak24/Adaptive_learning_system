
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

BANK = {
    "Easy": [
        ("She ___ to college every day.", "goes", "go", "going", "gone"),
        ("They ___ playing football.", "are", "is", "was", "be"),
        ("He ___ a new bicycle.", "has", "have", "having", "had"),
        ("The boys ___ in the playground.", "are", "is", "was", "be"),
        ("My mother ___ delicious food.", "cooks", "cook", "cooking", "cooked"),
        ("I ___ a student.", "am", "is", "are", "be"),
        ("The dog ___ loudly.", "barks", "bark", "barking", "barked"),
        ("We ___ ready for the examination.", "are", "is", "am", "be"),
        ("Ravi and Rohan ___ friends.", "are", "is", "was", "be"),
        ("The sun ___ in the east.", "rises", "rise", "rising", "risen"),
        ("She ___ English fluently.", "speaks", "speak", "speaking", "spoken"),
        ("The children ___ happy.", "are", "is", "am", "be"),
        ("My father ___ in a bank.", "works", "work", "working", "worked"),
        ("You ___ my best friend.", "are", "is", "am", "be"),
        ("The cat ___ milk.", "drinks", "drink", "drinking", "drunk"),
        ("Birds ___ in the sky.", "fly", "flies", "flying", "flown"),
        ("He ___ cricket every Sunday.", "plays", "play", "playing", "played"),
        ("The flowers ___ beautiful.", "look", "looks", "looking", "looked"),
        ("My sister ___ a doctor.", "is", "are", "am", "be"),
        ("The teacher ___ the lesson.", "explains", "explain", "explaining", "explained"),
        ("I ___ two brothers.", "have", "has", "having", "had"),
        ("The students ___ their homework.", "do", "does", "doing", "done"),
        ("She ___ very hard.", "studies", "study", "studying", "studied"),
        ("They ___ to school by bus.", "go", "goes", "going", "gone"),
        ("The baby ___ peacefully.", "sleeps", "sleep", "sleeping", "slept"),
        ("My friends ___ coming today.", "are", "is", "am", "be"),
        ("He ___ a letter every week.", "writes", "write", "writing", "written"),
        ("The players ___ practising.", "are", "is", "was", "be"),
        ("Water ___ at 100 degrees Celsius.", "boils", "boil", "boiling", "boiled"),
        ("Everyone ___ a chance to participate.", "has", "have", "having", "had")
    ],

    "Medium": [
        ("Each of the students ___ a notebook.", "has", "have", "are", "were"),
        ("Neither Ravi nor his friends ___ present.", "are", "is", "was", "has"),
        ("Either the teacher or the students ___ responsible.", "are", "is", "was", "has"),
        ("The quality of these products ___ excellent.", "is", "are", "were", "have"),
        ("One of my friends ___ in Japan.", "lives", "live", "living", "have"),
        ("The news ___ surprising.", "is", "are", "were", "have"),
        ("Mathematics ___ my favourite subject.", "is", "are", "were", "have"),
        ("A number of students ___ absent today.", "are", "is", "was", "has"),
        ("The number of applicants ___ increasing.", "is", "are", "were", "have"),
        ("Neither of the answers ___ correct.", "is", "are", "were", "have"),
        ("Everyone in the class ___ completed the assignment.", "has", "have", "are", "were"),
        ("The committee ___ divided in their opinions.", "are", "is", "has", "was"),
        ("Bread and butter ___ my usual breakfast.", "is", "are", "were", "have"),
        ("The poet and philosopher ___ arrived.", "has", "have", "are", "were"),
        ("The captain, along with the players, ___ ready.", "is", "are", "were", "have"),
        ("Neither the manager nor the employees ___ available.", "are", "is", "was", "has"),
        ("Ten kilometres ___ a long distance to walk.", "is", "are", "were", "have"),
        ("The furniture in these rooms ___ expensive.", "is", "are", "were", "have"),
        ("There ___ many reasons for his decision.", "are", "is", "was", "has"),
        ("There ___ a book on the table.", "is", "are", "were", "have"),
        ("Every boy and girl ___ invited.", "was", "were", "are", "have"),
        ("The police ___ investigating the case.", "are", "is", "was", "has"),
        ("The scissors ___ on the desk.", "are", "is", "was", "has"),
        ("My family ___ going on a holiday.", "is", "are", "were", "have"),
        ("Some of the water ___ spilled.", "has", "have", "are", "were"),
        ("Some of the students ___ absent.", "are", "is", "was", "has"),
        ("The principal, as well as the teachers, ___ attending.", "is", "are", "were", "have"),
        ("More than one student ___ applied for the scholarship.", "has", "have", "are", "were"),
        ("The rich ___ not always happy.", "are", "is", "was", "has"),
        ("Neither of my parents ___ at home.", "is", "are", "were", "have")
    ],

    "Hard": [
        ("Not only the students but also the teacher ___ responsible.", "is", "are", "were", "have"),
        ("Not only the teacher but also the students ___ responsible.", "are", "is", "was", "has"),
        ("The principal and secretary ___ attending the meeting.", "are", "is", "was", "has"),
        ("The principal and secretary of the school ___ attending the meeting.", "is", "are", "were", "have"),
        ("Many a student ___ failed to submit the assignment.", "has", "have", "are", "were"),
        ("More than one person ___ complained about the service.", "has", "have", "are", "were"),
        ("The majority of the students ___ passed the examination.", "have", "has", "is", "was"),
        ("The majority of the work ___ completed.", "is", "are", "were", "have"),
        ("A pair of shoes ___ lying near the door.", "is", "are", "were", "have"),
        ("The cattle ___ grazing in the field.", "are", "is", "was", "has"),
        ("What he says and what he does ___ different.", "are", "is", "was", "has"),
        ("To read and write ___ essential skills.", "are", "is", "was", "has"),
        ("Swimming in the sea ___ enjoyable.", "is", "are", "were", "have"),
        ("The United States ___ a large country.", "is", "are", "were", "have"),
        ("The Arabian Nights ___ an interesting book.", "is", "are", "were", "have"),
        ("Five years ___ a long time to wait.", "is", "are", "were", "have"),
        ("The proceeds from the sale ___ donated to charity.", "were", "was", "is", "has"),
        ("None of the information ___ accurate.", "is", "are", "were", "have"),
        ("None of the students ___ completed the test.", "have", "has", "is", "was"),
        ("The team ___ wearing their new uniforms.", "are", "is", "was", "has"),
        ("The jury ___ delivered its verdict.", "has", "have", "are", "were"),
        ("Either the players or the coach ___ responsible.", "is", "are", "were", "have"),
        ("Either the coach or the players ___ responsible.", "are", "is", "was", "has"),
        ("The poet, together with his friends, ___ arrived.", "has", "have", "are", "were"),
        ("Every one of these books ___ useful.", "is", "are", "were", "have"),
        ("The wages of sin ___ death.", "is", "are", "were", "have"),
        ("A great deal of money ___ spent on the project.", "was", "were", "are", "have"),
        ("The committee members ___ arguing among themselves.", "are", "is", "was", "has"),
        ("The data ___ collected from several sources.", "were", "was", "is", "has"),
        ("The criteria for selection ___ clearly defined.", "are", "is", "was", "has")
    ]
}


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    try:
        cur.execute("""
            SELECT id FROM lessons
            WHERE title = ? AND topic = ?
        """, ("Subject-Verb Agreement", "English"))

        result = cur.fetchone()

        if not result:
            raise Exception("Subject-Verb Agreement lesson not found.")

        lesson_id = result[0]
        print(f"Lesson found: ID {lesson_id}")

        for difficulty in ["Easy", "Medium", "Hard"]:

            cur.execute("""
                SELECT id FROM quizzes
                WHERE lesson_id = ?
                AND LOWER(difficulty) = LOWER(?)
            """, (lesson_id, difficulty))

            quiz = cur.fetchone()

            if quiz:
                quiz_id = quiz[0]
            else:
                cur.execute("""
                    INSERT INTO quizzes (lesson_id, title, difficulty)
                    VALUES (?, ?, ?)
                """, (
                    lesson_id,
                    f"Subject-Verb Agreement - {difficulty}",
                    difficulty
                ))
                quiz_id = cur.lastrowid

            cur.execute("""
                SELECT question FROM questions WHERE quiz_id = ?
            """, (quiz_id,))

            existing = {row[0] for row in cur.fetchall()}

            cur.execute("""
                SELECT COUNT(*) FROM questions WHERE quiz_id = ?
            """, (quiz_id,))

            count = cur.fetchone()[0]

            if count > 30:
                raise Exception(
                    f"{difficulty} already has {count} questions. "
                    "Check the database before continuing."
                )

            inserted = 0

            for index, item in enumerate(BANK[difficulty], start=1):

                if count >= 30:
                    break

                question_text, answer, wrong1, wrong2, wrong3 = item

                question = (
                    f"Subject-Verb Agreement {difficulty} {index}: "
                    f"{question_text}"
                )

                original = question
                version = 2

                while question in existing:
                    question = f"{original} (Version {version})"
                    version += 1

                options = [answer, wrong1, wrong2, wrong3]

                if len(set(options)) != 4:
                    raise Exception(f"Duplicate options: {question}")

                random.shuffle(options)
                correct = "ABCD"[options.index(answer)]

                cur.execute("""
                    INSERT INTO questions (
                        quiz_id, question, option_a, option_b,
                        option_c, option_d, correct_answer
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    quiz_id, question,
                    options[0], options[1], options[2], options[3],
                    correct
                ))

                existing.add(question)
                count += 1
                inserted += 1

            cur.execute("""
                SELECT COUNT(*) FROM questions WHERE quiz_id = ?
            """, (quiz_id,))

            final_count = cur.fetchone()[0]

            print(
                f"{difficulty}: {final_count}/30 "
                f"({inserted} newly inserted)"
            )

            if final_count != 30:
                raise Exception(
                    f"{difficulty} has {final_count} questions instead of 30."
                )

        con.commit()
        print("\nSUCCESS! Subject-Verb Agreement completed: 90/90 MCQs.")

    except Exception as error:
        con.rollback()
        print(f"\nERROR: {error}")
        raise

    finally:
        con.close()


if __name__ == "__main__":
    main()
