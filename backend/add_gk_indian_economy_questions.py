
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 165
LESSON_TITLE = "Indian Economy - Banking, Budget, GDP and Financial Awareness"
TOPIC = "General Knowledge"

BANK = {

"Easy": [

("What is the currency of India?", "Indian Rupee", "US Dollar", "Euro", "Pound"),
("Which institution is known as the central bank of India?", "Reserve Bank of India", "State Bank of India", "NABARD", "SEBI"),
("In which year was the Reserve Bank of India established?", "1935", "1947", "1950", "1920"),
("Where is the headquarters of the Reserve Bank of India?", "Mumbai", "New Delhi", "Kolkata", "Chennai"),
("What does ATM stand for?", "Automated Teller Machine", "Automatic Transfer Money", "Anytime Transaction Method", "Account Transfer Machine"),
("What does GDP stand for?", "Gross Domestic Product", "General Domestic Production", "Gross Development Plan", "Global Domestic Product"),
("Which bank is India's largest public sector bank?", "State Bank of India", "Punjab National Bank", "Bank of Baroda", "Canara Bank"),
("What is a bank account primarily used for?", "Depositing and managing money", "Manufacturing goods", "Producing electricity", "Measuring rainfall"),
("Which organisation regulates the securities market in India?", "SEBI", "RBI", "NABARD", "IRDAI"),
("What does UPI stand for?", "Unified Payments Interface", "Universal Payment Information", "United Payment Institution", "Unique Payment Identification"),
("Which organisation operates the UPI payment system?", "National Payments Corporation of India", "Reserve Bank of India directly", "State Bank of India", "SEBI"),
("What is inflation?", "A general rise in prices", "A fall in population", "An increase in rainfall", "A decrease in employment only"),
("What is a budget?", "A financial plan of income and expenditure", "A list of bank branches", "A record of population", "A list of imports only"),
("Who presents the Union Budget in Parliament?", "Union Finance Minister", "Prime Minister only", "RBI Governor", "President of India"),
("Which ministry prepares the Union Budget?", "Ministry of Finance", "Ministry of Home Affairs", "Ministry of Education", "Ministry of Defence"),
("What is a savings account?", "An account used to save money and earn interest", "An account used only by companies", "A loan account", "A government tax account"),
("What is a fixed deposit?", "A deposit kept for a fixed period", "A daily cash withdrawal", "A type of credit card", "A tax payment"),
("What is a loan?", "Money borrowed that must be repaid", "Money received as a gift", "A government subsidy only", "A type of savings account"),
("What does PAN stand for?", "Permanent Account Number", "Personal Account Name", "Primary Access Number", "Payment Allocation Note"),
("Which authority issues PAN cards in India?", "Income Tax Department", "Election Commission", "SEBI", "NABARD"),
("What does GST stand for?", "Goods and Services Tax", "General Sales Transfer", "Government Service Tariff", "Gross State Tax"),
("When was GST introduced in India?", "1 July 2017", "1 January 2015", "15 August 2016", "26 January 2018"),
("Which tax is levied on personal income in India?", "Income Tax", "Customs Duty only", "Excise Duty only", "Road Tax"),
("What is a cheque?", "A written instruction to a bank to pay money", "A type of currency note", "A government bond", "A credit card"),
("What is a debit card generally linked to?", "Bank account", "Stock exchange", "Passport", "Insurance policy"),
("What is a credit card primarily used for?", "Making purchases using borrowed credit", "Depositing cash directly", "Receiving salary only", "Opening a fixed deposit"),
("What does IFSC stand for?", "Indian Financial System Code", "International Finance Security Code", "Indian Fund Service Certificate", "Integrated Financial Savings Code"),
("Which institution supports agriculture and rural development through finance?", "NABARD", "SEBI", "IRDAI", "TRAI"),
("What does EMI stand for?", "Equated Monthly Instalment", "Estimated Money Income", "Electronic Monthly Investment", "Equal Market Interest"),
("What is financial literacy?", "Understanding financial concepts and managing money", "Learning only computer programming", "Studying geography", "Memorising currency names"),

],

"Medium": [

("What is the full form of CRR in banking?", "Cash Reserve Ratio", "Credit Reserve Rate", "Capital Return Ratio", "Cash Revenue Reserve"),
("What is the full form of SLR?", "Statutory Liquidity Ratio", "Standard Lending Rate", "Savings Liability Reserve", "State Loan Ratio"),
("Which institution decides the monetary policy of India?", "Reserve Bank of India", "SEBI", "NITI Aayog", "Finance Commission"),
("What is the repo rate?", "Rate at which RBI lends short-term funds to banks against eligible securities", "Rate at which banks lend to customers for home loans", "Rate of income tax", "Rate of GST collection"),
("What is the reverse repo rate traditionally associated with?", "Rate at which RBI borrows money from banks", "Rate at which customers borrow from banks", "Rate of currency exchange", "Rate of government taxation"),
("What is fiscal policy mainly concerned with?", "Government taxation and expenditure", "Bank employee recruitment", "Stock market trading only", "Foreign exchange rates only"),
("What is monetary policy mainly concerned with?", "Money supply and interest rates", "Government road construction", "Population growth", "Agricultural production only"),
("What is a fiscal deficit?", "Government expenditure exceeding its receipts excluding borrowings", "Government income exceeding expenditure", "Total exports exceeding imports", "Total savings exceeding investments"),
("What is a trade deficit?", "Imports exceeding exports", "Exports exceeding imports", "Equal imports and exports", "A fall in domestic production"),
("What is the balance of payments?", "Record of economic transactions between residents of a country and the rest of the world", "Record of government employee salaries", "Record of domestic bank deposits only", "Record of agricultural output"),
("Which organisation publishes India's national income estimates?", "National Statistical Office", "Election Commission", "SEBI", "NABARD"),
("What is per capita income?", "Average income per person", "Total government tax collection", "Income earned by banks only", "Total value of exports"),
("Which sector includes farming, fishing and forestry?", "Primary sector", "Secondary sector", "Tertiary sector", "Quaternary sector"),
("Which sector includes manufacturing and construction?", "Secondary sector", "Primary sector", "Tertiary sector", "Public administration only"),
("Which sector includes banking, transport and education services?", "Tertiary sector", "Primary sector", "Secondary sector", "Agricultural sector"),
("What is disinvestment?", "Sale of government ownership in public sector enterprises", "Increase in government subsidies", "Printing new currency", "Increasing income tax rates"),
("What is privatisation?", "Transfer of ownership or control from the public sector to the private sector", "Transfer of private companies to government ownership", "Increase in bank deposits", "Reduction in imports"),
("Which institution replaced the Planning Commission in India?", "NITI Aayog", "Finance Commission", "RBI", "SEBI"),
("In which year was NITI Aayog established?", "2015", "2010", "2005", "2020"),
("Which institution recommends the distribution of tax revenues between the Union and states?", "Finance Commission", "Election Commission", "NITI Aayog", "SEBI"),
("What is the main purpose of the Public Distribution System?", "Providing essential food items to eligible people at subsidised prices", "Providing free stock market accounts", "Offering private bank loans", "Exporting agricultural products"),
("What is Minimum Support Price (MSP)?", "A price announced by the government to support farmers for specified crops", "The maximum retail price of all goods", "The international price of gold", "The interest rate on savings accounts"),
("Which organisation is primarily responsible for deposit insurance in India?", "Deposit Insurance and Credit Guarantee Corporation", "SEBI", "NABARD", "NITI Aayog"),
("What is the current maximum deposit insurance cover per depositor per bank in India?", "₹5 lakh", "₹1 lakh", "₹10 lakh", "₹2 lakh"),
("What is a non-performing asset (NPA)?", "A loan or advance that has ceased to generate income for the bank under applicable rules", "A bank's profitable investment", "A savings account with high interest", "A government tax refund"),
("What is financial inclusion?", "Providing access to affordable financial services to all sections of society", "Restricting banking services to cities", "Increasing luxury spending", "Limiting access to digital payments"),
("Which scheme was launched to promote financial inclusion through bank accounts?", "Pradhan Mantri Jan Dhan Yojana", "Make in India", "Digital India only", "Swachh Bharat Mission"),
("What is the purpose of the Kisan Credit Card scheme?", "Providing timely credit to farmers", "Providing free housing to farmers", "Offering scholarships to students", "Providing health insurance to bank employees"),
("Which organisation regulates insurance companies in India?", "IRDAI", "SEBI", "RBI", "NABARD"),
("What is a mutual fund?", "An investment vehicle that pools money from investors", "A type of savings account", "A government tax", "A form of currency"),

],

"Hard": [

("Which committee recommended the adoption of inflation targeting in India's monetary policy framework?", "Urjit Patel Committee", "Narasimham Committee", "Rangarajan Committee", "Kelkar Committee"),
("What is the primary objective of inflation targeting by the RBI?", "Maintaining price stability", "Maximising exports only", "Increasing government borrowing", "Eliminating all taxes"),
("Which body is responsible for deciding the policy repo rate in India?", "Monetary Policy Committee", "Finance Commission", "NITI Aayog", "SEBI"),
("How many members are there in India's Monetary Policy Committee?", "Six", "Four", "Five", "Eight"),
("What is the statutory inflation target framework adopted by India?", "4% with a tolerance band of 2% to 6%", "2% with a tolerance band of 1% to 3%", "6% with a tolerance band of 4% to 8%", "5% with a tolerance band of 3% to 7%"),
("Which committee is associated with major banking sector reforms in India during the 1990s?", "Narasimham Committee", "Urjit Patel Committee", "Sarkaria Commission", "Mandal Commission"),
("Which committee recommended reforms relating to the Indian tax system and fiscal policy in the early 2000s?", "Kelkar Task Force", "Mandal Commission", "Sarkaria Commission", "Balwant Rai Mehta Committee"),
("What is the difference between GDP and GNP?", "GNP includes net factor income from abroad, while GDP measures domestic production", "GDP includes only exports, while GNP includes imports", "GDP measures population, while GNP measures employment", "There is no difference"),
("What is Gross Value Added (GVA)?", "Value of output minus intermediate consumption", "Total exports minus imports", "Government revenue minus expenditure", "Total savings minus investment"),
("What is the base year used for India's current official GDP constant-price series as of 2026?", "2011-12", "2004-05", "2015-16", "2020-21"),
("What does the current account of the balance of payments include?", "Trade in goods and services, primary income and secondary income", "Only government tax receipts", "Only foreign direct investment", "Only domestic bank deposits"),
("What is Foreign Direct Investment (FDI)?", "Investment involving lasting interest and significant influence in a foreign enterprise", "Short-term personal savings", "A domestic government tax", "A bank's cash reserve"),
("What is Foreign Portfolio Investment (FPI)?", "Investment in financial assets such as shares and bonds without controlling the enterprise", "Investment in agricultural land only", "A government subsidy", "A type of bank deposit"),
("Which organisation manages India's foreign exchange reserves?", "Reserve Bank of India", "SEBI", "NITI Aayog", "NABARD"),
("What is the purpose of the Liberalised Remittance Scheme?", "Allowing resident individuals to remit money abroad within prescribed limits and conditions", "Providing free foreign currency to tourists", "Allowing unlimited cash withdrawals", "Removing all import duties"),
("What is the primary objective of the Fiscal Responsibility and Budget Management Act?", "Promoting fiscal discipline and responsible management of government finances", "Regulating stock exchanges", "Controlling private bank salaries", "Managing agricultural exports only"),
("What is revenue deficit?", "Revenue expenditure exceeding revenue receipts", "Capital receipts exceeding capital expenditure", "Exports exceeding imports", "Total assets exceeding liabilities"),
("What is primary deficit?", "Fiscal deficit minus interest payments", "Revenue deficit plus exports", "Total tax revenue minus imports", "Government expenditure minus capital receipts"),
("What is capital expenditure by the government?", "Expenditure that creates assets or reduces liabilities", "Routine salary payments only", "Daily office expenses only", "Interest payments on existing debt"),
("What is the main role of the Comptroller and Auditor General of India?", "Auditing government accounts and public expenditure", "Setting interest rates", "Regulating stock exchanges", "Issuing currency notes"),
("Which organisation manages and regulates India's government securities market along with the RBI's statutory responsibilities?", "Reserve Bank of India", "NABARD", "IRDAI", "NITI Aayog"),
("What is the purpose of the Insolvency and Bankruptcy Code, 2016?", "Providing a time-bound framework for insolvency resolution", "Regulating agricultural prices", "Managing foreign exchange reserves", "Setting income tax slabs"),
("Which institution operates the National Electronic Funds Transfer system in India?", "Reserve Bank of India", "SEBI", "NABARD", "IRDAI"),
("What is the main purpose of the National Payments Corporation of India?", "Operating and developing retail payment and settlement systems", "Regulating insurance companies", "Managing government budgets", "Controlling stock market indices"),
("What does the term 'stagflation' mean?", "High inflation combined with stagnant economic growth and high unemployment", "Rapid growth with falling prices", "Low inflation with high employment", "A rise in exports and imports"),
("What is deflation?", "A sustained fall in the general price level", "A sustained rise in the general price level", "An increase in government spending", "A rise in population"),
("What is the Laffer Curve used to illustrate?", "Relationship between tax rates and tax revenue", "Relationship between rainfall and agriculture", "Relationship between imports and population", "Relationship between wages and education"),
("What is the Gini coefficient used to measure?", "Income or wealth inequality", "Inflation rate", "GDP growth", "Foreign exchange reserves"),
("What does the Human Development Index consider?", "Health, education and standard of living", "Only national income", "Only population growth", "Only industrial production"),
("Which institution publishes the Human Development Report?", "United Nations Development Programme", "World Trade Organization", "International Monetary Fund", "World Bank"),

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
                    f"Invalid format: {difficulty} question {index}"
                )

            question, correct, *wrong = item
            options = [correct] + wrong

            if not all(
                isinstance(value, str) and value.strip()
                for value in item
            ):
                raise ValueError(
                    f"Empty value: {difficulty} question {index}"
                )

            if len(set(options)) != 4:
                raise ValueError(
                    f"Duplicate options: {difficulty} question {index}"
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
                "Learn about the Indian economy, banking, budgeting, GDP and financial awareness."
            ))

            print("Lesson created successfully.")

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
                        quiz_id,
                        question,
                        option_a,
                        option_b,
                        option_c,
                        option_d,
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
        print("GK TOPIC 5 INSERTED SUCCESSFULLY")
        print("Indian Economy")
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
