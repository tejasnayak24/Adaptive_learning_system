
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

BANK = {
    "Easy": [
        ("If you heat ice, it ____.", "melts", "melt", "melted", "will melted"),
        ("If it rains, the ground ____ wet.", "gets", "get", "got", "getting"),
        ("If you study hard, you ____ the exam.", "will pass", "passed", "passing", "would passed"),
        ("If she comes early, we ____ together.", "will leave", "left", "would left", "leaving"),
        ("If I have time, I ____ you.", "will call", "called", "would called", "calling"),
        ("If water reaches 100°C, it ____.", "boils", "boil", "boiled", "will boiled"),
        ("If you don't hurry, you ____ the bus.", "will miss", "missed", "would missed", "missing"),
        ("If he works hard, he ____ successful.", "will become", "became", "would became", "becoming"),
        ("If you mix red and blue, you ____ purple.", "get", "gets", "got", "will got"),
        ("If I see her, I ____ her the message.", "will give", "gave", "would gave", "giving"),
        ("If babies are hungry, they ____.", "cry", "cries", "cried", "will cried"),
        ("If you touch fire, it ____ you.", "burns", "burn", "burned", "will burned"),
        ("If they invite me, I ____ to the party.", "will go", "went", "would went", "going"),
        ("If she studies, she ____ good marks.", "will get", "got", "would got", "getting"),
        ("If plants don't get water, they ____.", "die", "dies", "died", "will died"),
        ("If you press this button, the machine ____.", "starts", "start", "started", "will started"),
        ("If we leave now, we ____ on time.", "will arrive", "arrived", "would arrived", "arriving"),
        ("If he is tired, he ____ early.", "sleeps", "sleep", "slept", "will slept"),
        ("If you don't eat, you ____ hungry.", "will feel", "felt", "would felt", "feeling"),
        ("If the sun sets, it ____ dark.", "gets", "get", "got", "will got"),
        ("If I find your book, I ____ it to you.", "will return", "returned", "would returned", "returning"),
        ("If you freeze water, it ____ into ice.", "turns", "turn", "turned", "will turned"),
        ("If she practices daily, she ____ better.", "will perform", "performed", "would performed", "performing"),
        ("If people exercise, they ____ healthier.", "become", "becomes", "became", "will became"),
        ("If he calls me, I ____ him.", "will answer", "answered", "would answered", "answering"),
        ("If you heat chocolate, it ____.", "melts", "melt", "melted", "will melted"),
        ("If they work together, they ____ the task.", "will finish", "finished", "would finished", "finishing"),
        ("If you don't water the flowers, they ____.", "will wilt", "wilted", "would wilted", "wilting"),
        ("If the temperature falls below zero, water ____.", "freezes", "freeze", "froze", "will froze"),
        ("If I am free tomorrow, I ____ you.", "will visit", "visited", "would visited", "visiting")
    ],

    "Medium": [
        ("If I were rich, I ____ around the world.", "would travel", "will travel", "travelled", "would travelled"),
        ("If she knew the answer, she ____ us.", "would tell", "will tell", "told", "would told"),
        ("If I ____ you, I would accept the offer.", "were", "am", "was being", "be"),
        ("If he had more time, he ____ a new language.", "would learn", "will learn", "learned", "would learned"),
        ("If they invited us, we ____ the event.", "would attend", "will attend", "attended", "would attended"),
        ("If I had studied harder, I ____ the examination.", "would have passed", "will pass", "would pass", "had passed"),
        ("If she had left earlier, she ____ the train.", "would have caught", "will catch", "would catch", "had caught"),
        ("If they had informed me, I ____ them.", "would have helped", "will help", "would help", "had helped"),
        ("If he had taken an umbrella, he ____ wet.", "would not have got", "will not get", "would not get", "did not get"),
        ("If we had booked tickets, we ____ the concert.", "would have attended", "will attend", "would attend", "had attended"),
        ("You will succeed ____ you work hard.", "if", "unless", "although", "because"),
        ("You cannot enter ____ you have a ticket.", "unless", "if", "because", "although"),
        ("I will help you ____ you ask politely.", "provided that", "although", "despite", "whereas"),
        ("You can borrow my car ____ you drive carefully.", "as long as", "even though", "because", "so that"),
        ("____ you hurry, you will miss the train.", "Unless", "If", "Because", "Although"),
        ("If I ____ taller, I would become a basketball player.", "were", "am", "will be", "have been"),
        ("If he ____ earlier, he would have met the manager.", "had arrived", "arrives", "arrived", "has arrived"),
        ("If she ____ regularly, she will improve her English.", "practises", "practised", "will practise", "would practise"),
        ("If you had told me the truth, I ____ angry.", "would not have been", "will not be", "would not be", "am not"),
        ("If I won the lottery, I ____ a house.", "would buy", "will buy", "bought", "would have bought"),
        ("If the alarm rings, everyone ____ the building.", "will leave", "would leave", "left", "would have left"),
        ("If you don't charge your phone, it ____ off.", "will switch", "would switch", "switched", "would have switched"),
        ("If he were more careful, he ____ fewer mistakes.", "would make", "will make", "made", "would have made"),
        ("If they had practised more, they ____ the match.", "would have won", "will win", "would win", "won"),
        ("I would travel more ____ I had enough money.", "if", "unless", "although", "because"),
        ("You may use the computer ____ you do not change its settings.", "provided that", "even if", "although", "because"),
        ("If she had not missed the bus, she ____ on time.", "would have arrived", "will arrive", "would arrive", "arrived"),
        ("If I see an accident, I ____ the police.", "will inform", "would inform", "informed", "would have informed"),
        ("If he were the principal, he ____ the rules.", "would change", "will change", "changed", "would have changed"),
        ("If you heat metal, it usually ____.", "expands", "expand", "expanded", "will expanded")
    ],

    "Hard": [
        ("If I had accepted that job, I ____ in London now.", "would be living", "will be living", "would have lived", "am living"),
        ("If she were more organised, she ____ the deadline yesterday.", "would not have missed", "will not miss", "would not miss", "had not missed"),
        ("If he had taken the medicine, he ____ better now.", "would feel", "will feel", "would have felt", "felt"),
        ("If I ____ about the meeting, I would have attended it.", "had known", "knew", "have known", "would know"),
        ("Had I known about the traffic, I ____ earlier.", "would have left", "will leave", "would leave", "had left"),
        ("Were she here, she ____ the problem immediately.", "would solve", "will solve", "solved", "would have solved"),
        ("Should you need assistance, ____ the reception desk.", "contact", "contacted", "contacting", "to contact"),
        ("If he had saved enough money, he ____ a car by now.", "would have bought", "will buy", "would buy", "bought"),
        ("If I were not afraid of heights, I ____ skydiving last year.", "would have tried", "will try", "would try", "had tried"),
        ("If the company had invested in research, it ____ more competitive today.", "would be", "will be", "would have been", "is"),
        ("Unless you ____ the instructions, you may make mistakes.", "follow", "will follow", "followed", "would follow"),
        ("If he ____ harder last semester, he would be more confident now.", "had studied", "studies", "would study", "has studied"),
        ("If she were a doctor, she ____ the patient yesterday.", "would have treated", "will treat", "would treat", "had treated"),
        ("Had they informed us earlier, we ____ the necessary arrangements.", "would have made", "will make", "would make", "had made"),
        ("If I had not lost my passport, I ____ travelling now.", "would be", "will be", "would have been", "am"),
        ("If you should encounter any difficulty, ____ your supervisor.", "inform", "informed", "informing", "to informed"),
        ("If he ____ the truth earlier, the situation would be different now.", "had revealed", "reveals", "would reveal", "has revealed"),
        ("If the weather had improved, we ____ hiking yesterday.", "would have gone", "will go", "would go", "had gone"),
        ("If I were more experienced, I ____ the project last month.", "would have managed", "will manage", "would manage", "had managed"),
        ("If she had accepted the scholarship, she ____ abroad now.", "would be studying", "will study", "would have studied", "studied"),
        ("But for your timely help, I ____ the competition.", "would have lost", "will lose", "would lose", "had lost"),
        ("If he were to apologise, I ____ him.", "would forgive", "will forgive", "forgave", "would have forgiven"),
        ("If the machine had been maintained properly, it ____ working now.", "would still be", "will still be", "would have still been", "is still"),
        ("If you had followed the map, you ____ lost now.", "would not be", "will not be", "would not have been", "are not"),
        ("If I ____ the opportunity again, I would choose differently.", "were given", "am given", "will be given", "have given"),
        ("If the manager had approved the request, we ____ the work last week.", "would have completed", "will complete", "would complete", "had completed"),
        ("If she were more confident, she ____ for the leadership position last year.", "would have applied", "will apply", "would apply", "had applied"),
        ("If he had not ignored the warning, he ____ in trouble now.", "would not be", "will not be", "would not have been", "is not"),
        ("If I had a better internet connection, I ____ the online class yesterday.", "would have attended", "will attend", "would attend", "had attended"),
        ("If the research had been completed earlier, the results ____ available now.", "would be", "will be", "would have been", "are")
    ]
}


def main():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    try:
        cur.execute(
            "SELECT id FROM lessons WHERE title=? AND topic=?",
            ("Conditional Sentences", "English")
        )

        row = cur.fetchone()

        if not row:
            raise Exception(
                "Lesson 'Conditional Sentences' with topic 'English' was not found."
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
                        f"Conditional Sentences - {difficulty}",
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

        print("\nSUCCESS: Conditional Sentences has exactly 90 questions!")
        print("Easy: 30 | Medium: 30 | Hard: 30")

    except Exception as e:
        con.rollback()
        print("ERROR:", e)

    finally:
        con.close()


if __name__ == "__main__":
    main()
