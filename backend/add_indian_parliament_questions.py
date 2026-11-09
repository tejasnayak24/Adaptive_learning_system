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
        ("What is the main function of the Indian Parliament?", "To make laws", "To conduct school exams", "To run private companies", "To manage hospitals", "A"),
        ("How many houses does the Indian Parliament have?", "One", "Two", "Three", "Four", "B"),
        ("What are the two houses of Parliament?", "Lok Sabha and Rajya Sabha", "Vidhan Sabha and Gram Sabha", "Supreme Court and High Court", "Cabinet and Secretariat", "A"),
        ("Which house is called the House of the People?", "Rajya Sabha", "Lok Sabha", "Supreme Court", "Legislative Council", "B"),
        ("Which house represents the states of India?", "Lok Sabha", "Gram Sabha", "Rajya Sabha", "Municipal Council", "C"),
        ("Who is the constitutional head of India?", "Prime Minister", "Chief Justice", "President", "Speaker", "C"),
        ("Who presides over the Lok Sabha?", "President", "Speaker", "Prime Minister", "Governor", "B"),
        ("Who is the leader of the Union government?", "Prime Minister", "President of the Supreme Court", "Governor", "Mayor", "A"),
        ("What is a Member of Parliament commonly called?", "MLA", "MP", "Sarpanch", "Councillor", "B"),
        ("Which house is directly elected by the people?", "Rajya Sabha", "Lok Sabha", "Legislative Council", "Both houses indirectly", "B"),
        ("What is the minimum voting age in India?", "16 years", "17 years", "18 years", "21 years", "C"),
        ("What do citizens use to choose their representatives?", "Elections", "Court trials", "School tests", "Appointments by companies", "A"),
        ("What is the main purpose of elections?", "To select representatives", "To appoint judges directly", "To write textbooks", "To collect school fees", "A"),
        ("Who formally summons a session of Parliament?", "The President", "The Chief Minister", "The Mayor", "The Chief Election Commissioner", "A"),
        ("What is a bill?", "A proposed law", "A court building", "An election symbol", "A government employee", "A"),
        ("What does Parliament discuss?", "National issues and laws", "Only sports competitions", "Only private business deals", "Only school activities", "A"),
        ("Which house has members elected for a term of five years, normally?", "Lok Sabha", "Rajya Sabha", "Supreme Court", "Election Commission", "A"),
        ("Which house is a permanent house?", "Lok Sabha", "Rajya Sabha", "Both houses dissolve together", "Neither house", "B"),
        ("Who represents a constituency in the Lok Sabha?", "An MP", "A village accountant", "A judge", "A school principal", "A"),
        ("What is the Parliament building used for?", "Parliamentary proceedings", "Military training only", "School examinations", "Private weddings", "A"),
        ("What does democracy allow citizens to do?", "Choose their representatives", "Avoid all laws", "Cancel every election", "Rule without representatives", "A"),
        ("Which institution makes laws at the Union level?", "Parliament", "Police station", "Municipality alone", "District hospital", "A"),
        ("What is the official residence of the President called?", "Rashtrapati Bhavan", "Parliament House Library", "India Gate", "Red Fort", "A"),
        ("What is the term for a person elected to the Rajya Sabha?", "Member of Parliament", "Sarpanch", "Mayor", "District Collector", "A"),
        ("What is the role of opposition parties in Parliament?", "To question and scrutinise the government", "To cancel all elections", "To replace the courts", "To prevent every discussion", "A"),
        ("What does a parliamentary debate involve?", "Discussion of issues and proposals", "Only silent voting", "Only sporting events", "Only private interviews", "A"),
        ("Which body conducts elections to Parliament?", "Election Commission of India", "Supreme Court Registry", "Reserve Bank of India", "Union Public Service Commission", "A"),
        ("What is a constituency?", "An area represented by an elected member", "A government ministry", "A court judgment", "A type of tax", "A"),
        ("What is the main purpose of parliamentary questions?", "To seek information from the government", "To appoint every judge", "To conduct census interviews", "To issue school certificates", "A"),
        ("What does the word 'Parliament' refer to in India?", "The national law-making institution", "A state police unit", "A private organisation", "A local sports club", "A"),
    ],

    "Medium": [
        ("Why is Parliament important in a democracy?", "It allows elected representatives to make laws and hold the government accountable", "It replaces all courts", "It prevents citizens from voting", "It gives unlimited power to one official", "A"),
        ("How are Lok Sabha members generally elected?", "Directly by voters in constituencies", "Only by Supreme Court judges", "By village councils alone", "By the President without elections", "A"),
        ("How are most Rajya Sabha members elected?", "By elected members of State Legislative Assemblies", "Directly by all citizens in a nationwide vote", "By district police officers", "By school management committees", "A"),
        ("Why is the Rajya Sabha called a permanent house?", "It is not dissolved as a whole; members retire in rotation", "Its members never leave office", "It cannot discuss legislation", "It meets every day without interruption", "A"),
        ("What happens to a bill after it is introduced in Parliament?", "It is considered through parliamentary procedures and may be passed by the houses", "It automatically becomes law immediately", "It is always rejected", "It is sent directly to every state court", "A"),
        ("Why does Parliament question ministers?", "To examine government decisions and demand explanations", "To appoint private company directors", "To supervise school admissions", "To select sports teams", "A"),
        ("What is the purpose of parliamentary committees?", "To examine matters in greater detail", "To replace all elected members", "To conduct national elections independently", "To manage private banks", "A"),
        ("What is the usual term of the Lok Sabha?", "Five years unless dissolved earlier", "Two years in every circumstance", "Six years without dissolution", "Ten years without elections", "A"),
        ("Which statement about the Rajya Sabha is correct?", "It represents the states and Union Territories under constitutional arrangements", "It is directly elected by all voters in the same way as Lok Sabha", "It is a court", "It is a local village body", "A"),
        ("What is the role of the Speaker in the Lok Sabha?", "To preside over proceedings and maintain order", "To command the armed forces directly", "To appoint all state governors independently", "To decide every court case", "A"),
        ("What does collective responsibility of the Union Council of Ministers mean?", "The Council of Ministers is collectively responsible to the Lok Sabha", "Every minister answers only to the President and never Parliament", "Ministers cannot be questioned", "Only civil servants are responsible to Parliament", "A"),
        ("Why is the opposition important in Parliament?", "It scrutinises government policies and presents alternative views", "It has the sole power to pass every bill", "It prevents all parliamentary debate", "It replaces the Election Commission", "A"),
        ("What is the difference between a bill and an Act?", "A bill is a proposal; an Act is a law after the required approval", "An Act is a proposal and a bill is always a court order", "They always mean unrelated things", "A bill is an election result", "A"),
        ("Why are parliamentary debates useful?", "They allow different viewpoints to be considered before decisions", "They guarantee that all proposals are accepted", "They remove the need for elections", "They prevent public accountability", "A"),
        ("What is the main purpose of the Union Budget?", "To present the government's estimated receipts and expenditure", "To announce only election candidates", "To appoint judges", "To declare school holidays", "A"),
        ("Which house has a special role in approving demands for grants?", "Lok Sabha", "Rajya Sabha alone", "Supreme Court", "State High Court", "A"),
        ("What is a Money Bill mainly concerned with?", "Specified matters such as taxation and government borrowing", "Appointment of school teachers only", "Sports regulations only", "Private family disputes", "A"),
        ("Who decides whether a bill is a Money Bill in the Lok Sabha?", "The Speaker of the Lok Sabha", "The Prime Minister alone", "The Chief Justice of India", "The Governor of every state", "A"),
        ("What is Question Hour?", "A period when members ask ministers questions", "A period when Parliament is permanently suspended", "A national voting day", "A court hearing", "A"),
        ("What is Zero Hour commonly used for?", "Raising matters of urgent public importance", "Passing every bill without discussion", "Electing the President directly", "Dissolving the Supreme Court", "A"),
        ("Why are parliamentary records important?", "They document proceedings, questions and decisions", "They replace the Constitution", "They are used only for sports results", "They prevent citizens from learning about government", "A"),
        ("What does parliamentary oversight mean?", "Parliament examines and monitors government actions", "The government controls every private conversation", "Courts conduct elections", "Local bodies make all Union laws", "A"),
        ("Why can the Lok Sabha be dissolved?", "It is not a permanent house and may be dissolved under constitutional provisions", "It is a permanent house like the Rajya Sabha", "Its members serve for life", "It is a judicial institution", "A"),
        ("What happens when the Union Council of Ministers loses the confidence of the Lok Sabha?", "It is expected to resign or follow the constitutional process", "It automatically becomes the Rajya Sabha", "The Supreme Court becomes the cabinet", "All elections are permanently cancelled", "A"),
        ("What is the purpose of an adjournment in a parliamentary sitting?", "To suspend a sitting until a later time", "To permanently abolish Parliament", "To convert a bill into a court", "To appoint all MPs for life", "A"),
        ("Why must parliamentary actions follow the Constitution?", "The Constitution establishes powers, procedures and limits", "Parliament has unlimited authority outside the Constitution", "The Constitution applies only to courts", "It removes the need for public representatives", "A"),
        ("What does representation mean in Parliament?", "Elected members speak and act on behalf of the people or states they represent", "Every citizen becomes an MP automatically", "Only civil servants vote on laws", "Courts replace all elected members", "A"),
        ("What is the purpose of a no-confidence motion in the Lok Sabha?", "To test whether the government retains the house's confidence", "To elect the President directly", "To amend every state law", "To appoint the Speaker for life", "A"),
        ("Why is the President's assent important for an ordinary bill passed by Parliament?", "It is part of the constitutional process for the bill to become law", "It replaces every stage of parliamentary consideration", "It allows the President to write all questions", "It is only a ceremonial vote by citizens", "A"),
        ("How does Parliament help protect public interests?", "By debating issues, making laws and holding the executive accountable", "By preventing public representatives from speaking", "By replacing every local government", "By ending elections", "A"),
    ],

    "Hard": [
        ("Which constitutional article provides for the composition of the Parliament of India?", "Article 79", "Article 32", "Article 110", "Article 356", "A"),
        ("Which article defines a Money Bill?", "Article 110", "Article 21", "Article 72", "Article 280", "A"),
        ("Which article deals with the annual financial statement?", "Article 112", "Article 14", "Article 148", "Article 324", "A"),
        ("Under Article 75, the Union Council of Ministers is collectively responsible to which house?", "Lok Sabha", "Rajya Sabha", "Supreme Court", "State Legislative Council", "A"),
        ("What is the maximum interval permitted between two sessions of Parliament under Article 85?", "Six months", "Three months", "One year", "Two years", "A"),
        ("Which article provides for a joint sitting of both houses in certain legislative deadlocks?", "Article 108", "Article 123", "Article 226", "Article 368", "A"),
        ("Who normally presides over a joint sitting of Parliament?", "Speaker of the Lok Sabha", "President of India", "Chairperson of the Election Commission", "Chief Justice of India", "A"),
        ("Which type of bill cannot be introduced in the Rajya Sabha?", "Money Bill", "Ordinary bill", "Constitution Amendment Bill", "Private Member's Bill on any subject", "A"),
        ("For how long can the Rajya Sabha delay a Money Bill?", "Up to 14 days", "Up to six months", "Up to one year", "It can reject it permanently", "A"),
        ("Who has the final constitutional authority to certify a bill as a Money Bill in the Lok Sabha?", "Speaker of the Lok Sabha", "President of India", "Prime Minister", "Chairperson of the Rajya Sabha", "A"),
        ("What proportion of Rajya Sabha members retire every two years?", "Approximately one-third", "All members", "One-half", "No members ever retire", "A"),
        ("What is the minimum age to become a Lok Sabha member?", "25 years", "18 years", "21 years", "30 years", "A"),
        ("What is the minimum age to become a Rajya Sabha member?", "30 years", "18 years", "21 years", "25 years", "A"),
        ("Which constitutional article provides for the Speaker and Deputy Speaker of the Lok Sabha?", "Article 93", "Article 74", "Article 110", "Article 148", "A"),
        ("Which article deals with the privileges and powers of Parliament and its members?", "Article 105", "Article 19", "Article 40", "Article 280", "A"),
        ("Which article provides for the President's special address to Parliament?", "Article 87", "Article 14", "Article 51A", "Article 300A", "A"),
        ("Which article gives Parliament the power to legislate on matters in the Union List?", "Article 246 read with the Seventh Schedule", "Article 21 only", "Article 32 only", "Article 51A only", "A"),
        ("What majority is generally required in each house to pass a Constitution Amendment Bill under Article 368?", "A majority of the total membership and a two-thirds majority of members present and voting", "A simple majority of members present in every case", "Unanimous approval by all citizens", "Approval only by the Lok Sabha Speaker", "A"),
        ("Which constitutional article governs the procedure for passing ordinary bills?", "Articles 107 and 108, as applicable", "Article 17 only", "Article 40 only", "Article 352 only", "A"),
        ("What is the effect of a no-confidence motion being passed in the Lok Sabha?", "The Council of Ministers must resign because it has lost the house's confidence", "The Rajya Sabha is automatically dissolved", "The President's term ends immediately", "The Supreme Court is dissolved", "A"),
        ("Which house has the exclusive power to vote on demands for grants?", "Lok Sabha", "Rajya Sabha", "Both houses jointly in all cases", "Supreme Court", "A"),
        ("Which article deals with the procedure for the President's assent to bills?", "Article 111", "Article 19", "Article 72", "Article 324", "A"),
        ("What is the constitutional role of the Rajya Sabha under Article 249?", "It may authorise Parliament to legislate on a State List matter in the national interest under specified conditions", "It can permanently abolish state legislatures", "It appoints every Chief Minister", "It conducts all local elections", "A"),
        ("Under Article 312, what can the Rajya Sabha authorise by a special resolution?", "Creation of one or more All India Services", "Abolition of the Constitution", "Removal of every High Court", "Cancellation of the voting age", "A"),
        ("What special majority is required for a Rajya Sabha resolution under Article 249?", "Two-thirds of members present and voting", "A simple majority of the total population", "Unanimous approval of both houses", "One-third of Lok Sabha members", "A"),
        ("Which article permits the President to promulgate ordinances when Parliament is not in session, subject to constitutional conditions?", "Article 123", "Article 110", "Article 148", "Article 280", "A"),
        ("What is the constitutional purpose of parliamentary privileges?", "To enable Parliament and its members to perform their functions effectively, subject to constitutional law", "To place MPs above all criminal law in every situation", "To remove judicial review from the entire country", "To permit members to ignore all parliamentary rules", "A"),
        ("Which statement about a joint sitting is correct?", "It is not available for Money Bills or Constitution Amendment Bills", "It is mandatory for every bill", "It is chaired by the President in every case", "It can amend the Constitution without the required majority", "A"),
        ("Which article deals with the election of the Speaker and Deputy Speaker of the Lok Sabha?", "Article 93", "Article 80", "Article 123", "Article 280", "A"),
        ("Why is parliamentary control over public finance considered essential?", "It ensures that taxation and public expenditure are subject to representative scrutiny and constitutional procedures", "It allows spending without authorisation", "It removes the need for a budget", "It transfers all financial authority to private companies", "A"),
    ],
}


def main():
    db = SessionLocal()

    try:
        lesson = (
            db.query(Lesson)
            .filter(
                Lesson.title == "The Indian Parliament",
                Lesson.topic == "Social Science"
            )
            .first()
        )

        if not lesson:
            print("ERROR: The Indian Parliament lesson was not found.")
            print("Check the lesson title and topic in your database.")
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

            existing_texts = {
                q.question.strip().lower() for q in existing
            }

            if len(existing) >= 30:
                print(f"{difficulty}: already has {len(existing)} questions; skipped.")
                continue

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