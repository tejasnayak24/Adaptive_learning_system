import sqlite3
from pathlib import Path

DATABASE_PATH = (
    Path(__file__).resolve().parent.parent
    / "adaptive_learning.db"
)

TARGET_QUESTIONS = 30

QUESTION_BANK = {
    "Easy": [
        ("What is an ecosystem?", "Living organisms interacting with each other and their environment", "Only animals in a forest", "Only plants in a garden", "Only non-living things", "A"),
        ("Which of these is a producer?", "Lion", "Green plant", "Mushroom", "Earthworm", "B"),
        ("Which organism is a primary consumer?", "Grass", "Algae", "Rabbit feeding on grass", "Fungus decomposing wood", "C"),
        ("Which organism breaks down dead organic matter?", "Tiger", "Deer", "Grass", "Decomposer", "D"),
        ("Which of these is an abiotic factor?", "Sunlight", "Grass", "Fish", "Bacteria", "A"),
        ("Which of these is a biotic factor?", "Temperature", "Tree", "Water", "Rock", "B"),
        ("What is a food chain?", "A group of rocks", "A water cycle only", "A sequence showing feeding relationships", "A list of habitats", "C"),
        ("What is the main source of energy for most ecosystems?", "Moonlight", "Soil", "Wind only", "Sun", "D"),
        ("Which organism is commonly a decomposer?", "Fungus", "Eagle", "Deer", "Grass", "A"),
        ("What is a habitat?", "An organism's food only", "The place where an organism lives", "A type of energy", "A group of predators", "B"),
        ("Which of these is a herbivore?", "Tiger", "Eagle", "Cow", "Snake", "C"),
        ("Which of these is a carnivore?", "Rabbit", "Deer", "Goat", "Lion", "D"),
        ("What do omnivores eat?", "Both plants and animals", "Only plants", "Only animals", "Only dead wood", "A"),
        ("What is biodiversity?", "The amount of rainfall only", "The variety of living organisms", "The number of rocks", "The temperature of a habitat", "B"),
        ("Which of these is an aquatic ecosystem?", "Desert", "Grassland", "Pond", "Mountain peak", "C"),
        ("Which of these is a terrestrial ecosystem?", "Ocean", "Pond", "River", "Forest", "D"),
        ("What is a population in ecology?", "Members of one species living in an area", "All the rocks in an area", "Only plants and animals together", "A single non-living object", "A"),
        ("What is a community in ecology?", "Only one organism", "Populations of different species living and interacting in an area", "Only water and soil", "A group of identical rocks", "B"),
        ("Which organisms usually occupy the first trophic level?", "Carnivores", "Secondary consumers", "Producers", "Top predators", "C"),
        ("What is a predator?", "An organism that makes its own food", "An organism that decomposes rocks", "An organism that eats only plants", "An organism that hunts and eats other organisms", "D"),
        ("What is prey?", "An organism hunted by a predator", "A plant that produces seeds only", "A non-living factor", "A type of soil", "A"),
        ("Which process allows green plants to convert light energy into chemical energy?", "Respiration only", "Photosynthesis", "Digestion", "Fermentation only", "B"),
        ("Which gas do plants absorb during photosynthesis?", "Oxygen", "Nitrogen", "Carbon dioxide", "Hydrogen", "C"),
        ("What is an ecological niche?", "Only the physical size of an organism", "A type of rock", "The total rainfall in a region", "An organism's role and way of living in its environment", "D"),
        ("Which ecosystem is characterized by very low rainfall?", "Desert", "Rainforest", "Wetland", "Coral reef", "A"),
        ("What is a limiting factor?", "A factor that always increases population", "A factor that restricts population growth", "An organism that cannot reproduce", "A type of food chain", "B"),
        ("What is mutualism?", "A relationship where both organisms are harmed", "A relationship where one organism hunts another", "A relationship in which both species benefit", "A relationship with no living organisms", "C"),
        ("What is competition in an ecosystem?", "The transfer of sunlight to soil", "The formation of rocks", "The breakdown of water into minerals", "Organisms competing for limited resources", "D"),
        ("What is an ecosystem service?", "A benefit people obtain from ecosystems", "A machine used to measure temperature", "A type of animal movement", "A laboratory chemical", "A"),
        ("Which of these can damage an ecosystem?", "Habitat restoration", "Pollution", "Wildlife protection", "Planting native trees", "B"),
    ],

    "Medium": [
        ("Why are producers important in most food chains?", "They consume all predators", "They remove every nutrient", "They convert energy into organic matter that supports consumers", "They eliminate decomposers", "C"),
        ("Why is less energy available at higher trophic levels?", "Energy is created at every level", "Consumers do not use energy", "All energy is stored permanently", "Energy is used in life processes and lost as heat", "D"),
        ("What is the role of decomposers in nutrient cycling?", "They break down dead matter and release nutrients", "They stop all nutrient movement", "They produce sunlight", "They prevent organic matter from decaying", "A"),
        ("What may happen if a top predator disappears from an ecosystem?", "All producers immediately die", "Some prey populations may increase and alter the food web", "Energy stops entering the ecosystem", "All decomposers become producers", "B"),
        ("What is a food web?", "A single organism", "A type of soil", "Interconnected food chains in an ecosystem", "A list of abiotic factors only", "C"),
        ("Why are food webs generally more realistic than simple food chains?", "Every organism eats exactly one species", "They exclude decomposers", "They contain no producers", "Organisms often have multiple food sources and predators", "D"),
        ("What is carrying capacity?", "The maximum population an environment can sustainably support under given conditions", "The number of species on Earth", "The total amount of sunlight in a year", "The weight of a single animal", "A"),
        ("What is ecological succession?", "The daily movement of animals", "The gradual change in community composition over time", "The transfer of heat between organisms", "The immediate disappearance of all species", "B"),
        ("What is primary succession?", "Recovery in an area with intact soil after disturbance", "Seasonal migration", "Community development on a surface where soil is absent or newly formed", "The daily change in temperature", "C"),
        ("What is a keystone species?", "A species that is always the most numerous", "A species that has no ecological effect", "Any species found only in a desert", "A species with a disproportionately large effect on its ecosystem", "D"),
        ("Why can excessive fertilizer runoff cause fish deaths?", "Nutrient enrichment can trigger algal blooms and oxygen depletion", "It always increases dissolved oxygen", "It removes all algae", "It converts fish into plants", "A"),
        ("What is biomagnification?", "The decrease of all pollutants at higher trophic levels", "The increase in concentration of certain persistent substances at higher trophic levels", "The movement of water into soil", "The growth of plant roots", "B"),
        ("What is eutrophication?", "The complete absence of nutrients in soil", "The freezing of a lake", "Excessive nutrient enrichment that can cause algal blooms and oxygen depletion", "The migration of fish to oceans", "C"),
        ("How does nitrogen fixation help ecosystems?", "It removes every form of nitrogen", "It turns nitrogen into sunlight", "It stops plant growth", "It converts atmospheric nitrogen into biologically usable forms", "D"),
        ("What is a symbiotic relationship?", "A close, sustained interaction between different species", "A relationship only between rocks", "A type of weather forecast", "A process that excludes all microorganisms", "A"),
        ("What is parasitism?", "Both species always benefit equally", "One organism benefits while the host is harmed", "Neither organism is affected in any way", "Both organisms are always killed immediately", "B"),
        ("What is commensalism?", "Both species are harmed", "One species always kills the other", "One species benefits while the other is neither significantly helped nor harmed", "Both species receive identical benefits", "C"),
        ("Why are wetlands ecologically important?", "They cannot support wildlife", "They prevent all water movement", "They contain no nutrients", "They can filter water, store floodwater, and provide habitat", "D"),
        ("How can deforestation affect the carbon cycle?", "It can reduce carbon storage and release stored carbon", "It eliminates carbon dioxide from the atmosphere completely", "It stops all decomposition", "It prevents all plant respiration", "A"),
        ("What is an invasive species?", "A native species that never reproduces", "A non-native species that spreads and causes harm", "Any endangered native animal", "A species that exists only in fossils", "B"),
        ("What is habitat fragmentation?", "The creation of one continuous habitat", "The removal of every abiotic factor", "The division of a habitat into smaller, separated patches", "The conversion of sunlight into food", "C"),
        ("Why is genetic diversity important within a population?", "It prevents every mutation", "It makes all organisms identical", "It removes natural selection", "It can improve the population's ability to respond to environmental change", "D"),
        ("What is an ecological pyramid of energy?", "A diagram showing energy available at successive trophic levels", "A map of mountain heights", "A diagram of rainfall only", "A chart showing only the number of rocks", "A"),
        ("Why can some food chains contain only a few trophic levels?", "Energy increases without limit", "Energy available generally decreases at each transfer", "Predators never need energy", "Producers do not absorb sunlight", "B"),
        ("What is a detritivore?", "An organism that produces sunlight", "An organism that eats only living predators", "An organism that feeds on dead organic material or detritus", "An organism that consumes only minerals", "C"),
        ("How can overfishing affect a marine food web?", "It always increases every fish population", "It eliminates all ocean currents", "It prevents all plankton growth", "It can disrupt predator-prey relationships and reduce populations", "D"),
        ("What is ecological resilience?", "The ability of an ecosystem to recover from disturbance or maintain function", "The inability of any species to reproduce", "The total absence of environmental change", "The number of rocks in a river", "A"),
        ("Why do decomposers matter in a forest ecosystem?", "They stop nutrients from returning to the soil", "They recycle nutrients from dead organisms and waste", "They replace all producers", "They prevent all microbial activity", "B"),
        ("What is the main difference between a habitat and a niche?", "Both mean exactly the same thing in every context", "A habitat describes an organism's diet only", "Habitat is where it lives; niche describes its ecological role and resource use", "A niche is always a physical building", "C"),
        ("How can climate change affect biodiversity?", "It cannot affect species distributions", "It always increases every population", "It prevents habitat change", "It can alter habitats, seasonal patterns, and species distributions", "D"),
    ],

    "Hard": [
        ("A lake receives excess nitrogen and phosphorus. Which sequence is most likely?", "Algal bloom, decomposition, reduced dissolved oxygen", "Immediate oxygen increase forever", "Complete removal of nutrients", "Conversion of fish into producers", "A"),
        ("Why can the removal of a keystone predator trigger a trophic cascade?", "Predators do not influence prey populations", "Changes in predator pressure can affect prey, vegetation, and other trophic levels", "Energy is created from nothing", "Decomposers stop requiring nutrients", "B"),
        ("A pesticide persists in the environment and accumulates in animal tissues. Which organisms may experience the highest concentrations through biomagnification?", "Primary producers in every case", "Organisms with no feeding relationships", "Predators at high trophic levels", "Only decomposers in all ecosystems", "C"),
        ("Why can a small isolated population be at greater risk of extinction?", "It always has greater genetic diversity", "It is unaffected by random events", "It cannot experience disease", "Genetic drift, inbreeding, and environmental events can have larger effects", "D"),
        ("What is the likely effect of losing a major pollinator from an ecosystem?", "Reproduction of some flowering plants may decline", "All plants immediately become carnivores", "The water cycle stops", "Every decomposer disappears", "A"),
        ("How can a positive feedback loop amplify ecological change?", "It always restores the original state", "An initial change triggers effects that reinforce that change", "It prevents any system response", "It removes every energy input", "B"),
        ("Why can nitrogen become a limiting nutrient in some terrestrial ecosystems?", "Nitrogen is never required by organisms", "Plants use only atmospheric nitrogen directly in every case", "Usable nitrogen may be scarce relative to biological demand", "Nitrogen cannot enter soil", "C"),
        ("What is the significance of mycorrhizal associations for many plants?", "They prevent roots from absorbing water", "They eliminate all soil minerals", "They convert plants into animals", "Fungal partners can improve nutrient and water uptake", "D"),
        ("A forest is divided by roads into small patches. Which effect is a likely concern?", "Reduced connectivity and increased edge effects", "Guaranteed increase in every species", "Complete prevention of invasive species", "Elimination of all human impacts", "A"),
        ("Why might a species with a narrow ecological niche be vulnerable to environmental change?", "It can use every possible resource", "It may depend on a limited range of conditions or resources", "It has no habitat requirements", "It is always an invasive species", "B"),
        ("What is the main ecological concern associated with the loss of apex predators?", "Producers always disappear immediately", "Primary productivity must become zero", "Trophic interactions can change and some prey populations may increase", "Nutrient cycling always stops completely", "C"),
        ("How does carbon sequestration by forests help regulate climate?", "It converts all atmospheric nitrogen into oxygen", "It prevents all respiration", "It removes all greenhouse gases permanently", "It stores carbon in biomass and soils", "D"),
        ("Why may biodiversity increase ecosystem stability in some circumstances?", "Different species can respond differently to disturbances and support ecosystem functions", "All species perform identical roles", "Biodiversity prevents every disturbance", "Species diversity eliminates climate variation", "A"),
        ("What is the main difference between primary and secondary succession?", "Secondary succession never involves plants", "Primary succession begins where developed soil is absent, while secondary succession occurs where soil remains", "Primary succession always takes one day", "Secondary succession cannot follow a disturbance", "B"),
        ("Why can the introduction of a non-native predator be especially harmful on an island?", "Island species are always predators", "Islands contain no native organisms", "Native prey may lack effective defenses against the introduced predator", "Introduced predators never reproduce", "C"),
        ("What does the ten-percent rule approximately describe in many simplified energy pyramids?", "Exactly 10% of all matter disappears", "Exactly 10% of organisms survive", "All energy transfers with 100% efficiency", "Roughly 10% of energy at one trophic level may transfer to the next", "D"),
        ("Why is energy flow through an ecosystem different from nutrient cycling?", "Energy flows through trophic levels and dissipates as heat, while nutrients can be reused", "Energy cycles indefinitely without loss", "Nutrients cannot move between organisms", "Energy is created by decomposers", "A"),
        ("A drought reduces plant biomass substantially. What is a likely immediate consequence for herbivores?", "Food availability increases", "Food availability decreases and competition may increase", "All predators become producers", "Water becomes an energy source", "B"),
        ("Why can ecological restoration fail if only vegetation is replanted?", "Plants never interact with animals", "Soil conditions are irrelevant", "Other limiting factors, species interactions, and habitat conditions may remain unsuitable", "Restoration always removes biodiversity", "C"),
        ("What is the likely effect of excessive groundwater extraction on a wetland?", "The wetland must become deeper", "It always increases native biodiversity", "It prevents drought", "Reduced water availability may alter habitat and species composition", "D"),
        ("How can ocean acidification affect organisms that build calcium carbonate shells?", "It can make shell formation more difficult under some conditions", "It always increases shell thickness", "It converts calcium into sunlight", "It has no possible biological effect", "A"),
        ("Why can coral bleaching threaten reef biodiversity?", "It always increases coral growth", "Stress can cause corals to lose symbiotic algae and reduce their energy supply", "It converts corals into plants", "It stops all ocean currents", "B"),
        ("What is the main role of ecological corridors between habitat patches?", "Separate all populations permanently", "Increase habitat isolation", "Facilitate movement and gene flow between populations", "Prevent all animal migration", "C"),
        ("Why may a population overshoot its carrying capacity?", "Carrying capacity never changes", "Organisms cannot reproduce", "Resources are always unlimited", "Population growth may continue temporarily before resource limits affect survival or reproduction", "D"),
        ("What is a likely consequence of disrupting a major decomposer community?", "Slower decomposition and altered nutrient recycling", "Immediate production of unlimited nutrients", "Permanent elimination of gravity", "Automatic increase in soil fertility in every case", "A"),
        ("How can biological control help manage an invasive pest?", "By releasing unlimited pesticides into every habitat", "By using natural enemies while carefully evaluating ecological risks", "By removing all native species", "By eliminating every decomposer", "B"),
        ("Why is a simple food chain insufficient to describe many ecosystems?", "Every organism has exactly one food source", "Energy does not move through ecosystems", "Many organisms participate in multiple feeding relationships", "Producers never interact with consumers", "C"),
        ("Which measurement would most directly indicate oxygen depletion during eutrophication?", "Increased soil hardness", "Reduced wind speed", "Increased rock density", "Low dissolved oxygen concentration in the water", "D"),
        ("Why can conservation plans benefit from maintaining genetic connectivity between populations?", "Gene flow can help maintain genetic diversity and reduce inbreeding", "Gene flow always causes extinction", "It prevents every mutation", "It makes all species genetically identical", "A"),
        ("What is an important limitation of using species richness alone to measure biodiversity?", "Species richness always measures genetic variation perfectly", "It does not show differences in species abundance or genetic diversity", "It measures only rainfall", "It always identifies ecosystem function exactly", "B"),
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
            ("Ecosystems",),
        ).fetchone()

        if lesson is None:
            raise RuntimeError(
                "Ecosystems lesson was not found in the database."
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
                        f"Missing {difficulty} quiz for Ecosystems."
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
                            f"Skipping duplicate ({difficulty}): {question}"
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

        print("\nEcosystems expansion completed!")
        print(f"Total new questions inserted: {total_inserted}")
        print("Easy: 30 questions")
        print("Medium: 30 questions")
        print("Hard: 30 questions")
        print("Other lessons and Social Science were not modified.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()