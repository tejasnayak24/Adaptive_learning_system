import os
from pathlib import Path

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


TOPIC = "Indian Constitution"
SUBJECT = "Social Science"
TARGET_PER_DIFFICULTY = 30


QUESTION_BANK = {
    "Easy": [
        (
            "What is the supreme law of India?",
            "The Constitution",
            "The Parliament",
            "The Supreme Court",
            "The Election Commission",
            "A",
        ),
        (
            "When did the Constitution of India come into effect?",
            "15 August 1947",
            "26 January 1950",
            "26 November 1949",
            "2 October 1950",
            "B",
        ),
        (
            "Who chaired the Drafting Committee of the Indian Constitution?",
            "Jawaharlal Nehru",
            "Sardar Vallabhbhai Patel",
            "Dr. B. R. Ambedkar",
            "Dr. Rajendra Prasad",
            "C",
        ),
        (
            "What is the introduction to the Constitution called?",
            "The Schedule",
            "The Amendment",
            "The Directive",
            "The Preamble",
            "D",
        ),
        (
            "Which document establishes the structure of the Indian government?",
            "The Constitution",
            "A newspaper",
            "A political party manifesto",
            "A municipal notice",
            "A",
        ),
        (
            "Which day is celebrated as Republic Day in India?",
            "15 August",
            "26 January",
            "2 October",
            "14 November",
            "B",
        ),
        (
            "Who was the President of the Constituent Assembly?",
            "Dr. B. R. Ambedkar",
            "Mahatma Gandhi",
            "Dr. Rajendra Prasad",
            "Subhas Chandra Bose",
            "C",
        ),
        (
            "What does universal adult franchise mean?",
            "Only property owners can vote",
            "Only graduates can vote",
            "Only government employees can vote",
            "Eligible adult citizens can vote without discrimination based on wealth or education",
            "D",
        ),
        (
            "Which institution makes laws for the Union of India?",
            "Parliament",
            "The police",
            "The Election Commission",
            "The armed forces",
            "A",
        ),
        (
            "Which part of the Constitution contains Fundamental Rights?",
            "Part I",
            "Part III",
            "Part V",
            "Part IX",
            "B",
        ),
    ],

    "Medium": [
        (
            "Why is the separation of powers important in a democracy?",
            "It gives every power to one person",
            "It removes the need for courts",
            "It distributes government powers and helps prevent their misuse",
            "It prevents the legislature from making laws",
            "C",
        ),
        (
            "What is the primary role of the judiciary?",
            "To conduct elections",
            "To prepare the Union Budget",
            "To command the armed forces",
            "To interpret laws and administer justice",
            "D",
        ),
        (
            "What does federalism involve in India?",
            "Distribution of powers between the Union and the states",
            "Complete abolition of state governments",
            "Rule by local bodies alone",
            "Transfer of all powers to the judiciary",
            "A",
        ),
        (
            "What is the main purpose of Fundamental Rights?",
            "To guarantee that citizens never have duties",
            "To protect essential freedoms and rights",
            "To give unlimited power to the government",
            "To eliminate the need for courts",
            "B",
        ),
        (
            "What is the purpose of constitutional amendments?",
            "To abolish every existing institution",
            "To replace elections with appointments",
            "To change constitutional provisions through the prescribed procedure",
            "To suspend the Constitution permanently",
            "C",
        ),
        (
            "Why is an independent judiciary important?",
            "It allows judges to make laws without limits",
            "It makes elections unnecessary",
            "It puts courts under direct legislative control",
            "It helps courts decide cases without improper interference",
            "D",
        ),
        (
            "What does secularism mean in the Indian constitutional context?",
            "The state does not establish an official religion and must respect religious freedom",
            "Citizens must follow one religion",
            "Religious freedom is prohibited",
            "Only religious leaders can hold public office",
            "A",
        ),
        (
            "What is the main function of the Election Commission of India?",
            "To decide criminal appeals",
            "To supervise elections within its constitutional and legal mandate",
            "To introduce school textbooks",
            "To appoint every state minister",
            "B",
        ),
        (
            "What does the rule of law require?",
            "Only ordinary citizens must obey laws",
            "Government officials are exempt from laws",
            "The law applies to people and public authorities according to legal principles",
            "Courts cannot review government action",
            "C",
        ),
        (
            "What is the role of Directive Principles of State Policy?",
            "They replace Fundamental Rights",
            "They automatically remove elected governments",
            "They give courts unlimited legislative power",
            "They guide the state in making policies for social and economic welfare",
            "D",
        ),
    ],

    "Hard": [
        (
            "Which constitutional article empowers the Supreme Court to issue writs for enforcing Fundamental Rights?",
            "Article 32",
            "Article 40",
            "Article 51",
            "Article 368",
            "A",
        ),
        (
            "Which procedure is generally required to amend the Constitution under Article 368?",
            "Approval by a simple majority in every case",
            "A special majority in each House, with state ratification for specified amendments",
            "Approval by the Supreme Court alone",
            "Approval by every municipal council",
            "B",
        ),
        (
            "Which case is closely associated with the Basic Structure doctrine?",
            "Golaknath v. State of Punjab",
            "Maneka Gandhi v. Union of India",
            "Kesavananda Bharati v. State of Kerala",
            "Minerva Mills v. Union of India",
            "C",
        ),
        (
            "What is the constitutional significance of judicial review?",
            "Courts can replace elected governments at will",
            "Courts can amend any provision without following Article 368",
            "Courts must approve every ordinary administrative decision",
            "Courts can examine whether government action and laws comply with the Constitution",
            "D",
        ),
        (
            "Which article provides for the Finance Commission of India?",
            "Article 280",
            "Article 324",
            "Article 356",
            "Article 370",
            "A",
        ),
        (
            "Which article provides for the constitutional office of the Comptroller and Auditor General of India?",
            "Article 148",
            "Article 280",
            "Article 315",
            "Article 324",
            "A",
        ),
        (
            "Which feature helps maintain the independence of the Supreme Court?",
            "Judges are directly controlled by political parties",
            "Constitutional safeguards govern judicial tenure and removal",
            "The executive can dismiss judges at any time",
            "Judges must follow instructions from individual legislators",
            "B",
        ),
        (
            "Which constitutional provision establishes the procedure for resolving certain disputes between the Union and states through the Supreme Court's original jurisdiction?",
            "Article 14",
            "Article 21",
            "Article 131",
            "Article 226",
            "C",
        ),
        (
            "Which statement best describes a constitutional democracy?",
            "Elections allow the government to act without legal limits",
            "Courts have no role in protecting rights",
            "The executive alone determines the Constitution's meaning",
            "Democratic authority operates within constitutional limits and protections",
            "D",
        ),
        (
            "What is the principal purpose of the anti-defection provisions in the Tenth Schedule?",
            "To address certain forms of political defection by legislators",
            "To establish the Finance Commission",
            "To create the Supreme Court",
            "To determine citizenship by birth in every case",
            "A",
        ),
    ],
}


def find_or_create_quiz(db, difficulty):
    lesson = (
        db.query(Lesson)
        .filter(
            Lesson.title == TOPIC,
            Lesson.topic == SUBJECT,
        )
        .first()
    )

    if lesson is None:
        raise RuntimeError(
            "Indian Constitution lesson was not found. "
            "Run the Social Science setup script first."
        )

    title = f"{TOPIC} - {difficulty}"

    quiz = (
        db.query(Quiz)
        .filter(
            Quiz.lesson_id == lesson.id,
            Quiz.title == title,
        )
        .first()
    )

    if quiz is None:
        quiz = Quiz(
            lesson_id=lesson.id,
            title=title,
            difficulty=difficulty,
        )
        db.add(quiz)
        db.flush()

    return quiz


def add_questions(db, quiz, questions):
    existing = {
        q.question.strip().casefold()
        for q in db.query(Question)
        .filter(Question.quiz_id == quiz.id)
        .all()
    }

    added = 0

    for item in questions:
        question_text, option_a, option_b, option_c, option_d, answer = item

        if question_text.strip().casefold() in existing:
            continue

        db.add(
            Question(
                quiz_id=quiz.id,
                question=question_text,
                option_a=option_a,
                option_b=option_b,
                option_c=option_c,
                option_d=option_d,
                correct_answer=answer,
            )
        )

        existing.add(question_text.strip().casefold())
        added += 1

    db.flush()
    return added


def main():
    db = SessionLocal()

    try:
        print("Adding Indian Constitution questions...")

        for difficulty, questions in QUESTION_BANK.items():
            quiz = find_or_create_quiz(db, difficulty)

            existing_count = (
                db.query(Question)
                .filter(Question.quiz_id == quiz.id)
                .count()
            )

            remaining = max(
                0,
                TARGET_PER_DIFFICULTY - existing_count,
            )

            # Add only as many new questions as needed.
            added = add_questions(
                db,
                quiz,
                questions[:remaining],
            )

            db.commit()

            final_count = (
                db.query(Question)
                .filter(Question.quiz_id == quiz.id)
                .count()
            )

            print(
                f"{difficulty}: existing={existing_count}, "
                f"added={added}, total={final_count}/30"
            )

            if final_count < TARGET_PER_DIFFICULTY:
                print(
                    f"  Still needs "
                    f"{TARGET_PER_DIFFICULTY - final_count} questions."
                )

        print("\nQuestion-bank update completed.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()