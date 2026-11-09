import sqlite3
from pathlib import Path

DATABASE_PATH = (
    Path(__file__).resolve().parent.parent
    / "adaptive_learning.db"
)

TARGET_QUESTIONS = 30

QUESTION_BANK = {
    "Easy": [
        ("What is matter?", "Anything that has mass and occupies space", "Only liquids", "Only living things", "Only gases", "A"),
        ("Which of these is a solid?", "Oxygen", "Ice", "Steam", "Water vapour", "B"),
        ("Which state of matter has a definite volume but no definite shape?", "Solid", "Gas", "Liquid", "Plasma", "C"),
        ("Which state of matter has neither a definite shape nor a definite volume?", "Solid", "Liquid", "Ice", "Gas", "D"),
        ("What happens to ice when it melts?", "It changes into liquid water", "It becomes oxygen", "It disappears completely", "It becomes a metal", "A"),
        ("Which process changes liquid water into water vapour?", "Freezing", "Evaporation", "Condensation", "Melting", "B"),
        ("What is the change from gas to liquid called?", "Melting", "Freezing", "Condensation", "Sublimation", "C"),
        ("Which state of matter has particles that are generally closely packed in fixed positions?", "Gas", "Liquid", "Plasma", "Solid", "D"),
        ("What is the SI unit of mass?", "Kilogram", "Newton", "Metre", "Litre", "A"),
        ("Which of these is a physical change?", "Burning wood", "Melting ice", "Rusting iron", "Cooking an egg", "B"),
        ("Which of these is generally a chemical change?", "Breaking glass", "Melting wax", "Rusting iron", "Cutting paper", "C"),
        ("What is the boiling point of pure water at standard atmospheric pressure?", "0°C", "50°C", "90°C", "100°C", "D"),
        ("What is the freezing point of pure water at standard atmospheric pressure?", "0°C", "25°C", "50°C", "100°C", "A"),
        ("Which state of matter is usually the most compressible?", "Solid", "Gas", "Liquid", "Ice", "B"),
        ("What happens to most substances when heated?", "Their particles stop moving", "Their mass always doubles", "Their particles gain kinetic energy", "They always become gases immediately", "C"),
        ("Which of these is a mixture?", "Pure gold", "Distilled water", "Pure oxygen", "Air", "D"),
        ("Which of these is an element?", "Copper", "Salt water", "Air", "Sugar solution", "A"),
        ("Which of these is a compound?", "Iron", "Water", "Oxygen", "Copper", "B"),
        ("What is density?", "Mass multiplied by time", "Volume divided by temperature", "Mass per unit volume", "Force per unit time", "C"),
        ("Which instrument measures temperature?", "Barometer", "Ammeter", "Spring balance", "Thermometer", "D"),
        ("What is the process of changing a solid directly into a gas called?", "Sublimation", "Condensation", "Freezing", "Melting", "A"),
        ("Which property describes how much space an object occupies?", "Mass", "Volume", "Density", "Weight", "B"),
        ("Which of these is commonly considered a pure substance?", "Soil", "Milk", "Distilled water", "Air", "C"),
        ("What is the smallest particle of an element that retains its chemical identity?", "Tissue", "Cell", "Mixture", "Atom", "D"),
        ("Which state of matter flows and takes the shape of its container while retaining a definite volume?", "Liquid", "Solid", "Gas", "Vacuum", "A"),
        ("What happens during freezing?", "A solid becomes a liquid", "A liquid becomes a solid", "A gas becomes a liquid", "A solid becomes a gas", "B"),
        ("Which property can be observed without changing a substance's chemical identity?", "Flammability", "Ability to rust", "Colour", "Reactivity with acid", "C"),
        ("Which of these is a gas at room temperature?", "Iron", "Ice", "Copper", "Oxygen", "D"),
        ("What is the chemical formula of water?", "H₂O", "CO₂", "O₂", "NaCl", "A"),
        ("Which process changes a liquid into a solid?", "Evaporation", "Freezing", "Melting", "Sublimation", "B"),
    ],

    "Medium": [
        ("Why can gases be compressed more easily than solids?", "Gas particles cannot move", "Gas particles have no mass", "Gas particles have relatively large spaces between them", "Gas particles are fixed in position", "C"),
        ("Why does evaporation cause cooling?", "Particles stop existing", "Mass disappears", "The liquid always freezes", "Higher-energy particles escape from the liquid", "D"),
        ("What happens to the average kinetic energy of particles when temperature increases?", "It increases", "It decreases", "It becomes zero", "It remains zero", "A"),
        ("Which method is suitable for separating an insoluble solid from a liquid?", "Distillation", "Filtration", "Chromatography", "Crystallization only", "B"),
        ("Which method can separate dissolved salt from salt water by recovering the water?", "Filtration alone", "Sieving", "Distillation", "Magnetic separation", "C"),
        ("What is a solution?", "A single pure element only", "A mixture that always contains visible particles", "A compound that cannot vary in composition", "A homogeneous mixture of substances", "D"),
        ("What is the density of an object with mass 200 g and volume 50 cm³?", "4 g/cm³", "2 g/cm³", "10 g/cm³", "250 g/cm³", "A"),
        ("Why does the smell of perfume spread throughout a room?", "Gravity stops acting", "Particles diffuse through the air", "Perfume becomes a solid", "Air particles stop moving", "B"),
        ("What happens to the particles of a solid when it is heated but remains solid?", "They lose all kinetic energy", "They stop vibrating", "They vibrate more vigorously", "They immediately separate completely", "C"),
        ("Which statement about a chemical change is correct?", "It always produces only gases", "It always reverses immediately", "It never involves energy changes", "It produces substances with different chemical identities", "D"),
        ("Which technique separates coloured substances in ink based on their movement through a medium?", "Chromatography", "Filtration", "Decantation", "Sieving", "A"),
        ("Why is air considered a mixture?", "It contains only one type of atom", "It contains different gases that are not chemically bonded into one compound", "It has a fixed chemical formula", "It cannot be separated physically", "B"),
        ("What is the main difference between an element and a compound?", "Elements always contain two atom types", "Compounds contain only one element", "Compounds contain chemically combined elements", "Elements can always be separated by filtration", "C"),
        ("Which change of state releases latent heat to the surroundings?", "Melting", "Boiling", "Sublimation", "Condensation", "D"),
        ("What happens to the temperature of a pure substance during melting at constant pressure?", "It generally remains constant until melting is complete", "It must rise continuously", "It must fall continuously", "It becomes absolute zero", "A"),
        ("Which of these is an intensive property?", "Mass", "Density", "Volume", "Total energy", "B"),
        ("An object has a mass of 600 g and a volume of 200 cm³. What is its density?", "2 g/cm³", "4 g/cm³", "3 g/cm³", "6 g/cm³", "C"),
        ("Which method separates a mixture of sand and iron filings?", "Distillation", "Evaporation", "Chromatography", "Magnetic separation", "D"),
        ("Why does sugar dissolve faster in warm water than in cold water under comparable conditions?", "Particles generally move faster at higher temperatures", "Sugar turns into an element", "Water loses all its mass", "The sugar becomes magnetic", "A"),
        ("Which observation provides evidence that a chemical reaction may have occurred?", "A solid is cut into pieces", "Gas bubbles form when substances react", "Ice changes shape", "Water is poured into a glass", "B"),
        ("Which process separates a dissolved solid by forming crystals from its solution?", "Filtration", "Sieving", "Crystallization", "Magnetic separation", "C"),
        ("What is the role of a solvent in a solution?", "It must always be a solid", "It is always present in the smallest amount", "It chemically destroys every solute", "It dissolves the solute", "D"),
        ("Which statement about boiling is correct?", "It occurs throughout the liquid at its boiling point under specified pressure", "It occurs only at the surface at every temperature", "It never produces vapour", "It changes every liquid into a solid", "A"),
        ("What is the approximate density of pure water near 4°C?", "0.1 g/cm³", "1 g/cm³", "4 g/cm³", "10 g/cm³", "B"),
        ("Why can condensation occur when water vapour contacts a sufficiently cool surface?", "The particles stop having mass", "The surface turns water into oxygen", "The vapour loses energy and becomes liquid", "The vapour becomes a metal", "C"),
        ("Which property describes a substance's resistance to being scratched?", "Solubility", "Conductivity", "Boiling point", "Hardness", "D"),
        ("Which of these is a heterogeneous mixture?", "Sand mixed with water", "Salt dissolved completely in water", "Pure copper", "Distilled water", "A"),
        ("What is the difference between melting and dissolving?", "They are always identical processes", "Melting changes state, while dissolving forms a solution", "Dissolving always produces a new element", "Melting always requires a solvent", "B"),
        ("What is sublimation?", "Liquid changing into solid", "Gas changing into liquid", "Solid changing directly into gas", "Gas changing directly into solid only", "C"),
        ("Which factor affects the boiling point of a liquid?", "Its container colour only", "The clock time", "The mass of the thermometer", "External pressure", "D"),
    ],

    "Hard": [
        ("A substance has a mass of 150 g and occupies 50 cm³. What is its density?", "3 g/cm³", "2 g/cm³", "5 g/cm³", "7.5 g/cm³", "A"),
        ("Why does the temperature remain nearly constant while a pure substance melts at constant pressure?", "Its particles stop moving", "Energy is used to overcome intermolecular attractions rather than raise temperature", "Its mass becomes zero", "It stops absorbing energy", "B"),
        ("A liquid boils at a lower temperature at high altitude. What is the main reason?", "Gravity becomes zero", "The liquid gains extra mass", "Atmospheric pressure is lower", "The liquid becomes an element", "C"),
        ("Which method is best for separating ethanol and water based on their different boiling points?", "Filtration", "Magnetic separation", "Sieving", "Fractional distillation", "D"),
        ("A 100 g sample occupies 25 cm³. What is its density?", "4 g/cm³", "2.5 g/cm³", "5 g/cm³", "0.25 g/cm³", "A"),
        ("Why can increasing temperature increase the rate of diffusion?", "Particles become heavier", "Particles generally move faster and mix more rapidly", "Particles stop colliding", "All particles become solids", "B"),
        ("A mixture contains salt, sand, and water. Which sequence can recover the sand first and then the salt?", "Distillation followed by magnetism", "Chromatography followed by filtration of dry air", "Filtration followed by evaporation or crystallization", "Sieving followed by freezing only", "C"),
        ("What happens to the average spacing between particles when a typical liquid evaporates into a gas?", "It always becomes zero", "It decreases to zero", "It remains exactly fixed", "It generally increases greatly", "D"),
        ("Why is melting wax generally classified as a physical change?", "The substance changes state without necessarily forming a new chemical substance", "It always creates a new element", "Its atoms disappear", "It necessarily produces oxygen", "A"),
        ("Which statement correctly describes conservation of mass in a closed system during a chemical reaction?", "Mass is always destroyed", "Total mass of reactants equals total mass of products", "Products always weigh twice as much", "Atoms disappear during reactions", "B"),
        ("A gas occupies 2 L at a fixed temperature and pressure. If the amount of gas doubles while pressure and temperature remain constant, what volume is expected?", "1 L", "2 L", "4 L", "8 L", "C"),
        ("Which change is exothermic?", "Melting ice", "Evaporating water", "Subliming dry ice", "Freezing water", "D"),
        ("Why does a sealed flexible balloon generally expand when warmed, if external pressure remains approximately constant?", "The gas volume increases with temperature", "The gas particles lose all kinetic energy", "The gas mass automatically doubles", "The balloon becomes a liquid", "A"),
        ("Which statement distinguishes a chemical property from a physical property?", "Density is always a chemical property", "Flammability describes a substance's ability to undergo chemical change", "Colour always requires a chemical reaction to observe", "Mass is always a chemical property", "B"),
        ("A sample contains 20 g of salt dissolved in 180 g of water. What is the total mass of the solution?", "180 g", "2000 g", "200 g", "160 g", "C"),
        ("A solution contains 10 g of solute in 90 g of solvent. What is the solute mass percentage?", "5%", "9%", "11%", "10%", "D"),
        ("Why does a pressure cooker help food cook faster?", "Higher pressure raises the boiling point of water", "Pressure removes all water", "Food stops absorbing heat", "The cooker reduces water's boiling point to 0°C", "A"),
        ("Which technique is most appropriate for separating the different pigments in a leaf extract?", "Filtration only", "Paper chromatography", "Sieving", "Magnetic separation", "B"),
        ("A substance changes directly from solid to gas. Which statement is correct?", "The process is freezing", "The process is condensation", "The process is sublimation", "The process is melting", "C"),
        ("Which condition generally increases the solubility of most solid solutes in liquid water?", "Reducing mixing in every case", "Removing the solvent", "Freezing the solution completely", "Increasing temperature, depending on the solute", "D"),
        ("Why can oil and water form separate layers?", "Their molecular interactions make them largely immiscible", "Oil has no molecules", "Water has no mass", "Oil always turns into a solid", "A"),
        ("What is the main difference between a saturated and an unsaturated solution at a given temperature?", "A saturated solution contains no solvent", "A saturated solution contains the maximum dissolved solute at equilibrium under those conditions", "An unsaturated solution must contain a precipitate", "An unsaturated solution is always a pure substance", "B"),
        ("Which statement about particles in a gas is correct?", "They remain fixed in a regular lattice", "They cannot collide", "They move randomly and are relatively far apart", "They have no kinetic energy", "C"),
        ("A liquid is heated in an open container. Why may its mass decrease over time?", "Its atoms cease to exist", "Gravity disappears", "It becomes a new element automatically", "Some liquid particles escape into the gas phase", "D"),
        ("Why can filtration not separate dissolved salt from salt water?", "Dissolved salt particles pass through ordinary filter pores with the water", "Salt becomes magnetic in water", "Water cannot pass through a filter", "Salt always becomes a gas", "A"),
        ("What happens to the average kinetic energy of particles during a temperature increase?", "It decreases", "It increases", "It must remain constant", "It becomes negative", "B"),
        ("Which statement about compounds is correct?", "Their elements can always be separated by filtration", "They contain only one kind of atom", "Their elements are chemically combined in defined proportions", "They are always mixtures", "C"),
        ("Why is air not considered a pure compound?", "It contains only one atom type", "It cannot contain oxygen", "It always has a fixed molecular formula", "It is a mixture of gases with variable proportions", "D"),
        ("A material has a mass of 80 g and a volume of 100 cm³. What is its density?", "0.8 g/cm³", "1.25 g/cm³", "8 g/cm³", "180 g/cm³", "A"),
        ("Which statement about evaporation is correct?", "It occurs only at the boiling point", "It can occur at the surface of a liquid below its boiling point", "It always makes the liquid hotter", "It cannot occur in open air", "B"),
    ],
}


def normalize(text):
    return " ".join(text.casefold().split())


def main():
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DATABASE_PATH}"
        )

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        connection.execute("PRAGMA foreign_keys = ON")

        lesson = connection.execute(
            """
            SELECT id
            FROM lessons
            WHERE lower(trim(title)) = lower(trim(?))
            """,
            ("Matter and Its Properties",),
        ).fetchone()

        if lesson is None:
            raise RuntimeError(
                "Matter and Its Properties lesson was not found."
            )

        lesson_id = lesson[0]
        total_inserted = 0

        with connection:
            for difficulty, candidates in QUESTION_BANK.items():
                quiz = connection.execute(
                    """
                    SELECT id
                    FROM quizzes
                    WHERE lesson_id = ?
                      AND lower(trim(difficulty)) = lower(trim(?))
                    """,
                    (lesson_id, difficulty),
                ).fetchone()

                if quiz is None:
                    raise RuntimeError(
                        f"Missing {difficulty} quiz for Matter and Its Properties."
                    )

                quiz_id = quiz[0]

                existing_rows = connection.execute(
                    """
                    SELECT question
                    FROM questions
                    WHERE quiz_id = ?
                    """,
                    (quiz_id,),
                ).fetchall()

                existing_questions = {
                    normalize(row[0]) for row in existing_rows
                }
                current_count = len(existing_rows)

                if current_count > TARGET_QUESTIONS:
                    raise RuntimeError(
                        f"{difficulty} already has {current_count} "
                        f"questions; target is {TARGET_QUESTIONS}."
                    )

                added = 0

                for item in candidates:
                    if current_count >= TARGET_QUESTIONS:
                        break

                    question, a, b, c, d, answer = item
                    normalized_question = normalize(question)

                    if normalized_question in existing_questions:
                        print(
                            f"Skipping duplicate ({difficulty}): {question}"
                        )
                        continue

                    if answer not in {"A", "B", "C", "D"}:
                        raise ValueError(
                            f"Invalid answer key: {question}"
                        )

                    if not all(
                        option.strip() for option in (a, b, c, d)
                    ):
                        raise ValueError(
                            f"Empty answer option: {question}"
                        )

                    connection.execute(
                        """
                        INSERT INTO questions (
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
                        (quiz_id, question, a, b, c, d, answer),
                    )

                    existing_questions.add(normalized_question)
                    current_count += 1
                    added += 1
                    total_inserted += 1

                if current_count != TARGET_QUESTIONS:
                    raise RuntimeError(
                        f"{difficulty} has {current_count} questions, "
                        f"not {TARGET_QUESTIONS}. Add more unique questions. "
                        "The transaction will roll back."
                    )

                print(
                    f"{difficulty}: added {added}; "
                    f"final count = {current_count}"
                )

        print("\nMatter and Its Properties expansion completed!")
        print(f"Total new questions inserted: {total_inserted}")
        print("Easy: 30 questions")
        print("Medium: 30 questions")
        print("Hard: 30 questions")
        print("Other lessons and Social Science were not modified.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()