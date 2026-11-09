
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

BANK = {
    "Easy": [
        ("___! We won the match.", "Hurrah", "Alas", "Oops", "Hush"),
        ("___! I hurt my finger.", "Ouch", "Wow", "Bravo", "Hurray"),
        ("___! What a beautiful flower.", "Wow", "Alas", "Oops", "Hush"),
        ("___! I forgot my homework.", "Oops", "Bravo", "Hurrah", "Ahoy"),
        ("___! May I come in?", "Excuse me", "Hurrah", "Alas", "Wow"),
        ("___! That was a wonderful performance.", "Bravo", "Ouch", "Hush", "Alas"),
        ("___! We lost the final match.", "Alas", "Hurrah", "Wow", "Bravo"),
        ("___! Please be quiet.", "Hush", "Wow", "Hurrah", "Ouch"),
        ("___! I have passed the examination.", "Hurrah", "Alas", "Oops", "Oh dear"),
        ("___! That is a lovely dress.", "Wow", "Ouch", "Hush", "Alas"),
        ("___! I dropped my phone.", "Oops", "Bravo", "Hurrah", "Ahoy"),
        ("___! What a terrible accident.", "Oh dear", "Hurrah", "Bravo", "Wow"),
        ("___! I did not expect to see you here.", "Oh", "Hush", "Bravo", "Hurrah"),
        ("___! The baby is sleeping.", "Hush", "Wow", "Ouch", "Alas"),
        ("___! We are going on a holiday.", "Yippee", "Alas", "Oops", "Hush"),
        ("___! You did an excellent job.", "Bravo", "Ouch", "Alas", "Oops"),
        ("___! I cannot believe this happened.", "Oh", "Hush", "Hurrah", "Bravo"),
        ("___! That was close.", "Phew", "Alas", "Wow", "Hush"),
        ("___! Someone is at the door.", "Ah", "Ouch", "Hurrah", "Bravo"),
        ("___! I am so happy to meet you.", "Hello", "Alas", "Oops", "Hush"),
        ("___! What a shame.", "Alas", "Hurrah", "Yippee", "Wow"),
        ("___! Be careful while crossing the road.", "Hey", "Hurrah", "Bravo", "Alas"),
        ("___! I found my lost wallet.", "Aha", "Ouch", "Hush", "Alas"),
        ("___! We have finally reached the top.", "Phew", "Oops", "Alas", "Hush"),
        ("___! That tastes delicious.", "Mmm", "Ouch", "Alas", "Hush"),
        ("___! Stop making noise.", "Hey", "Hurrah", "Bravo", "Yippee"),
        ("___! I made a silly mistake.", "Oops", "Wow", "Bravo", "Hurrah"),
        ("___! What a pleasant surprise.", "Oh", "Alas", "Ouch", "Hush"),
        ("___! Welcome to our school.", "Hello", "Ouch", "Alas", "Oops"),
        ("___! Our team has won the trophy.", "Hurray", "Alas", "Hush", "Oops")
    ],

    "Medium": [
        ("___! I never expected such a result.", "Good heavens", "Bravo", "Hush", "Yippee"),
        ("___! How foolish of me to forget the keys.", "Dear me", "Hurrah", "Bravo", "Ahoy"),
        ("___! The poor man has lost everything.", "Alas", "Yippee", "Bravo", "Wow"),
        ("___! You have completed the project perfectly.", "Excellent", "Ouch", "Hush", "Alas"),
        ("___! I have finally solved the puzzle.", "Aha", "Alas", "Oops", "Hush"),
        ("___! What an extraordinary achievement.", "Wonderful", "Ouch", "Alas", "Hush"),
        ("___! I cannot believe how quickly time passed.", "Oh", "Bravo", "Hush", "Yippee"),
        ("___! The poor child is crying.", "Oh dear", "Hurrah", "Bravo", "Wow"),
        ("___! We have escaped the danger.", "Thank goodness", "Alas", "Oops", "Hush"),
        ("___! I accidentally broke the glass.", "Oops", "Bravo", "Hurrah", "Welcome"),
        ("___! You should not speak so rudely.", "Hey", "Hurrah", "Yippee", "Bravo"),
        ("___! What a magnificent building.", "Wow", "Alas", "Ouch", "Hush"),
        ("___! I wish I had studied harder.", "If only", "Bravo", "Hurrah", "Ahoy"),
        ("___! The concert was absolutely amazing.", "Bravo", "Alas", "Oops", "Hush"),
        ("___! I am exhausted after the long journey.", "Phew", "Yippee", "Bravo", "Ahoy"),
        ("___! Someone has stolen my bicycle.", "Oh no", "Hurrah", "Bravo", "Wow"),
        ("___! That is exactly what I was looking for.", "Aha", "Alas", "Ouch", "Hush"),
        ("___! I have received the scholarship.", "Hurray", "Alas", "Oops", "Oh dear"),
        ("___! The examination was much harder than expected.", "Goodness", "Bravo", "Yippee", "Ahoy"),
        ("___! Please listen to me carefully.", "Hey", "Hurrah", "Alas", "Wow"),
        ("___! I am delighted to see you again.", "Oh", "Ouch", "Hush", "Alas"),
        ("___! What a disappointing performance.", "Alas", "Bravo", "Yippee", "Hurrah"),
        ("___! I have forgotten his name again.", "Dear me", "Bravo", "Hurray", "Ahoy"),
        ("___! That was an incredibly close competition.", "Phew", "Alas", "Oops", "Hush"),
        ("___! Congratulations on your success.", "Bravo", "Ouch", "Alas", "Hush"),
        ("___! I have never seen such a beautiful sunset.", "Oh", "Oops", "Ouch", "Hush"),
        ("___! The dog is chasing us.", "Help", "Bravo", "Hurrah", "Yippee"),
        ("___! We have reached our destination safely.", "Thank goodness", "Alas", "Oops", "Hush"),
        ("___! I accidentally sent the wrong message.", "Oops", "Bravo", "Hurrah", "Ahoy"),
        ("___! What a wonderful opportunity.", "How exciting", "Alas", "Ouch", "Hush")
    ],

    "Hard": [
        ("___! Would that I had accepted the offer.", "If only", "Hurrah", "Bravo", "Ahoy"),
        ("___! The entire village was destroyed by the flood.", "Alas", "Yippee", "Bravo", "Wow"),
        ("___! I have discovered the missing document.", "Aha", "Ouch", "Hush", "Alas"),
        ("___! Heaven forbid that such a tragedy should happen again.", "Heaven forbid", "Hurrah", "Bravo", "Yippee"),
        ("___! How unfortunate that we missed the opportunity.", "What a pity", "Bravo", "Hurray", "Wow"),
        ("___! I am relieved that everyone is safe.", "Thank goodness", "Alas", "Oops", "Hush"),
        ("___! The speaker has delivered an outstanding address.", "Bravo", "Ouch", "Alas", "Oops"),
        ("___! I wish the situation were different.", "If only", "Hurrah", "Wow", "Ahoy"),
        ("___! The sudden announcement shocked everyone.", "Good heavens", "Yippee", "Bravo", "Hush"),
        ("___! I cannot tolerate this behaviour any longer.", "Enough", "Hurrah", "Bravo", "Wow"),
        ("___! The mystery has finally been solved.", "Aha", "Alas", "Ouch", "Hush"),
        ("___! What a remarkable display of courage.", "Indeed", "Ouch", "Alas", "Oops"),
        ("___! The old monument has been demolished.", "Alas", "Yippee", "Bravo", "Hurray"),
        ("___! May success follow you wherever you go.", "Good luck", "Ouch", "Alas", "Hush"),
        ("___! I never imagined that he would resign.", "Well", "Bravo", "Hurrah", "Yippee"),
        ("___! The child has fallen into the water.", "Help", "Bravo", "Hurray", "Wow"),
        ("___! What an astonishing coincidence.", "Goodness", "Ouch", "Alas", "Hush"),
        ("___! I regret not taking your advice.", "If only", "Hurrah", "Bravo", "Ahoy"),
        ("___! The team has achieved an extraordinary victory.", "Hurray", "Alas", "Oops", "Oh dear"),
        ("___! I have been waiting for hours.", "Good grief", "Bravo", "Yippee", "Hush"),
        ("___! The results are finally out.", "At last", "Ouch", "Alas", "Hush"),
        ("___! How unfortunate that the event was cancelled.", "What a shame", "Bravo", "Hurrah", "Wow"),
        ("___! I am grateful that nobody was hurt.", "Thank goodness", "Alas", "Oops", "Hush"),
        ("___! The audience gave the performer a standing ovation.", "Bravo", "Ouch", "Alas", "Oops"),
        ("___! I have made a terrible error.", "Oh dear", "Hurrah", "Bravo", "Yippee"),
        ("___! The plan has worked exactly as expected.", "Excellent", "Alas", "Ouch", "Hush"),
        ("___! I cannot believe that we have won.", "Good heavens", "Oops", "Alas", "Hush"),
        ("___! The poor family has lost its home.", "Alas", "Yippee", "Bravo", "Wow"),
        ("___! What a relief to finish the examination.", "Phew", "Alas", "Oops", "Hush"),
        ("___! May you have a prosperous future.", "Best wishes", "Ouch", "Alas", "Oops")
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
        """, ("Interjections", "English"))

        result = cur.fetchone()

        if not result:
            raise Exception("Interjections lesson not found.")

        lesson_id = result[0]
        print(f"Interjections lesson found: ID {lesson_id}")

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
                """, (lesson_id, f"Interjections - {difficulty}", difficulty))

                quiz_id = cur.lastrowid

            cur.execute("""
                SELECT question FROM questions WHERE quiz_id = ?
            """, (quiz_id,))

            existing_questions = {row[0] for row in cur.fetchall()}

            cur.execute("""
                SELECT COUNT(*) FROM questions WHERE quiz_id = ?
            """, (quiz_id,))

            current_count = cur.fetchone()[0]

            if current_count > 30:
                raise Exception(
                    f"{difficulty} already has {current_count} questions. "
                    "Please check the database."
                )

            inserted = 0

            for index, item in enumerate(BANK[difficulty], start=1):

                if current_count >= 30:
                    break

                question_text, answer, wrong1, wrong2, wrong3 = item

                question = (
                    f"Interjections MCQ {difficulty} {index}: {question_text}"
                )

                original_question = question
                version = 2

                while question in existing_questions:
                    question = f"{original_question} (Version {version})"
                    version += 1

                options = [answer, wrong1, wrong2, wrong3]

                if len(set(options)) != 4:
                    raise Exception(f"Duplicate options found: {question}")

                random.shuffle(options)
                correct_answer = "ABCD"[options.index(answer)]

                cur.execute("""
                    INSERT INTO questions (
                        quiz_id, question, option_a, option_b,
                        option_c, option_d, correct_answer
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    quiz_id, question,
                    options[0], options[1], options[2], options[3],
                    correct_answer
                ))

                existing_questions.add(question)
                current_count += 1
                inserted += 1

            cur.execute("""
                SELECT COUNT(*) FROM questions WHERE quiz_id = ?
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
        print("\nSUCCESS! Interjections completed: 90/90 MCQs.")

    except Exception as error:
        con.rollback()
        print(f"\nERROR: {error}")
        raise

    finally:
        con.close()


if __name__ == "__main__":
    main()
