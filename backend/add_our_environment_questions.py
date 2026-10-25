import os
import sys
import random
import logging
from pathlib import Path

logging.disable(logging.CRITICAL)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "adaptive_learning.db"

os.environ["DATABASE_URL"] = f"sqlite:///{DATABASE_PATH.as_posix()}"
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from app.database.connection import SessionLocal
from app.models.student import Student
from app.models.lesson import Lesson
from app.models.quiz import Quiz
from app.models.question import Question
from app.models.progress import Progress
from app.models.session import LearningSession
from app.models.reward import RewardHistory


LESSON_TITLE = "Our Environment"
SUBJECT = "Social Science"


QUESTION_BANK = {
    "Easy": [
        ("What is the environment?", "The surroundings in which living things exist", "Only buildings", "Only vehicles", "Only computers", "A"),
        ("Which of these is a living component of the environment?", "Rock", "Tree", "Water", "Air", "B"),
        ("Which of these is a non-living component?", "Bird", "Fish", "Water", "Grass", "C"),
        ("What do green plants use to make food?", "Only soil", "Only oxygen", "Only minerals", "Sunlight, water, and carbon dioxide", "D"),
        ("Which gas do plants absorb during photosynthesis?", "Carbon dioxide", "Nitrogen only", "Helium", "Hydrogen", "A"),
        ("Which gas do humans need for respiration?", "Carbon dioxide", "Oxygen", "Methane", "Neon", "B"),
        ("What is a habitat?", "A type of pollution", "A weather instrument", "The natural home of an organism", "A manufactured product", "C"),
        ("Which organism is a producer in a food chain?", "Lion", "Eagle", "Frog", "Green plant", "D"),
        ("Which organism is a consumer?", "Deer", "Grass", "Algae", "A green plant", "A"),
        ("What is pollution?", "The natural growth of plants", "The introduction of harmful substances or energy into the environment", "The conservation of forests", "The recycling of paper", "B"),
        ("Which activity can reduce plastic pollution?", "Throwing plastic into rivers", "Burning plastic in open spaces", "Reusing suitable items and reducing disposable plastics", "Leaving plastic in forests", "C"),
        ("Which of these is a natural resource?", "Plastic bottle", "Concrete road", "Mobile phone", "Water", "D"),
        ("What is biodiversity?", "The variety of living organisms in an area", "The number of roads in a city", "The amount of plastic produced", "The number of buildings", "A"),
        ("Which action helps protect forests?", "Cutting all trees", "Planting trees and preventing unnecessary deforestation", "Setting forests on fire", "Dumping waste in forests", "B"),
        ("Which of these is a renewable energy source?", "Coal", "Petroleum", "Sunlight", "Natural gas", "C"),
        ("Which of these is a non-renewable energy source?", "Wind", "Sunlight", "Tidal energy", "Coal", "D"),
        ("What is a food chain?", "A sequence showing how energy passes between organisms", "A list of restaurants", "A type of road network", "A method of manufacturing plastic", "A"),
        ("Which organisms break down dead plants and animals?", "Producers only", "Decomposers", "Herbivores only", "Carnivores only", "B"),
        ("Which of these is a decomposer?", "Tiger", "Eagle", "Fungus", "Deer", "C"),
        ("What is global warming?", "The cooling of every region", "The daily change in weather", "The movement of ocean waves", "The long-term rise in Earth's average surface temperature", "D"),
        ("Which human activity can increase air pollution?", "Burning fossil fuels", "Planting trees", "Using public transport", "Protecting forests", "A"),
        ("What is recycling?", "Dumping waste in rivers", "Processing used materials to make usable products", "Burning all rubbish", "Leaving rubbish in public spaces", "B"),
        ("Which of these is a water-pollution source?", "Rainwater harvesting", "Wetland restoration", "Untreated sewage", "Cleaning a riverbank", "C"),
        ("Why are trees important to the environment?", "They increase all forms of pollution", "They have no effect on soil", "They prevent every natural disaster", "They provide habitats and absorb carbon dioxide as they grow", "D"),
        ("Which of these is an example of solid waste?", "An empty plastic bottle", "Clean air", "Sunlight", "Wind", "A"),
        ("What does conservation mean?", "Using every resource immediately", "Protecting and managing resources carefully", "Increasing pollution", "Destroying habitats", "B"),
        ("Which of these is an ecosystem?", "A single manufactured object", "A pile of plastic", "A pond containing organisms and their physical surroundings", "An empty classroom", "C"),
        ("What is the main purpose of a national park?", "To encourage uncontrolled hunting", "To remove all wildlife", "To increase deforestation", "To protect natural habitats and wildlife", "D"),
        ("Which practice helps save electricity?", "Switching off unused lights", "Leaving appliances running unnecessarily", "Keeping every light on all day", "Using damaged electrical equipment", "A"),
        ("Why should we protect the environment?", "It has no effect on humans", "It supports life, health, and natural resources", "It is unrelated to future generations", "It only benefits wild animals", "B"),
    ],

    "Medium": [
        ("What is an ecosystem?", "Only the animals in a forest", "Only the soil in a field", "Living organisms interacting with one another and their physical surroundings", "Only the climate of a region", "C"),
        ("What is the main source of energy for most ecosystems?", "The Moon", "Earth's core", "Fossil fuels only", "The Sun", "D"),
        ("Which statement best describes a food web?", "A network of interconnected food chains", "A single organism's habitat", "A list of non-living things", "A type of pollution", "A"),
        ("What is the role of producers in an ecosystem?", "They consume every other organism", "They make organic food using an energy source such as sunlight", "They only decompose dead matter", "They prevent energy transfer", "B"),
        ("Why are decomposers important?", "They stop nutrient cycling", "They produce plastic naturally", "They break down dead material and return nutrients to ecosystems", "They remove all soil nutrients", "C"),
        ("What may happen if a major predator disappears from an ecosystem?", "All populations remain unchanged in every case", "Producers immediately disappear", "Energy stops entering the ecosystem", "Prey populations and other food-web relationships may change", "D"),
        ("What is the greenhouse effect?", "Warming caused when certain atmospheric gases absorb and re-emit infrared radiation", "The blocking of all sunlight by plants", "The cooling of Earth by coal", "The movement of tectonic plates", "A"),
        ("Which gas is a major contributor to human-caused global warming?", "Helium", "Carbon dioxide", "Neon", "Argon", "B"),
        ("How does deforestation contribute to climate change?", "It always increases carbon storage", "It eliminates greenhouse gases", "It releases stored carbon and reduces future carbon absorption as forests are lost", "It stops all weather changes", "C"),
        ("Which practice helps reduce household waste?", "Buying unnecessary disposable items", "Throwing reusable objects away", "Mixing all waste without sorting", "Reducing consumption, reusing items, and recycling suitable materials", "D"),
        ("What is eutrophication?", "Excess nutrient enrichment of water that can cause algal blooms and oxygen depletion", "The natural formation of mountains", "The cooling of ocean water by wind", "The removal of every nutrient from soil", "A"),
        ("Which is a major source of nutrient pollution in water?", "Planting trees far from rivers", "Fertilizer runoff from agricultural land", "Using a reusable water bottle", "Protecting wetlands", "B"),
        ("Why is biodiversity important for ecosystem stability?", "All species perform exactly the same role", "Biodiversity has no ecological value", "Different organisms contribute to ecological processes and resilience", "It prevents all environmental change", "C"),
        ("What is an invasive species?", "A native species living in its natural habitat", "A species that is always endangered", "A species that cannot reproduce", "A species introduced outside its native range that spreads and causes harm", "D"),
        ("How can wetlands help the environment?", "They can provide habitats, store water, and filter some pollutants", "They always increase water pollution", "They have no role in flood regulation", "They prevent all rainfall", "A"),
        ("What is sustainable development?", "Development that ignores future generations", "Meeting present needs without compromising future generations' ability to meet theirs", "Using all resources immediately", "Stopping every economic activity", "B"),
        ("Which action can reduce transport-related emissions?", "Driving alone for every journey", "Leaving vehicle engines running unnecessarily", "Using public transport where practical", "Increasing unnecessary journeys", "C"),
        ("Why is ozone in the stratosphere important?", "It produces all Earth's oxygen", "It eliminates all pollution", "It prevents all climate change", "It absorbs much of the Sun's harmful ultraviolet radiation", "D"),
        ("Which human-made chemicals have historically contributed to stratospheric ozone depletion?", "Chlorofluorocarbons (CFCs)", "Oxygen", "Nitrogen in the air", "Water vapour alone", "A"),
        ("What is biomagnification?", "A decrease in every pollutant at higher trophic levels", "An increase in the concentration of certain persistent pollutants at higher trophic levels", "The growth of plants in sunlight", "The recycling of organic waste", "B"),
        ("Why can plastic waste harm marine animals?", "Plastic always dissolves immediately", "It provides unlimited safe food", "Animals may ingest plastic or become entangled in it", "It increases oxygen in all oceans", "C"),
        ("What is an ecological footprint intended to estimate?", "Only the number of species in a forest", "Only the amount of rainfall", "Only the size of a house", "Human demand on ecological resources and ecosystem services", "D"),
        ("Which is an example of in-situ conservation?", "Protecting wildlife in its natural habitat within a national park", "Keeping seeds only in a laboratory", "Storing animal specimens in a museum", "Growing plants only in a laboratory", "A"),
        ("Which is an example of ex-situ conservation?", "Protecting a forest in its natural location", "Conserving seeds in a seed bank", "Protecting a wetland in place", "Establishing a marine protected area in the ocean", "B"),
        ("Why is untreated industrial wastewater dangerous?", "It always improves aquatic ecosystems", "It contains no harmful substances", "It may introduce toxic chemicals and other pollutants into water", "It automatically becomes drinking water", "C"),
        ("What is the purpose of an environmental impact assessment?", "To guarantee that every project has no impact", "To eliminate the need for planning", "To measure only construction costs", "To identify and evaluate likely environmental effects before a decision", "D"),
        ("How can composting benefit waste management?", "It can convert suitable organic waste into a useful soil amendment", "It turns plastic into fresh water", "It eliminates every kind of waste", "It increases the amount of untreated sewage", "A"),
        ("Which practice helps conserve water at home?", "Leaving leaking taps unrepaired", "Repairing leaks and using water efficiently", "Keeping taps open while brushing", "Washing small items under continuously running water", "B"),
        ("Why are pollinators important in many ecosystems and farms?", "They eliminate the need for all plants", "They cause every crop to fail", "They help many plants reproduce by transferring pollen", "They prevent all insect activity", "C"),
        ("Which approach best supports environmental protection?", "Rely only on cleaning up after pollution", "Ignore scientific evidence", "Use resources without monitoring", "Combine prevention, conservation, regulation, and public participation", "D"),
    ],

    "Hard": [
        ("A lake receives excess nutrients from farms and develops frequent algal blooms. What is the most direct long-term response?", "Reduce nutrient runoff through improved fertilizer management and wastewater treatment", "Add more fertilizer to the lake", "Remove all aquatic plants permanently", "Increase untreated sewage discharge", "A"),
        ("Why can the loss of one keystone species affect an entire ecosystem?", "Every species is completely independent", "Its ecological role can influence many other populations and interactions", "It always increases biodiversity", "It prevents all food-web changes", "B"),
        ("A forest is cleared and burned for agriculture. Which combination of effects is plausible?", "Carbon emissions must fall and biodiversity must rise", "Soil erosion becomes impossible", "Carbon can be released, habitats can be lost, and erosion risk can increase", "The water cycle stops globally", "C"),
        ("Why can persistent pollutants become more concentrated in organisms at higher trophic levels?", "All pollutants disappear immediately", "Predators never consume other organisms", "Energy transfer increases pollutant breakdown in every case", "Some persistent pollutants accumulate in organisms and are transferred through food chains", "D"),
        ("A city experiences high summer temperatures and extensive paved surfaces. Which approach could help reduce the urban heat island effect?", "Increase tree cover and green spaces where suitable", "Remove parks and trees", "Cover every open area with dark pavement", "Eliminate urban vegetation", "A"),
        ("Why is life-cycle assessment useful when comparing products?", "It measures only the product's colour", "It considers environmental impacts across stages such as material extraction, production, use, and disposal", "It guarantees a product has zero impact", "It ignores raw materials", "B"),
        ("A wetland is drained to build housing. Which potential environmental consequence should planners consider?", "Wetlands have no ecological functions", "Flood risk must disappear", "Loss of habitat, water storage, and some natural filtration functions", "Biodiversity must increase in every case", "C"),
        ("Why can an apparently renewable resource still be depleted?", "Renewable resources cannot be damaged", "They are always available without limits", "All renewable resources renew instantly", "The rate of use can exceed the rate of natural replenishment", "D"),
        ("Which strategy best reduces greenhouse-gas emissions from electricity generation?", "Increase energy efficiency and shift toward lower-emission energy sources", "Burn more coal without pollution controls", "Waste electricity deliberately", "Expand fossil-fuel use without considering alternatives", "A"),
        ("A protected area is isolated by roads and development. Why might wildlife corridors be useful?", "They stop all animal movement", "They can help connect habitats and allow some species to move between them", "They eliminate every human-wildlife conflict", "They make habitat quality irrelevant", "B"),
        ("Why is the precautionary principle relevant to environmental management?", "It requires ignoring every new risk", "It proves that all development is harmful", "It supports taking proportionate preventive action when credible risks exist despite scientific uncertainty", "It eliminates the need for evidence", "C"),
        ("A river has low dissolved oxygen after receiving large amounts of organic waste. What is a likely explanation?", "Organic waste always increases oxygen", "Fish produce unlimited oxygen", "Water temperature has no effect on oxygen", "Microorganisms decomposing the waste consume dissolved oxygen", "D"),
        ("Which approach best addresses both biodiversity loss and the needs of local communities?", "Conservation planning that protects habitats and involves affected communities", "Exclude communities from every decision", "Allow uncontrolled habitat destruction", "Focus only on short-term extraction", "A"),
        ("Why can replacing a diverse natural forest with a single-species plantation reduce biodiversity?", "Plantations always contain more species", "The simplified habitat may support fewer kinds of organisms than the natural forest", "Tree species have no ecological role", "Biodiversity is unrelated to habitat structure", "B"),
        ("A city separates organic waste and sends it to a managed composting facility. Which benefit is plausible?", "All waste streams become harmless automatically", "Plastic waste is converted into metal", "Organic waste can become compost and less waste may go to landfill", "Composting eliminates the need to manage contamination", "C"),
        ("Why is environmental monitoring important after an industrial project begins operating?", "Environmental effects can never change after approval", "Monitoring is useful only before construction", "Pollution levels never vary", "It helps identify actual impacts and whether controls are working", "D"),
        ("Which explanation best connects biodiversity to food security?", "Biodiversity supports ecosystem services such as pollination, soil processes, and genetic diversity", "Biodiversity has no connection to farming", "Every crop depends on only one organism", "Biodiversity prevents all crop diseases", "A"),
        ("A community relies on a forest for fuelwood and livelihoods. Which management approach is most likely to be sustainable?", "Ban every use without considering local needs", "Set locally appropriate harvesting rules and support regeneration and alternative livelihoods", "Encourage unrestricted tree cutting", "Replace the forest with a waste dump", "B"),
        ("Why can climate change increase some ecosystem risks even when annual rainfall remains similar?", "Rainfall totals alone determine all ecological outcomes", "Temperature has no effect on species", "Changes in rainfall timing, extremes, and temperature can affect species and water availability", "Ecosystems are unaffected by seasonal conditions", "C"),
        ("Which approach is most suitable for evaluating whether a city is becoming more sustainable?", "Measure only the number of buildings", "Measure only total population", "Ignore waste and energy use", "Assess multiple indicators such as emissions, transport, waste, water, and green space", "D"),
        ("Why can uncontrolled introduction of non-native species be risky?", "Some introduced species can spread, compete with native species, or alter ecosystems", "All introduced species are harmless", "Non-native species never reproduce", "Native species cannot be affected", "A"),
        ("A company claims a product is environmentally friendly because its packaging is recyclable. What is the best assessment?", "Recyclable packaging proves the entire product has no impact", "The full life cycle, actual recyclability, material use, and disposal conditions should be assessed", "Packaging is the only environmental factor", "Recycling labels eliminate the need for evidence", "B"),
        ("Which action best reduces the risk of plastic entering rivers from urban areas?", "Increase littering near drains", "Remove all street bins", "Improve waste collection, secure disposal, and prevent litter from entering storm drains", "Send plastic waste directly into streams", "C"),
        ("Why is habitat fragmentation a conservation concern?", "It always increases gene flow", "It creates identical conditions everywhere", "It prevents all edge effects", "It can isolate populations and reduce movement between habitats", "D"),
        ("A region is considering a dam. Which set of issues should a thorough environmental assessment examine?", "River ecology, sediment movement, communities, water supply, and downstream effects", "Construction cost alone", "Only the colour of the dam", "Only the number of nearby roads", "A"),
        ("Which statement about carbon sinks is most accurate?", "Carbon sinks create unlimited carbon-free energy", "Forests and oceans can absorb carbon, but their capacity and condition can change", "Carbon sinks have no role in climate", "Every forest absorbs exactly the same amount of carbon forever", "B"),
        ("Why can environmental justice be relevant to pollution control?", "Pollution affects every community identically in every situation", "Environmental risks have no social dimension", "Pollution burdens and access to environmental benefits can be unevenly distributed", "Only wildlife can be affected by pollution", "C"),
        ("A city improves public transport, walking paths, and cycling infrastructure. Which combined benefit is plausible?", "It guarantees that no one will drive", "It eliminates every traffic accident", "It makes urban planning unnecessary", "It can reduce some vehicle trips, emissions, and transport-related pollution", "D"),
        ("Why should environmental policies include measurable targets and regular review?", "They help assess progress and adapt measures when evidence or conditions change", "Targets make monitoring unnecessary", "Policies can never need revision", "Review prevents public participation", "A"),
        ("Which statement best summarizes ecosystem resilience?", "An ecosystem can never be disturbed", "The ability of an ecosystem to withstand or recover from disturbances depends partly on its structure, diversity, and condition", "Every ecosystem recovers at the same rate", "Resilience means pollution has no effect", "B"),
    ],
}


# Validate the question bank before touching the database.
for difficulty, bank in QUESTION_BANK.items():
    if len(bank) != 30:
        raise ValueError(
            f"{difficulty} must contain 30 questions; found {len(bank)}."
        )

    for index, item in enumerate(bank, start=1):
        if len(item) != 6:
            raise ValueError(
                f"{difficulty} question #{index} has {len(item)} values: "
                f"{item[0]}"
            )

        if item[5] not in {"A", "B", "C", "D"}:
            raise ValueError(
                f"Invalid correct answer in {difficulty} question #{index}."
            )


def shuffle_options(item):
    question, a, b, c, d, correct = item

    options = {
        "A": a,
        "B": b,
        "C": c,
        "D": d,
    }

    correct_text = options[correct]
    shuffled = list(options.values())
    random.shuffle(shuffled)

    return (
        question,
        shuffled[0],
        shuffled[1],
        shuffled[2],
        shuffled[3],
        "ABCD"[shuffled.index(correct_text)],
    )


def main():
    db = SessionLocal()

    try:
        lesson = (
            db.query(Lesson)
            .filter(
                Lesson.title == LESSON_TITLE,
                Lesson.topic == SUBJECT,
            )
            .first()
        )

        if not lesson:
            print(f"ERROR: Lesson '{LESSON_TITLE}' was not found.")
            print("No questions were added.")
            return

        added = 0

        for difficulty, bank in QUESTION_BANK.items():
            quiz = (
                db.query(Quiz)
                .filter(
                    Quiz.lesson_id == lesson.id,
                    Quiz.difficulty == difficulty,
                )
                .first()
            )

            if not quiz:
                quiz = Quiz(
                    lesson_id=lesson.id,
                    title=f"{LESSON_TITLE} - {difficulty} Quiz",
                    difficulty=difficulty,
                )
                db.add(quiz)
                db.flush()

            existing_questions = (
                db.query(Question)
                .filter(Question.quiz_id == quiz.id)
                .all()
            )

            existing_texts = {
                q.question.strip().casefold()
                for q in existing_questions
            }

            for item in bank:
                question_key = item[0].strip().casefold()

                if question_key in existing_texts:
                    continue

                q, a, b, c, d, correct = shuffle_options(item)

                db.add(
                    Question(
                        quiz_id=quiz.id,
                        question=q,
                        option_a=a,
                        option_b=b,
                        option_c=c,
                        option_d=d,
                        correct_answer=correct,
                    )
                )

                existing_texts.add(question_key)
                added += 1

        db.commit()

        print("\nFINAL VERIFICATION")
        print(f"Lesson: {LESSON_TITLE}")
        print(f"Subject: {SUBJECT}")

        total = 0

        for difficulty in ["Easy", "Medium", "Hard"]:
            quiz = (
                db.query(Quiz)
                .filter(
                    Quiz.lesson_id == lesson.id,
                    Quiz.difficulty == difficulty,
                )
                .first()
            )

            count = (
                db.query(Question)
                .filter(Question.quiz_id == quiz.id)
                .count()
                if quiz
                else 0
            )

            total += count
            print(f"{difficulty}: {count}/30")

        print(f"TOTAL: {total}/90")
        print(f"New questions added: {added}")

        if total == 90:
            print("SUCCESS: All 90 questions are present!")
        else:
            print("WARNING: The total is not 90. Check the counts above.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()