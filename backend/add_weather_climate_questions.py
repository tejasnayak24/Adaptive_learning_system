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
LESSON_TITLE = "Weather and Climate"


# =========================================================
# EASY QUESTIONS — 30
# =========================================================

EASY = [
    ("What is weather?", "The condition of the atmosphere at a particular time and place",
     "The shape of Earth", "The movement of continents", "The structure of the ocean floor", "A"),

    ("What is climate?", "Weather during one afternoon", "The long-term pattern of weather in a region",
     "The temperature of one room", "The direction of one gust of wind", "B"),

    ("Which instrument measures air temperature?", "Barometer", "Rain gauge",
     "Thermometer", "Wind vane", "C"),

    ("Which instrument measures rainfall?", "Compass", "Thermometer",
     "Barometer", "Rain gauge", "D"),

    ("Which instrument measures atmospheric pressure?", "Barometer",
     "Rain gauge", "Wind vane", "Anemometer", "A"),

    ("Which instrument shows wind direction?", "Thermometer", "Wind vane",
     "Rain gauge", "Barometer", "B"),

    ("Which instrument measures wind speed?", "Hygrometer", "Barometer",
     "Anemometer", "Rain gauge", "C"),

    ("What is humidity?", "The speed of a river", "The amount of dust in soil",
     "The height of a mountain", "The amount of water vapour in the air", "D"),

    ("What is precipitation?", "Water falling from the atmosphere to Earth's surface",
     "Water stored only underground", "The movement of tectonic plates",
     "The heating of soil", "A"),

    ("Which of these is a form of precipitation?", "Sunshine", "Rain",
     "Wind direction", "Air pressure", "B"),

    ("What is wind?", "Water flowing underground", "Heat stored in rocks",
     "Air moving from one place to another", "Clouds moving without air", "C"),

    ("What is a cloud mainly made of?", "Smoke only", "Dry soil",
     "Solid rock particles only", "Tiny water droplets or ice crystals", "D"),

    ("What is evaporation?", "Liquid water changing into water vapour",
     "Water vapour changing into liquid", "Ice changing directly into rock",
     "Rainwater entering a river", "A"),

    ("What is condensation?", "Liquid water changing into gas",
     "Water vapour changing into liquid water",
     "Soil changing into rock", "Wind changing direction", "B"),

    ("What is the water cycle?", "The movement of planets around the Sun",
     "The formation of mountains", "The continuous movement of water through Earth's systems",
     "The rotation of clouds around Earth", "C"),

    ("What provides most of the energy that drives Earth's weather?",
     "The Moon", "Ocean-floor rocks", "Earth's magnetic field",
     "The Sun", "D"),

    ("Which type of cloud is commonly associated with thunderstorms?",
     "Cumulonimbus", "Cirrus only", "Stratus only", "Fog", "A"),

    ("What is fog?", "Rain falling from tall clouds",
     "A cloud at or near the ground", "A strong ocean current",
     "A type of dry wind", "B"),

    ("What does a weather forecast provide?", "A map of underground minerals",
     "The exact climate of every century", "An estimate of upcoming atmospheric conditions",
     "A list of Earth's continents", "C"),

    ("Which condition describes a hot, sunny day?", "Heavy snowfall",
     "Freezing rain", "Dense fog necessarily", "High temperature with abundant sunshine", "D"),

    ("What is a season?", "A period of the year with characteristic weather patterns",
     "A type of weather instrument", "A single hour of rainfall",
     "A permanent landform", "A"),

    ("Which factor strongly influences the climate of a place?",
     "The colour of its buildings alone", "Latitude",
     "The names of its roads", "The number of schools alone", "B"),

    ("What is a drought?", "A period of unusually abundant rainfall",
     "A short period of strong winds only", "A prolonged period of unusually low water availability",
     "A daily change in temperature", "C"),

    ("What is a flood?", "A permanent lack of clouds",
     "A period of low humidity only", "A decrease in daylight",
     "Water overflowing onto normally dry land", "D"),

    ("What is a heatwave?", "A period of unusually hot weather",
     "A long period of snowfall everywhere", "A sudden earthquake",
     "A permanent change in Earth's orbit", "A"),

    ("What is a cold wave?", "A period of unusually heavy rainfall",
     "A period of unusually cold weather", "A rise in ocean salinity",
     "A type of cloud", "B"),

    ("Which gas is a major component of Earth's atmosphere?",
     "Helium only", "Hydrogen only", "Nitrogen", "Neon only", "C"),

    ("What is the atmosphere?", "The solid inner core of Earth",
     "The water stored in glaciers only", "The rocky outer layer of Earth",
     "The layer of gases surrounding Earth", "D"),

    ("Which part of the water cycle returns water to Earth's surface?",
     "Precipitation", "Evaporation", "Condensation only", "Transpiration only", "A"),

    ("Why is weather information useful?", "It changes the rotation of Earth",
     "It helps people plan activities and prepare for hazardous conditions",
     "It prevents every storm from forming", "It eliminates seasonal changes", "B"),
]


# =========================================================
# MEDIUM QUESTIONS — 30
# =========================================================

MEDIUM = [
    ("What is the main difference between weather and climate?",
     "Weather describes short-term conditions; climate describes long-term patterns",
     "Climate changes every minute, but weather never changes",
     "Weather occurs only in summer", "Climate refers only to rainfall", "A"),

    ("Why can coastal regions have milder temperatures than inland regions?",
     "Coastal regions receive no sunlight",
     "Water heats and cools more slowly than land",
     "Ocean water never changes temperature",
     "Coastal regions have no wind", "B"),

    ("What generally happens when warm, moist air rises and cools?",
     "It always becomes warmer", "It loses all its gases",
     "Water vapour may condense and form clouds",
     "Atmospheric pressure becomes infinite", "C"),

    ("Why does evaporation generally increase when temperature rises?",
     "Water becomes heavier",
     "Air stops moving",
     "Gravity becomes weaker",
     "More water molecules gain enough energy to escape into the air", "D"),

    ("How does condensation contribute to cloud formation?",
     "Water vapour cools and forms tiny liquid droplets or ice crystals",
     "Rain changes directly into soil",
     "Clouds absorb all sunlight permanently",
     "Wind becomes liquid water", "A"),

    ("Why does air pressure usually decrease with increasing altitude?",
     "Gravity disappears at high altitudes",
     "There is less air above exerting pressure",
     "Air becomes solid",
     "Earth stops rotating", "B"),

    ("What is relative humidity?",
     "The total mass of clouds in the sky",
     "The speed of wind near the ground",
     "The amount of water vapour present relative to the maximum possible at that temperature",
     "The depth of rainfall in a river", "C"),

    ("What usually happens to relative humidity when air cools without losing water vapour?",
     "It always becomes zero", "It cannot change",
     "It decreases to zero immediately", "It generally increases", "D"),

    ("What is the dew point?",
     "The temperature at which air becomes saturated with water vapour",
     "The hottest temperature of the year",
     "The speed at which clouds travel",
     "The temperature inside Earth's core", "A"),

    ("How do sea breezes generally develop during the day?",
     "Cool land air always moves toward the sea",
     "Land heats faster, causing cooler air from the sea to move inland",
     "The sea becomes hotter than land at every hour",
     "Air pressure becomes identical everywhere", "B"),

    ("How do land breezes generally develop at night?",
     "Warm air moves from the sea toward colder land in all cases",
     "Land stops releasing heat",
     "Land cools faster, and air tends to move from land toward the sea",
     "Ocean currents reverse Earth's rotation", "C"),

    ("Why do mountains influence rainfall?",
     "They prevent all clouds from forming",
     "They stop the water cycle",
     "They eliminate atmospheric pressure",
     "They force air upward, which can cause cooling and condensation", "D"),

    ("What is the rain-shadow effect?",
     "Rain falling equally on both sides of every mountain",
     "Drier conditions on the leeward side of a mountain range",
     "Rain occurring only over oceans",
     "A shadow cast by clouds at night", "B"),

    ("What is monsoon circulation commonly associated with?",
     "Seasonal changes in prevailing wind direction",
     "The daily rotation of the Moon",
     "Permanent absence of rainfall",
     "Movement of continents over a single season", "A"),

    ("Why is the Indian summer monsoon important?",
     "It stops all tropical cyclones",
     "It prevents evaporation",
     "It supplies a large share of rainfall to many parts of India",
     "It causes identical rainfall across the country", "C"),

    ("What is an air mass?",
     "A single raindrop",
     "A type of rain gauge",
     "A permanent region of high mountains",
     "A large body of air with relatively similar temperature and moisture characteristics", "D"),

    ("What is a weather front?",
     "The boundary between two air masses",
     "The centre of Earth",
     "A line of longitude",
     "A permanent ocean current", "A"),

    ("Which type of front forms when cold air advances and replaces warmer air?",
     "Warm front", "Cold front", "Stationary front only", "Ocean front", "B"),

    ("What is a tropical cyclone?",
     "A type of snowstorm near the poles only",
     "A slow-moving mountain glacier",
     "A rotating low-pressure storm system that develops over warm tropical waters",
     "A permanent area of high pressure", "C"),

    ("Why can warm ocean water help tropical cyclones develop?",
     "It removes all moisture from the atmosphere",
     "It stops clouds from forming",
     "It prevents air from rising",
     "It supplies heat and moisture that can fuel the storm", "D"),

    ("Which conditions commonly favour thunderstorm development?",
     "Moist, unstable air and rising motion",
     "Completely dry and stable air only",
     "No atmospheric moisture",
     "Constant freezing conditions at all levels", "A"),

    ("What is the main purpose of a weather station?",
     "To change local weather",
     "To observe and record atmospheric conditions",
     "To control the direction of winds",
     "To prevent cloud formation", "B"),

    ("Why are weather satellites useful?",
     "They measure every underground mineral directly",
     "They stop tropical cyclones from forming",
     "They observe cloud systems and large-scale atmospheric patterns",
     "They eliminate the need for any ground observations", "C"),

    ("What is the greenhouse effect?",
     "The process by which all sunlight is reflected into space",
     "The disappearance of Earth's atmosphere",
     "The process that creates Earth's magnetic field",
     "The warming caused when certain atmospheric gases absorb and re-emit infrared radiation", "D"),

    ("Which gas is a major human-caused contributor to global warming?",
     "Carbon dioxide", "Oxygen", "Argon", "Neon", "A"),

    ("What is climate change?",
     "A daily change in wind direction only",
     "A long-term shift in climate patterns and average conditions",
     "A single afternoon of rain",
     "A change in the shape of one cloud", "B"),

    ("Why can deforestation affect the local climate?",
     "It stops Earth's rotation",
     "It eliminates all atmospheric gases",
     "It changes evapotranspiration, surface properties and local energy balance",
     "It prevents all sunlight from reaching Earth", "C"),

    ("What does a weather map commonly use isobars to show?",
     "Rainfall totals only", "Wind direction only",
     "Cloud colour", "Lines connecting locations with equal atmospheric pressure", "D"),

    ("What does a closely spaced set of isobars often indicate?",
     "A strong pressure gradient and potentially stronger winds",
     "No atmospheric pressure",
     "A complete absence of wind in every case",
     "A permanent drought", "A"),

    ("Why can climate differ between two places at the same latitude?",
     "Latitude determines every aspect of climate",
     "Altitude, ocean currents, relief and distance from the sea can differ",
     "Longitude alone determines temperature",
     "Places at the same latitude always have identical rainfall", "B"),
]


# =========================================================
# HARD QUESTIONS — 30
# =========================================================

HARD = [
    ("Why does relative humidity usually rise as unsaturated air cools without gaining or losing water vapour?",
     "The saturation vapour pressure decreases as temperature falls",
     "The amount of nitrogen immediately becomes zero",
     "The air gains unlimited water vapour automatically",
     "Atmospheric pressure disappears", "A"),

    ("Air reaches its dew point. What condition has been reached?",
     "The air has become completely dry",
     "The air is saturated with water vapour under those conditions",
     "The air has reached absolute zero",
     "The wind speed must be zero", "B"),

    ("Why does rising air often cool even without exchanging heat with its surroundings?",
     "It absorbs heat from the Earth's core",
     "Its molecules stop moving",
     "It expands as surrounding pressure decreases, causing adiabatic cooling",
     "It changes into a liquid immediately", "C"),

    ("What is the difference between dry and saturated adiabatic cooling?",
     "Dry air cannot cool",
     "Saturated air cannot rise",
     "Both always have identical cooling rates",
     "Condensation releases latent heat, so saturated air often cools more slowly", "D"),

    ("What is the likely sequence when moist air is forced up a mountain?",
     "Air rises, cools, condensation may occur, and precipitation may develop",
     "Air sinks, heats indefinitely, and loses all oxygen",
     "Air pressure becomes zero at the mountain base",
     "Rainfall stops everywhere on both sides", "A"),

    ("Why is the leeward side of many mountain ranges relatively dry?",
     "It receives no sunlight",
     "Descending air often warms and its relative humidity decreases",
     "The mountain absorbs all atmospheric gases",
     "The water cycle stops permanently there", "B"),

    ("Why can the same amount of water vapour produce different relative humidity values at different temperatures?",
     "Water vapour has no relationship to temperature",
     "Relative humidity measures only wind speed",
     "Saturation vapour pressure varies with temperature",
     "Temperature does not affect air", "C"),

    ("What generally happens to atmospheric pressure as altitude increases in the troposphere?",
     "It increases without limit",
     "It remains exactly constant",
     "It changes only during rainfall",
     "It generally decreases because the overlying air column becomes smaller", "D"),

    ("Why does a low-pressure system commonly encourage cloud development?",
     "Surface air may converge and rise, cool, and condense",
     "Air must always sink in low-pressure systems",
     "Low pressure removes all moisture",
     "Clouds form only in high-pressure systems", "A"),

    ("Why are skies often clearer under persistent high-pressure conditions?",
     "High pressure always creates heavy rain",
     "Sinking air tends to warm and reduce relative humidity",
     "High pressure removes the atmosphere",
     "Cloud droplets cannot exist anywhere under high pressure", "B"),

    ("What is the principal energy source driving the global atmospheric circulation?",
     "Earth's internal heat alone",
     "The Moon's light",
     "Unequal solar heating of Earth's surface",
     "Heat produced by lightning", "C"),

    ("Why does unequal heating between the equator and poles contribute to global circulation?",
     "It makes Earth stop rotating",
     "It removes all pressure differences",
     "It creates identical temperatures everywhere",
     "It creates temperature and pressure differences that drive atmospheric motion", "D"),

    ("What is the Coriolis effect?",
     "The apparent deflection of moving air and other objects due to Earth's rotation",
     "The heating of water by sunlight",
     "The change of liquid water into vapour",
     "The force that creates all mountains", "A"),

    ("In which direction is the Coriolis deflection generally observed in the Northern Hemisphere?",
     "To the left of the direction of motion",
     "To the right of the direction of motion",
     "Directly upward in every case",
     "It always points toward the equator", "B"),

    ("Why do tropical cyclones generally require sufficiently warm ocean water?",
     "Warm water eliminates atmospheric pressure",
     "Warm water prevents evaporation",
     "Heat and moisture help sustain deep convection and release latent heat",
     "Warm water prevents all winds from developing", "C"),

    ("Why do tropical cyclones usually weaken after moving over land?",
     "Land provides unlimited ocean moisture",
     "The Earth's rotation stops over land",
     "Air pressure disappears",
     "They lose their oceanic moisture and heat supply, and surface friction increases", "D"),

    ("What is a storm surge?",
     "An abnormal rise of sea level associated with a storm",
     "A sudden decrease in air temperature only",
     "A permanent rise of every mountain",
     "A type of cloud classification", "A"),

    ("Why can a storm surge be especially dangerous near a shallow coast?",
     "Shallow water prevents waves from reaching land",
     "Water can pile up against the coast and inundate low-lying areas",
     "Shallow coasts eliminate storm winds",
     "Sea level becomes unrelated to atmospheric pressure", "B"),

    ("What is the primary difference between weather variability and climate change?",
     "Weather variability occurs only over centuries",
     "Climate change refers only to a single storm",
     "Weather varies over shorter periods, while climate change concerns long-term shifts",
     "They are exactly the same concept", "C"),

    ("Why can a single cold winter not, by itself, disprove long-term global warming?",
     "Global warming means every location must warm every day",
     "Winter temperatures are never measured",
     "Climate is unrelated to temperature",
     "Individual seasons vary, whereas climate trends are evaluated over longer periods and broader datasets", "D"),

    ("Which statement best distinguishes the greenhouse effect from global warming?",
     "The greenhouse effect is a natural physical process; enhanced greenhouse warming results from increased greenhouse-gas concentrations",
     "The greenhouse effect occurs only at night",
     "Global warming is the process that creates oxygen",
     "They have no relationship to atmospheric energy", "A"),

    ("Why is carbon dioxide important in discussions of human-caused climate change?",
     "It blocks every form of radiation",
     "It absorbs and emits infrared radiation and can increase heat retained in the climate system",
     "It is the most abundant gas in the atmosphere",
     "It prevents the water cycle", "B"),

    ("What is the difference between climate mitigation and climate adaptation?",
     "Mitigation means predicting weather; adaptation means measuring rainfall",
     "Mitigation addresses only floods; adaptation addresses only heat",
     "Mitigation reduces causes of climate change, while adaptation reduces harm from its impacts",
     "They are identical terms", "C"),

    ("Which is an example of climate adaptation?",
     "Increasing fossil-fuel use",
     "Removing every weather station",
     "Ignoring flood-risk maps",
     "Designing flood-resilient infrastructure for areas at risk", "D"),

    ("Which is an example of climate mitigation?",
     "Expanding renewable energy and improving energy efficiency",
     "Building only higher flood barriers",
     "Moving a weather station",
     "Measuring rainfall without changing emissions", "A"),

    ("Why can urban areas be warmer than nearby rural areas, especially at night?",
     "Cities receive no wind",
     "Built surfaces store heat and urban geometry and human activities can alter heat exchange",
     "Rural areas have no atmosphere",
     "Concrete prevents all solar radiation from reaching the surface", "B"),

    ("What is the urban heat-island effect?",
     "The cooling of every city below surrounding rural temperatures",
     "The formation of glaciers in cities",
     "Higher temperatures in urban areas compared with surrounding less-developed areas",
     "The permanent absence of clouds over cities", "C"),

    ("Why might two nearby places experience different rainfall totals?",
     "Rainfall is identical everywhere within a region",
     "Latitude is the only factor affecting rainfall",
     "Weather instruments cannot measure rainfall",
     "Relief, local convection, wind direction and storm paths can differ", "D"),

    ("What is one important limitation of a weather forecast?",
     "Forecast uncertainty generally increases with lead time",
     "Forecasts can never use observations",
     "Atmospheric conditions never change",
     "Forecasts are always exact for every location", "A"),

    ("Why do meteorologists combine satellite data, radar, surface observations and computer models?",
     "Each source independently predicts every event perfectly",
     "Different data sources provide complementary information for analysing and forecasting the atmosphere",
     "Ground observations make satellites useless",
     "Computer models eliminate all uncertainty", "B"),
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
            f"{difficulty} must contain 30 questions, "
            f"but contains {len(questions)}."
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

print("Validation passed: 30 Easy, 30 Medium and 30 Hard questions.")


# =========================================================
# HELPER FUNCTIONS
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

        print(f"\nLesson: {lesson.title}")
        print(f"Subject: {lesson.topic}")
        print("-" * 50)

        newly_added = 0

        for difficulty, questions in QUESTION_BANKS.items():
            quiz = get_or_create_quiz(db, lesson, difficulty)

            existing = (
                db.query(Question)
                .filter(Question.quiz_id == quiz.id)
                .all()
            )

            existing_texts = {
                q.question.strip().casefold()
                for q in existing
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

        print("\n" + "=" * 50)
        print("FINAL VERIFICATION")
        print("=" * 50)

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

        print("-" * 50)
        print(f"TOTAL QUESTIONS: {total}/90")
        print(f"NEW QUESTIONS ADDED: {newly_added}")

        if complete and total == 90:
            print(
                "\nSUCCESS: Weather and Climate has exactly "
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