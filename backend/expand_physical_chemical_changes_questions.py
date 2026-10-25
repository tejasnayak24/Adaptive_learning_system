
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"
LESSON_TITLE = "Physical and Chemical Changes"
TARGET_QUESTIONS = 30

QUESTION_BANK = {
    "Easy": [
        ("What is a physical change?", "A change in which no new substance is formed", "A change that always produces gas", "A change that creates a new element", "A change that always releases light", "A"),
        ("Which is an example of a physical change?", "Burning paper", "Melting ice", "Rusting iron", "Cooking an egg", "B"),
        ("Which is an example of a chemical change?", "Cutting paper", "Breaking glass", "Burning wood", "Melting wax", "C"),
        ("What is generally formed during a chemical change?", "Only a smaller object", "Only a different shape", "Only a change in state", "One or more new substances", "D"),
        ("Which change occurs when water freezes?", "Physical change", "Chemical change", "Nuclear change", "Combustion", "A"),
        ("What happens when iron rusts?", "It only changes shape", "A new substance forms", "It becomes pure water", "It melts immediately", "B"),
        ("Which process is usually reversible by simple physical means?", "Burning fuel", "Digesting food", "Melting ice", "Rusting metal", "C"),
        ("Which of these is a chemical change?", "Tearing cloth", "Dissolving sugar in water", "Breaking a stone", "Souring of milk", "D"),
        ("Which change happens when water evaporates?", "Physical change", "Chemical change", "Combustion", "Rusting", "A"),
        ("Which is a common sign of a chemical reaction?", "Only a change in size", "Formation of a new substance", "Only a change in shape", "Only movement", "B"),
        ("What type of change occurs when a candle's wax melts?", "Chemical only", "Nuclear", "Physical", "Biological only", "C"),
        ("What type of change occurs when candle wax burns?", "Physical only", "No change", "Change in shape only", "Chemical", "D"),
        ("Which process is a physical change?", "Cutting a piece of paper", "Burning a piece of paper", "Cooking rice", "Rusting iron", "A"),
        ("Which of these is a chemical change in food?", "Freezing juice", "Cooking an egg", "Chopping vegetables", "Grinding wheat", "B"),
        ("Which change occurs when sugar dissolves in water without reacting?", "Chemical change", "Nuclear change", "Physical change", "Combustion", "C"),
        ("Which is an example of a chemical change in nature?", "Water flowing in a river", "Ice melting", "A rock breaking", "Fruit ripening", "D"),
        ("What is condensation?", "A physical change from gas to liquid", "A chemical reaction with oxygen", "A change that forms a new element", "Burning a liquid", "A"),
        ("Which change occurs when a metal is hammered into a thin sheet?", "Chemical change", "Physical change", "Combustion", "Decomposition", "B"),
        ("Which of these is usually a chemical change?", "Breaking chalk", "Melting chocolate", "Burning magnesium", "Freezing water", "C"),
        ("What happens to the chemical identity of water when it freezes?", "It becomes hydrogen", "It becomes oxygen", "It forms salt", "It remains water", "D"),
        ("Which change occurs when a glass bottle breaks?", "Physical change", "Chemical change", "Oxidation", "Fermentation", "A"),
        ("Which of these is a chemical change?", "Boiling water", "Digestion of food", "Cutting a rope", "Crushing a can", "B"),
        ("Which process changes liquid water into water vapor?", "Combustion", "Rusting", "Evaporation", "Fermentation", "C"),
        ("Which is a physical change in a metal?", "Rusting", "Burning", "Chemical corrosion", "Bending a wire", "D"),
        ("Which process is associated with rust formation?", "Oxidation of iron", "Freezing of iron", "Melting of iron", "Dissolving iron in water only", "A"),
        ("Which is a physical change?", "Burning a match", "Slicing bread", "Cooking an egg", "Milk turning sour", "B"),
        ("What is sublimation?", "A liquid turning into a solid", "A gas turning into a liquid", "A solid changing directly into a gas", "A liquid turning into a new compound", "C"),
        ("Which change is involved in photosynthesis?", "Only a change of state", "Only a change of shape", "Only a physical separation", "Chemical change", "D"),
        ("Which process is generally a chemical change?", "Fermentation of sugar", "Melting ice", "Cutting paper", "Breaking glass", "A"),
        ("What is the best way to distinguish physical and chemical changes?", "By checking the object's size only", "By determining whether new substances form", "By checking whether the object moves", "By checking its color only", "B"),
        ("Which process changes a liquid into a solid without forming a new substance?", "Freezing water", "Burning petrol", "Rusting iron", "Cooking an egg", "A"),
        ("Which change occurs when steam condenses on a cool surface?", "Chemical change", "Physical change", "Combustion", "Rusting", "B"),
        ("Which process changes the shape of clay without forming a new substance?", "Burning clay", "Rusting clay", "Moulding clay", "Cooking clay", "C"),
        ("Which is an example of a chemical change in everyday life?", "Sharpening a pencil", "Tearing paper", "Melting butter", "Burning a candle wick", "D"),
        ("Which process is a physical change?", "Breaking a piece of chalk", "Burning coal", "Digesting food", "Cooking an egg", "A"),
    ],

    "Medium": [
        ("Why is melting ice considered a physical change?", "Water molecules become carbon dioxide", "Hydrogen and oxygen separate", "The substance remains H₂O", "A new element forms", "C"),
        ("Which observation alone does not prove that a chemical reaction occurred?", "A new solid forms from two solutions", "A gas forms during a reaction", "A lasting color change accompanies a reaction", "A substance changes shape", "D"),
        ("Why is burning paper a chemical change?", "New substances such as gases and ash form", "Paper only changes its shape", "The paper only changes state", "The paper remains chemically identical", "A"),
        ("Which statement about physical changes is correct?", "They always produce new compounds", "They often change state, shape, or size without changing chemical identity", "They always release light", "They cannot be reversed", "B"),
        ("Which of these is a chemical change caused by microorganisms?", "Melting butter", "Breaking a plate", "Milk fermenting into curd", "Freezing water", "C"),
        ("Which is an example of a chemical change involving oxygen?", "Melting ice", "Cutting wood", "Dissolving sugar", "Rusting iron", "D"),
        ("Which statement about dissolving salt in water is generally correct?", "It is a physical process, and the salt can be recovered by evaporation", "It always produces a new compound", "The salt atoms become oxygen", "It permanently destroys the salt", "A"),
        ("What happens during thermal decomposition?", "A substance changes shape only", "A substance breaks down chemically when heated", "A liquid freezes", "A solid is cut into pieces", "B"),
        ("Which process is a physical change even though energy is absorbed?", "Burning coal", "Rusting iron", "Melting ice", "Cooking food", "C"),
        ("Which process is an example of chemical decomposition?", "Ice melting", "Water boiling", "Glass breaking", "Hydrogen peroxide decomposing into water and oxygen", "D"),
        ("Which observation is the strongest evidence of a chemical reaction?", "A new substance with different properties forms", "A block is cut in half", "A liquid is poured into a new container", "A solid is crushed", "A"),
        ("Why is cutting wood a physical change?", "The wood becomes a new element", "The chemical composition of the wood is not fundamentally changed by cutting", "It always produces carbon dioxide", "The wood undergoes combustion", "B"),
        ("Which process is a chemical change in the human body?", "Blood flowing", "Bending an arm", "Digestion of carbohydrates", "Chewing food only", "C"),
        ("Which process is generally reversible through a physical change?", "Burning paper into ash", "Cooking an egg", "Rusting iron", "Freezing water into ice", "D"),
        ("Which statement about reversibility is correct?", "Reversibility alone does not reliably distinguish all physical and chemical changes", "Every physical change is reversible", "Every chemical change is irreversible under all conditions", "Only chemical changes can be reversed", "A"),
        ("What type of change occurs when silver tarnishes?", "Physical change only", "Chemical change", "Change in size only", "Change in shape only", "B"),
        ("Which process is a chemical change in plants?", "Water evaporating from a leaf", "A leaf falling to the ground", "Photosynthesis", "A leaf changing position", "C"),
        ("What is the main difference between boiling water and electrolyzing water?", "Both always produce new compounds", "Boiling breaks water into hydrogen", "Electrolysis only changes water's state", "Boiling is physical, while electrolysis chemically decomposes water", "D"),
        ("Which process is a chemical reaction that releases heat?", "Combustion of natural gas", "Melting ice", "Breaking a pencil", "Evaporation of water", "A"),
        ("Why is the formation of a precipitate often evidence of a chemical reaction?", "It proves that the temperature fell", "A new insoluble substance may have formed", "It proves that the liquid evaporated", "It means the container broke", "B"),
        ("Which change occurs when wax is heated and melts?", "Chemical change", "Chemical decomposition in every case", "Physical change", "Oxidation", "C"),
        ("Which process changes the chemical composition of food?", "Freezing vegetables", "Slicing fruit", "Grinding grains", "Baking a cake", "D"),
        ("Which process is an example of oxidation?", "Copper developing a green patina", "Ice melting", "Water boiling", "Sugar dissolving in water", "A"),
        ("Which statement about a chemical reaction is correct?", "Atoms are destroyed completely", "Atoms are rearranged to form new substances", "All reactions produce flames", "All reactions occur instantly", "B"),
        ("Which process is a physical separation rather than a chemical change?", "Burning a mixture", "Fermentation", "Separating sand from water by filtration", "Rust formation", "C"),
        ("Which change occurs when dry ice changes directly into carbon dioxide gas?", "Chemical reaction", "Combustion", "Decomposition", "Physical change called sublimation", "D"),
        ("Which pair consists of chemical changes?", "Burning wood and rusting iron", "Melting ice and boiling water", "Cutting paper and crushing chalk", "Dissolving sugar and freezing water", "A"),
        ("Which is not sufficient on its own to confirm a chemical reaction?", "Formation of a new gas under reaction conditions", "A change in shape", "Formation of a new precipitate", "A new substance with distinct properties", "B"),
        ("What happens to atoms during an ordinary chemical reaction?", "They vanish", "They change into different elements in every reaction", "They are rearranged, while nuclei generally remain unchanged", "They become energy only", "C"),
        ("Which process involves a chemical change followed by a physical change?", "Breaking a glass bottle", "Melting ice", "Cutting paper", "Burning a candle, followed by melting of the remaining wax", "D"),
    ],

    "Hard": [
        ("Which statement best describes conservation of mass in a chemical reaction?", "In a closed system, total mass of reactants equals total mass of products", "Mass always disappears when gas forms", "Products always weigh more than reactants", "Atoms are destroyed during combustion", "A"),
        ("Why might the measured mass decrease when a reaction produces a gas in an open container?", "Mass is destroyed by the reaction", "Some gaseous product escapes from the container", "The balance changes the chemical equation", "Atoms lose all their mass", "B"),
        ("Which equation represents chemical decomposition of water?", "H₂O → H₂O(l)", "H₂O(s) → H₂O(l)", "2H₂O → 2H₂ + O₂", "H₂O(l) → H₂O(g)", "C"),
        ("Which statement about activation energy is correct?", "It is the mass of the reactants", "It is the final temperature of a reaction", "It is energy released only after a reaction ends", "It is the minimum energy needed for a reaction pathway to proceed", "D"),
        ("Which observation most strongly supports that a new chemical substance formed?", "A reaction mixture produces a solid with different chemical properties", "A solid is ground into powder", "Water freezes", "A metal sheet is bent", "A"),
        ("Which is the balanced equation for iron reacting with oxygen to form iron(III) oxide?", "Fe + O₂ → FeO", "4Fe + 3O₂ → 2Fe₂O₃", "2Fe + O₂ → Fe₂O₃", "Fe + 3O₂ → FeO₃", "B"),
        ("Why is a color change not always proof of a chemical reaction?", "Colors never change in chemical reactions", "Color changes are impossible in mixtures", "Some physical processes can also change the observed color", "Every color change is caused by combustion", "C"),
        ("Which process is a chemical change that absorbs energy overall?", "Freezing water", "Condensation", "Breaking glass", "Photosynthesis", "D"),
        ("Which statement about a catalyst is correct?", "It provides an alternative pathway with lower activation energy and is not consumed overall", "It always changes the final equilibrium composition", "It must become the main product", "It makes every reaction instantaneous", "A"),
        ("What is the main difference between melting and combustion?", "Both form new substances", "Melting changes physical state; combustion involves chemical reactions", "Combustion is always a physical change", "Melting always changes elemental composition", "B"),
        ("Which example best illustrates a chemical reaction involving gas formation?", "Water evaporating from a puddle", "Air expanding when heated", "An acid reacting with a carbonate and releasing carbon dioxide", "Steam condensing on glass", "C"),
        ("Why should the total mass of a sealed reaction vessel remain constant during an ordinary chemical reaction?", "The vessel prevents atoms from moving", "The reaction stops all energy transfer", "The products have no mass", "Matter is conserved and no material enters or leaves", "D"),
        ("Which statement about energy in chemical reactions is correct?", "Chemical changes can release or absorb energy", "All chemical reactions release heat", "Physical changes never involve energy transfer", "Energy is created from nothing in exothermic reactions", "A"),
        ("Which process combines a chemical change with a visible energy release?", "Ice melting", "Combustion of methane", "Glass breaking", "Salt dissolving without reaction", "B"),
        ("Which equation represents the formation of water from hydrogen and oxygen?", "H₂ + O₂ → H₂O", "H₂ + O₂ → H₂O₂", "2H₂ + O₂ → 2H₂O", "H₂ + 2O₂ → H₂O", "C"),
        ("Why must chemical equations be balanced?", "To make every coefficient equal to one", "To show that products always weigh less", "To change the identity of elements", "To represent conservation of each type of atom", "D"),
        ("Which statement distinguishes a physical mixture from a chemical compound?", "Mixture components are not necessarily chemically bonded in fixed ratios", "A mixture always has a fixed formula", "A compound can always be separated by filtration", "Mixtures contain only one element", "A"),
        ("A solid dissolves in water and is recovered unchanged by evaporation. How is the process generally classified?", "Definitely a nuclear reaction", "Generally a physical change", "Always combustion", "Always chemical decomposition", "B"),
        ("Which process is a chemical change in the atmosphere?", "Water vapor condensing into clouds", "Ice crystals melting", "Formation of ozone from oxygen through photochemical reactions", "Wind moving dust", "C"),
        ("Which factor can increase the rate of many chemical reactions by increasing collision frequency or energy?", "Reducing all reactant contact", "Removing reactants", "Always lowering temperature", "Increasing temperature appropriately", "D"),
        ("What does an endothermic chemical reaction do overall?", "Absorbs energy from its surroundings", "Always releases heat", "Destroys mass", "Creates atoms from nothing", "A"),
        ("What does an exothermic chemical reaction do overall?", "Always absorbs heat", "Releases energy to its surroundings", "Cannot form new substances", "Only changes physical state", "B"),
        ("Which is an example of a chemical change in the nitrogen cycle?", "Water evaporating", "Clouds forming", "Bacteria converting nitrogen compounds through chemical reactions", "Soil particles settling", "C"),
        ("Which statement about burning magnesium is correct?", "It is a physical change because only shape changes", "It produces no new substance", "It is merely a phase transition", "It reacts with oxygen to form magnesium oxide", "D"),
        ("Why can crushing a sugar crystal be classified as a physical change?", "The sugar's shape and size change without necessarily changing its molecular identity", "It always forms carbon dioxide", "It creates a new element", "It necessarily produces caramel", "A"),
        ("Which process is a chemical change even though no flame is required?", "Melting candle wax", "Iron rusting in moist air", "Breaking a brick", "Boiling ethanol", "B"),
        ("Which statement about chemical bonds during a reaction is correct?", "No bonds ever change", "All atoms become protons", "Some bonds break and new bonds form as atoms rearrange", "Only the nuclei are rearranged in ordinary reactions", "C"),
        ("A reaction causes a temperature rise without external heating. What may this indicate?", "Only a physical change occurred", "The mass was destroyed", "The reaction absorbed all energy", "An exothermic process may have released energy", "D"),
        ("Which process is not a chemical change?", "Electrolysis of water", "Condensation of water vapor", "Combustion of propane", "Digestion of starch", "B"),
        ("Which statement best summarizes physical and chemical changes?", "Physical changes always require heating", "Chemical changes always produce a visible flame", "Physical changes affect only solids", "Chemical changes form new substances, while physical changes generally do not", "D"),
    ],
}


def normalize(text):
    return " ".join(text.strip().lower().split())


def main():
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DATABASE_PATH}")

    # Allow extra candidate questions so duplicates can be skipped.
    for difficulty, questions in QUESTION_BANK.items():
        if len(questions) < TARGET_QUESTIONS:
            raise ValueError(
                f"{difficulty} bank has only {len(questions)} questions; "
                f"at least {TARGET_QUESTIONS} are required."
            )

        normalized_bank = [normalize(q[0]) for q in questions]
        if len(normalized_bank) != len(set(normalized_bank)):
            print(
                f"Note: {difficulty} bank contains repeated question text; "
                "duplicates will be skipped."
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

        print("\nPhysical and Chemical Changes expansion completed!")
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
