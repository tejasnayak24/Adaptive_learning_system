
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 167
LESSON_TITLE = "Indian Polity - Constitution, Parliament and Fundamental Rights"
TOPIC = "General Knowledge"

BANK = {
    "Easy": [
        ("When was the Constitution of India adopted?", "26 November 1949", "15 August 1947", "26 January 1950", "2 October 1949"),
        ("When did the Constitution of India come into force?", "26 January 1950", "26 November 1949", "15 August 1947", "1 January 1950"),
        ("Who is known as the Father of the Indian Constitution?", "Dr. B. R. Ambedkar", "Mahatma Gandhi", "Jawaharlal Nehru", "Sardar Patel"),
        ("Who was the first President of India?", "Dr. Rajendra Prasad", "Dr. S. Radhakrishnan", "Zakir Hussain", "V. V. Giri"),
        ("Who is the constitutional head of India?", "President", "Prime Minister", "Chief Justice", "Speaker"),
        ("Who is the head of the Union Council of Ministers?", "Prime Minister", "President", "Vice-President", "Governor"),
        ("What is the lower house of the Indian Parliament called?", "Lok Sabha", "Rajya Sabha", "Vidhan Parishad", "Gram Sabha"),
        ("What is the upper house of the Indian Parliament called?", "Rajya Sabha", "Lok Sabha", "Vidhan Sabha", "Gram Panchayat"),
        ("What is the minimum voting age in India?", "18 years", "21 years", "16 years", "25 years"),
        ("How many houses does the Indian Parliament have?", "Two", "One", "Three", "Four"),
        ("Who appoints the Prime Minister of India?", "President", "Chief Justice", "Lok Sabha Speaker", "Election Commission"),
        ("Who is the constitutional head of a state in India?", "Governor", "Chief Minister", "President", "Speaker"),
        ("Which part of the Constitution contains Fundamental Rights?", "Part III", "Part I", "Part IV", "Part V"),
        ("Which part of the Constitution contains Directive Principles of State Policy?", "Part IV", "Part III", "Part II", "Part VI"),
        ("Which article guarantees equality before the law?", "Article 14", "Article 19", "Article 21", "Article 32"),
        ("Which article protects the right to life and personal liberty?", "Article 21", "Article 14", "Article 17", "Article 25"),
        ("Which article abolishes untouchability?", "Article 17", "Article 15", "Article 19", "Article 22"),
        ("Who presides over the Lok Sabha?", "Speaker", "President", "Vice-President", "Prime Minister"),
        ("Who is the ex-officio Chairman of the Rajya Sabha?", "Vice-President of India", "President of India", "Prime Minister", "Lok Sabha Speaker"),
        ("Which body conducts elections in India?", "Election Commission of India", "Supreme Court", "Parliament Secretariat", "Finance Commission"),
        ("What is the national voting system used for Lok Sabha elections?", "Universal adult suffrage", "Property-based voting", "Education-based voting", "Appointment system"),
        ("Which is the highest court in India?", "Supreme Court", "High Court", "District Court", "Lok Adalat"),
        ("Who appoints the Governor of a state?", "President", "Chief Minister", "Prime Minister alone", "State Legislature"),
        ("Who is the head of the state government?", "Chief Minister", "Governor", "President", "Chief Secretary"),
        ("Which document begins with the words 'We, the People of India'?", "Preamble", "Fundamental Duties", "First Schedule", "Union List"),
        ("Which day is celebrated as Constitution Day in India?", "26 November", "26 January", "15 August", "2 October"),
        ("How many Fundamental Duties are currently listed in the Indian Constitution?", "11", "10", "12", "9"),
        ("Which institution interprets the Constitution of India?", "Supreme Court", "Election Commission", "Finance Commission", "Planning Commission"),
        ("Which house of Parliament is permanent and cannot be dissolved?", "Rajya Sabha", "Lok Sabha", "Both houses", "Neither house"),
        ("What is the normal term of the Lok Sabha?", "Five years", "Four years", "Six years", "Seven years"),
    ],

    "Medium": [
        ("Which committee was responsible for drafting the Indian Constitution?", "Drafting Committee", "Union Powers Committee", "Rules Committee", "Finance Committee"),
        ("Who was the Chairman of the Drafting Committee?", "Dr. B. R. Ambedkar", "Dr. Rajendra Prasad", "Jawaharlal Nehru", "B. N. Rau"),
        ("Who was the President of the Constituent Assembly?", "Dr. Rajendra Prasad", "Dr. B. R. Ambedkar", "Jawaharlal Nehru", "Sardar Patel"),
        ("Who served as the Constitutional Adviser to the Constituent Assembly?", "B. N. Rau", "K. M. Munshi", "Alladi Krishnaswami Ayyar", "B. R. Ambedkar"),
        ("Which article deals with the procedure for constitutional amendments?", "Article 368", "Article 356", "Article 352", "Article 324"),
        ("Which article provides for the establishment of the Finance Commission?", "Article 280", "Article 148", "Article 324", "Article 110"),
        ("Which article deals with the Election Commission of India?", "Article 324", "Article 280", "Article 368", "Article 123"),
        ("Which article provides for the office of the Comptroller and Auditor General of India?", "Article 148", "Article 280", "Article 76", "Article 124"),
        ("Which article defines a Money Bill?", "Article 110", "Article 112", "Article 123", "Article 356"),
        ("Who decides whether a bill is a Money Bill in the Lok Sabha?", "Lok Sabha Speaker", "President", "Prime Minister", "Rajya Sabha Chairman"),
        ("Can the Rajya Sabha reject a Money Bill?", "No", "Yes, absolutely", "Only with the President's approval", "Only during a joint sitting"),
        ("What is the maximum permitted gap between two sessions of Parliament?", "Six months", "Three months", "One year", "Two months"),
        ("Which house of Parliament represents the states and Union Territories?", "Rajya Sabha", "Lok Sabha", "Both houses equally", "Gram Sabha"),
        ("What is the minimum age required to become a Lok Sabha member?", "25 years", "21 years", "30 years", "35 years"),
        ("What is the minimum age required to become a Rajya Sabha member?", "30 years", "25 years", "35 years", "21 years"),
        ("What is the minimum age required to become President of India?", "35 years", "30 years", "25 years", "40 years"),
        ("Which article provides for the impeachment of the President?", "Article 61", "Article 72", "Article 74", "Article 123"),
        ("Who elects the President of India?", "An electoral college", "Only the Lok Sabha", "Only the Rajya Sabha", "Directly all citizens"),
        ("Who elects the Vice-President of India?", "Members of both Houses of Parliament", "Only Lok Sabha members", "Only state legislators", "All registered voters"),
        ("Which article provides for the proclamation of a National Emergency?", "Article 352", "Article 356", "Article 360", "Article 368"),
        ("Which article deals with President's Rule in a state?", "Article 356", "Article 352", "Article 360", "Article 324"),
        ("Which article deals with Financial Emergency?", "Article 360", "Article 352", "Article 356", "Article 280"),
        ("Which Fundamental Right is protected under Article 19?", "Freedom rights", "Right to property", "Right to constitutional remedies only", "Right against exploitation only"),
        ("Which article allows citizens to approach the Supreme Court for enforcement of Fundamental Rights?", "Article 32", "Article 21", "Article 14", "Article 40"),
        ("Which writ means 'to produce the body'?", "Habeas Corpus", "Mandamus", "Certiorari", "Quo Warranto"),
        ("Which writ is issued to command a public authority to perform its legal duty?", "Mandamus", "Habeas Corpus", "Prohibition", "Quo Warranto"),
        ("Which schedule contains the Union List, State List and Concurrent List?", "Seventh Schedule", "First Schedule", "Fifth Schedule", "Tenth Schedule"),
        ("Which schedule deals with anti-defection provisions?", "Tenth Schedule", "Eighth Schedule", "Ninth Schedule", "Twelfth Schedule"),
        ("Which amendment lowered the voting age from 21 to 18 years?", "61st Amendment", "42nd Amendment", "44th Amendment", "73rd Amendment"),
        ("Which amendment is popularly called the Mini Constitution?", "42nd Amendment", "44th Amendment", "52nd Amendment", "61st Amendment"),
    ],

    "Hard": [
        ("Which case established the Basic Structure doctrine of the Indian Constitution?", "Kesavananda Bharati v. State of Kerala", "Golaknath v. State of Punjab", "Maneka Gandhi v. Union of India", "Minerva Mills v. Union of India"),
        ("In which year was the Basic Structure doctrine established?", "1973", "1950", "1967", "1980"),
        ("Which Supreme Court case expanded the interpretation of Article 21 to include the requirement of fair, just and reasonable procedure?", "Maneka Gandhi v. Union of India", "A. K. Gopalan v. State of Madras", "Shankari Prasad v. Union of India", "Berubari Union case"),
        ("Which article provides for the constitutional position of the Council of Ministers to aid and advise the President?", "Article 74", "Article 72", "Article 76", "Article 78"),
        ("Which article deals with the Attorney General of India?", "Article 76", "Article 148", "Article 280", "Article 324"),
        ("Which article provides for the appointment of the Prime Minister and other ministers?", "Article 75", "Article 74", "Article 77", "Article 78"),
        ("Which article provides for the establishment of the Supreme Court of India?", "Article 124", "Article 214", "Article 226", "Article 32"),
        ("Which article empowers High Courts to issue writs?", "Article 226", "Article 32", "Article 136", "Article 143"),
        ("Which article gives the Supreme Court advisory jurisdiction?", "Article 143", "Article 131", "Article 136", "Article 142"),
        ("Which article deals with the original jurisdiction of the Supreme Court in certain federal disputes?", "Article 131", "Article 124", "Article 226", "Article 148"),
        ("Which constitutional amendment introduced the anti-defection law?", "52nd Amendment", "42nd Amendment", "44th Amendment", "61st Amendment"),
        ("Which amendment added Fundamental Duties to the Constitution?", "42nd Amendment", "44th Amendment", "52nd Amendment", "73rd Amendment"),
        ("Which amendment introduced constitutional status for Panchayati Raj institutions?", "73rd Amendment", "74th Amendment", "42nd Amendment", "86th Amendment"),
        ("Which amendment gave constitutional status to municipalities?", "74th Amendment", "73rd Amendment", "61st Amendment", "91st Amendment"),
        ("Which amendment inserted Article 21A, providing the right to education?", "86th Amendment", "42nd Amendment", "44th Amendment", "73rd Amendment"),
        ("Which amendment introduced the Goods and Services Tax framework?", "101st Amendment", "100th Amendment", "102nd Amendment", "103rd Amendment"),
        ("Which amendment introduced the provision for reservation for Economically Weaker Sections?", "103rd Amendment", "101st Amendment", "104th Amendment", "105th Amendment"),
        ("Which article provides for the procedure of a joint sitting of both Houses of Parliament?", "Article 108", "Article 110", "Article 112", "Article 123"),
        ("Who presides over a joint sitting of Parliament?", "Speaker of the Lok Sabha", "President of India", "Vice-President of India", "Prime Minister"),
        ("Which article deals with the annual financial statement of the Union Government?", "Article 112", "Article 110", "Article 280", "Article 266"),
        ("Which fund is described as the main account into which government revenues are credited?", "Consolidated Fund of India", "Contingency Fund of India", "Public Account of India", "National Investment Fund"),
        ("Which article provides for the creation of new states or alteration of state boundaries?", "Article 3", "Article 1", "Article 2", "Article 4 only"),
        ("Which article states that India, that is Bharat, shall be a Union of States?", "Article 1", "Article 2", "Article 3", "Article 5"),
        ("Which schedule lists the recognised languages of India?", "Eighth Schedule", "Seventh Schedule", "Ninth Schedule", "Tenth Schedule"),
        ("Which schedule contains provisions relating to the administration of tribal areas in Assam, Meghalaya, Tripura and Mizoram?", "Sixth Schedule", "Fifth Schedule", "Fourth Schedule", "Seventh Schedule"),
        ("Which article provides for the National Commission for Scheduled Castes?", "Article 338", "Article 340", "Article 324", "Article 280"),
        ("Which article provides for the National Commission for Scheduled Tribes?", "Article 338A", "Article 338", "Article 342", "Article 343"),
        ("Which article provides for the official language of the Union?", "Article 343", "Article 345", "Article 348", "Article 351"),
        ("Which article provides for the constitutional amendment procedure?", "Article 368", "Article 356", "Article 352", "Article 360"),
        ("Which constitutional authority audits the accounts of the Union and state governments?", "Comptroller and Auditor General", "Finance Commission", "Election Commission", "Attorney General"),
    ]
}


def validate_bank():
    for difficulty, questions in BANK.items():
        if len(questions) != 30:
            raise ValueError(
                f"{difficulty}: Expected 30 questions, found {len(questions)}"
            )

        for index, item in enumerate(questions, 1):
            if len(item) != 5:
                raise ValueError(f"Invalid question format: {difficulty} #{index}")

            question, correct, *wrong = item
            options = [correct] + wrong

            if not all(isinstance(x, str) and x.strip() for x in item):
                raise ValueError(f"Empty field: {difficulty} #{index}")

            if len(set(options)) != 4:
                raise ValueError(f"Duplicate options: {difficulty} #{index}")

    print("Question bank validation successful.")


def main():
    validate_bank()

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT title, topic FROM lessons WHERE id = ?",
            (LESSON_ID,)
        )
        existing = cursor.fetchone()

        if existing is None:
            cursor.execute("""
                INSERT INTO lessons
                (id, title, topic, difficulty, content, created_at)
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (
                LESSON_ID,
                LESSON_TITLE,
                TOPIC,
                "Mixed",
                "Learn about the Indian Constitution, Parliament, Fundamental Rights and constitutional institutions."
            ))
        elif existing != (LESSON_TITLE, TOPIC):
            raise ValueError(
                f"Lesson ID {LESSON_ID} is already occupied by {existing}"
            )

        for difficulty, questions in BANK.items():
            cursor.execute("""
                SELECT id FROM quizzes
                WHERE lesson_id = ? AND difficulty = ?
            """, (LESSON_ID, difficulty))

            quiz_rows = cursor.fetchall()

            if len(quiz_rows) > 1:
                raise ValueError(f"Multiple {difficulty} quizzes found.")

            if quiz_rows:
                quiz_id = quiz_rows[0][0]
            else:
                cursor.execute("""
                    INSERT INTO quizzes (lesson_id, title, difficulty)
                    VALUES (?, ?, ?)
                """, (
                    LESSON_ID,
                    f"{LESSON_TITLE} - {difficulty}",
                    difficulty
                ))
                quiz_id = cursor.lastrowid

            cursor.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                (quiz_id,)
            )
            existing_count = cursor.fetchone()[0]

            if existing_count > 30:
                raise ValueError(
                    f"{difficulty} already has {existing_count} questions."
                )

            for item in questions[existing_count:]:
                question, correct, wrong1, wrong2, wrong3 = item

                options = [correct, wrong1, wrong2, wrong3]
                random.shuffle(options)

                correct_letter = "ABCD"[options.index(correct)]

                cursor.execute("""
                    INSERT INTO questions (
                        quiz_id, question,
                        option_a, option_b, option_c, option_d,
                        correct_answer
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    quiz_id,
                    question,
                    options[0],
                    options[1],
                    options[2],
                    options[3],
                    correct_letter
                ))

            cursor.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                (quiz_id,)
            )
            final_count = cursor.fetchone()[0]

            if final_count != 30:
                raise ValueError(
                    f"{difficulty} has {final_count} questions instead of 30."
                )

            print(f"{difficulty}: {final_count}/30 SUCCESS")

        connection.commit()

        print("\n====================================")
        print("GK TOPIC 7 INSERTED SUCCESSFULLY")
        print("Indian Polity")
        print("Easy: 30")
        print("Medium: 30")
        print("Hard: 30")
        print("TOTAL: 90 QUESTIONS")
        print("====================================")

    except Exception as error:
        connection.rollback()
        print("ERROR:", error)
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
