
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

BANK = {
    "Easy": [
        ("I like tea ___ coffee.", "and", "but", "or", "because"),
        ("She is poor ___ honest.", "but", "and", "or", "so"),
        ("Hurry up ___ you will miss the bus.", "or", "and", "because", "although"),
        ("I stayed home ___ it was raining.", "because", "but", "or", "and"),
        ("He is tall ___ his brother is short.", "but", "and", "so", "because"),
        ("Would you like tea ___ coffee?", "or", "and", "but", "because"),
        ("She studied hard ___ she passed the exam.", "so", "but", "or", "although"),
        ("I will call you ___ I reach home.", "when", "but", "or", "because"),
        ("He cannot read ___ write.", "or", "and", "but", "so"),
        ("___ it was cold, we went outside.", "Although", "Because", "So", "And"),
        ("Wait here ___ I return.", "until", "because", "but", "or"),
        ("She smiled ___ she saw her friend.", "when", "but", "or", "so"),
        ("He is intelligent ___ hardworking.", "and", "but", "or", "because"),
        ("I was tired, ___ I continued working.", "but", "because", "or", "so"),
        ("Take an umbrella ___ it may rain.", "because", "but", "and", "or"),
        ("You can stay here ___ leave now.", "or", "and", "but", "because"),
        ("She sings ___ dances beautifully.", "and", "but", "or", "although"),
        ("He failed ___ he did not study.", "because", "but", "or", "and"),
        ("I will wait ___ you come back.", "until", "because", "but", "so"),
        ("She was hungry ___ she ate lunch.", "so", "but", "or", "although"),
        ("He is young ___ experienced.", "but", "and", "or", "because"),
        ("We stayed indoors ___ it was raining.", "because", "although", "or", "and"),
        ("Study well ___ you will succeed.", "and", "but", "or", "although"),
        ("She was late ___ she missed the bus.", "so", "but", "or", "although"),
        ("I will go ___ you come with me.", "if", "but", "and", "because"),
        ("He works hard ___ earns well.", "and", "but", "or", "although"),
        ("You must hurry ___ you will be late.", "or", "and", "because", "although"),
        ("She is happy ___ she won the prize.", "because", "but", "or", "and"),
        ("He waited ___ the train arrived.", "until", "because", "but", "or"),
        ("I like him ___ he is kind.", "because", "but", "or", "although")
    ],

    "Medium": [
        ("She will succeed ___ she works hard.", "if", "unless", "although", "whereas"),
        ("You cannot enter ___ you have a ticket.", "unless", "because", "although", "while"),
        ("___ he was tired, he completed the work.", "Although", "Because", "Unless", "So"),
        ("I will attend the meeting ___ I am busy.", "even if", "because", "so", "therefore"),
        ("He is not only intelligent ___ also hardworking.", "but", "and", "or", "so"),
        ("She is both talented ___ disciplined.", "and", "but", "or", "although"),
        ("Neither Ravi ___ Rohan attended the meeting.", "nor", "or", "and", "but"),
        ("Either you ___ your brother must complete the task.", "or", "nor", "and", "but"),
        ("He studied hard; ___, he failed.", "however", "therefore", "because", "moreover"),
        ("She was ill; ___, she attended the class.", "nevertheless", "therefore", "because", "so"),
        ("I do not know ___ he will come.", "whether", "because", "although", "unless"),
        ("She waited ___ her mother returned.", "until", "because", "although", "unless"),
        ("He is older ___ I am.", "than", "then", "because", "although"),
        ("___ you practise regularly, you will improve.", "If", "Unless", "Although", "Whereas"),
        ("He speaks as ___ he knows everything.", "if", "because", "unless", "although"),
        ("She left early ___ she could catch the train.", "so that", "although", "unless", "whereas"),
        ("I will not go ___ you invite me.", "unless", "because", "although", "while"),
        ("He was working ___ his friends were playing.", "while", "because", "unless", "therefore"),
        ("She is more experienced ___ her colleague.", "than", "then", "as", "because"),
        ("___ you finish your work, you cannot leave.", "Until", "Although", "Because", "Whereas"),
        ("He failed ___ he had worked hard.", "although", "because", "so", "therefore"),
        ("She was so tired ___ she fell asleep immediately.", "that", "than", "while", "unless"),
        ("No sooner had he arrived ___ it started raining.", "than", "when", "then", "while"),
        ("Hardly had I reached home ___ the phone rang.", "when", "than", "while", "because"),
        ("She is neither lazy ___ careless.", "nor", "or", "and", "but"),
        ("He will come ___ you call him.", "if", "although", "unless", "whereas"),
        ("I stayed awake ___ I could finish the assignment.", "so that", "although", "unless", "whereas"),
        ("___ the teacher entered, the students became silent.", "As soon as", "Unless", "Although", "Whereas"),
        ("He prefers reading ___ watching television.", "to", "than", "over", "from"),
        ("She continued working ___ she was exhausted.", "even though", "because", "so", "unless")
    ],

    "Hard": [
        ("Scarcely had the match begun ___ it started raining.", "when", "than", "while", "because"),
        ("No sooner had she arrived ___ the meeting started.", "than", "when", "then", "while"),
        ("Not only did he win the race, ___ he also broke the record.", "but", "and", "or", "so"),
        ("Neither the manager ___ the employees were informed.", "nor", "or", "and", "but"),
        ("He behaves as though he ___ the owner.", "were", "is", "has", "will"),
        ("___ you apologize, I will not forgive you.", "Unless", "Although", "Because", "While"),
        ("The more you practise, ___ better you become.", "the", "a", "an", "than"),
        ("She is such a good speaker ___ everyone listens carefully.", "that", "than", "although", "unless"),
        ("He worked hard, ___ he could achieve his goal.", "so that", "although", "unless", "whereas"),
        ("Whether you agree ___ disagree, the decision is final.", "or", "and", "but", "nor"),
        ("He would rather walk ___ take a taxi.", "than", "then", "as", "because"),
        ("I will support you ___ you are right.", "provided that", "although", "whereas", "unless"),
        ("___ he had little experience, he performed exceptionally well.", "Although", "Because", "Since", "So"),
        ("She was so intelligent ___ she solved the problem quickly.", "that", "than", "unless", "while"),
        ("He neither called me ___ sent a message.", "nor", "or", "and", "but"),
        ("You must complete the work, ___ you will lose your opportunity.", "otherwise", "although", "because", "whereas"),
        ("The project was successful ___ everyone contributed equally.", "because", "although", "unless", "whereas"),
        ("I will remain here ___ you return.", "until", "because", "although", "unless"),
        ("He talks ___ he were an expert.", "as if", "because", "unless", "so that"),
        ("She cannot attend the event ___ she finishes her examination.", "until", "although", "because", "whereas"),
        ("The weather was pleasant, ___ we decided to go hiking.", "so", "although", "unless", "whereas"),
        ("___ he is rich, he is not generous.", "Although", "Because", "Since", "So"),
        ("He must study harder ___ he wants to pass.", "if", "unless", "although", "whereas"),
        ("The students remained silent ___ the principal was speaking.", "while", "because", "unless", "therefore"),
        ("She is as hardworking ___ her sister.", "as", "than", "then", "so"),
        ("He was absent, ___ nobody knew the reason.", "but", "because", "so that", "although"),
        ("I will help you ___ you tell me the truth.", "provided that", "although", "whereas", "unless"),
        ("___ you work consistently, you will not achieve your goal.", "Unless", "Although", "Because", "Since"),
        ("He not only completed the assignment ___ submitted it early.", "but also", "and also", "or else", "so that"),
        ("She had barely entered the room ___ the lights went out.", "when", "than", "while", "because")
    ]
}


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    try:
        cur.execute("""
            SELECT id FROM lessons
            WHERE title = ? AND topic = ?
        """, ("Conjunctions", "English"))

        result = cur.fetchone()

        if not result:
            raise Exception("Conjunctions lesson not found.")

        lesson_id = result[0]
        print(f"Conjunctions lesson found: ID {lesson_id}")

        for difficulty in ["Easy", "Medium", "Hard"]:

            cur.execute("""
                SELECT id FROM quizzes
                WHERE lesson_id = ?
                AND LOWER(difficulty) = LOWER(?)
            """, (lesson_id, difficulty))

            quiz = cur.fetchone()

            if quiz:
                quiz_id = quiz[0]
            else:
                cur.execute("""
                    INSERT INTO quizzes (lesson_id, title, difficulty)
                    VALUES (?, ?, ?)
                """, (lesson_id, f"Conjunctions - {difficulty}", difficulty))

                quiz_id = cur.lastrowid

            cur.execute("""
                SELECT question FROM questions WHERE quiz_id = ?
            """, (quiz_id,))

            existing_questions = {row[0] for row in cur.fetchall()}

            cur.execute("""
                SELECT COUNT(*) FROM questions WHERE quiz_id = ?
            """, (quiz_id,))

            current_count = cur.fetchone()[0]

            if current_count > 30:
                raise Exception(
                    f"{difficulty} already has {current_count} questions. "
                    "Please check the database."
                )

            inserted = 0

            for index, item in enumerate(BANK[difficulty], start=1):

                if current_count >= 30:
                    break

                question_text, answer, wrong1, wrong2, wrong3 = item

                question = (
                    f"Conjunctions MCQ {difficulty} {index}: {question_text}"
                )

                original_question = question
                version = 2

                while question in existing_questions:
                    question = f"{original_question} (Version {version})"
                    version += 1

                options = [answer, wrong1, wrong2, wrong3]

                if len(set(options)) != 4:
                    raise Exception(f"Duplicate options found: {question}")

                random.shuffle(options)
                correct_answer = "ABCD"[options.index(answer)]

                cur.execute("""
                    INSERT INTO questions (
                        quiz_id, question, option_a, option_b,
                        option_c, option_d, correct_answer
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    quiz_id, question,
                    options[0], options[1], options[2], options[3],
                    correct_answer
                ))

                existing_questions.add(question)
                current_count += 1
                inserted += 1

            cur.execute("""
                SELECT COUNT(*) FROM questions WHERE quiz_id = ?
            """, (quiz_id,))

            final_count = cur.fetchone()[0]

            print(
                f"{difficulty}: {final_count}/30 questions "
                f"({inserted} newly inserted)"
            )

            if final_count != 30:
                raise Exception(
                    f"{difficulty} has {final_count} questions instead of 30."
                )

        con.commit()
        print("\nSUCCESS! Conjunctions completed: 90/90 MCQs.")

    except Exception as error:
        con.rollback()
        print(f"\nERROR: {error}")
        raise

    finally:
        con.close()


if __name__ == "__main__":
    main()
