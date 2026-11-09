import logging
import os
from pathlib import Path

logging.disable(logging.CRITICAL)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "adaptive_learning.db"
os.environ["DATABASE_URL"] = f"sqlite:///{DATABASE_PATH.as_posix()}"

from app.database.connection import SessionLocal
from app.models.student import Student
from app.models.lesson import Lesson
from app.models.quiz import Quiz
from app.models.question import Question
from app.models.progress import Progress
from app.models.session import LearningSession
from app.models.reward import RewardHistory


QUESTION_BANK = {
    "Easy": [
        ("What is the main role of a government?", "To make decisions and provide public services", "To manage every family", "To prevent all public discussion", "To serve only wealthy people", "A"),
        ("Which is an example of a public service?", "Providing public healthcare", "Selling a personal bicycle", "Buying private clothes", "Choosing a personal hobby", "A"),
        ("Who makes laws for the whole of India at the Union level?", "Parliament", "A village school", "A private company", "A neighbourhood shop", "A"),
        ("Which body generally looks after local civic services in a city?", "Municipal corporation", "Supreme Court only", "Election candidate only", "Private sports club", "A"),
        ("Why do people pay taxes?", "To help fund public services and government activities", "To fund only private hobbies", "To avoid all laws", "To replace elections", "A"),
        ("Which branch of government interprets laws and settles legal disputes?", "Judiciary", "Legislature", "Political party", "Private business", "A"),
        ("Which branch is primarily responsible for making laws?", "Legislature", "Judiciary", "Police station", "Public library", "A"),
        ("What is a democracy?", "A system in which people have a role in choosing their government", "A system without public participation", "A private business arrangement", "A system ruled only by one family", "A"),
        ("Which service helps maintain public order?", "Police", "Cinema hall", "Clothing shop", "Restaurant", "A"),
        ("What is the purpose of elections?", "To allow voters to choose their representatives", "To appoint every citizen as a judge", "To stop public participation", "To remove all laws", "A"),
        ("Which level of government deals with the whole country?", "Union government", "A single village committee only", "A school council only", "A neighbourhood association", "A"),
        ("Which level of government serves a state?", "State government", "A private club", "A single household", "A shopkeepers' association", "A"),
        ("What is a constitution?", "A document establishing fundamental rules and principles of government", "A list of shop prices", "A personal diary", "A sports timetable", "A"),
        ("Which service helps children receive formal education?", "Schools", "Shopping malls", "Private cinemas", "Tourist hotels", "A"),
        ("What is the role of public hospitals?", "To provide healthcare services", "To conduct elections", "To write every law", "To settle all land borders", "A"),
        ("What does the judiciary help protect?", "Rights and the rule of law", "Only private profits", "Only sports results", "Only market prices", "A"),
        ("Who can vote in an Indian election if they meet the legal requirements?", "Eligible Indian citizens", "Every foreign visitor automatically", "Only government employees", "Only business owners", "A"),
        ("What is administration?", "Organising and carrying out public decisions and services", "Avoiding all public responsibilities", "Conducting only private sales", "Cancelling every public service", "A"),
        ("Why does a government maintain roads?", "To support transportation and public access", "To prevent people from travelling", "To replace all schools", "To conduct private family events", "A"),
        ("What is a government budget?", "A plan for public income and expenditure", "A personal shopping list", "A sports scorecard", "A map of rivers", "A"),
        ("Which institution can decide whether a law has been violated in a case?", "A court", "A private restaurant", "A sports shop", "A travel agency", "A"),
        ("What does public welfare mean?", "Promoting people's well-being", "Serving only a small private group", "Preventing access to healthcare", "Avoiding public needs", "A"),
        ("What is the purpose of public transport services?", "To help people travel", "To decide court cases", "To write textbooks only", "To conduct private weddings", "A"),
        ("Which activity is a government responsibility?", "Disaster response and public safety", "Choosing everyone's personal friends", "Controlling every private conversation", "Selecting every person's hobby", "A"),
        ("What is a representative?", "A person chosen to speak or act for others", "A person who owns every public service", "A person exempt from all laws", "A person who replaces every court", "A"),
        ("Why are rules and laws needed in society?", "They help establish standards of conduct and resolve disputes", "They make cooperation impossible", "They remove every right", "They eliminate public services", "A"),
        ("Which is an example of local government?", "A gram panchayat", "The United Nations", "A private bank", "A national sports club", "A"),
        ("What is accountability in government?", "Being answerable for decisions and actions", "Keeping every decision beyond scrutiny", "Avoiding all public questions", "Giving public money no oversight", "A"),
        ("What is the purpose of a public water supply?", "To provide water for community needs", "To conduct court hearings", "To register election candidates only", "To manufacture private vehicles", "A"),
        ("Why should governments listen to citizens?", "To understand public needs and concerns", "To remove public participation", "To avoid every complaint", "To prevent community discussion", "A"),
    ],

    "Medium": [
        ("Why are government responsibilities divided among different branches?", "To distribute powers and provide checks on authority", "To make all power unlimited", "To eliminate the need for laws", "To prevent courts from functioning", "A"),
        ("Which is an example of the legislature's work?", "Debating and passing laws", "Interpreting a court judgment", "Treating a patient", "Repairing a private phone", "A"),
        ("What is the judiciary's role when a dispute concerns the meaning of a law?", "Interpret the law and decide the case", "Collect every household's taxes directly", "Conduct all political campaigns", "Manage every school classroom", "A"),
        ("Why are local governments important?", "They can address community-level needs and services", "They replace the Union government entirely", "They make national courts unnecessary", "They control every private choice", "A"),
        ("How can taxes support public welfare?", "They help finance services such as roads, schools, and healthcare", "They are used only for private purchases", "They eliminate the need for budgets", "They automatically end inequality", "A"),
        ("What is one purpose of a government budget?", "To plan spending and estimate income", "To replace the constitution", "To select private hobbies", "To decide the result of every court case", "A"),
        ("Why should government actions follow the constitution?", "The constitution establishes governing principles and limits", "Government actions must never be reviewed", "The constitution applies only to private clubs", "It removes the need for accountability", "A"),
        ("What is a public policy?", "A course of action adopted to address a public issue", "A personal diary entry", "A private shopping receipt", "A sports competition rule only", "A"),
        ("Why are elections important in a democracy?", "They allow eligible voters to select representatives", "They eliminate every public debate", "They remove all legal protections", "They make citizens unnecessary", "A"),
        ("What is the purpose of government welfare programmes?", "To address public needs and support eligible people", "To prevent people from accessing services", "To replace all courts", "To cancel every public budget", "A"),
        ("How can citizens hold elected representatives accountable?", "By asking questions, participating in public processes, and voting", "By permanently giving up their rights", "By avoiding all public information", "By preventing every election", "A"),
        ("Why does a country need an independent judiciary?", "To decide cases impartially and review legal questions", "To make every decision for political parties", "To remove the rule of law", "To guarantee that no dispute occurs", "A"),
        ("Which example best illustrates a state government's responsibilities?", "Managing state-level services and implementing state policies", "Conducting only a private family's activities", "Replacing all local civic bodies", "Running every foreign government", "A"),
        ("Why might a municipality collect local taxes or fees?", "To help fund civic services and infrastructure", "To replace all national laws", "To eliminate public roads", "To select judges for every court", "A"),
        ("What is the role of civil servants in administration?", "Implementing policies and delivering public services", "Making every citizen a member of parliament", "Replacing the constitution", "Running only private businesses", "A"),
        ("Why is transparency important in government?", "It allows people to understand and scrutinise public decisions", "It prevents citizens from accessing information", "It removes the need for records", "It makes accountability impossible", "A"),
        ("What does separation of powers seek to achieve?", "Prevent excessive concentration of governmental authority", "Give one branch unlimited power", "Remove all judicial review", "Prevent legislatures from existing", "A"),
        ("How does a grievance-redressal system help citizens?", "It provides a channel for raising complaints and seeking remedies", "It prevents all complaints from being recorded", "It replaces every election", "It removes every public service", "A"),
        ("Why must government expenditure be monitored?", "To support accountability and responsible use of public funds", "To ensure public money is never examined", "To avoid all financial records", "To remove every public service", "A"),
        ("What can happen when a public service is poorly delivered?", "People may face delays or difficulty accessing essential support", "Every public need is automatically met", "Accountability becomes unnecessary", "All public problems disappear", "A"),
        ("What is the purpose of a legislative debate?", "To examine proposals and different viewpoints before decisions", "To prevent representatives from discussing laws", "To replace every court judgment", "To cancel all public participation", "A"),
        ("How does the rule of law apply to government?", "Public authorities must act within the law", "Officials are automatically above the law", "Laws apply only to ordinary citizens", "Government decisions never require legal authority", "A"),
        ("Why do governments collect reliable population data?", "To help plan services and allocate resources", "To prevent all planning", "To replace every public budget", "To eliminate the need for schools", "A"),
        ("What is a coalition government?", "A government formed by two or more political parties working together", "A government formed by a single family automatically", "A court formed to hear one case", "A local business association", "A"),
        ("Why can public consultation improve a policy?", "It can reveal community needs and possible unintended effects", "It guarantees every person agrees", "It makes evidence unnecessary", "It removes all implementation challenges", "A"),
        ("What is one responsibility of government during a natural disaster?", "Coordinate rescue, relief, and essential services", "Stop all emergency communication", "Prevent access to medical care", "Ignore affected communities", "A"),
        ("How can an audit help public administration?", "It examines records and the use of public funds", "It prevents financial oversight", "It replaces all elections", "It makes budgets unnecessary", "A"),
        ("Why are government departments assigned different responsibilities?", "Specialisation can help organise services and administration", "It removes all coordination needs", "It makes laws unnecessary", "It guarantees every service works perfectly", "A"),
        ("What does decentralisation mean in government?", "Distributing some authority to lower levels or local bodies", "Concentrating every decision in one office", "Removing all local participation", "Ending public administration", "A"),
        ("Why should a public scheme be evaluated after implementation?", "To assess whether it meets its objectives and identify improvements", "To ensure results are never examined", "To prevent feedback", "To avoid checking public expenditure", "A"),
    ],

    "Hard": [
        ("A public programme spends its budget but fails to reach its intended beneficiaries. What should an evaluation examine?", "Implementation, access barriers, outcomes, and resource use", "Only whether the budget was spent", "Only the programme's name", "Whether evaluation can be avoided", "A"),
        ("Why is the separation of powers important in a constitutional democracy?", "It helps limit concentrated authority through institutional checks", "It gives every branch unlimited power", "It removes the need for courts", "It makes constitutions irrelevant", "A"),
        ("A government department refuses to explain a major public expenditure. Which principle is most directly at issue?", "Transparency and accountability", "Cultural diversity", "Private recreation", "Personal preference", "A"),
        ("A law appears to conflict with a constitutional right. Which institution can adjudicate the legal dispute?", "The judiciary", "A private retailer", "A sports association", "A neighbourhood shop", "A"),
        ("Why should public policies be assessed for unintended consequences?", "A policy may create effects beyond its original objectives", "Policies can never have side effects", "Only announced objectives matter", "Evaluation prevents all public participation", "A"),
        ("What is a key difference between policy formulation and implementation?", "Formulation designs the approach; implementation puts it into practice", "They are always unrelated to government", "Implementation always happens before any plan", "Formulation means auditing private purchases", "A"),
        ("A city improves roads but ignores drainage in flood-prone areas. What does this illustrate?", "Infrastructure planning should consider connected local needs", "Road construction automatically solves every problem", "Public services never interact", "Local conditions are irrelevant", "A"),
        ("Why is coordination between Union, state, and local governments often necessary?", "Many public issues cross administrative responsibilities and boundaries", "Each level works on entirely unrelated matters", "Coordination removes every legal responsibility", "Local services never affect national goals", "A"),
        ("What is the value of independent audits of public spending?", "They can identify irregularities and strengthen financial accountability", "They guarantee no irregularity can occur", "They eliminate the need for records", "They prevent scrutiny of public funds", "A"),
        ("A policy is adopted without consulting affected communities. What is a possible risk?", "Important local needs and implementation barriers may be overlooked", "The policy must automatically succeed", "Consultation can never add useful information", "Every affected person will necessarily agree later", "A"),
        ("Why is access to public information important for democracy?", "It helps citizens scrutinise decisions and participate meaningfully", "It prevents public oversight", "It removes the need for elections", "It makes accountability impossible", "A"),
        ("What is a constitutional limitation on government power intended to do?", "Prevent authorities from exercising power without legal constraints", "Make government power unlimited", "Remove citizens' rights", "Prevent courts from applying law", "A"),
        ("Why should public services use clear eligibility criteria?", "Clear criteria can support consistent and reviewable decisions", "Hidden criteria always improve fairness", "Criteria should change arbitrarily for each person", "Eligibility should never be explained", "A"),
        ("A government scheme reaches many people but costs far more than planned. What should be reviewed?", "Costs, delivery efficiency, outcomes, and the reasons for overruns", "Only the scheme's logo", "Whether spending records should be destroyed", "Whether all evaluation should stop", "A"),
        ("How can legislative scrutiny improve government administration?", "Representatives can question decisions and examine proposed expenditure", "It prevents any questions about government", "It replaces every public service", "It guarantees that errors never happen", "A"),
        ("Why is an independent election process important?", "It supports credible competition and voters' ability to choose representatives", "It guarantees that every candidate wins", "It removes the need for eligible voters", "It prevents public participation", "A"),
        ("A local body identifies unsafe drinking water. Which response best reflects public responsibility?", "Investigate the problem, communicate risks, and arrange safe water measures", "Ignore the issue until the next election", "Prevent residents from reporting illness", "Remove all water-quality checks", "A"),
        ("Why should government decisions be based on reliable evidence?", "Evidence helps identify needs and assess likely policy effects", "Evidence guarantees every decision is perfect", "Evidence prevents all public debate", "Assumptions are always more accurate", "A"),
        ("What is the purpose of a grievance mechanism with an appeal option?", "It allows complaints to be reviewed when an initial decision is disputed", "It prevents decisions from ever being questioned", "It eliminates the need for records", "It makes every complaint automatically successful", "A"),
        ("Why might a policy require different implementation methods in different regions?", "Local conditions and needs can differ across regions", "Every region has identical circumstances", "Local information never matters", "Variation always violates fairness", "A"),
        ("How does legislative oversight differ from judicial review?", "Legislative oversight examines government activity; judicial review examines legal validity", "They are always the same process", "Judicial review is conducted by private businesses", "Legislative oversight replaces all courts", "A"),
        ("Why should the outcomes of a welfare programme be measured rather than only its activities?", "Activities alone do not establish whether people's needs were met", "Activity counts always prove success", "Outcomes are never relevant", "Budgets cannot be evaluated", "A"),
        ("A public authority makes a decision without following required legal procedure. What concern arises?", "Legality and procedural fairness", "Cultural celebration", "Private entertainment", "Personal taste", "A"),
        ("What is a possible benefit of decentralising some decisions?", "Local bodies may respond more directly to local needs", "Every local decision becomes automatically correct", "Coordination is never needed", "National responsibilities disappear", "A"),
        ("Why is public participation valuable in disaster planning?", "Local knowledge can help identify risks and suitable responses", "Residents can never contribute useful knowledge", "It removes the need for emergency services", "It guarantees that disasters cannot occur", "A"),
        ("A public service is available only through an inaccessible online portal. What should administrators examine?", "Whether alternative access methods are needed", "Whether some residents should lose their rights", "Whether all accessibility checks should end", "Whether the portal should remain unexplained", "A"),
        ("Why should an administrator document important decisions?", "Records support review, continuity, and accountability", "Records always prevent public service delivery", "Documentation removes legal obligations", "Decisions should never be reviewed", "A"),
        ("A public authority uses funds for a purpose not authorised by the budget. What issue may arise?", "Improper use of public funds and accountability concerns", "Automatic improvement in transparency", "Guaranteed compliance with the budget", "Removal of the need for auditing", "A"),
        ("How can performance indicators help assess a government programme?", "They provide measures for tracking progress toward defined objectives", "They guarantee the programme has no weaknesses", "They make public feedback unnecessary", "They replace every legal requirement", "A"),
        ("Why should governments review a policy when evidence shows it is ineffective?", "Revision can improve outcomes and use public resources more responsibly", "A policy must never change", "Evidence of failure should be ignored", "Public needs cannot change", "A"),
    ],
}


def main():
    db = SessionLocal()

    try:
        lesson = (
            db.query(Lesson)
            .filter(
                Lesson.title == "Government and Its Functions",
                Lesson.topic == "Social Science",
            )
            .first()
        )

        if lesson is None:
            print("Lesson not found. Run the Social Science seed script first.")
            return

        total_added = 0

        for difficulty, questions in QUESTION_BANK.items():
            quiz_title = f"Government and Its Functions - {difficulty}"

            quiz = (
                db.query(Quiz)
                .filter(
                    Quiz.lesson_id == lesson.id,
                    Quiz.title == quiz_title,
                )
                .first()
            )

            if quiz is None:
                quiz = Quiz(
                    lesson_id=lesson.id,
                    title=quiz_title,
                    difficulty=difficulty,
                )
                db.add(quiz)
                db.flush()

            existing = (
                db.query(Question)
                .filter(Question.quiz_id == quiz.id)
                .count()
            )

            if existing >= 30:
                print(f"{difficulty}: already has {existing} questions; skipped.")
                continue

            added = 0

            for item in questions:
                if existing + added >= 30:
                    break

                question_text, a, b, c, d, answer = item

                duplicate = (
                    db.query(Question)
                    .filter(
                        Question.quiz_id == quiz.id,
                        Question.question == question_text,
                    )
                    .first()
                )

                if duplicate:
                    continue

                db.add(
                    Question(
                        quiz_id=quiz.id,
                        question=question_text,
                        option_a=a,
                        option_b=b,
                        option_c=c,
                        option_d=d,
                        correct_answer=answer,
                    )
                )
                added += 1

            db.commit()

            final_count = (
                db.query(Question)
                .filter(Question.quiz_id == quiz.id)
                .count()
            )

            total_added += added
            print(f"{difficulty}: added {added}; final count {final_count}/30")

        print(f"\nTotal questions added: {total_added}")

    except Exception as error:
        db.rollback()
        print(f"Error: {error}")

    finally:
        db.close()


if __name__ == "__main__":
    main()