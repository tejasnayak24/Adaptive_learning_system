
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

LESSON_TITLE = "Natural Resources"
TARGET_QUESTIONS = 30

QUESTION_BANK = {
    "Easy": [
        ("What are natural resources?", ["Materials and substances obtained from nature that people and organisms use", "Only manufactured products", "Only electronic devices", "Objects made exclusively from plastic"], "A"),
        ("Which of these is a renewable resource?", ["Coal", "Sunlight", "Petroleum", "Natural gas"], "B"),
        ("Which resource is essential for drinking and many biological processes?", ["Granite", "Iron ore", "Water", "Plastic"], "C"),
        ("Which of these is a fossil fuel?", ["Wind", "Sunlight", "Flowing water", "Coal"], "D"),
        ("Which natural resource do plants use for photosynthesis?", ["Sunlight", "Petroleum", "Copper", "Coal"], "A"),
        ("Which of these is a mineral resource?", ["Wood", "Iron ore", "Wind", "Rainwater"], "B"),
        ("What is soil important for?", ["Producing petroleum instantly", "Stopping all plant growth", "Supporting plant growth and providing habitats", "Replacing sunlight"], "C"),
        ("Which resource is commonly used to generate wind energy?", ["Coal deposits", "Underground petroleum", "Metal ores", "Moving air"], "D"),
        ("Which of these is a non-renewable resource?", ["Coal", "Sunlight", "Wind", "Tidal energy"], "A"),
        ("Why are forests important natural resources?", ["They prevent all natural disasters", "They provide habitats, store carbon and supply useful materials", "They produce fossil fuels immediately", "They eliminate the water cycle"], "B"),
        ("Which gas do humans need for aerobic respiration?", ["Nitrogen", "Carbon dioxide", "Oxygen", "Helium"], "C"),
        ("Which natural resource is used to produce hydroelectricity?", ["Coal dust", "Dry sand", "Plastic waste only", "Flowing or falling water"], "D"),
        ("What is groundwater?", ["Water stored beneath Earth's surface", "Water found only in clouds", "Water produced by burning coal", "Water inside the Sun"], "A"),
        ("Which of these is a biological natural resource?", ["Copper wire", "Timber from trees", "Concrete", "Synthetic rubber"], "B"),
        ("What is conservation of natural resources?", ["Using every resource as quickly as possible", "Preventing people from using any resource", "Protecting resources and using them responsibly", "Converting all resources into waste"], "C"),
        ("Which energy source is replenished by natural processes and is generally considered renewable?", ["Coal", "Petroleum", "Natural gas", "Wind"], "D"),
        ("Which activity can help conserve water at home?", ["Repairing leaking taps", "Leaving taps running unnecessarily", "Washing pavements with a hose every day", "Ignoring leaking pipes"], "A"),
        ("What is deforestation?", ["Planting trees in a forest", "Clearing or removing forests", "Protecting wildlife habitats", "Restoring damaged soil"], "B"),
        ("Which of these is a major source of fresh water for many communities?", ["Ocean water without treatment", "Petroleum", "Rivers and groundwater", "Metal ores"], "C"),
        ("Why is air considered a natural resource?", ["It is manufactured in factories", "It is found only underground", "It has no role in life", "Living organisms use gases in the atmosphere"], "D"),
        ("Which of these is an example of a resource obtained from animals?", ["Wool", "Granite", "Copper ore", "Sunlight"], "A"),
        ("What is recycling?", ["Throwing all waste into rivers", "Processing used materials so they can be used again", "Burning every material in open air", "Extracting sunlight from soil"], "B"),
        ("Which practice helps protect soil from erosion?", ["Removing all vegetation", "Overgrazing every field", "Planting vegetation and maintaining ground cover", "Leaving slopes bare"], "C"),
        ("Which resource is used to make glass?", ["Coal alone", "Wool", "Petroleum alone in every glassmaking process", "Silica sand"], "D"),
        ("What is a habitat?", ["The natural environment in which an organism lives", "A type of mineral", "A fossil fuel", "A manufactured tool"], "A"),
        ("Which of these is a renewable biological resource when managed sustainably?", ["A finite mineral deposit", "Timber from a sustainably managed forest", "A fixed petroleum reserve", "A coal seam"], "B"),
        ("What does sustainable use of resources mean?", ["Using resources without considering future needs", "Preventing every form of resource use", "Meeting current needs while maintaining resources and environmental health for the future", "Using only non-renewable resources"], "C"),
        ("Which natural resource is the main source of energy for the water cycle?", ["Coal", "Petroleum", "Natural gas", "The Sun"], "D"),
        ("Why should wildlife habitats be protected?", ["They support biodiversity and ecosystem functions", "They have no ecological value", "They prevent all rainfall", "They contain only non-living materials"], "A"),
        ("Which of these actions reduces unnecessary use of paper?", ["Printing every email several times", "Using digital documents when suitable and recycling paper", "Throwing unused paper into rivers", "Cutting more trees without replanting"], "B"),
    ],

    "Medium": [
        ("Why are fossil fuels considered non-renewable on human timescales?", ["They are created in a few minutes", "They are replenished every day by sunlight", "They take millions of years to form and are consumed much faster than they form", "They cannot be used for energy"], "C"),
        ("How can excessive groundwater extraction affect a region?", ["It always increases rainfall", "It creates unlimited underground water", "It prevents all soil erosion", "It can lower the water table and reduce well supplies"], "D"),
        ("Why is biodiversity important when managing natural resources?", ["It supports ecosystem stability, resilience and useful ecological processes", "It guarantees that no species will ever become extinct", "It removes the need for water", "It means every organism uses the same resource"], "A"),
        ("What is one environmental advantage of solar energy over coal-fired electricity?", ["Solar panels produce no waste at any stage of their life cycle", "Generating electricity from sunlight generally produces much lower direct greenhouse-gas emissions", "Solar energy requires no land or materials", "Solar power is available at full output at every hour"], "B"),
        ("How can deforestation affect the water cycle?", ["It eliminates evaporation from oceans", "It creates new groundwater instantly", "It can reduce transpiration and alter runoff and local moisture patterns", "It prevents water from flowing downhill"], "C"),
        ("Why can soil be considered a slowly renewable resource rather than an unlimited resource?", ["Soil forms instantly whenever it rains", "Soil cannot support life", "Soil is made entirely by factories", "Soil formation can be slow, while erosion may remove it rapidly"], "D"),
        ("What is the main purpose of rainwater harvesting?", ["Collecting and storing rainwater for later use or groundwater recharge", "Increasing the use of fossil fuels", "Preventing all clouds from forming", "Turning seawater directly into petroleum"], "A"),
        ("Why is recycling aluminium often beneficial?", ["It requires more energy than producing it from ore in every case", "It can save substantial energy compared with producing aluminium from raw ore", "Aluminium cannot be reused", "It creates unlimited mineral deposits"], "B"),
        ("What is overfishing?", ["Fishing only in freshwater", "Protecting fish breeding grounds", "Removing fish faster than populations can replenish", "Reducing fishing pressure on vulnerable species"], "C"),
        ("How does vegetation help reduce soil erosion?", ["It makes soil particles float permanently", "It removes all nutrients from soil", "It increases the speed of every stream", "Roots help bind soil and plant cover reduces the impact of rain and wind"], "D"),
        ("Which practice is most likely to improve long-term forest resource management?", ["Selective harvesting combined with regeneration and habitat protection", "Clearing all trees at once without restoration", "Burning forests every season without assessment", "Removing all native species"], "A"),
        ("Why is freshwater conservation important even though water cycles through the environment?", ["All Earth's water is directly drinkable", "Only a small fraction of Earth's water is readily available freshwater for human use", "The water cycle permanently destroys all water", "Oceans contain no water"], "B"),
        ("How can excessive fertiliser use affect nearby lakes?", ["It always increases oxygen indefinitely", "It removes every aquatic plant", "Nutrient runoff can promote algal blooms and oxygen depletion", "It prevents microorganisms from growing"], "C"),
        ("What is the role of wetlands as natural resources?", ["They have no role in flood control", "They always cause pollution", "They contain no biodiversity", "They can store floodwater, filter some pollutants and provide wildlife habitats"], "D"),
        ("Why can replacing fossil fuels with renewable energy help mitigate climate change?", ["Many renewable sources produce less greenhouse gas during operation", "Renewable energy always releases more carbon dioxide than coal", "Climate change is unrelated to energy use", "Renewable energy stops all natural climate variation"], "A"),
        ("Which is an example of resource efficiency?", ["Leaving machinery running when unused", "Producing the same service with less material or energy", "Discarding reusable products immediately", "Increasing losses during manufacturing"], "B"),
        ("Why can mining cause environmental problems?", ["Minerals regenerate completely within hours", "Mining never changes land", "It can disturb habitats, generate waste and contaminate water if poorly managed", "It eliminates every form of erosion"], "C"),
        ("What is an aquifer?", ["A layer of clouds", "A type of fossil fuel", "A surface wind", "An underground geological formation that stores and transmits groundwater"], "D"),
        ("Why is crop rotation useful in sustainable agriculture?", ["It can improve soil management and help interrupt some pest and disease cycles", "It guarantees that fertiliser is never needed", "It prevents all rainfall", "It turns soil into rock"], "A"),
        ("Which action can help reduce household energy consumption?", ["Heating empty rooms with windows open", "Using efficient appliances and switching off equipment when appropriate", "Leaving all lights on overnight", "Using inefficient devices for every task"], "B"),
        ("What does the term carbon sink mean?", ["A machine that produces coal", "A place where no carbon exists", "A system that absorbs and stores more carbon than it releases over a given period", "A source that always emits more carbon than it absorbs"], "C"),
        ("Why is sustainable fisheries management important?", ["Fish populations cannot decline", "Oceans contain an unlimited number of fish", "Fishing pressure never affects reproduction", "Harvest limits and habitat protection can help populations remain productive over time"], "D"),
        ("How can urban green spaces support natural resource conservation?", ["They can provide habitat, absorb some stormwater and reduce local heat", "They eliminate the need for drinking water", "They increase every form of air pollution", "They prevent plants from growing"], "A"),
        ("Why is natural gas still considered a non-renewable resource despite often producing less carbon dioxide than coal when burned?", ["It is made from sunlight in a few hours", "It is a finite fossil fuel formed over geological timescales", "It contains no chemical energy", "It is replenished as quickly as wind"], "B"),
        ("Which practice can reduce pressure on forests?", ["Using more disposable paper without recycling", "Burning wood unnecessarily", "Reducing waste and using certified sustainably sourced wood products", "Clearing natural forests for every new building"], "C"),
        ("What is desertification?", ["The creation of new oceans", "The formation of glaciers in every climate", "A process that makes all land more fertile", "Land degradation in dry areas that reduces biological productivity"], "D"),
        ("Why should mineral resources be used efficiently?", ["Many mineral deposits are finite and extraction can cause environmental impacts", "All minerals regenerate every day", "Mining has no effect on ecosystems", "Minerals cannot be recycled"], "A"),
        ("How can public transport help conserve natural resources?", ["It always uses more fuel per passenger than private cars", "It can reduce fuel use and emissions per passenger when well utilised", "It eliminates the need for roads everywhere", "It produces fossil fuels"], "B"),
        ("Why are native plants often useful in ecological restoration?", ["They always require more water than every non-native species", "They cannot support local wildlife", "They may be well suited to local conditions and support native ecological relationships", "They prevent all other plants from growing"], "C"),
        ("What is a life-cycle assessment used for?", ["Measuring only the colour of a product", "Counting stars in a galaxy", "Predicting the exact weather for a century", "Evaluating environmental impacts associated with a product or process across its life cycle"], "D"),
    ],

    "Hard": [
        ("A town's groundwater level falls for several years despite normal rainfall. Which explanation is most plausible?", ["Groundwater extraction has exceeded recharge over that period", "Groundwater is created only by factories", "Rainfall never contributes to groundwater", "Aquifers cannot store water"], "A"),
        ("Why is the concept of renewable resources dependent on management practices?", ["Every renewable resource replenishes instantly regardless of use", "A renewable resource can be depleted if its rate of use exceeds its rate of regeneration", "Renewable resources cannot be damaged", "Resource management affects only fossil fuels"], "B"),
        ("A forest is cleared on a steep slope. Heavy rain then carries soil into a river. Which chain best explains the impact?", ["Tree removal increases root binding and prevents runoff", "Rainfall stops when trees are removed", "Reduced vegetation cover increases erosion and sediment delivery to the river", "Soil particles are converted into oxygen"], "C"),
        ("A region replaces a coal plant with a solar farm. Which assessment is most scientifically appropriate?", ["Solar power has zero environmental impact throughout its life cycle", "Solar panels work at full output regardless of weather and time", "Coal and solar have identical operational emissions in all cases", "Solar can reduce operational emissions, while land use, materials, storage and end-of-life management still matter"], "D"),
        ("A fishery harvests 12,000 tonnes annually while the population replaces only about 8,000 tonnes per year. If these rates persist, what is the likely result?", ["The population will decline because harvest exceeds replenishment", "The population will grow without limit", "The fishery is automatically sustainable", "The ocean will create exactly 4,000 extra tonnes"], "A"),
        ("Why can a resource with a large total global supply still be scarce for a particular community?", ["Global supply always guarantees local access", "Geography, infrastructure, quality, cost and governance can limit local availability", "All resources are distributed evenly", "Scarcity depends only on colour"], "B"),
        ("Which policy package is most likely to conserve a groundwater aquifer over the long term?", ["Increase pumping without monitoring", "Pave all recharge areas and remove vegetation", "Monitor withdrawals, protect recharge zones and align extraction with sustainable recharge", "Ban all measurements of groundwater"], "C"),
        ("Why can bioenergy from forests fail to be carbon-neutral over a short period?", ["Combustion never releases carbon dioxide", "Trees absorb carbon only after being cut", "Forest growth has no relationship to carbon storage", "Combustion releases carbon immediately, while regrowth and ecosystem recovery may take years or decades"], "D"),
        ("A city recycles more plastic but also increases total plastic consumption substantially. Why might total plastic waste still rise?", ["Waste generation depends on total material use as well as recycling rates", "Recycling always eliminates all waste", "Plastic use has no relationship to waste", "Every plastic product is recycled indefinitely without losses"], "A"),
        ("What is a potential trade-off in constructing a large hydroelectric dam?", ["It creates electricity without altering any environment", "It can provide low-operational-carbon electricity while flooding habitats and changing river ecosystems", "It makes river flow completely natural", "It eliminates the need for all other resource planning"], "B"),
        ("Why is resource depletion not determined solely by how much of a resource exists underground?", ["The extraction rate has no relevance", "Resources are always available at zero cost", "Accessibility, extraction technology, environmental constraints and demand also influence usable supply", "All deposits can be extracted without energy"], "C"),
        ("Which indicator would best help assess whether a forest harvest is sustainable?", ["The number of trucks used in one day only", "The market price of wood alone", "The number of buildings in a nearby city", "Whether harvesting remains compatible with regeneration, biodiversity and long-term forest function"], "D"),
        ("Why can protecting a watershed improve both water quality and quantity?", ["Vegetation and soils can influence infiltration, erosion, sediment transport and pollutant movement", "A watershed is unrelated to water", "Trees convert every pollutant into drinking water instantly", "Watershed protection stops all evaporation"], "A"),
        ("A country imports minerals instead of mining all of them domestically. Which conclusion is most accurate?", ["Importing minerals removes all environmental impacts", "Environmental impacts may shift to extraction and processing regions, so supply-chain assessment matters", "Imported minerals are always renewable", "Imports eliminate the need for resource efficiency"], "B"),
        ("Why can circular-economy strategies conserve natural resources more effectively than disposal-focused systems?", ["They require every product to be discarded immediately", "They prevent products from being repaired", "They emphasise reducing, reusing, repairing and recycling materials to keep them in use", "They increase demand for raw materials in every situation"], "C"),
        ("A river receives nutrient-rich runoff from farms. Dissolved oxygen declines after an algal bloom. What mechanism most directly contributes to the oxygen decline?", ["Algae transform oxygen into sunlight", "Nutrients eliminate all bacteria", "Water stops dissolving gases permanently", "Decomposers consume oxygen while breaking down excess organic matter"], "D"),
        ("Why should the environmental costs of a resource be evaluated across its entire life cycle?", ["Extraction, processing, use and disposal can each contribute significant impacts", "Only the purchase price matters", "Manufacturing has no environmental effect", "Disposal never produces waste"], "A"),
        ("A renewable forest resource grows at 3% per year while harvesting removes 5% of its stock annually, with other factors unchanged. What is the broad concern?", ["The forest must expand rapidly", "Harvesting exceeds the stated growth rate and may reduce the stock over time", "The resource is non-renewable by definition", "The forest will have no ecological function"], "B"),
        ("Why can energy efficiency reduce pressure on both renewable and non-renewable resources?", ["Efficiency always increases consumption by definition", "It has no effect on resource demand", "Less energy input may be required to provide the same service", "It eliminates the need for energy planning"], "C"),
        ("Which approach best balances mineral extraction with environmental protection?", ["Extract without waste management", "Ignore local communities and ecosystems", "Assume restoration is unnecessary", "Assess impacts, reduce waste, protect water and habitats, and plan site rehabilitation"], "D"),
        ("Why can desalination help address water scarcity but not solve every water-management problem?", ["It requires energy and infrastructure and produces concentrated brine that must be managed", "It turns seawater into freshwater without any process", "It eliminates all water demand", "It makes groundwater recharge unnecessary"], "A"),
        ("A city expands roads and buildings over a groundwater recharge zone. What is a likely consequence?", ["Groundwater recharge always increases", "Impervious surfaces can reduce infiltration and increase runoff", "Rainfall becomes unnecessary", "Aquifers stop existing underground"], "B"),
        ("Why might a life-cycle assessment favour repairing an existing device over replacing it?", ["Repair always has zero impact", "New devices never require materials", "Repair may avoid some impacts from manufacturing and disposing of a replacement", "Repair increases raw-material use in every case"], "C"),
        ("Which measure best distinguishes water withdrawal from water consumption?", ["Both terms always mean exactly the same thing", "Withdrawal refers only to rain, while consumption refers only to oceans", "Consumption means all water remains available in the same place", "Withdrawal is water taken from a source; consumption is the portion not returned to the same basin in a usable form"], "D"),
        ("Why can protecting mangroves be considered a natural-resource management strategy?", ["Mangroves can support fisheries, store carbon and help protect coasts from some wave and erosion impacts", "Mangroves have no relationship to biodiversity", "Mangroves increase coastal erosion in every situation", "Mangroves prevent all storms"], "A"),
        ("A region's demand for timber rises faster than its managed forests regenerate. Which response addresses the underlying sustainability issue?", ["Increase harvesting indefinitely", "Reduce waste, improve forest management and use alternative or recycled materials where suitable", "Stop monitoring forest stock", "Remove all forest regeneration programmes"], "B"),
        ("Why is it risky to evaluate renewable energy only by the emissions produced while generating electricity?", ["Operational emissions are always the only relevant impact", "Manufacturing equipment uses no resources", "Materials, construction, land use and disposal can also have environmental impacts", "Renewable energy systems never need maintenance"], "C"),
        ("What is the strongest reason to protect biodiversity while extracting natural resources?", ["Biodiversity has no effect on ecosystem services", "Only rare species influence ecosystems", "Resource extraction always improves every habitat", "Biodiversity supports ecological processes, resilience and benefits that people may depend on"], "D"),
        ("A region reduces per-unit water use in agriculture, but total irrigated land expands substantially. What should managers examine to determine whether total water use fell?", ["Total water withdrawals and consumption, not just water use per hectare", "Only the colour of irrigation pipes", "The number of farms without measuring water", "Only the price of crops"], "A"),
        ("Why is an adaptive resource-management approach useful under climate uncertainty?", ["It assumes environmental conditions never change", "It monitors outcomes and adjusts decisions as new evidence and conditions emerge", "It eliminates the need for data", "It guarantees that every prediction will be exact"], "B"),
    ],
}


def normalize(text):
    return " ".join(text.casefold().split())


def main():
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DATABASE_PATH}")

    connection = sqlite3.connect(str(DATABASE_PATH))

    try:
        with connection:
            connection.execute("PRAGMA foreign_keys = ON")
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT id
                FROM lessons
                WHERE LOWER(TRIM(title)) = LOWER(TRIM(?))
                """,
                (LESSON_TITLE,),
            )
            lesson = cursor.fetchone()

            if lesson is None:
                raise RuntimeError(f"Lesson '{LESSON_TITLE}' was not found.")

            lesson_id = lesson[0]
            inserted_total = 0

            for difficulty, questions in QUESTION_BANK.items():
                cursor.execute(
                    """
                    SELECT id
                    FROM quizzes
                    WHERE lesson_id = ?
                      AND LOWER(TRIM(difficulty)) = LOWER(TRIM(?))
                    ORDER BY id
                    """,
                    (lesson_id, difficulty),
                )
                quiz_rows = cursor.fetchall()

                if not quiz_rows:
                    raise RuntimeError(
                        f"No {difficulty} quiz found for {LESSON_TITLE}."
                    )

                if len(quiz_rows) > 1:
                    raise RuntimeError(
                        f"Multiple {difficulty} quizzes found for "
                        f"{LESSON_TITLE}; no questions were changed."
                    )

                quiz_id = quiz_rows[0][0]

                cursor.execute(
                    "SELECT question FROM questions WHERE quiz_id = ?",
                    (quiz_id,),
                )
                existing = {normalize(row[0]) for row in cursor.fetchall()}

                available = [
                    (question, options, answer)
                    for question, options, answer in questions
                    if normalize(question) not in existing
                ]

                cursor.execute(
                    "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                    (quiz_id,),
                )
                current_count = cursor.fetchone()[0]
                needed = TARGET_QUESTIONS - current_count

                if needed < 0:
                    raise RuntimeError(
                        f"{difficulty} already has {current_count} questions."
                    )

                if len(available) < needed:
                    raise RuntimeError(
                        f"{difficulty}: need {needed} new questions, but only "
                        f"{len(available)} unique questions are available. "
                        "No changes were committed."
                    )

                for question, options, answer in available[:needed]:
                    cursor.execute(
                        """
                        INSERT INTO questions (
                            quiz_id, question,
                            option_a, option_b, option_c, option_d,
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
                            answer,
                        ),
                    )
                    inserted_total += 1

                cursor.execute(
                    "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                    (quiz_id,),
                )
                final_count = cursor.fetchone()[0]

                if final_count != TARGET_QUESTIONS:
                    raise RuntimeError(
                        f"{difficulty}: expected {TARGET_QUESTIONS}, "
                        f"found {final_count}. No changes were committed."
                    )

                print(
                    f"{difficulty}: added {needed}; final count = {final_count}"
                )

        print("\nNatural Resources expansion completed!")
        print(f"Total new questions inserted: {inserted_total}")
        print("Easy: 30 questions")
        print("Medium: 30 questions")
        print("Hard: 30 questions")
        print("Other lessons and Social Science were not modified.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()
