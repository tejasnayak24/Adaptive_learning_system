
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

LESSON_TITLE = "Adaptations in Living Organisms"
TARGET_QUESTIONS = 30

QUESTION_BANK = {
    "Easy": [
        ("What is an adaptation?", ["A feature that helps an organism survive or reproduce in its environment", "A type of rock", "A weather instrument", "A method of cooking"], "A"),
        ("Which animal is well adapted to living in a desert?", ["Polar bear", "Camel", "Penguin", "Frog"], "B"),
        ("Why do many desert plants have spines instead of broad leaves?", ["To absorb more salt", "To attract large fish", "To reduce water loss", "To prevent photosynthesis"], "C"),
        ("Which feature helps a polar bear stay warm?", ["Thin skin with no insulation", "Large exposed ears only", "Brightly coloured feathers", "Thick fur and a layer of body fat"], "D"),
        ("Which animal has webbed feet that help it swim?", ["Duck", "Camel", "Lion", "Giraffe"], "A"),
        ("What is camouflage?", ["Producing food from sunlight", "Blending with the surroundings", "Moving to another planet", "Changing rocks into soil"], "B"),
        ("Which plant is adapted to store water in dry environments?", ["Water lily", "Moss", "Cactus", "Rice plant"], "C"),
        ("Why do fish have gills?", ["To walk on land", "To produce flowers", "To store food", "To extract dissolved oxygen from water"], "D"),
        ("Which body feature helps a duck move through water?", ["Webbed feet", "Hooves", "A long neck only", "Sharp claws for climbing"], "A"),
        ("What is migration?", ["An organism making its own food", "Seasonal movement from one region to another", "A plant losing all its roots", "The formation of clouds"], "B"),
        ("Which animal has a long neck that helps it reach leaves high in trees?", ["Frog", "Penguin", "Giraffe", "Shark"], "C"),
        ("Which adaptation helps a fish move efficiently through water?", ["Broad, flat feet for walking", "Feathers for flight", "Thick fur for snow", "A streamlined body"], "D"),
        ("Why do many nocturnal animals have good night vision?", ["They are active during low-light conditions", "They live only underwater", "They never need food", "They produce sunlight"], "A"),
        ("Which animal is known for seasonal migration over long distances?", ["Earthworm only", "Many migratory birds", "Domestic cats only", "Garden snails only"], "B"),
        ("What helps a polar bear's paws move across snow and ice?", ["Tiny wings", "Gills", "Large paws that help distribute weight and provide traction", "Webbed fish fins"], "C"),
        ("Which adaptation helps a bird fly?", ["Heavy stones attached to its body", "Gills for breathing underwater", "A body without muscles", "Wings and feathers"], "D"),
        ("What is a habitat?", ["The natural place where an organism lives", "A type of food chain only", "A body organ", "A kind of mineral"], "A"),
        ("Which plant adaptation helps mangroves cope with waterlogged, oxygen-poor soil?", ["Leaves that cannot exchange gases", "Specialised roots that help with gas exchange", "Roots that never touch soil", "Complete absence of roots"], "B"),
        ("Why do some animals have thick fur in cold regions?", ["To increase heat loss", "To prevent breathing", "To provide insulation and reduce heat loss", "To help them photosynthesise"], "C"),
        ("Which feature helps a woodpecker obtain insects from tree bark?", ["Webbed feet for swimming", "A flat bill for filtering water", "Gills", "A strong, pointed beak"], "D"),
        ("Which animal is commonly adapted to life in water with fins?", ["Fish", "Camel", "Eagle", "Kangaroo"], "A"),
        ("What is hibernation?", ["Daily hunting", "A period of greatly reduced activity during unfavourable conditions", "The production of seeds", "Movement caused by wind"], "B"),
        ("Which feature helps a cactus reduce water loss?", ["Large, thin leaves", "Soft feathers", "Leaves modified into spines", "Gills"], "C"),
        ("Why do some animals have large ears in hot environments?", ["To stop all sound", "To make their bodies heavier", "To help them fly", "Large ears can help release body heat in some species"], "D"),
        ("Which animal is adapted for jumping with powerful hind legs?", ["Kangaroo", "Shark", "Snail", "Oyster"], "A"),
        ("What is an aquatic habitat?", ["A dry desert", "A habitat in water", "A mountain cave only", "A treeless grassland only"], "B"),
        ("Which animal uses blubber as insulation in cold marine environments?", ["House sparrow", "Garden lizard", "Seal", "Butterfly"], "C"),
        ("Why might a leaf have a waxy coating?", ["To absorb every drop of water from the air", "To make the plant move", "To replace its roots", "To help reduce water loss"], "D"),
        ("What is a structural adaptation?", ["A physical feature of an organism that helps it function in its environment", "A seasonal change in weather", "A type of soil pollution", "A method of measuring temperature"], "A"),
        ("Why do some animals have protective colouring?", ["To make food disappear", "To avoid detection by predators or prey", "To stop all movement", "To eliminate the need for shelter"], "B"),
    ],

    "Medium": [
        ("How does a camel's ability to tolerate dehydration help it survive in deserts?", ["It allows it to live without any water forever", "It makes it produce water from sand", "It helps it cope with periods of limited water availability", "It prevents it from needing food"], "C"),
        ("Why are many desert plants' leaves small or modified into spines?", ["To increase water loss", "To stop their roots absorbing water", "To prevent all gas exchange", "To reduce surface area and limit water loss"], "D"),
        ("How does countercurrent heat exchange help some animals in cold environments?", ["It reduces heat loss by transferring heat between blood flowing in opposite directions", "It converts blood into ice", "It prevents circulation", "It makes body temperature equal to freezing water"], "A"),
        ("Why do many aquatic animals have streamlined bodies?", ["To increase drag", "To reduce resistance as they move through water", "To stop them swimming", "To increase their weight without benefit"], "B"),
        ("How can camouflage help both predators and prey?", ["It guarantees that neither will ever be seen", "It replaces the need for food", "It can help predators approach prey and prey avoid detection", "It prevents animals from reproducing"], "C"),
        ("Why do some plants in wetlands have air spaces in their tissues?", ["To replace all roots with leaves", "To make the plant unable to float", "To stop oxygen movement", "To help move oxygen through tissues in waterlogged conditions"], "D"),
        ("How does migration help some bird species survive seasonal changes?", ["It allows them to reach areas with suitable food and breeding conditions", "It permanently removes their need for energy", "It makes every climate suitable", "It stops them reproducing"], "A"),
        ("Why do nocturnal animals often have senses suited to low-light conditions?", ["They only eat during midday", "They need to locate food, navigate or detect danger at night", "They do not interact with their surroundings", "They use photosynthesis"], "B"),
        ("What is a behavioural adaptation?", ["A bone structure only", "A chemical element", "An action or pattern of behaviour that improves survival or reproduction", "A change in the colour of a rock"], "C"),
        ("Why do some desert animals remain in burrows during the hottest part of the day?", ["Burrows always contain unlimited food", "They need direct sunlight at all times", "Burrows increase exposure to heat", "Burrows can provide cooler, more sheltered conditions"], "D"),
        ("How can a thick layer of blubber help marine mammals in cold water?", ["It provides insulation and can also store energy", "It functions as a gill", "It makes the animal photosynthesise", "It prevents all movement"], "A"),
        ("Why are some mountain animals adapted to low-oxygen conditions?", ["High mountains contain more oxygen than sea level in every respect", "Their physiology may help them obtain and use oxygen more effectively", "They no longer need cellular respiration", "They obtain oxygen from rocks"], "B"),
        ("How does mimicry help certain organisms?", ["It guarantees immunity to all disease", "It makes predators unable to eat anything", "Resembling another organism or object may reduce predation or improve feeding success", "It removes the need for a habitat"], "C"),
        ("Why do some plants develop deep root systems in dry regions?", ["To avoid contact with soil", "To increase evaporation from the roots", "To replace photosynthesis", "To access water deeper in the soil"], "D"),
        ("Which combination is most helpful for a fish living in flowing water?", ["A streamlined body and fins", "Thick fur and feathered wings", "Hooves and broad leaves", "A shell designed for flying"], "A"),
        ("Why do some animals change the colour of their coats seasonally?", ["To become producers", "Seasonal colour changes can improve camouflage against changing backgrounds", "To eliminate the need for shelter", "To prevent body temperature regulation"], "B"),
        ("How might a plant's stomata help it balance gas exchange and water conservation?", ["They permanently remain open in all conditions", "They absorb minerals directly from sunlight", "Their opening and closing regulate carbon dioxide entry and water-vapour loss", "They replace the root system"], "C"),
        ("Why can a large surface-area-to-volume ratio be useful for some small animals in particular environments?", ["It always prevents heat loss", "It stops diffusion", "It guarantees survival in every habitat", "It can increase the rate of exchange of heat or materials, depending on conditions"], "D"),
        ("What is one benefit of huddling together in cold conditions for some animals?", ["It can reduce exposed surface area and conserve heat", "It stops every animal from breathing", "It prevents feeding permanently", "It makes the environment warmer everywhere"], "A"),
        ("Why are many desert plants succulent?", ["They cannot store water", "Their tissues store water that can be used during dry periods", "They only grow underwater", "They do not carry out photosynthesis"], "B"),
        ("How can a bird's beak shape be related to its diet?", ["All birds have identical diets", "Beak shape has no relationship to feeding", "Different beak shapes can help birds obtain and process different foods", "Beaks function only in temperature control"], "C"),
        ("Why can a polar animal's compact body shape help conserve heat?", ["It increases the exposed surface area relative to volume", "It stops all blood circulation", "It makes insulation unnecessary", "A lower surface-area-to-volume ratio can reduce heat loss relative to body volume"], "D"),
        ("Which adaptation would be most useful to a plant growing in a windy coastal habitat?", ["Flexible stems and features that help it withstand wind and salt exposure", "Extremely fragile stems only", "Roots that never anchor the plant", "Leaves that prevent all gas exchange"], "A"),
        ("Why do some animals use warning colours?", ["To attract every predator", "Bright or contrasting colours can signal chemical defence or unpalatability", "To avoid all communication", "To make their bodies invisible"], "B"),
        ("How can seasonal dormancy help some organisms survive?", ["It increases activity when resources are absent", "It guarantees constant growth", "It reduces activity during unfavourable conditions and conserves resources", "It replaces all reproduction"], "C"),
        ("Why are the roots of many mangroves specialised?", ["They are designed only for dry mountain soils", "They prevent gas exchange under all conditions", "They do not support the plant", "They help anchor the plant and cope with waterlogged, often saline conditions"], "D"),
        ("How does a frog's moist skin contribute to its biology?", ["It supports gas exchange through the skin in many species", "It functions as feathers", "It prevents all water movement", "It makes the frog independent of oxygen"], "A"),
        ("Why might an animal have large eyes in a dim environment?", ["Large eyes always improve hearing", "They can help gather more available light", "They prevent the need for a brain", "They allow photosynthesis"], "B"),
        ("What is an important limitation of a particular adaptation?", ["It is always useful under every environmental condition", "It prevents natural selection", "A feature beneficial in one environment may be less useful or costly in another", "It guarantees that an organism will never die"], "C"),
        ("How can a thick coat affect an animal in a hot environment?", ["It always improves cooling", "It replaces the need for water", "It guarantees survival in extreme heat", "It may increase heat retention and require other cooling strategies"], "D"),
    ],

    "Hard": [
        ("A desert plant has a thick stem, a waxy surface and reduced leaves. Which explanation best connects these features to survival?", ["Water storage and reduced transpiration help it cope with limited water", "These features maximise water loss", "They prevent the plant from making food", "They allow the plant to live without any nutrients"], "A"),
        ("Two mammals of similar shape live in different climates. One has a much lower surface-area-to-volume ratio. In a cold climate, this feature may help by:", ["Increasing heat loss per unit volume", "Reducing heat loss relative to body volume", "Preventing all metabolism", "Eliminating the need for insulation"], "B"),
        ("A population of insects varies in colour. Birds more often eat insects that contrast with tree bark. Over generations, what is a likely outcome?", ["All insects stop reproducing", "Tree bark changes to match every insect", "Better-camouflaged insects may leave more offspring, changing colour frequencies", "Individual insects deliberately change their genes to match the bark"], "C"),
        ("Why is it inaccurate to say that an individual organism develops every adaptation it needs during its lifetime?", ["Organisms never respond to environmental conditions", "Adaptations are always acquired through exercise", "Every adaptation appears immediately after a challenge", "Evolutionary adaptations generally arise across generations through heritable variation and natural selection"], "D"),
        ("A fish species lives in cold water. Which feature can help maintain efficient muscle function in that environment?", ["Physiological adaptations such as enzymes and membranes suited to low temperatures", "A complete absence of cell membranes", "Replacing oxygen with sunlight", "Stopping all biochemical reactions"], "A"),
        ("A plant species is moved from a moist forest to a dry desert. Why might it struggle even if it receives adequate sunlight?", ["Sunlight alone meets all plant requirements", "Its existing traits may not adequately manage water scarcity and other desert conditions", "All plants can instantly develop identical desert adaptations", "Water availability never affects plants"], "B"),
        ("How does natural selection change the frequency of an advantageous inherited trait in a population?", ["Every individual acquires the trait because it needs it", "The trait appears equally in all organisms instantly", "Individuals with the trait may reproduce more successfully, passing it to offspring", "Environmental challenges stop inheritance"], "C"),
        ("Why can a behavioural adaptation and a structural adaptation work together?", ["Behaviour and structure cannot interact", "Structural features always prevent behaviour", "Only structural features influence survival", "A behaviour can help an organism use a physical feature effectively in its environment"], "D"),
        ("An animal has large ears, thin fur and is active at night in a hot desert. Which combination of benefits is most plausible?", ["Heat dissipation and reduced daytime heat exposure", "Improved photosynthesis and underwater breathing", "Permanent elimination of water needs", "Ability to live without food"], "A"),
        ("Why can an adaptation have a trade-off?", ["Every adaptation benefits every biological function equally", "A feature that improves one function may reduce performance in another context", "Adaptations never affect energy use", "Natural selection cannot act on inherited traits"], "B"),
        ("A population of birds experiences a prolonged drought. Individuals with beaks better suited to the remaining available seeds reproduce more successfully. This is an example of:", ["Artificial weather control", "An organism changing its genes intentionally", "Natural selection favouring heritable variation", "A guarantee that all individuals survive"], "C"),
        ("Why might two closely related species develop different adaptations in different habitats?", ["Evolution always produces identical traits", "Habitat has no influence on selection", "Species do not inherit traits", "Different environmental pressures can favour different inherited traits over generations"], "D"),
        ("A plant in saline soil limits salt entry and stores excess salt in specialised tissues. These features primarily help it:", ["Manage salt stress and maintain internal water balance", "Increase salt damage in all cells", "Stop absorbing water entirely", "Replace photosynthesis with salt production"], "A"),
        ("Why can migration be costly even when it helps animals reach better habitats?", ["Migration never uses energy", "It requires energy and can expose animals to predators, weather and other risks", "Migrating animals never need food", "Migration guarantees reproduction"], "B"),
        ("An insect resembles a toxic species but is harmless. What type of adaptation does this resemble?", ["Hibernation", "Camouflage through colour matching only", "Batesian mimicry", "Nitrogen fixation"], "C"),
        ("Why is an adaptation not necessarily evidence that an organism is perfectly suited to its environment?", ["Evolution stops as soon as one adaptation appears", "All organisms are equally successful", "Adaptations remove every environmental risk", "Adaptations involve trade-offs and do not guarantee survival under every condition"], "D"),
        ("A high-altitude mammal has physiological features that improve oxygen delivery. Why are these useful?", ["Oxygen availability can be lower at high altitude, making oxygen uptake and delivery more challenging", "High altitude eliminates the need for respiration", "Oxygen is absent from all mountain habitats", "The animal obtains all energy directly from rocks"], "A"),
        ("Why can an adaptation that is beneficial today become less useful after a rapid environmental change?", ["Inherited traits always change instantly", "The new conditions may alter which traits improve survival and reproduction", "Environmental changes never affect fitness", "Natural selection always favours the same trait in every environment"], "B"),
        ("Which evidence would best support the claim that a trait is an inherited adaptation rather than only a temporary response?", ["One individual changes colour once", "An organism is observed resting", "Heritable variation in the trait is associated with reproductive success across generations", "The habitat contains no other organisms"], "C"),
        ("A species can tolerate a wide range of temperatures but has a narrow diet. What does this suggest about its ecological tolerance?", ["It must survive in every habitat", "It has no environmental limits", "It cannot be affected by food availability", "Tolerance can be broad for one environmental factor and narrow for another"], "D"),
        ("Why can insulation be disadvantageous for an animal during intense activity in a warm environment?", ["It may make heat dissipation more difficult", "It prevents all heat production", "It makes water unnecessary", "It removes the need for blood circulation"], "A"),
        ("A bird population moves into a habitat with different food sources. Over many generations, beak variation changes through selection. Which statement is most accurate?", ["Every bird changes its beak shape deliberately", "The population's inherited trait frequencies can change as individuals differ in reproductive success", "The environment directly rewrites every bird's DNA in the same way", "Evolution occurs only within one individual's lifetime"], "B"),
        ("Why may a specialist species be particularly vulnerable when its habitat changes?", ["Specialists can use every possible resource", "They have no ecological requirements", "They may depend on a narrow range of food or habitat conditions", "They always reproduce faster than generalists"], "C"),
        ("What is the significance of genetic variation for adaptation by natural selection?", ["It guarantees that all individuals survive", "It prevents inheritance", "It means environmental pressures do not matter", "It provides heritable differences on which selection can act"], "D"),
        ("A plant closes its stomata during severe drought. What is a likely benefit and cost of this response?", ["It reduces water loss but can also limit carbon dioxide uptake and photosynthesis", "It increases water loss while doubling carbon dioxide uptake", "It eliminates the need for roots", "It guarantees uninterrupted growth"], "A"),
        ("Why is the phrase 'survival of the fittest' not necessarily equivalent to 'survival of the strongest'?", ["Fitness only measures physical strength", "Fitness refers to reproductive success in a particular environment, not simply strength", "The strongest individual always produces the most offspring", "Fitness has no relationship to reproduction"], "B"),
        ("An animal's coat colour matches snow in winter but contrasts with dark soil in summer. What is the key ecological risk if the environment becomes snow-free earlier each year?", ["Its coat becomes a producer", "It no longer requires camouflage", "Seasonal colour timing may mismatch the background and increase detection", "Predators stop using vision"], "C"),
        ("Why can a species' range of tolerance help predict where it can live?", ["All environmental factors are identical everywhere", "A species can live outside all tolerance limits indefinitely", "Habitat suitability depends only on colour", "Its survival and reproduction depend on environmental conditions staying within tolerable ranges"], "D"),
        ("Which statement best distinguishes acclimation from evolutionary adaptation?", ["Acclimation is a change within an individual's lifetime; evolutionary adaptation involves heritable population changes across generations", "They always mean exactly the same thing", "Evolutionary adaptation occurs only during sleep", "Acclimation always changes DNA permanently"], "A"),
        ("Why should conservation plans consider the habitat requirements and adaptations of a species?", ["All species can survive in any habitat", "Protecting the conditions and resources a species depends on can improve its chance of persistence", "Adaptations make habitat loss irrelevant", "Conservation is unrelated to survival"], "B"),
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

        print("\nAdaptations in Living Organisms expansion completed!")
        print(f"Total new questions inserted: {inserted_total}")
        print("Easy: 30 questions")
        print("Medium: 30 questions")
        print("Hard: 30 questions")
        print("Other lessons and Social Science were not modified.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()
