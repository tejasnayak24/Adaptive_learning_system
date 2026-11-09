
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

LESSON_TITLE = "Pollution and Its Control"
TARGET_QUESTIONS = 30

QUESTION_BANK = {
    "Easy": [
        ("What is pollution?", ["The introduction of harmful substances or forms of energy into the environment", "The natural growth of plants", "The formation of clouds only", "The process of seed germination"], "A"),
        ("Which activity is a common source of air pollution?", ["Planting trees", "Burning fossil fuels", "Collecting rainwater", "Composting leaves"], "B"),
        ("Which gas is a major contributor to human-caused global warming?", ["Oxygen", "Helium", "Carbon dioxide", "Neon"], "C"),
        ("What type of pollution is caused by excessive unwanted sound?", ["Water pollution", "Soil pollution", "Light pollution", "Noise pollution"], "D"),
        ("Which action can help reduce air pollution?", ["Using public transport when practical", "Burning plastic waste outdoors", "Leaving vehicle engines running unnecessarily", "Burning rubbish in residential areas"], "A"),
        ("Which of these is a common source of water pollution?", ["Planting native trees", "Discharging untreated sewage into rivers", "Installing solar panels", "Using a reusable bottle"], "B"),
        ("Which pollutant can contaminate soil when electronic waste is improperly discarded?", ["Clean rainwater", "Oxygen", "Lead from some electronic components", "Sunlight"], "C"),
        ("What is the purpose of a wastewater treatment plant?", ["To increase sewage contamination", "To release all untreated waste into rivers", "To convert every pollutant into drinking water automatically", "To remove or reduce contaminants from wastewater"], "D"),
        ("Which of these is biodegradable under suitable conditions?", ["Fruit peels", "Glass bottles", "Aluminium cans", "Many plastic bags"], "A"),
        ("What is smog?", ["A type of clean drinking water", "Air pollution involving a mixture of pollutants and atmospheric conditions", "A form of soil fertiliser", "A natural mineral deposit"], "B"),
        ("Which human activity can cause soil pollution?", ["Planting trees", "Protecting wetlands", "Improper disposal of hazardous chemicals", "Collecting reusable materials"], "C"),
        ("Which of these can help reduce plastic pollution?", ["Using a new disposable bag for every item", "Throwing plastic into streams", "Burning plastic in open areas", "Using reusable bags and reducing single-use plastics"], "D"),
        ("What does the three-R principle commonly stand for?", ["Reduce, Reuse, Recycle", "Remove, Release, Replace", "Run, Rest, Repeat", "Read, Record, Report"], "A"),
        ("Which type of pollution can be caused by excessive artificial lighting at night?", ["Thermal pollution only", "Light pollution", "Soil erosion", "Radioactivity in every case"], "B"),
        ("What is one effect of noise pollution on humans?", ["Improved hearing in every situation", "Guaranteed better sleep", "Stress and hearing damage at high or prolonged exposure levels", "Increased soil fertility"], "C"),
        ("Which of these is a source of marine plastic pollution?", ["Properly collected recyclable materials", "Protected coastal vegetation", "Reusable containers", "Plastic waste entering waterways"], "D"),
        ("Which practice can help prevent water pollution at home?", ["Disposing of medicines and chemicals through appropriate collection systems", "Pouring motor oil into storm drains", "Dumping paint into streams", "Throwing batteries into ponds"], "A"),
        ("What is the main purpose of planting trees in polluted urban areas?", ["To produce plastic", "To provide shade and potentially capture some airborne particles and carbon", "To eliminate all pollutants instantly", "To prevent all rainfall"], "B"),
        ("Which of these is an example of air pollution from indoor sources?", ["Fresh air entering a well-ventilated room", "A healthy garden", "Smoke from burning solid fuels in a poorly ventilated kitchen", "Rainwater collected in a clean tank"], "C"),
        ("What is an oil spill?", ["A method of recycling paper", "A type of cloud formation", "A form of noise pollution", "The release of petroleum into the environment, often into water"], "D"),
        ("Which pollutant is commonly associated with vehicle exhaust?", ["Nitrogen oxides", "Pure drinking water", "Table sugar", "Clean oxygen only"], "A"),
        ("What can happen when fertiliser runoff enters a lake in excessive amounts?", ["The water becomes automatically sterile", "Excessive algal growth may occur", "All aquatic organisms gain unlimited oxygen", "The lake becomes pollution-free"], "B"),
        ("Which waste item should generally be kept out of ordinary household rubbish when a suitable collection programme exists?", ["Clean cardboard", "Reusable cloth", "Used batteries", "Uncontaminated paper"], "C"),
        ("Which is a simple way to reduce noise pollution from loud music?", ["Increase the volume continuously", "Use loudspeakers late at night near homes", "Place speakers facing neighbouring houses", "Keep sound levels reasonable and limit unnecessary loud noise"], "D"),
        ("What is water pollution?", ["Contamination of water that reduces its quality or makes it harmful", "The natural movement of clean water", "The evaporation of pure water", "The freezing of water"], "A"),
        ("Which of these is an example of land pollution?", ["Planting a community garden", "Dumping rubbish in an open field", "Restoring a wetland", "Composting food scraps properly"], "B"),
        ("Why should plastic waste not be burned in open spaces?", ["It always becomes harmless water", "It improves air quality", "Burning can release harmful gases and particles", "It eliminates all waste without environmental effects"], "C"),
        ("Which source can contribute to thermal pollution in a river?", ["Planting trees along the riverbank", "Collecting litter", "Reducing wastewater discharge", "Discharging heated industrial cooling water"], "D"),
        ("Which action helps reduce pollution from vehicles?", ["Maintaining vehicles and choosing lower-emission transport options", "Removing pollution-control equipment", "Burning fuel unnecessarily", "Ignoring engine problems"], "A"),
        ("Why is proper waste segregation useful?", ["It makes all waste hazardous", "It helps recyclable, organic and hazardous waste be handled appropriately", "It prevents every type of pollution immediately", "It increases contamination of clean materials"], "B"),
    ],

    "Medium": [
        ("How can fine particulate matter affect human health?", ["It improves lung function", "It only affects building colour", "It can penetrate the respiratory system and contribute to heart and lung problems", "It is always harmless at any concentration"], "C"),
        ("Why can excess nitrogen and phosphorus entering lakes be harmful?", ["They eliminate all plant growth", "They permanently increase dissolved oxygen", "They prevent algae from growing", "They can cause eutrophication and oxygen depletion"], "D"),
        ("What is the main purpose of catalytic converters in many vehicles?", ["To reduce certain harmful exhaust emissions", "To increase soot emissions", "To produce fuel from road dust", "To remove every pollutant from the atmosphere"], "A"),
        ("Why is untreated sewage dangerous when discharged into water bodies?", ["It always improves drinking-water quality", "It may introduce pathogens and organic matter that depletes oxygen", "It removes all nutrients from water", "It prevents microbial growth"], "B"),
        ("How can acid rain form?", ["When pure water freezes", "When oxygen turns directly into acid", "When certain sulfur and nitrogen oxides react in the atmosphere to form acids", "When plants release only water vapour"], "C"),
        ("What is a major benefit of composting suitable organic waste?", ["It creates non-biodegradable plastic", "It guarantees the removal of all hazardous chemicals", "It increases the amount of waste sent to landfills", "It converts organic waste into a useful soil amendment under controlled conditions"], "D"),
        ("Why is groundwater contamination particularly concerning?", ["Pollutants can be difficult to detect and remove once they enter an aquifer", "Groundwater cannot be used by people", "All pollutants naturally disappear within minutes", "Groundwater is never connected to surface water"], "A"),
        ("What is the purpose of an electrostatic precipitator in some industrial facilities?", ["To increase particulate emissions", "To remove particles from exhaust gases using electrical forces", "To treat drinking water with sunlight only", "To produce noise"], "B"),
        ("How can wetlands help improve water quality?", ["They convert all contaminants into oxygen", "They stop every water flow", "They can retain sediments and remove or transform some pollutants", "They guarantee that all wastewater is potable"], "C"),
        ("Why can persistent organic pollutants be dangerous?", ["They break down instantly in every environment", "They cannot enter food chains", "They are always essential nutrients", "Some persist, accumulate in organisms and can cause toxic effects"], "D"),
        ("What is secondary air pollution?", ["Pollution formed in the atmosphere through chemical reactions involving emitted pollutants", "Pollution that exists only indoors", "Pollution caused exclusively by noise", "Pollution that cannot affect people"], "A"),
        ("How can proper public transport systems reduce urban pollution?", ["They make every journey emission-free", "They can reduce vehicle use and emissions per passenger when well utilised", "They increase the need for individual cars in every case", "They eliminate the need for vehicle maintenance"], "B"),
        ("Why can open burning of waste be harmful even when the waste appears dry?", ["Dry waste can never release pollutants", "Burning always converts waste into clean oxygen", "Combustion can release particles and hazardous chemicals depending on the materials and conditions", "Dry waste contains no chemical energy"], "C"),
        ("What is biomagnification?", ["The breakdown of all pollutants into harmless substances", "The movement of clean water through soil", "The reduction of every chemical concentration at higher trophic levels", "An increase in the concentration of certain persistent substances at higher trophic levels"], "D"),
        ("How does a sanitary landfill differ from uncontrolled open dumping?", ["A sanitary landfill uses engineered controls to manage waste and reduce environmental risks", "Open dumping always provides better pollution control", "A sanitary landfill contains no waste", "Both methods have identical environmental safeguards"], "A"),
        ("Why is source reduction often preferred over recycling alone?", ["It requires more raw materials for every product", "Preventing waste avoids some material use and pollution before waste is generated", "It makes product design irrelevant", "It always increases landfill waste"], "B"),
        ("Which strategy can help control industrial wastewater pollution?", ["Discharging wastewater directly into rivers", "Mixing hazardous waste with drinking water", "Treating wastewater and monitoring compliance before discharge", "Ignoring chemical spills"], "C"),
        ("Why can excessive noise exposure damage hearing?", ["Sound has no energy", "The ear cannot respond to sound", "Only water can damage hearing", "High sound levels can damage delicate structures in the inner ear"], "D"),
        ("What is the main environmental concern associated with excessive pesticide runoff?", ["It can harm non-target organisms and contaminate surface water", "It always improves aquatic biodiversity", "It removes every pathogen without side effects", "It makes water safe to drink without treatment"], "A"),
        ("How can green roofs help reduce some urban environmental problems?", ["They guarantee that cities will have no pollution", "They can reduce stormwater runoff and help moderate building temperatures", "They increase roof temperatures in every case", "They prevent all urban wildlife"], "B"),
        ("Why can indoor air pollution be high in poorly ventilated buildings?", ["Indoor pollutants cannot be generated", "Outdoor air always contains more pollution", "Pollutants from cooking, materials or combustion can accumulate indoors", "Ventilation creates every pollutant"], "C"),
        ("What is the purpose of emission standards for factories and vehicles?", ["To encourage unlimited emissions", "To replace all environmental monitoring", "To guarantee that emissions never occur", "To set limits or requirements intended to control harmful releases"], "D"),
        ("How can planting vegetation along waterways help reduce agricultural pollution?", ["Vegetated buffer strips can trap sediment and intercept some nutrients before they reach water", "They increase runoff in every situation", "They remove the need to manage fertilisers", "They guarantee that no pollutant reaches the river"], "A"),
        ("Why is electronic waste a concern when improperly disposed of?", ["It contains only harmless plant material", "Some devices contain hazardous substances that can contaminate soil and water", "It always decomposes completely within one day", "It cannot be recycled"], "B"),
        ("What is thermal pollution?", ["A rise in air pressure only", "The formation of soil from rock", "A harmful change in the temperature of an environment, often affecting aquatic ecosystems", "A form of plastic recycling"], "C"),
        ("How can energy efficiency reduce air pollution?", ["It requires more fuel for the same output in every case", "It eliminates the need for any energy source", "It creates additional combustion by definition", "It can reduce fuel consumption and associated emissions for the same useful service"], "D"),
        ("Why is environmental monitoring important after an oil spill?", ["It helps assess contamination, ecological effects and recovery", "It guarantees that the spill never occurred", "It replaces the need to contain the oil", "It prevents all marine organisms from moving"], "A"),
        ("Which approach is most suitable for managing hazardous household chemicals?", ["Pouring them into storm drains", "Using designated collection or disposal programmes and following product guidance", "Burning them in the kitchen", "Mixing them randomly with other chemicals"], "B"),
        ("Why can air pollution cross national boundaries?", ["Air pollutants never move", "Every pollutant settles immediately at its source", "Atmospheric winds can transport pollutants over long distances", "Pollution exists only indoors"], "C"),
        ("What is one important limitation of using trees alone to solve air pollution?", ["Trees produce no ecological benefits", "Trees increase every pollutant in every situation", "Trees make emission standards unnecessary", "Trees cannot replace controlling pollution at its source"], "D"),
    ],

    "Hard": [
        ("A lake receives large quantities of agricultural runoff, develops algal blooms and later experiences fish deaths. Which mechanism best explains the fish deaths?", ["Decomposition of excess organic matter consumes dissolved oxygen, creating hypoxic conditions", "Algae permanently increase oxygen at all depths", "Nutrients immediately remove all microorganisms", "Fish die because water contains too much sunlight"], "A"),
        ("Why can reducing emissions of nitrogen oxides and volatile organic compounds help control ground-level ozone in many urban environments?", ["Ozone is emitted only by trees", "These pollutants participate in sunlight-driven atmospheric reactions that form ozone", "Ozone is formed only by boiling water", "Nitrogen oxides and volatile organic compounds have no atmospheric chemistry"], "B"),
        ("A factory installs particulate filters but continues releasing untreated dissolved chemicals into a river. What conclusion is most appropriate?", ["The filters have solved every pollution problem", "Particulate filters remove every dissolved chemical", "Controlling one pollution pathway does not necessarily control other pollutants or pathways", "River pollution depends only on particle size"], "C"),
        ("Why may a pollutant that is present at a low concentration still be a concern?", ["Low concentrations are always toxic", "All pollutants have identical toxicity", "Concentration never affects risk", "Risk can depend on toxicity, exposure duration, bioaccumulation and the sensitivity of exposed organisms"], "D"),
        ("A wastewater plant reduces organic matter but leaves high concentrations of dissolved nitrogen and phosphorus. Which additional treatment goal may be needed to reduce eutrophication risk?", ["Nutrient removal", "Increasing untreated sewage discharge", "Adding more fertiliser", "Eliminating all water monitoring"], "A"),
        ("Why can an environmental policy based only on the visible amount of litter underestimate pollution?", ["Invisible pollutants are always harmless", "Air, water and soil may contain contaminants that cannot be judged by appearance alone", "Every pollutant is brightly coloured", "Pollution can occur only as solid waste"], "B"),
        ("A city experiences a temperature inversion during a period of heavy traffic. Why can air quality worsen?", ["The inversion destroys all pollutants instantly", "Vehicles stop emitting pollutants during inversions", "Stable air can limit vertical mixing and trap pollutants near the ground", "Wind always increases during an inversion"], "C"),
        ("Why is the polluter-pays principle used in environmental management?", ["It exempts polluters from responsibility", "It makes pollution free to society", "It guarantees that damage can never occur", "It aims to place appropriate pollution prevention and damage costs on those responsible"], "D"),
        ("A contaminated site contains lead in soil. Why may simply covering the soil not always be a complete remediation solution?", ["The cover may reduce exposure but does not necessarily remove the lead, and long-term integrity must be maintained", "Lead always decomposes into harmless water", "Covering soil increases the amount of lead chemically destroyed", "Lead cannot move from soil to people"], "A"),
        ("Why can source apportionment be useful when controlling urban air pollution?", ["It assumes all sources contribute equally", "It helps estimate the relative contributions of different pollution sources", "It replaces all emission measurements with guesses", "It is used only to measure noise"], "B"),
        ("A river has high biochemical oxygen demand (BOD). What does this generally indicate?", ["The water contains no organic matter", "All aquatic life has unlimited oxygen", "Microorganisms may consume substantial oxygen while decomposing biodegradable material", "The water is guaranteed safe to drink"], "C"),
        ("Why is it important to assess both exposure and toxicity when evaluating a pollutant's health risk?", ["Every toxic substance causes the same effect at every dose", "Exposure duration is never relevant", "Toxicity alone always establishes the exact risk", "A hazardous substance's risk depends partly on how much, how often and by what route people encounter it"], "D"),
        ("Why can persistent pollutants be difficult to manage after they have entered a food web?", ["They may resist degradation and accumulate through feeding relationships", "They disappear immediately after entering organisms", "They cannot move between trophic levels", "They are always transformed into nutrients"], "A"),
        ("An industrial site reduces stack emissions but moves production to a location with weaker environmental controls. What broader concern arises?", ["The pollution has necessarily been eliminated", "The pollution burden may have shifted geographically rather than being fully reduced", "Pollution controls are never useful", "Industrial relocation cannot affect the environment"], "B"),
        ("Why can lifecycle analysis lead to a different environmental conclusion from considering only a product's use phase?", ["The use phase is always irrelevant", "Every product has the same manufacturing impact", "Manufacturing, raw-material extraction, transport and disposal can contribute substantially to total impacts", "Lifecycle analysis ignores resource use"], "C"),
        ("A wetland removes some nutrients from agricultural runoff. Why should it not be treated as an unlimited substitute for pollution prevention?", ["Wetlands create unlimited storage for every contaminant", "Wetlands cannot be damaged by pollutants", "All pollutants are harmless in wetlands", "Wetlands have finite capacity and can be degraded or overwhelmed by excessive pollutant loads"], "D"),
        ("Why can reducing sulphur dioxide emissions help reduce acid deposition?", ["Sulphur dioxide can be oxidised and converted into acidic compounds in the atmosphere", "Sulphur dioxide is a form of clean drinking water", "Sulphur dioxide always neutralises every acid", "Acid deposition is unrelated to atmospheric emissions"], "A"),
        ("Which finding would most strongly indicate that a pollution-control intervention is effective?", ["One photograph of a clean-looking street", "Comparable before-and-after measurements show reduced pollutant levels while accounting for relevant changes and variability", "A claim that the intervention must work", "A single measurement with no baseline"], "B"),
        ("Why is environmental justice relevant to pollution control?", ["Pollution affects all communities identically in every circumstance", "Environmental hazards have no social dimensions", "Pollution burdens and access to protection can be unevenly distributed among communities", "It concerns only wildlife classification"], "C"),
        ("A factory releases heated water into a stream. What is a potential ecological effect if the temperature rises substantially?", ["Dissolved oxygen always increases with temperature", "All organisms become more tolerant immediately", "Water temperature has no effect on aquatic life", "Warmer water can hold less dissolved oxygen and may stress temperature-sensitive organisms"], "D"),
        ("Why should particulate pollution controls be evaluated for their waste streams as well as their air emissions?", ["Captured particles may contain contaminants that require safe handling and disposal", "Captured particles automatically become harmless", "Air filters create no collected material", "Waste handling is unrelated to pollution prevention"], "A"),
        ("What is a key reason for using multiple monitoring locations when assessing a river pollution event?", ["Pollutants are distributed uniformly at all times", "Pollution levels can vary upstream, downstream and across locations", "A single point always represents the entire river", "Monitoring locations cannot affect interpretation"], "B"),
        ("Why might an intervention that reduces one pollutant increase another environmental burden?", ["Environmental systems cannot have trade-offs", "Pollution-control technology never uses energy or materials", "Some interventions shift impacts between media or require energy and materials that have their own impacts", "All interventions eliminate every impact simultaneously"], "C"),
        ("A community is exposed to low levels of a pollutant over many years. Why might a short-term measurement alone be inadequate?", ["Only acute exposures can affect health", "Long-term exposure is always harmless", "One measurement reveals every historical exposure", "Chronic exposure and cumulative dose may be important to risk assessment"], "D"),
        ("Why is open burning of mixed municipal waste especially problematic?", ["Mixed waste can release a variable combination of particulate matter and hazardous combustion products", "It guarantees complete destruction of all toxic substances", "It creates no air emissions", "It makes source segregation unnecessary"], "A"),
        ("Which strategy best addresses plastic pollution entering a river from multiple sources?", ["Clean only one visible pile and ignore all other sources", "Combine source reduction, collection, improved waste management and interception where appropriate", "Increase single-use plastic consumption", "Rely only on downstream cleanup"], "B"),
        ("Why should the effectiveness of a noise barrier be measured at relevant receiving locations?", ["Noise barriers always eliminate sound everywhere", "Sound does not travel around barriers", "Actual noise reduction depends on geometry, frequency, distance and local conditions", "A barrier's height has no acoustic effect"], "C"),
        ("A town treats drinking water but allows untreated sewage into the source river. Why is source protection still important?", ["Treatment makes every contaminant irrelevant", "Source pollution can never affect treatment needs", "Water sources are independent of public health", "Reducing source contamination can lower health risks and the burden on treatment systems"], "D"),
        ("Why can an environmental impact assessment be important before a large industrial project?", ["It helps identify likely impacts, alternatives and mitigation measures before decisions are finalised", "It guarantees that no impact will occur", "It replaces every operating permit automatically", "It is useful only after the project closes"], "A"),
        ("Which approach best supports long-term pollution control in a rapidly growing city?", ["Rely only on occasional clean-up drives", "Combine prevention, infrastructure, regulation, monitoring and public participation", "Ignore waste generation data", "Increase emissions while measuring only visible litter"], "B"),
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

        print("\nPollution and Its Control expansion completed!")
        print(f"Total new questions inserted: {inserted_total}")
        print("Easy: 30 questions")
        print("Medium: 30 questions")
        print("Hard: 30 questions")
        print("Other lessons and Social Science were not modified.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()
