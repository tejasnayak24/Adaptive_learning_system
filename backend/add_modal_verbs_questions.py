
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

BANK = {
    "Easy": [
        ("She ___ swim very well.", "can", "must", "should", "might"),
        ("You ___ obey traffic rules.", "must", "could", "might", "would"),
        ("___ I borrow your pen?", "May", "Must", "Should", "Would"),
        ("When I was young, I ___ run very fast.", "could", "can", "must", "may"),
        ("You ___ eat more vegetables to stay healthy.", "should", "might", "would", "can"),
        ("It ___ rain later today.", "might", "must", "should", "ought"),
        ("___ you please open the window?", "Could", "Must", "Should", "Might"),
        ("Students ___ wear their uniforms to school.", "must", "might", "could", "would"),
        ("I ___ speak three languages.", "can", "must", "should", "may"),
        ("You ___ not park your vehicle here.", "must", "could", "would", "might"),
        ("He ___ be at home; the lights are on.", "may", "should", "can", "would"),
        ("We ___ respect our elders.", "should", "might", "could", "would"),
        ("___ you like some coffee?", "Would", "Must", "Can", "Should"),
        ("You ___ finish your homework before playing.", "must", "might", "would", "could"),
        ("She ___ dance beautifully when she was a child.", "could", "can", "must", "may"),
        ("I ___ help you with your bags.", "will", "must", "should", "might"),
        ("You ___ take an umbrella; it looks cloudy.", "should", "would", "can", "mustn't"),
        ("___ I come in, sir?", "May", "Must", "Should", "Would"),
        ("He ___ not attend the meeting yesterday because he was ill.", "could", "can", "may", "must"),
        ("We ___ leave now or we will miss the bus.", "must", "might", "would", "could"),
        ("You ___ smoke in this hospital.", "must not", "could", "would", "might"),
        ("She ___ visit us next Sunday.", "may", "must", "should", "can"),
        ("I ___ like to become a doctor.", "would", "must", "can", "should"),
        ("You ___ apologise for your mistake.", "should", "might", "can", "would"),
        ("___ we begin the lesson now?", "Shall", "Must", "Might", "Would"),
        ("He ___ solve this puzzle easily.", "can", "must", "should", "might"),
        ("You ___ be quiet in the library.", "should", "might", "would", "could"),
        ("They ___ arrive late because of traffic.", "might", "must", "should", "can"),
        ("I ___ carry this box myself; it is too heavy.", "cannot", "must", "should", "may"),
        ("We ___ always speak the truth.", "should", "might", "would", "could"),
    ],

    "Medium": [
        ("You ___ have informed me about the change earlier.", "should", "can", "may", "will"),
        ("She ___ have forgotten the appointment; she is usually punctual.", "might", "must", "should", "can"),
        ("He ___ be the new manager; I am not completely sure.", "might", "must", "should", "will"),
        ("You ___ have bought so much food; we already had enough.", "needn't", "mustn't", "couldn't", "wouldn't"),
        ("The lights are off. They ___ have gone to bed.", "must", "should", "can", "would"),
        ("If I had more time, I ___ learn Japanese.", "would", "must", "can", "shall"),
        ("You ___ not have spoken to her so rudely.", "should", "can", "may", "will"),
        ("He ___ have reached home by now; the journey takes two hours.", "should", "can", "might", "would"),
        ("___ you mind closing the door?", "Would", "Must", "Shall", "May"),
        ("The students ___ submit their assignments by Friday.", "have to", "might", "could", "would"),
        ("You ___ have seen him yesterday; he was abroad.", "cannot", "must", "should", "may"),
        ("She ___ speak French fluently after living in Paris for years.", "can", "must", "should", "might"),
        ("We ___ to respect the laws of our country.", "ought", "may", "can", "would"),
        ("He ___ rather stay at home than go to the party.", "would", "must", "shall", "may"),
        ("You ___ consult a doctor if the pain continues.", "should", "would", "can", "might"),
        ("The road is wet. It ___ have rained during the night.", "must", "should", "can", "would"),
        ("I ___ have helped you if you had asked me.", "would", "will", "can", "shall"),
        ("She ___ not come to the event because she has another commitment.", "may", "must", "should", "would"),
        ("Employees ___ wear their identity cards inside the office.", "must", "might", "could", "would"),
        ("You ___ have completed the task by now, but you haven't.", "should", "can", "may", "will"),
        ("He ___ have taken the wrong bus; that would explain his delay.", "may", "must", "should", "will"),
        ("___ I help you carry those bags?", "Shall", "Must", "Would", "Might"),
        ("You ___ not reveal confidential information to outsiders.", "must", "could", "would", "might"),
        ("She ___ have been waiting for us at the station.", "might", "mustn't", "cannot", "wouldn't"),
        ("We ___ have taken a taxi instead of walking in the rain.", "could", "must", "shall", "may"),
        ("He ___ be tired after working for twelve hours.", "must", "can", "would", "shall"),
        ("You ___ better take your passport with you.", "had", "would", "should", "might"),
        ("I ___ rather not discuss this matter now.", "would", "must", "can", "shall"),
        ("They ___ have finished the work before the deadline, but they delayed it.", "could", "must", "may", "will"),
        ("Candidates ___ bring their admission tickets to the examination hall.", "must", "might", "would", "could"),
    ],

    "Hard": [
        ("He ___ have been seriously injured; he walked away without assistance.", "cannot", "must", "should", "may"),
        ("You ___ have told me the truth instead of hiding it.", "ought to", "can", "may", "will"),
        ("If she had prepared properly, she ___ have passed the examination.", "would", "will", "can", "shall"),
        ("The report ___ have been submitted yesterday, but it was delayed.", "should", "can", "may", "will"),
        ("He ___ be working late tonight, although I am not certain.", "might", "must", "should", "will"),
        ("You ___ have taken my permission before using the equipment.", "ought to", "can", "may", "will"),
        ("The suspect ___ have left the building through the back entrance.", "could", "mustn't", "shouldn't", "wouldn't"),
        ("She ___ not have been sleeping when I called; I heard her voice.", "can", "must", "should", "would"),
        ("The manager ___ well have misunderstood the instructions.", "may", "must", "should", "can"),
        ("You ___ as well finish the report now rather than postpone it.", "might", "must", "shall", "can"),
        ("He ___ have been informed about the meeting, but nobody contacted him.", "should", "must", "can", "will"),
        ("I ___ rather you did not mention this matter again.", "would", "must", "can", "shall"),
        ("The machine ___ have malfunctioned because of the power fluctuation.", "may", "should", "would", "can"),
        ("She ___ have completed the assignment; she started it only an hour ago.", "cannot", "must", "should", "would"),
        ("You ___ not have wasted so much time on unnecessary activities.", "need", "must", "can", "may"),
        ("The documents ___ to be signed before the application is processed.", "ought", "might", "would", "can"),
        ("If he were more careful, he ___ not make such mistakes.", "would", "will", "must", "can"),
        ("The announcement ___ have been made earlier to avoid confusion.", "should", "can", "might", "will"),
        ("She ___ have been waiting outside for nearly an hour before we arrived.", "must", "should", "can", "would"),
        ("You ___ have called me; I would have picked you up.", "could", "must", "should", "shall"),
        ("The evidence is incomplete, so the conclusion ___ be treated as final.", "cannot", "must", "should", "would"),
        ("He ___ have forgotten the keys, as they are not on the table.", "may", "mustn't", "cannot", "shouldn't"),
        ("We ___ to have informed the authorities immediately after the incident.", "ought", "might", "can", "would"),
        ("The team ___ have won the match if the captain had played.", "might", "must", "shall", "can"),
        ("You ___ not have paid for the meal; I had already arranged it.", "need", "must", "should", "may"),
        ("The patient ___ be recovering well, judging by the latest report.", "seems to", "mustn't", "cannot", "wouldn't"),
        ("I ___ have misunderstood your instructions; could you explain them again?", "may", "must", "should", "will"),
        ("The train ___ have arrived by now if there had been no delay.", "would", "must", "can", "shall"),
        ("No employee ___ disclose customer information without authorisation.", "shall", "might", "could", "would"),
        ("You ___ have checked the figures before submitting the financial report.", "should", "can", "may", "will"),
    ]
}


def main():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    try:
        cur.execute(
            "SELECT id FROM lessons WHERE title=? AND topic=?",
            ("Modal Verbs", "English")
        )
        row = cur.fetchone()

        if not row:
            raise Exception("Lesson 'Modal Verbs' with topic 'English' was not found.")

        lesson_id = row[0]

        for difficulty, questions in BANK.items():
            if len(questions) != 30:
                raise Exception(
                    f"{difficulty} bank must contain exactly 30 questions."
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
                    "INSERT INTO quizzes (lesson_id, title, difficulty) VALUES (?, ?, ?)",
                    (lesson_id, f"Modal Verbs - {difficulty}", difficulty)
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
                    raise Exception(f"Duplicate options found: {question}")

                random.shuffle(options)
                correct_letter = "ABCD"[options.index(answer)]

                cur.execute("""
                    INSERT INTO questions
                    (quiz_id, question, option_a, option_b, option_c, option_d, correct_answer)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    quiz_id,
                    question,
                    options[0],
                    options[1],
                    options[2],
                    options[3],
                    correct_letter
                ))

                inserted += 1

            cur.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id=?",
                (quiz_id,)
            )
            final_count = cur.fetchone()[0]

            if final_count != 30:
                raise Exception(
                    f"{difficulty}: Expected 30 questions, found {final_count}."
                )

            print(f"{difficulty}: {final_count}/30 questions ready.")

        con.commit()
        print("\nSUCCESS: Modal Verbs has exactly 90 questions!")

    except Exception as e:
        con.rollback()
        print("ERROR:", e)

    finally:
        con.close()


if __name__ == "__main__":
    main()
