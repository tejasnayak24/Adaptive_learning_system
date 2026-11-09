import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

LESSON_TITLE = "Respiration in Organisms"
TARGET_QUESTIONS = 30

QUESTION_BANK = {
    "Easy": [
        ("What is respiration?", ["The process of releasing energy from food", "The process of absorbing sunlight only", "The movement of water through soil", "The formation of seeds"], "A"),
        ("Which gas is commonly used in aerobic respiration?", ["Nitrogen", "Oxygen", "Hydrogen", "Helium"], "B"),
        ("Which gas is produced during aerobic respiration?", ["Nitrogen", "Helium", "Carbon dioxide", "Neon"], "C"),
        ("Where does glycolysis take place in a cell?", ["Nucleus", "Chloroplast", "Golgi apparatus", "Cytoplasm"], "D"),
        ("Which organelle is the main site of aerobic respiration in eukaryotic cells?", ["Mitochondrion", "Ribosome", "Vacuole", "Cell wall"], "A"),
        ("What is the main purpose of cellular respiration?", ["To produce sunlight", "To release usable energy from food", "To make soil", "To absorb minerals only"], "B"),
        ("Which process releases energy from glucose without directly requiring oxygen?", ["Photosynthesis", "Transpiration", "Anaerobic respiration", "Pollination"], "C"),
        ("What is breathing?", ["The breakdown of glucose inside cells", "The formation of proteins", "The transport of food in plants", "The movement of air into and out of the respiratory system"], "D"),
        ("Which organ is mainly responsible for gas exchange in humans?", ["Lungs", "Stomach", "Kidneys", "Liver"], "A"),
        ("Which structures in the lungs provide a large surface area for gas exchange?", ["Bronchi", "Alveoli", "Ribs", "Diaphragm"], "B"),
        ("Which muscle helps humans breathe by changing the volume of the chest cavity?", ["Biceps", "Triceps", "Diaphragm", "Calf muscle"], "C"),
        ("Which gas do humans take in from the air for aerobic respiration?", ["Carbon dioxide", "Nitrogen only", "Hydrogen", "Oxygen"], "D"),
        ("Which organism can respire without oxygen under suitable conditions?", ["Yeast", "Adult human brain cells under normal conditions", "All fish in every condition", "Only green plants"], "A"),
        ("What is the main energy-carrying molecule used by cells?", ["DNA", "ATP", "Cellulose", "Chlorophyll"], "B"),
        ("Which process occurs in yeast when it produces alcohol without oxygen?", ["Photosynthesis", "Transpiration", "Alcoholic fermentation", "Pollination"], "C"),
        ("What happens to breathing rate during exercise in many people?", ["It always becomes zero", "It never changes", "It decreases in every case", "It usually increases"], "D"),
        ("Which blood cells carry most oxygen in human blood?", ["Red blood cells", "Platelets", "White blood cells", "Nerve cells"], "A"),
        ("Which substance in red blood cells binds oxygen?", ["Insulin", "Haemoglobin", "Pepsin", "Bile"], "B"),
        ("What is the common product of aerobic respiration in cells?", ["Glucose and oxygen", "Starch and nitrogen", "Carbon dioxide, water and usable energy", "Chlorophyll and water"], "C"),
        ("Which organism commonly exchanges gases through its skin as well as its lungs?", ["Butterfly", "Housefly", "Earthworm only through lungs", "Frog"], "D"),
        ("What is the main function of the nose during breathing?", ["Filter, warm and moisten incoming air", "Digest food", "Pump blood", "Produce red blood cells"], "A"),
        ("Which tube carries air from the throat toward the bronchi?", ["Oesophagus", "Trachea", "Ureter", "Artery"], "B"),
        ("What is inhalation?", ["Air leaving the lungs", "Food entering the stomach", "Air entering the lungs", "Blood leaving the heart"], "C"),
        ("What is exhalation?", ["Air entering the lungs", "Oxygen entering red blood cells only", "The movement of food through the gut", "Air leaving the lungs"], "D"),
        ("Which process provides energy for muscle contraction?", ["Cellular respiration", "Pollination", "Seed dispersal", "Filtration of soil"], "A"),
        ("Which organism commonly uses gills to obtain dissolved oxygen from water?", ["Eagle", "Fish", "Earthworm", "Butterfly"], "B"),
        ("What is anaerobic respiration?", ["Respiration that always occurs in the lungs", "Respiration that produces no chemical energy", "Energy-releasing breakdown of food without oxygen", "The movement of oxygen through the nose"], "C"),
        ("Which activity commonly causes a temporary increase in breathing rate?", ["Sleeping quietly", "Sitting still", "Reading silently", "Running"], "D"),
        ("Which gas is carried from body tissues to the lungs for removal?", ["Carbon dioxide", "Oxygen only", "Helium", "Hydrogen"], "A"),
        ("Why do living organisms need energy from respiration?", ["To create sunlight", "For growth, movement, repair and other life processes", "To avoid all water use", "To stop every chemical reaction"], "B"),
    ],

    "Medium": [
        ("Which equation best summarises aerobic respiration?", ["Carbon dioxide + water → glucose + oxygen", "Oxygen + water → nitrogen + energy", "Glucose + oxygen → carbon dioxide + water + energy", "Glucose → chlorophyll + sunlight"], "C"),
        ("Why do alveoli have very thin walls?", ["To prevent oxygen from entering blood", "To store food", "To pump blood directly", "To allow gases to diffuse rapidly"], "D"),
        ("What happens to the diaphragm during normal inhalation?", ["It contracts and moves downward", "It relaxes and moves upward", "It stops moving permanently", "It closes the trachea"], "A"),
        ("Why does breathing rate increase during vigorous exercise?", ["Muscles stop using ATP", "Muscles need more oxygen and produce more carbon dioxide", "The lungs stop exchanging gases", "The body no longer requires energy"], "B"),
        ("Which statement distinguishes breathing from cellular respiration?", ["They are exactly the same process", "Cellular respiration occurs only outside cells", "Breathing moves air, while cellular respiration releases energy through chemical reactions", "Breathing produces glucose in mitochondria"], "C"),
        ("What is the main role of oxygen in aerobic respiration?", ["It acts as the main food molecule", "It converts ATP into sunlight", "It directly builds muscles", "It serves as the final electron acceptor in the electron transport chain"], "D"),
        ("Where does the Krebs cycle occur in a typical eukaryotic cell?", ["Mitochondrial matrix", "Nucleus", "Golgi apparatus", "Cell wall"], "A"),
        ("What is the net ATP yield of glycolysis per glucose molecule?", ["Four ATP", "Two ATP", "Thirty ATP", "Zero ATP"], "B"),
        ("Why can anaerobic respiration produce less ATP than aerobic respiration?", ["It always uses more oxygen", "It breaks down all glucose completely", "Glucose is not completely oxidised through fermentation pathways", "It occurs only in mitochondria"], "C"),
        ("Which product is commonly formed when human muscle cells use anaerobic metabolism during intense exercise?", ["Ethanol", "Oxygen", "Starch", "Lactate"], "D"),
        ("Which products are commonly formed during alcoholic fermentation in yeast?", ["Ethanol and carbon dioxide", "Oxygen and water only", "Lactate and oxygen", "Glucose and nitrogen"], "A"),
        ("Why is the inner mitochondrial membrane folded into cristae?", ["To stop ATP formation", "To provide more surface area for electron transport and ATP production", "To store genetic information only", "To make the cell wall thicker"], "B"),
        ("What is diffusion in gas exchange?", ["Movement requiring a pump in every case", "Movement of food through the digestive tract", "Net movement of particles from higher to lower concentration", "The production of ATP from sunlight"], "C"),
        ("Why does carbon dioxide move from blood into the alveoli?", ["Alveoli actively produce all blood carbon dioxide", "Blood contains no carbon dioxide", "Oxygen pushes carbon dioxide mechanically", "A partial-pressure gradient favours diffusion into the alveoli"], "D"),
        ("What is the main role of haemoglobin in respiration?", ["Transport oxygen in the blood", "Digest glucose in the stomach", "Produce ATP in the alveoli", "Remove all nitrogen from air"], "A"),
        ("Why is the surface of alveoli moist?", ["To prevent gases from dissolving", "Gases dissolve in the moisture before diffusing across the membrane", "To block oxygen movement", "To make the alveoli rigid"], "B"),
        ("What happens to the rib cage during normal inhalation?", ["It moves downward and inward", "It remains fixed in every case", "It moves upward and outward", "It closes the bronchi"], "C"),
        ("Why is cellular respiration essential even when an organism has stored food?", ["Stored food never contains chemical energy", "Respiration creates energy from nothing", "Food can be used only after being exhaled", "Respiration transfers chemical energy into usable forms such as ATP"], "D"),
        ("Which factor can reduce gas exchange efficiency in damaged lungs?", ["Reduced alveolar surface area", "A healthy thin alveolar membrane", "An adequate oxygen gradient", "Normal blood circulation"], "A"),
        ("Why can breathing into a paper bag be unsafe for someone with unexplained breathlessness?", ["It always increases oxygen concentration", "It can reduce the amount of oxygen available and worsen some conditions", "It cures all respiratory illnesses", "It stops carbon dioxide production in cells"], "B"),
        ("What is the role of the intercostal muscles during breathing?", ["Digest food", "Transport glucose in blood", "Help move the rib cage to change chest volume", "Produce haemoglobin"], "C"),
        ("Which process supplies oxygen to the blood in the lungs?", ["Filtration", "Osmosis of glucose", "Active transport of all air", "Diffusion across the alveolar-capillary membrane"], "D"),
        ("Why do cells require ATP continuously?", ["Many cellular activities require an immediate, usable energy supply", "ATP is a structural component of every cell wall", "ATP prevents all diffusion", "ATP replaces DNA"], "A"),
        ("What is oxygen debt commonly associated with after strenuous exercise?", ["A permanent stop in respiration", "Recovery processes that help restore the body's normal state after intense activity", "The absence of carbon dioxide in blood", "The conversion of lungs into muscles"], "B"),
        ("Which respiratory surface is generally most effective for gas exchange?", ["A thick, dry surface with little blood supply", "A small surface with no ventilation", "A large, thin, moist surface with good transport of gases", "A surface completely sealed from the environment"], "C"),
        ("Why do insects have a tracheal system?", ["To pump blood through lungs", "To digest food externally", "To produce oxygen by photosynthesis", "To deliver gases through branching tubes to body tissues"], "D"),
        ("What happens to glucose during glycolysis?", ["It is split into smaller molecules, producing a small amount of ATP", "It is converted directly into oxygen", "It becomes DNA without chemical reactions", "It is stored only in the nucleus"], "A"),
        ("Why is the oxygen supply important for endurance exercise?", ["Oxygen stops muscles from needing ATP", "It supports aerobic ATP production in working tissues", "It directly creates glucose from carbon dioxide in muscles", "It eliminates the need for blood circulation"], "B"),
        ("Which structure prevents food from entering the trachea during swallowing?", ["Alveolus", "Bronchiole", "Epiglottis", "Diaphragm"], "C"),
        ("Why can smoking damage gas exchange?", ["It increases alveolar surface area permanently", "It eliminates all mucus", "It guarantees improved oxygen transport", "It can damage airways and alveoli and impair oxygen delivery"], "D"),
    ],

    "Hard": [
        ("A person has emphysema, which destroys walls between alveoli. Which effect is most likely?", ["Reduced surface area for gas exchange", "Increased alveolar surface area", "Complete absence of carbon dioxide in blood", "Increased oxygen diffusion in every condition"], "A"),
        ("Why does oxygen diffuse from alveolar air into pulmonary blood?", ["Blood always contains more oxygen than alveoli", "The oxygen partial pressure is generally higher in alveoli than in incoming pulmonary blood", "Oxygen is actively pumped through the alveolar wall using ATP", "Haemoglobin repels oxygen"], "B"),
        ("A poison inhibits the electron transport chain in mitochondria. What is the likely immediate consequence?", ["Glycolysis stops in every cell instantly", "Cells produce unlimited ATP", "Oxidative ATP production falls sharply", "Photosynthesis begins in human cells"], "C"),
        ("Why can carbon monoxide poisoning be life-threatening?", ["It increases oxygen binding to haemoglobin", "It directly produces ATP", "It makes alveoli larger", "It binds strongly to haemoglobin and reduces oxygen transport"], "D"),
        ("During intense exercise, oxygen delivery cannot fully meet muscle demand. Which pathway can temporarily supplement ATP production?", ["Anaerobic glycolysis", "Photosynthesis", "Nitrogen fixation", "Protein synthesis only"], "A"),
        ("A student measures oxygen consumption by germinating seeds and non-germinating seeds under identical conditions. Why might germinating seeds consume more oxygen?", ["They do not carry out metabolism", "They require more energy for active growth and cellular processes", "They perform photosynthesis in darkness at a high rate", "They contain no stored food"], "B"),
        ("Why does the rate of aerobic respiration generally rise when cellular energy demand increases, if oxygen and substrates are available?", ["Cells stop using ATP", "Mitochondria become unnecessary", "More fuel oxidation and ATP production are needed to meet demand", "Carbon dioxide becomes the only source of energy"], "C"),
        ("A person breathes normally, but their haemoglobin concentration is very low. What problem may occur?", ["The lungs must stop expanding", "Carbon dioxide cannot diffuse at all", "The stomach stops digestion", "Blood oxygen-carrying capacity is reduced"], "D"),
        ("Which change would most directly impair diffusion across the alveolar-capillary membrane?", ["An increase in membrane thickness", "A larger gas exchange surface", "A stronger oxygen partial-pressure gradient", "A thin, moist membrane"], "A"),
        ("Why can a high concentration of carbon dioxide in blood stimulate increased ventilation?", ["Carbon dioxide has no effect on breathing regulation", "Chemoreceptors respond to changes associated with carbon dioxide and pH", "It stops the respiratory centre permanently", "It converts the diaphragm into bone"], "B"),
        ("What would happen if the diaphragm were paralysed and no alternative ventilation mechanism compensated?", ["The lungs would produce glucose", "The alveoli would make red blood cells", "Normal ventilation would be seriously impaired", "Cellular respiration would become photosynthesis"], "C"),
        ("Why does complete aerobic oxidation of glucose yield more ATP than fermentation?", ["Fermentation uses more electron transport chains", "Fermentation completely oxidises glucose to carbon dioxide and water", "Aerobic respiration does not use glucose", "Aerobic respiration extracts more energy through additional oxidation pathways and oxidative phosphorylation"], "D"),
        ("A cell has adequate glucose but its mitochondria cannot use oxygen. Which process can still provide some ATP?", ["Glycolysis", "The Krebs cycle at its normal aerobic rate", "The mitochondrial electron transport chain at its normal rate", "Oxidative phosphorylation at its normal rate"], "A"),
        ("Why does lactic acid-related metabolism not mean that muscles permanently stop functioning during intense exercise?", ["Muscles no longer require ATP", "Anaerobic glycolysis can provide limited ATP while aerobic metabolism and recovery continue", "Oxygen becomes toxic to all muscle cells", "Lactate contains no chemical energy"], "B"),
        ("Which factor combination best supports efficient alveolar gas exchange?", ["Thick dry walls, low surface area and no blood supply", "No ventilation and equal gas partial pressures", "Thin moist walls, large surface area and maintained partial-pressure gradients", "A sealed alveolus with no blood circulation"], "C"),
        ("Why does ventilation need to work together with blood circulation for efficient gas exchange?", ["Blood circulation makes oxygen unnecessary", "Ventilation transports glucose directly into mitochondria", "Both processes occur only in plants", "Ventilation renews alveolar air while circulation carries gases between lungs and tissues"], "D"),
        ("A drug reduces the activity of enzymes involved in glycolysis. What is a likely effect?", ["Reduced ATP production from glycolysis", "Increased glucose breakdown by those same inhibited enzymes", "Immediate production of chlorophyll", "Improved oxygen diffusion through the alveoli"], "A"),
        ("Why is ATP described as an energy currency rather than a long-term energy store?", ["ATP contains no usable energy", "Cells rapidly produce and use ATP to couple energy-releasing reactions to energy-requiring processes", "ATP is stored only outside cells", "ATP is a type of oxygen-carrying blood cell"], "B"),
        ("A person travels rapidly to a high altitude. Why may they initially breathe faster?", ["Air at altitude contains no nitrogen", "The body no longer needs oxygen", "Lower oxygen partial pressure can stimulate ventilation through physiological responses", "The diaphragm permanently stops contracting"], "C"),
        ("Which statement about oxygen transport is correct?", ["All oxygen is carried dissolved in plasma", "Haemoglobin transports carbon dioxide only and never oxygen", "Oxygen is carried only by platelets", "Most oxygen in blood is carried bound to haemoglobin"], "D"),
        ("Why does carbon dioxide need to be removed from the body?", ["Its accumulation can disturb blood pH and normal physiological function", "It is the main source of oxygen", "It replaces ATP in every cell", "It is required in unlimited concentrations for breathing"], "A"),
        ("A researcher blocks the movement of protons across the inner mitochondrial membrane through ATP synthase. What is most directly impaired?", ["DNA replication in every part of the cell", "ATP synthesis by oxidative phosphorylation", "Diffusion of oxygen into the lungs", "Digestion in the stomach"], "B"),
        ("Why do many actively growing plant tissues consume oxygen even when the plant is also photosynthesising?", ["Plants do not carry out respiration", "Photosynthesis removes the need for ATP", "Cells use aerobic respiration to generate ATP for growth and maintenance", "Oxygen can only be used by animals"], "C"),
        ("A patient has a pulmonary embolism blocking blood flow to part of the lung. How can this impair gas exchange?", ["It increases blood flow to the blocked region", "It makes the alveoli produce additional haemoglobin", "It guarantees normal oxygen delivery", "It reduces perfusion, disrupting effective matching of airflow and blood flow"], "D"),
        ("Why can severe airway narrowing reduce blood oxygen levels?", ["It reduces airflow to alveoli and can impair oxygen uptake", "It increases ventilation to every alveolus without limit", "It directly raises haemoglobin concentration", "It eliminates the body's demand for oxygen"], "A"),
        ("Which statement best explains why cellular respiration is essential to nerve cells?", ["Nerve cells obtain all energy directly from sunlight", "ATP supports ion gradients and other energy-dependent processes needed for nerve function", "Nerve cells never use glucose", "Nerve cells do not require membrane transport"], "B"),
        ("If the oxygen supply to a tissue falls severely, what may happen to ATP production?", ["Oxidative phosphorylation always speeds up", "ATP is no longer needed", "Aerobic ATP production falls and cells may rely more on anaerobic glycolysis", "The tissue begins producing oxygen by photosynthesis"], "C"),
        ("Why does carbon dioxide diffuse from active body tissues into the blood?", ["Blood always contains less carbon dioxide than the tissues under every circumstance", "Carbon dioxide is actively pumped by red blood cells in all cases", "It is converted to oxygen in the tissues", "The carbon dioxide partial pressure is generally higher in tissues than in incoming blood"], "D"),
        ("A person with severe anaemia has normal lung function but feels breathless during activity. Which explanation is most likely?", ["Reduced haemoglobin limits oxygen delivery despite normal lung ventilation", "Anaemia increases oxygen-carrying capacity", "The alveoli stop existing", "The person no longer produces carbon dioxide"], "A"),
        ("Why is the respiratory system's large exchange surface valuable?", ["It prevents diffusion", "It permits a greater rate of oxygen and carbon dioxide exchange", "It eliminates the need for circulation", "It makes breathing independent of pressure differences"], "B"),
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

        print("\nRespiration in Organisms expansion completed!")
        print(f"Total new questions inserted: {inserted_total}")
        print("Easy: 30 questions")
        print("Medium: 30 questions")
        print("Hard: 30 questions")
        print("Other lessons and Social Science were not modified.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()