
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 186
LESSON_TITLE = "Indian States, National Parks, Wildlife Sanctuaries and Biosphere Reserves"
TOPIC = "General Knowledge"

BANK = {
    "Easy": [
        ("Which Indian national park is famous for Asiatic lions?", "Gir National Park", "Kaziranga National Park", "Jim Corbett National Park", "Kanha National Park"),
        ("Kaziranga National Park is located in which state?", "Assam", "Gujarat", "Rajasthan", "Karnataka"),
        ("Which animal is Kaziranga National Park especially famous for?", "One-horned rhinoceros", "Asiatic lion", "Snow leopard", "Wild buffalo"),
        ("Jim Corbett National Park is located in which state?", "Uttarakhand", "Madhya Pradesh", "Kerala", "Assam"),
        ("Which was India's first national park?", "Jim Corbett National Park", "Gir National Park", "Kanha National Park", "Ranthambore National Park"),
        ("Which national park is famous for Bengal tigers in Rajasthan?", "Ranthambore National Park", "Periyar National Park", "Silent Valley National Park", "Hemis National Park"),
        ("Which national park is located in Madhya Pradesh?", "Kanha National Park", "Sundarbans National Park", "Eravikulam National Park", "Dachigam National Park"),
        ("Which national park is famous for the one-horned rhinoceros and is located in Assam?", "Kaziranga National Park", "Gir National Park", "Bandipur National Park", "Pench National Park"),
        ("Which national park is located in the Sundarbans delta?", "Sundarbans National Park", "Hemis National Park", "Keoladeo National Park", "Valley of Flowers National Park"),
        ("Which animal is commonly associated with the Sundarbans?", "Royal Bengal tiger", "Asiatic lion", "Red panda", "Snow leopard"),
        ("Which national park is located in Kerala and is famous for elephants and tigers?", "Periyar National Park", "Gir National Park", "Desert National Park", "Hemis National Park"),
        ("Which national park is famous for the Nilgiri tahr?", "Eravikulam National Park", "Ranthambore National Park", "Kanha National Park", "Dudhwa National Park"),
        ("Which national park is located in Jammu and Kashmir and is famous for the hangul deer?", "Dachigam National Park", "Gir National Park", "Bandipur National Park", "Pench National Park"),
        ("Which national park is famous for the snow leopard?", "Hemis National Park", "Kaziranga National Park", "Keoladeo National Park", "Nagarhole National Park"),
        ("Hemis National Park is located in which Union Territory?", "Ladakh", "Delhi", "Puducherry", "Chandigarh"),
        ("Which national park in Madhya Pradesh is associated with the conservation of tigers?", "Bandhavgarh National Park", "Sundarbans National Park", "Dachigam National Park", "Hemis National Park"),
        ("Which national park is located in Karnataka?", "Bandipur National Park", "Gir National Park", "Kaziranga National Park", "Ranthambore National Park"),
        ("Which bird sanctuary in Rajasthan is famous for migratory birds?", "Keoladeo National Park", "Gir National Park", "Kanha National Park", "Periyar National Park"),
        ("Which national park is famous for the Valley of Flowers?", "Valley of Flowers National Park", "Desert National Park", "Pench National Park", "Dudhwa National Park"),
        ("Which Indian state is home to the Great Himalayan National Park?", "Himachal Pradesh", "Gujarat", "Tamil Nadu", "Odisha"),
        ("Which national park is located in the Thar Desert region?", "Desert National Park", "Silent Valley National Park", "Nagarhole National Park", "Eravikulam National Park"),
        ("Which animal is protected in the Indian Wild Ass Sanctuary?", "Indian wild ass", "Asiatic lion", "Snow leopard", "One-horned rhinoceros"),
        ("The Indian Wild Ass Sanctuary is located in which state?", "Gujarat", "Assam", "Kerala", "Punjab"),
        ("Which national park is famous for its population of wild elephants in Kerala?", "Periyar National Park", "Desert National Park", "Hemis National Park", "Keoladeo National Park"),
        ("Which national park is located in Odisha and is famous for saltwater crocodiles?", "Bhitarkanika National Park", "Gir National Park", "Kanha National Park", "Dachigam National Park"),
        ("Which animal is the national aquatic animal of India?", "Ganges river dolphin", "Blue whale", "Sea turtle", "Crocodile"),
        ("Which Indian state is famous for the Manas National Park?", "Assam", "Rajasthan", "Maharashtra", "Karnataka"),
        ("Which national park is located in West Bengal and is part of the Sundarbans ecosystem?", "Sundarbans National Park", "Bandipur National Park", "Kanha National Park", "Hemis National Park"),
        ("What is the main purpose of a national park?", "Protecting wildlife and natural ecosystems", "Promoting industrial development", "Expanding urban settlements", "Mining natural resources"),
        ("Which organisation is responsible for coordinating Project Tiger in India?", "National Tiger Conservation Authority", "Reserve Bank of India", "Election Commission of India", "University Grants Commission"),
    ],

    "Medium": [
        ("In which year was Project Tiger launched in India?", "1973", "1980", "1965", "1992"),
        ("Which was the first tiger reserve established under Project Tiger?", "Jim Corbett Tiger Reserve", "Sariska Tiger Reserve", "Bandipur Tiger Reserve", "Kanha Tiger Reserve"),
        ("Which biosphere reserve is shared by Tamil Nadu, Kerala and Karnataka?", "Nilgiri Biosphere Reserve", "Nanda Devi Biosphere Reserve", "Gulf of Mannar Biosphere Reserve", "Pachmarhi Biosphere Reserve"),
        ("Which was the first biosphere reserve established in India?", "Nilgiri Biosphere Reserve", "Sundarbans Biosphere Reserve", "Nanda Devi Biosphere Reserve", "Gulf of Kachchh Biosphere Reserve"),
        ("Which biosphere reserve is located in the Andaman and Nicobar Islands?", "Great Nicobar Biosphere Reserve", "Nilgiri Biosphere Reserve", "Pachmarhi Biosphere Reserve", "Achanakmar Biosphere Reserve"),
        ("Which national park is famous for the conservation of the Sangai deer?", "Keibul Lamjao National Park", "Gir National Park", "Kanha National Park", "Periyar National Park"),
        ("Keibul Lamjao National Park is located in which state?", "Manipur", "Assam", "Nagaland", "Mizoram"),
        ("Which national park is known for the conservation of the red panda in India?", "Singalila National Park", "Gir National Park", "Ranthambore National Park", "Desert National Park"),
        ("Which state is home to the Namdapha National Park?", "Arunachal Pradesh", "Gujarat", "Kerala", "Punjab"),
        ("Which national park is located in the Western Ghats and is known for its tropical evergreen forests?", "Silent Valley National Park", "Desert National Park", "Ranthambore National Park", "Dudhwa National Park"),
        ("Silent Valley National Park is located in which state?", "Kerala", "Rajasthan", "Assam", "Uttarakhand"),
        ("Which national park is famous for the barasingha conservation programme?", "Kanha National Park", "Gir National Park", "Hemis National Park", "Sundarbans National Park"),
        ("Which national park is located in Uttar Pradesh near the Indo-Nepal border?", "Dudhwa National Park", "Periyar National Park", "Eravikulam National Park", "Hemis National Park"),
        ("Which national park in Maharashtra is located near Mumbai?", "Sanjay Gandhi National Park", "Gir National Park", "Kanha National Park", "Kaziranga National Park"),
        ("Which national park is located in the state of Goa?", "Mollem National Park", "Bandipur National Park", "Dachigam National Park", "Kanha National Park"),
        ("Which national park is part of the Nilgiri Biosphere Reserve?", "Mudumalai National Park", "Desert National Park", "Sundarbans National Park", "Hemis National Park"),
        ("Which biosphere reserve in India is famous for its coral reefs and marine biodiversity?", "Gulf of Mannar Biosphere Reserve", "Pachmarhi Biosphere Reserve", "Nanda Devi Biosphere Reserve", "Cold Desert Biosphere Reserve"),
        ("Which biosphere reserve is located in Madhya Pradesh?", "Pachmarhi Biosphere Reserve", "Nilgiri Biosphere Reserve", "Great Nicobar Biosphere Reserve", "Similipal Biosphere Reserve"),
        ("Which biosphere reserve is located in Uttarakhand?", "Nanda Devi Biosphere Reserve", "Gulf of Mannar Biosphere Reserve", "Pachmarhi Biosphere Reserve", "Achanakmar Biosphere Reserve"),
        ("Which national park is located in the Great Rann of Kutch region?", "Desert National Park", "Marine National Park", "Kanha National Park", "Valley of Flowers National Park"),
        ("Which national park in Rajasthan is famous for its desert ecosystem and the great Indian bustard?", "Desert National Park", "Keoladeo National Park", "Ranthambore National Park", "Sariska National Park"),
        ("Which animal is the main focus of Project Snow Leopard?", "Snow leopard", "Asiatic lion", "One-horned rhinoceros", "Blackbuck"),
        ("Which national park is famous for the conservation of the lion-tailed macaque?", "Silent Valley National Park", "Gir National Park", "Desert National Park", "Keoladeo National Park"),
        ("Which protected area in Assam is a UNESCO World Heritage Site and a tiger reserve?", "Manas National Park", "Gir National Park", "Periyar National Park", "Dachigam National Park"),
        ("Which national park is located in the state of Sikkim?", "Khangchendzonga National Park", "Kanha National Park", "Bandipur National Park", "Ranthambore National Park"),
        ("Which biosphere reserve is located in Odisha and is known for its forests and wildlife?", "Similipal Biosphere Reserve", "Nilgiri Biosphere Reserve", "Pachmarhi Biosphere Reserve", "Great Nicobar Biosphere Reserve"),
        ("Which national park in Karnataka is also known as Rajiv Gandhi National Park?", "Nagarhole National Park", "Bandipur National Park", "Kudremukh National Park", "Anshi National Park"),
        ("Which national park is associated with the conservation of the Indian rhinoceros in Assam?", "Kaziranga National Park", "Gir National Park", "Sariska National Park", "Desert National Park"),
        ("What is the main purpose of a wildlife sanctuary?", "Protecting wild animals and their habitats", "Allowing unrestricted hunting", "Promoting large-scale mining", "Converting forests into cities"),
        ("Which international programme recognises important biosphere reserves worldwide?", "UNESCO Man and the Biosphere Programme", "World Trade Organization Programme", "International Monetary Fund Programme", "World Bank Development Programme"),
    ],

    "Hard": [
        ("Which Indian biosphere reserve was included in UNESCO's World Network of Biosphere Reserves in 2000?", "Nilgiri Biosphere Reserve", "Pachmarhi Biosphere Reserve", "Great Nicobar Biosphere Reserve", "Achanakmar Biosphere Reserve"),
        ("Which Indian biosphere reserve was added to UNESCO's World Network of Biosphere Reserves in 2009?", "Pachmarhi Biosphere Reserve", "Nilgiri Biosphere Reserve", "Similipal Biosphere Reserve", "Cold Desert Biosphere Reserve"),
        ("Which biosphere reserve was included in UNESCO's World Network in 2012?", "Achanakmar-Amarkantak Biosphere Reserve", "Gulf of Mannar Biosphere Reserve", "Nanda Devi Biosphere Reserve", "Nokrek Biosphere Reserve"),
        ("Which Indian biosphere reserve was recognised by UNESCO in 2013?", "Great Nicobar Biosphere Reserve", "Nilgiri Biosphere Reserve", "Pachmarhi Biosphere Reserve", "Similipal Biosphere Reserve"),
        ("Which biosphere reserve became part of UNESCO's World Network in 2020?", "Panna Biosphere Reserve", "Nanda Devi Biosphere Reserve", "Gulf of Mannar Biosphere Reserve", "Nokrek Biosphere Reserve"),
        ("Which biosphere reserve is located in Meghalaya and is associated with the western part of the state?", "Nokrek Biosphere Reserve", "Nilgiri Biosphere Reserve", "Pachmarhi Biosphere Reserve", "Great Nicobar Biosphere Reserve"),
        ("Which biosphere reserve is located in the cold desert region of Himachal Pradesh?", "Cold Desert Biosphere Reserve", "Nilgiri Biosphere Reserve", "Panna Biosphere Reserve", "Gulf of Mannar Biosphere Reserve"),
        ("Which national park forms part of the Nanda Devi Biosphere Reserve?", "Nanda Devi National Park", "Gir National Park", "Kanha National Park", "Kaziranga National Park"),
        ("Which national park is part of the Great Nicobar Biosphere Reserve?", "Campbell Bay National Park", "Bandipur National Park", "Kanha National Park", "Dudhwa National Park"),
        ("Which national park is located within the Gulf of Mannar region?", "Gulf of Mannar Marine National Park", "Hemis National Park", "Kanha National Park", "Ranthambore National Park"),
        ("Which national park in India is famous for its floating biomass ecosystem called phumdis?", "Keibul Lamjao National Park", "Kaziranga National Park", "Gir National Park", "Sariska National Park"),
        ("Which species is locally known as Sangai and is protected in Manipur?", "Eld's deer", "Hangul", "Nilgiri tahr", "Blackbuck"),
        ("Which protected area is famous for the conservation of the hangul or Kashmir stag?", "Dachigam National Park", "Gir National Park", "Bandipur National Park", "Periyar National Park"),
        ("Which national park is located in the eastern Himalayas and is known for exceptionally high biodiversity?", "Namdapha National Park", "Desert National Park", "Keoladeo National Park", "Sanjay Gandhi National Park"),
        ("Which national park is known for its high-altitude cold desert ecosystem in Ladakh?", "Hemis National Park", "Silent Valley National Park", "Kanha National Park", "Sundarbans National Park"),
        ("Which protected area is known for the conservation of the Asiatic wild ass?", "Indian Wild Ass Sanctuary", "Dachigam National Park", "Periyar Tiger Reserve", "Nanda Devi National Park"),
        ("Which national park is part of the Manas Biosphere Reserve?", "Manas National Park", "Gir National Park", "Kanha National Park", "Eravikulam National Park"),
        ("Which national park in West Bengal is known for its mangrove ecosystem and tidal waterways?", "Sundarbans National Park", "Desert National Park", "Kanha National Park", "Hemis National Park"),
        ("Which national park in Assam is located in the eastern Himalayan foothills and is known for its biodiversity?", "Namdapha National Park", "Gir National Park", "Ranthambore National Park", "Periyar National Park"),
        ("Which national park in Karnataka is known for its shola forests and montane grasslands?", "Kudremukh National Park", "Desert National Park", "Dachigam National Park", "Keoladeo National Park"),
        ("Which biosphere reserve includes parts of the Satpura, Maikal and Vindhya landscape?", "Pachmarhi Biosphere Reserve", "Nilgiri Biosphere Reserve", "Great Nicobar Biosphere Reserve", "Gulf of Mannar Biosphere Reserve"),
        ("Which biosphere reserve is located in the Western Ghats and includes parts of Kerala, Karnataka and Tamil Nadu?", "Nilgiri Biosphere Reserve", "Nanda Devi Biosphere Reserve", "Panna Biosphere Reserve", "Nokrek Biosphere Reserve"),
        ("Which national park is famous for the conservation of the great Indian bustard?", "Desert National Park", "Gir National Park", "Kaziranga National Park", "Dachigam National Park"),
        ("Which wildlife sanctuary in Maharashtra is famous for the conservation of the giant squirrel?", "Bhimashankar Wildlife Sanctuary", "Gir Wildlife Sanctuary", "Indian Wild Ass Sanctuary", "Vedanthangal Bird Sanctuary"),
        ("Which bird sanctuary in Tamil Nadu is among India's important heronries?", "Vedanthangal Bird Sanctuary", "Ranganathittu Bird Sanctuary", "Nal Sarovar Bird Sanctuary", "Sultanpur Bird Sanctuary"),
        ("Which bird sanctuary in Karnataka is located on the banks of the Kaveri River?", "Ranganathittu Bird Sanctuary", "Vedanthangal Bird Sanctuary", "Nal Sarovar Bird Sanctuary", "Sultanpur Bird Sanctuary"),
        ("Which protected area in Gujarat is particularly important for the conservation of the Asiatic lion?", "Gir Wildlife Sanctuary", "Dachigam National Park", "Manas National Park", "Periyar Wildlife Sanctuary"),
        ("Which national park in India is known for its population of the Nilgiri tahr?", "Eravikulam National Park", "Ranthambore National Park", "Sundarbans National Park", "Hemis National Park"),
        ("Which national park in Uttarakhand is famous for alpine flowers and high-altitude meadows?", "Valley of Flowers National Park", "Desert National Park", "Gir National Park", "Keoladeo National Park"),
        ("What are the three main zones of a biosphere reserve under UNESCO's model?", "Core, buffer and transition", "Urban, rural and industrial", "Mountain, river and desert", "Northern, southern and eastern"),
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
                    "MCQ lesson covering Indian national parks, "
                    "wildlife sanctuaries and biosphere reserves."
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
