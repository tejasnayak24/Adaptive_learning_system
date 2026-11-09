
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 178
LESSON_TITLE = "International Organisations, Global Economy and World Affairs"
TOPIC = "General Knowledge"

BANK = {
    "Easy": [
        ("Where is the headquarters of the United Nations located?", "New York", "London", "Paris", "Tokyo"),
        ("In which year was the United Nations established?", "1945", "1919", "1950", "1965"),
        ("How many permanent members are there in the UN Security Council?", "Five", "Four", "Six", "Ten"),
        ("Which organisation works to improve global public health?", "WHO", "WTO", "IMF", "UNESCO"),
        ("What is the full form of WHO?", "World Health Organization", "World Human Organisation", "World Heritage Office", "Worldwide Health Organisation"),
        ("Where is the headquarters of WHO?", "Geneva", "New York", "Rome", "Vienna"),
        ("Which organisation promotes international trade rules?", "WTO", "WHO", "UNICEF", "UNESCO"),
        ("What does WTO stand for?", "World Trade Organization", "World Tourism Office", "World Transport Organisation", "Worldwide Trade Office"),
        ("Where is the headquarters of the World Trade Organization?", "Geneva", "Paris", "London", "Washington, D.C."),
        ("Which organisation provides financial assistance to countries facing balance of payments problems?", "IMF", "UNICEF", "WHO", "UNESCO"),
        ("What does IMF stand for?", "International Monetary Fund", "International Market Federation", "Indian Monetary Fund", "International Management Forum"),
        ("Where is the headquarters of the International Monetary Fund?", "Washington, D.C.", "Geneva", "New Delhi", "Rome"),
        ("Which organisation focuses on education, science and culture?", "UNESCO", "WHO", "WTO", "IMF"),
        ("What does UNESCO stand for?", "United Nations Educational, Scientific and Cultural Organization", "United Nations Economic and Social Council", "Universal Network for Education and Science", "United Nations Environmental Security Council"),
        ("Where is UNESCO headquartered?", "Paris", "New York", "Geneva", "Tokyo"),
        ("Which organisation works for the welfare of children worldwide?", "UNICEF", "IMF", "WTO", "NATO"),
        ("What does UNICEF primarily focus on?", "Children's rights and welfare", "International banking", "Military cooperation", "Global trade tariffs"),
        ("Which military alliance was established in 1949?", "NATO", "ASEAN", "SAARC", "OPEC"),
        ("What does NATO stand for?", "North Atlantic Treaty Organization", "National Asian Trade Organisation", "North American Transport Office", "New Atlantic Trade Organisation"),
        ("Which organisation is associated with oil-exporting countries?", "OPEC", "UNESCO", "WHO", "ASEAN"),
        ("Where is the headquarters of OPEC located?", "Vienna", "Paris", "New York", "Beijing"),
        ("Which regional organisation includes India, Nepal, Bhutan and Bangladesh?", "SAARC", "European Union", "NATO", "G7"),
        ("Where is the SAARC Secretariat located?", "Kathmandu", "New Delhi", "Dhaka", "Colombo"),
        ("Which organisation promotes cooperation among Southeast Asian nations?", "ASEAN", "SAARC", "NATO", "OPEC"),
        ("Where is the ASEAN Secretariat located?", "Jakarta", "Bangkok", "Manila", "Singapore"),
        ("Which international organisation publishes the Human Development Report?", "UNDP", "WTO", "IMF", "NATO"),
        ("What does G20 represent?", "A forum of major advanced and emerging economies", "A military alliance of 20 countries", "A group of 20 United Nations agencies", "A global sports organisation"),
        ("Which organisation is responsible for maintaining international peace and security?", "United Nations", "World Trade Organization", "OPEC", "FIFA"),
        ("Which organisation governs international football?", "FIFA", "IOC", "ICC", "UNESCO"),
        ("Where is the headquarters of the International Olympic Committee?", "Lausanne", "Geneva", "London", "Rome"),
    ],

    "Medium": [
        ("Which five countries are permanent members of the UN Security Council?", "China, France, Russia, UK and USA", "India, China, Japan, Germany and USA", "France, Germany, India, UK and USA", "Brazil, Russia, China, India and Japan"),
        ("What is the main purpose of the UN General Assembly?", "Providing a forum for discussion among all UN member states", "Commanding all national armies", "Setting global interest rates", "Regulating international sports"),
        ("Which UN body has primary responsibility for international peace and security?", "Security Council", "General Assembly", "Economic and Social Council", "International Court of Justice"),
        ("Where is the International Court of Justice located?", "The Hague", "Geneva", "New York", "Brussels"),
        ("What is the principal judicial organ of the United Nations?", "International Court of Justice", "International Criminal Court", "World Trade Organization", "International Monetary Fund"),
        ("Which organisation publishes the World Economic Outlook?", "International Monetary Fund", "World Health Organization", "UNESCO", "UNICEF"),
        ("Which organisation publishes the World Development Report?", "World Bank", "WTO", "WHO", "OPEC"),
        ("Where is the headquarters of the World Bank Group?", "Washington, D.C.", "Geneva", "Paris", "Vienna"),
        ("What is the main objective of the World Bank?", "Reducing poverty and supporting development", "Organising military alliances", "Regulating global sports", "Managing international criminal trials"),
        ("Which agreement established the World Trade Organization?", "Marrakesh Agreement", "Treaty of Versailles", "Paris Agreement", "Kyoto Protocol"),
        ("In which year did the WTO begin operations?", "1995", "1945", "1980", "2001"),
        ("Which organisation succeeded the General Agreement on Tariffs and Trade as the main multilateral trade organisation?", "World Trade Organization", "International Labour Organization", "World Health Organization", "United Nations Development Programme"),
        ("What does FDI stand for?", "Foreign Direct Investment", "Foreign Domestic Income", "Financial Development Index", "Federal Deposit Insurance"),
        ("What is a tariff in international trade?", "A tax imposed on imported or exported goods", "A subsidy paid to every consumer", "A type of currency", "A restriction on domestic employment"),
        ("What is globalisation?", "Increasing integration of economies and societies worldwide", "Complete separation of national economies", "Elimination of all international communication", "A system of local-only trade"),
        ("Which organisation promotes international labour standards?", "International Labour Organization", "World Trade Organization", "International Monetary Fund", "World Tourism Organization"),
        ("Where is the headquarters of the International Labour Organization?", "Geneva", "New York", "Rome", "Madrid"),
        ("Which organisation is responsible for international civil aviation standards?", "International Civil Aviation Organization", "International Maritime Organization", "World Meteorological Organization", "International Labour Organization"),
        ("Where is the headquarters of the International Civil Aviation Organization?", "Montreal", "Geneva", "London", "Vienna"),
        ("Which organisation deals with international maritime safety and shipping regulations?", "International Maritime Organization", "World Health Organization", "UNICEF", "International Monetary Fund"),
        ("Where is the headquarters of the International Maritime Organization?", "London", "Paris", "Rome", "Brussels"),
        ("Which group consists of Brazil, Russia, India, China and South Africa among its original members?", "BRICS", "G7", "NATO", "ASEAN"),
        ("Which country hosted the first BRICS summit in 2009?", "Russia", "India", "China", "Brazil"),
        ("Which regional organisation is associated with economic and political integration in Europe?", "European Union", "SAARC", "ASEAN", "OPEC"),
        ("Which treaty formally established the European Union?", "Maastricht Treaty", "Treaty of Rome only", "Treaty of Versailles", "Lisbon Agreement"),
        ("What is the common currency used by many European Union member countries?", "Euro", "Pound", "Dollar", "Franc"),
        ("Which organisation coordinates international efforts to combat climate change through its climate convention process?", "United Nations Framework Convention on Climate Change", "World Trade Organization", "International Monetary Fund", "International Olympic Committee"),
        ("Where was the Paris Agreement on climate change adopted?", "Paris", "Geneva", "New York", "London"),
        ("Which organisation is responsible for coordinating international responses to nuclear energy and safety issues?", "International Atomic Energy Agency", "World Trade Organization", "UNICEF", "International Labour Organization"),
        ("Where is the headquarters of the International Atomic Energy Agency?", "Vienna", "Paris", "New York", "Nairobi"),
    ],

    "Hard": [
        ("Which UN organ elects non-permanent members of the Security Council?", "UN General Assembly", "International Court of Justice", "UN Secretariat", "Economic and Social Council"),
        ("How long is the term of a non-permanent member of the UN Security Council?", "Two years", "One year", "Three years", "Five years"),
        ("How many non-permanent members are there in the UN Security Council?", "Ten", "Five", "Fifteen", "Twenty"),
        ("Which UN organ coordinates the economic and social work of specialised agencies?", "Economic and Social Council", "Security Council", "Trusteeship Council", "International Court of Justice"),
        ("Which UN body is responsible for the administration and coordination of the organisation's work?", "UN Secretariat", "Security Council", "General Assembly", "International Court of Justice"),
        ("Which institution was established under the Bretton Woods system to support international monetary cooperation?", "International Monetary Fund", "World Health Organization", "UNESCO", "International Labour Organization"),
        ("In which year was the Bretton Woods Conference held?", "1944", "1945", "1955", "1960"),
        ("Which institution was originally established as the International Bank for Reconstruction and Development?", "World Bank", "International Monetary Fund", "World Trade Organization", "Asian Development Bank"),
        ("Which organisation provides development financing primarily for the Asia-Pacific region?", "Asian Development Bank", "European Central Bank", "African Union", "OPEC"),
        ("Where is the headquarters of the Asian Development Bank?", "Manila", "Tokyo", "Singapore", "Bangkok"),
        ("Which institution is the central bank of the European Union's euro area?", "European Central Bank", "European Investment Bank", "World Bank", "Bank for International Settlements"),
        ("Where is the European Central Bank headquartered?", "Frankfurt", "Brussels", "Paris", "Amsterdam"),
        ("Which organisation is known as the central bank for central banks?", "Bank for International Settlements", "International Monetary Fund", "World Bank", "European Investment Bank"),
        ("Where is the headquarters of the Bank for International Settlements?", "Basel", "Geneva", "London", "New York"),
        ("Which agreement created the framework for the International Monetary Fund and the International Bank for Reconstruction and Development?", "Bretton Woods Agreements", "Marrakesh Agreement", "Maastricht Treaty", "Kyoto Protocol"),
        ("Which WTO principle requires equal trade treatment among member countries in comparable circumstances?", "Most-Favoured-Nation principle", "Nationalisation principle", "Absolute protection principle", "Currency parity principle"),
        ("What is the WTO principle of national treatment?", "Imported products should receive treatment no less favourable than like domestic products after entering the market", "Imports must always be taxed more heavily", "Exports must be banned during recessions", "Foreign companies must be owned by governments"),
        ("What is the main objective of the Agreement on Trade-Related Aspects of Intellectual Property Rights?", "Establishing minimum standards for intellectual property protection in trade", "Regulating international air travel", "Controlling global oil production", "Setting international labour wages"),
        ("Which organisation administers the Convention on International Trade in Endangered Species of Wild Fauna and Flora?", "CITES Secretariat", "WTO Secretariat", "IMF Secretariat", "NATO Secretariat"),
        ("Where is the CITES Secretariat based?", "Geneva", "New York", "Vienna", "Rome"),
        ("Which international agreement aims to protect the ozone layer?", "Montreal Protocol", "Paris Agreement", "Marrakesh Agreement", "Maastricht Treaty"),
        ("In which year was the Montreal Protocol adopted?", "1987", "1972", "1992", "2005"),
        ("Which international agreement established binding emission-reduction commitments for many developed countries in its first commitment period?", "Kyoto Protocol", "Paris Agreement", "Montreal Protocol", "Ramsar Convention"),
        ("In which year was the Kyoto Protocol adopted?", "1997", "1987", "2001", "2015"),
        ("Which organisation publishes the annual Human Development Report?", "United Nations Development Programme", "World Trade Organization", "International Labour Organization", "International Monetary Fund"),
        ("Which three dimensions are central to the Human Development Index?", "Health, education and standard of living", "Military strength, exports and population", "Agriculture, industry and tourism", "Inflation, taxation and interest rates"),
        ("Which organisation maintains the International Monetary Fund's Special Drawing Rights system?", "International Monetary Fund", "World Trade Organization", "World Bank", "Bank for International Settlements"),
        ("What are Special Drawing Rights?", "An international reserve asset created by the IMF", "A physical currency used worldwide", "A type of government tax", "A private bank deposit"),
        ("Which international organisation is responsible for setting global standards for postal services?", "Universal Postal Union", "International Maritime Organization", "World Meteorological Organization", "International Labour Organization"),
        ("Where is the headquarters of the Universal Postal Union?", "Bern", "Geneva", "Paris", "Vienna"),
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
                    f"Invalid question format: {difficulty} #{index}"
                )

            question, correct, *wrong = item
            options = [correct] + wrong

            if not all(isinstance(value, str) and value.strip() for value in item):
                raise ValueError(
                    f"Empty field: {difficulty} #{index}"
                )

            if len(set(options)) != 4:
                raise ValueError(
                    f"Duplicate options: {difficulty} #{index}"
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
                "Learn about international organisations, global trade, international finance, regional cooperation and major world agreements."
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
                raise ValueError(
                    f"Multiple {difficulty} quizzes found."
                )

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
        print("GK TOPIC 18 INSERTED SUCCESSFULLY")
        print("International Organisations, Global Economy and World Affairs")
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
