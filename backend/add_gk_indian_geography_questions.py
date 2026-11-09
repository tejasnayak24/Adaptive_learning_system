
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 164
LESSON_TITLE = "Indian Geography - Rivers, Mountains, Climate and Natural Resources"
TOPIC = "General Knowledge"

BANK = {

"Easy": [

("Which is the longest river in India?", "Ganga", "Yamuna", "Godavari", "Narmada"),
("Which is the highest mountain peak in India?", "Kangchenjunga", "Nanda Devi", "Anamudi", "Kamet"),
("Which mountain range is located in northern India?", "Himalayas", "Aravalli", "Western Ghats", "Vindhya"),
("Which is the largest desert in India?", "Thar Desert", "Sahara Desert", "Gobi Desert", "Kalahari Desert"),
("Which river is known as the Dakshin Ganga?", "Godavari", "Krishna", "Kaveri", "Mahanadi"),
("Which is the largest freshwater lake in India by area?", "Wular Lake", "Dal Lake", "Sambhar Lake", "Chilika Lake"),
("Which is the largest saltwater lake in India?", "Chilika Lake", "Wular Lake", "Dal Lake", "Loktak Lake"),
("Which river flows through Delhi?", "Yamuna", "Ganga", "Godavari", "Narmada"),
("Which river originates from the Gangotri Glacier?", "Ganga", "Yamuna", "Brahmaputra", "Godavari"),
("Which Indian state receives heavy rainfall from the southwest monsoon?", "Kerala", "Rajasthan", "Punjab", "Haryana"),
("Which is the southernmost point of mainland India?", "Kanyakumari", "Indira Point", "Rameswaram", "Kochi"),
("Which ocean lies to the south of India?", "Indian Ocean", "Pacific Ocean", "Atlantic Ocean", "Arctic Ocean"),
("Which sea lies to the west of India?", "Arabian Sea", "Red Sea", "South China Sea", "Black Sea"),
("Which bay lies to the east of India?", "Bay of Bengal", "Persian Gulf", "Gulf of Aden", "Arabian Sea"),
("Which is the highest peak in the Western Ghats?", "Anamudi", "Doddabetta", "Mahendragiri", "Guru Shikhar"),
("Which mountain range runs along India's western coast?", "Western Ghats", "Eastern Ghats", "Aravalli Range", "Satpura Range"),
("Which river flows westward into the Arabian Sea?", "Narmada", "Ganga", "Mahanadi", "Godavari"),
("Which river is associated with the state of Assam?", "Brahmaputra", "Kaveri", "Krishna", "Narmada"),
("Which state is famous for the backwaters of Alleppey?", "Kerala", "Goa", "Karnataka", "Tamil Nadu"),
("Which is the largest state in India by area?", "Rajasthan", "Madhya Pradesh", "Maharashtra", "Uttar Pradesh"),
("Which is the smallest state in India by area?", "Goa", "Sikkim", "Tripura", "Manipur"),
("Which plateau covers a large part of southern India?", "Deccan Plateau", "Tibetan Plateau", "Chota Nagpur Plateau", "Malwa Plateau"),
("Which river forms the famous Jog Falls?", "Sharavathi", "Kaveri", "Krishna", "Godavari"),
("Which Indian state is famous for the Sundarbans mangrove forest?", "West Bengal", "Odisha", "Kerala", "Gujarat"),
("Which type of soil is best suited for cotton cultivation?", "Black soil", "Laterite soil", "Desert soil", "Mountain soil"),
("Which mineral is commonly used in the production of steel?", "Iron ore", "Mica", "Limestone", "Bauxite"),
("Which state is famous for tea plantations in India?", "Assam", "Rajasthan", "Punjab", "Goa"),
("Which river flows through the city of Varanasi?", "Ganga", "Yamuna", "Godavari", "Krishna"),
("Which island group is located in the Arabian Sea?", "Lakshadweep", "Andaman Islands", "Nicobar Islands", "Sunderban Islands"),
("Which season brings most of India's annual rainfall?", "Southwest monsoon", "Winter season", "Summer season", "Northeast winter season"),

],

"Medium": [

("Which river is the longest peninsular river in India?", "Godavari", "Krishna", "Kaveri", "Narmada"),
("Which two rivers flow westward through rift valleys?", "Narmada and Tapi", "Ganga and Yamuna", "Godavari and Krishna", "Mahanadi and Kaveri"),
("Which river originates near Mahabaleshwar in Maharashtra?", "Krishna", "Godavari", "Narmada", "Mahanadi"),
("Which river forms the boundary between Madhya Pradesh and Gujarat in parts of its course?", "Narmada", "Ganga", "Kaveri", "Brahmaputra"),
("Which river is known as the lifeline of Madhya Pradesh?", "Narmada", "Yamuna", "Teesta", "Periyar"),
("Which river forms the famous delta shared by India and Bangladesh?", "Ganga-Brahmaputra", "Narmada-Tapi", "Krishna-Godavari", "Kaveri-Pennar"),
("Which is the largest brackish water lagoon in India?", "Chilika Lake", "Wular Lake", "Sambhar Lake", "Dal Lake"),
("Which lake in Manipur is famous for floating islands called phumdis?", "Loktak Lake", "Dal Lake", "Pulicat Lake", "Vembanad Lake"),
("Which is the largest inland salt lake in India?", "Sambhar Lake", "Wular Lake", "Dal Lake", "Loktak Lake"),
("Which mountain range separates the Indo-Gangetic Plain from the Deccan Plateau?", "Vindhya Range", "Himalayas", "Karakoram Range", "Pir Panjal Range"),
("Which is the oldest mountain range in India?", "Aravalli Range", "Himalayas", "Western Ghats", "Satpura Range"),
("Which mountain range runs parallel to the eastern coast of India?", "Eastern Ghats", "Western Ghats", "Aravalli Range", "Karakoram Range"),
("Which pass connects Srinagar with Leh through the Himalayan region?", "Zoji La", "Nathu La", "Bomdi La", "Palakkad Gap"),
("Which mountain pass connects Sikkim with Tibet?", "Nathu La", "Zoji La", "Shipki La", "Rohtang Pass"),
("Which pass is located in Arunachal Pradesh and provides access towards Tibet?", "Bomdi La", "Palakkad Gap", "Bhor Ghat", "Naneghat"),
("Which gap connects Kerala with Tamil Nadu through the Western Ghats?", "Palakkad Gap", "Zoji La", "Nathu La", "Bhor Ghat"),
("Which region receives rainfall mainly from the northeast monsoon?", "Tamil Nadu coast", "Rajasthan", "Punjab", "Ladakh"),
("Which part of India experiences a tropical monsoon climate?", "Most of peninsular India", "Ladakh only", "Thar Desert only", "High Himalayan peaks only"),
("Which state has the highest average annual rainfall in India?", "Meghalaya", "Rajasthan", "Punjab", "Haryana"),
("Which place in Meghalaya is famous for extremely high rainfall?", "Mawsynram", "Jaipur", "Leh", "Bikaner"),
("Which soil is commonly found in the Deccan Trap region?", "Black soil", "Alluvial soil", "Desert soil", "Mountain soil"),
("Which soil is commonly found in the northern plains of India?", "Alluvial soil", "Black soil", "Laterite soil", "Red soil"),
("Which mineral is the principal ore of aluminium?", "Bauxite", "Iron ore", "Manganese", "Copper"),
("Which Indian state is a major producer of mica?", "Jharkhand", "Punjab", "Goa", "Haryana"),
("Which state is particularly known for its large coal reserves in the Jharia coalfield?", "Jharkhand", "Kerala", "Himachal Pradesh", "Punjab"),
("Which river is associated with the Hirakud Dam?", "Mahanadi", "Godavari", "Krishna", "Narmada"),
("Which river is associated with the Sardar Sarovar Dam?", "Narmada", "Kaveri", "Ganga", "Yamuna"),
("Which river is associated with the Bhakra Nangal Dam?", "Sutlej", "Ravi", "Beas", "Chenab"),
("Which river is associated with the Tehri Dam?", "Bhagirathi", "Yamuna", "Godavari", "Tapi"),
("Which state is home to the famous Silent Valley National Park?", "Kerala", "Gujarat", "Rajasthan", "Punjab"),

],

"Hard": [

("Which river is known as the Tsangpo in Tibet before entering India?", "Brahmaputra", "Indus", "Sutlej", "Ganga"),
("Which river enters India through Arunachal Pradesh as the Siang or Dihang?", "Brahmaputra", "Ganga", "Teesta", "Barak"),
("Which river originates near Amarkantak and flows westward?", "Narmada", "Godavari", "Krishna", "Mahanadi"),
("Which river originates in the Brahmagiri hills of Karnataka?", "Kaveri", "Krishna", "Godavari", "Tungabhadra"),
("Which river originates near Trimbakeshwar in Maharashtra?", "Godavari", "Krishna", "Narmada", "Tapi"),
("Which river is also known as the Vriddha Ganga?", "Godavari", "Kaveri", "Mahanadi", "Krishna"),
("Which river flows through the Kashmir Valley?", "Jhelum", "Ravi", "Beas", "Sutlej"),
("Which river is a major tributary of the Indus and flows through Himachal Pradesh and Punjab?", "Sutlej", "Yamuna", "Son", "Chambal"),
("Which river is formed by the confluence of the Alaknanda and Bhagirathi at Devprayag?", "Ganga", "Yamuna", "Mandakini", "Kali"),
("At which place do the Alaknanda and Bhagirathi rivers meet?", "Devprayag", "Rudraprayag", "Karnaprayag", "Vishnuprayag"),
("Which river joins the Ganga at Prayagraj along with the Yamuna?", "Saraswati (traditionally believed)", "Godavari", "Narmada", "Kaveri"),
("Which river basin covers the largest area in India?", "Ganga basin", "Narmada basin", "Kaveri basin", "Tapi basin"),
("Which river is associated with the Majuli river island in Assam?", "Brahmaputra", "Ganga", "Godavari", "Mahanadi"),
("Which is one of the world's largest inhabited river islands, located in Assam?", "Majuli", "Diu", "Elephanta", "Minicoy"),
("Which mountain range contains the famous Anaimudi peak?", "Western Ghats", "Eastern Ghats", "Aravalli", "Vindhya"),
("Which is the highest peak in the Nilgiri Hills?", "Doddabetta", "Anamudi", "Guru Shikhar", "Mahendragiri"),
("Which mountain range is located mainly in Rajasthan and Gujarat?", "Aravalli Range", "Satpura Range", "Pir Panjal Range", "Shivalik Range"),
("Which range lies south of the Vindhya Range?", "Satpura Range", "Karakoram Range", "Zanskar Range", "Shivalik Range"),
("Which Himalayan range is also known as the Outer Himalayas?", "Shivalik Range", "Himadri", "Himachal", "Karakoram"),
("Which is the northernmost and highest Himalayan range?", "Himadri", "Shivalik", "Lesser Himalayas", "Purvanchal"),
("Which Indian state contains the Thar Desert?", "Rajasthan", "Assam", "Kerala", "Bihar"),
("Which cold desert is located in the Indian Himalayan region of Himachal Pradesh?", "Spiti Valley", "Thar Desert", "Rann of Kutch", "Sundarbans"),
("Which region is famous for the white salt desert known as the Great Rann of Kutch?", "Gujarat", "Rajasthan", "Maharashtra", "Odisha"),
("Which type of soil develops mainly under conditions of high temperature and heavy rainfall?", "Laterite soil", "Black soil", "Desert soil", "Alluvial soil"),
("Which soil is formed from volcanic basalt rocks and is rich in clay?", "Black soil", "Red soil", "Alluvial soil", "Laterite soil"),
("Which mineral is essential for the manufacture of cement?", "Limestone", "Mica", "Gold", "Copper"),
("Which state has the Kolar Gold Fields?", "Karnataka", "Odisha", "Jharkhand", "Rajasthan"),
("Which state is famous for the Kudremukh iron ore region?", "Karnataka", "Punjab", "Bihar", "Assam"),
("Which Indian state is home to the Jharia coalfield?", "Jharkhand", "Kerala", "Goa", "Haryana"),
("Which phenomenon causes the seasonal reversal of wind direction over the Indian subcontinent?", "Monsoon circulation", "Ocean tides", "Earthquakes", "Volcanic activity"),

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
                raise ValueError(
                    f"Invalid format: {difficulty} question {index}"
                )

            question, correct, *wrong = item
            options = [correct] + wrong

            if not all(
                isinstance(value, str) and value.strip()
                for value in item
            ):
                raise ValueError(
                    f"Empty value: {difficulty} question {index}"
                )

            if len(set(options)) != 4:
                raise ValueError(
                    f"Duplicate options: {difficulty} question {index}"
                )

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
                "Learn about Indian rivers, mountains, climate and natural resources."
            ))

            print("Lesson created successfully.")

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
                        quiz_id,
                        question,
                        option_a,
                        option_b,
                        option_c,
                        option_d,
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
        print("GK TOPIC 4 INSERTED SUCCESSFULLY")
        print("Indian Geography")
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
