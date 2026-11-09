
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

BANK = {
    "Easy": [
        ("She ___ to college every day.", "goes", "go", "going", "gone"),
        ("I ___ breakfast at 8 AM.", "eat", "eats", "eating", "ate"),
        ("They ___ cricket on Sundays.", "play", "plays", "playing", "played"),
        ("He ___ a book right now.", "is reading", "reads", "read", "has read"),
        ("We ___ English every day.", "study", "studies", "studying", "studied"),
        ("The baby ___ now.", "is sleeping", "sleep", "sleeps", "slept"),
        ("My mother ___ delicious food.", "cooks", "cook", "cooking", "cooked"),
        ("Look! The children ___.", "are dancing", "dance", "dances", "danced"),
        ("I ___ my homework at the moment.", "am doing", "do", "does", "did"),
        ("The sun ___ in the east.", "rises", "rise", "rising", "rose"),
        ("He ___ coffee every morning.", "drinks", "drink", "drinking", "drank"),
        ("They ___ TV right now.", "are watching", "watch", "watches", "watched"),
        ("She ___ two brothers.", "has", "have", "having", "had"),
        ("Water ___ at 100 degrees Celsius.", "boils", "boil", "boiling", "boiled"),
        ("We ___ for the bus now.", "are waiting", "wait", "waits", "waited"),
        ("My father ___ to work by car.", "drives", "drive", "driving", "drove"),
        ("I ___ a letter at present.", "am writing", "write", "writes", "wrote"),
        ("Birds ___ in the sky.", "fly", "flies", "flying", "flew"),
        ("She ___ her room every weekend.", "cleans", "clean", "cleaning", "cleaned"),
        ("The students ___ for the teacher.", "are waiting", "wait", "waits", "waited"),
        ("He ___ football very well.", "plays", "play", "playing", "played"),
        ("Listen! Someone ___ the piano.", "is playing", "plays", "play", "played"),
        ("I ___ in Mysuru.", "live", "lives", "living", "lived"),
        ("They ___ lunch at the moment.", "are having", "have", "has", "had"),
        ("She ___ her teeth twice a day.", "brushes", "brush", "brushing", "brushed"),
        ("We ___ a movie right now.", "are watching", "watch", "watches", "watched"),
        ("The train ___ at 9 AM every day.", "arrives", "arrive", "arriving", "arrived"),
        ("He ___ his bicycle now.", "is repairing", "repairs", "repair", "repaired"),
        ("I ___ water regularly.", "drink", "drinks", "drinking", "drank"),
        ("My friends ___ in the park every evening.", "walk", "walks", "walking", "walked"),
    ],

    "Medium": [
        ("She ___ in this company since 2022.", "has been working", "is working", "works", "worked"),
        ("I ___ three chapters so far.", "have completed", "completed", "am completing", "complete"),
        ("They ___ for the examination since morning.", "have been studying", "are studying", "studied", "study"),
        ("He ___ already submitted his assignment.", "has", "have", "is", "was"),
        ("We ___ this movie before.", "have seen", "saw", "are seeing", "see"),
        ("She ___ dinner while her brother is studying.", "is cooking", "cooks", "cook", "cooked"),
        ("The students ___ their project this week.", "are completing", "completes", "completed", "has completed"),
        ("I ___ for you for two hours.", "have been waiting", "am waiting", "wait", "waited"),
        ("He usually ___ early, but today he is late.", "wakes up", "is waking up", "wake up", "woke up"),
        ("My parents ___ in this house for twenty years.", "have lived", "are living", "lived", "live"),
        ("She ___ five emails today.", "has written", "writes", "is writing", "write"),
        ("The children ___ outside since 4 PM.", "have been playing", "are playing", "played", "plays"),
        ("Why ___ you ___ at me?", "are / looking", "do / looks", "have / look", "is / looking"),
        ("He ___ not understand the question.", "does", "do", "is", "has"),
        ("How long ___ you ___ English?", "have / been learning", "are / learn", "do / learning", "has / learned"),
        ("The manager ___ a meeting at the moment.", "is conducting", "conduct", "conducts", "conducted"),
        ("I ___ never ___ such a beautiful place.", "have / visited", "has / visit", "am / visiting", "did / visited"),
        ("She ___ her keys and cannot find them.", "has lost", "is losing", "lose", "lost"),
        ("They ___ for the new semester these days.", "are preparing", "prepares", "prepared", "has prepared"),
        ("It ___ heavily since morning.", "has been raining", "is raining", "rains", "rained"),
        ("He ___ three cups of coffee today.", "has had", "have had", "is having", "had"),
        ("The Earth ___ around the Sun.", "revolves", "is revolving", "revolve", "revolved"),
        ("We ___ the same teacher for two years.", "have had", "are having", "has", "had been"),
        ("She ___ to the gym regularly this month.", "has been going", "go", "went", "is go"),
        ("I ___ my laptop at the moment.", "am using", "uses", "use", "used"),
        ("How many books ___ you ___ this month?", "have / read", "has / read", "are / reading", "do / reads"),
        ("He ___ always ___ about his work.", "is / complaining", "does / complains", "has / complain", "are / complaining"),
        ("The company ___ a new product this week.", "is launching", "launch", "launched", "launches"),
        ("She ___ French for six months.", "has been learning", "is learn", "learned", "learn"),
        ("I ___ him since childhood.", "have known", "am knowing", "knows", "knew"),
    ],

    "Hard": [
        ("By this time, she ___ on the research for six months.", "has been working", "is working", "works", "worked"),
        ("Neither of the students ___ the correct answer.", "knows", "know", "are knowing", "have known"),
        ("The number of applicants ___ every year.", "increases", "increase", "are increasing", "have increased"),
        ("Each of the participants ___ a certificate.", "receives", "receive", "are receiving", "have receive"),
        ("I ___ this author since I was in school.", "have admired", "am admiring", "admire", "had admired"),
        ("She ___ three reports so far this week.", "has prepared", "have prepared", "is prepare", "prepares"),
        ("The quality of these products ___ over time.", "improves", "improve", "are improving", "have improve"),
        ("Why ___ he always ___ his responsibilities?", "is / avoiding", "does / avoiding", "has / avoid", "are / avoiding"),
        ("The committee ___ the proposal at present.", "is considering", "are consider", "consider", "has consider"),
        ("I ___ to contact you all morning.", "have been trying", "am trying", "try", "tried"),
        ("This is the first time we ___ such a challenging task.", "have undertaken", "undertake", "are undertaking", "undertook"),
        ("She ___ in the laboratory for the past three hours.", "has been experimenting", "is experiment", "experiments", "experimented"),
        ("The news ___ that the government is introducing new rules.", "suggests", "suggest", "are suggesting", "have suggested"),
        ("One of my friends ___ in Japan.", "lives", "live", "are living", "have lived"),
        ("He ___ the same mistake repeatedly.", "has been making", "is make", "make", "made"),
        ("The teacher, along with the students, ___ attending the seminar.", "is", "are", "have", "were"),
        ("I ___ what you mean now.", "understand", "am understanding", "have understanding", "understood"),
        ("She ___ for her final examination since last month.", "has been preparing", "is prepare", "prepared", "prepares"),
        ("The company ___ its services to several countries.", "provides", "provide", "are providing", "have provide"),
        ("How long ___ the machine ___ properly?", "has / been functioning", "is / function", "does / functioning", "have / function"),
        ("The percentage of students passing the exam ___ every year.", "varies", "vary", "are varying", "have varied"),
        ("I ___ never ___ such an unusual situation before.", "have / encountered", "has / encounter", "am / encountering", "did / encountered"),
        ("The staff ___ currently reviewing the applications.", "are", "is", "has", "was"),
        ("She ___ the piano since she was six years old.", "has been playing", "is playing", "plays", "played"),
        ("A pair of shoes ___ missing from the cupboard.", "is", "are", "have", "were"),
        ("He ___ not usually ___ mistakes in his calculations.", "does / make", "do / makes", "is / making", "has / made"),
        ("The water level ___ steadily over the past few days.", "has been rising", "is rise", "rise", "rose"),
        ("I ___ that this decision is important.", "believe", "am believing", "have believing", "believed"),
        ("The principal ___ the students every Monday.", "addresses", "address", "is address", "have addressed"),
        ("We ___ for a solution to this problem for several weeks.", "have been searching", "are search", "searched", "search"),
    ]
}


def main():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    try:
        cur.execute(
            "SELECT id FROM lessons WHERE title=? AND topic=?",
            ("Present Tense", "English")
        )
        row = cur.fetchone()

        if not row:
            raise Exception("Lesson 'Present Tense' with topic 'English' was not found.")

        lesson_id = row[0]

        for difficulty, questions in BANK.items():
            if len(questions) != 30:
                raise Exception(f"{difficulty} bank must contain exactly 30 questions.")

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
                    (lesson_id, f"Present Tense - {difficulty}", difficulty)
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
                    raise Exception(f"Duplicate options: {question}")

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
        print("\nSUCCESS: Present Tense has exactly 90 questions!")

    except Exception as e:
        con.rollback()
        print("ERROR:", e)

    finally:
        con.close()


if __name__ == "__main__":
    main()
