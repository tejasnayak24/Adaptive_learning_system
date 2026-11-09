
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 188
LESSON_TITLE = "Indian Languages, Literature, Classical Texts and Epics"
TOPIC = "General Knowledge"

BANK = {
    "Easy": [
        ("Which is the national language of India?", "India has no nationally designated language", "Hindi", "English", "Sanskrit"),
        ("Which language is primarily spoken in Tamil Nadu?", "Tamil", "Telugu", "Kannada", "Malayalam"),
        ("Which language is primarily spoken in Karnataka?", "Kannada", "Tamil", "Marathi", "Odia"),
        ("Which language is primarily spoken in Kerala?", "Malayalam", "Kannada", "Telugu", "Konkani"),
        ("Which language is primarily spoken in Andhra Pradesh?", "Telugu", "Tamil", "Gujarati", "Punjabi"),
        ("Which language is primarily spoken in Maharashtra?", "Marathi", "Bengali", "Assamese", "Kashmiri"),
        ("Which language is primarily spoken in West Bengal?", "Bengali", "Odia", "Marathi", "Dogri"),
        ("Which language is primarily spoken in Gujarat?", "Gujarati", "Punjabi", "Konkani", "Manipuri"),
        ("Which language is primarily spoken in Punjab?", "Punjabi", "Sindhi", "Bodo", "Nepali"),
        ("Which language is widely spoken in Assam?", "Assamese", "Kashmiri", "Malayalam", "Maithili"),
        ("Who wrote the Indian national anthem Jana Gana Mana?", "Rabindranath Tagore", "Bankim Chandra Chatterjee", "Sarojini Naidu", "Subramania Bharati"),
        ("Who wrote Vande Mataram?", "Bankim Chandra Chatterjee", "Rabindranath Tagore", "Munshi Premchand", "Kalidasa"),
        ("Which epic is traditionally attributed to Valmiki?", "Ramayana", "Mahabharata", "Silappatikaram", "Arthashastra"),
        ("Which epic is traditionally attributed to Ved Vyasa?", "Mahabharata", "Ramayana", "Meghaduta", "Abhijnanashakuntalam"),
        ("Who wrote the Bhagavad Gita as part of the Mahabharata?", "It is a dialogue within the Mahabharata, traditionally attributed to Vyasa", "Kalidasa", "Tulsidas", "Banabhatta"),
        ("Who wrote the Ramcharitmanas?", "Tulsidas", "Surdas", "Kabir", "Mirabai"),
        ("Who wrote the famous Sanskrit play Abhijnanashakuntalam?", "Kalidasa", "Bhasa", "Bhavabhuti", "Banabhatta"),
        ("Who wrote the book The Discovery of India?", "Jawaharlal Nehru", "Mahatma Gandhi", "B. R. Ambedkar", "Rabindranath Tagore"),
        ("Who wrote the autobiography My Experiments with Truth?", "Mahatma Gandhi", "Jawaharlal Nehru", "Sardar Patel", "Subhas Chandra Bose"),
        ("Which language is the classical language of ancient Indian texts such as the Vedas?", "Sanskrit", "French", "Portuguese", "Persian"),
        ("Which of these is one of the 22 languages listed in the Eighth Schedule of the Indian Constitution?", "Konkani", "Tulu", "Bhojpuri", "Rajasthani"),
        ("Which language is associated with the ancient Sangam literature of South India?", "Tamil", "Punjabi", "Bengali", "Gujarati"),
        ("Who wrote the poem collection Gitanjali?", "Rabindranath Tagore", "Sarojini Naidu", "Kuvempu", "Kusumagraj"),
        ("Which Indian writer is popularly known as Munshi Premchand?", "Dhanpat Rai Srivastava", "R. K. Narayan", "Mulk Raj Anand", "Harivansh Rai Bachchan"),
        ("Who wrote the novel Malgudi Days?", "R. K. Narayan", "Ruskin Bond", "Khushwant Singh", "Vikram Seth"),
        ("Who wrote the famous novel Godan?", "Munshi Premchand", "Bankim Chandra Chatterjee", "Rabindranath Tagore", "Mulk Raj Anand"),
        ("Which language is the original language of the Vedas?", "Sanskrit", "Tamil", "Pali", "Prakrit"),
        ("Which ancient Indian text is associated with the teachings of Buddha?", "Tripitaka", "Arthashastra", "Natyashastra", "Manusmriti"),
        ("Which language was widely used in many early Buddhist scriptures?", "Pali", "Persian", "Arabic", "French"),
        ("Which Indian poet wrote the national song Vande Mataram?", "Bankim Chandra Chatterjee", "Rabindranath Tagore", "Kuvempu", "Bharathidasan"),
    ],

    "Medium": [
        ("Which of the following is a Dravidian language?", "Kannada", "Hindi", "Bengali", "Punjabi"),
        ("Which of the following is an Indo-Aryan language?", "Marathi", "Tamil", "Telugu", "Malayalam"),
        ("Which language is traditionally associated with the state of Odisha?", "Odia", "Assamese", "Konkani", "Kashmiri"),
        ("Which language is associated with the state of Goa and is included in the Eighth Schedule?", "Konkani", "Tulu", "Kodava", "Bhojpuri"),
        ("Which language is primarily spoken in Jammu and Kashmir and is included in the Eighth Schedule?", "Kashmiri", "Tulu", "Bhojpuri", "Garhwali"),
        ("Which language is spoken in parts of Sikkim and is included in the Eighth Schedule?", "Nepali", "Tulu", "Kokborok", "Lepcha"),
        ("Which language is associated with the state of Manipur and is included in the Eighth Schedule?", "Manipuri (Meitei)", "Bodo", "Dogri", "Sindhi"),
        ("Which language is included in the Eighth Schedule and is widely associated with the Bodoland region?", "Bodo", "Tulu", "Kumaoni", "Kokborok"),
        ("Which classical language is associated with the ancient Tamil Sangam works?", "Tamil", "Persian", "Arabic", "Urdu"),
        ("Which of the following is a major work of ancient Tamil literature?", "Silappatikaram", "Arthashastra", "Rajatarangini", "Mudrarakshasa"),
        ("Who is traditionally credited with writing Silappatikaram?", "Ilango Adigal", "Tiruvalluvar", "Kamban", "Sekkizhar"),
        ("Who composed the Tamil ethical text Tirukkural?", "Tiruvalluvar", "Ilango Adigal", "Kamban", "Avvaiyar"),
        ("How many couplets are there in the Tirukkural?", "1,330", "1,000", "1,500", "2,000"),
        ("Who wrote the Tamil epic Manimekalai?", "Sattanar", "Ilango Adigal", "Tiruvalluvar", "Kamban"),
        ("Who translated the Ramayana into the Awadhi literary tradition as Ramcharitmanas?", "Tulsidas", "Surdas", "Kabir", "Rahim"),
        ("Who is traditionally associated with the composition of the Hindi devotional poetry Sur Sagar?", "Surdas", "Tulsidas", "Kabir", "Bihari"),
        ("Which poet is associated with the devotional songs known as Abhangs in Marathi?", "Sant Tukaram", "Mirabai", "Surdas", "Tulsidas"),
        ("Which saint-poet is associated with the Kannada Vachana movement?", "Basavanna", "Tulsidas", "Kabir", "Surdas"),
        ("Who wrote the Kannada epic Sri Ramayana Darshanam?", "Kuvempu", "D. R. Bendre", "Pampa", "Ranna"),
        ("Which Kannada poet is popularly known as Adikavi?", "Pampa", "Kuvempu", "D. R. Bendre", "K. S. Narasimhaswamy"),
        ("Who wrote the Malayalam novel Indulekha?", "O. Chandu Menon", "Vaikom Muhammad Basheer", "Thakazhi Sivasankara Pillai", "Kumaran Asan"),
        ("Who wrote the Bengali novel Anandamath?", "Bankim Chandra Chatterjee", "Rabindranath Tagore", "Sarat Chandra Chattopadhyay", "Michael Madhusudan Dutt"),
        ("Who wrote the Bengali novel Gora?", "Rabindranath Tagore", "Bankim Chandra Chatterjee", "Bibhutibhushan Bandyopadhyay", "Sarat Chandra Chattopadhyay"),
        ("Who wrote the novel Pather Panchali?", "Bibhutibhushan Bandyopadhyay", "Rabindranath Tagore", "Bankim Chandra Chatterjee", "Manik Bandopadhyay"),
        ("Who wrote the English novel Train to Pakistan?", "Khushwant Singh", "R. K. Narayan", "Mulk Raj Anand", "Ruskin Bond"),
        ("Who wrote the novel Untouchable?", "Mulk Raj Anand", "R. K. Narayan", "Vikram Seth", "Salman Rushdie"),
        ("Who wrote the novel A Suitable Boy?", "Vikram Seth", "Amitav Ghosh", "Arundhati Roy", "R. K. Narayan"),
        ("Which Indian writer won the Nobel Prize in Literature in 1913?", "Rabindranath Tagore", "Mulk Raj Anand", "R. K. Narayan", "Sarojini Naidu"),
        ("Which ancient Indian text is attributed to Kautilya and deals with statecraft and administration?", "Arthashastra", "Natya Shastra", "Rigveda", "Charaka Samhita"),
        ("Which ancient text is associated with grammar and is attributed to Panini?", "Ashtadhyayi", "Arthashastra", "Rajatarangini", "Panchatantra"),
    ],

    "Hard": [
        ("Which Veda is primarily associated with hymns and praises addressed to various deities?", "Rigveda", "Samaveda", "Yajurveda", "Atharvaveda"),
        ("Which Veda is especially associated with melodies and chants?", "Samaveda", "Rigveda", "Atharvaveda", "Yajurveda"),
        ("Which Veda contains many formulas and instructions used in sacrificial rituals?", "Yajurveda", "Rigveda", "Samaveda", "Atharvaveda"),
        ("Which Veda includes material associated with healing, charms and everyday concerns?", "Atharvaveda", "Samaveda", "Rigveda", "Yajurveda"),
        ("Which are the philosophical portions of the Vedic literature?", "Upanishads", "Puranas", "Jatakas", "Agamas"),
        ("Which Sanskrit grammatical work was composed by Panini?", "Ashtadhyayi", "Mahabhashya", "Arthashastra", "Natyashastra"),
        ("Who wrote the Mahabhashya, an important commentary on Sanskrit grammar?", "Patanjali", "Panini", "Katyayana", "Bharata Muni"),
        ("Which ancient Indian scholar is traditionally associated with the Arthashastra?", "Kautilya", "Kalidasa", "Banabhatta", "Bharavi"),
        ("Which work by Kalidasa narrates the story of King Dushyanta and Shakuntala?", "Abhijnanashakuntalam", "Meghaduta", "Raghuvamsha", "Kumarasambhava"),
        ("Which poem by Kalidasa describes a cloud carrying a message to the poet's beloved?", "Meghaduta", "Raghuvamsha", "Malavikagnimitram", "Kumarasambhava"),
        ("Which Sanskrit poet composed the epic Kiratarjuniya?", "Bharavi", "Kalidasa", "Magha", "Bhavabhuti"),
        ("Who composed the Sanskrit epic Shishupalavadha?", "Magha", "Bharavi", "Kalidasa", "Banabhatta"),
        ("Which Sanskrit dramatist wrote the play Mudrarakshasa?", "Vishakhadatta", "Bhasa", "Bhavabhuti", "Kalidasa"),
        ("Who wrote the Sanskrit prose romance Kadambari?", "Banabhatta", "Kalidasa", "Bharavi", "Dandin"),
        ("Which historical chronicle of Kashmir was written by Kalhana?", "Rajatarangini", "Harshacharita", "Kadambari", "Malavikagnimitram"),
        ("Who wrote the Sanskrit biography Harshacharita?", "Banabhatta", "Kalhana", "Dandin", "Bhasa"),
        ("Which Buddhist literary collection contains stories about the previous births of the Buddha?", "Jataka tales", "Panchatantra", "Hitopadesha", "Kathasaritsagara"),
        ("Which ancient Indian collection of animal fables is traditionally attributed to Vishnu Sharma?", "Panchatantra", "Jataka tales", "Rajatarangini", "Arthashastra"),
        ("Who wrote the Sanskrit text Hitopadesha?", "Narayana Pandit", "Vishnu Sharma", "Kalidasa", "Banabhatta"),
        ("Which ancient Tamil grammatical work is traditionally attributed to Tolkappiyar?", "Tolkappiyam", "Tirukkural", "Silappatikaram", "Manimekalai"),
        ("Which three major sections form the structure of the Tirukkural?", "Virtue, Wealth and Love", "War, Trade and Politics", "Poetry, Drama and Music", "Religion, Science and Medicine"),
        ("Which Kannada poet is one of the three famous poets known as the Ratnatraya of early Kannada literature?", "Pampa", "Kuvempu", "D. R. Bendre", "Gopalakrishna Adiga"),
        ("Which two poets are commonly grouped with Pampa as the Ratnatraya of early Kannada literature?", "Ponna and Ranna", "Kuvempu and Bendre", "Basavanna and Allama Prabhu", "Harihara and Raghavanka"),
        ("Which Kannada literary movement is especially associated with the Vachana compositions of Basavanna and other Sharanas?", "Vachana movement", "Navodaya movement", "Pragatisheela movement", "Navyottara movement"),
        ("Which Malayalam poet is known for the work Chandalabhikshuki and was a major figure in modern Malayalam poetry?", "Kumaran Asan", "O. Chandu Menon", "Thakazhi Sivasankara Pillai", "Vaikom Muhammad Basheer"),
        ("Which Assamese literary figure wrote the Kirtan Ghoxa?", "Srimanta Sankardev", "Lakshminath Bezbarua", "Hemchandra Barua", "Madhavdev"),
        ("Which literary figure is associated with the Assamese work Naam Ghoxa?", "Madhavdev", "Srimanta Sankardev", "Lakshminath Bezbarua", "Jyoti Prasad Agarwala"),
        ("Which Punjabi Sufi poet is associated with the famous poem Heer?", "Waris Shah", "Bulleh Shah", "Shah Hussain", "Bhai Vir Singh"),
        ("Which Persian-language work by Amir Khusrau is associated with the cultural history of the Delhi Sultanate?", "Khazain-ul-Futuh", "Akbarnama", "Baburnama", "Tuzuk-i-Jahangiri"),
        ("Which Mughal emperor's autobiography was originally written in Chagatai Turkish?", "Babur", "Akbar", "Jahangir", "Shah Jahan"),
    ]
}


def validate_bank():
    for difficulty, questions in BANK.items():
        if len(questions) != 30:
            raise ValueError(
                f"{difficulty} must contain exactly 30 questions; "
                f"found {len(questions)}"
            )

        for index, item in enumerate(questions, start=1):
            if len(item) != 5:
                raise ValueError(
                    f"{difficulty} question {index} must contain 5 values"
                )

            if not all(isinstance(value, str) and value.strip() for value in item):
                raise ValueError(
                    f"Empty or invalid value in {difficulty} question {index}"
                )

            if len(set(item[1:])) != 4:
                raise ValueError(
                    f"Duplicate options in {difficulty} question {index}"
                )


def main():
    validate_bank()

    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT title, topic FROM lessons WHERE id = ?",
            (LESSON_ID,)
        )
        lesson = cursor.fetchone()

        if lesson is None:
            cursor.execute(
                """
                INSERT INTO lessons
                (id, title, topic, difficulty, content, created_at)
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """,
                (
                    LESSON_ID,
                    LESSON_TITLE,
                    TOPIC,
                    "Mixed",
                    "MCQ lesson covering Indian languages, literature, "
                    "classical texts and epics."
                )
            )
            print(f"Created lesson {LESSON_ID}: {LESSON_TITLE}")

        elif lesson != (LESSON_TITLE, TOPIC):
            raise ValueError(
                f"Lesson ID {LESSON_ID} already belongs to "
                f"{lesson[0]!r} under topic {lesson[1]!r}. "
                "No data was changed."
            )

        for difficulty, questions in BANK.items():
            cursor.execute(
                """
                SELECT id FROM quizzes
                WHERE lesson_id = ? AND difficulty = ?
                ORDER BY id
                LIMIT 1
                """,
                (LESSON_ID, difficulty)
            )

            quiz = cursor.fetchone()

            if quiz is None:
                cursor.execute(
                    """
                    INSERT INTO quizzes (lesson_id, title, difficulty)
                    VALUES (?, ?, ?)
                    """,
                    (
                        LESSON_ID,
                        f"{LESSON_TITLE} - {difficulty}",
                        difficulty
                    )
                )
                quiz_id = cursor.lastrowid
                print(f"Created {difficulty} quiz: {quiz_id}")
            else:
                quiz_id = quiz[0]

            cursor.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                (quiz_id,)
            )
            existing_count = cursor.fetchone()[0]

            if existing_count > 30:
                raise ValueError(
                    f"{difficulty} quiz already has {existing_count} questions. "
                    "Expected maximum: 30."
                )

            for question, correct, wrong1, wrong2, wrong3 in questions[existing_count:]:
                options = [correct, wrong1, wrong2, wrong3]
                random.shuffle(options)

                correct_answer = "ABCD"[options.index(correct)]

                cursor.execute(
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
                        question,
                        options[0],
                        options[1],
                        options[2],
                        options[3],
                        correct_answer
                    )
                )

            cursor.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                (quiz_id,)
            )
            final_count = cursor.fetchone()[0]

            if final_count != 30:
                raise ValueError(
                    f"{difficulty} quiz has {final_count} questions, not 30"
                )

            print(f"{difficulty}: {final_count}/30 questions")

        connection.commit()

        print("\nSUCCESS!")
        print(f"Lesson ID: {LESSON_ID}")
        print(f"Lesson: {LESSON_TITLE}")
        print("Easy: 30 questions")
        print("Medium: 30 questions")
        print("Hard: 30 questions")
        print("Total: 90 questions")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
