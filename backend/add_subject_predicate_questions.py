
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

BANK = {
    "Easy": [
        ("In 'The boy is playing cricket', identify the subject.", "The boy", "is playing cricket", "playing", "cricket"),
        ("In 'Birds fly in the sky', identify the predicate.", "fly in the sky", "Birds", "in the sky", "the sky"),
        ("What is the subject in 'Ravi reads a book'?", "Ravi", "reads", "a book", "reads a book"),
        ("What is the predicate in 'The sun shines brightly'?", "shines brightly", "The sun", "sun", "brightly"),
        ("Identify the subject in 'My mother cooks dinner'.", "My mother", "cooks", "dinner", "cooks dinner"),
        ("Identify the predicate in 'The children are laughing'.", "are laughing", "The children", "children", "laughing"),
        ("In 'Dogs bark loudly', what is the subject?", "Dogs", "bark", "loudly", "bark loudly"),
        ("In 'The teacher explains the lesson', what is the predicate?", "explains the lesson", "The teacher", "the lesson", "teacher"),
        ("Identify the subject in 'A beautiful flower bloomed'.", "A beautiful flower", "bloomed", "beautiful", "flower bloomed"),
        ("Identify the predicate in 'The baby is sleeping'.", "is sleeping", "The baby", "baby", "sleeping"),
        ("In 'Students study every day', identify the subject.", "Students", "study", "every day", "study every day"),
        ("What is the predicate in 'The train arrived late'?", "arrived late", "The train", "train", "late"),
        ("Identify the subject in 'My friends play football'.", "My friends", "play", "football", "play football"),
        ("Identify the predicate in 'The cat chased the mouse'.", "chased the mouse", "The cat", "the mouse", "cat"),
        ("In 'The birds are singing', what is the subject?", "The birds", "are singing", "singing", "birds are singing"),
        ("In 'The girl opened the door', what is the predicate?", "opened the door", "The girl", "the door", "girl"),
        ("Identify the subject in 'A little puppy is barking'.", "A little puppy", "is barking", "barking", "little"),
        ("Identify the predicate in 'The stars shine at night'.", "shine at night", "The stars", "at night", "stars"),
        ("In 'My father drives a car', what is the subject?", "My father", "drives", "a car", "drives a car"),
        ("What is the predicate in 'The flowers look fresh'?", "look fresh", "The flowers", "flowers", "fresh"),
        ("Identify the subject in 'The old man walks slowly'.", "The old man", "walks slowly", "slowly", "old"),
        ("Identify the predicate in 'The children played outside'.", "played outside", "The children", "children", "outside"),
        ("In 'An elephant has a long trunk', identify the subject.", "An elephant", "has", "a long trunk", "long trunk"),
        ("What is the predicate in 'The river flows gently'?", "flows gently", "The river", "river", "gently"),
        ("Identify the subject in 'The doctor treats patients'.", "The doctor", "treats", "patients", "treats patients"),
        ("Identify the predicate in 'The moon looks bright'.", "looks bright", "The moon", "moon", "bright"),
        ("In 'Our school has a library', what is the subject?", "Our school", "has", "a library", "library"),
        ("What is the predicate in 'The horse runs fast'?", "runs fast", "The horse", "horse", "fast"),
        ("Identify the subject in 'A farmer grows crops'.", "A farmer", "grows", "crops", "grows crops"),
        ("Identify the predicate in 'The wind is blowing strongly'.", "is blowing strongly", "The wind", "wind", "strongly")
    ],

    "Medium": [
        ("In 'The tall boy with curly hair won the race', identify the complete subject.", "The tall boy with curly hair", "The tall boy", "won the race", "curly hair"),
        ("In 'The students in the classroom are preparing for the exam', identify the complete predicate.", "are preparing for the exam", "The students in the classroom", "the classroom", "preparing"),
        ("What is the simple subject in 'The little girl with a red bag is singing'?", "girl", "The little girl", "red bag", "is singing"),
        ("What is the simple predicate in 'The old man walked slowly across the road'?", "walked", "old man", "walked slowly across the road", "road"),
        ("Identify the compound subject in 'Ravi and Priya are classmates'.", "Ravi and Priya", "are classmates", "Priya", "classmates"),
        ("Identify the compound predicate in 'The dog barked and chased the cat'.", "barked and chased", "The dog", "the cat", "barked"),
        ("In 'The book on the table belongs to my sister', what is the simple subject?", "book", "The book on the table", "table", "belongs"),
        ("In 'My brother and his friends went to the park', what is the complete subject?", "My brother and his friends", "went to the park", "his friends", "the park"),
        ("Identify the complete predicate in 'The little birds built a nest in the tree'.", "built a nest in the tree", "The little birds", "a nest", "in the tree"),
        ("What is the simple predicate in 'The children have been playing outside'?", "have been playing", "children", "outside", "have"),
        ("In 'The captain of the team scored a goal', identify the complete subject.", "The captain of the team", "The captain", "scored a goal", "the team"),
        ("Which sentence has a compound subject?", "Rita and Sita dance well.", "Rita dances well.", "The girl dances well.", "She dances well."),
        ("Which sentence has a compound predicate?", "He cooked dinner and washed the dishes.", "He cooked dinner.", "Dinner was delicious.", "The dishes were clean."),
        ("In 'The man wearing a blue shirt is my uncle', identify the simple subject.", "man", "The man wearing a blue shirt", "blue shirt", "uncle"),
        ("Identify the complete predicate in 'Our new English teacher speaks fluently'.", "speaks fluently", "Our new English teacher", "English teacher", "fluently"),
        ("In 'The birds and squirrels live in the garden', identify the compound subject.", "The birds and squirrels", "live in the garden", "the garden", "squirrels"),
        ("Which part is the simple predicate in 'The hardworking students completed the assignment'?", "completed", "hardworking students", "completed the assignment", "assignment"),
        ("In 'A group of tourists visited the museum', identify the complete subject.", "A group of tourists", "tourists", "visited the museum", "the museum"),
        ("Which sentence contains a compound predicate?", "The baby smiled and waved.", "The baby smiled.", "The baby was happy.", "The smiling baby waved."),
        ("In 'The keys to the main door are missing', what is the simple subject?", "keys", "The keys to the main door", "main door", "are missing"),
        ("Identify the complete predicate in 'Several students from our college won prizes'.", "won prizes", "Several students from our college", "our college", "several students"),
        ("Which is the complete subject in 'The manager of the company announced the results'?", "The manager of the company", "The manager", "announced the results", "the company"),
        ("In 'My cousins and I visited the science museum', identify the complete predicate.", "visited the science museum", "My cousins and I", "the science museum", "cousins and I"),
        ("What is the simple subject in 'The quality of these products is excellent'?", "quality", "products", "The quality of these products", "excellent"),
        ("Which sentence contains a compound subject and a compound predicate?", "Ravi and Aman sang and danced.", "Ravi sang beautifully.", "Aman danced well.", "Ravi and Aman are friends."),
        ("In 'The woman with the green umbrella waited patiently', identify the simple predicate.", "waited", "woman", "waited patiently", "green umbrella"),
        ("Identify the complete subject in 'Those beautiful paintings on the wall belong to my aunt'.", "Those beautiful paintings on the wall", "Those paintings", "belong to my aunt", "my aunt"),
        ("In 'The teacher checked the notebooks and returned them', identify the compound predicate.", "checked the notebooks and returned them", "The teacher", "the notebooks", "returned them"),
        ("Which part is the complete predicate in 'The little boy near the gate dropped his lunchbox'?", "dropped his lunchbox", "The little boy near the gate", "near the gate", "his lunchbox"),
        ("In 'Neither the principal nor the teachers were present', identify the compound subject.", "Neither the principal nor the teachers", "were present", "the teachers", "the principal")
    ],

    "Hard": [
        ("In 'Running every morning improves physical fitness', identify the complete subject.", "Running every morning", "improves physical fitness", "every morning", "physical fitness"),
        ("In 'What she said surprised everyone', identify the subject.", "What she said", "surprised everyone", "everyone", "she"),
        ("In 'There are several books on the shelf', what is the grammatical subject?", "several books", "There", "on the shelf", "are"),
        ("In 'To forgive others requires courage', identify the complete subject.", "To forgive others", "requires courage", "others", "courage"),
        ("In 'The person who called you is my uncle', identify the complete subject.", "The person who called you", "The person", "who called you", "is my uncle"),
        ("In 'Although it was raining, the match continued', identify the subject of the main clause.", "the match", "it", "Although it was raining", "continued"),
        ("In 'The teacher gave the students extra homework', identify the simple predicate.", "gave", "teacher", "extra homework", "students"),
        ("In 'Swimming in the ocean can be dangerous', identify the simple subject.", "Swimming", "ocean", "can be dangerous", "dangerous"),
        ("In 'The committee has announced its decision', identify the complete predicate.", "has announced its decision", "The committee", "its decision", "announced"),
        ("In 'Neither the manager nor the employees were available', identify the compound subject.", "Neither the manager nor the employees", "were available", "the employees", "the manager"),
        ("In 'The girl who won the competition received a trophy', identify the subject of the main clause.", "The girl who won the competition", "who won the competition", "received a trophy", "a trophy"),
        ("In 'It is important to follow the rules', what is the grammatical subject?", "It", "to follow the rules", "the rules", "important"),
        ("In 'To learn a new language takes patience', identify the complete predicate.", "takes patience", "To learn a new language", "a new language", "patience"),
        ("In 'The players, exhausted after the match, returned home', identify the simple subject.", "players", "exhausted", "returned", "home"),
        ("In 'The person responsible for the mistake has apologized', identify the complete predicate.", "has apologized", "The person responsible for the mistake", "the mistake", "responsible"),
        ("In 'Where the road ends remains unknown', identify the subject.", "Where the road ends", "remains unknown", "the road", "unknown"),
        ("In 'The captain, along with the players, was honoured', identify the simple subject.", "captain", "players", "The captain along with the players", "was honoured"),
        ("In 'There was a sudden change in the weather', identify the grammatical subject.", "a sudden change", "There", "in the weather", "was"),
        ("In 'The books that you borrowed from me are overdue', identify the complete subject.", "The books that you borrowed from me", "The books", "that you borrowed from me", "are overdue"),
        ("In 'Walking through the forest, the explorers discovered a cave', identify the complete predicate.", "discovered a cave", "the explorers", "Walking through the forest", "a cave"),
        ("In 'The rich and the poor deserve equal opportunities', identify the compound subject.", "The rich and the poor", "deserve equal opportunities", "equal opportunities", "the poor"),
        ("In 'The news that the team had won delighted the fans', identify the simple subject.", "news", "team", "fans", "delighted"),
        ("In 'What the scientist discovered changed our understanding', identify the complete predicate.", "changed our understanding", "What the scientist discovered", "the scientist", "our understanding"),
        ("In 'The house, together with its gardens, was sold', identify the simple subject.", "house", "gardens", "The house together with its gardens", "was sold"),
        ("In 'To travel around the world is her greatest ambition', identify the simple subject.", "To travel", "world", "her greatest ambition", "is"),
        ("In 'The students who had completed their work were allowed to leave', identify the simple predicate.", "were allowed", "students", "completed", "leave"),
        ("In 'Honesty and integrity are essential qualities', identify the compound subject.", "Honesty and integrity", "are essential qualities", "essential qualities", "integrity"),
        ("In 'The reason why he resigned remains unclear', identify the simple subject.", "reason", "he", "resigned", "unclear"),
        ("In 'If the weather improves, we will go hiking', identify the subject of the subordinate clause.", "the weather", "we", "hiking", "will go"),
        ("In 'Close the door quietly', identify the implied subject.", "You", "I", "We", "They")
    ]
}


def main():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    try:
        cur.execute(
            "SELECT id FROM lessons WHERE title=? AND topic=?",
            ("Subject and Predicate", "English")
        )

        row = cur.fetchone()

        if not row:
            raise Exception(
                "Lesson 'Subject and Predicate' with topic 'English' was not found."
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
                        f"Subject and Predicate - {difficulty}",
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

        print("\nSUCCESS: Subject and Predicate has exactly 90 questions!")
        print("Easy: 30 | Medium: 30 | Hard: 30")

    except Exception as e:
        con.rollback()
        print("ERROR:", e)

    finally:
        con.close()


if __name__ == "__main__":
    main()
