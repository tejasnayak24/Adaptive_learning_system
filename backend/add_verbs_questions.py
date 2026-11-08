
import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"
TOPIC = "Verbs"
SUBJECT = "English"

QUESTIONS = {
    "Easy": [
        ("Identify the verb: Birds fly in the sky.", "fly", ["Birds", "Sky", "The"]),
        ("Choose the action verb: The boy runs fast.", "runs", ["boy", "fast", "the"]),
        ("Choose the correct verb: She ___ to school every day.", "goes", ["go", "going", "gone"]),
        ("Choose the correct verb: They ___ cricket on Sundays.", "play", ["plays", "playing", "played"]),
        ("Identify the helping verb: She is singing.", "is", ["She", "Singing", "None"]),
        ("Choose the correct verb: I ___ a student.", "am", ["is", "are", "be"]),
        ("Choose the correct verb: He ___ a new bicycle.", "has", ["have", "having", "had been"]),
        ("Identify the verb: The baby cried loudly.", "cried", ["Baby", "Loudly", "The"]),
        ("Choose the correct verb: We ___ happy today.", "are", ["is", "am", "be"]),
        ("Choose the correct verb: The sun ___ in the east.", "rises", ["rise", "rising", "risen"]),
        ("Identify the verb: Riya writes neatly.", "writes", ["Riya", "Neatly", "None"]),
        ("Choose the correct verb: The children ___ playing.", "are", ["is", "am", "be"]),
        ("Choose the correct verb: My mother ___ delicious food.", "cooks", ["cook", "cooking", "cooked"]),
        ("Identify the verb: The dog barked at the stranger.", "barked", ["Dog", "Stranger", "The"]),
        ("Choose the correct verb: I ___ my homework yesterday.", "completed", ["complete", "completing", "completes"]),
        ("Choose the correct verb: She ___ a beautiful song.", "sings", ["sing", "singing", "sung"]),
        ("Identify the verb: The teacher explained the lesson.", "explained", ["Teacher", "Lesson", "The"]),
        ("Choose the correct verb: Water ___ at 100 degrees Celsius at standard atmospheric pressure.", "boils", ["boil", "boiling", "boiled"]),
        ("Choose the correct verb: He ___ football now.", "is playing", ["play", "plays", "played"]),
        ("Identify the verb: The flowers bloom in spring.", "bloom", ["Flowers", "Spring", "The"]),
        ("Choose the correct verb: We ___ dinner at 8 p.m. yesterday.", "ate", ["eat", "eats", "eating"]),
        ("Choose the correct verb: The baby ___ sleeping.", "is", ["are", "am", "be"]),
        ("Identify the verb: Students study every day.", "study", ["Students", "Every", "Day"]),
        ("Choose the correct verb: She ___ two brothers.", "has", ["have", "having", "is"]),
        ("Choose the correct verb: I ___ going to the market.", "am", ["is", "are", "be"]),
        ("Identify the verb: The birds built a nest.", "built", ["Birds", "Nest", "A"]),
        ("Choose the correct verb: They ___ watching television.", "are", ["is", "am", "was"]),
        ("Choose the correct verb: He ___ the door yesterday.", "opened", ["open", "opens", "opening"]),
        ("Identify the verb: The horse galloped across the field.", "galloped", ["Horse", "Field", "Across"]),
        ("Choose the correct verb: She ___ English very well.", "speaks", ["speak", "speaking", "spoken"]),
    ],

    "Medium": [
        ("Choose the correct verb: Neither of the boys ___ present.", "is", ["are", "were", "have"]),
        ("Choose the correct verb: The list of items ___ on the table.", "is", ["are", "were", "have"]),
        ("Identify the linking verb: The soup tastes delicious.", "tastes", ["Soup", "Delicious", "The"]),
        ("Choose the correct verb: Each of the students ___ a notebook.", "has", ["have", "are", "were"]),
        ("Choose the correct verb: The news ___ surprising.", "is", ["are", "were", "have"]),
        ("Choose the correct verb: She ___ already finished her work.", "has", ["have", "is", "was"]),
        ("Identify the transitive verb: He kicked the ball.", "kicked", ["He", "Ball", "The"]),
        ("Identify the intransitive verb: The baby slept peacefully.", "slept", ["Baby", "Peacefully", "The"]),
        ("Choose the correct verb: By next week, I ___ the project.", "will have completed", ["will complete", "completed", "am completing"]),
        ("Choose the correct verb: If she studies hard, she ___ the exam.", "will pass", ["passed", "would passed", "passing"]),
        ("Choose the correct verb: The teacher, along with the students, ___ attending the event.", "is", ["are", "were", "have"]),
        ("Identify the finite verb: She wants to become a doctor.", "wants", ["To become", "Doctor", "None"]),
        ("Choose the correct verb: The players ___ practising since morning.", "have been", ["has been", "is", "was"]),
        ("Choose the correct verb: He ___ in this city for five years.", "has lived", ["have lived", "is living since", "live"]),
        ("Identify the modal verb: You should respect your elders.", "should", ["Respect", "Your", "Elders"]),
        ("Choose the correct verb: The train ___ before we reached the station.", "had departed", ["has departed", "departed", "departs"]),
        ("Choose the correct verb: Ten kilometres ___ a long distance to walk.", "is", ["are", "were", "have"]),
        ("Identify the phrasal verb: She gave up smoking.", "gave up", ["She", "Smoking", "Gave"]),
        ("Choose the correct verb: The furniture ___ delivered yesterday.", "was", ["were", "are", "have"]),
        ("Choose the correct verb: Neither Riya nor her friends ___ available.", "are", ["is", "was", "has"]),
        ("Identify the auxiliary verb: They have completed the assignment.", "have", ["They", "Completed", "Assignment"]),
        ("Choose the correct verb: I wish I ___ taller.", "were", ["am", "is", "be"]),
        ("Choose the correct verb: The committee ___ divided in their opinions.", "are", ["is", "has", "was"]),
        ("Identify the gerund: Swimming is good exercise.", "Swimming", ["Good", "Exercise", "Is"]),
        ("Choose the correct verb: She made him ___ the truth.", "tell", ["to tell", "telling", "told"]),
        ("Choose the correct verb: The teacher let the students ___ early.", "leave", ["to leave", "leaving", "left"]),
        ("Identify the participle: The broken window needs repair.", "broken", ["Window", "Needs", "Repair"]),
        ("Choose the correct verb: I would rather ___ at home.", "stay", ["to stay", "staying", "stayed"]),
        ("Choose the correct verb: The quality of these products ___ improved.", "has", ["have", "are", "were"]),
        ("Identify the modal verb: You must submit the form today.", "must", ["Submit", "Form", "Today"]),
    ],

    "Hard": [
        ("Choose the correct verb: The number of applicants ___ increasing.", "is", ["are", "have", "were"]),
        ("Choose the correct verb: A number of students ___ absent today.", "are", ["is", "was", "has"]),
        ("Choose the correct verb: Had I known about the meeting, I ___ attended it.", "would have", ["will have", "would", "had"]),
        ("Identify the subjunctive verb: The doctor suggested that he be admitted.", "be", ["Suggested", "Admitted", "Doctor"]),
        ("Choose the correct verb: It is essential that every member ___ present.", "be", ["is", "are", "was"]),
        ("Choose the correct verb: No sooner ___ the train left than it started raining.", "had", ["has", "did", "was"]),
        ("Choose the correct verb: Scarcely had she arrived when the programme ___.", "began", ["begin", "begins", "beginning"]),
        ("Identify the causative verb construction: The teacher made the students rewrite the answers.", "made", ["Students", "Rewrite", "Answers"]),
        ("Choose the correct verb: He is one of the writers who ___ regularly.", "write", ["writes", "writing", "has written"]),
        ("Choose the correct verb: She is the only one of the students who ___ won the prize.", "has", ["have", "are", "were"]),
        ("Choose the correct verb: The captain, as well as the players, ___ responsible.", "is", ["are", "were", "have"]),
        ("Identify the non-finite verb: To err is human.", "To err", ["Is", "Human", "None"]),
        ("Choose the correct verb: I would have helped you if you ___ me.", "had asked", ["asked", "have asked", "would ask"]),
        ("Choose the correct verb: By the time we arrived, the guests ___.", "had left", ["have left", "leave", "are leaving"]),
        ("Identify the perfect participle: Having completed the task, she went home.", "Having completed", ["Went", "Task", "Home"]),
        ("Choose the correct verb: The jury ___ reached its verdict.", "has", ["have", "are", "were"]),
        ("Choose the correct verb: More than one student ___ complained about the issue.", "has", ["have", "are", "were"]),
        ("Identify the phrasal verb: The meeting was called off.", "called off", ["Meeting", "Was", "The"]),
        ("Choose the correct verb: The data ___ collected from several sources.", "were", ["was", "has", "is"]),
        ("Choose the correct verb: Mathematics ___ my favourite subject.", "is", ["are", "were", "have"]),
        ("Identify the linking verb: The situation became difficult.", "became", ["Situation", "Difficult", "The"]),
        ("Choose the correct verb: If I ___ you, I would accept the offer.", "were", ["was", "am", "be"]),
        ("Choose the correct verb: The principal demanded that the report ___ submitted immediately.", "be", ["is", "was", "has"]),
        ("Identify the infinitive: She wants to learn French.", "to learn", ["Wants", "French", "She"]),
        ("Choose the correct verb: Not only the students but also the teacher ___ excited.", "was", ["were", "are", "have"]),
        ("Choose the correct verb: Either the manager or the employees ___ responsible.", "are", ["is", "was", "has"]),
        ("Identify the transitive verb: The committee rejected the proposal.", "rejected", ["Committee", "Proposal", "The"]),
        ("Choose the correct verb: The books, together with the notebook, ___ on the desk.", "are", ["is", "was", "has"]),
        ("Choose the correct verb: She ___ working here since 2020.", "has been", ["have been", "is", "was"]),
        ("Identify the auxiliary verb: The work should have been completed.", "should", ["Work", "Completed", "Been"]),
    ],
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
            raise ValueError("Verbs lesson not found in the database.")

        lesson_id = lesson[0]
        total_inserted = 0

        for difficulty, questions in QUESTIONS.items():

            if len(questions) != 30:
                raise ValueError(
                    f"{difficulty} contains {len(questions)} questions, not 30."
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

            print(f"{difficulty}: {final_count}/30 questions")

            if final_count != 30:
                raise ValueError(
                    f"{difficulty} has {final_count} questions instead of 30."
                )

        connection.commit()

        print("\nSUCCESS!")
        print(f"New questions inserted: {total_inserted}")
        print("Verbs completed: 90/90 MCQs.")

    except Exception as error:
        connection.rollback()
        print("ERROR:", error)
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
