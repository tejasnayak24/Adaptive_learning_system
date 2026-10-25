
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"
LESSON_TITLE = "Acids, Bases and Salts"
TARGET_QUESTIONS = 30

QUESTION_BANK = {
    "Easy": [
        ("Which of these is a common natural acid?", "Citric acid", "Sodium chloride", "Sodium hydroxide", "Calcium oxide", "A"),
        ("Which substance is commonly found in lemon juice?", "Sulfuric acid", "Citric acid", "Hydrochloric acid", "Nitric acid", "B"),
        ("What is the taste commonly associated with acids?", "Bitter", "Sweet", "Sour", "Salty only", "C"),
        ("Which substance is a base?", "Vinegar", "Lemon juice", "Orange juice", "Sodium hydroxide", "D"),
        ("What color does blue litmus turn in an acidic solution?", "Red", "Blue", "Green", "Yellow", "A"),
        ("What color does red litmus turn in a basic solution?", "Red", "Blue", "Yellow", "Orange", "B"),
        ("Which of these is a natural indicator?", "Sugar", "Salt", "Turmeric", "Sand", "C"),
        ("What is formed when an acid reacts with a base?", "Only oxygen", "Only hydrogen", "Only carbon dioxide", "Salt and water", "D"),
        ("Which substance is commonly used in cooking and contains acetic acid?", "Vinegar", "Soap", "Baking soda", "Chalk", "A"),
        ("Which of these is an acidic substance?", "Soap solution", "Vinegar", "Limewater", "Baking soda solution", "B"),
        ("Which of these is generally bitter and slippery to touch?", "Acid", "Pure water", "Base", "Sugar solution", "C"),
        ("What is the pH of a neutral solution at about 25°C?", "1", "5", "10", "7", "D"),
        ("Which of these is commonly used as an antacid?", "Magnesium hydroxide", "Hydrochloric acid", "Vinegar", "Lemon juice", "A"),
        ("Which acid is present in curd?", "Citric acid", "Lactic acid", "Acetic acid", "Formic acid", "B"),
        ("Which acid is present in vinegar?", "Lactic acid", "Citric acid", "Acetic acid", "Tartaric acid", "C"),
        ("Which acid is naturally present in the stomach?", "Acetic acid", "Citric acid", "Carbonic acid", "Hydrochloric acid", "D"),
        ("Which of these is a common base used in soap making?", "Sodium hydroxide", "Citric acid", "Acetic acid", "Carbonic acid", "A"),
        ("Which solution turns phenolphthalein pink?", "Acidic solution", "Basic solution", "Neutral water in all conditions", "Sugar solution always", "B"),
        ("What is the name of a substance used to identify whether a solution is acidic or basic?", "Solvent", "Reactant", "Indicator", "Catalyst", "C"),
        ("Which of these is a salt?", "Hydrochloric acid", "Sodium hydroxide", "Ammonia", "Sodium chloride", "D"),
        ("What is the approximate pH range of acidic solutions?", "Below 7", "Exactly 7", "Above 7", "Always 14", "A"),
        ("What is the approximate pH range of basic solutions?", "Below 7", "Above 7", "Exactly 7", "Always 0", "B"),
        ("Which household substance can turn red litmus blue?", "Vinegar", "Lemon juice", "Baking soda solution", "Orange juice", "C"),
        ("Which acid is found in tamarind?", "Hydrochloric acid", "Sulfuric acid", "Nitric acid", "Tartaric acid", "D"),
        ("Which of these is used to test pH with a range of colors?", "Universal indicator", "Table sugar", "Cooking oil", "Distilled salt", "A"),
        ("What is the chemical name of common table salt?", "Sodium carbonate", "Sodium chloride", "Calcium chloride", "Potassium nitrate", "B"),
        ("Which gas is often produced when an acid reacts with a carbonate?", "Oxygen", "Nitrogen", "Carbon dioxide", "Helium", "C"),
        ("What is neutralization?", "Freezing a solution", "Evaporating water", "Dissolving sugar", "Reaction between an acid and a base", "D"),
        ("Which of these is a basic household substance?", "Soap solution", "Vinegar", "Lemon juice", "Orange juice", "A"),
        ("Which acid is found in many citrus fruits?", "Lactic acid", "Citric acid", "Formic acid", "Hydrochloric acid", "B"),
    ],
    "Medium": [
        ("What are the products when hydrochloric acid reacts with sodium hydroxide?", "Sodium oxide and hydrogen", "Sodium and chlorine", "Sodium chloride and water", "Hydrogen and oxygen", "C"),
        ("Which equation correctly represents the reaction between hydrochloric acid and sodium hydroxide?", "HCl + NaOH → Na + H₂O", "HCl + NaOH → H₂ + NaCl", "HCl + NaOH → Na₂O + Cl₂", "HCl + NaOH → NaCl + H₂O", "D"),
        ("Why is an antacid used to relieve excess stomach acidity?", "It neutralizes some excess acid", "It makes the stomach more acidic", "It produces more hydrochloric acid", "It stops all digestion permanently", "A"),
        ("A solution has a pH of 3. What is its nature?", "Basic", "Acidic", "Neutral", "Cannot be classified", "B"),
        ("A solution has a pH of 11. What is its nature?", "Acidic", "Neutral", "Basic", "Always harmless", "C"),
        ("What happens to blue litmus paper in a basic solution?", "It turns red", "It becomes colorless", "It turns yellow", "It generally remains blue", "D"),
        ("Which combination produces carbon dioxide gas?", "Hydrochloric acid and sodium carbonate", "Sodium hydroxide and sodium chloride", "Water and sugar", "Sodium chloride and water", "A"),
        ("Which salt is formed when sulfuric acid reacts completely with sodium hydroxide?", "Sodium chloride", "Sodium sulfate", "Sodium carbonate", "Sodium nitrate", "B"),
        ("Which statement about an indicator is correct?", "It always neutralizes the solution", "It always produces a gas", "It changes color depending on the solution's nature", "It must be a metal", "C"),
        ("What is the approximate pH of a strongly acidic solution?", "12", "9", "7", "2", "D"),
        ("What is the approximate pH of a strongly basic solution?", "13", "4", "6", "7", "A"),
        ("Which acid-base pair forms sodium chloride and water?", "Nitric acid and potassium hydroxide", "Hydrochloric acid and sodium hydroxide", "Sulfuric acid and calcium hydroxide", "Acetic acid and magnesium hydroxide", "B"),
        ("Why should concentrated acids never be tasted in a laboratory?", "They are always sweet", "They are harmless in small amounts", "They can cause severe chemical burns and poisoning", "They turn into pure water on contact", "C"),
        ("What should generally be done when diluting concentrated acid in a laboratory?", "Pour water rapidly into concentrated acid", "Mix chemicals without protection", "Heat the acid until it boils", "Add acid slowly to water while stirring, following safety guidance", "D"),
        ("Which substance can neutralize acidic soil in many agricultural situations?", "Lime", "Vinegar", "Lemon juice", "Carbonated water", "A"),
        ("Which substance is commonly used to treat soil that is too basic?", "Sodium hydroxide", "Suitable organic matter or soil amendments based on soil testing", "Bleach", "More lime", "B"),
        ("What is the main purpose of adding lime to acidic soil?", "To increase acidity", "To remove all minerals", "To reduce acidity", "To make soil sterile", "C"),
        ("Which acid is used in car batteries?", "Citric acid", "Acetic acid", "Carbonic acid", "Sulfuric acid", "D"),
        ("Which acid is commonly associated with an ant sting?", "Formic acid", "Nitric acid", "Sulfuric acid", "Hydrochloric acid", "A"),
        ("Which salt is commonly known as baking soda?", "Sodium chloride", "Sodium hydrogen carbonate", "Calcium carbonate", "Potassium chloride", "B"),
        ("What happens when an acid reacts with a reactive metal such as magnesium?", "Only water is produced", "Oxygen is always produced", "A salt and hydrogen gas are generally produced", "The acid becomes a base without other products", "C"),
        ("Which gas is produced when magnesium reacts with dilute hydrochloric acid?", "Carbon dioxide", "Oxygen", "Nitrogen", "Hydrogen", "D"),
        ("Which of these is a correct property of a neutral solution at about 25°C?", "Its pH is approximately 7", "Its pH is always 0", "It must contain sodium chloride", "It turns every indicator red", "A"),
        ("Which statement about acids and bases is correct?", "All acids are safe to drink", "Some acids and bases are corrosive", "All bases are edible", "Acids cannot react with metals", "B"),
        ("Which salt can be formed by reacting nitric acid with potassium hydroxide?", "Sodium chloride", "Calcium sulfate", "Potassium nitrate", "Magnesium carbonate", "C"),
        ("What is the main role of a universal indicator?", "To measure mass", "To identify metals only", "To measure temperature", "To estimate pH by color", "D"),
        ("Which reaction is an example of neutralization?", "HNO₃ + KOH → KNO₃ + H₂O", "2H₂ + O₂ → 2H₂O", "CaCO₃ → CaO + CO₂", "2Mg + O₂ → 2MgO", "A"),
        ("What is produced when an acid reacts with a metal oxide that acts as a base?", "Only hydrogen", "Salt and water", "Only carbon dioxide", "A new metal", "B"),
        ("Which statement about pH is correct?", "Lower pH means lower acidity", "pH never changes", "Lower pH generally indicates greater acidity", "Higher pH always means a stronger acid", "C"),
        ("Why is distilled water considered approximately neutral at 25°C?", "It always contains equal amounts of acid and salt", "It contains concentrated alkali", "It has a pH of 1", "Its hydrogen and hydroxide ion concentrations are approximately equal", "D"),
    ],
    "Hard": [
        ("Which is the balanced equation for complete neutralization of sulfuric acid by sodium hydroxide?", "H₂SO₄ + 2NaOH → Na₂SO₄ + 2H₂O", "H₂SO₄ + NaOH → NaSO₄ + H₂O", "H₂SO₄ + 2NaOH → Na₂O + H₂", "H₂SO₄ + NaOH → NaCl + H₂O", "A"),
        ("Which salt is produced by complete neutralization of phosphoric acid with potassium hydroxide?", "Potassium chloride", "Potassium phosphate", "Potassium sulfate", "Potassium carbonate", "B"),
        ("A solution changes universal indicator to red. Which conclusion is most reasonable?", "It is strongly basic", "It is neutral", "It is strongly acidic", "It must be pure water", "C"),
        ("Which statement best describes the pH scale commonly used in school science?", "It measures mass directly", "It measures electrical resistance only", "It is a scale only for basic substances", "It indicates how acidic or basic an aqueous solution is", "D"),
        ("If an acidic solution is diluted with water, what generally happens to its pH?", "It moves toward 7", "It moves farther below 0 in every case", "It always becomes exactly 7 immediately", "It becomes more acidic", "A"),
        ("Which pair of reactants produces potassium chloride and water?", "Sulfuric acid and potassium hydroxide", "Hydrochloric acid and potassium hydroxide", "Nitric acid and potassium carbonate", "Acetic acid and sodium chloride", "B"),
        ("Which is the correct formula for calcium hydroxide?", "CaOH", "Ca₂OH", "Ca(OH)₂", "CaH₂O", "C"),
        ("Which acid has the formula HNO₃?", "Hydrochloric acid", "Sulfuric acid", "Carbonic acid", "Nitric acid", "D"),
        ("Which formula represents sodium carbonate?", "Na₂CO₃", "NaHCO₃", "NaCl", "NaOH", "A"),
        ("Which observation supports the production of carbon dioxide when an acid reacts with a carbonate?", "A glowing splint relights in the gas", "The gas turns limewater milky", "The gas burns with a pop", "The gas has a blue flame", "B"),
        ("Which equation correctly represents an acid reacting with a carbonate?", "Acid + carbonate → salt + hydrogen", "Acid + carbonate → base + oxygen", "Acid + carbonate → salt + water + carbon dioxide", "Acid + carbonate → metal + water", "C"),
        ("Which statement about strong and weak acids is scientifically appropriate?", "Every concentrated acid is weak", "Every dilute acid is strong", "Strength depends only on color", "Strength relates to the extent of ionization in water", "D"),
        ("Which statement distinguishes acid strength from acid concentration?", "Strength describes ionization; concentration describes amount of solute per volume", "Strength and concentration always mean the same thing", "Concentration describes color only", "Strength describes the container size", "A"),
        ("Which of these is a weak acid commonly found in vinegar?", "Hydrochloric acid", "Acetic acid", "Nitric acid", "Sulfuric acid", "B"),
        ("Which statement about a salt is correct?", "Every salt is safe to eat", "Every salt dissolves completely in water", "Salts are ionic compounds that can be formed in acid-base reactions", "Salts are always acidic", "C"),
        ("What is the formula of ammonium chloride?", "NH₄OH", "NaCl", "NH₄NO₃", "NH₄Cl", "D"),
        ("Which equation correctly represents the reaction of magnesium with dilute hydrochloric acid?", "Mg + 2HCl → MgCl₂ + H₂", "Mg + HCl → MgCl + H₂O", "Mg + 2HCl → MgO + Cl₂", "Mg + H₂O → MgCl₂ + H₂", "A"),
        ("Which substance is commonly used to neutralize excess acid in some industrial wastewater treatments?", "Sugar", "A suitable base such as lime, selected according to the wastewater", "Cooking oil", "Ethanol", "B"),
        ("Which statement about acid rain is correct?", "It is caused only by water vapor", "It always has a pH above 7", "It can form when sulfur dioxide and nitrogen oxides react in the atmosphere", "It is harmless to all buildings and ecosystems", "C"),
        ("Which of these is a common consequence of acid rain?", "It increases the pH of every lake", "It prevents all corrosion", "It produces pure oxygen", "It can acidify lakes and damage some materials", "D"),
        ("A solution has pH 2 and another has pH 4. At the same temperature, how do their hydrogen-ion concentrations compare approximately?", "The pH 2 solution has 100 times the hydrogen-ion concentration", "The pH 4 solution has 100 times the hydrogen-ion concentration", "Both have equal hydrogen-ion concentrations", "The pH 2 solution has twice the hydrogen-ion concentration", "A"),
        ("Which formula represents sulfuric acid?", "HCl", "H₂SO₄", "HNO₃", "H₂CO₃", "B"),
        ("Which acid-base reaction produces calcium chloride and water?", "HNO₃ + NaOH", "H₂SO₄ + KOH", "2HCl + Ca(OH)₂ → CaCl₂ + 2H₂O", "HCl + Na₂CO₃", "C"),
        ("Which statement best explains why an aqueous sodium hydroxide solution is basic?", "It releases carbon dioxide", "It contains only neutral molecules", "It has a pH below 7", "It produces hydroxide ions in water", "D"),
        ("What is the conjugate base formed when hydrochloric acid donates a proton?", "Chloride ion", "Sodium ion", "Hydroxide ion", "Calcium ion", "A"),
        ("Which statement about neutralization is most accurate?", "Every neutralization reaction releases hydrogen gas", "Acid and base react to form products, commonly salt and water", "Neutralization always produces a pH of exactly 7 regardless of amounts", "Neutralization can occur only with strong acids", "B"),
        ("What is the chemical formula of calcium carbonate?", "CaCl₂", "Ca(OH)₂", "CaCO₃", "CaSO₄", "C"),
        ("Which acid is diprotic, meaning one molecule can donate two protons in successive ionization steps?", "Hydrochloric acid", "Nitric acid", "Acetic acid", "Sulfuric acid", "D"),
        ("If equal amounts of a strong acid and a strong base react in the exact stoichiometric ratio, what is generally expected at about 25°C?", "A solution near neutral pH", "A solution always at pH 2", "A solution always at pH 12", "A solution containing only acid", "A"),
        ("Which laboratory practice is safest when handling acid or base splashes on skin?", "Ignore the splash if it is small", "Rinse immediately with plenty of running water and follow lab safety procedures", "Neutralize the skin using another concentrated chemical", "Wipe it off and continue working", "B"),
    ],
}


def normalize(text):
    return " ".join(text.strip().lower().split())


def main():
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DATABASE_PATH}\n"
            "Run this script from your project setup and verify the database path."
        )

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id, title FROM lessons WHERE LOWER(TRIM(title)) = LOWER(TRIM(?))",
            (LESSON_TITLE,),
        )
        lessons = cursor.fetchall()

        if len(lessons) != 1:
            raise RuntimeError(
                f"Expected exactly one lesson named '{LESSON_TITLE}', "
                f"but found {len(lessons)}."
            )

        lesson_id = lessons[0][0]
        added_total = 0
        final_counts = {}

        for difficulty in ("Easy", "Medium", "Hard"):
            cursor.execute(
                """
                SELECT id, difficulty
                FROM quizzes
                WHERE lesson_id = ?
                  AND LOWER(TRIM(difficulty)) = LOWER(TRIM(?))
                """,
                (lesson_id, difficulty),
            )
            quizzes = cursor.fetchall()

            if len(quizzes) != 1:
                raise RuntimeError(
                    f"Expected exactly one {difficulty} quiz for "
                    f"'{LESSON_TITLE}', but found {len(quizzes)}."
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
                    f"{difficulty} quiz already has {current_count} questions; "
                    f"target is {TARGET_QUESTIONS}. No questions were added."
                )

            needed = TARGET_QUESTIONS - current_count
            added = 0

            for question in QUESTION_BANK[difficulty]:
                question_text = question[0]
                normalized_question = normalize(question_text)

                if normalized_question in existing:
                    continue

                if added >= needed:
                    break

                cursor.execute(
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
                    (quiz_id, *question),
                )

                existing.add(normalized_question)
                added += 1

            if added < needed:
                raise RuntimeError(
                    f"{difficulty}: needed {needed} new unique questions, "
                    f"but only {added} were available. Transaction will roll back."
                )

            cursor.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                (quiz_id,),
            )
            final_count = cursor.fetchone()[0]

            if final_count != TARGET_QUESTIONS:
                raise RuntimeError(
                    f"{difficulty} count is {final_count}, expected "
                    f"{TARGET_QUESTIONS}. Transaction will roll back."
                )

            final_counts[difficulty] = final_count
            added_total += added
            print(
                f"{difficulty}: added {added}; "
                f"final count = {final_count}"
            )

        connection.commit()

        print("\nAcids, Bases and Salts expansion completed!")
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
