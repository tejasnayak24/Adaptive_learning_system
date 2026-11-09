
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 179
LESSON_TITLE = "Defence, Space Research, Indian Armed Forces and National Security"
TOPIC = "General Knowledge"

BANK = {
    "Easy": [
        ("Who is the Supreme Commander of the Indian Armed Forces?", "President of India", "Prime Minister", "Defence Minister", "Chief of Defence Staff"),
        ("Which organisation is responsible for India's space programme?", "ISRO", "DRDO", "HAL", "BARC"),
        ("What does ISRO stand for?", "Indian Space Research Organisation", "International Space Research Office", "Indian Satellite Research Organisation", "International Scientific Research Organisation"),
        ("Where is ISRO headquartered?", "Bengaluru", "New Delhi", "Mumbai", "Hyderabad"),
        ("Who is widely regarded as the father of the Indian space programme?", "Vikram Sarabhai", "Homi J. Bhabha", "A. P. J. Abdul Kalam", "Satish Dhawan"),
        ("What was India's first satellite?", "Aryabhata", "Rohini", "INSAT-1A", "Chandrayaan-1"),
        ("In which year was Aryabhata launched?", "1975", "1980", "1984", "1990"),
        ("Which organisation develops defence technologies for India's armed forces?", "DRDO", "ISRO", "UGC", "ICAR"),
        ("What does DRDO stand for?", "Defence Research and Development Organisation", "Department of Research and Defence Operations", "Defence Resources Development Office", "Directorate of Research and Defence Organisation"),
        ("Where is DRDO headquartered?", "New Delhi", "Bengaluru", "Chennai", "Kolkata"),
        ("Which branch of the armed forces protects India's maritime interests?", "Indian Navy", "Indian Army", "Indian Air Force", "Border Security Force"),
        ("Which branch primarily protects India's airspace?", "Indian Air Force", "Indian Navy", "Indian Army", "Indian Coast Guard"),
        ("Which branch is primarily responsible for land-based military operations?", "Indian Army", "Indian Navy", "Indian Air Force", "Coast Guard"),
        ("When is Indian Army Day celebrated?", "15 January", "26 January", "15 August", "4 December"),
        ("When is Indian Navy Day celebrated?", "4 December", "15 January", "8 October", "26 November"),
        ("When is Indian Air Force Day celebrated?", "8 October", "4 December", "15 January", "2 October"),
        ("Which is India's highest wartime gallantry award?", "Param Vir Chakra", "Ashoka Chakra", "Kirti Chakra", "Shaurya Chakra"),
        ("Which is India's highest peacetime gallantry award?", "Ashoka Chakra", "Param Vir Chakra", "Vir Chakra", "Sena Medal"),
        ("Who was the first Indian citizen to travel into space?", "Rakesh Sharma", "Kalpana Chawla", "Sunita Williams", "Vikram Sarabhai"),
        ("In which year did Rakesh Sharma travel into space?", "1984", "1975", "1990", "2001"),
        ("Which Indian mission was the country's first mission to Mars?", "Mars Orbiter Mission", "Chandrayaan-1", "Chandrayaan-2", "Aditya-L1"),
        ("What is the popular name of India's Mars Orbiter Mission?", "Mangalyaan", "Gaganyaan", "NavIC", "Aryabhata"),
        ("Which mission made India the first country to land near the Moon's south polar region?", "Chandrayaan-3", "Chandrayaan-1", "Mangalyaan", "Aditya-L1"),
        ("Which Indian launch vehicle is commonly known as the workhorse of ISRO?", "PSLV", "SLV-3", "ASLV", "Sounding Rocket"),
        ("What does PSLV stand for?", "Polar Satellite Launch Vehicle", "Primary Space Launch Vehicle", "Public Satellite Launch Vehicle", "Polar Science Launch Vehicle"),
        ("Which Indian mission is designed to demonstrate human spaceflight capability?", "Gaganyaan", "Mangalyaan", "Chandrayaan-1", "Astrosat"),
        ("Which force is responsible for guarding India's international borders with Pakistan and Bangladesh?", "Border Security Force", "Central Industrial Security Force", "National Security Guard", "National Disaster Response Force"),
        ("What does BSF stand for?", "Border Security Force", "Basic Security Force", "Border Safety Federation", "Bureau of Security Forces"),
        ("Which force is commonly known as the Black Cats?", "National Security Guard", "Border Security Force", "Central Reserve Police Force", "Indian Coast Guard"),
        ("Which ministry is primarily responsible for India's defence administration?", "Ministry of Defence", "Ministry of Home Affairs", "Ministry of External Affairs", "Ministry of Finance"),
    ],

    "Medium": [
        ("Who was the first Chief of Defence Staff of India?", "General Bipin Rawat", "General Manoj Pande", "Admiral Karambir Singh", "Air Chief Marshal R. K. S. Bhadauria"),
        ("What is the primary role of the Chief of Defence Staff?", "Promoting jointness and integration among the armed forces", "Commanding every army unit directly", "Managing India's space programme", "Regulating international trade"),
        ("Which organisation is responsible for India's nuclear research programme?", "Department of Atomic Energy", "Indian Council of Agricultural Research", "University Grants Commission", "National Highways Authority of India"),
        ("Where is the headquarters of the Department of Atomic Energy located?", "Mumbai", "New Delhi", "Bengaluru", "Chennai"),
        ("Who is known as the father of India's nuclear programme?", "Homi J. Bhabha", "Vikram Sarabhai", "C. V. Raman", "Satyendra Nath Bose"),
        ("Which Indian satellite navigation system is also known as NavIC?", "Indian Regional Navigation Satellite System", "Global Positioning System", "Galileo", "GLONASS"),
        ("What does NavIC stand for?", "Navigation with Indian Constellation", "National Vehicle Information Code", "Navigation in Central India", "National Integrated Communication"),
        ("Which Indian mission studies the Sun from the Sun-Earth L1 point?", "Aditya-L1", "Chandrayaan-3", "Mangalyaan", "Astrosat"),
        ("What is the main purpose of the Chandrayaan-1 mission?", "Study the Moon from lunar orbit", "Study the planet Mars", "Observe the Sun from L1", "Carry astronauts to the International Space Station"),
        ("Which launch vehicle placed Chandrayaan-3 on its initial Earth-bound trajectory?", "LVM3", "PSLV-C11", "SLV-3", "ASLV-D4"),
        ("What does LVM3 stand for?", "Launch Vehicle Mark-3", "Lunar Vehicle Mission-3", "Low Velocity Module-3", "Launch Vehicle Model-3"),
        ("Which Indian space mission was dedicated to studying the X-ray universe?", "XPoSat", "Mangalyaan", "Gaganyaan", "NavIC"),
        ("Which organisation is responsible for developing India's indigenous light combat aircraft Tejas?", "Aeronautical Development Agency", "National Aerospace Laboratories alone", "Indian Coast Guard", "Bharat Sanchar Nigam Limited"),
        ("Which public sector company manufactures aircraft and helicopters for India's defence sector?", "Hindustan Aeronautics Limited", "Bharat Electronics Limited", "Indian Oil Corporation", "Steel Authority of India"),
        ("What does HAL stand for?", "Hindustan Aeronautics Limited", "Heavy Aircraft Logistics", "High Altitude Laboratory", "Hindustan Army Logistics"),
        ("Which company is strongly associated with the manufacture of defence electronics in India?", "Bharat Electronics Limited", "Food Corporation of India", "National Thermal Power Corporation", "Life Insurance Corporation"),
        ("What does BEL stand for?", "Bharat Electronics Limited", "Bureau of Engineering Logistics", "Basic Electronics Laboratory", "Bharat Energy Limited"),
        ("Which Indian military command is headquartered in Thiruvananthapuram?", "Southern Air Command", "Western Air Command", "Eastern Air Command", "Central Air Command"),
        ("Which Indian naval command is headquartered in Mumbai?", "Western Naval Command", "Eastern Naval Command", "Southern Naval Command", "Northern Naval Command"),
        ("Where is the headquarters of the Indian Army's Northern Command?", "Udhampur", "Pune", "Lucknow", "Kolkata"),
        ("Which force is responsible for security at major airports and important industrial installations?", "Central Industrial Security Force", "Border Security Force", "Indo-Tibetan Border Police", "National Security Guard"),
        ("What does CISF stand for?", "Central Industrial Security Force", "Central Indian Safety Federation", "Civil Infrastructure Security Force", "Central Intelligence Security Force"),
        ("Which force primarily guards the Indo-China border in high-altitude regions?", "Indo-Tibetan Border Police", "Central Industrial Security Force", "National Security Guard", "Railway Protection Force"),
        ("What does ITBP stand for?", "Indo-Tibetan Border Police", "Indian Territorial Border Patrol", "International Tibetan Border Police", "Indian Tactical Border Protection"),
        ("Which force is primarily responsible for assisting state police in maintaining internal security and dealing with serious law-and-order situations?", "Central Reserve Police Force", "Indian Coast Guard", "Indian Navy", "Airports Authority of India"),
        ("What does CRPF stand for?", "Central Reserve Police Force", "Central Regional Protection Force", "Civil Reserve Patrol Federation", "Central Railway Police Federation"),
        ("Which Indian organisation investigates specified offences affecting national security and terrorism?", "National Investigation Agency", "NABARD", "SEBI", "National Highways Authority of India"),
        ("What does NIA stand for?", "National Investigation Agency", "National Intelligence Association", "National Internal Administration", "New Investigation Authority"),
        ("Which organisation is responsible for maritime law enforcement and search-and-rescue operations in India's maritime zones?", "Indian Coast Guard", "Central Reserve Police Force", "National Security Guard", "Indo-Tibetan Border Police"),
        ("Which Indian military exercise is conducted by the Army, Navy and Air Force together?", "Tri-service exercise", "Bilateral trade exercise", "Civil aviation exercise", "Agricultural field exercise"),
    ],

    "Hard": [
        ("Which committee recommended the creation of the post of Chief of Defence Staff following the Kargil conflict?", "Kargil Review Committee", "Sarkaria Commission", "Mandal Commission", "Punchhi Commission"),
        ("Which committee reviewed India's national security system after the Kargil conflict?", "Kargil Review Committee", "Narasimham Committee", "Kelkar Committee", "Shah Commission"),
        ("Which body is the apex decision-making body for India's nuclear command structure?", "Political Council of the Nuclear Command Authority", "National Security Guard", "Defence Research and Development Organisation", "Election Commission"),
        ("Who chairs the Political Council of India's Nuclear Command Authority?", "Prime Minister of India", "President of India", "Defence Secretary", "Chief of Defence Staff"),
        ("What is the primary purpose of India's Strategic Forces Command?", "Managing the country's strategic nuclear forces", "Managing civilian airports", "Conducting space exploration", "Regulating international shipping"),
        ("Which organisation is responsible for India's nuclear command and control arrangements?", "Nuclear Command Authority", "National Disaster Management Authority", "National Human Rights Commission", "Central Vigilance Commission"),
        ("Which missile family includes the Agni series?", "Ballistic missiles", "Anti-submarine torpedoes", "Surface-to-air guns", "Unmanned underwater vehicles"),
        ("Which Indian missile is an example of a surface-to-air missile system developed by DRDO?", "Akash", "Agni-V", "Prithvi-II", "Dhanush"),
        ("Which missile is part of India's indigenous anti-tank guided missile development programme?", "Nag", "Agni", "Prithvi", "Dhanush"),
        ("Which organisation developed the Akash missile system?", "DRDO", "ISRO", "NABARD", "BHEL"),
        ("Which Indian defence programme is associated with the development of the Arjun main battle tank?", "DRDO", "ISRO", "ICAR", "UGC"),
        ("Which research centre is associated with the development of India's main battle tank Arjun?", "Combat Vehicles Research and Development Establishment", "Vikram Sarabhai Space Centre", "National Aerospace Laboratories", "Central Food Technological Research Institute"),
        ("Which Indian organisation is responsible for the development of the Tejas light combat aircraft?", "Aeronautical Development Agency", "National Security Guard", "Indian Coast Guard", "National Investigation Agency"),
        ("Which organisation is responsible for India's satellite launch operations and space technology development?", "Indian Space Research Organisation", "Bharat Electronics Limited", "Hindustan Aeronautics Limited", "National Investigation Agency"),
        ("Which ISRO centre is responsible for developing launch vehicle technology?", "Vikram Sarabhai Space Centre", "Satish Dhawan Space Centre", "National Remote Sensing Centre", "Indian Institute of Remote Sensing"),
        ("Where is the Satish Dhawan Space Centre located?", "Sriharikota", "Bengaluru", "Thiruvananthapuram", "Ahmedabad"),
        ("Which ISRO centre is primarily associated with satellite development?", "U. R. Rao Satellite Centre", "Vikram Sarabhai Space Centre", "Satish Dhawan Space Centre", "Liquid Propulsion Systems Centre"),
        ("Which Indian mission was the first dedicated Indian astronomy mission covering multiple wavelengths?", "AstroSat", "Chandrayaan-1", "Mangalyaan", "Gaganyaan"),
        ("What is the primary scientific objective of the XPoSat mission?", "Studying X-ray polarisation", "Mapping ocean currents", "Measuring monsoon rainfall", "Studying Earth's magnetic poles only"),
        ("Which space mission is designed to demonstrate India's capability for human spaceflight?", "Gaganyaan", "Aditya-L1", "AstroSat", "RISAT"),
        ("What is the primary purpose of a geostationary satellite?", "Appearing stationary relative to a point on Earth's equator", "Orbiting only over the polar regions", "Landing on the Moon", "Travelling beyond the Solar System"),
        ("Which type of orbit is commonly used for Earth observation satellites that pass over different parts of Earth?", "Polar orbit", "Geostationary orbit only", "Lunar orbit", "Solar escape trajectory"),
        ("Which Indian agency is responsible for operating the Indian National Centre for Ocean Information Services?", "Ministry of Earth Sciences", "Ministry of Defence alone", "Ministry of Railways", "Ministry of Commerce"),
        ("Which organisation provides ocean information services such as tsunami advisories in India?", "INCOIS", "NABARD", "SEBI", "CPCB"),
        ("What does INCOIS stand for?", "Indian National Centre for Ocean Information Services", "International Network for Coastal Information Systems", "Indian National Council of Industrial Safety", "Institute of National Climate Observation and Information Studies"),
        ("Which force is responsible for protecting India's coastline and maritime interests alongside the Navy?", "Indian Coast Guard", "Central Industrial Security Force", "Indo-Tibetan Border Police", "Central Reserve Police Force"),
        ("Which act provides the legal basis for the National Investigation Agency in India?", "National Investigation Agency Act, 2008", "Armed Forces Act, 1950", "Official Secrets Act, 1923", "Disaster Management Act, 2005"),
        ("Which organisation is India's specialised counter-terrorism force commonly known as the Black Cats?", "National Security Guard", "Central Reserve Police Force", "Border Security Force", "Indian Coast Guard"),
        ("Which ministry administers the Central Armed Police Forces in India?", "Ministry of Home Affairs", "Ministry of External Affairs", "Ministry of Finance", "Ministry of Education"),
        ("Which constitutional office holds the position of Supreme Commander of the Indian Armed Forces?", "President of India", "Chief of Defence Staff", "Defence Secretary", "Prime Minister's Principal Secretary"),
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
                "Learn about India's armed forces, defence research, space missions, national security organisations and strategic institutions."
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
        print("GK TOPIC 19 INSERTED SUCCESSFULLY")
        print("Defence, Space Research, Indian Armed Forces and National Security")
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
