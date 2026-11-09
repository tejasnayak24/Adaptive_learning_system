
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 195
LESSON_TITLE = "World Organisations, International Relations and Global Institutions"
TOPIC = "General Knowledge"

BANK = {
    "Easy": [
        ("Where is the headquarters of the United Nations located?", "New York", "London", "Paris", "Geneva"),
        ("In which year was the United Nations established?", "1945", "1919", "1939", "1950"),
        ("How many permanent members are there in the UN Security Council?", "5", "10", "15", "20"),
        ("Which organisation is responsible for international public health?", "WHO", "WTO", "IMF", "ILO"),
        ("What is the full form of UNESCO?", "United Nations Educational, Scientific and Cultural Organization", "United Nations Economic and Social Council Organization", "Universal Network for Education and Science Cooperation", "United Nations Environmental and Social Cooperation Organization"),
        ("Where is the headquarters of WHO?", "Geneva", "New York", "Rome", "Vienna"),
        ("Which organisation works primarily for children's welfare worldwide?", "UNICEF", "IMF", "WTO", "NATO"),
        ("What is the full form of IMF?", "International Monetary Fund", "International Management Federation", "Indian Monetary Foundation", "International Market Forum"),
        ("Which organisation regulates international trade rules?", "WTO", "WHO", "UNICEF", "UNESCO"),
        ("Where is the headquarters of the World Trade Organization?", "Geneva", "Paris", "New York", "Tokyo"),
        ("Which organisation provides financial assistance to countries for development projects?", "World Bank", "UNICEF", "WHO", "INTERPOL"),
        ("Where is the headquarters of the World Bank?", "Washington, D.C.", "London", "Geneva", "Rome"),
        ("What is the full form of NATO?", "North Atlantic Treaty Organization", "National Association of Trade Organizations", "North Asian Treaty Office", "National Atlantic Trade Organisation"),
        ("Which organisation promotes cooperation among South Asian countries?", "SAARC", "ASEAN", "NATO", "OPEC"),
        ("What is the full form of ASEAN?", "Association of Southeast Asian Nations", "Asian Economic and Security Association", "Association of South European Nations", "Asian Society for Economic Advancement"),
        ("Where is the ASEAN Secretariat located?", "Jakarta", "Bangkok", "Singapore", "Manila"),
        ("Which organisation is associated with international policing cooperation?", "INTERPOL", "UNESCO", "WIPO", "FAO"),
        ("Where is the headquarters of INTERPOL?", "Lyon", "London", "New York", "Rome"),
        ("Which organisation works to improve food security and agriculture?", "FAO", "WHO", "WTO", "IMF"),
        ("What is the full form of FAO?", "Food and Agriculture Organization", "Federal Agricultural Office", "Food Administration Organisation", "Finance and Agriculture Office"),
        ("Which organisation is responsible for international labour standards?", "ILO", "IMF", "WTO", "NATO"),
        ("Where is the headquarters of the International Labour Organization?", "Geneva", "New York", "Berlin", "Madrid"),
        ("Which organisation promotes the protection of intellectual property worldwide?", "WIPO", "WHO", "FAO", "UNICEF"),
        ("What is the full form of G20?", "Group of Twenty", "Global Twenty Nations", "Government Twenty Council", "Group of International Economies"),
        ("Which organisation is a regional political and economic union in Europe?", "European Union", "African Union", "SAARC", "ASEAN"),
        ("Which organisation is responsible for international nuclear safeguards and peaceful nuclear cooperation?", "IAEA", "WIPO", "ILO", "UNICEF"),
        ("What is the full form of OPEC?", "Organization of the Petroleum Exporting Countries", "Organisation for Petroleum and Energy Cooperation", "Oil Producers Economic Council", "Organisation of Petroleum Export Companies"),
        ("Which organisation is associated with cooperation among Commonwealth countries?", "Commonwealth of Nations", "NATO", "OPEC", "WTO"),
        ("Which organisation promotes economic and political cooperation among African countries?", "African Union", "European Union", "SAARC", "ASEAN"),
        ("What is the primary purpose of the United Nations?", "Maintain international peace and security and promote cooperation", "Control all national governments", "Manage global commercial banks", "Regulate every country's currency"),
    ],

    "Medium": [
        ("Which principal organ of the United Nations has primary responsibility for maintaining international peace and security?", "Security Council", "General Assembly", "Economic and Social Council", "Secretariat"),
        ("How many total members are there in the UN Security Council?", "15", "10", "20", "25"),
        ("Which UN organ includes representatives of all member states?", "General Assembly", "Security Council", "International Court of Justice", "Secretariat"),
        ("Where is the International Court of Justice located?", "The Hague", "Geneva", "New York", "Vienna"),
        ("What is the principal judicial organ of the United Nations?", "International Court of Justice", "International Criminal Court", "European Court of Human Rights", "Permanent Court of Arbitration"),
        ("Which UN body coordinates economic and social work?", "Economic and Social Council", "Security Council", "Trusteeship Council", "International Court of Justice"),
        ("Which organisation was established through the Bretton Woods Conference?", "International Monetary Fund", "World Trade Organization", "ASEAN", "NATO"),
        ("In which year was the Bretton Woods Conference held?", "1944", "1945", "1950", "1939"),
        ("Which institution primarily provides long-term development loans and assistance?", "World Bank", "IMF", "WTO", "OPEC"),
        ("What is the primary objective of the IMF?", "Promote international monetary cooperation and financial stability", "Regulate international sports", "Protect endangered wildlife", "Manage global postal services"),
        ("Which agreement established the World Trade Organization?", "Marrakesh Agreement", "Treaty of Versailles", "Paris Agreement", "Geneva Convention"),
        ("In which year did the WTO begin operations?", "1995", "1945", "1980", "2001"),
        ("Which organisation replaced the General Agreement on Tariffs and Trade as the main global trade institution?", "World Trade Organization", "International Monetary Fund", "World Bank", "International Labour Organization"),
        ("Which regional organisation was established by the Bangkok Declaration of 1967?", "ASEAN", "SAARC", "European Union", "African Union"),
        ("In which year was SAARC established?", "1985", "1975", "1995", "2000"),
        ("Where is the SAARC Secretariat located?", "Kathmandu", "New Delhi", "Dhaka", "Colombo"),
        ("Which treaty formally established the European Union?", "Maastricht Treaty", "Treaty of Versailles", "Treaty of Rome", "Lisbon Treaty"),
        ("Which agreement is associated with the creation of the European Economic Community in 1957?", "Treaty of Rome", "Maastricht Treaty", "Paris Agreement", "North Atlantic Treaty"),
        ("Which organisation was founded through the North Atlantic Treaty of 1949?", "NATO", "ASEAN", "SAARC", "OPEC"),
        ("Which organisation focuses on international civil aviation standards?", "International Civil Aviation Organization", "International Maritime Organization", "World Health Organization", "International Labour Organization"),
        ("Where is the headquarters of the International Civil Aviation Organization?", "Montreal", "Geneva", "Paris", "London"),
        ("Which organisation is responsible for international maritime safety and shipping regulations?", "International Maritime Organization", "International Civil Aviation Organization", "World Trade Organization", "World Bank"),
        ("Which UN agency works for refugees and displaced persons?", "UNHCR", "UNICEF", "WIPO", "FAO"),
        ("What does the abbreviation UNHCR stand for?", "United Nations High Commissioner for Refugees", "United Nations Humanitarian Council for Relief", "Universal Network for Humanitarian Crisis Response", "United Nations Human Rights Committee"),
        ("Which organisation publishes the World Economic Outlook report?", "International Monetary Fund", "World Trade Organization", "UNESCO", "ILO"),
        ("Which organisation publishes the Human Development Report?", "United Nations Development Programme", "World Bank", "International Labour Organization", "World Health Organization"),
        ("Which organisation is associated with the Convention on International Trade in Endangered Species?", "CITES", "WIPO", "WTO", "ILO"),
        ("What is the primary purpose of the Paris Agreement?", "Address climate change through international cooperation", "Regulate international trade tariffs", "Establish a global currency", "Create a military alliance"),
        ("Which organisation is responsible for setting international standards for weather and climate information?", "World Meteorological Organization", "World Trade Organization", "International Monetary Fund", "UNICEF"),
        ("Which international organisation coordinates global postal services?", "Universal Postal Union", "International Labour Organization", "World Intellectual Property Organization", "International Monetary Fund"),
    ],

    "Hard": [
        ("Which article of the UN Charter gives the Security Council primary responsibility for international peace and security?", "Article 24", "Article 1", "Article 51", "Article 99"),
        ("Which chapter of the UN Charter deals with the Security Council's enforcement actions?", "Chapter VII", "Chapter I", "Chapter IV", "Chapter X"),
        ("Which article of the UN Charter recognises the inherent right of individual or collective self-defence?", "Article 51", "Article 24", "Article 33", "Article 2"),
        ("Which UN organ elects the non-permanent members of the Security Council?", "General Assembly", "Security Council", "International Court of Justice", "Secretariat"),
        ("How long is the term of a non-permanent member of the UN Security Council?", "Two years", "One year", "Three years", "Five years"),
        ("Which country is the depositary of the original United Nations Charter?", "United States", "United Kingdom", "France", "Switzerland"),
        ("Which international convention established the framework for diplomatic relations in 1961?", "Vienna Convention on Diplomatic Relations", "Geneva Convention of 1949", "Paris Convention of 1883", "Rome Statute"),
        ("Which convention governs consular relations and was adopted in 1963?", "Vienna Convention on Consular Relations", "Vienna Convention on Diplomatic Relations", "Montreal Convention", "Chicago Convention"),
        ("Which treaty established the International Criminal Court?", "Rome Statute", "Maastricht Treaty", "Marrakesh Agreement", "North Atlantic Treaty"),
        ("In which year did the International Criminal Court begin functioning?", "2002", "1995", "1945", "2010"),
        ("Where is the International Criminal Court headquartered?", "The Hague", "Geneva", "New York", "Brussels"),
        ("Which principle is central to the WTO's most-favoured-nation rule?", "Treating trading partners equally in covered trade matters", "Giving permanent preference to one trading partner", "Prohibiting all international imports", "Requiring every country to use the same currency"),
        ("Which WTO agreement deals specifically with trade-related aspects of intellectual property rights?", "TRIPS Agreement", "GATS", "GATT", "SPS Agreement"),
        ("What is the full form of TRIPS?", "Trade-Related Aspects of Intellectual Property Rights", "Treaty for Regional International Patent Systems", "Trade Regulations in International Public Services", "Technical Rules for Industrial Product Standards"),
        ("Which WTO agreement covers trade in services?", "GATS", "TRIPS", "GATT", "TBT"),
        ("What is the full form of GATS?", "General Agreement on Trade in Services", "Global Agreement on Tariff Systems", "General Association of Trade Standards", "Government Agreement on Technical Services"),
        ("Which institution is responsible for settling disputes between WTO members?", "Dispute Settlement Body", "International Court of Justice", "UN Security Council", "International Criminal Court"),
        ("Which organisation administers the Convention on Biological Diversity?", "United Nations Environment Programme", "World Trade Organization", "International Monetary Fund", "International Labour Organization"),
        ("Which international treaty aims to prevent the spread of nuclear weapons?", "Treaty on the Non-Proliferation of Nuclear Weapons", "Treaty of Rome", "North Atlantic Treaty", "Marrakesh Agreement"),
        ("In which year was the Nuclear Non-Proliferation Treaty opened for signature?", "1968", "1945", "1975", "1992"),
        ("Which organisation verifies compliance with nuclear safeguards under international agreements?", "International Atomic Energy Agency", "World Trade Organization", "International Labour Organization", "UNICEF"),
        ("Which treaty established the African Union's predecessor, the Organisation of African Unity?", "Charter of the Organisation of African Unity", "Treaty of Maastricht", "Treaty of Rome", "North Atlantic Treaty"),
        ("In which year was the African Union officially launched?", "2002", "1963", "1985", "1995"),
        ("Which organisation is the successor to the Organisation of African Unity?", "African Union", "European Union", "Arab League", "ASEAN"),
        ("Which international organisation was created by the 1944 Chicago Convention?", "International Civil Aviation Organization", "International Maritime Organization", "World Meteorological Organization", "International Telecommunication Union"),
        ("Which organisation allocates global radio-frequency spectrum and coordinates international telecommunications standards?", "International Telecommunication Union", "Universal Postal Union", "World Intellectual Property Organization", "International Civil Aviation Organization"),
        ("Which international agreement established the framework for the protection of the ozone layer?", "Vienna Convention for the Protection of the Ozone Layer", "Paris Agreement", "Kyoto Protocol", "Ramsar Convention"),
        ("Which protocol introduced legally binding emission reduction targets for developed countries under the UN climate framework?", "Kyoto Protocol", "Montreal Protocol", "Cartagena Protocol", "Nagoya Protocol"),
        ("Which convention focuses on the conservation of wetlands of international importance?", "Ramsar Convention", "Vienna Convention", "Basel Convention", "Rotterdam Convention"),
        ("Which organisation provides the secretariat for the UN Framework Convention on Climate Change?", "UNFCCC Secretariat", "World Trade Organization", "International Monetary Fund", "International Court of Justice"),
    ]
}


def validate_bank():
    print("\nValidating question bank...")

    for difficulty in ("Easy", "Medium", "Hard"):
        count = len(BANK[difficulty])
        print(f"{difficulty}: {count}/30")

        if count != 30:
            raise ValueError(
                f"{difficulty} must contain exactly 30 questions; found {count}"
            )

        for index, item in enumerate(BANK[difficulty], start=1):
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
                    "World organisations, international relations and "
                    "global institutions."
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
