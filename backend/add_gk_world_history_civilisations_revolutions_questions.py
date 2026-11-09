
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 196
LESSON_TITLE = "World History, Civilisations, Revolutions and Important Historical Events"
TOPIC = "General Knowledge"

BANK = {
    "Easy": [
        ("Which ancient civilisation developed along the Nile River?", "Egyptian civilisation", "Roman civilisation", "Chinese civilisation", "Greek civilisation"),
        ("Which civilisation developed between the Tigris and Euphrates rivers?", "Mesopotamian civilisation", "Indus Valley civilisation", "Mayan civilisation", "Aztec civilisation"),
        ("Which ancient civilisation built the pyramids of Giza?", "Ancient Egyptians", "Ancient Romans", "Ancient Greeks", "Persians"),
        ("Who was the first emperor of Rome?", "Augustus", "Julius Caesar", "Nero", "Constantine"),
        ("Which city was the centre of the ancient Greek civilisation?", "Athens", "Cairo", "Babylon", "Rome"),
        ("Who was the famous Macedonian king who created a vast empire?", "Alexander the Great", "Philip II", "Pericles", "Leonidas"),
        ("Which ancient civilisation developed democracy in Athens?", "Greek civilisation", "Egyptian civilisation", "Persian civilisation", "Chinese civilisation"),
        ("Who built the Great Wall of China in its early major unified form?", "Qin Shi Huang", "Kublai Khan", "Confucius", "Sun Yat-sen"),
        ("Which ancient civilisation developed the city of Mohenjo-daro?", "Indus Valley civilisation", "Roman civilisation", "Greek civilisation", "Egyptian civilisation"),
        ("Which river was central to the development of ancient Mesopotamia?", "Euphrates", "Amazon", "Danube", "Thames"),
        ("In which country did the Renaissance begin?", "Italy", "France", "Germany", "Spain"),
        ("Which invention helped spread books and knowledge in Europe during the Renaissance?", "Printing press", "Steam engine", "Telephone", "Television"),
        ("Who is commonly credited with developing the movable-type printing press in Europe?", "Johannes Gutenberg", "Leonardo da Vinci", "Galileo Galilei", "Isaac Newton"),
        ("Who painted the Mona Lisa?", "Leonardo da Vinci", "Michelangelo", "Raphael", "Vincent van Gogh"),
        ("In which year did the French Revolution begin?", "1789", "1776", "1815", "1848"),
        ("Which prison was stormed during the French Revolution on 14 July 1789?", "Bastille", "Tower of London", "Alcatraz", "Versailles Palace"),
        ("Who was the French military leader who became emperor in 1804?", "Napoleon Bonaparte", "Louis XVI", "Robespierre", "Charles de Gaulle"),
        ("Which country declared independence from Britain in 1776?", "United States of America", "Canada", "Australia", "South Africa"),
        ("Who was the first President of the United States?", "George Washington", "Thomas Jefferson", "Abraham Lincoln", "John Adams"),
        ("Which event is commonly considered the beginning of the First World War?", "Assassination of Archduke Franz Ferdinand", "Russian Revolution", "Fall of Berlin Wall", "Boston Tea Party"),
        ("In which year did the First World War end?", "1918", "1914", "1920", "1939"),
        ("In which year did the Second World War begin?", "1939", "1918", "1941", "1945"),
        ("Which country was ruled by Adolf Hitler during the Second World War?", "Germany", "Italy", "Japan", "France"),
        ("Which two Japanese cities were struck by atomic bombs in August 1945?", "Hiroshima and Nagasaki", "Tokyo and Kyoto", "Osaka and Kobe", "Nara and Yokohama"),
        ("In which year was the United Nations established?", "1945", "1919", "1939", "1955"),
        ("Which wall became a symbol of the Cold War division in Europe?", "Berlin Wall", "Great Wall of China", "Hadrian's Wall", "Western Wall"),
        ("In which year did the Berlin Wall fall?", "1989", "1961", "1975", "1991"),
        ("Which ancient civilisation developed the Olympic Games?", "Greek civilisation", "Roman civilisation", "Egyptian civilisation", "Persian civilisation"),
        ("Which empire was ruled by Genghis Khan?", "Mongol Empire", "Roman Empire", "Ottoman Empire", "Mughal Empire"),
        ("Which famous ancient city was buried after the eruption of Mount Vesuvius in AD 79?", "Pompeii", "Athens", "Sparta", "Alexandria"),
    ],

    "Medium": [
        ("Which ancient civilisation is associated with the development of cuneiform writing?", "Sumerian civilisation", "Mayan civilisation", "Roman civilisation", "Greek civilisation"),
        ("Who was the Babylonian king associated with the famous ancient law code?", "Hammurabi", "Nebuchadnezzar II", "Cyrus the Great", "Darius I"),
        ("Which ancient civilisation developed a sophisticated calendar and writing system in Mesoamerica?", "Mayan civilisation", "Roman civilisation", "Persian civilisation", "Sumerian civilisation"),
        ("Which empire was ruled by Cyrus the Great?", "Achaemenid Persian Empire", "Roman Empire", "Mongol Empire", "Byzantine Empire"),
        ("Which battle in 490 BCE was a major Greek victory over the Persians?", "Battle of Marathon", "Battle of Hastings", "Battle of Waterloo", "Battle of Actium"),
        ("Who was the Athenian statesman associated with the development of Athenian democracy?", "Cleisthenes", "Alexander the Great", "Hannibal", "Julius Caesar"),
        ("Which empire had Constantinople as its capital after the fall of the Western Roman Empire?", "Byzantine Empire", "Mongol Empire", "Mughal Empire", "Mali Empire"),
        ("In which year did Constantinople fall to the Ottoman Turks?", "1453", "1492", "1517", "1389"),
        ("Who was the Ottoman ruler who captured Constantinople in 1453?", "Mehmed II", "Suleiman I", "Osman I", "Selim I"),
        ("Which trade route connected China with regions of Central Asia, the Middle East and Europe?", "Silk Road", "Spice Route only", "Amber Road", "Royal Road of Persia"),
        ("Which Italian explorer reached the Americas in 1492 under the Spanish Crown?", "Christopher Columbus", "Marco Polo", "Vasco da Gama", "Ferdinand Magellan"),
        ("Who led the first expedition to circumnavigate the globe, although he died before its completion?", "Ferdinand Magellan", "Christopher Columbus", "James Cook", "Amerigo Vespucci"),
        ("Which treaty ended the Thirty Years' War in 1648?", "Peace of Westphalia", "Treaty of Versailles", "Treaty of Utrecht", "Treaty of Paris"),
        ("Which revolution began in England in 1688 and resulted in the overthrow of James II?", "Glorious Revolution", "French Revolution", "American Revolution", "Russian Revolution"),
        ("Which document limited the powers of the English monarch in 1689?", "English Bill of Rights", "Magna Carta", "Declaration of Independence", "Treaty of Paris"),
        ("Which event is associated with the beginning of the Industrial Revolution?", "Mechanisation of textile production", "Invention of the internet", "Discovery of electricity", "Development of nuclear power"),
        ("In which country did the Industrial Revolution begin?", "Great Britain", "France", "Russia", "Japan"),
        ("Who developed the improved steam engine that contributed significantly to the Industrial Revolution?", "James Watt", "Thomas Edison", "Michael Faraday", "Alexander Graham Bell"),
        ("Which revolution overthrew the Russian monarchy in February 1917?", "February Revolution", "October Revolution", "French Revolution", "Glorious Revolution"),
        ("Who led the Bolshevik Revolution in Russia in October 1917?", "Vladimir Lenin", "Joseph Stalin", "Leon Trotsky alone", "Tsar Nicholas II"),
        ("Which treaty formally ended the state of war between Germany and the Allied Powers after the First World War?", "Treaty of Versailles", "Treaty of Rome", "Treaty of Tordesillas", "Treaty of Brest-Litovsk"),
        ("Which international organisation was created after the First World War to promote peace?", "League of Nations", "United Nations", "NATO", "European Union"),
        ("Which event in 1929 marked the beginning of a major worldwide economic crisis?", "Wall Street Crash", "Russian Revolution", "Fall of Constantinople", "Suez Crisis"),
        ("Which conference in 1945 brought together Roosevelt, Churchill and Stalin to discuss post-war arrangements?", "Yalta Conference", "Vienna Congress", "Berlin Conference of 1884", "Bandung Conference"),
        ("Which country was divided into North and South after the Second World War along the 38th parallel?", "Korea", "Vietnam", "Germany", "China"),
        ("Which crisis in 1962 brought the United States and the Soviet Union close to nuclear war?", "Cuban Missile Crisis", "Suez Crisis", "Berlin Blockade", "Korean War"),
        ("Which movement opposed apartheid in South Africa?", "Anti-apartheid movement", "Boxer Rebellion", "Taiping Rebellion", "Meiji Restoration"),
        ("Who became South Africa's first Black president in 1994?", "Nelson Mandela", "Desmond Tutu", "Thabo Mbeki", "F. W. de Klerk"),
        ("Which revolution in 1979 overthrew the monarchy in Iran?", "Iranian Revolution", "Cuban Revolution", "Russian Revolution", "Young Turk Revolution"),
        ("Which country experienced the Meiji Restoration beginning in 1868?", "Japan", "China", "Korea", "Thailand"),
    ],

    "Hard": [
        ("Which ancient Mesopotamian city is associated with the earliest known extensive written law code of Ur-Nammu?", "Ur", "Nineveh", "Persepolis", "Memphis"),
        ("Which civilisation developed the Linear B script used for an early form of Greek?", "Mycenaean civilisation", "Mayan civilisation", "Egyptian civilisation", "Phoenician civilisation"),
        ("Which ancient Greek historian is often called the Father of History?", "Herodotus", "Thucydides", "Plutarch", "Xenophon"),
        ("Which war between Athens and Sparta ended with the defeat of Athens in 404 BCE?", "Peloponnesian War", "Persian War", "Punic War", "Trojan War"),
        ("Which Carthaginian general crossed the Alps during the Second Punic War?", "Hannibal", "Scipio Africanus", "Julius Caesar", "Cato the Elder"),
        ("Which Roman emperor issued the Edict of Milan in 313 CE with Licinius?", "Constantine I", "Augustus", "Nero", "Trajan"),
        ("Which event traditionally marks the fall of the Western Roman Empire?", "Deposition of Romulus Augustulus in 476 CE", "Fall of Constantinople in 1453", "Battle of Hastings in 1066", "Coronation of Charlemagne in 800"),
        ("Who was crowned emperor of the Romans by Pope Leo III in 800 CE?", "Charlemagne", "Otto I", "Frederick Barbarossa", "William the Conqueror"),
        ("Which document was sealed by King John of England in 1215?", "Magna Carta", "English Bill of Rights", "Petition of Right", "Act of Settlement"),
        ("Which pandemic devastated Europe during the 14th century?", "Black Death", "Spanish Flu", "Cholera pandemic of 19th century", "Hong Kong Flu"),
        ("Which council initiated major reforms in the Catholic Church during the Counter-Reformation?", "Council of Trent", "Council of Nicaea", "Council of Constance", "First Vatican Council"),
        ("Who published the Ninety-five Theses in 1517, initiating the Protestant Reformation?", "Martin Luther", "John Calvin", "Henry VIII", "Ignatius of Loyola"),
        ("Which treaty divided newly discovered lands outside Europe between Spain and Portugal in 1494?", "Treaty of Tordesillas", "Treaty of Utrecht", "Treaty of Westphalia", "Treaty of Paris"),
        ("Which battle in 1815 ended Napoleon Bonaparte's rule after his return from exile?", "Battle of Waterloo", "Battle of Trafalgar", "Battle of Austerlitz", "Battle of Leipzig"),
        ("Which international congress reorganised Europe after the Napoleonic Wars?", "Congress of Vienna", "Congress of Berlin in 1884", "Yalta Conference", "Congress of Aix-la-Chapelle only"),
        ("Which revolution in 1848 led to the overthrow of the July Monarchy in France?", "February Revolution of 1848", "October Revolution", "Glorious Revolution", "Haitian Revolution"),
        ("Which uprising in 1857 challenged British rule in India and is also known as the Indian Rebellion of 1857?", "Indian Rebellion of 1857", "Swadeshi Movement", "Non-Cooperation Movement", "Quit India Movement"),
        ("Which conference of 1884–1885 regulated European colonial claims in Africa?", "Berlin Conference", "Yalta Conference", "Potsdam Conference", "Bandung Conference"),
        ("Which battle in 1916 was one of the longest and bloodiest battles of the First World War?", "Battle of Verdun", "Battle of Waterloo", "Battle of Trafalgar", "Battle of Hastings"),
        ("Which revolution in 1911 ended the Qing dynasty in China?", "Xinhai Revolution", "Cultural Revolution", "Taiping Rebellion", "Boxer Rebellion"),
        ("Which treaty ended Russia's participation in the First World War in 1918?", "Treaty of Brest-Litovsk", "Treaty of Versailles", "Treaty of Trianon", "Treaty of Lausanne"),
        ("Which economic policy was introduced by Lenin in Soviet Russia in 1921?", "New Economic Policy", "Five-Year Plan", "Great Leap Forward", "Perestroika"),
        ("Which event in 1931 marked Japan's expansion into Manchuria?", "Mukden Incident", "Marco Polo Bridge Incident", "Mukden Treaty", "Siberian Intervention"),
        ("Which conference in 1945 established arrangements for the occupation of Germany after the Second World War?", "Potsdam Conference", "Congress of Vienna", "Bandung Conference", "Tehran Conference"),
        ("Which 1955 conference brought together Asian and African countries to discuss cooperation and anti-colonialism?", "Bandung Conference", "Yalta Conference", "Potsdam Conference", "Bretton Woods Conference"),
        ("Which treaty established the European Coal and Steel Community in 1951?", "Treaty of Paris", "Treaty of Maastricht", "Treaty of Lisbon", "Treaty of Versailles"),
        ("Which 1961 event formalised the creation of the Non-Aligned Movement?", "Belgrade Conference", "Bandung Conference", "Yalta Conference", "Geneva Conference of 1954"),
        ("Which reform policy introduced by Mikhail Gorbachev is commonly translated as restructuring?", "Perestroika", "Glasnost", "Détente", "Korenizatsiya"),
        ("Which reform policy introduced by Mikhail Gorbachev is commonly associated with openness?", "Glasnost", "Perestroika", "Collectivisation", "Bolshevism"),
        ("Which agreement signed in 1992 laid the foundation for the European Union?", "Maastricht Treaty", "Treaty of Rome", "Treaty of Paris of 1951", "Treaty of Versailles"),
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
                    "World history, ancient civilisations, revolutions "
                    "and important historical events."
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
