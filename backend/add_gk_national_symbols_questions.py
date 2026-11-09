import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 162
LESSON_TITLE = "National Symbols and Heritage of India"
TOPIC = "General Knowledge"

BANK = {
"Easy": [
("What is the national animal of India?", "Bengal Tiger", "Lion", "Elephant", "Leopard"),
("What is the national bird of India?", "Indian Peacock", "Parrot", "Eagle", "Swan"),
("What is the national flower of India?", "Lotus", "Rose", "Sunflower", "Jasmine"),
("What is the national fruit of India?", "Mango", "Apple", "Banana", "Orange"),
("What is the national tree of India?", "Banyan Tree", "Neem Tree", "Peepal Tree", "Coconut Tree"),
("What is the national aquatic animal of India?", "Ganges River Dolphin", "Blue Whale", "Sea Turtle", "Crocodile"),
("What is the national anthem of India?", "Jana Gana Mana", "Vande Mataram", "Saare Jahan Se Achha", "Ae Mere Watan Ke Logon"),
("Who composed India's national anthem?", "Rabindranath Tagore", "Bankim Chandra Chatterjee", "Sarojini Naidu", "Subramania Bharati"),
("What is the national song of India?", "Vande Mataram", "Jana Gana Mana", "Sare Jahan Se Achha", "Raghupati Raghav Raja Ram"),
("Who wrote Vande Mataram?", "Bankim Chandra Chatterjee", "Rabindranath Tagore", "Mahatma Gandhi", "Muhammad Iqbal"),
("What are the colours of the Indian national flag?", "Saffron, White and Green", "Red, White and Blue", "Yellow, Green and Blue", "Orange, Yellow and Green"),
("What is the wheel in the centre of the Indian national flag called?", "Ashoka Chakra", "Dharma Wheel", "Victory Wheel", "National Wheel"),
("How many spokes are there in the Ashoka Chakra?", "24", "12", "18", "32"),
("What is the national currency of India?", "Indian Rupee", "Taka", "Riyal", "Dinar"),
("What is the national river of India?", "Ganga", "Yamuna", "Godavari", "Narmada"),
("Which animal appears on India's national emblem?", "Lion", "Tiger", "Elephant", "Horse"),
("From which monument was India's national emblem adapted?", "Lion Capital of Ashoka at Sarnath", "India Gate", "Qutub Minar", "Red Fort"),
("What is written below India's national emblem?", "Satyameva Jayate", "Jai Hind", "Vande Mataram", "Bharat Mata Ki Jai"),
("Which festival is popularly known as the Festival of Lights?", "Diwali", "Holi", "Eid", "Onam"),
("Which Indian festival is known as the Festival of Colours?", "Holi", "Diwali", "Pongal", "Baisakhi"),
("Which monument is located in Agra?", "Taj Mahal", "Gateway of India", "Charminar", "India Gate"),
("Who built the Taj Mahal?", "Shah Jahan", "Akbar", "Babur", "Aurangzeb"),
("Which Indian monument is located in Delhi and was built by Shah Jahan?", "Red Fort", "Gateway of India", "Sanchi Stupa", "Hawa Mahal"),
("Which classical dance form originated in Tamil Nadu?", "Bharatanatyam", "Kathak", "Bihu", "Garba"),
("Which classical dance form is associated with Kerala?", "Kathakali", "Bharatanatyam", "Odissi", "Kuchipudi"),
("Which Indian state is famous for the Konark Sun Temple?", "Odisha", "Gujarat", "Rajasthan", "Karnataka"),
("Which monument is famous for its four minarets in Hyderabad?", "Charminar", "Qutub Minar", "Hawa Mahal", "Gol Gumbaz"),
("Which Indian festival is celebrated in Kerala with boat races and flower decorations?", "Onam", "Pongal", "Bihu", "Lohri"),
("Which festival is widely celebrated in Punjab during the harvest season?", "Baisakhi", "Onam", "Pongal", "Hornbill"),
("Which day is celebrated as India's Independence Day?", "15 August", "26 January", "2 October", "14 November"),
],

"Medium": [
("When was the Indian national flag adopted by the Constituent Assembly?", "22 July 1947", "15 August 1947", "26 January 1950", "2 October 1947"),
("Who designed the Indian national flag in its present basic form?", "Pingali Venkayya", "Rabindranath Tagore", "Mahatma Gandhi", "B. R. Ambedkar"),
("What does the saffron colour in the Indian flag traditionally represent?", "Courage and sacrifice", "Peace and truth", "Growth and fertility", "Prosperity alone"),
("What does the white band of the Indian flag represent?", "Peace and truth", "Courage", "Agriculture", "Strength"),
("What does the green band of the Indian flag traditionally represent?", "Growth and prosperity", "Peace and truth", "Sacrifice", "Justice"),
("What is the source of the Ashoka Chakra on the Indian flag?", "Lion Capital of Ashoka", "Sanchi Gateway", "Red Fort", "Ajanta Caves"),
("In which language was the original Jana Gana Mana composed?", "Bengali", "Hindi", "Sanskrit", "Tamil"),
("When was Jana Gana Mana first sung at a session of the Indian National Congress?", "1911", "1905", "1920", "1947"),
("Which book originally contained the song Vande Mataram?", "Anandamath", "Gitanjali", "Discovery of India", "Godan"),
("Who wrote the book Anandamath?", "Bankim Chandra Chatterjee", "Rabindranath Tagore", "Munshi Premchand", "Sarojini Naidu"),
("Which Indian classical dance form originated in Andhra Pradesh?", "Kuchipudi", "Kathakali", "Manipuri", "Mohiniyattam"),
("Which classical dance form originated in Odisha?", "Odissi", "Kathak", "Bharatanatyam", "Kuchipudi"),
("Which classical dance form is associated with Uttar Pradesh?", "Kathak", "Sattriya", "Mohiniyattam", "Bharatanatyam"),
("Which classical dance form originated in Assam?", "Sattriya", "Odissi", "Kathakali", "Kuchipudi"),
("Which classical dance form is associated with Manipur?", "Manipuri", "Kathak", "Bharatanatyam", "Odissi"),
("Which classical dance form is associated with Kerala and traditionally depicts stories through expressive gestures?", "Kathakali", "Garba", "Bhangra", "Ghoomar"),
("Which ancient site is famous for Buddhist rock-cut caves in Maharashtra?", "Ajanta Caves", "Elephanta Caves", "Badami Caves", "Udayagiri Caves"),
("Which monument in Madhya Pradesh is famous for its Buddhist stupas?", "Sanchi Stupa", "Taj Mahal", "Hawa Mahal", "Charminar"),
("Which UNESCO World Heritage site is famous for its ancient temples in Tamil Nadu?", "Great Living Chola Temples", "Sun Temple of Konark", "Sanchi Stupa", "Red Fort"),
("Which monument is located in Mumbai and was built to commemorate the visit of King George V?", "Gateway of India", "India Gate", "Charminar", "Victoria Memorial"),
("Which monument in Delhi commemorates Indian soldiers who died in World War I?", "India Gate", "Red Fort", "Qutub Minar", "Jama Masjid"),
("Which famous monument in Jaipur is known as the Palace of Winds?", "Hawa Mahal", "City Palace", "Amber Fort", "Jantar Mantar"),
("Which temple is famous for its stone chariot in Karnataka?", "Vittala Temple", "Meenakshi Temple", "Jagannath Temple", "Somnath Temple"),
("Which UNESCO World Heritage site is located in Karnataka and was once the capital of the Vijayanagara Empire?", "Hampi", "Mysuru Palace", "Gol Gumbaz", "Belur"),
("Which festival is associated with the harvest of crops in Tamil Nadu?", "Pongal", "Onam", "Bihu", "Lohri"),
("Which festival is celebrated in Assam and is associated with the Assamese New Year?", "Bohag Bihu", "Onam", "Pongal", "Baisakhi"),
("Which festival is celebrated by the people of Nagaland and showcases tribal culture?", "Hornbill Festival", "Onam", "Lohri", "Pongal"),
("Which traditional Indian art form uses coloured powders to create designs on floors?", "Rangoli", "Warli", "Madhubani", "Pattachitra"),
("Which Indian painting style is traditionally associated with Bihar?", "Madhubani painting", "Warli painting", "Kalamkari", "Pattachitra"),
("Which traditional art form is associated with Maharashtra's tribal communities?", "Warli painting", "Madhubani painting", "Kalamkari", "Phad painting"),
],

"Hard": [
("What is the national heritage animal of India?", "Indian Elephant", "Bengal Tiger", "Asiatic Lion", "One-horned Rhinoceros"),
("Which Indian institution declared the Ganges River Dolphin as India's national aquatic animal?", "Government of India", "Indian Navy", "UNESCO", "World Wildlife Fund"),
("In which year was the Ganges River Dolphin declared India's national aquatic animal?", "2009", "2005", "2012", "2015"),
("When was the Indian national anthem officially adopted?", "24 January 1950", "15 August 1947", "22 July 1947", "26 November 1949"),
("How long does the full version of India's national anthem take to play?", "Approximately 52 seconds", "Approximately 30 seconds", "Approximately 60 seconds", "Approximately 90 seconds"),
("How many lines are included in the full version of Jana Gana Mana?", "Five", "Three", "Four", "Seven"),
("Which part of Vande Mataram was adopted as India's national song?", "Its first two stanzas", "Its last two stanzas", "All six stanzas", "Only its final stanza"),
("Which ancient Indian ruler's lion capital inspired the national emblem?", "Ashoka", "Chandragupta Maurya", "Samudragupta", "Harsha"),
("How many lions are visible in the Lion Capital of Ashoka when viewed from the front?", "Three", "Two", "Four", "Five"),
("What is the motto Satyameva Jayate translated into English?", "Truth Alone Triumphs", "Victory to India", "Unity is Strength", "Knowledge is Power"),
("From which Upanishad is the motto Satyameva Jayate taken?", "Mundaka Upanishad", "Katha Upanishad", "Isha Upanishad", "Chandogya Upanishad"),
("Which UNESCO World Heritage site in India is famous for its prehistoric rock shelters?", "Bhimbetka Rock Shelters", "Ajanta Caves", "Ellora Caves", "Elephanta Caves"),
("In which state are the Bhimbetka Rock Shelters located?", "Madhya Pradesh", "Rajasthan", "Maharashtra", "Gujarat"),
("Which UNESCO World Heritage site contains the famous Kailasa Temple?", "Ellora Caves", "Ajanta Caves", "Elephanta Caves", "Badami Caves"),
("The Kailasa Temple at Ellora was primarily built under which dynasty?", "Rashtrakuta dynasty", "Chola dynasty", "Gupta dynasty", "Pallava dynasty"),
("Which UNESCO World Heritage site is associated with the Chola dynasty?", "Great Living Chola Temples", "Sanchi Stupa", "Hampi", "Red Fort"),
("Which temple is famous for its annual Rath Yatra festival?", "Jagannath Temple, Puri", "Meenakshi Temple", "Somnath Temple", "Kedarnath Temple"),
("Which Indian monument is known for its distinctive bulbous dome and is located in Bijapur, Karnataka?", "Gol Gumbaz", "Charminar", "Hawa Mahal", "Qutub Minar"),
("Which architectural feature is Gol Gumbaz especially famous for?", "Whispering Gallery", "Iron Pillar", "Stone Chariot", "Stepwell"),
("Which Indian classical dance form was traditionally performed in the Vaishnavite monasteries of Assam?", "Sattriya", "Kathakali", "Odissi", "Manipuri"),
("Which classical dance form is traditionally associated with the devotional traditions of Kerala?", "Mohiniyattam", "Kathak", "Kuchipudi", "Sattriya"),
("Which UNESCO World Heritage site in India is famous for its group of monuments built by the Pallava dynasty?", "Group of Monuments at Mahabalipuram", "Khajuraho Group of Monuments", "Hampi", "Sanchi"),
("Mahabalipuram is located in which Indian state?", "Tamil Nadu", "Kerala", "Andhra Pradesh", "Karnataka"),
("Which Indian state is famous for the traditional Pattachitra painting style?", "Odisha", "Punjab", "Haryana", "Himachal Pradesh"),
("Which traditional textile art is associated with the state of Gujarat and uses tie-dye techniques?", "Bandhani", "Chikankari", "Phulkari", "Kanjeevaram"),
("Which traditional embroidery style is associated with Punjab?", "Phulkari", "Chikankari", "Kantha", "Kasuti"),
("Which Indian state is associated with the traditional Chikankari embroidery of Lucknow?", "Uttar Pradesh", "Rajasthan", "Gujarat", "Madhya Pradesh"),
("Which festival celebrates the victory of good over evil and is associated with the burning of Ravana effigies?", "Dussehra", "Onam", "Baisakhi", "Pongal"),
("Which Indian festival is celebrated to mark the birth of Lord Krishna?", "Janmashtami", "Ram Navami", "Mahashivratri", "Ganesh Chaturthi"),
("Which Indian festival is celebrated in Maharashtra with the installation and worship of Lord Ganesha idols?", "Ganesh Chaturthi", "Baisakhi", "Bihu", "Lohri"),
]
}


def validate_bank():
    for difficulty, questions in BANK.items():
        if len(questions) != 30:
            raise ValueError(
                f"{difficulty} contains {len(questions)} questions instead of 30."
            )

        for index, item in enumerate(questions, 1):
            if len(item) != 5:
                raise ValueError(f"Invalid question format: {difficulty} #{index}")

            question, correct, *wrong = item
            options = [correct] + wrong

            if not all(isinstance(x, str) and x.strip() for x in item):
                raise ValueError(f"Empty value: {difficulty} #{index}")

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
                "Learn about Indian national symbols, festivals, monuments and heritage."
            ))

            print("Lesson created:", LESSON_TITLE)

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
                    f"{difficulty} already contains {existing_count} questions."
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
                    f"{difficulty} has {final_count} questions, expected 30."
                )

            print(f"{difficulty}: {final_count}/30 SUCCESS")

        connection.commit()

        print("\n====================================")
        print("GK TOPIC 2 INSERTED SUCCESSFULLY")
        print("National Symbols and Heritage of India")
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