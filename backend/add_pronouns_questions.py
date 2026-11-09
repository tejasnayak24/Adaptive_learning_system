
import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"
TOPIC = "Pronouns"
SUBJECT = "English"

QUESTIONS = {
    "Easy": [
        ("Choose the correct pronoun: ___ am a student.", "I", ["Me", "My", "Mine"]),
        ("Identify the pronoun: She is reading a book.", "She", ["Reading", "Book", "Is"]),
        ("Choose the correct pronoun: Rahul is my friend. ___ is kind.", "He", ["She", "It", "They"]),
        ("Choose the correct pronoun: This book belongs to me. It is ___.", "Mine", ["My", "Me", "I"]),
        ("Identify the pronoun: They are playing football.", "They", ["Playing", "Football", "Are"]),
        ("Choose the correct pronoun: The dog is hungry. ___ needs food.", "It", ["He", "They", "We"]),
        ("Choose the correct pronoun: ___ are my best friends.", "They", ["Them", "Their", "Theirs"]),
        ("Identify the personal pronoun: We went to school.", "We", ["Went", "School", "To"]),
        ("Choose the correct pronoun: Please give ___ the pencil.", "Me", ["I", "My", "Mine"]),
        ("Choose the correct pronoun: This is ___ bag.", "My", ["Me", "Mine", "I"]),
        ("Identify the demonstrative pronoun: These are beautiful.", "These", ["Beautiful", "Are", "None"]),
        ("Choose the correct pronoun: ___ is your name?", "What", ["Who", "Which", "Whom"]),
        ("Choose the correct pronoun: ___ is standing outside?", "Who", ["Which", "What", "Whose"]),
        ("Identify the reflexive pronoun: She completed the work herself.", "Herself", ["She", "Completed", "Work"]),
        ("Choose the correct pronoun: We enjoyed ___ at the party.", "Ourselves", ["Us", "Our", "We"]),
        ("Choose the correct pronoun: This pen is not yours; it is ___.", "Mine", ["My", "Me", "I"]),
        ("Identify the possessive pronoun: The red car is theirs.", "Theirs", ["Red", "Car", "Is"]),
        ("Choose the correct pronoun: ___ is raining today.", "It", ["He", "They", "We"]),
        ("Choose the correct pronoun: Both students brought ___ books.", "Their", ["Them", "They", "Theirs"]),
        ("Identify the pronoun: Nobody was present in the room.", "Nobody", ["Present", "Room", "Was"]),
        ("Choose the correct pronoun: ___ of these is your favourite?", "Which", ["Who", "Whom", "Whose"]),
        ("Choose the correct pronoun: The teacher called Ravi and ___.", "Me", ["I", "My", "Mine"]),
        ("Identify the indefinite pronoun: Everyone enjoyed the show.", "Everyone", ["Enjoyed", "Show", "The"]),
        ("Choose the correct pronoun: The children dressed ___.", "Themselves", ["Them", "Their", "They"]),
        ("Choose the correct pronoun: Is this umbrella ___?", "Yours", ["Your", "You", "Yourself"]),
        ("Identify the relative pronoun: The boy who won is my brother.", "Who", ["Boy", "Won", "Brother"]),
        ("Choose the correct pronoun: ___ are going to the market.", "We", ["Us", "Our", "Ours"]),
        ("Choose the correct pronoun: Please tell ___ the truth.", "Him", ["He", "His", "Himself"]),
        ("Identify the pronoun: Someone left a bag here.", "Someone", ["Left", "Bag", "Here"]),
        ("Choose the correct pronoun: My sister and ___ went shopping.", "I", ["Me", "My", "Mine"]),
    ],

    "Medium": [
        ("Choose the correct pronoun: Neither of the boys brought ___ notebook.", "his", ["their", "them", "theirs"]),
        ("Choose the correct pronoun: Each student must submit ___ assignment.", "his or her", ["theirselves", "them", "theirs"]),
        ("Identify the relative pronoun: The woman whose car was stolen called the police.", "Whose", ["Woman", "Car", "Police"]),
        ("Choose the correct pronoun: This is the student ___ I met yesterday.", "whom", ["whose", "which", "what"]),
        ("Choose the correct pronoun: The person ___ called you is my uncle.", "who", ["whom", "which", "whose"]),
        ("Identify the interrogative pronoun: Whom did you invite?", "Whom", ["You", "Did", "Invite"]),
        ("Choose the correct pronoun: Between you and ___, this is a secret.", "me", ["I", "my", "mine"]),
        ("Choose the correct pronoun: The players congratulated ___ after the match.", "themselves", ["their", "themself", "theirselves"]),
        ("Identify the indefinite pronoun: Several were absent today.", "Several", ["Absent", "Today", "Were"]),
        ("Choose the correct pronoun: One should always do ___ duty.", "one's", ["his", "their", "ones"]),
        ("Choose the correct pronoun: The girl ___ won the prize is my cousin.", "who", ["whom", "which", "whose"]),
        ("Identify the demonstrative pronoun: That is the house I told you about.", "That", ["House", "Told", "About"]),
        ("Choose the correct pronoun: The manager spoke to Anita and ___.", "me", ["I", "my", "mine"]),
        ("Choose the correct pronoun: All students must bring ___ identity cards.", "their", ["them", "theirs", "they"]),
        ("Identify the reflexive pronoun: I prepared the entire meal myself.", "Myself", ["I", "Meal", "Prepared"]),
        ("Choose the correct pronoun: The two sisters help ___ with their studies.", "each other", ["one another's", "themselves each", "their"]),
        ("Choose the correct pronoun: The athlete ___ performance was excellent received an award.", "whose", ["who", "whom", "which"]),
        ("Identify the relative pronoun: This is the book which I borrowed.", "Which", ["Book", "Borrowed", "This"]),
        ("Choose the correct pronoun: There are five candidates, but only ___ has qualified.", "one", ["ones", "each other", "themselves"]),
        ("Choose the correct pronoun: Neither Riya nor Priya brought ___ lunch.", "her", ["their", "them", "hers"]),
        ("Identify the reciprocal pronoun: The two friends trust each other.", "Each other", ["Two", "Friends", "Trust"]),
        ("Choose the correct pronoun: The child hurt ___ while playing.", "himself", ["him", "his", "he"]),
        ("Choose the correct pronoun: ___ of the two answers is correct?", "Which", ["Who", "Whom", "Whose"]),
        ("Identify the possessive pronoun: The responsibility is ours.", "Ours", ["Responsibility", "Is", "The"]),
        ("Choose the correct pronoun: The teacher asked Ravi and ___ to stay.", "him", ["he", "his", "himself"]),
        ("Choose the correct pronoun: Everyone should bring ___ own water bottle.", "their", ["them", "theirs", "they"]),
        ("Identify the relative pronoun: I know the place where she works.", "Where", ["Place", "Works", "She"]),
        ("Choose the correct pronoun: The boy blamed ___ for the mistake.", "himself", ["him", "his", "he"]),
        ("Choose the correct pronoun: This is the person to ___ I gave the documents.", "whom", ["who", "whose", "which"]),
        ("Identify the indefinite pronoun: Few understood the difficult question.", "Few", ["Understood", "Difficult", "Question"]),
    ],

    "Hard": [
        ("Choose the correct pronoun: If anyone calls, tell ___ that I am busy.", "them", ["their", "theirs", "themselves"]),
        ("Choose the correct pronoun: The committee members disagreed with ___ over the decision.", "one another", ["themselves", "each", "their"]),
        ("Identify the relative pronoun: The candidate whom we selected has accepted the offer.", "Whom", ["Candidate", "Selected", "Offer"]),
        ("Choose the correct pronoun: It was ___ who completed the assignment.", "she", ["her", "hers", "herself"]),
        ("Choose the correct pronoun: The award was given to my brother and ___.", "me", ["I", "my", "mine"]),
        ("Choose the correct pronoun: Neither of the two proposals has ___ advantages.", "its", ["their", "them", "theirs"]),
        ("Identify the intensive pronoun: The principal herself distributed the certificates.", "Herself", ["Principal", "Certificates", "Distributed"]),
        ("Choose the correct pronoun: The person ___ you think is responsible has resigned.", "whom", ["who", "whose", "which"]),
        ("Choose the correct pronoun: The twins often compare their work with ___.", "each other's", ["themselves", "one another", "their"]),
        ("Identify the relative pronoun: Whoever finishes first will receive a certificate.", "Whoever", ["Finishes", "First", "Certificate"]),
        ("Choose the correct pronoun: The students, each of ___ received a certificate, celebrated.", "whom", ["who", "whose", "which"]),
        ("Choose the correct pronoun: The company changed ___ policy last year.", "its", ["their", "them", "theirs"]),
        ("Choose the correct pronoun: She is one of those people who always ___ their promises.", "keep", ["keeps", "keeping", "kept"]),
        ("Identify the reciprocal pronoun: The team members supported one another.", "One another", ["Team", "Members", "Supported"]),
        ("Choose the correct pronoun: The person to ___ the letter was addressed could not be found.", "whom", ["who", "whose", "which"]),
        ("Choose the correct pronoun: Neither of the girls completed ___ project on time.", "her", ["their", "them", "hers"]),
        ("Identify the relative pronoun: The house, which was built in 1950, is still standing.", "Which", ["House", "Built", "Standing"]),
        ("Choose the correct pronoun: The responsibility for the mistake is ___, not mine.", "yours", ["your", "you", "yourself"]),
        ("Choose the correct pronoun: Let you and ___ handle the presentation.", "me", ["I", "my", "mine"]),
        ("Identify the indefinite pronoun: Many of the applicants were shortlisted.", "Many", ["Applicants", "Shortlisted", "Were"]),
        ("Choose the correct pronoun: The person ___ I believed to be honest deceived me.", "whom", ["who", "whose", "which"]),
        ("Choose the correct pronoun: The two departments exchanged reports with ___.", "each other", ["themselves", "their", "them"]),
        ("Identify the emphatic pronoun: The director himself approved the proposal.", "Himself", ["Director", "Proposal", "Approved"]),
        ("Choose the correct pronoun: This is the same student ___ helped us earlier.", "who", ["whom", "whose", "which"]),
        ("Choose the correct pronoun: The dog wagged ___ tail happily.", "its", ["it's", "their", "it"]),
        ("Identify the relative pronoun: The employee whose work was appreciated received a bonus.", "Whose", ["Employee", "Work", "Bonus"]),
        ("Choose the correct pronoun: The person ___ the award belongs to is absent.", "to whom", ["who", "whose", "which"]),
        ("Choose the correct pronoun: All the participants introduced ___ before the event.", "themselves", ["them", "their", "each other"]),
        ("Identify the interrogative pronoun: Which of these is your final decision?", "Which", ["These", "Your", "Decision"]),
        ("Choose the correct pronoun: The author and the editor praised ___ for the successful publication.", "each other", ["themselves", "their", "them"]),
    ]
}


def main():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT id FROM lessons WHERE title = ? AND topic = ?",
            (TOPIC, SUBJECT)
        )
        lesson = cursor.fetchone()

        if not lesson:
            raise ValueError("Pronouns lesson not found.")

        lesson_id = lesson[0]
        total_inserted = 0

        for difficulty, questions in QUESTIONS.items():

            if len(questions) != 30:
                raise ValueError(
                    f"{difficulty} has {len(questions)} questions, not 30."
                )

            cursor.execute(
                """
                SELECT id FROM quizzes
                WHERE lesson_id = ?
                AND LOWER(difficulty) = LOWER(?)
                """,
                (lesson_id, difficulty)
            )

            quiz = cursor.fetchone()

            if quiz:
                quiz_id = quiz[0]
            else:
                cursor.execute(
                    """
                    INSERT INTO quizzes (lesson_id, title, difficulty)
                    VALUES (?, ?, ?)
                    """,
                    (lesson_id, f"{TOPIC} - {difficulty}", difficulty)
                )
                quiz_id = cursor.lastrowid

            for question, answer, wrong_answers in questions:

                options = [answer] + wrong_answers

                if len(set(options)) != 4:
                    raise ValueError(
                        f"Duplicate options in question: {question}"
                    )

                cursor.execute(
                    """
                    SELECT id FROM questions
                    WHERE quiz_id = ? AND question = ?
                    """,
                    (quiz_id, question)
                )

                if cursor.fetchone():
                    continue

                random.shuffle(options)
                correct_answer = "ABCD"[options.index(answer)]

                cursor.execute(
                    """
                    INSERT INTO questions
                    (quiz_id, question, option_a, option_b,
                     option_c, option_d, correct_answer)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        quiz_id,
                        question,
                        options[0],
                        options[1],
                        options[2],
                        options[3],
                        correct_answer
                    )
                )

                total_inserted += 1

            cursor.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                (quiz_id,)
            )
            final_count = cursor.fetchone()[0]

            print(
                f"{difficulty}: {final_count}/30 questions | "
                f"Quiz ID: {quiz_id}"
            )

            if final_count != 30:
                raise ValueError(
                    f"{difficulty} has {final_count} questions instead of 30."
                )

        connection.commit()

        print("\nSUCCESS!")
        print(f"New questions inserted: {total_inserted}")
        print("Pronouns completed: 90/90 MCQs.")

    except Exception as error:
        connection.rollback()
        print("ERROR:", error)
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
