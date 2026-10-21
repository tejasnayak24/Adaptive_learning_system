import os
import random
import logging
from pathlib import Path

logging.disable(logging.CRITICAL)

# --------------------------------------------------
# DATABASE CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "adaptive_learning.db"

os.environ["DATABASE_URL"] = (
    f"sqlite:///{DATABASE_PATH.as_posix()}"
)

from app.database.connection import SessionLocal
from app.models.student import Student
from app.models.lesson import Lesson
from app.models.quiz import Quiz
from app.models.question import Question
from app.models.progress import Progress
from app.models.session import LearningSession
from app.models.reward import RewardHistory


# --------------------------------------------------
# QUESTION BANK
# Each tuple contains exactly 6 values.
# --------------------------------------------------

EASY = [
    ("What does sustainable development mean?", "Meeting present needs without compromising future generations", "Using all resources immediately", "Stopping all economic activity", "Avoiding all technology", "A"),
    ("Which of these is a renewable energy source?", "Solar energy", "Coal", "Petroleum", "Natural gas", "A"),
    ("Which resource is essential for all known human life?", "Water", "Plastic", "Petrol", "Coal", "A"),
    ("Which action helps conserve water?", "Repairing leaking taps", "Leaving taps running", "Washing one item at a time under running water", "Polluting lakes", "A"),
    ("Which activity helps reduce waste?", "Reusing containers", "Throwing reusable items away", "Burning all household waste", "Buying unnecessary products", "A"),
    ("What is biodiversity?", "The variety of living organisms", "The amount of plastic in a city", "The number of roads in a town", "The quantity of fuel used by cars", "A"),
    ("Which practice can help protect soil?", "Planting vegetation", "Removing all plant cover", "Dumping chemicals on farmland", "Leaving soil exposed to erosion", "A"),
    ("Which of these is biodegradable?", "Fruit peel", "Glass bottle", "Aluminium can", "Plastic wrapper", "A"),
    ("What is deforestation?", "Clearing or removing forests", "Planting new trees", "Protecting wildlife habitats", "Restoring wetlands", "A"),
    ("Which action helps reduce air pollution?", "Using public transport", "Burning rubbish in open spaces", "Keeping engines poorly maintained", "Burning more coal unnecessarily", "A"),
    ("What is recycling?", "Processing used materials into usable materials", "Throwing all waste into rivers", "Using every item only once", "Mixing all waste without sorting", "A"),
    ("Which of these is a fossil fuel?", "Coal", "Wind", "Sunlight", "Tidal energy", "A"),
    ("What is rainwater harvesting?", "Collecting and storing rainwater", "Allowing all rainwater to become polluted", "Removing water from every river", "Burning rainwater to produce energy", "A"),
    ("Why are trees important for the environment?", "They absorb carbon dioxide and provide habitats", "They increase plastic waste", "They prevent all rainfall", "They produce fossil fuels directly", "A"),
    ("Which farming method can reduce soil erosion?", "Contour farming on suitable slopes", "Removing all vegetation", "Ploughing directly down steep slopes in every case", "Leaving soil uncovered", "A"),
    ("What is a major cause of climate change?", "Human-caused greenhouse gas emissions", "Planting trees", "Using solar panels", "Protecting natural forests", "A"),
    ("Which is an example of clean energy?", "Wind power", "Coal power", "Diesel combustion", "Petroleum combustion", "A"),
    ("What does conservation mean?", "Protecting and managing resources responsibly", "Wasting natural resources", "Destroying wildlife habitats", "Using resources without limits", "A"),
    ("Which practice supports sustainable agriculture?", "Crop rotation", "Continuous cultivation without soil care", "Excessive chemical use without assessment", "Burning crop residues unnecessarily", "A"),
    ("What is compost made from?", "Decomposed organic waste", "Pure plastic", "Metal scraps only", "Petroleum only", "A"),
    ("Which action supports wildlife conservation?", "Protecting natural habitats", "Hunting endangered animals", "Destroying nesting areas", "Polluting forests", "A"),
    ("What is a carbon footprint?", "The greenhouse gas emissions associated with an activity or entity", "The number of trees in a forest", "The size of a person's shoe", "The depth of a river", "A"),
    ("Which transport choice can reduce emissions per passenger?", "Public bus with many passengers", "A separate car for every passenger", "An unnecessary short car journey", "A poorly maintained private vehicle", "A"),
    ("Why should plastic waste be managed properly?", "It can harm wildlife and pollute ecosystems", "It always decomposes immediately", "It improves every water source", "It has no environmental effects", "A"),
    ("Which is an example of responsible consumption?", "Buying what is needed and reducing waste", "Buying unnecessary goods and discarding them", "Replacing usable products every day", "Ignoring product durability", "A"),
    ("What is an ecosystem?", "Living organisms interacting with their environment", "A collection of roads only", "A group of buildings without living organisms", "A type of fuel", "A"),
    ("Which practice helps protect groundwater?", "Preventing harmful chemicals from entering the soil", "Dumping industrial waste onto land", "Allowing untreated sewage to seep into the ground", "Overusing groundwater without planning", "A"),
    ("What is the main purpose of protected areas?", "Conserving species and habitats", "Encouraging habitat destruction", "Increasing illegal hunting", "Eliminating all native vegetation", "A"),
    ("Which of these can help save electricity at home?", "Switching off unused lights", "Leaving every appliance running", "Using inefficient lighting unnecessarily", "Keeping devices on when not needed", "A"),
    ("What is the main idea of intergenerational equity?", "Considering fairness between present and future generations", "Giving all resources to the present generation", "Ignoring future resource needs", "Preventing future generations from using resources", "A"),
]

MEDIUM = [
    ("Why is sustainable development important?", "It balances environmental protection, social well-being and economic progress", "It focuses only on immediate profit", "It requires the complete end of development", "It encourages unlimited resource extraction", "A"),
    ("How can renewable energy support sustainable development?", "It can reduce dependence on fossil fuels and associated emissions", "It always produces zero environmental impact", "It makes energy conservation unnecessary", "It increases the need to burn coal in every case", "A"),
    ("Why is groundwater conservation necessary?", "Groundwater can be depleted when extraction exceeds recharge", "Groundwater is always unlimited", "Groundwater cannot be used by people", "Rainfall never affects groundwater", "A"),
    ("How does deforestation contribute to soil erosion?", "Removing vegetation exposes soil to wind and rain", "Tree roots always increase soil loss", "Forests prevent soil from interacting with water", "Deforestation permanently improves every soil type", "A"),
    ("Why can excessive fertilizer use harm the environment?", "Nutrients may run off into water bodies and cause eutrophication", "Fertilizers can never enter waterways", "It eliminates all aquatic plant growth", "It prevents every form of water pollution", "A"),
    ("What is the purpose of the 3Rs in waste management?", "Reduce, reuse and recycle materials", "Repair, remove and replace all resources", "Read, record and report weather", "Run, react and repeat industrial processes", "A"),
    ("How can public transportation contribute to sustainable cities?", "It can reduce congestion and emissions per passenger", "It guarantees that traffic disappears completely", "It requires every person to own a car", "It prevents people from accessing workplaces", "A"),
    ("What is one environmental benefit of urban green spaces?", "They provide habitat and can help moderate urban temperatures", "They always increase air pollution", "They eliminate the need for water management", "They prevent every natural disaster", "A"),
    ("Why is biodiversity important for ecosystem stability?", "Different species contribute to ecological processes and resilience", "Every species performs exactly the same role", "Biodiversity prevents all environmental change", "Species diversity has no relationship to ecosystems", "A"),
    ("How can drip irrigation improve water efficiency?", "It delivers water near plant roots and can reduce losses", "It floods every field continuously", "It removes the need to monitor crops", "It increases water evaporation in every case", "A"),
    ("What is eutrophication?", "Excess nutrient enrichment of water that can cause algal blooms and oxygen depletion", "The natural formation of mountain ranges", "The process of producing solar panels", "The complete absence of nutrients in soil", "A"),
    ("Why is waste segregation useful?", "It helps suitable materials be recycled or treated separately", "It makes all waste harmless immediately", "It prevents the need for waste collection", "It requires recyclable materials to be burned", "A"),
    ("How can sustainable forestry be practised?", "Harvesting responsibly while supporting forest regeneration", "Removing all trees without replanting", "Ignoring forest biodiversity", "Converting every forest into a parking area", "A"),
    ("What is the main purpose of environmental impact assessment?", "To identify and evaluate potential environmental effects before a project proceeds", "To guarantee that every project has no impact", "To determine only the cost of building materials", "To replace all project planning", "A"),
    ("Why can overfishing threaten marine ecosystems?", "Fish populations may decline faster than they can recover", "It guarantees that fish populations increase", "It removes all bycatch from fishing", "It improves marine biodiversity in every case", "A"),
    ("How can energy-efficient appliances support sustainability?", "They can provide services using less electricity", "They always consume more energy", "They make electricity generation unnecessary", "They prevent all household energy use", "A"),
    ("Why are wetlands environmentally valuable?", "They can support biodiversity, store water and reduce flood impacts", "They contain no living organisms", "They always increase flood damage", "They cannot filter pollutants", "A"),
    ("What is the relationship between poverty reduction and sustainable development?", "Improving livelihoods can support well-being when development is inclusive and sustainable", "Poverty reduction is unrelated to human well-being", "Sustainable development requires poverty to increase", "Economic opportunity must be denied to rural communities", "A"),
    ("Why can life-cycle thinking improve product sustainability?", "It considers environmental impacts across production, use and disposal", "It considers only the product's colour", "It ignores raw material extraction", "It excludes disposal from every assessment", "A"),
    ("What is one risk of relying heavily on a single natural resource?", "Resource depletion or market disruption can harm the economy", "The resource becomes unlimited", "The economy becomes immune to price changes", "Environmental monitoring becomes unnecessary", "A"),
    ("How can agroforestry benefit farmland?", "Trees and crops can be combined to support soil, biodiversity and livelihoods", "It requires removing all trees from farms", "It always prevents all crop growth", "It eliminates the need for water", "A"),
    ("Why is sustainable urban planning important?", "It coordinates housing, transport, services and environmental needs", "It considers buildings but ignores people", "It encourages unlimited land consumption", "It removes all public spaces", "A"),
    ("What does climate adaptation involve?", "Adjusting systems to reduce harm from actual or expected climate impacts", "Reducing only the colour of buildings", "Ignoring climate-related risks", "Guaranteeing that weather never changes", "A"),
    ("What does climate mitigation involve?", "Reducing greenhouse gas emissions or increasing their removal", "Preparing only for traffic congestion", "Increasing fossil fuel use without controls", "Ignoring energy production", "A"),
    ("Why can local community participation improve conservation projects?", "It incorporates local knowledge and can build community support", "It makes scientific evidence unnecessary", "It prevents residents from sharing concerns", "It guarantees that no compromise is required", "A"),
    ("How can sustainable tourism protect destinations?", "Managing visitor impacts while supporting local communities and conservation", "Allowing unlimited visitors regardless of ecological limits", "Removing local residents from all decisions", "Destroying cultural heritage to increase visitor numbers", "A"),
    ("Why is access to clean drinking water a sustainability issue?", "It affects health, equity and long-term resource management", "It matters only to industrial facilities", "It has no relationship to public health", "It makes sanitation unnecessary", "A"),
    ("What is a circular economy intended to achieve?", "Keeping products and materials in use and reducing waste", "Increasing the disposal of reusable products", "Using raw materials only once", "Eliminating all repair and reuse activities", "A"),
    ("Why should environmental policies consider social equity?", "Environmental benefits and burdens can affect communities differently", "Environmental problems affect all people identically in every case", "Equity prevents environmental monitoring", "Social conditions are never relevant to sustainability", "A"),
    ("How can restoring native vegetation benefit a degraded landscape?", "It can support habitat recovery, soil stability and water regulation", "It guarantees that every invasive species disappears immediately", "It removes the need to monitor recovery", "It prevents all future droughts", "A"),
]

HARD = [
    ("A town extracts groundwater faster than rainfall can replenish it. Which long-term response is most appropriate?", "Manage extraction, improve recharge and monitor groundwater levels", "Increase extraction without collecting data", "Ignore declining water levels", "Prevent all rainwater from entering the ground", "A"),
    ("A lake experiences repeated algal blooms after fertilizer runoff. Which response best addresses the underlying cause?", "Reduce nutrient runoff through improved farming and wastewater management", "Add more fertilizer to surrounding fields", "Remove all monitoring equipment", "Increase untreated sewage discharge", "A"),
    ("A city is choosing between two transport projects. One has high capacity but damages a sensitive habitat; the other improves public transport with lower habitat disturbance. What should planners do?", "Compare access, emissions, social benefits and ecological impacts before deciding", "Ignore habitat impacts completely", "Choose the project with the largest land footprint automatically", "Assess only construction cost", "A"),
    ("A forest provides timber, protects watersheds and supports local livelihoods. Which management strategy is most sustainable?", "Set harvesting limits, protect key habitats and involve local communities", "Clear the entire forest in one operation", "Ban all monitoring while increasing extraction", "Replace native forest with a single crop everywhere", "A"),
    ("Why can increasing agricultural production alone fail to ensure food security?", "Access, affordability, distribution and nutrition also matter", "Food security depends only on the colour of crops", "Food distribution has no effect on access", "Nutrition is unrelated to food security", "A"),
    ("A company claims its product is sustainable because the packaging is recyclable. What would provide a more complete assessment?", "Evaluate material sourcing, production, use, transport and end-of-life impacts", "Inspect only the packaging colour", "Assume recyclable packaging eliminates every impact", "Ignore energy and water consumption", "A"),
    ("A coastal community faces sea-level rise and stronger storm surges. Which plan best combines adaptation and sustainability?", "Protect or restore suitable coastal ecosystems and improve risk-aware planning", "Build without assessing future flood exposure", "Remove all coastal vegetation", "Encourage settlement in the highest-risk areas without safeguards", "A"),
    ("A renewable energy project requires land in an area with important wildlife habitat. What is the best planning principle?", "Assess alternatives and minimize ecological harm while meeting energy needs", "Assume renewable projects cannot affect ecosystems", "Ignore biodiversity surveys", "Select the site only by its distance from the nearest shop", "A"),
    ("Why can rebound effects reduce the expected environmental benefits of efficiency improvements?", "Lower operating costs may encourage additional use", "Efficiency always makes total resource use fall by exactly the same percentage", "Lower energy use per unit guarantees zero total consumption", "Efficiency improvements automatically prevent all economic growth", "A"),
    ("A district experiences both seasonal water shortages and flash floods. Which approach can help address both problems?", "Combine watershed restoration, rainwater storage and suitable drainage planning", "Send all rainfall away without considering recharge", "Remove vegetation from all slopes", "Increase groundwater pumping without limits", "A"),
    ("Which approach best evaluates whether a development project supports intergenerational equity?", "Assess current benefits alongside long-term environmental and social costs", "Count only this year's revenue", "Ignore future resource availability", "Assume future generations have no legitimate needs", "A"),
    ("A farming region suffers from declining soil fertility and high chemical runoff. Which strategy is most balanced?", "Use soil testing, crop rotation, suitable nutrient management and erosion control", "Apply increasing fertilizer quantities without testing", "Remove all ground cover", "Stop monitoring water quality", "A"),
    ("Why can protecting a network of connected habitats be more effective than protecting isolated small patches?", "Connectivity can support movement, gene flow and species survival", "Connected habitats prevent every natural disturbance", "Isolated patches always support more species", "Connectivity eliminates the need for habitat quality", "A"),
    ("A company offsets emissions but continues to increase its fossil fuel use. What is the strongest sustainability recommendation?", "Prioritize credible direct emission reductions and use offsets carefully for residual emissions", "Assume every offset cancels any quantity of emissions", "Stop measuring emissions", "Increase fossil fuel use because offsets exist", "A"),
    ("A waste-management programme has high recycling rates but rising total material consumption. What additional strategy is needed?", "Reduce unnecessary consumption and product waste at the source", "Increase single-use product consumption", "Stop repairing durable goods", "Ignore total material throughput", "A"),
    ("Why is environmental justice relevant when siting a waste treatment facility?", "Decision-makers should assess who bears risks and whether communities are treated fairly", "Facility impacts are always distributed equally", "Residents should never be consulted", "Environmental risks do not affect human health", "A"),
    ("A city plants many trees but chooses species that need large amounts of scarce water. What should planners do?", "Select suitable native or climate-adapted species and plan long-term maintenance", "Continue planting without considering water demand", "Remove all water monitoring", "Assume every tree species has identical needs", "A"),
    ("A region's economy depends on a non-renewable mineral resource. Which policy can improve long-term resilience?", "Diversify livelihoods, manage revenues responsibly and plan for resource depletion", "Increase dependence on the mineral alone", "Ignore price volatility and environmental costs", "Spend all resource revenue immediately", "A"),
    ("How can integrated watershed management improve sustainability?", "Coordinate land, water and ecosystem management across the watershed", "Manage each water source without considering upstream effects", "Allow pollution to move downstream without controls", "Ignore local communities and land use", "A"),
    ("A conservation programme excludes residents who depend on a forest for fuel and income. What is a likely risk?", "The programme may face hardship, conflict and reduced local support", "Exclusion guarantees permanent conservation success", "Local livelihoods are never affected by conservation rules", "Participation always reduces ecological knowledge", "A"),
    ("Why should climate-resilient infrastructure account for uncertainty in future climate conditions?", "Designs must remain useful under a range of plausible future hazards", "Future climate conditions are perfectly predictable", "Infrastructure should be designed only for yesterday's weather", "Uncertainty means risk assessment is impossible", "A"),
    ("A country expands solar power but lacks adequate storage and grid planning. What challenge may arise?", "Variable generation may be difficult to balance with electricity demand", "Solar panels generate identical output at all times", "Grid infrastructure becomes unnecessary", "Electricity demand stops changing", "A"),
    ("A city wants to reduce food waste and landfill methane emissions. Which combined strategy is strongest?", "Prevent edible food waste, redistribute safe surplus and compost suitable organic waste", "Send all edible food directly to landfill", "Mix organic waste with all recyclables", "Burn all waste without pollution controls", "A"),
    ("Why is measuring only GDP insufficient for judging sustainable development?", "GDP alone does not fully capture inequality, environmental damage or well-being", "GDP measures every aspect of human welfare perfectly", "Economic activity has no environmental effects", "Social well-being is always identical to income", "A"),
    ("A proposed dam provides electricity and irrigation but may displace communities and alter river ecosystems. What is the most responsible decision process?", "Evaluate alternatives, environmental flows, displacement and distribution of benefits", "Consider electricity output only", "Ignore downstream ecosystems", "Proceed without consulting affected communities", "A"),
    ("Why can protecting peatlands and other carbon-rich ecosystems help climate mitigation?", "They store substantial carbon that may be released when degraded", "They contain no stored carbon", "Their destruction always reduces emissions", "They are unrelated to climate processes", "A"),
    ("A city installs efficient streetlights but leaves them operating at full brightness when roads are empty. What additional measure could improve sustainability?", "Use appropriate controls and dimming while maintaining safety", "Replace efficient lights with less efficient ones", "Increase brightness everywhere at all times", "Remove all maintenance schedules", "A"),
    ("Why should sustainability indicators be monitored over time rather than measured only once?", "Trends help reveal whether interventions are producing lasting results", "One measurement guarantees permanent success", "Monitoring prevents any future changes", "Indicators have no value for decision-making", "A"),
    ("A region protects forests but imports timber linked to deforestation elsewhere. Which concept is relevant?", "Consumption impacts can occur outside the region's own boundaries", "Imports never have environmental consequences", "Local forest protection automatically prevents global deforestation", "Trade has no connection to resource use", "A"),
    ("A sustainable development plan must balance economic opportunity, ecological limits and public well-being. Which decision approach best supports this?", "Use evidence, assess trade-offs and include affected communities", "Maximize short-term profit regardless of harm", "Ignore scientific evidence and community needs", "Assume one indicator captures every outcome", "A"),
]


# --------------------------------------------------
# VALIDATION BEFORE DATABASE CHANGES
# --------------------------------------------------

BANKS = {
    "Easy": EASY,
    "Medium": MEDIUM,
    "Hard": HARD,
}

for difficulty, bank in BANKS.items():
    if len(bank) != 30:
        raise ValueError(
            f"{difficulty} must have 30 questions; found {len(bank)}."
        )

    for number, item in enumerate(bank, start=1):
        if len(item) != 6:
            raise ValueError(
                f"{difficulty} question {number} has {len(item)} values; expected 6."
            )

        if item[5] not in {"A", "B", "C", "D"}:
            raise ValueError(
                f"{difficulty} question {number} has an invalid answer key."
            )

print("Validation passed: 30 questions per difficulty.")


# --------------------------------------------------
# SHUFFLE OPTIONS WHILE PRESERVING THE CORRECT ANSWER
# --------------------------------------------------

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

    new_correct = "ABCD"[shuffled.index(correct_text)]

    return (
        question,
        shuffled[0],
        shuffled[1],
        shuffled[2],
        shuffled[3],
        new_correct,
    )


# --------------------------------------------------
# DATABASE INSERTION
# --------------------------------------------------

db = SessionLocal()

try:
    lesson = (
        db.query(Lesson)
        .filter(
            Lesson.title == "Sustainable Development",
            Lesson.topic == "Social Science",
        )
        .first()
    )

    if lesson is None:
        raise RuntimeError(
            "Lesson 'Sustainable Development' was not found under Social Science."
        )

    for difficulty, bank in BANKS.items():
        quiz = (
            db.query(Quiz)
            .filter(
                Quiz.lesson_id == lesson.id,
                Quiz.difficulty == difficulty,
            )
            .first()
        )

        if quiz is None:
            quiz = Quiz(
                lesson_id=lesson.id,
                title=f"Sustainable Development - {difficulty}",
                difficulty=difficulty,
            )
            db.add(quiz)
            db.flush()

        existing_questions = {
            question.question.strip().casefold()
            for question in (
                db.query(Question)
                .filter(Question.quiz_id == quiz.id)
                .all()
            )
        }

        added = 0

        for original_item in bank:
            item = shuffle_options(original_item)
            question_text = item[0].strip()

            if question_text.casefold() in existing_questions:
                continue

            question, a, b, c, d, correct = item

            db.add(
                Question(
                    quiz_id=quiz.id,
                    question=question,
                    option_a=a,
                    option_b=b,
                    option_c=c,
                    option_d=d,
                    correct_answer=correct,
                )
            )

            existing_questions.add(question_text.casefold())
            added += 1

        db.flush()
        print(f"{difficulty}: added {added} new questions.")

    db.commit()

    print("\n========== FINAL VERIFICATION ==========")

    total = 0

    for difficulty in ("Easy", "Medium", "Hard"):
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

    if total == 90:
        print(
            "SUCCESS: Sustainable Development has 90 questions."
        )
    else:
        print(
            "WARNING: The lesson does not yet contain exactly 90 questions. "
            "Check the counts above."
        )

except Exception:
    db.rollback()
    raise

finally:
    db.close()