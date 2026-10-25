import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

LESSON_TITLE = "Reproduction in Animals"
TARGET_QUESTIONS = 30

QUESTION_BANK = {
    "Easy": [
        ("What is reproduction?", ["The process by which organisms produce offspring", "The process of breathing", "The process of digestion", "The movement of blood"], "A"),
        ("Which type of reproduction involves the fusion of male and female gametes?", ["Asexual reproduction", "Sexual reproduction", "Vegetative propagation", "Budding only"], "B"),
        ("What is the male reproductive cell called?", ["Ovum", "Embryo", "Sperm", "Zygote"], "C"),
        ("What is the female reproductive cell called?", ["Sperm", "Pollen", "Embryo", "Ovum"], "D"),
        ("What is formed when a sperm fuses with an ovum?", ["Zygote", "Larva", "Pollen grain", "Bud"], "A"),
        ("What is fertilisation?", ["The formation of food", "Fusion of male and female gametes", "The growth of bones", "The removal of waste"], "B"),
        ("Which organ produces sperm in human males?", ["Ovaries", "Uterus", "Testes", "Kidneys"], "C"),
        ("Which organs produce ova in human females?", ["Testes", "Lungs", "Pancreas", "Ovaries"], "D"),
        ("Where does a human embryo normally develop?", ["Uterus", "Stomach", "Liver", "Kidney"], "A"),
        ("Which animal commonly lays eggs?", ["Cow", "Hen", "Dog", "Cat"], "B"),
        ("Which animal is an example of a mammal that gives birth to live young?", ["Frog", "Butterfly", "Cow", "Fish"], "C"),
        ("What is the early stage formed after fertilisation called?", ["Adult", "Pupa", "Larva", "Zygote"], "D"),
        ("Which animal commonly undergoes metamorphosis from tadpole to adult?", ["Frog", "Cow", "Dog", "Human"], "A"),
        ("What is budding?", ["Reproduction through seeds only", "Formation of a new individual from an outgrowth on the parent", "Fusion of sperm and ovum", "Growth of a bone"], "B"),
        ("Which organism commonly reproduces by budding?", ["Human", "Frog", "Hydra", "Cow"], "C"),
        ("Which organism can reproduce through binary fission?", ["Bird", "Cat", "Butterfly", "Amoeba"], "D"),
        ("What is the stage between an embryo and an adult in many insects called?", ["Larva", "Gamete", "Zygote", "Ovum"], "A"),
        ("Which reproductive process produces genetically varied offspring through gamete fusion?", ["Binary fission", "Sexual reproduction", "Budding only", "Fragmentation only"], "B"),
        ("What is the function of the uterus?", ["Produce sperm", "Produce digestive enzymes", "Support the development of an embryo and foetus", "Filter blood"], "C"),
        ("Which tube carries an ovum from an ovary toward the uterus?", ["Trachea", "Ureter", "Oesophagus", "Fallopian tube"], "D"),
        ("What is external fertilisation?", ["Fusion of gametes outside the female's body", "Fusion of gametes only inside the uterus", "Reproduction without gametes in every case", "Growth from a stem cutting"], "A"),
        ("Which animal commonly has external fertilisation?", ["Dog", "Frog", "Cow", "Human"], "B"),
        ("What is internal fertilisation?", ["Formation of a bud", "Release of eggs into soil", "Fusion of gametes inside the body", "Formation of a seed without fertilisation"], "C"),
        ("What is metamorphosis?", ["The movement of blood", "The process of digestion", "The formation of gametes only", "A major change in body form during development"], "D"),
        ("Which of these animals undergoes complete metamorphosis?", ["Butterfly", "Cow", "Dog", "Human"], "A"),
        ("What is a foetus?", ["An unfertilised egg", "A later developing stage of an embryo", "A male gamete", "A type of bacteria"], "B"),
        ("Which structure connects a developing human foetus to the placenta?", ["Oesophagus", "Trachea", "Umbilical cord", "Fallopian tube"], "C"),
        ("What is cloning in biology?", ["Formation of genetically unrelated individuals only", "Fusion of two different species", "A type of digestion", "Producing genetically identical copies of an organism or cell"], "D"),
        ("Why is reproduction essential for a species?", ["It enables continuation of the species across generations", "It prevents growth", "It stops all genetic inheritance", "It eliminates the need for food"], "A"),
        ("Which of these is a form of asexual reproduction?", ["Fertilisation", "Binary fission", "Cross-pollination", "Fusion of gametes"], "B"),
    ],

    "Medium": [
        ("What is the correct sequence in human sexual reproduction?", ["Embryo, gametes, fertilisation, zygote", "Fertilisation, gametes, embryo, zygote", "Gamete formation, fertilisation, zygote formation, embryo development", "Birth, fertilisation, gamete formation, zygote"], "C"),
        ("What is the main difference between sexual and asexual reproduction?", ["Asexual reproduction always requires two parents", "Sexual reproduction never involves gametes", "Both always produce identical offspring", "Sexual reproduction involves gamete fusion, while asexual reproduction does not"], "D"),
        ("Why is the zygote important?", ["It is the first cell formed by fertilisation and can develop into an embryo", "It is a fully developed adult", "It is always an unfertilised ovum", "It is a type of reproductive organ"], "A"),
        ("Why do sperm cells have a flagellum?", ["To store nutrients for months", "To help them move toward the ovum", "To produce ova", "To form the placenta"], "B"),
        ("What is the role of the placenta during human pregnancy?", ["It produces sperm", "It digests food in the mother's stomach", "It facilitates exchange of nutrients, gases and wastes between maternal and foetal blood", "It directly mixes maternal and foetal blood completely"], "C"),
        ("Why is the uterus lining important during pregnancy?", ["It prevents all blood flow", "It produces sperm", "It digests the embryo", "It supports implantation and development of the placenta"], "D"),
        ("What is ovulation?", ["Release of an egg from an ovary", "Fusion of sperm and egg", "Development of a zygote into an embryo", "Birth of a baby"], "A"),
        ("Where does fertilisation most commonly occur in humans?", ["Stomach", "Fallopian tube", "Large intestine", "Urinary bladder"], "B"),
        ("Why do many aquatic animals release large numbers of eggs?", ["Every egg is guaranteed to survive", "Their eggs never need water", "Many eggs or offspring may not survive to adulthood", "Their offspring are all genetically identical"], "C"),
        ("What is one advantage of internal fertilisation?", ["It requires all eggs to float freely in water", "It prevents sperm from reaching the egg", "It eliminates the need for reproductive cells", "It protects gametes and increases the likelihood of fertilisation in many environments"], "D"),
        ("Why can external fertilisation be common in aquatic animals?", ["Water helps keep gametes from drying out and supports their encounter", "It requires a uterus in every species", "It occurs only in mammals", "It prevents the release of eggs"], "A"),
        ("What is the role of the testes beyond sperm production?", ["They produce ova", "They produce testosterone", "They store the embryo", "They form the placenta"], "B"),
        ("Which hormone is mainly associated with the development of many female secondary sexual characteristics?", ["Insulin", "Adrenaline", "Oestrogen", "Pepsin"], "C"),
        ("What is the main role of testosterone in human males?", ["Digest proteins", "Produce bile", "Filter blood", "Support sperm production and male secondary sexual characteristics"], "D"),
        ("What happens during implantation?", ["The developing blastocyst attaches to the uterine lining", "The sperm leaves the testes", "The ovum is released from the ovary", "The baby is delivered"], "A"),
        ("Why is cell division important after fertilisation?", ["It immediately produces a fully formed adult", "It increases the number of cells as the embryo develops", "It prevents tissue formation", "It stops genetic information from being copied"], "B"),
        ("What is metamorphosis in a butterfly?", ["A seed growing into a tree", "An egg changing directly into an adult without development", "Development through egg, larva, pupa and adult stages", "A fertilised egg becoming a plant"], "C"),
        ("Which statement about asexual reproduction is correct?", ["It always involves sperm and ova", "It always produces more genetic variation than sexual reproduction", "It requires fertilisation", "It can produce offspring from one parent without gamete fusion"], "D"),
        ("Why may asexual reproduction be advantageous in a stable environment?", ["It can allow rapid production of many offspring without finding a mate", "It always produces maximum genetic variation", "It requires two unrelated parents", "It prevents the population from increasing"], "A"),
        ("What is the main function of the scrotum?", ["Produce ova", "Help maintain the testes at a suitable temperature for sperm production", "Store urine", "Connect the uterus to the ovaries"], "B"),
        ("What is the function of the oviduct in many egg-laying animals?", ["Produce blood cells", "Digest food", "Transport the egg from the ovary and may be the site of fertilisation", "Produce sperm"], "C"),
        ("Why is genetic variation important in a population?", ["It guarantees every individual survives", "It prevents natural selection", "It eliminates inherited differences", "It can increase the chance that some individuals cope with environmental changes"], "D"),
        ("What is the function of the epididymis in human males?", ["Sperm mature and are stored there", "Ova are produced there", "The foetus develops there", "Urine is filtered there"], "A"),
        ("Which statement about identical twins is generally correct?", ["They always develop from two unrelated sperm cells", "They usually arise when one early embryo separates into two developing embryos", "They must have different genetic parents", "They always have different genetic material from fertilisation of separate eggs"], "B"),
        ("What is the function of the amniotic fluid?", ["Produce red blood cells", "Carry food into the mother's stomach", "Cushion the developing foetus and help protect it from mechanical shocks", "Prevent all foetal movement"], "C"),
        ("Why do mammals usually provide parental care to their young?", ["Their young are always independent at birth", "It eliminates all competition", "It means reproduction is unnecessary", "Care can improve offspring survival by providing protection and nourishment"], "D"),
        ("What is the role of the ovary in human reproduction?", ["Produce ova and hormones such as oestrogen and progesterone", "Produce sperm and testosterone", "Transport urine", "Exchange gases with the foetus"], "A"),
        ("Why does a human embryo need a reliable supply of oxygen and nutrients?", ["To avoid all cell division", "To support growth, metabolism and development", "To become a gamete again", "To stop the placenta functioning"], "B"),
        ("What is a larva?", ["A fully developed adult", "A reproductive hormone", "An immature developmental stage that differs from the adult in many animals", "A fertilised plant ovule"], "C"),
        ("Why does sexual reproduction generally produce genetically different offspring?", ["Every gamete has identical DNA in every case", "Only one chromosome is inherited", "It stops DNA recombination", "Gamete formation and fertilisation combine genetic material in new ways"], "D"),
    ],

    "Hard": [
        ("A species produces many offspring through external fertilisation, but few survive. Which explanation is most plausible?", ["Gametes and young are exposed to environmental hazards and predation", "External fertilisation guarantees survival", "All offspring are clones", "The species does not need water"], "A"),
        ("A mutation prevents sperm from developing a functional flagellum. Which process is most directly affected?", ["Production of ova", "Sperm movement toward the egg", "Implantation in the uterus", "Placenta formation"], "B"),
        ("Why can damage to the fallopian tubes reduce fertility?", ["The ovaries immediately stop existing", "The uterus becomes a digestive organ", "It can prevent sperm and egg from meeting or impede movement of the early embryo", "It guarantees multiple fertilisations"], "C"),
        ("Which event usually occurs immediately after fertilisation in human development?", ["Birth", "Placenta delivery", "Puberty", "The zygote begins cleavage divisions"], "D"),
        ("Why can sexual reproduction help a population adapt over generations?", ["Genetic variation can provide differences on which natural selection acts", "Every offspring is genetically identical", "It prevents mutations", "It removes inherited traits"], "A"),
        ("A hydra develops a small outgrowth that eventually separates and becomes independent. Which mechanism is demonstrated?", ["External fertilisation", "Budding", "Metamorphosis", "Internal fertilisation"], "B"),
        ("Why is binary fission classified as asexual reproduction?", ["It requires fertilisation between two gametes", "It produces a placenta", "One parent cell divides to produce daughter cells without gamete fusion", "It occurs only in mammals"], "C"),
        ("A fertilised egg fails to implant in the uterine lining. What is the most direct consequence?", ["The embryo develops normally in the stomach", "The placenta is guaranteed to form elsewhere", "The egg becomes a sperm cell", "Pregnancy is unlikely to continue normally"], "D"),
        ("Why is the placenta important but not a complete barrier to harmful substances?", ["Some substances can cross the placenta from maternal to foetal circulation", "It allows no exchange of any substance", "It directly mixes all maternal and foetal blood", "It replaces the foetal lungs permanently after birth"], "A"),
        ("A developing embryo has a genetic condition that affects early cell division. Why can this have broad consequences?", ["Cell division is needed only after birth", "Early divisions provide cells that form the embryo's tissues and organs", "The embryo does not contain DNA", "All organs are already fully formed before fertilisation"], "B"),
        ("Why can identical twins have some differences despite usually sharing nearly identical DNA?", ["They always develop from separate species", "They never experience different environments", "Developmental, epigenetic and environmental factors can contribute to differences", "Their DNA must be completely unrelated"], "C"),
        ("Which situation best illustrates natural selection acting on reproductive success?", ["Every organism leaves exactly the same number of offspring", "Inherited variation has no effect on survival", "Individuals choose mutations deliberately", "Individuals with heritable traits that improve reproductive success contribute more offspring over generations"], "D"),
        ("A male animal produces sperm normally, but a blockage prevents sperm from entering the reproductive tract. Which outcome is most likely?", ["Fertility may be reduced because sperm cannot reach the egg", "The animal begins producing ova", "Fertilisation occurs more easily in every case", "The placenta forms in the male"], "A"),
        ("Why does meiosis matter in sexual reproduction?", ["It doubles chromosome number in every gamete", "It reduces chromosome number in gametes and contributes to genetic variation", "It produces only body cells", "It prevents fertilisation"], "B"),
        ("If human gametes contained the normal diploid chromosome number, what could happen after fertilisation?", ["The zygote would have no chromosomes", "The chromosome number would always remain haploid", "The zygote could have an abnormal doubled chromosome number", "The embryo would automatically become a plant"], "C"),
        ("Why does the release of an egg from the ovary not itself guarantee pregnancy?", ["An egg never contains genetic material", "Pregnancy occurs before ovulation", "The uterus is not involved in reproduction", "Fertilisation, embryo development and implantation must also occur successfully"], "D"),
        ("A population reproduces only asexually for many generations in a changing environment. What is a potential disadvantage?", ["Limited genetic variation may reduce the population's ability to respond to new challenges", "Every offspring will be perfectly adapted", "Asexual reproduction always produces more variation than sexual reproduction", "Environmental changes cannot affect asexual populations"], "A"),
        ("Why does sperm production require a temperature slightly below normal core body temperature in humans?", ["Sperm cells require sunlight", "Spermatogenesis functions best within a suitable temperature range", "The testes must digest food", "The temperature determines the mother's chromosome number"], "B"),
        ("What is the significance of the acrosome in a human sperm cell?", ["It produces ova", "It stores the embryo", "It contains enzymes that help sperm penetrate the egg's outer coverings", "It produces the placenta"], "C"),
        ("Why is a sudden increase in chromosome number during fertilisation normally avoided?", ["It improves every organism's health", "It means DNA is unnecessary", "It prevents the zygote from having genes", "Meiosis reduces chromosome number so fertilisation can restore the species' usual diploid number"], "D"),
        ("A frog's eggs are fertilised outside the body in water. Which environmental change would most directly threaten successful fertilisation?", ["Conditions that dry out the eggs and gametes", "A suitable supply of water", "Healthy reproductive adults", "Synchronous release of gametes"], "A"),
        ("Why is the corpus luteum important in early pregnancy?", ["It produces sperm", "It secretes progesterone that helps maintain the uterine lining in early pregnancy", "It carries oxygen to the lungs", "It becomes the embryo's heart"], "B"),
        ("A developing foetus receives insufficient oxygen for an extended period. Why is this dangerous?", ["Oxygen is not used by developing tissues", "It increases all cellular energy production", "Insufficient oxygen can impair cellular energy production and organ development", "It prevents the need for nutrients"], "C"),
        ("Which statement best distinguishes an embryo from a gamete?", ["An embryo is always a single unfertilised sperm", "A gamete develops directly into a fully formed adult without fertilisation", "Both are always haploid reproductive cells", "An embryo develops after fertilisation, whereas a gamete is a reproductive cell"], "D"),
        ("Why can a population benefit from producing offspring at different times or in different conditions?", ["It may reduce the risk that all offspring encounter the same adverse conditions", "It guarantees that every offspring survives", "It eliminates all environmental variation", "It prevents reproduction"], "A"),
        ("A genetic mutation affects a hormone receptor involved in reproductive development. What is a possible consequence?", ["All body systems must stop immediately", "Reproductive development or fertility may be altered depending on the receptor's role", "Every offspring will be genetically identical", "The organism will begin photosynthesis"], "B"),
        ("Why does implantation normally occur after several early divisions of the zygote?", ["A zygote must become a sperm first", "Implantation occurs before fertilisation", "The early embryo develops into a stage capable of attaching to the uterine lining", "The ovary transforms directly into a foetus"], "C"),
        ("Which factor most directly explains why external fertilisation is often associated with aquatic environments?", ["Gametes must be stored in a placenta", "The process always requires internal organs", "Water prevents all predators from reaching eggs", "Water helps prevent gametes from drying out and facilitates their encounter"], "D"),
        ("Why can inbreeding increase the chance of harmful recessive conditions appearing in offspring?", ["Related individuals are more likely to share copies of the same inherited recessive allele", "It removes all recessive alleles from a population immediately", "It guarantees greater genetic diversity", "It prevents genes from being inherited"], "A"),
        ("A researcher compares offspring survival in two animal species with different levels of parental care. Why must other factors also be considered?", ["Parental care is the only factor that affects survival", "Predation, habitat, offspring number and other differences can also influence survival", "Survival can never be measured", "All species have identical reproductive strategies"], "B"),
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

        print("\nReproduction in Animals expansion completed!")
        print(f"Total new questions inserted: {inserted_total}")
        print("Easy: 30 questions")
        print("Medium: 30 questions")
        print("Hard: 30 questions")
        print("Other lessons and Social Science were not modified.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()