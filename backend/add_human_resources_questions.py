import os
import sys
import random
import logging
from pathlib import Path

logging.disable(logging.CRITICAL)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "adaptive_learning.db"

os.environ["DATABASE_URL"] = f"sqlite:///{DATABASE_PATH.as_posix()}"
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from app.database.connection import SessionLocal
from app.models.student import Student
from app.models.lesson import Lesson
from app.models.quiz import Quiz
from app.models.question import Question
from app.models.progress import Progress
from app.models.session import LearningSession
from app.models.reward import RewardHistory


LESSON_TITLE = "Human Resources"
SUBJECT = "Social Science"


QUESTION_BANK = {
    "Easy": [
        ("What does the term human resources refer to?", "People and their abilities, knowledge, and skills", "Only machines", "Only minerals", "Only rivers", "A"),
        ("Which factor helps improve the quality of human resources?", "Deforestation", "Education", "Pollution", "Soil erosion", "B"),
        ("Which of these improves people's ability to work?", "Waste disposal", "Mining only", "Skill development", "Water pollution", "C"),
        ("What is population?", "The number of factories in a country", "The amount of rainfall in a year", "The number of rivers in a region", "The total number of people living in an area", "D"),
        ("What is literacy?", "The ability to read and write", "The ability to drive only", "The number of roads in a city", "The amount of land available", "A"),
        ("Which is an example of a human resource?", "A coal deposit", "A trained nurse", "A river", "A forest", "B"),
        ("What is a census?", "A type of farming", "A weather report", "An official count and collection of population information", "A mining process", "C"),
        ("Which factor can affect population distribution?", "Colour of buildings", "Number of television channels", "Shape of roads", "Availability of water", "D"),
        ("What does birth rate measure?", "The number of live births per unit of population over a period", "The number of schools in a town", "The number of factories built", "The amount of rainfall", "A"),
        ("What does death rate measure?", "The number of students graduating", "The number of deaths in a population over a period relative to its size", "The number of houses built", "The number of rivers", "B"),
        ("What is migration?", "Growing crops", "Building factories", "Movement of people from one place to another", "Measuring rainfall", "C"),
        ("Which is an example of internal migration?", "Moving from India to Japan", "Moving from one country to another", "Moving across an international border", "Moving from one Indian state to another", "D"),
        ("Why is education important for human resources?", "It develops knowledge and skills", "It reduces all human abilities", "It prevents people from learning", "It eliminates the need for health care", "A"),
        ("Which factor supports a healthy population?", "Air pollution", "Access to health care", "Unsafe drinking water", "Lack of sanitation", "B"),
        ("What is population density?", "The total land area of a country", "The number of cities in a state", "The number of people per unit of area", "The number of schools in a village", "C"),
        ("Which population is generally considered economically active?", "Only newborn babies", "Only retired people", "Only children below school age", "People who participate in economic activities", "D"),
        ("What is unemployment?", "A situation in which people seeking work cannot find suitable employment", "A rise in literacy", "An increase in school attendance", "A growth in health services", "A"),
        ("Which is a primary-sector occupation?", "Teaching", "Farming", "Banking", "Software development", "B"),
        ("Which is a secondary-sector occupation?", "Fishing", "Forestry", "Factory manufacturing", "Teaching", "C"),
        ("Which is a tertiary-sector occupation?", "Mining", "Crop cultivation", "Fishing", "Banking", "D"),
        ("What is life expectancy?", "The average number of years a person is expected to live under prevailing conditions", "The number of people born each day", "The number of jobs in a city", "The number of schools in a district", "A"),
        ("Which is a basic human need?", "Luxury cars", "Food", "Gold jewellery", "Expensive electronics", "B"),
        ("What is meant by population growth?", "A reduction in all human activities", "A change in rainfall", "An increase in the number of people over time", "A decline in the number of schools", "C"),
        ("Which service helps improve public health?", "Open sewage disposal", "Polluted drinking water", "Unsafe waste dumping", "Vaccination", "D"),
        ("Which factor can attract people to cities?", "Employment opportunities", "Lack of transport", "Absence of schools", "Unsafe housing", "A"),
        ("What is a demographic characteristic?", "The colour of a country's flag", "An attribute of a population, such as age or sex", "The shape of a mountain", "The number of rivers", "B"),
        ("Which is an example of a skilled occupation?", "Untrained activity requiring no specific skill", "Collecting stones as a hobby", "Electrical engineering", "Walking to school", "C"),
        ("Why is sanitation important?", "It increases disease transmission", "It makes drinking water unsafe", "It prevents access to health care", "It helps protect health and reduce disease", "D"),
        ("What is a population pyramid used to show?", "The age and sex composition of a population", "The height of mountains", "The amount of rainfall", "The number of factories", "A"),
        ("Why are people called a country's human resource?", "People only consume resources", "People use knowledge and skills to contribute to society and development", "People have no role in economic growth", "People cannot develop new technology", "B"),
    ],

    "Medium": [
        ("Which combination most directly improves the quality of human resources?", "Mining, deforestation, and pollution", "Population growth alone", "Education, health care, and skill development", "Increasing waste production", "C"),
        ("What is the natural increase in population?", "Total immigration only", "Total emigration only", "The number of schools built", "Births minus deaths over a period", "D"),
        ("How can net migration affect population change?", "Immigration and emigration can increase or decrease the population", "Migration never affects population", "Only births affect population size", "Only rainfall determines population size", "A"),
        ("Why are densely populated regions often found near fertile plains?", "Fertile plains prevent all human activity", "They may offer suitable land, water, transport, and livelihoods", "They always have no employment", "They have no agricultural value", "B"),
        ("What is an important cause of uneven population distribution?", "All places have identical climates", "People never migrate", "Physical conditions and economic opportunities vary by region", "Population is unrelated to resources", "C"),
        ("What is the dependency ratio broadly used to compare?", "The number of rivers with mountains", "The amount of land with rainfall", "The number of factories with roads", "The dependent-age population relative to the working-age population", "D"),
        ("Why can a high literacy rate benefit a country?", "It can improve access to information, employment, and participation", "It always increases unemployment", "It prevents skill development", "It eliminates the need for health services", "A"),
        ("Which situation is an example of rural-to-urban migration?", "A person moves from one city to another country", "A family moves from a village to a city for work", "A student walks to school", "A farmer travels to a nearby field daily", "B"),
        ("What is one possible effect of rapid urban population growth?", "Automatic elimination of housing demand", "No change in transport needs", "Greater pressure on housing, transport, and public services", "A guaranteed reduction in waste", "C"),
        ("Why is the age structure of a population important?", "It only shows the size of mountains", "It determines the amount of rainfall", "It makes education unnecessary", "It helps estimate future needs for schools, jobs, and health care", "D"),
        ("What is human capital?", "The knowledge, skills, health, and abilities of people", "Only physical machinery", "Only mineral deposits", "Only agricultural land", "A"),
        ("Why can investment in health care improve productivity?", "Healthy people can never become ill", "Better health can support attendance, learning, and the ability to work", "Health care has no effect on education", "It eliminates the need for nutrition", "B"),
        ("Which is an example of seasonal unemployment?", "A person works throughout the year", "A student attends classes", "An agricultural worker has no work during an off-season", "A doctor works regularly at a hospital", "C"),
        ("What is disguised unemployment?", "Everyone in a workplace is fully productive", "A person is on a planned holiday", "A worker receives advanced training", "More people are employed than necessary, so some add little or no extra output", "D"),
        ("How can vocational education help young people?", "It develops practical skills relevant to particular occupations", "It prevents people from entering employment", "It removes the need for learning", "It reduces all workplace skills", "A"),
        ("Why can gender inequality weaken human-resource development?", "It always increases access to education", "It can prevent some people from accessing education, health care, and jobs", "It guarantees equal opportunities", "It has no effect on economic participation", "B"),
        ("What is the purpose of population surveys?", "To measure only the weather", "To identify mineral deposits only", "To collect information for planning services and understanding population trends", "To determine the colour of buildings", "C"),
        ("Which is an example of international migration?", "Moving from one village to another in the same state", "Travelling to a nearby town for shopping", "Commuting to work every day", "Moving from India to another country to live", "D"),
        ("Why can education reduce some forms of social inequality?", "It can expand knowledge, skills, and access to opportunities", "It prevents all people from working", "It guarantees identical incomes", "It eliminates every social problem automatically", "A"),
        ("What is the working-age population?", "Only people above 90 years old", "People in the age range commonly considered capable of working, as defined by a study", "Only infants", "Only people attending primary school", "B"),
        ("Which measure is commonly used to assess population health?", "Number of shopping centres", "Number of roads only", "Life expectancy", "Number of television stations", "C"),
        ("How can poor sanitation affect human resources?", "It guarantees better school attendance", "It eliminates infectious diseases", "It has no effect on productivity", "It can increase disease and reduce participation in education or work", "D"),
        ("Which factor is a pull factor for migration?", "Availability of jobs", "Armed conflict forcing people to leave", "Severe drought in a home region", "A natural disaster destroying homes", "A"),
        ("Which factor is a push factor for migration?", "Better employment in a destination", "Lack of livelihood opportunities in the home region", "Access to higher education in a destination", "Improved health services elsewhere", "B"),
        ("Why can a rapidly ageing population create planning challenges?", "It always increases the number of schoolchildren", "It eliminates demand for health care", "It can increase demand for pensions, health services, and care", "It guarantees an unlimited workforce", "C"),
        ("What is the main purpose of a population pyramid?", "To show industrial production", "To show annual rainfall", "To measure the depth of rivers", "To visualize age and sex distribution", "D"),
        ("Which statement best explains the relationship between population and resources?", "Population needs and skills influence how resources are used and developed", "Population has no relationship to resources", "More people always cause economic decline", "Resources are unrelated to human needs", "A"),
        ("How can digital literacy improve employment opportunities?", "It prevents people from learning new skills", "It can help people access information and use digital tools at work", "It removes the need for education", "It guarantees every person a job", "B"),
        ("Which condition is most likely to improve child development?", "Unsafe water and poor nutrition", "Lack of schooling", "Access to nutrition, education, health care, and a safe environment", "Exposure to untreated waste", "C"),
        ("What is a major goal of human-resource planning?", "To ignore future skill requirements", "To prevent education and training", "To focus only on population size", "To align people's skills and well-being with social and economic needs", "D"),
    ],

    "Hard": [
        ("A country has a large young population but few suitable jobs. Which policy combination could best help?", "Improve education, vocational training, job creation, and links between skills and employers", "Reduce all school access", "Ignore employment demand", "Stop collecting labour-market information", "A"),
        ("Why might rapid population growth strain public services?", "Demand for services always decreases", "Schools, hospitals, housing, and infrastructure may struggle to keep pace", "Population size has no effect on services", "It automatically increases the supply of every service", "B"),
        ("A region has high literacy but poor health outcomes. What does this suggest?", "Education alone solves every development problem", "Health has no relationship to human resources", "Human-resource development requires attention to health and other living conditions as well as education", "Literacy prevents access to health care", "C"),
        ("Which measure best captures the natural increase of a population?", "Immigration minus emigration", "Total number of schools", "Number of jobs created", "Birth rate minus death rate over the same period", "D"),
        ("A country experiences both immigration and a higher number of deaths than births. What determines whether its population grows?", "The combined effect of natural change and net migration", "Births alone, regardless of migration", "Deaths alone, regardless of migration", "The number of schools alone", "A"),
        ("Why can an ageing population affect a country's labour market?", "It always increases the number of children", "Retirements may reduce the working-age share while demand for care increases", "It eliminates the need for skills", "It guarantees lower public spending", "B"),
        ("Which is the best example of investing in human capital?", "Building a road without considering any other need", "Extracting minerals without training workers", "Providing quality education, health care, and relevant skill training", "Increasing waste production", "C"),
        ("Why can a large population be both an opportunity and a challenge?", "It always guarantees prosperity", "It always causes poverty", "It has no effect on economic development", "People can contribute skills and labour, but need education, health care, and employment opportunities", "D"),
        ("A region experiences skilled-worker migration to another country. What is a possible effect on the region of origin?", "It may lose some skilled workers, although remittances and knowledge links can provide benefits", "It always gains every migrant's skills locally", "It eliminates all migration-related effects", "It guarantees that no jobs remain vacant", "A"),
        ("Why should population policies consider age and sex structure rather than population size alone?", "Total population size explains every service need", "Different population groups have different education, health, and employment needs", "Age structure has no planning value", "Sex structure determines rainfall", "B"),
        ("A government expands vocational education but does not assess employers' needs. What is a possible limitation?", "All trainees automatically receive suitable jobs", "Training becomes unnecessary", "Some skills taught may not match available employment opportunities", "Labour-market demand disappears", "C"),
        ("Why is disguised unemployment sometimes difficult to identify?", "It always appears as complete joblessness", "It occurs only in factories", "It can be measured only through rainfall", "People may appear employed even when some workers add little additional output", "D"),
        ("Which combination best supports inclusive human-resource development?", "Equal access to education, health care, skill development, and employment opportunities", "Restrict education to a small group", "Exclude disadvantaged communities from training", "Reduce access to basic health services", "A"),
        ("A city attracts migrants faster than housing construction expands. Which outcome is plausible?", "Housing demand disappears", "Pressure on housing and informal settlements may increase", "Transport needs become zero", "Public services become unnecessary", "B"),
        ("Why should census information be interpreted carefully?", "It always provides perfect information about every individual", "Population data can never change", "Definitions, coverage, timing, and data quality affect interpretation", "It measures only rainfall", "C"),
        ("A country has high life expectancy but low labour-force participation among some groups. What should policymakers examine?", "Only the national flag", "Only annual rainfall", "Only the number of rivers", "Barriers involving skills, health, care responsibilities, discrimination, and available jobs", "D"),
        ("How can poor nutrition affect educational outcomes?", "It can impair health, concentration, attendance, and learning", "It always improves memory", "It has no effect on children's development", "It eliminates the need for schools", "A"),
        ("Why can female education contribute to broader development outcomes?", "It prevents women from participating in work", "It can expand opportunities and improve outcomes for individuals, families, and communities", "It guarantees identical outcomes in every situation", "It has no relationship to health or employment", "B"),
        ("A region has many unemployed graduates while employers report skill shortages. What is a plausible explanation?", "The region has too many rivers", "Education has no economic value", "Qualifications and acquired skills may not match employers' needs", "All jobs require exactly the same skills", "C"),
        ("Which approach best evaluates the success of a human-resource development programme?", "Count only the number of buildings constructed", "Measure only population size", "Ignore participants' outcomes", "Assess changes in skills, employment, health, access, and relevant long-term outcomes", "D"),
        ("Why can migration statistics be important for urban planning?", "They help estimate changing demand for housing, transport, schools, and health services", "They eliminate the need for population data", "They predict every individual's future", "They measure only industrial pollution", "A"),
        ("Which is the most appropriate interpretation of population density?", "It proves all people live equally spread out", "It is an average that may conceal substantial differences within a region", "It directly measures income equality", "It shows only the number of cities", "B"),
        ("Why might a country with a high dependency ratio face fiscal pressure?", "Dependents always pay all public costs", "The working-age population never pays taxes", "A relatively smaller working-age population may support more dependents through taxes and services", "Dependency ratios have no economic relevance", "C"),
        ("A government wants to reduce youth unemployment. Which strategy is most comprehensive?", "Offer training without considering jobs", "Ignore local employers", "Stop career guidance", "Combine relevant training, job creation, career support, and employer partnerships", "D"),
        ("Why is health considered part of human capital?", "Health influences people's ability to learn, work, and participate in society", "Health is unrelated to productivity", "Only machines affect economic output", "Healthcare prevents all illness", "A"),
        ("Which factor best explains why population distribution is uneven?", "Every region has identical resources", "Climate, relief, water, jobs, infrastructure, and history vary geographically", "People never respond to economic opportunities", "All land is equally suitable for settlement", "B"),
        ("A region's working-age population grows faster than employment opportunities. What is a possible result?", "Unemployment must disappear", "Wages and jobs can never change", "Unemployment or underemployment may rise if job creation does not keep pace", "Education becomes unnecessary", "C"),
        ("Why should human-resource development include lifelong learning?", "Skills never become outdated", "Technology has no effect on occupations", "Workers never need to adapt", "People may need to update skills as technology and job requirements change", "D"),
        ("Which statement best explains the relationship between human resources and economic development?", "People's health, education, skills, and opportunities influence productive capacity and innovation", "Economic development depends only on mineral deposits", "Education and health have no economic relevance", "Population size alone determines prosperity", "A"),
        ("A government uses population data to plan hospitals and schools. What is the main benefit?", "It guarantees that every service will be perfect", "It can help estimate where services are needed and how much capacity may be required", "It eliminates the need for local assessment", "It prevents future population change", "B"),
    ],
}


# Validate all questions before accessing the database.
for difficulty, bank in QUESTION_BANK.items():
    if len(bank) != 30:
        raise ValueError(
            f"{difficulty} must have 30 questions; found {len(bank)}."
        )

    for index, item in enumerate(bank, start=1):
        if len(item) != 6:
            raise ValueError(
                f"{difficulty} question #{index} has {len(item)} values: "
                f"{item[0]}"
            )

        if item[5] not in {"A", "B", "C", "D"}:
            raise ValueError(
                f"Invalid answer key in {difficulty} question #{index}."
            )


def shuffle_options(item):
    question, a, b, c, d, correct = item

    options = {"A": a, "B": b, "C": c, "D": d}
    correct_text = options[correct]

    shuffled = list(options.values())
    random.shuffle(shuffled)

    new_correct = "ABCD"[shuffled.index(correct_text)]

    return (
        question,
        shuffled[0],
        shuffled[1],
        shuffled[2],
        shuffled[3],
        new_correct,
    )


def main():
    db = SessionLocal()

    try:
        lesson = (
            db.query(Lesson)
            .filter(
                Lesson.title == LESSON_TITLE,
                Lesson.topic == SUBJECT,
            )
            .first()
        )

        if not lesson:
            print(f"ERROR: '{LESSON_TITLE}' was not found under {SUBJECT}.")
            return

        added = 0

        for difficulty, bank in QUESTION_BANK.items():
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
                    title=f"{LESSON_TITLE} - {difficulty} Quiz",
                    difficulty=difficulty,
                )
                db.add(quiz)
                db.flush()

            existing = (
                db.query(Question)
                .filter(Question.quiz_id == quiz.id)
                .all()
            )

            existing_texts = {
                q.question.strip().casefold()
                for q in existing
            }

            for item in bank:
                key = item[0].strip().casefold()

                if key in existing_texts:
                    continue

                q, a, b, c, d, correct = shuffle_options(item)

                db.add(
                    Question(
                        quiz_id=quiz.id,
                        question=q,
                        option_a=a,
                        option_b=b,
                        option_c=c,
                        option_d=d,
                        correct_answer=correct,
                    )
                )

                existing_texts.add(key)
                added += 1

        db.commit()

        print("\nFINAL VERIFICATION")
        print(f"Lesson: {LESSON_TITLE}")
        print(f"Subject: {SUBJECT}")

        total = 0

        for difficulty in ["Easy", "Medium", "Hard"]:
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

        if total == 90:
            print("SUCCESS: All 90 questions are present!")
        else:
            print("WARNING: The total is not 90. Check the counts above.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()