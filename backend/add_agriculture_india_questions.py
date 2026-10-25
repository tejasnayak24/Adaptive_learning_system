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


LESSON_TITLE = "Agriculture in India"
SUBJECT = "Social Science"


QUESTION_BANK = {
    "Easy": [
        ("What is agriculture?", "Growing crops and raising livestock", "Building roads only", "Mining minerals only", "Manufacturing computers only", "A"),
        ("Which crop is commonly grown during the Kharif season?", "Wheat", "Rice", "Mustard", "Peas", "B"),
        ("Which crop is commonly associated with the Rabi season?", "Jute", "Cotton", "Wheat", "Rice", "C"),
        ("Which of these is a food crop?", "Rubber", "Cotton", "Tea", "Rice", "D"),
        ("Which crop is widely grown in India as a fibre crop?", "Cotton", "Wheat", "Rice", "Lentils", "A"),
        ("Which of these is a plantation crop?", "Wheat", "Tea", "Gram", "Millet", "B"),
        ("Which resource is essential for crop growth?", "Plastic", "Iron", "Water", "Glass", "C"),
        ("Which tool is traditionally used to loosen soil?", "Television", "Refrigerator", "Telephone", "Plough", "D"),
        ("What is irrigation?", "Supplying water to crops artificially", "Harvesting fish from oceans", "Cutting forests", "Transporting minerals", "A"),
        ("Which animal is commonly raised for milk?", "Tiger", "Cow", "Lion", "Wolf", "B"),
        ("Which crop is commonly used to produce sugar?", "Tea", "Cotton", "Sugarcane", "Jute", "C"),
        ("Which of these is a pulse crop?", "Cotton", "Tea", "Sugarcane", "Gram", "D"),
        ("What is harvesting?", "Collecting mature crops", "Preparing a road", "Digging for coal", "Planting a forest", "A"),
        ("Which crop grows well in warm conditions with adequate water?", "Apple in every climate", "Rice", "Barley only in deserts", "Tea without water", "B"),
        ("Which of these is an agricultural activity?", "Building a bridge", "Extracting petroleum", "Growing vegetables", "Manufacturing phones", "C"),
        ("Which crop is an important source of edible oil?", "Jute", "Cotton", "Tea", "Groundnut", "D"),
        ("What is livestock farming?", "Raising animals for useful products", "Growing only forest trees", "Mining coal", "Building dams", "A"),
        ("Which of these is a cash crop?", "Wheat grown only for household use", "Cotton", "Wild grass", "Forest moss", "B"),
        ("Which factor strongly influences agriculture?", "The colour of farm buildings", "The number of television channels", "Climate", "The shape of mobile phones", "C"),
        ("Which crop is commonly used to make fabric fibres?", "Rice", "Wheat", "Gram", "Cotton", "D"),
        ("What is ploughing?", "Turning and loosening the soil", "Collecting finished products from shops", "Packing tea leaves", "Transporting livestock by train", "A"),
        ("Which of these is a farming input?", "A cinema ticket", "Fertilizer", "A television programme", "A plastic toy", "B"),
        ("Which crop is commonly grown in flooded or water-rich fields?", "Cactus", "Mustard in all conditions", "Rice", "Olive in every region", "C"),
        ("What is sowing?", "Selling farm machinery", "Cleaning a river", "Storing harvested grain", "Placing seeds in soil for growth", "D"),
        ("Which of these is a horticultural activity?", "Growing fruits and vegetables", "Mining iron ore", "Manufacturing cars", "Building airports", "A"),
        ("Which of these is a natural factor affecting farming?", "Mobile phone design", "Rainfall", "Internet speed", "Cinema attendance", "B"),
        ("Which crop is commonly grown for beverages?", "Gram", "Wheat", "Tea", "Millet", "C"),
        ("What is manure commonly used for?", "Making roads", "Producing metal", "Cleaning machinery only", "Adding organic matter and nutrients to soil", "D"),
        ("Which of these is a cereal crop?", "Maize", "Cotton", "Tea", "Rubber", "A"),
        ("Why is agriculture important to India?", "It has no connection to livelihoods", "It supports food supply and many people's livelihoods", "It is unrelated to industry", "It uses no natural resources", "B"),
    ],

    "Medium": [
        ("What mainly distinguishes Kharif crops from Rabi crops?", "Kharif crops are grown only in winter", "Rabi crops always need flooding", "Their usual growing seasons differ", "They are all plantation crops", "C"),
        ("Which crop is generally sown with the onset of the monsoon and harvested in autumn?", "Wheat", "Mustard", "Gram", "Rice", "D"),
        ("Which crop is commonly grown during the winter Rabi season?", "Wheat", "Jute", "Rice in every region", "Cotton only", "A"),
        ("Why is the monsoon important for Indian agriculture?", "It removes the need for soil", "Rainfall provides water for many crops", "It guarantees the same yield everywhere", "It prevents all agricultural risks", "B"),
        ("Which combination is most important for successful crop production?", "Only attractive packaging", "Only farm size", "Suitable soil, water, climate, and farming practices", "Only the distance from a city", "C"),
        ("What is subsistence farming?", "Farming exclusively for global export", "Growing only flowers for decoration", "Producing only industrial chemicals", "Farming mainly to meet the farmer's household needs", "D"),
        ("What is commercial farming?", "Producing crops or livestock mainly for sale", "Growing crops only for family consumption", "Farming without any products", "Collecting only wild plants", "A"),
        ("Which is a characteristic of intensive subsistence farming?", "Using land only for grazing wild animals", "Cultivating small plots intensively to obtain high output", "Producing only for export on huge estates", "Avoiding all agricultural labour", "B"),
        ("Which crop is commonly associated with black soil in parts of India?", "Tea", "Jute", "Cotton", "Apple", "C"),
        ("Why is alluvial soil important in many agricultural regions?", "It is always infertile", "It cannot support crops", "It contains no mineral particles", "It is often fertile and suitable for cultivation", "D"),
        ("Which crop is commonly grown in regions with warm temperatures and suitable rainfall for its long growing season?", "Sugarcane", "Barley in every climate", "Apple in all plains", "Saffron in every state", "A"),
        ("What is mixed farming?", "Growing only one crop forever", "Combining crop cultivation with livestock rearing", "Mining and manufacturing only", "Fishing without any crop production", "B"),
        ("Which agricultural practice helps maintain soil fertility?", "Growing the same nutrient-demanding crop continuously without management", "Removing all organic matter", "Crop rotation", "Burning all soil organisms", "C"),
        ("What is the purpose of using fertilizers?", "To make soil unnecessary", "To prevent all pests permanently", "To replace rainfall", "To supply nutrients needed by crops", "D"),
        ("Which practice can help reduce water use in agriculture?", "Drip irrigation", "Flooding fields without control", "Leaving irrigation leaks unrepaired", "Watering crops excessively", "A"),
        ("Why is agricultural mechanization used?", "To eliminate the need for planning", "To improve efficiency and reduce some labour requirements", "To make all crops grow without water", "To remove the need for skilled operators", "B"),
        ("What is a major risk of excessive pesticide use?", "Guaranteed improvement of biodiversity", "Complete elimination of crop disease forever", "Harm to beneficial organisms and environmental contamination", "Automatic improvement of soil structure", "C"),
        ("Why do farmers use crop diversification?", "To ensure only one crop is ever harvested", "To eliminate the need for markets", "To stop all seasonal variation", "To spread risk and use resources more effectively", "D"),
        ("Which crop is an important raw material for the jute textile industry?", "Jute", "Rice", "Gram", "Wheat", "A"),
        ("What is a major benefit of agricultural storage facilities?", "They increase crop spoilage", "They help reduce post-harvest losses", "They make transport unnecessary", "They prevent all changes in market prices", "B"),
        ("Why is access to markets important for farmers?", "Markets have no role in agriculture", "Farmers cannot sell harvested products", "It helps farmers sell produce and obtain inputs", "It guarantees the same price for every crop", "C"),
        ("Which practice can help protect crops from soil erosion?", "Leaving sloping land bare", "Overgrazing farmland", "Removing field boundaries", "Maintaining cover crops or suitable vegetation", "D"),
        ("What is organic farming generally intended to emphasize?", "Ecological processes and organic inputs while limiting synthetic inputs", "Unlimited pesticide use", "Growing crops without soil nutrients", "Avoiding all biodiversity", "A"),
        ("Which factor can make farming difficult in arid regions?", "Excessive permanent rainfall", "Limited water availability", "Unlimited fertile wetlands", "Constant flooding everywhere", "B"),
        ("What is the purpose of agricultural extension services?", "To replace farmers with factories", "To prevent farmers from learning new methods", "To share farming knowledge and practical advice", "To eliminate local agricultural research", "C"),
        ("Which is an example of a plantation crop?", "Gram", "Wheat", "Millet", "Coffee", "D"),
        ("How can crop rotation help control some pests and diseases?", "Changing crops can interrupt the life cycles of certain pests", "It guarantees that every pest disappears", "It makes soil unnecessary", "It prevents every weather-related loss", "A"),
        ("What is the main purpose of irrigation scheduling?", "To use the maximum possible water at all times", "To supply water when crops need it", "To keep all fields permanently flooded", "To prevent farmers from monitoring soil moisture", "B"),
        ("Why is access to agricultural credit useful?", "It removes all risks from farming", "It guarantees a high selling price", "It can help farmers pay for inputs and equipment", "It replaces the need for farm management", "C"),
        ("Which statement best describes sustainable agriculture?", "It maximizes production regardless of environmental damage", "It avoids all technology", "It uses soil and water without limits", "It seeks productive farming while conserving natural resources", "D"),
    ],

    "Hard": [
        ("A farmer in a monsoon-dependent region experiences irregular rainfall. Which strategy can reduce vulnerability?", "Use suitable crop varieties, water harvesting, and diversified cropping", "Grow only water-intensive crops regardless of rainfall", "Ignore weather forecasts", "Remove all water storage facilities", "A"),
        ("Why can continuous monocropping reduce long-term farm resilience?", "It always increases soil biodiversity", "It can encourage certain pests and deplete particular soil nutrients", "It guarantees stable yields", "It eliminates the need for crop management", "B"),
        ("A farmer applies excessive nitrogen fertilizer before heavy rain. What is a likely environmental risk?", "All nutrients remain permanently in the field", "Groundwater becomes impossible to contaminate", "Nutrient runoff or leaching can pollute water", "Soil erosion becomes impossible", "C"),
        ("Which approach best combines higher productivity with soil conservation on sloping farmland?", "Plough directly downhill and remove vegetation", "Increase uncontrolled grazing", "Leave the land bare after harvest", "Use contour cultivation, suitable terraces, and ground cover", "D"),
        ("Why does access to reliable irrigation often improve agricultural productivity?", "It can reduce dependence on uncertain rainfall", "It guarantees that crops never suffer disease", "It makes soil fertility irrelevant", "It removes all price risks", "A"),
        ("A region grows a large amount of one crop for sale. What is a key risk of depending heavily on that crop?", "There can never be a market problem", "Price changes or crop failure can strongly affect farmers' incomes", "The crop becomes renewable only in winter", "Diversification becomes impossible everywhere", "B"),
        ("Which policy combination could best support small farmers over the long term?", "Remove access to markets and information", "Encourage unsustainable groundwater pumping", "Improve extension services, credit access, infrastructure, and market links", "Discourage soil conservation", "C"),
        ("Why can the overuse of groundwater for irrigation be unsustainable?", "Groundwater always replenishes immediately", "Pumping has no environmental effects", "It permanently increases aquifer storage", "Extraction can exceed recharge and lower water tables", "D"),
        ("A farmer rotates legumes with cereal crops. Which benefit is especially associated with many legumes?", "Certain legumes can help add nitrogen to soil through biological fixation", "All legumes eliminate every plant disease", "Legumes make irrigation unnecessary", "Legumes prevent all erosion without other measures", "A"),
        ("Which approach best reflects integrated pest management?", "Use the highest pesticide dose every time", "Combine monitoring, biological controls, cultural practices, and careful pesticide use when needed", "Never inspect crops", "Ignore pest populations until harvest", "B"),
        ("Why can post-harvest infrastructure improve food availability?", "It makes crop storage unnecessary", "It guarantees that all crops have the same price", "It reduces losses during storage, handling, and transport", "It removes the need for farmers", "C"),
        ("A farm uses drip irrigation and soil-moisture monitoring. What is the main management advantage?", "It guarantees zero water use", "It eliminates all crop diseases", "It prevents every drought", "It can align water application more closely with crop needs", "D"),
        ("Which factor explains why rice cultivation is concentrated in some regions rather than uniformly distributed?", "Climate, water availability, soils, and farming systems vary regionally", "Every region has identical rainfall", "Rice grows equally well under every condition", "Regional differences do not affect farming", "A"),
        ("How can climate change threaten agricultural production?", "It eliminates all weather variability", "Changes in temperature and rainfall can affect yields and growing seasons", "It guarantees higher yields for every crop", "It prevents all droughts", "B"),
        ("Which strategy can improve resilience to climate-related crop losses?", "Depend entirely on one vulnerable variety", "Remove local seed knowledge", "Diversify crops and use varieties suited to local conditions", "Ignore seasonal forecasts", "C"),
        ("Why can poorly managed irrigation increase soil salinity in dry regions?", "Salt disappears automatically after every irrigation", "All irrigation water contains no dissolved minerals", "Salinity cannot affect crop growth", "Water evaporates and may leave dissolved salts in the soil", "D"),
        ("Which is the strongest reason to combine traditional farming knowledge with scientific research?", "Both can contribute useful, locally relevant knowledge and tested practices", "Traditional knowledge is always incorrect", "Scientific research never helps farming", "Local conditions have no effect on farming", "A"),
        ("A farmer sells produce soon after harvest because suitable storage is unavailable. What challenge may result?", "The farmer is guaranteed a better price", "The farmer may have less flexibility to choose when to sell", "Storage has no effect on markets", "The crop cannot spoil after harvest", "B"),
        ("Which practice most directly helps conserve pollinators on farms?", "Remove flowering plants from every field edge", "Apply broad-spectrum pesticides without monitoring", "Maintain suitable habitat and reduce unnecessary harmful pesticide exposure", "Destroy all field boundaries", "C"),
        ("What is a major purpose of minimum support prices where such policies apply?", "Guarantee identical incomes to all farmers", "Remove every market fluctuation", "Ensure every crop is purchased in unlimited quantities", "Provide a policy-defined price floor for eligible crops under specified conditions", "D"),
        ("Why is diversification into livestock or other suitable farm activities sometimes useful?", "It can create additional income sources and spread some production risks", "It eliminates every agricultural risk", "It makes animal care unnecessary", "It guarantees profits regardless of costs", "A"),
        ("A farmer switches from excessive flood irrigation to carefully managed drip irrigation. Which outcome is plausible?", "Every crop will produce identical yields", "Water-use efficiency may improve, depending on crop and conditions", "The farm no longer needs soil nutrients", "Groundwater depletion becomes impossible everywhere", "B"),
        ("Why should agricultural policies consider both productivity and environmental impacts?", "Only short-term production matters", "Environmental effects never affect future yields", "Long-term food security depends on productive systems and healthy natural resources", "Conservation always prevents farming", "C"),
        ("Which approach best supports sustainable fertilizer management?", "Apply the same large quantity regardless of soil conditions", "Apply fertilizer immediately before expected heavy runoff", "Avoid assessing crop nutrient needs", "Use soil testing and apply appropriate amounts at suitable times", "D"),
        ("How can agricultural cooperatives help small farmers?", "They may improve collective purchasing, marketing, and access to services", "They eliminate the need for farm decisions", "They guarantee unlimited rainfall", "They prevent all changes in market demand", "A"),
        ("Which condition most strongly supports sustainable use of agricultural water?", "Unlimited pumping without measurement", "Extraction and irrigation demand are managed in relation to available supplies and recharge", "Wastewater is discharged untreated", "Water losses are deliberately increased", "B"),
        ("Why is soil organic matter important for long-term agricultural productivity?", "It prevents all nutrient cycling", "It makes soil organisms unnecessary", "It can improve soil structure, water retention, and nutrient cycling", "It eliminates the need for crop rotation in every case", "C"),
        ("A region experiences repeated crop failures after delayed monsoons. Which planning measure is most appropriate?", "Ignore seasonal information", "Use only crops with the longest water demand", "Remove all local water storage", "Improve forecasts, contingency plans, and access to suitable seeds", "D"),
        ("Which statement best explains the relationship between agriculture and food security?", "Reliable and sustainable agricultural systems contribute to food availability and livelihoods", "Agriculture has no connection to food supply", "Food security depends only on exports", "Agricultural production is unrelated to distribution", "A"),
        ("Which is the best example of a systems approach to sustainable agriculture?", "Maximize fertilizer use without monitoring", "Manage soil, water, biodiversity, crop choices, and farmer livelihoods together", "Focus only on a single season's yield", "Ignore the effects of farming on nearby communities", "B"),
    ],
}


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
            print("WARNING: The lesson does not yet contain 90 questions.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()