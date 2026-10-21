from pathlib import Path
import os
import random
import logging

from sqlalchemy import func

# =========================================================
# DATABASE CONFIGURATION
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "adaptive_learning.db"

os.environ["DATABASE_URL"] = f"sqlite:///{DATABASE_PATH.as_posix()}"

logging.disable(logging.CRITICAL)

from app.database.connection import SessionLocal
from app.models.student import Student
from app.models.lesson import Lesson
from app.models.quiz import Quiz
from app.models.question import Question
from app.models.progress import Progress
from app.models.session import LearningSession
from app.models.reward import RewardHistory


SUBJECT = "Social Science"
LESSON_TITLE = "The Indian Monsoon"


# =========================================================
# EASY QUESTIONS — 30
# =========================================================

EASY = [
    ("What is a monsoon?", "A seasonal reversal in prevailing wind patterns",
     "A permanent mountain range", "A type of soil", "A river delta", "A"),

    ("Which season brings most of India's annual rainfall to many regions?",
     "Winter season", "Southwest monsoon season",
     "Spring season only", "Autumn season only", "B"),

    ("From which direction do the southwest monsoon winds generally approach India?",
     "Northeast", "Northwest", "Southwest", "Southeast", "C"),

    ("Which body of water supplies moisture to the Arabian Sea branch of the monsoon?",
     "Arctic Ocean", "Mediterranean Sea", "Black Sea", "Arabian Sea", "D"),

    ("Which branch of the southwest monsoon first brings heavy rainfall to India's western coast?",
     "Arabian Sea branch", "Northeast branch", "Polar branch", "Atlantic branch", "A"),

    ("Which branch of the southwest monsoon brings rainfall to northeastern India?",
     "Arabian Sea branch only", "Bay of Bengal branch",
     "Mediterranean branch", "Arctic branch", "B"),

    ("What is rainfall?", "Water vapour rising into space",
     "Water stored inside rocks", "Water falling from the atmosphere",
     "The movement of tectonic plates", "C"),

    ("Which mountain range causes heavy orographic rainfall along India's western coast?",
     "Aravalli Range", "Vindhya Range", "Satpura Range", "Western Ghats", "D"),

    ("What is the dry period between monsoon rains often called?",
     "A break in the monsoon", "A glacier",
     "A cyclone eye", "A river delta", "A"),

    ("Which season generally follows the southwest monsoon withdrawal in much of India?",
     "Peak summer", "Post-monsoon season",
     "Permanent winter", "Spring everywhere", "B"),

    ("Which Indian state receives heavy rainfall from the southwest monsoon along the western coast?",
     "Rajasthan", "Punjab", "Kerala", "Haryana", "C"),

    ("Which region of India is known for very heavy monsoon rainfall?",
     "Western Rajasthan", "Ladakh's cold desert",
     "The driest parts of Kutch", "Meghalaya", "D"),

    ("What is a rain gauge used to measure?",
     "Rainfall", "Wind direction", "Air pressure", "Temperature", "A"),

    ("What is a drought?", "A period of continuous heavy rainfall",
     "A prolonged period of unusually low water availability",
     "A type of mountain wind", "A daily change in temperature", "B"),

    ("What is a flood?", "A long period without clouds",
     "A decrease in daylight", "Water overflowing onto normally dry land",
     "A type of desert", "C"),

    ("Why is the monsoon important for Indian agriculture?",
     "It prevents all crop diseases",
     "It eliminates the need for soil",
     "It stops river flow",
     "It supplies water to many rain-fed crops", "D"),

    ("What is the onset of the monsoon?",
     "The beginning of the seasonal monsoon rains in a region",
     "The end of winter everywhere", "The formation of a glacier",
     "The start of Earth's rotation", "A"),

    ("What is monsoon withdrawal?", "The beginning of snowfall",
     "The retreat of monsoon conditions from a region",
     "The formation of the Himalayas", "The movement of ocean floors", "B"),

    ("Which season is commonly associated with the retreating monsoon in India?",
     "Early summer", "Spring", "Post-monsoon season",
     "The entire winter season", "C"),

    ("Which coast receives substantial rainfall from the northeast monsoon?",
     "Konkan coast only", "Gujarat coast only",
     "Malabar coast only", "Coromandel coast of southeastern India", "D"),

    ("What is humidity?", "The amount of water vapour in the air",
     "The depth of a river", "The height of a mountain",
     "The speed of a vehicle", "A"),

    ("What provides the energy that drives evaporation from the ocean?",
     "Earthquakes", "Solar energy",
     "Mountain formation", "The Earth's magnetic field", "B"),

    ("What is orographic rainfall?", "Rain caused only by ocean tides",
     "Rain caused by volcanic eruptions",
     "Rain caused when moist air rises over elevated terrain",
     "Rain that occurs only in deserts", "C"),

    ("Which region is generally drier because it lies in the rain shadow of the Western Ghats?",
     "The windward western slopes", "The wettest coastal areas",
     "Parts of the western Himalayan foothills",
     "Parts of the interior Deccan Plateau", "D"),

    ("Which winds generally bring rainfall to much of India during summer?",
     "Southwest monsoon winds", "Polar easterlies",
     "Westerlies throughout the entire year", "Land breezes only", "A"),

    ("What is a cyclone?", "A stationary mountain",
     "A rotating weather system associated with a low-pressure centre",
     "A type of soil", "A permanent ocean island", "B"),

    ("Why can excessive monsoon rainfall be harmful?",
     "It prevents all river flow",
     "It eliminates groundwater",
     "It can cause floods, landslides and crop damage",
     "It stops all plant growth", "C"),

    ("What is irrigation?", "The removal of all soil nutrients",
     "A type of cloud", "The measurement of wind",
     "The artificial supply of water to crops", "D"),

    ("What is a rain shadow?", "A relatively dry region on the leeward side of a mountain range",
     "A region where rainfall is always highest",
     "A type of monsoon cloud", "A floodplain", "A"),

    ("Why do farmers monitor monsoon forecasts?",
     "To change Earth's rotation",
     "To plan sowing, irrigation and other agricultural activities",
     "To prevent all weather changes",
     "To eliminate seasonal variation", "B"),
]


# =========================================================
# MEDIUM QUESTIONS — 30
# =========================================================

MEDIUM = [
    ("Why does the Indian subcontinent experience a seasonal reversal of winds?",
     "Seasonal differences in heating and pressure patterns influence wind direction",
     "Earth stops rotating in summer",
     "The Himalayas move south every year",
     "Ocean currents stop completely during winter", "A"),

    ("Why does land generally heat faster than the ocean during summer?",
     "Land has no heat capacity",
     "Water has a higher effective heat capacity and mixes heat through a greater depth",
     "The ocean receives no sunlight",
     "Land does not lose heat", "B"),

    ("How does summer heating of the Indian landmass contribute to monsoon circulation?",
     "It removes all atmospheric moisture",
     "It stops winds over the ocean",
     "It contributes to low pressure that helps draw moist air inland",
     "It permanently reverses Earth's orbit", "C"),

    ("Why does the southwest monsoon bring heavy rainfall to Kerala?",
     "Kerala is located in a cold desert",
     "The region is far from the sea",
     "The Himalayas block all moisture from reaching Kerala",
     "Moist Arabian Sea winds encounter the Western Ghats and rise", "D"),

    ("Why does the Arabian Sea branch produce heavy rainfall on the windward side of the Western Ghats?",
     "Moist air is forced upward, cools and condenses",
     "The land prevents all condensation",
     "The winds contain no moisture",
     "The region is permanently below sea level", "A"),

    ("Why can areas east of the Western Ghats receive less rainfall than the western slopes?",
     "They are always closer to the sea",
     "Descending air on the leeward side can be relatively dry",
     "They receive no solar radiation",
     "The monsoon does not reach the peninsula", "B"),

    ("Why does the Bay of Bengal branch bring substantial rainfall to northeastern India?",
     "The region has no mountains",
     "It receives moisture only from the Arabian Sea",
     "Moist air is channelled toward the region and rises over elevated terrain",
     "All winds in the region are dry", "C"),

    ("Why can the Ganga plains experience rainfall differences from east to west?",
     "Longitude alone determines all rainfall",
     "The Himalayas prevent any rainfall in the east",
     "All locations receive identical rainfall",
     "Moisture availability and monsoon circulation vary across the plains", "D"),

    ("What is a monsoon trough?",
     "An elongated low-pressure zone associated with monsoon circulation",
     "A permanent ocean trench",
     "A mountain pass",
     "A dry riverbed", "A"),

    ("What can happen when the monsoon trough shifts northward toward the Himalayan foothills?",
     "Rainfall stops permanently across Asia",
     "Rainfall patterns can change, with increased activity near the foothills in some situations",
     "The southwest monsoon changes into snowfall everywhere",
     "The Earth's axis changes direction", "B"),

    ("What does a break in the southwest monsoon refer to?",
     "The permanent end of the Indian rainy season",
     "The absence of rainfall throughout the world",
     "A temporary reduction in monsoon rainfall over parts of India",
     "A period when Earth stops rotating", "C"),

    ("Why can monsoon rainfall be unevenly distributed?",
     "Every region has the same relief and wind exposure",
     "The monsoon always follows one straight path",
     "Rainfall depends only on latitude",
     "Relief, wind direction, moisture supply and weather systems vary by region", "D"),

    ("Why is the northeast monsoon particularly important for Tamil Nadu?",
     "Winds from the northeast and associated weather systems bring substantial rainfall during the post-monsoon period",
     "Tamil Nadu receives no rainfall from any other source",
     "The state is located in the Himalayas",
     "The northeast monsoon occurs only in summer", "A"),

    ("Why can tropical cyclones contribute to rainfall on India's eastern coast during the post-monsoon season?",
     "Cyclones cannot form over warm seas",
     "Storms over the Bay of Bengal can carry moisture toward the coast",
     "The eastern coast has no sea",
     "Cyclones always move away from India", "B"),

    ("What is the relationship between monsoon rainfall and groundwater recharge?",
     "Rainfall always reduces groundwater",
     "Groundwater cannot receive rainwater",
     "Some rainfall infiltrates the soil and replenishes groundwater stores",
     "Groundwater exists only beneath mountains", "C"),

    ("Why can intense rainfall produce flash floods?",
     "All rainfall immediately evaporates",
     "Rivers stop flowing during storms",
     "Soil absorbs unlimited water at every rate",
     "Rainfall can exceed infiltration and drainage capacity, causing rapid runoff", "D"),

    ("Why are landslides common in some hilly regions during heavy monsoon rainfall?",
     "Water can saturate slope materials and reduce their stability",
     "Rain permanently strengthens every slope",
     "Hills contain no loose material",
     "Gravity disappears during rainfall", "A"),

    ("What is one important effect of the Himalayas on India's monsoon climate?",
     "They prevent all summer rainfall",
     "They influence monsoon circulation and help block some cold continental air from the north",
     "They eliminate all low-pressure systems",
     "They stop the Bay of Bengal branch from existing", "B"),

    ("Why can the Thar Desert receive less rainfall than many western coastal areas?",
     "It is surrounded by oceans on every side",
     "It is permanently covered by snow",
     "Its location and regional circulation limit moisture delivery, and local relief affects rainfall",
     "It receives rainfall from every monsoon branch equally", "C"),

    ("Why is monsoon rainfall important for reservoirs?",
     "It removes all stored water",
     "It prevents river inflow",
     "It stops groundwater recharge",
     "It replenishes water storage used for irrigation, drinking water and power generation", "D"),

    ("What is the main purpose of a seasonal monsoon forecast?",
     "To estimate likely monsoon behaviour and support planning",
     "To determine Earth's exact age",
     "To prevent all rainfall",
     "To stop tropical cyclones", "A"),

    ("Why can agricultural production be affected by the timing of monsoon onset?",
     "Crop calendars are unrelated to rainfall",
     "Delayed or early rains can affect sowing dates and soil moisture",
     "Rainfall has no effect on crops",
     "All crops require exactly the same amount of water", "B"),

    ("What is one risk of a prolonged monsoon break?",
     "All rivers immediately overflow",
     "Rainfall becomes permanently uniform",
     "Soil moisture can decline and rain-fed crops may experience stress",
     "Groundwater always increases rapidly", "C"),

    ("Why can excessive rainfall be damaging even in a region that needs monsoon water?",
     "Water is never useful for agriculture",
     "All plants die from any rainfall",
     "Rainfall cannot affect settlements",
     "Rainfall intensity or duration can exceed the capacity of soils, rivers and drainage systems", "D"),

    ("What is the difference between monsoon onset and monsoon withdrawal?",
     "Onset marks the arrival of sustained monsoon conditions; withdrawal marks their retreat",
     "Onset occurs only in winter and withdrawal only in spring",
     "Both mean the same thing",
     "Withdrawal means the beginning of the year", "A"),

    ("Why can the monsoon advance in stages rather than arrive everywhere at once?",
     "The whole country is climatically identical",
     "Circulation patterns, moisture supply and regional geography vary",
     "The monsoon is a solid object moving across the land",
     "Rainfall cannot move across regions", "B"),

    ("How can El Niño influence the Indian monsoon?",
     "It guarantees drought in every Indian district",
     "It changes Earth's axial tilt",
     "It can alter large-scale ocean-atmosphere circulation and affect monsoon rainfall probabilities",
     "It prevents all clouds from forming", "C"),

    ("What is the Indian Ocean Dipole?",
     "A type of mountain range",
     "A system of inland lakes",
     "A permanent change in the direction of Earth's rotation",
     "A pattern of sea-surface temperature differences across parts of the tropical Indian Ocean", "D"),

    ("Why should El Niño not be used alone to predict every Indian monsoon outcome?",
     "Other oceanic, atmospheric and regional factors also influence monsoon behaviour",
     "El Niño determines rainfall with perfect accuracy",
     "The Indian monsoon is unrelated to atmospheric circulation",
     "Rainfall cannot be observed", "A"),

    ("What is one way to reduce agricultural vulnerability to irregular monsoon rainfall?",
     "Depend entirely on a single crop and sowing date",
     "Use water conservation, suitable crop choices and locally appropriate sowing strategies",
     "Remove all irrigation systems",
     "Ignore weather information", "B"),
]


# =========================================================
# HARD QUESTIONS — 30
# =========================================================

HARD = [
    ("Why is the Indian monsoon considered part of a coupled ocean-atmosphere system?",
     "Sea-surface temperatures, atmospheric pressure and winds interact to influence moisture transport and circulation",
     "The ocean has no effect on atmospheric conditions",
     "Monsoon winds occur without pressure differences",
     "Only Earth's internal heat controls the monsoon", "A"),

    ("How does the seasonal migration of the Intertropical Convergence Zone influence the Indian monsoon?",
     "It permanently eliminates the trade winds",
     "Its northward seasonal shift helps reorganise tropical convergence and monsoon circulation",
     "It changes the tilt of Earth's axis",
     "It prevents air from rising", "B"),

    ("Why can the Tibetan Plateau influence summer atmospheric circulation?",
     "It blocks all solar radiation from reaching Asia",
     "It creates ocean tides directly",
     "Its elevated surface heating can influence regional pressure patterns and atmospheric circulation",
     "It eliminates the need for moisture", "C"),

    ("What is the significance of the cross-equatorial flow in the southwest monsoon?",
     "It causes every wind to move directly north without turning",
     "It prevents moisture from entering the Arabian Sea",
     "It is unrelated to monsoon circulation",
     "Air crossing the equator helps supply the cross-equatorial flow that contributes to monsoon winds", "D"),

    ("Why can the Somali Jet be important to India's southwest monsoon?",
     "It is a strong low-level wind current over the western Indian Ocean that transports moisture toward the region",
     "It is a permanent Himalayan river",
     "It is a cold current in the Arctic Ocean",
     "It prevents the Arabian Sea from evaporating", "A"),

    ("Why does orographic rainfall depend on wind direction relative to a mountain range?",
     "Mountains create equal rainfall on every slope regardless of winds",
     "Moist air rising on windward slopes can cool and condense, while leeward areas may receive less rain",
     "Wind direction has no effect on rainfall",
     "Mountains eliminate atmospheric moisture", "B"),

    ("Why can the Western Ghats receive very heavy rainfall while parts of the interior Deccan Plateau remain relatively dry?",
     "The plateau receives no sunlight",
     "The Western Ghats have no influence on winds",
     "The windward slopes receive orographic rainfall and some interior areas lie in the rain shadow",
     "All monsoon moisture disappears before reaching India", "C"),

    ("What is one possible consequence of a prolonged break in the monsoon during a crop's critical growth stage?",
     "A guaranteed increase in harvest",
     "Permanent elimination of pests",
     "Unlimited soil moisture",
     "Water stress that may reduce crop growth and yields", "D"),

    ("Why is monsoon rainfall variability a challenge for water-resource management?",
     "Rainfall may be concentrated in short periods or vary substantially between years and regions",
     "All reservoirs receive exactly the same inflow every year",
     "Water demand never changes",
     "Groundwater cannot be replenished by rainfall", "A"),

    ("Why can intense rainfall cause urban flooding even when total seasonal rainfall is not unusually high?",
     "Urban surfaces absorb all rainwater",
     "Short-duration rainfall can exceed drainage capacity, especially where impermeable surfaces limit infiltration",
     "Cities contain no drainage systems",
     "Flooding depends only on annual average temperature", "B"),

    ("How can deforestation in a catchment influence monsoon-related runoff?",
     "It always eliminates rainfall",
     "It stops rivers from reaching the sea",
     "It can change interception, infiltration, erosion and runoff patterns",
     "It makes every slope completely stable", "C"),

    ("Why are monsoon depressions important for rainfall over central and northern India?",
     "They are permanent desert dunes",
     "They eliminate moisture transport",
     "They occur only over the Himalayas in winter",
     "They can organise moisture and rainfall over broad inland areas as they move", "D"),

    ("What does the term active monsoon phase generally describe?",
     "A period of enhanced monsoon rainfall over substantial parts of the monsoon region",
     "The permanent withdrawal of all monsoon winds",
     "A season without clouds anywhere",
     "The complete absence of low-pressure systems", "A"),

    ("Why can monsoon rainfall be stronger along the Himalayan foothills during some periods?",
     "The mountains prevent all air from rising",
     "The monsoon trough and moist air convergence can favour uplift near the foothills",
     "The region has no rivers",
     "The Sun stops heating the land", "B"),

    ("Why can the northeast monsoon produce significant rainfall in southeastern India?",
     "Northeast winds contain no moisture",
     "The Western Ghats block all winds from the Bay of Bengal",
     "Moisture from the Bay of Bengal and associated weather systems can reach the Coromandel Coast",
     "The region receives rainfall only from glaciers", "C"),

    ("Why are tropical cyclones in the Bay of Bengal a concern during the post-monsoon season?",
     "Cyclones cannot form after summer",
     "The Bay of Bengal has no warm water",
     "The eastern coast is protected from every storm",
     "Warm waters and favourable atmospheric conditions can support cyclones that threaten coastal communities", "D"),

    ("What is the main difference between seasonal rainfall total and rainfall intensity?",
     "Total is accumulated rainfall over a period; intensity is the rate at which rain falls",
     "Both always measure the same quantity",
     "Intensity measures wind speed",
     "Total rainfall measures atmospheric pressure", "A"),

    ("Why can a region experience meteorological drought even if some rainfall occurs?",
     "Any rainfall completely prevents drought",
     "Rainfall may remain significantly below the region's normal amount or fail to meet water needs",
     "Drought occurs only where it never rains",
     "Drought is caused only by snow", "B"),

    ("Why is agricultural drought different from meteorological drought?",
     "Agricultural drought refers only to ocean salinity",
     "Meteorological drought measures crop prices",
     "Agricultural drought concerns insufficient soil moisture for crops, while meteorological drought concerns rainfall deficits",
     "They are identical definitions", "C"),

    ("How can the Indian Ocean Dipole affect the Indian monsoon?",
     "It directly changes the length of Earth's year",
     "It determines every local storm with certainty",
     "It prevents all ocean evaporation",
     "Its sea-surface temperature pattern can influence atmospheric circulation and monsoon rainfall", "D"),

    ("Why can El Niño years sometimes be associated with weaker Indian summer monsoons?",
     "Changes in tropical Pacific ocean-atmosphere circulation can alter large-scale circulation patterns relevant to the monsoon",
     "El Niño changes India's latitude",
     "El Niño stops the Earth from rotating",
     "El Niño always removes all Indian Ocean moisture", "A"),

    ("Why is the relationship between El Niño and Indian monsoon rainfall not perfectly deterministic?",
     "The monsoon has no relationship to the ocean",
     "Other climate patterns and regional atmospheric conditions can strengthen or weaken the influence",
     "El Niño has identical effects in every year",
     "Rainfall cannot be measured", "B"),

    ("Why can Himalayan snow and glacier melt contribute to river flow before and during the monsoon?",
     "Snow and glaciers are formed only during rainfall",
     "Melting is unrelated to temperature",
     "Stored frozen water can melt and supply rivers, with amounts varying by season and conditions",
     "Glaciers prevent river flow", "C"),

    ("Why should long-term changes in monsoon rainfall be analysed using several decades of data?",
     "One day's rainfall determines the permanent climate",
     "Every year has identical monsoon conditions",
     "Climate cannot be studied using observations",
     "Long records help distinguish long-term patterns from natural year-to-year variability", "D"),

    ("What is a major limitation of using a single national rainfall average to describe the Indian monsoon?",
     "It can hide large regional differences and local extremes",
     "It identifies every village's rainfall exactly",
     "It removes all uncertainty",
     "It measures only wind speed", "A"),

    ("How can climate change affect monsoon-related hazards?",
     "It guarantees that every region will become wetter",
     "It can influence extreme rainfall risks and other aspects of the water cycle, with effects varying by region",
     "It eliminates all droughts",
     "It stops tropical cyclones from occurring", "B"),

    ("Why is rainwater harvesting useful in regions with variable monsoon rainfall?",
     "It changes the direction of monsoon winds",
     "It guarantees that drought cannot occur",
     "It can store some rainfall for later use and help manage water availability",
     "It prevents all groundwater recharge", "C"),

    ("Why can integrated watershed management reduce some monsoon-related risks?",
     "It increases erosion everywhere",
     "It prevents all rainfall from entering soil",
     "It replaces every river with a canal",
     "It can improve soil and water conservation, reduce erosion and support infiltration", "D"),

    ("Why should monsoon forecasts be communicated with uncertainty information?",
     "Forecasts are probabilistic and uncertainty helps people make informed decisions",
     "Forecasts are always exact",
     "Uncertainty means weather cannot be predicted at all",
     "Forecasts do not use observations", "A"),

    ("What is the most appropriate approach to managing monsoon-related agricultural risk?",
     "Rely on rainfall predictions without considering local conditions",
     "Combine forecasts with local observations, water management and suitable crop planning",
     "Use the same planting schedule in every region",
     "Ignore soil moisture and reservoir conditions", "B"),
]


# =========================================================
# VALIDATE QUESTION BANKS BEFORE DATABASE CHANGES
# =========================================================

QUESTION_BANKS = {
    "Easy": EASY,
    "Medium": MEDIUM,
    "Hard": HARD,
}

for difficulty, questions in QUESTION_BANKS.items():
    if len(questions) != 30:
        raise ValueError(
            f"{difficulty} must contain exactly 30 questions; "
            f"found {len(questions)}."
        )

    for index, item in enumerate(questions, start=1):
        if len(item) != 6:
            raise ValueError(
                f"{difficulty} question {index} has {len(item)} fields; "
                "exactly 6 are required."
            )

        if item[5] not in {"A", "B", "C", "D"}:
            raise ValueError(
                f"Invalid answer key in {difficulty} question {index}."
            )

print("Validation passed: 30 questions per difficulty.")


# =========================================================
# DATABASE HELPERS
# =========================================================

def shuffle_options(item):
    question, a, b, c, d, correct_letter = item

    options = {
        "A": a,
        "B": b,
        "C": c,
        "D": d,
    }

    correct_text = options[correct_letter]
    shuffled = list(options.values())
    random.shuffle(shuffled)

    new_correct_letter = "ABCD"[shuffled.index(correct_text)]

    return (
        question,
        shuffled[0],
        shuffled[1],
        shuffled[2],
        shuffled[3],
        new_correct_letter,
    )


def get_or_create_quiz(db, lesson, difficulty):
    quiz = (
        db.query(Quiz)
        .filter(
            Quiz.lesson_id == lesson.id,
            Quiz.difficulty == difficulty,
        )
        .first()
    )

    if quiz is None:
        quiz = Quiz(
            lesson_id=lesson.id,
            title=f"{lesson.title} - {difficulty}",
            difficulty=difficulty,
        )
        db.add(quiz)
        db.flush()

    return quiz


# =========================================================
# MAIN DATABASE OPERATION
# =========================================================

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

        if lesson is None:
            raise RuntimeError(
                f"Lesson '{LESSON_TITLE}' under '{SUBJECT}' was not found. "
                "Check the existing lesson title and subject."
            )

        print(f"\nLesson found: {lesson.title}")
        print(f"Subject: {lesson.topic}")
        print("-" * 55)

        newly_added = 0

        for difficulty, questions in QUESTION_BANKS.items():
            quiz = get_or_create_quiz(db, lesson, difficulty)

            existing_questions = (
                db.query(Question)
                .filter(Question.quiz_id == quiz.id)
                .all()
            )

            existing_texts = {
                q.question.strip().casefold()
                for q in existing_questions
            }

            added = 0

            for item in questions:
                (
                    question_text,
                    option_a,
                    option_b,
                    option_c,
                    option_d,
                    correct_answer,
                ) = shuffle_options(item)

                normalized = question_text.strip().casefold()

                if normalized in existing_texts:
                    continue

                db.add(
                    Question(
                        quiz_id=quiz.id,
                        question=question_text,
                        option_a=option_a,
                        option_b=option_b,
                        option_c=option_c,
                        option_d=option_d,
                        correct_answer=correct_answer,
                    )
                )

                existing_texts.add(normalized)
                added += 1

            db.flush()

            count = (
                db.query(func.count(Question.id))
                .filter(Question.quiz_id == quiz.id)
                .scalar()
            )

            print(f"{difficulty}: added {added}; total {count}/30")
            newly_added += added

        db.commit()

        print("\n" + "=" * 55)
        print("FINAL VERIFICATION")
        print("=" * 55)

        total = 0
        complete = True

        for difficulty in ("Easy", "Medium", "Hard"):
            quiz = (
                db.query(Quiz)
                .filter(
                    Quiz.lesson_id == lesson.id,
                    Quiz.difficulty == difficulty,
                )
                .first()
            )

            count = (
                db.query(func.count(Question.id))
                .filter(Question.quiz_id == quiz.id)
                .scalar()
            ) if quiz else 0

            print(f"{difficulty}: {count}/30")
            total += count

            if count != 30:
                complete = False

        print("-" * 55)
        print(f"TOTAL QUESTIONS: {total}/90")
        print(f"NEW QUESTIONS ADDED: {newly_added}")

        if complete and total == 90:
            print(
                "\nSUCCESS: The Indian Monsoon has exactly "
                "90 questions!"
            )
        else:
            print(
                "\nWARNING: The lesson does not yet have exactly "
                "30 questions at each difficulty."
            )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()