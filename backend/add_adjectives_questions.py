
import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"
TOPIC = "Adjectives"
SUBJECT = "English"

QUESTIONS = {
    "Easy": [
        ("Identify the adjective: She has a beautiful dress.", "beautiful", ["She", "Has", "Dress"]),
        ("Choose the adjective: The tall boy is my brother.", "tall", ["Boy", "Brother", "My"]),
        ("Which word describes colour?", "Red", ["Run", "Quickly", "Under"]),
        ("Choose the correct adjective: It is a ___ day.", "sunny", ["Sun", "Sunshine", "Sunnily"]),
        ("Identify the adjective: The clever student answered correctly.", "clever", ["Student", "Answered", "Correctly"]),
        ("Choose the adjective: I have three pencils.", "three", ["I", "Have", "Pencils"]),
        ("Identify the adjective: The little baby is sleeping.", "little", ["Baby", "Sleeping", "Is"]),
        ("Choose the correct adjective: This is a ___ flower.", "beautiful", ["Beautifully", "Beauty", "Beautify"]),
        ("Which word describes size?", "Huge", ["Slowly", "Jump", "There"]),
        ("Identify the adjective: The old man walked slowly.", "old", ["Man", "Walked", "Slowly"]),
        ("Choose the adjective: She bought a red handbag.", "red", ["Bought", "Handbag", "She"]),
        ("Which is an adjective of quantity?", "Some", ["Run", "Quickly", "Behind"]),
        ("Choose the correct adjective: The mango is ___.", "sweet", ["Sweetly", "Sweetness", "Sweeten"]),
        ("Identify the adjective: He lives in a small house.", "small", ["Lives", "House", "He"]),
        ("Choose the adjective: There are many students in the classroom.", "many", ["There", "Students", "Classroom"]),
        ("Which word describes a person's appearance?", "Beautiful", ["Beauty", "Beautify", "Beautifully"]),
        ("Identify the adjective: The hungry child wanted food.", "hungry", ["Child", "Wanted", "Food"]),
        ("Choose the correct adjective: The elephant is a ___ animal.", "large", ["Largely", "Larger", "Largeness"]),
        ("Which is a demonstrative adjective in 'This book is interesting'?", "This", ["Book", "Interesting", "Is"]),
        ("Choose the adjective: My father drives a new car.", "new", ["Father", "Drives", "Car"]),
        ("Identify the adjective: The water is cold.", "cold", ["Water", "Is", "The"]),
        ("Choose the correct adjective: She is a ___ girl.", "kind", ["Kindly", "Kindness", "Kinderly"]),
        ("Which word describes age?", "Young", ["Quickly", "Jump", "Under"]),
        ("Identify the adjective: The brave soldier fought well.", "brave", ["Soldier", "Fought", "Well"]),
        ("Choose the adjective: I ate two apples.", "two", ["Ate", "Apples", "I"]),
        ("Which is a possessive adjective?", "My", ["Mine", "Me", "Myself"]),
        ("Identify the adjective: The noisy children disturbed the class.", "noisy", ["Children", "Disturbed", "Class"]),
        ("Choose the correct adjective: The road is ___.", "narrow", ["Narrowly", "Narrowness", "Narrowing"]),
        ("Which word describes taste?", "Bitter", ["Bitterly", "Taste", "Eating"]),
        ("Identify the adjective: We watched an exciting movie.", "exciting", ["Watched", "Movie", "We"]),
    ],

    "Medium": [
        ("Choose the comparative form of 'tall'.", "Taller", ["Tallest", "More tall", "Tallly"]),
        ("Choose the superlative form of 'good'.", "Best", ["Better", "Goodest", "More good"]),
        ("Choose the comparative form of 'beautiful'.", "More beautiful", ["Beautifuler", "Most beautiful", "Beautifuller"]),
        ("Identify the quantitative adjective: She has little patience.", "little", ["She", "Patience", "Has"]),
        ("Identify the demonstrative adjective: Those houses are expensive.", "Those", ["Houses", "Expensive", "Are"]),
        ("Choose the correct adjective: This is the ___ of the two routes.", "shorter", ["Shortest", "More short", "Most short"]),
        ("Choose the correct adjective: Mount Everest is the ___ mountain in the world.", "highest", ["Higher", "High", "More high"]),
        ("Identify the distributive adjective: Each student received a certificate.", "Each", ["Student", "Received", "Certificate"]),
        ("Choose the correct adjective: She is ___ than her sister.", "more intelligent", ["Most intelligent", "Intelligenter", "Intelligentest"]),
        ("Identify the adjective of quantity: There is enough food for everyone.", "enough", ["Food", "Everyone", "There"]),
        ("Choose the correct form: This is the ___ solution to the problem.", "simplest", ["Simpler", "More simple", "Simplely"]),
        ("Identify the possessive adjective: Their house is near the school.", "Their", ["House", "Near", "School"]),
        ("Choose the correct adjective: This road is ___ than that one.", "wider", ["Widest", "More wide", "Most wide"]),
        ("Identify the adjective of number: Several students participated.", "Several", ["Students", "Participated", "None"]),
        ("Choose the correct form: She is the ___ player on the team.", "best", ["Better", "Good", "More good"]),
        ("Identify the proper adjective: We enjoy Italian food.", "Italian", ["Food", "Enjoy", "We"]),
        ("Choose the correct adjective: The weather is becoming ___.", "worse", ["Worst", "Badly", "Badder"]),
        ("Identify the adjective in: The first chapter is interesting.", "first", ["Chapter", "Interesting", "Is"]),
        ("Choose the correct form: Gold is ___ than silver.", "more expensive", ["Most expensive", "Expensiver", "Expensivest"]),
        ("Identify the adjective of quantity: He drank sufficient water.", "sufficient", ["Drank", "Water", "He"]),
        ("Choose the correct adjective: This is a ___ difficult question.", "rather", ["Much", "Many", "Few"]),
        ("Choose the correct form: Of all the students, Riya is the ___.", "most hardworking", ["More hardworking", "Hardworkinger", "Hardworking"]),
        ("Identify the adjective: The elderly woman crossed the road.", "elderly", ["Woman", "Crossed", "Road"]),
        ("Choose the correct adjective: I have ___ money than you.", "less", ["Few", "Littlely", "Least"]),
        ("Identify the interrogative adjective: Which book do you prefer?", "Which", ["Book", "Prefer", "You"]),
        ("Choose the correct form: This exercise is ___ than the previous one.", "easier", ["Easiest", "More easy", "Most easy"]),
        ("Identify the adjective of number: There are five chairs in the room.", "five", ["Chairs", "Room", "There"]),
        ("Choose the correct adjective: He is senior ___ me.", "to", ["Than", "From", "With"]),
        ("Choose the correct form: The Pacific is the ___ ocean.", "largest", ["Larger", "Large", "More large"]),
        ("Identify the adjective: The former captain addressed the team.", "former", ["Captain", "Addressed", "Team"]),
    ],

    "Hard": [
        ("Choose the correct form: She is one of the ___ students in the class.", "most diligent", ["more diligent", "diligenter", "diligentest"]),
        ("Choose the correct adjective: Of the two sisters, Meera is the ___.", "elder", ["eldest", "oldest", "most old"]),
        ("Identify the adjective clause: The book that I borrowed was fascinating.", "that I borrowed", ["The book", "Was fascinating", "Fascinating"]),
        ("Choose the correct form: No other metal is as ___ as platinum in this comparison.", "valuable", ["more valuable", "most valuable", "valuabler"]),
        ("Identify the compound adjective: She bought a well-known painting.", "well-known", ["Painting", "Bought", "She"]),
        ("Choose the correct adjective: This is the ___ of the two alternatives.", "better", ["Best", "Good", "More good"]),
        ("Identify the participial adjective: The frightened child ran away.", "frightened", ["Child", "Ran", "Away"]),
        ("Choose the correct form: The situation is ___ than we expected.", "worse", ["worst", "bad", "more bad"]),
        ("Identify the adjective phrase: The girl with long hair is my cousin.", "with long hair", ["The girl", "Is my cousin", "My cousin"]),
        ("Choose the correct adjective: He is junior ___ his colleague.", "to", ["than", "from", "with"]),
        ("Identify the absolute adjective: The answer is perfect.", "perfect", ["Answer", "Is", "The"]),
        ("Choose the correct form: This is the ___ performance of her career.", "finest", ["Finer", "More fine", "Most fine"]),
        ("Identify the adjective clause: Students who work hard usually succeed.", "who work hard", ["Students", "Usually succeed", "Hard"]),
        ("Choose the correct form: She is ___ of the two candidates.", "the more experienced", ["the most experienced", "more experienced", "most experienced"]),
        ("Identify the adjective used as a noun: The rich should help the poor.", "rich", ["Should", "Help", "The"]),
        ("Choose the correct adjective: The task was ___ difficult for the beginners.", "too", ["Enough", "Many", "Several"]),
        ("Identify the compound adjective: He gave a last-minute presentation.", "last-minute", ["Presentation", "Gave", "He"]),
        ("Choose the correct form: This is the ___ possible explanation.", "simplest", ["simpler", "more simple", "simple"]),
        ("Identify the adjective phrase: The house near the river belongs to us.", "near the river", ["The house", "Belongs to us", "The river"]),
        ("Choose the correct form: The climate here is ___ than in the desert.", "less extreme", ["least extreme", "more less extreme", "extremest"]),
        ("Identify the participial adjective: The movie was disappointing.", "disappointing", ["Movie", "Was", "The"]),
        ("Choose the correct form: She has the ___ experience among all applicants.", "least", ["less", "few", "littlely"]),
        ("Identify the adjective clause: I met a man whose daughter is a doctor.", "whose daughter is a doctor", ["I met a man", "A doctor", "I met"]),
        ("Choose the correct form: The more you practise, the ___ you become.", "better", ["best", "good", "more good"]),
        ("Identify the demonstrative adjective: Such behaviour is unacceptable.", "Such", ["Behaviour", "Unacceptable", "Is"]),
        ("Choose the correct form: This is by far the ___ route to the station.", "shortest", ["shorter", "more short", "most short"]),
        ("Identify the adjective: The main reason for the delay was traffic.", "main", ["Reason", "Delay", "Traffic"]),
        ("Choose the correct form: She is as ___ as her brother.", "intelligent", ["more intelligent", "most intelligent", "intelligenter"]),
        ("Identify the adjective clause: The place where we met is now a museum.", "where we met", ["The place", "Is now a museum", "A museum"]),
        ("Choose the correct form: Of the three proposals, this one is the ___.", "most practical", ["more practical", "practicaler", "practical"]),
    ],
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
            raise ValueError("Adjectives lesson not found.")

        lesson_id = lesson[0]
        total_inserted = 0

        for difficulty, questions in QUESTIONS.items():

            if len(questions) != 30:
                raise ValueError(
                    f"{difficulty} contains {len(questions)} questions."
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

            for question, answer, wrong_answers in questions:

                options = [answer] + wrong_answers

                if len(set(options)) != 4:
                    raise ValueError(
                        f"Duplicate options: {question}"
                    )

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

                total_inserted += 1

            cursor.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                (quiz_id,)
            )
            count = cursor.fetchone()[0]

            print(f"{difficulty}: {count}/30 questions")

            if count != 30:
                raise ValueError(
                    f"{difficulty} has {count} questions instead of 30."
                )

        connection.commit()

        print("\nSUCCESS!")
        print(f"New questions inserted: {total_inserted}")
        print("Adjectives completed: 90/90 MCQs.")

    except Exception as error:
        connection.rollback()
        print("ERROR:", error)
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
