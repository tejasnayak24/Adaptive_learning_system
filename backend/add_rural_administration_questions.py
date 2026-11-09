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


QUESTION_BANK = {
    "Easy": [
        ("Who maintains land records in a village?", "Patwari", "Doctor", "Teacher", "Pilot", "A"),
        ("Who is responsible for collecting land revenue in a village?", "Patwari", "Postman", "Nurse", "Shopkeeper", "A"),
        ("What is the main work of a Patwari?", "Maintaining land records", "Teaching students", "Treating patients", "Building roads", "A"),
        ("Who supervises the work of Patwaris?", "Revenue officer", "School principal", "Bus driver", "Librarian", "A"),
        ("What does a land record show?", "Details of land ownership", "School attendance", "Weather forecast", "Bus timings", "A"),
        ("Who may help resolve a village land dispute?", "Revenue officials", "Cricket coach", "Shop assistant", "Tour guide", "A"),
        ("What is a tehsil?", "An administrative area", "A type of crop", "A river", "A festival", "A"),
        ("Who heads the district administration?", "District Collector", "Patwari", "Village shopkeeper", "School student", "A"),
        ("Which department handles land records?", "Revenue department", "Railway department", "Tourism department", "Sports department", "A"),
        ("Why are land records important?", "They help establish land ownership", "They record exam marks", "They predict rainfall", "They issue train tickets", "A"),
        ("Who is commonly called the village accountant in many regions?", "Patwari", "Judge", "Doctor", "Engineer", "A"),
        ("What is a land survey used for?", "Measuring land", "Measuring exam scores", "Counting books", "Testing drinking water only", "A"),
        ("What can a farmer use to show ownership of land?", "Land records", "Bus pass", "Library card", "Sports certificate", "A"),
        ("Who records changes in land ownership?", "Revenue officials", "Cricket players", "Shopkeepers", "Tourists", "A"),
        ("What is a boundary of a field?", "The edge separating it from another area", "A crop seed", "A water pump", "A type of tax", "A"),
        ("Which official may inspect village land records?", "Revenue officer", "Music teacher", "Postman", "Chef", "A"),
        ("What is a village in rural administration?", "A settlement in the countryside", "A national ministry", "A seaport", "An airport", "A"),
        ("Why might land be measured?", "To identify its area and boundaries", "To determine school grades", "To count vehicles", "To measure wind speed", "A"),
        ("Which of these is related to rural land administration?", "Land ownership records", "Airline reservations", "Cinema tickets", "Online games", "A"),
        ("What may happen when land records are incorrect?", "Ownership disputes may arise", "The seasons stop changing", "Rivers disappear immediately", "Schools close permanently", "A"),
        ("What is a landowner?", "A person who owns land", "A person who pilots aircraft", "A person who treats animals only", "A person who sells train tickets", "A"),
        ("Who may update records after a land sale?", "Revenue officials", "Sports referees", "School monitors", "Bus conductors", "A"),
        ("What is rural administration concerned with?", "Managing administrative matters in rural areas", "Managing only airports", "Running international airlines", "Organising only films", "A"),
        ("Which document can contain information about a field?", "Land record", "Cinema ticket", "Restaurant menu", "Bus timetable", "A"),
        ("What is a land dispute?", "A disagreement about land", "A school competition", "A rainfall measurement", "A road race", "A"),
        ("Why are field boundaries recorded?", "To identify the limits of land", "To record a person's age", "To track school buses", "To calculate exam grades", "A"),
        ("Which area is generally associated with farming?", "Rural area", "Airport terminal", "Shopping mall", "Seaport only", "A"),
        ("What does the revenue department help administer?", "Land and revenue matters", "School sports only", "Movie production", "Air traffic only", "A"),
        ("Who can approach revenue officials about a land-record error?", "A concerned landholder", "Only a tourist", "Only a bus driver", "Only a sports player", "A"),
        ("What is one purpose of maintaining land records?", "Keeping official information about land", "Recording television programmes", "Listing film songs", "Tracking cricket scores", "A"),
    ],

    "Medium": [
        ("Why does a Patwari maintain records of cultivated land?", "To document land use and related details", "To issue school certificates", "To manage railway schedules", "To supervise hospitals", "A"),
        ("What is mutation of land records?", "Recording a change in ownership or rights", "Planting a new crop", "Measuring rainfall", "Building a school", "A"),
        ("Why may officials conduct a land survey?", "To establish measurements and boundaries", "To decide school holidays", "To count village festivals", "To inspect television signals", "A"),
        ("What is the purpose of a village map?", "To show plots and their locations", "To list all exam results", "To record bus fares", "To display national sports rankings", "A"),
        ("How can updated land records help farmers?", "They can help clarify ownership and land details", "They guarantee high crop prices", "They eliminate every drought", "They guarantee free machinery", "A"),
        ("What should a person do if a land record contains an error?", "Apply to the appropriate revenue authority for correction", "Destroy the record", "Change the official register secretly", "Ignore every future notice", "A"),
        ("Why are written land records useful in disputes?", "They provide official information for examination", "They automatically settle every dispute", "They replace all courts", "They guarantee ownership without verification", "A"),
        ("What is one role of a Tehsildar?", "Supervising revenue administration in a tehsil", "Managing an international airport", "Running a private cinema", "Teaching every village class", "A"),
        ("Why might a District Collector review revenue matters?", "To oversee district-level administration", "To select a national cricket team", "To operate every village shop", "To manage film studios", "A"),
        ("How can land surveys reduce disagreements?", "By clarifying measurements and boundaries", "By increasing land prices automatically", "By preventing all natural disasters", "By removing the need for records", "A"),
        ("Why might land ownership change after inheritance?", "Property rights may pass to legal heirs", "All village boundaries disappear", "The land becomes a public road automatically", "Agriculture becomes illegal", "A"),
        ("What does a revenue official do when recording a land transfer?", "Updates records according to applicable procedures", "Changes school examination papers", "Issues driving licences", "Determines monsoon dates", "A"),
        ("Why is transparency important in land administration?", "It helps people check decisions and records", "It makes all disputes impossible", "It removes every administrative rule", "It prevents all crop diseases", "A"),
        ("What may be needed to correct a disputed boundary?", "Relevant records and an appropriate survey", "A cinema ticket", "A sports medal", "A train reservation", "A"),
        ("How does land administration support rural governance?", "By maintaining records and handling revenue matters", "By controlling every private business", "By replacing all elected bodies", "By managing international trade alone", "A"),
        ("Why should land records be updated after a valid sale?", "To reflect the recorded change in rights", "To change the village climate", "To alter school timetables", "To create a new district automatically", "A"),
        ("Which information can be relevant to a land-record entry?", "Plot details and recorded ownership", "A student's favourite subject", "A shop's music playlist", "A team's match score", "A"),
        ("Why should officials follow established procedures in land cases?", "To support consistent and lawful decisions", "To avoid keeping any records", "To guarantee one side always wins", "To eliminate the need for evidence", "A"),
        ("What is a possible consequence of unclear land boundaries?", "Disagreements between neighbouring landholders", "An automatic increase in rainfall", "A change in the national flag", "The closure of all schools", "A"),
        ("Why might a farmer request a copy of a land record?", "To check or establish recorded land details", "To obtain a passport automatically", "To register a vehicle automatically", "To receive a school degree", "A"),
        ("What is the relationship between a Patwari and land records?", "The Patwari maintains specified village land records", "The Patwari decides every criminal case", "The Patwari manages all national banks", "The Patwari commands the army", "A"),
        ("Why is accurate measurement important during a survey?", "It helps determine the correct area and boundaries", "It determines a person's literacy", "It fixes the price of every crop", "It predicts election results", "A"),
        ("What can happen if an inheritance-related change is not recorded?", "Official records may not reflect the current rights", "The land vanishes", "The village becomes a city automatically", "All taxes are cancelled permanently", "A"),
        ("Why might two people consult revenue records during a dispute?", "To examine recorded information about the land", "To determine their exam ranks", "To compare their driving skills", "To choose a festival date", "A"),
        ("Which level of administration generally oversees a district?", "District administration", "A single household", "A school classroom", "A private shop", "A"),
        ("How can digitised land records be useful?", "They can make records easier to access and manage", "They guarantee that every entry is correct", "They eliminate all legal disputes", "They remove the need for verification", "A"),
        ("Why is a land map used with land records?", "It helps connect recorded plots with their locations", "It records only rainfall", "It replaces every ownership document", "It lists school attendance", "A"),
        ("What should officials consider before changing a land entry?", "Supporting documents and applicable procedures", "A person's favourite colour", "A random guess", "A sports team's ranking", "A"),
        ("How does an official record differ from a verbal claim?", "It is maintained as a formal administrative record", "It is always correct without review", "It makes evidence unnecessary", "It cannot ever be challenged", "A"),
        ("Why is coordination between revenue officials useful?", "It supports consistent handling of land matters", "It removes all administrative responsibilities", "It prevents every natural hazard", "It guarantees every farmer's profit", "A"),
    ],

    "Hard": [
        ("A land sale is completed, but the official record remains unchanged. What is the main concern?", "The record may not reflect the updated ownership information", "The village climate will change", "The plot will automatically become a road", "All revenue offices will close", "A"),
        ("Two neighbouring farmers disagree about a field boundary. What is a suitable administrative step?", "Examine relevant records and arrange an appropriate survey", "Choose a boundary without evidence", "Delete both land records", "Transfer the land to a random person", "A"),
        ("Why should mutation entries be supported by appropriate documentation?", "To maintain a reliable record of changes in rights", "To guarantee that land prices always rise", "To avoid identifying the parties", "To remove all legal procedures", "A"),
        ("A digital record contains a different area from an older verified document. What should officials do?", "Investigate the discrepancy using relevant evidence and procedures", "Accept the digital entry without checking", "Delete every historical record", "Ask an unrelated shopkeeper to decide", "A"),
        ("Why is maintaining a history of land-record changes valuable?", "It helps trace recorded changes over time", "It prevents every possible dispute", "It makes land surveys unnecessary", "It guarantees future inheritance outcomes", "A"),
        ("A farmer believes a boundary was wrongly marked. Which evidence is most relevant?", "Survey details, maps and applicable land records", "A television advertisement", "A school timetable", "A sports certificate", "A"),
        ("What is a risk of making a land-record change without verification?", "Incorrect ownership information may be recorded", "All crop production will stop immediately", "Every village road will disappear", "Rainfall will become predictable", "A"),
        ("How can clear administrative procedures improve public trust?", "They make record changes more transparent and accountable", "They ensure that no one can question a decision", "They remove the need for documents", "They guarantee that every claim is accepted", "A"),
        ("An inherited property has several legal heirs. What should record updates generally depend on?", "Relevant inheritance documents and applicable procedures", "A random selection of one heir", "The nearest shopkeeper's opinion", "The age of the village", "A"),
        ("Why should a land dispute be distinguished from a simple record correction?", "A dispute may require further examination of competing claims", "Every dispute can be resolved by deleting a record", "A correction always requires a criminal trial", "The two situations never involve records", "A"),
        ("A map identifies a plot, but its ownership entry is disputed. What is the best conclusion?", "The map alone may not resolve the ownership dispute", "The map automatically proves every ownership claim", "The map replaces all supporting documents", "The map makes the dispute invalid", "A"),
        ("Why is it important to identify the exact plot in a land dispute?", "It ensures the evidence relates to the land in question", "It establishes the weather for the year", "It determines the parties' education levels", "It automatically settles inheritance", "A"),
        ("A person requests correction of an official land entry. What should the authority prioritise?", "Checking the request and supporting evidence under applicable rules", "Changing the entry without review", "Rejecting every request automatically", "Removing the entire village register", "A"),
        ("How can inconsistent records across offices affect administration?", "They can create confusion and complicate verification", "They automatically improve accuracy", "They eliminate all ownership questions", "They make surveys legally impossible", "A"),
        ("Why should an official distinguish physical possession from recorded ownership?", "They are related but may require separate verification", "They are always identical in every case", "Physical possession makes every record unnecessary", "Recorded ownership can never be questioned", "A"),
        ("A land transfer is challenged by another claimant. What should happen before a disputed entry is treated as final?", "The claim should be examined through the appropriate process", "The first person to complain must automatically win", "All records should be destroyed", "The land should be assigned randomly", "A"),
        ("What is a key advantage of linking maps with verified land records?", "It can help relate plot locations to recorded information", "It eliminates every need for field inspection", "It guarantees that no map can contain errors", "It makes ownership laws unnecessary", "A"),
        ("Why should historical records be preserved when updating land details?", "They may help explain previous entries and changes", "They prevent any new information from being recorded", "They automatically determine every future sale", "They replace current verification", "A"),
        ("A survey reveals that a recorded boundary may be inaccurate. What should follow?", "The findings should be reviewed under the relevant procedures", "The nearest farmer should decide immediately", "All neighbouring plots should be cancelled", "The old record should be hidden", "A"),
        ("How does accountability help prevent errors in land administration?", "It makes officials' actions and record changes reviewable", "It prevents citizens from requesting corrections", "It removes the need to keep records", "It ensures every claim is accepted", "A"),
        ("Why might land records be relevant when obtaining a loan secured by property?", "They may help verify recorded property details", "They guarantee loan approval", "They determine the borrower's exam score", "They replace all lending requirements", "A"),
        ("An official receives two conflicting documents about a plot. What is the most responsible response?", "Verify their validity and follow the appropriate procedure", "Select one randomly", "Destroy both documents", "Change the entry to avoid investigation", "A"),
        ("What is a limitation of digitising inaccurate land records?", "Digitisation alone does not correct incorrect underlying information", "Digitisation always deletes ownership details", "Digital records cannot be updated", "Digitisation automatically settles every dispute", "A"),
        ("Why should land administration be accessible to rural residents?", "Residents need practical access to records and administrative services", "Only urban residents have land rights", "Accessibility removes the need for rules", "It guarantees that every application succeeds", "A"),
        ("A record correction affects several related plots. What should officials take care to do?", "Check the effect on related records before making changes", "Change every plot in the village identically", "Ignore the neighbouring entries", "Remove all maps from the register", "A"),
        ("Why is impartiality important when resolving land-record complaints?", "It supports fair consideration of evidence from the parties", "It requires officials to favour the first applicant", "It removes the need to hear both sides", "It guarantees that no disagreement exists", "A"),
        ("How can a clear chain of recorded ownership support administration?", "It helps track documented transfers and inheritance changes", "It guarantees every transfer is valid regardless of law", "It replaces all identity verification", "It prevents all future transfers", "A"),
        ("A landholder finds an error after a record has been digitised. What is the appropriate approach?", "Request review and correction through the authorised process", "Edit the official database without permission", "Ignore the error permanently", "Create an unrelated duplicate ownership claim", "A"),
        ("Why might a revenue authority need both documents and a field survey?", "Documents and physical measurements can provide complementary evidence", "A survey always makes documents irrelevant", "Documents always make physical boundaries irrelevant", "Neither can help clarify land details", "A"),
        ("What is the strongest general principle for reliable rural land administration?", "Accurate records, verification and fair procedures", "Unverified changes and informal guesses", "Keeping records secret from every authorised reviewer", "Resolving all claims without evidence", "A"),
    ],
}


def main():
    db = SessionLocal()

    try:
        lesson = (
            db.query(Lesson)
            .filter(
                Lesson.title == "Rural Administration",
                Lesson.topic == "Social Science",
            )
            .first()
        )

        if not lesson:
            print("ERROR: Rural Administration lesson was not found.")
            print("Check the lesson title and topic before proceeding.")
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
                    title=f"Rural Administration - {difficulty}",
                    difficulty=difficulty,
                )
                db.add(quiz)
                db.flush()
                print(f"Created {difficulty} quiz.")

            existing = (
                db.query(Question)
                .filter(Question.quiz_id == quiz.id)
                .all()
            )

            existing_text = {
                q.question.strip().lower()
                for q in existing
            }

            if len(existing) >= 30:
                print(
                    f"{difficulty}: already has {len(existing)} "
                    "questions; skipped."
                )
                continue

            added = 0

            for item in QUESTION_BANK[difficulty]:
                if len(existing) + added >= 30:
                    break

                question, a, b, c, d, correct_letter = item
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

                shuffled = [option_text for _, option_text in options]
                new_correct_letter = "ABCD"[
                    shuffled.index(correct_text)
                ]

                db.add(
                    Question(
                        quiz_id=quiz.id,
                        question=question,
                        option_a=shuffled[0],
                        option_b=shuffled[1],
                        option_c=shuffled[2],
                        option_d=shuffled[3],
                        correct_answer=new_correct_letter,
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