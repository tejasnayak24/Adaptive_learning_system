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
        ("What is the main law-making body at the state level in India?", "State Legislature", "Supreme Court", "Election Commission", "District Hospital", "A"),
        ("Who is the constitutional head of a state?", "Governor", "Chief Minister", "Mayor", "District Collector", "A"),
        ("Who is generally the head of the elected state government?", "Chief Minister", "Governor", "President of India", "Chief Justice of India", "A"),
        ("Who appoints the Governor of an Indian state?", "President of India", "Chief Minister alone", "Lok Sabha Speaker", "Mayor", "A"),
        ("Who appoints the Chief Minister of a state?", "Governor", "Chief Justice of India", "District Collector", "Election Commission", "A"),
        ("What is the main role of the Chief Minister?", "To lead the state government", "To preside over the Supreme Court", "To conduct national elections", "To command every district court", "A"),
        ("What is a Member of the Legislative Assembly called?", "MLA", "MP", "Sarpanch", "Councillor", "A"),
        ("What is the lower house of a state legislature called in states with two houses?", "Legislative Assembly", "Legislative Council", "Rajya Sabha", "Supreme Court", "A"),
        ("What is the upper house of a state legislature called where one exists?", "Legislative Council", "Legislative Assembly", "Lok Sabha", "District Court", "A"),
        ("Do all Indian states have a Legislative Council?", "No", "Yes, all states must have one", "Only union territories have one", "Only villages have one", "A"),
        ("What is the main function of the State Legislature?", "To make laws on matters within its legislative authority", "To decide every Supreme Court case", "To conduct all national elections", "To appoint the President", "A"),
        ("What does the state government manage?", "State-level public services and administration", "Only foreign affairs", "Only the armed forces", "All international treaties independently", "A"),
        ("Who is responsible for leading the state Council of Ministers?", "Chief Minister", "Governor alone", "Lok Sabha Speaker", "Chief Justice", "A"),
        ("What is the normal term of a State Legislative Assembly?", "Five years unless dissolved earlier", "Two years in every case", "Six years in every case", "Ten years without elections", "A"),
        ("Who elects the members of a State Legislative Assembly?", "Eligible voters in Assembly constituencies", "Supreme Court judges", "Private companies", "District police officers", "A"),
        ("What is a state constituency?", "An area represented by an elected MLA", "A court building", "A government department", "A state budget document", "A"),
        ("What is the purpose of the state budget?", "To present estimated state government receipts and expenditure", "To appoint all judges", "To select the President", "To conduct school examinations", "A"),
        ("What is the role of state ministers?", "To manage assigned departments and help implement government policy", "To decide every court case", "To conduct all Union government elections", "To replace the legislature", "A"),
        ("What is a state department?", "An administrative unit responsible for a particular area of government work", "A private sports club", "A court judgment", "An election constituency", "A"),
        ("Which government generally manages state police administration?", "State government, subject to the Constitution and applicable law", "A private company", "The village school", "The United Nations", "A"),
        ("Who is the constitutional head of the Union government?", "President of India", "Chief Minister", "Governor of every state jointly", "State Assembly Speaker", "A"),
        ("What does the opposition do in a State Legislature?", "Questions government decisions and presents alternative views", "Appoints every judge", "Conducts all national elections", "Replaces the Governor automatically", "A"),
        ("What is a state law?", "A law enacted by a competent state legislature within its authority", "A private company advertisement", "A school timetable", "A court building", "A"),
        ("Why are state elections important?", "They allow voters to choose their state representatives", "They appoint every Supreme Court judge", "They cancel the Constitution", "They replace all local governments", "A"),
        ("What is the role of the Speaker of a Legislative Assembly?", "To preside over Assembly proceedings and maintain order", "To head the state police", "To appoint the Chief Minister independently", "To decide all criminal appeals", "A"),
        ("What does the Governor generally do in the legislative process?", "Exercises constitutional functions concerning state legislation", "Makes every state law alone", "Replaces all elected MLAs", "Conducts all village elections", "A"),
        ("What is the Council of Ministers at the state level?", "The group of ministers headed by the Chief Minister", "A group of judges", "A committee of private business owners", "A national election body", "A"),
        ("What is a public service provided by a state government?", "State hospitals and public health services", "Foreign embassy management alone", "National currency printing alone", "International treaty negotiation alone", "A"),
        ("Why should state governments be accountable?", "They must answer for their decisions and use of public resources", "They can ignore all laws", "They never need to explain spending", "They are not subject to the Constitution", "A"),
        ("What is the relationship between the Governor and the Chief Minister?", "The Governor is the constitutional head, while the Chief Minister leads the elected government", "Both offices are identical", "The Chief Minister is a court judge", "The Governor is elected directly as an MLA", "A"),
    ],

    "Medium": [
        ("Why is the Chief Minister important in a state parliamentary system?", "The Chief Minister leads the Council of Ministers and coordinates state government policy", "The Chief Minister heads the Supreme Court", "The Chief Minister independently appoints every MLA", "The Chief Minister replaces the Constitution", "A"),
        ("What is the difference between the Governor and the Chief Minister?", "The Governor is the constitutional head, while the Chief Minister leads the elected executive", "The Governor is always the leader of the opposition", "The Chief Minister is the head of the judiciary", "Both offices have exactly the same functions", "A"),
        ("To which body is the state Council of Ministers collectively responsible?", "Legislative Assembly", "Supreme Court", "Rajya Sabha", "Election Commission", "A"),
        ("Why is the Legislative Assembly directly elected?", "It represents the people through elected constituency representatives", "It represents only appointed judges", "It consists entirely of civil servants", "It is selected by private companies", "A"),
        ("What is the main difference between a unicameral and bicameral state legislature?", "A unicameral legislature has one house; a bicameral legislature has two", "A unicameral legislature has no members", "A bicameral legislature has only courts", "Both terms refer to the same structure", "A"),
        ("How is a State Legislative Council different from a Legislative Assembly?", "The Council is an upper house where it exists, while the Assembly is the directly elected lower house", "The Council is always the directly elected lower house", "The Assembly is a court", "The Council exists in every state", "A"),
        ("Why are state budgets presented to the legislature?", "To enable legislative scrutiny and authorisation of public expenditure under applicable procedures", "To allow spending without any approval", "To select the Governor by direct election", "To abolish state taxation", "A"),
        ("What is the role of the opposition in a State Legislature?", "To scrutinise policies, question ministers and raise public concerns", "To appoint all state judges", "To run the Election Commission", "To replace all government departments", "A"),
        ("What happens if a state government loses the confidence of its Legislative Assembly?", "The Council of Ministers is expected to resign or follow the applicable constitutional process", "The Assembly automatically becomes a court", "The Governor's office ends permanently", "All state laws become invalid automatically", "A"),
        ("Why may the Governor exercise discretion in certain matters?", "The Constitution or applicable law provides discretion in specified circumstances", "The Governor has unlimited personal authority over every decision", "The Governor can ignore the Constitution", "The Governor replaces all elected institutions", "A"),
        ("What is the purpose of a state cabinet meeting?", "To discuss and coordinate important government decisions and policies", "To conduct Supreme Court trials", "To elect all Members of Parliament", "To replace the State Legislature permanently", "A"),
        ("How do state governments contribute to public health?", "They administer state health services and implement relevant policies", "They control every international treaty", "They print all national currency", "They replace all private medical professionals", "A"),
        ("Which subject is generally associated with the State List in the Seventh Schedule?", "Police", "Foreign affairs", "Defence", "Currency", "A"),
        ("Which subject is generally a Union List matter?", "Defence", "Public order", "Police", "Agriculture", "A"),
        ("What is the Concurrent List?", "A list of subjects on which both Parliament and State Legislatures may legislate, subject to constitutional rules", "A list containing only state police matters", "A list of court cases", "A list of election candidates", "A"),
        ("Why is the division of legislative powers important?", "It allocates law-making authority between the Union and states", "It gives every state unlimited authority over every subject", "It abolishes the Constitution", "It prevents all cooperation between governments", "A"),
        ("What is the role of the state administration?", "To implement laws, policies and public services within the state's jurisdiction", "To amend the Constitution independently", "To decide every Supreme Court appeal", "To manage foreign relations alone", "A"),
        ("What is the role of a state civil servant?", "To support administration and implement lawful government decisions", "To independently replace the legislature", "To elect the Governor directly", "To decide every judicial appeal", "A"),
        ("How can MLAs raise local constituency issues?", "Through Assembly questions, debates, motions and other permitted procedures", "Only by issuing court judgments", "By appointing the President", "By replacing all municipal bodies", "A"),
        ("What is a motion of no confidence in a State Legislative Assembly?", "A motion testing whether the state government retains the Assembly's confidence", "A motion appointing every High Court judge", "A motion cancelling every state election", "A motion dissolving the Supreme Court", "A"),
        ("Why are Assembly committees useful?", "They can examine legislation, expenditure and policy in detail", "They replace every election", "They run all national ministries", "They abolish the state budget", "A"),
        ("What is the purpose of a Governor's address to the State Legislature?", "To address the legislature at constitutionally specified occasions and outline the government's programme", "To deliver Supreme Court judgments", "To appoint every MLA", "To replace the state budget", "A"),
        ("Can a Governor reserve a state bill for the President's consideration?", "Yes, in circumstances permitted by the Constitution", "No, under no circumstances", "Yes, every bill must be reserved automatically", "Only the Speaker can reserve bills", "A"),
        ("Why are state elections essential to accountability?", "Voters can reward or replace representatives through democratic elections", "They permanently eliminate opposition parties", "They give the Governor unlimited power", "They remove the need for public services", "A"),
        ("What is the purpose of state legislation on public order?", "To regulate matters within the state's constitutional legislative authority", "To control all foreign affairs", "To print currency", "To negotiate all international treaties", "A"),
        ("What is the difference between an ordinance and an Act passed by a legislature?", "An ordinance is issued under a constitutional ordinance-making power; an Act is enacted through the legislative process", "An ordinance is always a court judgment", "An Act is never legally binding", "Both are private company rules", "A"),
        ("Why must the state government follow the Constitution?", "Its powers and actions are limited by constitutional provisions", "It has unlimited authority over every subject", "It can abolish fundamental rights independently", "It is not subject to judicial review", "A"),
        ("How can citizens hold a state government accountable between elections?", "Through lawful complaints, public debate, information requests and engagement with representatives", "By refusing to follow every law", "By making private judgments legally binding", "By cancelling the Constitution", "A"),
        ("What is the purpose of state-level welfare programmes?", "To address public needs through services and support within government authority", "To eliminate all public services", "To replace the judiciary", "To prevent people from accessing education", "A"),
        ("How does a state government differ from a local government?", "A state government operates at the state level, while local governments manage local matters under applicable law", "Local governments control foreign affairs", "State governments only manage private businesses", "They are the same institution", "A"),
    ],

    "Hard": [
        ("Which article provides for a Council of Ministers with the Chief Minister at its head to aid and advise the Governor?", "Article 163", "Article 14", "Article 32", "Article 110", "A"),
        ("Which article provides for the appointment of the Chief Minister and other state ministers?", "Article 164", "Article 21", "Article 51A", "Article 280", "A"),
        ("Which article provides for the composition of the Legislative Assemblies of states?", "Article 170", "Article 14", "Article 32", "Article 123", "A"),
        ("Which article deals with the duration of State Legislative Assemblies?", "Article 172", "Article 19", "Article 110", "Article 148", "A"),
        ("Which article provides for the Speaker and Deputy Speaker of a State Legislative Assembly?", "Article 178", "Article 74", "Article 124", "Article 280", "A"),
        ("Which article provides for the Governor's assent to bills passed by the State Legislature?", "Article 200", "Article 14", "Article 32", "Article 110", "A"),
        ("Which article provides for the Governor's ordinance-making power when the State Legislature is not in session, subject to constitutional conditions?", "Article 213", "Article 123", "Article 226", "Article 280", "A"),
        ("Which article deals with the constitution of State Legislatures?", "Article 168", "Article 14", "Article 32", "Article 51A", "A"),
        ("Which article provides for the Governor's power to summon, prorogue and dissolve the Legislative Assembly?", "Article 174", "Article 19", "Article 110", "Article 324", "A"),
        ("Which article provides for the Governor's special address to the State Legislature?", "Article 176", "Article 21", "Article 32", "Article 280", "A"),
        ("Which article provides that the state Council of Ministers is collectively responsible to the Legislative Assembly?", "Article 164(2)", "Article 14", "Article 110", "Article 148", "A"),
        ("Which article deals with the Governor's appointment by the President?", "Article 155", "Article 19", "Article 32", "Article 280", "A"),
        ("Which article specifies the Governor's term of office, subject to holding office during the President's pleasure?", "Article 156", "Article 14", "Article 21", "Article 110", "A"),
        ("Which article provides for the Governor's power to grant pardons and other forms of clemency for matters within the state's executive power?", "Article 161", "Article 32", "Article 110", "Article 280", "A"),
        ("Which article deals with the distribution of legislative powers between Parliament and State Legislatures?", "Article 246", "Article 14", "Article 21", "Article 51A", "A"),
        ("Which schedule lists the Union, State and Concurrent Lists?", "Seventh Schedule", "First Schedule", "Fifth Schedule", "Tenth Schedule", "A"),
        ("Which subject is generally included in the State List?", "Police", "Defence", "Foreign affairs", "Currency", "A"),
        ("Which article provides for Parliament's power to legislate on State List matters in the national interest following a qualifying Rajya Sabha resolution?", "Article 249", "Article 14", "Article 32", "Article 110", "A"),
        ("Which article permits Parliament to legislate on State List matters during a Proclamation of Emergency, subject to constitutional provisions?", "Article 250", "Article 19", "Article 21", "Article 280", "A"),
        ("Which article provides for Parliament to legislate for two or more states by consent?", "Article 252", "Article 14", "Article 32", "Article 110", "A"),
        ("Which article provides for Parliament's power to legislate on State List matters to implement international agreements?", "Article 253", "Article 21", "Article 32", "Article 148", "A"),
        ("Which article deals with the effect of inconsistency between laws made by Parliament and State Legislatures on Concurrent List matters?", "Article 254", "Article 14", "Article 19", "Article 51A", "A"),
        ("Which article provides for the creation or abolition of a State Legislative Council?", "Article 169", "Article 110", "Article 123", "Article 280", "A"),
        ("Which article provides that a Money Bill in a state legislature is defined in relation to the relevant constitutional provisions?", "Article 199", "Article 14", "Article 32", "Article 148", "A"),
        ("Which article concerns the annual financial statement of a state?", "Article 202", "Article 19", "Article 21", "Article 280", "A"),
        ("Which article provides for demands for grants in a state legislature?", "Article 203", "Article 14", "Article 32", "Article 110", "A"),
        ("Which article provides for the Governor's recommendation in relation to certain financial bills and demands for grants?", "Article 207", "Article 19", "Article 21", "Article 324", "A"),
        ("Which article addresses the appointment of a State Advocate General?", "Article 165", "Article 14", "Article 32", "Article 110", "A"),
        ("Which article provides for the High Court's superintendence over courts and tribunals within its territorial jurisdiction, subject to constitutional provisions?", "Article 227", "Article 19", "Article 110", "Article 280", "A"),
        ("What is the constitutional principle governing the Governor's role in a parliamentary state government?", "The Governor acts according to constitutional provisions, generally on ministerial aid and advice except where discretion is permitted", "The Governor has unlimited personal power over every state decision", "The Governor replaces the elected legislature", "The Governor is not bound by the Constitution", "A"),
    ],
}


def main():
    db = SessionLocal()

    try:
        lesson = (
            db.query(Lesson)
            .filter(
                Lesson.title == "The State Government",
                Lesson.topic == "Social Science"
            )
            .first()
        )

        if not lesson:
            print("ERROR: The State Government lesson was not found.")
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