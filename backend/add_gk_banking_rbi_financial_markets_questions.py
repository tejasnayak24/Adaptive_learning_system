
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 191
LESSON_TITLE = "Banking, RBI, Financial Markets and Digital Payments"
TOPIC = "General Knowledge"

BANK = {
    "Easy": [
        ("What is the full form of RBI?", "Reserve Bank of India", "Regional Bank of India", "Rural Banking Institution", "Reserve Banking Institute"),
        ("When was the Reserve Bank of India established?", "1935", "1947", "1950", "1969"),
        ("Which is the central bank of India?", "Reserve Bank of India", "State Bank of India", "Punjab National Bank", "Bank of Baroda"),
        ("Where is the headquarters of RBI located?", "Mumbai", "New Delhi", "Kolkata", "Chennai"),
        ("Which institution issues most currency notes in India?", "Reserve Bank of India", "State Bank of India", "SEBI", "NABARD"),
        ("Which Indian currency note is issued by the Government of India rather than the RBI?", "One-rupee note", "Ten-rupee note", "Hundred-rupee note", "Five-hundred-rupee note"),
        ("What is the full form of ATM?", "Automated Teller Machine", "Automatic Transfer Method", "Account Transaction Machine", "Automated Trade Management"),
        ("What is the full form of IFSC?", "Indian Financial System Code", "International Fund Security Code", "Indian Foreign Savings Code", "Internal Finance Service Code"),
        ("What is the full form of NEFT?", "National Electronic Funds Transfer", "National Exchange Finance Transaction", "New Electronic Fund Technology", "National Economy Fund Transfer"),
        ("What is the full form of RTGS?", "Real Time Gross Settlement", "Rapid Transfer Government System", "Real Transaction Guarantee Service", "Reserve Transfer General System"),
        ("What is the full form of UPI?", "Unified Payments Interface", "Universal Payment Institution", "United Payment Integration", "Unified Processing Information"),
        ("Which organisation operates UPI in India?", "National Payments Corporation of India", "SEBI", "NABARD", "IRDAI"),
        ("Which organisation regulates the securities market in India?", "SEBI", "RBI", "NABARD", "IRDAI"),
        ("What is the full form of SEBI?", "Securities and Exchange Board of India", "Stock Exchange Banking Institution", "Securities and Economic Bank of India", "State Exchange Board of India"),
        ("Which bank is India's largest public sector bank?", "State Bank of India", "Punjab National Bank", "Canara Bank", "Bank of India"),
        ("What is a savings bank account mainly used for?", "Saving money and earning interest", "Printing currency", "Conducting elections", "Issuing government laws"),
        ("What is a fixed deposit?", "A deposit kept for a specified period at an agreed interest rate", "A loan without repayment", "A current account for businesses", "A stock market investment"),
        ("What is a recurring deposit?", "A deposit in which a fixed amount is invested regularly", "A one-time share purchase", "A loan taken from RBI", "A government tax payment"),
        ("What is a cheque?", "A written instruction to a bank to pay a specified amount", "A type of currency note", "A government bond", "A debit card"),
        ("What is a debit card linked to?", "The cardholder's bank account", "A stock exchange account only", "A government office", "A loan application"),
        ("What is a credit card primarily used for?", "Making purchases using a credit facility", "Withdrawing only fixed deposits", "Printing currency", "Opening a savings account automatically"),
        ("What is the full form of KYC?", "Know Your Customer", "Keep Your Cash", "Know Your Credit", "Key Yield Certificate"),
        ("What is the main purpose of KYC in banking?", "Verifying customer identity", "Increasing currency production", "Fixing stock prices", "Calculating GDP"),
        ("Which institution supports agriculture and rural development through refinance and development activities?", "NABARD", "SEBI", "IRDAI", "EXIM Bank"),
        ("What is the full form of NABARD?", "National Bank for Agriculture and Rural Development", "National Association of Banking and Rural Deposits", "New Agricultural Bank and Rural Department", "National Authority for Business and Rural Development"),
        ("What is the full form of MICR?", "Magnetic Ink Character Recognition", "Money Identification and Cash Record", "Machine Integrated Credit Register", "Magnetic Information Currency Reading"),
        ("What is a bank loan?", "Money borrowed that must be repaid according to agreed terms", "Money received as a gift", "A type of tax", "A currency note"),
        ("What is internet banking?", "Banking services accessed through the internet", "Banking performed only using paper forms", "A stock exchange", "A currency printing system"),
        ("What is mobile banking?", "Banking services accessed through a mobile device", "A bank branch on a train", "A currency exchange counter", "A government savings bond"),
        ("What is the full form of PIN in banking?", "Personal Identification Number", "Payment Information Network", "Private Internet Number", "Personal Investment Note"),
    ],

    "Medium": [
        ("Which RBI department is primarily responsible for regulating and supervising banks?", "Department of Regulation and Department of Supervision", "Department of Agriculture", "Department of External Affairs", "Department of Statistics only"),
        ("What is the repo rate?", "The rate at which RBI lends short-term funds to banks against eligible securities", "The rate banks pay on every savings account", "The rate of income tax", "The rate charged by stock exchanges"),
        ("What is the Cash Reserve Ratio (CRR)?", "The percentage of a bank's net demand and time liabilities maintained as cash with RBI", "The percentage of loans given to farmers", "The percentage of profits paid as tax", "The amount of cash held by customers"),
        ("What is the Statutory Liquidity Ratio (SLR)?", "The proportion of a bank's net demand and time liabilities maintained in specified liquid assets", "The tax rate on bank deposits", "The rate at which RBI lends to the government", "The percentage of foreign investment"),
        ("What is the main purpose of the Monetary Policy Committee?", "To determine the policy interest rate required to achieve the inflation target", "To prepare the Union Budget", "To regulate insurance companies", "To conduct parliamentary elections"),
        ("How many members are there in India's Monetary Policy Committee?", "Six", "Four", "Five", "Eight"),
        ("Who chairs the Monetary Policy Committee?", "RBI Governor", "Finance Minister", "Prime Minister", "SEBI Chairperson"),
        ("What is the reverse repo rate traditionally associated with?", "The rate at which RBI absorbs liquidity from banks", "The rate at which RBI lends to businesses", "The rate of GST", "The rate paid on government bonds"),
        ("What is the marginal standing facility (MSF)?", "A facility through which scheduled banks can borrow overnight funds from RBI under specified conditions", "A facility for opening stock exchanges", "A government pension scheme", "A type of savings account"),
        ("What is the bank rate?", "The rate at which RBI is prepared to buy or rediscount eligible bills or other commercial paper under its framework", "The interest rate on every savings account", "The rate of GST on banking services", "The rate at which customers withdraw cash"),
        ("Which payment system is designed for large-value, real-time, gross settlement of transactions?", "RTGS", "NEFT", "IMPS", "UPI"),
        ("Which payment system processes fund transfers in batches at regular intervals?", "NEFT", "RTGS", "ATM", "Debit card"),
        ("Which electronic payment service supports immediate interbank fund transfers in India?", "IMPS", "Demand draft", "Cheque clearing only", "Fixed deposit"),
        ("What is the full form of IMPS?", "Immediate Payment Service", "Indian Money Processing System", "International Monetary Payment Service", "Instant Merchant Payment Scheme"),
        ("What is the main difference between NEFT and RTGS?", "NEFT processes transfers in batches while RTGS settles transactions individually in real time", "NEFT is only for international transfers", "RTGS is only for cash deposits", "Both are paper-based systems"),
        ("What is a Non-Performing Asset (NPA)?", "A loan or advance that has ceased to generate income as classified under applicable RBI norms", "A profitable bank investment", "A government savings scheme", "A fully repaid loan"),
        ("Generally, when does a term loan become an NPA under RBI income-recognition norms?", "When principal or interest remains overdue for more than 90 days", "After 15 days", "After 30 days", "After one year in every case"),
        ("What is the purpose of deposit insurance in India?", "To protect eligible bank deposits up to the insured limit", "To guarantee unlimited returns on investments", "To insure stock market profits", "To provide free loans"),
        ("Which organisation provides deposit insurance in India?", "Deposit Insurance and Credit Guarantee Corporation", "SEBI", "NABARD", "EXIM Bank"),
        ("What is the maximum deposit insurance cover per depositor per bank in India, including principal and interest?", "₹5 lakh", "₹1 lakh", "₹10 lakh", "₹20 lakh"),
        ("What is a demand draft?", "A prepaid negotiable instrument issued by a bank", "A type of credit card", "A stock market order", "A government tax receipt"),
        ("What is the main purpose of a bank's IFSC code?", "To identify a bank branch for electronic fund transfers", "To identify a customer's income tax slab", "To determine a loan interest rate", "To identify a stock exchange"),
        ("What is the full form of NPCI?", "National Payments Corporation of India", "National Public Credit Institution", "New Payment Council of India", "National Private Currency Institute"),
        ("Which of the following is a digital payment system based on UPI infrastructure?", "BHIM", "SWIFT only", "MICR", "CIBIL"),
        ("What is the full form of BHIM?", "Bharat Interface for Money", "Banking Hub for Indian Markets", "Basic High-speed Internet Money", "Bharat Housing Investment Model"),
        ("What does the term financial inclusion mean?", "Ensuring access to useful and affordable financial services", "Restricting banking services to large companies", "Eliminating all digital payments", "Providing loans only to government departments"),
        ("Which scheme was launched to promote access to basic bank accounts?", "Pradhan Mantri Jan Dhan Yojana", "Make in India", "Swachh Bharat Mission", "Startup India"),
        ("What is the purpose of the Credit Information Bureau India Limited (CIBIL)?", "Maintaining credit information and generating credit reports and scores", "Issuing currency notes", "Regulating insurance premiums", "Managing government tax collection"),
        ("What does a credit score generally indicate?", "A person's credit history and creditworthiness", "A person's educational qualification", "A company's market share", "The country's GDP"),
        ("What is the primary function of a stock exchange?", "Providing a regulated platform for trading securities", "Issuing currency notes", "Providing agricultural subsidies", "Collecting income tax"),
    ],

    "Hard": [
        ("Which RBI Act provision empowers the RBI to regulate the issue of bank notes?", "Section 22 of the RBI Act, 1934", "Section 5 of the Banking Regulation Act", "Article 110 of the Constitution", "Section 80 of the Companies Act"),
        ("Which legislation provides the principal statutory framework for regulating banking companies in India?", "Banking Regulation Act, 1949", "Companies Act, 2013 only", "SEBI Act, 1992", "Negotiable Instruments Act, 1881 only"),
        ("Which section of the Banking Regulation Act, 1949 deals with licensing of banking companies?", "Section 22", "Section 5", "Section 35", "Section 45"),
        ("Which section of the RBI Act, 1934 provides for the constitution of the Monetary Policy Committee?", "Section 45ZB", "Section 22", "Section 17", "Section 26"),
        ("What is the primary objective of inflation targeting under India's monetary policy framework?", "Maintain price stability while keeping the objective of growth in mind", "Fix all prices in the economy", "Eliminate all government borrowing", "Guarantee a fixed exchange rate"),
        ("Which committee is associated with the recommendation of a flexible inflation-targeting framework in India?", "Urjit Patel Committee", "Narasimham Committee", "Kelkar Committee", "Sarkaria Commission"),
        ("What is the Standing Deposit Facility (SDF) used for?", "Absorbing liquidity from banks without requiring collateral", "Providing long-term housing loans", "Issuing government bonds to citizens", "Insuring bank deposits"),
        ("What is the Liquidity Adjustment Facility (LAF)?", "A framework through which RBI manages short-term liquidity using repo and related instruments", "A system for collecting income tax", "A stock exchange settlement mechanism", "A government pension programme"),
        ("What is the primary purpose of Open Market Operations (OMO) by RBI?", "Buying and selling government securities to manage liquidity", "Regulating agricultural prices", "Issuing company shares", "Setting insurance premiums"),
        ("When RBI purchases government securities through open market operations, what is the usual liquidity effect?", "It injects liquidity into the banking system", "It absorbs liquidity from the banking system", "It automatically increases GST", "It reduces the number of bank branches"),
        ("What is sterilisation in monetary policy?", "Offsetting the domestic liquidity impact of foreign exchange intervention", "Closing all commercial banks", "Cancelling government securities", "Replacing all currency notes"),
        ("What is the primary role of the Clearing Corporation of India Limited (CCIL)?", "Providing clearing and settlement services in financial markets", "Regulating insurance companies", "Issuing currency notes", "Managing agricultural credit"),
        ("Which institution operates the Centralised Payment Systems such as NEFT and RTGS in India?", "Reserve Bank of India", "SEBI", "NABARD", "IRDAI"),
        ("What is the primary function of the National Financial Switch (NFS)?", "Interconnecting ATMs of participating banks", "Issuing government bonds", "Regulating mutual funds", "Managing stock market indices"),
        ("What is the full form of CTS in cheque processing?", "Cheque Truncation System", "Cash Transfer Service", "Credit Transaction Scheme", "Cheque Tracking Software"),
        ("What is the main advantage of cheque truncation?", "It enables electronic processing using cheque images instead of physical movement of cheques", "It eliminates the need for bank accounts", "It guarantees unlimited cheque payments", "It converts cheques into currency notes"),
        ("What does the term systemic risk refer to in financial markets?", "Risk that disruption in one part of the financial system spreads and threatens the wider system", "Risk limited to one individual savings account", "Risk of a single failed ATM transaction", "Risk of a change in one company's logo"),
        ("What is the primary purpose of capital adequacy requirements for banks?", "Ensure banks maintain sufficient capital to absorb unexpected losses", "Ensure banks lend only to governments", "Guarantee profits to shareholders", "Prevent customers from withdrawing deposits"),
        ("What is the full form of CRAR in banking?", "Capital to Risk-Weighted Assets Ratio", "Cash Reserve and Assets Register", "Credit Risk Assessment Report", "Capital Return and Revenue"),
        ("What does the Basel framework primarily establish?", "International standards for bank capital, liquidity and risk management", "Rules for international elections", "Global agricultural price controls", "International copyright law"),
        ("What is the purpose of the Prompt Corrective Action (PCA) framework for banks?", "Enable supervisory action when banks show specified financial weaknesses", "Provide free loans to customers", "Regulate stock exchange trading hours", "Guarantee bank dividends"),
        ("What is the SARFAESI Act, 2002 mainly concerned with?", "Enforcement of security interests and recovery of secured loans", "Regulation of insurance companies", "Control of foreign trade tariffs", "Issue of currency notes"),
        ("What does the Insolvency and Bankruptcy Code, 2016 aim to provide?", "A time-bound framework for insolvency resolution and bankruptcy", "A framework for fixing retail prices", "A system for issuing debit cards", "A system for conducting elections"),
        ("What is the primary purpose of the Negotiable Instruments Act, 1881?", "Provide a legal framework for negotiable instruments such as promissory notes, bills of exchange and cheques", "Regulate mutual funds", "Establish the RBI", "Regulate insurance premiums"),
        ("Which market deals primarily with the issuance and trading of short-term debt instruments?", "Money market", "Capital market", "Commodity market only", "Real estate market"),
        ("Which of the following is generally considered a money market instrument?", "Treasury Bill", "Equity share", "Long-term corporate debenture", "Real estate investment"),
        ("What is a certificate of deposit?", "A negotiable money market instrument issued by eligible banks and financial institutions", "A property ownership document", "A government identity card", "A share in a stock exchange"),
        ("What is commercial paper?", "An unsecured short-term money market instrument issued by eligible entities", "A secured long-term housing loan", "A government currency note", "A bank passbook"),
        ("What is the primary difference between the primary and secondary markets?", "Primary markets issue new securities while secondary markets trade existing securities", "Primary markets trade only currencies", "Secondary markets issue all new government currency", "There is no difference"),
        ("Which institution is responsible for regulating India's government securities market and monetary policy operations?", "Reserve Bank of India", "Election Commission of India", "NITI Aayog", "National Human Rights Commission"),
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
                    "MCQ lesson covering banking, RBI, financial markets "
                    "and digital payments."
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
