
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 183
LESSON_TITLE = "Indian Festivals, Fairs, Traditions and Religious Heritage"
TOPIC = "General Knowledge"

# Format: (question, correct answer, wrong option 1, wrong option 2, wrong option 3)

BANK = {
    "Easy": [
        ("Which festival is popularly known as the Festival of Lights?", "Diwali", "Holi", "Onam", "Baisakhi"),
        ("Which festival is known as the Festival of Colours?", "Holi", "Pongal", "Eid", "Christmas"),
        ("Which state is especially famous for the celebration of Onam?", "Kerala", "Punjab", "Gujarat", "Assam"),
        ("Bihu is a major festival of which Indian state?", "Assam", "Rajasthan", "Goa", "Bihar"),
        ("Which festival celebrates the harvest in Tamil Nadu?", "Pongal", "Baisakhi", "Lohri", "Hornbill"),
        ("Which festival is celebrated to mark the birth of Lord Krishna?", "Janmashtami", "Ram Navami", "Ganesh Chaturthi", "Makar Sankranti"),
        ("Ganesh Chaturthi is celebrated in honour of which deity?", "Lord Ganesha", "Lord Shiva", "Lord Vishnu", "Lord Brahma"),
        ("Which festival marks the birth of Lord Rama?", "Ram Navami", "Janmashtami", "Diwali", "Navratri"),
        ("Which festival is widely celebrated in Punjab during the harvest season?", "Baisakhi", "Onam", "Pongal", "Bihu"),
        ("Which festival is associated with the worship of Goddess Durga?", "Durga Puja", "Eid-ul-Fitr", "Christmas", "Buddha Purnima"),
        ("Which festival is celebrated at the end of Ramadan?", "Eid-ul-Fitr", "Eid-ul-Adha", "Muharram", "Christmas"),
        ("Which festival commemorates the birth of Jesus Christ?", "Christmas", "Easter", "Good Friday", "Diwali"),
        ("Which festival celebrates the birth of Gautama Buddha?", "Buddha Purnima", "Mahavir Jayanti", "Guru Nanak Jayanti", "Holi"),
        ("Which festival is associated with the birth of Guru Nanak?", "Guru Nanak Jayanti", "Baisakhi", "Lohri", "Diwali"),
        ("Which Indian festival is associated with the worship of the Sun God in Bihar?", "Chhath Puja", "Onam", "Bihu", "Pongal"),
        ("Which festival is popularly celebrated with bonfires in Punjab?", "Lohri", "Holi", "Diwali", "Raksha Bandhan"),
        ("Which festival celebrates the bond between brothers and sisters?", "Raksha Bandhan", "Karva Chauth", "Onam", "Baisakhi"),
        ("Which festival is associated with the worship of Goddess Saraswati?", "Vasant Panchami", "Makar Sankranti", "Eid-ul-Fitr", "Lohri"),
        ("Which famous fair is held in Pushkar, Rajasthan?", "Pushkar Camel Fair", "Surajkund Mela", "Sonepur Cattle Fair", "Hemis Festival"),
        ("Which festival is celebrated by the people of Nagaland as a major cultural event?", "Hornbill Festival", "Onam", "Pongal", "Bihu"),
        ("Which festival is known as the harvest festival of Kerala?", "Onam", "Lohri", "Baisakhi", "Makar Sankranti"),
        ("Which festival is celebrated by flying kites in Gujarat?", "Uttarayan", "Onam", "Durga Puja", "Christmas"),
        ("Which festival marks the victory of good over evil and is associated with Ravana's defeat?", "Dussehra", "Eid-ul-Adha", "Buddha Purnima", "Pongal"),
        ("Which festival is celebrated by lighting lamps during the Kartika month in many parts of India?", "Karthigai Deepam", "Bihu", "Lohri", "Baisakhi"),
        ("Which festival is especially famous in West Bengal?", "Durga Puja", "Onam", "Pongal", "Bihu"),
        ("Which festival is celebrated by the Jain community to mark the birth of Mahavira?", "Mahavir Jayanti", "Buddha Purnima", "Guru Nanak Jayanti", "Janmashtami"),
        ("Which festival is associated with the harvest of new crops in Assam?", "Magh Bihu", "Durga Puja", "Ganesh Chaturthi", "Raksha Bandhan"),
        ("Which festival is celebrated with a traditional boat race in Kerala?", "Onam", "Holi", "Diwali", "Lohri"),
        ("Which festival is associated with the worship of Lord Shiva?", "Maha Shivaratri", "Janmashtami", "Ram Navami", "Vasant Panchami"),
        ("Which famous religious gathering takes place at Prayagraj, Haridwar, Ujjain and Nashik?", "Kumbh Mela", "Pushkar Fair", "Hornbill Festival", "Surajkund Mela"),
    ],

    "Medium": [
        ("Which state hosts the famous Ambubachi Mela at the Kamakhya Temple?", "Assam", "Odisha", "Bihar", "West Bengal"),
        ("The Rath Yatra of Lord Jagannath is most famously celebrated in which city?", "Puri", "Varanasi", "Madurai", "Dwarka"),
        ("Which festival is associated with the worship of Goddess Kamakhya in Assam?", "Ambubachi Mela", "Hornbill Festival", "Bihu", "Chapchar Kut"),
        ("Chapchar Kut is a traditional festival of which Indian state?", "Mizoram", "Nagaland", "Manipur", "Tripura"),
        ("Wangala, also known as the Hundred Drums Festival, is celebrated by which community?", "Garo", "Bodo", "Khasi", "Mizo"),
        ("Losar is traditionally celebrated as the New Year festival in which cultural region?", "Tibetan Buddhist communities", "Tamil communities", "Punjabi communities", "Malayali communities"),
        ("Which state is famous for the Hemis Festival?", "Ladakh", "Kerala", "Gujarat", "Bihar"),
        ("Which traditional festival of Manipur is associated with the worship of the deity Sanamahi?", "Lai Haraoba", "Bihu", "Onam", "Lohri"),
        ("Which festival is celebrated by the Khasi community of Meghalaya?", "Nongkrem Dance Festival", "Hornbill Festival", "Baisakhi", "Pongal"),
        ("Which fair in Rajasthan is famous for camel trading and cultural activities?", "Pushkar Fair", "Surajkund Mela", "Kumbh Mela", "Gangasagar Mela"),
        ("The Surajkund International Crafts Mela is held in which state?", "Haryana", "Punjab", "Rajasthan", "Uttar Pradesh"),
        ("Which famous cattle fair is held at Sonepur in Bihar?", "Sonepur Mela", "Pushkar Fair", "Baneshwar Fair", "Gangasagar Mela"),
        ("Which festival in Kerala features the traditional Pulikali tiger dance?", "Onam", "Vishu", "Thrissur Pooram", "Attukal Pongala"),
        ("Vishu is traditionally celebrated as the New Year festival in which state?", "Kerala", "Assam", "Punjab", "Gujarat"),
        ("Which famous festival in Kerala is known for its elaborate elephant processions and percussion performances?", "Thrissur Pooram", "Bihu", "Lohri", "Hornbill Festival"),
        ("Which festival in Maharashtra is associated with the worship of Lord Ganesha and large public processions?", "Ganesh Chaturthi", "Onam", "Baisakhi", "Magh Bihu"),
        ("Which festival is associated with the traditional dance Garba?", "Navratri", "Onam", "Bihu", "Lohri"),
        ("Which state is particularly associated with the festival of Gangaur?", "Rajasthan", "Assam", "Kerala", "Nagaland"),
        ("Which festival is celebrated by the people of Goa with colourful processions and traditional performances before Lent?", "Carnival", "Bihu", "Pongal", "Onam"),
        ("Which festival in Karnataka is celebrated with the famous Mysuru Dasara procession?", "Mysuru Dasara", "Baisakhi", "Hornbill", "Vishu"),
        ("Which festival is associated with the traditional spring celebration of the Manipuri community?", "Yaoshang", "Lohri", "Pongal", "Vasant Panchami"),
        ("Which festival is celebrated by the people of Arunachal Pradesh as a major agricultural festival?", "Solung", "Onam", "Bihu", "Gangaur"),
        ("Which community celebrates the festival of Mopin in Arunachal Pradesh?", "Galo", "Garo", "Khasi", "Mizo"),
        ("Which festival of Sikkim is associated with the worship of Mount Kanchenjunga?", "Pang Lhabsol", "Hornbill", "Baisakhi", "Lai Haraoba"),
        ("Which festival is celebrated by the Buddhist community in Ladakh with masked dances at monasteries?", "Hemis Festival", "Vishu", "Magh Bihu", "Pongal"),
        ("Which Hindu festival is associated with the worship of the Sun God and is celebrated in the month of Magha?", "Ratha Saptami", "Janmashtami", "Raksha Bandhan", "Ganesh Chaturthi"),
        ("Which pilgrimage festival is associated with the confluence of the Ganga and the Bay of Bengal?", "Gangasagar Mela", "Pushkar Fair", "Surajkund Mela", "Hornbill Festival"),
        ("Which festival celebrates the beginning of the traditional Assamese New Year?", "Bohag Bihu", "Magh Bihu", "Kati Bihu", "Chapchar Kut"),
        ("Which festival is known as the festival of harvest and thanksgiving in parts of northeastern India?", "Wangala", "Diwali", "Eid-ul-Fitr", "Christmas"),
        ("Which traditional festival of Tamil Nadu is associated with the worship of Lord Murugan?", "Thaipusam", "Baisakhi", "Lohri", "Hornbill Festival"),
    ],

    "Hard": [
        ("Which ancient text is traditionally associated with the origin of the Kumbh Mela's mythological story of the churning of the ocean?", "Puranic traditions", "Arthashastra", "Natya Shastra", "Ashtadhyayi"),
        ("At which four locations is the traditional Kumbh Mela held in rotation?", "Prayagraj, Haridwar, Ujjain and Nashik", "Delhi, Jaipur, Patna and Lucknow", "Puri, Madurai, Kochi and Mysuru", "Amritsar, Varanasi, Ajmer and Gaya"),
        ("Which festival is associated with the annual pilgrimage to the shrine of Mata Vaishno Devi?", "Navratri", "Bihu", "Pongal", "Lohri"),
        ("Which religious gathering is held at the island of Sagar in West Bengal?", "Gangasagar Mela", "Pushkar Fair", "Hemis Festival", "Surajkund Mela"),
        ("Which festival of Ladakh celebrates the victory of good over evil through traditional masked dances?", "Dosmoche", "Vishu", "Wangala", "Bohag Bihu"),
        ("Which festival is associated with the traditional harvest celebrations of the Apatani community in Arunachal Pradesh?", "Dree Festival", "Hornbill Festival", "Wangala", "Chapchar Kut"),
        ("Which festival of Nagaland is celebrated by the Angami community?", "Sekrenyi", "Mopin", "Solung", "Nongkrem"),
        ("Which traditional festival is celebrated by the Ao Naga community?", "Moatsu", "Chapchar Kut", "Wangala", "Yaoshang"),
        ("Which festival is associated with the Konyak Naga community?", "Aoling", "Onam", "Vishu", "Lohri"),
        ("Which festival of Tripura is associated with the worship of fourteen deities?", "Kharchi Puja", "Bihu", "Gangaur", "Vasant Panchami"),
        ("Which festival of Meghalaya is associated with the harvest and thanksgiving traditions of the Khasi community?", "Shad Suk Mynsiem", "Hornbill Festival", "Baisakhi", "Onam"),
        ("Which festival of Manipur is associated with the traditional boat race and worship of the deity Lord Thangjing?", "Heikru Hidongba", "Lai Haraoba", "Yaoshang", "Ningol Chakouba"),
        ("Ningol Chakouba is a traditional festival celebrated mainly in which state?", "Manipur", "Assam", "Nagaland", "Mizoram"),
        ("Which festival of Arunachal Pradesh is celebrated by the Monpa community?", "Losar", "Mopin", "Solung", "Wangala"),
        ("Which traditional festival of Mizoram celebrates the completion of the jhum cultivation process?", "Mim Kut", "Onam", "Bihu", "Gangaur"),
        ("Which festival of Mizoram is associated with the post-harvest celebration of maize?", "Mim Kut", "Chapchar Kut", "Pang Lhabsol", "Moatsu"),
        ("Which traditional festival of the Bodo community in Assam is associated with spring and the new agricultural season?", "Bwisagu", "Wangala", "Mopin", "Sekrenyi"),
        ("Which festival of the Bhil community is associated with a major tribal gathering in Rajasthan and Madhya Pradesh?", "Baneshwar Fair", "Pushkar Fair", "Surajkund Mela", "Gangasagar Mela"),
        ("Which festival is associated with the worship of the goddess Kamakhya during the annual period of her symbolic menstruation?", "Ambubachi Mela", "Durga Puja", "Kali Puja", "Vasant Panchami"),
        ("Which traditional festival of Rajasthan is especially associated with married women praying for the well-being of their husbands?", "Gangaur", "Baisakhi", "Bihu", "Pongal"),
        ("Which festival is celebrated in Tamil Nadu to honour the birth of Lord Murugan and includes kavadi processions?", "Thaipusam", "Pongal", "Karthigai Deepam", "Aadi Perukku"),
        ("Which festival of Kerala is associated with the ceremonial offering of pongala to Goddess Attukal Bhagavathy?", "Attukal Pongala", "Thrissur Pooram", "Vishu", "Onam"),
        ("Which annual festival at the Jagannath Temple involves the ceremonial bathing of the deities before the Rath Yatra?", "Snana Yatra", "Dol Purnima", "Makar Sankranti", "Kartik Purnima"),
        ("Which festival is associated with the worship of the Sun God at the Konark Sun Temple region?", "Chandrabhaga Mela", "Pushkar Fair", "Surajkund Mela", "Baneshwar Fair"),
        ("Which festival is celebrated by the Tulu-speaking communities of coastal Karnataka as a traditional harvest and cultural celebration?", "Kambala season celebrations", "Hornbill Festival", "Wangala", "Mopin"),
        ("Which traditional event in coastal Karnataka involves buffalo racing in specially prepared muddy tracks?", "Kambala", "Jallikattu", "Vallam Kali", "Garba"),
        ("Which Tamil festival features the traditional bull-taming sport known as Jallikattu?", "Pongal", "Onam", "Vishu", "Bihu"),
        ("Which festival in Kerala is associated with the traditional snake boat races called Vallam Kali?", "Onam", "Lohri", "Baisakhi", "Navratri"),
        ("Which religious festival is observed by Jains to mark the birth anniversary of the 24th Tirthankara?", "Mahavir Jayanti", "Buddha Purnima", "Guru Purnima", "Janmashtami"),
        ("Which festival marks the first sermon of Gautama Buddha in Buddhist tradition?", "Dharmachakra Pravartana Day", "Mahavir Jayanti", "Guru Nanak Jayanti", "Diwali"),
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
                    "MCQ lesson covering Indian festivals, fairs, "
                    "traditions and religious heritage."
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
