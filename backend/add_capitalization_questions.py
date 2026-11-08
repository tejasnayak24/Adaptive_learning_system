
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

BANK = {
    "Easy": [
        ("Which word should begin with a capital letter in 'i live in india'?", "I", "live", "in", "india"),
        ("Which is the correctly capitalized name?", "Ravi", "ravi", "RAVI", "raVi"),
        ("Which day is correctly capitalized?", "Monday", "monday", "MONDAY", "monDay"),
        ("Which month is correctly capitalized?", "January", "january", "JANUARY", "janUary"),
        ("Which sentence is correctly capitalized?", "She is my friend.", "she is my friend.", "She is my Friend.", "she Is my friend."),
        ("Which word should be capitalized in 'we visited delhi'?", "Delhi", "visited", "we", "the"),
        ("Which is the correct way to write the pronoun referring to oneself?", "I", "i", "Me", "my"),
        ("Which sentence is correctly capitalized?", "My name is Anu.", "my name is Anu.", "My name is anu.", "my Name is anu."),
        ("Which holiday is correctly capitalized?", "Christmas", "christmas", "CHRISTMAS", "christMas"),
        ("Which is the correctly capitalized country name?", "Japan", "japan", "JAPAN", "jaPan"),
        ("Which sentence begins correctly?", "Today is a sunny day.", "today is a sunny day.", "TODAY is a sunny day.", "toDay is a sunny day."),
        ("Which name is correctly capitalized?", "Priya", "priya", "PRIYA", "prIya"),
        ("Which is the correctly capitalized language?", "English", "english", "ENGLISH", "engLish"),
        ("Which sentence is correctly written?", "We study English.", "we study English.", "We study english.", "we study english."),
        ("Which is the correct capitalization of a city?", "Mumbai", "mumbai", "MUMBAI", "mUmbai"),
        ("Which sentence is correctly capitalized?", "I visited Mysuru.", "i visited Mysuru.", "I visited mysuru.", "i visited mysuru."),
        ("Which word should be capitalized in 'my birthday is in june'?", "June", "birthday", "is", "in"),
        ("Which is the correctly capitalized name of a school?", "Green Valley School", "green valley school", "GREEN VALLEY SCHOOL", "Green valley school"),
        ("Which sentence is correctly capitalized?", "Are you coming today?", "are you coming today?", "Are You Coming Today?", "are You coming today?"),
        ("Which is the correct capitalization of a continent?", "Asia", "asia", "ASIA", "aSia"),
        ("Which word should be capitalized in 'my brother speaks kannada'?", "Kannada", "brother", "speaks", "my"),
        ("Which sentence is correctly capitalized?", "My sister lives in India.", "my sister lives in India.", "My sister lives in india.", "my Sister lives in india."),
        ("Which is the correct capitalization of a person's title before a name?", "Dr. Sharma", "dr. Sharma", "DR. sharma", "dr. sharma"),
        ("Which word should be capitalized in 'we celebrate diwali'?", "Diwali", "celebrate", "we", "the"),
        ("Which sentence is correctly capitalized?", "He likes playing cricket.", "he likes playing cricket.", "He Likes playing cricket.", "he Likes Playing Cricket."),
        ("Which is the correctly capitalized name of an ocean?", "Pacific Ocean", "pacific ocean", "PACIFIC OCEAN", "Pacific ocean"),
        ("Which word should be capitalized in 'i am from karnataka'?", "Karnataka", "am", "from", "the"),
        ("Which sentence is correctly capitalized?", "Tomorrow is Friday.", "tomorrow is Friday.", "Tomorrow is friday.", "tomorrow is friday."),
        ("Which is the correctly capitalized name of a festival?", "Holi", "holi", "HOLI", "hoLi"),
        ("Which sentence is correctly capitalized?", "My favourite subject is Science.", "my favourite subject is Science.", "My favourite subject is science.", "my favourite Subject is science.")
    ],

    "Medium": [
        ("Which sentence correctly capitalizes a proper noun?", "The Taj Mahal is in Agra.", "The taj mahal is in Agra.", "The Taj Mahal is in agra.", "the Taj Mahal is in Agra."),
        ("Which sentence correctly uses capitalization in a title?", "The Adventures of Tom Sawyer", "the Adventures of Tom Sawyer", "The adventures of tom sawyer", "THE ADVENTURES OF TOM SAWYER"),
        ("Which sentence correctly capitalizes a nationality?", "My friend is Japanese.", "My friend is japanese.", "my friend is Japanese.", "My Friend is japanese."),
        ("Which sentence correctly capitalizes a geographical feature?", "We crossed the Himalayas.", "We crossed the himalayas.", "we crossed the Himalayas.", "We Crossed the himalayas."),
        ("Which sentence correctly capitalizes a person's name and title?", "Professor Mehta teaches mathematics.", "professor Mehta teaches mathematics.", "Professor mehta teaches mathematics.", "professor mehta teaches mathematics."),
        ("Which sentence correctly capitalizes a historical event?", "India celebrates Independence Day.", "India celebrates independence day.", "india celebrates Independence Day.", "India celebrates INDEPENDENCE DAY."),
        ("Which sentence correctly capitalizes a language?", "She is learning French.", "She is learning french.", "she is learning French.", "She is Learning french."),
        ("Which sentence correctly capitalizes a specific organization?", "The United Nations promotes peace.", "The united nations promotes peace.", "the United Nations promotes peace.", "The United Nations promotes Peace."),
        ("Which sentence correctly capitalizes a book title?", "I read The Jungle Book.", "I read the jungle book.", "I read The jungle book.", "i read The Jungle Book."),
        ("Which sentence correctly capitalizes a religious holiday?", "Eid is celebrated by many people.", "eid is celebrated by many people.", "Eid is celebrated by many People.", "eid is celebrated by many People."),
        ("Which sentence correctly capitalizes a direction when it names a region?", "They travelled across South India.", "They travelled across south India.", "They travelled across South india.", "they travelled across South India."),
        ("Which sentence correctly capitalizes a university name?", "She studies at Oxford University.", "She studies at oxford university.", "she studies at Oxford University.", "She studies at Oxford university."),
        ("Which sentence correctly capitalizes a historical period?", "The Renaissance changed European art.", "The renaissance changed European art.", "The Renaissance changed european art.", "the Renaissance changed European art."),
        ("Which sentence correctly capitalizes a person's initials?", "A. P. J. Abdul Kalam was a scientist.", "a. p. j. Abdul Kalam was a scientist.", "A. P. J. abdul kalam was a scientist.", "a. P. J. Abdul Kalam was a scientist."),
        ("Which sentence correctly capitalizes a government institution?", "The Supreme Court delivered its judgment.", "The supreme court delivered its judgment.", "the Supreme Court delivered its judgment.", "The Supreme court delivered its judgment."),
        ("Which sentence correctly capitalizes a specific newspaper name?", "I read The Hindu every morning.", "I read the hindu every morning.", "i read The Hindu every morning.", "I read The hindu every morning."),
        ("Which sentence correctly capitalizes a national monument?", "The Red Fort is in Delhi.", "The red fort is in Delhi.", "The Red Fort is in delhi.", "the Red Fort is in Delhi."),
        ("Which sentence correctly capitalizes a planet?", "Mars is called the Red Planet.", "mars is called the Red Planet.", "Mars is called the red planet.", "mars is called the red planet."),
        ("Which sentence correctly capitalizes a specific mountain range?", "The Alps are in Europe.", "The alps are in Europe.", "The Alps are in europe.", "the Alps are in Europe."),
        ("Which sentence correctly capitalizes a specific space mission?", "Apollo 11 landed on the Moon in 1969.", "apollo 11 landed on the Moon in 1969.", "Apollo 11 landed on the moon in 1969.", "Apollo 11 Landed on the Moon in 1969."),
        ("Which sentence correctly capitalizes a historical document?", "The Constitution of India came into effect in 1950.", "The constitution of India came into effect in 1950.", "The Constitution of india came into effect in 1950.", "the Constitution of India came into effect in 1950."),
        ("Which sentence correctly capitalizes a specific lake?", "Lake Victoria is in Africa.", "Lake victoria is in Africa.", "lake Victoria is in Africa.", "Lake Victoria is in africa."),
        ("Which sentence correctly capitalizes a specific political party?", "The Indian National Congress was founded in 1885.", "The indian national congress was founded in 1885.", "the Indian National Congress was founded in 1885.", "The Indian National congress was founded in 1885."),
        ("Which sentence correctly capitalizes a person's formal title?", "The President of India addressed the nation.", "The president of India addressed the nation.", "The President of india addressed the nation.", "the President of India addressed the nation."),
        ("Which sentence correctly capitalizes a specific historical war?", "World War II ended in 1945.", "World war II ended in 1945.", "World War ii ended in 1945.", "world War II ended in 1945."),
        ("Which sentence correctly capitalizes a specific region?", "The Sahara Desert is in Africa.", "The sahara desert is in Africa.", "The Sahara Desert is in africa.", "the Sahara Desert is in Africa."),
        ("Which sentence correctly capitalizes an official government department?", "The Ministry of Education announced the policy.", "The ministry of education announced the policy.", "The Ministry of education announced the policy.", "the Ministry of Education announced the policy."),
        ("Which sentence correctly capitalizes a specific river?", "The Nile flows through Egypt.", "The nile flows through Egypt.", "The Nile flows through egypt.", "the Nile flows through Egypt."),
        ("Which sentence correctly capitalizes a specific country and nationality?", "The Italian artist visited India.", "The italian artist visited India.", "The Italian artist visited india.", "the Italian artist visited India."),
        ("Which sentence correctly capitalizes a named historical movement?", "The French Revolution began in 1789.", "The french revolution began in 1789.", "The French revolution began in 1789.", "the French Revolution began in 1789.")
    ],

    "Hard": [
        ("Which sentence correctly capitalizes a specific space mission?", "Apollo 11 landed on the Moon in 1969.", "apollo 11 landed on the Moon in 1969.", "Apollo 11 landed on the moon in 1969.", "Apollo 11 Landed on the Moon in 1969."),
        ("Which sentence correctly capitalizes a formal title used before a name?", "Prime Minister Narendra Modi addressed the gathering.", "prime minister Narendra Modi addressed the gathering.", "Prime Minister narendra Modi addressed the gathering.", "prime minister narendra modi addressed the gathering."),
        ("Which sentence correctly uses capitalization in a book title?", "Pride and Prejudice is a famous novel.", "Pride And Prejudice is a famous novel.", "pride and prejudice is a famous novel.", "Pride and prejudice is a famous novel."),
        ("Which sentence correctly capitalizes a named historical treaty?", "The Treaty of Versailles was signed in 1919.", "The treaty of Versailles was signed in 1919.", "The Treaty of versailles was signed in 1919.", "the Treaty of Versailles was signed in 1919."),
        ("Which sentence correctly capitalizes a specific astronomical object?", "Halley's Comet is visible from Earth.", "halley's comet is visible from Earth.", "Halley's comet is visible from earth.", "halley's Comet is visible from earth."),
        ("Which sentence correctly capitalizes a specific court case?", "The case Brown v. Board of Education changed American education.", "The case brown v. board of education changed American education.", "The case Brown v. board of education changed American education.", "the case Brown v. Board of Education changed American education."),
        ("Which sentence correctly capitalizes a specific government body?", "The Parliament of India passed the bill.", "The parliament of India passed the bill.", "The Parliament of india passed the bill.", "the Parliament of India passed the bill."),
        ("Which sentence correctly capitalizes a named scientific theory?", "Einstein developed the theory of relativity.", "einstein developed the theory of relativity.", "Einstein developed the Theory of Relativity.", "Einstein developed the theory of Relativity."),
        ("Which sentence correctly capitalizes a specific international organization?", "The World Health Organization issued guidelines.", "The world health organization issued guidelines.", "The World health organization issued guidelines.", "the World Health Organization issued guidelines."),
        ("Which sentence correctly capitalizes a named historical document?", "The Magna Carta was signed in 1215.", "The magna carta was signed in 1215.", "The Magna carta was signed in 1215.", "the Magna Carta was signed in 1215."),
        ("Which sentence correctly capitalizes a specific geographical region?", "The Middle East has a rich history.", "The middle east has a rich history.", "The Middle east has a rich history.", "the Middle East has a rich history."),
        ("Which sentence correctly capitalizes a named university department?", "She works in the Department of Physics at the university.", "She works in the department of physics at the university.", "She works in the Department of physics at the university.", "she works in the Department of Physics at the university."),
        ("Which sentence correctly capitalizes a specific award?", "She received the Nobel Prize in Literature.", "She received the nobel prize in literature.", "She received the Nobel prize in Literature.", "she received the Nobel Prize in Literature."),
        ("Which sentence correctly capitalizes a named historical period?", "The Victorian Era influenced British literature.", "The victorian era influenced British literature.", "The Victorian era influenced british literature.", "the Victorian Era influenced British literature."),
        ("Which sentence correctly capitalizes a specific military operation?", "Operation Desert Storm began in 1991.", "Operation desert storm began in 1991.", "operation Desert Storm began in 1991.", "Operation Desert Storm began in nineteen ninety-one."),
        ("Which sentence correctly capitalizes a named religious text?", "The Bhagavad Gita is an important Hindu scripture.", "The bhagavad gita is an important Hindu scripture.", "The Bhagavad gita is an important hindu scripture.", "the Bhagavad Gita is an important Hindu scripture."),
        ("Which sentence correctly capitalizes a named scientific institution?", "NASA launched the spacecraft.", "Nasa launched the spacecraft.", "nasa launched the spacecraft.", "NaSa launched the spacecraft."),
        ("Which sentence correctly capitalizes a named historical revolution?", "The Industrial Revolution transformed manufacturing.", "The industrial revolution transformed manufacturing.", "The Industrial revolution transformed manufacturing.", "the Industrial Revolution transformed manufacturing."),
        ("Which sentence correctly capitalizes a specific ocean?", "The Atlantic Ocean separates Europe and North America.", "The atlantic ocean separates Europe and North America.", "The Atlantic ocean separates Europe and North America.", "the Atlantic Ocean separates Europe and North America."),
        ("Which sentence correctly capitalizes a named political document?", "The Declaration of Independence was adopted in 1776.", "The declaration of independence was adopted in 1776.", "The Declaration of independence was adopted in 1776.", "the Declaration of Independence was adopted in 1776."),
        ("Which sentence correctly capitalizes a specific historical battle?", "The Battle of Plassey took place in 1757.", "The battle of Plassey took place in 1757.", "The Battle of plassey took place in 1757.", "the Battle of Plassey took place in 1757."),
        ("Which sentence correctly capitalizes a named international agreement?", "The Paris Agreement addresses climate change.", "The paris agreement addresses climate change.", "The Paris agreement addresses climate change.", "the Paris Agreement addresses climate change."),
        ("Which sentence correctly capitalizes a specific named building?", "The White House is located in Washington, D.C.", "The white house is located in Washington, D.C.", "The White House is located in washington, D.C.", "the White House is located in Washington, D.C."),
        ("Which sentence correctly capitalizes a specific named spacecraft?", "Voyager 1 sent data from interstellar space.", "voyager 1 sent data from interstellar space.", "Voyager 1 sent data from Interstellar Space.", "Voyager one sent data from interstellar space."),
        ("Which sentence correctly capitalizes a named historical dynasty?", "The Mughal Empire ruled large parts of India.", "The mughal empire ruled large parts of India.", "The Mughal empire ruled large parts of India.", "the Mughal Empire ruled large parts of India."),
        ("Which sentence correctly capitalizes a named scientific law?", "Newton's laws of motion explain the relationship between force and motion.", "Newton's Laws of Motion explain the relationship between force and motion.", "newton's laws of motion explain the relationship between force and motion.", "Newton's laws of motion explain the relationship between Force and Motion."),
        ("Which sentence correctly capitalizes a specific named festival?", "The Cannes Film Festival is held in France.", "The cannes film festival is held in France.", "The Cannes film festival is held in France.", "the Cannes Film Festival is held in France."),
        ("Which sentence correctly capitalizes a named geographical landmark?", "Mount Everest is the world's highest mountain above sea level.", "Mount everest is the world's highest mountain above sea level.", "mount Everest is the world's highest mountain above sea level.", "Mount Everest is the World's Highest Mountain above sea level."),
        ("Which sentence correctly capitalizes a named historical agreement?", "The Simla Agreement was signed in 1972.", "The simla agreement was signed in 1972.", "The Simla agreement was signed in 1972.", "the Simla Agreement was signed in 1972."),
        ("Which sentence correctly capitalizes a specific space telescope?", "The James Webb Space Telescope observes distant galaxies.", "The james webb space telescope observes distant galaxies.", "The James Webb space telescope observes distant galaxies.", "the James Webb Space Telescope observes distant galaxies.")
    ]
}


def main():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    try:
        cur.execute(
            "SELECT id FROM lessons WHERE title=? AND topic=?",
            ("Capitalization", "English")
        )

        row = cur.fetchone()

        if not row:
            raise Exception("Capitalization lesson was not found.")

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
                        f"Capitalization - {difficulty}",
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

            print(
                f"{difficulty}: {final_count}/30 questions ready."
            )

        con.commit()

        print("\nSUCCESS: Capitalization has exactly 90 questions!")
        print("Easy: 30 | Medium: 30 | Hard: 30")

    except Exception as e:
        con.rollback()
        print("ERROR:", e)

    finally:
        con.close()


if __name__ == "__main__":
    main()
