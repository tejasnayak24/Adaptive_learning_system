import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

LESSON_TITLE = "Plant Reproduction"
TARGET_QUESTIONS = 30

QUESTION_BANK = {
    "Easy": [
        ("What is reproduction in plants?", ["The process of producing new plants", "The process of absorbing water", "The process of making soil", "The process of losing leaves"], "A"),
        ("Which part of a flowering plant usually produces seeds?", ["Root", "Flower", "Stem", "Leaf"], "B"),
        ("What is pollination?", ["The growth of roots", "The formation of fruits", "The transfer of pollen from anther to stigma", "The absorption of water"], "C"),
        ("Which part of a flower produces pollen?", ["Stigma", "Ovary", "Petal", "Anther"], "D"),
        ("Which part of a flower receives pollen?", ["Stigma", "Anther", "Sepal", "Filament"], "A"),
        ("What develops into a fruit after fertilisation in a flowering plant?", ["Anther", "Ovary", "Stigma", "Petal"], "B"),
        ("What does an ovule usually develop into after fertilisation?", ["Leaf", "Root", "Seed", "Stem"], "C"),
        ("Which method of reproduction involves only one parent?", ["Cross-pollination", "Fertilisation", "Sexual reproduction", "Asexual reproduction"], "D"),
        ("Which of these is an example of vegetative propagation?", ["Growing a potato plant from a tuber", "Growing a plant from a seed", "Pollination by bees", "Formation of pollen"], "A"),
        ("Which organism commonly helps pollinate flowers?", ["Earthworm", "Bee", "Fish", "Frog"], "B"),
        ("What is the main function of petals in many flowers?", ["Absorb water from soil", "Anchor the plant", "Attract pollinators", "Produce roots"], "C"),
        ("Which flower part contains the ovules?", ["Petal", "Anther", "Filament", "Ovary"], "D"),
        ("What is fertilisation in flowering plants?", ["Fusion of male and female gametes", "Transfer of water to leaves", "Release of pollen into the air", "Growth of a stem"], "A"),
        ("Which of these plants can commonly be propagated using stem cuttings?", ["Mango only", "Rose", "Rice only", "Wheat only"], "B"),
        ("Which structure protects a flower when it is a bud?", ["Stigma", "Anther", "Sepal", "Ovary"], "C"),
        ("What is seed dispersal?", ["Production of chlorophyll", "Absorption of minerals", "Formation of pollen", "Movement of seeds away from the parent plant"], "D"),
        ("Which of these can disperse seeds?", ["Wind", "Only darkness", "Only soil", "Chlorophyll"], "A"),
        ("Which plant structure can grow into a new plant in vegetative propagation?", ["Only a flower petal", "Stem", "Only pollen grains", "Only fruit juice"], "B"),
        ("What is germination?", ["The transfer of pollen", "The formation of a fruit", "The beginning of growth of a seed", "The falling of leaves"], "C"),
        ("Which condition is generally needed for most seeds to germinate?", ["No water at all", "Complete absence of oxygen", "Extreme heat", "Suitable moisture"], "D"),
        ("What is the male reproductive part of a typical flower called?", ["Stamen", "Pistil", "Sepal", "Petal"], "A"),
        ("What is the female reproductive part of a typical flower called?", ["Stamen", "Pistil", "Filament", "Anther"], "B"),
        ("Which of these is a form of asexual reproduction in plants?", ["Seed formation after fertilisation", "Cross-pollination", "Vegetative propagation", "Fusion of gametes"], "C"),
        ("Which plant commonly reproduces through runners?", ["Mango", "Coconut", "Pea", "Strawberry"], "D"),
        ("Which of these is a seed-bearing structure in flowering plants?", ["Fruit", "Root hair", "Stem node only", "Leaf vein"], "A"),
        ("What is self-pollination?", ["Pollen transfer between unrelated plant species", "Pollen transfer to the stigma of the same flower or another flower on the same plant", "Seed dispersal by wind", "Growth from a cutting"], "B"),
        ("Which of these is a natural agent of seed dispersal?", ["Chlorophyll", "Stigma", "Water", "Anther"], "C"),
        ("What is the main role of seeds?", ["Attract all pollinators", "Absorb sunlight for the parent plant", "Produce pollen immediately", "Protect and contain the young plant embryo"], "D"),
        ("Which plant can reproduce using a bulb?", ["Onion", "Mango", "Pea", "Sunflower"], "A"),
        ("Why is reproduction important for plant species?", ["It prevents all growth", "It helps produce new individuals and continue the species", "It stops seed formation", "It removes the need for nutrients"], "B"),
    ],

    "Medium": [
        ("What is the correct sequence in sexual reproduction of a flowering plant?", ["Seed dispersal, pollination, leaf formation, fertilisation", "Germination, fruit formation, pollination, fertilisation", "Pollination, fertilisation, seed and fruit development", "Root growth, seed dispersal, pollination, pollen formation"], "C"),
        ("How does cross-pollination differ from self-pollination?", ["It occurs only in roots", "It never involves pollen", "It always produces identical offspring", "It transfers pollen between flowers on different plants of the same species"], "D"),
        ("Why can cross-pollination increase genetic variation?", ["It can combine genetic material from different parent plants", "It eliminates all inherited differences", "It prevents fertilisation", "It always produces clones"], "A"),
        ("Why are brightly coloured petals useful to many flowering plants?", ["They absorb all soil minerals", "They attract animal pollinators", "They directly form roots", "They prevent seeds from germinating"], "B"),
        ("What is the role of the pollen tube?", ["It carries water from roots to leaves", "It forms the fruit skin", "It allows the male gamete to reach the ovule", "It disperses seeds by wind"], "C"),
        ("Why do some seeds have hooks or barbs?", ["To absorb sunlight", "To produce pollen", "To attract minerals", "To attach to animal fur and aid dispersal"], "D"),
        ("Which feature is commonly associated with wind-pollinated flowers?", ["Light pollen and exposed anthers", "Large nectar stores in every flower", "Bright petals in every case", "Heavy pollen that sticks together"], "A"),
        ("Why might a farmer use vegetative propagation to grow a crop?", ["It always creates maximum genetic variation", "It can produce plants with characteristics similar to the parent", "It requires fertilisation for every cutting", "It prevents plants from growing roots"], "B"),
        ("Which statement about potato reproduction is correct?", ["Potatoes reproduce only through flowers", "A potato tuber is a seed", "A tuber with suitable buds can grow into a new plant", "Potato plants cannot reproduce sexually"], "C"),
        ("Why is water important during seed germination?", ["It replaces the embryo", "It makes sunlight unnecessary for the mature plant", "It prevents enzymes from working", "It helps activate metabolic processes and soften the seed coat"], "D"),
        ("Which condition is generally needed by most seeds for germination?", ["Suitable water, oxygen and temperature", "Continuous bright light for every species", "Fertiliser before water", "Complete absence of oxygen"], "A"),
        ("What is one possible disadvantage of producing plants only through asexual reproduction?", ["It always takes longer than growing from seeds", "Offspring generally have less genetic variation", "It always requires pollinators", "It prevents the parent from passing on traits"], "B"),
        ("How does fruit formation benefit many flowering plants?", ["It prevents seed development", "It stops all seed dispersal", "It can protect seeds and help with their dispersal", "It replaces the need for fertilisation"], "C"),
        ("Which part of the flower contains the stigma, style and ovary?", ["Stamen", "Sepal", "Petal", "Pistil"], "D"),
        ("What happens to the ovary in many flowering plants after fertilisation?", ["It develops into the fruit", "It becomes pollen", "It becomes the root system", "It disappears in every species"], "A"),
        ("Why is seed dispersal beneficial to plants?", ["It guarantees every seed will germinate", "It reduces competition with the parent plant and nearby seedlings", "It prevents plants from reaching sunlight", "It removes the embryo from every seed"], "B"),
        ("Which example correctly matches a plant with a vegetative structure?", ["Mango — pollen grain", "Pea — root hair", "Onion — bulb", "Sunflower — stigma"], "C"),
        ("How does a fern commonly reproduce?", ["By producing fruits", "By making flowers", "By forming seeds inside ovaries", "By producing spores"], "D"),
        ("Why are spores useful for reproduction in ferns and mosses?", ["They can develop into new organisms under suitable conditions", "They are always fertilised seeds", "They contain mature fruits", "They are produced only by flowering plants"], "A"),
        ("What is the main function of the ovule before fertilisation?", ["To attract insects", "To contain the female gamete and associated tissues", "To produce the pollen tube", "To form the petal"], "B"),
        ("What is the difference between pollination and fertilisation?", ["They are exactly the same process", "Pollination occurs only after fruit formation", "Pollination transfers pollen, while fertilisation involves fusion of gametes", "Fertilisation is the movement of seeds by wind"], "C"),
        ("Why might insect-pollinated flowers produce nectar?", ["To stop insects visiting", "To produce seeds without pollen", "To prevent pollen transfer", "To provide a reward that attracts pollinators"], "D"),
        ("What is a cutting in horticulture?", ["A plant part used to grow a new plant", "A type of pollen grain", "A seed dispersal agent", "A fertilised ovule"], "A"),
        ("Which process usually occurs before fertilisation in a flowering plant?", ["Fruit ripening", "Pollination", "Seed dispersal", "Seed germination"], "B"),
        ("Why are many wind-dispersed seeds small and light?", ["To stop them moving", "To make them unable to germinate", "To help air currents carry them", "To increase the weight of the parent plant"], "C"),
        ("Which statement about runners is correct?", ["They are female reproductive organs", "They are pollen-producing structures", "They are fruits containing seeds", "They are horizontal stems that can form new plants"], "D"),
        ("Why are grafting and budding used in agriculture?", ["To combine desirable plant characteristics or propagate selected varieties", "To remove all inherited traits", "To stop plant growth", "To make pollination impossible"], "A"),
        ("What happens when pollen from one flower reaches a compatible stigma?", ["The seed immediately disperses", "The pollen may germinate and form a pollen tube", "The root stops absorbing water", "The ovary becomes a leaf immediately"], "B"),
        ("Which factor is most likely to reduce successful pollination in a crop that depends on bees?", ["Adequate water supply", "Healthy flowers", "A major decline in pollinator visits", "Suitable temperatures"], "C"),
        ("Why can seed dormancy be beneficial?", ["It prevents every seed from ever growing", "It removes the embryo", "It means seeds need no suitable conditions", "It allows seeds to delay germination until conditions are favourable"], "D"),
    ],

    "Hard": [
        ("A flower is covered with a bag that prevents pollen from reaching its stigma. It receives no pollen from another flower. What is the most likely result if it is self-incompatible?", ["Fertilisation and seed formation will be prevented or greatly reduced", "It will produce seeds without any gametes", "Its ovules will become pollen grains", "Its petals will become roots"], "A"),
        ("A gardener wants many genetically similar rose plants quickly. Which method is most suitable?", ["Cross-pollinating roses and collecting seeds only", "Taking healthy stem cuttings from a desired parent plant", "Dispersing pollen into water", "Removing all buds from the parent plant"], "B"),
        ("Two plants of the same species grow from seeds produced by cross-pollination. Why might they differ genetically?", ["All seeds contain identical DNA", "Pollination removes all inherited variation", "Sexual reproduction combines genetic material from two parents", "Their roots create new genes from soil minerals"], "C"),
        ("A student removes the anthers from a flower before they release pollen, then transfers pollen from another plant of the same species to its stigma. What is the purpose?", ["To prevent the stigma from receiving pollen", "To ensure the flower reproduces through roots", "To eliminate the female gamete", "To control the pollen source and encourage cross-pollination"], "D"),
        ("A plant species has flowers with dull petals, abundant pollen and exposed feathery stigmas. Which pollination method is most likely?", ["Wind pollination", "Pollination only by large mammals", "Pollination only underwater", "Self-fertilisation without pollen transfer"], "A"),
        ("A seed has a fleshy fruit around it. Which ecological advantage may this provide?", ["It stops all animals from eating the fruit", "Animals may eat the fruit and disperse seeds elsewhere", "It prevents seed development", "It means the seed does not contain an embryo"], "B"),
        ("A farmer repeatedly grows a crop from cuttings of one plant. What is a likely consequence?", ["Every plant must have a different genotype", "The crop cannot grow roots", "Plants will generally retain the parent's genotype, except for mutations", "Each cutting requires pollination before rooting"], "C"),
        ("A seed has enough water and oxygen but is kept at a temperature too low for its species. What is likely to happen?", ["It will always germinate immediately", "It will produce a mature fruit first", "It will no longer contain an embryo", "Germination may be delayed or prevented until temperature becomes suitable"], "D"),
        ("A researcher finds that pollen grains land on the stigma, but no seeds form. Which explanation is plausible?", ["Pollination occurred, but fertilisation may have failed", "Pollination and fertilisation are identical", "The ovules must already have become fruits", "Seed dispersal always occurs before pollen reaches the stigma"], "A"),
        ("Why can producing crops through seeds be advantageous compared with cloning by cuttings in some breeding programmes?", ["Seeds always produce exact genetic copies", "Sexual reproduction can generate variation for selection", "Seed production never requires fertilisation", "Seeds cannot carry inherited traits"], "B"),
        ("A plant produces flowers but few fruits. Pollinator visits are rare, and pollen is not reaching the stigma. Which intervention is most directly relevant?", ["Reduce all light exposure", "Remove all healthy leaves", "Improve pollination opportunities, for example by supporting pollinators", "Prevent the plant from absorbing water"], "C"),
        ("Which statement best explains why asexual reproduction is useful for preserving a desirable crop variety?", ["It always creates new combinations of genes", "It requires two compatible gametes", "It prevents all inheritance", "It can produce offspring that closely resemble the selected parent"], "D"),
        ("A wind-dispersed seed has a broad, lightweight wing. How does this adaptation improve dispersal?", ["It increases the time the seed can remain airborne", "It guarantees that the seed will germinate", "It directly provides the seed with nutrients", "It eliminates the need for a suitable habitat"], "A"),
        ("A seed dispersal experiment releases equal numbers of winged and unwinged seeds in moving air. What should be controlled for a fair comparison?", ["The colour of the researcher’s notebook", "Release height and wind conditions", "The number of windows in another room", "The time of year in a different experiment only"], "B"),
        ("A plant species produces seeds that germinate only after a period of cold conditions. What is a likely advantage of this requirement?", ["It ensures seeds never germinate", "It makes fertilisation unnecessary", "It can prevent germination at an unsuitable time and help synchronize growth with favourable seasons", "It means the seeds cannot survive winter"], "C"),
        ("Why can a plant produced by grafting have shoots with one variety's fruit characteristics and roots from another variety?", ["The rootstock changes the genetic code of every shoot cell", "The grafted plant has no living tissues", "Pollen from the rootstock becomes the fruit", "The graft joins tissues from two plants while the scion retains its own genetic identity"], "D"),
        ("A flowering plant has functional anthers but its stigma is not receptive when pollen is released. How could this affect reproduction?", ["It may reduce successful self-pollination and encourage reliance on other timing or pollen sources", "It guarantees that all ovules are fertilised", "It means the plant produces no pollen", "It converts pollen into seeds without fertilisation"], "A"),
        ("Which observation provides the strongest evidence that a plant reproduced vegetatively?", ["A flower produced pollen", "A new shoot grew from a potato tuber bud", "A seed formed after fertilisation", "A bee visited a flower"], "B"),
        ("A species has separate male and female flowers on different individual plants. What is required for seed production?", ["Every flower must pollinate itself", "The female plant must produce pollen in its own flowers", "Pollen must be transferred from a male plant to a female flower of the same species", "Seeds must form before pollination"], "C"),
        ("A student claims that all plants reproduce through flowers and seeds. Which counterexample best disproves the claim?", ["Mango", "Pea", "Sunflower", "Fern, which reproduces using spores"], "D"),
        ("A fruit is eaten by a bird, and viable seeds are later deposited far from the parent plant. Which process is demonstrated?", ["Animal-mediated seed dispersal", "Pollination by wind", "Vegetative propagation by runners", "Fertilisation inside the bird"], "A"),
        ("Why might a species produce many seeds even though only a small fraction survive to adulthood?", ["Every seed is guaranteed to grow", "Producing many seeds can increase the chance that some offspring survive and reproduce", "Seeds do not need suitable habitats", "The parent plant has no reproductive limits"], "B"),
        ("A researcher compares seed germination in four groups, changing both temperature and water availability at the same time. What is the main weakness?", ["The seeds cannot contain embryos", "The experiment cannot use observations", "The effects of temperature and water cannot be separated clearly", "All groups will necessarily have identical results"], "C"),
        ("Why might a plant species benefit from both sexual reproduction and vegetative propagation?", ["Both methods always produce genetically identical offspring", "Neither method can support survival", "Sexual reproduction never produces seeds", "Sexual reproduction generates variation, while vegetative propagation can rapidly multiply successful genotypes"], "D"),
        ("A pollen grain lands on the stigma of a flower from a different species. Why may fertilisation fail?", ["The pollen may be incompatible and unable to complete the required reproductive process", "Every pollen grain fertilises every plant species", "The stigma always converts pollen into fruit", "The ovules are always absent from flowering plants"], "A"),
        ("A farmer selects a plant with high fruit yield and propagates it through cuttings. What is the primary reason for this choice?", ["To guarantee new genetic combinations in every offspring", "To preserve desirable characteristics of the selected plant", "To prevent the plant from producing leaves", "To ensure that every cutting forms a seed"], "B"),
        ("A plant's flowers are pollinated successfully, but a severe frost damages developing ovules. What is the likely consequence?", ["Pollination will occur retroactively", "All ovules will become pollen", "Seed development may be reduced even though pollination occurred", "The plant will switch to animal pollination immediately"], "C"),
        ("Which sequence correctly describes the main stages leading from pollination to a seed in a typical flowering plant?", ["Seed dispersal, germination, pollen formation, pollination", "Fruit ripening, leaf fall, pollination, root formation", "Root growth, photosynthesis, seed dispersal, pollen production", "Pollen reaches stigma, pollen tube grows, fertilisation occurs, ovule develops into a seed"], "D"),
        ("Why is genetic diversity important to plant populations facing environmental change?", ["It increases the chance that some individuals possess traits suited to new conditions", "It guarantees every individual survives", "It prevents all mutations", "It makes natural selection impossible"], "A"),
        ("A student compares two plant propagation methods and wants to determine which produces roots faster. What is the best experimental approach?", ["Use different plant species and different environmental conditions for every sample", "Use similar cuttings, standardize conditions, measure root development, and repeat trials", "Measure only the colour of the pots", "Change water, temperature and light differently for each cutting"], "B"),
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

        print("\nPlant Reproduction expansion completed!")
        print(f"Total new questions inserted: {inserted_total}")
        print("Easy: 30 questions")
        print("Medium: 30 questions")
        print("Hard: 30 questions")
        print("Other lessons and Social Science were not modified.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()