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
        ("What are fundamental rights?", "Basic rights protected by the Constitution", "Private company rules", "School examination rules", "Election slogans", "A"),
        ("Where are the fundamental rights of Indian citizens mainly provided?", "Part III of the Constitution", "Part I only", "Part V only", "Part IX only", "A"),
        ("What are fundamental duties?", "Responsibilities of citizens recognised by the Constitution", "Powers of private companies", "Court punishments", "Election results", "A"),
        ("Which part of the Indian Constitution contains fundamental duties?", "Part IVA", "Part II", "Part III", "Part VI", "A"),
        ("Which article lists the fundamental duties?", "Article 51A", "Article 14", "Article 21", "Article 110", "A"),
        ("Which right guarantees equality before the law?", "Right to Equality", "Right against Exploitation", "Right to Freedom of Religion", "Cultural and Educational Rights", "A"),
        ("Which right protects certain freedoms such as speech and expression, subject to constitutional restrictions?", "Right to Freedom", "Right to Property as a fundamental right", "Right against Exploitation", "Right to Constitutional Remedies only", "A"),
        ("Which right prohibits human trafficking and forced labour?", "Right against Exploitation", "Right to Equality only", "Right to Education only", "Cultural Rights only", "A"),
        ("Which right protects freedom of conscience and religion, subject to constitutional provisions?", "Right to Freedom of Religion", "Right to Property", "Right to Vote", "Right to Employment in every case", "A"),
        ("Which rights help protect the language and culture of communities?", "Cultural and Educational Rights", "Right against Exploitation only", "Right to Property only", "Right to Information only", "A"),
        ("Which right allows people to approach courts to enforce fundamental rights?", "Right to Constitutional Remedies", "Right to Property", "Right to Work in every circumstance", "Right to Travel Abroad in every circumstance", "A"),
        ("What is one fundamental duty of Indian citizens?", "To respect the Constitution and its ideals", "To ignore national laws", "To damage public property", "To prevent others from voting", "A"),
        ("Which national symbols are citizens expected to respect under Article 51A?", "The National Flag and the National Anthem", "Every private company logo", "All foreign flags equally as a constitutional duty", "Only state sports team logos", "A"),
        ("What should citizens protect according to a fundamental duty?", "The natural environment", "Pollution of rivers", "Destruction of forests", "Damage to public facilities", "A"),
        ("Which duty encourages citizens to develop scientific temper?", "Developing scientific temper, humanism and a spirit of inquiry", "Rejecting all investigation", "Ignoring evidence", "Preventing education", "A"),
        ("What does the Constitution say about protecting public property?", "Citizens should safeguard public property and abjure violence", "Citizens should destroy public property", "Only judges must protect public property", "Public property has no value", "A"),
        ("Which right protects children aged 6 to 14 through free and compulsory education?", "Right to Education", "Right to Property", "Right to Vote", "Right to Privacy in every circumstance", "A"),
        ("What is equality before the law intended to promote?", "Fair and equal legal treatment", "Special legal immunity for powerful people", "Different laws based only on wealth", "The removal of courts", "A"),
        ("Can fundamental rights have reasonable constitutional restrictions?", "Yes, certain rights are subject to constitutionally permitted restrictions", "No right has any limits in any situation", "Only private companies decide restrictions", "Restrictions never need a legal basis", "A"),
        ("Who has a duty to protect the unity and integrity of India?", "Citizens, as stated in Article 51A", "Only private businesses", "Only school principals", "Only sports organisations", "A"),
        ("What is the purpose of fundamental duties?", "To encourage responsible citizenship", "To remove every citizen's right", "To replace the Constitution", "To abolish elections", "A"),
        ("Which institution can provide remedies when fundamental rights are violated?", "Appropriate courts", "Private shops", "Sports clubs", "School libraries only", "A"),
        ("What does the right against exploitation seek to prevent?", "Practices such as human trafficking and forced labour", "All forms of education", "All religious practice", "All cultural activities", "A"),
        ("What does freedom of religion protect?", "Religious freedom subject to constitutional provisions", "The right to force everyone to follow one religion", "Freedom from all laws", "The power to cancel other people's rights", "A"),
        ("What is one purpose of cultural and educational rights?", "To protect specified cultural and educational interests of minorities", "To abolish all schools", "To prevent minority communities from preserving their language", "To replace courts with private groups", "A"),
        ("Which duty encourages parents or guardians to provide educational opportunities to children aged 6 to 14?", "The duty under Article 51A(k)", "The duty under Article 110", "The duty under Article 148", "The duty under Article 280", "A"),
        ("What does fraternity encourage?", "A sense of brotherhood and mutual respect among people", "Discrimination between citizens", "Violence against communities", "Disrespect for others", "A"),
        ("Which of these is a responsible civic action?", "Following laws and respecting others' rights", "Damaging public property", "Spreading discrimination", "Ignoring every public responsibility", "A"),
        ("Are fundamental duties important for democracy?", "Yes, they encourage citizens to act responsibly", "No, they require citizens to break laws", "They replace all fundamental rights", "They abolish representative government", "A"),
        ("What is the relationship between rights and duties?", "Rights protect freedoms, while duties encourage responsible conduct", "Rights and duties always cancel each other", "Duties remove all constitutional protections", "Rights apply only to government officials", "A"),
    ],

    "Medium": [
        ("Why are fundamental rights important in a democracy?", "They protect essential freedoms and help limit arbitrary state action", "They give the government unlimited power", "They eliminate the need for courts", "They prevent citizens from expressing opinions", "A"),
        ("What is the purpose of Article 14?", "To guarantee equality before the law and equal protection of the laws", "To establish the Election Commission", "To define Money Bills", "To establish the office of the President", "A"),
        ("Which statement about Article 19 is correct?", "It protects specified freedoms subject to constitutional restrictions", "It guarantees unlimited freedom without any constitutional restrictions", "It deals only with property ownership", "It lists the fundamental duties", "A"),
        ("What does Article 21 protect?", "Life and personal liberty, except according to procedure established by law", "The right to become Prime Minister", "The power to make laws", "The right to ignore court orders", "A"),
        ("What is the significance of Article 21A?", "It provides free and compulsory education for children aged 6 to 14", "It establishes the Supreme Court", "It defines the Union Budget", "It abolishes all educational institutions", "A"),
        ("Why is Article 32 important?", "It provides a constitutional remedy through the Supreme Court for enforcement of fundamental rights", "It establishes local government", "It regulates all private contracts", "It abolishes judicial review", "A"),
        ("How does Article 17 promote equality?", "It abolishes untouchability and forbids its practice", "It establishes the Rajya Sabha", "It creates the office of Governor", "It regulates the national budget", "A"),
        ("What is the purpose of Article 23?", "It prohibits human trafficking, begar and other similar forms of forced labour", "It establishes Parliament", "It guarantees a government job to everyone", "It regulates elections", "A"),
        ("What does Article 25 protect?", "Freedom of conscience and the right to profess, practise and propagate religion, subject to constitutional limits", "Unlimited authority to force religious conversion", "The right to ignore all public-order laws", "The right to make religious laws override the Constitution", "A"),
        ("Why are cultural and educational rights important?", "They help protect specified cultural, linguistic and educational interests, including those of minorities", "They prevent communities from preserving their culture", "They remove every educational right", "They replace all state governments", "A"),
        ("What is the main purpose of fundamental duties?", "To encourage citizens to respect constitutional values and fulfil civic responsibilities", "To give citizens unlimited government powers", "To replace all enforceable rights", "To allow people to ignore public property", "A"),
        ("Which amendment added the list of fundamental duties to the Constitution?", "The 42nd Constitutional Amendment Act, 1976", "The 1st Constitutional Amendment Act, 1951", "The 44th Constitutional Amendment Act, 1978", "The 73rd Constitutional Amendment Act, 1992", "A"),
        ("Which amendment added the duty concerning educational opportunities for children aged 6 to 14?", "The 86th Constitutional Amendment Act, 2002", "The 42nd Constitutional Amendment Act, 1976", "The 52nd Constitutional Amendment Act, 1985", "The 101st Constitutional Amendment Act, 2016", "A"),
        ("Are all fundamental duties directly enforceable by courts in the same way as fundamental rights?", "No, their direct enforceability differs; some laws may give effect to them", "Yes, every duty automatically creates an identical criminal penalty", "No duty is mentioned in the Constitution", "Yes, every duty overrides fundamental rights", "A"),
        ("How can fundamental duties support environmental protection?", "They encourage citizens to protect and improve the natural environment", "They require citizens to pollute rivers", "They prevent environmental laws from being passed", "They abolish all wildlife protection", "A"),
        ("What does the duty to develop scientific temper encourage?", "Reasoning, inquiry and evidence-based thinking", "Accepting every claim without examination", "Rejecting scientific research", "Preventing public education", "A"),
        ("What does the duty to safeguard public property promote?", "Responsible use and protection of shared public resources", "Damage to public buildings", "Private ownership of all public roads", "The abolition of public services", "A"),
        ("Why is the right to constitutional remedies described as important to rights protection?", "It gives people a legal route to seek enforcement of fundamental rights", "It prevents courts from hearing rights cases", "It guarantees success in every case", "It replaces every other constitutional provision", "A"),
        ("What is the difference between a fundamental right and a fundamental duty?", "A right protects an entitlement or freedom; a duty identifies a civic responsibility", "A right is always a punishment and a duty is always a court", "Both mean only a government tax", "A duty automatically removes all rights", "A"),
        ("Can the State place restrictions on freedom of speech and expression?", "Yes, Article 19 permits specified reasonable restrictions on constitutional grounds", "No restriction is ever permitted", "Only private companies may impose constitutional restrictions", "Any restriction is valid without legal grounds", "A"),
        ("What is the purpose of the prohibition of discrimination under Article 15?", "To prohibit State discrimination on specified grounds, subject to constitutional provisions", "To abolish equality before the law", "To prohibit all educational opportunities", "To establish the Supreme Court", "A"),
        ("How does Article 16 support fairness?", "It guarantees equality of opportunity in matters of public employment, subject to constitutional provisions", "It guarantees every citizen a particular government job", "It prevents public employment from being regulated", "It applies only to private sports clubs", "A"),
        ("What does Article 20 protect against?", "Specified protections in criminal proceedings, including certain forms of retrospective punishment and double jeopardy", "All taxation", "All civil contracts", "Every election dispute", "A"),
        ("What safeguards are associated with Article 22?", "Certain protections relating to arrest and detention, subject to its provisions and exceptions", "Unlimited freedom to detain anyone without legal safeguards", "A guarantee of employment", "The right to amend the Constitution individually", "A"),
        ("Why is equality before the law essential to the rule of law?", "It limits arbitrary privilege and supports equal legal accountability", "It places officials permanently above the law", "It prevents courts from hearing cases", "It makes legal rules optional for wealthy people", "A"),
        ("What is the relationship between fundamental rights and the Constitution?", "Fundamental rights are constitutionally protected and interpreted within the constitutional framework", "They are private rules created by companies", "They can never be considered by courts", "They apply only to elected representatives", "A"),
        ("How can citizens fulfil their duty to promote harmony?", "By respecting diversity and avoiding practices that undermine dignity and unity", "By encouraging discrimination", "By damaging public property", "By denying other communities their rights", "A"),
        ("What is the significance of respecting the National Flag and National Anthem as a fundamental duty?", "It expresses respect for constitutional values and national symbols", "It removes the need to obey laws", "It gives one citizen authority over all others", "It replaces the Constitution", "A"),
        ("Why should fundamental duties be taught alongside fundamental rights?", "To promote both awareness of rights and responsible citizenship", "To convince citizens that they have no rights", "To eliminate civic education", "To replace all laws with personal opinions", "A"),
        ("What should happen when a law conflicts with a fundamental right?", "A competent court may examine its constitutional validity under applicable law", "The law always overrides the Constitution", "The conflict must never be examined", "A private company decides the constitutional question", "A"),
    ],

    "Hard": [
        ("Which part of the Indian Constitution contains fundamental rights?", "Part III", "Part II", "Part IVA", "Part V", "A"),
        ("Which articles cover fundamental rights in Part III?", "Articles 12 to 35", "Articles 36 to 51", "Articles 51A only", "Articles 79 to 122", "A"),
        ("Which article defines the State for the purposes of Part III?", "Article 12", "Article 14", "Article 21", "Article 32", "A"),
        ("Which article declares laws inconsistent with fundamental rights void to the extent of inconsistency?", "Article 13", "Article 19", "Article 40", "Article 110", "A"),
        ("Which article guarantees equality before the law and equal protection of the laws?", "Article 14", "Article 17", "Article 23", "Article 29", "A"),
        ("Which article abolishes untouchability?", "Article 17", "Article 15", "Article 20", "Article 25", "A"),
        ("Which article prohibits trafficking in human beings and forced labour?", "Article 23", "Article 16", "Article 21A", "Article 30", "A"),
        ("Which article prohibits employment of children below 14 years in factories, mines and other hazardous employment covered by the provision?", "Article 24", "Article 14", "Article 25", "Article 32", "A"),
        ("Which article protects freedom of conscience and religion?", "Article 25", "Article 19", "Article 21A", "Article 51A", "A"),
        ("Which article protects the right of minorities to establish and administer educational institutions?", "Article 30", "Article 17", "Article 23", "Article 40", "A"),
        ("Which article empowers the Supreme Court to issue writs for enforcing fundamental rights?", "Article 32", "Article 14", "Article 51A", "Article 110", "A"),
        ("Which article empowers High Courts to issue writs for fundamental rights and other legal purposes within its scope?", "Article 226", "Article 124", "Article 143", "Article 280", "A"),
        ("Which amendment introduced fundamental duties into the Constitution?", "42nd Amendment Act, 1976", "1st Amendment Act, 1951", "44th Amendment Act, 1978", "73rd Amendment Act, 1992", "A"),
        ("Which article contains the fundamental duties?", "Article 51A", "Article 32", "Article 110", "Article 226", "A"),
        ("Which amendment added the duty of parents or guardians to provide educational opportunities for children aged 6 to 14?", "86th Amendment Act, 2002", "42nd Amendment Act, 1976", "52nd Amendment Act, 1985", "101st Amendment Act, 2016", "A"),
        ("How many fundamental duties are currently listed in Article 51A?", "Eleven", "Seven", "Ten", "Fourteen", "A"),
        ("Which article provides for free and compulsory education for children aged 6 to 14?", "Article 21A", "Article 19", "Article 32", "Article 51A", "A"),
        ("Which article protects against conviction for offences in specified circumstances, including certain retrospective criminal laws?", "Article 20", "Article 14", "Article 25", "Article 30", "A"),
        ("Which article protects life and personal liberty?", "Article 21", "Article 16", "Article 23", "Article 29", "A"),
        ("Which article protects against discrimination by the State on specified grounds?", "Article 15", "Article 17", "Article 24", "Article 32", "A"),
        ("Which article guarantees equality of opportunity in public employment?", "Article 16", "Article 18", "Article 21A", "Article 30", "A"),
        ("Which article protects specified freedoms, including speech and expression, subject to constitutional restrictions?", "Article 19", "Article 20", "Article 23", "Article 51A", "A"),
        ("Which article contains provisions relating to protection against arrest and detention?", "Article 22", "Article 14", "Article 17", "Article 29", "A"),
        ("Which article protects the interests of sections of citizens regarding language, script or culture?", "Article 29", "Article 16", "Article 21A", "Article 40", "A"),
        ("Which article gives minorities the right to establish and administer educational institutions of their choice?", "Article 30", "Article 14", "Article 19", "Article 23", "A"),
        ("Which article is associated with the constitutional right to property as a legal right rather than a fundamental right?", "Article 300A", "Article 21A", "Article 32", "Article 51A", "A"),
        ("Which article allows Parliament to modify the application of fundamental rights to armed forces and certain other services to ensure proper discharge of duties?", "Article 33", "Article 14", "Article 19", "Article 226", "A"),
        ("Which article provides for restrictions on fundamental rights while martial law is in force in an area, as specified?", "Article 34", "Article 16", "Article 21A", "Article 51A", "A"),
        ("Which article empowers Parliament to legislate on matters related to certain provisions of Part III as specified in the Constitution?", "Article 35", "Article 12", "Article 17", "Article 29", "A"),
        ("What is the constitutional relationship between fundamental rights and fundamental duties?", "Rights protect constitutional freedoms, while duties encourage responsible citizenship; both are interpreted within the Constitution", "Fundamental duties automatically cancel fundamental rights", "Fundamental rights apply only to public officials", "Fundamental duties allow citizens to ignore the law", "A"),
    ],
}


def main():
    db = SessionLocal()

    try:
        lesson = (
            db.query(Lesson)
            .filter(
                Lesson.title == "Fundamental Rights and Duties",
                Lesson.topic == "Social Science"
            )
            .first()
        )

        if not lesson:
            print("ERROR: Fundamental Rights and Duties lesson was not found.")
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