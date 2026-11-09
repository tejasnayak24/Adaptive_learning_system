import sqlite3
from pathlib import Path

DATABASE_PATH = (
    Path(__file__).resolve().parent.parent / "adaptive_learning.db"
)

TARGET_QUESTIONS = 30
LESSON_TITLE = "Photosynthesis"

QUESTION_BANK = {
    "Easy": [
        ("What is photosynthesis?", ["The process by which plants make food", "The process of breathing", "The process of absorbing minerals", "The process of seed formation"], "A"),
        ("Which gas do plants absorb during photosynthesis?", ["Oxygen", "Carbon dioxide", "Nitrogen", "Hydrogen"], "B"),
        ("Which gas is released during photosynthesis?", ["Carbon dioxide", "Nitrogen", "Oxygen", "Hydrogen"], "C"),
        ("Which part of a plant mainly carries out photosynthesis?", ["Root", "Flower", "Stem", "Leaf"], "D"),
        ("Which green pigment helps plants absorb light?", ["Chlorophyll", "Haemoglobin", "Melanin", "Keratin"], "A"),
        ("What is the main source of energy for photosynthesis?", ["Moonlight", "Sunlight", "Soil", "Wind"], "B"),
        ("Which substance do plants absorb from the soil for photosynthesis?", ["Oxygen", "Sugar", "Water", "Starch"], "C"),
        ("Where is chlorophyll mainly found?", ["Nucleus", "Cell wall", "Vacuole", "Chloroplast"], "D"),
        ("Which of these is produced during photosynthesis?", ["Glucose", "Sand", "Protein only", "Nitrogen"], "A"),
        ("Which part of a plant absorbs most of its water?", ["Flowers", "Roots", "Fruits", "Seeds"], "B"),
        ("Which gas is present in the air and used by plants to make food?", ["Helium", "Oxygen", "Carbon dioxide", "Neon"], "C"),
        ("What is the usual colour of chlorophyll?", ["Red", "Blue", "Yellow", "Green"], "D"),
        ("Which of these is an essential requirement for photosynthesis?", ["Light", "Plastic", "Salt crystals", "Sound"], "A"),
        ("In which organelle does photosynthesis occur?", ["Mitochondrion", "Chloroplast", "Ribosome", "Nucleus"], "B"),
        ("What type of organism can make its own food using sunlight?", ["Lion", "Mushroom", "Green plant", "Earthworm"], "C"),
        ("What is the food-making process in green plants called?", ["Digestion", "Respiration", "Transpiration", "Photosynthesis"], "D"),
        ("Which part of sunlight is captured by chlorophyll?", ["Light energy", "Sound energy", "Chemical energy from soil", "Nuclear energy"], "A"),
        ("What is glucose?", ["A mineral", "A simple sugar", "A gas", "A plant pigment"], "B"),
        ("Which material provides carbon for glucose formation?", ["Soil", "Oxygen gas", "Carbon dioxide", "Nitrogen gas"], "C"),
        ("Which of these is NOT directly required as a raw material for photosynthesis?", ["Water", "Carbon dioxide", "Light energy", "Oxygen"], "D"),
        ("What do plants use glucose for?", ["Energy and growth", "Making sunlight", "Creating soil", "Producing minerals"], "A"),
        ("Which structure allows gases to enter and leave many leaves?", ["Petals", "Stomata", "Root caps", "Seeds"], "B"),
        ("Which plant part transports water from roots toward leaves?", ["Fruit", "Flower", "Xylem", "Seed coat"], "C"),
        ("What is the main role of leaves in most green plants?", ["Absorbing minerals only", "Anchoring the plant", "Producing seeds only", "Making food"], "D"),
        ("Which of these is a product of photosynthesis?", ["Sugar", "Carbon dioxide only", "Soil", "Water only"], "A"),
        ("What usually happens to photosynthesis when a plant receives no light?", ["It becomes faster", "Its rate greatly decreases or stops", "It produces more light", "It requires no water"], "B"),
        ("Which part of a plant usually contains the most chlorophyll?", ["Roots", "Dry seeds", "Green leaves", "Petals of every flower"], "C"),
        ("What is sunlight converted into during photosynthesis?", ["Sound energy", "Wind energy", "Electrical energy directly", "Chemical energy stored in sugars"], "D"),
        ("Why are most leaves broad and flat?", ["To capture more sunlight", "To absorb soil", "To prevent all gas exchange", "To store stones"], "A"),
        ("Which statement about photosynthesis is correct?", ["Only animals perform it", "Green plants use light energy to make food", "It always occurs without water", "It produces no chemical energy"], "B"),
    ],

    "Medium": [
        ("Which word equation best represents photosynthesis?", ["Glucose + oxygen → carbon dioxide + water", "Water + oxygen → glucose + carbon dioxide", "Carbon dioxide + water → glucose + oxygen, using light", "Nitrogen + glucose → water + oxygen"], "C"),
        ("Why is chlorophyll important for photosynthesis?", ["It absorbs minerals from soil", "It transports glucose through roots", "It releases carbon dioxide", "It absorbs light energy"], "D"),
        ("What is the main function of stomata in photosynthesis?", ["Allow gas exchange", "Absorb sunlight through roots", "Produce chlorophyll", "Transport sugars in the phloem"], "A"),
        ("Why might a plant kept in darkness for several days have little starch in its leaves?", ["Its roots stop absorbing water permanently", "It uses stored carbohydrates and cannot replenish them through photosynthesis", "It absorbs extra sunlight", "Its leaves produce unlimited glucose"], "B"),
        ("What would most directly limit photosynthesis if carbon dioxide became very scarce?", ["The amount of soil around the pot", "The colour of the roots", "The supply of carbon needed to form sugars", "The number of seeds in the fruit"], "C"),
        ("Why is a leaf often tested for starch in a photosynthesis experiment?", ["Starch is the gas released", "Starch absorbs all sunlight", "Starch replaces chlorophyll", "Starch indicates that sugars have been produced and stored"], "D"),
        ("What is the purpose of covering part of a leaf with opaque paper during a light experiment?", ["To test whether light is needed for starch formation", "To increase carbon dioxide around the leaf", "To measure root growth", "To prevent water entering the roots"], "A"),
        ("Why is a plant often destarched before testing a leaf for starch?", ["To make its leaves colourless permanently", "To reduce previously stored starch that could affect the result", "To remove all chlorophyll", "To stop water transport"], "B"),
        ("If light intensity increases while other factors remain suitable, what may happen to photosynthesis?", ["It always decreases", "It stops immediately", "Its rate may increase until another factor becomes limiting", "It no longer needs carbon dioxide"], "C"),
        ("Which tissue transports sugars made in the leaves to other plant parts?", ["Xylem", "Epidermis", "Cork", "Phloem"], "D"),
        ("Why do plants need both xylem and phloem?", ["They transport different materials through the plant", "Both only transport sunlight", "Both produce chlorophyll", "They are used only during seed germination"], "A"),
        ("What may happen to the rate of photosynthesis when temperature rises from a very low level to a suitable level?", ["It must become zero", "It may increase because enzyme-controlled reactions become faster", "It removes the need for light", "It stops all gas exchange"], "B"),
        ("Why can extremely high temperatures reduce photosynthesis?", ["They create more chlorophyll in every case", "They turn carbon dioxide into soil", "They can damage enzymes and cause excessive water loss", "They eliminate the need for water"], "C"),
        ("A plant receives light and water but has very little carbon dioxide. Which factor is most likely limiting photosynthesis?", ["Light", "Water", "Chlorophyll colour", "Carbon dioxide"], "D"),
        ("Why are plants often placed in sunlight after being destarched?", ["To allow photosynthesis to produce new starch", "To remove all leaf cells", "To stop carbon dioxide entering", "To convert chlorophyll into soil"], "A"),
        ("What is the role of water in photosynthesis?", ["It acts only as a pigment", "It supplies hydrogen and electrons for the reactions", "It is the source of the carbon atoms in glucose", "It prevents light absorption"], "B"),
        ("Which observation supports the idea that light is needed for starch production in a leaf?", ["Both covered and uncovered areas turn blue-black equally", "The whole leaf contains no cells", "Only the illuminated area turns blue-black after iodine testing", "The roots become green"], "C"),
        ("Why is iodine solution used in a leaf starch test?", ["It measures carbon dioxide directly", "It measures light intensity", "It identifies oxygen", "It turns blue-black when starch is present"], "D"),
        ("What is a likely result when a healthy green plant is deprived of carbon dioxide in light?", ["Photosynthesis will be severely limited", "It will produce unlimited glucose", "It will not need chlorophyll", "It will convert nitrogen directly into sunlight"], "A"),
        ("Which statement distinguishes photosynthesis from respiration?", ["Both processes only occur in animals", "Photosynthesis stores light energy in sugars, while respiration releases usable energy from food", "Respiration produces sunlight", "Photosynthesis breaks down all glucose for energy"], "B"),
        ("Why do plants photosynthesise less effectively when their stomata remain closed for a long time?", ["Their leaves receive too much carbon", "Their roots begin producing sunlight", "Less carbon dioxide can enter the leaves", "Their chloroplasts become flowers"], "C"),
        ("Which factor is commonly studied when measuring oxygen bubbles from an aquatic plant?", ["Number of soil particles", "Colour of the container only", "Age of the observer", "Rate of photosynthesis"], "D"),
        ("Why should a fair experiment change only one photosynthesis factor at a time?", ["To identify the effect of that factor", "To make every result identical", "To prevent plants from having cells", "To remove the need for measurements"], "A"),
        ("What is likely to happen to photosynthesis if a plant lacks magnesium, needed for chlorophyll formation?", ["It will produce more chlorophyll", "Chlorophyll production may decrease and photosynthesis may be impaired", "It will no longer need light", "Its leaves will absorb nitrogen gas as food"], "B"),
        ("Why do many plants have more stomata on the lower surface of leaves?", ["The lower surface makes all the glucose", "The lower surface absorbs water directly from soil", "It can reduce water loss while allowing gas exchange", "Stomata produce sunlight"], "C"),
        ("What happens to the oxygen released during photosynthesis?", ["It is always stored permanently in roots", "It becomes chlorophyll directly", "It is converted into soil minerals", "Some diffuses out of the plant into the surroundings"], "D"),
        ("A plant is given light, water and carbon dioxide, but its leaves are damaged and lack chlorophyll. What is the likely effect?", ["Photosynthesis will be greatly reduced", "Photosynthesis will become unlimited", "The plant will make glucose without light energy", "The plant will absorb glucose from the air"], "A"),
        ("Why is the rate of photosynthesis not always increased by adding more light?", ["Plants cannot absorb any light", "Another factor, such as carbon dioxide or temperature, may become limiting", "Light changes directly into nitrogen", "Water becomes unnecessary"], "B"),
        ("Which substance stores chemical energy produced during photosynthesis?", ["Carbon dioxide", "Oxygen gas", "Glucose", "Chlorophyll alone"], "C"),
        ("Why is photosynthesis important to most food chains?", ["It removes every mineral from soil", "It prevents all organisms from respiring", "It creates energy from nothing", "It converts light energy into chemical energy available to organisms"], "D"),
    ],

    "Hard": [
        ("A plant is kept in darkness for 48 hours and then one leaf is partly covered before exposure to light. After an iodine test, which result is expected?", ["The uncovered area turns blue-black, while the covered area does not", "The covered area turns blue-black but the uncovered area does not", "Both areas must remain blue-black", "Both areas produce starch without light"], "A"),
        ("In a photosynthesis experiment, increasing light intensity raises oxygen output at first, but further increases have little effect. What best explains this plateau?", ["The plant has stopped needing carbon dioxide", "Another factor has become limiting", "Chlorophyll now produces nitrogen", "Photosynthesis no longer uses enzymes"], "B"),
        ("An aquatic plant produces 12 oxygen bubbles per minute at one light intensity and 24 per minute at a higher intensity. What is the simplest interpretation, assuming bubble size is similar?", ["Photosynthesis has stopped", "The plant has consumed all its chlorophyll", "The estimated photosynthetic rate has doubled", "The plant is producing no oxygen"], "C"),
        ("Why might counting oxygen bubbles be an imperfect method of measuring photosynthesis?", ["Oxygen is never produced", "Bubble counting measures root length", "Every bubble always contains exactly the same gas volume", "Bubble sizes may vary, so counts may not represent equal gas volumes"], "D"),
        ("A plant receives abundant light and carbon dioxide but has insufficient water. Why can photosynthesis decline?", ["Water is a reactant, and water stress can cause stomata to close", "Water is the only source of carbon atoms in glucose", "Water directly replaces chlorophyll", "Water prevents all enzyme activity at normal temperatures"], "A"),
        ("Which conclusion is justified if a leaf area exposed to light turns blue-black with iodine while its covered area remains brown?", ["Light is unnecessary for starch formation", "Light exposure was associated with starch formation in the tested conditions", "The covered area produced more starch", "Iodine directly measures oxygen concentration"], "B"),
        ("A student wants to test whether carbon dioxide is necessary for photosynthesis. Which design is best?", ["Place two plants in different temperatures and compare height", "Cover both plants completely with opaque paper", "Keep similar destarched plants under the same light, but remove carbon dioxide from one setup", "Give one plant water and the other no water"], "C"),
        ("Why is potassium hydroxide or soda lime sometimes placed in a sealed plant experiment?", ["To provide extra oxygen", "To increase light intensity", "To produce chlorophyll", "To absorb carbon dioxide from the air"], "D"),
        ("If carbon dioxide concentration is increased while light intensity is extremely low, why might photosynthesis increase only slightly?", ["Low light remains a limiting factor", "Carbon dioxide prevents chlorophyll formation in every case", "The plant no longer needs water", "Oxygen becomes the only raw material"], "A"),
        ("Two identical plants receive the same light and carbon dioxide, but one is kept at a temperature far above its optimum. Why may it photosynthesise more slowly?", ["High temperature always increases enzyme activity without limit", "Photosynthetic enzymes may lose function and water loss may increase", "The plant changes all glucose into chlorophyll", "The leaves stop containing carbon"], "B"),
        ("Which statement correctly describes the source of the oxygen released in oxygenic photosynthesis?", ["It comes from glucose breaking down in the leaf", "It comes directly from carbon dioxide atoms in every released oxygen molecule", "It is produced from the splitting of water during the light-dependent reactions", "It comes from nitrogen in the soil"], "C"),
        ("Why is carbon dioxide called a carbon source for photosynthesis?", ["It supplies the energy of sunlight", "It forms chlorophyll without other materials", "It is the gas released by water splitting", "Its carbon atoms are incorporated into organic molecules such as sugars"], "D"),
        ("A plant's photosynthesis rate is measured at increasing carbon dioxide concentrations. The rate rises and then levels off. What is the best explanation?", ["Carbon dioxide is no longer the main limiting factor and another constraint dominates", "The plant has started photosynthesising without light", "The plant has converted all water into oxygen", "Carbon dioxide destroys every chloroplast at high concentration"], "A"),
        ("A leaf has green and white regions. After exposure to light, only the green regions test positive for starch. What does this suggest?", ["White regions contain more chlorophyll", "Chlorophyll is necessary for starch formation under these conditions", "Light is not involved in starch formation", "White regions contain no living cells under all circumstances"], "B"),
        ("Why must a leaf be decolourised with alcohol during a standard iodine starch test?", ["To increase its starch content", "To make the leaf absorb more carbon dioxide", "To remove chlorophyll so the iodine colour change can be observed clearly", "To convert starch into glucose"], "C"),
        ("In a controlled experiment, a plant exposed to bright light has closed stomata. Which immediate effect is most likely?", ["Carbon dioxide entry increases without limit", "Glucose production becomes independent of carbon dioxide", "Oxygen production always doubles", "Carbon dioxide entry decreases, potentially limiting carbon fixation"], "D"),
        ("Why can photosynthesis continue to increase with light intensity only up to a certain point?", ["The plant's photosynthetic machinery and other required factors impose limits", "Plants cannot absorb visible light", "Increasing light always removes carbon dioxide", "Glucose cannot store chemical energy"], "A"),
        ("A scientist measures the mass of dry plant material over several weeks. Which process is the principal source of much of the carbon incorporated into new plant biomass?", ["Absorption of soil particles through roots", "Fixation of carbon dioxide during photosynthesis", "Absorption of glucose through leaves from the air", "Conversion of minerals directly into carbon"], "B"),
        ("Which result would most strongly support the claim that carbon dioxide is required for photosynthesis?", ["A plant grows in soil", "A leaf contains chlorophyll", "A destarched plant without available carbon dioxide forms less starch than a comparable control in light", "Roots absorb water from moist soil"], "C"),
        ("Why does photosynthesis generally stop or slow substantially at night in most plants?", ["Plants lose all their chlorophyll after sunset", "Carbon dioxide disappears from the atmosphere at night", "Water cannot move through xylem at night", "Light-dependent reactions lack sufficient light energy"], "D"),
        ("An experiment finds that doubling light intensity has no effect, but increasing carbon dioxide raises oxygen output. What was most likely limiting the rate initially?", ["Carbon dioxide availability", "The number of roots", "The colour of the pot", "The number of petals"], "A"),
        ("Which combination is most likely to support a high photosynthetic rate in a healthy green plant, assuming values remain within safe limits?", ["No light, no water and high oxygen", "Suitable light, sufficient carbon dioxide, adequate water and an appropriate temperature", "Very high temperature and closed stomata", "No chlorophyll and abundant minerals"], "B"),
        ("Why does photosynthesis matter for atmospheric carbon cycling?", ["It converts oxygen into sunlight", "It destroys all atmospheric gases", "It removes carbon dioxide from the environment and incorporates carbon into organic compounds", "It turns every carbon atom into a mineral"], "C"),
        ("A plant is exposed to light, but a chemical blocks electron transport in the chloroplasts. What is the likely consequence?", ["Photosynthesis becomes independent of chloroplasts", "Carbon dioxide is converted directly into light", "Oxygen output increases without limit", "The light-dependent reactions and overall photosynthesis are impaired"], "D"),
        ("Why can a plant in very dry conditions show a reduced photosynthetic rate even before leaves visibly wilt?", ["Stomatal closure can reduce carbon dioxide uptake", "Dry conditions create unlimited carbon dioxide", "Chlorophyll begins absorbing soil", "The plant stops requiring enzymes"], "A"),
        ("A student compares photosynthesis at 15°C, 25°C and 45°C while keeping light and carbon dioxide constant. The highest rate occurs at 25°C. What is the most reasonable conclusion?", ["Photosynthesis always increases as temperature rises", "The tested plant has a temperature optimum near 25°C under those conditions", "Temperature has no effect on photosynthesis", "The plant cannot photosynthesise at 15°C"], "B"),
        ("Which explanation best links photosynthesis to the oxygen available for aerobic organisms?", ["Photosynthesis uses up all oxygen in the atmosphere", "Oxygen is produced only by animal respiration", "Oxygen released by photosynthetic organisms contributes to atmospheric and aquatic oxygen", "Photosynthesis converts oxygen into nitrogen"], "C"),
        ("Why should control plants in a photosynthesis experiment be as similar as possible to experimental plants?", ["To ensure all plants receive different conditions", "To avoid recording any results", "To guarantee the desired outcome", "To reduce confounding variables so differences can be linked to the tested factor"], "D"),
        ("A researcher finds a low photosynthetic rate despite adequate light, carbon dioxide and water. Which additional factor could explain the result?", ["A deficiency of an essential mineral needed for normal plant function", "The presence of a pot label", "The plant's position in a numbered list", "The use of a transparent ruler nearby"], "A"),
        ("Which statement best explains why photosynthesis is considered an energy-conversion process?", ["It creates energy from nothing", "It converts light energy into chemical energy stored in organic molecules", "It converts all glucose into sunlight", "It changes matter into energy without any energy input"], "B"),
    ],
}


def normalize(text):
    return " ".join(text.casefold().split())


def main():
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DATABASE_PATH}"
        )

    connection = sqlite3.connect(str(DATABASE_PATH))

    try:
        with connection:
            connection.execute("PRAGMA foreign_keys = ON")
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT id
                FROM lessons
                WHERE LOWER(TRIM(title)) = LOWER(TRIM(?))
                """,
                (LESSON_TITLE,),
            )
            lesson = cursor.fetchone()

            if lesson is None:
                raise RuntimeError(
                    f"Lesson '{LESSON_TITLE}' was not found."
                )

            lesson_id = lesson[0]
            inserted_total = 0

            for difficulty, questions in QUESTION_BANK.items():
                cursor.execute(
                    """
                    SELECT id
                    FROM quizzes
                    WHERE lesson_id = ?
                      AND LOWER(TRIM(difficulty)) = LOWER(TRIM(?))
                    ORDER BY id
                    """,
                    (lesson_id, difficulty),
                )
                quiz_rows = cursor.fetchall()

                if not quiz_rows:
                    raise RuntimeError(
                        f"No {difficulty} quiz found for {LESSON_TITLE}."
                    )

                if len(quiz_rows) > 1:
                    raise RuntimeError(
                        f"Multiple {difficulty} quizzes found for "
                        f"{LESSON_TITLE}; no questions were changed."
                    )

                quiz_id = quiz_rows[0][0]

                cursor.execute(
                    "SELECT question FROM questions WHERE quiz_id = ?",
                    (quiz_id,),
                )
                existing = {
                    normalize(row[0])
                    for row in cursor.fetchall()
                }

                available = []
                for question, options, answer in questions:
                    if normalize(question) in existing:
                        continue
                    available.append((question, options, answer))

                cursor.execute(
                    "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                    (quiz_id,),
                )
                current_count = cursor.fetchone()[0]

                needed = TARGET_QUESTIONS - current_count

                if needed < 0:
                    raise RuntimeError(
                        f"{difficulty} already has {current_count} questions."
                    )

                if len(available) < needed:
                    raise RuntimeError(
                        f"{difficulty}: need {needed} new questions, "
                        f"but only {len(available)} unique questions are available. "
                        "No changes were committed."
                    )

                for question, options, answer in available[:needed]:
                    cursor.execute(
                        """
                        INSERT INTO questions (
                            quiz_id, question,
                            option_a, option_b, option_c, option_d,
                            correct_answer
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            quiz_id,
                            question,
                            options[0],
                            options[1],
                            options[2],
                            options[3],
                            answer,
                        ),
                    )
                    inserted_total += 1

                cursor.execute(
                    "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                    (quiz_id,),
                )
                final_count = cursor.fetchone()[0]

                if final_count != TARGET_QUESTIONS:
                    raise RuntimeError(
                        f"{difficulty}: expected {TARGET_QUESTIONS}, "
                        f"found {final_count}. No changes were committed."
                    )

                print(
                    f"{difficulty}: added {needed}; "
                    f"final count = {final_count}"
                )

        print("\nPhotosynthesis expansion completed!")
        print(f"Total new questions inserted: {inserted_total}")
        print("Easy: 30 questions")
        print("Medium: 30 questions")
        print("Hard: 30 questions")
        print("Other lessons and Social Science were not modified.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()