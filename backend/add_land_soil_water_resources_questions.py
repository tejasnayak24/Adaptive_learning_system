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


LESSON_TITLE = "Land, Soil and Water Resources"
SUBJECT = "Social Science"


QUESTION_BANK = {
    "Easy": [
        ("Which natural resource provides land for farming?", "Soil-covered land", "Petroleum", "Natural gas", "Coal", "A"),
        ("What is soil?", "A type of metal", "The upper layer of Earth's surface that supports plant growth", "A type of fuel", "A man-made plastic", "B"),
        ("Which resource is essential for drinking?", "Coal", "Iron ore", "Fresh water", "Petroleum", "C"),
        ("Which activity can cause soil erosion?", "Planting trees", "Terrace farming", "Growing grass", "Removing vegetation", "D"),
        ("Which of these is a major source of freshwater?", "Rivers", "Oceans", "Salt lakes", "Seawater", "A"),
        ("What is soil erosion?", "Formation of new mountains", "Removal of the topsoil by wind or water", "Increase in forest cover", "Storage of rainwater", "B"),
        ("Which practice helps conserve soil on slopes?", "Overgrazing", "Deforestation", "Terrace farming", "Excessive mining", "C"),
        ("Which activity helps conserve water?", "Leaving taps open", "Dumping rubbish into rivers", "Washing vehicles with running hoses", "Rainwater harvesting", "D"),
        ("Which of these is a land resource?", "A field", "A cloud", "Sunlight", "Wind", "A"),
        ("Which process occurs when rainwater flows over the ground and removes soil?", "Afforestation", "Water erosion", "Recycling", "Condensation", "B"),
        ("Which resource is needed by plants to grow?", "Plastic", "Petroleum", "Water", "Glass", "C"),
        ("Which is an example of land degradation?", "Planting trees", "Restoring wetlands", "Improving soil fertility", "Loss of soil quality due to harmful activities", "D"),
        ("Which action can help prevent soil erosion?", "Planting vegetation", "Removing all plants", "Overgrazing", "Burning forests", "A"),
        ("What is rainwater harvesting?", "Sending all rainwater into drains", "Collecting and storing rainwater", "Increasing water pollution", "Removing all ponds", "B"),
        ("Which type of water is generally suitable for drinking after appropriate treatment?", "Untreated seawater", "Polluted industrial wastewater", "Freshwater", "Water mixed with chemicals", "C"),
        ("Which human activity can pollute rivers?", "Cleaning up waste", "Planting riverbank vegetation", "Protecting wetlands", "Discharging untreated industrial waste", "D"),
        ("What does afforestation mean?", "Planting trees on land with little or no forest cover", "Removing all forests", "Building roads through forests", "Mining minerals", "A"),
        ("Which resource is often damaged by excessive grazing?", "Air", "Soil and vegetation", "Sunlight", "Tidal energy", "B"),
        ("Which of these is a water conservation method?", "Leaving leaking pipes unrepaired", "Washing pavements daily", "Repairing leaking taps", "Allowing wastewater to enter rivers", "C"),
        ("Which natural process helps replenish groundwater?", "Burning waste", "Deforestation", "Soil dumping", "Infiltration of rainwater into the ground", "D"),
        ("What is groundwater?", "Water stored beneath Earth's surface", "Water found only in clouds", "Water in the open ocean", "Water produced by factories", "A"),
        ("Which of these is a land-use activity?", "Watching clouds", "Agriculture", "Measuring sunlight", "Observing stars", "B"),
        ("Why are wetlands important?", "They always increase pollution", "They have no ecological value", "They provide habitats and help regulate water", "They eliminate all rainfall", "C"),
        ("Which is a common cause of water scarcity?", "Repairing water leaks", "Protecting watersheds", "Reusing treated water", "Excessive use of available water", "D"),
        ("What is a watershed?", "An area of land that drains water into a common outlet", "A type of mineral", "A machine for digging mines", "A method of cutting trees", "A"),
        ("Which activity can reduce groundwater recharge?", "Protecting open soil", "Covering large areas with impermeable concrete", "Planting suitable vegetation", "Building rainwater recharge pits", "B"),
        ("Which resource supports the growth of crops?", "Plastic sheets alone", "Petroleum alone", "Fertile soil", "Metal objects", "C"),
        ("Which practice is harmful to land?", "Contour ploughing", "Planting cover crops", "Afforestation", "Uncontrolled mining", "D"),
        ("Which action helps keep water bodies clean?", "Disposing of waste properly", "Dumping plastic into rivers", "Releasing untreated sewage", "Throwing chemicals into lakes", "A"),
        ("Why should natural resources be conserved?", "They have no value", "To support present and future needs", "To increase wastage", "To encourage pollution", "B"),
    ],

    "Medium": [
        ("Which combination best explains soil formation?", "Only rainfall and sunlight", "Only human activity", "Weathering of rocks and the action of organisms over time", "Only wind direction", "C"),
        ("Why is topsoil especially important for agriculture?", "It contains no nutrients", "It is always made of solid rock", "It prevents all plant growth", "It often contains nutrients and organic matter needed by plants", "D"),
        ("Which practice is most effective for reducing erosion on steep agricultural slopes?", "Terrace farming", "Removing vegetation", "Ploughing directly downhill", "Overgrazing", "A"),
        ("How do trees help reduce soil erosion?", "They make soil flow faster", "Roots help hold soil together", "They remove all soil nutrients", "They prevent all rainfall", "B"),
        ("What is water scarcity?", "A situation where water is always unlimited", "An increase in ocean salinity only", "Insufficient available water to meet needs", "A condition affecting only glaciers", "C"),
        ("Which factor can increase pressure on freshwater resources?", "Reducing leaks", "Reusing treated wastewater", "Protecting catchments", "Population growth and rising water demand", "D"),
        ("How does rainwater harvesting help communities?", "It can collect water and support groundwater recharge", "It increases the amount of plastic waste", "It prevents all evaporation", "It turns seawater into freshwater automatically", "A"),
        ("Which is a major cause of groundwater depletion?", "Repairing irrigation systems", "Pumping groundwater faster than it is replenished", "Planting trees in suitable locations", "Collecting rooftop rainwater", "B"),
        ("What can happen when excessive irrigation causes waterlogging?", "All soil becomes permanently fertile", "Groundwater disappears immediately", "Plant roots may receive insufficient oxygen", "Soil erosion becomes impossible", "C"),
        ("Which practice helps reduce water loss in agriculture?", "Flooding fields without control", "Using broken irrigation pipes", "Irrigating during strong winds only", "Drip irrigation", "D"),
        ("Why can deforestation lead to increased runoff?", "Less vegetation intercepts rainfall and holds soil", "Tree removal always increases infiltration", "Forests create no effect on water movement", "Deforestation prevents rainfall everywhere", "A"),
        ("Which method can reduce wind erosion in dry regions?", "Removing all shrubs", "Planting shelter belts", "Overgrazing grasslands", "Leaving fields bare", "B"),
        ("What is land degradation?", "A guaranteed increase in crop production", "The creation of new freshwater lakes", "A decline in the quality or productive capacity of land", "The formation of clouds", "C"),
        ("Which activity may lead to soil salinity?", "Planting trees", "Using contour bunds", "Restoring wetlands", "Poorly managed irrigation in areas with high evaporation", "D"),
        ("Why is excessive chemical use a concern for soil and water?", "It can contaminate soil and nearby water bodies", "It always improves water quality", "It prevents every type of erosion", "It eliminates all agricultural risks", "A"),
        ("What is the role of a watershed in water management?", "It prevents all rain from reaching rivers", "It collects and channels runoff toward a common outlet", "It produces groundwater without rainfall", "It is used only for mining", "B"),
        ("How can wetlands support water management?", "They always cause drought", "They prevent every flood", "They can store water and filter some pollutants", "They eliminate the need for rivers", "C"),
        ("Which option best describes sustainable land use?", "Using land without considering damage", "Removing all vegetation for short-term gain", "Allowing uncontrolled erosion", "Meeting current needs while maintaining land quality", "D"),
        ("Why can urbanization affect groundwater recharge?", "Paved surfaces can reduce water infiltration", "Concrete always increases infiltration", "Buildings create unlimited groundwater", "Roads prevent all runoff", "A"),
        ("Which action best protects a river from agricultural runoff?", "Applying chemicals immediately before heavy rain", "Maintaining vegetation along riverbanks", "Dumping unused fertilizers into streams", "Removing all buffer vegetation", "B"),
        ("What is the purpose of contour bunding?", "To increase downhill water flow", "To remove topsoil", "To slow runoff and reduce soil erosion", "To increase uncontrolled grazing", "C"),
        ("How does crop rotation help maintain soil quality?", "It guarantees that pests disappear forever", "It removes all organic matter", "It makes irrigation unnecessary in every case", "It can improve nutrient management and break some pest cycles", "D"),
        ("Which is an example of watershed conservation?", "Protecting vegetation and controlling erosion in the drainage area", "Dumping rubbish into streams", "Removing every tree from slopes", "Allowing untreated sewage into reservoirs", "A"),
        ("Why is untreated sewage harmful to freshwater ecosystems?", "It always increases oxygen levels", "It can introduce pathogens and increase organic pollution", "It makes all water safe to drink", "It prevents algal growth in every case", "B"),
        ("Which approach can improve the sustainability of groundwater use?", "Pumping continuously without measurement", "Filling recharge areas with concrete", "Monitoring extraction and supporting recharge", "Ignoring local water demand", "C"),
        ("What is a likely effect of mining without proper restoration?", "Guaranteed soil improvement", "Increased natural vegetation everywhere", "Elimination of waste", "Land disturbance and possible water contamination", "D"),
        ("Which combination is most likely to conserve both soil and water?", "Cover crops and efficient irrigation", "Deforestation and excessive pumping", "Overgrazing and uncontrolled runoff", "Dumping waste into waterways", "A"),
        ("Why is soil organic matter useful?", "It makes soil unable to hold water", "It can improve soil structure and nutrient availability", "It eliminates all soil organisms", "It prevents plants from absorbing nutrients", "B"),
        ("Which statement about freshwater is correct?", "All water on Earth is readily drinkable", "Ocean water can always be consumed untreated", "Only a limited portion of Earth's water is readily accessible freshwater", "Water pollution has no effect on availability", "C"),
        ("What is the main benefit of protecting catchment vegetation?", "It guarantees no floods can occur", "It stops all rainfall", "It removes the need for water treatment", "It can reduce erosion and help regulate runoff", "D"),
    ],

    "Hard": [
        ("A hillside farm loses fertile topsoil after heavy rain. Which combination best addresses the underlying problem?", "Contour farming, vegetation cover, and terracing where suitable", "Removing trees and increasing slope length", "Ploughing downhill and leaving soil bare", "Increasing uncontrolled grazing", "A"),
        ("A town replaces open ground with roads and concrete. What is one likely hydrological effect?", "Groundwater recharge always increases", "Infiltration may decrease while surface runoff increases", "Rainfall immediately stops", "Water pollution becomes impossible", "B"),
        ("A village extracts groundwater faster than its aquifer is replenished. Which policy is most appropriate?", "Encourage unlimited pumping", "Ignore well levels", "Monitor extraction and improve recharge and water efficiency", "Seal all rainwater collection systems", "C"),
        ("A farmer uses excessive irrigation in an area with poor drainage. Which problem may develop?", "Permanent elimination of soil salts", "Unlimited crop growth", "Guaranteed groundwater recharge", "Waterlogging and soil salinity", "D"),
        ("Which explanation best connects deforestation with downstream sedimentation?", "Loss of vegetation increases erosion, allowing more sediment to enter rivers", "Tree removal prevents all soil movement", "Forests have no influence on runoff", "Deforestation removes sediment from rivers", "A"),
        ("A community wants to reduce dependence on seasonal rainfall. Which strategy is most suitable?", "Increase water wastage", "Combine rainwater harvesting, storage, and efficient use", "Remove vegetation from catchments", "Pollute local ponds", "B"),
        ("Why can excessive groundwater withdrawal cause wells to dry up?", "Groundwater cannot move underground", "Aquifers are always replenished instantly", "The water table may fall below the depth of wells", "Pumping creates additional water", "C"),
        ("A river receives fertilizer-rich runoff from farms. What environmental issue may result?", "Permanent elimination of algae", "Unlimited drinking water", "No change in aquatic life", "Nutrient pollution and possible eutrophication", "D"),
        ("Which land-management choice best reduces erosion while supporting farming on slopes?", "Contour cultivation with appropriate vegetation strips", "Clearing the slope before every rainy season", "Ploughing straight downhill", "Increasing livestock pressure on bare land", "A"),
        ("A watershed has lost much of its tree cover. Which restoration approach is most likely to improve its resilience?", "Expand dumping sites near streams", "Restore suitable vegetation and control erosion", "Pave all remaining open land", "Remove natural streamside plants", "B"),
        ("Why may a region with substantial rainfall still experience water scarcity?", "Rainfall always guarantees safe drinking water", "All rainfall enters aquifers immediately", "Seasonal distribution, storage limits, pollution, and demand affect availability", "Water demand has no effect on scarcity", "C"),
        ("Which is the strongest reason to treat wastewater before releasing it into rivers?", "Treatment makes rivers unnecessary", "It eliminates all water needs", "Untreated sewage always improves ecosystems", "Treatment can reduce pathogens and pollutant loads", "D"),
        ("A mining company restores vegetation and stabilizes exposed soil after extraction. Which principle does this demonstrate?", "Rehabilitation of disturbed land", "Uncontrolled resource depletion", "Groundwater over-extraction", "Urban heat island formation", "A"),
        ("Which measure best reduces soil erosion caused by strong winds across open agricultural land?", "Remove crop residues", "Maintain ground cover and establish suitable shelter belts", "Increase overgrazing", "Leave all fields bare", "B"),
        ("A farmer changes from flood irrigation to well-managed drip irrigation. What is the main expected benefit?", "It guarantees no crop diseases", "It makes rainfall unnecessary", "It can deliver water more directly to plant roots and reduce losses", "It increases water use in every situation", "C"),
        ("Which combination can improve both soil fertility and erosion control?", "Removing crop residues and burning all vegetation", "Overgrazing and continuous bare fallow", "Excessive tillage and downhill ploughing", "Adding suitable organic matter and maintaining protective cover", "D"),
        ("Why should groundwater quality be monitored alongside groundwater quantity?", "Contamination can make available groundwater unsafe or costly to use", "Quantity is the only factor that matters", "Pollutants cannot enter aquifers", "Monitoring automatically removes every contaminant", "A"),
        ("A city protects wetlands near a river. Which combination of benefits is most plausible?", "Guaranteed prevention of every natural disaster", "Water storage, habitat support, and filtration of some pollutants", "Unlimited production of drinking water without treatment", "Complete elimination of drought", "B"),
        ("Which situation best illustrates an external cost of poor land management?", "A farmer improves soil structure", "A village repairs leaking pipes", "Erosion from one farm deposits sediment in a shared reservoir", "A community protects a catchment", "C"),
        ("A district plans new housing over an important recharge zone. What should planners assess first?", "Only the colour of building materials", "Only the number of roads", "Only the height of nearby buildings", "Effects on infiltration, runoff, groundwater, and local water demand", "D"),
        ("Which approach best supports long-term water security in an agricultural region?", "Combine demand management, efficient irrigation, recharge, and monitoring", "Increase pumping without limits", "Allow all wastewater into streams", "Remove vegetation from riverbanks", "A"),
        ("Why can planting trees alone fail to solve every soil erosion problem?", "Trees never help soil", "Appropriate species, slope conditions, land use, and complementary practices also matter", "Soil erosion is always unrelated to vegetation", "Tree planting increases erosion in every situation", "B"),
        ("A reservoir fills with sediment after years of erosion in its catchment. Which action addresses the source of the problem?", "Increase deforestation upstream", "Remove all ground cover", "Reduce catchment erosion through vegetation and soil conservation", "Increase uncontrolled hillside cultivation", "C"),
        ("Which practice is most consistent with integrated watershed management?", "Manage each resource without considering the others", "Focus only on downstream water supply", "Ignore land use and community needs", "Coordinate soil, vegetation, water, and local land-use management", "D"),
        ("A farmer applies fertilizer just before heavy rain. Why is this risky?", "Rain can carry nutrients into nearby water bodies", "Rain makes fertilizer permanently harmless", "Nutrients cannot move with runoff", "The practice guarantees better water quality", "A"),
        ("Which statement best describes the relationship between land and water resources?", "They are independent in all natural systems", "Land use influences runoff, infiltration, erosion, and water quality", "Water has no effect on land", "Soil cannot influence water storage", "B"),
        ("A village restores a traditional pond and protects its catchment. Which outcome is reasonably possible?", "The village will never face drought again", "All water becomes potable without treatment", "Local water storage and recharge may improve", "Groundwater use becomes unnecessary everywhere", "C"),
        ("Why is sustainable land use important for future food security?", "Soil quality is unrelated to crop production", "Land resources are always unlimited", "Erosion increases fertile topsoil everywhere", "Maintaining soil productivity supports continued agricultural production", "D"),
        ("Which indicator would best help identify excessive groundwater extraction over time?", "Repeated measurements of groundwater levels and pumping rates", "The colour of nearby buildings", "The number of roads alone", "Daily air temperature alone", "A"),
        ("Which overall strategy best reflects sustainable management of land, soil, and water?", "Maximize extraction regardless of environmental effects", "Use resources efficiently, prevent degradation, and monitor environmental impacts", "Replace all natural ecosystems with concrete", "Ignore community needs and future availability", "B"),
    ],
}


def shuffle_options(question_data):
    question, a, b, c, d, correct = question_data

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
            print("Check the lesson title and subject in the database.")
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

            existing = (
                db.query(Question)
                .filter(Question.quiz_id == quiz.id)
                .all()
            )

            existing_texts = {
                q.question.strip().casefold()
                for q in existing
            }

            for item in bank:
                if item[0].strip().casefold() in existing_texts:
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

                existing_texts.add(q.strip().casefold())
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
            print("WARNING: The lesson does not yet contain 90 questions.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()