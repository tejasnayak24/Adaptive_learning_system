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
        ("What is the main function of the judiciary?", "To interpret laws and deliver justice", "To conduct elections", "To collect school fees", "To build roads", "A"),
        ("Which is the highest court in India?", "District Court", "Supreme Court", "High Court", "Family Court", "B"),
        ("Where is the Supreme Court of India located?", "Mumbai", "Chennai", "New Delhi", "Kolkata", "C"),
        ("What is the head of the Supreme Court called?", "Chief Justice of India", "Prime Minister", "President of Parliament", "Attorney General of a state", "A"),
        ("What is a judge's main responsibility?", "To decide cases according to law", "To make election posters", "To run private companies", "To manage schools", "A"),
        ("Which court generally operates at the district level?", "Supreme Court", "District Court", "Parliament", "Gram Sabha", "B"),
        ("What does an independent judiciary mean?", "Courts can decide cases without improper influence", "Courts must follow every political instruction", "Judges make decisions for personal benefit", "Courts do not follow laws", "A"),
        ("What is the Constitution?", "The supreme legal framework of the country", "A list of sports rules", "A private contract only", "A school timetable", "A"),
        ("What is a court case?", "A legal dispute or matter considered by a court", "A parliamentary election", "A school competition", "A business advertisement", "A"),
        ("Who can approach a court to seek justice?", "People who have a legal matter or grievance", "Only ministers", "Only police officers", "Only judges", "A"),
        ("What is a lawyer's role in court?", "To represent and advise a client on legal matters", "To decide the final judgment", "To command the police", "To conduct elections", "A"),
        ("What is a judgment?", "A court's decision in a case", "A government budget", "An election campaign", "A police uniform", "A"),
        ("What is an appeal?", "A request to a higher court to review a decision", "A request to cancel the Constitution", "A type of election", "A school examination", "A"),
        ("What does the rule of law mean?", "Everyone is subject to the law", "Only ordinary citizens must follow laws", "Officials can ignore every law", "Courts are above the Constitution", "A"),
        ("Which courts operate at the state level as the highest courts in their respective states?", "High Courts", "District Courts", "Village schools", "Municipal offices", "A"),
        ("Who appoints judges of the Supreme Court of India under the constitutional process?", "The President of India", "The Prime Minister acting alone", "The Lok Sabha Speaker alone", "The Chief Minister of every state", "A"),
        ("What is the purpose of evidence in a court case?", "To help establish facts relevant to the case", "To replace every law", "To choose election candidates", "To set school holidays", "A"),
        ("What is a witness?", "A person who provides relevant information about a matter", "A person who always decides the case", "A court building", "A type of law", "A"),
        ("Why are courts important in society?", "They resolve legal disputes and protect rights", "They replace all elected governments", "They conduct every school exam", "They manage private shops", "A"),
        ("What is justice?", "Fair treatment according to law and rights", "Giving special treatment to powerful people", "Ignoring evidence", "Punishing everyone equally regardless of facts", "A"),
        ("What does a criminal court generally deal with?", "Cases involving alleged offences", "Only property sales", "Only school admissions", "Only road construction", "A"),
        ("What does a civil court generally deal with?", "Disputes involving matters such as property or contracts", "Only national elections", "Only military training", "Only weather reports", "A"),
        ("What is legal aid?", "Assistance that helps eligible people access legal services", "A fine imposed by a court", "A type of election", "A government building", "A"),
        ("What does a fair trial require?", "A fair opportunity to present and examine the case under law", "A decision before hearing evidence", "Punishment without a hearing", "A decision based only on popularity", "A"),
        ("What is the role of the police in the justice system?", "To investigate offences and maintain law and order within the law", "To deliver every final court judgment", "To amend the Constitution", "To appoint Supreme Court judges", "A"),
        ("Can a court review whether a government action follows the Constitution?", "Yes, within its jurisdiction and applicable law", "No court can ever examine government action", "Only a private company can do so", "Only a school principal can do so", "A"),
        ("What is a petition?", "A formal request submitted to an authority or court", "A type of court building", "A police uniform", "A parliamentary seat", "A"),
        ("What does a summons generally require?", "A person to appear before a court or authority as directed", "A judge to resign", "A law to disappear", "An election to end permanently", "A"),
        ("Why must judges be impartial?", "To ensure decisions are based on law and evidence rather than bias", "To favour wealthy parties", "To avoid reading evidence", "To follow public rumours", "A"),
        ("What is the purpose of a court hearing?", "To consider arguments, evidence or legal issues", "To conduct a national election", "To write school textbooks", "To appoint village leaders", "A"),
    ],

    "Medium": [
        ("Why is judicial independence essential in a democracy?", "It helps courts decide cases fairly without improper external pressure", "It allows judges to ignore the Constitution", "It gives courts the power to conduct elections", "It removes the need for legal procedures", "A"),
        ("What is the hierarchy of the Indian judicial system generally?", "Supreme Court, High Courts, and subordinate courts", "High Courts, Parliament, and police stations", "District Courts, Parliament, and Cabinet", "Supreme Court, municipal offices, and schools", "A"),
        ("What is judicial review?", "The power of courts to examine the constitutional validity of laws and government actions", "The process of conducting elections", "The appointment of every minister", "A method of collecting taxes", "A"),
        ("What is the main difference between civil and criminal cases?", "Civil cases usually concern private rights or disputes; criminal cases concern alleged offences", "Civil cases always involve imprisonment, while criminal cases never do", "Both are handled only by Parliament", "There is no difference in any circumstance", "A"),
        ("Why are High Courts important?", "They exercise jurisdiction over their states or territories and supervise subordinate courts as provided by law", "They replace the Supreme Court in every matter", "They conduct all parliamentary elections", "They make all Union laws", "A"),
        ("What does the right to constitutional remedies help citizens do?", "Approach appropriate courts to enforce fundamental rights", "Avoid all legal responsibilities", "Choose Supreme Court judges by direct election", "Cancel all court proceedings", "A"),
        ("Which writ may be used to require a public authority to perform a legal duty?", "Mandamus", "Habeas corpus", "Quo warranto", "Certiorari in every circumstance", "A"),
        ("What is the purpose of habeas corpus?", "To protect against unlawful detention by requiring the detained person to be brought before a court", "To appoint a judge", "To approve a government budget", "To conduct a parliamentary vote", "A"),
        ("What does the writ of prohibition generally do?", "Prevents a lower court or tribunal from proceeding beyond its jurisdiction", "Appoints a new government", "Cancels all criminal laws", "Orders a person to become a minister", "A"),
        ("What is the purpose of certiorari?", "A higher court may quash an order of a lower court or tribunal on recognised legal grounds", "It is used only to register voters", "It creates a new state", "It approves every private contract", "A"),
        ("What does quo warranto question?", "The legal authority of a person to hold a public office", "The result of every election", "The amount of a school fee", "The ownership of every private vehicle", "A"),
        ("Why is legal aid important?", "It helps eligible people who cannot afford legal services seek justice", "It guarantees victory in every case", "It allows lawyers to ignore evidence", "It replaces all courts", "A"),
        ("What is public interest litigation (PIL)?", "Legal proceedings brought to address a matter affecting public interest under applicable rules", "A private business advertisement", "A mandatory election campaign", "A process for appointing ministers", "A"),
        ("How can the judiciary protect fundamental rights?", "By providing remedies when rights are violated, within its jurisdiction", "By suspending all rights permanently", "By replacing the Constitution", "By preventing people from approaching courts", "A"),
        ("What is the role of precedent in the judicial system?", "Earlier relevant judicial decisions can guide or bind later decisions according to legal rules", "Every past decision must be followed regardless of law", "It replaces written legislation entirely", "It applies only to school examinations", "A"),
        ("What is contempt of court generally concerned with?", "Conduct that legally interferes with or undermines the administration of justice", "Any disagreement with a friend", "Every criticism of a public official", "All parliamentary debates", "A"),
        ("Why are court procedures important?", "They support fairness, consistency and proper consideration of cases", "They allow decisions without evidence", "They remove the need for legal rights", "They ensure every case has the same outcome", "A"),
        ("What is the role of a public prosecutor in a criminal case?", "To present the prosecution's case on behalf of the state", "To act as the judge", "To appoint the accused person's lawyer in every case", "To decide the final sentence independently", "A"),
        ("What is the presumption of innocence?", "An accused person is treated as innocent unless guilt is established according to law", "Every accusation proves guilt", "Only wealthy people are presumed innocent", "Evidence is never required in criminal cases", "A"),
        ("What does an acquittal mean?", "The accused is found not guilty in the case", "The accused is automatically elected to Parliament", "The judge is removed from office", "The case becomes a new law", "A"),
        ("What is the purpose of cross-examination?", "To test a witness's testimony through questions by the opposing side", "To appoint a judge", "To make a new Constitution", "To decide the election schedule", "A"),
        ("Why may a higher court overturn a lower court's decision?", "It may identify legal or procedural errors within its appellate jurisdiction", "It can change any decision without legal authority", "It must overturn every lower court decision", "It replaces every trial with an election", "A"),
        ("What is the difference between original and appellate jurisdiction?", "Original jurisdiction concerns cases first heard by a court; appellate jurisdiction concerns reviewing decisions", "Original jurisdiction is for elections only; appellate jurisdiction is for schools", "They mean exactly the same thing", "Appellate jurisdiction means writing legislation", "A"),
        ("Why is separation of powers relevant to the judiciary?", "It helps limit concentration of power and supports checks and balances", "It makes courts subordinate to every private company", "It eliminates all constitutional limits", "It gives judges control over every government function", "A"),
        ("How can delays in court cases affect justice?", "They can increase costs and postpone relief for people involved", "They always improve access to justice", "They automatically prove the accused is guilty", "They remove the need for evidence", "A"),
        ("What is mediation?", "A process in which a neutral person helps parties try to reach an agreement", "A type of criminal punishment in every case", "A method of electing judges", "A parliamentary session", "A"),
        ("What is arbitration?", "A dispute-resolution process in which an arbitrator gives a decision under applicable rules", "A national election", "A police investigation in every case", "A method of amending the Constitution", "A"),
        ("Why is access to justice important?", "People need practical and fair ways to protect rights and resolve disputes", "Only wealthy people should use courts", "Courts should accept no complaints", "Legal rights should never be enforced", "A"),
        ("What does judicial accountability seek to ensure?", "Judges and courts operate according to constitutional and legal standards", "Judges may act without any legal constraints", "Every judgment is decided by public opinion polls", "Courts can ignore all procedures", "A"),
        ("How does the judiciary support constitutional government?", "It interprets and applies the Constitution and checks unlawful actions within its authority", "It replaces all elections and legislatures", "It writes every government policy alone", "It eliminates the rule of law", "A"),
    ],

    "Hard": [
        ("Which article establishes the Supreme Court of India?", "Article 124", "Article 32", "Article 226", "Article 280", "A"),
        ("Which article empowers the Supreme Court to issue writs for enforcement of fundamental rights?", "Article 32", "Article 40", "Article 110", "Article 360", "A"),
        ("Which article empowers High Courts to issue writs?", "Article 226", "Article 14", "Article 75", "Article 123", "A"),
        ("Which article provides for the appointment and conditions of office of a High Court judge?", "Article 217", "Article 32", "Article 110", "Article 356", "A"),
        ("Which article provides for the Supreme Court to be a court of record?", "Article 129", "Article 21", "Article 72", "Article 280", "A"),
        ("Which article provides for the Supreme Court's advisory jurisdiction?", "Article 143", "Article 19", "Article 40", "Article 148", "A"),
        ("Which article deals with the law declared by the Supreme Court being binding on all courts in India?", "Article 141", "Article 14", "Article 110", "Article 324", "A"),
        ("Which article provides for the review of Supreme Court judgments or orders?", "Article 137", "Article 21", "Article 75", "Article 280", "A"),
        ("Under which article can the Supreme Court transfer certain cases between High Courts or from a High Court to itself?", "Article 139A", "Article 19", "Article 110", "Article 352", "A"),
        ("Which article provides for the establishment of a common High Court for two or more states or for states and Union Territories?", "Article 231", "Article 32", "Article 74", "Article 123", "A"),
        ("Which article provides for the control of subordinate courts by the High Court?", "Article 235", "Article 14", "Article 110", "Article 280", "A"),
        ("Which article addresses the appointment of district judges?", "Article 233", "Article 21", "Article 75", "Article 324", "A"),
        ("Which article provides for the removal of a Supreme Court judge through a constitutionally prescribed process?", "Article 124(4)", "Article 19(1)", "Article 110", "Article 360", "A"),
        ("What is the retirement age of a Supreme Court judge in India?", "65 years", "60 years", "62 years", "70 years", "A"),
        ("What is the retirement age of a High Court judge in India?", "62 years", "60 years", "65 years", "70 years", "A"),
        ("Which article deals with the transfer of a High Court judge from one High Court to another?", "Article 222", "Article 32", "Article 110", "Article 280", "A"),
        ("Which article grants the Supreme Court power to do complete justice in a matter before it?", "Article 142", "Article 19", "Article 75", "Article 324", "A"),
        ("Which article provides for appeals to the Supreme Court in certain civil matters?", "Article 133", "Article 14", "Article 40", "Article 123", "A"),
        ("Which article provides for appeals to the Supreme Court in certain criminal matters?", "Article 134", "Article 21", "Article 110", "Article 148", "A"),
        ("Which article allows the Supreme Court to grant special leave to appeal, subject to constitutional exceptions?", "Article 136", "Article 19", "Article 75", "Article 280", "A"),
        ("Which article deals with the appointment of the Chief Justice and other judges of a High Court?", "Article 217", "Article 124", "Article 143", "Article 226", "A"),
        ("Which article provides for the High Court to be a court of record?", "Article 215", "Article 32", "Article 110", "Article 360", "A"),
        ("Which article gives Parliament power to extend the Supreme Court's jurisdiction in certain matters, subject to constitutional provisions?", "Article 138", "Article 14", "Article 40", "Article 352", "A"),
        ("Which article concerns the law-making power of Parliament regarding the jurisdiction and powers of the Supreme Court?", "Article 140", "Article 19", "Article 75", "Article 324", "A"),
        ("What is the basic-structure doctrine associated with judicial review?", "Parliament cannot alter the Constitution's basic structure through its amendment power", "Parliament can abolish every constitutional limit", "Courts must approve every ordinary policy before it begins", "Fundamental rights can never be interpreted by courts", "A"),
        ("What is the collegium system in judicial appointments?", "A judge-led system developed through Supreme Court decisions for recommending higher judicial appointments", "A direct election of all judges by citizens", "A committee of state police chiefs", "A system for electing members of Parliament", "A"),
        ("What does the doctrine of separation of powers seek to prevent?", "Excessive concentration of governmental powers in one institution", "All cooperation among government branches", "All judicial review", "The enforcement of fundamental rights", "A"),
        ("Which statement best describes judicial review in India?", "Courts can examine the constitutionality of laws and executive actions within their jurisdiction", "Every court may repeal any law without legal reasoning", "Only Parliament can interpret the Constitution", "Judicial review applies only to private contracts", "A"),
        ("What is the difference between Article 32 and Article 226?", "Article 32 concerns Supreme Court remedies for fundamental rights; Article 226 gives High Courts broader writ jurisdiction", "Article 32 applies only to elections, while Article 226 applies only to taxes", "Both articles give identical jurisdiction in every respect", "Article 226 removes High Court writ powers", "A"),
        ("Why is the independence of the judiciary protected through constitutional safeguards?", "To support impartial adjudication and protect the rule of law", "To allow judges to ignore the Constitution", "To make judges accountable only to political parties", "To prevent courts from hearing citizens' cases", "A"),
    ],
}


def main():
    db = SessionLocal()

    try:
        lesson = (
            db.query(Lesson)
            .filter(
                Lesson.title == "The Judiciary",
                Lesson.topic == "Social Science"
            )
            .first()
        )

        if not lesson:
            print("ERROR: The Judiciary lesson was not found.")
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