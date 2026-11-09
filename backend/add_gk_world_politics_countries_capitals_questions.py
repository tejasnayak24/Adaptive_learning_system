
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 197
LESSON_TITLE = "World Politics, Countries, Capitals, Currencies and International Relations"
TOPIC = "General Knowledge"

BANK = {
    "Easy": [
        ("What is the capital of France?", "Paris", "Rome", "Berlin", "Madrid"),
        ("What is the capital of Japan?", "Tokyo", "Seoul", "Beijing", "Bangkok"),
        ("What is the capital of Australia?", "Canberra", "Sydney", "Melbourne", "Perth"),
        ("What is the capital of Canada?", "Ottawa", "Toronto", "Vancouver", "Montreal"),
        ("What is the capital of Germany?", "Berlin", "Munich", "Hamburg", "Frankfurt"),
        ("What is the capital of Italy?", "Rome", "Venice", "Milan", "Florence"),
        ("What is the capital of China?", "Beijing", "Shanghai", "Hong Kong", "Wuhan"),
        ("What is the capital of Russia?", "Moscow", "Saint Petersburg", "Kazan", "Sochi"),
        ("What is the capital of Nepal?", "Kathmandu", "Pokhara", "Lalitpur", "Biratnagar"),
        ("What is the capital of Bangladesh?", "Dhaka", "Chittagong", "Khulna", "Sylhet"),
        ("What is the currency of Japan?", "Yen", "Won", "Yuan", "Baht"),
        ("What is the currency of the United States?", "US Dollar", "Euro", "Pound Sterling", "Franc"),
        ("What is the currency of the United Kingdom?", "Pound Sterling", "Euro", "Dollar", "Krona"),
        ("What is the currency of China?", "Renminbi", "Yen", "Won", "Rupee"),
        ("What is the currency of Bangladesh?", "Taka", "Rupee", "Riyal", "Dinar"),
        ("Which organisation was established in 1945 to promote international peace and cooperation?", "United Nations", "NATO", "ASEAN", "OPEC"),
        ("Where is the headquarters of the United Nations located?", "New York", "London", "Paris", "Geneva"),
        ("Which organisation is primarily concerned with global public health?", "World Health Organization", "World Trade Organization", "International Monetary Fund", "UNESCO"),
        ("Where is the headquarters of the World Health Organization?", "Geneva", "New York", "Rome", "Vienna"),
        ("Which organisation promotes international trade rules?", "World Trade Organization", "World Health Organization", "UNICEF", "NATO"),
        ("What does NATO stand for?", "North Atlantic Treaty Organization", "National Asian Trade Organization", "North American Tourism Organization", "New Atlantic Trade Organisation"),
        ("Which country is known as the Land of the Rising Sun?", "Japan", "China", "Thailand", "South Korea"),
        ("Which country has the largest population in the world according to recent estimates?", "India", "United States", "Russia", "Japan"),
        ("Which country is famous for the pyramids of Giza?", "Egypt", "Greece", "Mexico", "Turkey"),
        ("What is the capital of South Korea?", "Seoul", "Busan", "Incheon", "Daegu"),
        ("What is the capital of Thailand?", "Bangkok", "Phuket", "Chiang Mai", "Pattaya"),
        ("What is the capital of Saudi Arabia?", "Riyadh", "Jeddah", "Mecca", "Medina"),
        ("What is the capital of Brazil?", "Brasilia", "Rio de Janeiro", "Sao Paulo", "Salvador"),
        ("Which country is home to the city of Istanbul?", "Turkey", "Greece", "Iran", "Egypt"),
        ("Which international organisation works to protect children's rights and welfare?", "UNICEF", "IMF", "WTO", "OPEC"),
    ],

    "Medium": [
        ("What is the capital of Switzerland?", "Bern", "Zurich", "Geneva", "Basel"),
        ("What is the capital of New Zealand?", "Wellington", "Auckland", "Christchurch", "Hamilton"),
        ("What is the capital of Turkey?", "Ankara", "Istanbul", "Izmir", "Antalya"),
        ("What is the capital of Kazakhstan?", "Astana", "Almaty", "Shymkent", "Aktobe"),
        ("What is the capital of Nigeria?", "Abuja", "Lagos", "Kano", "Ibadan"),
        ("What is the capital of Morocco?", "Rabat", "Casablanca", "Marrakesh", "Tangier"),
        ("What is the capital of Argentina?", "Buenos Aires", "Cordoba", "Rosario", "Mendoza"),
        ("What is the capital of Norway?", "Oslo", "Bergen", "Trondheim", "Stavanger"),
        ("What is the capital of Sweden?", "Stockholm", "Gothenburg", "Malmo", "Uppsala"),
        ("What is the capital of Vietnam?", "Hanoi", "Ho Chi Minh City", "Da Nang", "Hue"),
        ("What is the currency of Switzerland?", "Swiss Franc", "Euro", "Krone", "Pound"),
        ("What is the currency of South Korea?", "Won", "Yen", "Yuan", "Baht"),
        ("What is the currency of South Africa?", "Rand", "Naira", "Cedi", "Shilling"),
        ("What is the currency of Russia?", "Ruble", "Euro", "Lira", "Dinar"),
        ("What is the currency of Saudi Arabia?", "Saudi Riyal", "Dirham", "Dinar", "Pound"),
        ("Where is the headquarters of the International Monetary Fund?", "Washington, D.C.", "Geneva", "New York", "Paris"),
        ("Where is the headquarters of the World Trade Organization?", "Geneva", "Washington, D.C.", "London", "Brussels"),
        ("Which organisation provides financial assistance and development loans to countries?", "World Bank", "WHO", "UNESCO", "INTERPOL"),
        ("Which organisation is responsible for international civil aviation standards?", "International Civil Aviation Organization", "International Labour Organization", "World Health Organization", "World Trade Organization"),
        ("Where is the headquarters of UNESCO?", "Paris", "Rome", "Geneva", "Vienna"),
        ("Which group includes Brazil, Russia, India, China and South Africa among its founding members?", "BRICS", "G7", "NATO", "ASEAN"),
        ("Which organisation promotes regional cooperation among Southeast Asian countries?", "ASEAN", "SAARC", "NATO", "OPEC"),
        ("Which regional organisation was established in 1985 to promote cooperation in South Asia?", "SAARC", "ASEAN", "European Union", "African Union"),
        ("Which organisation is primarily associated with cooperation among major oil-exporting countries?", "OPEC", "WTO", "UNESCO", "NATO"),
        ("Which country has the capital city of Addis Ababa?", "Ethiopia", "Kenya", "Uganda", "Tanzania"),
        ("Which country has the capital city of Buenos Aires?", "Argentina", "Chile", "Peru", "Uruguay"),
        ("Which country has the capital city of Helsinki?", "Finland", "Sweden", "Norway", "Denmark"),
        ("Which country has the capital city of Lisbon?", "Portugal", "Spain", "Greece", "Austria"),
        ("Which country has the capital city of Doha?", "Qatar", "Kuwait", "Oman", "Bahrain"),
        ("Which country has the capital city of Reykjavik?", "Iceland", "Ireland", "Norway", "Finland"),
    ],

    "Hard": [
        ("Which treaty formally established the European Union in 1993?", "Maastricht Treaty", "Treaty of Rome", "Treaty of Lisbon", "Treaty of Paris"),
        ("Which agreement established the European Economic Community in 1957?", "Treaty of Rome", "Maastricht Treaty", "Treaty of Versailles", "Treaty of Utrecht"),
        ("Which city hosts the International Court of Justice?", "The Hague", "Geneva", "Brussels", "Vienna"),
        ("Which principal organ of the United Nations has primary responsibility for international peace and security?", "Security Council", "General Assembly", "Economic and Social Council", "Secretariat"),
        ("How many permanent members are there in the UN Security Council?", "Five", "Four", "Six", "Ten"),
        ("Which of these is a permanent member of the UN Security Council?", "France", "Germany", "Japan", "India"),
        ("Which UN agency is responsible for international labour standards?", "International Labour Organization", "UNICEF", "UNESCO", "World Bank"),
        ("Where is the headquarters of the International Labour Organization?", "Geneva", "Paris", "New York", "Rome"),
        ("Which organisation was created by the Bretton Woods Conference in 1944?", "International Monetary Fund", "NATO", "ASEAN", "African Union"),
        ("Which agreement established the World Trade Organization in 1995?", "Marrakesh Agreement", "Maastricht Treaty", "Treaty of Rome", "Geneva Convention"),
        ("Which organisation administers the international system of intellectual property protection?", "World Intellectual Property Organization", "World Trade Organization", "International Labour Organization", "UNICEF"),
        ("Where is the headquarters of the International Atomic Energy Agency?", "Vienna", "Geneva", "Paris", "New York"),
        ("Which organisation was established through the Treaty of Brussels in 1948 as a European defence cooperation arrangement?", "Western Union", "European Union", "NATO", "Council of Europe"),
        ("Which declaration adopted in 1948 sets out fundamental human rights?", "Universal Declaration of Human Rights", "Geneva Convention of 1864", "Atlantic Charter", "Helsinki Final Act"),
        ("Which international convention of 1951 primarily deals with the status and protection of refugees?", "Refugee Convention", "Vienna Convention", "Montreal Convention", "Ramsar Convention"),
        ("Which organisation replaced the Organisation of African Unity in 2002?", "African Union", "Arab League", "Commonwealth", "European Union"),
        ("Which treaty created the Association of Southeast Asian Nations in 1967?", "Bangkok Declaration", "Manila Treaty", "Treaty of Rome", "Jakarta Agreement"),
        ("Which country hosted the first summit of the Non-Aligned Movement in 1961?", "Yugoslavia", "India", "Egypt", "Indonesia"),
        ("Which city hosted the first summit of the Non-Aligned Movement?", "Belgrade", "Cairo", "New Delhi", "Jakarta"),
        ("Which international agreement established the framework for the European single market?", "Single European Act", "Treaty of Versailles", "Treaty of Tordesillas", "Treaty of Utrecht"),
        ("Which country is not a member of the G7?", "China", "Japan", "Canada", "Italy"),
        ("Which country is associated with the capital city of Naypyidaw?", "Myanmar", "Cambodia", "Laos", "Thailand"),
        ("Which country has the capital city of Tbilisi?", "Georgia", "Armenia", "Azerbaijan", "Moldova"),
        ("Which country has the capital city of Ljubljana?", "Slovenia", "Slovakia", "Croatia", "Serbia"),
        ("Which country has the capital city of Podgorica?", "Montenegro", "North Macedonia", "Albania", "Bosnia and Herzegovina"),
        ("Which country has the capital city of Thimphu?", "Bhutan", "Nepal", "Maldives", "Sri Lanka"),
        ("Which country has the capital city of Bandar Seri Begawan?", "Brunei", "Malaysia", "Singapore", "Indonesia"),
        ("Which country has the capital city of Yerevan?", "Armenia", "Georgia", "Azerbaijan", "Kazakhstan"),
        ("Which country has the capital city of Ulaanbaatar?", "Mongolia", "Nepal", "Kyrgyzstan", "Tajikistan"),
        ("Which country has the capital city of Nicosia?", "Cyprus", "Malta", "Greece", "Albania"),
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
                    f"Empty or invalid value in {difficulty} question {index}."
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
                    "World politics, countries, capitals, currencies "
                    "and international relations."
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
