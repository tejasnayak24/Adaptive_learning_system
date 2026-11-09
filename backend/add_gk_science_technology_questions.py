
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 172
LESSON_TITLE = "Science and Technology - Space, Inventions, Computers and Discoveries"
TOPIC = "General Knowledge"

BANK = {
    "Easy": [
        ("Which planet is known as the Red Planet?", "Mars", "Venus", "Jupiter", "Mercury"),
        ("Which is the largest planet in our solar system?", "Jupiter", "Saturn", "Earth", "Neptune"),
        ("Which star is at the centre of our solar system?", "Sun", "Sirius", "Polaris", "Proxima Centauri"),
        ("What is the natural satellite of Earth?", "Moon", "Mars", "Sun", "Venus"),
        ("Which instrument is used to observe distant stars and planets?", "Telescope", "Microscope", "Periscope", "Barometer"),
        ("Who is widely credited with inventing the telephone?", "Alexander Graham Bell", "Thomas Edison", "James Watt", "Nikola Tesla"),
        ("Who invented the practical incandescent light bulb?", "Thomas Edison", "Isaac Newton", "Galileo Galilei", "Charles Babbage"),
        ("Which device is known as the brain of a computer?", "CPU", "Monitor", "Keyboard", "Mouse"),
        ("What does CPU stand for?", "Central Processing Unit", "Computer Personal Unit", "Central Program Utility", "Control Processing User"),
        ("Which of these is an input device?", "Keyboard", "Monitor", "Printer", "Speaker"),
        ("Which of these is an output device?", "Monitor", "Mouse", "Keyboard", "Scanner"),
        ("What does WWW stand for?", "World Wide Web", "World Web Window", "Wide World Website", "Web World Wide"),
        ("Which gas do plants absorb during photosynthesis?", "Carbon dioxide", "Oxygen", "Nitrogen", "Hydrogen"),
        ("Which organ pumps blood throughout the human body?", "Heart", "Lungs", "Brain", "Kidneys"),
        ("Which vitamin is produced in the skin with sunlight exposure?", "Vitamin D", "Vitamin C", "Vitamin B12", "Vitamin K"),
        ("What is the chemical symbol for water?", "H2O", "CO2", "O2", "NaCl"),
        ("Which force pulls objects towards Earth?", "Gravity", "Magnetism", "Friction", "Electricity"),
        ("Which scientist formulated the laws of motion?", "Isaac Newton", "Albert Einstein", "Galileo Galilei", "Marie Curie"),
        ("Which scientist developed the theory of relativity?", "Albert Einstein", "Isaac Newton", "Charles Darwin", "Niels Bohr"),
        ("Which Indian space agency is known as ISRO?", "Indian Space Research Organisation", "Indian Scientific Research Office", "International Space Research Organisation", "Indian Satellite Research Office"),
        ("What was India's first satellite?", "Aryabhata", "Rohini", "INSAT-1A", "Chandrayaan-1"),
        ("Which Indian mission successfully landed near the Moon's south polar region in 2023?", "Chandrayaan-3", "Chandrayaan-1", "Mangalyaan", "Aditya-L1"),
        ("Which planet is famous for its prominent ring system?", "Saturn", "Mercury", "Mars", "Earth"),
        ("Which technology allows wireless communication over short distances using radio waves?", "Bluetooth", "Ethernet", "Fibre optics", "HDMI"),
        ("What does AI stand for?", "Artificial Intelligence", "Automated Internet", "Advanced Information", "Applied Interface"),
        ("Which company developed the Windows operating system?", "Microsoft", "Apple", "Google", "IBM"),
        ("Which part of a computer permanently stores data even when power is switched off?", "Hard drive or SSD", "RAM", "Cache", "CPU register"),
        ("Which scientist is known for discovering penicillin?", "Alexander Fleming", "Louis Pasteur", "Edward Jenner", "Robert Koch"),
        ("What is the basic unit of life?", "Cell", "Tissue", "Organ", "Atom"),
        ("Which device converts sound into electrical signals for recording?", "Microphone", "Speaker", "Monitor", "Projector"),
    ],

    "Medium": [
        ("Who is known as the father of the computer?", "Charles Babbage", "Alan Turing", "John von Neumann", "Blaise Pascal"),
        ("Who is often called the first computer programmer?", "Ada Lovelace", "Grace Hopper", "Katherine Johnson", "Marie Curie"),
        ("Which scientist proposed the three laws of planetary motion?", "Johannes Kepler", "Galileo Galilei", "Isaac Newton", "Copernicus"),
        ("Who proposed the heliocentric model that placed the Sun at the centre of the planetary system?", "Nicolaus Copernicus", "Ptolemy", "Aristotle", "Tycho Brahe"),
        ("What is the approximate speed of light in vacuum?", "300,000 km/s", "30,000 km/s", "150,000 km/s", "3,000 km/s"),
        ("Which layer of the atmosphere contains most of the ozone layer?", "Stratosphere", "Troposphere", "Mesosphere", "Thermosphere"),
        ("Which particle has a negative electric charge?", "Electron", "Proton", "Neutron", "Positron"),
        ("Which particle has no electric charge?", "Neutron", "Proton", "Electron", "Positron"),
        ("What is the SI unit of electric current?", "Ampere", "Volt", "Ohm", "Watt"),
        ("What is the SI unit of force?", "Newton", "Joule", "Pascal", "Watt"),
        ("Which gas is most abundant in Earth's atmosphere?", "Nitrogen", "Oxygen", "Carbon dioxide", "Argon"),
        ("Which blood cells help the body fight infections?", "White blood cells", "Red blood cells", "Platelets", "Plasma cells only"),
        ("Which part of the cell contains most of its genetic material?", "Nucleus", "Ribosome", "Cell membrane", "Cytoplasm"),
        ("Which molecule carries genetic information in most living organisms?", "DNA", "ATP", "Glucose", "Lipid"),
        ("Which scientist is associated with the theory of evolution by natural selection?", "Charles Darwin", "Gregor Mendel", "Louis Pasteur", "Robert Hooke"),
        ("Who is known for pioneering work on radioactivity and winning Nobel Prizes in two scientific fields?", "Marie Curie", "Rosalind Franklin", "Dorothy Hodgkin", "Lise Meitner"),
        ("Which Indian scientist won the Nobel Prize in Physics in 1930 for work on light scattering?", "C. V. Raman", "Homi J. Bhabha", "Satyendra Nath Bose", "Vikram Sarabhai"),
        ("What was the name of India's first Mars mission?", "Mars Orbiter Mission", "Chandrayaan-1", "AstroSat", "Aditya-L1"),
        ("In which year did India's Mars Orbiter Mission enter Mars orbit?", "2014", "2012", "2015", "2016"),
        ("Which Indian mission studies the Sun from the Sun-Earth L1 point?", "Aditya-L1", "Chandrayaan-3", "Mangalyaan", "AstroSat"),
        ("What does GPS stand for?", "Global Positioning System", "General Positioning Service", "Global Processing Satellite", "Geographical Programming System"),
        ("Which technology is used to create three-dimensional objects layer by layer?", "3D printing", "Laser scanning", "Cloud computing", "Blockchain"),
        ("What is the main function of an operating system?", "Manage computer hardware and software resources", "Create only presentations", "Provide internet access only", "Store files permanently without hardware"),
        ("Which programming language was named after the comedy group Monty Python?", "Python", "Java", "C", "Ruby"),
        ("What does URL stand for?", "Uniform Resource Locator", "Universal Reference Link", "Unified Resource Language", "Uniform Routing Location"),
        ("Which type of memory is volatile?", "RAM", "ROM", "Flash memory", "SSD"),
        ("What does LAN stand for?", "Local Area Network", "Large Access Network", "Long Area Node", "Linked Application Network"),
        ("Which technology enables computers to learn patterns from data?", "Machine learning", "Word processing", "File compression", "Screen mirroring"),
        ("Which telescope was launched into space in December 2021 to study the universe in infrared?", "James Webb Space Telescope", "Hubble Space Telescope", "Chandra X-ray Observatory", "Kepler Space Telescope"),
        ("Which was the first artificial satellite launched into space?", "Sputnik 1", "Explorer 1", "Vanguard 1", "Luna 1"),
    ],

    "Hard": [
        ("Which mathematician is credited with developing the concept of the Turing machine?", "Alan Turing", "Charles Babbage", "John von Neumann", "Claude Shannon"),
        ("Who introduced the term 'artificial intelligence' at the Dartmouth workshop proposal?", "John McCarthy", "Alan Turing", "Marvin Minsky", "Geoffrey Hinton"),
        ("Which scientist formulated the uncertainty principle?", "Werner Heisenberg", "Niels Bohr", "Erwin Schrödinger", "Max Planck"),
        ("Who proposed the wave equation of quantum mechanics?", "Erwin Schrödinger", "Werner Heisenberg", "Paul Dirac", "Max Born"),
        ("Which physicist discovered the neutron in 1932?", "James Chadwick", "Ernest Rutherford", "J. J. Thomson", "Niels Bohr"),
        ("Which scientist discovered the electron?", "J. J. Thomson", "James Chadwick", "Ernest Rutherford", "Robert Millikan"),
        ("Which experiment is associated with the discovery of the atomic nucleus?", "Gold foil experiment", "Millikan oil-drop experiment", "Michelson-Morley experiment", "Double-slit experiment"),
        ("Who discovered the law of electromagnetic induction?", "Michael Faraday", "James Clerk Maxwell", "André-Marie Ampère", "Georg Ohm"),
        ("Which scientist unified electricity and magnetism through a set of equations?", "James Clerk Maxwell", "Michael Faraday", "Isaac Newton", "Heinrich Hertz"),
        ("What is the SI unit of magnetic flux?", "Weber", "Tesla", "Henry", "Farad"),
        ("Which law states that the pressure of a gas is inversely proportional to its volume at constant temperature?", "Boyle's law", "Charles's law", "Avogadro's law", "Ohm's law"),
        ("Which principle explains why a ship floats in water?", "Archimedes' principle", "Pascal's law", "Bernoulli's principle", "Newton's third law"),
        ("Which scientist developed the first successful polio vaccine?", "Jonas Salk", "Edward Jenner", "Louis Pasteur", "Alexander Fleming"),
        ("Who developed the first widely used smallpox vaccine?", "Edward Jenner", "Jonas Salk", "Robert Koch", "Joseph Lister"),
        ("Which scientist is credited with discovering the structure of penicillin?", "Dorothy Crowfoot Hodgkin", "Marie Curie", "Rosalind Franklin", "Barbara McClintock"),
        ("Which technique is commonly used to amplify specific DNA sequences?", "Polymerase Chain Reaction", "Gel electrophoresis", "Chromatography", "Centrifugation"),
        ("Who developed the polymerase chain reaction technique?", "Kary Mullis", "James Watson", "Francis Crick", "Frederick Sanger"),
        ("Which organelle is primarily responsible for producing ATP in eukaryotic cells?", "Mitochondrion", "Golgi apparatus", "Lysosome", "Ribosome"),
        ("Which enzyme unwinds the DNA double helix during replication?", "Helicase", "Ligase", "Amylase", "Lipase"),
        ("Which Indian scientist is associated with the Bose-Einstein statistics?", "Satyendra Nath Bose", "C. V. Raman", "Meghnad Saha", "Homi J. Bhabha"),
        ("Who is known as the father of India's space programme?", "Vikram Sarabhai", "A. P. J. Abdul Kalam", "Homi J. Bhabha", "Satish Dhawan"),
        ("Which Indian launch vehicle is designed to carry heavier payloads into geostationary transfer orbit?", "LVM3", "SSLV", "Sounding Rocket", "Rohini-75"),
        ("What is the full form of PSLV?", "Polar Satellite Launch Vehicle", "Primary Space Launch Vehicle", "Payload Satellite Launch Vehicle", "Polar Space Landing Vehicle"),
        ("Which mission made India the first country to land near the Moon's south polar region?", "Chandrayaan-3", "Chandrayaan-2", "Luna 25", "Apollo 11"),
        ("Which spacecraft carried the first humans to land on the Moon?", "Apollo 11", "Apollo 8", "Gemini 7", "Vostok 1"),
        ("Who was the first human to travel into outer space?", "Yuri Gagarin", "Neil Armstrong", "Buzz Aldrin", "Alan Shepard"),
        ("Which space telescope discovered thousands of exoplanet candidates using the transit method?", "Kepler Space Telescope", "Hubble Space Telescope", "Chandra X-ray Observatory", "Spitzer Space Telescope"),
        ("What does the term 'exoplanet' mean?", "A planet outside our solar system", "A planet without an atmosphere", "A moon orbiting a planet", "A star that has collapsed"),
        ("Which technology underlies most modern cryptocurrencies by maintaining a distributed ledger?", "Blockchain", "Cloud storage", "Virtual reality", "Optical character recognition"),
        ("Which cryptographic technique uses a pair of public and private keys?", "Asymmetric cryptography", "Symmetric cryptography", "Hashing only", "Data compression"),
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
                "Learn about scientific discoveries, space exploration, inventions, computers and modern technology."
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
        print("GK TOPIC 12 INSERTED SUCCESSFULLY")
        print("Science and Technology")
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
