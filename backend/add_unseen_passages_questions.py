
import random
import sqlite3
from pathlib import Path

# --------------------------------------------------
# DATABASE CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 155
TOPIC = "English"

DIFFICULTIES = ["Easy", "Medium", "Hard"]


# --------------------------------------------------
# QUESTION BANK
# Each passage has 5 questions.
# 6 passages x 5 questions = 30 per difficulty.
# --------------------------------------------------

def make_questions(passages):
    questions = []

    for passage, items in passages:
        for question, correct, wrong1, wrong2, wrong3 in items:
            full_question = (
                f"Read the passage:\n{passage}\n\n"
                f"Question: {question}"
            )

            questions.append((
                full_question,
                correct,
                wrong1,
                wrong2,
                wrong3
            ))

    return questions


EASY_PASSAGES = [
    (
        "Maya has a small garden behind her house. "
        "She grows roses, sunflowers, and tomatoes. "
        "Every morning, she waters the plants. "
        "Butterflies often visit the colourful flowers.",
        [
            ("Where is Maya's garden?", "Behind her house", "Near her school", "On the roof", "Inside her classroom"),
            ("Which vegetable does Maya grow?", "Tomatoes", "Potatoes", "Carrots", "Onions"),
            ("When does Maya water the plants?", "Every morning", "Every night", "Once a week", "At noon only"),
            ("Which insects visit the flowers?", "Butterflies", "Ants", "Mosquitoes", "Beetles"),
            ("What is the passage mainly about?", "Maya's garden", "Maya's school", "A butterfly farm", "A vegetable market"),
        ]
    ),
    (
        "Rohan enjoys reading books. Every Saturday, he visits "
        "the library near his home. He usually borrows two books "
        "and returns them the following week. His favourite books "
        "are adventure stories.",
        [
            ("What does Rohan enjoy doing?", "Reading books", "Playing football", "Painting pictures", "Cooking food"),
            ("When does he visit the library?", "Saturday", "Monday", "Wednesday", "Friday"),
            ("Where is the library?", "Near his home", "Near his office", "Inside his school", "Next to a hospital"),
            ("How many books does he usually borrow?", "Two", "One", "Three", "Five"),
            ("What type of books does he like most?", "Adventure stories", "History books", "Science journals", "Poetry books"),
        ]
    ),
    (
        "The school organised a cleanliness drive on Friday. "
        "Students collected plastic waste from the playground. "
        "Teachers explained the importance of keeping the "
        "environment clean. Everyone worked together.",
        [
            ("What did the school organise?", "A cleanliness drive", "A music competition", "A sports day", "A science exhibition"),
            ("When was the drive organised?", "Friday", "Monday", "Tuesday", "Sunday"),
            ("What did students collect?", "Plastic waste", "Books", "Flowers", "Old clothes"),
            ("Where did students collect waste?", "The playground", "The library", "The canteen", "The laboratory"),
            ("What did teachers explain?", "The importance of cleanliness", "How to play cricket", "How to cook food", "How to paint walls"),
        ]
    ),
    (
        "A farmer planted rice in his field during the rainy season. "
        "He worked hard and regularly checked the crops. "
        "After several months, the rice was ready for harvesting. "
        "The farmer was happy with his good harvest.",
        [
            ("What did the farmer plant?", "Rice", "Wheat", "Cotton", "Sugarcane"),
            ("When did he plant the crop?", "During the rainy season", "During winter", "During summer", "During autumn"),
            ("What did he regularly check?", "The crops", "The road", "The house", "The market"),
            ("When was the rice ready?", "After several months", "After one day", "After one week", "After one hour"),
            ("How did the farmer feel about the harvest?", "Happy", "Angry", "Afraid", "Disappointed"),
        ]
    ),
    (
        "Anita wanted to improve her health. She started walking "
        "for thirty minutes every morning. She also began eating "
        "fresh fruits and vegetables. After a few weeks, she felt "
        "more active and energetic.",
        [
            ("What did Anita want to improve?", "Her health", "Her handwriting", "Her cooking", "Her singing"),
            ("How long did she walk?", "Thirty minutes", "Ten minutes", "One hour", "Two hours"),
            ("When did she walk?", "Every morning", "Every evening", "At midnight", "Only on Sundays"),
            ("What food did she start eating?", "Fresh fruits and vegetables", "Only sweets", "Fried snacks", "Fast food"),
            ("How did she feel after a few weeks?", "Active and energetic", "Tired and weak", "Angry and upset", "Bored and sleepy"),
        ]
    ),
    (
        "The town opened a new public park. It has walking paths, "
        "benches, and a children's play area. Families visit the park "
        "in the evening. The park gives people a pleasant place "
        "to relax.",
        [
            ("What did the town open?", "A public park", "A shopping mall", "A hospital", "A cinema"),
            ("What can children find in the park?", "A play area", "A swimming school", "A computer centre", "A library"),
            ("When do families visit?", "In the evening", "At midnight", "Early afternoon only", "Before sunrise"),
            ("What is available for walking?", "Walking paths", "Railway tracks", "Highways", "Building corridors"),
            ("Why do people visit the park?", "To relax", "To attend classes", "To buy groceries", "To repair vehicles"),
        ]
    ),
]


MEDIUM_PASSAGES = [
    (
        "Many cities are encouraging people to use public transport. "
        "Buses and trains can carry large numbers of passengers at once. "
        "This reduces the number of private vehicles on roads and may "
        "help decrease traffic congestion and air pollution. However, "
        "public transport must be reliable and convenient to attract users.",
        [
            ("What is the main purpose of the passage?", "To explain the benefits and requirements of public transport", "To describe private car manufacturing", "To compare different railway engines", "To discuss city tourism"),
            ("How can buses and trains reduce traffic?", "By carrying many passengers at once", "By increasing private vehicle ownership", "By reducing road space", "By stopping all city travel"),
            ("Which problem may public transport help reduce?", "Air pollution", "Rainfall", "Population growth", "Noise from nature"),
            ("What is necessary to attract more users?", "Reliable and convenient services", "Higher ticket prices", "Fewer routes", "Longer waiting times"),
            ("What can be inferred about public transport?", "Its success depends partly on service quality", "It is useful only in villages", "It completely eliminates pollution", "It should replace every road"),
        ]
    ),
    (
        "Bees play an important role in agriculture because they pollinate "
        "many flowering plants. During pollination, pollen is transferred "
        "between flowers, helping plants produce seeds and fruits. "
        "However, habitat loss and excessive pesticide use can threaten "
        "bee populations. Protecting flowering habitats can support them.",
        [
            ("What important role do bees perform?", "Pollination", "Seed storage", "Soil removal", "Water purification"),
            ("What happens during pollination?", "Pollen is transferred between flowers", "Roots change into leaves", "Fruits become flowers", "Seeds disappear"),
            ("Which factor threatens bee populations?", "Excessive pesticide use", "Planting native flowers", "Protecting habitats", "Reducing chemical exposure"),
            ("How can people support bees?", "By protecting flowering habitats", "By removing all flowers", "By destroying gardens", "By increasing pesticide use"),
            ("Why are bees important to agriculture?", "They help plants produce seeds and fruits", "They directly manufacture fertilisers", "They remove all crop diseases", "They replace irrigation systems"),
        ]
    ),
    (
        "Digital payments have changed the way many people make purchases. "
        "Customers can transfer money using mobile applications without "
        "carrying cash. These transactions are often convenient, but users "
        "must protect their passwords and avoid sharing confidential "
        "information with unknown people.",
        [
            ("What change is discussed in the passage?", "The growth of digital payments", "The decline of mobile technology", "The history of paper currency", "The development of public transport"),
            ("What can customers use to transfer money?", "Mobile applications", "Printed newspapers", "Library cards", "Television remotes"),
            ("What should users protect?", "Their passwords", "Their shopping bags", "Their notebooks", "Their furniture"),
            ("What should users avoid sharing?", "Confidential information", "Public advertisements", "Weather reports", "Product descriptions"),
            ("What is the central message?", "Digital payments are convenient but require careful security practices", "Digital payments are always unsafe", "Cash is never used anywhere", "Passwords should be shared freely"),
        ]
    ),
    (
        "Forests help regulate the climate by absorbing carbon dioxide "
        "and storing carbon. They also provide habitats for wildlife and "
        "help protect soil from erosion. When forests are cleared rapidly, "
        "these benefits are reduced. Sustainable forest management can "
        "help balance human needs with environmental protection.",
        [
            ("How do forests help regulate climate?", "By absorbing carbon dioxide", "By producing plastic", "By increasing soil erosion", "By blocking all sunlight"),
            ("What do forests provide for wildlife?", "Habitats", "Factories", "Road networks", "Artificial shelters only"),
            ("What may happen when forests are cleared rapidly?", "Environmental benefits are reduced", "Wildlife habitats always increase", "Soil becomes permanently protected", "Carbon storage becomes unlimited"),
            ("What does sustainable forest management aim to balance?", "Human needs and environmental protection", "Tourism and entertainment only", "Road construction and traffic", "Mining and manufacturing only"),
            ("Which statement best summarises the passage?", "Forests provide important environmental services and need careful management", "Forests are useful only for timber", "Forest clearing has no consequences", "Wildlife does not depend on forests"),
        ]
    ),
    (
        "Regular exercise supports physical and mental well-being. "
        "Activities such as walking, cycling, and swimming can improve "
        "fitness. Exercise may also help reduce stress and improve sleep. "
        "Health experts generally recommend choosing activities that "
        "match an individual's abilities and maintaining consistency.",
        [
            ("What is the passage mainly discussing?", "Benefits of regular exercise", "The history of swimming", "Professional sports competitions", "The design of fitness centres"),
            ("Which activity is mentioned?", "Cycling", "Painting", "Gardening only", "Reading"),
            ("How may exercise support mental well-being?", "By helping reduce stress", "By increasing confusion", "By preventing all emotions", "By reducing concentration"),
            ("Why should activities match individual abilities?", "To make exercise suitable for the person", "To make every person exercise equally", "To avoid all physical activity", "To guarantee professional performance"),
            ("What does consistency mean in this passage?", "Continuing the activity regularly", "Changing activities every minute", "Exercising only once", "Avoiding planned routines"),
        ]
    ),
    (
        "Libraries are adapting to changing learning needs. In addition "
        "to printed books, many now provide digital resources, computers, "
        "and online databases. These services allow visitors to access "
        "information in different formats. Libraries still play an "
        "important role in supporting education and independent learning.",
        [
            ("How are libraries adapting?", "By providing digital resources alongside printed books", "By removing all learning materials", "By becoming sports centres", "By limiting access to information"),
            ("Which facility may modern libraries provide?", "Online databases", "Vehicle repair shops", "Medical laboratories", "Food factories"),
            ("What do different formats allow visitors to do?", "Access information in different ways", "Avoid reading completely", "Stop using computers", "Replace education"),
            ("What role do libraries continue to play?", "Supporting education and independent learning", "Manufacturing electronic devices", "Organising road transport", "Providing private housing"),
            ("Which title best suits the passage?", "Modern Libraries and Changing Learning Needs", "The History of Farming", "How to Build a Computer", "The Decline of Education"),
        ]
    ),
]


HARD_PASSAGES = [
    (
        "Urban development frequently creates tension between economic "
        "growth and ecological preservation. New roads and buildings may "
        "improve connectivity and provide employment, yet poorly planned "
        "expansion can fragment habitats and increase surface runoff. "
        "Integrated planning attempts to evaluate these competing effects "
        "before irreversible changes occur.",
        [
            ("What central conflict does the passage identify?", "Economic development versus ecological preservation", "Tourism versus international trade", "Education versus technology", "Agriculture versus manufacturing"),
            ("What can poorly planned expansion cause?", "Habitat fragmentation and increased surface runoff", "Improved biodiversity in every location", "Complete elimination of flooding", "Automatic restoration of ecosystems"),
            ("What does the word 'irreversible' most nearly mean?", "Unable to be undone", "Easily repeated", "Temporarily delayed", "Carefully measured"),
            ("Why is integrated planning important?", "It evaluates competing effects before major changes occur", "It guarantees that development has no costs", "It prevents all construction permanently", "It considers employment but ignores ecology"),
            ("Which assumption underlies the passage?", "Development decisions can have long-term environmental consequences", "Economic growth always destroys every habitat", "Roads never provide social benefits", "Environmental effects are always temporary"),
        ]
    ),
    (
        "Scientific findings are rarely strengthened by repetition alone. "
        "A result becomes more convincing when independent researchers "
        "use transparent methods and obtain comparable evidence. "
        "Differences between studies do not necessarily indicate failure; "
        "they may reveal limitations, contextual factors, or questions "
        "that require further investigation.",
        [
            ("What makes a scientific result more convincing?", "Independent replication using transparent methods", "Repeated claims without evidence", "Avoiding comparison between studies", "Suppressing contradictory findings"),
            ("How should differences between studies be interpreted?", "As possible clues to limitations or contextual factors", "As automatic proof of fraud", "As evidence that research is unnecessary", "As reasons to discard every result"),
            ("What does 'independent' imply in the passage?", "Conducted separately by other researchers", "Copied without examination", "Controlled by the original author", "Completed without a method"),
            ("What is the author's attitude toward differing results?", "Analytical and open to further investigation", "Dismissive and hostile", "Unquestioningly supportive", "Entirely indifferent to evidence"),
            ("Which principle is most strongly supported?", "Scientific knowledge improves through transparent scrutiny", "A single study settles every question", "Repetition is more important than method", "Disagreement should be concealed"),
        ]
    ),
    (
        "The rapid expansion of artificial intelligence has prompted "
        "debates about accountability. Automated systems can process "
        "large datasets and support complex decisions, but their outputs "
        "may reflect biases present in training data. Effective oversight "
        "therefore requires documentation, evaluation, and clear "
        "responsibility for decisions influenced by these systems.",
        [
            ("What issue is central to the passage?", "Accountability in the use of artificial intelligence", "The history of computer hardware", "The cost of internet access", "The decline of scientific research"),
            ("Why might automated outputs reflect bias?", "Biases may exist in the training data", "Computers always reject data", "Algorithms operate without information", "All datasets are perfectly balanced"),
            ("What does 'oversight' most nearly mean?", "Supervision and monitoring", "Automatic expansion", "Complete independence", "Unplanned development"),
            ("Which measures does the passage identify as necessary?", "Documentation, evaluation, and clear responsibility", "Secrecy, speed, and unrestricted deployment", "Advertising, entertainment, and profit", "Data deletion and avoidance of review"),
            ("What can be inferred about AI-supported decisions?", "Human responsibility remains important", "They are always unbiased", "They require no evaluation", "They cannot influence real outcomes"),
        ]
    ),
    (
        "Water scarcity is not determined solely by the amount of rainfall "
        "a region receives. Infrastructure, distribution systems, "
        "consumption patterns, and governance also influence access. "
        "Consequently, a region may experience shortages even when "
        "its annual rainfall appears relatively high. Long-term solutions "
        "must address both supply and demand.",
        [
            ("What is the passage's main argument?", "Water scarcity depends on several factors beyond rainfall", "Rainfall alone determines water access", "High rainfall always prevents shortages", "Water demand is unrelated to infrastructure"),
            ("Which factor influences access to water?", "Distribution systems", "The colour of buildings", "The number of television channels", "The shape of vehicles"),
            ("Why might a high-rainfall region still face shortages?", "Its infrastructure or distribution may be inadequate", "Rainfall always disappears immediately", "Water cannot be stored anywhere", "Its population must be zero"),
            ("What does 'consequently' indicate?", "A result or conclusion", "A contrast", "A question", "An unrelated example"),
            ("What should long-term solutions address?", "Both water supply and demand", "Rainfall alone", "Only industrial profits", "Only seasonal forecasts"),
        ]
    ),
    (
        "Cultural heritage is not preserved merely by keeping old "
        "structures intact. Traditions, languages, craftsmanship, and "
        "community knowledge also contribute to cultural continuity. "
        "Preservation initiatives are more sustainable when local "
        "communities participate in decisions rather than being treated "
        "only as passive recipients of outside expertise.",
        [
            ("What broader view of cultural heritage does the passage present?", "It includes both physical structures and living traditions", "It consists only of ancient buildings", "It is limited to written records", "It excludes community knowledge"),
            ("Why is community participation important?", "It makes preservation more sustainable and inclusive", "It removes the need for local knowledge", "It guarantees that traditions never change", "It transfers every decision to outsiders"),
            ("What does 'passive recipients' suggest?", "People who receive decisions without actively shaping them", "People who lead every decision", "People who reject all assistance", "People who document every tradition"),
            ("Which element is explicitly identified as heritage?", "Craftsmanship", "Modern advertising", "Industrial machinery", "Traffic management"),
            ("What is the author's implied criticism?", "Preservation can fail when communities are excluded from decisions", "Old structures should always be demolished", "Outside expertise is never useful", "Traditions have no connection to identity"),
        ]
    ),
    (
        "In public policy, a measure that produces immediate benefits "
        "may also create costs that emerge much later. Evaluating a policy "
        "only by its short-term outcomes can therefore produce an "
        "incomplete assessment. Decision-makers need to consider delayed "
        "effects, distribution of benefits, and the possibility that "
        "different groups experience the same policy differently.",
        [
            ("What limitation of policy evaluation is highlighted?", "Focusing only on short-term outcomes", "Considering long-term consequences", "Examining different affected groups", "Assessing the distribution of benefits"),
            ("What may immediate benefits conceal?", "Costs that emerge later", "The complete absence of consequences", "Guaranteed equal outcomes", "A lack of public interest"),
            ("What does 'incomplete assessment' mean?", "An evaluation that leaves out important considerations", "A perfectly balanced judgement", "A final decision supported by all evidence", "A measurement with no limitations"),
            ("Why should policymakers consider different groups?", "The same policy may affect groups differently", "Every group always receives identical benefits", "Policies never influence communities", "Group differences are irrelevant"),
            ("Which conclusion best follows from the passage?", "Sound policy evaluation requires a broad and long-term perspective", "Immediate success is sufficient to judge every policy", "Delayed effects should be ignored", "All policies affect people equally"),
        ]
    ),
]


# --------------------------------------------------
# BUILD BANK
# --------------------------------------------------

BANK = {
    "Easy": make_questions(EASY_PASSAGES),
    "Medium": make_questions(MEDIUM_PASSAGES),
    "Hard": make_questions(HARD_PASSAGES),
}


# --------------------------------------------------
# VALIDATION
# --------------------------------------------------

def validate_bank():
    for difficulty in DIFFICULTIES:
        questions = BANK[difficulty]

        if len(questions) != 30:
            raise ValueError(
                f"{difficulty} contains {len(questions)} questions, not 30."
            )

        for index, item in enumerate(questions, start=1):
            if len(item) != 5:
                raise ValueError(
                    f"{difficulty} question {index} does not contain 5 values."
                )

            question, correct, wrong1, wrong2, wrong3 = item

            options = [correct, wrong1, wrong2, wrong3]

            if any(not isinstance(value, str) or not value.strip()
                   for value in [question] + options):
                raise ValueError(
                    f"{difficulty} question {index} contains an empty value."
                )

            if len(set(options)) != 4:
                raise ValueError(
                    f"{difficulty} question {index} has duplicate options."
                )

    print("VALIDATION PASSED")

    for difficulty in DIFFICULTIES:
        print(f"{difficulty}: {len(BANK[difficulty])}/30")


# --------------------------------------------------
# DATABASE INSERTION
# --------------------------------------------------

def main():
    validate_bank()

    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT id FROM lessons WHERE id = ? AND topic = ?",
            (LESSON_ID, TOPIC)
        )

        lesson = cursor.fetchone()

        if not lesson:
            raise ValueError(
                f"Lesson ID {LESSON_ID} with topic '{TOPIC}' was not found."
            )

        print(f"\nFound lesson ID: {LESSON_ID}")

        for difficulty in DIFFICULTIES:

            cursor.execute(
                """
                SELECT id FROM quizzes
                WHERE lesson_id = ? AND difficulty = ?
                """,
                (LESSON_ID, difficulty)
            )

            quiz_rows = cursor.fetchall()

            if len(quiz_rows) > 1:
                raise ValueError(
                    f"Multiple {difficulty} quizzes found for lesson "
                    f"{LESSON_ID}. Please resolve duplicates first."
                )

            if quiz_rows:
                quiz_id = quiz_rows[0][0]
            else:
                cursor.execute(
                    """
                    INSERT INTO quizzes (lesson_id, title, difficulty)
                    VALUES (?, ?, ?)
                    """,
                    (
                        LESSON_ID,
                        f"Unseen Passages - {difficulty}",
                        difficulty
                    )
                )
                quiz_id = cursor.lastrowid

            cursor.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                (quiz_id,)
            )

            existing_count = cursor.fetchone()[0]

            if existing_count > 30:
                raise ValueError(
                    f"{difficulty} already has {existing_count} questions. "
                    "Expected exactly 30."
                )

            questions_to_add = BANK[difficulty][existing_count:]

            for item in questions_to_add:
                question, correct, wrong1, wrong2, wrong3 = item

                options = [correct, wrong1, wrong2, wrong3]
                random.shuffle(options)

                correct_letter = "ABCD"[options.index(correct)]

                cursor.execute(
                    """
                    INSERT INTO questions (
                        quiz_id,
                        question,
                        option_a,
                        option_b,
                        option_c,
                        option_d,
                        correct_answer
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        quiz_id,
                        question,
                        options[0],
                        options[1],
                        options[2],
                        options[3],
                        correct_letter
                    )
                )

            cursor.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                (quiz_id,)
            )

            final_count = cursor.fetchone()[0]

            if final_count != 30:
                raise ValueError(
                    f"{difficulty} has {final_count} questions after insertion."
                )

            print(
                f"{difficulty}: {final_count}/30 questions SUCCESS"
            )

        connection.commit()

        print("\n===================================")
        print("UNSEEN PASSAGES INSERTION COMPLETE")
        print("Easy:   30 questions")
        print("Medium: 30 questions")
        print("Hard:   30 questions")
        print("TOTAL:  90 QUESTIONS")
        print("===================================")

    except Exception as error:
        connection.rollback()
        print("\nERROR:", error)
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
