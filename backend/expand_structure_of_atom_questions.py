
import sqlite3
from pathlib import Path
import re

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

LESSON_TITLE = "Structure of the Atom"
TARGET_QUESTIONS = 30

QUESTIONS = {
    "Easy": [
        ("Who proposed the nuclear model of the atom based on the gold foil experiment?",
         "J. J. Thomson", "Ernest Rutherford", "Niels Bohr", "James Chadwick", "B"),
        ("Which subatomic particle has a negative charge?",
         "Proton", "Neutron", "Electron", "Nucleus", "C"),
        ("Which subatomic particle has a positive charge?",
         "Electron", "Proton", "Neutron", "Photon", "B"),
        ("Which subatomic particle has no electric charge?",
         "Proton", "Electron", "Neutron", "Positron", "C"),
        ("Where are protons and neutrons located in an atom?",
         "In the nucleus", "In fixed shells outside the nucleus", "Only on the atom's surface", "Between separate atoms", "A"),
        ("Who discovered the electron?",
         "Ernest Rutherford", "J. J. Thomson", "James Chadwick", "John Dalton", "B"),
        ("Who discovered the neutron?",
         "Niels Bohr", "Ernest Rutherford", "James Chadwick", "J. J. Thomson", "C"),
        ("What is the central part of an atom called?",
         "Orbit", "Shell", "Electron cloud", "Nucleus", "D"),
        ("What does the atomic number represent?",
         "Number of protons", "Number of neutrons only", "Number of shells", "Number of isotopes", "A"),
        ("What is the mass number of an atom?",
         "Number of electrons only", "Number of protons plus neutrons", "Number of shells", "Number of protons minus electrons", "B"),
        ("In a neutral atom, the number of electrons is equal to the number of:",
         "Neutrons", "Shells", "Protons", "Isotopes", "C"),
        ("Which particle contributes very little to an atom's mass?",
         "Proton", "Neutron", "Nucleus", "Electron", "D"),
        ("Which scientist proposed that electrons occupy specific energy levels?",
         "Niels Bohr", "James Chadwick", "John Dalton", "Dmitri Mendeleev", "A"),
        ("What is the symbol commonly used for a proton?",
         "e⁻", "p⁺", "n⁰", "γ", "B"),
        ("What is the symbol commonly used for an electron?",
         "p⁺", "n⁰", "e⁻", "α", "C"),
        ("What is the symbol commonly used for a neutron?",
         "e⁻", "p⁺", "α", "n⁰", "D"),
        ("Which particle determines the identity of a chemical element?",
         "Proton", "Neutron", "Electron", "Photon", "A"),
        ("An atom has 8 protons. Which element is it?",
         "Carbon", "Oxygen", "Nitrogen", "Neon", "B"),
        ("How many protons does a carbon atom have?",
         "4", "5", "6", "8", "C"),
        ("What is the electrical charge of a neutral atom overall?",
         "Positive", "Negative", "Always zero only if it has no neutrons", "Zero", "D"),
        ("Which part of an atom occupies most of its volume?",
         "The region occupied by electrons", "The nucleus alone", "Protons alone", "Neutrons alone", "A"),
        ("Which subatomic particles are found in the nucleus of most atoms?",
         "Electrons and protons", "Protons and neutrons", "Electrons and neutrons", "Electrons only", "B"),
        ("What is an isotope?",
         "Atoms with different proton numbers but the same neutron number",
         "Atoms with the same mass number but different proton numbers",
         "Atoms of the same element with different numbers of neutrons",
         "Atoms with no electrons", "C"),
        ("What is the atomic number of hydrogen?",
         "0", "2", "3", "1", "D"),
        ("Which particle is involved most directly in forming chemical bonds?",
         "Electron", "Neutron", "Proton inside the nucleus", "Nucleon only", "A"),
        ("What is a positively charged ion called?",
         "Anion", "Cation", "Isotope", "Neutron", "B"),
        ("What is a negatively charged ion called?",
         "Cation", "Isotope", "Anion", "Nucleus", "C"),
        ("If a neutral atom loses one electron, what does it become?",
         "A neutron", "A negatively charged ion", "A different element", "A positively charged ion", "D"),
        ("Which scientist's model described electrons embedded in a positively charged sphere?",
         "J. J. Thomson", "Niels Bohr", "James Chadwick", "Ernest Rutherford", "A"),
        ("Which experiment provided evidence for a small, dense, positively charged nucleus?",
         "Oil-drop experiment", "Gold foil experiment", "Double-slit experiment", "Millikan's experiment alone", "B"),
    ],

    "Medium": [
        ("An atom has atomic number 11 and mass number 23. How many neutrons does it have?",
         "11", "12", "23", "34", "B"),
        ("An atom contains 17 protons and 18 neutrons. What is its mass number?",
         "17", "18", "35", "1", "C"),
        ("A neutral atom has atomic number 12. How many electrons does it have?",
         "12", "6", "24", "10", "A"),
        ("An ion has 11 protons and 10 electrons. What is its charge?",
         "−1", "0", "+1", "+2", "C"),
        ("Which pair represents isotopes of the same element?",
         "Atoms with 6 and 7 protons respectively",
         "Atoms with 8 protons and 8 neutrons, and 8 protons and 10 neutrons",
         "Atoms with 6 protons and 6 electrons, and 7 protons and 7 electrons",
         "Atoms with the same mass number but different proton numbers", "B"),
        ("What is the electronic configuration of a neutral sodium atom with atomic number 11 in shell notation?",
         "2, 7, 2", "2, 8, 2", "2, 8, 1", "2, 6, 3", "C"),
        ("What is the electronic configuration of a neutral oxygen atom with atomic number 8 in shell notation?",
         "2, 6", "2, 8", "2, 5, 1", "4, 4", "A"),
        ("An atom has 13 protons and 14 neutrons. What is its mass number?",
         "13", "14", "26", "27", "D"),
        ("Which statement about isotopes is correct?",
         "They always have different atomic numbers",
         "They have the same number of protons but different numbers of neutrons",
         "They always have different chemical symbols",
         "They must have different numbers of electrons when neutral", "B"),
        ("Why do isotopes of an element generally have similar chemical properties?",
         "They have identical mass numbers",
         "They contain no neutrons",
         "They have the same number of protons and, when neutral, the same electron arrangement",
         "They all have the same number of nucleons", "C"),
        ("An atom has 9 protons and 10 electrons. What is its charge?",
         "−1", "+1", "0", "+2", "A"),
        ("Which statement about Rutherford's gold foil experiment is correct?",
         "All alpha particles bounced straight back",
         "The atom was shown to be a solid sphere with no empty space",
         "Electrons were found inside the nucleus",
         "Most alpha particles passed through, while a small number were strongly deflected", "D"),
        ("What did the large deflection of a few alpha particles suggest?",
         "The atom contains no charged particles",
         "Positive charge and most atomic mass are concentrated in a small region",
         "The nucleus occupies the entire atom",
         "Electrons have more mass than protons", "B"),
        ("Which limitation was associated with Rutherford's classical nuclear model?",
         "It could not include a nucleus",
         "It stated that electrons have no charge",
         "It did not explain why orbiting electrons would not lose energy and collapse into the nucleus",
         "It claimed atoms contain no empty space", "C"),
        ("What is the maximum number of electrons in the first shell under the basic shell model?",
         "2", "8", "18", "32", "A"),
        ("What is the maximum number of electrons in the second shell under the basic shell model?",
         "2", "18", "32", "8", "D"),
        ("An atom has electronic configuration 2, 8, 7. How many electrons are in its outermost shell?",
         "2", "7", "8", "17", "B"),
        ("Which subatomic particle count changes when one isotope of an element becomes another isotope of the same element?",
         "Proton count", "Atomic number", "Neutron count", "Element identity", "C"),
        ("An ion has 12 protons and 10 electrons. What is its charge?",
         "−2", "−1", "+1", "+2", "D"),
        ("What is the atomic number of an atom with 19 protons?",
         "19", "20", "38", "9", "A"),
        ("Which statement distinguishes the mass number from the atomic number?",
         "Mass number counts electrons only",
         "Mass number is protons plus neutrons, while atomic number is protons",
         "Atomic number is protons plus neutrons",
         "They always have the same value", "B"),
        ("A neutral atom has mass number 40 and atomic number 20. How many neutrons does it contain?",
         "10", "20", "40", "60", "B"),
        ("What happens to the atomic number when an atom becomes an ion by gaining electrons?",
         "It increases by one", "It decreases by one", "It remains unchanged", "It becomes zero", "C"),
        ("Which particle has approximately the same mass as a neutron?",
         "Electron", "Photon", "Positron", "Proton", "D"),
        ("Which observation from Rutherford's experiment showed that atoms are mostly empty space?",
         "Most alpha particles passed through the foil with little or no deflection",
         "Every alpha particle bounced back",
         "The foil dissolved in the experiment",
         "Electrons became visible to the naked eye", "A"),
        ("What is the electronic configuration of magnesium with atomic number 12 in shell notation?",
         "2, 7, 3", "2, 8, 2", "2, 6, 4", "2, 8, 1", "B"),
        ("A neutral atom has 15 electrons. What is its atomic number?",
         "8", "10", "15", "30", "C"),
        ("Which statement about a neutral atom and its ion is correct?",
         "They must have different numbers of protons",
         "They must be different elements",
         "They always have the same number of electrons",
         "They have the same number of protons but different electron counts", "D"),
        ("Which scientist is credited with proposing the nuclear model after the gold foil experiment?",
         "Ernest Rutherford", "J. J. Thomson", "James Chadwick", "John Dalton", "A"),
        ("An atom has 16 protons, 16 electrons and 18 neutrons. What is its mass number?",
         "16", "34", "32", "50", "B"),
    ],

    "Hard": [
        ("An ion has 16 protons, 18 electrons and 16 neutrons. What are its charge and mass number?",
         "−2 charge and mass number 32", "+2 charge and mass number 32",
         "−2 charge and mass number 34", "0 charge and mass number 16", "A"),
        ("An element has two isotopes: one has 10 neutrons and the other has 12 neutrons. Both have 8 protons. Which statement is correct?",
         "They are different elements", "Their atomic numbers are 10 and 12",
         "Their mass numbers are 18 and 20", "They must have different proton numbers", "C"),
        ("A neutral atom has mass number 31 and 15 protons. How many electrons and neutrons does it have?",
         "15 electrons and 31 neutrons", "16 electrons and 15 neutrons",
         "31 electrons and 15 neutrons", "15 electrons and 16 neutrons", "D"),
        ("An ion has 13 protons and 10 electrons. Which notation correctly describes its charge?",
         "3−", "3+", "1+", "0", "B"),
        ("An atom has 20 protons and 20 neutrons. Which statement is correct?",
         "Its atomic number is 20 and its mass number is 40",
         "Its atomic number is 40 and its mass number is 20",
         "Its atomic number is 20 and its mass number is 20",
         "Its atomic number is 40 and its mass number is 40", "A"),
        ("Which pair of atoms has the same mass number but different atomic numbers?",
         "Two isotopes of carbon", "Two neutral atoms of the same element",
         "Carbon-14 and nitrogen-14", "Two atoms with the same number of protons and different neutrons", "C"),
        ("An atom has electronic configuration 2, 8, 3. How many electrons must it lose to achieve the preceding noble gas configuration?",
         "1", "2", "8", "3", "D"),
        ("An atom has electronic configuration 2, 8, 7. How many electrons would it typically gain to complete its outer shell?",
         "7", "1", "2", "8", "B"),
        ("Which statement best explains why most of an atom's mass is concentrated in the nucleus?",
         "Protons and neutrons are much more massive than electrons",
         "Electrons have no charge",
         "The nucleus occupies most of the atom's volume",
         "Electrons are located inside protons", "A"),
        ("An element has atomic number 17. What is the number of protons in its 37Cl isotope?",
         "37", "20", "17", "54", "C"),
        ("For a neutral atom of chlorine-37 with atomic number 17, how many neutrons are present?",
         "17", "37", "54", "20", "D"),
        ("Which conclusion is NOT supported by Rutherford's gold foil experiment?",
         "The atom contains a small nucleus",
         "The nucleus is negatively charged",
         "Most of the atom is empty space",
         "The nucleus is positively charged", "B"),
        ("Why did Rutherford's model replace Thomson's model?",
         "It showed that electrons have no charge",
         "It showed that atoms cannot contain electrons",
         "The scattering results indicated a small, dense, positively charged nucleus",
         "It proved the nucleus occupies most of the atom's volume", "C"),
        ("An ion has 9 protons, 10 neutrons and 10 electrons. Which description is correct?",
         "Atomic number 9, mass number 19, charge −1",
         "Atomic number 10, mass number 19, charge +1",
         "Atomic number 19, mass number 9, charge −1",
         "Atomic number 9, mass number 10, charge 0", "A"),
        ("Two species have the same number of electrons but different numbers of protons. What can be concluded?",
         "They are necessarily isotopes of the same element",
         "They must have the same atomic number",
         "They must be neutral atoms",
         "They represent different elements, though they may be ions", "D"),
        ("A neutral atom has 26 protons and 30 neutrons. Which pair gives its atomic number and mass number?",
         "30 and 56", "26 and 56", "26 and 30", "56 and 26", "B"),
        ("Which statement about electron shells is correct in the simplified Bohr model?",
         "Electrons can occupy any energy without restriction",
         "The first shell can contain 8 electrons",
         "Electrons occupy discrete energy levels",
         "Neutrons orbit in the shells", "C"),
        ("An atom loses two electrons but its nucleus remains unchanged. What changes?",
         "Its atomic number doubles",
         "Its number of protons decreases by two",
         "Its number of neutrons increases by two",
         "Its charge becomes +2", "D"),
        ("Which species has 18 electrons and 17 protons?",
         "A chloride ion with a −1 charge",
         "A neutral chlorine atom",
         "A potassium ion with a +1 charge",
         "A neutral argon atom", "A"),
        ("A neutral atom has 14 electrons and mass number 28. How many neutrons does it have?",
         "28", "14", "42", "12", "B"),
        ("Which statement about isotopes is correct when they are electrically neutral?",
         "They have different numbers of protons and identical electrons",
         "They must have different chemical properties in every reaction",
         "They have the same electron configuration but different neutron numbers",
         "They always have the same mass number", "C"),
        ("An ion contains 24 electrons and has a 3+ charge. How many protons does it contain?",
         "21", "24", "27", "27", "C"),
        ("A species has 12 protons, 10 electrons and 13 neutrons. What is its mass number?",
         "22", "23", "25", "35", "B"),
        ("Which observation indicates that the nucleus is very small compared with the atom?",
         "Most alpha particles pass through thin gold foil without large deflection",
         "Every alpha particle is absorbed by the foil",
         "All alpha particles are deflected at right angles",
         "Gold atoms have no electrons", "A"),
        ("What is the charge of a species with 8 protons and 10 electrons?",
         "0", "+2", "+1", "−2", "D"),
        ("An element has isotopes of mass numbers 35 and 37. If both have atomic number 17, how many neutrons do they have respectively?",
         "17 and 19", "18 and 20", "35 and 37", "17 and 17", "B"),
        ("Which statement about atomic number is always true for a given element?",
         "It changes when the atom gains an electron",
         "It equals the number of neutrons",
         "It equals the number of protons in the nucleus",
         "It equals the mass number", "C"),
        ("An atom contains 11 protons, 12 neutrons and 10 electrons. Which description is correct?",
         "Neutral sodium atom with mass number 23",
         "Sodium ion with a −1 charge and mass number 21",
         "Magnesium ion with a +2 charge and mass number 23",
         "Sodium ion with a +1 charge and mass number 23", "D"),
        ("Which statement correctly compares protons, neutrons and electrons?",
         "Protons are positive, neutrons are neutral, and electrons are negative",
         "Protons and electrons are both positive",
         "Neutrons are negative and electrons are neutral",
         "All three have equal mass and charge", "A"),
        ("An atom has 19 protons and mass number 39. How many neutrons does it contain?",
         "19", "20", "39", "58", "B"),
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
