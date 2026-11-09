
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 190
LESSON_TITLE = "Indian Economy, Budget, Taxation and Economic Policies"
TOPIC = "General Knowledge"

BANK = {
    "Easy": [
        ("Which institution is responsible for issuing currency notes in India, except the one-rupee note?", "Reserve Bank of India", "State Bank of India", "Finance Ministry", "NITI Aayog"),
        ("Which institution is India's central bank?", "Reserve Bank of India", "State Bank of India", "NABARD", "SEBI"),
        ("What is the currency of India?", "Indian Rupee", "US Dollar", "Pound Sterling", "Euro"),
        ("Which organisation regulates the securities market in India?", "SEBI", "RBI", "NABARD", "IRDAI"),
        ("What does GDP stand for?", "Gross Domestic Product", "General Domestic Production", "Gross Development Plan", "General Development Product"),
        ("Which sector includes agriculture, forestry and fishing?", "Primary sector", "Secondary sector", "Tertiary sector", "Quaternary sector"),
        ("Which sector includes manufacturing and construction?", "Secondary sector", "Primary sector", "Tertiary sector", "Public sector"),
        ("Which sector includes banking, transport and education services?", "Tertiary sector", "Primary sector", "Secondary sector", "Agricultural sector"),
        ("Which tax is levied on the supply of goods and services in India?", "Goods and Services Tax", "Income Tax", "Wealth Tax", "Property Tax"),
        ("What is the full form of GST?", "Goods and Services Tax", "General Sales Tariff", "Government Service Tax", "Gross Supply Tax"),
        ("Which ministry presents the Union Budget in Parliament?", "Ministry of Finance", "Ministry of Commerce", "Ministry of Agriculture", "Ministry of Home Affairs"),
        ("Who presents the Union Budget in Parliament on behalf of the government?", "Union Finance Minister", "RBI Governor", "President", "Lok Sabha Speaker"),
        ("What is a budget?", "An estimate of income and expenditure", "A list of government employees", "A bank account statement", "A record of imports only"),
        ("Which organisation replaced the Planning Commission?", "NITI Aayog", "Finance Commission", "RBI", "SEBI"),
        ("What is the full form of NITI in NITI Aayog?", "National Institution for Transforming India", "National Institute of Trade and Industry", "New Indian Technology Institution", "National Investment and Trade Initiative"),
        ("Which bank is commonly known as India's largest public sector bank?", "State Bank of India", "Punjab National Bank", "Bank of Baroda", "Canara Bank"),
        ("Which institution provides development finance and support to agriculture and rural development?", "NABARD", "SEBI", "IRDAI", "EXIM Bank"),
        ("What does ATM stand for?", "Automated Teller Machine", "Automatic Transfer Method", "Any Time Money", "Account Transfer Machine"),
        ("What is inflation?", "A general rise in prices", "A general fall in prices", "A rise in exports only", "A fall in population"),
        ("What is deflation?", "A sustained fall in the general price level", "A sustained rise in prices", "An increase in government spending", "An increase in exports"),
        ("Which tax is generally levied directly on an individual's income?", "Income Tax", "GST", "Customs Duty", "Excise Duty"),
        ("Which tax is generally classified as an indirect tax?", "GST", "Income Tax", "Corporate Income Tax", "Capital Gains Tax"),
        ("What is the main purpose of taxation?", "To raise revenue for public expenditure", "To eliminate all businesses", "To stop international trade", "To replace currency"),
        ("What is the meaning of a fiscal deficit?", "Government expenditure exceeds its receipts excluding borrowings", "Government revenue exceeds expenditure", "Exports exceed imports", "Imports equal exports"),
        ("What is the main function of a commercial bank?", "Accept deposits and provide loans", "Print currency notes", "Conduct national elections", "Prepare the Union Budget"),
        ("Which institution is responsible for monetary policy in India?", "Reserve Bank of India", "SEBI", "NABARD", "NITI Aayog"),
        ("What is the full form of UPI?", "Unified Payments Interface", "Universal Payment Institution", "United Payment Integration", "Unified Banking Investment"),
        ("Which organisation operates the UPI platform in India?", "National Payments Corporation of India", "Reserve Bank of India alone", "SEBI", "NABARD"),
        ("What is the main objective of the Make in India initiative?", "Encourage manufacturing in India", "Promote only agricultural exports", "Replace all banks", "Reduce school enrolment"),
        ("Which scheme aims to promote financial inclusion by providing access to bank accounts?", "Pradhan Mantri Jan Dhan Yojana", "Swachh Bharat Mission", "Beti Bachao Beti Padhao", "Digital India"),
    ],

    "Medium": [
        ("Which organisation calculates India's national income estimates?", "National Statistical Office", "SEBI", "NABARD", "Election Commission"),
        ("Which of the following is included in GDP?", "Value of final goods and services produced within a country", "Only government tax revenue", "Only exports", "Only agricultural production"),
        ("What is per capita income?", "Average income per person", "Total government revenue", "Total exports of a country", "Income earned only by companies"),
        ("What is GNP?", "Gross National Product", "General National Production", "Gross Net Product", "Government National Plan"),
        ("Which measure includes the income earned by a country's residents, including net factor income from abroad?", "Gross National Income", "Gross Domestic Product only", "Fiscal deficit", "Consumer Price Index"),
        ("Which index is commonly used to measure retail inflation in India?", "Consumer Price Index", "Index of Industrial Production", "Sensex", "Nifty"),
        ("Which index measures changes in wholesale prices?", "Wholesale Price Index", "Consumer Price Index", "Human Development Index", "Nifty 50"),
        ("Which institution announces the policy repo rate in India?", "Monetary Policy Committee of the RBI", "SEBI", "Finance Commission", "NABARD"),
        ("What is the repo rate?", "The rate at which RBI lends short-term funds to banks against eligible securities", "The rate at which banks lend to customers for housing", "The rate of GST", "The rate paid on all savings accounts"),
        ("What is the reverse repo rate traditionally associated with?", "The rate at which RBI absorbs funds from banks", "The rate at which RBI lends to businesses", "The rate of income tax", "The rate of customs duty"),
        ("What is the Cash Reserve Ratio (CRR)?", "The share of a bank's net demand and time liabilities kept as cash with RBI", "The share of bank profits paid as tax", "The amount of cash held by customers", "The percentage of loans that must be given to farmers"),
        ("What is the Statutory Liquidity Ratio (SLR)?", "The proportion of a bank's net demand and time liabilities maintained in specified liquid assets", "The tax rate on bank deposits", "The interest rate charged by RBI", "The amount of foreign currency held by exporters"),
        ("Which institution regulates insurance companies in India?", "IRDAI", "SEBI", "NABARD", "PFRDA"),
        ("Which institution regulates pension funds in India?", "PFRDA", "SEBI", "IRDAI", "NABARD"),
        ("Which institution regulates and develops the securities market in India?", "SEBI", "RBI", "NITI Aayog", "NABARD"),
        ("Which organisation is responsible for export-import finance and promotion in India?", "EXIM Bank", "NABARD", "SIDBI", "Regional Rural Bank"),
        ("Which institution primarily supports the financing and development of micro, small and medium enterprises?", "SIDBI", "SEBI", "IRDAI", "FCI"),
        ("What is the main purpose of the Minimum Support Price (MSP)?", "To provide a price assurance mechanism to farmers for notified crops", "To fix the price of all manufactured goods", "To determine income tax rates", "To regulate stock exchanges"),
        ("Which organisation recommends Minimum Support Prices to the government?", "Commission for Agricultural Costs and Prices", "Reserve Bank of India", "SEBI", "Finance Commission"),
        ("Which body is responsible for maintaining India's central foodgrain buffer stocks and undertaking foodgrain procurement and distribution functions?", "Food Corporation of India", "NABARD", "SEBI", "EXIM Bank"),
        ("What is disinvestment?", "Sale of government stake in a public sector enterprise", "Increase in government ownership", "Printing additional currency", "Cancellation of all private companies"),
        ("What is privatisation?", "Transfer of ownership or control from the public sector to the private sector", "Transfer of private firms to the government", "Increase in import duties", "Reduction in bank deposits"),
        ("What is the balance of trade?", "Difference between the value of merchandise exports and imports", "Difference between government revenue and expenditure", "Total foreign exchange reserves", "Total domestic savings"),
        ("What does the current account of the balance of payments record?", "Trade in goods and services, primary income and secondary income", "Only foreign direct investment", "Only government borrowing", "Only stock market transactions"),
        ("What is Foreign Direct Investment (FDI)?", "Investment involving a lasting interest or significant influence in an enterprise in another country", "A short-term domestic bank deposit", "A government tax refund", "A purchase of goods for personal use"),
        ("What is the purpose of the Pradhan Mantri Mudra Yojana?", "To support eligible micro and small non-corporate enterprises with loans", "To provide free housing to all citizens", "To regulate stock exchanges", "To fund only large industries"),
        ("Which scheme is associated with health insurance or health cover for eligible vulnerable families?", "Ayushman Bharat - PM-JAY", "PM-KISAN", "MUDRA Yojana", "Atal Pension Yojana"),
        ("What is the primary objective of PM-KISAN?", "Provide income support to eligible farmer families", "Provide free electricity to every industry", "Provide loans to foreign companies", "Regulate agricultural exports"),
        ("Which initiative aims to improve digital infrastructure and digital services in India?", "Digital India", "Green Revolution", "White Revolution", "Operation Flood"),
        ("What is the main purpose of the Production Linked Incentive (PLI) scheme?", "Encourage domestic manufacturing through performance-linked incentives", "Provide pensions to all citizens", "Control retail inflation directly", "Replace the GST system"),
    ],

    "Hard": [
        ("Which of the following best describes revenue expenditure in a government budget?", "Expenditure that generally does not create assets or reduce liabilities", "Expenditure that always creates physical assets", "Only expenditure on buying land", "Only repayment of government debt"),
        ("Which of the following is an example of capital expenditure by the government?", "Construction of a national highway", "Payment of salaries", "Payment of pensions", "Interest on government debt"),
        ("What is the difference between a fiscal deficit and a revenue deficit?", "Fiscal deficit measures the overall borrowing requirement, while revenue deficit is the excess of revenue expenditure over revenue receipts", "They are exactly the same", "Revenue deficit includes only foreign borrowing", "Fiscal deficit measures only tax collections"),
        ("What is a primary deficit?", "Fiscal deficit minus interest payments", "Revenue deficit plus exports", "Fiscal deficit plus interest payments", "Total tax revenue minus subsidies"),
        ("What is the effective revenue deficit?", "Revenue deficit minus grants for creation of capital assets", "Fiscal deficit minus exports", "Primary deficit plus interest payments", "Revenue receipts minus capital receipts"),
        ("Which constitutional article requires the President to cause the annual financial statement to be laid before Parliament?", "Article 112", "Article 110", "Article 123", "Article 280"),
        ("What is the constitutional name of the Union Budget?", "Annual Financial Statement", "Finance Commission Report", "Economic Survey", "Appropriation Report"),
        ("Which bill authorises the withdrawal of money from the Consolidated Fund of India?", "Appropriation Bill", "Finance Bill", "Private Member's Bill", "Constitution Amendment Bill"),
        ("Which fund receives all revenues, loans raised and money received by the Union government in repayment of loans?", "Consolidated Fund of India", "Contingency Fund of India", "Public Account of India", "National Investment Fund"),
        ("Which fund is available to the President to meet unforeseen expenditure pending parliamentary authorisation?", "Contingency Fund of India", "Consolidated Fund of India", "Public Account of India", "Finance Commission Fund"),
        ("Money held by the government in trust, such as certain provident fund deposits, is generally accounted for in which fund?", "Public Account of India", "Consolidated Fund of India", "Contingency Fund of India", "National Disaster Response Fund"),
        ("Which constitutional article provides for the creation of the GST Council?", "Article 279A", "Article 280", "Article 246A", "Article 368"),
        ("Which constitutional amendment introduced the GST framework in India?", "101st Amendment", "97th Amendment", "86th Amendment", "73rd Amendment"),
        ("Which article gives Parliament and state legislatures power to make laws on GST, subject to constitutional provisions?", "Article 246A", "Article 110", "Article 280", "Article 352"),
        ("Which article provides for the levy and collection of GST on inter-state supplies?", "Article 269A", "Article 148", "Article 324", "Article 356"),
        ("Which body recommends the rates, exemptions and other important GST-related matters?", "GST Council", "Finance Commission", "SEBI", "NITI Aayog"),
        ("What is the main purpose of input tax credit under GST?", "To reduce cascading of taxes by allowing eligible credit for tax paid on inputs", "To increase the number of tax payments on the same value", "To exempt all imports from tax", "To replace income tax"),
        ("Which of the following is generally outside the current GST levy in India?", "Alcoholic liquor for human consumption", "Mobile phones", "Packaged food", "Furniture"),
        ("Which type of tax system imposes a higher tax rate as taxable income increases?", "Progressive tax system", "Regressive tax system", "Proportional tax system", "Flat indirect tax system"),
        ("What is tax buoyancy?", "Responsiveness of tax revenue to changes in national income", "The total number of taxpayers", "The rate of inflation in an economy", "The share of exports in GDP"),
        ("What is the Laffer Curve generally used to illustrate?", "The relationship between tax rates and tax revenue", "The relationship between exports and imports", "The relationship between inflation and population", "The relationship between savings and literacy"),
        ("What is crowding out in public finance?", "Government borrowing may reduce funds available for private investment", "Private investment always increases government revenue", "Exports replace domestic production", "Inflation automatically falls when taxes rise"),
        ("What is monetisation of a fiscal deficit in its traditional sense?", "Financing government deficit through central bank money creation or credit", "Financing government spending only through exports", "Reducing government expenditure to zero", "Increasing private savings through taxation"),
        ("Which measure of inflation excludes certain volatile components, commonly food and energy?", "Core inflation", "Headline inflation", "Wholesale inflation only", "Imported inflation only"),
        ("What is stagflation?", "High inflation combined with stagnant economic growth and elevated unemployment", "Rapid growth with zero inflation", "Falling prices with full employment", "A rise in exports with falling imports"),
        ("What is the main objective of inflation targeting by the RBI?", "Maintain price stability while keeping the objective of growth in mind", "Fix all wages in the economy", "Set the prices of every commodity", "Eliminate all government borrowing"),
        ("Which committee is associated with the recommendation of an inflation-targeting monetary policy framework in India?", "Urjit Patel Committee", "Narasimham Committee", "Kelkar Committee", "Sarkaria Commission"),
        ("Which committee is associated with major banking sector reforms in India in the 1990s?", "Narasimham Committee", "Mandal Commission", "Sarkaria Commission", "Punchhi Commission"),
        ("What is the twin balance sheet problem in the Indian economy?", "Simultaneous stress in corporate balance sheets and bank balance sheets", "A mismatch between exports and imports only", "A difference between state and Union budgets", "A problem involving only household savings"),
        ("What is the primary objective of the Fiscal Responsibility and Budget Management Act, 2003?", "Promote fiscal discipline and improve management of government finances", "Regulate stock exchanges", "Control agricultural production", "Establish the Reserve Bank of India"),
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
                    "MCQ lesson covering the Indian economy, Union Budget, "
                    "taxation and economic policies."
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
