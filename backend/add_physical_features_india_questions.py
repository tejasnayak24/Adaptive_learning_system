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
LESSON_TITLE = "Physical Features of India"


# =========================================================
# EASY QUESTIONS — 30
# =========================================================

EASY = [
    ("Which mountain range forms India's northern boundary?",
     "The Himalayas", "The Aravalli Range", "The Western Ghats",
     "The Eastern Ghats", "A"),

    ("Which is the highest mountain range in India?",
     "Vindhya Range", "Himalayas", "Satpura Range",
     "Aravalli Range", "B"),

    ("Which major physical division lies south of the Himalayas?",
     "The Thar Desert", "The coastal plains",
     "The Northern Plains", "The Indian Ocean", "C"),

    ("Which rivers have formed much of the Northern Plains?",
     "Narmada and Tapi", "Godavari and Krishna",
     "Mahanadi and Kaveri", "Indus, Ganga and Brahmaputra systems", "D"),

    ("Which physical division covers much of peninsular India?",
     "The Peninsular Plateau", "The Northern Plains",
     "The Himalayan Mountains", "The islands only", "A"),

    ("Which desert is located mainly in northwestern India?",
     "Sahara Desert", "Thar Desert", "Gobi Desert",
     "Kalahari Desert", "B"),

    ("Which mountain range runs along much of India's western coast?",
     "Eastern Ghats", "Aravalli Range", "Western Ghats",
     "Himalayas", "C"),

    ("Which mountain range lies along parts of India's eastern side of the plateau?",
     "Himalayas", "Aravalli Range", "Western Ghats",
     "Eastern Ghats", "D"),

    ("Which body of water lies to the west of India?",
     "Arabian Sea", "Bay of Bengal", "Red Sea",
     "South China Sea", "A"),

    ("Which body of water lies to the east of India?",
     "Arabian Sea", "Bay of Bengal", "Mediterranean Sea",
     "Black Sea", "B"),

    ("Which ocean lies south of India?",
     "Atlantic Ocean", "Pacific Ocean", "Indian Ocean",
     "Arctic Ocean", "C"),

    ("Which island group lies in the Arabian Sea?",
     "Andaman and Nicobar Islands", "Sundarbans",
     "Sri Lanka", "Lakshadweep Islands", "D"),

    ("Which island group lies in the Bay of Bengal?",
     "Andaman and Nicobar Islands", "Lakshadweep Islands",
     "Maldives", "Lakshadweep and Maldives together", "A"),

    ("What is a plateau?",
     "A deep valley below sea level", "An elevated area with a relatively flat top",
     "A narrow river channel", "A sandy beach only", "B"),

    ("What is a plain?",
     "A steep mountain slope", "A volcanic crater only",
     "A broad area of relatively flat land", "A deep ocean trench", "C"),

    ("What is a mountain?",
     "A low area covered only by sand", "A flat coastal area",
     "A river delta", "A major natural elevation of Earth's surface", "D"),

    ("Which physical division is known for fertile alluvial soil?",
     "The Northern Plains", "The Thar Desert",
     "The high Himalayan peaks", "The rocky islands only", "A"),

    ("Which river is associated with the western part of the Northern Plains?",
     "Kaveri", "Indus", "Godavari", "Krishna", "B"),

    ("Which river flows through Assam as part of the Brahmaputra system?",
     "Narmada", "Tapi", "Brahmaputra", "Mahi", "C"),

    ("Which physical division contains many old crystalline rocks?",
     "The Northern Plains", "The coastal wetlands only",
     "The Ganga delta only", "The Peninsular Plateau", "D"),

    ("What is a coastal plain?",
     "A low-lying area bordering the sea", "A high mountain peak",
     "A dry inland plateau only", "A frozen polar region", "A"),

    ("Which coast is located along India's western side?",
     "Coromandel Coast", "Western coastal region",
     "Northern Plains", "Malabar is not a coastal region", "B"),

    ("Which coast is associated with much of Tamil Nadu's eastern shoreline?",
     "Malabar Coast", "Konkan Coast", "Coromandel Coast",
     "Kutch coast only", "C"),

    ("Which physical feature separates much of the Deccan Plateau from the western coast?",
     "Eastern Himalayas", "Aravalli Range",
     "Shivalik Hills", "Western Ghats", "D"),

    ("What is a delta?",
     "A landform formed by sediment deposition near a river's mouth",
     "A high mountain pass", "A desert dune",
     "A glacier's source", "A"),

    ("Which major delta is associated with the Ganga and Brahmaputra river systems?",
     "Narmada Delta", "Ganga-Brahmaputra Delta",
     "Tapi Delta only", "Indus Delta only", "B"),

    ("Which region of India is particularly known for sand dunes?",
     "The Northern Plains", "The Himalayan foothills",
     "The Thar Desert", "The Western coastal plains only", "C"),

    ("Which physical division is home to many glaciers?",
     "The Deccan Plateau", "The eastern coastal plains",
     "The Thar Desert", "The Himalayas", "D"),

    ("What is a valley?",
     "Low land between hills or mountains",
     "The highest point of a mountain", "An isolated island",
     "A flat ocean floor only", "A"),

    ("Why are India's physical features important?",
     "They have no effect on human activities",
     "They influence climate, agriculture, settlement and transport",
     "They prevent all rainfall", "They make every region identical", "B"),
]


# =========================================================
# MEDIUM QUESTIONS — 30
# =========================================================

MEDIUM = [
    ("Why are the Northern Plains generally suitable for agriculture?",
     "They have extensive fertile alluvial deposits and relatively level land",
     "They receive no rainfall",
     "They consist entirely of bare rock",
     "They have permanently frozen soil", "A"),

    ("How were much of the Northern Plains formed?",
     "By recent volcanic eruptions only",
     "By deposition of sediments brought by river systems",
     "By coral growth alone",
     "By wind erosion alone", "B"),

    ("Why is the Peninsular Plateau considered an ancient landmass?",
     "It formed entirely from recent river deposits",
     "It consists only of loose desert sand",
     "It contains old, stable rock formations",
     "It is made entirely of modern coral reefs", "C"),

    ("What is one important difference between the Himalayas and the Peninsular Plateau?",
     "Both are equally young fold mountains",
     "The plateau consists only of recent alluvium",
     "The Himalayas are older than every rock in the plateau",
     "The Himalayas are young fold mountains, while the plateau is an older stable landmass", "D"),

    ("Why do the Western Ghats influence rainfall in western India?",
     "They force moist winds to rise, encouraging orographic rainfall",
     "They prevent the Arabian Sea from evaporating",
     "They stop all monsoon winds",
     "They create rainfall only in winter", "A"),

    ("Why are some areas east of the Western Ghats relatively dry?",
     "They are below sea level",
     "They can lie in the rain shadow of the Western Ghats",
     "They have no atmosphere",
     "The Sun never reaches them", "B"),

    ("What is the general difference between the Western and Eastern Ghats?",
     "The Eastern Ghats form one continuous higher wall",
     "The Western Ghats are entirely below sea level",
     "The Western Ghats are generally more continuous, while the Eastern Ghats are more discontinuous",
     "The two ranges are identical in every respect", "C"),

    ("Why are many Himalayan rivers perennial?",
     "They flow only during summer rainfall",
     "They have no tributaries",
     "They dry completely every winter",
     "They receive water from rainfall and, in many upper catchments, snow and glacier melt", "D"),

    ("What is a major difference between Himalayan and many Peninsular rivers?",
     "Many Himalayan rivers have large snow-fed catchments, while many Peninsular rivers depend more on rainfall",
     "All Peninsular rivers are longer than Himalayan rivers",
     "Himalayan rivers never flood",
     "Peninsular rivers never form valleys", "A"),

    ("Why are river valleys important for human settlement?",
     "They prevent farming",
     "They can provide water, fertile land and transport routes",
     "They contain no natural resources",
     "They are always free from floods", "B"),

    ("What is the Bhabar belt in the Himalayan foothill region?",
     "A coastal marsh",
     "A high desert plateau",
     "A porous belt of coarse sediments where streams may disappear underground",
     "A delta at the mouth of the Ganga", "C"),

    ("What characterises the Terai region?",
     "A high snow-covered summit",
     "A dry rocky plateau",
     "A coral island",
     "A relatively wet, marshy belt south of the Bhabar", "D"),

    ("What is the Bhangar?",
     "Older alluvium found on relatively higher parts of the Northern Plains",
     "Newer alluvium deposited every year",
     "A mountain range in southern India",
     "A volcanic island group", "A"),

    ("What is the Khadar?",
     "A type of desert dune",
     "Newer alluvium associated with active floodplains",
     "A high Himalayan peak",
     "A coastal mountain range", "B"),

    ("Why can the Khadar be agriculturally productive?",
     "It has no water supply",
     "It contains only exposed bedrock",
     "New alluvial deposits can replenish soil nutrients",
     "It is permanently frozen", "C"),

    ("Which physical feature is strongly associated with the formation of the Thar Desert?",
     "Heavy year-round rainfall everywhere",
     "Permanent glaciers",
     "Dense tropical rainforest throughout",
     "Arid conditions and limited rainfall", "D"),

    ("Why are the Himalayas important for India's river systems?",
     "They contain snowfields and glaciers that feed several major river systems",
     "They prevent all rivers from flowing south",
     "They have no influence on drainage",
     "They are made entirely of sand dunes", "A"),

    ("What is the significance of the Deccan Trap region?",
     "It is a recent coral reef",
     "It includes extensive basaltic lava formations",
     "It is a glacier-covered coastal plain",
     "It is a part of the Thar Desert", "B"),

    ("Why do many east-flowing Peninsular rivers form large deltas?",
     "They flow entirely underground",
     "They never carry sediments",
     "They deposit sediments as they approach their mouths on relatively broad coastal plains",
     "They all end in inland deserts", "C"),

    ("Why do the Narmada and Tapi rivers differ from many other major Peninsular rivers?",
     "They flow into the Bay of Bengal",
     "They originate in the Himalayas",
     "They form the Ganga-Brahmaputra Delta",
     "They flow westward through rift valleys toward the Arabian Sea", "D"),

    ("What is the importance of the coastal plains?",
     "They support ports, fishing, farming and settlements",
     "They contain no human settlements",
     "They prevent all maritime trade",
     "They are all high mountain ranges", "A"),

    ("Why are islands strategically important?",
     "They eliminate the need for coastal security",
     "They can support maritime activity and help monitor surrounding sea areas",
     "They have no relationship to sea routes",
     "They prevent ships from entering oceans", "B"),

    ("Which physical division contains the Karakoram and many high Himalayan ranges?",
     "The eastern coastal plains",
     "The Thar Desert",
     "The northern mountainous region",
     "The Lakshadweep Islands", "C"),

    ("What is the significance of mountain passes?",
     "They prevent all movement across mountains",
     "They occur only in deserts",
     "They are always underwater",
     "They provide routes through mountain barriers", "D"),

    ("Why can the Himalayas act as a climatic barrier?",
     "They influence the movement of air masses and help block some cold winds from the north",
     "They stop Earth from rotating",
     "They eliminate the summer monsoon",
     "They prevent every form of precipitation", "A"),

    ("How can relief affect the distribution of population?",
     "People always settle only at the highest peaks",
     "Steep terrain can make transport, farming and construction more difficult",
     "Relief never influences settlement",
     "All plateaus are uninhabitable", "B"),

    ("Why is the Peninsular Plateau important for mineral resources?",
     "It consists entirely of recent river mud",
     "It has no exposed rocks",
     "Its ancient rock formations contain a variety of mineral deposits",
     "All minerals are restricted to coastal beaches", "C"),

    ("Which feature is commonly associated with the western coastal plain?",
     "It lies entirely north of the Himalayas",
     "It consists only of sand dunes",
     "It has no ports or settlements",
     "It is a relatively narrow coastal strip between the Western Ghats and the Arabian Sea in many areas", "D"),

    ("Why do some parts of India's eastern coast experience cyclones?",
     "The Bay of Bengal is a region where tropical cyclones can develop and move toward the coast",
     "The eastern coast has no sea",
     "The Himalayas create every cyclone directly",
     "Cyclones can occur only in deserts", "A"),

    ("How do physical features influence transportation networks?",
     "Mountains and rivers never affect routes",
     "Relief can require tunnels, bridges, passes and alternative routes",
     "All roads must follow the equator",
     "Transport routes are unrelated to landforms", "B"),
]


# =========================================================
# HARD QUESTIONS — 30
# =========================================================

HARD = [
    ("Why are the Himalayas described as young fold mountains?",
     "They formed through relatively recent geological compression and folding associated with plate convergence",
     "They are made entirely of new river sediment",
     "They were formed by modern human construction",
     "They are older than Earth's crust", "A"),

    ("What geological process contributed substantially to the formation of the Himalayas?",
     "The separation of the Moon from Earth",
     "The collision of the Indian Plate with the Eurasian Plate",
     "The freezing of the Indian Ocean",
     "The movement of desert dunes alone", "B"),

    ("Why does the Peninsular Plateau have a comparatively stable geological structure?",
     "It is formed entirely of loose alluvium",
     "It is a young delta",
     "It is part of an ancient, relatively stable continental block",
     "It moves several kilometres every year", "C"),

    ("Why do the Himalayas continue to experience earthquakes?",
     "All tectonic movement ended millions of years ago",
     "They are made only of sand",
     "Earthquakes occur only near the equator",
     "The Indian and Eurasian plates continue to interact and deform the region", "D"),

    ("What explains the presence of black soil across parts of the Deccan Plateau?",
     "Weathering of basaltic volcanic rocks in many areas",
     "Deposition of Himalayan glacier ice",
     "Coral growth in an ancient ocean everywhere",
     "Accumulation of desert dunes only", "A"),

    ("Why are the Western Ghats important for the Indian monsoon?",
     "They stop all winds from reaching India",
     "They force moist westerly monsoon air upward, causing heavy orographic rainfall on windward slopes",
     "They eliminate rainfall on the western coast",
     "They reverse Earth's rotation", "B"),

    ("What causes the rain-shadow effect east of a mountain range?",
     "Air becomes permanently colder as it descends",
     "All moisture moves underground",
     "Air loses moisture on the windward side and often descends warmer and drier on the leeward side",
     "Mountains prevent the Sun from shining", "C"),

    ("Why do the Indus, Ganga and Brahmaputra river systems have extensive alluvial plains?",
     "They carry no sediment",
     "They flow only through hard rock",
     "They are entirely artificial rivers",
     "They transport and deposit sediments over broad low-lying areas", "D"),

    ("What is the geological significance of a rift valley?",
     "It is a depressed area formed by tectonic faulting",
     "It is always a river delta",
     "It is a type of coral reef",
     "It is a sand dune created by wind", "A"),

    ("Why do the Narmada and Tapi flow through rift valleys?",
     "They follow the Himalayan crest",
     "Their courses are associated with faulted and down-dropped geological structures",
     "They flow across the Bay of Bengal",
     "They are artificial canals", "B"),

    ("Why do many east-flowing rivers of the Peninsular Plateau form deltas?",
     "They all flow into the Arabian Sea",
     "They carry no sediment",
     "Their sediments accumulate near river mouths along broad coastal plains",
     "They end at the top of the Western Ghats", "C"),

    ("Why do the Narmada and Tapi generally form estuaries rather than the large deltas typical of many east-flowing rivers?",
     "They are glacier-fed rivers flowing north",
     "They have no mouths",
     "They end in inland lakes",
     "Their westward courses through rift valleys and coastal conditions favour estuarine mouths", "D"),

    ("What is the main geomorphological difference between an estuary and a delta?",
     "An estuary is a tidal river mouth, while a delta is formed by sediment accumulation at a river mouth",
     "An estuary is always a mountain",
     "A delta forms only in deserts",
     "They are exactly the same landform", "A"),

    ("Why are alluvial fans often found where streams emerge from mountain valleys onto flatter plains?",
     "Water flows faster on every flat surface",
     "A stream may lose energy and deposit sediment as the gradient decreases",
     "The river turns into a glacier",
     "The mountains absorb all the water", "B"),

    ("Why can the Bhabar belt have fewer surface streams than nearby regions?",
     "It receives no precipitation",
     "It lies under the ocean",
     "Coarse, porous sediments allow streams to seep underground",
     "All rivers flow uphill there", "C"),

    ("What explains the wetter conditions often associated with the Terai belt?",
     "It lies at the top of the Himalayas",
     "It contains only exposed bedrock",
     "It is a polar desert",
     "Groundwater emerging from the porous Bhabar belt can contribute to wet, marshy conditions", "D"),

    ("Why can the Khadar belt be renewed more frequently than the Bhangar belt?",
     "Khadar is associated with active floodplains that receive newer alluvial deposits",
     "Khadar is a permanent mountain glacier",
     "Bhangar forms only on ocean islands",
     "Bhangar is renewed by every daily tide", "A"),

    ("Which statement best explains the relationship between physical relief and river drainage patterns?",
     "Rivers always flow in straight lines regardless of relief",
     "Relief and geological structure influence river direction, gradient and valley form",
     "Rivers have no relationship to slopes",
     "All rivers flow toward the highest mountain", "B"),

    ("Why can the Himalayan region experience landslides during heavy rainfall?",
     "All mountain slopes are completely flat",
     "Rainfall permanently strengthens every slope",
     "Water can raise pore pressure and weaken slope materials, especially on unstable terrain",
     "Landslides occur only on beaches", "C"),

    ("Why is the Himalayan region especially sensitive to certain natural hazards?",
     "It has no steep slopes",
     "It is free from tectonic activity",
     "It has no rivers",
     "Steep relief, active tectonics, intense rainfall and other local conditions can combine to increase risk", "D"),

    ("What is the primary reason the Thar Desert has sparse vegetation in many areas?",
     "Low and irregular rainfall limits available water",
     "It receives heavy rainfall throughout the year",
     "The soil is permanently covered by glaciers",
     "The region has no sunlight", "A"),

    ("Why do sand dunes form in arid regions?",
     "Rivers deposit only large boulders",
     "Wind transports and deposits sand when its carrying capacity decreases",
     "Glaciers melt into sand",
     "Earthquakes turn every rock into a dune", "B"),

    ("How can the physical geography of the Indian coastline affect settlement patterns?",
     "Coasts are always unsuitable for settlement",
     "All coasts have identical terrain",
     "Ports, estuaries, fertile deltas and low-lying land can attract settlements but may also face hazards",
     "Coastal landforms do not affect human activity", "C"),

    ("Why are the Andaman and Nicobar Islands geographically distinct from Lakshadweep?",
     "Both groups are identical coral atolls",
     "Both lie in the Arabian Sea",
     "Lakshadweep is a Himalayan mountain range",
     "Andaman and Nicobar lie in the Bay of Bengal region, while Lakshadweep lies in the Arabian Sea and is largely coral in origin", "D"),

    ("Why are coral islands generally sensitive to changes in sea conditions?",
     "Coral reef ecosystems depend on particular marine environmental conditions",
     "Coral islands are made entirely of Himalayan granite",
     "They never experience coastal erosion",
     "They are unaffected by water temperature or sea level", "A"),

    ("What is the significance of the Deccan Trap's basaltic formations?",
     "They were deposited by the Ganga floodplain",
     "They record extensive ancient volcanic lava flows",
     "They are made entirely of coral",
     "They formed from recent glacial deposits", "B"),

    ("Why can the Himalayas influence the distribution of natural vegetation?",
     "Vegetation is unrelated to altitude",
     "Every Himalayan slope has the same climate",
     "Altitude, temperature, rainfall and slope aspect vary across the mountain region",
     "All vegetation stops at the foothills", "C"),

    ("Why do the Northern Plains support dense populations in many areas?",
     "They have no rivers",
     "They are permanently frozen",
     "They contain no cultivable land",
     "Fertile soils, water availability, relatively level terrain and transport routes support settlement", "D"),

    ("How can river flooding both benefit and harm the Northern Plains?",
     "Floods can deposit fertile sediment but can also damage settlements, crops and infrastructure",
     "Floods only improve conditions and never cause damage",
     "Floods permanently eliminate soil fertility",
     "Floods cannot affect human activity", "A"),

    ("Why should physical geography be considered when planning infrastructure in India?",
     "All regions have identical geological and climatic conditions",
     "Terrain, geology, rivers, coastlines and hazards affect design, cost and safety",
     "Infrastructure never interacts with landforms",
     "Physical geography matters only for tourism", "B"),
]


# =========================================================
# VALIDATE ALL QUESTION BANKS BEFORE DATABASE CHANGES
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
                "\nSUCCESS: Physical Features of India has "
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