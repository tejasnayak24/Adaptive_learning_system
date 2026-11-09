
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

BANK = {
    "Easy": [
        ("A person who teaches students.", "Teacher", "Doctor", "Farmer", "Driver"),
        ("A person who treats sick people.", "Doctor", "Lawyer", "Pilot", "Chef"),
        ("A person who writes books.", "Author", "Actor", "Painter", "Singer"),
        ("A person who flies an aircraft.", "Pilot", "Sailor", "Driver", "Guard"),
        ("A person who grows crops.", "Farmer", "Tailor", "Baker", "Carpenter"),
        ("A person who cuts and styles hair.", "Barber", "Plumber", "Mason", "Mechanic"),
        ("A person who prepares food professionally.", "Chef", "Judge", "Nurse", "Clerk"),
        ("A person who repairs water pipes.", "Plumber", "Electrician", "Carpenter", "Painter"),
        ("A person who makes wooden furniture.", "Carpenter", "Tailor", "Baker", "Potter"),
        ("A person who stitches clothes.", "Tailor", "Barber", "Farmer", "Driver"),
        ("A place where books are kept for reading.", "Library", "Museum", "Hospital", "Stadium"),
        ("A place where patients are treated.", "Hospital", "Library", "Factory", "Theatre"),
        ("A place where aircraft take off and land.", "Airport", "Harbour", "Station", "Market"),
        ("A place where animals are kept for public viewing.", "Zoo", "Library", "Bank", "School"),
        ("A place where historical objects are displayed.", "Museum", "Factory", "Office", "Restaurant"),
        ("A person who cannot read or write.", "Illiterate", "Intelligent", "Innocent", "Immature"),
        ("A person who loves his or her country.", "Patriot", "Tourist", "Foreigner", "Merchant"),
        ("A person who travels to different places for pleasure.", "Tourist", "Scientist", "Politician", "Artist"),
        ("A person who makes scientific discoveries.", "Scientist", "Journalist", "Sculptor", "Musician"),
        ("A person who performs on stage.", "Actor", "Doctor", "Farmer", "Engineer"),
        ("A person who sells goods in a shop.", "Shopkeeper", "Customer", "Teacher", "Patient"),
        ("A person who delivers letters and parcels.", "Postman", "Policeman", "Firefighter", "Pilot"),
        ("A person who protects people from danger.", "Bodyguard", "Accountant", "Librarian", "Author"),
        ("A person who makes bread and cakes.", "Baker", "Tailor", "Barber", "Plumber"),
        ("A person who paints pictures.", "Painter", "Singer", "Dancer", "Sailor"),
        ("A person who takes photographs.", "Photographer", "Geographer", "Biologist", "Astronomer"),
        ("A person who studies stars and planets.", "Astronomer", "Botanist", "Historian", "Chemist"),
        ("A person who looks after patients.", "Nurse", "Lawyer", "Pilot", "Carpenter"),
        ("A person who represents people in court.", "Lawyer", "Farmer", "Chef", "Driver"),
        ("A person who puts out fires.", "Firefighter", "Librarian", "Tailor", "Accountant")
    ],

    "Medium": [
        ("A person who studies plants.", "Botanist", "Zoologist", "Geologist", "Astronomer"),
        ("A person who studies animals.", "Zoologist", "Botanist", "Historian", "Physicist"),
        ("A person who studies the history of mankind.", "Historian", "Biologist", "Geologist", "Economist"),
        ("A person who studies the structure of the Earth.", "Geologist", "Psychologist", "Botanist", "Linguist"),
        ("A person who studies the human mind and behaviour.", "Psychologist", "Sociologist", "Archaeologist", "Economist"),
        ("A person who studies society and social relationships.", "Sociologist", "Psychologist", "Physicist", "Linguist"),
        ("A person who collects stamps.", "Philatelist", "Numismatist", "Bibliophile", "Cartographer"),
        ("A person who collects coins.", "Numismatist", "Philatelist", "Bibliophile", "Archaeologist"),
        ("A person who loves books.", "Bibliophile", "Philanthropist", "Misogynist", "Pessimist"),
        ("A person who loves mankind.", "Philanthropist", "Misanthrope", "Misogynist", "Narcissist"),
        ("A person who hates mankind.", "Misanthrope", "Philanthropist", "Optimist", "Patriot"),
        ("A person who believes that everything is predetermined.", "Fatalist", "Optimist", "Realist", "Idealist"),
        ("A person who expects the best in every situation.", "Optimist", "Pessimist", "Cynic", "Fatalist"),
        ("A person who expects the worst in every situation.", "Pessimist", "Optimist", "Idealist", "Realist"),
        ("A person who speaks many languages.", "Polyglot", "Monolingual", "Orator", "Translator"),
        ("A person who can speak two languages.", "Bilingual", "Monolingual", "Trilingual", "Polyglot"),
        ("A person who makes maps.", "Cartographer", "Calligrapher", "Biographer", "Photographer"),
        ("A person who writes the life story of another person.", "Biographer", "Autobiographer", "Novelist", "Editor"),
        ("A person who writes about his or her own life.", "Autobiographer", "Biographer", "Journalist", "Playwright"),
        ("A person who walks in sleep.", "Somnambulist", "Insomniac", "Optimist", "Hypochondriac"),
        ("A person who cannot sleep.", "Insomniac", "Somnambulist", "Amnesiac", "Misanthrope"),
        ("A person who eats too much.", "Glutton", "Vegetarian", "Gourmet", "Fasting"),
        ("A person who does not eat meat.", "Vegetarian", "Carnivore", "Omnivore", "Herbivore"),
        ("A person who eats both plants and animals.", "Omnivore", "Carnivore", "Herbivore", "Vegetarian"),
        ("A person who eats only plants.", "Herbivore", "Carnivore", "Omnivore", "Insectivore"),
        ("A person who is new to a profession or activity.", "Novice", "Veteran", "Expert", "Specialist"),
        ("A person with long experience in a profession.", "Veteran", "Novice", "Amateur", "Beginner"),
        ("A person who is unable to pay debts.", "Insolvent", "Wealthy", "Affluent", "Solvent"),
        ("A person who is legally appointed to manage another person's property.", "Trustee", "Debtor", "Creditor", "Tenant"),
        ("A person who is skilled in public speaking.", "Orator", "Novelist", "Sculptor", "Cartographer")
    ],

    "Hard": [
        ("Government by the people, directly or through elected representatives.", "Democracy", "Monarchy", "Oligarchy", "Autocracy"),
        ("Government by a king or queen.", "Monarchy", "Democracy", "Republic", "Anarchy"),
        ("Government by a small group of powerful people.", "Oligarchy", "Democracy", "Monarchy", "Theocracy"),
        ("Government by a single ruler with absolute power.", "Autocracy", "Democracy", "Republic", "Anarchy"),
        ("Government controlled by religious leaders.", "Theocracy", "Democracy", "Monarchy", "Oligarchy"),
        ("A government in which no authority is recognised.", "Anarchy", "Monarchy", "Democracy", "Theocracy"),
        ("The practice of having more than one spouse.", "Polygamy", "Monogamy", "Celibacy", "Bigotry"),
        ("The practice of having only one spouse at a time.", "Monogamy", "Polygamy", "Celibacy", "Patriarchy"),
        ("The practice of not marrying.", "Celibacy", "Monogamy", "Polygamy", "Bigamy"),
        ("The murder of a king.", "Regicide", "Patricide", "Matricide", "Fratricide"),
        ("The murder of one's father.", "Patricide", "Matricide", "Regicide", "Fratricide"),
        ("The murder of one's mother.", "Matricide", "Patricide", "Regicide", "Genocide"),
        ("The murder of one's brother.", "Fratricide", "Patricide", "Matricide", "Regicide"),
        ("The deliberate killing of a large group of people of a particular nationality or ethnic group.", "Genocide", "Regicide", "Homicide", "Suicide"),
        ("The killing of a human being by another human being.", "Homicide", "Genocide", "Regicide", "Fratricide"),
        ("The scientific study of the origin and development of words.", "Etymology", "Phonetics", "Syntax", "Semantics"),
        ("The study of the origin and history of place names.", "Toponymy", "Etymology", "Typography", "Phonology"),
        ("The study of the meaning of words and language.", "Semantics", "Syntax", "Phonetics", "Morphology"),
        ("The study of speech sounds.", "Phonetics", "Semantics", "Syntax", "Etymology"),
        ("The study of sentence structure and grammatical rules.", "Syntax", "Semantics", "Phonetics", "Etymology"),
        ("A person who believes in the existence of God.", "Theist", "Atheist", "Agnostic", "Sceptic"),
        ("A person who does not believe in the existence of God.", "Atheist", "Theist", "Agnostic", "Deist"),
        ("A person who believes that the existence of God is unknown or unknowable.", "Agnostic", "Atheist", "Theist", "Polytheist"),
        ("A person who believes in many gods.", "Polytheist", "Monotheist", "Atheist", "Agnostic"),
        ("A person who believes in one God.", "Monotheist", "Polytheist", "Atheist", "Agnostic"),
        ("A person who studies ancient societies through material remains.", "Archaeologist", "Anthropologist", "Geologist", "Palaeontologist"),
        ("A person who studies human societies and cultures.", "Anthropologist", "Archaeologist", "Sociologist", "Psychologist"),
        ("A person who studies fossils and prehistoric life.", "Palaeontologist", "Archaeologist", "Botanist", "Geographer"),
        ("A person who studies the science of language.", "Linguist", "Orator", "Cartographer", "Philatelist"),
        ("A person who is excessively concerned about their own importance and appearance.", "Narcissist", "Philanthropist", "Misanthrope", "Altruist")
    ]
}


def validate_bank():
    for difficulty, questions in BANK.items():
        if len(questions) != 30:
            raise ValueError(
                f"{difficulty} must contain exactly 30 questions."
            )

        for item in questions:
            if len(item) != 5:
                raise ValueError(f"Invalid question format: {item}")

            question, answer, wrong1, wrong2, wrong3 = item
            options = [answer, wrong1, wrong2, wrong3]

            if len(set(options)) != 4:
                raise ValueError(
                    f"Duplicate options in {difficulty}: {question}"
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
                ("One-Word Substitutions", "English")
            )
            row = cur.fetchone()

            if not row:
                raise Exception(
                    "Lesson 'One-Word Substitutions' with topic "
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
                            f"One-Word Substitutions - {difficulty}",
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
                "\nSUCCESS: One-Word Substitutions "
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
