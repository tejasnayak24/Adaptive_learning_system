
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 168
LESSON_TITLE = "Indian Art, Culture, Festivals and Heritage"
TOPIC = "General Knowledge"

BANK = {
    "Easy": [
        ("Which festival is popularly known as the Festival of Lights?", "Diwali", "Holi", "Onam", "Baisakhi"),
        ("Which festival is known as the Festival of Colours?", "Holi", "Pongal", "Eid", "Christmas"),
        ("Which classical dance form originated in Tamil Nadu?", "Bharatanatyam", "Kathak", "Odissi", "Manipuri"),
        ("Kathak is traditionally associated with which region of India?", "North India", "Kerala", "Tamil Nadu", "Assam"),
        ("Which festival is widely celebrated in Kerala as a harvest festival?", "Onam", "Bihu", "Lohri", "Pongal"),
        ("Which Indian state is famous for the Bihu festival?", "Assam", "Punjab", "Gujarat", "Rajasthan"),
        ("Which festival marks the harvest season in Tamil Nadu?", "Pongal", "Onam", "Baisakhi", "Bihu"),
        ("Which monument is located in Agra and is a UNESCO World Heritage Site?", "Taj Mahal", "India Gate", "Gateway of India", "Charminar"),
        ("Which Indian state is famous for Garba dance?", "Gujarat", "Kerala", "Odisha", "Manipur"),
        ("Which musical instrument is associated with Pandit Ravi Shankar?", "Sitar", "Tabla", "Shehnai", "Flute"),
        ("Which festival celebrates the birth of Lord Krishna?", "Janmashtami", "Dussehra", "Diwali", "Makar Sankranti"),
        ("Which festival celebrates the victory of good over evil and is associated with Lord Rama's return to Ayodhya?", "Diwali", "Eid", "Christmas", "Baisakhi"),
        ("Which Indian state is famous for the traditional dance form Kathakali?", "Kerala", "Punjab", "Bihar", "Haryana"),
        ("Which dance form is traditionally performed during Navratri in Gujarat?", "Garba", "Bhangra", "Lavani", "Ghoomar"),
        ("Which festival is celebrated by the Sikh community to mark the formation of the Khalsa?", "Vaisakhi", "Onam", "Pongal", "Holi"),
        ("Which city is famous for the Charminar monument?", "Hyderabad", "Jaipur", "Mumbai", "Delhi"),
        ("Which Indian state is famous for the Ghoomar folk dance?", "Rajasthan", "Assam", "Goa", "Kerala"),
        ("Which festival is associated with the worship of Goddess Durga, especially in West Bengal?", "Durga Puja", "Pongal", "Lohri", "Bihu"),
        ("Which language is traditionally associated with classical Carnatic music?", "Tamil", "All of these regional languages are used", "Only Sanskrit", "Only Hindi"),
        ("Which Indian state is famous for the Hornbill Festival?", "Nagaland", "Kerala", "Gujarat", "Punjab"),
        ("Which traditional art form from Bihar is known for intricate paintings?", "Madhubani painting", "Warli painting", "Pattachitra", "Kalamkari"),
        ("Which Indian state is associated with the Warli painting tradition?", "Maharashtra", "Assam", "Punjab", "Sikkim"),
        ("Which festival is celebrated with bonfires in Punjab during winter?", "Lohri", "Onam", "Bihu", "Ugadi"),
        ("Which Indian monument is popularly known as the symbol of love?", "Taj Mahal", "Qutub Minar", "Hawa Mahal", "Sanchi Stupa"),
        ("Which classical dance form originated in Odisha?", "Odissi", "Kathakali", "Kuchipudi", "Mohiniyattam"),
        ("Which Indian state is famous for the Kuchipudi dance form?", "Andhra Pradesh", "Rajasthan", "Punjab", "Assam"),
        ("Which festival marks the beginning of the Hindu lunar new year in many parts of India?", "Ugadi", "Christmas", "Eid-ul-Fitr", "Lohri"),
        ("Which famous Indian festival is associated with kite flying in Gujarat?", "Uttarayan", "Onam", "Bihu", "Durga Puja"),
        ("Which traditional Indian instrument has a pair of drums?", "Tabla", "Sitar", "Veena", "Flute"),
        ("Which Indian state is particularly associated with the festival of Onam?", "Kerala", "Bihar", "Himachal Pradesh", "Madhya Pradesh"),
    ],

    "Medium": [
        ("How many classical dance forms are officially recognised in India?", "Eight", "Six", "Seven", "Ten"),
        ("Which dance form is associated with the Kuchipudi village?", "Kuchipudi", "Kathak", "Odissi", "Sattriya"),
        ("Sattriya classical dance originated in which state?", "Assam", "Odisha", "Kerala", "Manipur"),
        ("Mohiniyattam is a classical dance form from which state?", "Kerala", "Tamil Nadu", "Andhra Pradesh", "Karnataka"),
        ("Which ancient Indian text is traditionally associated with performing arts and theatre?", "Natya Shastra", "Arthashastra", "Manusmriti", "Rigveda"),
        ("Who is traditionally credited with composing the Natya Shastra?", "Bharata Muni", "Kalidasa", "Valmiki", "Panini"),
        ("Which UNESCO World Heritage Site is famous for its ancient Buddhist stupas and monuments?", "Sanchi", "Hampi", "Khajuraho", "Konark"),
        ("The Sun Temple at Konark is located in which state?", "Odisha", "Gujarat", "Rajasthan", "Maharashtra"),
        ("Which dynasty built the famous Brihadeeswara Temple at Thanjavur?", "Chola dynasty", "Gupta dynasty", "Mughal dynasty", "Maurya dynasty"),
        ("The Group of Monuments at Hampi is associated with which empire?", "Vijayanagara Empire", "Maurya Empire", "Mughal Empire", "Gupta Empire"),
        ("Which painting tradition is associated with Odisha?", "Pattachitra", "Madhubani", "Phad", "Kalamkari"),
        ("Which traditional textile art is associated with Andhra Pradesh and Telangana?", "Kalamkari", "Phulkari", "Chikankari", "Bandhani"),
        ("Phulkari embroidery is traditionally associated with which state?", "Punjab", "Kerala", "Assam", "Odisha"),
        ("Which Indian state is famous for Chikankari embroidery?", "Uttar Pradesh", "Rajasthan", "Nagaland", "Tamil Nadu"),
        ("Which folk dance is associated with Maharashtra?", "Lavani", "Bihu", "Garba", "Ghoomar"),
        ("Which folk dance is traditionally associated with Punjab?", "Bhangra", "Ghoomar", "Chhau", "Garba"),
        ("Which Indian classical music tradition is mainly associated with North India?", "Hindustani music", "Carnatic music", "Western classical music", "Gregorian chant"),
        ("Which classical music tradition is primarily associated with South India?", "Carnatic music", "Hindustani music", "Jazz", "Qawwali"),
        ("Which instrument is closely associated with the shehnai maestro Ustad Bismillah Khan?", "Shehnai", "Sitar", "Sarod", "Santoor"),
        ("Which festival in Rajasthan is particularly associated with the worship of Lord Brahma?", "Pushkar Fair", "Gangaur", "Teej", "Desert Festival"),
        ("Which Indian state hosts the famous Rath Yatra of Lord Jagannath at Puri?", "Odisha", "West Bengal", "Gujarat", "Bihar"),
        ("Which festival is celebrated in Karnataka to mark the victory of Goddess Chamundeshwari over Mahishasura?", "Mysuru Dasara", "Onam", "Bihu", "Pongal"),
        ("Which Indian state is associated with the traditional Theyyam ritual performance?", "Kerala", "Punjab", "Gujarat", "Madhya Pradesh"),
        ("Which Indian folk theatre form is traditionally associated with Karnataka?", "Yakshagana", "Jatra", "Tamasha", "Nautanki"),
        ("Which Indian folk theatre form is popular in Maharashtra?", "Tamasha", "Yakshagana", "Bhaona", "Therukoothu"),
        ("Which monument in Delhi was built by Qutb-ud-din Aibak and later completed by successors?", "Qutub Minar", "Red Fort", "Humayun's Tomb", "Jama Masjid"),
        ("Which Mughal emperor commissioned the construction of the Red Fort in Delhi?", "Shah Jahan", "Akbar", "Babur", "Aurangzeb"),
        ("Which Indian state is famous for the traditional blue pottery of Jaipur?", "Rajasthan", "Gujarat", "Assam", "Kerala"),
        ("Which festival is celebrated in Nagaland to showcase the culture of its tribes?", "Hornbill Festival", "Lohri", "Onam", "Pongal"),
        ("Which UNESCO-listed Indian site is famous for its rock-cut Buddhist, Hindu and Jain caves?", "Ellora Caves", "India Gate", "Victoria Memorial", "Gateway of India"),
    ],

    "Hard": [
        ("Which UNESCO convention provides the international framework for safeguarding intangible cultural heritage?", "2003 Convention", "1972 Convention", "1954 Convention", "1992 Convention"),
        ("Which ancient Indian treatise discusses music, dance and drama?", "Natya Shastra", "Charaka Samhita", "Sushruta Samhita", "Arthashastra"),
        ("Which temple architecture style is characterised by a curvilinear shikhara and is common in northern India?", "Nagara", "Dravida", "Vesara", "Gandhara"),
        ("Which temple architecture style is traditionally associated with South India and features a pyramidal vimana?", "Dravida", "Nagara", "Gandhara", "Indo-Islamic"),
        ("The Vesara style of temple architecture is generally associated with which region?", "Deccan region", "Himalayan region", "Gangetic plains only", "Northeastern region"),
        ("Which dynasty is closely associated with the construction of the Kailasa Temple at Ellora?", "Rashtrakuta dynasty", "Chola dynasty", "Pallava dynasty", "Gupta dynasty"),
        ("The Shore Temple at Mahabalipuram was built under which dynasty?", "Pallava dynasty", "Chola dynasty", "Maurya dynasty", "Mughal dynasty"),
        ("Which ruler is associated with the construction of the Great Stupa at Sanchi?", "Ashoka", "Kanishka", "Harsha", "Chandragupta II"),
        ("Which Indian UNESCO World Heritage Site is famous for its group of erotic sculptures and temples?", "Khajuraho", "Sanchi", "Hampi", "Mahabalipuram"),
        ("The Ajanta caves are primarily associated with which religious tradition?", "Buddhism", "Sikhism", "Islam", "Zoroastrianism"),
        ("Which painting style is traditionally associated with the royal courts of Rajasthan?", "Miniature painting", "Warli painting", "Madhubani painting", "Cheriyal painting"),
        ("Which school of miniature painting developed under the Mughal emperors?", "Mughal miniature painting", "Pattachitra", "Kalamkari", "Warli"),
        ("Which Indian art tradition uses natural dyes and hand-painted or block-printed motifs on fabric?", "Kalamkari", "Phulkari", "Chikankari", "Bidriware"),
        ("Bidriware, a metal handicraft tradition, is associated with which place?", "Bidar", "Jaipur", "Kochi", "Varanasi"),
        ("Which traditional Indian textile technique involves tying and dyeing sections of fabric to create patterns?", "Bandhani", "Chikankari", "Phulkari", "Zardozi"),
        ("Which Indian classical dance form is closely associated with the Vaishnavite monasteries called Satras?", "Sattriya", "Odissi", "Kathak", "Bharatanatyam"),
        ("Which dance form is known for its distinctive martial movements and is associated with eastern India?", "Chhau", "Mohiniyattam", "Kuchipudi", "Sattriya"),
        ("Which Indian classical music system uses ragas and talas and developed primarily in northern India?", "Hindustani music", "Carnatic music", "Gregorian music", "Western opera"),
        ("Which term refers to a melodic framework in Indian classical music?", "Raga", "Tala", "Shruti", "Laya"),
        ("In Indian classical music, what does the term Tala refer to?", "Rhythmic cycle", "Melodic scale", "Musical instrument", "Vocal register"),
        ("Which instrument is associated with the Carnatic music composer and performer M. S. Subbulakshmi?", "Vocal music", "Shehnai", "Sarod", "Santoor"),
        ("Which medieval Indian poet-composer is traditionally associated with the development of Hindustani classical music and the Dhrupad tradition?", "Swami Haridas", "Tansen alone", "Tyagaraja", "Purandara Dasa"),
        ("Which saint-composer is widely regarded as a major figure in Carnatic music and composed many kritis?", "Tyagaraja", "Amir Khusro", "Tansen", "Kabir"),
        ("Which Indian festival is associated with the harvest and the traditional boat races of Kerala?", "Onam", "Lohri", "Bihu", "Baisakhi"),
        ("Which festival of Arunachal Pradesh is celebrated by the Monpa community?", "Losar", "Pongal", "Gangaur", "Nuakhai"),
        ("Which festival is celebrated by the Garo community in Meghalaya?", "Wangala", "Onam", "Teej", "Lohri"),
        ("Which ancient Indian university site is located in Bihar and is a UNESCO World Heritage Site?", "Nalanda", "Takshashila", "Vikramashila", "Vallabhi"),
        ("Which Indian monument is a prominent example of Indo-Islamic architecture and was built by the Mughals?", "Humayun's Tomb", "Sanchi Stupa", "Brihadeeswara Temple", "Konark Sun Temple"),
        ("Which Indian UNESCO World Heritage Site is known for its astronomical instruments built by Maharaja Sawai Jai Singh II?", "Jantar Mantar, Jaipur", "Qutub Minar", "Gol Gumbaz", "Charminar"),
        ("Which Indian state is home to the living root bridges traditionally created by the Khasi and Jaintia communities?", "Meghalaya", "Sikkim", "Nagaland", "Manipur"),
    ]
}


def validate_bank():
    for difficulty, questions in BANK.items():
        if len(questions) != 30:
            raise ValueError(
                f"{difficulty}: Expected 30 questions, found {len(questions)}"
            )

        for index, item in enumerate(questions, 1):
            if len(item) != 5:
                raise ValueError(f"Invalid question format: {difficulty} #{index}")

            question, correct, *wrong = item
            options = [correct] + wrong

            if not all(isinstance(x, str) and x.strip() for x in item):
                raise ValueError(f"Empty field: {difficulty} #{index}")

            if len(set(options)) != 4:
                raise ValueError(f"Duplicate options: {difficulty} #{index}")

    print("Question bank validation successful.")


def main():
    validate_bank()

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT title, topic FROM lessons WHERE id = ?",
            (LESSON_ID,)
        )
        existing = cursor.fetchone()

        if existing is None:
            cursor.execute("""
                INSERT INTO lessons
                (id, title, topic, difficulty, content, created_at)
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (
                LESSON_ID,
                LESSON_TITLE,
                TOPIC,
                "Mixed",
                "Explore Indian art, classical dances, festivals, monuments, music and cultural heritage."
            ))
        elif existing != (LESSON_TITLE, TOPIC):
            raise ValueError(
                f"Lesson ID {LESSON_ID} is already occupied by {existing}"
            )

        for difficulty, questions in BANK.items():
            cursor.execute("""
                SELECT id FROM quizzes
                WHERE lesson_id = ? AND difficulty = ?
            """, (LESSON_ID, difficulty))

            quiz_rows = cursor.fetchall()

            if len(quiz_rows) > 1:
                raise ValueError(f"Multiple {difficulty} quizzes found.")

            if quiz_rows:
                quiz_id = quiz_rows[0][0]
            else:
                cursor.execute("""
                    INSERT INTO quizzes (lesson_id, title, difficulty)
                    VALUES (?, ?, ?)
                """, (
                    LESSON_ID,
                    f"{LESSON_TITLE} - {difficulty}",
                    difficulty
                ))
                quiz_id = cursor.lastrowid

            cursor.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                (quiz_id,)
            )
            existing_count = cursor.fetchone()[0]

            if existing_count > 30:
                raise ValueError(
                    f"{difficulty} already has {existing_count} questions."
                )

            for item in questions[existing_count:]:
                question, correct, wrong1, wrong2, wrong3 = item

                options = [correct, wrong1, wrong2, wrong3]
                random.shuffle(options)

                correct_letter = "ABCD"[options.index(correct)]

                cursor.execute("""
                    INSERT INTO questions (
                        quiz_id, question,
                        option_a, option_b, option_c, option_d,
                        correct_answer
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    quiz_id,
                    question,
                    options[0],
                    options[1],
                    options[2],
                    options[3],
                    correct_letter
                ))

            cursor.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                (quiz_id,)
            )
            final_count = cursor.fetchone()[0]

            if final_count != 30:
                raise ValueError(
                    f"{difficulty} has {final_count} questions instead of 30."
                )

            print(f"{difficulty}: {final_count}/30 SUCCESS")

        connection.commit()

        print("\n====================================")
        print("GK TOPIC 8 INSERTED SUCCESSFULLY")
        print("Indian Art, Culture, Festivals and Heritage")
        print("Easy: 30")
        print("Medium: 30")
        print("Hard: 30")
        print("TOTAL: 90 QUESTIONS")
        print("====================================")

    except Exception as error:
        connection.rollback()
        print("ERROR:", error)
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
