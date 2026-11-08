
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent / "adaptive_learning.db"

ENGLISH_TOPICS = [
    ("Parts of Speech", "Introduction to the eight parts of speech and their functions in English sentences."),
    ("Nouns", "Learn about common, proper, collective, abstract and material nouns, including singular and plural forms."),
    ("Pronouns", "Understand personal, possessive, reflexive, demonstrative, relative and interrogative pronouns."),
    ("Verbs", "Learn action verbs, helping verbs, linking verbs, transitive verbs and intransitive verbs."),
    ("Adjectives", "Study descriptive, quantitative, demonstrative, possessive and comparative adjectives."),
    ("Adverbs", "Understand adverbs of manner, time, place, frequency and degree."),
    ("Articles", "Learn the correct use of the articles a, an and the."),
    ("Prepositions", "Understand prepositions of time, place, direction and movement."),
    ("Conjunctions", "Study coordinating, subordinating and correlative conjunctions."),
    ("Interjections", "Learn how interjections express emotions and sudden feelings."),
    ("Subject-Verb Agreement", "Understand how subjects and verbs agree in number and person."),
    ("Tenses", "Introduction to present, past and future tenses and their uses."),
    ("Present Tense", "Learn simple present, present continuous, present perfect and present perfect continuous."),
    ("Past Tense", "Study simple past, past continuous, past perfect and past perfect continuous."),
    ("Future Tense", "Understand simple future, future continuous, future perfect and future perfect continuous."),
    ("Active and Passive Voice", "Learn how to identify and transform sentences between active and passive voice."),
    ("Direct and Indirect Speech", "Understand reported speech and the changes in tense, pronouns and time expressions."),
    ("Modal Verbs", "Study modal verbs such as can, could, may, might, must, should and would."),
    ("Sentence Types", "Learn declarative, interrogative, imperative and exclamatory sentences."),
    ("Sentence Structure", "Understand simple, compound and complex sentences."),
    ("Punctuation", "Learn the correct use of full stops, commas, question marks, apostrophes and quotation marks."),
    ("Capitalization", "Understand capitalization rules for names, places, titles and beginnings of sentences."),
    ("Subject and Predicate", "Identify the subject and predicate and understand their roles in sentences."),
    ("Question Tags", "Learn how to form question tags using auxiliary verbs and pronouns."),
    ("Conditional Sentences", "Study zero, first, second and third conditional sentences."),
    ("Synonyms", "Build vocabulary by identifying words with similar meanings."),
    ("Antonyms", "Develop vocabulary by identifying words with opposite meanings."),
    ("Homophones and Homonyms", "Understand words that sound alike or have the same spelling but different meanings."),
    ("One-Word Substitutions", "Learn single words used to replace longer expressions or descriptions."),
    ("Idioms and Phrases", "Understand common English idioms and phrases and their meanings."),
    ("Proverbs", "Learn common English proverbs and the lessons or meanings they communicate."),
    ("Vocabulary Building", "Improve vocabulary through word meanings, usage and contextual understanding."),
    ("Prefixes and Suffixes", "Understand how prefixes and suffixes change the meanings and forms of words."),
    ("Reading Comprehension", "Develop the ability to understand passages, identify main ideas and interpret information."),
    ("Unseen Passages", "Practice reading unfamiliar passages and answering factual and inferential questions."),
    ("Paragraph Writing", "Learn paragraph organization, topic sentences, supporting details and conclusions."),
    ("Letter Writing", "Understand formal and informal letter formats, structure and language."),
    ("Story Writing", "Learn story structure, characters, setting, plot and conclusion."),
    ("Essay Writing", "Understand essay structure, introductions, body paragraphs and conclusions."),
    ("Literary Devices and Figures of Speech", "Study simile, metaphor, personification, alliteration, hyperbole and other literary devices.")
]

def add_english_lessons():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        inserted = 0
        skipped = 0

        for title, content in ENGLISH_TOPICS:

            cursor.execute("""
                SELECT id FROM lessons
                WHERE title = ? AND topic = 'English'
            """, (title,))

            if cursor.fetchone():
                print(f"Already exists: {title}")
                skipped += 1
                continue

            cursor.execute("""
                INSERT INTO lessons
                (title, topic, difficulty, content, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                title,
                "English",
                "MIXED",
                content,
                datetime.now().isoformat()
            ))

            inserted += 1
            print(f"Added: {title}")

        conn.commit()

        cursor.execute("""
            SELECT id, title
            FROM lessons
            WHERE topic = 'English'
            ORDER BY id
        """)

        lessons = cursor.fetchall()

        print("\n========== ENGLISH LESSON SUMMARY ==========")
        print(f"New lessons inserted: {inserted}")
        print(f"Already existing lessons skipped: {skipped}")
        print(f"Total English lessons: {len(lessons)}")

        print("\nENGLISH LESSON IDs:")
        for lesson_id, title in lessons:
            print(f"{lesson_id} - {title}")

        print("\nEnglish lesson creation completed successfully!")

    except Exception as error:
        conn.rollback()
        print("Error:", error)

    finally:
        conn.close()


if __name__ == "__main__":
    add_english_lessons()
