
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"
LESSON_TITLE = "Atoms and Molecules"
TARGET_QUESTIONS = 30

QUESTION_BANK = {
    "Easy": [
        ("What is an atom?", "The smallest unit of an element that retains its chemical identity", "A group of planets", "A type of energy", "A mixture of substances", "A"),
        ("What is a molecule?", "A single proton", "Two or more atoms chemically bonded together", "A type of cell", "A mixture that cannot react", "B"),
        ("Which particle has a positive electric charge?", "Electron", "Neutron", "Proton", "Photon", "C"),
        ("Which subatomic particle has a negative charge?", "Proton", "Neutron", "Nucleus", "Electron", "D"),
        ("Which subatomic particle has no electric charge?", "Neutron", "Proton", "Electron", "Ion", "A"),
        ("Where are protons and neutrons found in an atom?", "In the outer shell", "In the nucleus", "Outside the atom", "Only in molecules", "B"),
        ("Which symbol represents oxygen?", "Ox", "Og", "O", "On", "C"),
        ("What is the chemical symbol for hydrogen?", "Hy", "He", "Hg", "H", "D"),
        ("What is the chemical symbol for carbon?", "C", "Ca", "Co", "Cr", "A"),
        ("What is the chemical formula of water?", "CO₂", "H₂O", "O₂", "NaCl", "B"),
        ("How many hydrogen atoms are present in one water molecule?", "One", "Three", "Two", "Four", "C"),
        ("What does the subscript 2 in O₂ indicate?", "Two oxygen molecules", "Two protons only", "Two different elements", "Two oxygen atoms in one molecule", "D"),
        ("What is the chemical symbol for sodium?", "Na", "S", "So", "N", "A"),
        ("What is the chemical symbol for iron?", "Ir", "Fe", "In", "I", "B"),
        ("Which formula represents carbon dioxide?", "CO", "C₂O", "CO₂", "CaO", "C"),
        ("What is the formula of common table salt?", "KCl", "CaCO₃", "NaOH", "NaCl", "D"),
        ("What is the approximate relative atomic mass of hydrogen?", "1", "8", "12", "16", "A"),
        ("What is the approximate relative atomic mass of carbon-12?", "6", "12", "14", "16", "B"),
        ("Which of these is a diatomic molecule of an element?", "H₂O", "CO₂", "O₂", "NH₃", "C"),
        ("Which of these is a compound?", "O₂", "N₂", "He", "H₂O", "D"),
        ("What is the chemical symbol for calcium?", "Ca", "C", "Cl", "Cu", "A"),
        ("What is the chemical symbol for potassium?", "P", "K", "Po", "Pt", "B"),
        ("How many oxygen atoms are present in one CO₂ molecule?", "One", "Three", "Two", "Four", "C"),
        ("What is the chemical symbol for nitrogen?", "Ni", "Ne", "Na", "N", "D"),
        ("Which particle mainly determines the identity of an element?", "Number of protons", "Number of neutrons", "Number of molecules", "Number of shells", "A"),
        ("What is the smallest unit of an element that participates in ordinary chemical reactions?", "A tissue", "An atom", "An organ", "A solution", "B"),
        ("Which of these is a molecule of a compound?", "H₂", "N₂", "NH₃", "O₂", "C"),
        ("What is the chemical symbol for silver?", "Si", "S", "Au", "Ag", "D"),
        ("What is the chemical symbol for gold?", "Au", "Ag", "Gd", "Go", "A"),
        ("Which formula represents methane?", "CH₃", "CH₄", "C₂H₆", "CO₂", "B"),
    ],
    "Medium": [
        ("How many atoms are present in one molecule of H₂SO₄?", "5", "6", "7", "8", "C"),
        ("How many total atoms are present in one molecule of glucose, C₆H₁₂O₆?", "12", "18", "20", "24", "D"),
        ("What is the molecular mass of water, H₂O, using H = 1 and O = 16?", "18 u", "16 u", "17 u", "20 u", "A"),
        ("What is the molecular mass of carbon dioxide, CO₂, using C = 12 and O = 16?", "28 u", "44 u", "32 u", "48 u", "B"),
        ("What is the molecular mass of oxygen gas, O₂?", "8 u", "16 u", "32 u", "64 u", "C"),
        ("What is the molecular mass of ammonia, NH₃, using N = 14 and H = 1?", "14 u", "16 u", "18 u", "17 u", "D"),
        ("What is the formula of calcium chloride?", "CaCl₂", "Ca₂Cl", "CaCl", "Ca₂Cl₂", "A"),
        ("What is the formula of magnesium oxide?", "Mg₂O", "MgO", "MgO₂", "Mg₂O₃", "B"),
        ("What is the formula of aluminium oxide?", "AlO", "AlO₂", "Al₂O₃", "Al₃O₂", "C"),
        ("What is the formula of sodium carbonate?", "NaCO₃", "Na₂CO₂", "NaCO₂", "Na₂CO₃", "D"),
        ("What is the valency of oxygen in common compounds such as water?", "2", "1", "3", "4", "A"),
        ("What is the usual valency of sodium?", "2", "1", "3", "0", "B"),
        ("Which particle determines the atomic number of an element?", "Neutrons", "Electrons in every ion", "Protons", "Molecules", "C"),
        ("An atom has 11 protons. Which element is it?", "Magnesium", "Oxygen", "Calcium", "Sodium", "D"),
        ("How many electrons does a neutral carbon atom have?", "6", "12", "8", "4", "A"),
        ("What is the mass number of an atom containing 8 protons and 8 neutrons?", "8", "16", "24", "4", "B"),
        ("Which statement describes isotopes of an element?", "They have different numbers of protons", "They must have different chemical symbols", "They have the same number of protons but different numbers of neutrons", "They always have different numbers of electrons in neutral atoms", "C"),
        ("Which formula represents calcium hydroxide?", "CaOH", "Ca₂OH", "CaOH₂", "Ca(OH)₂", "D"),
        ("What is the relative molecular mass of methane, CH₄, using C = 12 and H = 1?", "16", "14", "12", "18", "A"),
        ("What is the formula of potassium oxide?", "KO", "K₂O", "KO₂", "K₂O₃", "B"),
        ("How many atoms are present in one formula unit of CaCO₃?", "3", "4", "5", "6", "C"),
        ("Which of these contains a polyatomic ion?", "NaCl", "MgO", "H₂", "CaCO₃", "D"),
        ("What is the charge on a typical oxide ion?", "2−", "1−", "1+", "2+", "A"),
        ("What is the charge on a sodium ion?", "2+", "1+", "1−", "2−", "B"),
        ("What is the formula of aluminium chloride?", "AlCl", "AlCl₂", "AlCl₃", "Al₃Cl", "C"),
        ("What is the molecular mass of nitrogen gas, N₂, using N = 14?", "14 u", "21 u", "28 u", "32 u", "C"),
        ("Which statement about a chemical formula is correct?", "It gives the color of a substance", "It shows only the physical state", "It tells the age of a compound", "It represents the types and relative numbers of atoms or ions", "D"),
        ("What is the formula of calcium carbonate?", "CaCO₃", "Ca₂CO₃", "CaC₂O₃", "CaCO₂", "A"),
        ("What is the total number of atoms in one formula unit of Na₂SO₄?", "6", "7", "8", "9", "B"),
        ("Which pair consists of molecules of elements?", "H₂O and CO₂", "NaCl and MgO", "H₂ and O₂", "NH₃ and CH₄", "C"),
    ],
    "Hard": [
        ("What is the formula mass of Ca(OH)₂ using Ca = 40, O = 16, and H = 1?", "56 u", "57 u", "72 u", "74 u", "D"),
        ("What is the formula mass of Na₂CO₃ using Na = 23, C = 12, and O = 16?", "106 u", "84 u", "100 u", "112 u", "A"),
        ("What is the formula mass of MgCl₂ using Mg = 24 and Cl = 35.5?", "59.5 u", "95 u", "83 u", "71 u", "B"),
        ("What is the molecular mass of HNO₃ using H = 1, N = 14, and O = 16?", "47 u", "62 u", "63 u", "64 u", "C"),
        ("What is the formula mass of Al₂(SO₄)₃ using Al = 27, S = 32, and O = 16?", "324 u", "342 u", "360 u", "342? u", "B"),
        ("How many oxygen atoms are present in one formula unit of Al₂(SO₄)₃?", "3", "4", "8", "12", "D"),
        ("What is the total number of atoms in one formula unit of Mg(NO₃)₂?", "9", "7", "5", "11", "A"),
        ("What is the formula of iron(III) oxide?", "FeO", "Fe₂O₃", "Fe₃O₂", "FeO₂", "B"),
        ("What is the formula of copper(II) chloride?", "CuCl", "Cu₂Cl", "CuCl₂", "Cu₂Cl₃", "C"),
        ("An ion contains 12 protons and 10 electrons. What is its charge?", "2−", "1−", "1+", "2+", "D"),
        ("An atom has atomic number 17 and mass number 35. How many neutrons does it have?", "18", "17", "35", "52", "A"),
        ("Which statement about isotopes is correct?", "They always have different atomic numbers", "They have the same atomic number but different mass numbers", "They contain different elements", "They must have different numbers of protons", "B"),
        ("What is the molar mass of water, approximately?", "9 g/mol", "16 g/mol", "18 g/mol", "20 g/mol", "C"),
        ("How many moles are present in 36 g of water if its molar mass is 18 g/mol?", "1 mol", "0.5 mol", "3 mol", "2 mol", "D"),
        ("Approximately how many particles are in one mole of a substance?", "6.022 × 10²³", "3.0 × 10⁸", "9.81 × 10²", "1.6 × 10⁻¹⁹", "A"),
        ("What is the number of moles in 44 g of CO₂ if its molar mass is 44 g/mol?", "2 mol", "1 mol", "0.5 mol", "4 mol", "B"),
        ("What is the mass of 2 moles of oxygen gas, O₂, with molar mass 32 g/mol?", "16 g", "32 g", "64 g", "96 g", "C"),
        ("What is the correct formula for ammonium sulfate?", "(NH₄)₂SO₄", "NH₄SO₄", "NH₄(SO₄)₂", "N₂H₄SO₄", "A"),
        ("Which formula represents iron(II) sulfate?", "Fe₂SO₄", "FeSO₄", "Fe₂(SO₄)₃", "Fe(SO₄)₂", "B"),
        ("What is the formula mass of KNO₃ using K = 39, N = 14, and O = 16?", "85 u", "95 u", "101 u", "117 u", "C"),
        ("What is the simplest whole-number ratio of atoms in C₆H₁₂O₆?", "6:12:6", "1:2:2", "2:1:2", "1:1:1", "B"),
        ("Which statement best distinguishes an empirical formula from a molecular formula?", "The empirical formula gives the simplest whole-number ratio of atoms", "The empirical formula always gives the exact number of atoms in a molecule", "The molecular formula never gives atom counts", "Both formulas must always be identical", "A"),
        ("A neutral atom has 20 protons. What is its atomic number?", "10", "20", "40", "Cannot be determined", "B"),
        ("How many electrons does a neutral atom with atomic number 13 have?", "10", "12", "13", "26", "C"),
        ("Which formula is correct for magnesium nitrate?", "MgNO₃", "Mg₂NO₃", "Mg(NO₃)₃", "Mg(NO₃)₂", "D"),
        ("What is the formula mass of NH₄NO₃ using N = 14, H = 1, and O = 16?", "80 u", "64 u", "62 u", "96 u", "A"),
        ("Which sample contains the greatest number of molecules?", "1 mole of H₂", "1 mole of CO₂", "1 mole of O₂", "All contain the same number of molecules", "D"),
        ("What is the mass of 0.5 mol of NaCl if its molar mass is 58.5 g/mol?", "58.5 g", "29.25 g", "117 g", "11.7 g", "B"),
        ("How many moles are present in 18 g of glucose if its molar mass is 180 g/mol?", "10 mol", "1 mol", "0.1 mol", "0.01 mol", "C"),
        ("Which statement about ionic compounds is generally correct?", "They are always made of separate molecules", "They contain only neutral atoms", "Their formulas show the exact number of molecules", "Their formulas show the simplest ratio of ions in the compound", "D"),
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
                    f"Expected exactly one {difficulty} quiz; found {len(quizzes)}."
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
                if normalize(question[0]) in existing:
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
                existing.add(normalize(question[0]))
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

        print("\nAtoms and Molecules expansion completed!")
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
