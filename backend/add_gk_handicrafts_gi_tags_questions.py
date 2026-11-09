
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 182
LESSON_TITLE = "Indian Artisans, Handicrafts, GI Tags and Cultural Heritage"
TOPIC = "General Knowledge"

BANK = {
    "Easy": [
        ("Which Indian state is famous for Mysore silk?", "Karnataka", "Kerala", "Punjab", "Assam"),
        ("Pashmina shawls are traditionally associated with which region?", "Kashmir", "Rajasthan", "Bihar", "Goa"),
        ("Which state is famous for Madhubani paintings?", "Bihar", "Gujarat", "Karnataka", "Punjab"),
        ("Which Indian city is famous for blue pottery?", "Jaipur", "Mysuru", "Kochi", "Patna"),
        ("Banarasi silk sarees are associated with which city?", "Varanasi", "Surat", "Chennai", "Pune"),
        ("Which state is famous for Channapatna wooden toys?", "Karnataka", "Maharashtra", "Odisha", "Assam"),
        ("Warli painting is traditionally associated with which state?", "Maharashtra", "Tamil Nadu", "Haryana", "Sikkim"),
        ("Which state is famous for Pochampally Ikat textiles?", "Telangana", "Punjab", "Goa", "Himachal Pradesh"),
        ("Kanchipuram silk sarees originate from which state?", "Tamil Nadu", "Kerala", "Bihar", "Rajasthan"),
        ("Which state is famous for the traditional craft of Dhokra metal casting?", "West Bengal", "Punjab", "Haryana", "Goa"),
        ("Which Indian state is famous for the traditional craft of Pattachitra?", "Odisha", "Haryana", "Punjab", "Nagaland"),
        ("Phulkari embroidery is traditionally associated with which state?", "Punjab", "Kerala", "Assam", "Manipur"),
        ("Which state is famous for the traditional craft of blue pottery in Jaipur?", "Rajasthan", "Karnataka", "Bihar", "Tripura"),
        ("Which Indian state is known for its bamboo and cane handicrafts?", "Assam", "Punjab", "Goa", "Haryana"),
        ("What does GI stand for in the term GI Tag?", "Geographical Indication", "General Identification", "Global Industry", "Geographical Institute"),
        ("What does a Geographical Indication identify?", "A product linked to a specific geographical origin", "A product made only by machines", "A company's trademark", "A product's retail price"),
        ("Which Indian state is famous for the traditional craft of Kondapalli toys?", "Andhra Pradesh", "Kerala", "Punjab", "Meghalaya"),
        ("Which state is famous for Kullu shawls?", "Himachal Pradesh", "Gujarat", "Tamil Nadu", "Bihar"),
        ("Which Indian city is famous for Chikankari embroidery?", "Lucknow", "Jaipur", "Kochi", "Mysuru"),
        ("Which state is famous for the traditional craft of Bidriware?", "Karnataka", "Assam", "Punjab", "Odisha"),
        ("Which material is traditionally used to make many Indian terracotta crafts?", "Clay", "Glass", "Rubber", "Steel"),
        ("Which state is famous for the traditional craft of Rogan painting?", "Gujarat", "Kerala", "Punjab", "Manipur"),
        ("Which Indian state is associated with the craft of Sambalpuri textiles?", "Odisha", "Goa", "Haryana", "Sikkim"),
        ("Which state is famous for the traditional craft of Toda embroidery?", "Tamil Nadu", "Rajasthan", "Bihar", "Uttar Pradesh"),
        ("Which Indian state is known for the craft of Naga shawl weaving?", "Nagaland", "Gujarat", "Punjab", "Kerala"),
        ("Which city is famous for the traditional craft of Moradabad brassware?", "Moradabad", "Udaipur", "Kochi", "Madurai"),
        ("Which Indian state is associated with the craft of Thanjavur paintings?", "Tamil Nadu", "Maharashtra", "Assam", "Punjab"),
        ("Which state is famous for the traditional craft of Kasuti embroidery?", "Karnataka", "Bihar", "Goa", "Haryana"),
        ("Which state is associated with the traditional craft of Aranmula metal mirrors?", "Kerala", "Rajasthan", "Punjab", "Assam"),
        ("What is the main purpose of protecting traditional handicrafts?", "Preserving cultural heritage and livelihoods", "Replacing all handmade products", "Stopping traditional art", "Reducing cultural diversity"),
    ],

    "Medium": [
        ("Which organisation administers the Geographical Indications Registry in India?", "Office of the Controller General of Patents, Designs and Trade Marks", "Reserve Bank of India", "NITI Aayog", "Election Commission of India"),
        ("In which year did India's Geographical Indications of Goods Act come into force?", "2003", "1991", "2010", "2015"),
        ("Which international agreement contains provisions relating to geographical indications?", "TRIPS Agreement", "Kyoto Protocol", "Montreal Protocol", "Paris Climate Agreement"),
        ("Which Indian craft is known for intricate silver inlay work on a black metal alloy?", "Bidriware", "Blue pottery", "Warli painting", "Phulkari"),
        ("Which state is associated with the GI-tagged Kani shawls?", "Jammu and Kashmir", "Rajasthan", "Tamil Nadu", "West Bengal"),
        ("Which traditional art form from Odisha uses cloth or treated fabric as its painting surface?", "Pattachitra", "Warli", "Madhubani", "Kalamkari"),
        ("Which state is associated with the GI-tagged Mysore rosewood inlay work?", "Karnataka", "Gujarat", "Punjab", "Assam"),
        ("Which traditional textile technique involves tying and dyeing sections of yarn before weaving?", "Ikat", "Block printing", "Chikankari", "Zardozi"),
        ("Which state is famous for the GI-tagged Kutch embroidery?", "Gujarat", "Kerala", "Bihar", "Odisha"),
        ("Which traditional painting style is associated with the Mithila region?", "Madhubani", "Pattachitra", "Kalamkari", "Tanjore"),
        ("Which craft involves decorating fabric with metallic threads and decorative elements?", "Zardozi", "Warli", "Terracotta", "Blue pottery"),
        ("Which Indian state is associated with the GI-tagged Kashmir saffron?", "Jammu and Kashmir", "Rajasthan", "Madhya Pradesh", "Assam"),
        ("Which city is associated with the GI-tagged Kolhapuri chappals?", "Kolhapur", "Lucknow", "Jaipur", "Kochi"),
        ("Which state is famous for the traditional craft of Nirmal paintings and toys?", "Telangana", "Punjab", "Goa", "Himachal Pradesh"),
        ("Which traditional craft uses natural dyes and hand-carved wooden blocks to print fabric?", "Ajrakh printing", "Bidriware", "Dhokra casting", "Stone carving"),
        ("Which Indian state is associated with the GI-tagged Blue Pottery of Jaipur?", "Rajasthan", "Karnataka", "Assam", "Bihar"),
        ("Which craft tradition is associated with the use of lacquer on wooden objects in Channapatna?", "Lacquerware", "Stone carving", "Metal engraving", "Glass blowing"),
        ("Which state is associated with the traditional craft of Pipli appliqué work?", "Odisha", "Punjab", "Kerala", "Nagaland"),
        ("Which GI-tagged craft is associated with the town of Etikoppaka?", "Wooden toys", "Silk carpets", "Metal mirrors", "Stone jewellery"),
        ("Which state is associated with the traditional craft of Kashmir papier-mâché?", "Jammu and Kashmir", "Tamil Nadu", "Gujarat", "Meghalaya"),
        ("Which traditional craft of Rajasthan is known for its hand-block-printed textiles?", "Bagru printing", "Bidriware", "Toda embroidery", "Pattachitra"),
        ("Which Indian state is associated with the GI-tagged Kinnauri shawls?", "Himachal Pradesh", "Kerala", "Odisha", "West Bengal"),
        ("Which craft involves creating decorative designs by applying coloured thread to fabric?", "Embroidery", "Pottery", "Metal casting", "Wood turning"),
        ("Which state is associated with the GI-tagged Cheriyal scroll paintings?", "Telangana", "Rajasthan", "Bihar", "Punjab"),
        ("Which traditional craft is associated with the use of brass and bell metal in parts of India?", "Metal casting", "Paper folding", "Glass painting", "Stone polishing"),
        ("Which Indian state is famous for the traditional craft of Kalamkari?", "Andhra Pradesh", "Haryana", "Sikkim", "Punjab"),
        ("What is the primary objective of a GI tag for traditional products?", "To protect products associated with a specific region", "To grant patents to all manufacturers", "To set a fixed retail price", "To certify imported goods"),
        ("Which traditional art form is associated with the tribal communities of Maharashtra?", "Warli painting", "Kalamkari", "Pattachitra", "Tanjore painting"),
        ("Which Indian state is associated with the GI-tagged Muga silk?", "Assam", "Punjab", "Gujarat", "Rajasthan"),
        ("Which craft is traditionally associated with the town of Kutch in Gujarat?", "Ajrakh block printing", "Channapatna toy making", "Bidriware", "Kanchipuram silk weaving"),
    ],

    "Hard": [
        ("Which Indian law provides the statutory framework for registering and protecting geographical indications?", "Geographical Indications of Goods (Registration and Protection) Act, 1999", "Copyright Act, 1957", "Patents Act, 1970", "Trade Marks Act, 1999"),
        ("Where is the Geographical Indications Registry of India located?", "Chennai", "New Delhi", "Mumbai", "Kolkata"),
        ("Which international organisation administers the Lisbon System for appellations of origin and geographical indications?", "World Intellectual Property Organization", "World Trade Organization", "UNESCO", "International Labour Organization"),
        ("Under India's GI law, for how long is a registered GI initially valid?", "10 years", "5 years", "15 years", "20 years"),
        ("Can the registration of a geographical indication in India be renewed?", "Yes, for further periods of 10 years", "No, it cannot be renewed", "Only once for 5 years", "Only after 25 years"),
        ("Which of the following best describes a geographical indication?", "A sign identifying goods as originating from a place where a quality or reputation is linked to that origin", "A patent for a new machine", "A trademark owned by one individual only", "A copyright for a literary work"),
        ("Which traditional Indian textile is associated with the double-ikat weaving technique?", "Pochampally Ikat", "Chikankari", "Phulkari", "Kashmir papier-mâché"),
        ("Which state is associated with the GI-tagged Kotpad handloom fabric?", "Odisha", "Gujarat", "Kerala", "Punjab"),
        ("Which Indian craft is known for using a distinctive red and black natural dye tradition in parts of Andhra Pradesh?", "Kalamkari", "Blue pottery", "Bidriware", "Warli painting"),
        ("Which GI-tagged craft is associated with the village of Sualkuchi?", "Assam silk textiles", "Kashmir carpets", "Rajasthan pottery", "Karnataka wooden toys"),
        ("Which traditional craft is associated with the use of a special alloy and silver inlay in Bidar?", "Bidriware", "Dhokra", "Pattachitra", "Ajrakh"),
        ("Which Indian state is associated with the GI-tagged Bastar Dhokra craft?", "Chhattisgarh", "Punjab", "Kerala", "Haryana"),
        ("Which traditional Indian craft uses lost-wax casting to create metal objects?", "Dhokra", "Chikankari", "Madhubani", "Bagru printing"),
        ("Which Indian state is associated with the GI-tagged Aranmula Kannadi?", "Kerala", "Gujarat", "Assam", "Rajasthan"),
        ("What makes the Aranmula Kannadi distinct from an ordinary glass mirror?", "It is a handmade metal-alloy mirror", "It is made entirely of wood", "It uses polished ceramic only", "It is made from woven silk"),
        ("Which Indian state is associated with the GI-tagged Thanjavur art plate?", "Tamil Nadu", "Bihar", "Punjab", "Himachal Pradesh"),
        ("Which craft is associated with the traditional wooden toys of Varanasi?", "Wooden lacquerware toys", "Metal mirror making", "Stone inlay work", "Silk carpet weaving"),
        ("Which GI-tagged textile is traditionally associated with the town of Chanderi?", "Chanderi fabric", "Kullu shawl", "Muga silk", "Kota Doria"),
        ("Which Indian state is associated with the GI-tagged Kota Doria textile?", "Rajasthan", "Assam", "Kerala", "Nagaland"),
        ("Which state is associated with the GI-tagged Paithani saree?", "Maharashtra", "Odisha", "Punjab", "Meghalaya"),
        ("Which Indian state is associated with the GI-tagged Baluchari saree?", "West Bengal", "Gujarat", "Karnataka", "Haryana"),
        ("Which craft is associated with the traditional metalwork of Pembarthi?", "Brass sheet metal craft", "Silk embroidery", "Wooden toy making", "Stone pottery"),
        ("Which Indian state is associated with the GI-tagged Pembarthi Metal Craft?", "Telangana", "Punjab", "Kerala", "Goa"),
        ("Which traditional art form from Andhra Pradesh is known for painted cloth panels and storytelling?", "Kalamkari", "Warli", "Phulkari", "Blue pottery"),
        ("Which GI-tagged craft is associated with the town of Molela in Rajasthan?", "Terracotta plaques", "Silk weaving", "Metal mirrors", "Bamboo baskets"),
        ("Which Indian state is associated with the GI-tagged Ganjifa cards of Mysore?", "Karnataka", "Assam", "Bihar", "Punjab"),
        ("Which traditional craft is associated with the wooden toys of Kondapalli?", "Andhra Pradesh toy making", "Kashmir carpet weaving", "Rajasthan blue pottery", "Odisha palm-leaf engraving"),
        ("Which organisation maintains the international system for classifying and registering appellations of origin under the Lisbon Agreement?", "WIPO", "UNESCO", "WTO", "FAO"),
        ("What is the key difference between a GI and an individual trademark?", "A GI identifies products linked to a geographical origin, while a trademark distinguishes commercial sources", "A GI protects inventions, while a trademark protects books", "A GI applies only to imported goods", "A trademark can only be used by governments"),
        ("Which Indian state is associated with the GI-tagged Naga tree tomato?", "Nagaland", "Gujarat", "Tamil Nadu", "Rajasthan"),
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
                    "MCQ lesson covering Indian artisans, handicrafts, "
                    "geographical indications and cultural heritage."
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

                # FIXED: Seven placeholders and seven supplied values.
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
