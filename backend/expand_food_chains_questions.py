
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

LESSON_TITLE = "Food Chains and Food Webs"
TARGET_QUESTIONS = 30

QUESTION_BANK = {
    "Easy": [
        ("What is a food chain?", ["A sequence showing how energy passes between organisms", "A group of rocks", "A type of weather", "A water storage system"], "A"),
        ("Which organisms are usually producers in a food chain?", ["Lions", "Green plants", "Frogs", "Eagles"], "B"),
        ("Which of these is a primary consumer?", ["Grass", "Algae", "A rabbit that eats grass", "A hawk that eats rabbits"], "C"),
        ("What is the main source of energy for most ecosystems?", ["Moonlight", "Soil", "Wind", "The Sun"], "D"),
        ("Which organisms break down dead plants and animals?", ["Decomposers", "Producers", "Herbivores", "Pollinators only"], "A"),
        ("Which animal is a herbivore?", ["Tiger", "Deer", "Eagle", "Wolf"], "B"),
        ("Which animal is commonly a secondary consumer in a grassland food chain?", ["Grass", "Grasshopper", "Frog that eats grasshoppers", "Grass seed"], "C"),
        ("What does an arrow in a food chain generally indicate?", ["The size of an organism", "The age of an organism", "The direction an animal walks", "The direction of energy transfer"], "D"),
        ("Which of these is a producer in a pond ecosystem?", ["Phytoplankton", "Small fish", "Frog", "Water snake"], "A"),
        ("What is a food web?", ["A single animal's home", "A network of interconnected food chains", "A type of spider web only", "A collection of unrelated rocks"], "B"),
        ("Which organism is a carnivore?", ["Cow", "Rabbit", "Lion", "Grass"], "C"),
        ("Which group obtains energy by eating plants or other organisms?", ["Producers only", "Sunlight", "Minerals only", "Consumers"], "D"),
        ("What is the first trophic level in a typical grazing food chain?", ["Producers", "Primary consumers", "Secondary consumers", "Top predators"], "A"),
        ("Which organism might eat a grasshopper in a simple grassland food chain?", ["Grass", "Frog", "Grass seed", "Flower"], "B"),
        ("Which of these is an example of a decomposer?", ["Eagle", "Deer", "Many fungi", "Grasshopper"], "C"),
        ("What do herbivores mainly eat?", ["Other animals", "Only dead rocks", "Only minerals", "Plants or plant material"], "D"),
        ("Which of these is an omnivore?", ["A bear that eats both berries and animals", "A cow that eats grass", "A tiger that eats meat", "A plant that makes its own food"], "A"),
        ("What happens to energy as it moves through successive trophic levels?", ["It increases without limit", "Some energy is lost as heat at each transfer", "It remains exactly the same", "It changes into matter only"], "B"),
        ("Which of these is a simple food chain?", ["Sun → soil → rock", "Tiger → grass → Sun", "Grass → grasshopper → frog", "Water → stone → mountain"], "C"),
        ("What is a predator?", ["An organism that makes its own food", "A type of producer", "An organism that only decomposes leaves", "An organism that hunts and eats other organisms"], "D"),
        ("What is prey?", ["An organism hunted and eaten by a predator", "An organism that produces sunlight", "A non-living mineral", "A type of decomposer only"], "A"),
        ("Which organism is likely to be a top predator in a simple grassland chain?", ["Grass", "Eagle", "Grasshopper", "Rabbit"], "B"),
        ("Why are green plants important in most food chains?", ["They consume all the oxygen", "They eat every consumer", "They convert light energy into chemical energy through photosynthesis", "They obtain all their energy by hunting"], "C"),
        ("Which of these is a primary consumer in a marine food chain?", ["Shark that eats seals", "Seaweed", "Large predatory fish", "Zooplankton that eats phytoplankton"], "D"),
        ("What is a trophic level?", ["A feeding position in a food chain or food web", "The temperature of an ecosystem", "The depth of a lake only", "The age of a forest"], "A"),
        ("Which organisms can return nutrients to the environment by decomposing dead material?", ["Only top predators", "Bacteria and fungi", "Only herbivores", "Only flowering plants"], "B"),
        ("What could happen if a predator population decreases significantly?", ["All producers immediately disappear", "Sunlight stops reaching the ecosystem", "Some prey populations may increase", "Every food chain ends instantly"], "C"),
        ("Which relationship occurs when one organism hunts and eats another?", ["Mutualism only", "Pollination", "Competition only", "Predation"], "D"),
        ("Which of these is a food chain from a grassland?", ["Grass → rabbit → fox", "Fox → grass → rabbit", "Rabbit → fox → grass", "Grass → fox → rabbit"], "A"),
        ("Why can a food web be more realistic than a single food chain?", ["It includes only one species", "It shows multiple feeding relationships in an ecosystem", "It excludes predators", "It shows only non-living things"], "B"),
    ],

    "Medium": [
        ("In the chain grass → grasshopper → frog → snake, which organism is the secondary consumer?", ["Grass", "Grasshopper", "Frog", "Snake"], "C"),
        ("Why is less energy usually available at higher trophic levels?", ["Energy is created at every level", "Producers use no energy", "Consumers convert all energy into biomass", "Organisms use energy for life processes and lose some as heat"], "D"),
        ("If grass is the producer and a rabbit eats it, what trophic level does the rabbit occupy?", ["Primary consumer", "Producer", "Secondary consumer", "Decomposer"], "A"),
        ("What may happen to grass if the rabbit population in a grassland decreases sharply, assuming other factors remain similar?", ["Grass must disappear", "Grass may increase because fewer rabbits eat it", "Grass becomes a consumer", "Grass stops photosynthesis"], "B"),
        ("Which sequence correctly represents energy flow in a simple aquatic food chain?", ["Shark → phytoplankton → zooplankton", "Zooplankton → sunlight → phytoplankton", "Phytoplankton → zooplankton → small fish", "Small fish → phytoplankton → sunlight"], "C"),
        ("What is the main difference between energy flow and nutrient cycling in ecosystems?", ["Both stop at producers", "Energy cycles indefinitely without loss", "Nutrients flow in only one direction and never return", "Energy flows through ecosystems while nutrients can be recycled"], "D"),
        ("If a pesticide kills many insects in a field, what could happen to insect-eating birds?", ["Their food supply may decrease", "Their food supply must increase", "They immediately become producers", "They no longer need energy"], "A"),
        ("Why can removing a top predator affect several species in a food web?", ["Top predators never affect prey", "Changes in predator numbers can alter prey and other interconnected populations", "Food webs contain no interconnected species", "Predators produce all the plants"], "B"),
        ("What is a grazing food chain generally based on?", ["Dead organic matter only", "Predators eating predators only", "Living green plants or algae as producers", "Minerals eating plants"], "C"),
        ("What is a detritus food chain based on?", ["Sunlight directly consumed by animals", "Only living grass", "Only top predators", "Dead organic material and the organisms feeding on it"], "D"),
        ("In a chain algae → zooplankton → small fish → large fish, which organism is the tertiary consumer?", ["Large fish", "Zooplankton", "Algae", "Small fish"], "A"),
        ("Why are food chains usually limited in length?", ["Energy increases at each transfer", "Available energy decreases at successive trophic levels", "Producers cannot store energy", "Predators never require energy"], "B"),
        ("What could happen if a disease greatly reduces the number of rabbits in a food web?", ["All plants immediately die", "Foxes become producers", "Predators that depend heavily on rabbits may decline or switch prey", "All decomposers disappear"], "C"),
        ("What role do decomposers play in nutrient cycling?", ["They permanently lock all nutrients in dead matter", "They create sunlight", "They stop dead matter from breaking down", "They break down organic matter and release nutrients into the environment"], "D"),
        ("Which statement about omnivores is correct?", ["They can feed at more than one trophic level", "They are always producers", "They eat plants only", "They never interact with food webs"], "A"),
        ("How could competition occur between two predators in the same ecosystem?", ["They both make their own food", "They may depend on the same prey species", "They never share habitat", "They both act as decomposers"], "B"),
        ("What does a biomass pyramid represent?", ["The number of hours in a day", "Only the temperature at each level", "The amount of living biological material at different trophic levels", "The number of abiotic factors only"], "C"),
        ("Why might a pyramid of energy always show less energy at higher trophic levels?", ["Energy is recycled completely as heat", "Consumers do not use energy", "Producers receive energy from predators", "Energy is lost from the usable biological system during transfers, including as heat"], "D"),
        ("If a herbicide reduces the abundance of aquatic plants, which population may be directly affected first among these choices?", ["Herbivores that feed on those plants", "A distant land predator with no connection", "Clouds", "Mountain rocks"], "A"),
        ("What is a trophic cascade?", ["A waterfall that contains fish", "An indirect chain of effects across trophic levels caused by changes in one population", "A process in which all organisms become producers", "The movement of rocks between habitats"], "B"),
        ("Why might a food web be more resilient than a food chain in some circumstances?", ["It always prevents extinction", "It has no predators", "Some consumers may have alternative food sources if one prey species declines", "It contains no energy losses"], "C"),
        ("What happens to much of the chemical energy an animal obtains from food?", ["All of it becomes offspring", "All of it remains stored permanently", "It changes into sunlight", "It is used for metabolism and released as heat, while some supports growth and other functions"], "D"),
        ("Which organisms are most directly responsible for converting sunlight into chemical energy in most ecosystems?", ["Photosynthetic producers", "Carnivores", "Decomposers only", "Parasites only"], "A"),
        ("A decline in phytoplankton could affect zooplankton and fish because:", ["Fish make all phytoplankton", "Phytoplankton supports the base of many aquatic food webs", "Zooplankton never eats phytoplankton", "Fish obtain energy directly from rocks"], "B"),
        ("What is bioaccumulation?", ["The loss of all nutrients from soil", "The production of oxygen by predators", "The buildup of a substance in an organism over time", "The movement of water through plants"], "C"),
        ("Why can some persistent pollutants reach high concentrations in top predators?", ["Top predators always excrete every pollutant instantly", "Pollutants disappear when eaten", "Pollutants cannot enter food webs", "Some persistent substances biomagnify as contaminated prey are consumed"], "D"),
        ("If a snake eats frogs that eat grasshoppers that feed on plants, the snake is indirectly dependent on:", ["The producers at the base of the chain", "Only rocks", "No other organisms", "Only decomposers"], "A"),
        ("Which factor is abiotic rather than a living component of a food web?", ["Grass", "Temperature", "Fungi", "Rabbit"], "B"),
        ("How does overfishing a large predatory fish potentially affect a marine food web?", ["It cannot affect any other population", "All prey species immediately vanish", "Some prey populations may rise and cause further changes in the web", "It creates new sunlight"], "C"),
        ("Why is biodiversity important for ecosystem functioning?", ["It guarantees that ecosystems never change", "It removes the need for energy", "It means every species occupies the same role", "A variety of species can support ecological processes and interconnected relationships"], "D"),
    ],

    "Hard": [
        ("In a food chain, producers store 20,000 kJ of energy. If approximately 10% transfers to each next trophic level, how much reaches the secondary consumer?", ["200 kJ", "2,000 kJ", "20 kJ", "18,000 kJ"], "A"),
        ("A pesticide persists in the environment and becomes more concentrated at successive trophic levels. What is this process called?", ["Decomposition", "Biomagnification", "Photosynthesis", "Nitrogen fixation"], "B"),
        ("A top predator is removed from an ecosystem. Herbivores increase and plant biomass declines. This pattern is best described as:", ["A nutrient cycle", "Primary succession only", "A trophic cascade", "A change unrelated to predation"], "C"),
        ("Why can the 10% rule only be treated as an approximate ecological model?", ["All ecosystems transfer exactly 10% of energy", "Energy transfer is always 100%", "It applies only to non-living things", "Transfer efficiency varies with organisms, food quality and ecological conditions"], "D"),
        ("A producer level contains 50,000 kJ. Assuming 10% transfer at each step, how much energy is expected at the tertiary consumer level?", ["50 kJ", "500 kJ", "5,000 kJ", "45,000 kJ"], "A"),
        ("A population of herbivores declines after a drought reduces plant growth. What is the most direct explanation?", ["Herbivores have become producers", "Reduced primary productivity lowers the food available to herbivores", "The drought increases all plant biomass", "Herbivores no longer need energy"], "B"),
        ("In a stable ecosystem, why can a species with several prey species be less vulnerable to the decline of one prey than a specialist predator?", ["Generalists do not need food", "Specialists always eat every available species", "It may switch to alternative prey when one food source declines", "Alternative prey eliminate all competition"], "C"),
        ("A lake experiences excessive nutrient input, followed by an algal bloom and low dissolved oxygen. Which chain best explains this event?", ["Nutrients decrease algae, increasing oxygen demand", "Fish produce all nutrients", "Algae remove every decomposer", "Nutrient enrichment promotes algal growth; decomposition of excess biomass can consume oxygen"], "D"),
        ("Why may a small amount of a persistent pollutant in water become a much larger concentration in a top predator?", ["The pollutant can accumulate in organisms and pass through many prey-to-predator transfers", "Water turns every pollutant into nutrients", "Top predators produce the pollutant through photosynthesis", "The pollutant must be harmless if its initial concentration is low"], "A"),
        ("A food web contains two predators that share prey. If one predator increases greatly, what is a plausible indirect effect?", ["The other predator must increase at exactly the same rate", "Competition for shared prey may increase and alter both populations", "The prey becomes a producer", "Energy transfer stops in the entire ecosystem"], "B"),
        ("Why does an energy pyramid differ fundamentally from some pyramids of numbers or biomass?", ["Energy is created at every trophic level", "Energy can be recycled without loss", "Energy available for transfer declines at successive levels because organisms use and dissipate energy", "Energy pyramids show only the number of species"], "C"),
        ("In a detritus food web, what is the significance of dead leaves entering the soil?", ["They have no chemical energy", "They are consumed only by top predators", "They permanently stop nutrient cycling", "They provide organic material for detritivores and decomposers"], "D"),
        ("A disease reduces a dominant plant species. Which outcome is most plausible?", ["Herbivores dependent on that plant may decline, while other plant species may benefit from reduced competition", "Every animal must immediately become extinct", "All decomposers stop functioning", "Energy enters the ecosystem without producers"], "A"),
        ("Why can removing a keystone predator produce a disproportionately large ecological effect?", ["Its population is always the largest", "Its interactions can regulate populations and help maintain community structure", "It produces all primary energy", "It prevents every species from reproducing"], "B"),
        ("A researcher compares two ecosystems with equal producer energy but different transfer efficiencies. What should be expected if one ecosystem has higher transfer efficiency at every trophic transfer?", ["It will have less energy at every higher level", "The two ecosystems must have identical energy pyramids", "More energy may reach its higher trophic levels", "Its producers will no longer photosynthesise"], "C"),
        ("Which observation provides the strongest evidence of biomagnification rather than simple bioaccumulation?", ["A pollutant is found in one organism", "A pollutant is detected in water", "An organism absorbs a pollutant over time", "Pollutant concentration systematically increases across successive trophic levels"], "D"),
        ("Why might a food web recover differently from two disturbances of similar size?", ["The species affected and the structure of their interactions can differ", "Every disturbance has exactly the same effect", "Food-web structure has no ecological importance", "Only sunlight determines recovery"], "A"),
        ("A grassland loses many pollinating insects. What is one possible indirect effect on the food web?", ["All carnivores immediately become producers", "Reduced pollination may lower reproduction in some flowering plants, affecting organisms that depend on them", "Herbivores stop eating plants", "Decomposers become sunlight"], "B"),
        ("Why can energy transfer efficiency vary between trophic levels?", ["All organisms digest all food equally", "Energy transfer depends only on body colour", "Food digestibility, metabolism and the fraction assimilated into biomass differ among organisms", "Energy never leaves an organism"], "C"),
        ("A fish population declines after its main prey declines, even though the fish itself is not directly targeted by humans. This is an example of:", ["Direct photosynthesis", "Abiotic nutrient formation", "A change with no food-web connection", "An indirect effect mediated through feeding relationships"], "D"),
        ("Which statement best distinguishes a food web from a simple linear food chain?", ["A food web represents multiple overlapping feeding pathways and connections", "A food web contains no producers", "A food chain always includes every species in an ecosystem", "A food web shows only energy from the Sun and no organisms"], "A"),
        ("If 15% of the energy at one trophic level transfers to the next, how much energy reaches the third trophic level from 10,000 kJ at the first level, assuming the first level is producers and transfer is 15% each time?", ["1,500 kJ", "225 kJ", "22.5 kJ", "8,500 kJ"], "B"),
        ("Why may a simplified food-chain diagram not fully predict the effect of removing one species?", ["Food chains contain no feeding relationships", "All species depend only on sunlight", "The species may participate in additional feeding links not shown in the simplified chain", "Species cannot change their diets"], "C"),
        ("A top predator consumes prey containing a persistent fat-soluble chemical. Why might the chemical become concentrated in the predator's tissues?", ["The chemical is always converted into harmless oxygen", "The predator produces the chemical by photosynthesis", "Fat-soluble chemicals cannot enter organisms", "The chemical may be retained and accumulate faster than it is eliminated"], "D"),
        ("What would most directly reduce the amount of energy entering a grazing food chain?", ["A substantial reduction in photosynthesis by its producers", "An increase in the number of top predators alone", "A change in the colour of a non-living rock", "A decrease in the number of decomposers without any change in producer productivity"], "A"),
        ("Why are decomposers essential even though they do not usually occupy a single simple consumer position in a grazing chain?", ["They create energy from nothing", "They break down dead matter and help return nutrients to ecosystems", "They consume sunlight instead of organic matter", "They prevent matter from cycling"], "B"),
        ("A predator switches from a declining prey species to another prey species. What does this illustrate?", ["That energy transfer has stopped", "That the predator has become a producer", "That feeding relationships can change and connect different parts of a food web", "That prey species are not part of ecosystems"], "C"),
        ("An ecosystem loses several species that perform similar ecological roles. Why could this make the ecosystem less resilient?", ["It guarantees more alternative food sources", "It removes every disturbance", "It makes all species interchangeable", "Fewer species may remain to maintain the same functions when conditions change"], "D"),
        ("Which approach is most appropriate for testing whether a predator controls herbivore abundance in an ecosystem?", ["Use replicated predator-exclusion and control areas while monitoring herbivores and relevant environmental factors", "Remove all organisms and assume the result", "Measure only the colour of the soil once", "Change predator abundance and every other factor without recording them"], "A"),
        ("Why is it inaccurate to say that all energy entering an ecosystem is eventually recycled in the same way as nutrients?", ["Energy never enters ecosystems", "Energy flows through trophic transfers and is eventually dissipated as heat, whereas matter can be recycled", "Nutrients cannot be recycled", "Heat is a producer that reproduces"], "B"),
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

        print("\nFood Chains and Food Webs expansion completed!")
        print(f"Total new questions inserted: {inserted_total}")
        print("Easy: 30 questions")
        print("Medium: 30 questions")
        print("Hard: 30 questions")
        print("Other lessons and Social Science were not modified.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()
