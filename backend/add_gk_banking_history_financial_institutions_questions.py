
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 194
LESSON_TITLE = "Indian Banking History, Financial Institutions and Government Financial Schemes"
TOPIC = "General Knowledge"

BANK = {
    "Easy": [
        ("In which year was the Reserve Bank of India established?", "1935", "1947", "1950", "1969"),
        ("When was the Reserve Bank of India nationalised?", "1949", "1935", "1955", "1969"),
        ("Which was the first bank established in India?", "Bank of Hindostan", "State Bank of India", "Punjab National Bank", "Bank of Baroda"),
        ("Which bank was established in 1806 as the Bank of Calcutta?", "State Bank of India", "Punjab National Bank", "Canara Bank", "Union Bank of India"),
        ("In which year was the Imperial Bank of India established?", "1921", "1935", "1949", "1955"),
        ("Which institution was created in 1955 by transforming the Imperial Bank of India?", "State Bank of India", "Reserve Bank of India", "NABARD", "EXIM Bank"),
        ("In which year was the State Bank of India established?", "1955", "1949", "1969", "1982"),
        ("When were 14 major commercial banks nationalised in India?", "1969", "1955", "1980", "1991"),
        ("In which year were six more commercial banks nationalised?", "1980", "1969", "1975", "1990"),
        ("Which bank is commonly known as SBI?", "State Bank of India", "Standard Bank of India", "Small Banking Institution", "State Business Institution"),
        ("What is the full form of NABARD?", "National Bank for Agriculture and Rural Development", "National Association of Banking and Rural Deposits", "National Bank for Advanced Research and Development", "New Agricultural Bank and Rural Department"),
        ("In which year was NABARD established?", "1982", "1949", "1969", "1991"),
        ("What is the full form of SIDBI?", "Small Industries Development Bank of India", "State Industrial Deposit Bank of India", "Small Investment and Development Board of India", "Service Industries Development Bureau of India"),
        ("In which year was SIDBI established?", "1990", "1982", "1955", "2000"),
        ("What is the full form of EXIM Bank?", "Export-Import Bank of India", "External Investment Management Bank", "Export Insurance Market Bank", "Exchange and Import Monetary Bank"),
        ("In which year was EXIM Bank of India established?", "1982", "1949", "1969", "1995"),
        ("Which institution regulates insurance companies in India?", "IRDAI", "SEBI", "RBI", "NABARD"),
        ("What is the full form of IRDAI?", "Insurance Regulatory and Development Authority of India", "Indian Reserve Deposit Authority of India", "Insurance Research and Development Association of India", "International Regulatory Department of India"),
        ("Which institution regulates India's securities market?", "SEBI", "RBI", "NABARD", "SIDBI"),
        ("In which year was SEBI established as a statutory body?", "1992", "1982", "1955", "2000"),
        ("What is the main objective of Pradhan Mantri Jan Dhan Yojana?", "Promote financial inclusion", "Provide free housing to everyone", "Build national highways", "Promote agricultural exports"),
        ("In which year was Pradhan Mantri Jan Dhan Yojana launched?", "2014", "2010", "2016", "2008"),
        ("Which scheme provides accident insurance coverage to eligible subscribers?", "Pradhan Mantri Suraksha Bima Yojana", "Atal Pension Yojana", "PM-KISAN", "MUDRA Yojana"),
        ("Which scheme is associated with pension benefits for eligible subscribers?", "Atal Pension Yojana", "PM-KISAN", "Stand-Up India", "PMAY"),
        ("Which scheme provides income support to eligible farmer families?", "PM-KISAN", "MUDRA Yojana", "Skill India", "Startup India"),
        ("What is the full form of MUDRA?", "Micro Units Development and Refinance Agency", "Monetary Unit Development and Rural Association", "Micro Urban Deposit and Revenue Authority", "Management of Unified Development and Rural Assets"),
        ("Which scheme supports micro and small business enterprises through institutional credit?", "Pradhan Mantri MUDRA Yojana", "PM-KISAN", "Swachh Bharat Mission", "Ayushman Bharat"),
        ("Which institution is responsible for managing India's foreign exchange reserves?", "Reserve Bank of India", "SEBI", "NABARD", "IRDAI"),
        ("Which institution provides credit information and credit scores in India?", "TransUnion CIBIL", "NABARD", "EXIM Bank", "IRDAI"),
        ("What is the main purpose of a cooperative bank?", "Provide banking services to its members and communities", "Print currency notes", "Regulate stock exchanges", "Manage national defence"),
    ],

    "Medium": [
        ("Which bank is known as the oldest joint-stock bank in India that is still operating under its present name?", "Allahabad Bank is no longer a separate operating bank", "Punjab National Bank", "Bank of Baroda", "Canara Bank"),
        ("Which bank was founded in 1894 and is headquartered in Lahore originally?", "Punjab National Bank", "Bank of India", "Canara Bank", "Union Bank of India"),
        ("Which institution was established to promote industrial finance before its functions were transferred to other institutions?", "Industrial Development Bank of India", "NABARD", "IRDAI", "NPCI"),
        ("In which year was the Industrial Development Bank of India established?", "1964", "1955", "1982", "1992"),
        ("Which institution was established to support agricultural and rural development finance?", "NABARD", "SEBI", "EXIM Bank", "IRDAI"),
        ("Which institution primarily supports the financing and development of small industries?", "SIDBI", "NABARD", "RBI", "LIC"),
        ("What is the primary function of EXIM Bank of India?", "Financing and promoting India's international trade", "Regulating insurance companies", "Managing stock exchanges", "Issuing currency notes"),
        ("Which institution provides life insurance services in India?", "Life Insurance Corporation of India", "SEBI", "NABARD", "NPCI"),
        ("In which year was the Life Insurance Corporation of India established?", "1956", "1949", "1969", "1982"),
        ("Which committee is associated with major banking sector reforms in India during the 1990s?", "Narasimham Committee", "Sarkaria Commission", "Mandal Commission", "Kothari Commission"),
        ("Which committee recommended reforms in the Indian banking system in 1991?", "Narasimham Committee I", "Urjit Patel Committee", "Rangarajan Committee", "Kelkar Committee"),
        ("What was a major objective of the 1991 banking sector reforms?", "Improve efficiency, competition and financial stability", "Eliminate all private banks", "Stop all foreign trade", "Replace all bank deposits with cash"),
        ("What is priority sector lending?", "Bank lending to sectors identified as important for inclusive economic development", "Lending only to large corporations", "Loans given only to foreign governments", "Loans restricted to stock exchanges"),
        ("Which of the following is generally included in priority sector lending?", "Agriculture", "Luxury tourism only", "Foreign stock speculation", "Entertainment awards"),
        ("What is the main objective of the Pradhan Mantri Mudra Yojana?", "Provide access to institutional finance for eligible micro enterprises", "Provide free electricity to all households", "Fund large multinational corporations", "Finance only government departments"),
        ("Which MUDRA loan category covers loans up to ₹50,000?", "Shishu", "Kishor", "Tarun", "Vikas"),
        ("Which MUDRA category traditionally covers loans above ₹50,000 and up to ₹5 lakh?", "Kishor", "Shishu", "Tarun", "Vikas"),
        ("Which MUDRA category traditionally covers loans above ₹5 lakh and up to ₹10 lakh?", "Tarun", "Shishu", "Kishor", "Jan Dhan"),
        ("What is the primary objective of Stand-Up India?", "Promote entrepreneurship among women and SC/ST borrowers", "Provide pension to government employees", "Insure agricultural crops only", "Provide free school textbooks"),
        ("What is the primary purpose of the Kisan Credit Card scheme?", "Provide timely credit to farmers for agricultural and related needs", "Provide free agricultural land", "Provide life insurance to all citizens", "Finance only urban housing"),
        ("Which scheme is associated with crop insurance for farmers?", "Pradhan Mantri Fasal Bima Yojana", "Atal Pension Yojana", "MUDRA Yojana", "Stand-Up India"),
        ("Which institution operates the Employees' Provident Fund system?", "Employees' Provident Fund Organisation", "SEBI", "NABARD", "NPCI"),
        ("What is the full form of EPFO?", "Employees' Provident Fund Organisation", "Economic Pension Finance Office", "Employee Payment Fund Organisation", "External Provident Finance Office"),
        ("Which institution manages the National Pension System framework under the pension regulator?", "Pension Fund Regulatory and Development Authority", "SEBI", "IRDAI", "NABARD"),
        ("What is the full form of PFRDA?", "Pension Fund Regulatory and Development Authority", "Public Finance Regulation and Development Association", "Personal Fund Research and Deposit Authority", "Pension Finance Reserve Department of India"),
        ("Which institution regulates pension funds in India?", "PFRDA", "SEBI", "RBI", "IRDAI"),
        ("What is the main objective of the Financial Inclusion Fund?", "Support initiatives that expand access to financial services", "Fund only stock market speculation", "Finance luxury imports", "Replace the banking system"),
        ("What is the purpose of the Business Correspondent model in banking?", "Extend banking services through authorised agents", "Replace all bank branches with stock exchanges", "Issue currency notes through private companies", "Regulate insurance premiums"),
        ("Which organisation operates the RuPay card payment network?", "NPCI", "SEBI", "IRDAI", "NABARD"),
        ("What is the main purpose of the Bharat Bill Payment System?", "Provide an interoperable platform for bill payments", "Provide agricultural loans", "Regulate stock trading", "Issue government bonds"),
    ],

    "Hard": [
        ("Which Act established the Reserve Bank of India?", "Reserve Bank of India Act, 1934", "Banking Regulation Act, 1949", "Companies Act, 1956", "Securities Contracts Regulation Act, 1956"),
        ("Which Act provides the principal legal framework for regulating banking companies in India?", "Banking Regulation Act, 1949", "RBI Act, 1934", "SEBI Act, 1992", "Insurance Act, 1938"),
        ("Which committee is associated with the second major review of banking sector reforms in India in 1998?", "Narasimham Committee II", "Urjit Patel Committee", "Raghuram Rajan Committee", "Sarkaria Commission"),
        ("Which committee recommended the establishment of a separate institution for rural credit that later became NABARD?", "B. Sivaraman Committee", "Narasimham Committee", "Urjit Patel Committee", "Kelkar Committee"),
        ("NABARD was established through which Act?", "NABARD Act, 1981", "RBI Act, 1934", "SEBI Act, 1992", "Banking Regulation Act, 1949"),
        ("Which institution took over the agricultural credit functions of RBI and the refinance functions of the Agricultural Refinance and Development Corporation when it was established?", "NABARD", "SIDBI", "EXIM Bank", "IRDAI"),
        ("Which institution was originally established as the Industrial Development Bank of India in 1964?", "IDBI", "NABARD", "SIDBI", "EXIM Bank"),
        ("Which institution was established in 1982 to provide specialised export-import financing?", "EXIM Bank of India", "NABARD", "SIDBI", "National Housing Bank"),
        ("Which institution was established in 1988 to promote housing finance institutions?", "National Housing Bank", "NABARD", "EXIM Bank", "SIDBI"),
        ("Which institution was established in 1987 as a specialised financial institution for housing finance?", "National Housing Bank", "Reserve Bank of India", "SEBI", "IRDAI"),
        ("Which Act established the Securities and Exchange Board of India as a statutory authority?", "SEBI Act, 1992", "RBI Act, 1934", "Companies Act, 2013", "Insurance Act, 1938"),
        ("Which Act regulates contracts in securities and stock exchanges in India?", "Securities Contracts (Regulation) Act, 1956", "RBI Act, 1934", "NABARD Act, 1981", "Banking Regulation Act, 1949"),
        ("Which Act provides the statutory framework for the regulation of insurance business in India?", "Insurance Act, 1938", "SEBI Act, 1992", "RBI Act, 1934", "NABARD Act, 1981"),
        ("Which Act established the Insurance Regulatory and Development Authority of India?", "IRDA Act, 1999", "SEBI Act, 1992", "RBI Act, 1934", "Banking Regulation Act, 1949"),
        ("Which Act established the Pension Fund Regulatory and Development Authority as a statutory body?", "PFRDA Act, 2013", "RBI Act, 1934", "SEBI Act, 1992", "NABARD Act, 1981"),
        ("Which institution is the principal regulator of the National Pension System?", "PFRDA", "RBI", "SEBI", "IRDAI"),
        ("Which scheme was launched to provide social security through life insurance coverage to eligible subscribers?", "Pradhan Mantri Jeevan Jyoti Bima Yojana", "Atal Pension Yojana", "PM-KISAN", "Stand-Up India"),
        ("Which scheme provides accident insurance coverage under a low-premium social security programme?", "Pradhan Mantri Suraksha Bima Yojana", "Pradhan Mantri Jeevan Jyoti Bima Yojana", "Atal Pension Yojana", "PM-KISAN"),
        ("Which scheme provides an assured minimum pension to eligible subscribers, subject to scheme conditions?", "Atal Pension Yojana", "PM-KISAN", "MUDRA Yojana", "Stand-Up India"),
        ("Which government scheme aims to provide institutional credit to street vendors?", "PM SVANidhi", "PM-KISAN", "Atal Pension Yojana", "PM Fasal Bima Yojana"),
        ("What is the main objective of the PM SVANidhi scheme?", "Provide working capital loans to eligible street vendors", "Provide crop insurance to farmers", "Provide pension to all citizens", "Finance large industrial projects"),
        ("Which scheme aims to promote entrepreneurship and self-employment through support for new enterprises?", "Prime Minister's Employment Generation Programme", "PM-KISAN", "Atal Pension Yojana", "PM Fasal Bima Yojana"),
        ("Which organisation implements the Prime Minister's Employment Generation Programme at the national level?", "Khadi and Village Industries Commission", "SEBI", "IRDAI", "NPCI"),
        ("Which institution is responsible for operating the Deposit Insurance and Credit Guarantee Corporation?", "Reserve Bank of India", "SEBI", "NABARD", "PFRDA"),
        ("Under the DICGC framework, what is the insured deposit limit per depositor per bank?", "₹5 lakh", "₹1 lakh", "₹10 lakh", "₹20 lakh"),
        ("Which institution is responsible for regulating payment systems in India under the Payment and Settlement Systems Act, 2007?", "Reserve Bank of India", "SEBI", "IRDAI", "PFRDA"),
        ("Which Act provides the legal framework for payment systems in India?", "Payment and Settlement Systems Act, 2007", "SEBI Act, 1992", "NABARD Act, 1981", "Companies Act, 2013"),
        ("Which institution operates the Aadhaar Enabled Payment System through the NPCI network?", "NPCI", "SEBI", "IRDAI", "EXIM Bank"),
        ("What is the primary purpose of the Financial Stability and Development Council?", "Coordinate financial-sector development and financial stability", "Prepare the Union Budget", "Regulate only agricultural exports", "Conduct national elections"),
        ("Which ministry chairs the Financial Stability and Development Council?", "Ministry of Finance", "Ministry of Agriculture", "Ministry of Education", "Ministry of External Affairs"),
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
                    "MCQ lesson covering Indian banking history, financial "
                    "institutions and government financial schemes."
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
