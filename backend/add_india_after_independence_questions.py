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
        ("When did India become independent?", "15 August 1947", "26 January 1950", "2 October 1947", "15 August 1950", "A"),
        ("Who was India's first Prime Minister?", "Jawaharlal Nehru", "Sardar Vallabhbhai Patel", "Rajendra Prasad", "Lal Bahadur Shastri", "A"),
        ("When did the Constitution of India come into effect?", "26 January 1950", "15 August 1947", "26 November 1949", "2 October 1950", "A"),
        ("Who chaired the Drafting Committee of the Indian Constitution?", "Dr. B. R. Ambedkar", "Jawaharlal Nehru", "Mahatma Gandhi", "Sardar Patel", "A"),
        ("Who was India's first President?", "Dr. Rajendra Prasad", "Dr. S. Radhakrishnan", "Zakir Husain", "V. V. Giri", "A"),
        ("What was one major challenge India faced after independence?", "Partition and refugee rehabilitation", "Establishing British rule", "Ending all elections permanently", "Restoring the East India Company", "A"),
        ("What is a republic?", "A country whose head of state is not a hereditary monarch", "A country ruled permanently by a king", "A country without laws", "A country without citizens", "A"),
        ("What is universal adult franchise?", "The right of eligible adult citizens to vote", "The right of only wealthy people to vote", "The right of children to vote", "The right of only government employees to vote", "A"),
        ("What was the main purpose of the States Reorganisation Act of 1956?", "Reorganising states largely on linguistic lines", "Declaring India independent", "Introducing British colonial rule", "Creating the Indian National Congress", "A"),
        ("What is a Five-Year Plan associated with?", "Planned economic development", "Conducting school examinations", "Selecting the President directly", "Drawing district maps only", "A"),
        ("Which sector includes farming and fishing?", "Primary sector", "Secondary sector", "Tertiary sector", "Information sector only", "A"),
        ("Which sector includes manufacturing industries?", "Secondary sector", "Primary sector", "Household sector only", "Judicial sector", "A"),
        ("Which sector includes banking and transport services?", "Tertiary sector", "Primary sector only", "Mining sector only", "Agricultural sector only", "A"),
        ("What is the Green Revolution mainly associated with?", "Increasing agricultural production through improved methods and inputs", "Expanding railway stations only", "Building more courts", "Ending all irrigation", "A"),
        ("What is the purpose of elections in a democracy?", "To allow citizens to choose their representatives", "To appoint hereditary rulers", "To end public participation", "To remove the Constitution", "A"),
        ("What does secularism mean in the Indian constitutional context?", "The state respects religious freedom and does not establish an official religion", "The state requires everyone to follow one religion", "Only one community may vote", "Religious freedom is prohibited", "A"),
        ("What is the main role of the Election Commission of India?", "Conducting elections to Parliament and state legislatures and certain constitutional offices", "Making every law in Parliament", "Deciding every court case", "Running all private businesses", "A"),
        ("What is a planned economy?", "An economy in which public authorities use plans to guide development priorities", "An economy without any production", "An economy based only on barter", "An economy without workers", "A"),
        ("What is the purpose of a dam used for irrigation?", "Storing and regulating water for agricultural use", "Conducting elections", "Printing currency", "Running courts", "A"),
        ("What is national integration?", "Strengthening unity among people of the country", "Separating every community permanently", "Ending cultural diversity", "Removing all state governments", "A"),
        ("Which institution makes laws at the national level in India?", "Parliament", "Municipal corporation only", "Village school", "Private company", "A"),
        ("What is the main purpose of a census?", "Collecting information about a population", "Conducting parliamentary debates", "Issuing court judgments", "Manufacturing agricultural equipment", "A"),
        ("What is a public sector enterprise?", "An enterprise owned or controlled by the government", "A business owned only by a foreign tourist", "A household without a business", "A private diary service", "A"),
        ("What is privatisation?", "Transfer of ownership or control of an activity or enterprise from the public sector to the private sector", "Transfer of all private property to villages", "The introduction of universal voting", "The abolition of all businesses", "A"),
        ("What is the purpose of a national highway?", "Connecting important places and supporting transport", "Conducting national elections", "Storing drinking water only", "Teaching constitutional law only", "A"),
        ("What does literacy generally mean?", "The ability to read and write with understanding", "The ability to drive every vehicle", "The ability to vote before adulthood", "The ability to build a bridge", "A"),
        ("What is poverty?", "A condition in which people lack sufficient resources to meet basic needs", "A condition of having unlimited wealth", "A type of election", "A system of government", "A"),
        ("What is the purpose of public education?", "Providing learning opportunities and developing knowledge and skills", "Preventing children from learning", "Replacing every hospital", "Conducting business transactions only", "A"),
        ("What is the main purpose of the Indian Constitution?", "Establishing the framework of government and protecting rights and principles", "Replacing all elected institutions with hereditary rulers", "Ending the rule of law", "Preventing all elections", "A"),
        ("What is independence?", "Freedom from external political control", "Permanent rule by another country", "The absence of any government", "The end of all public institutions", "A"),
    ],

    "Medium": [
        ("Why was the integration of princely states important after independence?", "It helped create a politically unified Indian Union", "It restored every princely state as an independent foreign country", "It ended the Indian Constitution", "It abolished all state administrations", "A"),
        ("Why did Partition create major humanitarian challenges?", "It led to large-scale migration, displacement, and communal violence", "It immediately eliminated every refugee problem", "It ended all population movement", "It made rehabilitation unnecessary", "A"),
        ("Why was adopting a democratic Constitution significant for India?", "It established constitutional government and democratic institutions", "It restored permanent colonial rule", "It abolished fundamental rights", "It made elections unnecessary", "A"),
        ("Why was linguistic reorganisation of states demanded?", "Language was an important basis of regional identity and administration", "All Indians spoke only one language", "States wanted to abolish local administration", "It was intended to end education", "A"),
        ("What was the purpose of the Planning Commission when it was established in 1950?", "To formulate plans and advise on national development priorities", "To conduct all criminal trials", "To supervise every private school directly", "To replace Parliament", "A"),
        ("Why did independent India emphasise industrial development?", "To expand productive capacity, employment, and economic self-reliance", "To eliminate every form of manufacturing", "To prevent infrastructure development", "To replace all agriculture immediately", "A"),
        ("What was an important goal of land reforms after independence?", "Changing certain landholding arrangements and addressing agrarian inequalities", "Restoring every colonial land system unchanged", "Eliminating all farming", "Transferring every farm abroad", "A"),
        ("How did the Green Revolution affect Indian agriculture?", "It increased food-grain production in several regions through improved seeds and inputs", "It eliminated all regional differences in agriculture", "It ended the need for irrigation everywhere", "It replaced farming with manufacturing", "A"),
        ("Why was food security important after independence?", "India needed reliable access to sufficient food for its population", "Food production was unrelated to public welfare", "All citizens already had unlimited food", "Agriculture was prohibited", "A"),
        ("What was an important goal of public sector industries?", "Supporting strategic industries, infrastructure, and development objectives", "Conducting elections only", "Eliminating the need for skilled workers", "Preventing all industrial production", "A"),
        ("Why were large infrastructure projects important to development planning?", "They supported irrigation, electricity, transport, and industrial growth", "They were intended to eliminate public services", "They made roads and electricity unnecessary", "They replaced the Constitution", "A"),
        ("What is the significance of universal adult franchise in India?", "It established broad voting rights for eligible adult citizens", "It limited voting to landowners", "It restricted voting to government officials", "It allowed only one region to vote", "A"),
        ("How does a federal system distribute governmental power?", "It divides powers between Union and state governments under the Constitution", "It gives all power to village markets", "It eliminates state governments", "It gives every private company legislative authority", "A"),
        ("Why is the Indian Constitution considered adaptable?", "It can be amended through prescribed procedures as society and needs change", "It can be ignored by every government", "It prohibits all institutional change", "It is replaced automatically every year", "A"),
        ("What is the role of the judiciary in independent India?", "Interpreting laws and resolving disputes, including constitutional questions", "Conducting every election directly", "Preparing all economic plans", "Manufacturing public-sector goods", "A"),
        ("Why are public health and education important development indicators?", "They reflect important aspects of people's well-being and capabilities", "They measure only the size of a country's borders", "They have no relationship to development", "They measure only industrial output", "A"),
        ("How can cooperative institutions help rural development?", "They can enable members to pool resources and improve access to services or markets", "They guarantee that farming is unnecessary", "They replace all democratic institutions", "They prevent members from working together", "A"),
        ("Why did India adopt economic planning after independence?", "To coordinate investment and address development challenges and resource constraints", "To stop all economic activity", "To eliminate every public institution", "To end infrastructure construction", "A"),
        ("What is one purpose of the Public Distribution System?", "Distributing selected essential commodities to eligible households through designated channels", "Providing every luxury product free to everyone", "Conducting national elections", "Building every private factory", "A"),
        ("Why is national integration important in a diverse country?", "It supports shared citizenship while allowing cultural and linguistic diversity", "It requires every community to abandon its language", "It prevents citizens from participating in government", "It eliminates constitutional rights", "A"),
        ("What was an important challenge in rehabilitating Partition refugees?", "Providing shelter, livelihoods, and support for displaced people", "Preventing all displaced people from receiving assistance", "Ending all public housing", "Making migration impossible to document", "A"),
        ("Why is a census useful for public planning?", "Population data can help plan schools, hospitals, housing, and other services", "It replaces all local surveys in every situation", "It determines every individual's political opinion", "It directly makes all laws", "A"),
        ("How can irrigation contribute to agricultural development?", "It can improve water availability and reduce dependence on rainfall", "It eliminates all crop diseases", "It guarantees identical yields in every region", "It makes soil quality irrelevant", "A"),
        ("What is one concern associated with large dams?", "They may displace communities and affect ecosystems and livelihoods", "They never affect people or the environment", "They eliminate every water-management challenge", "They prevent all electricity generation", "A"),
        ("Why did India pursue scientific and technical education after independence?", "To develop skilled people and support research and economic development", "To prevent industrial innovation", "To eliminate all professional training", "To replace all schools with factories", "A"),
        ("What is the purpose of affirmative action policies?", "To address historical disadvantage and improve representation for specified groups", "To remove every constitutional safeguard", "To abolish education", "To restrict all public employment to one family", "A"),
        ("How can urbanisation affect post-independence India?", "It can create jobs and services while increasing pressure on housing and infrastructure", "It guarantees that every city has no traffic", "It eliminates the need for rural development", "It prevents population movement", "A"),
        ("What is a mixed economy?", "An economy combining public-sector roles with private economic activity", "An economy prohibiting all private businesses permanently", "An economy without government activity", "An economy based entirely on barter", "A"),
        ("What was an important aim of the economic reforms introduced in 1991?", "To liberalise parts of the economy and change industrial, trade, and investment policies", "To declare independence from Britain", "To adopt the Constitution for the first time", "To introduce the Green Revolution in the 1960s", "A"),
        ("Why should development be assessed beyond national income alone?", "Health, education, equality, and living conditions also affect people's well-being", "National income measures every aspect of life perfectly", "Social conditions never matter", "Development has no connection to people's lives", "A"),
    ],

    "Hard": [
        ("Why was the integration of princely states a complex political task?", "Different rulers, territorial circumstances, and political interests required negotiation and other measures", "Every princely state had identical political conditions", "All princely states had already merged before independence", "The Constitution prohibited any integration", "A"),
        ("How did Partition influence the priorities of the new Indian government?", "Refugee rehabilitation, communal peace, and territorial stability became urgent concerns", "It removed all humanitarian challenges", "It ended the need for public administration", "It made citizenship irrelevant", "A"),
        ("Why was constitutional democracy important in a society marked by inequality?", "It established political rights and institutions through which citizens could seek representation and justice", "It guaranteed that inequality would disappear immediately", "It removed the need for public participation", "It made all social policies unnecessary", "A"),
        ("What tension can arise between rapid industrialisation and environmental protection?", "Industrial growth may generate jobs and output while also creating pollution and ecological costs", "Industrialisation has no environmental effects", "Environmental protection always prevents all economic activity", "Both objectives are unrelated in every situation", "A"),
        ("Why did India's early development plans assign a major role to the public sector?", "The state sought to build infrastructure and develop industries requiring substantial investment", "Private economic activity was the only legal activity", "Infrastructure was considered unnecessary", "All industries were already equally developed", "A"),
        ("What was a major limitation of the Green Revolution's benefits?", "Its gains were uneven across crops, regions, and farmers", "It reduced food-grain production in every region", "It eliminated the need for agricultural inputs", "It made irrigation irrelevant everywhere", "A"),
        ("How can land reform contribute to social justice?", "It can address unequal landholding structures and improve the position of disadvantaged cultivators", "It guarantees equal wealth without implementation", "It eliminates all agricultural work", "It automatically solves every rural problem", "A"),
        ("Why is federalism important in India's governance?", "It allows national and state institutions to exercise constitutionally assigned powers", "It gives all authority to one local shop", "It removes state-level decision-making", "It prevents regional representation", "A"),
        ("How can linguistic state reorganisation strengthen democratic governance?", "It can make administration more responsive to linguistic and regional identities", "It guarantees that no regional dispute will ever occur", "It eliminates India's language diversity", "It abolishes the Union government", "A"),
        ("Why should the success of a development plan be evaluated against its outcomes?", "Planned targets do not automatically prove that benefits reached people fairly or effectively", "Announcing a plan guarantees success", "Budgets have no relationship to outcomes", "Public services never need evaluation", "A"),
        ("What does the shift toward economic reforms in 1991 illustrate?", "Economic policy can change in response to fiscal pressures and changing domestic and global conditions", "India became independent for the first time in 1991", "The Constitution was adopted in 1991", "All public institutions were abolished", "A"),
        ("Why is the Public Distribution System significant for food security?", "It is one mechanism used to provide selected essential food commodities to eligible households", "It guarantees that nobody can ever experience hunger", "It produces all food consumed in India", "It eliminates the need for agricultural production", "A"),
        ("How can large infrastructure projects produce both benefits and costs?", "They can support energy, irrigation, and transport while also causing displacement or ecological change", "They provide benefits without any possible trade-offs", "They always destroy every local livelihood", "They cannot contribute to economic activity", "A"),
        ("Why is education considered an investment in human development?", "It can improve knowledge, capabilities, employment opportunities, and participation", "It guarantees identical incomes for everyone", "It removes the need for public health", "It prevents people from learning new skills", "A"),
        ("How does universal adult franchise change the political status of citizens?", "It recognises eligible adults as voters without restricting voting to property owners or elites", "It allows only wealthy citizens to vote", "It gives voting rights only to civil servants", "It abolishes representative government", "A"),
        ("Why is the protection of minority rights important in a democracy?", "It helps prevent majority power from undermining constitutional equality and freedom", "It means every group must agree on every issue", "It eliminates the need for elections", "It gives one community permanent control of all institutions", "A"),
        ("What is a potential drawback of judging development only by GDP growth?", "Growth can occur without equal improvements in health, education, or distribution of benefits", "GDP measures every dimension of well-being perfectly", "Economic output never affects living standards", "Social indicators have no analytical value", "A"),
        ("How can urbanisation reflect both progress and challenges?", "It can expand access to jobs and services while increasing demand for housing and infrastructure", "It guarantees that rural areas no longer need investment", "It automatically removes poverty", "It prevents economic opportunities from changing", "A"),
        ("Why did India invest in scientific and technical institutions after independence?", "To build domestic expertise for research, industry, and national development", "To prevent technical education", "To end all scientific research", "To make skilled employment impossible", "A"),
        ("How can affirmative action contribute to substantive equality?", "It can address structural barriers that prevent historically disadvantaged groups from accessing opportunities", "It guarantees that all social inequalities disappear immediately", "It removes the need for constitutional rights", "It prevents disadvantaged groups from entering education", "A"),
        ("Why is national integration not the same as cultural uniformity?", "Unity can coexist with different languages, religions, traditions, and regional identities", "National unity requires every person to share the same language", "Cultural differences make citizenship impossible", "Integration requires abolishing regional identities", "A"),
        ("What is the significance of India's parliamentary system?", "The executive is accountable to the elected legislature under constitutional rules", "The executive is permanently hereditary", "The judiciary conducts all elections", "The President personally makes every law without Parliament", "A"),
        ("Why is independent evaluation of welfare programmes useful?", "It can reveal whether intended beneficiaries receive services and where implementation needs improvement", "It guarantees every programme succeeds", "It makes public data unnecessary", "It prevents any policy from changing", "A"),
        ("How can irrigation and improved seeds interact in agricultural development?", "Reliable water and suitable seeds can complement each other in raising yields under appropriate conditions", "Seeds alone guarantee high yields regardless of water or soil", "Irrigation always reduces crop production", "Agricultural inputs never interact", "A"),
        ("Why can economic self-reliance differ from complete economic isolation?", "A country can build domestic capabilities while continuing beneficial international trade", "Self-reliance requires ending all international contact", "Trade automatically eliminates domestic industry", "Domestic production makes all technology unnecessary", "A"),
        ("What is a key governance challenge when planning for a large and diverse population?", "Policies must respond to varied regional needs while coordinating national priorities", "Every region has identical needs", "Public services should be distributed without considering population", "Regional conditions never affect policy", "A"),
        ("Why should achievements after independence be studied alongside unresolved problems?", "It provides a balanced understanding of progress, limitations, and continuing policy challenges", "It proves that every policy failed", "It proves that every problem disappeared", "It makes historical evidence unnecessary", "A"),
        ("How can decentralised governance complement national development planning?", "Local institutions can help identify and respond to community-specific needs", "Local institutions replace the Constitution entirely", "National planning must ignore all local information", "Decentralisation removes every public responsibility", "A"),
        ("Why does the rule of law matter to democratic institutions?", "Government action must operate within constitutional and legal limits", "Officials can ignore all laws", "Courts must follow private advertisements", "Elections are unnecessary under the rule of law", "A"),
        ("Which combination best describes the central challenges of building India after independence?", "Consolidating national unity, establishing democratic institutions, and promoting inclusive development", "Restoring colonial rule and ending citizenship", "Eliminating elections and public services", "Preventing economic and social change", "A"),
    ],
}


def main():
    db = SessionLocal()
    added = 0

    try:
        lesson = (
            db.query(Lesson)
            .filter(
                Lesson.title == "India After Independence",
                Lesson.topic == "Social Science",
            )
            .first()
        )

        if not lesson:
            print("ERROR: India After Independence lesson was not found.")
            print("Check the lesson title and topic in the database.")
            return

        for difficulty, questions in QUESTION_BANK.items():
            quiz = (
                db.query(Quiz)
                .filter(
                    Quiz.lesson_id == lesson.id,
                    Quiz.difficulty == difficulty,
                )
                .first()
            )

            if not quiz:
                quiz = Quiz(
                    lesson_id=lesson.id,
                    title=f"{lesson.title} - {difficulty}",
                    difficulty=difficulty,
                )
                db.add(quiz)
                db.flush()

            existing = (
                db.query(Question)
                .filter(Question.quiz_id == quiz.id)
                .all()
            )

            if len(existing) >= 30:
                print(f"{difficulty}: already has {len(existing)} questions; skipped.")
                continue

            existing_texts = {q.question.strip().lower() for q in existing}

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
                        correct_answer=new_correct_letter,
                    )
                )

                existing_texts.add(question_text.strip().lower())
                existing.append(None)
                added += 1

        db.commit()

        print("\nFINAL VERIFICATION")
        total = 0

        for difficulty in QUESTION_BANK:
            quiz = (
                db.query(Quiz)
                .filter(
                    Quiz.lesson_id == lesson.id,
                    Quiz.difficulty == difficulty,
                )
                .first()
            )

            count = (
                db.query(Question)
                .filter(Question.quiz_id == quiz.id)
                .count()
                if quiz
                else 0
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