import sqlite3
from pathlib import Path

DATABASE_PATH = (
    Path(__file__).resolve().parent.parent
    / "adaptive_learning.db"
)

TARGET_QUESTIONS = 30

QUESTION_BANK = {
    "Easy": [
        ("Which organ pumps blood throughout the human body?", "Lungs", "Heart", "Kidneys", "Stomach", "B"),
        ("Which organs help us breathe?", "Lungs", "Liver", "Pancreas", "Intestines", "A"),
        ("Which organ controls most body activities?", "Heart", "Stomach", "Brain", "Kidney", "C"),
        ("Which organs filter waste from the blood to produce urine?", "Lungs", "Heart", "Stomach", "Kidneys", "D"),
        ("Where does most digestion and nutrient absorption occur?", "Small intestine", "Oesophagus", "Trachea", "Urinary bladder", "A"),
        ("Which organ produces bile?", "Pancreas", "Liver", "Heart", "Lungs", "B"),
        ("Which body system provides support and protects many internal organs?", "Digestive system", "Respiratory system", "Skeletal system", "Endocrine system", "C"),
        ("Which system carries oxygen and nutrients around the body?", "Nervous system", "Digestive system", "Skeletal system", "Circulatory system", "D"),
        ("Which organ connects the mouth to the stomach?", "Oesophagus", "Trachea", "Ureter", "Aorta", "A"),
        ("Which organ begins the digestion of starch using salivary amylase?", "Liver", "Mouth", "Large intestine", "Kidney", "B"),
        ("Which muscle helps the lungs expand during breathing?", "Biceps", "Triceps", "Diaphragm", "Calf muscle", "C"),
        ("Which blood cells help defend the body against infections?", "Red blood cells", "Platelets", "Plasma cells only", "White blood cells", "D"),
        ("Which blood components help form clots?", "Platelets", "Red blood cells", "Neurons", "Alveoli", "A"),
        ("Which organs remove carbon dioxide from the body?", "Kidneys", "Lungs", "Stomach", "Pancreas", "B"),
        ("Which system coordinates rapid responses to stimuli?", "Digestive system", "Skeletal system", "Nervous system", "Urinary system", "C"),
        ("What connects muscles to bones?", "Ligaments", "Cartilage", "Nerves", "Tendons", "D"),
        ("What connects one bone to another at a joint?", "Ligament", "Tendon", "Neuron", "Alveolus", "A"),
        ("Which organ stores urine before it is released?", "Kidney", "Urinary bladder", "Liver", "Pancreas", "B"),
        ("Which organ produces insulin?", "Liver", "Stomach", "Pancreas", "Lungs", "C"),
        ("Which system breaks food into simpler substances?", "Respiratory system", "Circulatory system", "Nervous system", "Digestive system", "D"),
        ("What is the main function of red blood cells?", "Transport oxygen", "Digest proteins", "Produce bile", "Filter urine", "A"),
        ("Which structures in the lungs allow gas exchange?", "Bronchi only", "Alveoli", "Vocal cords", "Nasal hairs", "B"),
        ("Which organ is primarily responsible for pumping blood?", "Brain", "Liver", "Heart", "Spleen", "C"),
        ("Which body system includes the skin, hair, and nails?", "Digestive system", "Nervous system", "Muscular system", "Integumentary system", "D"),
        ("What is the main function of the large intestine?", "Absorb water and form faeces", "Pump blood", "Exchange oxygen", "Produce insulin", "A"),
        ("Which system enables body movement through muscles and bones?", "Endocrine system", "Musculoskeletal system", "Urinary system", "Respiratory system", "B"),
        ("Which organ detects light and enables vision?", "Ear", "Nose", "Eye", "Tongue", "C"),
        ("Which organ is mainly responsible for hearing?", "Skin", "Heart", "Liver", "Ear", "D"),
        ("Which system produces hormones that regulate body functions?", "Endocrine system", "Skeletal system", "Digestive system", "Respiratory system", "A"),
        ("Which tube carries air from the throat towards the lungs?", "Oesophagus", "Trachea", "Ureter", "Urethra", "B"),
    ],

    "Medium": [
        ("Why does the small intestine have numerous villi?", "To pump blood", "To produce urine", "To increase the surface area for absorption", "To store oxygen", "C"),
        ("What is the main role of haemoglobin?", "Digest fats", "Produce hormones", "Filter blood", "Bind and transport oxygen", "D"),
        ("What happens to the diaphragm during normal inhalation?", "It contracts and moves downward", "It relaxes and moves upward", "It stops moving permanently", "It closes the oesophagus", "A"),
        ("What is the main function of the nephron?", "Produce digestive enzymes", "Filter blood and help form urine", "Pump blood to the lungs", "Transmit sound", "B"),
        ("Which blood vessels generally carry blood away from the heart?", "Veins", "Capillaries only", "Arteries", "Lymph nodes", "C"),
        ("Why are capillaries suitable for exchange of substances?", "They have very thick walls", "They contain bones", "They prevent all diffusion", "Their thin walls allow exchange", "D"),
        ("Which chamber pumps oxygenated blood into the aorta?", "Left ventricle", "Right atrium", "Right ventricle", "Left atrium", "A"),
        ("What is the function of the valves in the heart?", "Produce red blood cells", "Prevent backward flow of blood", "Exchange gases in the lungs", "Digest proteins", "B"),
        ("What happens to most proteins during digestion?", "They become DNA", "They become oxygen", "They are broken down into amino acids", "They are converted directly into bones", "C"),
        ("Which enzyme begins protein digestion in the stomach?", "Amylase", "Lipase", "Lactase", "Pepsin", "D"),
        ("What is the main function of insulin?", "Help regulate blood glucose levels", "Carry oxygen", "Digest cellulose in humans", "Produce urine", "A"),
        ("Which part of the brain helps coordinate balance and movement?", "Medulla only", "Cerebellum", "Spinal disc", "Retina", "B"),
        ("What is the role of the spinal cord?", "Produce bile", "Absorb nutrients", "Transmit nerve signals and coordinate reflexes", "Filter urine", "C"),
        ("Which system returns excess tissue fluid to the bloodstream and supports immunity?", "Digestive system", "Respiratory system", "Skeletal system", "Lymphatic system", "D"),
        ("What is the function of the epiglottis during swallowing?", "Helps prevent food entering the airway", "Pumps blood", "Produces insulin", "Filters waste from blood", "A"),
        ("What is the main role of bile in digestion?", "Break down starch into glucose", "Emulsify fats into smaller droplets", "Digest proteins into amino acids", "Absorb oxygen", "B"),
        ("Where does most gas exchange occur in the respiratory system?", "Trachea", "Nasal cavity", "Alveoli", "Larynx", "C"),
        ("What is the main role of the large intestine?", "Produce oxygen", "Pump blood", "Break bones down", "Absorb water and help form faeces", "D"),
        ("Why does the body sweat when it becomes too hot?", "To help cool the body through evaporation", "To increase body temperature", "To stop blood circulation", "To prevent breathing", "A"),
        ("What is a reflex action?", "A slow response requiring conscious planning every time", "A rapid, automatic response to a stimulus", "A type of digestion", "A process that produces hormones only", "B"),
        ("What is the main function of synovial fluid in movable joints?", "Transport oxygen to the brain", "Produce digestive enzymes", "Reduce friction between joint surfaces", "Form red blood cells", "C"),
        ("What is the primary function of the liver in metabolism?", "Pump blood", "Exchange gases", "Transmit electrical impulses", "Process nutrients and detoxify many substances", "D"),
        ("Which hormone helps lower blood glucose levels?", "Insulin", "Adrenaline", "Melatonin", "Thyroxine", "A"),
        ("What is the function of the ureters?", "Carry urine outside the body", "Transport urine from kidneys to bladder", "Filter air entering the lungs", "Carry food to the stomach", "B"),
        ("Which structure carries oxygenated blood from the lungs to the heart?", "Pulmonary artery", "Vena cava", "Pulmonary veins", "Aorta from the body", "C"),
        ("What is the role of the medulla oblongata?", "Produce bile", "Absorb nutrients", "Control bone growth directly", "Help regulate breathing and heart rate", "D"),
        ("Which type of muscle is generally under voluntary control?", "Skeletal muscle", "Cardiac muscle", "Smooth muscle in the intestine", "Muscle in blood vessel walls", "A"),
        ("What is the main function of the pancreas in digestion?", "Store urine", "Release digestive enzymes into the small intestine", "Exchange gases", "Transmit visual signals", "B"),
        ("Why is the human skeleton important for movement?", "Bones contract like muscles", "Bones produce digestive juices", "Bones provide attachment points for muscles", "Bones replace the nervous system", "C"),
        ("What is the main function of the immune system?", "Digest fats", "Pump oxygen directly into cells", "Regulate vision", "Protect the body against pathogens", "D"),
    ],

    "Hard": [
        ("Why does blood flow through pulmonary circulation?", "To carry blood between the heart and lungs for gas exchange", "To carry food from the intestine", "To produce urine", "To send nerve impulses", "A"),
        ("What is the main advantage of double circulation in humans?", "It eliminates the need for lungs", "It separates pulmonary and systemic circulation and supports efficient oxygen delivery", "It prevents the heart from beating", "It stops blood pressure from changing", "B"),
        ("What happens when blood glucose rises after a meal in a healthy person?", "Insulin secretion always stops", "The kidneys stop functioning", "Insulin promotes glucose uptake and storage", "The lungs release insulin", "C"),
        ("Why does damage to the alveoli impair oxygen uptake?", "Alveoli normally produce red blood cells", "Alveoli pump blood directly", "Alveoli digest proteins", "Damage reduces effective gas-exchange surface area", "D"),
        ("What is the likely consequence of severe blockage in a coronary artery?", "Reduced oxygen supply to heart muscle", "Increased oxygen delivery to all tissues", "Immediate improvement in heart function", "Increased digestion of fats", "A"),
        ("Why does the left ventricle have a thicker muscular wall than the right ventricle?", "It receives all air from the lungs", "It pumps blood around the systemic circulation at higher pressure", "It filters urine", "It controls digestion", "B"),
        ("What is the main purpose of negative feedback in endocrine regulation?", "Increase every hormone continuously", "Prevent all body changes", "Counteract deviations from a regulated condition", "Stop communication between organs", "C"),
        ("How does antidiuretic hormone generally help when the body lacks water?", "It prevents all kidney filtration", "It increases water loss in urine", "It stops blood circulation", "It increases water reabsorption by the kidneys", "D"),
        ("Why can damage to the myelin sheath slow nerve transmission?", "It interferes with efficient conduction along the axon", "It increases bone density", "It produces digestive enzymes", "It causes alveoli to expand", "A"),
        ("What is the main benefit of the countercurrent arrangement in the kidney loop of Henle?", "It prevents blood from entering the kidneys", "It helps establish an osmotic gradient for concentrating urine", "It produces insulin", "It stops filtration permanently", "B"),
        ("Why can severe diarrhoea lead to dehydration and electrolyte imbalance?", "It increases bone formation", "It stops oxygen entering the lungs", "It causes excessive loss of water and electrolytes", "It makes the heart produce urine", "C"),
        ("What is the immediate purpose of vasoconstriction in many blood vessels?", "Increase the diameter of the vessel", "Stop all nerve activity", "Increase intestinal absorption directly", "Narrow the vessel and increase resistance to blood flow", "D"),
        ("Why does exercise usually increase breathing rate?", "Working muscles require more oxygen and produce more carbon dioxide", "The kidneys stop filtering blood", "The body stops producing ATP", "The skeleton replaces the lungs", "A"),
        ("What is the function of the sinoatrial node?", "Filter blood plasma", "Initiate the normal electrical rhythm of the heart", "Produce bile", "Control voluntary movement directly", "B"),
        ("How does the body usually respond to a sudden drop in blood pressure?", "It stops the heart permanently", "It stops all hormone release", "Reflex responses increase heart rate and vascular tone", "It prevents blood from reaching the brain", "C"),
        ("Why can kidney failure disturb acid-base balance?", "Kidneys produce all oxygen in the body", "Kidneys control vision directly", "Kidneys form skeletal muscles", "Kidneys help regulate hydrogen ions and bicarbonate", "D"),
        ("What is the main effect of a deficiency of thyroid hormones in children?", "Impaired growth and development", "Increased oxygen production by the lungs", "Loss of all digestive enzymes", "Immediate increase in bone length without limit", "A"),
        ("Why are the hepatic portal veins important?", "They carry air to the liver", "They transport nutrient-rich blood from digestive organs to the liver", "They carry urine to the bladder", "They connect the brain directly to the lungs", "B"),
        ("What is the role of surfactant in the alveoli?", "Increase surface tension", "Digest oxygen", "Reduce surface tension and help prevent alveolar collapse", "Block all gas exchange", "C"),
        ("Why does damage to the medulla oblongata pose a serious risk?", "It stores all body calcium", "It controls the formation of teeth only", "It produces bile", "It contains centres involved in vital functions such as breathing", "D"),
        ("What is the primary role of the sinoatrial node in a normal heartbeat?", "Act as the heart's natural pacemaker", "Filter blood in the kidneys", "Produce red blood cells", "Control intestinal absorption", "A"),
        ("How does the Bohr effect assist oxygen delivery to active tissues?", "It makes haemoglobin unable to bind oxygen anywhere", "Higher carbon dioxide and lower pH promote oxygen unloading", "It stops carbon dioxide transport", "It prevents oxygen from entering the blood", "B"),
        ("Why does the body increase aldosterone release when sodium levels or effective circulating volume are low?", "To increase sodium loss in urine", "To stop kidney function", "To promote sodium reabsorption by the kidneys", "To stop water movement completely", "C"),
        ("What is the main danger of a thrombus blocking a cerebral artery?", "Improved oxygen delivery to the brain", "Increased digestion", "Increased urine production", "Reduced blood supply can cause an ischaemic stroke", "D"),
        ("Why can damage to pancreatic beta cells cause diabetes mellitus?", "Insulin production may become inadequate", "The lungs stop producing oxygen", "Red blood cells become neurons", "The liver stops receiving blood entirely", "A"),
        ("What is the function of the loop of Henle in the nephron?", "Produce bile", "Help establish the medullary concentration gradient", "Pump blood through the heart", "Transmit impulses to skeletal muscles", "B"),
        ("Why can excessive loss of potassium affect heart rhythm?", "Potassium has no role in electrical activity", "It only affects digestion", "Potassium gradients help determine cardiac cell electrical activity", "It prevents all muscle contraction permanently", "C"),
        ("What is the physiological significance of the baroreceptor reflex?", "It regulates eye colour", "It digests carbohydrates", "It produces red blood cells", "It helps stabilize blood pressure in response to changes", "D"),
        ("Why can chronic obstruction of airflow make breathing difficult?", "It increases resistance to airflow", "It eliminates the need for respiratory muscles", "It increases the number of kidneys", "It stops the heart from receiving blood directly", "A"),
        ("What is the main function of the hypothalamus in homeostasis?", "Digest food in the stomach", "Help regulate temperature, thirst, and endocrine control", "Filter waste from blood", "Produce red blood cells", "B"),
    ],
}


def normalize(text):
    return " ".join(text.casefold().split())


def main():
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DATABASE_PATH}"
        )

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        connection.execute("PRAGMA foreign_keys = ON")

        lesson = connection.execute(
            """
            SELECT id
            FROM lessons
            WHERE lower(trim(title)) = lower(trim(?))
            """,
            ("Human Body Systems",),
        ).fetchone()

        if lesson is None:
            raise RuntimeError(
                "Human Body Systems lesson was not found."
            )

        lesson_id = lesson[0]
        total_inserted = 0

        # All changes are committed together.
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
                        f"Missing {difficulty} quiz for Human Body Systems."
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
                        f"{difficulty} already has {current_count} "
                        f"questions; target is {TARGET_QUESTIONS}."
                    )

                added = 0

                for item in candidates:
                    if current_count >= TARGET_QUESTIONS:
                        break

                    question, a, b, c, d, answer = item
                    normalized_question = normalize(question)

                    if normalized_question in existing_questions:
                        print(
                            f"Skipping duplicate ({difficulty}): "
                            f"{question}"
                        )
                        continue

                    if answer not in {"A", "B", "C", "D"}:
                        raise ValueError(
                            f"Invalid answer key: {question}"
                        )

                    if not all(
                        option.strip() for option in (a, b, c, d)
                    ):
                        raise ValueError(
                            f"Empty answer option: {question}"
                        )

                    connection.execute(
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
                        (quiz_id, question, a, b, c, d, answer),
                    )

                    existing_questions.add(normalized_question)
                    current_count += 1
                    added += 1
                    total_inserted += 1

                if current_count != TARGET_QUESTIONS:
                    raise RuntimeError(
                        f"{difficulty} has {current_count} questions, "
                        f"not {TARGET_QUESTIONS}. Add more unique questions. "
                        "The transaction will roll back."
                    )

                print(
                    f"{difficulty}: added {added}; "
                    f"final count = {current_count}"
                )

        print("\nHuman Body Systems expansion completed!")
        print(f"Total new questions inserted: {total_inserted}")
        print("Easy: 30 questions")
        print("Medium: 30 questions")
        print("Hard: 30 questions")
        print("Other lessons and Social Science were not modified.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()