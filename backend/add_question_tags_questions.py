
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

BANK = {
    "Easy": [
        ("You are a student, _____?", "aren't you", "are you", "isn't you", "don't you"),
        ("She is happy, _____?", "isn't she", "is she", "doesn't she", "aren't she"),
        ("They are playing, _____?", "aren't they", "are they", "isn't they", "don't they"),
        ("He isn't tired, _____?", "is he", "isn't he", "does he", "doesn't he"),
        ("We can swim, _____?", "can't we", "can we", "do we", "don't we"),
        ("You like coffee, _____?", "don't you", "do you", "aren't you", "didn't you"),
        ("She doesn't sing, _____?", "does she", "doesn't she", "is she", "isn't she"),
        ("It is raining, _____?", "isn't it", "is it", "doesn't it", "aren't it"),
        ("They went home, _____?", "didn't they", "did they", "don't they", "weren't they"),
        ("He has a car, _____?", "doesn't he", "hasn't he", "isn't he", "didn't he"),
        ("You will come, _____?", "won't you", "will you", "don't you", "aren't you"),
        ("She can dance, _____?", "can't she", "can she", "doesn't she", "isn't she"),
        ("We aren't late, _____?", "are we", "aren't we", "do we", "don't we"),
        ("He plays football, _____?", "doesn't he", "does he", "isn't he", "didn't he"),
        ("They haven't arrived, _____?", "have they", "haven't they", "are they", "did they"),
        ("I am right, _____?", "aren't I", "am I", "isn't I", "don't I"),
        ("She was absent, _____?", "wasn't she", "was she", "isn't she", "didn't she"),
        ("You didn't call me, _____?", "did you", "didn't you", "do you", "don't you"),
        ("He is your brother, _____?", "isn't he", "is he", "doesn't he", "aren't he"),
        ("We should help them, _____?", "shouldn't we", "should we", "don't we", "aren't we"),
        ("The baby is sleeping, _____?", "isn't it", "is it", "doesn't it", "aren't they"),
        ("You haven't eaten, _____?", "have you", "haven't you", "did you", "are you"),
        ("She works here, _____?", "doesn't she", "does she", "isn't she", "didn't she"),
        ("They won't leave, _____?", "will they", "won't they", "do they", "are they"),
        ("He was working, _____?", "wasn't he", "was he", "didn't he", "isn't he"),
        ("We must hurry, _____?", "mustn't we", "must we", "don't we", "aren't we"),
        ("You are coming tomorrow, _____?", "aren't you", "are you", "won't you", "don't you"),
        ("She hasn't finished, _____?", "has she", "hasn't she", "does she", "is she"),
        ("It looks beautiful, _____?", "doesn't it", "does it", "isn't it", "didn't it"),
        ("They were happy, _____?", "weren't they", "were they", "aren't they", "didn't they")
    ],

    "Medium": [
        ("Let's go for a walk, _____?", "shall we", "will we", "do we", "aren't we"),
        ("Open the window, _____?", "will you", "do you", "are you", "shall you"),
        ("Don't make noise, _____?", "will you", "do you", "won't you", "are you"),
        ("Nobody called you, _____?", "did they", "didn't they", "did he", "does he"),
        ("Everyone enjoyed the party, _____?", "didn't they", "did he", "didn't he", "weren't they"),
        ("Nothing is impossible, _____?", "is it", "isn't it", "does it", "doesn't it"),
        ("Someone has taken my pen, _____?", "haven't they", "hasn't he", "have they", "didn't they"),
        ("There is a problem, _____?", "isn't there", "is there", "doesn't there", "aren't there"),
        ("There were many people, _____?", "weren't there", "were there", "wasn't there", "aren't there"),
        ("I am not disturbing you, _____?", "am I", "aren't I", "do I", "don't I"),
        ("You had finished the work, _____?", "hadn't you", "had you", "didn't you", "haven't you"),
        ("She used to live here, _____?", "didn't she", "usedn't she", "doesn't she", "wasn't she"),
        ("He hardly speaks, _____?", "does he", "doesn't he", "is he", "did he"),
        ("Few students understood the lesson, _____?", "did they", "didn't they", "were they", "weren't they"),
        ("A little progress has been made, _____?", "hasn't it", "has it", "hasn't they", "isn't it"),
        ("You would rather stay home, _____?", "wouldn't you", "would you", "hadn't you", "won't you"),
        ("She ought to apologise, _____?", "oughtn't she", "should she", "doesn't she", "isn't she"),
        ("He never tells lies, _____?", "does he", "doesn't he", "is he", "didn't he"),
        ("The train rarely arrives late, _____?", "does it", "doesn't it", "is it", "did it"),
        ("Neither of them came, _____?", "did they", "didn't they", "did he", "were they"),
        ("One should respect elders, _____?", "shouldn't one", "should one", "doesn't one", "shouldn't you"),
        ("You have to finish this today, _____?", "don't you", "haven't you", "have you", "aren't you"),
        ("She had better leave now, _____?", "hadn't she", "had she", "didn't she", "wouldn't she"),
        ("He needn't worry, _____?", "need he", "needn't he", "does he", "doesn't he"),
        ("They dare not challenge him, _____?", "dare they", "daren't they", "do they", "don't they"),
        ("I don't think he is honest, _____?", "is he", "isn't he", "do I", "don't I"),
        ("The students must obey the rules, _____?", "mustn't they", "must they", "don't they", "aren't they"),
        ("She has to attend the meeting, _____?", "doesn't she", "hasn't she", "has she", "isn't she"),
        ("You seldom visit us, _____?", "do you", "don't you", "are you", "didn't you"),
        ("Nothing happened yesterday, _____?", "did it", "didn't it", "does it", "was it")
    ],

    "Hard": [
        ("I am expected to attend the meeting, _____?", "aren't I", "am I", "isn't I", "don't I"),
        ("Let's not waste time, _____?", "shall we", "will we", "do we", "won't we"),
        ("Don't forget to lock the door, _____?", "will you", "do you", "won't you", "shall you"),
        ("Everybody has submitted the assignment, _____?", "haven't they", "hasn't he", "have they", "didn't they"),
        ("Neither of the answers is correct, _____?", "is it", "isn't it", "are they", "aren't they"),
        ("Few people knew the truth, _____?", "did they", "didn't they", "were they", "weren't they"),
        ("He scarcely visits his grandparents, _____?", "does he", "doesn't he", "is he", "did he"),
        ("She had no reason to complain, _____?", "did she", "didn't she", "had she", "hadn't she"),
        ("There used to be a cinema here, _____?", "didn't there", "usedn't there", "wasn't there", "doesn't there"),
        ("You would have helped me, _____?", "wouldn't you", "would you", "hadn't you", "didn't you"),
        ("The police have arrested the suspect, _____?", "haven't they", "hasn't it", "have they", "didn't they"),
        ("No one objected to the proposal, _____?", "did they", "didn't they", "did he", "was it"),
        ("All the information was correct, _____?", "wasn't it", "was it", "weren't they", "didn't it"),
        ("The news hasn't been confirmed, _____?", "has it", "hasn't it", "is it", "does it"),
        ("What he said was surprising, _____?", "wasn't it", "was it", "didn't he", "wasn't he"),
        ("One of the students has won the prize, _____?", "hasn't he or she", "haven't they", "has he", "didn't they"),
        ("I don't suppose she will agree, _____?", "will she", "won't she", "do I", "don't I"),
        ("I believe they have completed the project, _____?", "haven't they", "have they", "don't I", "do I"),
        ("He must have forgotten the appointment, _____?", "mustn't he", "must he", "hasn't he", "didn't he"),
        ("You needn't have brought all these books, _____?", "need you", "needn't you", "did you", "don't you"),
        ("She is rarely seen in public, _____?", "is she", "isn't she", "does she", "doesn't she"),
        ("There cannot be any mistake, _____?", "can there", "can't there", "is there", "isn't there"),
        ("The committee has not reached a decision, _____?", "has it", "hasn't it", "have they", "haven't they"),
        ("Neither Ravi nor his friends were invited, _____?", "were they", "weren't they", "was he", "wasn't he"),
        ("You'd better not tell anyone, _____?", "had you", "hadn't you", "would you", "wouldn't you"),
        ("Nothing could have been done earlier, _____?", "could it", "couldn't it", "could they", "couldn't they"),
        ("The number of applicants has increased, _____?", "hasn't it", "haven't they", "has it", "doesn't it"),
        ("A number of students were absent, _____?", "weren't they", "wasn't it", "were they", "didn't they"),
        ("He is the person who helped you, _____?", "isn't he", "is he", "didn't he", "wasn't he"),
        ("What a beautiful painting this is, _____?", "isn't it", "is it", "doesn't it", "wasn't it")
    ]
}


def main():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    try:
        cur.execute(
            "SELECT id FROM lessons WHERE title=? AND topic=?",
            ("Question Tags", "English")
        )

        row = cur.fetchone()

        if not row:
            raise Exception(
                "Lesson 'Question Tags' with topic 'English' was not found."
            )

        lesson_id = row[0]

        for difficulty, questions in BANK.items():

            if len(questions) != 30:
                raise Exception(
                    f"{difficulty} bank has {len(questions)} questions instead of 30."
                )

            cur.execute(
                "SELECT id FROM quizzes WHERE lesson_id=? AND difficulty=?",
                (lesson_id, difficulty)
            )

            quiz = cur.fetchone()

            if quiz:
                quiz_id = quiz[0]
            else:
                cur.execute(
                    """
                    INSERT INTO quizzes (lesson_id, title, difficulty)
                    VALUES (?, ?, ?)
                    """,
                    (
                        lesson_id,
                        f"Question Tags - {difficulty}",
                        difficulty
                    )
                )
                quiz_id = cur.lastrowid

            cur.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id=?",
                (quiz_id,)
            )

            existing = cur.fetchone()[0]

            if existing > 30:
                raise Exception(
                    f"{difficulty} already has {existing} questions. "
                    "Please check the database."
                )

            inserted = 0

            for question, answer, wrong1, wrong2, wrong3 in questions:

                if existing + inserted >= 30:
                    break

                options = [answer, wrong1, wrong2, wrong3]

                if len(set(options)) != 4:
                    raise Exception(
                        f"Duplicate options found: {question}"
                    )

                random.shuffle(options)
                correct_letter = "ABCD"[options.index(answer)]

                question_text = question

                cur.execute(
                    """
                    SELECT COUNT(*) FROM questions
                    WHERE quiz_id=? AND question=?
                    """,
                    (quiz_id, question_text)
                )

                if cur.fetchone()[0] > 0:
                    question_text = question + " (Version 2)"

                cur.execute(
                    """
                    INSERT INTO questions
                    (
                        quiz_id,
                        question,
                        option_a,
                        option_b,
                        option_c,
                        option_d,
                        correct_answer
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        quiz_id,
                        question_text,
                        options[0],
                        options[1],
                        options[2],
                        options[3],
                        correct_letter
                    )
                )

                inserted += 1

            cur.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id=?",
                (quiz_id,)
            )

            final_count = cur.fetchone()[0]

            if final_count != 30:
                raise Exception(
                    f"{difficulty} has {final_count}/30 questions."
                )

            print(f"{difficulty}: {final_count}/30 questions ready.")

        con.commit()

        print("\nSUCCESS: Question Tags has exactly 90 questions!")
        print("Easy: 30 | Medium: 30 | Hard: 30")

    except Exception as e:
        con.rollback()
        print("ERROR:", e)

    finally:
        con.close()


if __name__ == "__main__":
    main()
