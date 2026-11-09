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
LESSON_TITLE = "Population and Settlements"


# =========================================================
# EASY QUESTIONS — 30
# =========================================================

EASY = [
    ("What is population?", "The number of people living in an area",
     "The number of mountains in an area", "The amount of rainfall",
     "The total area of forests", "A"),

    ("What is a settlement?", "A type of river",
     "A place where people live", "A mountain range",
     "A weather condition", "B"),

    ("Which of these is a rural settlement?", "A major airport",
     "A large industrial city", "A village", "A metropolitan shopping district", "C"),

    ("Which of these is an urban settlement?", "A small farming hamlet",
     "An isolated forest camp", "A remote pasture",
     "A city", "D"),

    ("What is population density?", "The number of people per unit area",
     "The number of rivers in a state", "The height of a mountain",
     "The annual rainfall of a region", "A"),

    ("Which factor can influence where people settle?", "The colour of the sky alone",
     "Availability of water", "The names of nearby streets only",
     "The number of clouds on one day", "B"),

    ("What is migration?", "The growth of crops",
     "The formation of mountains", "The movement of people from one place to another",
     "The daily rotation of Earth", "C"),

    ("What is birth rate?", "The number of schools in an area",
     "The number of people leaving a country",
     "The total number of houses",
     "The number of live births relative to population during a specified period", "D"),

    ("What is death rate?", "The number of deaths relative to population during a specified period",
     "The number of births in a village", "The total area of a city",
     "The number of roads in a district", "A"),

    ("What is a census?", "A method of predicting rainfall",
     "An official count and collection of information about a population",
     "A type of settlement", "A system of irrigation", "B"),

    ("What is immigration?", "Moving away from a country",
     "Travelling to school", "Moving into a country or area to live",
     "Moving goods between cities", "C"),

    ("What is emigration?", "Moving into a country",
     "Changing houses within one street",
     "Travelling for a short holiday",
     "Leaving a country or area to live elsewhere", "D"),

    ("Which occupation is traditionally common in many rural areas?",
     "Agriculture", "Space tourism", "Stock exchange trading only",
     "International airport management only", "A"),

    ("Which activity is commonly associated with urban economies?",
     "Subsistence farming only", "Manufacturing and services",
     "Herding in remote pastures only", "Forest gathering only", "B"),

    ("What is a hamlet?", "A large metropolitan region",
     "A national capital", "A very small settlement",
     "A major seaport", "C"),

    ("What is a village?", "A large international airport",
     "A mountain summit", "An industrial port only",
     "A settlement that is generally smaller than a town or city", "D"),

    ("What is a city?", "A relatively large and densely populated settlement",
     "An uninhabited mountain", "A type of rainfall",
     "A river source", "A"),

    ("Which natural resource is essential for human settlements?",
     "Plastic waste", "Fresh water", "Air pollution", "Traffic congestion", "B"),

    ("What is infrastructure?", "The number of births in a region",
     "The total amount of rainfall", "Basic facilities and systems such as roads, water supply and electricity",
     "The distance between planets", "C"),

    ("What is urbanisation?", "The movement of rivers toward the sea",
     "The growth of forests only", "The decline of all industries",
     "The increasing proportion of people living in urban areas", "D"),

    ("What is a household?", "A person or group of people who live together and organise domestic living",
     "A mountain range", "A type of census form only",
     "A river basin", "A"),

    ("Which of these is a push factor for migration?",
     "Better employment opportunities at the destination",
     "Lack of jobs in the place of origin",
     "Improved facilities at the destination",
     "Access to better education at the destination", "B"),

    ("Which of these is a pull factor for migration?",
     "Conflict in the place of origin", "Crop failure in the place of origin",
     "Better employment opportunities elsewhere",
     "A natural disaster at home", "C"),

    ("What is a public service in a settlement?",
     "A private collection of luxury cars",
     "A personal hobby", "A household decoration",
     "A service such as sanitation, public transport or water supply", "D"),

    ("What is a slum generally characterised by?",
     "Inadequate housing and limited access to essential services",
     "Only large luxury homes", "No human population",
     "Permanent snow cover", "A"),

    ("Why do many settlements develop near rivers?",
     "Rivers prevent all forms of agriculture",
     "Rivers can provide water, fertile soil and transport opportunities",
     "Rivers eliminate the need for roads everywhere",
     "Rivers prevent trade", "B"),

    ("What is a metropolitan area?", "An isolated farm",
     "A single small house", "A large urban area that may include a central city and surrounding connected areas",
     "An uninhabited desert", "C"),

    ("What is population growth?", "A decrease in the number of people",
     "The movement of rivers", "The expansion of forests only",
     "An increase in the number of people in a population over time", "D"),

    ("Which service helps improve public health in settlements?",
     "Sanitation", "Open sewage disposal", "Contaminated drinking water",
     "Unmanaged waste dumping", "A"),

    ("Why is settlement planning important?", "It makes every settlement identical",
     "It helps provide services, manage land use and improve living conditions",
     "It eliminates all population growth",
     "It prevents all migration", "B"),
]


# =========================================================
# MEDIUM QUESTIONS — 30
# =========================================================

MEDIUM = [
    ("Why do fertile plains often support dense populations?",
     "They can support agriculture, transport and relatively easy construction",
     "They have no water resources",
     "They prevent all economic activity",
     "They are always free from natural hazards", "A"),

    ("Why are some mountainous regions sparsely populated?",
     "All mountains lack rainfall",
     "Steep slopes and difficult access can limit farming, transport and construction",
     "Mountains cannot contain settlements",
     "Mountain regions have no natural resources", "B"),

    ("How is natural population growth generally calculated?",
     "Immigration minus emigration only",
     "Total houses minus total roads",
     "Births minus deaths over a specified period",
     "Urban population divided by land area", "C"),

    ("What happens when the birth rate exceeds the death rate, ignoring migration?",
     "The population must decrease",
     "The population remains unchanged",
     "The settlement disappears",
     "The population increases through natural growth", "D"),

    ("How can migration affect the population of a city?",
     "It can increase or decrease the population depending on migration flows",
     "It never affects population",
     "It changes the city's latitude",
     "It prevents natural population growth", "A"),

    ("Why might people migrate from rural to urban areas?",
     "To eliminate all education opportunities",
     "To seek employment, education and better access to services",
     "Because cities never have problems",
     "Because rural areas have no inhabitants", "B"),

    ("What is a major challenge associated with rapid urbanisation?",
     "The disappearance of all transport demand",
     "The elimination of housing needs",
     "Pressure on housing, transport, water and sanitation",
     "The permanent absence of employment", "C"),

    ("Why is population density useful in geographical studies?",
     "It measures rainfall directly",
     "It gives the exact income of every household",
     "It identifies every person's occupation",
     "It helps compare how concentrated populations are across areas", "D"),

    ("Area A has 100,000 people and an area of 200 square kilometres. What is its population density?",
     "500 people per square kilometre",
     "200 people per square kilometre",
     "1,000 people per square kilometre",
     "50 people per square kilometre", "A"),

    ("A district has 300,000 people and covers 600 square kilometres. What is its population density?",
     "300 people per square kilometre",
     "500 people per square kilometre",
     "600 people per square kilometre",
     "1,800 people per square kilometre", "B"),

    ("Why is a census important for government planning?",
     "It directly prevents every disease",
     "It determines every person's future job",
     "It provides population information for planning services and allocating resources",
     "It eliminates the need for public infrastructure", "C"),

    ("What is an age-sex structure diagram used to show?",
     "Only a country's rainfall",
     "The location of every road",
     "The types of soil in a district",
     "The distribution of a population by age and sex", "D"),

    ("What does a broad base in a population pyramid often indicate?",
     "A relatively high proportion of young people",
     "A population containing only elderly people",
     "A complete absence of children",
     "An equal population at every age", "A"),

    ("What is dependency ratio used to describe?",
     "The number of rivers per district",
     "The relationship between dependent age groups and the working-age population",
     "The number of houses per road",
     "The annual rainfall per household", "B"),

    ("Why can an ageing population create planning challenges?",
     "It eliminates the need for healthcare",
     "It always increases school enrolment",
     "It can increase demand for healthcare and pension support relative to the workforce",
     "It makes all settlements rural", "C"),

    ("What is a dispersed settlement pattern?",
     "Houses arranged tightly around a central square",
     "A city with continuous high-rise buildings",
     "A settlement entirely surrounded by water",
     "Homes spread out over a relatively large area", "D"),

    ("What is a nucleated settlement?",
     "A settlement where buildings are clustered closely together",
     "A settlement with one isolated house only",
     "An area with no permanent inhabitants",
     "A network of roads without homes", "A"),

    ("Why might a linear settlement develop along a road or river?",
     "People cannot travel along roads",
     "Transport, water and access may encourage buildings to develop along the route",
     "Buildings must always form a circle",
     "Linear settlements occur only in deserts", "B"),

    ("How can industrial development influence settlement growth?",
     "It always reduces employment",
     "It prevents transport development",
     "It can attract workers and supporting services",
     "It removes the need for housing", "C"),

    ("Why can informal settlements grow rapidly on city outskirts?",
     "All urban housing is always affordable",
     "No one migrates to cities",
     "Cities never attract workers",
     "Affordable housing shortages and rapid population growth may push people into informal housing", "D"),

    ("What is suburbanisation?",
     "The growth of residential areas around the edges of a city",
     "The disappearance of every town",
     "The formation of a desert",
     "The movement of a river underground", "A"),

    ("What is urban sprawl?",
     "The concentration of every activity in one building",
     "The outward expansion of urban development into surrounding areas",
     "The decline of all roads",
     "The natural growth of forests only", "B"),

    ("Why can urban sprawl increase commuting distances?",
     "Homes and workplaces always become closer",
     "All public transport becomes unnecessary",
     "Residential and employment areas may spread farther apart",
     "It eliminates road networks", "C"),

    ("What is one benefit of mixed land-use planning?",
     "It requires all homes to be far from shops",
     "It prevents people from walking",
     "It eliminates public transport",
     "It can place homes, services and workplaces closer together", "D"),

    ("Why are settlements often located near transport junctions?",
     "Junctions can improve connectivity, trade and access to services",
     "Junctions prevent all travel",
     "They eliminate economic activity",
     "They have no influence on accessibility", "A"),

    ("How can climate affect settlement patterns?",
     "Climate never affects human activity",
     "Temperature, rainfall and extreme weather can influence water supply, livelihoods and housing",
     "Climate determines only road names",
     "Every climate supports identical population density", "B"),

    ("Why can coastal cities attract large populations?",
     "Coasts never experience hazards",
     "Coastal land has no economic value",
     "Ports, trade, fishing and related industries can attract people",
     "Coastal areas cannot support transport", "C"),

    ("What is rural depopulation?",
     "An increase in rural population in every village",
     "The growth of all farming activities",
     "The formation of a new mountain",
     "A decline in the population of rural areas", "D"),

    ("Why can access to education influence migration?",
     "People may move to places where educational institutions and opportunities are more available",
     "Education has no relationship to migration",
     "Schools determine Earth's rotation",
     "Education eliminates all settlement growth", "A"),

    ("Why should population data be interpreted with geographical context?",
     "The same density always produces identical living conditions",
     "Population patterns are also influenced by resources, infrastructure, livelihoods and the environment",
     "Population data directly measures rainfall",
     "Geography has no relationship to population", "B"),
]


# =========================================================
# HARD QUESTIONS — 30
# =========================================================

HARD = [
    ("Why can population density alone be insufficient to assess pressure on local resources?",
     "It does not directly show consumption patterns, resource availability or infrastructure capacity",
     "It measures every household's income exactly",
     "It includes every environmental factor automatically",
     "It is identical to population growth", "A"),

    ("A city grows from 200,000 to 250,000 people. What is its percentage population increase?",
     "20%", "25%", "50%", "125%", "B"),

    ("A region has 800,000 people and an area of 2,000 square kilometres. What is its population density?",
     "200 people per square kilometre",
     "800 people per square kilometre",
     "400 people per square kilometre",
     "1,600 people per square kilometre", "C"),

    ("Why can a country experience population growth even when its birth rate is falling?",
     "A falling birth rate always means immediate population decline",
     "Migration never influences population",
     "The population cannot change after a census",
     "Births may still exceed deaths, and migration can also affect population change", "D"),

    ("What is demographic transition?",
     "A process describing changes in birth rates, death rates and population growth as societies develop",
     "The movement of all people into one city",
     "A type of settlement along a river",
     "The annual movement of monsoon winds", "A"),

    ("What commonly occurs in an early stage of demographic transition?",
     "Both birth and death rates are always extremely low",
     "Birth and death rates are both high, often resulting in relatively slow long-term growth",
     "The population has no children",
     "Migration is impossible", "B"),

    ("What can cause rapid population growth during a transitional demographic stage?",
     "A simultaneous permanent rise in death rates",
     "The disappearance of medical services",
     "Death rates decline while birth rates remain relatively high",
     "All migration stops permanently", "C"),

    ("What is population momentum?",
     "The immediate disappearance of a population",
     "A measure of annual rainfall",
     "The speed of migration between two streets",
     "Continued population growth that can occur because of a young age structure even after fertility declines", "D"),

    ("Why can a youthful population increase future demand for schools and employment?",
     "Large younger age groups will progress into school-age and working-age groups over time",
     "Young people never require public services",
     "Age structure has no effect on service demand",
     "Every young person migrates abroad immediately", "A"),

    ("What does a high old-age dependency ratio generally indicate?",
     "There are no elderly people",
     "There are relatively more older dependants compared with the working-age population",
     "Every person is employed",
     "The region has no healthcare needs", "B"),

    ("Why is net migration different from total migration?",
     "Net migration counts only people born locally",
     "Total migration is always negative",
     "Net migration is the difference between immigration and emigration",
     "Net migration measures population density", "C"),

    ("A city receives 30,000 immigrants and 18,000 emigrants during a year. What is its net migration?",
     "48,000 people leaving", "18,000 people entering",
     "30,000 people entering", "12,000 people entering", "D"),

    ("Why can rural-to-urban migration produce both benefits and challenges?",
     "It can expand the labour force and economic activity but also increase pressure on urban services",
     "It always reduces city population",
     "It prevents economic growth",
     "It eliminates the need for urban planning", "A"),

    ("What is counterurbanisation?",
     "The movement from one city centre to another",
     "The movement of people from urban areas toward smaller settlements or rural areas",
     "The increase of urban density in every neighbourhood",
     "The growth of population in the same house", "B"),

    ("How can transport improvements contribute to urban sprawl?",
     "They prevent all development outside the city centre",
     "They eliminate commuting",
     "They can make distant residential and commercial locations more accessible",
     "They stop new roads from being built", "C"),

    ("Why can urban sprawl create environmental problems?",
     "It always increases natural vegetation",
     "It eliminates private vehicle use",
     "It prevents habitat fragmentation",
     "It can consume agricultural land, fragment habitats and increase transport-related emissions", "D"),

    ("What is the urban heat-island effect in settlement geography?",
     "Urban areas can be warmer than surrounding rural areas because of built surfaces and human activities",
     "Cities are always colder than rural areas",
     "Urban temperature is unrelated to land cover",
     "It refers to rainfall occurring only in cities", "A"),

    ("Why can informal settlements be vulnerable to environmental hazards?",
     "They always have the strongest infrastructure",
     "Some occupy hazard-prone locations and lack adequate drainage, services or secure housing",
     "They cannot experience flooding",
     "They are always located far from rivers and coasts", "B"),

    ("How can inclusive urban planning help reduce settlement inequality?",
     "By removing essential services from poorer neighbourhoods",
     "By preventing access to education",
     "By improving affordable housing, transport, sanitation and access to public services",
     "By concentrating every facility in wealthy areas only", "C"),

    ("Why is the carrying capacity of a settlement important?",
     "It identifies the exact population that must live there forever",
     "It measures the speed of Earth's rotation",
     "It prevents every form of migration",
     "It concerns the ability of local resources and infrastructure to support a population sustainably", "D"),

    ("Why might a settlement near a river face both opportunities and risks?",
     "The river may provide water and transport while also creating flood risk",
     "Rivers provide no resources",
     "River settlements never experience hazards",
     "River location prevents agriculture", "A"),

    ("Why can coastal settlement growth increase disaster risk?",
     "Coastal regions have no economic activity",
     "More people and infrastructure may be exposed to cyclones, storm surges and coastal flooding",
     "Coastal cities cannot experience storms",
     "Population growth eliminates sea-level change", "B"),

    ("What is a sustainable settlement?",
     "A settlement that uses unlimited resources without planning",
     "A settlement without public services",
     "A settlement designed to support quality of life while managing environmental and resource impacts",
     "A settlement where population never changes", "C"),

    ("Why is mixed-use development often encouraged in sustainable urban planning?",
     "It requires all workplaces to be far from homes",
     "It prevents walking and cycling",
     "It eliminates the need for public spaces",
     "It can reduce travel distances and improve access to daily services", "D"),

    ("How can reliable public transport influence urban development?",
     "It can improve accessibility and reduce dependence on private vehicles",
     "It always increases travel times",
     "It prevents people from accessing jobs",
     "It has no relationship to land use", "A"),

    ("Why can the loss of agricultural land around expanding cities be a concern?",
     "Agricultural land has no ecological or economic value",
     "It can reduce local food-producing areas and affect rural livelihoods",
     "Urban expansion always increases farmland",
     "Food production never depends on land", "B"),

    ("Why should population projections be used carefully in infrastructure planning?",
     "Population never changes",
     "All projections are exact predictions",
     "They depend on assumptions about fertility, mortality and migration that may change",
     "Infrastructure has no relationship to population", "C"),

    ("Why can a settlement have a high population density but relatively poor living conditions?",
     "High density always guarantees excellent services",
     "Population density measures household income exactly",
     "Dense settlements never experience overcrowding",
     "Housing shortages, inadequate infrastructure and unequal access to services can reduce living conditions", "D"),

    ("Why is the age-sex structure of a population important for public policy?",
     "It helps estimate differing needs for education, healthcare, employment and social support",
     "It determines the exact rainfall of the next decade",
     "It eliminates the need for a census",
     "It measures the size of every road", "A"),

    ("What is the most appropriate way to plan for rapid population growth in a city?",
     "Ignore future demand and build only after shortages occur",
     "Use population projections, inclusive land-use planning and investment in infrastructure and services",
     "Prevent the development of public transport",
     "Remove water and sanitation services from expanding areas", "B"),
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
                "\nSUCCESS: Population and Settlements has "
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