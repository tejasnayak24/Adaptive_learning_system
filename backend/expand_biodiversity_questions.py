
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

LESSON_TITLE = "Conservation of Biodiversity"
TARGET_QUESTIONS = 30

QUESTION_BANK = {
    "Easy": [
        ("What does biodiversity mean?", ["The variety of living organisms in an area or on Earth", "The number of buildings in a city", "The amount of rainfall only", "The study of rocks alone"], "A"),
        ("Which of these is a threatened animal in India?", ["Domestic chicken", "Bengal tiger", "House cat", "Domestic goat"], "B"),
        ("What is conservation?", ["Using all resources immediately", "Removing every forest", "Protecting and managing nature and its resources", "Preventing all organisms from reproducing"], "C"),
        ("Which activity helps conserve forests?", ["Illegal logging", "Uncontrolled forest burning", "Destroying wildlife habitats", "Planting trees and managing forests sustainably"], "D"),
        ("What is a national park mainly established to do?", ["Protect wildlife and natural ecosystems", "Provide land exclusively for factories", "Encourage illegal hunting", "Remove all native plants"], "A"),
        ("Which of these is an example of an endangered animal?", ["Domestic cow", "Amur leopard", "Common pigeon", "Domestic dog"], "B"),
        ("What is poaching?", ["Planting native trees", "Observing birds responsibly", "Illegal hunting or capturing of wildlife", "Cleaning a river"], "C"),
        ("Why are bees important to many ecosystems?", ["They produce fossil fuels", "They stop all plant growth", "They eliminate the need for seeds", "They pollinate many flowering plants"], "D"),
        ("What is a wildlife sanctuary?", ["A protected area intended to conserve wildlife and habitats", "A place where all wildlife must be removed", "An industrial mining zone", "A landfill for hazardous waste"], "A"),
        ("Which action can help protect endangered species?", ["Destroying their breeding grounds", "Protecting their habitats", "Increasing illegal trade", "Introducing pollution into their habitats"], "B"),
        ("What is an ecosystem?", ["A collection of non-living rocks only", "A group of buildings", "Living organisms interacting with one another and their physical environment", "A single weather event"], "C"),
        ("Which of these is a major cause of biodiversity loss?", ["Habitat restoration", "Wildlife protection", "Sustainable forestry", "Habitat destruction"], "D"),
        ("What is deforestation?", ["The clearing or removal of forests", "The restoration of a wetland", "The protection of endangered animals", "The growth of a new forest"], "A"),
        ("Which of these is a renewable biological resource when managed sustainably?", ["A fixed petroleum reserve", "Timber from a sustainably managed forest", "A finite coal deposit", "A mineral ore deposit"], "B"),
        ("Why should coral reefs be protected?", ["They have no living organisms", "They are made entirely of plastic", "They support diverse marine life and provide important ecosystem services", "They prevent all ocean currents"], "C"),
        ("What is an invasive species?", ["A species native to every ecosystem", "An organism that cannot reproduce", "A species that exists only in laboratories", "A non-native species whose introduction causes or is likely to cause harm"], "D"),
        ("Which practice can help conserve water ecosystems?", ["Preventing sewage and harmful waste from entering rivers", "Dumping chemicals into lakes", "Destroying wetlands", "Removing all aquatic plants"], "A"),
        ("What does extinction mean?", ["A species moves to a different habitat", "A species no longer exists anywhere on Earth", "An organism changes its diet", "A species becomes more abundant"], "B"),
        ("Which of these is an example of in-situ conservation?", ["Keeping seeds only in a laboratory freezer", "Displaying a stuffed animal in a museum", "Protecting a species in its natural habitat", "Growing every plant only indoors"], "C"),
        ("Which of these is an example of ex-situ conservation?", ["Protecting an entire natural forest", "Creating a marine protected area", "Preventing hunting in a national park", "Maintaining endangered animals in a conservation breeding programme"], "D"),
        ("Why are forests important for biodiversity?", ["They provide habitats, food and shelter for many organisms", "They prevent all natural changes", "They contain no animal life", "They eliminate the water cycle"], "A"),
        ("Which action can help reduce wildlife trafficking?", ["Buying products made from endangered animals", "Supporting legal enforcement and avoiding illegal wildlife products", "Capturing wild animals for entertainment", "Ignoring suspicious wildlife trade"], "B"),
        ("What is a habitat?", ["A type of mineral", "A food-processing machine", "The natural place where an organism lives", "A form of weather"], "C"),
        ("Which group includes organisms that help pollinate many crops?", ["Only large mammals", "Only reptiles", "Only fish", "Bees and other pollinating animals"], "D"),
        ("Why are seed banks useful?", ["They store seeds to help preserve plant genetic diversity", "They increase habitat destruction", "They replace all natural ecosystems", "They store only animal bones"], "A"),
        ("What is one benefit of biodiversity to humans?", ["It prevents every disease", "It supports food production, medicines and ecosystem services", "It removes the need for clean water", "It guarantees that natural disasters never happen"], "B"),
        ("Which action can help protect marine biodiversity?", ["Dumping plastic into the sea", "Increasing destructive fishing", "Reducing marine pollution and protecting important habitats", "Destroying mangroves"], "C"),
        ("What is an endemic species?", ["A species found naturally everywhere", "A species that cannot reproduce", "A species created from plastic", "A species native to and restricted to a particular geographic area"], "D"),
        ("Which practice supports biodiversity in a garden?", ["Planting a variety of suitable native plants", "Removing all flowering plants", "Using pesticides unnecessarily", "Replacing every habitat with concrete"], "A"),
        ("Why is genetic diversity important within a species?", ["It makes all individuals identical", "It provides variation that can help populations respond to environmental changes", "It prevents reproduction", "It eliminates natural selection"], "B"),
    ],

    "Medium": [
        ("Why can habitat fragmentation threaten biodiversity even when some forest remains?", ["Fragments always provide more habitat than continuous forest", "Fragmentation prevents all animal movement", "Small isolated populations may have reduced gene flow and greater extinction risk", "It guarantees that every species will adapt"], "C"),
        ("How can protecting a keystone species benefit an ecosystem?", ["It always increases every population equally", "It removes all competition", "It prevents natural selection", "Its protection can maintain ecological interactions and community structure"], "D"),
        ("Why is genetic diversity important for conservation breeding programmes?", ["It can reduce inbreeding risks and preserve the capacity to respond to change", "It makes all offspring genetically identical", "It guarantees that no animal will become ill", "It eliminates the need to protect habitats"], "A"),
        ("What is a wildlife corridor designed to do?", ["Separate all wildlife populations permanently", "Connect habitat patches and support organism movement", "Increase illegal hunting", "Replace every protected area with roads"], "B"),
        ("Why can monoculture farming reduce biodiversity compared with a diverse natural habitat?", ["It always supports more native species", "It prevents all pest outbreaks", "It often provides fewer types of habitats and resources for different organisms", "It guarantees healthy soil under all conditions"], "C"),
        ("How can climate change threaten species with narrow environmental requirements?", ["It keeps every habitat unchanged", "It prevents temperature changes", "It eliminates all seasonal variation", "It can shift conditions beyond the range those species tolerate"], "D"),
        ("What is the primary purpose of a seed bank in plant conservation?", ["Preserving seeds and their genetic diversity for future use", "Destroying rare plant varieties", "Preventing plants from reproducing in nature", "Replacing all forests with farms"], "A"),
        ("Why are wetlands important for biodiversity conservation?", ["They contain no specialised species", "They provide habitats and can support water filtration and flood regulation", "They always increase water pollution", "They prevent all aquatic organisms from living"], "B"),
        ("How can overfishing affect marine food webs?", ["It always increases predator populations", "It removes the need for marine conservation", "It can reduce target species and alter relationships among predators and prey", "It creates unlimited fish stocks"], "C"),
        ("Why can invasive species spread rapidly in a new environment?", ["They always have more predators in the new area", "They cannot reproduce outside their native range", "They never compete with native organisms", "They may face fewer natural enemies and compete successfully for resources"], "D"),
        ("What is the main distinction between in-situ and ex-situ conservation?", ["In-situ protects organisms in their natural habitats; ex-situ conserves them outside those habitats", "In-situ uses only zoos", "Ex-situ always protects entire ecosystems", "Both terms mean illegal hunting"], "A"),
        ("Why is habitat restoration often important after protecting an endangered species?", ["Protection alone always restores damaged habitat immediately", "The species may still lack sufficient food, shelter or breeding sites", "Restoration prevents every natural process", "Habitat quality does not affect survival"], "B"),
        ("How can pesticide overuse affect biodiversity?", ["It affects only the intended pest", "It always increases pollinator numbers", "It can harm non-target organisms, including pollinators and natural pest predators", "It eliminates all environmental risks"], "C"),
        ("Why can small isolated wildlife populations be vulnerable to extinction?", ["They always have unlimited genetic diversity", "They are unaffected by disease", "They can never experience random population changes", "They may face inbreeding, low genetic variation and greater sensitivity to random events"], "D"),
        ("What is one advantage of establishing marine protected areas?", ["They can protect habitats and allow some populations to recover when well designed and enforced", "They guarantee that no marine pollution occurs", "They eliminate all fishing worldwide", "They prevent ocean currents"], "A"),
        ("Why is protecting pollinators important for agriculture and ecosystems?", ["Pollination is unnecessary for every plant", "Many flowering plants depend on animal pollinators for successful reproduction", "Pollinators consume all crops", "Pollinators prevent seed production"], "B"),
        ("How can sustainable harvesting help conserve a wild population?", ["It removes all mature individuals", "It ignores reproductive rates", "It keeps extraction within levels that allow the population to replenish", "It guarantees unlimited population growth"], "C"),
        ("Why can restoring native vegetation improve local biodiversity?", ["Native vegetation always eliminates all wildlife", "It replaces every ecosystem process with farming", "It prevents all insects from surviving", "It can restore food sources, shelter and ecological relationships suited to local species"], "D"),
        ("What is a major role of protected areas in conservation?", ["Maintaining important habitats and reducing certain human pressures on wildlife", "Guaranteeing that all environmental threats disappear", "Encouraging uncontrolled habitat destruction", "Preventing every species from moving"], "A"),
        ("Why can genetic rescue be considered in some small isolated populations?", ["It always removes every disease risk", "Introducing carefully selected individuals may increase genetic diversity and reduce inbreeding", "It replaces all habitat conservation", "It guarantees immediate population recovery"], "B"),
        ("How can light pollution affect biodiversity?", ["It affects only non-living objects", "It always improves animal navigation", "It can disrupt the behaviour and movement of nocturnal organisms", "It eliminates all urban wildlife risks"], "C"),
        ("Why is illegal wildlife trade a conservation concern?", ["It always increases wild population sizes", "It affects only domesticated animals", "It has no relationship to extinction risk", "It can remove individuals from wild populations and threaten vulnerable species"], "D"),
        ("What is ecological restoration?", ["Assisting the recovery of a degraded or damaged ecosystem", "Replacing every natural area with buildings", "Removing all native vegetation", "Preventing all ecological processes"], "A"),
        ("Why can conserving a single species without protecting its habitat be insufficient?", ["Species never depend on habitat", "The species may still lose the food, shelter and breeding conditions it needs", "Habitat has no relationship to reproduction", "Captivity always replaces every ecological need"], "B"),
        ("What does carrying capacity describe in ecology?", ["The number of different colours in an ecosystem", "The speed of a river", "The population size an environment can support over time under given conditions", "The age of the oldest tree only"], "C"),
        ("Why can overgrazing contribute to biodiversity loss?", ["It always increases plant diversity", "It prevents all soil erosion", "It guarantees forest regeneration", "It can remove vegetation, degrade soil and alter habitats"], "D"),
        ("How can community participation improve conservation outcomes?", ["Local people can contribute knowledge, stewardship and support for sustainable management", "It guarantees that no conflict will occur", "It removes the need for scientific monitoring", "It prevents all policy enforcement"], "A"),
        ("Why should conservation programmes monitor populations over time?", ["A single observation proves permanent recovery", "Long-term data help identify trends and evaluate whether actions are effective", "Monitoring changes population sizes directly in every case", "Population trends never change"], "B"),
        ("Which strategy best addresses biodiversity loss caused by habitat destruction?", ["Increase habitat fragmentation", "Remove native vegetation", "Protect remaining habitats and restore degraded areas where feasible", "Increase illegal logging"], "C"),
        ("Why is maintaining biodiversity across several trophic levels important?", ["Only top predators matter", "Producers do not support food webs", "Every species performs exactly the same function", "Species at different trophic levels contribute to interconnected ecosystem processes"], "D"),
    ],

    "Hard": [
        ("A protected population has very low genetic diversity and a high rate of inbreeding. Which management action may help, alongside habitat protection?", ["Carefully managed genetic rescue that increases gene flow", "Further isolating every individual", "Reducing the population size without assessment", "Preventing all reproduction"], "A"),
        ("Why can a protected area fail to conserve a species if it is too small or isolated?", ["Protected status guarantees unlimited habitat", "It may not support viable populations or movement between habitats", "Small areas always contain every ecosystem", "Isolation always increases genetic diversity"], "B"),
        ("A restoration project plants many tree species but removes natural grassland that supports endemic species. What is the key concern?", ["More trees always mean greater biodiversity", "Endemic species never depend on habitats", "Restoration must reflect the original ecosystem and local conservation priorities rather than maximising tree cover alone", "Grasslands contain no biodiversity"], "C"),
        ("Why can a population bottleneck reduce a species' ability to respond to future environmental change?", ["It always increases every allele frequency equally", "It prevents all natural selection", "It guarantees stronger offspring", "It can reduce genetic variation through a sharp decline in population size"], "D"),
        ("An invasive predator is introduced to an island where native species evolved without similar predators. Why can the effects be severe?", ["Native prey may lack effective behavioural or ecological defences against the new predator", "Island species always resist every predator", "Predators cannot change food webs", "Introduced predators never reproduce"], "A"),
        ("Which evidence would best show that a wildlife corridor is functioning as intended?", ["The corridor has a signboard", "Monitoring shows animals moving between habitat patches and, where relevant, increased gene flow", "Aerial photographs show only its colour", "The corridor is built but never monitored"], "B"),
        ("Why is conservation prioritisation often necessary when resources are limited?", ["Every conservation action has the same cost and benefit", "Species never face different threat levels", "Managers must choose actions likely to deliver meaningful benefits given limited time, funding and capacity", "Prioritisation means ignoring all threatened species"], "C"),
        ("A population increases after hunting is banned, but its habitat continues to shrink. What is the most appropriate conclusion?", ["The species is now guaranteed permanent survival", "Habitat loss no longer matters", "Population recovery proves no further monitoring is needed", "Reduced hunting may help, but ongoing habitat loss can still threaten long-term viability"], "D"),
        ("Why can preserving genetic material outside natural habitats complement in-situ conservation?", ["It can provide a backup for some genetic diversity but cannot replace functioning habitats and ecosystems", "It always protects every ecological interaction", "It eliminates the need to restore habitats", "It guarantees that extinct ecosystems will recover automatically"], "A"),
        ("What is a major conservation risk of relying entirely on captive breeding for an endangered species?", ["Captive breeding always increases habitat quality", "Animals may adapt to captivity or retain insufficient skills for survival after release without careful management", "Captive populations never experience genetic problems", "Release always succeeds regardless of habitat"], "B"),
        ("A protected species is recovering, but its main prey is declining because of pesticide exposure. What does this illustrate?", ["Conserving a predator never requires ecosystem-level thinking", "Prey populations cannot affect predators", "Species recovery may depend on managing wider ecological interactions and indirect threats", "Pesticides affect only plants"], "C"),
        ("Why can conservation of umbrella species sometimes help other species?", ["Umbrella species always occupy every habitat", "They have no ecological relationships", "Protecting one species guarantees the survival of all others", "Protecting their extensive habitat may also protect many co-occurring species, although benefits must be assessed"], "D"),
        ("A conservation programme records more animals after switching from ground surveys to camera traps. Why should managers be cautious when interpreting this increase?", ["The change in detection method may explain part of the difference rather than a real population increase", "Camera traps always count every animal perfectly", "Survey methods never affect results", "The population must have doubled immediately"], "A"),
        ("Why is adaptive management useful for biodiversity conservation?", ["It requires decisions never to change", "It uses monitoring and new evidence to adjust actions as conditions and outcomes change", "It removes the need for measurable objectives", "It guarantees complete certainty"], "B"),
        ("A population has enough individuals to appear stable but very low reproductive success due to inbreeding. What should conservationists investigate?", ["Only the colour of the animals", "Whether the habitat has a road sign", "Genetic health, reproductive outcomes and possible causes of reduced fitness", "Whether all individuals can be made identical"], "C"),
        ("Why can climate corridors and connected habitats become more important under climate change?", ["They prevent the climate from changing", "They stop species from dispersing", "They guarantee every species can migrate", "They may allow species to move as suitable climate conditions shift, where routes and habitats remain viable"], "D"),
        ("Which approach best assesses whether a conservation intervention caused an observed population improvement?", ["Compare suitable monitoring data over time and, where possible, use control sites or other robust comparison designs", "Assume every increase was caused by the intervention", "Use only one photograph after the project", "Ignore changes in weather, habitat and survey effort"], "A"),
        ("Why can protecting a large number of species in a single habitat be insufficient for conserving regional biodiversity?", ["All species occur in one habitat", "Different species depend on different habitats and ecological processes across a landscape", "Habitats have no effect on biodiversity", "Regional conservation never requires connectivity"], "B"),
        ("A threatened plant can survive in a botanical garden but has disappeared from the wild. Which conservation challenge remains?", ["There is no conservation challenge because plants are indoors", "The species has automatically regained its ecological role", "Its natural habitat and ecological interactions may still need restoration for successful reintroduction", "Captivity means it is no longer a species"], "C"),
        ("Why can removing an invasive species require long-term monitoring even after initial control appears successful?", ["Invasive populations never reproduce", "Monitoring is unrelated to reinvasion", "All invasive species disappear after one treatment", "Surviving individuals, seed banks or new introductions may allow the species to return"], "D"),
        ("What is one limitation of using species richness alone to measure biodiversity?", ["It does not capture all information about abundance, genetic variation or ecological differences", "It always measures genetic diversity exactly", "It provides complete information about ecosystem function", "It shows the population trend of every species"], "A"),
        ("Why can protecting a culturally important species also require attention to local communities?", ["Cultural values always conflict with conservation", "Community rights, knowledge and participation can influence whether conservation is fair and effective", "Local communities have no relationship to landscapes", "Conservation works best when nobody is consulted"], "B"),
        ("A wildlife population is divided by a highway into two groups. What is one possible long-term consequence?", ["Gene flow always increases", "The highway creates unlimited habitat", "Reduced movement may lower gene flow and increase isolation-related risks", "All individuals immediately become extinct"], "C"),
        ("Why can ecosystem-based conservation be more effective than focusing on a single species alone?", ["Single species never interact with others", "Ecosystem conservation ignores habitats", "It guarantees that all threats disappear", "It can address habitats, ecological processes and multiple interacting species together"], "D"),
        ("A reintroduction programme releases captive-bred animals into a degraded habitat. Why may the programme fail despite healthy animals?", ["The habitat may lack adequate food, shelter, breeding sites or protection from threats", "Healthy animals never need a habitat", "Captive breeding guarantees success", "Wildlife does not depend on environmental conditions"], "A"),
        ("Why should invasive-species management assess possible non-target effects?", ["Control methods never affect native species", "Some methods can harm native organisms or disrupt ecological relationships if poorly designed", "Invasive species are always beneficial", "Non-target species do not exist"], "B"),
        ("A rare species is threatened by illegal collection and habitat destruction. Which strategy best addresses both direct and habitat-related threats?", ["Only build a visitor centre", "Move every individual to a city without assessment", "Combine habitat protection, enforcement, monitoring and engagement with affected communities", "Ignore collection because the species is rare"], "C"),
        ("Why can a species' extinction risk increase after a sequence of extreme weather events even if each event is temporary?", ["Temporary events can never affect populations", "Species always recover instantly", "Weather events cannot interact with other threats", "Repeated events may reduce population size and recovery time, especially when other pressures persist"], "D"),
        ("Which approach best balances conservation and sustainable development in a biodiverse landscape?", ["Use evidence-based planning, protect critical habitats, assess trade-offs and involve affected communities", "Allow unlimited development in all habitats", "Prevent all monitoring", "Assume economic and ecological outcomes never interact"], "A"),
        ("Why is it important to distinguish correlation from causation when evaluating biodiversity trends?", ["Any two changes occurring together prove a direct cause", "Other factors may explain the observed relationship, so stronger study designs are needed", "Causation cannot be investigated scientifically", "Monitoring data never contain uncertainty"], "B"),
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

        print("\nConservation of Biodiversity expansion completed!")
        print(f"Total new questions inserted: {inserted_total}")
        print("Easy: 30 questions")
        print("Medium: 30 questions")
        print("Hard: 30 questions")
        print("Other lessons and Social Science were not modified.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()
