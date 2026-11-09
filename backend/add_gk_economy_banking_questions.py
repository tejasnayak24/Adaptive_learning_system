
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 177
LESSON_TITLE = "Indian Economy, Business, Banking and Financial Awareness"
TOPIC = "General Knowledge"

BANK = {
    "Easy": [
        ("What is the full form of GDP?", "Gross Domestic Product", "General Domestic Price", "Gross Development Plan", "General Development Product"),
        ("Which institution is India's central bank?", "Reserve Bank of India", "State Bank of India", "NABARD", "SEBI"),
        ("What is the currency of India?", "Indian Rupee", "Dollar", "Pound", "Yen"),
        ("Which organisation issues currency notes in India?", "Reserve Bank of India", "State Bank of India", "SEBI", "NABARD"),
        ("What does ATM stand for?", "Automated Teller Machine", "Automatic Transfer Method", "Account Transaction Machine", "Automated Tax Management"),
        ("Which bank is commonly known as SBI?", "State Bank of India", "South Bank of India", "Standard Bank of India", "Small Bank of India"),
        ("What is a savings account mainly used for?", "Saving money and earning interest", "Printing currency", "Paying government salaries", "Issuing shares"),
        ("What does a cheque represent?", "A written instruction to a bank to pay money", "A type of currency note", "A government bond", "A credit card"),
        ("Which tax is generally levied on the supply of goods and services in India?", "GST", "Income tax only", "Property tax only", "Road tax only"),
        ("What is the full form of GST?", "Goods and Services Tax", "General Sales Transaction", "Government Service Tariff", "Goods Supply Transfer"),
        ("What is inflation?", "A general rise in prices", "A general fall in prices", "An increase in rainfall", "A decrease in population"),
        ("Which institution regulates the securities market in India?", "SEBI", "RBI", "NABARD", "IRDAI"),
        ("What does PAN stand for?", "Permanent Account Number", "Personal Account Name", "Public Access Number", "Payment Allocation Note"),
        ("Which institution provides insurance regulation in India?", "IRDAI", "SEBI", "RBI", "NITI Aayog"),
        ("What is a loan?", "Money borrowed that must be repaid", "Money received as a gift", "A type of tax", "A bank deposit"),
        ("What is a fixed deposit?", "Money deposited for a fixed period at an agreed interest rate", "Money kept only in a current account", "A type of insurance claim", "A share in a company"),
        ("Which of these is a public sector bank in India?", "Punjab National Bank", "HDFC Bank", "ICICI Bank", "Axis Bank"),
        ("What is the main function of a bank?", "Accept deposits and provide loans", "Manufacture goods", "Conduct elections", "Build highways"),
        ("What does UPI stand for?", "Unified Payments Interface", "Universal Payment Institution", "United Payment Information", "Unified Purchase Index"),
        ("Which organisation operates the UPI payment system in India?", "National Payments Corporation of India", "Reserve Bank of India directly", "SEBI", "NABARD"),
        ("What is a debit card primarily used for?", "Making payments using funds in a linked account", "Borrowing unlimited money", "Issuing currency", "Buying company shares"),
        ("What is a credit card?", "A payment card that allows borrowing up to a credit limit", "A savings account passbook", "A government identity card", "A fixed deposit certificate"),
        ("Which sector includes banking and insurance services?", "Service sector", "Agricultural sector", "Mining sector", "Manufacturing sector"),
        ("What is a budget?", "A financial plan of income and expenditure", "A list of company employees", "A type of bank account", "A stock exchange"),
        ("Which organisation prepares and presents the Union Budget in India?", "Ministry of Finance", "Ministry of Agriculture", "Ministry of Defence", "Ministry of Education"),
        ("What is the full form of ATM PIN?", "Personal Identification Number", "Private Internet Name", "Payment Information Note", "Personal Investment Number"),
        ("What is a stock exchange?", "A marketplace for buying and selling securities", "A place for storing food grains", "A currency printing centre", "A government tax office"),
        ("Which of these is an example of an online payment method?", "UPI", "Barter", "Cheque book printing", "Postal stamp"),
        ("What is the main purpose of insurance?", "Protection against specified financial risks", "Guaranteed profit from shares", "Avoiding all taxes", "Increasing currency supply"),
        ("What does EMI stand for?", "Equated Monthly Instalment", "Estimated Money Investment", "Electronic Market Index", "Equal Money Insurance"),
    ],

    "Medium": [
        ("What is the primary objective of monetary policy in India?", "Maintaining price stability while keeping growth in mind", "Managing school admissions", "Regulating agricultural exports only", "Setting company salaries"),
        ("Who chairs the Monetary Policy Committee of India?", "RBI Governor", "Finance Secretary", "Prime Minister", "SEBI Chairperson"),
        ("What is the repo rate?", "Rate at which RBI lends short-term funds to banks against eligible securities", "Rate banks pay on savings accounts", "Rate of GST", "Rate of income tax"),
        ("What is the reverse repo rate traditionally associated with?", "Rate at which RBI borrows funds from banks", "Rate at which banks lend to customers", "Rate of company taxation", "Rate of currency exchange"),
        ("What is CRR?", "Cash Reserve Ratio", "Credit Recovery Rate", "Capital Return Ratio", "Currency Regulation Reserve"),
        ("What does SLR stand for?", "Statutory Liquidity Ratio", "Standard Lending Rate", "Special Loan Reserve", "Savings Liability Return"),
        ("Which institution is primarily responsible for regulating banks in India?", "Reserve Bank of India", "Election Commission", "SEBI alone", "NITI Aayog"),
        ("What is the main role of NABARD?", "Supporting agriculture and rural development finance", "Regulating stock exchanges", "Issuing passports", "Managing national highways"),
        ("What is the main function of SIDBI?", "Promoting and financing the development of MSMEs", "Managing India's foreign policy", "Regulating insurance companies", "Conducting population census"),
        ("What does MSME stand for?", "Micro, Small and Medium Enterprises", "Medium, Standard and Major Enterprises", "Micro, State and Manufacturing Economy", "Modern Small Market Enterprises"),
        ("What is fiscal policy?", "Government policy relating to taxation and public expenditure", "RBI policy on bank lending only", "Policy for managing company employees", "Policy for controlling rainfall"),
        ("What is a fiscal deficit?", "Excess of total government expenditure over total receipts excluding borrowings", "Excess of exports over imports", "Excess of savings over investments", "Excess of tax revenue over expenditure"),
        ("What is a trade deficit?", "When the value of imports exceeds the value of exports", "When exports exceed imports", "When government spending exceeds revenue", "When savings exceed investment"),
        ("What is the balance of payments?", "A record of economic transactions between residents of a country and the rest of the world", "A record of only domestic taxes", "A list of bank deposits", "A record of government employees"),
        ("What is foreign direct investment?", "Investment involving a lasting interest in an enterprise in another country", "A domestic savings account", "A short-term personal loan", "A government pension"),
        ("What is disinvestment?", "Sale of government stake in a public sector enterprise", "Purchase of additional government shares", "Increase in income tax", "Cancellation of all bank loans"),
        ("Which tax is generally classified as a direct tax in India?", "Income tax", "GST", "Customs duty", "Excise duty"),
        ("Which of these is an indirect tax?", "GST", "Personal income tax", "Corporate income tax", "Capital gains tax"),
        ("What is the primary purpose of the Public Distribution System?", "Providing essential commodities to eligible beneficiaries", "Providing stock market loans", "Managing foreign exchange", "Funding private airlines"),
        ("Which body recommends the distribution of certain tax revenues between the Union and states?", "Finance Commission", "Election Commission", "UPSC", "SEBI"),
        ("What is the full form of NPCI?", "National Payments Corporation of India", "National Public Credit Institution", "New Payment Council of India", "National Private Currency Institute"),
        ("What is NEFT?", "National Electronic Funds Transfer", "National Exchange Finance Transaction", "New Electronic Financial Tax", "National Equity Fund Transfer"),
        ("What is RTGS mainly used for?", "Real-time gross settlement of high-value transfers", "Printing bank statements", "Buying insurance policies", "Opening demat accounts"),
        ("What is a demat account used for?", "Holding securities in electronic form", "Depositing physical cash only", "Receiving salary only", "Paying electricity bills only"),
        ("What does IPO stand for?", "Initial Public Offering", "International Purchase Order", "Investment Payment Option", "Internal Profit Organisation"),
        ("What is a mutual fund?", "A pooled investment vehicle managed according to its scheme objectives", "A type of savings bank account", "A government tax receipt", "A personal loan"),
        ("What is the Nifty 50?", "An index representing 50 major companies listed on NSE", "A list of 50 banks", "A government savings scheme", "A tax collection system"),
        ("What is the Sensex?", "A benchmark index of the Bombay Stock Exchange", "An RBI lending rate", "A government bond", "A foreign exchange reserve"),
        ("What is compound interest?", "Interest calculated on principal and accumulated interest", "Interest calculated only on the original principal", "A tax on bank deposits", "A fee charged for withdrawals"),
        ("What is financial inclusion?", "Ensuring access to useful and affordable financial services", "Restricting banking services to large companies", "Eliminating all cash transactions", "Providing loans only to exporters"),
    ],

    "Hard": [
        ("Which committee recommended the establishment of the Monetary Policy Committee framework in India?", "Urjit Patel Committee", "Narasimham Committee", "Kelkar Committee", "Rangarajan Committee"),
        ("What is the main purpose of the RBI's inflation-targeting framework?", "Maintaining price stability", "Fixing the prices of all products", "Guaranteeing stock market returns", "Setting agricultural wages"),
        ("What is the inflation target framework in India expressed in terms of?", "Consumer Price Index inflation", "Wholesale exports", "GDP growth alone", "Foreign exchange reserves"),
        ("What does the term 'open market operations' mean in monetary policy?", "RBI buying or selling government securities", "Banks opening new branches", "Companies selling products abroad", "Government purchasing private land"),
        ("What is the main objective of the Marginal Standing Facility?", "Providing banks with an overnight liquidity facility from RBI", "Providing long-term housing loans to individuals", "Financing exports directly", "Offering insurance to depositors"),
        ("What is the Bank Rate?", "A rate at which RBI is prepared to buy or rediscount eligible bills or provide specified lending", "The interest rate on every savings account", "The rate of GST on banking services", "The rate charged by private moneylenders"),
        ("Which committee is associated with major banking sector reforms in India during the 1990s?", "Narasimham Committee", "Mandal Commission", "Sarkaria Commission", "Balwant Rai Mehta Committee"),
        ("What is priority sector lending?", "Bank lending to specified sectors considered important for inclusive development", "Loans given only to large corporations", "Loans exclusively for stock trading", "Loans provided only to government employees"),
        ("Which institution operates the Credit Guarantee Fund Trust for Micro and Small Enterprises jointly with the Government of India?", "CGTMSE", "SEBI", "IRDAI", "NITI Aayog"),
        ("What is the main purpose of the Deposit Insurance and Credit Guarantee Corporation?", "Providing deposit insurance to eligible bank depositors", "Insuring company shares against market losses", "Guaranteeing all personal loans", "Regulating stock exchanges"),
        ("What is the maximum deposit insurance cover per depositor per bank provided by DICGC?", "₹5 lakh", "₹1 lakh", "₹10 lakh", "₹50 lakh"),
        ("What is the main purpose of the Insolvency and Bankruptcy Code, 2016?", "Providing a time-bound framework for insolvency resolution", "Regulating agricultural production", "Fixing interest rates on savings accounts", "Managing national highways"),
        ("Which authority regulates the securities market and protects investors in India?", "SEBI", "RBI", "NABARD", "CAG"),
        ("What is the primary role of the Securities Appellate Tribunal?", "Hearing appeals against specified orders of financial regulators", "Printing currency notes", "Managing government expenditure", "Approving the Union Budget"),
        ("What is the primary function of the Comptroller and Auditor General of India?", "Auditing government accounts", "Regulating private banks", "Setting monetary policy", "Managing stock exchanges"),
        ("Which account is used to record foreign investment, external loans and other capital transactions in the balance of payments?", "Capital and financial account", "Current account only", "Revenue account", "Household account"),
        ("What does a current account deficit indicate?", "Current account payments exceed current account receipts", "Exports always exceed imports", "Government revenue exceeds expenditure", "Domestic savings exceed investment"),
        ("What is the purpose of sterilisation by a central bank?", "Offsetting the domestic liquidity impact of foreign exchange interventions", "Preventing all imports", "Fixing the price of gold", "Eliminating income tax"),
        ("What is the difference between nominal GDP and real GDP?", "Real GDP adjusts for price changes", "Nominal GDP excludes services", "Real GDP excludes agriculture", "Nominal GDP is always lower"),
        ("What is GDP deflator used for?", "Measuring price changes in all domestically produced final goods and services", "Measuring only unemployment", "Measuring only export volumes", "Calculating bank reserves"),
        ("Which measure includes the value of final goods and services produced within a country's domestic territory?", "GDP", "GNP only", "Personal savings", "Fiscal deficit"),
        ("What is the primary objective of the FRBM framework in India?", "Promoting fiscal discipline and managing government deficits", "Regulating private insurance companies", "Controlling agricultural exports", "Managing school education"),
        ("What is the full form of FRBM?", "Fiscal Responsibility and Budget Management", "Financial Regulation and Banking Management", "Federal Revenue and Budget Mechanism", "Fiscal Reform and Banking Mission"),
        ("Which institution compiles India's national income estimates?", "National Statistical Office", "Reserve Bank of India", "SEBI", "NABARD"),
        ("What is the primary function of the National Financial Reporting Authority?", "Overseeing accounting and auditing standards for specified entities", "Regulating agricultural credit", "Issuing currency notes", "Managing public distribution shops"),
        ("What is the purpose of the Financial Intelligence Unit-India?", "Receiving and analysing information related to suspicious financial transactions", "Setting repo rates", "Regulating railway fares", "Approving foreign university admissions"),
        ("Which law is primarily concerned with preventing money laundering in India?", "Prevention of Money Laundering Act", "Companies Act only", "Consumer Protection Act", "Right to Information Act"),
        ("What does the term 'non-performing asset' generally refer to in banking?", "A loan or advance that has ceased to generate income as classified under applicable rules", "A bank's profitable investment", "A fully repaid loan", "A savings account with regular deposits"),
        ("What is the primary purpose of the SARFAESI Act, 2002?", "Enabling secured creditors to enforce security interests under specified conditions", "Regulating stock exchanges", "Setting agricultural minimum support prices", "Managing foreign trade agreements"),
        ("What is the main purpose of the Unified Payments Interface?", "Enabling instant bank-to-bank payments through a single interface", "Providing long-term investment guarantees", "Replacing all bank accounts", "Issuing physical currency"),
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

            if not all(isinstance(value, str) and value.strip() for value in item):
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
                "Learn about the Indian economy, banking system, financial institutions, taxation, monetary policy, markets and financial awareness."
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
        print("GK TOPIC 17 INSERTED SUCCESSFULLY")
        print("Indian Economy, Business, Banking and Financial Awareness")
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
