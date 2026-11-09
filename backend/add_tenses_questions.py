
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

BANK = {
    "Easy": [
        ("She ___ to school every day.", "goes", "go", "going", "gone"),
        ("They ___ football yesterday.", "played", "play", "plays", "playing"),
        ("I ___ my homework now.", "am doing", "do", "did", "have do"),
        ("He ___ dinner at 8 PM every day.", "eats", "eat", "eating", "ate"),
        ("We ___ to the beach last Sunday.", "went", "go", "gone", "going"),
        ("She ___ a book at the moment.", "is reading", "reads", "read", "has read"),
        ("I ___ him tomorrow.", "will meet", "met", "meet", "meeting"),
        ("The sun ___ in the east.", "rises", "rise", "rose", "rising"),
        ("They ___ TV when I arrived.", "were watching", "watch", "watched", "are watching"),
        ("He ___ already finished his work.", "has", "have", "had", "is"),
        ("I ___ in this city since 2020.", "have lived", "lived", "am living", "live"),
        ("She ___ when the phone rang.", "was sleeping", "sleeps", "is sleeping", "has slept"),
        ("We ___ a movie last night.", "watched", "watch", "watching", "watches"),
        ("Look! The baby ___.", "is crying", "cries", "cried", "cry"),
        ("He ___ his grandparents next week.", "will visit", "visited", "visits", "visiting"),
        ("Water ___ at 100 degrees Celsius.", "boils", "boil", "boiled", "boiling"),
        ("I ___ breakfast before going to college every day.", "eat", "ate", "eating", "eaten"),
        ("She ___ the letter yesterday.", "wrote", "writes", "writing", "written"),
        ("They ___ for the bus right now.", "are waiting", "wait", "waited", "waits"),
        ("He ___ never visited Delhi.", "has", "have", "is", "was"),
        ("My father ___ to work by car every morning.", "drives", "drive", "drove", "driving"),
        ("We ___ our project last week.", "completed", "complete", "completing", "completes"),
        ("I think it ___ rain tomorrow.", "will", "was", "has", "did"),
        ("She ___ English very well.", "speaks", "speak", "speaking", "spoken"),
        ("The children ___ in the garden now.", "are playing", "play", "played", "plays"),
        ("He ___ the room before I entered.", "had left", "has leave", "leaves", "is leaving"),
        ("I ___ a new phone yesterday.", "bought", "buy", "buys", "buying"),
        ("They ___ here for two hours.", "have been", "was", "is", "be"),
        ("She ___ to music every evening.", "listens", "listen", "listened", "listening"),
        ("We ___ you soon.", "will call", "called", "calling", "calls"),
    ],

    "Medium": [
        ("By the time we arrived, the train ___.", "had left", "has left", "leaves", "was leaving"),
        ("She ___ for three hours before she took a break.", "had been studying", "has studied", "studies", "will study"),
        ("I ___ this book for two weeks, but I haven't finished it.", "have been reading", "read", "am read", "had read"),
        ("When I called him, he ___ dinner.", "was having", "has", "had", "is having"),
        ("By next Monday, they ___ the assignment.", "will have completed", "complete", "completed", "have completing"),
        ("The students ___ for the examination since morning.", "have been preparing", "prepared", "are prepare", "had prepare"),
        ("She usually ___ coffee, but today she is drinking tea.", "drinks", "is drinking", "drank", "has drunk"),
        ("I ___ him before the meeting started.", "had met", "have meet", "meet", "am meeting"),
        ("At this time tomorrow, we ___ to Mumbai.", "will be travelling", "travelled", "have travelled", "are travelled"),
        ("He ___ at this company since 2019.", "has been working", "is working", "worked", "will work"),
        ("They ___ the match before it started raining.", "had won", "have win", "win", "were win"),
        ("By 2030, she ___ her degree.", "will have completed", "will complete", "has completed", "completed"),
        ("While the teacher was explaining, the students ___ notes.", "were taking", "are taking", "have taken", "take"),
        ("I ___ my keys, so I cannot open the door.", "have lost", "lost", "had lose", "am losing"),
        ("He ___ for the company for five years by next June.", "will have been working", "has worked", "worked", "is working"),
        ("The meeting ___ before we reached the office.", "had started", "has start", "starts", "will start"),
        ("She ___ a letter when her friend visited her.", "was writing", "writes", "has written", "will write"),
        ("They ___ in the library every afternoon.", "study", "are study", "studied", "studying"),
        ("I ___ the report by the time you return.", "will have finished", "finish", "finished", "have finishing"),
        ("He ___ continuously for an hour when the power went out.", "had been working", "has worked", "works", "will work"),
        ("Listen! Someone ___ at the door.", "is knocking", "knocks", "knocked", "has knock"),
        ("She ___ to Japan twice so far.", "has travelled", "travelled", "is travelling", "had travel"),
        ("We ___ lunch when the guests arrived.", "were having", "have", "are having", "will have"),
        ("By the time the doctor arrived, the patient ___.", "had recovered", "has recover", "recovers", "will recover"),
        ("He ___ his car every weekend.", "washes", "is wash", "washed", "washing"),
        ("I ___ for you since 9 AM.", "have been waiting", "waited", "am waited", "had wait"),
        ("This time next year, I ___ in Japan.", "will be studying", "study", "studied", "have studied"),
        ("She ___ the work before the deadline yesterday.", "had completed", "has completed", "completes", "will complete"),
        ("They ___ a new bridge in our town these days.", "are building", "build", "built", "have build"),
        ("The bus ___ before we reached the stop.", "had departed", "has depart", "departs", "will depart"),
    ],

    "Hard": [
        ("By the end of this year, she ___ at the university for a decade.", "will have been teaching", "will teach", "has taught", "is teaching"),
        ("No sooner ___ the station than the train started moving.", "had we reached", "we had reached", "have we reached", "we reach"),
        ("Hardly ___ asleep when the alarm rang.", "had I fallen", "I had fallen", "have I fallen", "I fall"),
        ("If he ___ harder, he would have passed the examination.", "had studied", "studied", "has studied", "would study"),
        ("By the time you read this message, I ___ the country.", "will have left", "leave", "left", "have leaving"),
        ("She ___ in London for five years before she moved to Canada.", "had been living", "has lived", "is living", "will live"),
        ("I wish I ___ more carefully before making that decision.", "had thought", "think", "have thought", "will think"),
        ("This is the first time I ___ such a difficult problem.", "have faced", "faced", "am facing", "had face"),
        ("The committee ___ the proposal before the final meeting began.", "had been reviewing", "has review", "reviews", "will review"),
        ("By 6 PM tomorrow, the team ___ the entire project.", "will have completed", "will complete", "completed", "has completed"),
        ("He talks as though he ___ everything about the subject.", "knew", "knows", "has know", "will know"),
        ("When she arrived, I ___ for nearly two hours.", "had been waiting", "have waited", "am waiting", "will wait"),
        ("If I ___ about the delay, I would have taken another route.", "had known", "knew", "have known", "would know"),
        ("The students ___ the examination for an hour when the fire alarm rang.", "had been writing", "have written", "write", "will write"),
        ("By the time the guests arrive, we ___ the arrangements.", "will have made", "made", "have making", "make"),
        ("It is high time you ___ responsibility for your actions.", "took", "take", "have taken", "will take"),
        ("She ___ three research papers before joining the new institution.", "had published", "has publish", "publishes", "will publish"),
        ("I would rather you ___ the matter with the manager yesterday.", "had discussed", "discuss", "have discussed", "will discuss"),
        ("By next March, he ___ here for exactly twenty years.", "will have been working", "has worked", "worked", "is working"),
        ("The moment he ___ the news, he called his family.", "heard", "has heard", "will hear", "hearing"),
        ("If she were more confident, she ___ in the competition.", "would participate", "will participate", "participated", "has participated"),
        ("The scientist said that the earth ___ around the sun.", "revolves", "revolved", "is revolving", "has revolved"),
        ("I ___ the book for a month before I finally returned it.", "had been borrowing", "had had", "have been reading", "will read"),
        ("By the time the semester ends, we ___ all the required chapters.", "will have covered", "cover", "covered", "are covering"),
        ("He ___ the same company since he graduated, and he still works there.", "has been working for", "worked for", "had worked for", "will work for"),
        ("If they had started earlier, they ___ the deadline.", "would have met", "will meet", "would meet", "have met"),
        ("She ___ for the interview when the recruiter called to reschedule it.", "was preparing", "has prepared", "will prepare", "prepares"),
        ("By the time I reached the airport, the flight ___.", "had already departed", "has already departed", "already departs", "will already depart"),
        ("I ___ this software since it was first released.", "have been using", "used", "am use", "had use"),
        ("The manager announced that the company ___ a new branch the following year.", "would open", "will opened", "opens", "has opened"),
    ]
}


def main():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    try:
        cur.execute(
            "SELECT id FROM lessons WHERE title=? AND topic=?",
            ("Tenses", "English")
        )
        row = cur.fetchone()

        if not row:
            raise Exception("Lesson 'Tenses' with topic 'English' was not found.")

        lesson_id = row[0]

        for difficulty, questions in BANK.items():
            if len(questions) != 30:
                raise Exception(f"{difficulty} bank does not contain exactly 30 questions.")

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
                    (lesson_id, f"Tenses - {difficulty}", difficulty)
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
                    "Please check duplicates before proceeding."
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
        print("\nSUCCESS: Tenses has exactly 90 questions!")

    except Exception as e:
        con.rollback()
        print("ERROR:", e)

    finally:
        con.close()


if __name__ == "__main__":
    main()
