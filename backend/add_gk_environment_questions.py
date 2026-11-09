
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 175
LESSON_TITLE = "Environment, Ecology, Wildlife and Climate Change"
TOPIC = "General Knowledge"

BANK = {
    "Easy": [
        ("Which gas is primarily responsible for global warming due to human activities?", "Carbon dioxide", "Oxygen", "Helium", "Neon"),
        ("Which layer protects Earth from harmful ultraviolet radiation?", "Ozone layer", "Troposphere", "Mesosphere", "Ionosphere"),
        ("Which of the following is a renewable source of energy?", "Solar energy", "Coal", "Petroleum", "Natural gas"),
        ("Which of these is a non-renewable resource?", "Coal", "Wind", "Sunlight", "Tidal energy"),
        ("What is the main source of energy for Earth?", "Sun", "Moon", "Wind", "Ocean"),
        ("Which process allows green plants to prepare food?", "Photosynthesis", "Respiration", "Transpiration", "Fermentation"),
        ("What is the natural habitat of a tiger?", "Forest", "Desert only", "Polar region", "Open ocean"),
        ("Which animal is commonly called the ship of the desert?", "Camel", "Horse", "Elephant", "Yak"),
        ("Which is the largest land animal?", "African elephant", "Tiger", "Giraffe", "Rhinoceros"),
        ("Which is the largest animal on Earth?", "Blue whale", "African elephant", "Great white shark", "Giraffe"),
        ("Which Indian animal is protected as the national animal of India?", "Bengal tiger", "Asiatic lion", "Indian elephant", "Leopard"),
        ("Which bird is the national bird of India?", "Indian peacock", "Sparrow", "Parrot", "Eagle"),
        ("Which Indian state is famous for the Gir National Park, home of Asiatic lions?", "Gujarat", "Rajasthan", "Madhya Pradesh", "Maharashtra"),
        ("Which national park is famous for one-horned rhinoceroses?", "Kaziranga National Park", "Gir National Park", "Ranthambore National Park", "Bandipur National Park"),
        ("What is the main purpose of a national park?", "Protect wildlife and natural ecosystems", "Promote industrial development", "Increase mining activities", "Expand urban settlements"),
        ("What does recycling mean?", "Processing used materials into new products", "Burning all waste", "Dumping waste into rivers", "Using resources only once"),
        ("Which of these is biodegradable?", "Vegetable peels", "Plastic bottle", "Glass jar", "Aluminium can"),
        ("Which of these is a major source of air pollution?", "Vehicle exhaust", "Rainwater", "Solar panels", "Planting trees"),
        ("Which of these contributes to water pollution?", "Industrial waste", "Rainwater harvesting", "Tree planting", "Wind energy"),
        ("What is deforestation?", "Large-scale removal of forests", "Planting new trees", "Protecting wildlife", "Conserving soil"),
        ("Which practice helps conserve water?", "Rainwater harvesting", "Leaving taps running", "Dumping waste into lakes", "Excessive irrigation"),
        ("What is the main function of forests in the environment?", "Maintain ecological balance", "Increase air pollution", "Reduce biodiversity", "Increase soil erosion"),
        ("Which of these is an example of an endangered animal in India?", "Great Indian bustard", "Domestic cat", "House crow", "Common pigeon"),
        ("Which international day is celebrated on 5 June?", "World Environment Day", "World Water Day", "Earth Day", "World Wildlife Day"),
        ("When is Earth Day celebrated?", "22 April", "5 June", "16 September", "21 June"),
        ("When is World Wildlife Day observed?", "3 March", "5 June", "22 April", "11 July"),
        ("Which gas is released by plants during photosynthesis?", "Oxygen", "Carbon dioxide", "Nitrogen", "Methane"),
        ("Which natural disaster involves the overflow of water onto normally dry land?", "Flood", "Drought", "Earthquake", "Volcanic eruption"),
        ("What is biodiversity?", "Variety of living organisms", "Only the number of trees", "Only the number of animals", "Amount of rainfall"),
        ("Which of these helps reduce soil erosion?", "Planting trees", "Removing vegetation", "Overgrazing", "Deforestation"),
    ],

    "Medium": [
        ("What is the greenhouse effect?", "Warming caused by gases trapping heat in the atmosphere", "Cooling caused by ocean currents", "Loss of oxygen from the atmosphere", "Formation of clouds only"),
        ("Which gas is a major contributor to human-caused greenhouse gas emissions?", "Carbon dioxide", "Oxygen", "Helium", "Hydrogen"),
        ("Which greenhouse gas is commonly released from livestock and landfills?", "Methane", "Oxygen", "Nitrogen", "Argon"),
        ("What is the main cause of ozone layer depletion?", "Ozone-depleting substances such as CFCs", "Excess oxygen", "Rainwater harvesting", "Solar energy"),
        ("Which international agreement aims to protect the ozone layer?", "Montreal Protocol", "Kyoto Protocol", "Paris Agreement", "Ramsar Convention"),
        ("Which agreement focuses on limiting global temperature rise and addressing climate change?", "Paris Agreement", "Montreal Protocol", "Ramsar Convention", "CITES"),
        ("Which international agreement established emission reduction commitments for developed countries?", "Kyoto Protocol", "Ramsar Convention", "Montreal Protocol", "Convention on Biological Diversity"),
        ("What is the main objective of the Ramsar Convention?", "Conservation and wise use of wetlands", "Protection of the ozone layer", "Control of nuclear weapons", "Promotion of international trade"),
        ("What does CITES regulate?", "International trade in endangered species", "Global carbon emissions", "International shipping", "Use of fossil fuels"),
        ("Which organisation publishes major global climate assessment reports?", "Intergovernmental Panel on Climate Change", "World Trade Organization", "International Monetary Fund", "International Olympic Committee"),
        ("What is an ecosystem?", "A community of organisms interacting with their environment", "A group of only plants", "A collection of only animals", "A non-living geological formation"),
        ("Which organisms are called primary producers in most ecosystems?", "Green plants", "Carnivores", "Herbivores", "Decomposers"),
        ("Which organisms break down dead plants and animals?", "Decomposers", "Producers", "Primary consumers", "Predators"),
        ("What is the first trophic level in a typical food chain?", "Producers", "Primary consumers", "Secondary consumers", "Tertiary consumers"),
        ("What is the role of decomposers in an ecosystem?", "Recycle nutrients", "Produce sunlight", "Stop photosynthesis", "Increase plastic pollution"),
        ("What is biomagnification?", "Increase in concentration of certain pollutants at higher trophic levels", "Decrease in biodiversity due to rainfall", "Growth of plants in water", "Increase in soil fertility"),
        ("Which chemical was historically associated with biomagnification and harm to birds?", "DDT", "Glucose", "Calcium carbonate", "Sodium chloride"),
        ("What is eutrophication?", "Excessive nutrient enrichment of water bodies", "Loss of all nutrients from soil", "Formation of glaciers", "Increase in forest cover"),
        ("Which practice is most effective in preventing soil erosion on slopes?", "Terrace farming", "Overgrazing", "Deforestation", "Excessive ploughing"),
        ("What is desertification?", "Land degradation in dry regions", "Formation of new forests", "Expansion of wetlands", "Increase in freshwater availability"),
        ("Which Indian movement is associated with villagers protecting trees by hugging them?", "Chipko Movement", "Swadeshi Movement", "Bhoodan Movement", "Quit India Movement"),
        ("Who is popularly associated with the Chipko Movement in India?", "Sunderlal Bahuguna", "Verghese Kurien", "M. S. Swaminathan", "Homi Bhabha"),
        ("Which Indian programme focuses on conserving tigers in the wild?", "Project Tiger", "Project Elephant", "Project Snow Leopard", "Project Crocodile"),
        ("In which year was Project Tiger launched in India?", "1973", "1980", "1986", "1992"),
        ("Which programme was launched in India to protect elephants and their habitats?", "Project Elephant", "Project Tiger", "Project Rhino", "Project Lion"),
        ("Which Indian biosphere reserve is located in the Western Ghats?", "Nilgiri Biosphere Reserve", "Nanda Devi Biosphere Reserve", "Sundarbans Biosphere Reserve", "Pachmarhi Biosphere Reserve"),
        ("Which Indian wetland is famous for migratory birds and is a UNESCO World Heritage Site?", "Keoladeo National Park", "Gir National Park", "Periyar National Park", "Bandipur National Park"),
        ("Which forest type is commonly found in regions receiving heavy rainfall?", "Tropical evergreen forest", "Tropical thorn forest", "Desert scrub", "Alpine grassland"),
        ("Which biome is characterised by permanently frozen subsoil?", "Tundra", "Savanna", "Tropical rainforest", "Temperate grassland"),
        ("What is the term for the variety of species in a particular ecosystem?", "Species diversity", "Atmospheric pressure", "Soil salinity", "Water table"),
    ],

    "Hard": [
        ("Which international agreement aims to conserve biological diversity and promote sustainable use of its components?", "Convention on Biological Diversity", "Montreal Protocol", "Kyoto Protocol", "Ramsar Convention"),
        ("Which protocol was adopted under the Convention on Biological Diversity to address biosafety?", "Cartagena Protocol", "Kyoto Protocol", "Montreal Protocol", "Nagoya Protocol"),
        ("Which protocol deals with access to genetic resources and fair sharing of benefits?", "Nagoya Protocol", "Cartagena Protocol", "Kyoto Protocol", "Montreal Protocol"),
        ("Which global framework replaced the Aichi Biodiversity Targets in 2022?", "Kunming-Montreal Global Biodiversity Framework", "Paris Climate Framework", "Kyoto Biodiversity Framework", "Ramsar Global Framework"),
        ("What does the term 'carbon sink' refer to?", "A system that absorbs more carbon than it releases", "A source that releases only oxygen", "A device that produces fossil fuels", "A system that increases atmospheric carbon"),
        ("Which ecosystem is especially important for storing large amounts of carbon in waterlogged soils?", "Peatlands", "Deserts", "Coral reefs", "Alpine meadows"),
        ("What is ocean acidification primarily caused by?", "Absorption of atmospheric carbon dioxide", "Excess oxygen in seawater", "Increased salt formation", "Reduction in ocean currents"),
        ("Which phenomenon describes the bleaching of corals when they lose their symbiotic algae?", "Coral bleaching", "Eutrophication", "Biomagnification", "Desertification"),
        ("Which organisms form the major symbiotic partnership with reef-building corals?", "Zooxanthellae algae", "Nitrogen-fixing bacteria", "Fungi", "Lichens"),
        ("What is an invasive alien species?", "A non-native species that spreads and causes harm", "A native species protected by law", "A species that lives only in deserts", "An organism that cannot reproduce"),
        ("Which ecological term describes the gradual change in community composition over time?", "Ecological succession", "Biomagnification", "Transpiration", "Eutrophication"),
        ("What is the climax community in classical ecological succession?", "A relatively stable mature community", "The first pioneer species", "A temporary group of insects", "A community with no producers"),
        ("Which process describes the movement of nitrogen from the atmosphere into biologically usable compounds?", "Nitrogen fixation", "Denitrification", "Transpiration", "Evaporation"),
        ("Which bacteria are commonly associated with nitrogen fixation in legume root nodules?", "Rhizobium", "Lactobacillus", "Escherichia coli", "Streptococcus"),
        ("Which process converts nitrates into atmospheric nitrogen?", "Denitrification", "Nitrification", "Ammonification", "Photosynthesis"),
        ("What is the 10 percent law in ecology associated with?", "Energy transfer between trophic levels", "Transfer of water between ecosystems", "Population growth in forests", "Rate of soil formation"),
        ("Which ecological pyramid is always upright in terms of energy?", "Pyramid of energy", "Pyramid of numbers", "Pyramid of biomass", "All ecological pyramids"),
        ("What is the term for the maximum population size an environment can sustainably support?", "Carrying capacity", "Biotic potential", "Ecological succession", "Population density"),
        ("Which index is commonly used to measure species diversity in ecological studies?", "Shannon diversity index", "Reynolds number", "Gini coefficient", "Consumer price index"),
        ("Which Indian law provides a broad legal framework for environmental protection?", "Environment (Protection) Act, 1986", "Indian Contract Act, 1872", "Companies Act, 2013", "Right to Information Act, 2005"),
        ("Which Indian law specifically deals with the protection of wild animals, birds and plants?", "Wild Life (Protection) Act, 1972", "Forest Rights Act, 2006", "Water Act, 1974", "Air Act, 1981"),
        ("Which Indian law aims to prevent and control water pollution?", "Water (Prevention and Control of Pollution) Act, 1974", "Air (Prevention and Control of Pollution) Act, 1981", "Environment (Protection) Act, 1986", "Wild Life (Protection) Act, 1972"),
        ("Which Indian law aims to prevent and control air pollution?", "Air (Prevention and Control of Pollution) Act, 1981", "Water Act, 1974", "Forest Conservation Act, 1980", "Biological Diversity Act, 2002"),
        ("Which constitutional provision directs the Indian state to protect and improve the environment?", "Article 48A", "Article 14", "Article 19", "Article 32"),
        ("Which Fundamental Duty asks citizens to protect and improve the natural environment?", "Article 51A(g)", "Article 21A", "Article 17", "Article 40"),
        ("Which Indian organisation is the statutory body responsible for preventing and controlling pollution at the national level?", "Central Pollution Control Board", "NITI Aayog", "National Disaster Management Authority", "University Grants Commission"),
        ("Which Indian institution is responsible for coordinating wildlife conservation and protected-area management at the national level?", "National Board for Wildlife", "Election Commission", "Finance Commission", "National Human Rights Commission"),
        ("Which global assessment platform focuses on biodiversity and ecosystem services?", "IPBES", "WTO", "WHO", "ILO"),
        ("What is the main purpose of an Environmental Impact Assessment?", "Evaluate likely environmental effects before a project is approved", "Measure only a project's financial profit", "Determine the market price of land", "Calculate employee productivity"),
        ("What does the term 'ecological footprint' estimate?", "Human demand on biologically productive land and water", "The number of animal footprints in a forest", "The depth of groundwater", "The amount of rainfall in a region"),
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
                    f"Invalid question format: {difficulty} #{index}"
                )

            question, correct, *wrong = item
            options = [correct] + wrong

            if not all(isinstance(value, str) and value.strip() for value in item):
                raise ValueError(
                    f"Empty field: {difficulty} #{index}"
                )

            if len(set(options)) != 4:
                raise ValueError(
                    f"Duplicate options: {difficulty} #{index}"
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
                "Learn about ecosystems, biodiversity, wildlife conservation, environmental laws, pollution and climate change."
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
                raise ValueError(
                    f"Multiple {difficulty} quizzes found."
                )

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
        print("GK TOPIC 15 INSERTED SUCCESSFULLY")
        print("Environment, Ecology, Wildlife and Climate Change")
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
