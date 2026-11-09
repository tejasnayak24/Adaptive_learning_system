
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

# Format: (question, correct answer, wrong1, wrong2, wrong3)

BANK = {
    "Easy": [
        ("Which figure of speech compares two things using 'like' or 'as'?", "Simile", "Metaphor", "Personification", "Irony"),
        ("Which figure of speech directly compares two different things without using 'like' or 'as'?", "Metaphor", "Simile", "Alliteration", "Onomatopoeia"),
        ("Which figure of speech gives human qualities to non-human things?", "Personification", "Hyperbole", "Oxymoron", "Allusion"),
        ("Which literary device involves deliberate exaggeration?", "Hyperbole", "Simile", "Euphemism", "Pun"),
        ("Which literary device uses words that imitate sounds?", "Onomatopoeia", "Metaphor", "Irony", "Symbolism"),
        ("Which figure of speech repeats the same initial consonant sound in nearby words?", "Alliteration", "Assonance", "Metaphor", "Hyperbole"),
        ("Identify the figure of speech: 'The stars danced in the sky.'", "Personification", "Simile", "Pun", "Litotes"),
        ("Identify the simile: 'Her smile was like sunshine.'", "Like sunshine", "Her smile", "Was", "Sunshine"),
        ("Which device is used in the expression 'I have told you a million times'?", "Hyperbole", "Metaphor", "Alliteration", "Oxymoron"),
        ("What is an idiom?", "An expression with a meaning different from its literal words", "A word that imitates a sound", "A repeated vowel sound", "A type of punctuation"),
        ("What is a rhyme?", "The repetition of similar ending sounds", "The repetition of sentence meanings", "The use of opposite ideas", "The description of a character"),
        ("Which device is used in 'Peter Piper picked a peck of pickled peppers'?", "Alliteration", "Metaphor", "Irony", "Euphemism"),
        ("What is symbolism?", "Using an object or image to represent a deeper meaning", "Repeating the same word accidentally", "Using only factual statements", "Writing without descriptive language"),
        ("Which literary device creates humour through a play on words?", "Pun", "Simile", "Personification", "Allusion"),
        ("What is irony?", "A contrast between expectation and reality or intended meaning", "A direct comparison using like", "The repetition of initial sounds", "An imitation of natural sounds"),
        ("Which figure of speech is used in 'The classroom was a zoo'?", "Metaphor", "Simile", "Alliteration", "Onomatopoeia"),
        ("Identify the onomatopoeia in 'The bees buzzed around the flowers.'", "Buzzed", "Flowers", "Around", "The"),
        ("Which device is used in 'The wind whispered softly'?", "Personification", "Hyperbole", "Pun", "Oxymoron"),
        ("What is a proverb?", "A short saying expressing general wisdom or advice", "A word imitating a sound", "A comparison using like", "A fictional character"),
        ("Which literary device repeats a word or phrase for emphasis?", "Repetition", "Metaphor", "Euphemism", "Irony"),
        ("What is a contrast in literary writing?", "Showing differences between two ideas or things", "Repeating a sound", "Imitating an animal sound", "Giving human qualities to objects"),
        ("Which phrase is an example of an oxymoron?", "Deafening silence", "Bright sunshine", "Running quickly", "Blue sky"),
        ("Which figure of speech is used in 'He is as brave as a lion'?", "Simile", "Metaphor", "Pun", "Irony"),
        ("What is a rhetorical question?", "A question asked for effect rather than an actual answer", "A question that must have a numerical answer", "A question used only in examinations", "A question without punctuation"),
        ("Which device is used in 'Time is a thief'?", "Metaphor", "Simile", "Alliteration", "Onomatopoeia"),
        ("What is a stanza in poetry?", "A group of lines forming a unit in a poem", "The title of a novel", "A type of character", "A sentence in a paragraph"),
        ("What is imagery in literature?", "Descriptive language that appeals to the senses", "A list of grammatical rules", "A collection of unrelated facts", "A type of punctuation"),
        ("Which device is used in 'The leaves whispered secrets'?", "Personification", "Simile", "Pun", "Euphemism"),
        ("Which literary device is used in 'Tick-tock went the clock'?", "Onomatopoeia", "Metaphor", "Irony", "Allusion"),
        ("What is the purpose of figures of speech?", "To make language more expressive and meaningful", "To remove all emotion from writing", "To replace every sentence with numbers", "To eliminate descriptive language")
    ],

    "Medium": [
        ("Which figure of speech repeats vowel sounds in nearby words?", "Assonance", "Alliteration", "Consonance", "Onomatopoeia"),
        ("Which device repeats consonant sounds, often within or at the ends of words?", "Consonance", "Assonance", "Simile", "Hyperbole"),
        ("Which figure of speech involves a deliberate understatement?", "Litotes", "Hyperbole", "Personification", "Onomatopoeia"),
        ("What is an allusion?", "An indirect reference to a known person, event, text or idea", "A direct comparison using like", "An imitation of a sound", "A repeated consonant sound"),
        ("Which literary device uses a part to represent the whole or the whole to represent a part?", "Synecdoche", "Simile", "Hyperbole", "Assonance"),
        ("Which device uses a related concept or object to refer to something else?", "Metonymy", "Alliteration", "Oxymoron", "Onomatopoeia"),
        ("Identify the metonymy in 'The Crown announced a new policy.'", "The Crown represents the monarchy", "The Crown represents a physical hat only", "The Crown represents a country road", "The Crown represents a flower"),
        ("Which sentence contains an example of synecdoche?", "All hands were needed to finish the work.", "The wind was very cold.", "The stars were shining.", "She ran like the wind."),
        ("What is an oxymoron?", "A combination of contradictory terms", "A comparison using like or as", "A repeated vowel sound", "An indirect reference to history"),
        ("Which device is used in 'Bittersweet memories'?", "Oxymoron", "Alliteration", "Personification", "Euphemism"),
        ("What is a paradox?", "A seemingly contradictory statement that may reveal a truth", "A direct comparison using like", "A repeated initial consonant", "A word that imitates a sound"),
        ("Identify the paradox: 'Less is more.'", "Paradox", "Simile", "Alliteration", "Onomatopoeia"),
        ("What is a euphemism?", "A mild expression used instead of a harsh or unpleasant one", "An exaggerated statement", "A comparison between two objects", "A repeated vowel sound"),
        ("Which phrase is an example of euphemism?", "Passed away", "Died suddenly", "Shouted loudly", "Ran quickly"),
        ("What is a transferred epithet?", "An adjective transferred from the person to something associated with them", "A comparison using like or as", "A word that imitates a sound", "A statement that expresses a contradiction"),
        ("Which phrase contains a transferred epithet?", "A sleepless night", "A bright moon", "A tall building", "A beautiful flower"),
        ("What is anaphora?", "Repetition of a word or phrase at the beginning of successive clauses", "Repetition of vowel sounds at the end of words", "A comparison using like", "A statement with opposite meanings"),
        ("Which sentence demonstrates anaphora?", "We will work, we will learn, we will succeed.", "The stars danced in the sky.", "The room was as cold as ice.", "The clock went tick-tock."),
        ("What is epistrophe?", "Repetition of a word or phrase at the end of successive clauses", "Repetition of words at the beginning of clauses", "A direct comparison between objects", "An imitation of animal sounds"),
        ("What is a rhetorical device called antithesis?", "Placing contrasting ideas in a balanced structure", "Repeating the same vowel sound", "Using a mild expression for an unpleasant event", "Giving human qualities to objects"),
        ("Identify the antithesis: 'To err is human; to forgive, divine.'", "Antithesis", "Simile", "Onomatopoeia", "Personification"),
        ("What is a climax as a rhetorical device?", "Arranging ideas in increasing order of importance or intensity", "Arranging words alphabetically", "Repeating a sound at the end of words", "Using an indirect reference"),
        ("Which sentence demonstrates a rhetorical climax?", "He lost his home, his possessions and finally his hope.", "She bought apples, bananas and oranges.", "The door was painted blue.", "The bird sat on a branch."),
        ("What is bathos in literature?", "An abrupt shift from an elevated or serious style to something trivial or ridiculous", "A gradual increase in emotional intensity", "A comparison between two similar objects", "The repetition of initial sounds"),
        ("What is a malapropism?", "The humorous misuse of a word in place of a similar-sounding word", "The deliberate repetition of a phrase", "A comparison using like", "A reference to a historical event"),
        ("What is a double entendre?", "An expression with two possible meanings, often one being humorous or suggestive", "A phrase with only one literal meaning", "A repeated consonant sound", "A statement that exaggerates size"),
        ("Which device is used in 'The pen is mightier than the sword'?", "Metonymy", "Assonance", "Onomatopoeia", "Litotes"),
        ("What is a mixed metaphor?", "A combination of incompatible metaphors", "A metaphor that uses only one comparison", "A comparison using like and as", "A repeated sound in poetry"),
        ("Which statement best describes dramatic irony?", "The audience knows information that a character does not", "The narrator knows every character's thoughts", "The story has no conflict", "The characters speak in rhyme"),
        ("What is a foil character?", "A character whose qualities contrast with another character to highlight their traits", "The main character of a story", "A character who narrates every event", "A character who appears only at the ending")
    ],

    "Hard": [
        ("Which literary device involves addressing an absent person, object or abstract idea as if it were present?", "Apostrophe", "Metonymy", "Synecdoche", "Assonance"),
        ("Identify the apostrophe: 'O Death, where is thy sting?'", "Addressing Death directly", "Comparing Death to a person using like", "Repeating the initial sound", "Imitating a natural sound"),
        ("What is an extended metaphor?", "A metaphor developed over several lines or throughout a text", "A metaphor limited to one word", "A comparison using like or as", "A phrase that imitates a sound"),
        ("What is a conceit in literature?", "An elaborate and often surprising extended comparison", "A simple repeated rhyme", "A direct factual statement", "A type of punctuation"),
        ("Which literary device is used when an author deliberately leaves out conjunctions between successive clauses?", "Asyndeton", "Polysyndeton", "Anaphora", "Epistrophe"),
        ("Which sentence demonstrates asyndeton?", "I came, I saw, I conquered.", "I came and I saw and I conquered.", "I came because I wanted to win.", "I came after the competition ended."),
        ("What is polysyndeton?", "The deliberate use of many conjunctions in close succession", "The deliberate omission of conjunctions", "The repetition of vowel sounds", "The use of contradictory terms"),
        ("Which sentence demonstrates polysyndeton?", "We laughed and danced and sang and celebrated.", "We laughed, danced, sang, celebrated.", "We celebrated yesterday.", "We were happy after the event."),
        ("What is chiasmus?", "A reversal of grammatical structures in successive phrases", "A repetition of initial consonant sounds", "An indirect reference to mythology", "A comparison using like"),
        ("Which sentence demonstrates chiasmus?", "Never let a fool kiss you or a kiss fool you.", "The moon was bright.", "The river flowed quickly.", "She was as brave as a lion."),
        ("What is antimetabole?", "Repetition of words in reverse order in successive clauses", "Repetition of a phrase at the beginning of clauses", "An exaggerated statement", "A comparison between unrelated objects"),
        ("Which sentence demonstrates antimetabole?", "Ask not what your country can do for you; ask what you can do for your country.", "The wind whispered softly.", "The stars shone brightly.", "He ran as fast as a horse."),
        ("What is zeugma?", "A figure of speech in which one word governs two others in different senses", "A comparison using like or as", "A repeated vowel sound", "A phrase with contradictory terms"),
        ("Which sentence demonstrates zeugma?", "She broke his car and his heart.", "The sun was bright and warm.", "The children played in the park.", "The leaves danced in the wind."),
        ("What is syllepsis?", "A form of zeugma in which a word applies to two others in different grammatical or semantic senses", "A direct comparison using like", "A repeated consonant sound", "An indirect historical reference"),
        ("What is synesthesia in literary writing?", "Describing one sensory experience using terms associated with another sense", "Repeating a word at the end of every line", "Using two contradictory words together", "Giving an object a human name"),
        ("Which phrase demonstrates synesthesia?", "A loud colour", "A blue sky", "A cold morning", "A sweet mango"),
        ("What is hypallage?", "A figure of speech in which an adjective is grammatically transferred to a different noun from the one it logically describes", "A comparison using like", "A repeated consonant sound", "A deliberate exaggeration"),
        ("What is anadiplosis?", "Repeating the last word of one clause at the beginning of the next", "Repeating the first word of every line", "Repeating vowel sounds", "Omitting conjunctions"),
        ("Which sentence demonstrates anadiplosis?", "Fear leads to anger; anger leads to hate.", "We came, we saw, we conquered.", "The wind whispered through the trees.", "Life is a journey."),
        ("What is epanalepsis?", "Repeating the opening word or phrase at the end of the same clause or sentence", "Repeating the end of one clause at the beginning of another", "Repeating vowel sounds in nearby words", "Using many conjunctions"),
        ("Which sentence demonstrates epanalepsis?", "Nothing can be done without hope, nothing.", "Hope leads to action; action leads to change.", "The room was dark and silent.", "She ran like the wind."),
        ("What is litotes?", "A form of understatement that expresses an idea by negating its opposite", "An extreme exaggeration", "A direct comparison", "A repeated sound"),
        ("Which sentence demonstrates litotes?", "The test was not easy.", "The test was unbelievably difficult.", "The test was like a mountain.", "The test shouted at me."),
        ("What is an enthymeme?", "An argument in which one premise is implied rather than explicitly stated", "A poem with a fixed rhyme scheme", "A comparison involving two objects", "A phrase that imitates a sound"),
        ("What is a pathetic fallacy?", "Attributing human emotions or feelings to aspects of nature", "Giving an animal the ability to speak", "Using a word in two different senses", "Repeating the same phrase"),
        ("Which sentence demonstrates pathetic fallacy?", "The angry storm battered the lonely village.", "The storm brought heavy rainfall.", "The village was near a river.", "The wind measured twenty kilometres per hour."),
        ("What is the difference between metonymy and synecdoche?", "Metonymy uses a related concept, while synecdoche uses a part or whole to represent something", "Metonymy uses rhyme, while synecdoche uses rhythm", "Metonymy is exaggeration, while synecdoche is understatement", "They are both forms of onomatopoeia"),
        ("What is an allegory?", "A narrative in which characters and events represent broader ideas or principles", "A sentence that repeats initial sounds", "A direct comparison using like", "A word that imitates a sound"),
        ("What is the primary purpose of a literary motif?", "To repeatedly present an element that reinforces a theme or idea", "To replace the plot with unrelated events", "To provide the author's biography", "To eliminate symbolism from a text")
    ]
}


def validate_bank():
    for difficulty, questions in BANK.items():
        if len(questions) != 30:
            raise ValueError(
                f"{difficulty} must contain exactly 30 questions. "
                f"Found {len(questions)}."
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
    validate_bank()
    print("Question bank validation successful.")

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    try:
        cur.execute(
            "SELECT id FROM lessons WHERE title=? AND topic=?",
            ("Literary Devices and Figures of Speech", "English")
        )

        row = cur.fetchone()

        if not row:
            raise Exception(
                "Lesson 'Literary Devices and Figures of Speech' "
                "with topic 'English' was not found."
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
                    INSERT INTO quizzes (lesson_id, title, difficulty)
                    VALUES (?, ?, ?)
                    """,
                    (
                        lesson_id,
                        f"Literary Devices and Figures of Speech - {difficulty}",
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
                    f"{difficulty} already has {existing} questions."
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
                    INSERT INTO questions (
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

        print(
            "\nSUCCESS: Literary Devices and Figures of Speech "
            "has exactly 90 questions!"
        )

    except Exception as e:
        con.rollback()
        print("ERROR:", e)

    finally:
        con.close()


if __name__ == "__main__":
    main()
