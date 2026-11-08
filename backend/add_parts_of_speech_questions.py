
import sqlite3
import random
from pathlib import Path

random.seed(42)

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"
TOPIC = "Parts of Speech"
SUBJECT = "English"

QUESTIONS = {
    "Easy": [
        ("Identify the noun: The dog is barking.", "dog", ["barking", "the", "is"]),
        ("Identify the verb: She sings beautifully.", "sings", ["she", "beautifully", "the"]),
        ("Identify the adjective: It is a beautiful flower.", "beautiful", ["flower", "is", "it"]),
        ("Identify the adverb: He runs quickly.", "quickly", ["runs", "he", "the"]),
        ("Which word is a pronoun?", "They", ["Table", "Quickly", "Beautiful"]),
        ("Identify the preposition: The book is on the table.", "on", ["book", "table", "is"]),
        ("Identify the conjunction: Ram and Shyam are friends.", "and", ["Ram", "friends", "are"]),
        ("Which word is an interjection?", "Wow!", ["Slowly", "Under", "Because"]),
        ("Identify the noun: The teacher entered the classroom.", "teacher", ["entered", "the", "quickly"]),
        ("Identify the verb: Birds fly in the sky.", "fly", ["birds", "sky", "the"]),
        ("Which word describes a noun?", "Adjective", ["Verb", "Pronoun", "Preposition"]),
        ("Which part of speech replaces a noun?", "Pronoun", ["Adverb", "Conjunction", "Interjection"]),
        ("Identify the adverb: She speaks softly.", "softly", ["speaks", "she", "the"]),
        ("Identify the adjective: He has a red car.", "red", ["car", "has", "he"]),
        ("Which word is a preposition?", "Behind", ["Happy", "Sing", "They"]),
        ("Which word is a conjunction?", "But", ["Beautiful", "Slowly", "Chair"]),
        ("Identify the pronoun: We are going to school.", "We", ["school", "going", "are"]),
        ("Identify the noun: Honesty is the best policy.", "Honesty", ["best", "is", "the"]),
        ("Identify the verb: The baby sleeps peacefully.", "sleeps", ["baby", "peacefully", "the"]),
        ("Which word expresses sudden emotion?", "Interjection", ["Noun", "Verb", "Adjective"]),
        ("Identify the adjective: She wore a lovely dress.", "lovely", ["wore", "dress", "she"]),
        ("Identify the adverb: He worked hard.", "hard", ["worked", "he", "the"]),
        ("Which word is a noun?", "Garden", ["Run", "Quickly", "Under"]),
        ("Which word is a verb?", "Dance", ["Beauty", "Blue", "They"]),
        ("Identify the preposition: The cat is under the chair.", "under", ["cat", "chair", "is"]),
        ("Identify the conjunction: I wanted to go, but it rained.", "but", ["wanted", "rained", "go"]),
        ("Which word is a pronoun?", "She", ["Apple", "Jump", "Slowly"]),
        ("Identify the interjection: Alas! We lost the match.", "Alas!", ["lost", "match", "we"]),
        ("Which part of speech names a person, place or thing?", "Noun", ["Verb", "Adverb", "Conjunction"]),
        ("Which part of speech shows an action?", "Verb", ["Noun", "Adjective", "Pronoun"]),
    ],

    "Medium": [
        ("Identify the adjective: The extremely tall building collapsed.", "tall", ["extremely", "building", "collapsed"]),
        ("Identify the adverb: She almost completed the assignment.", "almost", ["she", "completed", "assignment"]),
        ("Identify the pronoun: Everyone enjoyed the celebration.", "Everyone", ["enjoyed", "celebration", "the"]),
        ("Identify the preposition: The keys are beneath the newspaper.", "beneath", ["keys", "newspaper", "are"]),
        ("Identify the conjunction: Although it was raining, we continued.", "Although", ["raining", "continued", "was"]),
        ("Identify the verb: The committee has approved the proposal.", "approved", ["committee", "proposal", "the"]),
        ("Identify the noun: Her kindness impressed everyone.", "kindness", ["impressed", "her", "everyone"]),
        ("Identify the adverb: The children played happily.", "happily", ["children", "played", "the"]),
        ("Identify the adjective: Several students participated in the competition.", "Several", ["students", "participated", "competition"]),
        ("Identify the interjection: Hurray! Our team has won.", "Hurray!", ["team", "won", "our"]),
        ("Which word functions as a noun in this sentence: Swimming is good exercise.", "Swimming", ["good", "is", "exercise"]),
        ("Identify the verb: They have been waiting for hours.", "waiting", ["they", "hours", "for"]),
        ("Identify the preposition: She walked across the bridge.", "across", ["walked", "bridge", "she"]),
        ("Identify the conjunction: Neither Ravi nor Rahul attended.", "nor", ["Ravi", "attended", "neither"]),
        ("Identify the pronoun: This belongs to my sister.", "This", ["belongs", "sister", "my"]),
        ("Identify the adverb: He rarely makes mistakes.", "rarely", ["makes", "mistakes", "he"]),
        ("Identify the adjective: The ancient temple attracted tourists.", "ancient", ["temple", "attracted", "tourists"]),
        ("Identify the noun: The audience applauded loudly.", "audience", ["applauded", "loudly", "the"]),
        ("Identify the verb: The sun disappeared behind the clouds.", "disappeared", ["sun", "clouds", "behind"]),
        ("Which word is a conjunction in: Work hard so that you succeed.", "so that", ["work", "hard", "succeed"]),
        ("Identify the adverb: She answered the question correctly.", "correctly", ["answered", "question", "she"]),
        ("Identify the adjective: We visited a picturesque village.", "picturesque", ["visited", "village", "we"]),
        ("Identify the pronoun: Somebody left their umbrella here.", "Somebody", ["umbrella", "left", "here"]),
        ("Identify the preposition: The plane flew over the mountains.", "over", ["plane", "mountains", "flew"]),
        ("Identify the interjection: Bravo! You performed wonderfully.", "Bravo!", ["performed", "wonderfully", "you"]),
        ("Identify the noun: Childhood is a memorable stage.", "Childhood", ["memorable", "stage", "is"]),
        ("Identify the verb: The flowers have blossomed beautifully.", "blossomed", ["flowers", "beautifully", "the"]),
        ("Identify the adverb: The athlete ran exceptionally fast.", "exceptionally", ["athlete", "ran", "fast"]),
        ("Identify the adjective: Each participant received a certificate.", "Each", ["participant", "received", "certificate"]),
        ("Identify the conjunction: I will call you unless I get busy.", "unless", ["call", "busy", "you"]),
    ],

    "Hard": [
        ("Identify the part of speech of 'fast' in: She drives a fast car.", "Adjective", ["Adverb", "Noun", "Verb"]),
        ("Identify the part of speech of 'fast' in: She drives fast.", "Adverb", ["Adjective", "Noun", "Pronoun"]),
        ("Identify the part of speech of 'light' in: Please switch on the light.", "Noun", ["Adjective", "Verb", "Adverb"]),
        ("Identify the part of speech of 'light' in: This bag is light.", "Adjective", ["Noun", "Verb", "Conjunction"]),
        ("Identify the part of speech of 'before' in: I met her before.", "Adverb", ["Preposition", "Conjunction", "Noun"]),
        ("Identify the part of speech of 'before' in: Finish your work before dinner.", "Preposition", ["Adverb", "Verb", "Pronoun"]),
        ("Identify the part of speech of 'before' in: Finish your work before you leave.", "Conjunction", ["Preposition", "Adverb", "Adjective"]),
        ("Identify the gerund in: Reading improves vocabulary.", "Reading", ["improves", "vocabulary", "none"]),
        ("Identify the participle in: The broken window was repaired.", "broken", ["window", "repaired", "was"]),
        ("Identify the infinitive in: She wants to become a doctor.", "to become", ["wants", "doctor", "she"]),
        ("Identify the part of speech of 'well' in: She sings well.", "Adverb", ["Adjective", "Noun", "Verb"]),
        ("Identify the part of speech of 'well' in: She is well today.", "Adjective", ["Adverb", "Noun", "Preposition"]),
        ("Identify the part of speech of 'that' in: I know that he is honest.", "Conjunction", ["Pronoun", "Adjective", "Adverb"]),
        ("Identify the part of speech of 'that' in: That book is mine.", "Adjective", ["Conjunction", "Verb", "Adverb"]),
        ("Identify the part of speech of 'that' in: That is my house.", "Pronoun", ["Preposition", "Adjective", "Conjunction"]),
        ("Identify the part of speech of 'round' in: We walked round the park.", "Preposition", ["Noun", "Adjective", "Pronoun"]),
        ("Identify the part of speech of 'round' in: The children sat in a round circle.", "Adjective", ["Preposition", "Verb", "Adverb"]),
        ("Identify the part of speech of 'round' in: The earth is round.", "Adjective", ["Noun", "Conjunction", "Interjection"]),
        ("Identify the part of speech of 'since' in: I have lived here since 2020.", "Preposition", ["Conjunction", "Adverb", "Adjective"]),
        ("Identify the part of speech of 'since' in: Since you are here, we can begin.", "Conjunction", ["Preposition", "Noun", "Pronoun"]),
        ("Identify the part of speech of 'only' in: Only Riya answered correctly.", "Adverb", ["Adjective", "Noun", "Verb"]),
        ("Identify the part of speech of 'only' in: This is my only chance.", "Adjective", ["Adverb", "Pronoun", "Conjunction"]),
        ("Identify the part of speech of 'up' in: She climbed up the ladder.", "Preposition", ["Adjective", "Noun", "Pronoun"]),
        ("Identify the part of speech of 'up' in: Prices went up.", "Adverb", ["Noun", "Adjective", "Conjunction"]),
        ("Identify the part of speech of 'helping' in: She is helping her mother.", "Verb", ["Noun", "Adjective", "Adverb"]),
        ("Identify the part of speech of 'helping' in: Helping others is important.", "Noun", ["Verb", "Adjective", "Preposition"]),
        ("Identify the part of speech of 'empty' in: Please empty the box.", "Verb", ["Adjective", "Noun", "Adverb"]),
        ("Identify the part of speech of 'empty' in: The box is empty.", "Adjective", ["Verb", "Noun", "Pronoun"]),
        ("Identify the part of speech of 'but' in: Everyone but Rahul attended.", "Preposition", ["Conjunction", "Adverb", "Interjection"]),
        ("Identify the part of speech of 'but' in: I called him, but he did not answer.", "Conjunction", ["Preposition", "Adjective", "Noun"]),
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

            if not quiz:
                cursor.execute(
                    """
                    INSERT INTO quizzes (lesson_id, title, difficulty)
                    VALUES (?, ?, ?)
                    """,
                    (lesson_id, f"{TOPIC} - {difficulty}", difficulty)
                )
                quiz_id = cursor.lastrowid
            else:
                quiz_id = quiz[0]

            inserted = 0

            for question, answer, wrong_answers in questions:
                options = [answer] + wrong_answers

                if len(set(options)) != 4:
                    raise ValueError(f"Duplicate options in: {question}")

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

            total_inserted += inserted

            cursor.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                (quiz_id,)
            )
            final_count = cursor.fetchone()[0]

            print(
                f"{difficulty}: {inserted} inserted | "
                f"{final_count} total questions | Quiz ID: {quiz_id}"
            )

        connection.commit()

        print("\nSUCCESS!")
        print(f"New questions inserted: {total_inserted}")
        print(f"Expected total: 90")

    except Exception as error:
        connection.rollback()
        print("ERROR:", error)
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
