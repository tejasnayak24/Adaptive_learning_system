
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 181
LESSON_TITLE = "Indian Literature, Languages, Newspapers and Famous Publications"
TOPIC = "General Knowledge"

# Each question: (question, correct answer, wrong option 1, wrong option 2, wrong option 3)

BANK = {
    "Easy": [
        ("Who wrote the national anthem of India, Jana Gana Mana?", "Rabindranath Tagore", "Bankim Chandra Chatterjee", "Sarojini Naidu", "Subramania Bharati"),
        ("Who wrote the famous book Gitanjali?", "Rabindranath Tagore", "Munshi Premchand", "R. K. Narayan", "Mulk Raj Anand"),
        ("Who wrote the novel Godaan?", "Munshi Premchand", "Rabindranath Tagore", "Bankim Chandra Chatterjee", "Khushwant Singh"),
        ("Which language is primarily associated with the ancient text Tirukkural?", "Tamil", "Sanskrit", "Hindi", "Bengali"),
        ("Who wrote the Ramcharitmanas?", "Tulsidas", "Valmiki", "Kalidasa", "Kabir"),
        ("Who wrote the play Abhijnanasakuntalam?", "Kalidasa", "Bhavabhuti", "Bhasa", "Banabhatta"),
        ("Which Indian poet wrote the poem Vande Mataram?", "Bankim Chandra Chatterjee", "Rabindranath Tagore", "Sarojini Naidu", "Subramania Bharati"),
        ("Who wrote the novel Malgudi Days?", "R. K. Narayan", "Raja Rao", "Mulk Raj Anand", "Ruskin Bond"),
        ("Which script is used to write standard Hindi?", "Devanagari", "Gurmukhi", "Persian", "Tamil"),
        ("How many languages are listed in the Eighth Schedule of the Indian Constitution?", "22", "18", "20", "24"),
        ("Which language is the primary language of the classical text Mahabharata?", "Sanskrit", "Tamil", "Pali", "Prakrit"),
        ("Who wrote the book The Discovery of India?", "Jawaharlal Nehru", "Mahatma Gandhi", "B. R. Ambedkar", "Sardar Patel"),
        ("Who wrote the autobiography My Experiments with Truth?", "Mahatma Gandhi", "Jawaharlal Nehru", "Subhas Chandra Bose", "Rabindranath Tagore"),
        ("Which newspaper was founded by Bal Gangadhar Tilak?", "Kesari", "The Hindu", "Amrita Bazar Patrika", "The Tribune"),
        ("Who founded the newspaper Sambad Kaumudi?", "Raja Ram Mohan Roy", "Ishwar Chandra Vidyasagar", "Dadabhai Naoroji", "Gopal Krishna Gokhale"),
        ("Which language is associated with the literary work Kamba Ramayanam?", "Tamil", "Kannada", "Telugu", "Malayalam"),
        ("Who wrote the poem The Golden Threshold?", "Sarojini Naidu", "Toru Dutt", "Kamala Das", "Amrita Pritam"),
        ("Which Indian writer created the fictional town of Malgudi?", "R. K. Narayan", "Ruskin Bond", "Khushwant Singh", "Vikram Seth"),
        ("Who wrote the Sanskrit poem Meghaduta?", "Kalidasa", "Tulsidas", "Banabhatta", "Bharavi"),
        ("Which language is primarily spoken in Karnataka?", "Kannada", "Telugu", "Tamil", "Malayalam"),
        ("Which newspaper is commonly associated with Mahatma Gandhi's journalism?", "Young India", "Kesari", "The Statesman", "The Tribune"),
        ("Who wrote the book Wings of Fire?", "A. P. J. Abdul Kalam", "Vikram Sarabhai", "Homi Bhabha", "C. V. Raman"),
        ("Which language is primarily associated with the poet Subramania Bharati?", "Tamil", "Bengali", "Marathi", "Gujarati"),
        ("Who wrote the novel Anandamath?", "Bankim Chandra Chatterjee", "Munshi Premchand", "R. K. Narayan", "Mulk Raj Anand"),
        ("Which language is primarily associated with the ancient Buddhist texts known as the Pali Canon?", "Pali", "Persian", "Arabic", "English"),
        ("Who wrote the book India Wins Freedom?", "Maulana Abul Kalam Azad", "Jawaharlal Nehru", "B. R. Ambedkar", "Rajendra Prasad"),
        ("Which newspaper was founded in Bombay in 1822 by Fardunjee Marzban?", "Bombay Samachar", "The Hindu", "Kesari", "The Pioneer"),
        ("Who wrote the Kannada literary work Sri Ramayana Darshanam?", "Kuvempu", "D. R. Bendre", "S. L. Bhyrappa", "Pampa"),
        ("Which language is primarily associated with the poet Kabir's devotional compositions?", "Hindi and related North Indian vernacular traditions", "Classical Greek", "Latin", "Japanese"),
        ("Who wrote the book The Guide?", "R. K. Narayan", "Mulk Raj Anand", "Raja Rao", "Ruskin Bond"),
    ],

    "Medium": [
        ("Who composed the Tamil classic Silappatikaram?", "Ilango Adigal", "Sekkizhar", "Kamban", "Tiruvalluvar"),
        ("Who is traditionally credited with composing the Sanskrit epic Ramayana?", "Valmiki", "Ved Vyasa", "Kalidasa", "Banabhatta"),
        ("Which work is traditionally attributed to Ved Vyasa?", "Mahabharata", "Meghaduta", "Tirukkural", "Abhijnanasakuntalam"),
        ("Who wrote the Bengali novel Anandamath?", "Bankim Chandra Chatterjee", "Sarat Chandra Chattopadhyay", "Rabindranath Tagore", "Michael Madhusudan Dutt"),
        ("Who founded the newspaper Amrita Bazar Patrika along with his brother Motilal Ghosh?", "Sisir Kumar Ghosh", "G. Subramania Iyer", "Fardunjee Marzban", "Bal Gangadhar Tilak"),
        ("Who was a prominent editor and founder associated with The Hindu newspaper?", "G. Subramania Iyer", "Raja Ram Mohan Roy", "Sisir Kumar Ghosh", "Fardunjee Marzban"),
        ("Which Indian literary work was written by Thiruvalluvar?", "Tirukkural", "Silappatikaram", "Manimekalai", "Periyapuranam"),
        ("Who wrote the novel Train to Pakistan?", "Khushwant Singh", "R. K. Narayan", "Mulk Raj Anand", "Raja Rao"),
        ("Which writer authored Untouchable?", "Mulk Raj Anand", "R. K. Narayan", "Vikram Seth", "Salman Rushdie"),
        ("Who wrote the novel Kanthapura?", "Raja Rao", "Mulk Raj Anand", "Khushwant Singh", "Ruskin Bond"),
        ("Which Indian poet wrote the collection A River?", "A. K. Ramanujan", "Nissim Ezekiel", "Jayanta Mahapatra", "Keki N. Daruwalla"),
        ("Who wrote the English novel A Suitable Boy?", "Vikram Seth", "Amitav Ghosh", "Arundhati Roy", "Salman Rushdie"),
        ("Which language was the original language of the literary work Gora by Rabindranath Tagore?", "Bengali", "Hindi", "English", "Urdu"),
        ("Who wrote the novel Chokher Bali?", "Rabindranath Tagore", "Bankim Chandra Chatterjee", "Sarat Chandra Chattopadhyay", "Bibhutibhushan Bandyopadhyay"),
        ("Which Indian writer authored The God of Small Things?", "Arundhati Roy", "Kiran Desai", "Anita Desai", "Jhumpa Lahiri"),
        ("Who wrote the novel The White Tiger?", "Aravind Adiga", "Amitav Ghosh", "Vikram Chandra", "Rohinton Mistry"),
        ("Which newspaper was started by Raja Ram Mohan Roy in Persian?", "Mirat-ul-Akhbar", "Kesari", "Young India", "The Hindu"),
        ("Which newspaper was founded by Fardunjee Marzban?", "Bombay Samachar", "Amrita Bazar Patrika", "The Tribune", "The Hindu"),
        ("Who edited the newspaper Harijan?", "Mahatma Gandhi", "Bal Gangadhar Tilak", "Gopal Krishna Gokhale", "Dadabhai Naoroji"),
        ("Which language is the original language of the literary work Ponniyin Selvan?", "Tamil", "Telugu", "Kannada", "Malayalam"),
        ("Who wrote the Telugu literary work Amuktamalyada?", "Krishnadevaraya", "Nannaya", "Tikkana", "Pothana"),
        ("Who is known as the Adikavi of Kannada literature?", "Pampa", "Kuvempu", "D. R. Bendre", "Ranna"),
        ("Which language is associated with the poet Lal Ded?", "Kashmiri", "Punjabi", "Assamese", "Odia"),
        ("Who wrote the Malayalam novel Chemmeen?", "Thakazhi Sivasankara Pillai", "Vaikom Muhammad Basheer", "M. T. Vasudevan Nair", "O. V. Vijayan"),
        ("Who wrote the Assamese literary work Kirtan Ghoxa?", "Srimanta Sankardev", "Lakshminath Bezbaroa", "Homen Borgohain", "Jyoti Prasad Agarwala"),
        ("Which writer authored the novel Pinjar?", "Amrita Pritam", "Ismat Chughtai", "Qurratulain Hyder", "Krishna Sobti"),
        ("Who wrote the Urdu novel Umrao Jaan Ada?", "Mirza Hadi Ruswa", "Saadat Hasan Manto", "Premchand", "Mir Taqi Mir"),
        ("Which language was used by Amir Khusrau in many of his Hindavi compositions?", "Hindavi", "Latin", "Greek", "French"),
        ("Who wrote the novel The Shadow Lines?", "Amitav Ghosh", "Vikram Seth", "R. K. Narayan", "Salman Rushdie"),
        ("Which Indian author wrote the novel Midnight's Children?", "Salman Rushdie", "Amitav Ghosh", "Aravind Adiga", "Rohinton Mistry"),
    ],

    "Hard": [
        ("Who authored the Sanskrit literary work Kadambari?", "Banabhatta", "Kalidasa", "Bharavi", "Magha"),
        ("Which ancient Sanskrit grammarian composed the Ashtadhyayi?", "Panini", "Patanjali", "Bharata Muni", "Katyayana"),
        ("Who wrote the Sanskrit treatise Natyashastra?", "Bharata Muni", "Panini", "Kalidasa", "Varahamihira"),
        ("Which poet composed the Sanskrit epic Kiratarjuniya?", "Bharavi", "Magha", "Kalidasa", "Bhavabhuti"),
        ("Who authored the Sanskrit poem Shishupalavadha?", "Magha", "Bharavi", "Banabhatta", "Bhasa"),
        ("Which scholar wrote the Sanskrit literary work Rajatarangini?", "Kalhana", "Bilhana", "Banabhatta", "Dandin"),
        ("Who wrote the Sanskrit prose work Dashakumaracharita?", "Dandin", "Kalidasa", "Bharavi", "Magha"),
        ("Which ancient Tamil grammatical text is traditionally attributed to Tolkappiyar?", "Tolkappiyam", "Tirukkural", "Silappatikaram", "Manimekalai"),
        ("Who authored the Tamil epic Manimekalai?", "Sattanar", "Ilango Adigal", "Kamban", "Tiruvalluvar"),
        ("Which Kannada poet authored the Vikramarjuna Vijaya, also known as Pampa Bharata?", "Pampa", "Ranna", "Janna", "Kuvempu"),
        ("Who wrote the Kannada epic Gadayuddha?", "Ranna", "Pampa", "Janna", "Harihara"),
        ("Which Telugu poet is traditionally known as Adikavi for beginning the Telugu Mahabharata translation?", "Nannaya", "Tikkana", "Errana", "Pothana"),
        ("Who completed the Telugu translation of the Mahabharata after Nannaya and Tikkana?", "Errana", "Pothana", "Srinatha", "Krishnadevaraya"),
        ("Who authored the Telugu devotional work Andhra Mahabhagavatamu?", "Pothana", "Nannaya", "Tikkana", "Gurajada Apparao"),
        ("Which Malayalam writer authored the novel Indulekha?", "O. Chandu Menon", "Thakazhi Sivasankara Pillai", "Vaikom Muhammad Basheer", "M. T. Vasudevan Nair"),
        ("Who wrote the Malayalam novel Randamoozham?", "M. T. Vasudevan Nair", "O. V. Vijayan", "Thakazhi Sivasankara Pillai", "Kumaran Asan"),
        ("Which Bengali writer authored the novel Pather Panchali?", "Bibhutibhushan Bandyopadhyay", "Sarat Chandra Chattopadhyay", "Bankim Chandra Chatterjee", "Tarashankar Bandyopadhyay"),
        ("Who wrote the Bengali novel Srikanta?", "Sarat Chandra Chattopadhyay", "Rabindranath Tagore", "Bankim Chandra Chatterjee", "Bibhutibhushan Bandyopadhyay"),
        ("Which Indian writer authored the novel Aag Ka Darya?", "Qurratulain Hyder", "Ismat Chughtai", "Amrita Pritam", "Krishna Sobti"),
        ("Who wrote the Urdu short story Toba Tek Singh?", "Saadat Hasan Manto", "Mirza Hadi Ruswa", "Ismat Chughtai", "Rajinder Singh Bedi"),
        ("Which Indian writer wrote the short story Lihaaf?", "Ismat Chughtai", "Amrita Pritam", "Qurratulain Hyder", "Krishna Sobti"),
        ("Who founded the journal and newspaper Kesari along with the English publication The Mahratta?", "Bal Gangadhar Tilak", "Gopal Krishna Gokhale", "Dadabhai Naoroji", "Lala Lajpat Rai"),
        ("Who founded the newspaper The Bengalee?", "Surendranath Banerjee", "Raja Ram Mohan Roy", "G. Subramania Iyer", "Sisir Kumar Ghosh"),
        ("Which publication was associated with the reformist work of Ishwar Chandra Vidyasagar?", "Som Prakash", "Young India", "Kesari", "Mirat-ul-Akhbar"),
        ("Who founded the newspaper The Tribune in Lahore in 1881?", "Sardar Dyal Singh Majithia", "Bal Gangadhar Tilak", "G. Subramania Iyer", "Sisir Kumar Ghosh"),
        ("Which publication was started by Mahatma Gandhi in South Africa in 1903?", "Indian Opinion", "Young India", "Harijan", "Navajivan"),
        ("Which publication did Gandhi use to communicate his ideas after returning to India, publishing in Gujarati and English?", "Navajivan", "Kesari", "The Bengalee", "Amrita Bazar Patrika"),
        ("Who wrote the literary criticism work The Indian Renaissance?", "K. R. Srinivasa Iyengar", "A. K. Ramanujan", "Nissim Ezekiel", "Mulk Raj Anand"),
        ("Which Indian English poet wrote the collection The Exact Name?", "Nissim Ezekiel", "A. K. Ramanujan", "Jayanta Mahapatra", "Dom Moraes"),
        ("Who authored the novel The Serpent and the Rope?", "Raja Rao", "R. K. Narayan", "Mulk Raj Anand", "Khushwant Singh"),
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
                    f"{difficulty} question {index} must have 5 values"
                )

            question, correct, *wrong = item

            if not all(isinstance(value, str) and value.strip() for value in item):
                raise ValueError(
                    f"Empty or invalid value in {difficulty} question {index}"
                )

            options = [correct] + wrong

            if len(set(options)) != 4:
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
                    "MCQ lesson covering Indian literature, languages, "
                    "newspapers and famous publications."
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
                    f"{difficulty} quiz already has "
                    f"{existing_count} questions. Expected maximum: 30."
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
