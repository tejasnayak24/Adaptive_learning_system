import os
import sys
import random
import logging
from pathlib import Path

logging.disable(logging.CRITICAL)

# --------------------------------------------------
# DATABASE CONFIGURATION
# --------------------------------------------------

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


LESSON_TITLE = "Industries"
SUBJECT = "Social Science"


# Each question has exactly six values:
# question, option A, option B, option C, option D, correct answer

QUESTION_BANK = {
    "Easy": [
        ("What is an industry?", "An economic activity that produces goods or provides services", "Only growing crops", "Only studying weather", "Only collecting rainwater", "A"),
        ("Which is a manufacturing industry?", "Fishing", "Car manufacturing", "Forestry", "Hunting", "B"),
        ("Which industry uses cotton as a raw material?", "Iron and steel", "Cement", "Textile", "Petroleum refining", "C"),
        ("Which industry produces cement?", "Dairy", "Fishing", "Tourism", "Cement industry", "D"),
        ("Which is an agro-based industry?", "Sugar industry", "Iron and steel", "Aluminium smelting", "Petroleum refining", "A"),
        ("Which industry uses iron ore to produce steel?", "Tea processing", "Iron and steel", "Cotton textile", "Paper recycling only", "B"),
        ("What is a raw material?", "A finished product", "A transport service", "A basic material used to make a product", "A financial document", "C"),
        ("Which is a mineral-based industry?", "Dairy farming", "Fruit cultivation", "Fishing", "Iron and steel", "D"),
        ("Which industry processes milk into cheese and butter?", "Dairy industry", "Cement industry", "Shipbuilding", "Coal mining", "A"),
        ("What does manufacturing involve?", "Growing crops only", "Converting raw materials into goods", "Providing rainfall", "Mapping mountains only", "B"),
        ("Which is an example of a cottage industry?", "Large automobile factory", "Oil refinery", "Making baskets at home", "Large steel plant", "C"),
        ("Which industry produces paper?", "Automobile", "Shipbuilding", "Petroleum refining", "Paper industry", "D"),
        ("Which factor influences industrial location?", "Availability of raw materials", "Colour of nearby houses", "Television programmes", "Shape of school bags", "A"),
        ("Which is a service industry?", "Steel production", "Tourism", "Cement manufacturing", "Cotton spinning", "B"),
        ("What is an industrial region?", "An area used only for forests", "A place without economic activity", "An area where industries are concentrated", "An area consisting only of farms", "C"),
        ("Which industry produces vehicles?", "Textile", "Dairy", "Paper", "Automobile", "D"),
        ("Which industry uses sugarcane to produce sugar?", "Sugar industry", "Cement industry", "Steel industry", "Electronics industry", "A"),
        ("Who is an industrial worker?", "A person who only studies rivers", "A person employed in industrial activities", "A person who predicts weather", "A person who grows forests only", "B"),
        ("Which is an example of a large-scale industry?", "A person making baskets at home", "A family pottery workshop", "A large automobile manufacturing plant", "A home garden", "C"),
        ("Which industry processes crude oil into fuels?", "Cotton textile", "Dairy", "Sugar", "Petroleum refining", "D"),
        ("What is a finished product?", "A good ready for use or sale", "A raw mineral deposit", "An unprocessed crop only", "An unused natural resource", "A"),
        ("Which industry makes clothes from fabric?", "Coal mining", "Garment industry", "Cement production", "Petroleum extraction", "B"),
        ("Which is a forest-based industry?", "Sugar industry", "Dairy industry", "Paper industry using wood pulp", "Iron ore mining", "C"),
        ("What is industrial pollution?", "Environmental protection", "Safe recycling", "Planting trees", "Pollution caused by industrial activities", "D"),
        ("Which industry produces electronic devices?", "Electronics industry", "Agriculture only", "Forestry only", "Fishing only", "A"),
        ("Why do industries need energy?", "To eliminate raw materials", "To operate machinery and production processes", "To stop transportation", "To prevent production", "B"),
        ("Which is an industrial raw material?", "A finished television", "A packaged car", "Cotton used to make fabric", "A railway ticket", "C"),
        ("What is an industrial product?", "A natural mountain", "Rainfall", "Wild grass", "A good produced through industrial activity", "D"),
        ("Which industry manufactures medicines?", "Pharmaceutical industry", "Cement industry", "Jute cultivation", "Coal transport", "A"),
        ("Why are industries important to an economy?", "They eliminate services", "They produce goods, create jobs, and support economic activity", "They use no resources", "They have no connection to trade", "B"),
    ],

    "Medium": [
        ("Which group classifies industries by their raw materials?", "Rural, urban, coastal", "Local, national, international", "Agro-based, mineral-based, forest-based", "Public, private, household only", "C"),
        ("Which is a mineral-based industry?", "Sugar processing", "Dairy processing", "Cotton textiles", "Iron and steel production", "D"),
        ("Why are industries often located near raw materials?", "To reduce transport costs and improve supply", "To avoid raw materials", "To eliminate all labour", "To prevent access to markets", "A"),
        ("What is a footloose industry?", "An industry always beside a coal mine", "An industry relatively less dependent on a specific raw-material location", "An industry using only crops", "An industry that cannot use electricity", "B"),
        ("What is important when locating a food-processing industry?", "Distance from all transport", "Lack of storage", "Access to raw materials, transport, and markets", "Absence of electricity", "C"),
        ("What is the purpose of industrial infrastructure?", "To replace all workers", "To eliminate markets", "To prevent movement of goods", "To support production with power, roads, and communication", "D"),
        ("What characterizes a public-sector industry?", "Ownership and operation by the government", "Ownership by one private individual", "A household craft activity", "An informal stall only", "A"),
        ("What characterizes a private-sector industry?", "It is always government-owned", "It is owned by private individuals or companies", "It cannot employ workers", "It produces no goods", "B"),
        ("What is a joint-sector enterprise?", "A household activity", "A factory without ownership", "An enterprise involving public and private participation", "A mineral deposit", "C"),
        ("Why is iron and steel considered a basic industry?", "It produces only food", "It is used only in decoration", "It has no industrial applications", "It supplies materials to many other industries", "D"),
        ("Why is the iron and steel industry important?", "Steel is used in construction, machinery, transport, and other industries", "Steel is used only for food", "Steel has no industrial applications", "Steel replaces all agricultural products", "A"),
        ("Which factors matter when locating a large factory?", "Colour of the land", "Raw materials, power, labour, transport, and markets", "Television signals only", "Number of nearby parks", "B"),
        ("What is an industrial cluster?", "An isolated farm", "A single household workshop", "A concentration of related industries or businesses", "A natural forest only", "C"),
        ("How can transport access improve competitiveness?", "It removes all costs", "It makes products unnecessary", "It eliminates competition", "It can reduce delivery time and transport costs", "D"),
        ("What is a concern associated with untreated industrial wastewater?", "It can contaminate rivers and harm aquatic life", "It always improves drinking water", "It has no ecosystem effects", "It guarantees clean groundwater", "A"),
        ("How can recycling benefit manufacturing?", "It makes all raw materials unnecessary", "It can reduce virgin-material demand and waste", "It guarantees zero pollution", "It prevents all costs", "B"),
        ("Why is skilled labour important in modern industries?", "It makes training unnecessary", "It eliminates quality control", "It supports efficient operation, maintenance, and innovation", "It prevents technology from changing", "C"),
        ("What is industrial automation?", "Replacing all energy with sunlight", "Producing goods without equipment", "Stopping computer use", "Using control systems and machinery to perform tasks automatically", "D"),
        ("What is the purpose of quality control?", "Checking whether products meet required standards", "Increasing defective products", "Preventing product testing", "Removing customer feedback", "A"),
        ("Why are industrial estates developed?", "To isolate factories from infrastructure", "To provide planned locations with shared facilities", "To prevent transport access", "To eliminate industrial jobs", "B"),
        ("Which is a secondary-sector activity?", "Growing wheat", "Fishing", "Turning cotton into fabric", "Providing legal advice", "C"),
        ("Which tertiary-sector activity supports industry?", "Mining iron ore", "Growing sugarcane", "Manufacturing cement", "Transporting finished goods", "D"),
        ("How can industries contribute to urbanization?", "They attract workers and support town and city growth", "They always reduce urban populations", "They eliminate housing needs", "They prevent service development", "A"),
        ("Why is reliable electricity important for factories?", "It eliminates machinery", "Power interruptions can disrupt production", "It makes raw materials unnecessary", "It prevents maintenance", "B"),
        ("What is industrial diversification?", "Producing one product everywhere", "Stopping all new industries", "Developing a wider range of industries and products", "Replacing all factories with farms", "C"),
        ("Why might a textile industry locate near a major market?", "To avoid producing goods", "Markets have no influence", "To eliminate workers", "To improve customer access and reduce distribution costs", "D"),
        ("Which measure can reduce industrial air pollution?", "Installing suitable emission-control equipment", "Burning waste openly", "Ignoring emissions", "Removing monitoring systems", "A"),
        ("What is the purpose of factory safety measures?", "To increase hazards", "To protect workers and reduce accidents", "To eliminate training", "To prevent emergency planning", "B"),
        ("Why do high-technology industries need skilled workers?", "They do not use technical knowledge", "They require no innovation", "They depend on specialized knowledge, design, and development", "They only process crops", "C"),
        ("What is sustainable industrial development?", "Increasing output regardless of damage", "Prohibiting all manufacturing", "Ignoring workers and communities", "Balancing production with responsible resource and pollution management", "D"),
    ],

    "Hard": [
        ("A steel plant is near iron ore but far from reliable power and transport. What should planners do?", "Evaluate raw materials, power, transport, labour, and markets together", "Choose based only on ore", "Ignore energy access", "Assume transport costs do not matter", "A"),
        ("Why may a software company be less tied to bulky raw materials than a steel plant?", "Software uses more iron ore", "Software depends more on skills and digital infrastructure than bulky physical inputs", "Steel needs no raw materials", "Software cannot use communication networks", "B"),
        ("A textile factory releases untreated dye wastewater into a river. What is the best response?", "Increase discharge during dry weather", "Move waste to farmland untreated", "Treat wastewater appropriately and monitor discharge", "Stop water-quality monitoring", "C"),
        ("Why can related firms in an industrial cluster improve productivity?", "They eliminate all competition", "They make transport irrelevant", "They prevent workers changing jobs", "They can improve supplier access, labour matching, and knowledge sharing", "D"),
        ("What is a balanced assessment of industrial automation?", "It may improve consistency and productivity while changing workers' required skills", "It guarantees no workers are ever needed", "It always reduces quality", "It eliminates maintenance", "A"),
        ("Why is iron and steel called a basic industry?", "It produces only food", "It supplies materials used by many industries and infrastructure projects", "It does not use minerals", "It has no connection to manufacturing", "B"),
        ("A region depends on one industry for most jobs. What is a major risk?", "Employment can never change", "It becomes immune to recessions", "A downturn can affect many local workers and businesses", "All other industries automatically grow", "C"),
        ("Which strategy supports industrial development where infrastructure is limited?", "Build factories without checking power or transport", "Ignore worker skills", "Avoid communication networks", "Coordinate infrastructure, training, services, and suitable industries", "D"),
        ("Why can the environmental cost of a product exceed its factory production cost?", "Pollution and resource damage can impose costs on communities and ecosystems", "Environmental damage benefits everyone", "Factories have no external effects", "Resource extraction is always free", "A"),
        ("Which policies best promote cleaner industrial production?", "Remove pollution standards", "Encourage efficient energy use, cleaner technology, waste treatment, and enforcement", "Allow untreated waste into rivers", "Discourage recycling", "B"),
        ("A company chooses a factory site near customers but far from suppliers. How should it evaluate the decision?", "Consider customer distance alone", "Ignore transport and storage costs", "Compare total logistics costs, input availability, and market access", "Avoid supply-chain analysis", "C"),
        ("Why can industrial specialization create risks as well as benefits?", "It eliminates regional inequality", "It guarantees unlimited demand", "It makes worker skills irrelevant", "It improves efficiency but may increase dependence on a narrow range of activities", "D"),
        ("Which strategy best reduces manufacturing waste?", "Improve material efficiency, reuse by-products, and design for repair or recycling", "Increase unnecessary packaging", "Discard usable materials immediately", "Ignore waste data", "A"),
        ("A factory has high output but frequent worker injuries. What is the best conclusion?", "High output makes safety unnecessary", "Productivity must be assessed alongside worker safety and working conditions", "Injuries do not affect industry", "Safety always reduces quality", "B"),
        ("Why might pharmaceutical firms locate near research institutions?", "Medicines need no technical knowledge", "Research has no role in drug development", "Specialized skills and collaboration can support innovation and quality", "Pharmaceuticals require no quality controls", "C"),
        ("What is important when planning electronics manufacturing?", "Farmland alone", "A nearby coal mine alone", "Ocean fishing alone", "Reliable electricity, skilled workers, supply chains, and communication infrastructure", "D"),
        ("Which example shows industrial backward and forward linkages?", "A food processor buys crops from farmers and sells packaged products to retailers", "A factory operates without suppliers or customers", "A company has no connection to other sectors", "A mine produces no usable output", "A"),
        ("Why is industrial research and development important?", "It prevents new products", "It can improve processes, product quality, and technological competitiveness", "It guarantees every invention succeeds", "It eliminates skilled workers", "B"),
        ("A factory reduces energy consumption per unit of product. What is a plausible result?", "Costs must become infinite", "Waste must increase", "Energy efficiency may improve and emissions may fall depending on the energy source", "Quality must decline", "C"),
        ("Why should industrial planning consider nearby residential areas?", "Factories cannot affect residents", "Residential areas have no infrastructure needs", "Industry always improves air quality", "Noise, emissions, traffic, and safety risks can affect communities", "D"),
        ("Which action supports a circular economy?", "Design products and processes to reduce waste and keep materials in use longer", "Send reusable materials to landfill", "Discard everything after one use", "Prevent repair and reuse", "A"),
        ("Why are small-scale industries important to regional development?", "They operate only in capital cities", "They can create local jobs and use local skills and resources", "They never need markets", "They cannot support supply chains", "B"),
        ("A factory relies on one supplier for a critical component. What is a major risk?", "The factory becomes immune to disruption", "The component becomes unusable", "Supplier disruption may interrupt production", "Supplier reliability becomes irrelevant", "C"),
        ("How should two possible industrial sites be compared?", "Compare land prices only", "Ignore labour and transport", "Choose the largest site regardless of needs", "Assess total costs, infrastructure, labour, markets, and environmental impacts", "D"),
        ("Why are industrial pollution limits and monitoring important?", "They help detect and control harmful emissions and discharges", "They make pollution impossible without enforcement", "They remove the need for treatment systems", "They eliminate equipment maintenance", "A"),
        ("How can industrialization affect employment?", "It creates identical numbers of jobs in every sector", "It can create jobs while changing required skills and occupations", "It eliminates education needs", "It has no effect on labour markets", "B"),
        ("Factories face frequent electricity cuts. What could improve production reliability?", "Ignore maintenance", "Increase dependence on unpredictable power", "Improve grid reliability and assess suitable backup energy options", "Stop production planning", "C"),
        ("Why is worker training important when new technologies are introduced?", "Technology never changes work tasks", "Training prevents equipment use", "Only managers need safety knowledge", "Training helps workers operate and maintain systems safely and effectively", "D"),
        ("Which example illustrates responsible industrial growth?", "Factories create jobs while managing waste, protecting workers, and using resources efficiently", "Production increases while pollution is ignored", "Worker safety is sacrificed", "Resources are exhausted without planning", "A"),
        ("Why assess the full supply chain when improving industrial sustainability?", "Only factory gates affect the environment", "Impacts occur during extraction, production, transport, use, and disposal", "Suppliers never affect emissions", "Product disposal has no consequences", "B"),
    ],
}


# --------------------------------------------------
# VALIDATE QUESTION BANK BEFORE DATABASE CHANGES
# --------------------------------------------------

for difficulty, bank in QUESTION_BANK.items():
    if len(bank) != 30:
        raise ValueError(
            f"{difficulty} must contain exactly 30 questions; found {len(bank)}."
        )

    for index, item in enumerate(bank, start=1):
        if len(item) != 6:
            raise ValueError(
                f"{difficulty} question #{index} has {len(item)} values "
                f"instead of 6: {item[0]}"
            )

        if item[5] not in {"A", "B", "C", "D"}:
            raise ValueError(
                f"{difficulty} question #{index} has an invalid answer key."
            )


def shuffle_options(item):
    question, a, b, c, d, correct = item

    options = {
        "A": a,
        "B": b,
        "C": c,
        "D": d,
    }

    correct_text = options[correct]
    shuffled = list(options.values())
    random.shuffle(shuffled)

    return (
        question,
        shuffled[0],
        shuffled[1],
        shuffled[2],
        shuffled[3],
        "ABCD"[shuffled.index(correct_text)],
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
            print(f"ERROR: Lesson '{LESSON_TITLE}' was not found.")
            print("No questions were added.")
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

            existing_questions = (
                db.query(Question)
                .filter(Question.quiz_id == quiz.id)
                .all()
            )

            existing_texts = {
                q.question.strip().casefold()
                for q in existing_questions
            }

            for item in bank:
                question_key = item[0].strip().casefold()

                if question_key in existing_texts:
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

                existing_texts.add(question_key)
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
            print(
                "WARNING: The total is not 90. "
                "Check whether this lesson already had extra questions."
            )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()