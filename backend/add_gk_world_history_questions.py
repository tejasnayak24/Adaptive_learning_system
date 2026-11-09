
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 170
LESSON_TITLE = "World History - Ancient Civilizations, Revolutions and Historical Events"
TOPIC = "General Knowledge"

BANK = {
    "Easy": [
        ("Which ancient civilization developed along the Nile River?", "Egyptian civilization", "Roman civilization", "Mayan civilization", "Chinese civilization"),
        ("Which ancient civilization developed in Mesopotamia?", "Sumerian civilization", "Inca civilization", "Aztec civilization", "Greek civilization"),
        ("Who was the first Emperor of Rome?", "Augustus", "Julius Caesar", "Nero", "Constantine"),
        ("Which ancient civilization built the pyramids of Giza?", "Egyptians", "Romans", "Greeks", "Persians"),
        ("Who was the famous Macedonian king who created a vast empire?", "Alexander the Great", "Philip II", "Darius I", "Julius Caesar"),
        ("Which city was the centre of ancient Greek democracy?", "Athens", "Sparta", "Troy", "Corinth"),
        ("Who was known as the first President of the United States?", "George Washington", "Abraham Lincoln", "Thomas Jefferson", "John Adams"),
        ("In which year did the French Revolution begin?", "1789", "1776", "1815", "1848"),
        ("Which country experienced the Industrial Revolution first?", "Great Britain", "France", "Germany", "United States"),
        ("Who was the famous leader of the Indian independence movement known for non-violence?", "Mahatma Gandhi", "Napoleon Bonaparte", "Winston Churchill", "Abraham Lincoln"),
        ("Which wall fell in 1989, symbolising the end of the Cold War division in Europe?", "Berlin Wall", "Great Wall of China", "Hadrian's Wall", "Wailing Wall"),
        ("Who was the leader of Nazi Germany during World War II?", "Adolf Hitler", "Benito Mussolini", "Joseph Stalin", "Winston Churchill"),
        ("Which event started World War I in 1914?", "Assassination of Archduke Franz Ferdinand", "Attack on Pearl Harbor", "Russian Revolution", "Invasion of Poland"),
        ("In which year did World War II end?", "1945", "1939", "1941", "1950"),
        ("Which ancient civilization developed in the Indus Valley?", "Harappan civilization", "Mayan civilization", "Roman civilization", "Greek civilization"),
        ("Who was the famous queen of ancient Egypt associated with Julius Caesar and Mark Antony?", "Cleopatra", "Nefertiti", "Hatshepsut", "Boudica"),
        ("Which country was ruled by the pharaohs?", "Egypt", "Greece", "Rome", "Persia"),
        ("Who was the founder of the Mongol Empire?", "Genghis Khan", "Kublai Khan", "Attila", "Tamerlane"),
        ("Which ancient city was buried by the eruption of Mount Vesuvius in AD 79?", "Pompeii", "Athens", "Sparta", "Alexandria"),
        ("Who was the first emperor of China, known for the Terracotta Army?", "Qin Shi Huang", "Kangxi", "Sun Yat-sen", "Confucius"),
        ("Which revolution resulted in the independence of the United States from Britain?", "American Revolution", "French Revolution", "Russian Revolution", "Industrial Revolution"),
        ("Who was the famous French military leader who became Emperor in 1804?", "Napoleon Bonaparte", "Louis XVI", "Charles de Gaulle", "Robespierre"),
        ("Which ancient civilization is associated with the city of Machu Picchu?", "Inca", "Aztec", "Maya", "Olmec"),
        ("Which empire was ruled by Julius Caesar?", "Roman Republic", "Mongol Empire", "Ottoman Empire", "Persian Empire"),
        ("Who was the British Prime Minister during most of World War II?", "Winston Churchill", "Neville Chamberlain", "Clement Attlee", "Margaret Thatcher"),
        ("Which organisation was established in 1945 to promote international peace and cooperation?", "United Nations", "League of Nations", "European Union", "NATO"),
        ("Which country launched the first artificial satellite, Sputnik 1?", "Soviet Union", "United States", "China", "United Kingdom"),
        ("Who was the first human to travel into space?", "Yuri Gagarin", "Neil Armstrong", "Buzz Aldrin", "Alan Shepard"),
        ("Which ancient Greek philosopher taught Alexander the Great?", "Aristotle", "Socrates", "Plato", "Pythagoras"),
        ("Which ship famously sank in 1912 during its maiden voyage?", "Titanic", "Lusitania", "Mayflower", "Bismarck"),
    ],

    "Medium": [
        ("Which ancient civilization is credited with developing cuneiform writing?", "Sumerians", "Romans", "Greeks", "Phoenicians"),
        ("Which Mesopotamian king is associated with one of the earliest surviving written law codes?", "Hammurabi", "Sargon of Akkad", "Nebuchadnezzar II", "Gilgamesh"),
        ("Which ancient civilization developed a sophisticated calendar and writing system in Mesoamerica?", "Maya", "Inca", "Roman", "Persian"),
        ("Which empire was ruled by Cyrus the Great?", "Achaemenid Persian Empire", "Roman Empire", "Mongol Empire", "Ottoman Empire"),
        ("Which battle in 480 BCE involved the Greek defence against the Persian army at a narrow pass?", "Battle of Thermopylae", "Battle of Marathon", "Battle of Salamis", "Battle of Plataea"),
        ("Who was the Carthaginian general who crossed the Alps during the Second Punic War?", "Hannibal", "Scipio Africanus", "Julius Caesar", "Marius"),
        ("Which Roman emperor issued the Edict of Milan in 313 CE with Licinius?", "Constantine I", "Nero", "Augustus", "Trajan"),
        ("Which event is traditionally used to mark the fall of the Western Roman Empire?", "Deposition of Romulus Augustulus in 476 CE", "Fall of Constantinople in 1453", "Battle of Actium", "Assassination of Julius Caesar"),
        ("Which Byzantine emperor commissioned the compilation of the Corpus Juris Civilis?", "Justinian I", "Constantine I", "Theodosius I", "Heraclius"),
        ("Which battle in 1066 led to the Norman conquest of England?", "Battle of Hastings", "Battle of Agincourt", "Battle of Waterloo", "Battle of Bosworth"),
        ("Which document was sealed by King John of England in 1215?", "Magna Carta", "Petition of Right", "Bill of Rights", "Act of Settlement"),
        ("Which pandemic devastated Europe in the 14th century?", "Black Death", "Spanish flu", "Cholera pandemic", "Smallpox epidemic"),
        ("Which Italian city is commonly regarded as a major centre of the Renaissance?", "Florence", "Venice", "Naples", "Milan"),
        ("Who painted the ceiling of the Sistine Chapel?", "Michelangelo", "Leonardo da Vinci", "Raphael", "Donatello"),
        ("Who wrote the book The Prince?", "Niccolò Machiavelli", "Thomas More", "Dante Alighieri", "Erasmus"),
        ("Which explorer reached India by sea around the Cape of Good Hope in 1498?", "Vasco da Gama", "Christopher Columbus", "Ferdinand Magellan", "James Cook"),
        ("Which event is commonly associated with the beginning of the Protestant Reformation in 1517?", "Martin Luther's Ninety-five Theses", "Council of Trent", "English Civil War", "Peace of Westphalia"),
        ("Which revolution began in Russia in 1917 and led to the fall of the Romanov monarchy?", "February Revolution", "Glorious Revolution", "American Revolution", "Cultural Revolution"),
        ("Who led the Bolsheviks during the October Revolution of 1917?", "Vladimir Lenin", "Joseph Stalin", "Leon Trotsky", "Alexander Kerensky"),
        ("Which treaty formally ended the state of war between Germany and the Allied Powers after World War I?", "Treaty of Versailles", "Treaty of Paris", "Treaty of Tordesillas", "Treaty of Utrecht"),
        ("Which event triggered the United States' entry into World War II?", "Attack on Pearl Harbor", "Invasion of Poland", "Battle of Britain", "Fall of France"),
        ("Which conference in 1945 brought together Roosevelt, Churchill and Stalin to discuss post-war Europe?", "Yalta Conference", "Bandung Conference", "Vienna Congress", "Berlin Conference"),
        ("Which country was divided into North and South after World War II along the 38th parallel?", "Korea", "Vietnam", "Germany", "China"),
        ("Who became the first Chancellor of a unified Germany in 1871?", "Otto von Bismarck", "Wilhelm II", "Frederick the Great", "Konrad Adenauer"),
        ("Which event is associated with the beginning of the French Revolution?", "Storming of the Bastille", "Battle of Waterloo", "Congress of Vienna", "Reign of Elizabeth I"),
        ("Which Haitian leader played a major role in the Haitian Revolution?", "Toussaint Louverture", "Simon Bolivar", "José de San Martín", "Emiliano Zapata"),
        ("Which invention is closely associated with Johannes Gutenberg?", "Movable-type printing press", "Steam engine", "Telephone", "Spinning jenny"),
        ("Who developed the theory of evolution by natural selection?", "Charles Darwin", "Gregor Mendel", "Louis Pasteur", "Isaac Newton"),
        ("Which movement in the United States fought for the abolition of slavery?", "Abolitionist movement", "Temperance movement", "Suffrage movement", "Progressive movement"),
        ("Which international organisation preceded the United Nations?", "League of Nations", "NATO", "European Union", "World Trade Organization"),
    ],

    "Hard": [
        ("Which Sumerian city-state is associated with the famous ruler Ur-Nammu and an early law code?", "Ur", "Uruk", "Lagash", "Eridu"),
        ("Which battle in 331 BCE resulted in Alexander the Great's decisive victory over Darius III?", "Battle of Gaugamela", "Battle of Issus", "Battle of Granicus", "Battle of Chaeronea"),
        ("Which Hellenistic dynasty ruled Egypt after the death of Alexander the Great?", "Ptolemaic dynasty", "Seleucid dynasty", "Antigonid dynasty", "Argead dynasty"),
        ("Which Roman emperor divided the administration of the Roman Empire between eastern and western regions during his reign?", "Diocletian", "Augustus", "Hadrian", "Marcus Aurelius"),
        ("Which battle in 732 is traditionally associated with Charles Martel's victory over an Umayyad force?", "Battle of Tours", "Battle of Hastings", "Battle of Poitiers in 1356", "Battle of Agincourt"),
        ("Which Abbasid caliph founded Baghdad as the new capital in 762 CE?", "Al-Mansur", "Harun al-Rashid", "Al-Ma'mun", "Al-Mutawakkil"),
        ("Which West African empire was famously ruled by Mansa Musa in the 14th century?", "Mali Empire", "Songhai Empire", "Ghana Empire", "Benin Empire"),
        ("Which Chinese dynasty was in power during the voyages of Zheng He?", "Ming dynasty", "Tang dynasty", "Song dynasty", "Qing dynasty"),
        ("Which Ottoman sultan captured Constantinople in 1453?", "Mehmed II", "Suleiman I", "Selim I", "Osman I"),
        ("Which treaty divided newly discovered lands outside Europe between Spain and Portugal in 1494?", "Treaty of Tordesillas", "Treaty of Utrecht", "Treaty of Westphalia", "Treaty of Paris"),
        ("Which event in 1648 helped establish the principle of state sovereignty in European international relations?", "Peace of Westphalia", "Congress of Vienna", "Treaty of Versailles", "Treaty of Utrecht"),
        ("Which English revolution resulted in the overthrow of James II in 1688?", "Glorious Revolution", "Puritan Revolution", "American Revolution", "French Revolution"),
        ("Which English political document was enacted in 1689 after the Glorious Revolution?", "English Bill of Rights", "Magna Carta", "Petition of Right", "Act of Union"),
        ("Which battle in 1757 established the East India Company's political influence in Bengal?", "Battle of Plassey", "Battle of Buxar", "Battle of Panipat", "Battle of Wandiwash"),
        ("Which treaty in 1763 ended the Seven Years' War between major European powers?", "Treaty of Paris", "Treaty of Versailles", "Treaty of Utrecht", "Treaty of Tordesillas"),
        ("Which philosopher wrote The Social Contract, an influential work associated with Enlightenment political thought?", "Jean-Jacques Rousseau", "John Locke", "Montesquieu", "Voltaire"),
        ("Which French revolutionary leader became associated with the Reign of Terror?", "Maximilien Robespierre", "Napoleon Bonaparte", "Louis XVI", "Charles de Gaulle"),
        ("Which event in 1815 ended Napoleon Bonaparte's rule following his return from exile?", "Battle of Waterloo", "Battle of Trafalgar", "Battle of Austerlitz", "Battle of Leipzig"),
        ("Which congress sought to restore the balance of power in Europe after the Napoleonic Wars?", "Congress of Vienna", "Congress of Berlin", "Congress of Aix-la-Chapelle", "Congress of Verona"),
        ("Which revolution in 1848 led to the overthrow of the July Monarchy in France?", "February Revolution", "October Revolution", "Glorious Revolution", "Bolshevik Revolution"),
        ("Which conflict was fought between the northern and southern states of the United States from 1861 to 1865?", "American Civil War", "War of 1812", "Spanish-American War", "Mexican-American War"),
        ("Which treaty ended the Russo-Japanese War in 1905?", "Treaty of Portsmouth", "Treaty of Brest-Litovsk", "Treaty of Nanking", "Treaty of Shimonoseki"),
        ("Which secret agreement of 1916 proposed dividing Ottoman territories between Britain and France?", "Sykes-Picot Agreement", "Treaty of Brest-Litovsk", "Balfour Declaration", "Potsdam Agreement"),
        ("Which treaty took Russia out of World War I in 1918?", "Treaty of Brest-Litovsk", "Treaty of Versailles", "Treaty of Trianon", "Treaty of Sevres"),
        ("Which economic crisis began with the Wall Street Crash of October 1929?", "Great Depression", "Long Depression", "Oil Crisis", "Asian Financial Crisis"),
        ("Which conference in 1944 established the framework for the post-war international monetary system?", "Bretton Woods Conference", "Yalta Conference", "Potsdam Conference", "Bandung Conference"),
        ("Which 1955 conference brought together Asian and African countries to promote cooperation and oppose colonialism?", "Bandung Conference", "Yalta Conference", "Vienna Congress", "Tehran Conference"),
        ("Which treaty established the European Economic Community in 1957?", "Treaty of Rome", "Treaty of Maastricht", "Treaty of Lisbon", "Treaty of Amsterdam"),
        ("Which agreement in 1978 created a framework for peace between Egypt and Israel?", "Camp David Accords", "Oslo Accords", "Dayton Agreement", "Helsinki Accords"),
        ("Which 1991 event formally dissolved the Soviet Union?", "Belovezha Accords", "Treaty of Rome", "Warsaw Pact", "Potsdam Agreement"),
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

            if not all(isinstance(x, str) and x.strip() for x in item):
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
                "Explore ancient civilizations, world revolutions, empires and major historical events."
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
        print("GK TOPIC 10 INSERTED SUCCESSFULLY")
        print("World History")
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
