
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 200
LESSON_TITLE = "World Geography, Oceans, Mountains, Deserts, Natural Wonders and Physical Features"
TOPIC = "General Knowledge"

BANK = {
    "Easy": [
        ("Which is the largest ocean in the world?", "Pacific Ocean", "Atlantic Ocean", "Indian Ocean", "Arctic Ocean"),
        ("Which is the smallest ocean in the world?", "Arctic Ocean", "Indian Ocean", "Atlantic Ocean", "Pacific Ocean"),
        ("Which is the highest mountain in the world above sea level?", "Mount Everest", "K2", "Kangchenjunga", "Mount Kilimanjaro"),
        ("Which is the largest continent by area?", "Asia", "Africa", "Europe", "North America"),
        ("Which is the smallest continent by area?", "Australia", "Europe", "Antarctica", "South America"),
        ("Which is the largest hot desert in the world?", "Sahara Desert", "Gobi Desert", "Kalahari Desert", "Arabian Desert"),
        ("Which river is commonly recognised as the longest river in Africa?", "Nile", "Congo", "Niger", "Zambezi"),
        ("Which is the largest rainforest in the world?", "Amazon Rainforest", "Congo Rainforest", "Daintree Rainforest", "Sundarbans"),
        ("Which country is home to Mount Fuji?", "Japan", "China", "South Korea", "Nepal"),
        ("Which mountain range separates Europe from Asia in a commonly used geographical boundary?", "Ural Mountains", "Alps", "Andes", "Rocky Mountains"),
        ("Which is the deepest ocean trench in the world?", "Mariana Trench", "Tonga Trench", "Java Trench", "Puerto Rico Trench"),
        ("Which continent contains the Sahara Desert?", "Africa", "Asia", "Australia", "South America"),
        ("Which ocean lies between Africa and Australia?", "Indian Ocean", "Atlantic Ocean", "Arctic Ocean", "Southern Ocean"),
        ("Which is the largest island in the world, excluding continental landmasses?", "Greenland", "Madagascar", "Borneo", "New Guinea"),
        ("Which country is famous for the Great Barrier Reef?", "Australia", "Indonesia", "Philippines", "South Africa"),
        ("Which waterfall is located on the border of Zambia and Zimbabwe?", "Victoria Falls", "Niagara Falls", "Angel Falls", "Iguazu Falls"),
        ("Which is the highest waterfall in the world?", "Angel Falls", "Victoria Falls", "Niagara Falls", "Yosemite Falls"),
        ("Which mountain range runs along the western edge of South America?", "Andes", "Alps", "Himalayas", "Rockies"),
        ("Which sea separates Europe and Africa?", "Mediterranean Sea", "Caribbean Sea", "Arabian Sea", "Bering Sea"),
        ("Which is the largest lake in the world by surface area?", "Caspian Sea", "Lake Superior", "Lake Victoria", "Lake Baikal"),
        ("Which is the deepest freshwater lake in the world?", "Lake Baikal", "Lake Superior", "Lake Victoria", "Lake Tanganyika"),
        ("Which continent is covered largely by ice and has no permanent native human population?", "Antarctica", "Europe", "Africa", "Australia"),
        ("Which strait separates Asia from North America?", "Bering Strait", "Strait of Gibraltar", "Malacca Strait", "Dover Strait"),
        ("Which country contains the famous Grand Canyon?", "United States", "Canada", "Mexico", "Brazil"),
        ("Which desert is located mainly in Mongolia and northern China?", "Gobi Desert", "Sahara Desert", "Atacama Desert", "Kalahari Desert"),
        ("Which is the largest country in the world by area?", "Russia", "Canada", "China", "United States"),
        ("Which is the smallest independent country in the world by area?", "Vatican City", "Monaco", "San Marino", "Liechtenstein"),
        ("Which ocean surrounds the North Pole?", "Arctic Ocean", "Southern Ocean", "Indian Ocean", "Atlantic Ocean"),
        ("Which famous mountain is located in Tanzania?", "Mount Kilimanjaro", "Mount Elbrus", "Mount Fuji", "Mount Blanc"),
        ("Which river flows through Egypt and empties into the Mediterranean Sea?", "Nile", "Amazon", "Danube", "Mississippi"),
    ],

    "Medium": [
        ("Which is the longest continental mountain range in the world?", "Andes", "Rocky Mountains", "Himalayas", "Alps"),
        ("Which is the largest peninsula in the world?", "Arabian Peninsula", "Indian Peninsula", "Iberian Peninsula", "Scandinavian Peninsula"),
        ("Which is the largest gulf in the world?", "Gulf of Mexico", "Persian Gulf", "Gulf of California", "Gulf of Aden"),
        ("Which river has the largest drainage basin in the world?", "Amazon River", "Nile River", "Yangtze River", "Mississippi River"),
        ("Which river flows through the Grand Canyon?", "Colorado River", "Mississippi River", "Columbia River", "Rio Grande"),
        ("Which desert is considered the driest non-polar desert in the world?", "Atacama Desert", "Sahara Desert", "Gobi Desert", "Kalahari Desert"),
        ("Which is the largest peninsula in Europe?", "Scandinavian Peninsula", "Iberian Peninsula", "Balkan Peninsula", "Italian Peninsula"),
        ("Which mountain range contains Mont Blanc?", "Alps", "Andes", "Pyrenees", "Carpathians"),
        ("Which country is home to the fjords of Geiranger and Sognefjord?", "Norway", "Sweden", "Finland", "Iceland"),
        ("Which plateau is commonly known as the Roof of the World?", "Tibetan Plateau", "Deccan Plateau", "Colorado Plateau", "Iranian Plateau"),
        ("Which lake is shared by Tanzania, Uganda and Kenya?", "Lake Victoria", "Lake Baikal", "Lake Superior", "Lake Titicaca"),
        ("Which African lake is the source of the White Nile through its outlet at Jinja?", "Lake Victoria", "Lake Chad", "Lake Malawi", "Lake Tanganyika"),
        ("Which river forms much of the border between the United States and Mexico?", "Rio Grande", "Colorado River", "Missouri River", "Yukon River"),
        ("Which sea is known for its extremely high salinity and lies between Jordan and Israel and the West Bank?", "Dead Sea", "Red Sea", "Black Sea", "Caspian Sea"),
        ("Which is the world's largest coral reef system?", "Great Barrier Reef", "Belize Barrier Reef", "New Caledonia Barrier Reef", "Red Sea Coral Reef"),
        ("Which country contains the Danakil Depression?", "Ethiopia", "Kenya", "Nigeria", "Morocco"),
        ("Which mountain is the highest peak in Africa?", "Mount Kilimanjaro", "Mount Kenya", "Mount Stanley", "Mount Meru"),
        ("Which mountain is the highest peak in Europe under the commonly used Caucasus boundary definition?", "Mount Elbrus", "Mont Blanc", "Matterhorn", "Mount Olympus"),
        ("Which is the largest island in the Mediterranean Sea?", "Sicily", "Crete", "Cyprus", "Sardinia"),
        ("Which river flows through Budapest?", "Danube", "Rhine", "Seine", "Thames"),
        ("Which river flows through Paris?", "Seine", "Rhine", "Danube", "Loire"),
        ("Which river flows through London?", "Thames", "Seine", "Elbe", "Tiber"),
        ("Which ocean current is associated with warming the climate of western Europe?", "North Atlantic Drift", "Labrador Current", "Peru Current", "Benguela Current"),
        ("Which current flows northward along the western coast of South America?", "Humboldt Current", "Gulf Stream", "Kuroshio Current", "Agulhas Current"),
        ("Which desert is located along the southwestern coast of Africa?", "Namib Desert", "Sahara Desert", "Gobi Desert", "Thar Desert"),
        ("Which country contains the Salar de Uyuni salt flat?", "Bolivia", "Chile", "Peru", "Argentina"),
        ("Which mountain range separates France and Spain?", "Pyrenees", "Alps", "Carpathians", "Apennines"),
        ("Which strait connects the Mediterranean Sea with the Atlantic Ocean?", "Strait of Gibraltar", "Bering Strait", "Bosporus Strait", "Malacca Strait"),
        ("Which waterway connects the Mediterranean Sea and the Red Sea?", "Suez Canal", "Panama Canal", "Kiel Canal", "Corinth Canal"),
        ("Which waterway connects the Atlantic and Pacific oceans through Central America?", "Panama Canal", "Suez Canal", "Kiel Canal", "Erie Canal"),
    ],

    "Hard": [
        ("Which is the deepest known point in the world's oceans?", "Challenger Deep", "Horizon Deep", "Milwaukee Deep", "Brownson Deep"),
        ("Which tectonic plate is primarily responsible for the formation of the Himalayas through its collision with the Eurasian Plate?", "Indian Plate", "African Plate", "Pacific Plate", "Nazca Plate"),
        ("Which mountain range is traditionally regarded as the boundary between France and Spain?", "Pyrenees", "Alps", "Apennines", "Carpathians"),
        ("Which river flows through the largest number of countries in Europe?", "Danube", "Rhine", "Volga", "Seine"),
        ("Which is the longest river entirely within Europe?", "Volga", "Danube", "Rhine", "Dnieper"),
        ("Which river is the longest in Asia?", "Yangtze", "Yellow River", "Mekong", "Ganges"),
        ("Which African river crosses the Equator twice?", "Congo River", "Nile River", "Niger River", "Zambezi River"),
        ("Which desert is located in the rain shadow of the Andes in Argentina?", "Patagonian Desert", "Atacama Desert", "Sechura Desert", "Monte Desert"),
        ("Which is the world's largest endorheic basin by area?", "Caspian Sea basin", "Lake Baikal basin", "Lake Victoria basin", "Dead Sea basin"),
        ("Which lake is located at the highest elevation among the world's large navigable lakes?", "Lake Titicaca", "Lake Victoria", "Lake Superior", "Lake Tanganyika"),
        ("Which mountain is the highest peak in the Alps?", "Mont Blanc", "Matterhorn", "Dufourspitze", "Jungfrau"),
        ("Which mountain range contains Aconcagua, the highest peak outside Asia?", "Andes", "Rockies", "Alps", "Himalayas"),
        ("Which country contains the Danube Delta, where the river meets the Black Sea?", "Romania", "Germany", "Austria", "Hungary"),
        ("Which strait connects the Black Sea with the Sea of Marmara?", "Bosporus Strait", "Dardanelles Strait", "Strait of Gibraltar", "Kerch Strait"),
        ("Which strait connects the Sea of Marmara with the Aegean Sea?", "Dardanelles Strait", "Bosporus Strait", "Bering Strait", "Dover Strait"),
        ("Which sea is connected to the Atlantic Ocean through the Strait of Gibraltar?", "Mediterranean Sea", "Black Sea", "Baltic Sea", "Red Sea"),
        ("Which current is a cold ocean current flowing northward along the western coast of southern Africa?", "Benguela Current", "Agulhas Current", "Kuroshio Current", "Brazil Current"),
        ("Which current is a warm western boundary current in the North Atlantic Ocean?", "Gulf Stream", "Labrador Current", "Canary Current", "California Current"),
        ("Which ocean current flows northward along the eastern coast of Japan?", "Kuroshio Current", "Oyashio Current", "Humboldt Current", "Benguela Current"),
        ("Which geological feature is formed where two continental plates collide?", "Fold mountains", "Mid-ocean ridge", "Ocean trench", "Rift valley"),
        ("Which type of plate boundary is associated with the formation of the Mid-Atlantic Ridge?", "Divergent boundary", "Convergent boundary", "Transform boundary", "Collision boundary"),
        ("Which valley in East Africa is part of a major tectonic rift system?", "Great Rift Valley", "Death Valley", "Napa Valley", "Rhine Valley"),
        ("Which country contains the Okavango Delta?", "Botswana", "Namibia", "Angola", "Zambia"),
        ("Which river forms the spectacular Iguazu Falls on the border region of Argentina and Brazil?", "Iguazu River", "Paraná River", "Amazon River", "Uruguay River"),
        ("Which island is the largest in the Indonesian archipelago by area?", "New Guinea", "Java", "Sumatra", "Sulawesi"),
        ("Which is the largest archipelago country in the world by number of islands, according to commonly cited national counts?", "Sweden", "Indonesia", "Japan", "Philippines"),
        ("Which mountain range is located between the Black Sea and the Caspian Sea?", "Caucasus Mountains", "Ural Mountains", "Alps", "Carpathians"),
        ("Which plateau is located mainly in western China and is known for its high elevation and extensive desert landscapes?", "Tibetan Plateau", "Deccan Plateau", "Brazilian Plateau", "Anatolian Plateau"),
        ("Which is the largest freshwater island in the world by area?", "Manitoulin Island", "Victoria Island", "Madagascar", "Baffin Island"),
        ("Which ocean basin contains the Ring of Fire?", "Pacific Ocean", "Atlantic Ocean", "Indian Ocean", "Arctic Ocean"),
    ]
}


def validate_bank():
    print("\nValidating question bank...")

    for difficulty in ("Easy", "Medium", "Hard"):
        questions = BANK[difficulty]
        print(f"{difficulty}: {len(questions)}/30")

        if len(questions) != 30:
            raise ValueError(
                f"{difficulty} must contain exactly 30 questions; "
                f"found {len(questions)}"
            )

        for index, item in enumerate(questions, start=1):
            if len(item) != 5:
                raise ValueError(
                    f"{difficulty} question {index} must contain 5 values."
                )

            if not all(isinstance(value, str) and value.strip() for value in item):
                raise ValueError(
                    f"Invalid or empty value in {difficulty} question {index}."
                )

            if len(set(item[1:])) != 4:
                raise ValueError(
                    f"Duplicate options in {difficulty} question {index}."
                )

    print("Validation successful: exactly 90 questions.")


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
                    "World geography, oceans, mountains, deserts, "
                    "natural wonders and physical features."
                )
            )
            print("Lesson created.")

        elif lesson != (LESSON_TITLE, TOPIC):
            raise ValueError(
                f"Lesson ID {LESSON_ID} already belongs to another lesson: {lesson}"
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
            else:
                quiz_id = quiz[0]

            cursor.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                (quiz_id,)
            )
            existing_count = cursor.fetchone()[0]

            if existing_count > 30:
                raise ValueError(
                    f"{difficulty} quiz already has {existing_count} questions."
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
                    f"{difficulty} quiz has {final_count} questions instead of 30."
                )

            print(f"{difficulty}: {final_count}/30 questions")

        connection.commit()

        print("\nSUCCESS!")
        print(f"Lesson ID: {LESSON_ID}")
        print(f"Lesson: {LESSON_TITLE}")
        print("Easy: 30 questions")
        print("Medium: 30 questions")
        print("Hard: 30 questions")
        print("Total: 90 questions.")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
