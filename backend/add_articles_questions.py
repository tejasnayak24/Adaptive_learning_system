
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

# Format: (question, correct answer, wrong option 1, wrong option 2, wrong option 3)

BANK = {
    "Easy": [
        ("I ate ___ apple.", "an", "a", "the", "no article"),
        ("She is ___ teacher.", "a", "an", "the", "no article"),
        ("He bought ___ umbrella.", "an", "a", "the", "no article"),
        ("The sun is ___ star.", "a", "an", "the", "no article"),
        ("I saw ___ elephant at the zoo.", "an", "a", "the", "no article"),
        ("She has ___ beautiful dress.", "a", "an", "the", "no article"),
        ("He is ___ honest man.", "an", "a", "the", "no article"),
        ("I need ___ pen to write.", "a", "an", "the", "no article"),
        ("___ moon looks beautiful tonight.", "The", "A", "An", "No article"),
        ("She is reading ___ interesting book.", "an", "a", "the", "no article"),
        ("He lives in ___ small house.", "a", "an", "the", "no article"),
        ("I saw ___ owl on the tree.", "an", "a", "the", "no article"),
        ("This is ___ orange.", "an", "a", "the", "no article"),
        ("He is ___ university student.", "a", "an", "the", "no article"),
        ("She bought ___ new bag.", "a", "an", "the", "no article"),
        ("___ Earth moves around the Sun.", "The", "A", "An", "No article"),
        ("I have ___ idea.", "an", "a", "the", "no article"),
        ("He ate ___ banana.", "a", "an", "the", "no article"),
        ("She is ___ engineer.", "an", "a", "the", "no article"),
        ("We saw ___ tiger in the forest.", "a", "an", "the", "no article"),
        ("He is ___ best player in the team.", "the", "a", "an", "no article"),
        ("I found ___ coin on the road.", "a", "an", "the", "no article"),
        ("She wants to become ___ artist.", "an", "a", "the", "no article"),
        ("He gave me ___ gift.", "a", "an", "the", "no article"),
        ("___ sky is blue.", "The", "A", "An", "No article"),
        ("I saw ___ eagle flying.", "an", "a", "the", "no article"),
        ("She has ___ cat.", "a", "an", "the", "no article"),
        ("He is ___ intelligent boy.", "an", "a", "the", "no article"),
        ("Please close ___ door.", "the", "a", "an", "no article"),
        ("My father reads ___ newspaper every morning.", "a", "an", "the", "no article")
    ],

    "Medium": [
        ("She is ___ MBA graduate.", "an", "a", "the", "no article"),
        ("He is ___ European citizen.", "a", "an", "the", "no article"),
        ("We visited ___ Taj Mahal last year.", "the", "a", "an", "no article"),
        ("She plays ___ piano very well.", "the", "a", "an", "no article"),
        ("He goes to ___ school every day.", "no article", "the", "a", "an"),
        ("___ Ganga is a sacred river.", "The", "A", "An", "No article"),
        ("She wants to become ___ IAS officer.", "an", "a", "the", "no article"),
        ("He is ___ one-eyed man.", "a", "an", "the", "no article"),
        ("I met ___ old friend yesterday.", "an", "a", "the", "no article"),
        ("Mount Everest is ___ highest mountain in the world.", "the", "a", "an", "no article"),
        ("She speaks ___ French fluently.", "no article", "the", "a", "an"),
        ("He was elected ___ president of the club.", "the", "a", "an", "no article"),
        ("We had ___ lunch at noon.", "no article", "a", "an", "the"),
        ("She is ___ heir to the property.", "an", "a", "the", "no article"),
        ("He returned after ___ hour.", "an", "a", "the", "no article"),
        ("___ rich should help the poor.", "The", "A", "An", "No article"),
        ("She lives in ___ United States.", "the", "a", "an", "no article"),
        ("He is ___ unique person.", "a", "an", "the", "no article"),
        ("I usually travel by ___ bus.", "no article", "the", "a", "an"),
        ("This is ___ most interesting story I have read.", "the", "a", "an", "no article"),
        ("She was born in ___ April.", "no article", "the", "a", "an"),
        ("He is ___ eldest son in the family.", "the", "a", "an", "no article"),
        ("They crossed ___ Pacific Ocean.", "the", "a", "an", "no article"),
        ("She studies at ___ university in Bengaluru.", "a", "an", "the", "no article"),
        ("He became ___ doctor after graduation.", "a", "an", "the", "no article"),
        ("___ Himalayas are covered with snow.", "The", "A", "An", "No article"),
        ("I saw him ___ day before yesterday.", "the", "a", "an", "no article"),
        ("She is ___ honest and hardworking student.", "an", "a", "the", "no article"),
        ("He is good at playing ___ cricket.", "no article", "the", "a", "an"),
        ("We stayed at ___ hotel near the airport.", "a", "an", "the", "no article")
    ],

    "Hard": [
        ("He is ___ man who helped me yesterday.", "the", "a", "an", "no article"),
        ("___ more you practise, ___ better you become.", "The, the", "A, a", "An, the", "No article, the"),
        ("She was appointed ___ chairperson of the committee.", "no article", "a", "an", "the"),
        ("He is ___ Shakespeare of our school.", "the", "a", "an", "no article"),
        ("This is ___ same book that I borrowed yesterday.", "the", "a", "an", "no article"),
        ("He has ___ little knowledge of mathematics.", "a", "the", "an", "no article"),
        ("There is ___ little hope of recovery.", "a", "the", "an", "no article"),
        ("___ number of students has increased.", "The", "A", "An", "No article"),
        ("She is ___ only person who knows the answer.", "the", "a", "an", "no article"),
        ("He was sent to ___ prison for theft.", "no article", "the", "a", "an"),
        ("The injured man was taken to ___ hospital.", "the", "a", "an", "no article"),
        ("She plays ___ violin in an orchestra.", "the", "a", "an", "no article"),
        ("He is ___ first person to arrive.", "the", "a", "an", "no article"),
        ("___ French are known for their cuisine.", "The", "A", "An", "No article"),
        ("He earns ___ hundred rupees a day.", "a", "an", "the", "no article"),
        ("She has ___ MBA degree from a reputed college.", "an", "a", "the", "no article"),
        ("He is ___ man of great wisdom.", "a", "an", "the", "no article"),
        ("___ gold is a precious metal.", "No article", "The", "A", "An"),
        ("She went to ___ bed early last night.", "no article", "the", "a", "an"),
        ("The train travels at ___ speed of 100 kilometres per hour.", "a", "an", "the", "no article"),
        ("He is ___ tallest boy in his class.", "the", "a", "an", "no article"),
        ("We visited ___ Netherlands during our holiday.", "the", "a", "an", "no article"),
        ("She has been waiting for ___ hour and a half.", "an", "a", "the", "no article"),
        ("He is ___ European who works in India.", "a", "an", "the", "no article"),
        ("___ Mount Kilimanjaro is in Africa.", "No article", "The", "A", "An"),
        ("He was the first person to climb ___ Mount Everest.", "no article", "the", "a", "an"),
        ("She is ___ woman of remarkable courage.", "a", "an", "the", "no article"),
        ("___ elderly need special care and attention.", "The", "A", "An", "No article"),
        ("He went to ___ school to meet the principal.", "the", "a", "an", "no article"),
        ("She has ___ better understanding of the subject now.", "a", "an", "the", "no article")
    ]
}


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    try:
        # Find the Articles lesson
        cur.execute("""
            SELECT id FROM lessons
            WHERE title = ? AND topic = ?
        """, ("Articles", "English"))

        result = cur.fetchone()

        if not result:
            raise Exception("Articles lesson was not found in the lessons table.")

        lesson_id = result[0]
        print(f"Articles lesson found: ID {lesson_id}")

        for difficulty in ["Easy", "Medium", "Hard"]:

            # Find or create the quiz
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
                """, (lesson_id, f"Articles - {difficulty}", difficulty))

                quiz_id = cur.lastrowid

            # Check existing questions
            cur.execute("""
                SELECT question FROM questions
                WHERE quiz_id = ?
            """, (quiz_id,))

            existing_questions = {row[0] for row in cur.fetchall()}

            cur.execute("""
                SELECT COUNT(*) FROM questions
                WHERE quiz_id = ?
            """, (quiz_id,))

            current_count = cur.fetchone()[0]

            if current_count > 30:
                raise Exception(
                    f"{difficulty} already has {current_count} questions. "
                    "Please check the database before continuing."
                )

            # Insert questions until exactly 30 are available
            inserted = 0

            for index, item in enumerate(BANK[difficulty], start=1):

                if current_count >= 30:
                    break

                question_text, answer, wrong1, wrong2, wrong3 = item

                question = f"Articles MCQ {difficulty} {index}: {question_text}"

                # Ensure a unique question text
                original_question = question
                suffix = 2

                while question in existing_questions:
                    question = f"{original_question} (Version {suffix})"
                    suffix += 1

                options = [answer, wrong1, wrong2, wrong3]
                random.shuffle(options)

                correct_answer = "ABCD"[options.index(answer)]

                cur.execute("""
                    INSERT INTO questions (
                        quiz_id,
                        question,
                        option_a,
                        option_b,
                        option_c,
                        option_d,
                        correct_answer
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    quiz_id,
                    question,
                    options[0],
                    options[1],
                    options[2],
                    options[3],
                    correct_answer
                ))

                existing_questions.add(question)
                current_count += 1
                inserted += 1

            # Final verification
            cur.execute("""
                SELECT COUNT(*) FROM questions
                WHERE quiz_id = ?
            """, (quiz_id,))

            final_count = cur.fetchone()[0]

            print(
                f"{difficulty}: {final_count}/30 questions "
                f"({inserted} newly inserted)"
            )

            if final_count != 30:
                raise Exception(
                    f"{difficulty} has {final_count} questions instead of 30."
                )

        con.commit()
        print("\nSUCCESS! Articles completed: 90/90 MCQs.")

    except Exception as error:
        con.rollback()
        print(f"\nERROR: {error}")
        raise

    finally:
        con.close()


if __name__ == "__main__":
    main()
