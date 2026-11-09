import os
import logging
import random
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
        ("Who is responsible for managing a city's municipal services?", "Municipal corporation", "Railway station", "Village school", "Airport authority", "A"),
        ("Who is the elected head of a municipal corporation in many Indian cities?", "Mayor", "Patwari", "Governor", "District judge", "A"),
        ("Which body generally manages services in a large city?", "Municipal corporation", "Gram Sabha", "Village council only", "Forest department", "A"),
        ("Which service is commonly provided by urban local bodies?", "Garbage collection", "National defence", "Currency printing", "International diplomacy", "A"),
        ("Who collects property tax for a municipality?", "Municipal authorities", "School students", "Railway passengers", "Tour guides", "A"),
        ("What is a ward in a city?", "An administrative area for local representation", "A type of vehicle", "A farming tool", "A mountain range", "A"),
        ("Who represents residents in a municipal ward?", "Ward councillor", "Patwari", "Army officer", "Postman", "A"),
        ("Which service helps keep city streets clean?", "Municipal sanitation service", "Air traffic control", "Passport printing", "National elections only", "A"),
        ("What is a municipality?", "An urban local government body", "A private shopping mall", "A national court", "A village crop", "A"),
        ("Which authority may maintain public parks in a city?", "Urban local body", "International airport", "Private household only", "National army unit", "A"),
        ("Why do cities need drainage systems?", "To carry away wastewater and rainwater", "To store school books", "To manage train tickets", "To produce electricity only", "A"),
        ("Which service provides drinking water to urban residents?", "Urban water supply system", "Cinema hall", "Sports club", "Post office only", "A"),
        ("What is one purpose of street lighting?", "To improve visibility and safety at night", "To measure rainfall", "To grow crops indoors", "To issue land titles", "A"),
        ("What do municipal workers often collect from households?", "Solid waste", "Exam papers", "Passports", "Railway signals", "A"),
        ("Why are public roads maintained?", "To support safe movement and transport", "To record school attendance", "To regulate national borders", "To issue birth certificates only", "A"),
        ("Which body can help address a local garbage problem?", "Municipal authority", "International court", "Airline company", "Foreign embassy", "A"),
        ("What is property tax generally associated with?", "Property within the relevant local jurisdiction", "School examination marks", "Train arrival times", "Weather forecasts", "A"),
        ("Who can raise a complaint about a broken streetlight?", "A city resident", "Only a foreign visitor", "Only a district judge", "Only a railway driver", "A"),
        ("What does urban administration deal with?", "Managing services and local matters in towns and cities", "Running every national ministry", "Managing only farms", "Conducting international wars", "A"),
        ("Why are public toilets important in cities?", "They support sanitation and public health", "They issue driving licences", "They determine land ownership", "They control traffic signals only", "A"),
        ("Which local service helps remove blocked drains?", "Municipal maintenance service", "Library membership desk", "Railway booking office", "School examination board", "A"),
        ("What is a municipal budget used for?", "Planning income and expenditure", "Recording sports scores", "Predicting earthquakes exactly", "Selecting national holidays only", "A"),
        ("Why are urban local elections held?", "To elect local representatives", "To appoint every national minister directly", "To choose school textbooks only", "To determine monsoon dates", "A"),
        ("What is one responsibility of a ward councillor?", "Representing residents' local concerns", "Commanding the national army", "Issuing international visas", "Managing every state court", "A"),
        ("What is sewage?", "Wastewater carried through sewer systems", "Freshly harvested grain", "A type of road sign", "A public election", "A"),
        ("Which facility helps reduce litter in public spaces?", "Waste bins and collection services", "Unmarked private vehicles", "Closed water pipes", "Unused railway tracks", "A"),
        ("Why do urban areas need traffic management?", "To improve the movement and safety of road users", "To increase household waste", "To record land inheritance", "To organise farm irrigation only", "A"),
        ("Which is an example of a public urban facility?", "Public park", "Private bedroom", "Personal laptop", "Household cupboard", "A"),
        ("What may a municipal office issue or register under applicable rules?", "Certain local certificates and records", "International passports in every case", "University degrees for all students", "Military commands", "A"),
        ("Who should residents contact about a municipal service problem?", "The relevant local authority", "A random tourist", "A distant airline", "A sports commentator", "A"),
    ],
    "Medium": [
        ("Why do municipal bodies collect property tax?", "To help finance local public services", "To pay for every private purchase", "To replace all national taxes", "To set school examination marks", "A"),
        ("How can ward councillors help improve urban services?", "By representing local concerns to the urban body", "By replacing all courts", "By commanding national defence", "By managing foreign trade", "A"),
        ("Why is waste segregation useful?", "It can improve recycling and waste processing", "It makes all waste disappear immediately", "It removes the need for collection", "It guarantees that no landfill is ever needed", "A"),
        ("What may happen when city drainage is poorly maintained?", "Waterlogging and local flooding may increase", "All roads become railways", "Drinking water becomes unlimited", "Property tax disappears", "A"),
        ("Why should municipal budgets be planned carefully?", "Resources must be allocated among competing local needs", "Every project has unlimited funding", "Budgets remove the need for services", "Local authorities never receive revenue", "A"),
        ("How can residents participate in urban administration?", "By reporting issues and engaging with local representatives", "By secretly changing municipal records", "By avoiding every public meeting", "By replacing elected bodies individually", "A"),
        ("Why is regular water-quality monitoring important?", "It helps identify possible risks to public health", "It guarantees unlimited water supply", "It replaces drainage maintenance", "It determines road tax rates", "A"),
        ("What is a major challenge for growing cities?", "Providing adequate infrastructure as population increases", "Maintaining village crop records only", "Managing ocean tides directly", "Eliminating all forms of transport", "A"),
        ("How can timely garbage collection benefit residents?", "It can reduce waste accumulation and related health risks", "It prevents every communicable disease", "It removes all household expenses", "It guarantees zero pollution", "A"),
        ("Why do municipalities maintain public parks?", "To provide shared recreational and green spaces", "To replace all residential housing", "To store every city's waste", "To operate national courts", "A"),
        ("What is the purpose of a municipal ward?", "To organise local representation and administration", "To divide the country into nations", "To identify international borders", "To replace the state legislature", "A"),
        ("How can citizen complaints improve local services?", "They can alert authorities to problems needing attention", "They automatically guarantee immediate solutions", "They eliminate the need for inspection", "They replace every municipal budget", "A"),
        ("Why should public infrastructure be maintained regularly?", "To preserve safety, reliability and service quality", "To guarantee that repairs are never needed", "To stop all urban development", "To eliminate the need for workers", "A"),
        ("Which approach can help reduce traffic congestion?", "Better transport planning and traffic management", "Blocking every public road", "Removing all traffic signs", "Closing all pedestrian crossings", "A"),
        ("Why is coordination between city departments important?", "Many services depend on one another", "Every department performs exactly the same task", "Coordination makes budgets unnecessary", "It eliminates the need for planning", "A"),
        ("What can transparent municipal spending help promote?", "Public accountability", "Secret decision-making", "Automatic tax exemption for everyone", "The elimination of public services", "A"),
        ("Why may urban local bodies need building regulations?", "To guide safer and planned development", "To prevent every building from being repaired", "To determine school grades", "To manage national defence", "A"),
        ("What is a likely benefit of public transport planning?", "Improved access and movement around the city", "Guaranteed elimination of every traffic accident", "The end of all walking", "Automatic reduction of every household bill", "A"),
        ("How can uncollected waste affect urban residents?", "It can attract pests and create sanitation problems", "It always improves drinking-water quality", "It guarantees better air quality", "It eliminates drainage blockages", "A"),
        ("Why might a municipality prioritise repairing a dangerous road?", "To reduce risks to road users", "To increase the road's potholes", "To avoid public safety responsibilities", "To replace the city council", "A"),
        ("What is an advantage of maintaining accurate municipal records?", "They support informed administration and service planning", "They guarantee every decision is correct automatically", "They remove the need for staff", "They prevent residents from asking questions", "A"),
        ("Why is equitable service delivery important?", "Different neighbourhoods should receive fair consideration", "Only wealthy neighbourhoods need services", "It removes all local revenue needs", "It guarantees identical costs for every project", "A"),
        ("How can urban trees contribute to a city?", "They can provide shade and support urban environments", "They replace all water-supply systems", "They remove every source of pollution", "They eliminate the need for public parks", "A"),
        ("Why should municipalities plan for heavy rainfall?", "To prepare drainage and reduce flood-related disruption", "To prevent rain from occurring", "To remove all water bodies", "To stop all public transport permanently", "A"),
        ("What can a municipal audit help examine?", "Financial records and the use of public funds", "Only residents' hobbies", "Only school sports scores", "The timing of every monsoon", "A"),
        ("Why should streetlights be repaired promptly?", "Poor lighting can affect visibility and public safety", "Streetlights control property ownership", "Repairs determine school admissions", "Lighting replaces road maintenance", "A"),
        ("What is a key purpose of sanitation services?", "Maintaining cleaner surroundings and protecting public health", "Issuing international passports", "Determining crop prices", "Running national elections", "A"),
        ("How can urban planning support future growth?", "By anticipating infrastructure and service requirements", "By ignoring population changes", "By preventing all housing construction", "By eliminating local government", "A"),
        ("Why should residents know which authority manages a service?", "It helps direct complaints and requests appropriately", "It guarantees every complaint is accepted", "It removes the need for evidence", "It replaces all elected representatives", "A"),
        ("What is one way municipalities can improve accountability?", "Publishing understandable information about decisions and spending", "Hiding every public record", "Avoiding all public feedback", "Removing all financial checks", "A"),
    ],
    "Hard": [
        ("A neighbourhood repeatedly floods after heavy rain. What is the most suitable first administrative response?", "Inspect drainage, identify causes and plan appropriate corrective action", "Blame residents without inspection", "Close every road permanently", "Stop recording rainfall", "A"),
        ("A city has limited funds and several urgent service needs. What should its administration do?", "Assess urgency, public impact and available resources before prioritising", "Spend the entire budget on one minor project", "Ignore all safety-related repairs", "Allocate money randomly", "A"),
        ("Why should a municipal authority publish clear expenditure information?", "It enables residents to scrutinise the use of public funds", "It guarantees that no mistakes can occur", "It removes all auditing requirements", "It prevents residents from making complaints", "A"),
        ("A waste contractor misses collections in several wards. What is a sound administrative response?", "Check service records, investigate failures and enforce applicable contract terms", "Pay every invoice without review", "Stop all waste collection citywide indefinitely", "Delete residents' complaints", "A"),
        ("How can rapid urbanisation strain local government?", "Demand for housing, water, sanitation and transport may outpace capacity", "It automatically increases all infrastructure capacity", "It eliminates the need for budgets", "It guarantees that every resident has equal access", "A"),
        ("Two neighbourhoods report unequal access to water. What should officials examine?", "Supply data, infrastructure conditions and distribution arrangements", "Only the number of nearby shops", "The residents' favourite sports", "The colour of the water tanks", "A"),
        ("Why is a life-cycle approach useful for urban infrastructure planning?", "It considers construction, operation, maintenance and eventual renewal", "It considers construction costs alone", "It assumes infrastructure never deteriorates", "It removes the need for future budgeting", "A"),
        ("A proposed road project may affect homes and pedestrian safety. What should planning consider?", "Relevant legal requirements, impacts, alternatives and safety measures", "Only the project's opening ceremony", "Only the colour of road markings", "Avoiding every form of assessment", "A"),
        ("What is a risk of relying only on complaint counts to allocate services?", "Areas with less access to reporting may have unmet needs", "Every complaint always represents the same cost", "Complaint counts reveal every hidden problem", "It guarantees equal service delivery", "A"),
        ("Why should municipalities coordinate drainage work with road construction?", "Coordination can prevent duplicated work and infrastructure conflicts", "It makes engineering checks unnecessary", "It guarantees that rain will stop", "It removes the need for contractors", "A"),
        ("A municipal project is delayed and costs exceed estimates. What should administrators do?", "Review progress, costs, causes and corrective options", "Hide the revised costs permanently", "Stop maintaining all other services", "Approve every extra expense without review", "A"),
        ("How can public consultation improve a local development project?", "It can reveal residents' needs and potential local impacts", "It guarantees that every resident agrees", "It replaces technical and legal assessment", "It removes the need for budgets", "A"),
        ("A city digitises property records but does not validate existing entries. What is the key risk?", "Errors may persist in the digital records", "Every ownership dispute will end automatically", "Digital records cannot be searched", "All property taxes will become zero", "A"),
        ("Why should municipal service performance be measured using clear indicators?", "Indicators help compare results against service objectives", "Indicators guarantee success without action", "They replace all public services", "They make budgets unnecessary", "A"),
        ("A road repair repeatedly fails after rainfall. What should be investigated?", "Drainage, materials, design and quality of previous repairs", "Only the road's name", "The residents' school grades", "The number of city parks", "A"),
        ("How can transparent procurement help a municipality?", "It supports scrutiny and fair competition in public purchasing", "It guarantees that every supplier is perfect", "It removes the need to check quality", "It prevents all project delays", "A"),
        ("A low-income settlement has poor sanitation but few formal complaints. What is the best approach?", "Assess conditions proactively and consult affected residents", "Assume that no service is needed", "Allocate all funds to already well-served areas", "Wait until every resident files a complaint", "A"),
        ("Why should emergency plans identify responsibilities across city departments?", "Clear roles can improve coordination during a crisis", "They guarantee emergencies never occur", "They eliminate the need for training", "They replace all response resources", "A"),
        ("What is a limitation of judging a municipal department only by how much it spends?", "Spending alone does not show service quality or outcomes", "Higher spending always means better results", "Lower spending always means better service", "Financial information is never useful", "A"),
        ("How can accessible complaint channels support inclusive urban governance?", "They allow more residents to report service problems", "They guarantee every issue is resolved instantly", "They eliminate the need for staff", "They replace elected local bodies", "A"),
        ("A public park is built but remains inaccessible to many residents. What should be reviewed?", "Access routes, design, safety and the needs of different users", "Only the park's opening date", "The number of private shops elsewhere", "The city's school examination results", "A"),
        ("Why should municipal maintenance plans use asset-condition information?", "It helps prioritise repairs based on need and risk", "It guarantees that no asset will fail", "It eliminates all operating costs", "It makes inspections unnecessary", "A"),
        ("A city wants to reduce landfill use. Which strategy is most comprehensive?", "Reduce waste, segregate it, support reuse and recycling, and manage residual waste", "Mix all waste together and increase dumping", "Stop collecting household waste", "Send every recyclable item to landfill", "A"),
        ("Why can urban development worsen flooding when planning ignores natural drainage?", "Construction can obstruct or reduce areas that absorb or carry water", "Buildings always increase natural water absorption", "Roads eliminate all rainfall", "Drainage systems never affect flooding", "A"),
        ("A municipal authority receives conflicting reports about a water outage. What should it do?", "Verify the affected areas and coordinate a response using reliable information", "Publish an unverified cause immediately", "Ignore all reports", "Close the entire water network permanently", "A"),
        ("How does clear division of responsibilities improve municipal work?", "It reduces confusion and helps establish accountability", "It makes communication unnecessary", "It guarantees no employee makes mistakes", "It removes all service standards", "A"),
        ("Why should urban infrastructure planning consider accessibility for people with disabilities?", "Public services should be usable by people with different needs", "Accessibility is relevant only to private homes", "It removes the need for maintenance", "It guarantees identical travel times for everyone", "A"),
        ("A contractor claims a project is complete, but residents report defects. What is appropriate?", "Inspect the work against specifications before accepting it", "Accept it without inspection", "Delete the residents' reports", "Pay the full amount solely on the contractor's claim", "A"),
        ("Why should municipal authorities evaluate a project after implementation?", "To assess outcomes and identify lessons for future projects", "To avoid measuring service results", "To guarantee every project was perfect", "To stop all future planning", "A"),
        ("What principle best supports effective urban administration?", "Accountable, evidence-based and equitable management of local services", "Unverified decisions without public oversight", "Spending without planning or review", "Ignoring residents and service outcomes", "A"),
    ],
}


def main():
    db = SessionLocal()

    try:
        lesson = (
            db.query(Lesson)
            .filter(
                Lesson.title == "Urban Administration",
                Lesson.topic == "Social Science",
            )
            .first()
        )

        if not lesson:
            print("ERROR: Urban Administration lesson was not found.")
            print("Check the lesson title and topic.")
            return

        print(f"Lesson found: {lesson.title} (ID: {lesson.id})")
        total_added = 0

        for difficulty in ["Easy", "Medium", "Hard"]:
            quiz = (
                db.query(Quiz)
                .filter(
                    Quiz.lesson_id == lesson.id,
                    Quiz.difficulty == difficulty,
                )
                .first()
            )

            if not quiz:
                quiz = Quiz(
                    lesson_id=lesson.id,
                    title=f"Urban Administration - {difficulty}",
                    difficulty=difficulty,
                )
                db.add(quiz)
                db.flush()

            existing = (
                db.query(Question)
                .filter(Question.quiz_id == quiz.id)
                .all()
            )

            existing_text = {
                q.question.strip().lower() for q in existing
            }

            if len(existing) >= 30:
                print(
                    f"{difficulty}: already has {len(existing)} "
                    "questions; skipped."
                )
                continue

            added = 0

            for question, a, b, c, d, correct_letter in QUESTION_BANK[difficulty]:
                if len(existing) + added >= 30:
                    break

                if question.strip().lower() in existing_text:
                    continue

                options = [
                    ("A", a),
                    ("B", b),
                    ("C", c),
                    ("D", d),
                ]
                correct_text = dict(options)[correct_letter]
                random.shuffle(options)
                shuffled = [value for _, value in options]
                new_correct = "ABCD"[shuffled.index(correct_text)]

                db.add(
                    Question(
                        quiz_id=quiz.id,
                        question=question,
                        option_a=shuffled[0],
                        option_b=shuffled[1],
                        option_c=shuffled[2],
                        option_d=shuffled[3],
                        correct_answer=new_correct,
                    )
                )

                existing_text.add(question.strip().lower())
                added += 1

            db.flush()
            total_added += added
            print(
                f"{difficulty}: added {added} questions "
                f"({len(existing) + added}/30 total)."
            )

        db.commit()

        print("\nFINAL VERIFICATION")
        grand_total = 0

        for difficulty in ["Easy", "Medium", "Hard"]:
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
                if quiz else 0
            )

            grand_total += count
            print(f"{difficulty}: {count}/30")

        print(f"Total: {grand_total}/90")
        print(f"New questions added: {total_added}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()