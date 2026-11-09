
import sqlite3
import random
from pathlib import Path

random.seed(42)

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"
TOPIC = "Nouns"
SUBJECT = "English"

QUESTIONS = {
    "Easy": [
        ("Identify the noun: The girl is reading.", "girl", ["reading", "is", "the"]),
        ("Which of these is a proper noun?", "India", ["country", "city", "village"]),
        ("Which of these is a common noun?", "teacher", ["Ramesh", "London", "Monday"]),
        ("Identify the abstract noun.", "Honesty", ["Table", "Pencil", "Garden"]),
        ("Which word is a collective noun?", "Team", ["Player", "Ball", "Coach"]),
        ("Identify the noun: The dog chased the cat.", "dog", ["chased", "the", "quickly"]),
        ("Which is a material noun?", "Gold", ["Chair", "School", "Child"]),
        ("What is the plural of child?", "Children", ["Childs", "Childes", "Childrens"]),
        ("What is the plural of mouse?", "Mice", ["Mouses", "Mouse", "Mices"]),
        ("Which is a countable noun?", "Apple", ["Water", "Milk", "Rice"]),
        ("Which is an uncountable noun?", "Sugar", ["Book", "Pen", "Chair"]),
        ("Identify the proper noun: Rahul lives in Delhi.", "Rahul", ["lives", "in", "the"]),
        ("Which word names a person?", "Doctor", ["Hospital", "Medicine", "Treatment"]),
        ("Which word names a place?", "Library", ["Teacher", "Student", "Book"]),
        ("Which word names a thing?", "Computer", ["Running", "Beautiful", "Quickly"]),
        ("Identify the abstract noun.", "Bravery", ["Soldier", "Sword", "Battle"]),
        ("Which is a collective noun for birds?", "Flock", ["Crow", "Wing", "Feather"]),
        ("What is the plural of box?", "Boxes", ["Boxs", "Boxies", "Boxen"]),
        ("What is the singular form of leaves?", "Leaf", ["Leafs", "Leave", "Leavs"]),
        ("Which is a proper noun?", "Monday", ["Month", "Day", "Week"]),
        ("Identify the noun: The baby smiled happily.", "baby", ["smiled", "happily", "the"]),
        ("Which is a collective noun for players?", "Team", ["Player", "Game", "Ground"]),
        ("Which is an abstract noun?", "Kindness", ["Kind", "Person", "House"]),
        ("What is the plural of tooth?", "Teeth", ["Tooths", "Toothes", "Toothies"]),
        ("Which is a material noun?", "Silver", ["Bottle", "Window", "Teacher"]),
        ("Identify the common noun.", "River", ["Ganga", "India", "Ravi"]),
        ("Which is a collective noun for cattle?", "Herd", ["Cow", "Bull", "Calf"]),
        ("What is the plural of city?", "Cities", ["Citys", "Cityes", "Citis"]),
        ("Which noun represents a feeling?", "Happiness", ["Chair", "School", "Bottle"]),
        ("Identify the noun: Birds build nests.", "nests", ["build", "birds", "the"]),
    ],

    "Medium": [
        ("Identify the abstract noun formed from 'wise'.", "Wisdom", ["Wiser", "Wisely", "Wise"]),
        ("What is the collective noun for a group of wolves?", "Pack", ["Flock", "Bunch", "Fleet"]),
        ("Which sentence contains a proper noun?", "Maya visited Paris.", ["The girl visited a city.", "A student read a book.", "The boy played outside."]),
        ("Identify the material noun: The ring is made of gold.", "gold", ["ring", "made", "the"]),
        ("Which noun is uncountable?", "Furniture", ["Chair", "Table", "Cupboard"]),
        ("Choose the correct plural of phenomenon.", "Phenomena", ["Phenomenons", "Phenomenas", "Phenomenae"]),
        ("Choose the correct plural of analysis.", "Analyses", ["Analysises", "Analysis", "Analysies"]),
        ("Which is a compound noun?", "Toothbrush", ["Quickly", "Beautiful", "Running"]),
        ("Identify the abstract noun in: Childhood is precious.", "Childhood", ["precious", "is", "none"]),
        ("Which is a collective noun for sailors?", "Crew", ["Ship", "Ocean", "Captain"]),
        ("Identify the noun functioning as the subject: The students completed the task.", "students", ["completed", "task", "the"]),
        ("Which sentence uses a possessive noun correctly?", "The girl's bag is blue.", ["The girls bag is blue.", "The girl bag's is blue.", "The girls's bag is blue."]),
        ("Choose the correct plural of cactus.", "Cacti", ["Cactuseses", "Cactis", "Cactus"]),
        ("What is the abstract noun of 'strong'?", "Strength", ["Strongly", "Stronger", "Strongest"]),
        ("Which is a collective noun for musicians?", "Band", ["Song", "Instrument", "Stage"]),
        ("Identify the common noun: Dr. Sharma works at a hospital.", "hospital", ["Dr. Sharma", "Sharma", "none"]),
        ("Which word is a countable noun?", "Suitcase", ["Information", "Advice", "Luggage"]),
        ("Choose the correct plural of criterion.", "Criteria", ["Criterions", "Criterias", "Criteriones"]),
        ("Identify the abstract noun: Her patience impressed everyone.", "patience", ["impressed", "everyone", "her"]),
        ("Which is a compound noun?", "Mother-in-law", ["Motherly", "Loving", "Mothers"]),
        ("What is the collective noun for a group of judges?", "Panel", ["Courtroom", "Law", "Verdict"]),
        ("Which noun is formed from the verb 'decide'?", "Decision", ["Decisive", "Deciding", "Decided"]),
        ("Choose the correct plural of ox.", "Oxen", ["Oxes", "Oxs", "Oxies"]),
        ("Identify the noun in: The committee reached a decision.", "committee", ["reached", "a", "the"]),
        ("Which is a proper noun?", "Pacific Ocean", ["ocean", "sea", "river"]),
        ("Which sentence contains an abstract noun?", "Freedom is valuable.", ["The bird is flying.", "The table is wooden.", "The child is playing."]),
        ("Which is a collective noun for bees?", "Swarm", ["Hive", "Honey", "Wing"]),
        ("What is the plural of radius?", "Radii", ["Radiuseses", "Radiis", "Radius"]),
        ("Identify the noun formed from 'perform'.", "Performance", ["Performing", "Performed", "Performerly"]),
        ("Which is an uncountable noun?", "Equipment", ["Machine", "Tool", "Device"]),
    ],

    "Hard": [
        ("Identify the function of 'swimming' in: Swimming is an excellent exercise.", "Gerund functioning as a noun", ["Present participle functioning as an adjective", "Finite verb", "Adverb"]),
        ("Identify the noun clause: What he said surprised everyone.", "What he said", ["surprised everyone", "everyone", "said surprised"]),
        ("Identify the appositive noun phrase: My brother, a talented musician, plays the piano.", "a talented musician", ["My brother", "plays the piano", "the piano"]),
        ("Which sentence contains a noun used as an adjective?", "She bought a school bag.", ["She went to school.", "The school is large.", "The children study."]),
        ("Identify the abstract noun formed from 'able'.", "Ability", ["Able", "Ably", "Enable"]),
        ("Which is the correct plural of syllabus?", "Syllabuses", ["Syllabuss", "Syllabiess", "Syllabii"]),
        ("Which is the correct plural of oasis?", "Oases", ["Oasises", "Oasis", "Oasies"]),
        ("Identify the noun phrase: The tall boy with curly hair won the prize.", "The tall boy with curly hair", ["won the prize", "with curly hair", "curly hair"]),
        ("Identify the gerund phrase: Walking along the beach relaxes me.", "Walking along the beach", ["along the beach", "relaxes me", "the beach"]),
        ("Which sentence contains a noun clause functioning as an object?", "I believe that she is honest.", ["That she is honest.", "She is honest.", "I believe her."]),
        ("Identify the abstract noun in: His refusal surprised the manager.", "refusal", ["surprised", "manager", "his"]),
        ("Which is the correct plural of appendix?", "Appendices", ["Appendixs", "Appendixes only", "Appendicies"]),
        ("Identify the compound noun written as one word.", "Notebook", ["Note taking", "Well-known", "In front of"]),
        ("Which sentence contains a noun in the possessive case?", "The children's toys are scattered.", ["The children are playing.", "The toys are scattered.", "Children enjoy toys."]),
        ("Identify the noun clause in: Whoever arrives first will receive a prize.", "Whoever arrives first", ["will receive a prize", "a prize", "arrives first"]),
        ("Which noun is derived from the adjective 'deep'?", "Depth", ["Deeply", "Deepen", "Deeper"]),
        ("Identify the verbal noun in: The building of the bridge took years.", "building", ["bridge", "took", "years"]),
        ("Which sentence uses a collective noun as a single unit?", "The committee has announced its decision.", ["The committee have disagreed among themselves.", "The members are arguing.", "Several members left."]),
        ("Choose the correct plural of memorandum.", "Memoranda", ["Memorandums", "Memorandii", "Memorandum"]),
        ("Identify the noun phrase functioning as the object: She admired the beautiful painting.", "the beautiful painting", ["She", "admired", "beautiful"]),
        ("Which is an example of a concrete noun?", "Perfume", ["Honesty", "Freedom", "Wisdom"]),
        ("Which is an example of an abstract noun?", "Justice", ["Judge", "Court", "Lawyer"]),
        ("Identify the noun clause: The fact that he resigned shocked us.", "that he resigned", ["The fact", "shocked us", "us"]),
        ("Which sentence contains a gerund used as the object of a preposition?", "She is interested in painting.", ["Painting is enjoyable.", "She paints daily.", "She bought a painting."]),
        ("What is the correct plural of analysis?", "Analyses", ["Analysis", "Analysises", "Analysies"]),
        ("Identify the noun formed from the verb 'arrive'.", "Arrival", ["Arriving", "Arrived", "Arrivable"]),
        ("Which sentence contains a noun phrase in apposition?", "Riya, my closest friend, lives nearby.", ["Riya lives nearby.", "My friend lives nearby.", "She lives nearby."]),
        ("Identify the noun clause functioning as the subject: Why he left remains unknown.", "Why he left", ["remains unknown", "unknown", "he left"]),
        ("Which is the correct plural of alumnus?", "Alumni", ["Alumnuses", "Alumnis", "Alumnas"]),
        ("Identify the abstract noun in: Their generosity helped the villagers.", "generosity", ["helped", "villagers", "their"]),
    ]
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
            raise ValueError(f"Lesson '{TOPIC}' not found under {SUBJECT}.")

        lesson_id = lesson[0]
        total_inserted = 0

        for difficulty, questions in QUESTIONS.items():

            if len(questions) != 30:
                raise ValueError(
                    f"{difficulty} has {len(questions)} questions instead of 30."
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

            inserted = 0

            for question, answer, wrong_answers in questions:

                options = [answer] + wrong_answers

                if len(set(options)) != 4:
                    raise ValueError(f"Duplicate options: {question}")

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

                inserted += 1

            cursor.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                (quiz_id,)
            )

            final_count = cursor.fetchone()[0]

            print(
                f"{difficulty}: {inserted} inserted | "
                f"{final_count} total questions | Quiz ID: {quiz_id}"
            )

            total_inserted += inserted

        connection.commit()

        print("\nSUCCESS!")
        print(f"New questions inserted: {total_inserted}")
        print("Expected: 90 questions (30 Easy + 30 Medium + 30 Hard)")

    except Exception as error:
        connection.rollback()
        print("ERROR:", error)
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
