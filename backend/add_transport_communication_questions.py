import os
import random
import logging
from pathlib import Path

logging.disable(logging.CRITICAL)

# --------------------------------------------------
# DATABASE CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "adaptive_learning.db"

os.environ["DATABASE_URL"] = (
    f"sqlite:///{DATABASE_PATH.as_posix()}"
)

from app.database.connection import SessionLocal
from app.models.student import Student
from app.models.lesson import Lesson
from app.models.quiz import Quiz
from app.models.question import Question
from app.models.progress import Progress
from app.models.session import LearningSession
from app.models.reward import RewardHistory


# --------------------------------------------------
# QUESTION BANK
# Every question must contain exactly 6 values:
# question, option A, option B, option C, option D,
# correct answer letter
# --------------------------------------------------

EASY = [
    ("What is transportation?", "Movement of people and goods", "Growing crops", "Making laws", "Producing electricity", "A"),
    ("Which of these is a means of road transport?", "Bus", "Ship", "Aeroplane", "Submarine", "A"),
    ("Which vehicle travels on railway tracks?", "Train", "Car", "Bicycle", "Tractor", "A"),
    ("Which transport is commonly used to cross oceans?", "Ship", "Bicycle", "Motorcycle", "Bullock cart", "A"),
    ("Which transport travels through the air?", "Aeroplane", "Train", "Bus", "Truck", "A"),
    ("What is communication?", "Sharing information", "Growing vegetables", "Building roads", "Mining coal", "A"),
    ("Which device is commonly used for telephone communication?", "Mobile phone", "Cooking stove", "Refrigerator", "Washing machine", "A"),
    ("Which is an example of written communication?", "Letter", "Handshake", "Facial expression", "Whistle", "A"),
    ("Which medium broadcasts programmes to listeners?", "Radio", "Bicycle", "Train", "Ship", "A"),
    ("Which medium provides television programmes?", "Television", "Plough", "Tractor", "Crane", "A"),
    ("Which of these is a traditional means of communication?", "Messenger carrying a letter", "Video conference", "Email", "Instant messaging", "A"),
    ("What is a road used for?", "Travel by road vehicles", "Travel only by ships", "Sending radio signals only", "Producing food", "A"),
    ("What is a railway station?", "A place where trains stop for passengers or goods", "A place where ships are built", "An airport runway", "A farming field", "A"),
    ("What is an airport mainly used for?", "Air travel", "Rail travel", "Road repair", "Fishing", "A"),
    ("Which transport is useful on navigable rivers?", "Boat", "Aeroplane", "Motorcycle", "Metro train", "A"),
    ("Which of these is a digital communication service?", "Email", "Bullock cart", "Hand plough", "Water pump", "A"),
    ("What does a postal service help people do?", "Send letters and parcels", "Grow crops", "Construct bridges", "Generate electricity", "A"),
    ("Which transport is often used for short trips within a town?", "Bicycle", "Cargo ship", "Long-distance aircraft", "Ocean liner", "A"),
    ("What is a bridge commonly built to do?", "Allow transport across an obstacle", "Broadcast television", "Store messages online", "Produce petrol", "A"),
    ("Which of these is a form of mass communication?", "Newspaper", "Private whisper", "Personal diary", "One-to-one handshake", "A"),
    ("What is a harbour?", "A sheltered place where ships can anchor", "A railway ticket", "An airport control tower", "A highway tunnel", "A"),
    ("Which transport is generally suitable for carrying heavy goods over long distances by sea?", "Cargo ship", "Bicycle", "Scooter", "Handcart", "A"),
    ("What is a traffic signal used for?", "Controlling road traffic", "Guiding ships underwater", "Printing newspapers", "Charging mobile phones", "A"),
    ("Which of these helps people communicate across long distances instantly?", "Telephone call", "Handwritten message carried on foot", "Notice board in a village", "Printed book", "A"),
    ("What is a newspaper?", "A publication containing news and information", "A type of vehicle", "A railway line", "A communication tower", "A"),
    ("Which transport is commonly used to carry containers between countries by sea?", "Cargo ship", "Bicycle", "Auto-rickshaw", "Scooter", "A"),
    ("What is a railway track designed for?", "Movement of trains", "Movement of ships", "Flying aircraft", "Walking across rivers", "A"),
    ("Which is an example of non-verbal communication?", "Facial expression", "Email", "Newspaper article", "Text message", "A"),
    ("What is a bus stop?", "A place where buses pick up and drop off passengers", "A shipbuilding yard", "A railway engine", "An internet website", "A"),
    ("Why are roads important?", "They connect places and support travel", "They replace all communication", "They stop all trade", "They are used only for farming", "A"),
]

MEDIUM = [
    ("Why is road transport important in many parts of India?", "It connects towns, villages and markets", "It operates only across oceans", "It needs no roads", "It can carry only passengers", "A"),
    ("Why is railway transport useful for long-distance travel?", "It can carry many passengers and large quantities of goods", "It travels through the air", "It operates only on rivers", "It cannot carry freight", "A"),
    ("Which factor most directly affects the construction of roads in mountainous regions?", "Steep slopes and difficult terrain", "The colour of vehicles", "The number of television channels", "The language used in newspapers", "A"),
    ("Why is air transport particularly useful during emergencies?", "It can reach distant places quickly", "It always costs less than road travel", "It requires no airports or landing areas", "It is unaffected by all weather conditions", "A"),
    ("What is one important advantage of waterways for bulk cargo?", "They can transport large loads efficiently", "They connect every inland village directly", "They require no navigable water", "They are always faster than aircraft", "A"),
    ("Why are ports important for international trade?", "They enable ships to load and unload goods", "They manufacture every imported product", "They replace all roads and railways", "They provide internet access to every home", "A"),
    ("What is a major role of public transport?", "Moving many people using shared services", "Transporting only one person at a time", "Replacing all pedestrian paths", "Preventing people from reaching workplaces", "A"),
    ("How can a well-developed transport network help farmers?", "It helps move agricultural produce to markets", "It prevents produce from leaving farms", "It eliminates the need for storage", "It guarantees identical crop prices everywhere", "A"),
    ("Why can poor road connectivity affect rural development?", "It can make access to markets and services difficult", "It guarantees lower travel costs", "It removes the need for schools", "It increases access to every service automatically", "A"),
    ("What is the main purpose of a railway junction?", "Connecting railway routes", "Connecting television programmes", "Storing aircraft fuel only", "Printing railway maps for sale", "A"),
    ("How does the internet support modern communication?", "It enables rapid exchange of information worldwide", "It works only through printed letters", "It prevents digital information sharing", "It is used only for railway reservations", "A"),
    ("What is an advantage of video conferencing?", "People in different locations can communicate face to face online", "It always eliminates the need for electricity", "It requires everyone to be in one room", "It can transmit only handwritten letters", "A"),
    ("Why are newspapers considered mass media?", "They distribute information to many readers", "They communicate only with one person", "They are used exclusively for navigation", "They carry passengers between cities", "A"),
    ("What is the role of a communication satellite?", "Relaying signals over large distances", "Building roads across mountains", "Carrying freight on railway tracks", "Producing paper for newspapers", "A"),
    ("Why is mobile connectivity important in remote areas?", "It can improve access to information and services", "It makes roads unnecessary for all purposes", "It prevents emergency communication", "It guarantees uninterrupted service everywhere", "A"),
    ("Which transport mode is generally most suitable for urgent international passenger travel?", "Air transport", "Slow-moving cargo vessel", "Handcart", "Bullock cart", "A"),
    ("What is multimodal transportation?", "Using more than one transport mode for a journey or shipment", "Using only bicycles for all journeys", "Communicating through several languages", "Building several roads in one town", "A"),
    ("Why are warehouses often located near transport hubs?", "Goods can be transferred and distributed more easily", "Goods never need to be stored there", "Vehicles cannot reach these locations", "Communication becomes unnecessary", "A"),
    ("How can traffic congestion affect a city?", "It increases travel delays and can worsen air pollution", "It always reduces journey times", "It eliminates fuel consumption", "It improves every road's carrying capacity", "A"),
    ("Which action can help reduce transport-related air pollution in cities?", "Encouraging public transport and cleaner vehicles", "Increasing unnecessary private car journeys", "Keeping all engines poorly maintained", "Removing all pedestrian facilities", "A"),
    ("Why is communication important during natural disasters?", "It helps share warnings and coordinate emergency responses", "It prevents all natural hazards", "It removes the need for rescue teams", "It guarantees that no infrastructure will be damaged", "A"),
    ("What is a major benefit of fibre-optic communication?", "It can transmit large amounts of data at high speeds", "It carries passengers between railway stations", "It replaces all electrical appliances", "It works only as a road surface", "A"),
    ("What is the digital divide?", "Unequal access to digital technology and internet services", "A physical gap between railway tracks", "A difference between ship sizes", "A division of roads into lanes", "A"),
    ("Why is reliable communication important for businesses?", "It supports coordination with customers, suppliers and employees", "It prevents businesses from sharing information", "It eliminates every business expense", "It removes the need to transport goods", "A"),
    ("What is one limitation of air freight compared with sea freight for heavy bulk goods?", "It is generally more expensive", "It cannot transport any goods", "It operates only on rivers", "It requires no fuel or infrastructure", "A"),
    ("Why do transport routes often develop near major cities?", "Cities concentrate people, jobs, markets and services", "Cities have no demand for travel", "Cities cannot exchange goods", "Transport routes need no users", "A"),
    ("How can online communication support education?", "It allows learners and teachers to exchange resources remotely", "It prevents access to learning materials", "It works only when students travel by train", "It replaces the need to understand lessons", "A"),
    ("Why should transport infrastructure be maintained regularly?", "Maintenance improves safety and reliability", "Maintenance guarantees that accidents become impossible", "It removes the need for traffic rules", "It makes all transport free", "A"),
    ("What is the main purpose of a logistics network?", "Coordinating the movement and storage of goods", "Producing television dramas", "Teaching only road signs", "Replacing all communication systems", "A"),
    ("Why can waterways be less suitable than roads for some inland destinations?", "Many places lack navigable waterways", "Ships can travel on every road", "Waterways never carry goods", "Roads cannot connect inland settlements", "A"),
]

HARD = [
    ("A company must move a large shipment of non-urgent goods overseas at low cost. Which option is generally most appropriate?", "Sea freight using cargo ships", "Individual air courier for every item", "Passenger taxis across the ocean", "Bicycles transported separately", "A"),
    ("A remote village is cut off during heavy rainfall. Which communication measure can best support emergency coordination when local mobile networks fail?", "Use available satellite or radio communication systems", "Wait until every road is repaired before sending any message", "Rely only on a newspaper delivered next week", "Disable all emergency communication equipment", "A"),
    ("A city wants to reduce congestion without restricting essential travel. Which policy package is most likely to help?", "Improve public transport, walking and cycling facilities", "Expand parking while discouraging public transport", "Remove bus services from busy routes", "Encourage every commuter to drive alone", "A"),
    ("A shipment must travel from an inland factory to an overseas customer. Which sequence is a plausible multimodal route?", "Truck to rail terminal, train to port, ship overseas", "Ship directly from the factory without reaching water", "Aircraft to a road lane, then a bicycle across the ocean", "Pedestrian path directly to the overseas warehouse", "A"),
    ("Why may building a highway through a fragile ecosystem require an environmental assessment?", "Construction can affect habitats, drainage and wildlife movement", "Highways have no possible environmental effects", "Assessment determines the colour of every vehicle", "The process guarantees that no land is used", "A"),
    ("A region has many small settlements separated by rivers and hills. What is the strongest planning approach for improving connectivity?", "Combine locally suitable roads, bridges and other transport links", "Build only a major airport and ignore local access", "Create a single port far from all settlements", "Replace transport links with printed advertisements", "A"),
    ("A transport planner compares cost, travel time and environmental impact. What is this an example of?", "Evaluating trade-offs among transport alternatives", "Choosing routes without considering evidence", "Measuring only vehicle colour", "Ignoring the needs of travellers", "A"),
    ("Why can dependence on a single transport corridor create a supply-chain risk?", "A disruption on that corridor may delay many shipments", "It guarantees that goods always arrive early", "It eliminates the need for backup plans", "It makes weather irrelevant to transport", "A"),
    ("A disaster damages mobile towers but a hospital needs to coordinate with rescue teams. Which option is a useful backup if available?", "Radio communication or satellite phones", "Only social media accessed through the failed network", "Printed posters that cannot be distributed", "A road traffic signal with no communication equipment", "A"),
    ("Which measure best addresses the digital divide in underserved communities?", "Improve affordable connectivity, devices and digital skills", "Make internet services more expensive", "Remove digital literacy programmes", "Restrict public access to online services", "A"),
    ("Why is end-to-end tracking valuable in freight transportation?", "It improves shipment visibility and helps identify delays", "It prevents the physical movement of goods", "It removes the need for accurate records", "It guarantees that every shipment is damage-free", "A"),
    ("A city has an overcrowded central railway station. Which intervention may improve passenger flow?", "Improve station layout, passenger information and service planning", "Block all station entrances during peak hours", "Remove signs and passenger information displays", "Reduce coordination between connecting services", "A"),
    ("Why is last-mile connectivity important in public transportation?", "It links major transport services with people's final destinations", "It refers only to international sea shipping", "It eliminates the need for public transport", "It describes the distance signals travel through space", "A"),
    ("A company needs to transport temperature-sensitive medicine over a long distance. What should its logistics plan prioritize?", "Suitable temperature control and reliable delivery arrangements", "The lowest price regardless of storage conditions", "Unmonitored exposure to changing temperatures", "Avoiding all packaging and tracking", "A"),
    ("Which approach can make transport planning more inclusive?", "Consult users with different mobility needs and improve accessibility", "Design services only for people who drive", "Remove ramps and accessible boarding facilities", "Ignore feedback from passengers", "A"),
    ("A coastal port becomes temporarily unusable after a storm. Why might a diversified transport network help?", "Alternative routes and modes may keep some shipments moving", "Every alternative route is guaranteed to have unlimited capacity", "A diversified network prevents all storms", "It removes the need to assess route conditions", "A"),
    ("What is a key concern when expanding roads to reduce congestion?", "Induced traffic may offset some congestion benefits", "Additional road capacity can never change travel behaviour", "Road expansion automatically removes all emissions", "Every new road eliminates the need for land", "A"),
    ("A remote district receives early cyclone warnings through radio, SMS and community networks. What is the key strength of this approach?", "Multiple channels can improve the chance that warnings reach people", "It guarantees that every person receives every message", "It prevents cyclones from forming", "It makes emergency planning unnecessary", "A"),
    ("Why can integrated ticketing improve a public transport system?", "Passengers can transfer between services more conveniently", "It forces every passenger to use a private car", "It removes the need for route information", "It prevents connections between transport modes", "A"),
    ("A logistics manager must deliver urgent small medical supplies to a remote area with poor roads. Which factor could make air transport preferable?", "Speed and access when surface routes are difficult", "The assumption that air transport is always the cheapest", "The absence of any need for landing arrangements", "A guarantee that weather cannot cause delays", "A"),
    ("Why should transport systems consider both passenger and freight requirements?", "Their needs influence capacity, scheduling and infrastructure design", "Passenger and freight movement never interact", "Freight movement does not use infrastructure", "Passenger demand never changes", "A"),
    ("A country improves broadband infrastructure but many residents cannot use online services confidently. What additional action is most relevant?", "Provide digital literacy training and accessible support", "Remove public information about online services", "Increase complexity without user assistance", "Limit educational resources to printed advertisements", "A"),
    ("Why can accurate weather information be important for aviation and shipping?", "It supports safer route and operational decisions", "It removes the need for trained operators", "It guarantees that every journey is risk-free", "It replaces navigation equipment entirely", "A"),
    ("A town is planning a new bus network. Which data would best support route design?", "Population distribution, travel demand and destination patterns", "The colour preferences of vehicle manufacturers alone", "The number of newspapers printed nationally", "The distance between unrelated television studios", "A"),
    ("Why might rail transport be preferred for moving heavy freight along a suitable inland corridor?", "It can move large loads efficiently over established routes", "It can reach every home without connecting infrastructure", "It never requires maintenance", "It is always faster than air transport", "A"),
    ("A communication network remains operational after one link fails because traffic can use another link. Which design principle does this illustrate?", "Redundancy and resilience", "Single-point dependency", "Information isolation", "Permanent disconnection", "A"),
    ("Why can unplanned urban growth increase transport problems?", "Travel demand may grow faster than transport infrastructure and services", "It automatically creates sufficient public transport", "It removes the need for road maintenance", "It guarantees shorter commutes for everyone", "A"),
    ("A company compares air, rail, road and sea options for a shipment. Which decision method is most defensible?", "Compare cost, urgency, cargo type, route access and environmental impact", "Always select the fastest mode regardless of all other needs", "Always select the cheapest quoted price without checking reliability", "Choose a mode based only on its popularity", "A"),
    ("Why should emergency communication plans include accessible formats and multiple languages where needed?", "Different communities must be able to understand and act on warnings", "All people use the same language and communication method", "Accessible formats make warnings less useful", "Emergency information should reach only transport operators", "A"),
    ("A region wants to improve economic access while limiting emissions. Which strategy best balances both goals?", "Coordinate public transport, efficient freight, active travel and cleaner technology", "Expand private vehicle use without improving alternatives", "Stop all transport links to rural areas", "Ignore emissions and accessibility in planning", "A"),
]


# --------------------------------------------------
# VALIDATE THE QUESTION BANK BEFORE DATABASE CHANGES
# --------------------------------------------------

BANKS = {
    "Easy": EASY,
    "Medium": MEDIUM,
    "Hard": HARD,
}

for difficulty, bank in BANKS.items():
    if len(bank) != 30:
        raise ValueError(
            f"{difficulty} bank must contain 30 questions; found {len(bank)}."
        )

    for index, item in enumerate(bank, start=1):
        if len(item) != 6:
            raise ValueError(
                f"{difficulty} question {index} has {len(item)} values; expected 6."
            )

        if item[5] not in {"A", "B", "C", "D"}:
            raise ValueError(
                f"{difficulty} question {index} has an invalid answer key: {item[5]}"
            )

print("Question bank validation passed: 30 Easy, 30 Medium, 30 Hard.")


# --------------------------------------------------
# SHUFFLE OPTIONS AND PRESERVE THE CORRECT ANSWER
# --------------------------------------------------

def shuffle_options(item):
    question, a, b, c, d, correct = item

    options = [
        ("A", a),
        ("B", b),
        ("C", c),
        ("D", d),
    ]

    correct_text = dict(options)[correct]
    random.shuffle(options)

    shuffled_options = [option_text for _, option_text in options]
    new_correct = "ABCD"[shuffled_options.index(correct_text)]

    return (
        question,
        shuffled_options[0],
        shuffled_options[1],
        shuffled_options[2],
        shuffled_options[3],
        new_correct,
    )


# --------------------------------------------------
# INSERT QUESTIONS INTO THE EXISTING DATABASE
# --------------------------------------------------

db = SessionLocal()

try:
    lesson = (
        db.query(Lesson)
        .filter(
            Lesson.title == "Transport and Communication",
            Lesson.topic == "Social Science",
        )
        .first()
    )

    if lesson is None:
        raise RuntimeError(
            "Lesson 'Transport and Communication' was not found under "
            "Social Science. No questions were inserted."
        )

    for difficulty, bank in BANKS.items():
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
                title=f"Transport and Communication - {difficulty}",
                difficulty=difficulty,
            )
            db.add(quiz)
            db.flush()

        existing_questions = {
            q.question.strip().casefold()
            for q in db.query(Question)
            .filter(Question.quiz_id == quiz.id)
            .all()
        }

        added = 0

        for original_item in bank:
            item = shuffle_options(original_item)
            question_text = item[0].strip()

            if question_text.casefold() in existing_questions:
                continue

            question, a, b, c, d, correct = item

            db.add(
                Question(
                    quiz_id=quiz.id,
                    question=question,
                    option_a=a,
                    option_b=b,
                    option_c=c,
                    option_d=d,
                    correct_answer=correct,
                )
            )

            existing_questions.add(question_text.casefold())
            added += 1

        db.flush()
        print(f"{difficulty}: added {added} new questions.")

    db.commit()

    print("\n========== FINAL VERIFICATION ==========")

    total = 0

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
            db.query(Question)
            .filter(Question.quiz_id == quiz.id)
            .count()
            if quiz
            else 0
        )

        total += count
        print(f"{difficulty}: {count}/30")

    print(f"TOTAL: {total}/90")

    if total == 90:
        print("SUCCESS: Transport and Communication has 90 questions.")
    else:
        print(
            "WARNING: The lesson does not yet contain exactly 90 questions. "
            "Check the counts above."
        )

except Exception:
    db.rollback()
    raise

finally:
    db.close()