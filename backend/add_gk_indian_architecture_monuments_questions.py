
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 184
LESSON_TITLE = "Indian Architecture, Monuments, Temples and Historical Sites"
TOPIC = "General Knowledge"

BANK = {
    "Easy": [
        ("Which monument is known as the symbol of love in India?", "Taj Mahal", "Qutub Minar", "India Gate", "Charminar"),
        ("In which city is the Taj Mahal located?", "Agra", "Delhi", "Jaipur", "Lucknow"),
        ("Who built the Taj Mahal?", "Shah Jahan", "Akbar", "Aurangzeb", "Humayun"),
        ("Which monument is located in New Delhi and commemorates Indian soldiers?", "India Gate", "Gateway of India", "Charminar", "Gol Gumbaz"),
        ("Which famous monument is located in Mumbai?", "Gateway of India", "India Gate", "Hawa Mahal", "Qutub Minar"),
        ("Which monument is famous for its five-storey structure in Delhi?", "Qutub Minar", "Taj Mahal", "Sanchi Stupa", "Konark Sun Temple"),
        ("Which Indian monument is popularly known as the Palace of Winds?", "Hawa Mahal", "Mysore Palace", "City Palace", "Jal Mahal"),
        ("In which city is the Charminar located?", "Hyderabad", "Chennai", "Mumbai", "Kolkata"),
        ("Which Indian state is home to the Konark Sun Temple?", "Odisha", "Gujarat", "Rajasthan", "Karnataka"),
        ("Which monument is associated with the ancient Buddhist site of Sanchi?", "Great Stupa", "Iron Pillar", "Gol Gumbaz", "Victoria Memorial"),
        ("Where is the famous Golden Temple located?", "Amritsar", "Delhi", "Jaipur", "Varanasi"),
        ("Which city is famous for the Mysore Palace?", "Mysuru", "Bengaluru", "Hubballi", "Mangaluru"),
        ("Which Indian state is home to the Ajanta Caves?", "Maharashtra", "Kerala", "Punjab", "Assam"),
        ("Which Indian state is home to the Ellora Caves?", "Maharashtra", "Tamil Nadu", "Bihar", "Sikkim"),
        ("Which temple is famous for its giant chariot-shaped structure?", "Konark Sun Temple", "Meenakshi Temple", "Golden Temple", "Kedarnath Temple"),
        ("Where is the Meenakshi Amman Temple located?", "Madurai", "Mysuru", "Puri", "Bhopal"),
        ("Which temple is located in Puri, Odisha?", "Jagannath Temple", "Somnath Temple", "Kashi Vishwanath Temple", "Brihadeeswara Temple"),
        ("Which monument is located in Fatehpur Sikri?", "Buland Darwaza", "Charminar", "Gateway of India", "India Gate"),
        ("Who commissioned the construction of the Red Fort in Delhi?", "Shah Jahan", "Akbar", "Babur", "Sher Shah Suri"),
        ("Which Indian monument is famous for its leaning minaret-like towers called Charminar?", "Charminar", "Qutub Minar", "India Gate", "Hawa Mahal"),
        ("Which temple is dedicated to Lord Shiva and located in Thanjavur?", "Brihadeeswara Temple", "Jagannath Temple", "Sun Temple", "Lotus Temple"),
        ("Which monument is located in Kolkata and was built in memory of Queen Victoria?", "Victoria Memorial", "India Gate", "Gateway of India", "Rashtrapati Bhavan"),
        ("Which famous temple is located in Amritsar?", "Golden Temple", "Somnath Temple", "Meenakshi Temple", "Akshardham Temple"),
        ("Which ancient site is famous for Buddhist rock-cut caves in Maharashtra?", "Ajanta Caves", "Elephanta Caves", "Udayagiri Caves", "Badami Caves"),
        ("Which monument is located in Delhi and contains the tomb of Humayun?", "Humayun's Tomb", "Safdarjung's Tomb", "Taj Mahal", "Gol Gumbaz"),
        ("Which temple is famous for its large gopurams in Tamil Nadu?", "Meenakshi Temple", "Golden Temple", "Sun Temple", "Lotus Temple"),
        ("Which Indian monument is associated with the city of Bijapur?", "Gol Gumbaz", "Qutub Minar", "Hawa Mahal", "India Gate"),
        ("Which famous monument is located at Mahabalipuram?", "Shore Temple", "Golden Temple", "Charminar", "Victoria Memorial"),
        ("Which Indian state is home to the famous Dilwara Jain Temples?", "Rajasthan", "Odisha", "Punjab", "Assam"),
        ("Which monument is located in Delhi and is famous for its lotus-shaped design?", "Lotus Temple", "Red Fort", "India Gate", "Qutub Minar"),
    ],

    "Medium": [
        ("Which dynasty built the Brihadeeswara Temple at Thanjavur?", "Chola dynasty", "Gupta dynasty", "Maurya dynasty", "Kushan dynasty"),
        ("Who commissioned the construction of the Sun Temple at Konark?", "Narasimhadeva I", "Ashoka", "Raja Raja Chola I", "Krishnadevaraya"),
        ("Which architectural style is commonly associated with temples of North India?", "Nagara", "Dravida", "Vesara", "Indo-Islamic"),
        ("Which architectural style is traditionally associated with South Indian temples?", "Dravida", "Nagara", "Gothic", "Persian"),
        ("Which temple complex is famous for its stone chariot in Hampi?", "Vittala Temple", "Meenakshi Temple", "Jagannath Temple", "Somnath Temple"),
        ("Hampi was the capital of which historical empire?", "Vijayanagara Empire", "Maurya Empire", "Mughal Empire", "Gupta Empire"),
        ("Which ruler commissioned the construction of the Gol Gumbaz?", "Mohammed Adil Shah", "Akbar", "Shah Jahan", "Alauddin Khilji"),
        ("Which monument is famous for its whispering gallery?", "Gol Gumbaz", "Qutub Minar", "India Gate", "Hawa Mahal"),
        ("Which cave complex is famous for its ancient Hindu, Buddhist and Jain monuments?", "Ellora Caves", "Ajanta Caves", "Elephanta Caves", "Amarnath Caves"),
        ("Which cave complex is particularly famous for Buddhist paintings and murals?", "Ajanta Caves", "Elephanta Caves", "Badami Caves", "Udayagiri Caves"),
        ("Which ruler is associated with the construction of the Qutub Minar complex?", "Qutb-ud-din Aibak", "Akbar", "Sher Shah Suri", "Babur"),
        ("Who completed much of the Qutub Minar after Qutb-ud-din Aibak?", "Iltutmish", "Humayun", "Aurangzeb", "Alauddin Khilji"),
        ("Which monument in Delhi is known for its massive red sandstone walls?", "Red Fort", "Lotus Temple", "Humayun's Tomb", "Safdarjung's Tomb"),
        ("Which Mughal emperor built Fatehpur Sikri?", "Akbar", "Babur", "Jahangir", "Shah Jahan"),
        ("Which architectural feature is prominently associated with Mughal architecture?", "Domes and arches", "Wooden pagodas", "Gothic spires", "Thatched roofs"),
        ("Which monument is considered an early example of Mughal garden-tomb architecture in India?", "Humayun's Tomb", "India Gate", "Charminar", "Gol Gumbaz"),
        ("Which historical site in Karnataka is famous for its Chalukyan temples?", "Pattadakal", "Sanchi", "Nalanda", "Sarnath"),
        ("Which dynasty is strongly associated with the temples at Pattadakal?", "Chalukyas", "Mughals", "Mauryas", "Pallavas"),
        ("Which temple is famous for its monolithic rock-cut architecture at Mahabalipuram?", "Pancha Rathas", "Golden Temple", "Somnath Temple", "Akshardham Temple"),
        ("Which dynasty was responsible for many of the monuments at Mahabalipuram?", "Pallava dynasty", "Gupta dynasty", "Mughal dynasty", "Maurya dynasty"),
        ("Which ancient university site in Bihar contains the remains of a major Buddhist learning centre?", "Nalanda", "Hampi", "Pattadakal", "Sanchi"),
        ("Which ruler is associated with the construction of the Great Stupa at Sanchi?", "Ashoka", "Harsha", "Akbar", "Chandragupta II"),
        ("Which temple in Gujarat is traditionally associated with one of the twelve Jyotirlingas?", "Somnath Temple", "Jagannath Temple", "Meenakshi Temple", "Sun Temple"),
        ("Which historical monument in Delhi was built by Sher Shah Suri?", "Purana Qila", "Lotus Temple", "India Gate", "Rashtrapati Bhavan"),
        ("Which Indian monument is famous for its intricate marble inlay work?", "Taj Mahal", "Qutub Minar", "Charminar", "Gol Gumbaz"),
        ("Which temple in Karnataka is famous for its Hoysala architecture?", "Chennakesava Temple at Belur", "Golden Temple", "Somnath Temple", "Jagannath Temple"),
        ("Which dynasty built the famous temples at Belur and Halebidu?", "Hoysala dynasty", "Maurya dynasty", "Mughal dynasty", "Pala dynasty"),
        ("Which monument in Delhi was built as a victory tower after the Battle of Panipat?", "None of these", "Qutub Minar", "India Gate", "Lotus Temple"),
        ("Which UNESCO World Heritage Site in Madhya Pradesh is famous for its erotic sculptures?", "Khajuraho Group of Monuments", "Sanchi Stupa", "Bhimbetka Rock Shelters", "Gwalior Fort"),
        ("Which dynasty constructed most of the famous temples at Khajuraho?", "Chandela dynasty", "Chola dynasty", "Pallava dynasty", "Mughal dynasty"),
    ],

    "Hard": [
        ("Which architectural feature is characteristic of the Nagara style of temple architecture?", "Curvilinear shikhara", "Pyramidal vimana with tiered storeys", "Large onion dome", "Pointed Gothic arch"),
        ("Which feature is characteristic of the Dravida style of temple architecture?", "Pyramidal vimana", "Curvilinear northern shikhara", "Onion dome", "Flying buttress"),
        ("The Vesara style of temple architecture is generally understood as a combination of which traditions?", "Nagara and Dravida", "Mughal and Gothic", "Persian and Roman", "Buddhist and Greek"),
        ("Which Chola ruler commissioned the Gangaikonda Cholapuram temple?", "Rajendra Chola I", "Raja Raja Chola I", "Kulothunga Chola III", "Vijayalaya Chola"),
        ("Which temple was built by Raja Raja Chola I and is also known as the Peruvudaiyar Kovil?", "Brihadeeswara Temple", "Airavatesvara Temple", "Shore Temple", "Kailasa Temple"),
        ("The Kailasa Temple at Ellora was primarily commissioned by which Rashtrakuta ruler?", "Krishna I", "Amoghavarsha I", "Dantidurga", "Govinda III"),
        ("Which cave at Elephanta is especially famous for the Maheshmurti sculpture?", "Cave 1", "Cave 2", "Cave 3", "Cave 5"),
        ("The Maheshmurti sculpture at Elephanta represents which Hindu deity?", "Shiva", "Vishnu", "Brahma", "Indra"),
        ("Which architectural element is the main entrance tower of a South Indian temple complex called?", "Gopuram", "Shikhara", "Mandapa", "Stupa"),
        ("In North Indian temple architecture, what is the tower above the sanctum commonly called?", "Shikhara", "Gopuram", "Minaret", "Vihara"),
        ("Which temple is a major example of Kalinga architecture?", "Lingaraja Temple", "Meenakshi Temple", "Brihadeeswara Temple", "Golden Temple"),
        ("Which Indian temple is famous for its 13th-century construction and depiction of a solar chariot?", "Konark Sun Temple", "Somnath Temple", "Kedarnath Temple", "Virupaksha Temple"),
        ("Which ruler of the Eastern Ganga dynasty commissioned the Konark Sun Temple?", "Narasimhadeva I", "Anantavarman Chodaganga", "Kapilendra Deva", "Purushottama Deva"),
        ("Which temple complex in Odisha is traditionally associated with the Kalinga architectural style and the Lingaraja shrine?", "Bhubaneswar", "Madurai", "Thanjavur", "Amritsar"),
        ("Which Hoysala temple is located at Halebidu and is dedicated to Shiva?", "Hoysaleswara Temple", "Chennakesava Temple", "Virupaksha Temple", "Vittala Temple"),
        ("Which temple at Belur is dedicated to Chennakesava, a form of which deity?", "Vishnu", "Shiva", "Brahma", "Surya"),
        ("Which monument in Delhi contains the famous Iron Pillar associated with the Gupta period?", "Qutub complex", "Red Fort", "Humayun's Tomb", "Purana Qila"),
        ("The Iron Pillar in the Qutub complex is generally associated with which Gupta ruler?", "Chandragupta II", "Samudragupta", "Skandagupta", "Kumaragupta I"),
        ("Which Mughal garden-tomb is laid out according to the charbagh concept?", "Humayun's Tomb", "India Gate", "Charminar", "Gateway of India"),
        ("What does the Persian term charbagh refer to?", "A four-part garden layout", "A domed prayer hall", "A fortified palace", "A royal audience chamber"),
        ("Which Mughal monument is famous for its double dome and elaborate pietra dura decoration?", "Taj Mahal", "Qutub Minar", "Gol Gumbaz", "Hawa Mahal"),
        ("What is pietra dura in Mughal architecture?", "Inlay work using coloured stones in marble", "A type of sandstone carving", "A method of brick bonding", "A wooden roof construction technique"),
        ("Which monument in Fatehpur Sikri is known for its monumental gateway?", "Buland Darwaza", "Charminar", "India Gate", "Gateway of India"),
        ("Which ruler built the Buland Darwaza at Fatehpur Sikri?", "Akbar", "Jahangir", "Shah Jahan", "Aurangzeb"),
        ("Which ancient Buddhist monument is known for its gateways called toranas?", "Sanchi Stupa", "Gol Gumbaz", "Qutub Minar", "Charminar"),
        ("Which site in Madhya Pradesh contains prehistoric rock shelters and paintings?", "Bhimbetka", "Sarnath", "Nalanda", "Pattadakal"),
        ("Which historical site is associated with the first sermon of Gautama Buddha?", "Sarnath", "Bodh Gaya", "Kushinagar", "Lumbini"),
        ("Which monument in Karnataka is known for its massive monolithic statue of Bahubali?", "Gommateshwara statue at Shravanabelagola", "Statue of Unity", "Nandi statue at Lepakshi", "Buddha statue at Amaravati"),
        ("Which dynasty is associated with the construction of the Virupaksha Temple at Pattadakal?", "Chalukya dynasty", "Chola dynasty", "Mughal dynasty", "Maurya dynasty"),
        ("Which UNESCO World Heritage Site in India is famous for its group of monuments representing the Vijayanagara Empire?", "Hampi", "Sanchi", "Ajanta", "Mahabalipuram"),
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
                    "MCQ lesson covering Indian architecture, monuments, "
                    "temples and historical sites."
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
