
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"
LESSON_TITLE = "Metals and Non-Metals"
TARGET_QUESTIONS = 30

QUESTION_BANK = {
    "Easy": [
        ("Which of these is a metal?", "Iron", "Sulfur", "Oxygen", "Carbon", "A"),
        ("Which of these is a non-metal?", "Copper", "Sulfur", "Aluminium", "Iron", "B"),
        ("Which property allows metals to be drawn into wires?", "Brittleness", "Ductility", "Transparency", "Solubility", "B"),
        ("Which property allows metals to be hammered into sheets?", "Malleability", "Ductility", "Elasticity", "Conductivity", "A"),
        ("Which metal is liquid at room temperature?", "Iron", "Copper", "Mercury", "Aluminium", "C"),
        ("Which non-metal is essential for respiration?", "Nitrogen", "Carbon", "Hydrogen", "Oxygen", "D"),
        ("Which metal is commonly used in electrical wiring?", "Copper", "Sulfur", "Phosphorus", "Carbon", "A"),
        ("Which of these is a generally brittle non-metal in its solid form?", "Copper", "Sulfur", "Aluminium", "Iron", "B"),
        ("What is the usual appearance of freshly cut sodium?", "Black", "Green", "Silvery", "Blue", "C"),
        ("Which gas is a non-metal?", "Iron", "Copper", "Gold", "Oxygen", "D"),
        ("Which property is typical of many metals?", "Good electrical conductivity", "Poor heat conductivity in all cases", "Always being gases", "Being transparent", "A"),
        ("Which metal is commonly used to make cooking utensils?", "Sulfur", "Aluminium", "Phosphorus", "Chlorine", "B"),
        ("Which non-metal is used in pencil leads in the form of graphite?", "Sulfur", "Oxygen", "Carbon", "Nitrogen", "C"),
        ("What is the chemical symbol for iron?", "Ir", "In", "I", "Fe", "D"),
        ("What is the chemical symbol for copper?", "Cu", "Co", "Cp", "Cr", "A"),
        ("Which gas is commonly used in balloons because it is light and non-flammable?", "Oxygen", "Helium", "Chlorine", "Hydrogen chloride", "B"),
        ("What is the chemical symbol for aluminium?", "Au", "Ag", "Al", "Am", "C"),
        ("Which metal is used in many food cans because of its corrosion resistance and low weight?", "Sodium", "Calcium", "Mercury", "Aluminium", "D"),
        ("Which of these is a noble gas and a non-metal?", "Neon", "Iron", "Zinc", "Copper", "A"),
        ("Which metal is attracted strongly to a magnet?", "Gold", "Iron", "Silver", "Aluminium", "B"),
        ("Which non-metal is present in diamond?", "Sulfur", "Oxygen", "Carbon", "Chlorine", "C"),
        ("Which of these metals is commonly used in jewellery?", "Sodium", "Calcium", "Potassium", "Gold", "D"),
        ("Which property makes copper useful in electrical cables?", "High electrical conductivity", "High brittleness", "Poor conductivity", "Transparency", "A"),
        ("Which of these is a liquid non-metal at room temperature?", "Mercury", "Bromine", "Iron", "Copper", "B"),
        ("Which metal reacts vigorously with water and must be stored carefully?", "Gold", "Silver", "Sodium", "Copper", "C"),
        ("Which non-metal is used to disinfect drinking water in controlled treatment processes?", "Carbon", "Sulfur", "Phosphorus", "Chlorine", "D"),
        ("What is the chemical symbol for gold?", "Au", "Ag", "Gd", "Go", "A"),
        ("Which of these is a common property of non-metals?", "All are good conductors", "Many are poor conductors of heat and electricity", "All are malleable", "All are magnetic", "B"),
        ("Which metal is commonly used for galvanizing iron?", "Copper", "Silver", "Zinc", "Gold", "C"),
        ("Which non-metal is a major component of the air we breathe?", "Iron", "Copper", "Aluminium", "Nitrogen", "D"),
    ],

    "Medium": [
        ("What happens when magnesium burns in oxygen?", "It forms magnesium oxide", "It forms magnesium chloride", "It forms magnesium sulfide", "It forms magnesium carbonate", "A"),
        ("Which gas is commonly released when a reactive metal reacts with dilute hydrochloric acid?", "Oxygen", "Hydrogen", "Nitrogen", "Carbon dioxide", "B"),
        ("Which of these metals is relatively unreactive?", "Sodium", "Potassium", "Gold", "Calcium", "C"),
        ("Which metal is commonly extracted from bauxite ore?", "Copper", "Iron", "Zinc", "Aluminium", "D"),
        ("Why is sodium stored under kerosene or a suitable protective liquid?", "To limit contact with air and moisture", "To make it dissolve in water", "To increase its melting point", "To turn it into a non-metal", "A"),
        ("Which oxide is generally basic in nature?", "Carbon dioxide", "Magnesium oxide", "Sulfur dioxide", "Nitrogen dioxide", "B"),
        ("Which oxide is generally acidic in nature?", "Sodium oxide", "Calcium oxide", "Sulfur dioxide", "Magnesium oxide", "C"),
        ("What is the name of the process in which a metal surface is protected by coating it with zinc?", "Distillation", "Crystallization", "Electrolysis", "Galvanization", "D"),
        ("Which metal is commonly used as a sacrificial coating to protect iron from rusting?", "Zinc", "Gold", "Silver", "Mercury", "A"),
        ("What is formed when zinc reacts with dilute hydrochloric acid?", "Zinc oxide and water", "Zinc chloride and hydrogen", "Zinc carbonate and oxygen", "Zinc hydroxide only", "B"),
        ("Which statement about metals is generally correct?", "All metals are gases", "All metals are brittle", "Many metals conduct heat and electricity well", "All metals react vigorously with water", "C"),
        ("Which metal is commonly extracted from hematite?", "Aluminium", "Sodium", "Calcium", "Iron", "D"),
        ("What is the chemical formula of magnesium oxide?", "MgO", "MgO2", "Mg2O", "Mg2O3", "A"),
        ("Which of these is an amphoteric oxide?", "Sodium oxide", "Aluminium oxide", "Carbon dioxide", "Sulfur dioxide", "B"),
        ("What happens when copper is exposed to moist air containing carbon dioxide over a long period?", "It forms sodium chloride", "It melts at room temperature", "It can develop a green patina", "It turns into pure carbon", "C"),
        ("Which non-metal is commonly used in the manufacture of fertilizers and matches?", "Helium", "Neon", "Argon", "Phosphorus", "D"),
        ("Which reaction is an example of displacement?", "Zinc + copper sulfate → zinc sulfate + copper", "Water freezing into ice", "Sugar dissolving in water", "Ice melting", "A"),
        ("Why is aluminium often used in aircraft structures?", "It is the densest common metal", "It has a relatively low density and useful strength-to-weight characteristics", "It is a liquid at room temperature", "It is a non-metal", "B"),
        ("Which metal is commonly used in thermometers in older designs because it is liquid near room temperature?", "Iron", "Copper", "Mercury", "Zinc", "C"),
        ("Which statement describes an ionic compound such as sodium chloride?", "It contains only neutral metal atoms", "It is a physical mixture of sodium and chlorine", "It contains covalent bonds between sodium and chlorine atoms", "It consists of sodium and chloride ions in an ionic lattice", "D"),
        ("Which metal reacts with dilute acids to release hydrogen but is less reactive than sodium?", "Zinc", "Gold", "Silver", "Platinum", "A"),
        ("Which non-metal is a key ingredient in many sulfuric acid manufacturing processes?", "Helium", "Sulfur", "Neon", "Argon", "B"),
        ("What is the main purpose of alloying metals?", "To make every metal radioactive", "To remove all metallic properties", "To improve properties such as strength or corrosion resistance", "To ensure the metal becomes a gas", "C"),
        ("Which alloy is primarily made from copper and zinc?", "Bronze", "Steel", "Solder", "Brass", "D"),
        ("Which metal is a major component of steel?", "Iron", "Gold", "Silver", "Mercury", "A"),
        ("Which statement about metal reactivity is correct?", "Gold reacts more vigorously with water than sodium", "More reactive metals can displace less reactive metals from some salt solutions", "All metals react equally with acids", "Copper displaces sodium from sodium chloride solution", "B"),
        ("Which of these is a chemical property of a metal?", "Its color", "Its density", "Its tendency to react with acids", "Its melting point", "C"),
        ("Which substance forms when calcium reacts with oxygen?", "Calcium chloride", "Calcium sulfate", "Calcium carbonate", "Calcium oxide", "D"),
        ("Which metal is used to protect iron by sacrificial action?", "Zinc", "Gold", "Silver", "Platinum", "A"),
        ("Which statement about non-metal oxides is generally correct?", "All are basic", "Many non-metal oxides are acidic", "All are neutral", "They cannot react with water", "B"),
    ],

    "Hard": [
        ("Which equation correctly represents magnesium reacting with oxygen?", "2Mg + O2 → 2MgO", "Mg + O2 → MgO2", "Mg + O2 → Mg2O", "Mg + O2 → MgCO3", "A"),
        ("Which equation represents zinc reacting with dilute hydrochloric acid?", "Zn + HCl → ZnO + H2", "Zn + 2HCl → ZnCl2 + H2", "Zn + HCl → ZnCl2 + O2", "Zn + 2HCl → ZnO + Cl2", "B"),
        ("Why can zinc displace copper from copper sulfate solution?", "Copper is more reactive than zinc", "Zinc and copper have identical reactivity", "Zinc is more reactive than copper", "Copper sulfate is a non-metal", "C"),
        ("Which metal is generally extracted by electrolysis rather than reduction with carbon in a basic school-level extraction scheme?", "Iron", "Copper", "Lead", "Aluminium", "D"),
        ("What is the principal role of cryolite in the electrolytic extraction of aluminium?", "It helps lower the operating temperature and improve the electrolyte's conductivity", "It converts aluminium into iron", "It acts as the aluminium ore", "It prevents all electrical current", "A"),
        ("Which metal can be extracted from its oxide by reduction with carbon under suitable conditions?", "Sodium", "Iron", "Potassium", "Calcium", "B"),
        ("Which of these metals is at the top end of the common school-level reactivity series?", "Gold", "Copper", "Potassium", "Silver", "C"),
        ("What is the oxidation state of oxygen in magnesium oxide?", "+2", "0", "-1", "-2", "D"),
        ("Which equation represents the reaction of iron with steam under suitable conditions?", "3Fe + 4H2O → Fe3O4 + 4H2", "Fe + H2O → FeO + O2", "Fe + 2H2O → Fe(OH)2 + H2", "Fe + H2O → FeCl2 + H2", "A"),
        ("Why does aluminium resist corrosion better than expected from its reactivity?", "It does not react with oxygen", "A thin, protective aluminium oxide layer forms on its surface", "It is a non-metal", "It dissolves immediately in water", "B"),
        ("Which statement about ionic compounds formed between metals and non-metals is correct?", "Electrons are always shared equally", "They contain only neutral atoms in a molecule", "Electron transfer commonly produces oppositely charged ions", "They contain no electrostatic attractions", "C"),
        ("Which pair is correctly matched?", "Brass — copper and tin", "Bronze — copper and zinc", "Steel — copper and zinc only", "Brass — copper and zinc", "D"),
        ("Which metal is commonly used as the anode material in some sacrificial corrosion-protection systems for steel?", "Zinc", "Gold", "Silver", "Platinum", "A"),
        ("Which reaction shows copper being displaced from a solution by iron?", "Cu + FeSO4 → CuSO4 + Fe", "Fe + CuSO4 → FeSO4 + Cu", "Fe + Cu → FeCu", "Cu + H2O → CuO + H2", "B"),
        ("Which statement about metal oxides is most accurate?", "Every metal oxide is acidic", "Every metal oxide dissolves completely in water", "Many metal oxides are basic, while some are amphoteric", "Metal oxides contain no oxygen", "C"),
        ("Which oxide reacts with both acids and bases?", "Sodium oxide", "Carbon dioxide", "Sulfur dioxide", "Aluminium oxide", "D"),
        ("Which non-metal is essential for vulcanization of rubber?", "Sulfur", "Helium", "Neon", "Argon", "A"),
        ("What happens when copper(II) oxide reacts with dilute sulfuric acid?", "Copper and hydrogen form", "Copper(II) sulfate and water form", "Copper sulfide forms", "Copper carbonate and hydrogen form", "B"),
        ("Which statement explains why graphite conducts electricity although it is a non-metal?", "It contains freely moving protons", "It is actually a metal", "It has delocalized electrons that can move through its structure", "It contains liquid copper", "C"),
        ("Which metal is commonly protected from corrosion by tin coating in some food containers?", "Aluminium", "Sodium", "Potassium", "Iron or steel", "D"),
        ("Which statement about the reactivity series is correct?", "A more reactive metal can often displace a less reactive metal from its compound", "A less reactive metal always displaces a more reactive one", "All metals react with cold water at the same rate", "The series ranks non-metals only", "A"),
        ("Which product forms when calcium reacts with water?", "Calcium oxide and oxygen", "Calcium hydroxide and hydrogen", "Calcium chloride and hydrogen", "Calcium carbonate and oxygen", "B"),
        ("Which equation represents sodium reacting with water?", "Na + H2O → NaOH", "Na + H2O → NaO + H2", "2Na + 2H2O → 2NaOH + H2", "Na + 2H2O → NaCl + H2", "C"),
        ("Which metal is commonly used as a catalyst in some industrial hydrogenation processes?", "Sodium", "Calcium", "Magnesium", "Nickel", "D"),
        ("Why are highly reactive metals commonly stored under suitable protective liquids?", "To prevent rapid reaction with oxygen or moisture", "To make them non-metals", "To increase their electrical resistance permanently", "To convert them into noble gases", "A"),
        ("Which statement about the reaction of metals with dilute acids is correct?", "Every metal releases hydrogen from every acid", "Metals above hydrogen in the reactivity series often release hydrogen from dilute non-oxidizing acids", "Gold always releases hydrogen rapidly", "Copper always reacts with dilute hydrochloric acid to release hydrogen", "B"),
        ("Which formula represents iron(III) oxide?", "FeO", "FeO2", "Fe2O3", "Fe3O4 only", "C"),
        ("Which of these is an example of a metalloid rather than a typical metal or non-metal?", "Sodium", "Sulfur", "Copper", "Silicon", "D"),
        ("What is the main purpose of adding chromium to stainless steel?", "To improve corrosion resistance", "To make it a liquid at room temperature", "To eliminate all iron atoms", "To turn it into a pure non-metal", "A"),
        ("Which statement about metal extraction is correct?", "All metals are extracted using the same method", "The method depends on the metal's reactivity and the nature of its ore", "Gold must always be extracted by electrolysis of molten gold oxide", "Sodium is usually extracted by reducing its oxide with carbon", "B"),
    ],
}


def normalize(text):
    return " ".join(text.strip().lower().split())


def main():
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DATABASE_PATH}")

    for difficulty, questions in QUESTION_BANK.items():
        if len(questions) < TARGET_QUESTIONS:
            raise ValueError(
                f"{difficulty} bank has only {len(questions)} questions; "
                f"at least {TARGET_QUESTIONS} are required."
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

        print("\nMetals and Non-Metals expansion completed!")
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