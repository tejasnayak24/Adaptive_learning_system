
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

BANK = {
    "Easy": [
        ("I can ___ the birds singing.", "hear", "here", "hare", "hair"),
        ("The sun is very ___ today.", "bright", "bride", "brake", "write"),
        ("She ate a ___ of cake.", "piece", "peace", "peas", "pease"),
        ("The dog wagged ___ tail.", "its", "it's", "it", "itself"),
        ("I want to ___ a new bicycle.", "buy", "by", "bye", "bay"),
        ("The students are going ___ school.", "to", "too", "two", "tow"),
        ("The ___ is shining brightly.", "sun", "son", "soon", "sum"),
        ("Please write your name ___ the paper.", "on", "one", "won", "own"),
        ("The ___ of the mountain was covered with snow.", "peak", "peek", "pick", "peck"),
        ("I have ___ books on my desk.", "two", "to", "too", "tow"),
        ("The teacher asked us to ___ neatly.", "write", "right", "rite", "writ"),
        ("The knight rode a ___ horse.", "white", "quiet", "quite", "night"),
        ("We went to the ___ to swim.", "sea", "see", "she", "say"),
        ("The ___ is barking loudly.", "dog", "dug", "dig", "dag"),
        ("I ate a ___ for breakfast.", "pear", "pair", "pare", "peer"),
        ("Please ___ the door before leaving.", "close", "clothes", "claws", "clause"),
        ("The baby wore a ___ dress.", "blue", "blew", "blow", "below"),
        ("I ___ the answer to the question.", "know", "no", "now", "knew"),
        ("The wind ___ strongly yesterday.", "blew", "blue", "blow", "below"),
        ("She has long brown ___.", "hair", "hare", "hear", "here"),
        ("The teacher gave us a useful ___.", "lesson", "lessen", "listen", "listed"),
        ("We will ___ our grandparents tomorrow.", "meet", "meat", "mete", "mate"),
        ("The ___ of the story was interesting.", "tale", "tail", "tile", "tall"),
        ("Please ___ your shoes before entering.", "remove", "removal", "removable", "removes"),
        ("The flower has a red ___.", "petal", "pedal", "peddle", "petals"),
        ("I ___ a beautiful rainbow yesterday.", "saw", "sew", "so", "sow"),
        ("The ___ is dark and quiet.", "night", "knight", "neat", "net"),
        ("Please ___ your hands before eating.", "wash", "watch", "wish", "swish"),
        ("The ___ of the school addressed the students.", "principal", "principle", "prince", "principals"),
        ("I have to ___ my homework tonight.", "do", "due", "dew", "dough")
    ],

    "Medium": [
        ("The new rule will ___ everyone in the school.", "affect", "effect", "infect", "perfect"),
        ("The medicine had a positive ___ on the patient.", "effect", "affect", "effort", "affection"),
        ("The school ___ addressed the students.", "principal", "principle", "principality", "principled"),
        ("Honesty is an important moral ___.", "principle", "principal", "principality", "principled"),
        ("Please ___ your seat belt before driving.", "fasten", "faster", "fast", "fasting"),
        ("The company will ___ a new product next month.", "launch", "lunch", "lounge", "lynch"),
        ("The judge listened to the witness's ___.", "testimony", "testament", "testify", "testimonial"),
        ("The workers will ___ the damaged bridge.", "repair", "repay", "prepare", "repeat"),
        ("The farmer planted seeds in the ___.", "soil", "sole", "soul", "coil"),
        ("The ___ of the company approved the proposal.", "board", "bored", "broad", "boar"),
        ("The students were ___ during the long lecture.", "bored", "board", "boar", "broad"),
        ("The athlete ran around the ___.", "track", "tract", "trick", "truck"),
        ("The principal gave a short ___ at the assembly.", "speech", "species", "special", "speechless"),
        ("The artist used a ___ brush to paint the wall.", "coarse", "course", "cause", "corse"),
        ("The ___ of the river was strong.", "current", "currant", "currency", "curtain"),
        ("She bought a box of black ___.", "currants", "currents", "currencies", "curtains"),
        ("The detective followed the suspect's ___.", "trail", "trial", "trawl", "train"),
        ("The lawyer prepared for the court ___.", "trial", "trail", "trawl", "train"),
        ("The company will ___ its annual report tomorrow.", "release", "releases", "released", "releasing"),
        ("The ___ of the room needs painting.", "ceiling", "sealing", "sailing", "ceilings"),
        ("The patient was asked to ___ the medicine twice daily.", "take", "tack", "tech", "talk"),
        ("The ___ of the mountain was difficult to reach.", "summit", "submit", "summary", "somewhat"),
        ("The company will ___ the new policy immediately.", "implement", "compliment", "complement", "supplement"),
        ("The blue curtains ___ the colour of the walls.", "complement", "compliment", "implement", "supplement"),
        ("She received a lovely ___ on her presentation.", "compliment", "complement", "implement", "supplement"),
        ("The manager asked us to ___ the documents carefully.", "review", "revue", "revenue", "reveal"),
        ("The ___ of the company increased this year.", "revenue", "review", "revue", "reveal"),
        ("The soldiers were asked to ___ their position.", "defend", "depend", "define", "defer"),
        ("The ___ of the two candidates was difficult.", "choice", "choir", "chore", "chase"),
        ("The teacher asked the students to ___ the poem aloud.", "recite", "resight", "receipt", "reside")
    ],

    "Hard": [
        ("The company will ___ the new policy next week.", "adopt", "adapt", "adept", "opt"),
        ("The author had to ___ the novel for younger readers.", "adapt", "adopt", "adept", "opt"),
        ("The committee will ___ the proposal after discussion.", "accept", "except", "expect", "access"),
        ("Everyone attended the meeting ___ the manager.", "except", "accept", "expect", "access"),
        ("The scientist made an important ___ during the experiment.", "observation", "observance", "obstruction", "reservation"),
        ("The school celebrates the annual ___ of its foundation day.", "observance", "observation", "obstruction", "reservation"),
        ("The company decided to ___ the old equipment.", "discard", "disregard", "discover", "disclose"),
        ("The witness refused to ___ the confidential information.", "disclose", "discard", "disregard", "discover"),
        ("The new law will ___ the working conditions.", "affect", "effect", "infect", "reflect"),
        ("The new policy will have a positive ___ on employees.", "effect", "affect", "infect", "reflect"),
        ("The speaker gave an ___ explanation of the concept.", "elaborate", "eliminate", "elevate", "illustrate"),
        ("The company plans to ___ unnecessary expenses.", "eliminate", "elaborate", "elevate", "illustrate"),
        ("The judge asked the lawyer to present the legal ___.", "precedent", "president", "precedence", "preceding"),
        ("The ___ addressed the nation on television.", "president", "precedent", "precedence", "preceding"),
        ("The two musical performances were completely ___.", "complementary", "complimentary", "complement", "compliment"),
        ("The hotel offered ___ breakfast to its guests.", "complimentary", "complementary", "complement", "compliment"),
        ("The historian studied the ___ records carefully.", "historical", "historic", "historian", "history"),
        ("The signing of the treaty was a ___ event.", "historic", "historical", "historian", "history"),
        ("The company appointed new ___ to manage its operations.", "personnel", "personal", "person", "personify"),
        ("Please do not share your ___ details online.", "personal", "personnel", "person", "personify"),
        ("The manager asked the employee to ___ the report.", "revise", "review", "revive", "reveal"),
        ("The doctor advised the patient to ___ after surgery.", "recover", "discover", "uncover", "remove"),
        ("The company wants to ___ its customer service.", "enhance", "enforce", "enlarge", "ensure"),
        ("The police must ___ the law fairly.", "enforce", "enhance", "enlarge", "ensure"),
        ("The scientist tried to ___ the results of the experiment.", "verify", "vary", "clarify", "classify"),
        ("The teacher asked us to ___ the animals into groups.", "classify", "clarify", "verify", "vary"),
        ("The two departments must work in ___ with each other.", "cooperation", "corporation", "coordination", "competition"),
        ("The ___ of the business was discussed at the meeting.", "corporation", "cooperation", "coordination", "competition"),
        ("The manager asked the team to ___ the project before Friday.", "complete", "compete", "complain", "compare"),
        ("The two companies will ___ for the same contract.", "compete", "complete", "complain", "compare")
    ]
}


def validate_bank():
    for difficulty, questions in BANK.items():
        if len(questions) != 30:
            raise ValueError(
                f"{difficulty} must contain exactly 30 questions."
            )

        for question_data in questions:
            if len(question_data) != 5:
                raise ValueError(
                    f"Invalid question format: {question_data}"
                )

            question, answer, wrong1, wrong2, wrong3 = question_data
            options = [answer, wrong1, wrong2, wrong3]

            if len(set(options)) != 4:
                raise ValueError(
                    f"Duplicate options found in {difficulty}: {question}"
                )


def main():
    try:
        validate_bank()
        print("Question bank validation successful.")

        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()

        try:
            cur.execute(
                "SELECT id FROM lessons WHERE title=? AND topic=?",
                ("Homophones and Homonyms", "English")
            )
            row = cur.fetchone()

            if not row:
                raise Exception(
                    "Lesson 'Homophones and Homonyms' with topic "
                    "'English' was not found."
                )

            lesson_id = row[0]

            for difficulty, questions in BANK.items():

                cur.execute(
                    """
                    SELECT id FROM quizzes
                    WHERE lesson_id=? AND difficulty=?
                    """,
                    (lesson_id, difficulty)
                )
                quiz = cur.fetchone()

                if quiz:
                    quiz_id = quiz[0]
                else:
                    cur.execute(
                        """
                        INSERT INTO quizzes
                        (lesson_id, title, difficulty)
                        VALUES (?, ?, ?)
                        """,
                        (
                            lesson_id,
                            f"Homophones and Homonyms - {difficulty}",
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
                    random.shuffle(options)

                    correct_letter = "ABCD"[options.index(answer)]

                    question_text = question
                    suffix = 2

                    while True:
                        cur.execute(
                            """
                            SELECT COUNT(*) FROM questions
                            WHERE quiz_id=? AND question=?
                            """,
                            (quiz_id, question_text)
                        )

                        if cur.fetchone()[0] == 0:
                            break

                        question_text = f"{question} (Version {suffix})"
                        suffix += 1

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

                print(
                    f"{difficulty}: {final_count}/30 questions ready."
                )

            con.commit()
            print(
                "\nSUCCESS: Homophones and Homonyms "
                "has exactly 90 questions!"
            )

        except Exception as e:
            con.rollback()
            print("ERROR:", e)

        finally:
            con.close()

    except Exception as e:
        print("VALIDATION ERROR:", e)


if __name__ == "__main__":
    main()
