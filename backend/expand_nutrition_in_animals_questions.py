import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

LESSON_TITLE = "Nutrition in Animals"
TARGET_QUESTIONS = 30

QUESTION_BANK = {
    "Easy": [
        ("What is nutrition?", ["The process of obtaining and using food", "The process of breathing only", "The movement of water", "The removal of waste only"], "A"),
        ("Which nutrient is the body's main source of energy?", ["Vitamins", "Carbohydrates", "Minerals", "Water"], "B"),
        ("Which organ is mainly responsible for chewing food?", ["Stomach", "Liver", "Mouth", "Small intestine"], "C"),
        ("Which enzyme in saliva begins the digestion of starch?", ["Pepsin", "Lipase", "Trypsin", "Salivary amylase"], "D"),
        ("Where does most digestion and absorption of nutrients occur in humans?", ["Small intestine", "Large intestine", "Oesophagus", "Mouth"], "A"),
        ("Which organ produces bile?", ["Stomach", "Liver", "Pancreas", "Small intestine"], "B"),
        ("What is the main function of the teeth?", ["Absorb nutrients", "Produce bile", "Break food into smaller pieces", "Transport blood"], "C"),
        ("Which organ carries food from the mouth to the stomach?", ["Trachea", "Large intestine", "Pancreas", "Oesophagus"], "D"),
        ("Which nutrient is important for growth and tissue repair?", ["Protein", "Water only", "Fibre only", "Salt only"], "A"),
        ("Which organ stores food temporarily and mixes it with gastric juice?", ["Liver", "Stomach", "Kidney", "Heart"], "B"),
        ("What is the process of breaking complex food into simpler substances called?", ["Respiration", "Circulation", "Digestion", "Excretion"], "C"),
        ("Which part of the digestive system absorbs much of the remaining water from undigested food?", ["Mouth", "Oesophagus", "Stomach", "Large intestine"], "D"),
        ("Which nutrient helps build and repair body tissues?", ["Proteins", "Carbohydrates only", "Water only", "Fibre only"], "A"),
        ("What is the function of the tongue during eating?", ["Produce insulin", "Help mix food with saliva and swallow it", "Absorb most nutrients", "Produce bile"], "B"),
        ("Which organ produces digestive enzymes and bicarbonate that enter the small intestine?", ["Heart", "Kidney", "Pancreas", "Lungs"], "C"),
        ("What is the semi-liquid mixture of partially digested food in the stomach called?", ["Saliva", "Bile", "Blood plasma", "Chyme"], "D"),
        ("Which type of animal eats only plants?", ["Herbivore", "Carnivore", "Omnivore", "Scavenger only"], "A"),
        ("Which type of animal eats other animals?", ["Herbivore", "Carnivore", "Producer", "Decomposer only"], "B"),
        ("Which animal is an example of an omnivore?", ["Cow", "Deer", "Human", "Rabbit"], "C"),
        ("What is absorption in digestion?", ["Chewing food", "Swallowing food", "Breaking food into pieces", "Movement of digested nutrients into blood or lymph"], "D"),
        ("Which vitamin can the human body produce in the skin with sufficient sunlight exposure?", ["Vitamin D", "Vitamin C", "Vitamin B12", "Vitamin K only from sunlight"], "A"),
        ("What is the function of the epiglottis during swallowing?", ["Produce digestive enzymes", "Help prevent food from entering the airway", "Absorb nutrients", "Store bile"], "B"),
        ("Which substance helps emulsify fats in the small intestine?", ["Saliva", "Hydrochloric acid", "Bile", "Insulin"], "C"),
        ("Which teeth are mainly used for cutting food?", ["Molars", "Premolars", "Canines", "Incisors"], "D"),
        ("Which teeth are mainly used for grinding food?", ["Molars", "Incisors", "Canines", "Milk teeth only"], "A"),
        ("What is the main function of the large intestine?", ["Produce saliva", "Absorb water and form faeces", "Begin protein digestion", "Produce bile"], "B"),
        ("Which nutrient provides the most energy per gram among carbohydrates, proteins and fats?", ["Carbohydrates", "Proteins", "Fats", "Water"], "C"),
        ("What is the process of taking food into the body called?", ["Absorption", "Assimilation", "Egestion", "Ingestion"], "D"),
        ("Which part of the digestive system contains villi that increase the surface area for absorption?", ["Small intestine", "Oesophagus", "Mouth", "Trachea"], "A"),
        ("Why is a balanced diet important?", ["It contains only one nutrient", "It supplies different nutrients in suitable amounts", "It eliminates the need for water", "It prevents all diseases with certainty"], "B"),
    ],

    "Medium": [
        ("Why is digestion necessary for many food molecules?", ["All food molecules are already small enough to enter blood", "Digestion converts oxygen into nutrients", "Large, complex molecules must be broken into absorbable smaller molecules", "Digestion occurs only to remove water"], "C"),
        ("What is the main role of hydrochloric acid in the stomach?", ["Emulsify fats", "Absorb glucose", "Produce bile", "Provide an acidic environment and help kill many microbes"], "D"),
        ("Why does the small intestine have numerous villi?", ["To increase the surface area for nutrient absorption", "To store food for several days", "To produce teeth", "To prevent all movement of food"], "A"),
        ("What is the main function of bile in fat digestion?", ["Break proteins into amino acids directly", "Emulsify fats into smaller droplets", "Convert starch into glucose directly", "Digest cellulose in humans"], "B"),
        ("Which enzyme breaks proteins into smaller peptides in the stomach?", ["Amylase", "Lipase", "Pepsin", "Maltase"], "C"),
        ("Why does chewing improve digestion?", ["It completes all chemical digestion", "It absorbs glucose directly into blood", "It produces bile", "It increases the surface area of food and mixes it with saliva"], "D"),
        ("What is peristalsis?", ["Wave-like muscular contractions that move food along the digestive tract", "The chemical breakdown of starch only", "Absorption of water in the kidneys", "Production of red blood cells"], "A"),
        ("What happens to most digested glucose after absorption?", ["It is converted immediately into bile", "It enters circulation and can be used for energy or stored", "It becomes an enzyme in the stomach", "It leaves the body unchanged in faeces"], "B"),
        ("Why are proteins broken down during digestion?", ["Proteins cannot contain nitrogen", "Proteins are absorbed only as whole muscles", "They are broken into amino acids and small peptides for absorption", "They must be changed into fats before entering the intestine"], "C"),
        ("Which statement correctly describes the role of pancreatic juice?", ["It contains only bile pigments", "It stores undigested food", "It prevents food from entering the stomach", "It supplies enzymes and bicarbonate to the small intestine"], "D"),
        ("Why does the stomach normally not digest itself?", ["Its mucus-bicarbonate barrier protects the lining, alongside other protective mechanisms", "It contains no acid", "It contains no digestive enzymes", "Its lining is made of food particles"], "A"),
        ("What is assimilation?", ["Movement of food into the mouth", "Use of absorbed nutrients by body cells", "Removal of faeces from the body", "Mechanical chewing of food"], "B"),
        ("Why can a lack of dietary fibre contribute to constipation?", ["Fibre destroys all intestinal bacteria", "Fibre prevents water from entering food", "Fibre helps stool retain water and supports normal bowel movement", "Fibre stops the intestine from contracting"], "C"),
        ("Which enzyme begins carbohydrate digestion in the mouth?", ["Pepsin", "Trypsin", "Lipase only", "Salivary amylase"], "D"),
        ("Where does most chemical digestion and absorption of nutrients occur?", ["Small intestine", "Oesophagus", "Large intestine", "Rectum"], "A"),
        ("Why is the pancreas important for digestion?", ["It stores all faeces", "It releases digestive enzymes into the small intestine", "It chews food", "It transports food to the stomach"], "B"),
        ("What is the role of lipase?", ["Break down starch", "Break down DNA only", "Break down fats into fatty acids and monoglycerides", "Break down oxygen"], "C"),
        ("Why can lactose intolerance cause bloating and diarrhoea after dairy consumption?", ["The stomach produces too much bile in every case", "Lactose becomes protein", "The small intestine absorbs lactose unchanged in everyone", "Insufficient lactase leaves lactose to be fermented and draw water into the intestine"], "D"),
        ("What is the main role of the oesophagus?", ["Move swallowed food toward the stomach", "Absorb most amino acids", "Produce insulin", "Store bile"], "A"),
        ("Why does the body need water as part of a balanced diet?", ["It provides more energy per gram than fat", "It supports transport, temperature regulation and chemical reactions", "It replaces all vitamins", "It is the body's main source of protein"], "B"),
        ("Which food combination is a good source of both protein and fibre?", ["Sugar and oil", "Butter and candy", "Beans and lentils", "Soft drinks and sweets"], "C"),
        ("What is egestion?", ["Absorption of nutrients", "Chemical digestion of proteins", "Movement of food into the mouth", "Removal of undigested material as faeces"], "D"),
        ("Why is the stomach muscular?", ["To churn food and mix it with gastric secretions", "To absorb all nutrients directly", "To produce saliva", "To filter blood like a kidney"], "A"),
        ("What is the primary function of the rectum?", ["Produce digestive enzymes", "Temporarily store faeces before elimination", "Absorb most fats", "Produce bile"], "B"),
        ("Which adaptation helps ruminants digest cellulose-rich plant material?", ["A stomach with no microbes", "Absence of any fermentation", "Microorganisms in specialised digestive compartments", "Teeth that produce enzymes"], "C"),
        ("Why do herbivores often have broad molars?", ["To tear meat only", "To inject venom", "To absorb water", "To grind plant material"], "D"),
        ("Which nutrient is the body's main long-term energy store?", ["Fat", "Water", "Vitamin C", "Mineral salts"], "A"),
        ("Why can severe protein deficiency affect growth and healing?", ["Proteins only provide flavour", "The body lacks sufficient amino acids for tissue synthesis and repair", "Protein deficiency increases all enzyme activity", "Protein is needed only for digestion in the mouth"], "B"),
        ("What is the role of intestinal microvilli?", ["Store bile", "Move food through the oesophagus", "Further increase the absorptive surface area of intestinal cells", "Produce teeth"], "C"),
        ("Why should food be chewed before swallowing?", ["To make food impossible to digest", "To prevent saliva mixing with food", "To stop peristalsis permanently", "To form a manageable bolus and begin mechanical digestion"], "D"),
    ],

    "Hard": [
        ("A person has damage to the villi of the small intestine. Which effect is most likely?", ["Reduced absorption of nutrients", "Increased production of saliva", "Improved nutrient absorption in every case", "Complete prevention of chewing"], "A"),
        ("A patient produces very little pancreatic lipase. Which digestive process is most directly affected?", ["Starch digestion in the mouth", "Fat digestion in the small intestine", "Mechanical chewing", "Movement of food through the oesophagus"], "B"),
        ("Why can blockage of the bile duct interfere with fat absorption?", ["Bile is the enzyme that digests all proteins", "Bile transports oxygen to the stomach", "Less bile reaches the intestine to emulsify fats and support their digestion and absorption", "Bile is required for chewing"], "C"),
        ("A person has a deficiency of lactase. Which substance is most likely to remain incompletely digested after drinking milk?", ["Starch", "Protein", "Triglyceride", "Lactose"], "D"),
        ("Why can prolonged diarrhoea lead to dehydration?", ["The body loses excessive water and electrolytes in frequent stools", "The body absorbs too much water", "The stomach stops producing teeth", "The liver converts all water into fat"], "A"),
        ("A person has a narrowed oesophagus but normal stomach enzyme production. Which function is most directly impaired?", ["Absorption of amino acids in the small intestine", "Transport of swallowed food to the stomach", "Production of bile", "Absorption of most water in the large intestine"], "B"),
        ("Why can untreated damage to pancreatic cells affect both digestion and blood glucose regulation?", ["The pancreas only stores food", "The pancreas produces red blood cells", "The pancreas supplies digestive secretions and hormones such as insulin", "The pancreas is the main site of chewing"], "C"),
        ("A person has low stomach acid. Which consequence may occur?", ["Fat digestion stops completely in the mouth", "The small intestine no longer has villi", "All carbohydrates become proteins", "Protein digestion and the stomach's defence against some microbes may be impaired"], "D"),
        ("Which sequence correctly follows the movement of food after swallowing?", ["Oesophagus → stomach → small intestine → large intestine", "Small intestine → oesophagus → stomach → rectum", "Stomach → mouth → large intestine → oesophagus", "Trachea → stomach → kidney → small intestine"], "A"),
        ("Why does emulsification improve the efficiency of fat digestion?", ["It changes fats directly into amino acids", "It increases the surface area available to lipase", "It removes the need for digestive enzymes", "It converts fats into carbohydrates before digestion"], "B"),
        ("A person consumes enough calories but very little vitamin C over a long period. Which problem may develop?", ["Scurvy and impaired collagen formation", "Lactose intolerance in every case", "Excessive production of vitamin C", "Inability to digest all carbohydrates"], "C"),
        ("Why can a diet extremely low in dietary fibre contribute to bowel problems?", ["Fibre is the only source of protein", "Fibre prevents stool from forming", "Fibre is digested completely into oxygen", "Low fibre intake can reduce stool bulk and make bowel movements more difficult"], "D"),
        ("Which change is most likely to impair protein digestion in the stomach?", ["Loss of pepsin activity", "Reduced chewing of fats", "Increased absorption of water by the colon", "Increased bile release into the gallbladder"], "A"),
        ("Why does the stomach's acidic environment help pepsin function?", ["It converts pepsin into a carbohydrate", "Pepsin works best in an acidic environment", "It makes bile unnecessary", "It directly absorbs all amino acids"], "B"),
        ("A person has extensive damage to the intestinal lining. Why might weight loss occur even when food intake is adequate?", ["Food intake alone guarantees absorption", "The liver stops producing every enzyme", "Reduced absorptive surface can cause nutrient malabsorption", "The oesophagus begins absorbing all nutrients"], "C"),
        ("Which statement best distinguishes digestion from absorption?", ["Digestion moves nutrients into blood; absorption breaks food apart", "Digestion and absorption are identical", "Absorption occurs only in the mouth", "Digestion breaks food into simpler substances; absorption moves digested nutrients into the body"], "D"),
        ("Why does the small intestine receive pancreatic bicarbonate?", ["To neutralise acidic chyme and create a more suitable pH for intestinal enzymes", "To convert all fats into proteins", "To stop nutrients from being absorbed", "To produce hydrochloric acid"], "A"),
        ("A person has difficulty swallowing because the epiglottis does not function correctly. What is a major risk?", ["Increased vitamin absorption", "Food or liquid entering the airway", "Excessive production of bile", "Failure of teeth to develop"], "B"),
        ("Which nutrient deficiency is most directly associated with impaired oxygen transport due to reduced haemoglobin production?", ["Vitamin D deficiency only", "Fibre deficiency", "Iron deficiency", "Water deficiency only"], "C"),
        ("Why can a very high-fat meal delay stomach emptying in some circumstances?", ["Fat is absorbed only in the mouth", "Fat immediately becomes glucose in the stomach", "Fat prevents the stomach from contracting at all", "Fat in the small intestine triggers signals that can slow gastric emptying"], "D"),
        ("Which adaptation makes the small intestine effective at absorption?", ["Long length, folds, villi and microvilli with a rich blood supply", "Thick enamel and no blood vessels", "A complete absence of epithelial cells", "A narrow tube with no internal surface area"], "A"),
        ("Why does the body convert excess glucose into glycogen for storage?", ["Glycogen provides no stored energy", "Glycogen provides a readily mobilised carbohydrate reserve, mainly in liver and muscle", "Glycogen is a digestive enzyme", "Glycogen replaces all body proteins"], "B"),
        ("A person has a blocked pancreatic duct. Which outcome is most likely?", ["Food cannot enter the mouth", "The liver stops producing bile immediately in every case", "Digestive enzymes and bicarbonate may not reach the small intestine adequately", "The large intestine begins producing teeth"], "C"),
        ("Why can severe diarrhoea be particularly dangerous in young children?", ["Children never need electrolytes", "It increases body water indefinitely", "It prevents all nutrient digestion but causes no fluid loss", "Dehydration and electrolyte imbalance can develop rapidly"], "D"),
        ("Which statement about bile is correct?", ["It is produced by the liver and stored in the gallbladder", "It is produced by the teeth", "It is an enzyme that directly breaks proteins into amino acids", "It is produced only in the large intestine"], "A"),
        ("Why can a lack of intrinsic factor lead to vitamin B12 deficiency?", ["It prevents carbohydrate digestion in the mouth", "Intrinsic factor is needed for normal vitamin B12 absorption in the terminal ileum", "It prevents bile from being produced", "It stops the stomach from moving food"], "B"),
        ("A person has a disease that damages the terminal ileum. Which deficiency risk may increase?", ["Vitamin C only", "Calcium in every case regardless of diet", "Vitamin B12 malabsorption", "Oxygen deficiency from reduced breathing"], "C"),
        ("Why is protein-energy malnutrition especially harmful during childhood?", ["It improves immune function in all cases", "It guarantees rapid growth", "It affects only tooth colour", "It can impair growth, tissue repair, immunity and development"], "D"),
        ("Which combination best describes the major roles of the liver in digestion and metabolism?", ["Produces bile, processes absorbed nutrients and helps regulate metabolism", "Produces saliva and chews food", "Stores all undigested faeces", "Moves food through the oesophagus"], "A"),
        ("A patient has reduced intestinal motility and severe constipation. Which process is most directly affected?", ["Production of saliva", "Movement of intestinal contents and elimination of faeces", "Production of chlorophyll", "Pollination"], "B"),
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

        print("\nNutrition in Animals expansion completed!")
        print(f"Total new questions inserted: {inserted_total}")
        print("Easy: 30 questions")
        print("Medium: 30 questions")
        print("Hard: 30 questions")
        print("Other lessons and Social Science were not modified.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()