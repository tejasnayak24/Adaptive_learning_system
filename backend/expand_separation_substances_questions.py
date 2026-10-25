
import sqlite3
from pathlib import Path
import re

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

LESSON_TITLE = "Separation of Substances"
TARGET_QUESTIONS = 30

QUESTIONS = {
    "Easy": [
        ("Which method is commonly used to separate stones from rice?",
         "Filtration", "Handpicking", "Distillation", "Evaporation", "B"),
        ("Which method separates tea leaves from prepared tea?",
         "Sieving", "Churning", "Filtration", "Magnetic separation", "C"),
        ("Which method can separate sand from water?",
         "Filtration", "Evaporation only", "Churning", "Magnetic separation", "A"),
        ("Which method separates larger particles from smaller particles using a mesh?",
         "Distillation", "Sieving", "Condensation", "Sedimentation", "B"),
        ("Which substance can be attracted by a magnet?",
         "Sugar", "Salt", "Iron filings", "Sand", "C"),
        ("What happens during sedimentation?",
         "A liquid changes into gas", "Heavier insoluble particles settle at the bottom",
         "A gas changes into liquid", "A solid dissolves completely", "B"),
        ("What is decantation?",
         "Pouring off a liquid carefully from settled solids",
         "Heating a solid until it melts", "Separating using a magnet",
         "Changing vapour into liquid", "A"),
        ("Which method is useful for obtaining salt from saltwater?",
         "Handpicking", "Sieving", "Evaporation", "Magnetic separation", "C"),
        ("Which mixture can be separated using a magnet?",
         "Iron filings and sand", "Salt and sugar dissolved in water",
         "Oil and water", "Rice and flour", "A"),
        ("Which method is used to separate butter from curd traditionally?",
         "Sieving", "Churning", "Handpicking", "Decantation", "B"),
        ("What is filtration mainly used to separate?",
         "Two dissolved substances", "Two gases",
         "An insoluble solid from a liquid", "Two completely miscible liquids", "C"),
        ("Which of these is a mixture?",
         "Pure gold", "Distilled water", "Oxygen", "Sand and salt", "D"),
        ("What is the main purpose of separating substances in a mixture?",
         "To obtain useful components or remove unwanted materials",
         "To turn every mixture into a gas", "To destroy all components",
         "To increase the number of substances", "A"),
        ("Which method can separate flour from bran?",
         "Distillation", "Sieving", "Churning", "Condensation", "B"),
        ("Which process allows water vapour to change into liquid water?",
         "Evaporation", "Sublimation", "Condensation", "Sedimentation", "C"),
        ("Which method separates insoluble mud from water after the mud settles?",
         "Magnetic separation", "Churning", "Sublimation", "Decantation", "D"),
        ("Which of these dissolves readily in water?",
         "Clean sand", "Common salt", "Iron filings", "Chalk powder", "B"),
        ("Which mixture can be separated by handpicking?",
         "Salt dissolved in water", "Alcohol and water",
         "Peas mixed with small stones", "Sugar dissolved in tea", "C"),
        ("What is the liquid that passes through filter paper called?",
         "Filtrate", "Residue", "Sediment", "Solute", "A"),
        ("What is the solid left on filter paper called?",
         "Filtrate", "Solvent", "Residue", "Vapour", "C"),
        ("Which method is best for separating husk from heavier grains using wind?",
         "Winnowing", "Filtration", "Distillation", "Churning", "A"),
        ("What is the substance that dissolves in a solvent called?",
         "Residue", "Solute", "Filtrate", "Sediment", "B"),
        ("Which of these is generally insoluble in water?",
         "Sugar", "Common salt", "Sand", "Some food colouring", "C"),
        ("Which method separates a liquid from an insoluble solid by allowing the solid to settle?",
         "Sedimentation followed by decantation", "Churning only",
         "Sublimation only", "Magnetic separation only", "A"),
        ("What is a sieve?",
         "A device with holes used to separate particles by size",
         "A device that dissolves solids", "A type of magnet",
         "A container used only for heating liquids", "A"),
        ("Which method removes small impurities from grains by picking them out?",
         "Distillation", "Handpicking", "Condensation", "Filtration", "B"),
        ("Which state change is involved in evaporation?",
         "Liquid to gas", "Gas to solid", "Solid to liquid only", "Gas to liquid", "A"),
        ("Which mixture contains a soluble solid dissolved in a liquid?",
         "Sand and water", "Oil and water", "Salt and water", "Iron filings and sand", "C"),
        ("What usually remains after all the water evaporates from a salt solution?",
         "Only water", "Salt", "Oxygen", "Nothing at all", "B"),
        ("Which method is commonly used to separate grains from stalks after harvesting?",
         "Threshing", "Filtration", "Distillation", "Condensation", "A"),
    ],

    "Medium": [
        ("Why is sedimentation often followed by decantation?",
         "To dissolve the sediment", "To pour off the clearer liquid after solids settle",
         "To turn the solid into vapour", "To make insoluble solids magnetic", "B"),
        ("A mixture contains sand and dissolved salt in water. What should be done first to remove the sand?",
         "Magnetic separation", "Churning", "Filtration", "Sublimation", "C"),
        ("After filtering saltwater to remove sand, how can the dissolved salt be recovered?",
         "Evaporate the water", "Use handpicking", "Use a sieve", "Use winnowing", "A"),
        ("Which property makes filtration useful for separating sand from water?",
         "Sand evaporates quickly", "Sand is magnetic",
         "Sand is insoluble and can be retained by the filter", "Water is insoluble", "C"),
        ("Why does evaporation leave salt behind when saltwater is heated?",
         "Salt turns into oxygen", "Water evaporates while salt remains under ordinary conditions",
         "Salt becomes magnetic", "Water changes into salt", "B"),
        ("Which method is most suitable for separating iron filings from sulphur powder?",
         "Decantation", "Filtration", "Evaporation", "Magnetic separation", "D"),
        ("Which sequence is suitable for separating a mixture of sand, salt and water?",
         "Filter to remove sand, then evaporate water to recover salt",
         "Use a magnet, then handpick the salt", "Sieve the solution, then churn it",
         "Condense the sand, then filter the salt", "A"),
        ("What is the main difference between a solute and a solvent?",
         "A solute is always a liquid", "A solvent is always a solid",
         "A solute dissolves in a solvent", "A solvent cannot dissolve anything", "C"),
        ("Which technique is based mainly on differences in particle size?",
         "Distillation", "Sieving", "Evaporation", "Condensation", "B"),
        ("Why is winnowing effective for separating husk from grains?",
         "Husk is generally lighter and can be carried farther by wind",
         "Husk dissolves in air", "Grains become magnetic",
         "Husk turns into water", "A"),
        ("Which method is suitable for separating two immiscible liquids such as oil and water?",
         "Sieving", "Handpicking", "Separating funnel or careful decantation",
         "Magnetic separation", "C"),
        ("What is the purpose of distillation?",
         "To separate components using differences in boiling behaviour and condensation",
         "To separate particles only by size", "To pick out solids by hand",
         "To separate only magnetic materials", "A"),
        ("During simple distillation of saltwater, what is collected after the vapour condenses?",
         "Salt crystals only", "Sand", "Iron filings", "Water", "D"),
        ("Why is a dissolved substance not removed from water by ordinary filtration?",
         "It is always magnetic", "Its dissolved particles pass through ordinary filter paper with water",
         "It settles immediately", "It is too large to pass through the filter", "B"),
        ("Which method can be used to obtain relatively pure crystals of a dissolved solid from a suitable solution?",
         "Handpicking", "Winnowing", "Crystallisation", "Threshing", "C"),
        ("What happens to the concentration of a salt solution when some water evaporates?",
         "It generally increases", "It always becomes zero",
         "It becomes a pure solvent", "It never changes", "A"),
        ("Which combination is appropriate for separating a mixture of iron filings and sand?",
         "Filtration followed by distillation", "Evaporation followed by churning",
         "Sieving followed by condensation", "Magnetic separation", "D"),
        ("Why should a filter funnel be placed securely during filtration?",
         "To make the solid dissolve faster", "To collect the filtrate without spilling",
         "To increase the magnetism of the mixture", "To stop all evaporation permanently", "B"),
        ("Which method is suitable for separating two miscible liquids with sufficiently different boiling points?",
         "Handpicking", "Winnowing", "Distillation", "Sieving", "C"),
        ("What is the residue when muddy water is filtered?",
         "The mud retained by the filter", "The clear water collected below",
         "Water vapour", "Dissolved oxygen only", "A"),
        ("Which statement about evaporation is correct?",
         "It can occur only at 100°C", "It occurs only in a vacuum",
         "It can occur at the surface of a liquid below its boiling point",
         "It always freezes a liquid", "C"),
        ("Why can a mixture of rice and fine flour be separated by sieving?",
         "They have different colours only", "Their particles differ in size",
         "One is always magnetic", "Both dissolve at different rates", "B"),
        ("Which process is commonly used to separate cotton fibres from seeds?",
         "Condensation", "Distillation", "Sedimentation", "Ginning", "D"),
        ("What is the purpose of loading in traditional water treatment?",
         "To help fine suspended particles clump together and settle",
         "To turn water into vapour", "To dissolve sand completely",
         "To separate dissolved salt using a magnet", "A"),
        ("Which method is most appropriate for separating a small quantity of insoluble chalk powder from water?",
         "Winnowing", "Filtration", "Churning", "Threshing", "B"),
        ("A student wants to recover both water and salt from saltwater. Which method is most suitable?",
         "Handpicking", "Sieving", "Distillation", "Magnetic separation", "C"),
        ("What is the function of a condenser in distillation?",
         "To cool vapour and convert it into liquid", "To grind the solid",
         "To attract iron", "To filter out large stones", "A"),
        ("Which method is suitable for separating cream from milk in a dairy using rapid spinning?",
         "Sieving", "Handpicking", "Sublimation", "Centrifugation", "D"),
        ("Why is crystallisation often preferred over evaporating a solution completely?",
         "It makes all impurities magnetic", "It can produce crystals and may leave some impurities in the remaining solution",
         "It converts the solute into a gas", "It separates components only by particle size", "B"),
        ("Which pair of methods is suitable for separating sand and dissolved sugar from water?",
         "Magnetic separation then winnowing", "Churning then handpicking",
         "Filtration followed by evaporation or crystallisation", "Sieving followed by threshing", "C"),
    ],

    "Hard": [
        ("A mixture contains iron filings, sand and salt. Which sequence best separates all three components?",
         "Add water, filter out sand, magnetically remove salt, then evaporate",
         "Use a magnet to remove iron, add water to dissolve salt, filter sand, then evaporate the filtrate",
         "Evaporate first, then sieve all the components",
         "Use winnowing to remove iron and distil the sand", "B"),
        ("A student filters a solution of sugar in water. What will most likely happen?",
         "Sugar remains entirely on the filter paper", "The filter paper dissolves",
         "Sugar and water pass through as a solution", "Sugar becomes magnetic", "C"),
        ("Why is ordinary filtration insufficient to obtain pure water from saltwater?",
         "Saltwater contains no liquid", "Salt is magnetic",
         "Water cannot pass through filter paper", "Dissolved salt passes through with the water", "D"),
        ("A liquid mixture contains two miscible liquids with close boiling points. Which method is generally more suitable than simple distillation?",
         "Fractional distillation", "Handpicking", "Sieving", "Magnetic separation", "A"),
        ("During distillation, why must the vapour be cooled?",
         "To increase the size of solid particles", "To condense it into a collectable liquid",
         "To make the mixture magnetic", "To prevent the liquid from boiling ever again", "B"),
        ("A mixture contains ammonium chloride and sand. Which property can be used to separate them?",
         "Both dissolve equally in water", "Both are attracted to a magnet",
         "Ammonium chloride sublimes on heating while sand does not under ordinary laboratory conditions",
         "Sand evaporates at room temperature", "C"),
        ("Which statement best distinguishes a pure substance from a mixture?",
         "A mixture always contains exactly two substances",
         "A pure substance can be separated into components by handpicking",
         "Every mixture has a fixed boiling point",
         "A pure substance has a definite composition, while a mixture can have variable composition", "D"),
        ("A student heats a salt solution to dryness. Which component is lost mainly as vapour?",
         "Water", "Salt", "The container", "The dissolved salt and water in equal amounts", "A"),
        ("Which method would be most appropriate for separating pigments in ink for analysis?",
         "Winnowing", "Paper chromatography", "Handpicking", "Magnetic separation", "B"),
        ("Why can chromatography separate different dyes in ink?",
         "All dyes have identical attraction to paper and solvent",
         "The paper chemically destroys every dye",
         "Dyes move differently because of differences in their interactions with the stationary and mobile phases",
         "The ink is converted entirely into gas", "C"),
        ("A mixture of oil and water is allowed to stand. Which observation is expected?",
         "Oil dissolves completely in water", "Both form a single uniform layer",
         "Oil turns into a solid immediately", "Two layers form, with the less dense oil usually on top", "D"),
        ("Which method is best for separating very fine suspended particles from a liquid by rapid rotation?",
         "Centrifugation", "Handpicking", "Threshing", "Sieving", "A"),
        ("Why does a separating funnel work for oil and water?",
         "The liquids must have identical densities", "The immiscible liquids form separate layers that can be drained separately",
         "The funnel turns oil into vapour", "Water becomes a solid", "B"),
        ("A saturated salt solution is cooled slowly. What may happen if the salt is less soluble at the lower temperature?",
         "All the salt turns into gas", "The solvent becomes magnetic",
         "Some dissolved salt may crystallise out", "The salt changes into a different element", "C"),
        ("Which condition generally increases the rate of evaporation?",
         "Lower temperature and still air", "Smaller exposed surface area",
         "Higher humidity in the surrounding air", "Higher temperature and greater exposed surface area", "D"),
        ("Why does increasing wind speed generally increase evaporation?",
         "It removes water vapour near the surface, allowing more liquid to evaporate",
         "It turns liquid water into salt", "It stops molecules from moving",
         "It makes the liquid boil at every temperature", "A"),
        ("A student needs to separate a dissolved solid that decomposes on strong heating. Which approach may be preferable?",
         "Heat the solution strongly to dryness in every case",
         "Consider crystallisation under suitable conditions",
         "Use a magnet regardless of the solid's properties",
         "Use handpicking to remove dissolved particles", "B"),
        ("Which statement about sedimentation is correct?",
         "It separates all dissolved substances from water",
         "It works only when the solid is magnetic",
         "It relies on suspended particles settling under gravity",
         "It converts a liquid directly into gas", "C"),
        ("A sample contains salt, sand and water. After filtration, what does the filtrate contain?",
         "Only dry sand", "Only air", "Only filter-paper fibres",
         "Water with dissolved salt", "D"),
        ("Which technique is commonly used to separate and identify components of a small mixture of soluble substances?",
         "Chromatography", "Threshing", "Handpicking", "Winnowing", "A"),
        ("Why should distillation equipment be arranged so vapour can pass into the condenser?",
         "To allow the solid to be picked by hand",
         "To cool and collect the vapour as a liquid",
         "To increase the mixture's particle size",
         "To make the dissolved solid pass through a magnet", "B"),
        ("Which approach best separates a mixture of two solids when one sublimes on heating and the other does not?",
         "Decantation", "Filtration", "Sublimation", "Centrifugation", "C"),
        ("A student uses a sieve with openings that are too large to separate fine sand from coarse sand. What is the main problem?",
         "The sand becomes soluble", "The sieve changes the substances chemically",
         "The sieve creates a magnetic field", "Both particle sizes may pass through the openings", "D"),
        ("Which statement about crystallisation is most accurate?",
         "It can separate a dissolved solid by forming crystals from a suitable solution",
         "It separates only magnetic materials", "It works only for insoluble solids",
         "It always removes every impurity completely", "A"),
        ("A solution contains a non-volatile dissolved solid. Which process is suitable if only the solid needs to be recovered?",
         "Condensation alone", "Evaporation or crystallisation, depending on the substance",
         "Winnowing", "Magnetic separation", "B"),
        ("Why is fractional distillation useful for separating miscible liquids with similar boiling points?",
         "It separates substances by colour only",
         "It requires the liquids to be insoluble",
         "Repeated vaporisation and condensation in a fractionating column improves separation",
         "It works only with magnetic liquids", "C"),
        ("Which factor is NOT a usual basis for choosing a separation method?",
         "Particle size", "Solubility", "Boiling point", "The name of the person who collected the mixture", "D"),
        ("A mixture contains salt and sand. Water is added and the mixture is stirred. Which property allows the salt to be separated from sand?",
         "Salt dissolves in water while sand remains insoluble",
         "Sand evaporates at room temperature",
         "Salt is attracted strongly to an ordinary magnet",
         "Sand changes into a liquid immediately", "A"),
        ("After separating salt from sand by dissolving, filtering and evaporating, which precaution helps avoid losing material?",
         "Discard the filtrate before evaporation",
         "Transfer the filtrate carefully and heat it safely under supervision",
         "Remove the sand from the filter before filtration finishes",
         "Add more sand to the filtrate", "B"),
        ("Which statement correctly compares evaporation and distillation?",
         "Both always recover the solvent as a collected liquid",
         "Evaporation separates only magnetic substances",
         "Distillation can recover condensed solvent, while simple evaporation usually leaves the non-volatile solute behind",
         "Neither method involves a change of state", "C"),
    ],
}


def normalize(text):
    return re.sub(r"\s+", " ", text.strip().lower())


def main():
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DATABASE_PATH}")

    conn = sqlite3.connect(DATABASE_PATH)
    try:
        cur = conn.cursor()

        cur.execute(
            "SELECT id FROM lessons WHERE LOWER(TRIM(title)) = LOWER(TRIM(?))",
            (LESSON_TITLE,),
        )
        lesson_rows = cur.fetchall()

        if len(lesson_rows) != 1:
            raise RuntimeError(
                f"Expected exactly one lesson titled '{LESSON_TITLE}', "
                f"but found {len(lesson_rows)}."
            )

        lesson_id = lesson_rows[0][0]
        inserted_total = 0

        for difficulty, question_bank in QUESTIONS.items():
            cur.execute(
                """
                SELECT id FROM quizzes
                WHERE lesson_id = ? AND LOWER(TRIM(difficulty)) = LOWER(TRIM(?))
                """,
                (lesson_id, difficulty),
            )
            quiz_rows = cur.fetchall()

            if len(quiz_rows) != 1:
                raise RuntimeError(
                    f"Expected exactly one {difficulty} quiz for "
                    f"'{LESSON_TITLE}', but found {len(quiz_rows)}."
                )

            quiz_id = quiz_rows[0][0]

            cur.execute(
                "SELECT question FROM questions WHERE quiz_id = ?",
                (quiz_id,),
            )
            existing = {normalize(row[0]) for row in cur.fetchall()}

            cur.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                (quiz_id,),
            )
            current_count = cur.fetchone()[0]
            needed = max(0, TARGET_QUESTIONS - current_count)

            added = 0
            for item in question_bank:
                question, a, b, c, d, answer = item
                key = normalize(question)

                if key in existing:
                    continue

                if answer not in {"A", "B", "C", "D"}:
                    raise ValueError(f"Invalid answer key for: {question}")

                if added >= needed:
                    break

                cur.execute(
                    """
                    INSERT INTO questions
                    (quiz_id, question, option_a, option_b, option_c,
                     option_d, correct_answer)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (quiz_id, question, a, b, c, d, answer),
                )

                existing.add(key)
                added += 1

            cur.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                (quiz_id,),
            )
            final_count = cur.fetchone()[0]

            if final_count < TARGET_QUESTIONS:
                raise RuntimeError(
                    f"{difficulty} has only {final_count} questions after "
                    f"expansion. Add more unique questions to the bank."
                )

            inserted_total += added
            print(
                f"{difficulty}: started with {current_count}, "
                f"added {added}, final total {final_count}"
            )

        conn.commit()
        print(f"\nSuccess! Added {inserted_total} questions to '{LESSON_TITLE}'.")
        print("Each difficulty now has at least 30 questions.")
        print("Other lessons and Social Science were not modified.")

    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
