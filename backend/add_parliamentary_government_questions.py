import os
import random
import logging
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
        ("What is a parliamentary form of government?", "A system in which the executive is responsible to the legislature", "A system without elections", "A system ruled only by judges", "A system without laws", "A"),
        ("Who is the head of the Union government in India?", "Prime Minister", "Chief Justice", "Governor", "Lok Sabha Speaker", "A"),
        ("Who is the constitutional head of the Indian Union?", "President", "Prime Minister", "Chief Minister", "District Collector", "A"),
        ("To which house is the Union Council of Ministers collectively responsible?", "Lok Sabha", "Rajya Sabha", "Supreme Court", "State Legislative Council", "A"),
        ("What are the two houses of the Indian Parliament?", "Lok Sabha and Rajya Sabha", "Supreme Court and High Court", "Gram Sabha and Gram Panchayat", "Cabinet and Secretariat", "A"),
        ("What is the Lok Sabha commonly called?", "House of the People", "Council of States", "House of Judges", "Council of Ministers", "A"),
        ("What is the Rajya Sabha commonly called?", "Council of States", "House of the People", "House of Governors", "National Court", "A"),
        ("How are Lok Sabha members generally chosen?", "By direct election by eligible voters", "By appointment by the Supreme Court", "By selection by school councils", "By appointment by private companies", "A"),
        ("Who appoints the Prime Minister of India?", "President of India", "Chief Justice of India", "Speaker of the Lok Sabha", "Election Commission", "A"),
        ("What is the main role of the Council of Ministers?", "To assist and advise the President and run the government", "To decide every court case", "To conduct all school examinations", "To replace Parliament permanently", "A"),
        ("What does the opposition do in Parliament?", "Questions and scrutinises the government", "Appoints every judge", "Conducts all elections", "Makes every decision without debate", "A"),
        ("What is a coalition government?", "A government formed by two or more political parties working together", "A government without any representatives", "A court-controlled government", "A government run by one judge", "A"),
        ("What is a minister?", "A member of the government responsible for assigned areas of work", "A member of the Supreme Court in every case", "An election machine operator", "A village school student", "A"),
        ("What is a parliamentary election?", "An election to choose representatives for a legislature", "A court hearing", "A school competition", "A government budget meeting", "A"),
        ("What is a constituency?", "An area represented by an elected representative", "A government department", "A court building", "A political speech", "A"),
        ("What is a vote of no confidence?", "A motion testing whether a government retains the confidence of the Lok Sabha", "A motion to appoint every judge", "A vote to cancel the Constitution", "A vote to select the President directly", "A"),
        ("What is the main function of the Speaker of the Lok Sabha?", "To preside over proceedings and maintain order", "To command every state police force", "To decide every judicial appeal", "To appoint the Prime Minister independently", "A"),
        ("What is the normal term of the Lok Sabha?", "Five years unless dissolved earlier", "Two years in every circumstance", "Six years without any possibility of dissolution", "Ten years without elections", "A"),
        ("What is a cabinet?", "A group of senior ministers responsible for major government decisions", "A court building", "A group of election voters", "A private company board in every case", "A"),
        ("Why are parliamentary debates held?", "To discuss issues and examine proposed laws and policies", "To prevent representatives from speaking", "To cancel every election", "To replace the judiciary", "A"),
        ("What is the main purpose of Question Hour?", "To allow members to ask ministers questions", "To conduct national examinations", "To elect judges", "To announce sports results", "A"),
        ("What is a bill?", "A proposal for a law", "A final court judgment", "An election constituency", "A government building", "A"),
        ("Who formally summons a session of the Indian Parliament?", "President of India", "Chief Minister", "Chief Justice", "Mayor", "A"),
        ("What does collective responsibility mean?", "The Council of Ministers is collectively responsible to the Lok Sabha", "Each minister is responsible only to private companies", "Ministers cannot be questioned", "The judiciary runs the cabinet", "A"),
        ("What is the purpose of parliamentary committees?", "To examine matters in greater detail", "To replace all elected representatives", "To conduct all court trials", "To abolish public debate", "A"),
        ("What is the main purpose of a government budget?", "To present estimated government receipts and expenditure", "To list election candidates only", "To appoint judges", "To announce school holidays", "A"),
        ("What does majority support mean in a parliamentary system?", "Having the support of more than half of the relevant voting members", "Having support from one voter only", "Having the support of every court", "Having no elected representatives", "A"),
        ("What is the role of political parties in parliamentary government?", "They contest elections, represent interests and help form governments", "They replace all courts", "They appoint every voter", "They prevent all political discussion", "A"),
        ("Why is accountability important in parliamentary government?", "It helps ensure the government answers for its actions", "It allows ministers to ignore the legislature", "It removes the need for elections", "It prevents citizens from asking questions", "A"),
        ("What happens when a government loses the confidence of the Lok Sabha?", "It is expected to resign or follow the applicable constitutional process", "It automatically becomes the Supreme Court", "The Rajya Sabha is permanently abolished", "The President's office ends immediately", "A"),
    ],

    "Medium": [
        ("Why is parliamentary government described as responsible government?", "The executive is accountable to the elected legislature", "The judiciary appoints every minister", "The executive never answers to Parliament", "Citizens cannot change their representatives", "A"),
        ("What is the difference between the nominal and real executive in India?", "The President is the constitutional head, while the Prime Minister and Council of Ministers exercise executive functions under the Constitution", "The Prime Minister is a judge and the President is a voter", "The Speaker is the real executive in all matters", "There is no constitutional distinction", "A"),
        ("Why is the Prime Minister central to parliamentary government?", "The Prime Minister leads the Council of Ministers and coordinates government policy", "The Prime Minister decides every court judgment", "The Prime Minister independently replaces Parliament", "The Prime Minister appoints all voters", "A"),
        ("What is the principle of collective responsibility?", "Ministers stand together as a government and are collectively accountable to the Lok Sabha", "Each minister can remain in office regardless of the government's confidence", "Only the President answers questions in Parliament", "Ministers are responsible only to political opponents", "A"),
        ("Why is the opposition essential to parliamentary democracy?", "It scrutinises policies, raises concerns and offers alternative approaches", "It has the sole power to pass all laws", "It removes the need for elections", "It replaces the judiciary", "A"),
        ("How does Question Hour strengthen accountability?", "It enables members to seek explanations and information from ministers", "It prevents ministers from explaining decisions", "It appoints the Speaker", "It dissolves Parliament automatically", "A"),
        ("What is the role of a no-confidence motion?", "To test whether the government still has the confidence of the Lok Sabha", "To appoint the Chief Justice", "To amend every constitutional provision", "To conduct a presidential election", "A"),
        ("How is a coalition government different from a single-party government?", "A coalition involves two or more parties cooperating to form or support a government", "A coalition has no political parties", "A single-party government cannot have ministers", "A coalition is always appointed by the judiciary", "A"),
        ("Why may coalition governments require negotiations among parties?", "Partners may have different policies and priorities that need coordination", "Coalition partners cannot discuss policy", "Negotiations automatically abolish Parliament", "All coalition partners must have identical manifestos", "A"),
        ("What is the role of the Council of Ministers under the Constitution?", "It aids and advises the President in exercising constitutional functions", "It replaces the Constitution", "It controls the judiciary in every case", "It conducts all state elections", "A"),
        ("What is the distinction between the Council of Ministers and the Cabinet?", "The Cabinet is the smaller, senior decision-making body within the larger Council of Ministers", "The Cabinet consists only of judges", "The Council of Ministers consists only of opposition MPs", "There is no distinction in any context", "A"),
        ("Why is a parliamentary majority important for government formation?", "It normally enables a government to secure confidence and pass legislation", "It gives a government unlimited power beyond the Constitution", "It prevents the legislature from meeting", "It removes all opposition rights", "A"),
        ("What does a hung Parliament mean?", "No party or pre-election alliance has an outright majority", "Every seat is vacant", "Parliament has been permanently abolished", "Every bill has automatically passed", "A"),
        ("What may happen after a hung Parliament election?", "Parties may negotiate support or a coalition, subject to constitutional processes", "The Constitution automatically ends", "The judiciary becomes the cabinet", "All elected representatives lose their seats automatically", "A"),
        ("Why are parliamentary committees useful?", "They can scrutinise legislation, expenditure and policy in detail", "They replace all public elections", "They make court judgments binding", "They prevent members from studying policy", "A"),
        ("What is the purpose of the Union Budget being presented to Parliament?", "To obtain legislative consideration and authorisation for public finances under constitutional procedures", "To cancel all taxes permanently", "To appoint state governors", "To select the Speaker directly", "A"),
        ("What is the significance of the Speaker's role in the Lok Sabha?", "The Speaker presides over proceedings and applies the House's rules", "The Speaker independently runs every ministry", "The Speaker decides all appeals in the Supreme Court", "The Speaker conducts all state elections", "A"),
        ("How does parliamentary government differ from presidential government in a key respect?", "In parliamentary government, the executive is generally drawn from and accountable to the legislature", "In presidential government, there is no executive", "Parliamentary government has no legislature", "Presidential government always has a hereditary ruler", "A"),
        ("Why is a question or debate in Parliament not the same as a law?", "Discussion examines an issue, while legislation must follow the required law-making process", "Every question automatically becomes law", "Debates are court judgments", "All bills become law without approval", "A"),
        ("What is a private member's bill?", "A bill introduced by a member who is not a minister", "A bill written by a private company and automatically enacted", "A court judgment", "A government budget", "A"),
        ("What is the purpose of an adjournment in a parliamentary sitting?", "To suspend the sitting until a later time", "To permanently dissolve every house", "To remove the Constitution", "To appoint every minister for life", "A"),
        ("How can Parliament hold the executive accountable beyond Question Hour?", "Through debates, committees, motions and scrutiny of public expenditure", "Only by conducting court trials", "By preventing ministers from attending", "By abolishing elections", "A"),
        ("Why is the President generally expected to act on ministerial advice under India's parliamentary system?", "The Constitution provides for the President to act on the aid and advice of the Council of Ministers, subject to its provisions", "The President personally makes every policy without constitutional limits", "The judiciary writes the budget", "The Speaker controls the President in all matters", "A"),
        ("What does ministerial responsibility mean?", "Ministers are answerable for their departments and the government is collectively accountable to the Lok Sabha", "Ministers have no obligation to explain decisions", "Only civil servants can be questioned", "The opposition runs every ministry", "A"),
        ("Why does a government need legislative approval for public expenditure?", "It supports democratic scrutiny and lawful control of public finances", "It allows spending without limits", "It removes the need for a budget", "It gives private companies control of the treasury", "A"),
        ("What is the significance of party discipline in parliamentary government?", "It helps parties coordinate legislative voting and maintain government support", "It makes every MP legally identical", "It eliminates all internal party debate", "It gives parties power to ignore the Constitution", "A"),
        ("What is a caretaker government generally expected to do during a transition?", "Handle necessary administration while respecting applicable conventions and legal limits", "Make unlimited irreversible decisions in every case", "Cancel the next election", "Abolish Parliament", "A"),
        ("Why can parliamentary debate improve legislation?", "It allows representatives to identify problems and consider alternatives", "It guarantees every proposal is perfect", "It prevents amendments", "It removes public accountability", "A"),
        ("What is the role of the ruling party or coalition in Parliament?", "To support the government and pursue its legislative programme while following parliamentary rules", "To replace all courts", "To cancel the Constitution", "To prevent every opposition member from speaking", "A"),
        ("Why is the confidence of the Lok Sabha important for the Union government?", "The Council of Ministers is collectively responsible to that House", "The government is responsible only to the Rajya Sabha", "The government never needs legislative support", "The judiciary elects the cabinet", "A"),
    ],

    "Hard": [
        ("Which article provides that the Council of Ministers is collectively responsible to the Lok Sabha?", "Article 75(3)", "Article 14", "Article 110", "Article 280", "A"),
        ("Which article provides for a Council of Ministers with the Prime Minister at its head to aid and advise the President?", "Article 74", "Article 32", "Article 123", "Article 226", "A"),
        ("Which article provides for the appointment of the Prime Minister and other ministers?", "Article 75", "Article 14", "Article 110", "Article 148", "A"),
        ("Which article deals with the President's power to summon and prorogue Parliament and dissolve the Lok Sabha?", "Article 85", "Article 21", "Article 32", "Article 280", "A"),
        ("What is the constitutional maximum interval between two sessions of Parliament?", "Six months", "Three months", "One year", "Two years", "A"),
        ("Which article provides for the Speaker and Deputy Speaker of the Lok Sabha?", "Article 93", "Article 74", "Article 110", "Article 123", "A"),
        ("Which article deals with the President's special address to Parliament?", "Article 87", "Article 14", "Article 32", "Article 280", "A"),
        ("Which article defines a Money Bill?", "Article 110", "Article 75", "Article 85", "Article 148", "A"),
        ("Which article provides for the annual financial statement, commonly called the Union Budget?", "Article 112", "Article 14", "Article 21", "Article 324", "A"),
        ("Which house has the exclusive power to vote on demands for grants?", "Lok Sabha", "Rajya Sabha", "Supreme Court", "State Legislative Council", "A"),
        ("How long may the Rajya Sabha retain a Money Bill before returning it with recommendations?", "Up to 14 days", "Up to six months", "Up to one year", "Indefinitely", "A"),
        ("Who certifies whether a bill is a Money Bill in the Lok Sabha?", "Speaker of the Lok Sabha", "President of India", "Prime Minister", "Chief Justice of India", "A"),
        ("What happens if the Lok Sabha passes a no-confidence motion against the Council of Ministers?", "The Council of Ministers must resign or follow the applicable constitutional process", "The Rajya Sabha is automatically dissolved", "The President's term immediately ends", "The Supreme Court is dissolved", "A"),
        ("What does the principle of collective responsibility require of ministers?", "The Council of Ministers remains collectively accountable to the Lok Sabha", "Every minister may disregard the confidence of the Lok Sabha", "Ministers are accountable only to the Rajya Sabha", "Ministers cannot be questioned by Parliament", "A"),
        ("What is the main constitutional difference between the President and the Prime Minister in India's parliamentary system?", "The President is the constitutional head; the Prime Minister leads the Council of Ministers", "The President is the head of the Supreme Court", "The Prime Minister is elected directly as President", "Both offices have identical constitutional functions", "A"),
        ("What is the significance of Article 78?", "It specifies duties of the Prime Minister concerning information and communication with the President", "It establishes the Supreme Court", "It defines a Money Bill", "It establishes the Election Commission", "A"),
        ("Which article provides that the President may address either House or both Houses of Parliament and send messages, subject to constitutional provisions?", "Article 86", "Article 14", "Article 21", "Article 280", "A"),
        ("What is the purpose of a motion of confidence?", "To demonstrate that the government commands the support of the Lok Sabha", "To appoint the Chief Justice", "To amend every fundamental right", "To dissolve the Supreme Court", "A"),
        ("What is the constitutional significance of Question Hour?", "It is a parliamentary procedure through which members can seek answers from ministers", "It is explicitly defined in a single constitutional article as the only way to scrutinise ministers", "It automatically removes a minister", "It replaces all legislative procedures", "A"),
        ("What is the main role of the Cabinet in the Union executive?", "It is the senior decision-making body within the Council of Ministers", "It is a branch of the Supreme Court", "It consists only of opposition members", "It conducts all state elections", "A"),
        ("What is the distinction between dissolution and prorogation?", "Dissolution ends the Lok Sabha, while prorogation ends a session of a House", "They always mean the same thing", "Prorogation permanently abolishes Parliament", "Dissolution only suspends a single sitting", "A"),
        ("Which statement about the Rajya Sabha is correct when the Lok Sabha is dissolved?", "The Rajya Sabha continues because it is a permanent House", "The Rajya Sabha is automatically dissolved with the Lok Sabha", "The Rajya Sabha becomes the Supreme Court", "All Rajya Sabha members immediately lose their seats", "A"),
        ("What is the purpose of parliamentary financial control?", "To ensure public funds are considered and authorised through constitutional legislative procedures", "To permit unlimited expenditure without scrutiny", "To eliminate the annual financial statement", "To transfer all public funds to private companies", "A"),
        ("What is a hung Parliament?", "A situation in which no party or alliance has an outright majority in the Lok Sabha", "A Parliament without any elected members", "A Parliament that has passed every proposed bill", "A Parliament in which the Rajya Sabha is abolished", "A"),
        ("How may a government be formed when no party has a clear Lok Sabha majority?", "Through constitutional processes involving a leader who can demonstrate the confidence of the House", "Automatically by the Chief Justice", "By allowing the largest private company to choose ministers", "Without any need to demonstrate legislative support", "A"),
        ("Why is the Speaker expected to maintain impartiality while presiding over the Lok Sabha?", "To conduct proceedings fairly according to parliamentary rules", "To give the ruling party unlimited power", "To decide all criminal cases", "To replace the President", "A"),
        ("What is the purpose of parliamentary committees in financial scrutiny?", "They examine expenditure, accounts and related matters in greater detail", "They replace the Comptroller and Auditor General in every function", "They approve all court judgments", "They abolish the Union Budget", "A"),
        ("What does the doctrine of ministerial responsibility connect?", "The executive's continued political accountability with the confidence of the elected House", "The judiciary's control over all elections", "Private companies with constitutional amendments", "The President's office with local village councils only", "A"),
        ("Why is parliamentary government considered a system of checks and accountability?", "The executive must answer to Parliament and may lose office if it loses the Lok Sabha's confidence", "The executive is legally unlimited", "Parliament cannot question ministers", "The judiciary must run every ministry", "A"),
        ("How does the Constitution shape parliamentary government in India?", "It establishes executive offices, ministerial responsibility, legislative procedures and constitutional limits", "It gives the executive unlimited authority", "It removes the role of Parliament", "It makes every minister directly elected as President", "A"),
    ],
}


def main():
    db = SessionLocal()

    try:
        lesson = (
            db.query(Lesson)
            .filter(
                Lesson.title == "Parliamentary Government",
                Lesson.topic == "Social Science"
            )
            .first()
        )

        if not lesson:
            print("ERROR: Parliamentary Government lesson was not found.")
            print("Check the exact lesson title and topic in your database.")
            return

        added = 0

        for difficulty, questions in QUESTION_BANK.items():
            quiz = (
                db.query(Quiz)
                .filter(
                    Quiz.lesson_id == lesson.id,
                    Quiz.difficulty == difficulty
                )
                .first()
            )

            if not quiz:
                quiz = Quiz(
                    lesson_id=lesson.id,
                    title=f"{lesson.title} - {difficulty}",
                    difficulty=difficulty
                )
                db.add(quiz)
                db.flush()

            existing = db.query(Question).filter(
                Question.quiz_id == quiz.id
            ).all()

            if len(existing) >= 30:
                print(f"{difficulty}: already has {len(existing)} questions; skipped.")
                continue

            existing_texts = {
                q.question.strip().lower() for q in existing
            }

            for item in questions:
                if len(existing) >= 30:
                    break

                question_text, a, b, c, d, correct_letter = item

                if question_text.strip().lower() in existing_texts:
                    continue

                options = [a, b, c, d]
                correct_text = options[ord(correct_letter) - ord("A")]
                random.shuffle(options)
                new_correct_letter = "ABCD"[options.index(correct_text)]

                db.add(
                    Question(
                        quiz_id=quiz.id,
                        question=question_text,
                        option_a=options[0],
                        option_b=options[1],
                        option_c=options[2],
                        option_d=options[3],
                        correct_answer=new_correct_letter
                    )
                )

                existing_texts.add(question_text.strip().lower())
                existing.append(None)
                added += 1

            print(f"{difficulty}: prepared {min(len(existing), 30)}/30 questions.")

        db.commit()

        print("\n========== FINAL VERIFICATION ==========")
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

        print(f"TOTAL: {total}/90")
        print(f"New questions added: {added}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()