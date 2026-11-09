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
LESSON_TITLE = "The Earth and Its Movements"


# =========================================================
# EASY QUESTIONS — 30
# =========================================================

EASY = [
    ("What are the two main movements of Earth?",
     "Rotation and revolution", "Melting and freezing",
     "Condensation and evaporation", "Erosion and deposition", "A"),

    ("What is Earth's rotation?", "Earth moving around the Sun",
     "Earth spinning on its axis", "The Moon moving around Earth",
     "The Sun moving around Earth", "B"),

    ("What is Earth's revolution?", "Earth spinning on its axis",
     "The Moon spinning on its axis", "Earth moving around the Sun",
     "The Sun moving around the Moon", "C"),

    ("How long does Earth take to complete approximately one rotation?",
     "One month", "One year", "One week", "24 hours", "D"),

    ("How long does Earth take to revolve around the Sun?",
     "Approximately one year", "One day", "One week", "One month", "A"),

    ("What causes day and night on Earth?",
     "Earth's revolution alone", "Earth's rotation",
     "The Moon's revolution", "Ocean tides", "B"),

    ("Which part of Earth faces the Sun during daytime?",
     "The side facing away from the Sun",
     "Only the North Pole", "The side facing the Sun",
     "The entire planet equally", "C"),

    ("What causes the change from day to night?",
     "The Sun switches off", "The Moon blocks the whole Earth",
     "Earth stops moving", "Earth rotates and different areas face away from the Sun", "D"),

    ("What is Earth's axis?", "An imaginary line through Earth from pole to pole",
     "A ring around the equator", "The path of the Moon",
     "The edge of the atmosphere", "A"),

    ("What is the equator?", "A line joining the poles",
     "An imaginary line around the middle of Earth",
     "The orbit of Earth", "The boundary between continents", "B"),

    ("Which direction does Earth rotate when viewed from above the North Pole?",
     "East to west", "South to north", "West to east", "North to south", "C"),

    ("In which direction does the Sun appear to move across the sky each day?",
     "North to south only", "South to north only",
     "West to east", "East to west", "D"),

    ("Why does the Sun appear to rise in the east?",
     "Earth rotates from west to east",
     "Earth rotates from east to west",
     "The Sun revolves around Earth daily",
     "The Moon pushes the Sun westward", "A"),

    ("What is a leap year in the commonly used Gregorian calendar?",
     "A year with 360 days", "A year with 366 days",
     "A year with 364 days", "A year with 365 weeks", "B"),

    ("Why is an extra day added in a leap year?",
     "Earth stops rotating for one day",
     "The Moon completes two orbits",
     "The calendar year is adjusted to account for the extra fraction of a day in Earth's orbit",
     "The Sun becomes closer to Earth", "C"),

    ("Which celestial body does Earth orbit?",
     "The Moon", "Mars", "Jupiter", "The Sun", "D"),

    ("What is an orbit?", "The path one celestial body follows around another",
     "The line dividing day and night permanently",
     "A mountain range", "The surface of a planet", "A"),

    ("What is a year?", "The time Earth takes to rotate once",
     "The time Earth takes to complete one revolution around the Sun",
     "The time the Moon takes to rotate once only",
     "The time between two sunsets", "B"),

    ("What is a day caused by?",
     "Earth's revolution alone", "The changing seasons",
     "Earth's rotation", "The Moon's phases", "C"),

    ("What is the North Pole?", "The centre of Earth",
     "The point where the equator crosses the Prime Meridian",
     "The centre of the Sun", "The northern end of Earth's rotational axis", "D"),

    ("What is the South Pole?", "The southern end of Earth's rotational axis",
     "The centre of the equator", "The centre of the Moon",
     "The highest point on Earth", "A"),

    ("What is a hemisphere?", "A type of ocean current",
     "One half of a sphere or globe", "A type of mountain",
     "A complete revolution", "B"),

    ("Which imaginary line divides Earth into Northern and Southern Hemispheres?",
     "Prime Meridian", "Tropic of Capricorn", "Equator", "Arctic Circle", "C"),

    ("What is the Prime Meridian mainly used for?",
     "Dividing Earth into Northern and Southern Hemispheres",
     "Marking Earth's axis", "Showing the equator's latitude",
     "Providing the reference for measuring longitude", "D"),

    ("What is a solstice associated with?",
     "One of the year's longest or shortest daylight periods",
     "The daily formation of clouds", "An earthquake",
     "A change in the length of Earth's axis", "A"),

    ("What is an equinox?",
     "The day with no sunlight anywhere",
     "A time when day and night are approximately equal in length worldwide",
     "The longest day everywhere",
     "The day Earth stops revolving", "B"),

    ("What causes the seasons mainly?",
     "Changes in Earth's distance from the Moon",
     "The Sun turning on and off",
     "Earth's axial tilt as Earth revolves around the Sun",
     "Changes in Earth's rotation speed each day", "C"),

    ("How many main seasons are commonly recognised in many four-season systems?",
     "Two", "Three", "Five", "Four", "D"),

    ("When it is summer in the Northern Hemisphere, what season is generally occurring in the Southern Hemisphere?",
     "Winter", "Summer", "Spring everywhere", "Autumn everywhere", "A"),

    ("Does Earth stop rotating when it is nighttime in a location?",
     "Yes, every night", "No, Earth continues rotating",
     "Only in winter", "Only near the equator", "B"),
]


# =========================================================
# MEDIUM QUESTIONS — 30
# =========================================================

MEDIUM = [
    ("Why do different places on Earth experience daytime at different times?",
     "Earth rotates, bringing different longitudes toward the Sun at different times",
     "The Sun moves around Earth once every hour",
     "The Moon controls local time", "Earth stops rotating over oceans", "A"),

    ("Why does the length of daylight change through the year in many places?",
     "Earth's axis becomes vertical every month",
     "Earth's tilted axis keeps approximately the same orientation as it revolves around the Sun",
     "The Sun changes its rotation direction",
     "Earth's orbit stops in winter", "B"),

    ("What is the approximate tilt of Earth's rotational axis relative to a line perpendicular to its orbital plane?",
     "0 degrees", "90 degrees", "23.5 degrees", "45 degrees", "C"),

    ("When the Northern Hemisphere tilts toward the Sun, what generally happens there?",
     "It experiences winter everywhere", "It receives no sunlight",
     "Day and night disappear throughout the hemisphere",
     "It receives more direct sunlight and generally has longer days", "D"),

    ("Why are seasons opposite in the two hemispheres?",
     "The hemispheres tilt toward and away from the Sun at opposite times",
     "Earth rotates in opposite directions in each hemisphere",
     "The Sun gives different energy to each hemisphere permanently",
     "The Moon blocks sunlight from one hemisphere", "A"),

    ("What happens during an equinox?",
     "Earth is closest to the Sun",
     "Neither hemisphere is tilted strongly toward the Sun",
     "Earth stops rotating",
     "The poles receive no daylight", "B"),

    ("What happens during a solstice?",
     "Day and night are always exactly equal",
     "Earth stops revolving",
     "One hemisphere has its greatest tilt toward or away from the Sun",
     "Earth's axis loses its tilt", "C"),

    ("Why are high-latitude regions able to experience very long summer days?",
     "They rotate more quickly than the equator",
     "They are always closer to the Sun",
     "Earth does not rotate near the poles",
     "Earth's axial tilt causes the Sun to remain above the horizon for extended periods", "D"),

    ("What is the approximate duration of Earth's orbital period?",
     "365.24 days", "24 hours", "30 days", "12 hours", "A"),

    ("Why does the calendar use leap years?",
     "Earth rotates twice as fast every four years",
     "The tropical year is not exactly 365 whole days",
     "The Moon's orbit is exactly 366 days",
     "The seasons repeat every 360 hours", "B"),

    ("What is the main difference between rotation and revolution?",
     "Rotation means orbiting the Sun; revolution means spinning on an axis",
     "Both mean the same movement",
     "Rotation is spinning on an axis; revolution is orbital movement around another body",
     "Rotation happens only to the Moon", "C"),

    ("Why do we have different time zones?",
     "Earth has different gravity at each longitude",
     "The Sun shines only over one country at a time",
     "The Moon changes local clocks",
     "Different longitudes face the Sun at different times as Earth rotates", "D"),

    ("What is local solar noon?",
     "The time when the Sun reaches its highest point in the local sky",
     "Midnight everywhere on Earth",
     "The moment Earth completes its orbit",
     "The time the Moon rises", "A"),

    ("What causes the apparent daily movement of stars across the sky?",
     "Stars orbit Earth every day",
     "Earth's rotation",
     "The Moon's phases",
     "The yearly revolution of Mars", "B"),

    ("Why does Polaris appear nearly stationary in the night sky for observers in the Northern Hemisphere?",
     "It is the closest star to Earth",
     "It does not emit light",
     "It lies close to the direction of Earth's rotational axis",
     "Earth does not rotate in the Northern Hemisphere", "C"),

    ("What is the circle of illumination?",
     "The equator",
     "The orbit of Earth",
     "The path of the Moon",
     "The boundary separating the daylight and nighttime halves of Earth", "D"),

    ("Why is the circle of illumination not usually aligned with Earth's axis?",
     "Earth's axis is tilted relative to the plane of its orbit",
     "Earth has no poles",
     "The Sun changes shape daily",
     "Earth rotates only during daytime", "A"),

    ("What would happen to the seasonal cycle if Earth's axial tilt were zero, assuming its orbit remained similar?",
     "Seasons would become more extreme everywhere",
     "Seasonal differences caused by axial tilt would be greatly reduced",
     "Earth would stop rotating",
     "Every place would have six months of darkness", "B"),

    ("Why is summer generally warmer than winter in a given temperate location?",
     "Earth moves much closer to the Moon",
     "The Sun becomes much hotter in summer",
     "The Sun is higher in the sky and daylight lasts longer",
     "Earth's atmosphere disappears in winter", "C"),

    ("Why is the Northern Hemisphere's summer not caused mainly by Earth being closer to the Sun?",
     "Earth has no orbit",
     "The Sun is equally distant at every moment",
     "The Moon determines all seasons",
     "The hemispheres experience opposite seasons at the same time", "D"),

    ("What is the tropic of Cancer?",
     "A latitude line about 23.5 degrees north",
     "A longitude line at 0 degrees",
     "The southernmost latitude on Earth",
     "The line dividing day from night", "A"),

    ("What is the tropic of Capricorn?",
     "A longitude line at 180 degrees",
     "A latitude line about 23.5 degrees south",
     "The North Pole",
     "The Prime Meridian", "B"),

    ("What is the Arctic Circle associated with?",
     "The equator's crossing of the Prime Meridian",
     "The southernmost point of Earth",
     "A high northern latitude where at least one day each year can have 24-hour daylight or darkness",
     "The orbit of the Moon", "C"),

    ("What is the Antarctic Circle associated with?",
     "The equator",
     "The Prime Meridian only",
     "The Tropic of Cancer",
     "A high southern latitude where at least one day each year can have 24-hour daylight or darkness", "D"),

    ("Why do places near the equator generally have less seasonal variation in day length?",
     "The Sun's apparent path changes less in relation to the horizon through the year",
     "Earth does not rotate near the equator",
     "The equator is farther from the Sun",
     "The equator receives no direct sunlight", "A"),

    ("What is the main cause of the leap-year adjustment in the Gregorian calendar?",
     "Earth's rotation changes direction",
     "The calendar year is adjusted to stay aligned with Earth's seasonal cycle",
     "The Sun orbits Earth",
     "The Moon creates an extra day each year", "B"),

    ("Why is a solar day slightly different from Earth's rotation period relative to distant stars?",
     "Earth's axis disappears daily",
     "The Sun moves around Earth",
     "Earth moves along its orbit while rotating, so it must rotate a little more for the Sun to return to the same position",
     "The Moon changes Earth's direction", "C"),

    ("Which movement of Earth is most directly responsible for the annual cycle of seasons?",
     "Daily rotation alone", "The Moon's revolution",
     "The daily movement of clouds", "Revolution around the Sun combined with axial tilt", "D"),

    ("Why does the Sun's noon altitude change during the year at many locations?",
     "Earth's axial tilt changes the Sun's apparent position in the sky through the year",
     "The Sun switches its direction of rotation",
     "Earth's equator moves to the poles every month",
     "The Moon controls the Sun's altitude", "A"),

    ("What is the main reason Earth's poles experience periods of continuous daylight or darkness?",
     "The poles do not rotate",
     "Earth's axial tilt points a polar region toward or away from the Sun for extended periods",
     "The poles are outside Earth's atmosphere",
     "The Sun stops shining during winter", "B"),
]


# =========================================================
# HARD QUESTIONS — 30
# =========================================================

HARD = [
    ("Earth's axis is tilted approximately 23.5 degrees from the perpendicular to its orbital plane. What would happen if this tilt were much greater?",
     "Seasonal contrasts would generally become more extreme",
     "Earth would stop revolving",
     "Day and night would cease everywhere",
     "Earth's gravity would disappear", "A"),

    ("Why does the Southern Hemisphere experience summer when the Northern Hemisphere experiences winter?",
     "Earth stops rotating in the north",
     "The Southern Hemisphere is tilted toward the Sun while the Northern Hemisphere is tilted away",
     "The Sun produces energy only in the south",
     "The Moon blocks sunlight in the north", "B"),

    ("Why is Earth's revolution around the Sun not, by itself, enough to explain the seasons?",
     "Earth does not revolve",
     "The Sun has no light",
     "The seasons result mainly from axial tilt changing the angle and duration of sunlight during revolution",
     "The seasons are caused only by the Moon", "C"),

    ("At the June solstice, which statement is generally correct?",
     "The Southern Hemisphere has its longest day everywhere",
     "Day and night are equal at every location",
     "Earth stops revolving around the Sun",
     "The Northern Hemisphere is tilted most directly toward the Sun", "D"),

    ("At the December solstice, which statement is generally correct?",
     "The Southern Hemisphere is tilted most directly toward the Sun",
     "The Northern Hemisphere receives its longest daylight everywhere",
     "Earth's axis has no tilt",
     "The equator experiences no daylight", "A"),

    ("During an equinox, why are day and night approximately equal in length over much of Earth?",
     "Earth is closest to the Sun",
     "Neither hemisphere is tilted strongly toward or away from the Sun",
     "Earth stops rotating",
     "The Sun is directly over both poles", "B"),

    ("Why are the actual durations of daylight and darkness not always exactly 12 hours on an equinox?",
     "Earth rotates only at night",
     "The Sun's size changes daily",
     "Atmospheric refraction and the apparent size of the Sun affect sunrise and sunset times",
     "Earth's axis becomes horizontal", "C"),

    ("Why is the solar day slightly longer than the average sidereal rotation period?",
     "Earth slows to a stop every afternoon",
     "The Moon pushes Earth backward",
     "The Sun rotates around Earth daily",
     "Earth advances along its orbit while rotating, requiring extra rotation for the Sun to return to the local meridian", "D"),

    ("What is a sidereal day?",
     "The approximate time Earth takes to rotate once relative to distant stars",
     "The time Earth takes to orbit the Sun",
     "The time between two full moons",
     "The time from one solstice to another", "A"),

    ("Why do leap years usually occur every four years in the Gregorian calendar, with century exceptions?",
     "Earth's rotation adds four hours every day",
     "The calendar uses a correction rule to approximate the length of the tropical year",
     "Earth completes exactly 366 rotations in every year",
     "The Moon's orbit determines the Gregorian calendar", "B"),

    ("Why are century years such as 1900 not leap years in the Gregorian calendar unless divisible by 400?",
     "Earth's axis changes every century",
     "The Sun's apparent size changes",
     "The exception improves the calendar's approximation to the tropical year",
     "Earth does not revolve during century years", "C"),

    ("A location is at noon when the Sun crosses its local meridian. Why can another location have a different local solar time?",
     "The other location has a different rotational speed",
     "The Sun shines at different speeds",
     "The other location has a different axis",
     "Different longitudes face the Sun at different moments because Earth rotates", "D"),

    ("What is the approximate time difference in local solar time for every 15 degrees of longitude?",
     "One hour", "One minute", "Six hours", "One day", "A"),

    ("Why do time zones generally follow political boundaries instead of strict longitude lines everywhere?",
     "Longitude cannot be measured",
     "Countries and regions adopt practical standard times for administration and daily life",
     "Earth rotates differently within each country",
     "The equator controls all time zones", "B"),

    ("If Earth rotated from east to west instead of west to east, what would happen to the apparent daily movement of the Sun?",
     "The Sun would not be visible",
     "The seasons would disappear automatically",
     "The Sun would appear to move from west to east",
     "Earth would stop revolving", "C"),

    ("If Earth stopped rotating but continued revolving around the Sun, which statement is most accurate in an idealised model?",
     "Normal 24-hour day and night would continue unchanged",
     "The Sun would rise and set every hour",
     "The Moon would stop orbiting",
     "The familiar daily cycle would change dramatically, with the Sun's apparent motion dominated by Earth's orbital motion", "D"),

    ("Why do polar regions receive less solar energy per unit area during their winter?",
     "The Sun remains low below or near the horizon, spreading incoming energy over a larger area when it is visible",
     "Earth's poles contain no atmosphere",
     "The Sun stops producing energy",
     "The poles move outside Earth's orbit", "A"),

    ("Why can a polar region have 24-hour daylight during part of the year?",
     "The region stops rotating",
     "Earth's axial tilt keeps the Sun above the horizon throughout a daily rotation",
     "The Sun moves around the pole",
     "The region is closer to the Moon", "B"),

    ("Why can the Arctic experience 24-hour darkness during part of the year?",
     "The Arctic is outside Earth's atmosphere",
     "The Sun disappears permanently",
     "Earth's axial tilt keeps the region turned away from the Sun throughout a daily rotation",
     "The Arctic has no longitude", "C"),

    ("What is the relationship between Earth's axial tilt and the polar circles?",
     "The polar circles are determined by the boundaries of the continents",
     "The polar circles mark the equator",
     "The polar circles change position every day",
     "Their latitudes are approximately 90 degrees minus Earth's axial tilt", "D"),

    ("Why is the Sun's direct overhead position limited to the region between the Tropic of Cancer and Tropic of Capricorn?",
     "Earth's axial tilt limits the latitudes where the Sun can be directly overhead at local noon",
     "Earth's orbit is perfectly square",
     "The Sun does not shine beyond the tropics",
     "The poles block the Sun's rays", "A"),

    ("Why is the duration of daylight near the equator relatively consistent throughout the year?",
     "The equator does not experience sunrise",
     "The geometry of Earth's axial tilt causes comparatively small annual changes in day length there",
     "The equator is always tilted toward the Sun",
     "Earth's rotation stops at the equator", "B"),

    ("Which combination best explains annual seasonal changes in solar heating?",
     "Earth's distance from the Moon and ocean tides",
     "The changing speed of the Sun around Earth",
     "Axial tilt, revolution, and changes in solar angle and day length",
     "The daily formation of clouds only", "C"),

    ("Why are the seasons reversed between the hemispheres even though both hemispheres are part of the same planet?",
     "The Sun shines only on one hemisphere for a whole year",
     "Earth's axis reverses direction every six months",
     "Each hemisphere has a different Sun",
     "The hemispheres receive different angles and durations of sunlight because of axial tilt", "D"),

    ("Why is the Northern Hemisphere's summer not necessarily the hottest season everywhere at the same time?",
     "Local climates also depend on oceans, altitude, clouds, circulation and other factors",
     "Summer never increases daylight",
     "Earth has no atmosphere",
     "Latitude has no effect on climate", "A"),

    ("What is the approximate shape of Earth's orbit around the Sun?",
     "A perfect square", "An ellipse that is close to circular",
     "A straight line", "A spiral that never repeats", "B"),

    ("Why does Earth's changing distance from the Sun not explain the opposite seasons in the two hemispheres?",
     "Earth has no orbital movement",
     "The Sun's output is zero in winter",
     "Both hemispheres share nearly the same Earth-Sun distance at the same time but experience opposite seasons",
     "The Moon changes Earth's orbital distance every day", "C"),

    ("What determines the apparent path of the Sun across the sky over a day?",
     "Earth's revolution alone",
     "The annual cycle of the Moon",
     "Changes in Earth's magnetic field",
     "Earth's rotation combined with the observer's location and the season", "D"),

    ("Why does the Sun appear higher in the sky at noon during summer than during winter in many temperate locations?",
     "The hemisphere is tilted toward the Sun during summer",
     "Earth stops revolving in winter",
     "The Sun moves closer to each summer location",
     "The observer's latitude changes every season", "A"),

    ("Which statement best describes the relationship between rotation and revolution?",
     "Rotation causes the year, while revolution causes the daily cycle",
     "Rotation produces the daily cycle, while revolution combined with axial tilt explains the annual seasonal cycle",
     "Both movements are identical",
     "Revolution occurs only during the day", "B"),
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
                "\nSUCCESS: The Earth and Its Movements has "
                "exactly 90 questions!"
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