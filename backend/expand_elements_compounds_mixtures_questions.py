
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"
LESSON_TITLE = "Elements, Compounds and Mixtures"
TARGET_QUESTIONS = 30

QUESTION_BANK = {
    "Easy": [
        ("What is an element?", "A pure substance made of one type of atom", "A mixture of many compounds", "A substance that must contain water", "A solution of two liquids", "A"),
        ("What is a compound?", "A mixture separated by filtration", "A substance formed when elements chemically combine in fixed proportions", "A single uncombined atom only", "A physical blend of substances", "B"),
        ("What is a mixture?", "A substance containing only one kind of atom", "A chemical formula", "Two or more substances physically combined", "A single pure compound", "C"),
        ("Which of these is an element?", "Water", "Carbon dioxide", "Sodium chloride", "Oxygen", "D"),
        ("Which of these is a compound?", "Water", "Iron", "Gold", "Helium", "A"),
        ("Which of these is a mixture?", "Pure oxygen", "Air", "Pure copper", "Distilled water", "B"),
        ("What is the chemical symbol for gold?", "Ag", "Gd", "Au", "Go", "C"),
        ("Which substance is made of hydrogen and oxygen chemically combined?", "Air", "Brass", "Soil", "Water", "D"),
        ("Which method can separate sand from water?", "Filtration", "Magnetization only", "Freezing only", "Chromatography only", "A"),
        ("Which of these is a homogeneous mixture?", "Sand and gravel", "Salt solution", "Oil and water after settling", "A bowl of cereal", "B"),
        ("Which of these is a heterogeneous mixture?", "Pure copper", "Distilled water", "Sand mixed with iron filings", "Pure oxygen", "C"),
        ("Which substance is commonly used to separate iron filings from sand?", "Filter paper", "A thermometer", "A funnel without a filter", "A magnet", "D"),
        ("What is the main component of air by volume?", "Nitrogen", "Oxygen", "Carbon dioxide", "Hydrogen", "A"),
        ("Which of these is a metal element?", "Sulfur", "Copper", "Oxygen", "Chlorine", "B"),
        ("Which of these is a non-metal element?", "Aluminium", "Iron", "Sulfur", "Copper", "C"),
        ("Which formula represents carbon dioxide?", "CO", "C₂O", "CaO", "CO₂", "D"),
        ("Can the components of a mixture usually retain their individual properties?", "Yes", "No, never", "Only when heated", "Only when frozen", "A"),
        ("Which method is commonly used to obtain salt from saltwater?", "Magnetic separation", "Evaporation", "Sieving", "Sedimentation alone", "B"),
        ("Which of these is a pure substance?", "Soil", "Milk", "Pure distilled water", "Air", "C"),
        ("What is brass?", "A pure element", "A pure compound with a fixed formula", "A gas", "An alloy of copper and zinc", "D"),
        ("Which of these is a compound made from sodium and chlorine?", "Sodium chloride", "Oxygen", "Copper", "Nitrogen", "A"),
        ("Which separation method is suitable for separating different-sized solid particles?", "Distillation", "Sieving", "Decantation of gases", "Electrolysis", "B"),
        ("Which of these is an example of a solution?", "Granite", "Sand and stones", "Sugar dissolved in water", "Iron filings and sulfur", "C"),
        ("Which statement about a compound is correct?", "Its components can always be separated by hand", "It has no chemical bonds", "Its composition changes randomly", "Its elements are chemically combined", "D"),
        ("Which of these is a mixture of gases?", "Air", "Pure oxygen", "Pure nitrogen", "Pure helium", "A"),
        ("Which process can separate colored dyes in ink?", "Filtration", "Paper chromatography", "Sieving", "Magnetic separation", "B"),
        ("Which of these is an element represented by the symbol Fe?", "Fluorine", "Francium", "Iron", "Fermium", "C"),
        ("Which is a characteristic of a pure compound?", "Its composition varies at random", "It must be a liquid", "It can always be separated by filtration", "Its elements are present in a definite ratio", "D"),
        ("Which method can separate oil and water in a laboratory?", "A separating funnel", "A magnet", "Paper chromatography in every case", "Sieving", "A"),
        ("Which statement best describes a physical mixture?", "Its components must form new chemical bonds", "Its components are combined without necessarily forming a new substance", "It always has a fixed chemical formula", "It always contains only one element", "B"),
    ],
    "Medium": [
        ("Why is water classified as a compound?", "It contains only one type of atom", "It can be separated by sieving", "Hydrogen and oxygen are chemically combined in a fixed ratio", "Its composition changes from sample to sample", "C"),
        ("Which method is most suitable for separating ethanol and water based on their different boiling points?", "Sieving", "Magnetic separation", "Simple handpicking", "Fractional distillation", "D"),
        ("Which statement distinguishes a compound from a mixture?", "A compound has elements chemically combined in a definite ratio", "A compound always contains visible particles", "A mixture always has a fixed formula", "A mixture must contain solids only", "A"),
        ("Which mixture can be separated using a magnet?", "Sugar and salt", "Iron filings and sulfur", "Water and ethanol", "Salt and water", "B"),
        ("What is the best method to separate an insoluble solid from a liquid?", "Fractional distillation", "Chromatography", "Filtration", "Sublimation in every case", "C"),
        ("Which technique is commonly used to obtain pure water from a salt solution?", "Sieving", "Handpicking", "Magnetic separation", "Distillation", "D"),
        ("Which statement about an alloy is correct?", "It is generally a mixture containing a metal and one or more other elements", "It must be a pure element", "It can contain only gases", "It always has the formula H₂O", "A"),
        ("Which of these is a heterogeneous mixture?", "Salt dissolved completely in water", "Oil and water", "Pure nitrogen", "Pure copper", "B"),
        ("Why can the components of many mixtures be separated by physical methods?", "They always have identical properties", "They are chemically bonded in fixed ratios", "They retain distinct physical properties", "They have the same chemical formula", "C"),
        ("Which method is useful for separating a mixture of substances with different solubilities in a solvent?", "Magnetic separation only", "Sieving only", "Handpicking only", "Crystallization or fractional crystallization", "D"),
        ("What is the main purpose of crystallization?", "To obtain a solid in purer crystalline form from a solution", "To convert all solids into gases", "To separate iron using a magnet", "To measure electric current", "A"),
        ("Which pair consists of compounds?", "O₂ and N₂", "CO₂ and NaCl", "Cu and Fe", "He and Ne", "B"),
        ("Which pair consists of elements?", "H₂O and CO₂", "NaCl and CaCO₃", "Fe and Cu", "Air and brass", "C"),
        ("Which method is best suited to separate colored components of a soluble ink sample?", "Filtration", "Sedimentation", "Magnetic separation", "Paper chromatography", "D"),
        ("What happens to the chemical identity of elements when they form a compound?", "They form a new substance with properties different from those of the elements", "They always retain all their original properties unchanged", "They become a mixture only", "They cannot form chemical bonds", "A"),
        ("Which of the following is generally a homogeneous mixture?", "Granite", "Air", "Soil", "Oil and water", "B"),
        ("Why is air considered a mixture?", "It has a single fixed chemical formula", "All its gases are chemically bonded together", "Its gases are physically mixed and their proportions can vary", "It contains only oxygen", "C"),
        ("Which technique separates a dissolved solid from a solution by forming crystals as the solution cools?", "Filtration", "Sieving", "Decantation only", "Crystallization", "D"),
        ("Which statement about the composition of a mixture is correct?", "The proportions of its components can vary", "It must contain elements in fixed ratios", "It always has a unique chemical formula", "It always forms through a chemical reaction", "A"),
        ("Which method separates a liquid from dissolved solids by heating and condensing the vapor?", "Handpicking", "Distillation", "Sieving", "Magnetic separation", "B"),
        ("Which substance is an example of a colloid?", "Pure sodium chloride", "Pure oxygen", "Milk", "Distilled water", "C"),
        ("Which process can separate ammonium chloride from a mixture with common salt under suitable laboratory conditions?", "Filtration", "Magnetic separation", "Decantation", "Sublimation", "D"),
        ("What is the chemical formula of calcium carbonate?", "CaCO₃", "CaCl₂", "CaO", "Ca(OH)₂", "A"),
        ("Which observation indicates that a sample may be a heterogeneous mixture?", "It has a uniform composition throughout", "Different components or phases can be distinguished", "It consists of only one pure substance", "It has a fixed molecular formula", "B"),
        ("Which statement about elements is correct?", "They can always be broken down into simpler substances by ordinary chemical reactions", "They are always mixtures of atoms", "They cannot be decomposed into simpler substances by ordinary chemical methods", "They must contain two or more kinds of atoms", "C"),
        ("Why is sodium chloride classified as a compound rather than a mixture?", "Its components are mixed in any proportion", "It can be separated by a magnet", "It contains only one element", "Sodium and chlorine are chemically combined in a definite ratio", "D"),
        ("Which method is most appropriate for separating immiscible liquids with different densities?", "Separating funnel", "Paper chromatography", "Sieving", "Sublimation", "A"),
        ("Which of these is a physical change rather than the formation of a new compound?", "Rusting iron", "Dissolving sugar in water", "Burning magnesium", "Reacting acid with a base", "B"),
        ("Which statement about a solution is correct?", "It must contain visible particles", "It is always a pure compound", "It is a homogeneous mixture of solute and solvent", "It cannot contain a gas", "C"),
        ("Which method is commonly used to separate different fractions of crude oil?", "Filtration", "Magnetic separation", "Simple sieving", "Fractional distillation", "D"),
    ],
    "Hard": [
        ("A mixture contains sand, salt, and iron filings. Which sequence can separate all three components effectively?", "Use a magnet, dissolve salt in water, filter sand, then evaporate water", "Filter the dry mixture, then use a magnet on the filtrate", "Evaporate the dry mixture, then sieve it", "Use chromatography only", "A"),
        ("Which statement best explains why compounds have fixed composition?", "Their components are physically mixed in any ratio", "Their elements combine chemically in definite proportions", "Their composition depends only on the container", "They always contain equal numbers of every atom", "B"),
        ("A sample contains two visible solid phases. Which conclusion is justified?", "It must be a pure element", "It must be a compound with a fixed formula", "It may be a heterogeneous mixture, but more evidence is needed", "It must be a gas", "C"),
        ("Which method is most appropriate for separating two miscible liquids with close boiling points?", "Handpicking", "Magnetic separation", "Filtration", "Fractional distillation", "D"),
        ("Why does paper chromatography separate the dyes in ink?", "Different components move differently because of their interactions with the mobile and stationary phases", "All dyes have identical solubility and attraction", "The paper reacts chemically with every dye", "The dyes are separated by magnetic force", "A"),
        ("Which statement about a pure substance is correct?", "It must always be an element", "It can be an element or a compound with characteristic composition", "It must contain several visible phases", "Its composition changes continuously", "B"),
        ("A solid dissolves in water, but another solid does not. Which method can help separate them?", "Distillation alone before adding water", "Magnetic separation regardless of materials", "Dissolve in water, filter the insoluble solid, then recover the dissolved solid", "Use sieving after both solids have dissolved", "C"),
        ("Which of these is a compound made from three different elements?", "O₂", "N₂", "NaCl", "CaCO₃", "D"),
        ("What is the mass percentage of oxygen in water, using H = 1 and O = 16?", "About 88.9%", "About 11.1%", "About 50%", "About 66.7%", "A"),
        ("Which statement correctly compares a compound and an alloy?", "Both must have fixed molecular formulas", "A compound has a definite chemical composition, while an alloy is generally a mixture", "An alloy must be a non-metal", "A compound can always be separated by filtration", "B"),
        ("A liquid mixture is heated and the vapor is condensed. What is the main basis for separation by distillation?", "Differences in color", "Differences in magnetic properties", "Differences in volatility and boiling behavior", "Differences in particle shape only", "C"),
        ("Which method is best for obtaining a dissolved solid when heating to dryness might decompose it?", "Strong heating until everything disappears", "Magnetic separation", "Sieving", "Crystallization under suitable conditions", "D"),
        ("Which of these is a homogeneous mixture but not a compound?", "Brass", "Pure water", "Pure carbon dioxide", "Pure sodium chloride", "A"),
        ("Why can a mixture's components often be present in different proportions?", "They must combine in fixed atomic ratios", "They are not necessarily chemically combined in a fixed ratio", "Their atoms are always identical", "Every mixture has a unique molecular formula", "B"),
        ("Which statement about the separation of saltwater is correct?", "Filtration alone removes dissolved salt", "A magnet extracts the dissolved salt", "Distillation can recover water, while evaporation can recover salt", "Sieving separates the dissolved ions", "C"),
        ("A sample of pure copper is mixed with pure sulfur without heating. What is initially formed?", "Copper sulfide compound immediately in all conditions", "A solution of copper in sulfur", "A new element", "A physical mixture of copper and sulfur", "D"),
        ("Which observation most clearly indicates a chemical reaction rather than simple mixing?", "Formation of a new substance with new properties", "Two solids being placed in the same container", "Sand settling in water", "Salt dissolving in water without reaction", "A"),
        ("Which technique could separate pigments extracted from plant leaves?", "Sieving", "Paper chromatography", "Magnetic separation", "Separating funnel", "B"),
        ("Which statement is correct about the formula CO₂?", "It represents a mixture of carbon and oxygen", "It means one carbon atom is physically mixed with two oxygen molecules", "It represents a compound with one carbon atom and two oxygen atoms per molecule", "It represents three carbon atoms", "C"),
        ("Which sample is most likely to have a variable composition?", "Pure oxygen", "Pure water", "Pure sodium chloride", "A mixture of sand and salt", "D"),
        ("A mixture contains ethanol and water. Which method is commonly used to separate them based on boiling behavior?", "Fractional distillation", "Magnetic separation", "Filtration", "Sieving", "A"),
        ("Which is the best explanation for why iron and sulfur can be separated with a magnet before reacting?", "Sulfur is strongly magnetic", "Iron responds to the magnet, while sulfur does not under ordinary conditions", "Both are dissolved in water", "They have the same magnetic properties", "B"),
        ("Which process separates an insoluble solid that settles at the bottom from a liquid by carefully pouring off the liquid?", "Chromatography", "Sublimation", "Decantation", "Fractional distillation", "C"),
        ("Which statement about the particles in a homogeneous mixture is correct?", "They are always chemically bonded to each other", "They must all be atoms of one element", "They must be visible to the naked eye", "Its composition is uniform at the macroscopic scale", "D"),
        ("Which of the following is a chemical change?", "Melting ice", "Formation of rust on iron", "Separating sand by filtration", "Evaporating water", "B"),
        ("A sample of seawater contains dissolved salts and suspended particles. What is the best classification?", "A pure element", "A single compound", "A mixture", "A single atom", "C"),
        ("Which statement about compounds is correct?", "Their properties can differ substantially from those of their constituent elements", "They always retain the properties of each element unchanged", "They can only contain two atoms", "They can always be separated by physical filtration", "A"),
        ("Which method separates a sublimable solid from a non-sublimable solid?", "Decantation", "Sublimation", "Separating funnel", "Simple filtration of dry solids", "B"),
        ("Why is filtration ineffective for removing dissolved sodium chloride from water?", "Salt is magnetic", "Water is insoluble", "The dissolved ions pass through ordinary filter paper with the water", "Salt evaporates instantly at room temperature", "C"),
        ("Which combination correctly matches the mixture with a suitable separation method?", "Sand and water — fractional distillation", "Iron filings and sand — paper chromatography", "Oil and water — sieving", "Colored dyes in ink — paper chromatography", "D"),
    ],
}


def normalize(text):
    return " ".join(text.strip().lower().split())


def main():
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DATABASE_PATH}")

    for difficulty, questions in QUESTION_BANK.items():
        if len(questions) != TARGET_QUESTIONS:
            raise ValueError(
                f"{difficulty} bank has {len(questions)} questions; "
                f"expected {TARGET_QUESTIONS}."
            )

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id FROM lessons
            WHERE LOWER(TRIM(title)) = LOWER(TRIM(?))
            """,
            (LESSON_TITLE,),
        )
        lessons = cursor.fetchall()

        if len(lessons) != 1:
            raise RuntimeError(
                f"Expected exactly one lesson named '{LESSON_TITLE}', "
                f"found {len(lessons)}."
            )

        lesson_id = lessons[0][0]
        added_total = 0
        final_counts = {}

        for difficulty in ("Easy", "Medium", "Hard"):
            cursor.execute(
                """
                SELECT id FROM quizzes
                WHERE lesson_id = ?
                  AND LOWER(TRIM(difficulty)) = LOWER(TRIM(?))
                """,
                (lesson_id, difficulty),
            )
            quizzes = cursor.fetchall()

            if len(quizzes) != 1:
                raise RuntimeError(
                    f"Expected exactly one {difficulty} quiz; "
                    f"found {len(quizzes)}."
                )

            quiz_id = quizzes[0][0]
            cursor.execute(
                "SELECT question FROM questions WHERE quiz_id = ?",
                (quiz_id,),
            )
            existing = {normalize(row[0]) for row in cursor.fetchall()}

            cursor.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                (quiz_id,),
            )
            current_count = cursor.fetchone()[0]

            if current_count > TARGET_QUESTIONS:
                raise RuntimeError(
                    f"{difficulty} already has {current_count} questions; "
                    f"target is {TARGET_QUESTIONS}."
                )

            needed = TARGET_QUESTIONS - current_count
            added = 0

            for question in QUESTION_BANK[difficulty]:
                normalized_question = normalize(question[0])
                if normalized_question in existing:
                    continue
                if added >= needed:
                    break

                cursor.execute(
                    """
                    INSERT INTO questions (
                        quiz_id, question, option_a, option_b,
                        option_c, option_d, correct_answer
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (quiz_id, *question),
                )
                existing.add(normalized_question)
                added += 1

            if added != needed:
                raise RuntimeError(
                    f"{difficulty}: needed {needed} new unique questions, "
                    f"but inserted {added}. Transaction will roll back."
                )

            cursor.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                (quiz_id,),
            )
            final_count = cursor.fetchone()[0]

            if final_count != TARGET_QUESTIONS:
                raise RuntimeError(
                    f"{difficulty} final count is {final_count}; "
                    f"expected {TARGET_QUESTIONS}."
                )

            final_counts[difficulty] = final_count
            added_total += added
            print(f"{difficulty}: added {added}; final count = {final_count}")

        connection.commit()

        print("\nElements, Compounds and Mixtures expansion completed!")
        print(f"Total new questions inserted: {added_total}")
        for difficulty in ("Easy", "Medium", "Hard"):
            print(f"{difficulty}: {final_counts[difficulty]} questions")
        print("Other lessons and Social Science were not modified.")

    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


if __name__ == "__main__":
    main()
