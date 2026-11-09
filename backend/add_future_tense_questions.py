
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

BANK = {
    "Easy": [
        ("I ___ you tomorrow.", "will meet", "met", "meet", "meeting"),
        ("She ___ a doctor in the future.", "will become", "became", "becomes", "becoming"),
        ("They ___ to Delhi next week.", "will travel", "travelled", "travelling", "travels"),
        ("We ___ the project tomorrow.", "will complete", "completed", "completing", "completes"),
        ("He ___ his homework tonight.", "will do", "did", "does", "doing"),
        ("It ___ rain tomorrow.", "will", "did", "has", "was"),
        ("I think she ___ the competition.", "will win", "won", "wins", "winning"),
        ("My parents ___ us next Sunday.", "will visit", "visited", "visiting", "visits"),
        ("The train ___ at 8 AM tomorrow.", "will arrive", "arrived", "arriving", "arrives yesterday"),
        ("We ___ a new house next year.", "will buy", "bought", "buying", "buys"),
        ("At 8 PM tomorrow, I ___ TV.", "will be watching", "watched", "watch", "have watched"),
        ("This time tomorrow, she ___ to London.", "will be flying", "flew", "flies", "has flown"),
        ("They ___ for the examination at this time tomorrow.", "will be studying", "studied", "study", "have studied"),
        ("He ___ dinner when we arrive.", "will be having", "had", "has", "is have"),
        ("At noon tomorrow, we ___ in the meeting.", "will be sitting", "sat", "sit", "have sat"),
        ("By next Monday, I ___ the assignment.", "will have finished", "finish", "finished", "am finishing"),
        ("She ___ her degree by next year.", "will have completed", "completes", "completed", "is completing"),
        ("They ___ home by 6 PM.", "will have reached", "reach", "reached", "are reaching"),
        ("By tomorrow morning, he ___ the book.", "will have read", "reads", "read", "is reading"),
        ("We ___ the work before the deadline.", "will have completed", "complete", "completed", "completing"),
        ("I ___ you when I reach home.", "will call", "called", "calling", "calls"),
        ("She ___ a new laptop next month.", "will purchase", "purchased", "purchasing", "purchases yesterday"),
        ("The children ___ in the park tomorrow evening.", "will be playing", "played", "play", "have played"),
        ("He ___ at the office at 10 AM tomorrow.", "will be working", "worked", "works", "has worked"),
        ("By the end of this week, we ___ the syllabus.", "will have covered", "cover", "covered", "are covering"),
        ("I promise I ___ you.", "will help", "helped", "helping", "helps"),
        ("They ___ a party next Saturday.", "will organize", "organized", "organizing", "organizes"),
        ("At this time next week, we ___ on the beach.", "will be relaxing", "relaxed", "relax", "have relaxed"),
        ("By 2028, she ___ her studies.", "will have completed", "completed", "completes", "is completing"),
        ("He ___ the results tomorrow.", "will announce", "announced", "announcing", "announces yesterday"),
    ],

    "Medium": [
        ("By the time you arrive, I ___ dinner.", "will have prepared", "prepare", "prepared", "am preparing"),
        ("This time next month, she ___ in Japan.", "will be studying", "studied", "studies", "has studied"),
        ("By 2030, they ___ in this city for ten years.", "will have been living", "will live", "have lived", "are living"),
        ("At 9 AM tomorrow, the students ___ their examination.", "will be writing", "write", "wrote", "have written"),
        ("By the end of the year, he ___ five novels.", "will have written", "writes", "wrote", "is writing"),
        ("I ___ for you at the airport when your flight lands.", "will be waiting", "waited", "wait", "have waited"),
        ("By next June, she ___ at this company for five years.", "will have been working", "will work", "worked", "is working"),
        ("Don't call me at 7 PM because I ___ a presentation.", "will be giving", "gave", "give", "have given"),
        ("By the time the guests arrive, we ___ the decorations.", "will have finished", "finish", "finished", "are finishing"),
        ("At this time tomorrow, they ___ across the ocean.", "will be sailing", "sailed", "sail", "have sailed"),
        ("By 5 PM, the workers ___ the repairs.", "will have completed", "complete", "completed", "are completing"),
        ("She ___ for three hours by the time the examination begins.", "will have been studying", "will study", "studied", "is studying"),
        ("The manager ___ the new policy at tomorrow's meeting.", "will announce", "announced", "announcing", "has announce"),
        ("When you reach the station, the train ___ already ___.", "will / have departed", "will / departing", "has / depart", "is / departed"),
        ("At 6 PM tomorrow, I ___ my driving lesson.", "will be attending", "attended", "attend", "have attended"),
        ("By the end of this month, we ___ the entire course.", "will have completed", "complete", "completed", "are completing"),
        ("By next December, he ___ English for two years.", "will have been learning", "will learn", "learned", "is learning"),
        ("I ___ the report before the director arrives.", "will have submitted", "submit", "submitted", "am submitting"),
        ("This time next year, my brother ___ at a university abroad.", "will be studying", "studied", "studies", "has studied"),
        ("By midnight, the team ___ for twelve hours.", "will have been working", "will work", "worked", "are working"),
        ("She ___ the conference tomorrow afternoon.", "will be attending", "attended", "attends", "has attended"),
        ("By the time we get there, the movie ___.", "will have started", "starts", "started", "is starting"),
        ("At this time next Sunday, we ___ our final match.", "will be playing", "played", "play", "have played"),
        ("By 2035, scientists ___ new methods of treatment.", "will have developed", "develop", "developed", "are developing"),
        ("He ___ in the library for four hours by 8 PM.", "will have been studying", "will study", "studied", "is studying"),
        ("The company ___ its new branch next month.", "will open", "opened", "opening", "opens yesterday"),
        ("By tomorrow evening, I ___ all the emails.", "will have answered", "answer", "answered", "am answering"),
        ("At 11 AM tomorrow, the principal ___ the annual function.", "will be addressing", "addressed", "addresses", "has addressed"),
        ("By the end of the week, she ___ here for a month.", "will have been staying", "will stay", "stayed", "is staying"),
        ("They ___ the new software before the launch date.", "will have tested", "test", "tested", "are testing"),
    ],

    "Hard": [
        ("By the time the project is evaluated, the team ___ on it for eighteen months.", "will have been working", "will work", "has worked", "worked"),
        ("At this time next year, she ___ her postgraduate studies in Japan.", "will be pursuing", "pursued", "pursues", "has pursued"),
        ("By 2032, the scientists ___ the research for more than a decade.", "will have been conducting", "will conduct", "conducted", "are conducting"),
        ("The conference ___ by the time the delegates reach the venue.", "will have begun", "will begin", "began", "has begun"),
        ("By the end of this semester, I ___ all the required credits.", "will have earned", "earn", "earned", "am earning"),
        ("At 10 PM tonight, the technicians ___ the system upgrade.", "will be performing", "performed", "perform", "have performed"),
        ("By next April, he ___ in the organisation for fifteen years.", "will have been serving", "will serve", "served", "is serving"),
        ("Don't visit her at noon because she ___ an important interview.", "will be attending", "attended", "attends", "has attended"),
        ("By the time the deadline arrives, we ___ the proposal several times.", "will have revised", "revise", "revised", "are revising"),
        ("At this time tomorrow, the researchers ___ their findings to the panel.", "will be presenting", "presented", "present", "have presented"),
        ("By 2040, the city ___ significantly in population.", "will have grown", "grows", "grew", "is growing"),
        ("By the time she retires, she ___ children for thirty years.", "will have been teaching", "will teach", "taught", "is teaching"),
        ("The company ___ its annual financial report next Friday.", "will release", "released", "releasing", "has release"),
        ("By the time the guests arrive, the chef ___ the entire meal.", "will have prepared", "prepares", "prepared", "is preparing"),
        ("At 7 PM tomorrow, the committee ___ the final candidates.", "will be interviewing", "interviewed", "interviews", "has interviewed"),
        ("By the end of 2027, she ___ Japanese for three years.", "will have been learning", "will learn", "learned", "is learning"),
        ("The engineers ___ the bridge before the monsoon begins.", "will have completed", "complete", "completed", "are completing"),
        ("By the time you return, I ___ all the necessary arrangements.", "will have made", "make", "made", "am making"),
        ("At this time next month, the athletes ___ for the international tournament.", "will be training", "trained", "train", "have trained"),
        ("By 6 PM, he ___ continuously for eight hours.", "will have been driving", "will drive", "drove", "is driving"),
        ("The students ___ their final examination at this time next Monday.", "will be taking", "took", "take", "have taken"),
        ("By the time the new manager joins, the current manager ___ the transition.", "will have completed", "completes", "completed", "is completing"),
        ("By next September, they ___ in the new apartment for two years.", "will have been living", "will live", "lived", "are living"),
        ("At midnight, the security team ___ the premises.", "will be monitoring", "monitored", "monitors", "has monitored"),
        ("By the end of the decade, renewable energy ___ a larger share of electricity production.", "will have become", "becomes", "became", "is becoming"),
        ("By the time the programme ends, participants ___ several practical projects.", "will have completed", "complete", "completed", "are completing"),
        ("At 3 PM tomorrow, the legal team ___ the contract with the client.", "will be reviewing", "reviewed", "reviews", "has reviewed"),
        ("By January, the organisation ___ the new system for six months.", "will have been using", "will use", "used", "is using"),
        ("The director ___ the final decision after reviewing all the applications.", "will make", "made", "making", "has make"),
        ("By the time the exhibition closes, thousands of visitors ___ it.", "will have visited", "visit", "visited", "are visiting"),
    ]
}


def main():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    try:
        cur.execute(
            "SELECT id FROM lessons WHERE title=? AND topic=?",
            ("Future Tense", "English")
        )
        row = cur.fetchone()

        if not row:
            raise Exception("Lesson 'Future Tense' with topic 'English' was not found.")

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
                    (lesson_id, f"Future Tense - {difficulty}", difficulty)
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
        print("\nSUCCESS: Future Tense has exactly 90 questions!")

    except Exception as e:
        con.rollback()
        print("ERROR:", e)

    finally:
        con.close()


if __name__ == "__main__":
    main()
