
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 189
LESSON_TITLE = "Indian Government, Parliament, Judiciary and Constitutional Bodies"
TOPIC = "General Knowledge"

BANK = {
    "Easy": [
        ("Who is the constitutional head of India?", "The President", "The Prime Minister", "The Chief Justice", "The Speaker"),
        ("Who is the head of the Union Council of Ministers?", "The Prime Minister", "The President", "The Vice-President", "The Chief Justice"),
        ("What is the lower house of the Indian Parliament called?", "Lok Sabha", "Rajya Sabha", "Vidhan Parishad", "Legislative Council"),
        ("What is the upper house of the Indian Parliament called?", "Rajya Sabha", "Lok Sabha", "Gram Sabha", "Vidhan Sabha"),
        ("Where is the Parliament of India located?", "New Delhi", "Mumbai", "Kolkata", "Chennai"),
        ("Who presides over the Lok Sabha?", "Speaker", "President", "Vice-President", "Prime Minister"),
        ("Who is the ex-officio Chairman of the Rajya Sabha?", "Vice-President of India", "President of India", "Prime Minister", "Lok Sabha Speaker"),
        ("What is the minimum age required to become a member of the Lok Sabha?", "25 years", "21 years", "30 years", "35 years"),
        ("What is the minimum age required to become a member of the Rajya Sabha?", "30 years", "25 years", "21 years", "35 years"),
        ("What is the minimum age required to become the President of India?", "35 years", "25 years", "30 years", "40 years"),
        ("Who appoints the Prime Minister of India?", "President of India", "Chief Justice of India", "Lok Sabha Speaker", "Election Commission"),
        ("Who appoints the Governor of a state?", "President of India", "Chief Minister", "Prime Minister alone", "State Legislative Assembly"),
        ("Who is the head of the state government?", "Chief Minister", "Governor", "President", "Chief Justice"),
        ("Who is the constitutional head of a state?", "Governor", "Chief Minister", "Speaker", "District Collector"),
        ("Which institution conducts elections to Parliament and state legislatures in India?", "Election Commission of India", "Supreme Court", "Finance Commission", "Union Public Service Commission"),
        ("Which is the highest court in India?", "Supreme Court", "High Court", "District Court", "Lok Adalat"),
        ("Who is the head of the Supreme Court of India?", "Chief Justice of India", "President", "Attorney General", "Law Minister"),
        ("Which body is responsible for auditing government accounts in India?", "Comptroller and Auditor General", "Election Commission", "Finance Commission", "NITI Aayog"),
        ("Which constitutional body conducts examinations for recruitment to many central government services?", "Union Public Service Commission", "Election Commission", "Finance Commission", "National Human Rights Commission"),
        ("Which body recommends the distribution of certain tax revenues between the Union and states?", "Finance Commission", "Election Commission", "UPSC", "Supreme Court"),
        ("Which part of the Constitution contains Fundamental Rights?", "Part III", "Part II", "Part IV", "Part V"),
        ("Which part of the Constitution contains Directive Principles of State Policy?", "Part IV", "Part III", "Part I", "Part VI"),
        ("Which article guarantees equality before the law?", "Article 14", "Article 19", "Article 21", "Article 32"),
        ("Which article protects life and personal liberty?", "Article 21", "Article 14", "Article 17", "Article 40"),
        ("Which article is associated with the right to constitutional remedies?", "Article 32", "Article 15", "Article 20", "Article 44"),
        ("How many houses does the Indian Parliament have?", "Two", "One", "Three", "Four"),
        ("What is the normal term of the Lok Sabha?", "Five years", "Four years", "Six years", "Seven years"),
        ("Is the Rajya Sabha a permanent house?", "Yes", "No", "Only during emergencies", "Only during elections"),
        ("Who gives assent to a bill passed by Parliament before it becomes an Act?", "President of India", "Chief Justice of India", "Prime Minister", "Lok Sabha Speaker"),
        ("Which local government institution operates at the village level in rural India?", "Gram Panchayat", "Municipal Corporation", "Zila Parishad only", "Cantonment Board"),
    ],

    "Medium": [
        ("Which article of the Constitution provides for the office of the President of India?", "Article 52", "Article 63", "Article 74", "Article 79"),
        ("Which article provides for the office of the Vice-President of India?", "Article 63", "Article 52", "Article 76", "Article 80"),
        ("Which article provides for a Council of Ministers headed by the Prime Minister to aid and advise the President?", "Article 74", "Article 72", "Article 78", "Article 85"),
        ("Which article provides for the Attorney General of India?", "Article 76", "Article 148", "Article 280", "Article 324"),
        ("Which article deals with the Comptroller and Auditor General of India?", "Article 148", "Article 280", "Article 315", "Article 324"),
        ("Which article provides for the Election Commission of India?", "Article 324", "Article 280", "Article 356", "Article 368"),
        ("Which article provides for the Finance Commission?", "Article 280", "Article 148", "Article 76", "Article 110"),
        ("Which article provides for the Union Public Service Commission?", "Article 315", "Article 324", "Article 280", "Article 124"),
        ("Which article defines a Money Bill?", "Article 110", "Article 112", "Article 123", "Article 368"),
        ("Who has the final authority to decide whether a bill is a Money Bill in the Lok Sabha?", "Lok Sabha Speaker", "President", "Prime Minister", "Rajya Sabha Chairman"),
        ("In which house can a Money Bill be introduced?", "Lok Sabha only", "Rajya Sabha only", "Either house", "A joint sitting only"),
        ("For how many days can the Rajya Sabha retain a Money Bill?", "14 days", "30 days", "60 days", "90 days"),
        ("Who presides over a joint sitting of both houses of Parliament?", "Lok Sabha Speaker", "President", "Vice-President", "Prime Minister"),
        ("Which article provides for a joint sitting of Parliament?", "Article 108", "Article 110", "Article 123", "Article 368"),
        ("Which house of Parliament cannot be dissolved?", "Rajya Sabha", "Lok Sabha", "Both houses", "Neither house"),
        ("What proportion of Rajya Sabha members retire every two years?", "One-third", "One-half", "One-fourth", "All members"),
        ("Who elects the President of India?", "An electoral college of elected MPs and elected MLAs", "All citizens directly", "Only Lok Sabha members", "Only state Governors"),
        ("Who elects the Vice-President of India?", "Members of both houses of Parliament", "Only elected Lok Sabha members", "All elected MLAs", "All citizens directly"),
        ("Which writ is issued to produce a person who has been unlawfully detained?", "Habeas Corpus", "Mandamus", "Certiorari", "Quo Warranto"),
        ("Which writ commands a public authority to perform a public duty?", "Mandamus", "Habeas Corpus", "Prohibition", "Quo Warranto"),
        ("Which writ is used to challenge a person's legal authority to hold a public office?", "Quo Warranto", "Habeas Corpus", "Mandamus", "Certiorari"),
        ("Which writ can be issued by a higher court to quash an order of a lower court or tribunal?", "Certiorari", "Habeas Corpus", "Mandamus", "Quo Warranto"),
        ("Which writ prevents a lower court or tribunal from exceeding its jurisdiction?", "Prohibition", "Mandamus", "Habeas Corpus", "Quo Warranto"),
        ("Which constitutional amendment gave constitutional status to Panchayati Raj institutions?", "73rd Amendment", "42nd Amendment", "44th Amendment", "74th Amendment"),
        ("Which constitutional amendment gave constitutional status to urban local bodies?", "74th Amendment", "73rd Amendment", "52nd Amendment", "61st Amendment"),
        ("Which schedule of the Constitution lists the recognised languages?", "Eighth Schedule", "Seventh Schedule", "Ninth Schedule", "Tenth Schedule"),
        ("Which schedule deals with the division of legislative powers through Union, State and Concurrent Lists?", "Seventh Schedule", "Eighth Schedule", "Fifth Schedule", "Tenth Schedule"),
        ("Which schedule contains provisions relating to anti-defection?", "Tenth Schedule", "Ninth Schedule", "Seventh Schedule", "Eleventh Schedule"),
        ("Which constitutional body advises the President on the allocation of seats in the Lok Sabha after a census through delimitation arrangements?", "Delimitation Commission", "Finance Commission", "UPSC", "NITI Aayog"),
        ("Who is the chief legal adviser to the Government of India?", "Attorney General of India", "Chief Justice of India", "Solicitor General of a state", "Law Secretary"),
    ],

    "Hard": [
        ("Which article empowers the President to promulgate ordinances when Parliament is not in session?", "Article 123", "Article 110", "Article 352", "Article 368"),
        ("Which article empowers a Governor to promulgate ordinances when the state legislature is not in session?", "Article 213", "Article 200", "Article 356", "Article 161"),
        ("Which article deals with the constitutional procedure for amending the Constitution?", "Article 368", "Article 356", "Article 324", "Article 280"),
        ("Which article provides for the proclamation of a National Emergency?", "Article 352", "Article 356", "Article 360", "Article 368"),
        ("Which article deals with President's Rule in a state?", "Article 356", "Article 352", "Article 360", "Article 365"),
        ("Which article provides for a Financial Emergency?", "Article 360", "Article 352", "Article 356", "Article 368"),
        ("Which article provides for the establishment of the Supreme Court of India?", "Article 124", "Article 214", "Article 226", "Article 32"),
        ("Which article gives High Courts the power to issue writs?", "Article 226", "Article 32", "Article 136", "Article 141"),
        ("Which article gives the Supreme Court special leave jurisdiction?", "Article 136", "Article 124", "Article 226", "Article 143"),
        ("Which article empowers the President to seek the advisory opinion of the Supreme Court?", "Article 143", "Article 136", "Article 141", "Article 131"),
        ("Which article makes the law declared by the Supreme Court binding on all courts in India?", "Article 141", "Article 143", "Article 226", "Article 32"),
        ("Which article deals with the original jurisdiction of the Supreme Court in disputes between the Union and states?", "Article 131", "Article 136", "Article 143", "Article 226"),
        ("Which article provides for the removal of the President through impeachment?", "Article 61", "Article 72", "Article 74", "Article 110"),
        ("Which article deals with the removal of Supreme Court judges?", "Article 124(4)", "Article 148", "Article 280", "Article 324"),
        ("What is the constitutional minimum number of members required to form a quorum in either house of Parliament?", "One-tenth of the total membership", "One-third of the total membership", "One-half of the total membership", "One-fourth of the total membership"),
        ("What is the maximum permitted gap between two sessions of Parliament?", "Six months", "Three months", "One year", "Two months"),
        ("Which parliamentary committee examines the reports of the Comptroller and Auditor General?", "Public Accounts Committee", "Estimates Committee", "Rules Committee", "Business Advisory Committee"),
        ("Which parliamentary committee examines estimates of government expenditure and suggests economies?", "Estimates Committee", "Public Accounts Committee", "Committee on Privileges", "Petitions Committee"),
        ("Which parliamentary committee examines whether delegated powers are being properly exercised by the executive?", "Committee on Subordinate Legislation", "Public Accounts Committee", "Estimates Committee", "Business Advisory Committee"),
        ("Which constitutional amendment is commonly called the Mini Constitution?", "42nd Amendment", "44th Amendment", "52nd Amendment", "61st Amendment"),
        ("Which amendment lowered the voting age from 21 to 18 years?", "61st Amendment", "42nd Amendment", "44th Amendment", "73rd Amendment"),
        ("Which amendment introduced the anti-defection provisions into the Constitution?", "52nd Amendment", "44th Amendment", "61st Amendment", "86th Amendment"),
        ("Which amendment inserted the words Socialist, Secular and Integrity into the Preamble?", "42nd Amendment", "24th Amendment", "44th Amendment", "73rd Amendment"),
        ("Which article provides for the right to education for children aged 6 to 14 years?", "Article 21A", "Article 19", "Article 24", "Article 30"),
        ("Which article directs the state to organise village panchayats?", "Article 40", "Article 32", "Article 44", "Article 51"),
        ("Which article provides for the constitutional protection of the independence of the Election Commission?", "Article 324", "Article 280", "Article 315", "Article 148"),
        ("Which body recommends measures for the distribution of financial resources between the Union and states?", "Finance Commission", "Election Commission", "UPSC", "National Development Council"),
        ("Who appoints the Comptroller and Auditor General of India?", "President of India", "Prime Minister", "Chief Justice of India", "Lok Sabha Speaker"),
        ("Who appoints the Chief Election Commissioner and other Election Commissioners under the current constitutional and statutory framework?", "President of India", "Chief Justice of India", "Lok Sabha Speaker", "Governor"),
        ("Which institution replaced the Planning Commission in 2015?", "NITI Aayog", "Finance Commission", "National Development Council", "Inter-State Council"),
    ]
}


def validate_bank():
    for difficulty, questions in BANK.items():
        if len(questions) != 30:
            raise ValueError(
                f"{difficulty} must contain exactly 30 questions; "
                f"found {len(questions)}"
            )

        for index, item in enumerate(questions, start=1):
            if len(item) != 5:
                raise ValueError(
                    f"{difficulty} question {index} must contain 5 values"
                )

            if not all(isinstance(value, str) and value.strip() for value in item):
                raise ValueError(
                    f"Empty or invalid value in {difficulty} question {index}"
                )

            if len(set(item[1:])) != 4:
                raise ValueError(
                    f"Duplicate options in {difficulty} question {index}"
                )


def main():
    validate_bank()

    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT title, topic FROM lessons WHERE id = ?",
            (LESSON_ID,)
        )
        lesson = cursor.fetchone()

        if lesson is None:
            cursor.execute(
                """
                INSERT INTO lessons
                (id, title, topic, difficulty, content, created_at)
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """,
                (
                    LESSON_ID,
                    LESSON_TITLE,
                    TOPIC,
                    "Mixed",
                    "MCQ lesson covering Indian government, Parliament, "
                    "judiciary and constitutional bodies."
                )
            )
            print(f"Created lesson {LESSON_ID}: {LESSON_TITLE}")

        elif lesson != (LESSON_TITLE, TOPIC):
            raise ValueError(
                f"Lesson ID {LESSON_ID} already belongs to "
                f"{lesson[0]!r} under topic {lesson[1]!r}. "
                "No data was changed."
            )

        for difficulty, questions in BANK.items():
            cursor.execute(
                """
                SELECT id FROM quizzes
                WHERE lesson_id = ? AND difficulty = ?
                ORDER BY id
                LIMIT 1
                """,
                (LESSON_ID, difficulty)
            )

            quiz = cursor.fetchone()

            if quiz is None:
                cursor.execute(
                    """
                    INSERT INTO quizzes (lesson_id, title, difficulty)
                    VALUES (?, ?, ?)
                    """,
                    (
                        LESSON_ID,
                        f"{LESSON_TITLE} - {difficulty}",
                        difficulty
                    )
                )
                quiz_id = cursor.lastrowid
                print(f"Created {difficulty} quiz: {quiz_id}")
            else:
                quiz_id = quiz[0]

            cursor.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                (quiz_id,)
            )
            existing_count = cursor.fetchone()[0]

            if existing_count > 30:
                raise ValueError(
                    f"{difficulty} quiz already has {existing_count} questions. "
                    "Expected maximum: 30."
                )

            for question, correct, wrong1, wrong2, wrong3 in questions[existing_count:]:
                options = [correct, wrong1, wrong2, wrong3]
                random.shuffle(options)

                correct_answer = "ABCD"[options.index(correct)]

                cursor.execute(
                    """
                    INSERT INTO questions
                    (
                        quiz_id,
                        question,
                        option_a,
                        option_b,
                        option_c,
                        option_d,
                        correct_answer
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        quiz_id,
                        question,
                        options[0],
                        options[1],
                        options[2],
                        options[3],
                        correct_answer
                    )
                )

            cursor.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                (quiz_id,)
            )
            final_count = cursor.fetchone()[0]

            if final_count != 30:
                raise ValueError(
                    f"{difficulty} quiz has {final_count} questions, not 30"
                )

            print(f"{difficulty}: {final_count}/30 questions")

        connection.commit()

        print("\nSUCCESS!")
        print(f"Lesson ID: {LESSON_ID}")
        print(f"Lesson: {LESSON_TITLE}")
        print("Easy: 30 questions")
        print("Medium: 30 questions")
        print("Hard: 30 questions")
        print("Total: 90 questions")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
