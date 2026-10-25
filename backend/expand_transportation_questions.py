import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

LESSON_TITLE = "Transportation in Plants and Animals"
TARGET_QUESTIONS = 30

QUESTION_BANK = {
    "Easy": [
        ("What is transportation in living organisms?", ["Movement of substances from one part of an organism to another", "Production of sunlight", "Formation of seeds only", "Breakdown of rocks"], "A"),
        ("Which tissue transports water and minerals in plants?", ["Phloem", "Xylem", "Epidermis", "Cortex only"], "B"),
        ("Which tissue transports sugars in plants?", ["Xylem", "Root cap", "Phloem", "Stomata"], "C"),
        ("Which organ pumps blood throughout the human body?", ["Liver", "Lungs", "Kidney", "Heart"], "D"),
        ("What is the liquid component of blood called?", ["Plasma", "Platelet", "Haemoglobin", "Lymph node"], "A"),
        ("Which blood cells carry oxygen?", ["White blood cells", "Red blood cells", "Platelets", "Nerve cells"], "B"),
        ("Which blood components help fight infections?", ["Red blood cells", "Platelets", "White blood cells", "Plasma proteins only"], "C"),
        ("Which blood components help in clotting?", ["Red blood cells", "Neurons", "Alveoli", "Platelets"], "D"),
        ("What are the blood vessels that carry blood away from the heart called?", ["Arteries", "Veins", "Capillaries", "Lymph vessels"], "A"),
        ("Which blood vessels generally carry blood toward the heart?", ["Arteries", "Veins", "Capillaries", "Aorta only"], "B"),
        ("Which tiny blood vessels allow exchange between blood and tissues?", ["Arteries", "Veins", "Capillaries", "Bronchi"], "C"),
        ("What is the main function of roots in water transport?", ["Produce blood", "Pump water using a heart", "Transport sugars only", "Absorb water and minerals from soil"], "D"),
        ("What is transpiration?", ["Loss of water vapour from aerial parts of plants, mainly through stomata", "Absorption of glucose by roots", "Movement of blood", "Production of pollen"], "A"),
        ("Which plant structures mainly regulate gas exchange and water loss?", ["Root hairs", "Stomata", "Flowers", "Seeds"], "B"),
        ("Which mineral is essential for making chlorophyll?", ["Sodium", "Iodine", "Magnesium", "Gold"], "C"),
        ("What is the main function of the human circulatory system?", ["Digest food in the mouth", "Produce sunlight", "Make bones longer", "Transport oxygen, nutrients and wastes"], "D"),
        ("Which side of the human heart receives oxygen-rich blood from the lungs?", ["Left side", "Right side", "Both sides receive only oxygen-poor blood", "Neither side"], "A"),
        ("Which blood vessel carries oxygen-rich blood from the lungs to the heart?", ["Pulmonary artery", "Pulmonary vein", "Vena cava", "Aorta"], "B"),
        ("Which vessel carries oxygen-poor blood from the heart to the lungs?", ["Aorta", "Pulmonary vein", "Pulmonary artery", "Coronary vein only"], "C"),
        ("What is pulse?", ["Movement of food through the gut", "Air entering the lungs", "Loss of water from leaves", "Rhythmic expansion of arteries caused by heartbeats"], "D"),
        ("What is the main function of root hairs?", ["Increase the surface area for absorption", "Produce red blood cells", "Pump blood", "Make seeds directly"], "A"),
        ("Which plant tissue is made mainly of living cells that transport sugars?", ["Xylem vessels only", "Phloem", "Cork", "Root cap"], "B"),
        ("Which organ removes many metabolic wastes from human blood?", ["Heart", "Stomach", "Kidneys", "Lungs only"], "C"),
        ("What is the main role of valves in the heart?", ["Produce oxygen", "Make blood cells", "Absorb nutrients", "Prevent backward flow of blood"], "D"),
        ("What is the largest artery in the human body?", ["Aorta", "Vena cava", "Pulmonary vein", "Carotid capillary"], "A"),
        ("Which process helps water move upward through many plants?", ["Digestion", "Transpiration pull", "Blood clotting", "Fermentation"], "B"),
        ("Which part of blood contains haemoglobin?", ["Plasma", "Platelets", "Red blood cells", "White blood cells"], "C"),
        ("Which circulation carries blood between the heart and lungs?", ["Systemic circulation", "Digestive circulation", "Portal circulation only", "Pulmonary circulation"], "D"),
        ("What is the function of valves in many veins?", ["Help prevent blood from flowing backward", "Produce blood plasma", "Absorb water from soil", "Release oxygen into leaves"], "A"),
        ("Why do organisms need transport systems?", ["To stop all chemical reactions", "To deliver useful substances and remove wastes", "To eliminate the need for cells", "To prevent growth"], "B"),
    ],

    "Medium": [
        ("Why is xylem well suited to transport water upward in plants?", ["It carries only sugars", "It is made entirely of soft leaf cells", "Its vessels form continuous pathways and are often reinforced with lignin", "It transports blood using a heart"], "C"),
        ("What is the main driving force for transpiration pull in tall plants?", ["Movement of glucose through phloem", "Pressure from flowers", "Heart contractions", "Evaporation of water from leaf surfaces creates tension in the xylem"], "D"),
        ("How does phloem transport differ from xylem transport?", ["Phloem moves sugars from source to sink, while xylem transports water and minerals mainly upward", "Both only transport water upward", "Xylem transports blood", "Phloem carries oxygen only"], "A"),
        ("Why does blood flow more slowly through capillaries than through large arteries in many tissues?", ["Capillaries have no blood", "The total cross-sectional area of capillaries is very large", "Capillaries are larger than the aorta individually", "Capillaries pump blood independently"], "B"),
        ("What is the main function of haemoglobin?", ["Digest carbohydrates", "Produce antibodies", "Bind and transport oxygen", "Clot blood"], "C"),
        ("Why do arteries have thick, elastic walls?", ["They carry no blood", "They absorb nutrients from food", "They prevent the heart from beating", "They withstand and smooth out high-pressure blood flow"], "D"),
        ("Which chamber pumps oxygenated blood into the aorta?", ["Left ventricle", "Right ventricle", "Right atrium", "Left atrium"], "A"),
        ("Which chamber receives oxygen-poor blood returning from the body?", ["Left ventricle", "Right atrium", "Left atrium", "Aorta"], "B"),
        ("What is the purpose of the septum in the human heart?", ["To produce platelets", "To open the heart valves", "To separate the left and right sides of the heart", "To transport urine"], "C"),
        ("Why do veins often contain valves, especially in the limbs?", ["To increase blood pressure to arterial levels", "To produce red blood cells", "To exchange gases directly with air", "To reduce backward flow as blood returns to the heart"], "D"),
        ("What is double circulation in humans?", ["Blood passes through the heart twice during one complete circuit of the body", "Blood passes through the heart only once in a complete circuit", "Blood bypasses the lungs", "Blood flows only through arteries"], "A"),
        ("What is the main role of plasma?", ["Carry oxygen using haemoglobin", "Transport dissolved substances such as nutrients, hormones and wastes", "Form the walls of arteries", "Produce electrical impulses"], "B"),
        ("Why are red blood cells shaped like biconcave discs?", ["To make them rigid bones", "To allow them to produce antibodies", "To provide a large surface area and flexibility for gas transport", "To digest food"], "C"),
        ("How do white blood cells help protect the body?", ["They carry most oxygen", "They transport sugars through plants", "They prevent every blood vessel from narrowing", "They defend against pathogens through immune responses"], "D"),
        ("What is the function of platelets?", ["Help form blood clots", "Carry most oxygen", "Transport water in plants", "Produce bile"], "A"),
        ("Why can high transpiration rates cause a plant to wilt?", ["They prevent water from evaporating", "Water loss can exceed the rate of water uptake by roots", "They make the roots absorb unlimited water", "They stop all mineral transport permanently"], "B"),
        ("Which environmental condition commonly increases transpiration if other factors are suitable?", ["High humidity", "Still, saturated air", "Warm, dry and windy conditions", "Complete darkness in every species"], "C"),
        ("Why does high humidity usually reduce transpiration?", ["It increases the water-vapour gradient", "It forces xylem to produce glucose", "It increases root pressure without limit", "It reduces the water-vapour gradient between the leaf and surrounding air"], "D"),
        ("What is translocation in plants?", ["Movement of organic substances through phloem", "Movement of blood through the heart", "Loss of water through stomata", "Absorption of sunlight by roots"], "A"),
        ("Which example is a source in phloem translocation?", ["A root receiving stored sugar", "A mature leaf producing sugars through photosynthesis", "A growing root tip consuming sugar", "A fruit storing imported sugar"], "B"),
        ("Which example is a sink in phloem translocation?", ["A mature leaf exporting sugars", "A photosynthesising leaf producing carbohydrates", "A developing fruit receiving sugars", "A leaf releasing water vapour"], "C"),
        ("Why is the left ventricle's wall thicker than the right ventricle's wall?", ["It pumps blood only to the lungs", "It contains no muscle", "It receives blood from the body", "It must generate greater pressure to pump blood around the body"], "D"),
        ("What happens when the heart's atria contract?", ["They help push blood into the ventricles", "They push blood directly into the aorta", "They stop the ventricles filling", "They pump blood into the lungs independently"], "A"),
        ("What is blood pressure?", ["The amount of sugar in blood", "The force exerted by blood against vessel walls", "The number of white blood cells", "The volume of air in the lungs"], "B"),
        ("Why is the capillary wall only one cell thick?", ["To prevent all exchange", "To carry blood at the highest pressure", "To allow efficient diffusion of substances between blood and tissues", "To store blood cells permanently"], "C"),
        ("Which pathway correctly describes blood flow from the body to the lungs?", ["Aorta → left ventricle → pulmonary vein", "Pulmonary vein → left atrium → vena cava", "Left ventricle → aorta → lungs", "Vena cava → right atrium → right ventricle → pulmonary artery"], "D"),
        ("How does root pressure differ from transpiration pull?", ["Root pressure can push water upward, while transpiration pull creates tension through evaporation at leaves", "Root pressure occurs only in animal hearts", "Transpiration pull transports blood", "Both processes require a plant heart"], "A"),
        ("Why can a ring of bark removed from a tree affect sugar transport?", ["It removes the xylem from the roots in every case", "It can interrupt phloem transport through the bark region", "It increases phloem flow without limit", "It prevents the leaves from receiving sunlight immediately"], "B"),
        ("What is the main purpose of systemic circulation?", ["Move blood only between the heart and lungs", "Transport water from plant roots", "Deliver blood between the heart and body tissues", "Produce digestive enzymes"], "C"),
        ("Why is a continuous supply of blood important for active tissues?", ["It eliminates the need for cellular respiration", "It prevents all waste formation", "It allows tissues to survive without nutrients", "It supplies oxygen and nutrients and removes metabolic wastes"], "D"),
    ],

    "Hard": [
        ("A plant is placed in a warm, dry and windy environment. Assuming water is available, what is likely to happen initially?", ["Transpiration rate may increase", "Transpiration must stop completely", "Phloem becomes xylem", "Roots stop absorbing all water immediately"], "A"),
        ("Why can excessive transpiration cause stomata to close?", ["To increase water loss without limit", "To reduce further water loss when the plant experiences water stress", "To make roots produce oxygen", "To convert xylem into phloem"], "B"),
        ("A tree's phloem is damaged but much of its xylem remains intact. Which function is most directly impaired?", ["Water transport from roots", "Mechanical support from lignified vessels", "Movement of sugars from sources to sinks", "Absorption of water by root hairs"], "C"),
        ("Why can xylem water rise to the top of a tall tree without a central pumping organ?", ["Leaves contract like a heart", "Phloem generates blood pressure", "Water is pushed upward by animal-like muscles", "Cohesion between water molecules and transpiration-generated tension help pull water upward"], "D"),
        ("A person has a damaged heart valve that allows backward flow. What is a likely consequence?", ["Reduced efficiency of forward blood flow", "Increased separation between the heart chambers", "Production of extra red blood cells by the valve", "Direct absorption of nutrients by the valve"], "A"),
        ("Why is double circulation beneficial in humans?", ["It mixes oxygen-rich and oxygen-poor blood in the normal healthy heart", "It supports efficient separation of pulmonary and systemic blood flow", "It eliminates the need for lungs", "It means blood never passes through capillaries"], "B"),
        ("If the left ventricle cannot contract effectively, which process is most directly affected?", ["Blood returning from the body to the right atrium", "Oxygen diffusion into alveoli only", "Delivery of oxygenated blood to systemic tissues", "Water absorption by plant roots"], "C"),
        ("Why does blood in the pulmonary artery normally contain less oxygen than blood in the pulmonary vein?", ["Arteries always carry oxygen-rich blood", "The pulmonary vein carries blood away from the heart", "The pulmonary artery transports blood from the lungs to the left atrium", "The pulmonary artery carries blood toward the lungs before gas exchange"], "D"),
        ("A patient has a very low platelet count. Which problem is most likely?", ["Difficulty forming normal blood clots", "Increased oxygen binding by haemoglobin", "Excessive sugar transport in phloem", "Improved closure of all heart valves"], "A"),
        ("Why can severe anaemia reduce exercise tolerance?", ["It increases oxygen-carrying capacity", "Reduced haemoglobin can limit oxygen delivery to working muscles", "It makes capillaries transport sugars from leaves", "It stops carbon dioxide from existing"], "B"),
        ("A plant's roots absorb water normally, but the xylem vessels are blocked. What is the likely effect on leaves?", ["Sugar transport increases without limit", "Blood circulation stops", "Water delivery to leaves decreases", "The leaves immediately become roots"], "C"),
        ("How does transpiration help mineral transport in many plants?", ["Minerals are produced from sunlight", "Minerals move only through phloem", "Water evaporates without affecting xylem flow", "Water movement through xylem helps carry dissolved mineral ions from roots toward shoots"], "D"),
        ("A researcher measures transpiration under different wind speeds while keeping other conditions similar. Why should temperature and humidity be controlled?", ["They also affect transpiration and could confound the results", "They never affect water loss", "They determine the plant's genetic code", "They remove the need for repeated measurements"], "A"),
        ("Why can capillaries exchange materials efficiently despite having narrow individual diameters?", ["Their walls are thicker than artery walls", "Their extensive network provides a large total surface area and short diffusion distances", "They contain valves that pump blood", "They prevent all contact with tissues"], "B"),
        ("A blockage occurs in the vena cava. Which immediate transport function is most directly affected?", ["Blood flow from the left ventricle to the aorta", "Transport of sugars through plant phloem", "Return of blood from the body to the right atrium", "Movement of water through xylem"], "C"),
        ("Why can a severe reduction in blood flow to the kidneys impair waste removal?", ["Kidneys create all oxygen in the body", "Blood flow is unrelated to filtration", "Kidneys transport sugars to leaves", "Reduced renal perfusion can reduce filtration and affect fluid balance"], "D"),
        ("A plant has a high rate of photosynthesis but its phloem transport is disrupted. What may happen?", ["Sugars may accumulate near source tissues and growing sinks may receive less", "Water can no longer enter roots under any condition", "All xylem vessels immediately disappear", "Photosynthesis must increase indefinitely"], "A"),
        ("Why does water move from soil into root hair cells by osmosis in a typical plant root?", ["The root hairs pump soil water using a heart", "A water-potential gradient favours water movement across the partially permeable membrane", "Water is converted into glucose before entry", "The cell wall actively transports water using ATP"], "B"),
        ("Which factor most directly supports the movement of oxygen from systemic capillaries into active tissues?", ["Equal oxygen partial pressures in blood and tissues", "A complete absence of circulation", "A higher oxygen partial pressure in blood than in the tissues", "A thicker capillary wall"], "C"),
        ("Why is the pressure generated by the left ventricle greater than that generated by the right ventricle?", ["The right ventricle pumps blood throughout the body", "The left ventricle pumps blood only a short distance to the lungs", "Both ventricles pump into the same artery", "The left ventricle must drive blood through the higher-resistance systemic circuit"], "D"),
        ("If pulmonary circulation is impaired, which gas-exchange consequence is most likely?", ["Less effective oxygen uptake and carbon dioxide removal from blood", "Improved delivery of oxygen to all tissues", "Increased water absorption by roots", "More efficient sugar transport in phloem"], "A"),
        ("Why does phloem translocation sometimes occur in opposite directions in different sieve tubes of the same plant?", ["All sugars must move upward only", "Different source-sink relationships can drive movement in different directions in separate phloem pathways", "Xylem carries sugar downward and upward instead", "Phloem transports only water"], "B"),
        ("A plant wilts at midday but recovers overnight when conditions cool. What is a plausible explanation?", ["Its xylem permanently changes into phloem each night", "It stops absorbing minerals forever", "Daytime water loss temporarily exceeds uptake, while cooler night conditions allow water balance to recover", "Its roots begin pumping blood at night"], "C"),
        ("Why can narrowing of arteries increase the workload on the heart?", ["It makes blood viscosity zero", "It guarantees lower resistance", "It prevents any pressure from developing", "It can increase resistance to blood flow and require greater pressure to maintain circulation"], "D"),
        ("Which change would most directly increase water absorption capacity in a healthy root system?", ["An increase in root hair surface area", "A complete loss of root hairs", "A blockage of all water channels", "A decrease in root contact with moist soil"], "A"),
        ("A person has a defect in the septum separating the ventricles. Why can this be harmful?", ["It always improves oxygen delivery", "It may allow mixing between oxygen-rich and oxygen-poor blood and alter circulation", "It makes the heart unnecessary", "It stops the kidneys from absorbing water directly"], "B"),
        ("Why is the lymphatic system important alongside blood circulation?", ["It pumps oxygen directly into alveoli", "It replaces every artery", "It returns excess tissue fluid to the bloodstream and supports immune functions", "It produces glucose in the lungs"], "C"),
        ("A plant's stomata close during a drought. What is the trade-off?", ["Water loss increases while carbon dioxide entry increases", "Photosynthesis becomes independent of carbon dioxide", "Xylem stops transporting water in every case", "Water loss decreases, but carbon dioxide uptake and photosynthesis may also decline"], "D"),
        ("Why can blood pressure fall after severe blood loss?", ["Circulating blood volume decreases", "The number of leaves decreases", "Xylem vessels become wider", "The stomach absorbs more oxygen"], "A"),
        ("Which statement best links plant transport and animal circulation?", ["Both systems use an identical heart and blood", "Both distribute essential materials through specialised pathways, but their structures and mechanisms differ", "Plants have blood vessels identical to arteries", "Animals use xylem to carry oxygen"], "B"),
    ],
}


def normalize(text):
    return " ".join(text.casefold().split())


def main():
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DATABASE_PATH}")

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
                raise RuntimeError(f"Lesson '{LESSON_TITLE}' was not found.")

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
                existing = {normalize(row[0]) for row in cursor.fetchall()}

                available = [
                    (question, options, answer)
                    for question, options, answer in questions
                    if normalize(question) not in existing
                ]

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
                        f"{difficulty}: need {needed} new questions, but only "
                        f"{len(available)} unique questions are available. "
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
                    f"{difficulty}: added {needed}; final count = {final_count}"
                )

        print("\nTransportation in Plants and Animals expansion completed!")
        print(f"Total new questions inserted: {inserted_total}")
        print("Easy: 30 questions")
        print("Medium: 30 questions")
        print("Hard: 30 questions")
        print("Other lessons and Social Science were not modified.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()