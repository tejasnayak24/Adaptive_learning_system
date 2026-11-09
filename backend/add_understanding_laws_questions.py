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
        ("What is a law?", "A rule recognised and enforced by the legal system", "A personal wish", "A school timetable", "A sports score", "A"),
        ("Why do societies need laws?", "To maintain order and protect people's rights", "To prevent all public discussion", "To allow everyone to act without limits", "To replace education", "A"),
        ("Who makes laws for the whole country at the Union level?", "Parliament", "A village school", "A private company", "A district hospital", "A"),
        ("What is the Constitution?", "The supreme legal framework of a country", "A list of advertisements", "A sports rulebook", "A private diary", "A"),
        ("What can happen when a person breaks a law?", "Legal consequences may follow", "They automatically become a judge", "The Constitution disappears", "No legal process is possible", "A"),
        ("Who interprets laws when legal disputes arise?", "Courts", "Sports clubs", "Private shops", "School teams", "A"),
        ("What does equality before the law mean?", "The law applies equally without unlawful discrimination", "Only wealthy people must follow the law", "Officials can ignore every law", "Different people have no legal rights", "A"),
        ("What is a fundamental right?", "A basic right protected by the Constitution", "A private business rule", "A school subject", "A type of tax", "A"),
        ("What is the purpose of traffic laws?", "To improve road safety and regulate traffic", "To organise school examinations", "To choose political parties", "To set food prices", "A"),
        ("What is a legal punishment?", "A consequence imposed through lawful procedures for an offence", "Any action taken because of a rumour", "A personal disagreement", "A school timetable change", "A"),
        ("Can laws be changed?", "Yes, through the applicable legal and constitutional procedures", "No law can ever change", "Only private companies can change national laws", "Any person can change a law by announcing it", "A"),
        ("What is the rule of law?", "Everyone, including public officials, is subject to the law", "Only ordinary citizens must follow laws", "Powerful people are always above the law", "Courts do not need to follow the Constitution", "A"),
        ("What is an offence?", "An act or omission that violates criminal law", "A legal school holiday", "A parliamentary building", "A type of election", "A"),
        ("What is a court?", "An institution that resolves legal cases", "A private shopping centre", "A sports ground", "A transport service", "A"),
        ("What is the purpose of a written law?", "To state legal rules in an accessible and formal manner", "To replace every court", "To prevent people from learning their rights", "To record only personal opinions", "A"),
        ("What is a citizen's responsibility regarding laws?", "To obey applicable laws and respect others' rights", "To ignore every public rule", "To decide court cases personally", "To change the Constitution alone", "A"),
        ("What does the word 'illegal' mean?", "Contrary to the law", "Required by every school", "Always popular", "Related only to sports", "A"),
        ("What is a legal right?", "An entitlement recognised or protected by law", "A personal preference with no legal recognition", "A private rumour", "A sports award", "A"),
        ("What is discrimination?", "Unfair treatment based on characteristics or identity", "Equal treatment in every situation", "Following a lawful safety rule", "Participating in an election", "A"),
        ("Why should citizens know their rights?", "To understand and protect their legal entitlements", "To avoid all responsibilities", "To replace judges", "To ignore public institutions", "A"),
        ("What is the role of the police in enforcing criminal law?", "To investigate offences and maintain law and order within the law", "To make every final court judgment", "To amend the Constitution alone", "To elect Members of Parliament", "A"),
        ("What is a law court's judgment?", "A decision made by a court in a case", "A proposed school rule", "A campaign poster", "A private advertisement", "A"),
        ("What is a bill?", "A proposal for a law", "A law enforcement officer", "A court sentence in every case", "A voting machine", "A"),
        ("What is an Act?", "A law enacted through the required legislative process", "A personal opinion", "A court building", "A private invitation", "A"),
        ("What is the purpose of consumer protection laws?", "To protect consumers against specified unfair practices and violations", "To prevent consumers from making complaints", "To abolish all markets", "To control school sports", "A"),
        ("What do environmental laws aim to protect?", "The environment and public interests through legal standards", "Only private advertisements", "Only election campaigns", "Only school buildings", "A"),
        ("What does a witness do in a court case?", "Provides relevant information or testimony", "Automatically decides the case", "Writes every law", "Appoints the judge", "A"),
        ("What is legal evidence?", "Information considered under legal rules to establish facts", "A rumour that must always be accepted", "A personal guess", "An election slogan", "A"),
        ("Why are laws published or made publicly accessible?", "So people can learn about the rules that apply to them", "So nobody can understand legal rules", "To prevent legal accountability", "To replace all public institutions", "A"),
        ("What should a person do if they believe their legal rights have been violated?", "Seek appropriate legal advice or approach the relevant authority or court", "Punish the other person without a process", "Ignore every available remedy", "Change the law personally", "A"),
    ],

    "Medium": [
        ("Why should laws apply equally to all people?", "Equality before the law supports fairness and limits arbitrary treatment", "It gives officials unlimited power", "It prevents courts from hearing disputes", "It means every case must have the same outcome regardless of facts", "A"),
        ("How does the Constitution limit the power of lawmakers?", "It establishes constitutional rules, rights and limits that laws must respect", "It allows lawmakers to ignore every right", "It gives private companies the power to repeal laws", "It removes the judiciary", "A"),
        ("What is the difference between a bill and an Act?", "A bill is a proposal; an Act is legislation enacted through the required process", "A bill is always a court judgment", "An Act is always a proposed law", "They are names for election candidates", "A"),
        ("Why are laws debated before being passed?", "Debate helps representatives examine proposals and consider different viewpoints", "Debate guarantees every proposal is rejected", "Debate replaces the Constitution", "Debate removes the need for public representatives", "A"),
        ("What is the purpose of judicial review?", "To allow courts to examine whether laws or government actions are constitutionally valid", "To let courts conduct all elections", "To allow judges to ignore the Constitution", "To replace every legislature", "A"),
        ("What does due process or fair legal procedure seek to ensure?", "People receive procedures required by law before decisions affecting them are made", "Every accused person is automatically guilty", "Authorities can impose punishment without any legal basis", "Evidence is never considered", "A"),
        ("Why is the right to constitutional remedies important?", "It enables people to approach appropriate courts to enforce fundamental rights", "It prevents courts from protecting rights", "It permits citizens to ignore all laws", "It removes constitutional safeguards", "A"),
        ("How can a law protect vulnerable groups?", "By prohibiting specified forms of exploitation or discrimination and providing remedies", "By denying those groups access to courts", "By making their rights unenforceable", "By exempting every offender from legal consequences", "A"),
        ("Why should laws be clear and publicly available?", "People need to understand legal requirements and how to comply with them", "Laws should be understandable only to officials", "Public access prevents enforcement", "It removes the need for courts", "A"),
        ("What is the purpose of consumer protection legislation?", "To provide safeguards and remedies against specified unfair trade practices", "To prevent customers from seeking refunds under any circumstances", "To remove all product standards", "To abolish legal contracts", "A"),
        ("How do environmental laws help society?", "They establish standards and responsibilities for protecting environmental quality", "They guarantee that pollution can never occur", "They replace all scientific research", "They apply only to private homes", "A"),
        ("What is the purpose of labour laws?", "To regulate employment relationships and protect applicable worker rights", "To abolish every workplace safety standard", "To prevent workers from knowing their rights", "To regulate only sporting events", "A"),
        ("What is the difference between civil and criminal law?", "Civil law commonly addresses private disputes, while criminal law addresses offences prosecuted under criminal law", "Civil law always involves imprisonment", "Criminal law only deals with property contracts", "They are always identical", "A"),
        ("Why is an independent judiciary necessary for enforcing laws?", "It supports impartial interpretation and application of the law", "It allows judges to make decisions based on political pressure", "It removes the need for evidence", "It means judges can disregard all legal rules", "A"),
        ("What is legal aid intended to do?", "Help eligible people access legal services when they cannot afford them", "Guarantee victory to every applicant", "Replace all judicial proceedings", "Prevent people from seeking legal advice", "A"),
        ("Why are laws against corruption important?", "They provide legal mechanisms to address specified corrupt practices and protect public trust", "They make all public spending secret", "They prevent any investigation of officials", "They remove accountability", "A"),
        ("What is the purpose of a contract law?", "To establish rules governing agreements and available remedies", "To regulate only elections", "To replace all criminal law", "To make every verbal statement a criminal offence", "A"),
        ("Why do legal systems provide an appeal process?", "It allows eligible parties to seek review of a decision by a higher court", "It guarantees every decision will be reversed", "It replaces all trials with elections", "It allows any person to change a judgment without authority", "A"),
        ("What does presumption of innocence mean in criminal proceedings?", "An accused person is treated as innocent unless guilt is established according to law", "Every accusation is proof of guilt", "Evidence is never necessary", "Only certain social groups receive a fair trial", "A"),
        ("Why are laws against domestic violence important?", "They provide legal protections and remedies against covered forms of abuse", "They prevent victims from seeking help", "They make all family disputes criminal automatically", "They remove access to courts", "A"),
        ("How can laws support public health?", "They can establish safety standards and regulate public-health risks", "They guarantee nobody will ever become ill", "They replace all medical professionals", "They prevent public-health information from being shared", "A"),
        ("What is the purpose of the Right to Information framework in India?", "To enable access to information held by public authorities, subject to legal provisions and exemptions", "To make every private conversation public", "To abolish all government records", "To prevent citizens from asking public authorities questions", "A"),
        ("Why are laws sometimes amended?", "To respond to changing circumstances, problems or policy needs through proper procedures", "Because every law automatically expires each month", "To eliminate the Constitution", "Because courts cannot interpret laws", "A"),
        ("What is delegated legislation?", "Rules or regulations made by an authorised body under powers granted by legislation", "A law made by any person without authority", "A court judgment in every case", "A referendum conducted by citizens", "A"),
        ("What is the purpose of an enforcement agency?", "To carry out duties assigned by law, such as investigating or enforcing legal requirements", "To create unlimited powers for itself", "To replace the legislature and courts", "To decide every constitutional question", "A"),
        ("Why should penalties for offences be imposed through lawful procedures?", "To protect fairness and prevent arbitrary punishment", "To allow punishment based on rumours", "To remove the right to a hearing in all cases", "To ensure every offence receives an identical sentence regardless of law", "A"),
        ("What is the relationship between fundamental rights and ordinary laws?", "Ordinary laws must comply with applicable constitutional protections", "Ordinary laws always override the Constitution", "Fundamental rights apply only to elected representatives", "Courts cannot examine conflicts between laws and rights", "A"),
        ("How can citizens participate in improving laws?", "Through lawful democratic processes such as consultation, representation and advocacy", "By ignoring all legal procedures", "By issuing binding judgments themselves", "By replacing Parliament individually", "A"),
        ("Why is transparency in lawmaking valuable?", "It helps people understand proposals and scrutinise decisions", "It prevents representatives from discussing legislation", "It makes all laws secret", "It removes public accountability", "A"),
        ("What is the purpose of a legal remedy?", "To provide relief or address a legal violation through an available legal process", "To guarantee success in every dispute", "To replace all laws", "To punish a person without investigation", "A"),
    ],

    "Hard": [
        ("Which article of the Indian Constitution guarantees equality before the law and equal protection of the laws?", "Article 14", "Article 19", "Article 32", "Article 51A", "A"),
        ("Which article prohibits discrimination by the State on specified grounds?", "Article 15", "Article 21", "Article 40", "Article 110", "A"),
        ("Which article guarantees equality of opportunity in public employment?", "Article 16", "Article 25", "Article 32", "Article 51A", "A"),
        ("Which article abolishes untouchability?", "Article 17", "Article 19", "Article 22", "Article 30", "A"),
        ("Which article protects life and personal liberty?", "Article 21", "Article 14", "Article 40", "Article 110", "A"),
        ("Which article provides the right to constitutional remedies for fundamental rights?", "Article 32", "Article 51A", "Article 80", "Article 280", "A"),
        ("Which article gives High Courts power to issue writs?", "Article 226", "Article 124", "Article 110", "Article 360", "A"),
        ("Which article defines the procedure for passing Money Bills?", "Article 110", "Article 21", "Article 32", "Article 148", "A"),
        ("Which article establishes that laws inconsistent with fundamental rights are void to the extent of inconsistency?", "Article 13", "Article 40", "Article 75", "Article 280", "A"),
        ("Which article protects certain rights regarding freedom of speech and other specified freedoms, subject to constitutional restrictions?", "Article 19", "Article 14", "Article 32", "Article 51A", "A"),
        ("What is the basic-structure doctrine?", "Parliament's amendment power cannot destroy the Constitution's basic structure", "Parliament can remove every constitutional limit", "Courts must approve every ordinary law before introduction", "Fundamental rights cannot be interpreted by courts", "A"),
        ("What is the principle of natural justice commonly intended to ensure?", "Fair decision-making, including an opportunity to be heard where required", "Punishment without hearing", "Decisions based solely on personal bias", "Automatic acceptance of every allegation", "A"),
        ("What does the principle 'audi alteram partem' mean?", "Hear the other side", "No one is above the law", "Let the buyer beware", "The law does not concern itself with trivial matters", "A"),
        ("What does 'nemo judex in causa sua' mean?", "No one should be a judge in their own cause", "Hear the other side", "Ignorance of law is always a defence", "A contract must always be written", "A"),
        ("What is the principle of proportionality in public law?", "A measure should not impose an excessive burden relative to its legitimate aim", "Every government action must have the same result", "All restrictions are automatically valid", "Legal review is never permitted", "A"),
        ("What is the purpose of delegated legislation?", "To allow authorised bodies to make detailed rules within powers granted by a parent law", "To let anyone create binding laws without authority", "To abolish parliamentary legislation", "To prevent courts from reviewing legality", "A"),
        ("What is the ultra vires doctrine?", "An action is beyond the legal powers of the body taking it", "An action is always constitutionally valid", "A law automatically expires after one day", "A court has no power to review public action", "A"),
        ("What does judicial review of administrative action examine?", "Whether public authorities acted lawfully and within the limits of their powers", "Whether every policy is popular", "Whether every official should be elected", "Whether all administrative decisions must be identical", "A"),
        ("What is the purpose of a writ of mandamus?", "To direct a public authority to perform a public or legal duty when legally appropriate", "To release a person from unlawful detention in every case", "To question a person's authority to hold public office", "To stop every parliamentary debate", "A"),
        ("What is the primary purpose of habeas corpus?", "To provide a remedy against unlawful detention", "To appoint public prosecutors", "To approve the national budget", "To invalidate every contract", "A"),
        ("What is the distinction between a void law and a voidable legal act in general legal usage?", "A void law has no legal effect to the relevant extent, while a voidable act remains effective unless set aside under applicable rules", "Both terms always mean that a law is automatically valid", "A void law can only be a school rule", "A voidable act can never be challenged", "A"),
        ("Why must criminal offences and penalties have a legal basis?", "The principle of legality limits arbitrary punishment and requires offences and penalties to be established by law", "Officials can create offences after the act and punish anyone without limits", "Evidence is never needed", "Courts cannot interpret criminal legislation", "A"),
        ("What does the principle against retrospective criminal punishment generally protect?", "People from being convicted for an act that was not an offence when committed, subject to constitutional provisions", "All people from any future legal change", "Every contract from being enforced", "Officials from judicial review", "A"),
        ("Which article protects against conviction for offences except in accordance with law and contains safeguards against specified forms of retrospective criminal punishment and double jeopardy?", "Article 20", "Article 14", "Article 40", "Article 110", "A"),
        ("Which article provides safeguards relating to arrest and detention?", "Article 22", "Article 16", "Article 30", "Article 280", "A"),
        ("What does Article 39A of the Indian Constitution promote?", "Equal justice and free legal aid", "Abolition of the Supreme Court", "Direct election of all judges", "Abolition of fundamental rights", "A"),
        ("What is the significance of the doctrine of precedent in India?", "The law declared by the Supreme Court is binding on all courts under Article 141", "Every statement by any official binds all courts", "Precedents replace the written Constitution", "Only private contracts can create precedents", "A"),
        ("How does the separation of powers support the rule of law?", "It distributes governmental functions and helps prevent excessive concentration of power", "It gives one branch unlimited authority", "It eliminates constitutional accountability", "It prevents courts from hearing legal disputes", "A"),
        ("What is the relationship between Article 13 and judicial review?", "Article 13 provides that laws inconsistent with fundamental rights are void to the extent of inconsistency, supporting constitutional scrutiny", "Article 13 abolishes all fundamental rights", "Article 13 prevents courts from considering constitutional questions", "Article 13 applies only to private school rules", "A"),
        ("Why is access to justice considered a rule-of-law requirement?", "Rights need effective and fair procedures through which violations can be challenged and remedies obtained", "Only wealthy people should be able to enforce rights", "Legal disputes should never be heard", "Public authorities should be immune from every legal challenge", "A"),
    ],
}


def main():
    db = SessionLocal()

    try:
        lesson = (
            db.query(Lesson)
            .filter(
                Lesson.title == "Understanding Laws",
                Lesson.topic == "Social Science"
            )
            .first()
        )

        if not lesson:
            print("ERROR: Understanding Laws lesson was not found.")
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