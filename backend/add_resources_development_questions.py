import os
import sys
import random
import logging
from pathlib import Path

# Keep terminal output clean
logging.disable(logging.CRITICAL)

# Use the project's root database
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "adaptive_learning.db"

os.environ["DATABASE_URL"] = (
    f"sqlite:///{DATABASE_PATH.as_posix()}"
)

sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from app.database.connection import SessionLocal
from app.models.student import Student
from app.models.lesson import Lesson
from app.models.quiz import Quiz
from app.models.question import Question
from app.models.progress import Progress
from app.models.session import LearningSession
from app.models.reward import RewardHistory


LESSON_TITLE = "Resources and Development"
SUBJECT = "Social Science"


QUESTION_BANK = {
    "Easy": [
        ("What is a resource?", "Anything that satisfies a need and has utility", "Only money", "Only machines", "Something with no use", "A"),
        ("Which of these is a natural resource?", "Plastic", "Water", "Computer", "Concrete", "B"),
        ("Which resource is renewable?", "Coal", "Petroleum", "Sunlight", "Natural gas", "C"),
        ("Which is a non-renewable resource?", "Wind", "Sunlight", "Flowing water", "Coal", "D"),
        ("Which of these is a human-made resource?", "Road", "River", "Forest", "Mountain", "A"),
        ("Which resource is obtained from forests?", "Petroleum", "Timber", "Iron ore", "Natural gas", "B"),
        ("Which is a biotic resource?", "Air", "Rocks", "Plants", "Sunlight", "C"),
        ("Which is an abiotic resource?", "Animals", "Trees", "Fish", "Minerals", "D"),
        ("Which resource provides energy from moving air?", "Wind", "Coal", "Petroleum", "Uranium", "A"),
        ("Which of these is a human resource?", "A river", "A skilled teacher", "A mineral deposit", "A forest", "B"),
        ("What does conservation of resources mean?", "Using everything quickly", "Avoiding all resources", "Using resources carefully", "Wasting resources", "C"),
        ("Which resource is essential for agriculture?", "Plastic", "Petroleum only", "Gold", "Soil", "D"),
        ("Which is an example of a human-made resource?", "A bridge", "A river", "A forest", "A natural lake", "A"),
        ("Which of these is a fossil fuel?", "Wind", "Petroleum", "Sunlight", "Tidal energy", "B"),
        ("Which resource is used to generate solar power?", "Coal", "Timber", "Sunlight", "Iron", "C"),
        ("Which resource is commonly used to make paper?", "Copper", "Petroleum only", "Sand", "Wood pulp", "D"),
        ("What is the main purpose of resource conservation?", "To protect resources for future use", "To increase wastage", "To stop all development", "To use resources without planning", "A"),
        ("Which of these is a water resource?", "Plastic", "A lake", "A road", "A factory", "B"),
        ("Which activity can help conserve water?", "Leaving taps open", "Washing roads daily", "Rainwater harvesting", "Throwing waste into rivers", "C"),
        ("Which of these is a mineral resource?", "Cotton", "Wheat", "Fish", "Iron ore", "D"),
        ("What is sustainable development?", "Development that considers future generations", "Using all resources immediately", "Stopping every economic activity", "Increasing pollution", "A"),
        ("Which resource is used to produce wind energy?", "Coal deposits", "Moving air", "Petroleum", "Wood", "B"),
        ("Which action helps prevent soil erosion?", "Removing all plants", "Overgrazing", "Planting trees", "Leaving soil uncovered", "C"),
        ("Which of these is a natural resource?", "A factory", "A railway line", "A plastic bottle", "A river", "D"),
        ("Which resource is important for building construction?", "Sand", "Clouds", "Wild animals", "Sunlight alone", "A"),
        ("Which practice can reduce household waste?", "Burning all rubbish", "Reusing materials", "Throwing waste into lakes", "Buying unnecessary products", "B"),
        ("What is recycling?", "Dumping waste in forests", "Using a product only once", "Processing used materials into usable products", "Wasting raw materials", "C"),
        ("Which is an example of a renewable resource?", "Coal", "Petroleum", "Natural gas", "Wind energy", "D"),
        ("Why are forests important resources?", "They provide timber and support biodiversity", "They increase soil erosion everywhere", "They produce plastic naturally", "They have no ecological value", "A"),
        ("What is the basic aim of resource planning?", "Using resources without considering needs", "Using resources efficiently and fairly", "Increasing pollution", "Exhausting mineral deposits quickly", "B"),
    ],

    "Medium": [
        ("Which pair contains only renewable energy sources?", "Coal and petroleum", "Natural gas and coal", "Solar and wind energy", "Petroleum and uranium", "C"),
        ("Why are resources not equally distributed across the world?", "All places have identical climates", "People distribute every resource equally", "Resources exist only in cities", "Physical conditions vary from place to place", "D"),
        ("Which classification is based on whether a resource is living or non-living?", "Biotic and abiotic", "Renewable and non-renewable", "Individual and community", "Potential and developed", "A"),
        ("What are potential resources?", "Resources already fully used everywhere", "Resources that may be useful in the future", "Resources that have no possible use", "Resources found only underground", "B"),
        ("What are developed resources?", "Resources that have never been surveyed", "Resources that cannot be used", "Resources surveyed and assessed for use", "Resources that exist only in theory", "C"),
        ("What are stock resources?", "Resources that are always fully accessible", "Resources already exhausted", "Resources with no scientific value", "Materials that could be useful but lack suitable technology for use", "D"),
        ("What are reserves?", "Part of stock that can be used with existing technology but is saved for future use", "Resources that have no known use", "Resources that are already destroyed", "Only resources found in oceans", "A"),
        ("Which is an example of an actual resource?", "An unexplored mineral deposit with unknown quantity", "A surveyed coal deposit being mined", "A possible future wind farm site", "An untested underground deposit", "B"),
        ("Why is resource planning important in India?", "Resources are unlimited", "Every region has the same resources", "Resources are unevenly distributed and need careful use", "Planning eliminates the need for conservation", "C"),
        ("Which is the first major step in resource planning?", "Using every resource immediately", "Building factories everywhere", "Importing all resources", "Identifying and surveying resources", "D"),
        ("Which action is part of resource planning?", "Matching resource development with national plans", "Ignoring regional differences", "Avoiding resource surveys", "Using resources without assessment", "A"),
        ("What is land degradation?", "Improvement in soil fertility", "Decline in the quality or productive capacity of land", "Creation of new forests", "Increase in groundwater recharge", "B"),
        ("Which activity can cause land degradation?", "Afforestation", "Contour ploughing", "Overgrazing", "Rainwater harvesting", "C"),
        ("How can mining contribute to land degradation?", "It always improves soil fertility", "It creates forests automatically", "It eliminates waste", "It can damage land and produce mining waste", "D"),
        ("Which method helps conserve soil on steep slopes?", "Terrace farming", "Removing vegetation", "Excessive grazing", "Uncontrolled deforestation", "A"),
        ("What is contour ploughing?", "Ploughing straight downhill", "Ploughing along the natural contour lines of a slope", "Removing topsoil", "Ploughing only during floods", "B"),
        ("How do shelter belts help conserve soil?", "They increase wind speed", "They remove all vegetation", "They reduce wind speed and limit erosion", "They make slopes steeper", "C"),
        ("What is a major cause of soil erosion?", "Planting grass", "Building check dams", "Terrace farming", "Removal of protective vegetation", "D"),
        ("Why is over-irrigation harmful in some areas?", "It may cause waterlogging and salinity", "It always improves drainage", "It prevents all soil problems", "It eliminates groundwater", "A"),
        ("Which practice can help restore degraded land?", "Uncontrolled mining", "Afforestation", "Overgrazing", "Dumping industrial waste", "B"),
        ("What does sustainable resource use require?", "Using resources as quickly as possible", "Ignoring environmental effects", "Balancing current needs with future needs", "Stopping all use of natural resources", "C"),
        ("Why are human resources important?", "People cannot improve resources", "People only consume resources", "Skills have no effect on development", "People use knowledge and skills to develop resources", "D"),
        ("Which factor can turn a material into a useful resource?", "Knowledge and technology", "Colour alone", "Its size alone", "Its location name", "A"),
        ("Why can the same natural material be a resource at one time but not another?", "Nature never changes", "Technology and human needs can change", "Materials have no utility", "Resources are always identical in value", "B"),
        ("Which approach helps manage forests sustainably?", "Clear-cutting every forest", "Burning forest waste indiscriminately", "Regulated harvesting and replanting", "Removing all wildlife habitats", "C"),
        ("Which of these is a community-level conservation activity?", "Wasting water", "Destroying local ponds", "Cutting all village trees", "Protecting a local pond and its catchment", "D"),
        ("What is rainwater harvesting?", "Collecting and storing rainwater for later use", "Sending all rainwater into drains", "Increasing water pollution", "Removing water from every well", "A"),
        ("Which of these is a non-conventional energy source?", "Coal", "Solar energy", "Petroleum", "Firewood", "B"),
        ("Why is recycling useful?", "It always creates unlimited resources", "It makes waste impossible", "It reduces demand for some new raw materials", "It eliminates the need for waste management", "C"),
        ("Which statement about resource distribution is correct?", "All resources occur in equal amounts everywhere", "Human-made resources are never regional", "Climate has no influence on resources", "Resource availability varies with physical and human factors", "D"),
    ],

    "Hard": [
        ("A region has rich mineral deposits but lacks transport and processing facilities. What best explains why the deposits may remain underused?", "Infrastructure and technology affect resource development", "Minerals have no economic value", "All minerals are renewable", "Climate alone determines mineral use", "A"),
        ("A community uses groundwater faster than rainfall replenishes it. What is the likely long-term result?", "Unlimited groundwater growth", "Declining groundwater levels", "Automatic creation of new aquifers", "No change in water availability", "B"),
        ("Which option best distinguishes a resource from a mere material?", "Every material is equally useful in all situations", "Materials never depend on human needs", "Utility, technology, and human needs influence whether something is a resource", "Resources cannot change over time", "C"),
        ("A wind-rich area has not installed turbines because suitable technology is unavailable. Wind energy there is best described as what?", "An exhausted resource", "A fully developed resource", "A non-renewable resource", "A potential resource", "D"),
        ("Why is a surveyed mineral deposit being saved for future use often classified as a reserve?", "It is part of the usable resource stock kept for future use", "It has no known possible use", "It is necessarily renewable", "It cannot be measured", "A"),
        ("Which sequence best represents resource planning?", "Use resources, ignore impacts, then survey", "Identify resources, develop a planning structure, and match plans with development", "Exhaust resources, then estimate availability", "Import everything without assessing local resources", "B"),
        ("A farmer ploughs a hillside straight downhill. Which change would best reduce runoff and soil loss?", "Remove remaining vegetation", "Increase slope length", "Plough along contour lines", "Increase uncontrolled grazing", "C"),
        ("Why can deforestation increase soil erosion?", "Tree roots increase rainfall", "Forests prevent all weathering", "Trees make soil impermeable everywhere", "Removing vegetation exposes soil to water and wind", "D"),
        ("Which situation is the clearest example of unsustainable development?", "A factory repeatedly pollutes a river used by nearby communities", "A village restores a pond", "Farmers plant trees on eroded land", "A town repairs water leaks", "A"),
        ("A mineral is known to exist, but current technology cannot extract it economically. Which category may best describe it?", "A fully developed resource", "Stock", "An actual resource already in production", "A renewable resource", "B"),
        ("Why is the distinction between renewable and non-renewable resources important?", "It proves renewable resources can never be damaged", "It means non-renewable resources are always useless", "It helps guide decisions about replenishment, conservation, and use", "It removes the need for resource planning", "C"),
        ("A farming area suffers from salinity caused partly by excessive irrigation. Which response is most appropriate?", "Increase irrigation without drainage", "Remove all crops permanently", "Allow more waterlogging", "Improve irrigation management and drainage", "D"),
        ("Which combination is most likely to reduce soil erosion on a sloping farm?", "Terrace farming and vegetation cover", "Deforestation and overgrazing", "Downhill ploughing and bare soil", "Uncontrolled mining and road cutting", "A"),
        ("Why are human beings considered an important resource?", "People cannot change their surroundings", "Education and skills help people develop and use other resources", "Human knowledge has no economic effect", "All development depends only on minerals", "B"),
        ("A district has abundant sunlight but limited coal deposits. Which energy strategy best matches its natural advantages?", "Depend entirely on imported coal", "Avoid electricity generation", "Develop suitable solar energy systems", "Replace sunlight with firewood everywhere", "C"),
        ("Which statement best describes the relationship between technology and resources?", "Technology never changes resource value", "Technology makes all resources renewable", "Resources have identical utility in every era", "Technology can make previously unusable materials useful", "D"),
        ("A community protects a forest while collecting limited forest products under agreed rules. Which principle does this illustrate?", "Sustainable resource management", "Unrestricted extraction", "Permanent resource exhaustion", "Land degradation", "A"),
        ("What is a likely consequence of excessive mining without land restoration?", "Guaranteed improvement in biodiversity", "Land damage and possible contamination", "Permanent increase in soil fertility", "Elimination of waste", "B"),
        ("Why should resource planning consider both local needs and national development?", "Every region has identical priorities", "Local communities do not use resources", "Balanced planning can improve distribution and reduce regional disparities", "National development requires ignoring local resources", "C"),
        ("A village collects rainwater, repairs leaking pipes, and protects its watershed. What is the combined purpose?", "Increase water wastage", "Prevent all rainfall", "Replace every water source immediately", "Improve water conservation and local availability", "D"),
        ("Which example best illustrates a human-made resource developed from natural materials?", "A steel bridge built using processed iron", "An untouched mountain", "A natural spring", "A wild grassland", "A"),
        ("A region has fertile soil but severe erosion due to loss of vegetation. What does this show?", "Fertile soil can never degrade", "Resource quality can decline through human activities", "All soil erosion is beneficial", "Land resources are unaffected by land use", "B"),
        ("Which strategy most directly supports intergenerational equity?", "Consume all available resources today", "Transfer pollution to another region", "Conserve resources so future generations can meet their needs", "Ignore long-term environmental effects", "C"),
        ("A country has large reserves of a mineral but chooses not to extract them immediately. Which reason best supports this decision?", "Minerals always renew in one year", "Extraction has no environmental effect", "Reserves cannot ever be used", "Future needs and environmental costs may justify careful use", "D"),
        ("Which is the strongest reason to assess resources before developing a region?", "Assessment helps estimate availability, quality, and suitable uses", "Assessment makes resources unlimited", "Assessment eliminates all environmental risks", "Assessment means development is unnecessary", "A"),
        ("Which pair correctly matches a problem with a suitable conservation method?", "Waterlogging — remove every tree", "Wind erosion — establish shelter belts", "Soil erosion — increase overgrazing", "Land degradation — dump more waste", "B"),
        ("Why can resource-rich regions still experience poverty?", "Natural resources always guarantee prosperity", "Resources cannot support livelihoods", "Infrastructure, skills, governance, and distribution also affect development", "Resource availability is the only factor in development", "C"),
        ("Which statement about sustainable development is most accurate?", "It requires using every resource immediately", "It focuses only on short-term profit", "It prohibits all economic activity", "It seeks development while protecting environmental and future needs", "D"),
        ("A forest is cleared for farming without considering soil quality or slope. Which risk is most directly increased?", "Soil erosion and land degradation", "Unlimited soil formation", "Guaranteed groundwater recharge", "Elimination of runoff", "A"),
        ("Why is resource conservation a shared responsibility?", "Only governments use resources", "Individuals, communities, industries, and governments all influence resource use", "Only farmers affect the environment", "Conservation is unrelated to daily activities", "B"),
    ],
}


def shuffle_options(question_data):
    question, option_a, option_b, option_c, option_d, correct = question_data

    options = [
        ("A", option_a),
        ("B", option_b),
        ("C", option_c),
        ("D", option_d),
    ]

    correct_text = dict(options)[correct]
    random.shuffle(options)

    new_options = [option_text for _, option_text in options]
    new_correct = "ABCD"[new_options.index(correct_text)]

    return (
        question,
        new_options[0],
        new_options[1],
        new_options[2],
        new_options[3],
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
            print(f"ERROR: Lesson '{LESSON_TITLE}' was not found.")
            print("Check that the lesson exists under Social Science.")
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

            for question_data in bank:
                question_text = question_data[0].strip().casefold()

                if question_text in existing_texts:
                    continue

                q, a, b, c, d, correct = shuffle_options(question_data)

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

                existing_texts.add(question_text)
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
            print("WARNING: The lesson does not yet contain 90 questions.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()