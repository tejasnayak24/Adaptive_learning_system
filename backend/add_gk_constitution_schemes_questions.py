
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 174
LESSON_TITLE = "Indian Constitution, Government Schemes and Important Institutions"
TOPIC = "General Knowledge"

BANK = {
    "Easy": [
        ("When did the Constitution of India come into effect?", "26 January 1950", "15 August 1947", "26 November 1949", "2 October 1950"),
        ("Who is known as the chief architect of the Indian Constitution?", "Dr. B. R. Ambedkar", "Mahatma Gandhi", "Jawaharlal Nehru", "Sardar Patel"),
        ("What is the supreme law of India?", "The Constitution", "The Parliament", "The Supreme Court", "The Election Commission"),
        ("How many Fundamental Rights are currently recognised in the Indian Constitution?", "Six", "Five", "Seven", "Eight"),
        ("Which part of the Constitution contains the Directive Principles of State Policy?", "Part IV", "Part II", "Part III", "Part V"),
        ("Which part of the Constitution deals with Fundamental Rights?", "Part III", "Part II", "Part IV", "Part VI"),
        ("Who is the constitutional head of India?", "The President", "The Prime Minister", "The Chief Justice", "The Speaker"),
        ("Who is the head of the Union Government?", "The Prime Minister", "The President", "The Vice-President", "The Chief Justice"),
        ("What is the lower house of the Indian Parliament called?", "Lok Sabha", "Rajya Sabha", "Vidhan Parishad", "Gram Sabha"),
        ("What is the upper house of the Indian Parliament called?", "Rajya Sabha", "Lok Sabha", "Vidhan Sabha", "Gram Panchayat"),
        ("Who presides over the Lok Sabha?", "Speaker", "President", "Vice-President", "Prime Minister"),
        ("Who is the ex-officio Chairman of the Rajya Sabha?", "Vice-President of India", "President of India", "Prime Minister", "Lok Sabha Speaker"),
        ("What is the minimum voting age in India?", "18 years", "21 years", "25 years", "16 years"),
        ("Which body conducts elections in India?", "Election Commission of India", "Supreme Court", "NITI Aayog", "Finance Commission"),
        ("Which is the highest court in India?", "Supreme Court", "High Court", "District Court", "Sessions Court"),
        ("Which amendment lowered the voting age from 21 to 18 years?", "61st Amendment", "42nd Amendment", "44th Amendment", "73rd Amendment"),
        ("Which national programme aims to provide bank accounts to financially excluded citizens?", "Pradhan Mantri Jan Dhan Yojana", "Digital India", "Make in India", "Beti Bachao Beti Padhao"),
        ("Which scheme provides health insurance coverage to eligible poor and vulnerable families?", "Ayushman Bharat PM-JAY", "PM-KISAN", "Ujjwala Yojana", "Swachh Bharat Mission"),
        ("Which scheme provides income support to eligible farmer families?", "PM-KISAN", "PMAY", "UJALA", "Skill India"),
        ("Which scheme aims to provide LPG connections to eligible women from poor households?", "Pradhan Mantri Ujjwala Yojana", "PM-KISAN", "Digital India", "Atal Pension Yojana"),
        ("Which campaign focuses on cleanliness and sanitation in India?", "Swachh Bharat Mission", "Make in India", "Startup India", "Skill India"),
        ("Which initiative promotes digital infrastructure and online services in India?", "Digital India", "Green India Mission", "PM-KISAN", "Ujjwala Yojana"),
        ("Which initiative encourages manufacturing within India?", "Make in India", "Digital India", "Beti Bachao Beti Padhao", "Ayushman Bharat"),
        ("Which programme promotes the education and welfare of girls?", "Beti Bachao Beti Padhao", "PM-KISAN", "Atal Pension Yojana", "PMAY"),
        ("Which institution is India's central bank?", "Reserve Bank of India", "State Bank of India", "NITI Aayog", "SEBI"),
        ("Where is the headquarters of the Reserve Bank of India?", "Mumbai", "New Delhi", "Kolkata", "Chennai"),
        ("Which organisation regulates the securities market in India?", "SEBI", "RBI", "ISRO", "UGC"),
        ("What does ISRO stand for?", "Indian Space Research Organisation", "Indian Scientific Research Office", "International Space Research Organisation", "Indian Satellite Research Organisation"),
        ("Which organisation replaced the Planning Commission in 2015?", "NITI Aayog", "Finance Commission", "Election Commission", "UPSC"),
        ("Which body is responsible for auditing government accounts in India?", "Comptroller and Auditor General", "Election Commission", "NITI Aayog", "RBI"),
    ],

    "Medium": [
        ("Who was the President of the Constituent Assembly of India?", "Dr. Rajendra Prasad", "Dr. B. R. Ambedkar", "Jawaharlal Nehru", "Sardar Patel"),
        ("Who moved the Objectives Resolution in the Constituent Assembly?", "Jawaharlal Nehru", "Dr. Rajendra Prasad", "Dr. B. R. Ambedkar", "Sardar Patel"),
        ("When was the Constitution of India adopted by the Constituent Assembly?", "26 November 1949", "26 January 1950", "15 August 1947", "2 October 1949"),
        ("Which Article guarantees equality before the law?", "Article 14", "Article 19", "Article 21", "Article 32"),
        ("Which Article guarantees protection of life and personal liberty?", "Article 21", "Article 14", "Article 17", "Article 25"),
        ("Which Article provides the right to constitutional remedies?", "Article 32", "Article 14", "Article 19", "Article 44"),
        ("Which Article abolishes untouchability?", "Article 17", "Article 15", "Article 21", "Article 29"),
        ("Which Article provides freedom of speech and expression?", "Article 19", "Article 14", "Article 21", "Article 32"),
        ("Which amendment is popularly called the Mini Constitution?", "42nd Amendment", "44th Amendment", "52nd Amendment", "61st Amendment"),
        ("Which amendment introduced the anti-defection provisions?", "52nd Amendment", "42nd Amendment", "44th Amendment", "73rd Amendment"),
        ("Which amendment gave constitutional status to Panchayati Raj institutions?", "73rd Amendment", "74th Amendment", "42nd Amendment", "61st Amendment"),
        ("Which amendment gave constitutional status to urban local bodies?", "74th Amendment", "73rd Amendment", "52nd Amendment", "86th Amendment"),
        ("Which amendment made education a Fundamental Right for children aged 6 to 14?", "86th Amendment", "73rd Amendment", "44th Amendment", "61st Amendment"),
        ("Which Article deals with the constitutional provision for the Finance Commission?", "Article 280", "Article 324", "Article 356", "Article 368"),
        ("Which Article deals with the Election Commission of India?", "Article 324", "Article 280", "Article 148", "Article 110"),
        ("Which Article deals with the procedure for amending the Constitution?", "Article 368", "Article 352", "Article 356", "Article 370"),
        ("Which Article provides for the President's Rule in a state?", "Article 356", "Article 352", "Article 360", "Article 368"),
        ("Which Article deals with the proclamation of a National Emergency?", "Article 352", "Article 356", "Article 360", "Article 324"),
        ("Who appoints the Governor of an Indian state?", "President of India", "Prime Minister directly", "Chief Minister", "Chief Justice of India"),
        ("Who appoints the Chief Justice of India?", "President of India", "Prime Minister", "Lok Sabha Speaker", "Vice-President"),
        ("Which body recommends the distribution of tax revenues between the Union and states?", "Finance Commission", "Election Commission", "UPSC", "NITI Aayog"),
        ("Which constitutional body conducts examinations for recruitment to central government services?", "Union Public Service Commission", "Election Commission", "Finance Commission", "NITI Aayog"),
        ("Which scheme provides pension benefits to subscribers in the unorganised sector through a contributory system?", "Atal Pension Yojana", "PM-KISAN", "Ujjwala Yojana", "PMAY"),
        ("Which scheme aims to provide affordable housing to eligible urban and rural households?", "Pradhan Mantri Awas Yojana", "Digital India", "PM-KISAN", "Startup India"),
        ("Which initiative supports entrepreneurship and innovation through startup promotion?", "Startup India", "Swachh Bharat Mission", "Ujjwala Yojana", "PM-JAY"),
        ("Which scheme aims to improve institutional delivery and maternal health outcomes?", "Janani Suraksha Yojana", "PM-KISAN", "Digital India", "Make in India"),
        ("Which institution is responsible for monetary policy in India?", "Reserve Bank of India", "SEBI", "NITI Aayog", "NABARD"),
        ("Which institution primarily regulates insurance companies in India?", "IRDAI", "SEBI", "RBI", "NABARD"),
        ("Which institution regulates and supervises cooperative banks and rural financial institutions along with other functions?", "NABARD", "SEBI", "ISRO", "UGC"),
        ("Which organisation promotes higher education and maintains standards in Indian universities?", "University Grants Commission", "Election Commission", "NITI Aayog", "RBI"),
    ],

    "Hard": [
        ("Which committee was responsible for preparing the initial draft of the Indian Constitution?", "Drafting Committee", "Union Powers Committee", "Rules Committee", "Steering Committee"),
        ("Who was the Chairman of the Drafting Committee?", "Dr. B. R. Ambedkar", "Dr. Rajendra Prasad", "Jawaharlal Nehru", "B. N. Rau"),
        ("Who served as the Constitutional Adviser to the Constituent Assembly?", "B. N. Rau", "Dr. B. R. Ambedkar", "K. M. Munshi", "Alladi Krishnaswami Ayyar"),
        ("Which country is the principal source of the parliamentary system in the Indian Constitution?", "United Kingdom", "United States", "Canada", "Australia"),
        ("The concept of Fundamental Rights in the Indian Constitution was primarily inspired by which country's Constitution?", "United States", "United Kingdom", "Ireland", "France"),
        ("The Directive Principles of State Policy were borrowed from the Constitution of which country?", "Ireland", "United States", "Canada", "Australia"),
        ("Which constitutional feature was influenced by the Canadian Constitution?", "Strong Centre in a federal system", "Fundamental Duties", "Concurrent List", "Judicial review"),
        ("Which Schedule contains the Union, State and Concurrent Lists?", "Seventh Schedule", "Fifth Schedule", "Sixth Schedule", "Tenth Schedule"),
        ("Which Schedule deals with the allocation of seats in the Rajya Sabha?", "Fourth Schedule", "First Schedule", "Seventh Schedule", "Tenth Schedule"),
        ("Which Schedule contains the anti-defection provisions?", "Tenth Schedule", "Ninth Schedule", "Eleventh Schedule", "Twelfth Schedule"),
        ("Which Schedule deals with the administration of tribal areas in Assam, Meghalaya, Tripura and Mizoram?", "Sixth Schedule", "Fifth Schedule", "Seventh Schedule", "Ninth Schedule"),
        ("Which Schedule contains the list of recognised languages in India?", "Eighth Schedule", "Seventh Schedule", "Ninth Schedule", "Tenth Schedule"),
        ("Which Article empowers Parliament to create a new state or alter the boundaries of existing states?", "Article 3", "Article 1", "Article 32", "Article 368"),
        ("Which Article provides for the establishment of the Supreme Court of India?", "Article 124", "Article 110", "Article 148", "Article 214"),
        ("Which Article establishes the office of the Comptroller and Auditor General of India?", "Article 148", "Article 280", "Article 324", "Article 356"),
        ("Which Article provides for the Attorney General of India?", "Article 76", "Article 78", "Article 72", "Article 124"),
        ("Which Article deals with the powers of the President to grant pardons and reprieves?", "Article 72", "Article 76", "Article 123", "Article 143"),
        ("Which Article empowers the Supreme Court to issue writs for enforcement of Fundamental Rights?", "Article 32", "Article 226", "Article 136", "Article 141"),
        ("Which Article empowers High Courts to issue writs?", "Article 226", "Article 32", "Article 124", "Article 368"),
        ("Which type of majority is generally required for a constitutional amendment under Article 368?", "Special majority of Parliament", "Simple majority only", "Two-thirds of all state legislatures", "Unanimous approval of Parliament"),
        ("Which body recommends the principles governing grants-in-aid to states from the Consolidated Fund of India?", "Finance Commission", "Election Commission", "UPSC", "NITI Aayog"),
        ("Which institution replaced the Planning Commission and functions as a policy think tank of the Government of India?", "NITI Aayog", "Finance Commission", "RBI", "SEBI"),
        ("Which scheme provides direct income support to eligible farmer families in India?", "PM-KISAN", "PM-JAY", "PMAY", "Atal Pension Yojana"),
        ("Which scheme is associated with financial support for the girl child's education and welfare through awareness and intervention?", "Beti Bachao Beti Padhao", "PM-KISAN", "Ujjwala Yojana", "Atal Pension Yojana"),
        ("Which scheme aims to promote skill development and employability among Indian youth?", "Skill India Mission", "PM-KISAN", "Swachh Bharat Mission", "PM-JAY"),
        ("Which institution manages India's foreign exchange reserves and acts as the banker to the government?", "Reserve Bank of India", "SEBI", "NABARD", "IRDAI"),
        ("Which institution is responsible for regulating and developing India's capital market?", "SEBI", "RBI", "IRDAI", "NABARD"),
        ("Which constitutional body audits the accounts of the Union and state governments?", "Comptroller and Auditor General of India", "Finance Commission", "UPSC", "Election Commission"),
        ("Which institution is responsible for conducting the national population census in India?", "Office of the Registrar General and Census Commissioner", "NITI Aayog", "Election Commission", "National Statistical Commission"),
        ("Which body is responsible for the protection and promotion of human rights in India at the national level?", "National Human Rights Commission", "Election Commission", "Finance Commission", "NITI Aayog"),
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
                raise ValueError(
                    f"Invalid question format: {difficulty} #{index}"
                )

            question, correct, *wrong = item
            options = [correct] + wrong

            if not all(isinstance(value, str) and value.strip() for value in item):
                raise ValueError(
                    f"Empty field: {difficulty} #{index}"
                )

            if len(set(options)) != 4:
                raise ValueError(
                    f"Duplicate options: {difficulty} #{index}"
                )

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
                "Learn about the Indian Constitution, Fundamental Rights, Parliament, government schemes and important national institutions."
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
                raise ValueError(
                    f"Multiple {difficulty} quizzes found."
                )

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
        print("GK TOPIC 14 INSERTED SUCCESSFULLY")
        print("Indian Constitution, Government Schemes and Institutions")
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
