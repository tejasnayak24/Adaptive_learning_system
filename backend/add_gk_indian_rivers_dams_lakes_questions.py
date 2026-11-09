
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 185
LESSON_TITLE = "Indian Rivers, Dams, Lakes and Water Resources"
TOPIC = "General Knowledge"

BANK = {
    "Easy": [
        ("Which is the longest river in India by length within the country?", "Ganga", "Yamuna", "Godavari", "Narmada"),
        ("Which river is known as the Dakshin Ganga?", "Godavari", "Krishna", "Kaveri", "Mahanadi"),
        ("Which river flows through Delhi?", "Yamuna", "Godavari", "Narmada", "Tapti"),
        ("Which river is associated with the city of Varanasi?", "Ganga", "Krishna", "Kaveri", "Mahanadi"),
        ("Which is the largest river in South India by length?", "Godavari", "Periyar", "Vaigai", "Palar"),
        ("The Brahmaputra enters India through which state?", "Arunachal Pradesh", "Punjab", "Rajasthan", "Gujarat"),
        ("Which river flows westward into the Arabian Sea?", "Narmada", "Ganga", "Brahmaputra", "Mahanadi"),
        ("Which river is famous for forming the Sundarbans delta along with the Brahmaputra?", "Ganga", "Krishna", "Kaveri", "Luni"),
        ("Which is the largest freshwater lake in India by surface area?", "Wular Lake", "Chilika Lake", "Sambhar Lake", "Pulicat Lake"),
        ("Which is the largest brackish water lagoon in India?", "Chilika Lake", "Wular Lake", "Dal Lake", "Loktak Lake"),
        ("Dal Lake is located in which city?", "Srinagar", "Jaipur", "Bhopal", "Kochi"),
        ("Which lake in Rajasthan is famous as a saltwater lake?", "Sambhar Lake", "Dal Lake", "Wular Lake", "Loktak Lake"),
        ("Which dam is built across the Narmada River in Gujarat?", "Sardar Sarovar Dam", "Bhakra Dam", "Hirakud Dam", "Tehri Dam"),
        ("Bhakra Nangal Dam is built across which river?", "Sutlej", "Ganga", "Godavari", "Kaveri"),
        ("Which river is associated with the Hirakud Dam?", "Mahanadi", "Krishna", "Yamuna", "Periyar"),
        ("Tehri Dam is located in which Indian state?", "Uttarakhand", "Gujarat", "Odisha", "Karnataka"),
        ("Which river flows through the state of Assam?", "Brahmaputra", "Narmada", "Kaveri", "Sabarmati"),
        ("Which river originates near Mahabaleshwar in Maharashtra?", "Krishna", "Ganga", "Yamuna", "Brahmaputra"),
        ("Which river flows through the city of Ahmedabad?", "Sabarmati", "Godavari", "Mahanadi", "Kaveri"),
        ("Which lake is famous for floating islands called phumdis?", "Loktak Lake", "Dal Lake", "Sambhar Lake", "Pulicat Lake"),
        ("Loktak Lake is located in which state?", "Manipur", "Assam", "Meghalaya", "Tripura"),
        ("Which river is known for its famous Jog Falls?", "Sharavathi", "Krishna", "Godavari", "Kaveri"),
        ("Jog Falls is located in which state?", "Karnataka", "Kerala", "Tamil Nadu", "Goa"),
        ("Which river is considered sacred and originates from the Gangotri Glacier region?", "Ganga", "Godavari", "Mahanadi", "Tapti"),
        ("Which river is also known as the Tsangpo in Tibet?", "Brahmaputra", "Ganga", "Yamuna", "Narmada"),
        ("Which river flows through the state of Kerala?", "Periyar", "Yamuna", "Sutlej", "Luni"),
        ("Which lake is located between Andhra Pradesh and Tamil Nadu?", "Pulicat Lake", "Wular Lake", "Dal Lake", "Sambhar Lake"),
        ("Which river forms the famous Dhuandhar Falls?", "Narmada", "Krishna", "Godavari", "Kaveri"),
        ("Which river is associated with the city of Kolkata through its distributary Hooghly?", "Ganga", "Narmada", "Tapti", "Luni"),
        ("What is the main use of dams in India?", "Water storage, irrigation and electricity generation", "Only tourism", "Only fishing", "Only transportation"),
    ],

    "Medium": [
        ("Which two rivers are traditionally associated with the formation of the Ganga at Devprayag?", "Bhagirathi and Alaknanda", "Yamuna and Chambal", "Mandakini and Pindar", "Kosi and Gandak"),
        ("At which place do the Alaknanda and Bhagirathi rivers meet to form the Ganga?", "Devprayag", "Rudraprayag", "Karnaprayag", "Vishnuprayag"),
        ("Which river is known as the lifeline of Madhya Pradesh?", "Narmada", "Yamuna", "Sutlej", "Periyar"),
        ("Which river flows through a rift valley between the Vindhya and Satpura ranges?", "Narmada", "Ganga", "Brahmaputra", "Mahanadi"),
        ("Which river is a major tributary of the Ganga and originates near Yamunotri?", "Yamuna", "Godavari", "Kaveri", "Tapti"),
        ("Which river is known as the Sorrow of Bihar?", "Kosi", "Damodar", "Mahanadi", "Sabarmati"),
        ("Which river was historically called the Sorrow of Bengal?", "Damodar", "Krishna", "Periyar", "Luni"),
        ("Which river is the main tributary of the Yamuna in central India?", "Chambal", "Kaveri", "Periyar", "Sharavathi"),
        ("Which river originates in the Amarkantak region and flows westward?", "Narmada", "Ganga", "Godavari", "Brahmaputra"),
        ("Which major river flows through the Deccan Plateau and empties into the Bay of Bengal?", "Godavari", "Narmada", "Sabarmati", "Luni"),
        ("Which dam is built across the Krishna River in Telangana?", "Nagarjuna Sagar Dam", "Tehri Dam", "Bhakra Dam", "Hirakud Dam"),
        ("Which dam is constructed across the Kaveri River in Karnataka?", "Krishna Raja Sagara Dam", "Sardar Sarovar Dam", "Tehri Dam", "Rihand Dam"),
        ("Which dam is associated with the Mettur Reservoir in Tamil Nadu?", "Stanley Reservoir Dam", "Bhakra Dam", "Hirakud Dam", "Ukai Dam"),
        ("Which river is associated with the Indira Sagar Dam?", "Narmada", "Ganga", "Yamuna", "Brahmaputra"),
        ("Which dam is built across the Ravi River?", "Ranjit Sagar Dam", "Tehri Dam", "Hirakud Dam", "Nagarjuna Sagar Dam"),
        ("Which river is associated with the Koyna Dam?", "Koyna", "Godavari", "Tapti", "Mahanadi"),
        ("Which Indian lake is famous for the Keibul Lamjao floating national park?", "Loktak Lake", "Dal Lake", "Wular Lake", "Chilika Lake"),
        ("Which lake is a major wintering ground for migratory birds in Odisha?", "Chilika Lake", "Sambhar Lake", "Dal Lake", "Naini Lake"),
        ("Which lake is shared by Andhra Pradesh and Tamil Nadu?", "Pulicat Lake", "Wular Lake", "Loktak Lake", "Dal Lake"),
        ("Which is the largest inland salt lake in India?", "Sambhar Lake", "Wular Lake", "Dal Lake", "Bhimtal Lake"),
        ("Which river is formed by the confluence of the Tunga and Bhadra rivers?", "Tungabhadra", "Godavari", "Krishna", "Kaveri"),
        ("Which river is an important tributary of the Krishna River?", "Tungabhadra", "Yamuna", "Kosi", "Sutlej"),
        ("Which river flows through the city of Vijayawada?", "Krishna", "Ganga", "Narmada", "Brahmaputra"),
        ("Which river forms an estuary rather than a large delta at its mouth?", "Narmada", "Ganga", "Mahanadi", "Godavari"),
        ("Which river is associated with the Ukai Dam in Gujarat?", "Tapti", "Narmada", "Sabarmati", "Mahi"),
        ("Which river is associated with the Gandhi Sagar Dam?", "Chambal", "Kaveri", "Periyar", "Brahmaputra"),
        ("Which river flows through the state of Jharkhand and is associated with the Maithon Dam?", "Barakar", "Kaveri", "Yamuna", "Sharavathi"),
        ("Which river is associated with the Jayakwadi Dam in Maharashtra?", "Godavari", "Krishna", "Narmada", "Tapti"),
        ("Which river is associated with the famous Bhimashankar region in Maharashtra?", "Bhima", "Ganga", "Periyar", "Luni"),
        ("Which river is associated with the Nagarjuna Sagar Project?", "Krishna", "Godavari", "Mahanadi", "Sutlej"),
    ],

    "Hard": [
        ("Which river system has the largest drainage basin in India?", "Ganga river system", "Narmada river system", "Kaveri river system", "Periyar river system"),
        ("Which river originates near the Mansarovar region and enters India as the Brahmaputra?", "Yarlung Tsangpo", "Indus", "Sutlej", "Karnali"),
        ("Which is the principal source stream of the Ganga according to its traditional identification at Gangotri?", "Bhagirathi", "Alaknanda", "Mandakini", "Pindar"),
        ("Which river joins the Alaknanda at Rudraprayag?", "Mandakini", "Bhagirathi", "Yamuna", "Dhauliganga"),
        ("Which river joins the Alaknanda at Vishnuprayag?", "Dhauliganga", "Mandakini", "Bhagirathi", "Pindar"),
        ("Which river joins the Alaknanda at Karnaprayag?", "Pindar", "Mandakini", "Bhagirathi", "Yamuna"),
        ("Which river is formed after the confluence of the Chandra and Bhaga rivers?", "Chenab", "Ravi", "Beas", "Sutlej"),
        ("Which river is known as the Vitasta in ancient Indian texts?", "Jhelum", "Ravi", "Beas", "Chenab"),
        ("Which river is known as the Vipasa in ancient Indian texts?", "Beas", "Jhelum", "Sutlej", "Ravi"),
        ("Which river is known as the Shatadru in ancient Indian texts?", "Sutlej", "Ravi", "Beas", "Chenab"),
        ("Which river is associated with the Farakka Barrage?", "Ganga", "Godavari", "Narmada", "Krishna"),
        ("The Tehri Dam is built on which tributary of the Ganga?", "Bhagirathi", "Alaknanda", "Yamuna", "Mandakini"),
        ("Which project is associated with the multipurpose development of the Damodar River Valley?", "Damodar Valley Project", "Narmada Valley Project", "Kosi Project", "Bhakra Project"),
        ("Which was one of the first major multipurpose river valley projects in independent India?", "Damodar Valley Project", "Tehri Project", "Sardar Sarovar Project", "Indira Sagar Project"),
        ("Which river is associated with the Polavaram multipurpose project?", "Godavari", "Krishna", "Kaveri", "Mahanadi"),
        ("Which river is associated with the Almatti Dam?", "Krishna", "Godavari", "Narmada", "Tapti"),
        ("Which river is associated with the Tungabhadra Dam near Hospet?", "Tungabhadra", "Kaveri", "Periyar", "Sharavathi"),
        ("Which river is associated with the Bansagar Dam?", "Son", "Yamuna", "Ganga", "Mahi"),
        ("Which river is associated with the Rihand Dam?", "Rihand", "Sutlej", "Krishna", "Kaveri"),
        ("Which reservoir is created by the Hirakud Dam?", "Hirakud Reservoir", "Gobind Sagar", "Tehri Reservoir", "Indira Sagar"),
        ("Which lake is a Ramsar site and is known for its floating vegetation islands called phumdis?", "Loktak Lake", "Sambhar Lake", "Pulicat Lake", "Naini Lake"),
        ("Which Indian lake is a Ramsar site and is famous for its brackish water lagoon ecosystem?", "Chilika Lake", "Dal Lake", "Bhimtal Lake", "Naini Lake"),
        ("Which lake is located in the Kashmir Valley and is one of India's largest freshwater lakes?", "Wular Lake", "Sambhar Lake", "Chilika Lake", "Pulicat Lake"),
        ("Which river flows through the Kutch region and drains into the Rann of Kutch?", "Luni", "Ganga", "Godavari", "Kaveri"),
        ("Which river is an important west-flowing river that forms an estuary near Bharuch?", "Narmada", "Mahanadi", "Godavari", "Krishna"),
        ("Which river is associated with the Gulf of Khambhat and flows through Gujarat?", "Mahi", "Ganga", "Brahmaputra", "Kaveri"),
        ("Which river has its source near the Brahmagiri Hills in Karnataka?", "Kaveri", "Godavari", "Narmada", "Tapti"),
        ("Which river forms the Shivanasamudra Falls?", "Kaveri", "Krishna", "Godavari", "Tungabhadra"),
        ("Which river is associated with the Srisailam Dam?", "Krishna", "Godavari", "Mahanadi", "Narmada"),
        ("Which river basin is shared by Maharashtra, Telangana, Andhra Pradesh and other states?", "Godavari basin", "Narmada basin", "Periyar basin", "Sabarmati basin"),
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
                    "MCQ lesson covering Indian rivers, dams, lakes "
                    "and water resources."
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
