import os
import logging
import random
from pathlib import Path

logging.disable(logging.CRITICAL)

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


# Each question: question, option A, option B, option C,
# option D, correct answer letter.

EASY = [
    ("What is local government?", "Government at the village or town level", "Government of another country", "A private company", "An international court", "A"),
    ("Which body governs a village in India?", "Gram Panchayat", "Lok Sabha", "Supreme Court", "Rajya Sabha", "A"),
    ("Who is generally elected to lead a Gram Panchayat?", "Sarpanch", "President of India", "Governor", "Chief Justice", "A"),
    ("Which body governs a large city?", "Municipal Corporation", "Gram Sabha only", "Parliament only", "Election Commission", "A"),
    ("Who elects representatives to local bodies?", "Eligible voters", "Only judges", "Only police officers", "Foreign citizens", "A"),
    ("Which is a function of local government?", "Maintaining local roads", "Declaring war on another country", "Printing all currency", "Appointing the President", "A"),
    ("What is a Gram Sabha?", "Assembly of registered voters in a village area", "A national court", "A state police unit", "A city business group", "A"),
    ("Which service is commonly managed by a municipality?", "Garbage collection", "National defence", "Foreign relations", "Space exploration", "A"),
    ("Which level of government is closest to residents?", "Local government", "International government", "Foreign government", "United Nations", "A"),
    ("What is one source of local-government income?", "Local taxes and fees", "Only foreign aid", "Only private gifts", "Money printed by households", "A"),
    ("What does sanitation help maintain?", "Clean and healthy surroundings", "Military strength", "International trade agreements", "Space stations", "A"),
    ("Which body may manage village drinking-water facilities?", "Gram Panchayat", "Supreme Court", "Rajya Sabha", "Foreign ministry", "A"),
    ("What is a ward in a city?", "A local electoral area", "A country", "A mountain range", "A national ministry", "A"),
    ("Why are local representatives elected?", "To represent local residents", "To replace every court", "To control other countries", "To cancel all elections", "A"),
    ("Which is an urban local body?", "Municipality", "Gram Sabha", "Village-only assembly", "Forest animal group", "A"),
    ("What should residents do to report a broken streetlight?", "Contact the relevant local body", "Contact a foreign embassy", "Ask the Supreme Court to repair it directly", "Contact an international sports body", "A"),
    ("Which place is usually served by a Gram Panchayat?", "A village", "An entire continent", "A foreign capital", "An ocean", "A"),
    ("What is a public park?", "A shared community space", "A private bedroom", "A court judgment", "A national border", "A"),
    ("Which activity helps keep a neighbourhood clean?", "Proper waste disposal", "Dumping rubbish in drains", "Blocking sewers", "Wasting drinking water", "A"),
    ("What does a local budget describe?", "Expected income and spending", "Only the weather forecast", "A list of foreign armies", "The history of the Moon", "A"),
    ("What is a municipality mainly responsible for?", "Civic services in a town", "National defence", "International treaties", "Printing passports for the world", "A"),
    ("Which is an example of public property?", "A public road", "A personal notebook", "A private toothbrush", "A family photograph", "A"),
    ("Why are drains maintained?", "To carry wastewater and reduce waterlogging", "To store election ballots permanently", "To increase littering", "To block rainwater flow", "A"),
    ("What is a civic problem?", "A broken public water pipe", "A private favourite colour", "A personal hobby", "A fictional planet", "A"),
    ("What is a local election?", "An election for a local governing body", "An election in another country only", "A school sports match", "A court examination", "A"),
    ("Which group can raise a local issue with elected representatives?", "Community residents", "Only foreign ambassadors", "Only international athletes", "Only film actors", "A"),
    ("What does street cleaning improve?", "Public hygiene", "Ocean depth", "National borders", "Planetary rotation", "A"),
    ("Which service can a town local body help provide?", "Street lighting", "Command of the armed forces", "Control of all national courts", "Foreign policy for India", "A"),
    ("Why should local taxes be paid when legally due?", "They help fund public services", "They automatically end all elections", "They replace the Constitution", "They remove every public responsibility", "A"),
    ("What is a common goal of local government?", "Improving residents' daily lives", "Governing the entire world", "Replacing all state governments", "Managing other countries' elections", "A"),
]

MEDIUM = [
    ("Why is local government important in a democracy?", "It allows people to participate in nearby public decisions", "It removes the need for elections", "It replaces the national government", "It gives every decision to courts", "A"),
    ("What is a key role of a Gram Panchayat?", "Managing village civic needs and development", "Conducting foreign affairs", "Commanding the national army", "Making international treaties", "A"),
    ("Who can generally participate in a Gram Sabha meeting?", "Registered voters of the Gram Sabha area", "Only the village head's family", "Only national ministers", "Only government contractors", "A"),
    ("Why are municipal services important?", "They support public health and orderly urban life", "They decide international borders", "They appoint all Members of Parliament", "They control other nations", "A"),
    ("What is decentralisation?", "Distributing powers to lower levels of government", "Concentrating every decision in one office", "Ending local elections", "Removing public services", "A"),
    ("Why should local budgets be transparent?", "Residents can examine how public money is used", "Budgets should never be discussed", "It prevents residents from asking questions", "It makes spending unlimited", "A"),
    ("Which is a suitable example of citizen participation?", "Attending a Gram Sabha meeting", "Ignoring every community problem", "Damaging public property", "Preventing others from voting", "A"),
    ("What can happen when drains are not maintained?", "Waterlogging and sanitation problems may increase", "Roads become immune to rain", "Waste disappears automatically", "Drinking water becomes unlimited", "A"),
    ("What is the main purpose of property tax collected by urban local bodies?", "Helping fund civic services", "Funding only foreign embassies", "Replacing the national Constitution", "Paying private household bills", "A"),
    ("Why do towns need waste-management systems?", "To collect and dispose of waste safely", "To move all waste into drinking-water sources", "To eliminate the need for sanitation", "To prevent all recycling", "A"),
    ("What is one benefit of elected local representatives?", "They can raise residents' concerns in local decisions", "They have unlimited national powers", "They can ignore all laws", "They replace the judiciary", "A"),
    ("Which issue is most directly suited to a municipal body?", "A damaged city drainage line", "A national defence treaty", "A Supreme Court constitutional appeal", "An international currency agreement", "A"),
    ("Why might rural and urban local bodies differ?", "Their areas and service needs differ", "Villages and cities have identical populations", "Urban areas never need water", "Rural areas never need roads", "A"),
    ("What is the purpose of local development planning?", "To identify and address community needs", "To prevent public facilities from improving", "To cancel local budgets", "To transfer all local decisions abroad", "A"),
    ("Why should local representatives consult residents?", "Residents can explain local needs and priorities", "Consultation makes public needs irrelevant", "Residents must never discuss services", "Consultation automatically ends elections", "A"),
    ("What is an important feature of a Gram Sabha?", "It provides a forum for village voters to discuss matters", "It is India's highest court", "It is the national legislature's upper house", "It is a private company board", "A"),
    ("Which action supports accountability in local government?", "Checking spending records and asking questions", "Hiding every public account", "Refusing to explain decisions", "Preventing all public meetings", "A"),
    ("Why are streetlights maintained?", "To improve visibility and public safety", "To increase waste in drains", "To replace public transport", "To control rainfall", "A"),
    ("Which example shows a local body responding to residents?", "Repairing a reported damaged public road", "Changing another country's laws", "Commanding the armed forces", "Deciding a foreign court case", "A"),
    ("What can local governments do to improve public health?", "Support sanitation and waste collection", "Encourage sewage to enter drinking-water supplies", "Block every public drain", "Stop all clean-water maintenance", "A"),
    ("Why do local bodies collect information about community needs?", "To help prioritise services and development projects", "To prevent all planning", "To remove all public facilities", "To cancel every meeting", "A"),
    ("Which statement best describes a municipal corporation?", "An urban local body generally serving a large city", "A village assembly of registered voters", "A national defence command", "An international court", "A"),
    ("Why is public participation valuable during budgeting?", "It helps identify important community priorities", "It guarantees that every request must be funded", "It removes the need for accounts", "It makes taxes unnecessary", "A"),
    ("What is one challenge local bodies may face?", "Limited funds and growing service demands", "Having no residents anywhere", "Never needing infrastructure", "Being responsible for every foreign government", "A"),
    ("Why must local bodies follow applicable laws?", "Their decisions and spending must be lawful", "Local decisions are exempt from every law", "They may cancel the Constitution", "They can ignore all financial rules", "A"),
    ("How can residents help a local waste-management programme?", "Segregating waste and using collection services", "Dumping rubbish into storm drains", "Burning every kind of waste anywhere", "Mixing all waste with drinking water", "A"),
    ("Why is a local grievance system useful?", "It gives residents a way to report service problems", "It prevents residents from reporting problems", "It replaces all elected bodies", "It removes public accountability", "A"),
    ("What is one purpose of local roads?", "Connecting homes with workplaces and public facilities", "Setting international boundaries", "Controlling the national currency", "Replacing all railway networks", "A"),
    ("Why should local projects be monitored?", "To check progress, quality and use of funds", "To ensure nobody checks spending", "To make delays impossible to report", "To remove every public record", "A"),
    ("What helps local government reflect democratic values?", "Elections, participation and accountability", "Secret spending without oversight", "Permanent exclusion of residents", "Unlimited power without legal limits", "A"),
]

HARD = [
    ("A village residents' meeting identifies unsafe drinking water. What is the most appropriate first local-government response?", "Assess the problem and coordinate a lawful repair or safe-water response", "Ignore the complaint until the next national election", "Close every village school permanently", "Transfer responsibility to a foreign government", "A"),
    ("A Gram Panchayat project has unexplained spending. Which action best supports accountability?", "Review expenditure records and seek an explanation through proper procedures", "Destroy the financial records", "Prevent residents from asking questions", "Approve all future spending without review", "A"),
    ("A city faces repeated flooding because drains are blocked. Which response addresses the underlying civic problem?", "Inspect, clear and maintain the drainage system", "Block more drains", "Stop collecting all waste", "Remove every streetlight", "A"),
    ("A local body has funds for only one of two urgent repairs. What should guide its decision?", "Public need, urgency, evidence and available resources", "The personal preference of one contractor alone", "Which project has the least public benefit", "A random choice without assessment", "A"),
    ("Residents complain that garbage collection is irregular. Which approach is most constructive?", "Record missed collections and raise the issue with the responsible local body", "Dump more rubbish into nearby drains", "Damage the collection vehicles", "Prevent neighbours from reporting problems", "A"),
    ("Why is decentralised decision-making useful for local services?", "Local representatives can respond to area-specific needs", "It removes every legal responsibility", "It guarantees unlimited money", "It makes citizen participation unnecessary", "A"),
    ("A local project is delayed repeatedly. What should residents reasonably request?", "An update on progress, reasons for delay and a plan for completion", "Destruction of all project records", "An end to all public meetings", "Transfer of the project to an unrelated foreign agency", "A"),
    ("A municipality plans a new public park. Which step can improve the plan?", "Assess residents' needs, accessibility, cost and maintenance", "Ignore every potential user", "Spend the entire budget without estimating costs", "Choose a site without checking its suitability", "A"),
    ("Which combination best supports responsible local governance?", "Public participation, transparent accounts and lawful decisions", "Secret accounts, exclusion and arbitrary spending", "No records and no public consultation", "Unlimited authority without oversight", "A"),
    ("A village has several competing requests for drinking water, roads and decoration. What is a sound planning method?", "Assess essential needs, urgency and available funds", "Fund decoration automatically before basic services", "Reject all requests without review", "Choose only the request of one influential person", "A"),
    ("Why should local-government responsibilities be clearly assigned?", "It helps residents know which body should address an issue", "It guarantees that no one is accountable", "It eliminates all need for coordination", "It prevents every public service from operating", "A"),
    ("A road was repaired poorly despite public spending. What should be examined?", "Work quality, contract terms and expenditure records", "Only the colour of the road signs", "The weather on another continent", "The personal hobbies of every resident", "A"),
    ("How can a Gram Sabha help scrutinise village development?", "By discussing plans, needs and relevant local decisions", "By replacing the Supreme Court", "By controlling foreign policy", "By printing national currency", "A"),
    ("Why should a local budget include maintenance costs for a new facility?", "The facility needs resources to remain usable after construction", "Maintenance is never needed for public facilities", "Construction automatically pays every future bill", "Maintenance prevents public use", "A"),
    ("A municipality wants to reduce waste sent to landfill. Which measure can help?", "Promote waste segregation, recycling and suitable processing", "Mix recyclable materials with all other waste permanently", "Dump rubbish into rivers", "Stop collecting household waste", "A"),
    ("Which is the clearest example of a local issue rather than a national-level issue?", "Repairing a neighbourhood footpath", "Negotiating a national defence agreement", "Managing India's foreign relations", "Passing a national law in Parliament", "A"),
    ("Residents disagree about the location of a community facility. What should local representatives do?", "Consider consultation, access, safety and relevant planning rules", "Hide the proposal from everyone", "Ignore all legal requirements", "Let one resident decide without any process", "A"),
    ("Why is publishing local project information beneficial?", "It enables residents to understand decisions and scrutinise spending", "It guarantees that projects need no monitoring", "It makes financial records unnecessary", "It removes the public's right to ask questions", "A"),
    ("A rural area has poor access to a public service. What should local planning examine?", "Population needs, distance, infrastructure and available resources", "Only the preferences of distant visitors", "Whether all residents can be excluded", "How to stop the service from being used", "A"),
    ("What is a responsible response if a local body lacks funds for every requested project?", "Explain constraints and prioritise needs within lawful procedures", "Promise every project regardless of resources", "Hide the budget from residents", "Spend without records or approval", "A"),
    ("How do local elections support democratic accountability?", "Voters can choose representatives and evaluate their performance", "They eliminate all laws", "They guarantee every policy succeeds", "They remove citizens' ability to raise issues", "A"),
    ("A local water source is polluted. Which response is most appropriate?", "Coordinate testing, public safety measures and corrective action", "Tell residents to ignore the pollution", "Add household waste to the source", "Stop all public communication", "A"),
    ("Which evidence is most useful for evaluating a local sanitation programme?", "Collection coverage, service records and cleanliness outcomes", "The number of unrelated advertisements", "The personal favourite songs of officials", "The shape of the national flag", "A"),
    ("A local representative receives a complaint outside their body's jurisdiction. What should they do?", "Explain the proper authority and help direct the complaint appropriately", "Claim that no authority can ever help", "Destroy the complaint", "Punish the resident for asking", "A"),
    ("Why should local infrastructure planning consider accessibility?", "Facilities should be usable by people with differing mobility needs", "Public facilities should exclude people with disabilities", "Accessibility has no relationship to public services", "Only private buildings require entrances", "A"),
    ("Which approach can reduce misuse of local public funds?", "Clear procurement procedures, records and oversight", "Unrecorded payments without checks", "Secret contracts with no documentation", "Approving spending without authority", "A"),
    ("A city expands rapidly and its water demand rises. What should local planners consider?", "Demand forecasts, supply capacity and sustainable management", "Assume water demand will always remain unchanged", "Stop monitoring water quality", "Build facilities without assessing needs", "A"),
    ("Why is coordination sometimes needed between local and state governments?", "Some services and funding responsibilities involve multiple levels", "Local bodies control every state function", "State governments have no legal role anywhere", "Coordination always removes local responsibility", "A"),
    ("A local project benefits one neighbourhood but leaves another without basic services. What should planners review?", "Whether resources and service access reflect assessed needs fairly", "How to prevent residents from reporting unequal access", "Whether to remove all services from both areas", "How to hide project details permanently", "A"),
    ("Which measure best indicates that local government is responsive?", "Residents' concerns are considered and services are followed up", "Complaints are deleted without review", "Public accounts are permanently hidden", "Meetings are cancelled to avoid discussion", "A"),
]


def get_or_create_quiz(db, lesson, difficulty):
    title = f"Local Government - {difficulty}"

    quiz = (
        db.query(Quiz)
        .filter(
            Quiz.lesson_id == lesson.id,
            Quiz.difficulty == difficulty
        )
        .first()
    )

    if quiz is None:
        quiz = Quiz(
            lesson_id=lesson.id,
            title=title,
            difficulty=difficulty
        )
        db.add(quiz)
        db.flush()
        print(f"Created quiz: {title}")

    return quiz


def add_questions(db, quiz, question_bank, difficulty):
    existing = (
        db.query(Question)
        .filter(Question.quiz_id == quiz.id)
        .count()
    )

    if existing >= 30:
        print(f"{difficulty}: already has {existing} questions; skipped.")
        return 0

    if existing > 0:
        print(
            f"{difficulty}: has {existing} questions; "
            "adding only enough to reach 30."
        )

    # Avoid inserting duplicate question text.
    existing_texts = {
        q.question.strip().casefold()
        for q in db.query(Question)
        .filter(Question.quiz_id == quiz.id)
        .all()
    }

    added = 0

    for item in question_bank:
        if existing + added >= 30:
            break

        question_text, a, b, c, d, correct = item

        if question_text.strip().casefold() in existing_texts:
            continue

        # Shuffle options so the correct answer is not always A.
        options = [a, b, c, d]
        correct_text = options[ord(correct.upper()) - ord("A")]
        random.shuffle(options)
        correct_letter = "ABCD"[options.index(correct_text)]

        db.add(
            Question(
                quiz_id=quiz.id,
                question=question_text,
                option_a=options[0],
                option_b=options[1],
                option_c=options[2],
                option_d=options[3],
                correct_answer=correct_letter
            )
        )

        existing_texts.add(question_text.strip().casefold())
        added += 1

    print(
        f"{difficulty}: added {added}; "
        f"expected final count {existing + added}/30"
    )

    return added


def main():
    db = SessionLocal()

    try:
        lesson = (
            db.query(Lesson)
            .filter(
                Lesson.title == "Local Government",
                Lesson.topic == "Social Science"
            )
            .first()
        )

        if lesson is None:
            print("ERROR: Local Government lesson not found.")
            print("No questions were inserted.")
            return

        print(f"Lesson found: {lesson.title} (ID {lesson.id})")

        total_added = 0

        for difficulty, bank in [
            ("Easy", EASY),
            ("Medium", MEDIUM),
            ("Hard", HARD),
        ]:
            quiz = get_or_create_quiz(db, lesson, difficulty)
            total_added += add_questions(
                db, quiz, bank, difficulty
            )

        db.commit()

        print(f"\nTotal questions added: {total_added}")

        print("\nFINAL VERIFICATION")
        total = 0

        for difficulty in ["Easy", "Medium", "Hard"]:
            quiz = (
                db.query(Quiz)
                .filter(
                    Quiz.lesson_id == lesson.id,
                    Quiz.difficulty == difficulty
                )
                .first()
            )

            count = (
                db.query(Question)
                .filter(Question.quiz_id == quiz.id)
                .count()
                if quiz else 0
            )

            total += count
            print(f"{difficulty}: {count}/30")

        print(f"Total: {total}/90")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()