import sqlite3
from pathlib import Path

DATABASE_PATH = (
    Path(__file__).resolve().parent.parent
    / "adaptive_learning.db"
)

TARGET_QUESTIONS = 30

QUESTION_BANK = {
    "Easy": [
        ("Which part of a plant usually absorbs water from the soil?", "Root", "Flower", "Fruit", "Leaf", "A"),
        ("Which part of a plant mainly prepares food through photosynthesis?", "Root", "Leaf", "Flower", "Seed", "B"),
        ("Which pigment absorbs light for photosynthesis?", "Chlorophyll", "Haemoglobin", "Melanin", "Keratin", "A"),
        ("Which plant part usually supports leaves and transports substances?", "Root hair", "Petal", "Stem", "Seed coat", "C"),
        ("Which plant part develops into a fruit after fertilization in flowering plants?", "Root", "Stem", "Leaf", "Ovary", "D"),
        ("What is the main function of roots?", "Absorb water and minerals and anchor the plant", "Produce pollen", "Make seeds directly", "Attract pollinators only", "A"),
        ("Which gas do plants take in during photosynthesis?", "Oxygen", "Carbon dioxide", "Nitrogen", "Hydrogen", "B"),
        ("Which gas is released during photosynthesis?", "Carbon dioxide", "Nitrogen", "Oxygen", "Methane", "C"),
        ("Which part of a flower commonly attracts pollinators with its colour?", "Sepal", "Root", "Stem", "Petal", "D"),
        ("What is the main function of a seed?", "Develop into a new plant under suitable conditions", "Absorb minerals throughout the plant's life", "Transport blood", "Produce pollen in every plant", "A"),
        ("Which structures in leaves allow gas exchange?", "Root caps", "Stomata", "Petals", "Seed coats", "B"),
        ("What is the name of the process by which plants make food using light?", "Respiration", "Transpiration", "Photosynthesis", "Germination", "C"),
        ("Which of these is a flowering plant?", "Moss", "Fern", "Pine", "Sunflower", "D"),
        ("Which plant tissue transports water and dissolved minerals from roots?", "Xylem", "Phloem", "Epidermis only", "Pollen", "A"),
        ("Which plant tissue transports sugars from sources to other parts of the plant?", "Xylem", "Phloem", "Cork only", "Root cap", "B"),
        ("What is germination?", "The production of fruit only", "The loss of all leaves", "The beginning of growth of a seed into a seedling", "The movement of pollen by wind", "C"),
        ("Which part of a plant anchors it in the soil?", "Flower", "Fruit", "Leaf", "Root", "D"),
        ("What is the main function of a flower in flowering plants?", "Sexual reproduction", "Absorb water from soil", "Anchor the plant", "Transport water only", "A"),
        ("What is transpiration?", "The production of seeds", "The loss of water vapour from aerial plant parts", "The absorption of sunlight by roots", "The formation of soil", "B"),
        ("Which mineral nutrient is important for chlorophyll formation?", "Sodium only", "Gold", "Magnesium", "Silver", "C"),
        ("What is a plant embryo?", "A mature fruit", "A fully grown tree", "A leaf without veins", "The young developing plant inside a seed", "D"),
        ("Which part protects a flower when it is still a bud?", "Sepal", "Root hair", "Xylem vessel", "Seed", "A"),
        ("Which of these is a non-flowering plant?", "Rose", "Fern", "Mango", "Hibiscus", "B"),
        ("What do plants generally need for photosynthesis?", "Only oxygen and darkness", "Only soil and wind", "Light, water, and carbon dioxide", "Only minerals and oxygen", "C"),
        ("Which structure contains the ovules in a typical flowering plant?", "Anther", "Filament", "Petal", "Ovary", "D"),
        ("Which part of a flower produces pollen?", "Anther", "Stigma", "Sepal", "Ovary", "A"),
        ("What is the function of the stigma?", "Absorb minerals from soil", "Receive pollen during pollination", "Transport water to leaves", "Protect roots", "B"),
        ("Which plant structure connects the leaf blade to the stem in many plants?", "Root cap", "Anther", "Petiole", "Seed coat", "C"),
        ("What is a seed coat?", "A structure that absorbs sunlight", "A tube that carries water", "A flower's male part", "The protective outer covering of a seed", "D"),
        ("Which of these is a plant's main source of energy for photosynthesis?", "Sunlight", "Soil", "Oxygen", "Mineral salts alone", "A"),
    ],

    "Medium": [
        ("Why are root hairs useful to plants?", "They produce pollen", "They increase the surface area for water and mineral absorption", "They make seeds directly", "They prevent all respiration", "B"),
        ("What is the role of stomata in leaves?", "Produce seeds", "Transport sugars through phloem", "Allow gas exchange and water vapour loss", "Anchor the plant", "C"),
        ("Why is xylem important?", "It transports sugars from leaves only", "It produces pollen", "It absorbs sunlight", "It transports water and minerals through the plant", "D"),
        ("How does phloem differ from xylem?", "Phloem transports sugars and other organic substances", "Phloem transports only oxygen", "Phloem forms the seed coat", "Phloem absorbs sunlight", "A"),
        ("What is the main function of chloroplasts?", "Store urine", "Carry out photosynthesis", "Transport blood", "Produce pollen in all plants", "B"),
        ("Why do most leaves have a broad, flat surface?", "To reduce all light absorption", "To prevent gas exchange", "To capture light efficiently and support gas exchange", "To replace roots", "C"),
        ("What happens to a plant that cannot absorb enough water?", "It always grows faster", "It produces unlimited seeds", "It stops needing minerals", "It may wilt and its growth may be reduced", "D"),
        ("Which process moves water through a selectively permeable membrane from a region of higher water potential to lower water potential?", "Osmosis", "Pollination", "Fertilization", "Germination", "A"),
        ("What is pollination?", "The formation of roots", "The transfer of pollen from anther to stigma", "The absorption of water by roots", "The opening of stomata only", "B"),
        ("What is fertilization in flowering plants?", "The movement of pollen through air", "The formation of a leaf", "Fusion of male and female gametes", "The loss of water vapour", "C"),
        ("Which condition is usually necessary for most seeds to germinate?", "Bright light in every species", "Fertilizer in every case", "A mature flower", "Suitable water, oxygen, and temperature", "D"),
        ("Why is nitrogen important for plant growth?", "It is needed to make amino acids and nucleic acids", "It replaces sunlight", "It prevents water absorption", "It is the main component of every fruit's sugar", "A"),
        ("What is the main role of guard cells?", "Produce pollen", "Regulate the opening and closing of stomata", "Form the seed embryo", "Transport water through xylem only", "B"),
        ("Why do plants need magnesium?", "To form cellulose only", "To produce animal haemoglobin", "It is part of the chlorophyll molecule", "To replace carbon dioxide", "C"),
        ("What is the function of the root cap?", "Absorb sunlight", "Receive pollen", "Produce fruit", "Protect the growing root tip", "D"),
        ("How does a plant generally respond to light coming from one direction?", "The shoot may grow towards the light", "The shoot always grows away from the light", "The roots produce flowers immediately", "All leaves stop growing", "A"),
        ("What is phototropism?", "Growth in response to gravity only", "Directional growth in response to light", "The loss of water vapour", "The fusion of gametes", "B"),
        ("What is gravitropism?", "Growth in response to sound", "The production of chlorophyll only", "Directional growth in response to gravity", "The movement of pollen by insects", "C"),
        ("Why do many plants close their stomata during water stress?", "To increase water loss", "To stop all cellular respiration", "To prevent roots from absorbing minerals", "To reduce water loss through transpiration", "D"),
        ("Which statement about photosynthesis is correct?", "Light energy is converted into chemical energy stored in organic molecules", "Plants convert oxygen directly into sunlight", "Photosynthesis occurs only in roots", "Photosynthesis does not require any energy input", "A"),
        ("What is the function of the anther?", "Receive pollen", "Produce pollen grains", "Protect the root tip", "Transport sugars", "B"),
        ("What is the function of the ovule after successful fertilization?", "It becomes the stem", "It produces chlorophyll for the whole plant", "It generally develops into a seed", "It becomes the root cap", "C"),
        ("What does the ovary usually develop into after fertilization?", "Root", "Leaf", "Pollen grain", "Fruit", "D"),
        ("Why are leaves often arranged to reduce excessive overlap?", "To improve access to light", "To prevent all photosynthesis", "To stop gas exchange", "To eliminate the need for roots", "A"),
        ("What is the main role of the cuticle on many leaves?", "Absorb pollen", "Reduce uncontrolled water loss", "Transport sugars", "Produce seeds", "B"),
        ("Which tissue commonly forms the outer protective layer of a young plant organ?", "Phloem", "Xylem", "Epidermis", "Pollen", "C"),
        ("Why do plants need phosphorus?", "It replaces every other nutrient", "It prevents seed formation", "It is the only element in chlorophyll", "It is important in ATP, nucleic acids, and membranes", "D"),
        ("What is the main function of the filament in a flower?", "Support the anther", "Receive pollen", "Develop into a fruit", "Absorb minerals from soil", "A"),
        ("What is seed dispersal?", "The production of chlorophyll", "The movement of seeds away from the parent plant", "The absorption of water by root hairs", "The transfer of pollen to the stigma", "B"),
        ("Why can seed dispersal benefit a plant species?", "It ensures every seed survives", "It removes the need for germination", "It can reduce competition with the parent plant and help colonize new areas", "It prevents all environmental changes", "C"),
    ],

    "Hard": [
        ("A plant's roots absorb water, but its xylem is severely damaged. What is a likely result?", "Water transport to aerial parts becomes impaired", "Sugar production immediately doubles", "Pollen production stops in every nearby plant", "The plant no longer needs water", "A"),
        ("Why does water generally move upward through xylem in tall plants?", "Water is pumped by the heart", "Transpiration pull, cohesion, and adhesion help maintain water movement", "Gravity pushes water upward", "Phloem creates all the water", "B"),
        ("What is the likely effect of closing stomata during a drought?", "Carbon dioxide entry always increases", "Transpiration becomes unlimited", "Water loss decreases, but carbon dioxide uptake may also decrease", "Photosynthesis becomes independent of light", "C"),
        ("Why can a lack of magnesium cause leaves to become yellow?", "Magnesium is the only component of cellulose", "Magnesium replaces all plant proteins", "It prevents roots from existing", "Magnesium is needed for chlorophyll, so deficiency can reduce chlorophyll formation", "D"),
        ("A ring of bark containing phloem is removed from a tree trunk while xylem remains mostly intact. What may happen above the ring over time?", "Sugars can accumulate because downward phloem transport is interrupted", "Water transport immediately increases without limit", "The tree no longer performs photosynthesis", "The roots become leaves", "A"),
        ("Why can excessive fertilizer damage plants and nearby waterways?", "It always increases biodiversity", "High salt concentrations can harm roots, and nutrient runoff can cause eutrophication", "It removes all dissolved minerals", "It prevents algae from growing under every condition", "B"),
        ("How does auxin commonly contribute to shoot phototropism?", "It prevents all cell elongation", "It converts leaves into roots", "Unequal auxin distribution can promote greater elongation on the shaded side", "It makes light unnecessary for every plant process", "C"),
        ("Why can a seed remain dormant even when it is alive?", "It has no genetic material", "It never requires water", "It has already become a mature tree", "Conditions or internal dormancy mechanisms may prevent germination", "D"),
        ("What is the ecological advantage of fruit formation in many flowering plants?", "Fruits can protect seeds and aid their dispersal", "Fruits always perform most water absorption", "Fruits replace the need for photosynthesis", "Fruits prevent reproduction", "A"),
        ("Why is the palisade mesophyll often located near the upper surface of a leaf?", "It absorbs minerals directly from soil", "It is positioned to receive substantial incoming light", "It transports urine", "It produces pollen grains", "B"),
        ("What would likely happen if a plant's root hairs were severely reduced?", "Water absorption always increases", "The plant stops needing minerals", "The effective surface area for absorption would decrease", "The leaves immediately become roots", "C"),
        ("Why can waterlogged soil harm many terrestrial plants?", "It increases oxygen availability to roots indefinitely", "It prevents every microorganism from existing", "It removes all gravitational effects", "Oxygen availability to roots may decline, impairing respiration", "D"),
        ("What is the significance of the proton gradient in chloroplasts during photosynthesis?", "It helps drive ATP synthesis", "It turns chlorophyll into soil", "It replaces carbon dioxide", "It prevents light absorption", "A"),
        ("Which process directly fixes carbon dioxide into organic molecules in the Calvin cycle?", "Water splitting in the light reactions", "Carbon fixation by the enzyme RuBisCO", "Pollen formation", "Seed dispersal", "B"),
        ("Why can plants show reduced growth when soil lacks nitrate ions?", "Nitrate is the main source of sunlight", "Nitrate replaces water in every reaction", "Nitrogen availability can limit amino acid and protein synthesis", "Nitrate is the only source of carbon", "C"),
        ("What is the role of the Casparian strip in roots?", "Produce pollen", "Carry out photosynthesis", "Form the petals", "Help regulate movement of water and dissolved substances into the vascular tissues", "D"),
        ("Why can a plant wilt even when the soil contains some water?", "Water uptake may not keep pace with water loss, or the water may be difficult to access", "Plants never lose water", "Wilting means photosynthesis has permanently stopped in every cell", "Roots cannot absorb any minerals when soil is wet", "A"),
        ("What is the main difference between xylem vessel elements and sieve tube elements?", "Both transport only sugars", "Xylem conducts water and minerals, while phloem transports organic substances", "Xylem produces pollen and phloem absorbs sunlight", "Phloem transports only oxygen", "B"),
        ("Why can removing all leaves seriously affect a plant?", "It stops the roots from existing immediately", "It makes the plant produce unlimited glucose", "It greatly reduces photosynthetic surface area and can reduce food production", "It prevents all water absorption forever", "C"),
        ("How can mycorrhizal fungi benefit plant roots?", "They convert the plant into an animal", "They prevent all mineral uptake", "They stop every form of respiration", "They can improve access to phosphorus and water", "D"),
        ("What is the main consequence of a mutation that prevents chlorophyll synthesis?", "Photosynthetic light absorption would be severely impaired", "Root hairs become flowers", "The plant no longer needs carbon dioxide", "The plant produces unlimited ATP from darkness", "A"),
        ("Why is the light-dependent stage of photosynthesis important?", "It forms fruits directly without other processes", "It produces ATP and reducing power and releases oxygen through water splitting", "It occurs only in roots", "It consumes all chlorophyll permanently", "B"),
        ("What is the role of pollen tubes in flowering plants?", "Transport water from roots to leaves", "Carry sugars through phloem", "Deliver male gametes towards the ovule", "Produce root hairs", "C"),
        ("Why can wind pollination produce large amounts of pollen?", "Every pollen grain must become a fruit", "Wind carries pollen only a few millimetres", "Plants cannot reproduce without animals", "Many pollen grains may never reach a compatible stigma", "D"),
        ("What is double fertilization in flowering plants?", "Two seeds fuse into one root", "One sperm fertilizes the egg and another fuses with the central cell to form endosperm", "Two pollen grains always form one leaf", "The ovary divides into two plants", "B"),
        ("Why can salinity stress make water uptake difficult for roots?", "Salt always increases water potential outside roots", "Salt turns all water into oxygen", "Low external water potential can reduce water entry into root cells", "Salt eliminates every osmotic effect", "C"),
        ("What is the function of the endosperm in many flowering plant seeds?", "Provide nourishment to the developing embryo", "Transport blood", "Form the flower stigma", "Absorb sunlight for the adult plant", "A"),
        ("Why is transpiration often higher on a warm, dry, windy day?", "Wind always closes all stomata", "These conditions can increase evaporation and removal of moist air around leaves", "Roots stop absorbing all water", "The plant produces no water vapour", "B"),
        ("What is the main benefit of vascular tissues in land plants?", "They eliminate the need for nutrients", "They prevent all reproduction", "They support long-distance transport of water, minerals, and organic substances", "They make photosynthesis unnecessary", "C"),
        ("Why may a plant growing in deep shade develop larger, thinner leaves?", "To eliminate chlorophyll", "To stop all gas exchange", "To avoid absorbing any light", "To capture limited light more effectively, depending on the species", "D"),
    ],
}


def normalize(text):
    return " ".join(text.casefold().split())


def main():
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DATABASE_PATH}")

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        connection.execute("PRAGMA foreign_keys = ON")

        lesson = connection.execute(
            """
            SELECT id
            FROM lessons
            WHERE lower(trim(title)) = lower(trim(?))
            """,
            ("Introduction to Plants",),
        ).fetchone()

        if lesson is None:
            raise RuntimeError(
                "Introduction to Plants lesson was not found in the database."
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
                        f"Missing {difficulty} quiz for Introduction to Plants."
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
                        f"{difficulty} already has {current_count} questions; "
                        f"target is {TARGET_QUESTIONS}."
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
                        raise ValueError(f"Invalid answer key: {question}")

                    if not all(
                        option.strip() for option in (a, b, c, d)
                    ):
                        raise ValueError(f"Empty option: {question}")

                    connection.execute(
                        """
                        INSERT INTO questions (
                            quiz_id, question, option_a,
                            option_b, option_c, option_d,
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
                        f"{difficulty} has {current_count} questions, not 30. "
                        "Add more unique questions. The transaction will roll back."
                    )

                print(
                    f"{difficulty}: added {added}; "
                    f"final count = {current_count}"
                )

        print("\nIntroduction to Plants expansion completed!")
        print(f"Total new questions inserted: {total_inserted}")
        print("Easy: 30 questions")
        print("Medium: 30 questions")
        print("Hard: 30 questions")
        print("Other lessons and Social Science were not modified.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()