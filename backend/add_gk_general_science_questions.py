
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 166
LESSON_TITLE = "General Science - Physics, Chemistry and Biology"
TOPIC = "General Knowledge"

BANK = {
    "Easy": [
        ("What is the SI unit of force?", "Newton", "Joule", "Watt", "Pascal"),
        ("Which planet is known as the Red Planet?", "Mars", "Venus", "Jupiter", "Mercury"),
        ("What is the chemical formula of water?", "H2O", "CO2", "O2", "NaCl"),
        ("Which gas do plants absorb during photosynthesis?", "Carbon dioxide", "Oxygen", "Nitrogen", "Hydrogen"),
        ("Which organ pumps blood throughout the human body?", "Heart", "Lungs", "Kidney", "Liver"),
        ("What is the boiling point of water at standard atmospheric pressure?", "100°C", "50°C", "75°C", "150°C"),
        ("Which vitamin is produced in the skin with sunlight exposure?", "Vitamin D", "Vitamin A", "Vitamin B12", "Vitamin K"),
        ("What is the nearest star to Earth?", "Sun", "Sirius", "Proxima Centauri", "Polaris"),
        ("Which gas is essential for human respiration?", "Oxygen", "Carbon dioxide", "Helium", "Neon"),
        ("What is the SI unit of electric current?", "Ampere", "Volt", "Ohm", "Watt"),
        ("Which part of a plant absorbs water from the soil?", "Roots", "Leaves", "Flowers", "Fruits"),
        ("What is the chemical symbol for gold?", "Au", "Ag", "Fe", "Cu"),
        ("Which organ is mainly responsible for filtering blood and producing urine?", "Kidneys", "Heart", "Stomach", "Lungs"),
        ("What is the basic structural and functional unit of life?", "Cell", "Tissue", "Organ", "Atom"),
        ("Which force pulls objects towards Earth?", "Gravity", "Friction", "Magnetism", "Tension"),
        ("Which gas makes up the largest percentage of Earth's atmosphere?", "Nitrogen", "Oxygen", "Carbon dioxide", "Hydrogen"),
        ("What is the freezing point of pure water at standard atmospheric pressure?", "0°C", "10°C", "32°C", "100°C"),
        ("Which blood cells help fight infections?", "White blood cells", "Red blood cells", "Platelets", "Plasma"),
        ("Which instrument measures temperature?", "Thermometer", "Barometer", "Ammeter", "Hygrometer"),
        ("What is the chemical symbol for iron?", "Fe", "Ir", "In", "I"),
        ("Which part of the human body controls most voluntary activities?", "Brain", "Heart", "Liver", "Pancreas"),
        ("Which energy source comes directly from the Sun?", "Solar energy", "Geothermal energy", "Tidal energy", "Nuclear energy"),
        ("Which gas is released by plants during photosynthesis?", "Oxygen", "Nitrogen", "Methane", "Hydrogen"),
        ("What is the SI unit of power?", "Watt", "Newton", "Joule", "Ampere"),
        ("Which substance is commonly called table salt?", "Sodium chloride", "Calcium carbonate", "Sodium bicarbonate", "Potassium nitrate"),
        ("How many chambers does the human heart have?", "Four", "Two", "Three", "Five"),
        ("Which vitamin is important for normal blood clotting?", "Vitamin K", "Vitamin C", "Vitamin D", "Vitamin B1"),
        ("What is the chemical symbol for oxygen?", "O", "Ox", "Og", "Om"),
        ("Which part of the eye controls the amount of light entering it?", "Iris", "Retina", "Cornea", "Optic nerve"),
        ("Which instrument is used to observe very small objects?", "Microscope", "Telescope", "Periscope", "Stethoscope"),
    ],

    "Medium": [
        ("What is the SI unit of electrical resistance?", "Ohm", "Ampere", "Volt", "Coulomb"),
        ("Which law states that pressure applied to an enclosed fluid is transmitted equally in all directions?", "Pascal's law", "Newton's law", "Ohm's law", "Hooke's law"),
        ("What is the approximate speed of light in vacuum?", "3 × 10^8 m/s", "3 × 10^6 m/s", "3 × 10^5 m/s", "3 × 10^10 m/s"),
        ("Which type of lens is used to correct myopia?", "Concave lens", "Convex lens", "Cylindrical lens only", "Bifocal lens only"),
        ("Which particle has a negative electric charge?", "Electron", "Proton", "Neutron", "Positron"),
        ("What is the pH of a neutral solution at 25°C?", "7", "0", "5", "14"),
        ("Which gas is commonly used in fire extinguishers?", "Carbon dioxide", "Oxygen", "Hydrogen", "Chlorine"),
        ("What is the chemical formula of baking soda?", "NaHCO3", "NaCl", "CaCO3", "H2SO4"),
        ("Which element has atomic number 1?", "Hydrogen", "Helium", "Lithium", "Oxygen"),
        ("Which process converts a liquid into a gas at its surface below the boiling point?", "Evaporation", "Condensation", "Freezing", "Sublimation"),
        ("Which cell organelle is known as the powerhouse of the cell?", "Mitochondrion", "Ribosome", "Nucleus", "Golgi apparatus"),
        ("Which molecule carries genetic information in most living organisms?", "DNA", "ATP", "Glucose", "Haemoglobin"),
        ("Which blood group is commonly called the universal red-cell donor type?", "O negative", "AB positive", "A positive", "B negative"),
        ("Which hormone helps regulate blood glucose levels by lowering them?", "Insulin", "Adrenaline", "Thyroxine", "Melatonin"),
        ("Which part of the brain is important for balance and coordination?", "Cerebellum", "Cerebrum", "Medulla", "Hypothalamus"),
        ("What is the functional unit of the kidney?", "Nephron", "Neuron", "Alveolus", "Villus"),
        ("Which plant tissue transports water and minerals from roots?", "Xylem", "Phloem", "Epidermis", "Cambium"),
        ("Which enzyme in saliva begins the digestion of starch?", "Amylase", "Pepsin", "Lipase", "Trypsin"),
        ("Which vitamin deficiency causes scurvy?", "Vitamin C", "Vitamin A", "Vitamin D", "Vitamin B12"),
        ("Which gas is primarily responsible for the greenhouse effect among the following choices?", "Carbon dioxide", "Oxygen", "Argon", "Helium"),
        ("Which layer of Earth's atmosphere contains most weather phenomena?", "Troposphere", "Stratosphere", "Mesosphere", "Thermosphere"),
        ("What is the SI unit of frequency?", "Hertz", "Decibel", "Joule", "Tesla"),
        ("Which phenomenon causes the bending of light when it passes from one medium to another?", "Refraction", "Reflection", "Diffraction", "Interference"),
        ("Which metal is liquid at ordinary room temperature?", "Mercury", "Iron", "Aluminium", "Copper"),
        ("Which acid is present in the human stomach?", "Hydrochloric acid", "Sulfuric acid", "Nitric acid", "Acetic acid"),
        ("What is the chemical formula of methane?", "CH4", "C2H6", "CO2", "NH3"),
        ("Which blood component is mainly responsible for clotting?", "Platelets", "Red blood cells", "White blood cells", "Plasma proteins only"),
        ("Which disease is caused by the deficiency of iodine?", "Goitre", "Scurvy", "Rickets", "Anaemia"),
        ("Which part of a flower produces pollen grains?", "Anther", "Stigma", "Ovary", "Sepal"),
        ("Which type of reproduction involves only one parent?", "Asexual reproduction", "Sexual reproduction", "Cross-pollination", "External fertilisation"),
    ],

    "Hard": [
        ("Which principle explains why a body immersed in a fluid experiences an upward buoyant force?", "Archimedes' principle", "Bernoulli's principle", "Pascal's law", "Coulomb's law"),
        ("What is the dimensional formula of force?", "MLT^-2", "ML^2T^-2", "ML^-1T^-2", "M^0LT^-1"),
        ("Which law relates the voltage, current and resistance in an electrical circuit?", "Ohm's law", "Faraday's law", "Lenz's law", "Kepler's law"),
        ("What is the SI unit of magnetic flux?", "Weber", "Tesla", "Henry", "Farad"),
        ("Which phenomenon is responsible for the blue colour of the daytime sky?", "Rayleigh scattering", "Total internal reflection", "Diffraction", "Dispersion"),
        ("Which law states that the induced current opposes the change that produces it?", "Lenz's law", "Ohm's law", "Newton's first law", "Boyle's law"),
        ("What is the approximate value of the universal gravitational constant?", "6.67 × 10^-11 N m²/kg²", "9.8 N/kg", "3 × 10^8 m/s", "1.6 × 10^-19 C"),
        ("Which thermodynamic law introduces the concept of entropy?", "Second law of thermodynamics", "Zeroth law of thermodynamics", "First law of thermodynamics", "Newton's law of cooling"),
        ("Which type of semiconductor is formed by doping silicon with a pentavalent impurity?", "N-type", "P-type", "Intrinsic", "Insulating"),
        ("Which electromagnetic radiation has the highest frequency among these?", "Gamma rays", "Microwaves", "Infrared", "Radio waves"),
        ("Which quantum number determines the shape of an atomic orbital?", "Azimuthal quantum number", "Principal quantum number", "Magnetic quantum number", "Spin quantum number"),
        ("Which principle states that no two electrons in an atom can have the same four quantum numbers?", "Pauli exclusion principle", "Aufbau principle", "Hund's rule", "Heisenberg uncertainty principle"),
        ("What is the oxidation state of chromium in potassium dichromate (K2Cr2O7)?", "+6", "+3", "+4", "+7"),
        ("Which type of chemical bond involves the sharing of electron pairs?", "Covalent bond", "Ionic bond", "Metallic bond", "Hydrogen bond"),
        ("Which gas is produced at the cathode during the electrolysis of acidified water?", "Hydrogen", "Oxygen", "Chlorine", "Nitrogen"),
        ("Which catalyst is commonly used in the Haber process for ammonia production?", "Iron", "Platinum", "Nickel", "Copper"),
        ("Which functional group is present in alcohols?", "Hydroxyl group", "Carboxyl group", "Aldehyde group", "Amino group"),
        ("What is the hybridisation of carbon in methane?", "sp3", "sp2", "sp", "dsp2"),
        ("Which law states that equal volumes of gases at the same temperature and pressure contain equal numbers of molecules?", "Avogadro's law", "Boyle's law", "Charles's law", "Dalton's law"),
        ("Which organelle modifies, sorts and packages proteins for transport?", "Golgi apparatus", "Lysosome", "Mitochondrion", "Centrosome"),
        ("During which stage of mitosis do chromosomes align at the cell's equatorial plane?", "Metaphase", "Prophase", "Anaphase", "Telophase"),
        ("Which enzyme joins Okazaki fragments during DNA replication?", "DNA ligase", "DNA helicase", "DNA primase", "RNA polymerase"),
        ("Which type of RNA carries amino acids to the ribosome during protein synthesis?", "Transfer RNA", "Messenger RNA", "Ribosomal RNA", "Small nuclear RNA"),
        ("Which part of the nephron is primarily responsible for ultrafiltration of blood?", "Glomerulus", "Loop of Henle", "Collecting duct", "Distal convoluted tubule"),
        ("Which hormone is primarily responsible for increasing blood calcium levels?", "Parathyroid hormone", "Insulin", "Calcitonin", "Thyroxine"),
        ("Which blood vessel carries oxygenated blood from the lungs to the heart?", "Pulmonary vein", "Pulmonary artery", "Aorta", "Vena cava"),
        ("Which ecological pyramid is always upright?", "Pyramid of energy", "Pyramid of numbers", "Pyramid of biomass", "All pyramids of numbers"),
        ("Which process converts atmospheric nitrogen into ammonia through biological activity?", "Nitrogen fixation", "Nitrification", "Denitrification", "Transpiration"),
        ("Which genetic condition is caused by an extra copy of chromosome 21?", "Down syndrome", "Turner syndrome", "Klinefelter syndrome", "Cri-du-chat syndrome"),
        ("Which enzyme unwinds the DNA double helix during DNA replication?", "DNA helicase", "DNA ligase", "DNA polymerase", "RNA primase"),
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
                raise ValueError(f"Invalid question format: {difficulty} #{index}")

            question, correct, *wrong = item
            options = [correct] + wrong

            if not all(isinstance(x, str) and x.strip() for x in item):
                raise ValueError(f"Empty field: {difficulty} #{index}")

            if len(set(options)) != 4:
                raise ValueError(f"Duplicate options: {difficulty} #{index}")

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
                "Study fundamental concepts in physics, chemistry and biology."
            ))
        elif existing != (LESSON_TITLE, TOPIC):
            raise ValueError(
                f"Lesson ID {LESSON_ID} is occupied by {existing}"
            )

        for difficulty, questions in BANK.items():
            cursor.execute("""
                SELECT id FROM quizzes
                WHERE lesson_id = ? AND difficulty = ?
            """, (LESSON_ID, difficulty))

            quiz_rows = cursor.fetchall()

            if len(quiz_rows) > 1:
                raise ValueError(f"Multiple {difficulty} quizzes found.")

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
        print("GK TOPIC 6 INSERTED SUCCESSFULLY")
        print("General Science")
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
