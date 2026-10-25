import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

LESSON_TITLE = "Microorganisms"
TARGET_QUESTIONS = 30

QUESTION_BANK = {
    "Easy": [
        ("What are microorganisms?", ["Organisms that are generally too small to see clearly without magnification", "Very large animals", "Only flowering plants", "Non-living rocks"], "A"),
        ("Which instrument is commonly used to observe many microorganisms?", ["Telescope", "Microscope", "Periscope", "Binoculars only"], "B"),
        ("Which of these is a bacterium?", ["Mushroom", "Fern", "Lactobacillus", "Earthworm"], "C"),
        ("Which microorganism causes malaria?", ["Bacterium", "Fungus", "Virus", "Plasmodium"], "D"),
        ("Which microorganism is commonly used to make bread rise?", ["Yeast", "Amoeba", "Plasmodium", "Paramecium"], "A"),
        ("Which of these is a virus?", ["Lactobacillus", "Influenza virus", "Yeast", "Amoeba"], "B"),
        ("Which microorganism is used to make curd from milk?", ["Plasmodium", "Mushroom", "Lactic acid bacteria", "Mosquito"], "C"),
        ("Which group includes organisms such as mushrooms and moulds?", ["Viruses", "Protozoa", "Bacteria", "Fungi"], "D"),
        ("What is fermentation by yeast commonly used to produce in bread dough?", ["Carbon dioxide", "Oxygen", "Nitrogen", "Helium"], "A"),
        ("Which of these is a single-celled protozoan?", ["Mango plant", "Amoeba", "Earthworm", "Mushroom"], "B"),
        ("Which microorganism is commonly associated with the disease tuberculosis?", ["Yeast", "Plasmodium", "Mycobacterium tuberculosis", "Influenza virus"], "C"),
        ("What is the process of killing harmful microorganisms on suitable surfaces called?", ["Pollination", "Photosynthesis", "Fermentation", "Disinfection"], "D"),
        ("Which of these diseases is caused by a virus?", ["Influenza", "Tuberculosis", "Cholera", "Ringworm"], "A"),
        ("What is an antibiotic mainly used to treat?", ["All viral infections", "Certain bacterial infections", "Broken bones", "Vitamin deficiencies"], "B"),
        ("Which microorganism helps convert atmospheric nitrogen into forms plants can use?", ["Influenza virus", "Plasmodium", "Certain nitrogen-fixing bacteria", "Bread mould only"], "C"),
        ("Which of these is a useful role of microorganisms in the environment?", ["They stop all decomposition", "They eliminate all soil nutrients", "They prevent every plant from growing", "They decompose dead organic matter"], "D"),
        ("Which microorganism is commonly used in making some cheeses and fermented foods?", ["Bacteria", "Mosquitoes", "Earthworms only", "Fish"], "A"),
        ("What is the basic genetic material found in viruses?", ["Only starch", "DNA or RNA", "Only cellulose", "Only protein with no genetic material"], "B"),
        ("Which of these is a fungal disease in humans?", ["Malaria", "Influenza", "Ringworm", "Polio"], "C"),
        ("What is pasteurisation?", ["Freezing food until it becomes solid", "Adding soil to milk", "Removing all nutrients from food", "Heating a food or drink under controlled conditions to reduce harmful microbes"], "D"),
        ("Which microorganism is commonly used in the production of yoghurt?", ["Lactic acid bacteria", "Plasmodium", "Influenza virus", "Amoeba"], "A"),
        ("What is a vaccine designed to do?", ["Cause every disease", "Train the immune system to recognise a pathogen or its components", "Replace all blood cells", "Digest food"], "B"),
        ("Which microorganism can cause cholera?", ["Yeast", "Influenza virus", "Vibrio cholerae bacterium", "Amoeba proteus"], "C"),
        ("Which of these is a common way to prevent the spread of many infections?", ["Sharing unwashed utensils", "Ignoring food safety", "Drinking untreated water", "Washing hands with soap"], "D"),
        ("What is decomposition?", ["Breakdown of dead organic matter", "Formation of sunlight", "Production of rocks by animals", "Movement of planets"], "A"),
        ("Which microorganism is used in the production of penicillin?", ["Amoeba", "Penicillium mould", "Plasmodium", "Influenza virus"], "B"),
        ("What is a pathogen?", ["A useful mineral", "A type of nutrient", "An organism or agent that can cause disease", "A plant root"], "C"),
        ("Which of these can spread some infectious diseases between humans?", ["Only sunlight", "Only clean drinking water", "Only oxygen", "Contaminated hands or surfaces"], "D"),
        ("Why should antibiotics be used only when appropriate and as directed by a qualified healthcare professional?", ["Misuse can contribute to antibiotic resistance", "They cure every viral infection", "They have no effect on bacteria", "They replace vaccination"], "A"),
        ("Which group includes microscopic organisms that lack a membrane-bound nucleus?", ["Fungi", "Bacteria", "Animals", "Plants"], "B"),
    ],

    "Medium": [
        ("Why are viruses often described as being at the boundary between living and non-living?", ["They carry out all metabolism independently", "They are made of cells like animals", "They require host cells to replicate and cannot reproduce independently", "They have no genetic material"], "C"),
        ("How do many bacteria reproduce under favourable conditions?", ["By forming flowers", "By producing seeds", "By mating like mammals", "By binary fission"], "D"),
        ("Why is yeast useful in baking?", ["It ferments sugars and releases carbon dioxide", "It consumes all the flour without producing gas", "It converts oxygen into nitrogen", "It prevents dough from rising"], "A"),
        ("What is the role of decomposer microorganisms in an ecosystem?", ["They prevent nutrient cycling", "They break down organic material and recycle nutrients", "They produce all sunlight", "They eliminate soil fertility"], "B"),
        ("Why can contaminated water spread diseases such as cholera?", ["Cholera is transmitted only by air", "Bacteria cannot survive in water", "Water containing the pathogen may be ingested", "Water automatically kills every pathogen"], "C"),
        ("How does vaccination help protect against certain infectious diseases?", ["It replaces the immune system", "It guarantees that no infection can ever occur", "It directly kills every pathogen in the environment", "It prepares immune responses against a specific pathogen or antigen"], "D"),
        ("Why should raw and cooked foods be kept separate during preparation?", ["To reduce cross-contamination by harmful microorganisms", "To increase contamination", "To make food lose all nutrients", "To encourage bacterial growth"], "A"),
        ("What is antibiotic resistance?", ["A person's immunity to every virus", "The ability of bacteria to survive or grow despite an antibiotic that would normally inhibit them", "The ability of antibiotics to destroy all organisms", "A condition caused only by cold weather"], "B"),
        ("Why can some bacteria be beneficial to humans?", ["All bacteria cause disease", "Bacteria cannot live in the human body", "Some help digestion, produce useful substances or support other normal functions", "They replace all human cells"], "C"),
        ("Which condition generally encourages the rapid growth of many food-spoilage bacteria?", ["Suitable warmth, moisture and nutrients", "Extreme dryness for every species", "Complete absence of nutrients", "Conditions that destroy their cells"], "D"),
        ("What is the purpose of refrigeration in food preservation?", ["It slows the growth of many microorganisms", "It sterilises every food completely", "It creates antibiotics in food", "It guarantees indefinite food safety"], "A"),
        ("How does drying help preserve food?", ["It increases available water for microbes", "It reduces the water available for microbial growth", "It creates new microorganisms", "It increases food temperature indefinitely"], "B"),
        ("Why is mould commonly found on moist bread left in warm conditions?", ["Bread cannot contain nutrients", "Mould grows only in frozen conditions", "Suitable moisture, temperature and nutrients support fungal growth", "Mould is a type of insect"], "C"),
        ("Which statement correctly describes nitrogen fixation?", ["It converts oxygen into glucose", "It is performed only by animals", "It destroys all nitrogen compounds", "Certain microorganisms convert atmospheric nitrogen into usable nitrogen compounds"], "D"),
        ("Why are legumes often associated with nitrogen-fixing bacteria?", ["Some have root nodules where bacteria such as Rhizobium live", "Their leaves contain no cells", "Their roots produce antibiotics in every case", "They do not require nitrogen"], "A"),
        ("What is the main difference between antiseptics and disinfectants?", ["They are always identical in use", "Antiseptics are intended for suitable living tissues, while disinfectants are used on objects or surfaces", "Disinfectants are foods", "Antiseptics are used only to preserve metals"], "B"),
        ("Why is sterilisation different from ordinary cleaning?", ["Cleaning always destroys every microbial form", "Sterilisation only removes visible dirt", "Sterilisation aims to eliminate all forms of microbial life, including resistant forms where validated", "Sterilisation means adding microorganisms"], "C"),
        ("Which disease is caused by a protozoan parasite?", ["Influenza", "Tuberculosis", "Ringworm", "Malaria"], "D"),
        ("How does malaria commonly spread between people?", ["Through bites of infected female Anopheles mosquitoes", "Through pollen", "Through direct sunlight", "Through sharing textbooks"], "A"),
        ("Why do antibiotics generally not treat viral infections?", ["Viruses are large bacteria", "Antibiotics target bacterial structures or processes that viruses do not possess in the same way", "Viruses are made only of water", "Antibiotics always strengthen viruses"], "B"),
        ("What is the purpose of food fermentation in products such as yoghurt?", ["To make food radioactive", "To eliminate all beneficial microbes", "Microorganisms transform ingredients and produce acids or other compounds that change flavour and texture", "To turn all protein into plastic"], "C"),
        ("Why is handwashing effective against many infectious diseases?", ["It increases pathogen numbers", "It replaces all vaccines", "It makes pathogens stronger", "It physically removes many microbes and can disrupt some of them when soap is used"], "D"),
        ("What does the term host mean in infectious disease biology?", ["An organism in or on which a pathogen lives or replicates", "A disinfectant", "A type of microscope", "A nutrient produced by sunlight"], "A"),
        ("Why can some fungi be useful in medicine?", ["All fungi are harmless", "Some fungi produce compounds that can be developed into medicines", "Fungi do not produce chemicals", "Fungi replace the immune system"], "B"),
        ("Which practice helps reduce the risk of foodborne illness?", ["Eating food left unrefrigerated for long periods regardless of conditions", "Using the same unwashed board for raw meat and ready-to-eat food", "Cooking food thoroughly and handling it hygienically", "Drinking water from an unknown unsafe source"], "C"),
        ("What is a carrier of an infectious disease?", ["A nutrient that cannot move", "A type of white blood cell only", "A sterilisation machine", "A person or organism that can harbour and transmit a pathogen"], "D"),
        ("Why is a complete course or prescribed duration of antibiotics important when instructed by a clinician?", ["It helps ensure the infection is treated appropriately and reduces risks associated with improper use", "It guarantees antibiotics cure viruses", "It means antibiotics can be shared with others", "It makes resistance impossible"], "A"),
        ("What is the function of a microbial culture medium in a laboratory?", ["To measure the weight of planets", "To provide nutrients and conditions for growing selected microorganisms", "To remove all genetic material from organisms", "To produce sunlight"], "B"),
        ("Why can mould spoil fruits and vegetables?", ["Moulds do not grow on organic material", "They convert every food into oxygen", "They grow on suitable produce and break down its components", "They prevent all chemical changes"], "C"),
        ("Which is an example of a disease caused by a bacterium?", ["Chickenpox", "Measles", "Influenza", "Tuberculosis"], "D"),
    ],

    "Hard": [
        ("A bacterial population is exposed to an antibiotic, and a few resistant cells survive and multiply. What best explains the resulting population?", ["Natural selection favoured bacteria with resistance traits", "The antibiotic deliberately taught every bacterium to resist it", "All bacteria became viruses", "The bacteria stopped reproducing permanently"], "A"),
        ("Why can antibiotics disrupt the normal microbiota as well as harmful bacteria?", ["Antibiotics target only viruses", "Some antibiotics affect susceptible beneficial bacteria too", "Beneficial bacteria contain no cellular structures", "Normal microbiota cannot be affected by medicines"], "B"),
        ("A sealed jar of improperly preserved food develops gas and a swollen lid. What is the safest conclusion?", ["The food is definitely safe to eat", "Gas proves that all microbes are beneficial", "Microbial activity may have occurred, so the food should not be tasted", "Heating the lid with a flame makes the food safe"], "C"),
        ("Why can bacterial endospores make food preservation more challenging?", ["They are reproductive seeds of plants", "They are always destroyed by refrigeration", "They cannot survive any environmental stress", "Some endospores resist harsh conditions and may survive treatments that kill ordinary bacterial cells"], "D"),
        ("A scientist wants to determine whether a disinfectant reduces bacterial growth. Which design provides the strongest evidence?", ["Compare treated and untreated samples under matched conditions with replication", "Use only one treated sample and no comparison", "Change the disinfectant, temperature and incubation time together", "Assume any clear-looking surface is sterile"], "A"),
        ("Why should laboratory cultures of unknown microorganisms be handled using appropriate biosafety procedures?", ["All unknown microbes are harmless", "Some may be pathogenic or produce harmful substances", "Microorganisms cannot spread outside a laboratory", "Biosafety procedures increase contamination"], "B"),
        ("How can a plasmid contribute to the spread of antibiotic resistance among bacteria?", ["It converts bacteria into fungi", "It prevents all DNA transfer", "It may carry resistance genes and can sometimes transfer between bacteria", "It destroys every resistance gene"], "C"),
        ("Why can a virus reproduce inside a host cell but not independently in the same way as a bacterium?", ["Viruses have complete cellular machinery for independent reproduction", "Viruses reproduce through plant roots", "Viruses contain no genetic instructions", "Viruses depend on host-cell machinery to make new virus particles"], "D"),
        ("A vaccine stimulates immune memory. What is the advantage of this memory during later exposure to the same pathogen?", ["The immune system may respond more rapidly and effectively", "The pathogen is guaranteed never to enter the body", "The immune system stops producing cells", "The vaccine becomes an antibiotic"], "A"),
        ("Why does misuse of antibiotics in humans and agriculture raise public-health concerns?", ["It makes all bacteria harmless", "It can select for resistant bacteria that spread between people, animals and environments", "It eliminates genetic variation in all organisms", "It prevents bacterial evolution"], "B"),
        ("Two food samples have similar nutrient content, but one has much less available water. Why may microbial growth differ?", ["Microorganisms do not need water", "Water availability only affects plants", "Lower water activity can inhibit growth of many microorganisms", "Microbial growth depends only on food colour"], "C"),
        ("Why can pasteurisation improve food safety without making a product completely sterile?", ["It adds new pathogens", "It always destroys every spore", "It is a process used only for frozen metals", "It reduces targeted harmful microorganisms but may not eliminate every microbial form"], "D"),
        ("A bacterial culture grows poorly when its pH is changed substantially from its optimum. What is the likely explanation?", ["pH affects enzyme activity and cellular processes", "Bacteria do not contain enzymes", "pH affects only the colour of the container", "All bacteria grow best at every pH"], "A"),
        ("Why is a control group important when testing a new antimicrobial substance?", ["It guarantees a positive result", "It provides a baseline for comparison against the treated group", "It removes the need for repeated trials", "It proves the treatment works before testing"], "B"),
        ("A person infected with a virus takes an antibiotic without a bacterial co-infection. Why is this unlikely to treat the viral infection itself?", ["Viruses are always killed by antibiotics", "Antibiotics convert viruses into bacteria", "The drug's bacterial targets are absent or substantially different in viruses", "Viruses do not contain genetic material"], "C"),
        ("Why can disease prevention rely on several measures rather than only one?", ["One measure always stops every pathogen", "Handwashing replaces all vaccination", "Pathogens cannot spread through more than one route", "Hygiene, vaccination, safe water and appropriate healthcare address different transmission risks"], "D"),
        ("A food sample contains bacteria that produce toxins. Why might reheating not always make the food safe?", ["Some toxins can remain active even after bacteria are killed", "Heat always removes every toxin under all conditions", "Bacteria never produce toxins", "Reheating converts toxins into nutrients"], "A"),
        ("Why are viruses usually not classified as cells?", ["They are larger than every bacterium", "They lack the full cellular structure and independent metabolism of cells", "They always have a nucleus and cytoplasm", "They reproduce only through binary fission"], "B"),
        ("A researcher observes a clear zone around an antibiotic disc on a bacterial lawn. What does it generally indicate?", ["The bacteria grew more quickly near the disc", "The disc increased bacterial mutation", "Growth was inhibited in that region under the test conditions", "The bacteria became viruses"], "C"),
        ("Why must a clear zone around an antibiotic disc be interpreted carefully?", ["It always proves the patient will be cured", "It measures only the colour of the bacteria", "It means no resistance can exist anywhere", "Zone size depends on the organism, drug diffusion and test conditions and must be interpreted with standards"], "D"),
        ("What is one ecological consequence of widespread use of broad-spectrum antibiotics?", ["Disruption of microbial communities and selection for resistance", "Guaranteed elimination of all disease", "Permanent prevention of mutation", "Conversion of bacteria into plants"], "A"),
        ("Why are bacteriophages scientifically useful?", ["They infect only human red blood cells", "They infect bacteria and can be studied for bacterial biology or potential targeted applications", "They are a type of antibiotic molecule", "They contain no genetic material"], "B"),
        ("A population of microbes is exposed to repeated sublethal doses of an antimicrobial. Why can this be concerning?", ["It prevents all adaptation", "It guarantees immediate sterilisation", "It may select for organisms better able to tolerate the treatment", "It makes all organisms genetically identical"], "C"),
        ("Why is the relationship between microbes and humans not always harmful?", ["Every microbe causes disease", "Microbes have no role in digestion", "Humans do not host any microorganisms", "Many microbes support digestion, nutrient cycling, food production and other useful processes"], "D"),
        ("A researcher wants to compare bacterial growth at different temperatures. Which variables should be kept similar?", ["Starting inoculum, growth medium, incubation duration and other relevant conditions", "Only the label colour", "Different bacterial species and different nutrients for every temperature", "All measurements except the temperature"], "A"),
        ("Why can an infection spread even when an infected person has mild or no symptoms?", ["Pathogens cannot spread before severe symptoms", "Some infected people can transmit pathogens before symptoms or without obvious illness", "All pathogens require visible symptoms to reproduce", "Mild symptoms prove there is no infection"], "B"),
        ("Which statement best explains why nitrogen-fixing bacteria are important in ecosystems?", ["They convert all nitrogen into oxygen", "They stop plants from absorbing nutrients", "They convert atmospheric nitrogen into compounds that can enter biological nutrient cycles", "They remove all nitrogen from soil"], "C"),
        ("Why can food spoilage occur even when food initially looks and smells normal?", ["Spoiled food always changes appearance immediately", "Pathogens always produce a strong smell", "Microbial contamination can never occur without visible mould", "Some harmful microbes or toxins may be present without obvious sensory changes"], "D"),
        ("A hospital uses antimicrobial agents frequently but ignores cleaning and hand hygiene. Why may infections still spread?", ["Antimicrobial agents do not replace infection-control measures and can select for resistance", "Antibiotics stop all transmission routes permanently", "Pathogens cannot survive on hands", "Cleaning increases the virulence of every pathogen"], "A"),
        ("Why is a pure microbial culture useful in experiments?", ["It contains many unidentified species by design", "It helps researchers attribute observed effects to a particular microorganism", "It guarantees that the organism is harmless", "It removes the need for experimental controls"], "B"),
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

        print("\nMicroorganisms expansion completed!")
        print(f"Total new questions inserted: {inserted_total}")
        print("Easy: 30 questions")
        print("Medium: 30 questions")
        print("Hard: 30 questions")
        print("Other lessons and Social Science were not modified.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()