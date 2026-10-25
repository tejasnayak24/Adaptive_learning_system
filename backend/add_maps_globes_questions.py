from pathlib import Path
import os
import random
import logging

from sqlalchemy import func

# ---------------------------------------------------------
# DATABASE CONFIGURATION
# ---------------------------------------------------------

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
LESSON_TITLE = "Maps and Globes"

# Each question must contain:
# question, option A, option B, option C, option D, correct answer


# =========================================================
# EASY QUESTIONS — 30
# =========================================================

EASY = [
    ("What is a map?", "A drawing of an area on a flat surface",
     "A type of mountain", "A weather instrument", "A water body", "A"),

    ("What is a globe?", "A flat drawing", "A spherical model of Earth",
     "A type of compass", "A map symbol", "B"),

    ("Which shape best represents Earth?", "Cube", "Cylinder",
     "Sphere", "Triangle", "C"),

    ("Which instrument helps us find directions?", "Thermometer",
     "Compass", "Rain gauge", "Barometer", "B"),

    ("Which direction is usually at the top of a map?",
     "South", "East", "West", "North", "D"),

    ("Which direction is opposite to north?", "South", "East",
     "West", "North-east", "A"),

    ("Which direction is opposite to east?", "North", "West",
     "South", "North-east", "B"),

    ("Which direction is opposite to west?", "South", "North",
     "East", "South-west", "C"),

    ("What does a map show?", "Only planets", "Only oceans",
     "Places and features of an area", "Only stars", "C"),

    ("What is an atlas?", "A collection of maps",
     "A type of globe", "A direction", "A mountain range", "A"),

    ("What does a map symbol represent?", "A real feature or object",
     "The age of a map", "The weight of Earth", "A season", "A"),

    ("What is a map scale used for?", "Finding temperature",
     "Measuring actual distances using map distances",
     "Predicting rainfall", "Measuring population directly", "B"),

    ("What is a sketch?", "A rough drawing of an area",
     "A perfect globe", "A weather chart", "A satellite", "A"),

    ("What is a plan commonly used to show?", "The whole universe",
     "The entire solar system", "A small area in detail",
     "Only oceans", "C"),

    ("Which of these is a natural feature?",
     "Bridge", "Railway station", "Airport", "Mountain", "D"),

    ("Which of these is a human-made feature?",
     "River", "Road", "Hill", "Valley", "B"),

    ("What is a map legend also called?", "Map key",
     "Map border", "Map scale", "Map title", "A"),

    ("Which colour is commonly used to show water on maps?",
     "Blue", "Pink", "Black", "Orange", "A"),

    ("What is a political map mainly used to show?",
     "Rainfall", "Boundaries of countries and states",
     "Soil types only", "Ocean depth only", "B"),

    ("What does a physical map mainly show?",
     "Election results", "Languages only",
     "Natural landforms and physical features", "Road traffic", "C"),

    ("Which feature is commonly shown using contour lines?",
     "Political parties", "Languages", "Population names",
     "Elevation and land shape", "D"),

    ("What is a map title used for?",
     "To describe what the map shows",
     "To show the map's weight", "To measure rainfall",
     "To indicate the Earth's age", "A"),

    ("What is a direction?", "A type of mountain",
     "A way of describing where something is located",
     "A map colour", "A landform", "B"),

    ("Which is one of the four cardinal directions?",
     "North-east", "South-west", "North", "North-west", "C"),

    ("Which direction lies between north and east?",
     "South-east", "South-west", "North-west", "North-east", "D"),

    ("What is a map projection?", "A method of showing Earth's curved surface on a flat map",
     "A type of weather", "A mountain-building process",
     "A method of measuring rainfall", "A"),

    ("Which model helps us understand Earth's shape?",
     "Compass", "Globe", "Ruler", "Thermometer", "B"),

    ("What is a road map designed to help people do?",
     "Measure earthquakes", "Study soil layers",
     "Find routes and roads", "Observe stars", "C"),

    ("What does a map grid help with?", "Measuring temperature",
     "Predicting rainfall", "Identifying rock types",
     "Locating places using grid references", "D"),

    ("Why are maps useful?", "They help us locate places and understand areas",
     "They stop natural disasters", "They change Earth's shape",
     "They eliminate all travel difficulties", "A"),
]


# =========================================================
# MEDIUM QUESTIONS — 30
# =========================================================

MEDIUM = [
    ("Why can a globe represent Earth more realistically than a flat map?",
     "It shows every street", "It represents Earth's spherical shape",
     "It never needs a scale", "It shows every building", "B"),

    ("Why do flat maps sometimes distort Earth's features?",
     "Earth has no atmosphere", "Maps cannot show directions",
     "A curved surface must be represented on a flat surface",
     "All maps are drawn by hand", "C"),

    ("What does a large-scale map generally show?",
     "A small area with more detail", "The whole world with little detail",
     "Only oceans", "Only continents", "A"),

    ("What does a small-scale map generally show?",
     "A classroom in great detail", "A wide area with less detail",
     "Only one building", "A single street corner", "B"),

    ("On a map, 1 cm represents 5 km. What distance does 4 cm represent?",
     "5 km", "10 km", "20 km", "25 km", "C"),

    ("On a map, 1 cm represents 10 km. Two towns are 7 cm apart. What is their actual distance?",
     "17 km", "50 km", "60 km", "70 km", "D"),

    ("What is the main purpose of a map scale?",
     "To show the age of a place", "To relate map distance to actual distance",
     "To identify languages", "To show population growth", "B"),

    ("Which map would be most useful for studying mountain ranges?",
     "Political map", "Road map", "Physical map", "Population map", "C"),

    ("Which map would be most useful for identifying state boundaries?",
     "Political map", "Weather map", "Soil map", "Relief map only", "A"),

    ("Why is a legend important on a map?",
     "It changes the map scale", "It explains the symbols used",
     "It shows the Earth's rotation", "It gives every location's population", "B"),

    ("What is the equator?",
     "A line showing the Prime Meridian",
     "A line marking the North Pole",
     "An imaginary line dividing Earth into Northern and Southern Hemispheres",
     "The boundary of a continent", "C"),

    ("Which imaginary line divides Earth into Eastern and Western Hemispheres?",
     "Equator", "Tropic of Cancer", "Arctic Circle",
     "Prime Meridian", "D"),

    ("What is latitude measured in?",
     "Degrees north or south of the equator",
     "Kilometres from the nearest city", "Hours of daylight",
     "Metres above sea level only", "A"),

    ("What is longitude measured in?",
     "Degrees north or south of the equator",
     "Degrees east or west of the Prime Meridian",
     "Kilometres above sea level", "Degrees of rainfall", "B"),

    ("What is the latitude of the equator?",
     "90 degrees north", "90 degrees south",
     "0 degrees", "180 degrees", "C"),

    ("What is the longitude of the Prime Meridian?",
     "90 degrees east", "180 degrees", "90 degrees west",
     "0 degrees", "D"),

    ("Which coordinates are commonly used to locate a place on Earth?",
     "Latitude and longitude", "Rainfall and temperature",
     "Height and weight", "Population and area", "A"),

    ("What is a thematic map?",
     "A map showing every physical feature",
     "A map focusing on a particular subject or theme",
     "A model of the solar system", "A drawing without a purpose", "B"),

    ("Which map is most suitable for showing population distribution?",
     "A road map only", "A map of mountain heights only",
     "A population distribution map", "A map showing only rivers", "C"),

    ("Why are conventional symbols used on maps?",
     "To make maps impossible to read",
     "To replace all geographical information",
     "To increase the size of the Earth",
     "To represent features in a standardised way", "D"),

    ("What is a sketch map usually based on?",
     "Observation and approximate representation",
     "Exact satellite measurements in every case",
     "Only latitude and longitude", "A globe's rotation", "A"),

    ("What is a plan particularly useful for?",
     "Showing the entire world",
     "Showing the layout of a small area in detail",
     "Showing only national borders",
     "Displaying all planetary orbits", "B"),

    ("What is a contour line on a topographic map?",
     "A line joining places with equal rainfall",
     "A line separating countries",
     "A line joining places of equal elevation",
     "A line marking a road", "C"),

    ("What do closely spaced contour lines usually indicate?",
     "Flat land", "A large lake", "A wide plain",
     "A steep slope", "D"),

    ("What do widely spaced contour lines usually indicate?",
     "A gentle slope", "A vertical cliff in every case",
     "A political boundary", "A deep ocean trench in every case", "A"),

    ("Why is north commonly placed at the top of maps?",
     "Earth always faces north",
     "It is a widely adopted mapping convention",
     "The Sun rises in the north everywhere",
     "South cannot be shown at the bottom", "B"),

    ("Which tool can help a traveller orient a paper map?",
     "Rain gauge", "Thermometer", "Compass", "Barometer", "C"),

    ("Which map would best help someone plan a driving route?",
     "Soil map", "Climate map", "Geological map",
     "Road map", "D"),

    ("What is one limitation of a globe?",
     "It is difficult to view the whole Earth at once",
     "It always changes Earth's shape",
     "It cannot show continents", "It has no spatial information", "A"),

    ("Why might different map projections be used?",
     "To make Earth flat in reality",
     "To suit different mapping purposes and reduce particular distortions",
     "To remove all map symbols",
     "To eliminate the need for coordinates", "B"),
]


# =========================================================
# HARD QUESTIONS — 30
# =========================================================

HARD = [
    ("A map scale is 1:100,000. What actual distance does 3 cm represent?",
     "300 m", "30 km", "3 km", "300 km", "C"),

    ("A map uses the scale 1:50,000. Two places are 8 cm apart on it. What is the actual distance?",
     "400 m", "40 km", "8 km", "4 km", "D"),

    ("The actual distance between two towns is 24 km. On a map, it is 6 cm. What is the scale in words?",
     "1 cm represents 4 km", "1 cm represents 6 km",
     "1 cm represents 24 km", "1 cm represents 144 km", "A"),

    ("On a map, 2 cm represents 15 km. What distance does 6 cm represent?",
     "15 km", "45 km", "30 km", "60 km", "B"),

    ("Which statement about a map projection is correct?",
     "Every projection preserves all properties perfectly",
     "Projection removes the need for a scale",
     "Different projections preserve different properties and distort others",
     "Projection changes Earth's actual shape", "C"),

    ("Why can areas near the poles look exaggerated on some world maps?",
     "The poles have no longitude",
     "Earth is completely flat near the poles",
     "The equator has no latitude",
     "Some projections enlarge high-latitude regions", "D"),

    ("Which projection property is most important when comparing the relative sizes of countries?",
     "Area preservation", "Road connectivity",
     "Place-name spelling", "Map border thickness", "A"),

    ("Which projection property is especially important for maintaining local angles and shapes?",
     "Preserving every area", "Conformality",
     "Showing population", "Showing elevation only", "B"),

    ("A location is at 20 degrees north latitude and 75 degrees east longitude. What does 20 degrees north indicate?",
     "Its distance east of the Prime Meridian",
     "Its elevation above sea level",
     "Its angular position north of the equator",
     "Its distance from the North Pole in kilometres", "C"),

    ("Two places lie on the same latitude. Which statement is correct?",
     "They must be in the same country",
     "They must have the same longitude",
     "They must have identical climates",
     "They lie along the same parallel of latitude", "D"),

    ("Two places lie on the same longitude. Which statement is correct?",
     "They lie along the same meridian",
     "They must be on the equator",
     "They must have the same latitude",
     "They must be in the same time zone under every system", "A"),

    ("Which coordinate is most directly useful for identifying how far north or south a place is?",
     "Longitude", "Latitude", "Map scale", "Grid colour", "B"),

    ("Which coordinate is most directly useful for identifying how far east or west a place is?",
     "Latitude", "Altitude", "Longitude", "Contour interval", "C"),

    ("What is the approximate maximum latitude value at either pole?",
     "0 degrees", "45 degrees", "180 degrees", "90 degrees", "D"),

    ("What is the approximate maximum longitude value when expressed east or west from the Prime Meridian?",
     "180 degrees", "90 degrees", "45 degrees", "360 degrees", "A"),

    ("A map has a scale of 1:250,000. What does 1 cm on the map represent on the ground?",
     "250 m", "2.5 km", "25 km", "250 km", "B"),

    ("A road measures 12 cm on a map with a scale of 1:200,000. What is its actual length?",
     "2.4 km", "12 km", "24 km", "240 km", "C"),

    ("Which map type is best for examining both elevation and detailed natural and human-made features?",
     "A simple political map only",
     "A map showing only country names",
     "A map showing only population",
     "A topographic map", "D"),

    ("Why are contour intervals important when interpreting a topographic map?",
     "They indicate the elevation difference between adjacent contour lines",
     "They show the number of roads",
     "They identify country capitals",
     "They indicate longitude differences", "A"),

    ("If contour lines form closed loops with elevations increasing toward the centre, what feature is commonly indicated?",
     "A river flowing uphill", "A hill or peak",
     "A national boundary", "A straight road", "B"),

    ("On a topographic map, contour lines crossing a valley often form a V shape. The V generally points toward which direction?",
     "Downstream in all cases", "East",
     "Upstream toward higher ground", "West", "C"),

    ("Why should map users check the date of a map?",
     "Latitude changes every day",
     "The globe changes its size each year",
     "All map scales become invalid after a month",
     "Roads, boundaries and other features may change over time", "D"),

    ("Which method is most appropriate for finding the straight-line ground distance between two mapped points?",
     "Measure their map distance and apply the map scale",
     "Count the map's colours",
     "Use the map title as a measurement",
     "Compare the sizes of the symbols", "A"),

    ("A map scale is 1:25,000. A path is 4 cm long on the map. What is the actual distance?",
     "100 m", "1 km", "10 km", "25 km", "B"),

    ("Which statement best describes a thematic map?",
     "It must show every road and building",
     "It cannot contain numerical data",
     "It emphasises the spatial distribution of a selected topic",
     "It always represents the entire solar system", "C"),

    ("Why is a choropleth map often used to compare population density across regions?",
     "It shows only road directions",
     "It represents every person individually",
     "It replaces the need for data",
     "It uses different shading or colours to represent data values by area", "D"),

    ("What is a potential problem when comparing raw population totals between regions of very different sizes?",
     "The totals do not account for differences in area",
     "Population cannot be represented on maps",
     "Longitude cannot be measured",
     "All regions have identical populations", "A"),

    ("Why should a map reader understand its projection before comparing distances across a world map?",
     "All projections show every distance accurately",
     "Projection can distort distances and shapes in different ways",
     "Projection eliminates the need for coordinates",
     "Distances on maps never relate to actual distances", "B"),

    ("Which statement about a globe is most accurate?",
     "It can display every street at once in full detail",
     "It has no scale",
     "It represents Earth's overall shape well but has limited surface detail",
     "It eliminates all geographical distortions in every measurement", "C"),

    ("A map shows 5 cm between two locations, and its scale is 1:400,000. What is the actual distance?",
     "2 km", "10 km", "15 km", "20 km", "D"),
]


# =========================================================
# VALIDATE EVERYTHING BEFORE MODIFYING THE DATABASE
# =========================================================

QUESTION_BANKS = {
    "Easy": EASY,
    "Medium": MEDIUM,
    "Hard": HARD,
}

for difficulty, questions in QUESTION_BANKS.items():
    if len(questions) != 30:
        raise ValueError(
            f"{difficulty} bank must contain exactly 30 questions; "
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
                f"{difficulty} question {index} has an invalid answer key."
            )

print("Question-bank validation passed: 30 questions per difficulty.")


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
# ADD QUESTIONS
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
                "Check the existing lesson title and subject in the database."
            )

        print(f"\nLesson found: {lesson.title}")
        print(f"Subject: {lesson.topic}")
        print("-" * 55)

        added_total = 0

        for difficulty, bank in QUESTION_BANKS.items():
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

            for item in bank:
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

                question = Question(
                    quiz_id=quiz.id,
                    question=question_text,
                    option_a=option_a,
                    option_b=option_b,
                    option_c=option_c,
                    option_d=option_d,
                    correct_answer=correct_answer,
                )

                db.add(question)
                existing_texts.add(normalized)
                added += 1

            db.flush()

            total_for_difficulty = (
                db.query(func.count(Question.id))
                .filter(Question.quiz_id == quiz.id)
                .scalar()
            )

            print(
                f"{difficulty}: added {added}; "
                f"total {total_for_difficulty}/30"
            )

            added_total += added

        db.commit()

        print("\n" + "=" * 55)
        print("FINAL VERIFICATION")
        print("=" * 55)

        total_questions = 0
        all_complete = True

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
            total_questions += count

            if count != 30:
                all_complete = False

        print("-" * 55)
        print(f"TOTAL QUESTIONS: {total_questions}/90")
        print(f"NEW QUESTIONS ADDED: {added_total}")

        if all_complete and total_questions == 90:
            print("\nSUCCESS: Maps and Globes has exactly 90 questions!")
        else:
            print(
                "\nWARNING: The lesson does not yet have exactly "
                "30 questions at each difficulty."
            )
            print(
                "Check the counts above before moving to the next lesson."
            )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()