
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 187
LESSON_TITLE = "Indian Art, Music, Dance and Classical Performing Arts"
TOPIC = "General Knowledge"

BANK = {
    "Easy": [
        ("How many classical dance forms are recognised by the Sangeet Natak Akademi?", "Eight", "Six", "Ten", "Twelve"),
        ("Bharatanatyam originated in which Indian state?", "Tamil Nadu", "Kerala", "Odisha", "Assam"),
        ("Kathak is traditionally associated with which part of India?", "North India", "South India", "Northeast India", "Western India"),
        ("Kathakali is a classical dance-drama form of which state?", "Kerala", "Punjab", "Gujarat", "Bihar"),
        ("Kuchipudi originated in which Indian state?", "Andhra Pradesh", "Rajasthan", "Assam", "Haryana"),
        ("Odissi is the classical dance form of which state?", "Odisha", "Karnataka", "Maharashtra", "Manipur"),
        ("Manipuri dance originated in which state?", "Manipur", "Tripura", "Nagaland", "Mizoram"),
        ("Mohiniyattam is a classical dance form of which state?", "Kerala", "Tamil Nadu", "Gujarat", "Punjab"),
        ("Sattriya dance originated in which state?", "Assam", "Bihar", "Rajasthan", "Goa"),
        ("Which classical dance form is known for elaborate facial expressions and colourful costumes?", "Kathakali", "Bhangra", "Garba", "Ghoomar"),
        ("Which instrument is commonly associated with Hindustani classical music?", "Sitar", "Veena", "Nadaswaram", "Ghatam"),
        ("Which instrument is strongly associated with the shehnai maestro Ustad Bismillah Khan?", "Shehnai", "Tabla", "Sitar", "Sarod"),
        ("Which percussion instrument is widely used in Indian classical music?", "Tabla", "Flute", "Sitar", "Santoor"),
        ("Who is popularly known as the Nightingale of India and was a famous singer?", "M. S. Subbulakshmi", "Sarojini Naidu", "Lata Mangeshkar", "Amrita Sher-Gil"),
        ("Which famous Indian musician was known for playing the sitar?", "Ravi Shankar", "Bismillah Khan", "Zakir Hussain", "Hariprasad Chaurasia"),
        ("Which instrument is associated with Ustad Zakir Hussain?", "Tabla", "Sitar", "Sarangi", "Flute"),
        ("Which musical tradition is mainly associated with South India?", "Carnatic music", "Hindustani music", "Qawwali", "Bhangra"),
        ("Which musical tradition is mainly associated with North India?", "Hindustani music", "Carnatic music", "Lavani", "Bihu"),
        ("Bhangra is a folk dance associated with which state?", "Punjab", "Kerala", "Odisha", "Manipur"),
        ("Garba is a traditional folk dance of which state?", "Gujarat", "Assam", "Bihar", "Karnataka"),
        ("Ghoomar is a traditional folk dance of which state?", "Rajasthan", "Tamil Nadu", "Mizoram", "Kerala"),
        ("Bihu dance is associated with which state?", "Assam", "Punjab", "Goa", "Haryana"),
        ("Lavani is a traditional folk performance associated with which state?", "Maharashtra", "Kerala", "Nagaland", "Sikkim"),
        ("Which Indian state is famous for the folk dance form Yakshagana?", "Karnataka", "Punjab", "Bihar", "Tripura"),
        ("Which Indian art form combines dance, music, dialogue and elaborate costumes?", "Yakshagana", "Warli painting", "Madhubani painting", "Blue pottery"),
        ("Which traditional Indian painting style is associated with Bihar?", "Madhubani", "Warli", "Pattachitra", "Kalamkari"),
        ("Warli painting is traditionally associated with which state?", "Maharashtra", "Assam", "Punjab", "Kerala"),
        ("Which traditional painting style is associated with Odisha?", "Pattachitra", "Madhubani", "Phad", "Warli"),
        ("Which Indian art form uses coloured powders to create decorative floor designs?", "Rangoli", "Kathakali", "Yakshagana", "Qawwali"),
        ("Which festival is especially associated with traditional Garba performances?", "Navratri", "Onam", "Baisakhi", "Pongal"),
    ],

    "Medium": [
        ("Which classical dance form is traditionally associated with the Vaishnavite monasteries known as Satras?", "Sattriya", "Kathak", "Odissi", "Bharatanatyam"),
        ("Who is widely credited with reviving and popularising Bharatanatyam in the twentieth century?", "Rukmini Devi Arundale", "Birju Maharaj", "Kelucharan Mohapatra", "Guru Bipin Singh"),
        ("Which dancer is particularly associated with the revival and development of Odissi?", "Kelucharan Mohapatra", "Birju Maharaj", "Uday Shankar", "Vempati Chinna Satyam"),
        ("Which famous Kathak dancer belonged to the Lucknow gharana?", "Birju Maharaj", "Ravi Shankar", "Bismillah Khan", "Zakir Hussain"),
        ("Which dance form is known for its strong use of circular movements and devotional themes in Manipur?", "Manipuri", "Kathakali", "Kuchipudi", "Bharatanatyam"),
        ("Which dance form traditionally includes vigorous movements, dramatic expressions and elaborate makeup?", "Kathakali", "Mohiniyattam", "Manipuri", "Sattriya"),
        ("Which classical dance form is traditionally performed by women and is known for graceful, swaying movements?", "Mohiniyattam", "Bhangra", "Chhau", "Garba"),
        ("Which classical dance form originated in the village of Kuchipudi in Andhra Pradesh?", "Kuchipudi", "Kathak", "Odissi", "Sattriya"),
        ("Which dance form is associated with the Jagannath tradition and temples of Odisha?", "Odissi", "Bharatanatyam", "Kathakali", "Manipuri"),
        ("Which dance form is traditionally associated with storytelling through rhythmic footwork and spins?", "Kathak", "Mohiniyattam", "Sattriya", "Manipuri"),
        ("Which musician is famous for popularising the Indian flute internationally?", "Hariprasad Chaurasia", "Zakir Hussain", "Bismillah Khan", "Amjad Ali Khan"),
        ("Which instrument is associated with Amjad Ali Khan?", "Sarod", "Tabla", "Shehnai", "Flute"),
        ("Which instrument is traditionally associated with Shivkumar Sharma?", "Santoor", "Sitar", "Shehnai", "Mridangam"),
        ("Which percussion instrument is central to Carnatic music?", "Mridangam", "Tabla", "Dhol", "Dafli"),
        ("Which instrument is a traditional plucked string instrument used in Carnatic music?", "Veena", "Shehnai", "Dhol", "Flute"),
        ("Which famous vocalist was a leading exponent of Carnatic classical music?", "M. S. Subbulakshmi", "Lata Mangeshkar", "Asha Bhosle", "Begum Akhtar"),
        ("Which Indian musician received international recognition for his work with the tabla?", "Zakir Hussain", "Ravi Shankar", "Amjad Ali Khan", "Bismillah Khan"),
        ("Which classical music system uses ragas and talas as important musical frameworks?", "Both Hindustani and Carnatic music", "Only Western classical music", "Only folk music", "Only electronic music"),
        ("What is a raga in Indian classical music?", "A melodic framework", "A percussion instrument", "A type of costume", "A dance stage"),
        ("What is tala in Indian classical music?", "A rhythmic cycle", "A type of painting", "A musical instrument", "A vocal ornament"),
        ("Which folk dance of Assam is performed during the Bihu festival?", "Bihu dance", "Garba", "Ghoomar", "Lavani"),
        ("Which folk dance is traditionally performed by women in Rajasthan?", "Ghoomar", "Bhangra", "Bihu", "Dandiya Raas"),
        ("Which folk dance of Gujarat is performed using decorated sticks?", "Dandiya Raas", "Lavani", "Bihu", "Ghoomar"),
        ("Which folk performance from Maharashtra is known for energetic singing and dance?", "Lavani", "Garba", "Bihu", "Rouf"),
        ("Which traditional dance-drama form is popular in coastal Karnataka?", "Yakshagana", "Kathakali", "Sattriya", "Mohiniyattam"),
        ("Which Indian dance form is associated with the martial traditions of Odisha, Jharkhand and West Bengal?", "Chhau", "Garba", "Ghoomar", "Lavani"),
        ("Which painting tradition is known for using natural colours and intricate narrative designs in Odisha?", "Pattachitra", "Warli", "Kalamkari", "Phad"),
        ("Which traditional art form from Andhra Pradesh involves painting on cloth using natural dyes?", "Kalamkari", "Warli", "Madhubani", "Phad"),
        ("Which Indian painter is known for the famous painting Bharat Mata and for being associated with the Bengal School?", "Abanindranath Tagore", "M. F. Husain", "Raja Ravi Varma", "Jamini Roy"),
        ("Which Indian artist is famous for combining Indian themes with European academic painting techniques?", "Raja Ravi Varma", "Amrita Sher-Gil", "Tyeb Mehta", "F. N. Souza"),
    ],

    "Hard": [
        ("Which ancient Sanskrit text is a major source for the theory of Indian performing arts?", "Natya Shastra", "Arthashastra", "Manusmriti", "Rajatarangini"),
        ("Who is traditionally credited with composing the Natya Shastra?", "Bharata Muni", "Kalidasa", "Panini", "Valmiki"),
        ("Which concept in the Natya Shastra refers to the aesthetic experience or emotional flavour of performance?", "Rasa", "Tala", "Shruti", "Alankara"),
        ("Which term refers to the expressive technique of conveying emotions through gestures and facial expressions in Indian dance?", "Abhinaya", "Alapana", "Tihai", "Jhala"),
        ("Which of the following is one of the four types of Abhinaya described in the Natya Shastra?", "Angika", "Raga", "Tala", "Shruti"),
        ("Which gharana of Kathak is particularly associated with Lucknow?", "Lucknow gharana", "Jaipur gharana", "Banaras gharana", "Raigarh gharana"),
        ("Which Kathak gharana is especially known for strong rhythmic footwork and complex compositions?", "Jaipur gharana", "Lucknow gharana", "Banaras gharana", "All of these equally"),
        ("Which guru is closely associated with the development of the Kuchipudi dance style?", "Vempati Chinna Satyam", "Kelucharan Mohapatra", "Birju Maharaj", "Rukmini Devi Arundale"),
        ("Which dancer is particularly associated with the revival of Manipuri dance?", "Guru Bipin Singh", "Birju Maharaj", "Uday Shankar", "Kelucharan Mohapatra"),
        ("Which institution founded by Rukmini Devi Arundale is associated with classical dance and arts education?", "Kalakshetra", "Sangeet Natak Akademi", "Lalit Kala Akademi", "National School of Drama"),
        ("In which year was the Sangeet Natak Akademi established?", "1953", "1947", "1961", "1975"),
        ("Which national institution is dedicated to the promotion of music, dance and drama in India?", "Sangeet Natak Akademi", "Lalit Kala Akademi", "Sahitya Akademi", "National Museum"),
        ("Which academy in India is primarily concerned with the promotion of visual arts?", "Lalit Kala Akademi", "Sangeet Natak Akademi", "Sahitya Akademi", "National School of Drama"),
        ("Which academy is responsible for promoting literature in Indian languages?", "Sahitya Akademi", "Lalit Kala Akademi", "Sangeet Natak Akademi", "Film and Television Institute of India"),
        ("Which Indian classical music system is traditionally associated with the compositions of Tyagaraja?", "Carnatic music", "Hindustani music", "Western classical music", "Persian classical music"),
        ("Tyagaraja is traditionally grouped with which two composers as the Carnatic Music Trinity?", "Muthuswami Dikshitar and Syama Sastri", "Purandara Dasa and Kanaka Dasa", "Tansen and Amir Khusrau", "Ravi Shankar and Ali Akbar Khan"),
        ("Which composer is widely known as the Pitamaha of Carnatic music?", "Purandara Dasa", "Tyagaraja", "Muthuswami Dikshitar", "Syama Sastri"),
        ("Which musical form is especially associated with the devotional compositions of the Carnatic tradition?", "Kriti", "Ghazal", "Qawwali", "Thumri"),
        ("Which form of Hindustani classical music is generally considered a major vocal genre with elaborate raga development?", "Khayal", "Lavani", "Bihu", "Dhrupad dance"),
        ("Which Hindustani classical vocal form is known for its ancient tradition and structured presentation?", "Dhrupad", "Garba", "Kriti", "Kuchipudi"),
        ("Which legendary musician is associated with the court of Emperor Akbar and the development of Hindustani music?", "Tansen", "Tyagaraja", "Purandara Dasa", "Muthuswami Dikshitar"),
        ("Which Indian classical instrument is associated with the Maihar gharana and Ravi Shankar's guru?", "Sitar", "Shehnai", "Mridangam", "Nadaswaram"),
        ("Who was Ravi Shankar's guru in Indian classical music?", "Allauddin Khan", "Bismillah Khan", "Zakir Hussain", "Bade Ghulam Ali Khan"),
        ("Which Indian musician is associated with the Maihar gharana and was the guru of Ravi Shankar and Ali Akbar Khan?", "Allauddin Khan", "Amjad Ali Khan", "Hariprasad Chaurasia", "Shivkumar Sharma"),
        ("Which traditional dance-drama form of Kerala is known for its stylised hand gestures called mudras?", "Kathakali", "Bhangra", "Garba", "Ghoomar"),
        ("Which dance form is traditionally associated with the Mahari and Gotipua traditions of Odisha?", "Odissi", "Kathak", "Sattriya", "Mohiniyattam"),
        ("Which folk dance of Jammu and Kashmir is traditionally performed by women in a group?", "Rouf", "Bhangra", "Garba", "Lavani"),
        ("Which dance form from Tamil Nadu is associated with martial movements and traditional stick fighting?", "Silambam", "Ghoomar", "Bihu", "Dandiya Raas"),
        ("Which Indian painting style is particularly associated with the Bengal School and its revivalist approach to Indian art?", "Bengal School of Art", "Company School", "Deccan School", "Mughal miniature school"),
        ("Which Indian painter is known for the painting Three Girls and is associated with modern Indian art?", "Amrita Sher-Gil", "Raja Ravi Varma", "Abanindranath Tagore", "Jamini Roy"),
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
                    "MCQ lesson covering Indian art, music, dance "
                    "and classical performing arts."
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
