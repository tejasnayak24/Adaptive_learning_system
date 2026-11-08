
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

BANK = {
    "Easy": [
        ("She ___ to school yesterday.", "went", "go", "goes", "going"),
        ("I ___ a movie last night.", "watched", "watch", "watches", "watching"),
        ("They ___ football yesterday.", "played", "play", "plays", "playing"),
        ("He ___ his homework last evening.", "completed", "complete", "completes", "completing"),
        ("We ___ dinner at 8 PM yesterday.", "ate", "eat", "eats", "eating"),
        ("She ___ a beautiful dress last week.", "bought", "buy", "buys", "buying"),
        ("I ___ him at the market yesterday.", "met", "meet", "meets", "meeting"),
        ("The baby ___ all night.", "cried", "cry", "cries", "crying"),
        ("He ___ the window this morning.", "opened", "open", "opens", "opening"),
        ("They ___ to Mumbai last month.", "travelled", "travel", "travels", "travelling"),
        ("My father ___ a new car last year.", "purchased", "purchase", "purchases", "purchasing"),
        ("She ___ the letter yesterday.", "wrote", "write", "writes", "writing"),
        ("We ___ the museum last Sunday.", "visited", "visit", "visits", "visiting"),
        ("He ___ late for class yesterday.", "was", "is", "were", "be"),
        ("They ___ happy with the results.", "were", "was", "are", "is"),
        ("I ___ TV when you called.", "was watching", "watched", "am watching", "watch"),
        ("She ___ when I entered the room.", "was sleeping", "slept", "sleeps", "is sleeping"),
        ("The children ___ in the garden.", "were playing", "played", "play", "are play"),
        ("We ___ dinner when the lights went out.", "were having", "have", "had", "are having"),
        ("He ___ a book at 7 PM yesterday.", "was reading", "reads", "read", "is reading"),
        ("I ___ my keys yesterday.", "lost", "lose", "loses", "losing"),
        ("She ___ the exam last year.", "passed", "pass", "passes", "passing"),
        ("The train ___ late yesterday.", "arrived", "arrive", "arrives", "arriving"),
        ("He ___ his bicycle last weekend.", "repaired", "repair", "repairs", "repairing"),
        ("It ___ heavily last night.", "rained", "rain", "rains", "raining"),
        ("I ___ breakfast before leaving home.", "had", "have", "has", "having"),
        ("They ___ the match last Sunday.", "won", "win", "wins", "winning"),
        ("She ___ me a birthday gift.", "gave", "give", "gives", "giving"),
        ("We ___ our grandparents last month.", "visited", "visit", "visits", "visiting"),
        ("He ___ the answer correctly.", "answered", "answer", "answers", "answering"),
    ],

    "Medium": [
        ("By the time we reached the station, the train ___.", "had left", "has left", "leaves", "was leaving"),
        ("She ___ dinner when her friend arrived.", "was cooking", "cooked", "cooks", "has cooked"),
        ("I ___ the assignment before the deadline.", "had completed", "have completed", "complete", "was completing"),
        ("They ___ for two hours before the rain started.", "had been playing", "have played", "were play", "will play"),
        ("While I ___ to college, I saw an accident.", "was travelling", "travelled", "am travelling", "have travelled"),
        ("He ___ the movie before I recommended it.", "had seen", "has seen", "sees", "was seeing"),
        ("We ___ for the bus when it started raining.", "were waiting", "waited", "wait", "have waited"),
        ("She ___ in Bengaluru for five years before moving to Mysuru.", "had lived", "has lived", "lives", "is living"),
        ("The students ___ the test when the bell rang.", "were writing", "write", "have written", "are writing"),
        ("I ___ for an hour before he finally called.", "had been waiting", "have waited", "wait", "am waiting"),
        ("He ___ his wallet, so he could not pay.", "had forgotten", "has forgotten", "forgets", "was forgetting"),
        ("When we arrived, the guests ___ already ___.", "had / departed", "have / depart", "were / depart", "did / departed"),
        ("She ___ a song while her brother played the guitar.", "was singing", "sang", "sings", "has sung"),
        ("They ___ the project before the manager reviewed it.", "had finished", "have finished", "finish", "were finishing"),
        ("I ___ when the alarm suddenly rang.", "was sleeping", "sleep", "slept", "have slept"),
        ("He ___ for the company for ten years before he resigned.", "had been working", "has worked", "works", "is working"),
        ("The teacher ___ the lesson before the students arrived.", "had explained", "has explained", "explains", "was explaining"),
        ("While the children ___, their mother prepared lunch.", "were studying", "studied", "study", "have studied"),
        ("She ___ the book by the time the examination began.", "had read", "has read", "reads", "was reading"),
        ("We ___ for the examination since early morning before taking a break.", "had been preparing", "have prepared", "prepare", "are preparing"),
        ("He ___ his leg while he was playing football.", "broke", "break", "breaks", "breaking"),
        ("I ___ the email before the meeting started.", "had sent", "have send", "send", "was sending"),
        ("The workers ___ the road when the storm began.", "were repairing", "repaired", "repair", "have repaired"),
        ("She ___ in the library when I saw her.", "was studying", "studied", "studies", "has studied"),
        ("By 9 PM, they ___ all the arrangements.", "had made", "have make", "make", "were making"),
        ("He was tired because he ___ all day.", "had been working", "has worked", "works", "is working"),
        ("After she ___ the report, she submitted it.", "had completed", "has completed", "completes", "was completing"),
        ("The phone rang while I ___ a shower.", "was taking", "take", "took", "have taken"),
        ("They ___ the house before the guests arrived.", "had cleaned", "have cleaned", "clean", "were cleaning"),
        ("I ___ my homework when my friends came over.", "was doing", "did", "do", "have done"),
    ],

    "Hard": [
        ("By the time the investigation began, the evidence ___.", "had already disappeared", "has already disappeared", "already disappears", "will disappear"),
        ("She ___ for three hours before she realised she had taken the wrong route.", "had been driving", "has driven", "was driving", "will drive"),
        ("No sooner ___ the announcement than the audience began applauding.", "had he made", "he had made", "has he made", "he makes"),
        ("Hardly ___ the office when the manager called him back.", "had he left", "he had left", "has he left", "he leaves"),
        ("If I ___ about the meeting, I would have attended it.", "had known", "knew", "have known", "would know"),
        ("She ___ the manuscript for months before she finally submitted it.", "had been revising", "has revised", "was revising", "revises"),
        ("The suspect ___ before the police arrived.", "had escaped", "has escaped", "escapes", "was escaping"),
        ("I wish I ___ more attention during the lecture.", "had paid", "paid", "have paid", "would pay"),
        ("By the time the rescue team arrived, the villagers ___ for several hours.", "had been waiting", "have waited", "were waiting", "will wait"),
        ("He ___ the company before the merger was announced.", "had left", "has left", "leaves", "was leaving"),
        ("While the researchers ___ the data, they discovered an unexpected pattern.", "were analysing", "analysed", "have analysed", "analyse"),
        ("The audience ___ for nearly an hour before the speaker appeared.", "had been waiting", "has waited", "waits", "is waiting"),
        ("If she had accepted the offer, she ___ in Tokyo now.", "would be working", "will work", "worked", "has worked"),
        ("The committee ___ several proposals before reaching a final decision.", "had considered", "has consider", "considers", "was consider"),
        ("He spoke as though he ___ the entire incident himself.", "had witnessed", "has witnessed", "witnesses", "will witness"),
        ("By the time the semester ended, the students ___ all the prescribed chapters.", "had covered", "have covered", "cover", "were covering"),
        ("The machine ___ properly before the technician inspected it.", "had not been functioning", "has not function", "does not functioning", "will not function"),
        ("She ___ at the university for eight years when she received the promotion.", "had been teaching", "has taught", "teaches", "will teach"),
        ("The guests had already eaten when we ___ at the restaurant.", "arrived", "had arrived", "have arrived", "arrive"),
        ("I ___ the document twice before noticing the error.", "had checked", "have checked", "check", "was checking"),
        ("The athlete ___ for months before the championship was cancelled.", "had been training", "has trained", "trains", "will train"),
        ("If they had left earlier, they ___ the flight.", "would have caught", "will catch", "would catch", "have caught"),
        ("The director explained that the team ___ the project the previous year.", "had completed", "has completed", "completes", "will complete"),
        ("She ___ the same question repeatedly before the teacher answered it.", "had been asking", "has asked", "asks", "will ask"),
        ("When I entered the hall, the presentation ___ already ___.", "had / begun", "has / begin", "was / begin", "did / began"),
        ("He ___ the instructions carefully, yet he made several mistakes.", "had read", "has read", "reads", "is reading"),
        ("The roads were flooded because it ___ continuously throughout the night.", "had been raining", "has rained", "rains", "is raining"),
        ("By the time the doctor examined him, the fever ___.", "had subsided", "has subside", "subsides", "will subside"),
        ("She realised that she ___ her passport at home.", "had left", "has leave", "leaves", "was leaving"),
        ("The organisation ___ several campaigns before it received international recognition.", "had conducted", "has conduct", "conducts", "will conduct"),
    ]
}


def main():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    try:
        cur.execute(
            "SELECT id FROM lessons WHERE title=? AND topic=?",
            ("Past Tense", "English")
        )
        row = cur.fetchone()

        if not row:
            raise Exception("Lesson 'Past Tense' with topic 'English' was not found.")

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
                    (lesson_id, f"Past Tense - {difficulty}", difficulty)
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
        print("\nSUCCESS: Past Tense has exactly 90 questions!")

    except Exception as e:
        con.rollback()
        print("ERROR:", e)

    finally:
        con.close()


if __name__ == "__main__":
    main()
