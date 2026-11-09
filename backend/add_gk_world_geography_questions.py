
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 169
LESSON_TITLE = "World Geography - Continents, Oceans, Countries and Capitals"
TOPIC = "General Knowledge"

BANK = {
    "Easy": [
        ("How many continents are there?", "Seven", "Five", "Six", "Eight"),
        ("Which is the largest continent?", "Asia", "Africa", "Europe", "Australia"),
        ("Which is the smallest continent?", "Australia", "Europe", "Antarctica", "South America"),
        ("Which is the largest ocean?", "Pacific Ocean", "Atlantic Ocean", "Indian Ocean", "Arctic Ocean"),
        ("Which ocean lies between Africa and Australia?", "Indian Ocean", "Atlantic Ocean", "Arctic Ocean", "Southern Ocean"),
        ("What is the capital of France?", "Paris", "Rome", "Madrid", "Berlin"),
        ("What is the capital of Japan?", "Tokyo", "Seoul", "Beijing", "Bangkok"),
        ("What is the capital of Australia?", "Canberra", "Sydney", "Melbourne", "Perth"),
        ("What is the capital of the United Kingdom?", "London", "Manchester", "Edinburgh", "Liverpool"),
        ("What is the capital of Italy?", "Rome", "Venice", "Milan", "Florence"),
        ("Which continent is known as the Dark Continent in historical terminology?", "Africa", "Asia", "Europe", "South America"),
        ("Which continent is home to the Amazon Rainforest?", "South America", "Africa", "Europe", "Australia"),
        ("Which is the coldest continent?", "Antarctica", "Europe", "Asia", "North America"),
        ("Which country is famous for the Great Wall?", "China", "Japan", "India", "South Korea"),
        ("What is the capital of Germany?", "Berlin", "Munich", "Hamburg", "Frankfurt"),
        ("What is the capital of Russia?", "Moscow", "Saint Petersburg", "Kazan", "Sochi"),
        ("What is the capital of Nepal?", "Kathmandu", "Pokhara", "Thimphu", "Dhaka"),
        ("What is the capital of Bangladesh?", "Dhaka", "Chittagong", "Kathmandu", "Colombo"),
        ("What is the capital of Bhutan?", "Thimphu", "Paro", "Dhaka", "Male"),
        ("Which ocean is located between North America and Europe?", "Atlantic Ocean", "Indian Ocean", "Pacific Ocean", "Arctic Ocean"),
        ("Which continent contains the Sahara Desert?", "Africa", "Asia", "Australia", "Europe"),
        ("Which country is shaped like a boot?", "Italy", "Spain", "Greece", "Portugal"),
        ("What is the capital of Egypt?", "Cairo", "Alexandria", "Nairobi", "Rabat"),
        ("What is the capital of Thailand?", "Bangkok", "Hanoi", "Jakarta", "Manila"),
        ("Which country has the maple leaf on its national flag?", "Canada", "Australia", "New Zealand", "Switzerland"),
        ("What is the capital of the United States?", "Washington, D.C.", "New York City", "Los Angeles", "Chicago"),
        ("Which continent is Brazil located in?", "South America", "North America", "Africa", "Europe"),
        ("Which ocean surrounds the Maldives?", "Indian Ocean", "Pacific Ocean", "Atlantic Ocean", "Arctic Ocean"),
        ("What is the capital of South Korea?", "Seoul", "Busan", "Tokyo", "Pyongyang"),
        ("Which country is famous for the pyramids of Giza?", "Egypt", "Mexico", "Peru", "Greece"),
    ],

    "Medium": [
        ("Which is the largest country in the world by land area?", "Russia", "Canada", "China", "United States"),
        ("Which country has the largest population in the world according to recent estimates?", "India", "China", "United States", "Indonesia"),
        ("Which is the longest continental mountain range in the world?", "Andes", "Himalayas", "Rockies", "Alps"),
        ("Which river flows through Egypt?", "Nile", "Amazon", "Danube", "Yangtze"),
        ("Which is the largest hot desert in the world?", "Sahara Desert", "Gobi Desert", "Kalahari Desert", "Arabian Desert"),
        ("Which country is known as the Land of the Rising Sun?", "Japan", "China", "Thailand", "South Korea"),
        ("What is the capital of Switzerland?", "Bern", "Zurich", "Geneva", "Basel"),
        ("What is the capital of Turkey?", "Ankara", "Istanbul", "Izmir", "Antalya"),
        ("What is the capital of New Zealand?", "Wellington", "Auckland", "Christchurch", "Hamilton"),
        ("What is the capital of Argentina?", "Buenos Aires", "Santiago", "Lima", "Montevideo"),
        ("What is the capital of Kenya?", "Nairobi", "Mombasa", "Kampala", "Dodoma"),
        ("What is the capital of Nigeria?", "Abuja", "Lagos", "Kano", "Accra"),
        ("What is the capital of Vietnam?", "Hanoi", "Ho Chi Minh City", "Phnom Penh", "Vientiane"),
        ("What is the capital of Indonesia?", "Jakarta", "Bali", "Surabaya", "Bandung"),
        ("Which strait separates Asia from North America?", "Bering Strait", "Strait of Gibraltar", "Malacca Strait", "Bosporus Strait"),
        ("Which sea separates Europe and Africa?", "Mediterranean Sea", "Red Sea", "Black Sea", "Baltic Sea"),
        ("Which country is completely surrounded by South Africa?", "Lesotho", "Botswana", "Namibia", "Zimbabwe"),
        ("Which is the largest island in the world, excluding continents?", "Greenland", "Madagascar", "Borneo", "New Guinea"),
        ("Which mountain is the highest above sea level?", "Mount Everest", "K2", "Kangchenjunga", "Lhotse"),
        ("Which river is generally recognised as the longest river in South America?", "Amazon River", "Parana River", "Orinoco River", "Sao Francisco River"),
        ("Which country has the city of Marrakech?", "Morocco", "Algeria", "Tunisia", "Egypt"),
        ("What is the capital of Iceland?", "Reykjavik", "Oslo", "Helsinki", "Stockholm"),
        ("Which country has the capital city of Addis Ababa?", "Ethiopia", "Eritrea", "Somalia", "Sudan"),
        ("Which is the deepest ocean trench in the world?", "Mariana Trench", "Java Trench", "Puerto Rico Trench", "Tonga Trench"),
        ("Which country is home to the ancient city of Petra?", "Jordan", "Lebanon", "Syria", "Iraq"),
        ("Which continent has the greatest number of countries?", "Africa", "Asia", "Europe", "South America"),
        ("Which European country is famous for its fjords?", "Norway", "Poland", "Hungary", "Austria"),
        ("Which lake is commonly recognised as the world's deepest freshwater lake?", "Lake Baikal", "Lake Superior", "Lake Victoria", "Lake Tanganyika"),
        ("Which country has the capital city of Ulaanbaatar?", "Mongolia", "Kazakhstan", "Uzbekistan", "Kyrgyzstan"),
        ("Which country is home to the ancient city of Machu Picchu?", "Peru", "Chile", "Bolivia", "Ecuador"),
    ],

    "Hard": [
        ("Which is the world's largest inland body of water by surface area?", "Caspian Sea", "Lake Superior", "Lake Victoria", "Black Sea"),
        ("Which African country was formerly known as Abyssinia?", "Ethiopia", "Eritrea", "Sudan", "Somalia"),
        ("Which country has the longest coastline in the world?", "Canada", "Russia", "Australia", "Indonesia"),
        ("Which river crosses the Equator twice?", "Congo River", "Nile River", "Amazon River", "Zambezi River"),
        ("Which plateau is often called the Roof of the World?", "Tibetan Plateau", "Deccan Plateau", "Colorado Plateau", "Iranian Plateau"),
        ("Which mountain range traditionally forms part of the boundary between Europe and Asia?", "Ural Mountains", "Alps", "Andes", "Atlas Mountains"),
        ("Which country is home to the Atacama Desert?", "Chile", "Brazil", "Argentina", "Colombia"),
        ("Which desert is located mainly in Mongolia and northern China?", "Gobi Desert", "Sahara Desert", "Kalahari Desert", "Atacama Desert"),
        ("Which African lake is the largest by surface area?", "Lake Victoria", "Lake Tanganyika", "Lake Malawi", "Lake Chad"),
        ("Which river forms a large part of the border between the United States and Mexico?", "Rio Grande", "Colorado River", "Mississippi River", "Columbia River"),
        ("Which country has the capital city of Tbilisi?", "Georgia", "Armenia", "Azerbaijan", "Moldova"),
        ("What is the capital of Kazakhstan?", "Astana", "Almaty", "Tashkent", "Bishkek"),
        ("Which country has the capital city of Ljubljana?", "Slovenia", "Slovakia", "Croatia", "Serbia"),
        ("What is the capital of Uzbekistan?", "Tashkent", "Samarkand", "Bishkek", "Dushanbe"),
        ("Which country has the capital city of Podgorica?", "Montenegro", "North Macedonia", "Albania", "Bosnia and Herzegovina"),
        ("Which is the southernmost capital city of a sovereign country?", "Wellington", "Canberra", "Buenos Aires", "Cape Town"),
        ("Which channel separates Madagascar from mainland Africa?", "Mozambique Channel", "English Channel", "Bering Strait", "Suez Canal"),
        ("Which sea is bordered by Kazakhstan, Turkmenistan, Iran, Azerbaijan and Russia?", "Caspian Sea", "Aral Sea", "Black Sea", "Red Sea"),
        ("Which country contains the region of Transylvania?", "Romania", "Bulgaria", "Hungary", "Serbia"),
        ("Which river flows through Baghdad?", "Tigris", "Euphrates", "Jordan", "Indus"),
        ("Which two countries share the world's longest international land border?", "Canada and the United States", "Russia and China", "India and China", "Argentina and Chile"),
        ("Which country is home to the Okavango Delta?", "Botswana", "Namibia", "Zambia", "Angola"),
        ("Which African mountain is the highest peak on the continent?", "Mount Kilimanjaro", "Mount Kenya", "Mount Stanley", "Mount Meru"),
        ("Which country contains the ancient city of Timbuktu?", "Mali", "Niger", "Chad", "Senegal"),
        ("Which current is responsible for warming the climate of western Europe?", "North Atlantic Drift", "Labrador Current", "Canary Current", "Benguela Current"),
        ("Which is the largest peninsula in the world?", "Arabian Peninsula", "Indian Peninsula", "Iberian Peninsula", "Scandinavian Peninsula"),
        ("Which country is home to the Danakil Depression?", "Ethiopia", "South Africa", "Morocco", "Ghana"),
        ("Which strait connects the Persian Gulf with the Gulf of Oman?", "Strait of Hormuz", "Bab-el-Mandeb", "Strait of Malacca", "Dover Strait"),
        ("Which country has the capital city of Naypyidaw?", "Myanmar", "Laos", "Cambodia", "Thailand"),
        ("Which is the largest archipelagic country in the world by number of islands?", "Sweden", "Indonesia", "Philippines", "Japan"),
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
                "Explore continents, oceans, countries, capitals, mountains, rivers and important geographical features."
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
        print("GK TOPIC 9 INSERTED SUCCESSFULLY")
        print("World Geography")
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
