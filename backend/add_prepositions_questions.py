
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

BANK = {
    "Easy": [
        ("The book is ___ the table.", "on", "in", "at", "by"),
        ("She lives ___ Bengaluru.", "in", "on", "at", "by"),
        ("The cat is hiding ___ the bed.", "under", "over", "between", "beside"),
        ("We go to school ___ bus.", "by", "in", "on", "with"),
        ("The meeting starts ___ 10 AM.", "at", "in", "on", "by"),
        ("My birthday is ___ Monday.", "on", "in", "at", "by"),
        ("He was born ___ July.", "in", "on", "at", "by"),
        ("The keys are ___ the drawer.", "in", "on", "at", "over"),
        ("She is sitting ___ her mother.", "beside", "between", "through", "above"),
        ("The bird flew ___ the window.", "through", "under", "between", "beside"),
        ("He walked ___ the bridge.", "across", "among", "inside", "below"),
        ("The school is ___ the bank and the hospital.", "between", "among", "over", "through"),
        ("The picture is hanging ___ the wall.", "on", "in", "at", "under"),
        ("She arrived ___ the airport early.", "at", "in", "on", "by"),
        ("The children are playing ___ the garden.", "in", "on", "at", "above"),
        ("He jumped ___ the swimming pool.", "into", "onto", "above", "between"),
        ("The plane is flying ___ the clouds.", "above", "under", "inside", "between"),
        ("She received a gift ___ her friend.", "from", "to", "by", "at"),
        ("The train travels ___ Mangaluru to Bengaluru.", "from", "at", "on", "with"),
        ("He is good ___ mathematics.", "at", "in", "on", "by"),
        ("We waited ___ the bus stop.", "at", "in", "on", "under"),
        ("The dog ran ___ the road.", "across", "between", "inside", "above"),
        ("She put the flowers ___ a vase.", "in", "on", "at", "over"),
        ("The shop is opposite ___ the school.", "to", "at", "by", "from"),
        ("He is standing ___ the door.", "near", "between", "through", "above"),
        ("The ball rolled ___ the chair.", "under", "over", "between", "inside"),
        ("I will meet you ___ the evening.", "in", "on", "at", "by"),
        ("She has been waiting ___ two hours.", "for", "since", "at", "by"),
        ("He came ___ his brother.", "with", "from", "at", "by"),
        ("The children ran ___ the classroom.", "into", "between", "above", "under")
    ],

    "Medium": [
        ("She has lived here ___ 2020.", "since", "for", "during", "by"),
        ("He has been studying ___ three hours.", "for", "since", "from", "at"),
        ("The train arrived ___ time.", "on", "in", "at", "by"),
        ("She completed the assignment ___ the deadline.", "before", "between", "among", "during"),
        ("The manager divided the work ___ the employees.", "among", "between", "beside", "across"),
        ("The agreement was made ___ the two companies.", "between", "among", "within", "through"),
        ("He is interested ___ learning Japanese.", "in", "on", "at", "for"),
        ("She is responsible ___ managing the team.", "for", "of", "with", "at"),
        ("The students were absent ___ class yesterday.", "from", "at", "in", "by"),
        ("He apologized ___ his mistake.", "for", "with", "at", "from"),
        ("She is afraid ___ spiders.", "of", "from", "with", "by"),
        ("The teacher congratulated him ___ his success.", "on", "for", "at", "with"),
        ("He insisted ___ paying the bill.", "on", "at", "in", "for"),
        ("The book was written ___ a famous author.", "by", "with", "from", "at"),
        ("The room was filled ___ smoke.", "with", "by", "from", "at"),
        ("She prefers tea ___ coffee.", "to", "than", "over", "from"),
        ("He is senior ___ me in the company.", "to", "than", "from", "with"),
        ("The children were excited ___ the trip.", "about", "with", "at", "from"),
        ("We should protect the environment ___ pollution.", "from", "by", "with", "at"),
        ("He succeeded ___ solving the problem.", "in", "at", "on", "for"),
        ("She is capable ___ handling difficult situations.", "of", "for", "with", "at"),
        ("The match was postponed ___ heavy rain.", "because of", "although", "despite of", "instead"),
        ("He walked ___ the tunnel.", "through", "across", "among", "between"),
        ("The temperature dropped ___ zero.", "below", "above", "over", "between"),
        ("She divided the cake ___ four equal parts.", "into", "in", "among", "between"),
        ("He has been working here ___ last June.", "since", "for", "during", "from"),
        ("The office is open ___ Monday to Friday.", "from", "since", "between", "during"),
        ("She was praised ___ her excellent performance.", "for", "at", "with", "from"),
        ("He is married ___ a doctor.", "to", "with", "by", "for"),
        ("The students discussed the topic ___ detail.", "in", "on", "at", "by")
    ],

    "Hard": [
        ("He has a strong preference ___ classical music.", "for", "of", "with", "at"),
        ("The company complied ___ all safety regulations.", "with", "to", "for", "at"),
        ("She is accustomed ___ waking up early.", "to", "with", "for", "at"),
        ("The manager is responsible ___ the final decision.", "for", "of", "with", "at"),
        ("He was accused ___ stealing confidential information.", "of", "for", "with", "at"),
        ("The new policy is applicable ___ all employees.", "to", "for", "with", "at"),
        ("She has no objection ___ working late.", "to", "for", "with", "at"),
        ("The success of the project depends ___ teamwork.", "on", "in", "at", "for"),
        ("He was prevented ___ entering the building.", "from", "of", "by", "with"),
        ("The teacher was pleased ___ the students' progress.", "with", "for", "at", "from"),
        ("She has great admiration ___ her mentor.", "for", "of", "with", "at"),
        ("The results are consistent ___ our expectations.", "with", "to", "for", "at"),
        ("He is indifferent ___ criticism.", "to", "with", "for", "at"),
        ("The committee consists ___ ten members.", "of", "from", "with", "by"),
        ("She is proficient ___ several programming languages.", "in", "at", "on", "for"),
        ("The decision was made ___ consultation with the team.", "in", "on", "at", "by"),
        ("He was deprived ___ his basic rights.", "of", "from", "with", "by"),
        ("The project was completed ___ spite of several difficulties.", "in", "on", "at", "by"),
        ("She is keen ___ pursuing higher education.", "on", "in", "at", "for"),
        ("The manager attributed the success ___ effective teamwork.", "to", "for", "with", "at"),
        ("He is eligible ___ the scholarship.", "for", "to", "with", "at"),
        ("The new system is superior ___ the old one.", "to", "than", "from", "with"),
        ("She refrained ___ making unnecessary comments.", "from", "of", "with", "at"),
        ("The witness gave evidence ___ the accused.", "against", "for", "with", "at"),
        ("He was congratulated ___ winning the competition.", "on", "for", "at", "with"),
        ("The final decision rests ___ the director.", "with", "on", "at", "for"),
        ("She takes pride ___ her achievements.", "in", "on", "at", "for"),
        ("The company invested heavily ___ research and development.", "in", "on", "at", "for"),
        ("He was unaware ___ the changes in the schedule.", "of", "about", "with", "from"),
        ("The speaker spoke ___ behalf of the entire team.", "on", "in", "at", "by")
    ]
}


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    try:
        # Find the Prepositions lesson
        cur.execute("""
            SELECT id FROM lessons
            WHERE title = ? AND topic = ?
        """, ("Prepositions", "English"))

        result = cur.fetchone()

        if not result:
            raise Exception("Prepositions lesson not found.")

        lesson_id = result[0]
        print(f"Prepositions lesson found: ID {lesson_id}")

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
                """, (lesson_id, f"Prepositions - {difficulty}", difficulty))

                quiz_id = cur.lastrowid

            # Get existing questions
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
                    "Please check the database."
                )

            inserted = 0

            for index, item in enumerate(BANK[difficulty], start=1):

                if current_count >= 30:
                    break

                question_text, answer, wrong1, wrong2, wrong3 = item

                question = (
                    f"Prepositions MCQ {difficulty} {index}: {question_text}"
                )

                # Ensure unique question text
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

            # Verify final count
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
        print("\nSUCCESS! Prepositions completed: 90/90 MCQs.")

    except Exception as error:
        con.rollback()
        print(f"\nERROR: {error}")
        raise

    finally:
        con.close()


if __name__ == "__main__":
    main()
