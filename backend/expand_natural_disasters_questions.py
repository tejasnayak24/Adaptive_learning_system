
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"
LESSON_TITLE = "Natural Disasters and Preparedness"
TARGET_QUESTIONS = 30

# Format: question, option A, option B, option C, option D, correct answer
QUESTION_BANK = {
    "Easy": [
        ("What is a natural disaster?", "A natural event that causes serious damage or loss", "A school celebration", "A routine traffic signal", "A computer update", "A"),
        ("Which instrument is commonly used to measure earthquake vibrations?", "Thermometer", "Seismograph", "Barometer", "Hygrometer", "B"),
        ("Which natural disaster involves the sudden overflow of water onto normally dry land?", "Drought", "Earthquake", "Flood", "Heatwave", "C"),
        ("What should you do during an earthquake if you are indoors?", "Stand beside a glass window", "Use the lift immediately", "Run toward hanging lights", "Drop, cover and hold on", "D"),
        ("Which disaster is associated with a long period of unusually low rainfall?", "Drought", "Cyclone", "Tsunami", "Landslide", "A"),
        ("What is a tsunami?", "A type of desert wind", "A series of large sea waves often caused by undersea disturbances", "A volcanic rock", "A period of low rainfall", "B"),
        ("Which event involves molten rock reaching Earth's surface?", "Flood", "Drought", "Volcanic eruption", "Tornado", "C"),
        ("What is a cyclone?", "A sudden snowstorm only", "An earthquake beneath the sea", "A long period without rain", "A large rotating storm system", "D"),
        ("Which item is useful in an emergency kit?", "First-aid supplies", "Broken glass", "Open flames", "Perishable food left uncovered", "A"),
        ("What should you do if an official evacuation order is issued?", "Ignore it until the disaster arrives", "Follow the instructions and evacuate safely", "Move toward the hazard to observe it", "Block emergency vehicles", "B"),
        ("What is a landslide?", "A sudden rise in sea level caused by tides", "A period of extreme heat", "The movement of rock, soil or debris down a slope", "A type of cloud", "C"),
        ("Which natural disaster can be triggered by intense rainfall on unstable slopes?", "Solar eclipse", "Drought", "Heatwave", "Landslide", "D"),
        ("What is the safest place during a thunderstorm?", "Inside a substantial building or enclosed vehicle", "Under an isolated tall tree", "In an open field holding metal objects", "In a swimming pool", "A"),
        ("Which disaster can result from prolonged extreme temperatures?", "Tsunami", "Heatwave", "Earthquake", "Volcanic eruption", "B"),
        ("What is disaster preparedness?", "Waiting until a disaster happens", "Ignoring warnings", "Planning and preparing before emergencies occur", "Spreading unverified rumours", "C"),
        ("Why should emergency exits be kept clear?", "To store heavy furniture", "To prevent people from leaving", "To block smoke in every situation", "To allow safe and rapid evacuation", "D"),
        ("Which organisation should people generally follow for official local disaster warnings?", "The relevant authorised disaster management or emergency agency", "Unverified social media posts", "Anonymous online accounts", "Rumours from strangers", "A"),
        ("What should you do if floodwater covers a road?", "Drive through quickly", "Avoid entering the floodwater and seek a safer route", "Walk through it without checking depth", "Stand in the water to measure it", "B"),
        ("Which natural hazard is associated with shaking of Earth's crust?", "Cyclone", "Drought", "Earthquake", "Heatwave", "C"),
        ("Why is clean drinking water important after a disaster?", "It increases the intensity of storms", "It prevents all building damage", "It replaces the need for shelter", "It helps prevent dehydration and waterborne illness", "D"),
        ("What should a family emergency plan include?", "Meeting places and emergency contacts", "Only a list of favourite movies", "Instructions to ignore warnings", "A plan to use lifts during every emergency", "A"),
        ("What is a wildfire?", "A controlled classroom experiment", "An uncontrolled fire spreading through vegetation", "A type of ocean current", "A period of heavy snowfall", "B"),
        ("Which condition can increase wildfire risk?", "Wet vegetation and cool conditions in every case", "Heavy rainfall with saturated soil", "Hot, dry and windy weather", "Low temperatures and high humidity only", "C"),
        ("What is the purpose of a first-aid kit?", "To predict earthquakes", "To stop all natural disasters", "To replace emergency services in every situation", "To provide basic supplies for treating minor injuries", "D"),
        ("What is a hazard map used for?", "Identifying areas exposed to particular hazards", "Predicting every disaster with certainty", "Measuring people's height", "Recording school attendance", "A"),
        ("What is an aftershock?", "A storm following a heatwave", "An earthquake that follows a larger earthquake in the same region", "A flood caused only by a dam", "A volcanic rock", "B"),
        ("Why are emergency drills conducted?", "To make evacuation routes harder to find", "To increase panic", "To practise safe responses before an emergency", "To replace all emergency plans", "C"),
        ("What should you do if you smell gas after an earthquake?", "Light a match to find the leak", "Switch electrical appliances on and off repeatedly", "Stay inside and ignore it", "Avoid flames and electrical switches, leave the area and report it from a safe location", "D"),
        ("Which action helps reduce flood risk in communities?", "Keeping drainage systems clear", "Dumping rubbish into drains", "Building on every floodplain without planning", "Blocking natural waterways", "A"),
        ("Why should people avoid spreading unverified disaster reports?", "They always improve rescue work", "False information can create panic and obstruct emergency response", "It guarantees accurate evacuation", "It prevents hazards from occurring", "B"),
    ],
    "Medium": [
        ("Why do many earthquakes occur near tectonic plate boundaries?", "The atmosphere pushes plates together", "Rainfall directly creates tectonic plates", "Plate interactions build up and release stress along faults", "The Moon melts Earth's crust", "C"),
        ("What is the difference between a hazard and a disaster?", "A hazard is always harmless", "A disaster cannot affect people", "They mean exactly the same thing in every context", "A hazard is a potential source of harm; a disaster occurs when impacts seriously disrupt a community", "D"),
        ("Why can deforestation increase landslide risk on some slopes?", "Removing vegetation can reduce root reinforcement and alter water movement", "Tree removal makes every slope stronger", "It eliminates gravity", "It prevents rainfall from reaching soil", "A"),
        ("What does an early warning system aim to do?", "Guarantee that no hazard occurs", "Provide timely information so people can take protective action", "Replace evacuation planning", "Stop all earthquakes", "B"),
        ("Why are coastal areas vulnerable to storm surges?", "They are always above sea level", "They cannot experience strong winds", "Strong storm winds and pressure changes can raise sea levels near the coast", "They prevent ocean water from moving", "C"),
        ("What is the purpose of an evacuation route map?", "To identify the deepest floodwater", "To show only tourist attractions", "To predict the exact time of every earthquake", "To guide people toward safer locations using planned routes", "D"),
        ("Why should people avoid using lifts during a building fire or earthquake?", "Power failure or structural damage can trap occupants", "Lifts always move to the safest floor", "Lifts prevent smoke from spreading everywhere", "Lifts are designed only for outdoor use", "A"),
        ("How can wetlands help reduce some flood impacts?", "They generate additional storms", "They can store excess water and slow its movement", "They prevent all rainfall", "They make rivers overflow more quickly in every case", "B"),
        ("What is the main purpose of seismic building design?", "To make buildings completely immune to every possible earthquake", "To increase structural brittleness", "To improve a structure's ability to resist earthquake forces and reduce collapse risk", "To remove tectonic plate movement", "C"),
        ("Why is it dangerous to walk through moving floodwater?", "Floodwater is always shallow", "It contains no hidden hazards", "It cannot move people", "It can sweep people away and conceal holes, debris or electrical hazards", "D"),
        ("What is a storm surge?", "An abnormal rise in coastal water level caused mainly by a storm's winds and pressure", "A sudden fall in mountain temperature", "A small earthquake after an eruption", "A long-term absence of rainfall", "A"),
        ("Which practice helps reduce heat-related illness during a heatwave?", "Performing strenuous exercise at midday", "Staying hydrated and limiting strenuous activity during the hottest hours", "Wearing heavy clothing in direct sunlight", "Ignoring symptoms of heat exhaustion", "B"),
        ("Why is land-use planning important in hazard-prone areas?", "It prevents all geological processes", "It makes warning systems unnecessary", "It can reduce exposure by limiting unsafe development in high-risk areas", "It guarantees that storms will weaken", "C"),
        ("What is disaster mitigation?", "The act of spreading rumours", "Emergency treatment only after an event", "A method of predicting every event exactly", "Actions that reduce the likelihood or severity of disaster impacts", "D"),
        ("What is disaster response?", "Immediate actions to protect life and meet urgent needs during and just after an event", "Only long-term economic planning", "A method of creating natural hazards", "A process limited to writing reports years later", "A"),
        ("Why should emergency supplies include essential medicines where appropriate?", "They make disasters impossible", "They can help people maintain necessary treatment when normal services are disrupted", "They replace all medical advice", "They can be stored without regard to expiry dates", "B"),
        ("What should be considered when preparing an emergency plan for people with disabilities?", "Only the number of nearby shops", "Whether all alarms are silent", "Accessible warnings, evacuation arrangements and individual support needs", "How to prevent them from receiving information", "C"),
        ("Why can heavy rainfall trigger flash floods?", "All rain evaporates instantly", "Rivers always absorb unlimited water", "Rain cannot flow across land", "Rainfall may exceed infiltration and drainage capacity, causing rapid runoff", "D"),
        ("What is a key benefit of community disaster drills?", "They help people practise roles, routes and communication procedures", "They make emergency contacts unnecessary", "They prevent every storm", "They replace safe infrastructure", "A"),
        ("Why should people avoid touching fallen electrical wires after a storm?", "The wires are always disconnected", "They may remain energised and cause severe electric shock", "Water neutralises electricity", "Rubber shoes guarantee complete protection", "B"),
        ("What is one way to reduce drought vulnerability in agriculture?", "Use more water regardless of availability", "Remove all soil cover", "Improve irrigation efficiency and choose suitable crops", "Ignore weather forecasts", "C"),
        ("What does structural vulnerability describe?", "The number of clouds in the sky", "The exact magnitude of every earthquake", "The distance between planets", "How susceptible buildings or infrastructure are to damage from hazards", "D"),
        ("How can mangroves help some coastal communities?", "They can reduce wave energy and help stabilise shorelines", "They stop all tsunamis", "They prevent every storm surge", "They eliminate sea-level rise", "A"),
        ("Why is risk communication important during an emergency?", "It makes all hazards disappear", "It helps people understand threats and take appropriate action", "It replaces rescue operations", "It guarantees that no one will be affected", "B"),
        ("What is the difference between preparedness and recovery?", "Preparedness happens only after all damage is repaired", "Recovery means predicting earthquakes", "Preparedness occurs before an emergency; recovery restores services and livelihoods afterward", "They are unrelated to disaster management", "C"),
        ("Why should emergency drinking water be stored safely?", "To increase contamination", "To make it unsuitable for use", "To prevent anyone from accessing it", "To maintain a usable supply if normal water services are disrupted", "D"),
        ("What is the purpose of a go-bag or emergency kit?", "To keep essential supplies ready for evacuation or temporary disruption", "To store only decorative items", "To replace all community shelters", "To guarantee that a disaster will not happen", "A"),
        ("Why can building on steep unstable slopes increase risk?", "Slopes are never affected by rain", "Slope failure can move soil and debris onto buildings and roads", "Gravity does not act on buildings", "Vegetation has no relationship to slope stability", "B"),
        ("How can satellite observations support disaster management?", "They prevent every natural hazard", "They remove floodwater directly", "They can help monitor storms, fires, floods and changes over large areas", "They make local warnings unnecessary", "C"),
        ("What is the main purpose of post-disaster damage assessment?", "To determine which rumours are popular", "To guarantee there will be no future disasters", "To delay all assistance", "To identify impacts, urgent needs and recovery priorities", "D"),
    ],
    "Hard": [
        ("A town faces frequent river floods. Which strategy best combines mitigation and preparedness?", "Improve floodplain planning and drainage while maintaining warning systems and evacuation plans", "Wait until floodwater enters homes before planning", "Block every natural waterway without assessment", "Ignore historical flood records", "A"),
        ("Why can earthquake magnitude and observed intensity differ?", "Magnitude measures damage at one building only", "Magnitude describes earthquake size, while intensity describes shaking and effects at a particular location", "Intensity is always the same everywhere", "Magnitude measures rainfall", "B"),
        ("A region receives 120 mm of rain in three hours. The soil and drainage can handle only 20 mm per hour. Why is rapid runoff likely?", "Rainfall is below drainage capacity", "All rain will evaporate before reaching the ground", "Rainfall intensity exceeds the combined local capacity to absorb or drain water", "The region has no gravity", "C"),
        ("Which approach is most appropriate for communicating a tsunami warning to a coastal community?", "Wait for people to see the wave before acting", "Use only an unverified online post", "Tell people to gather at the shoreline", "Use authorised alerts and clear evacuation instructions, including routes to high ground or designated safe areas", "D"),
        ("Why can disaster losses be reduced even when a hazard cannot be prevented?", "Exposure and vulnerability can be reduced through planning, safer infrastructure and preparedness", "All hazards can be switched off", "Preparedness changes the Earth's tectonic plates", "Hazards never affect unprepared communities", "A"),
        ("A building is located near a fault. Which measure most directly reduces structural earthquake risk?", "Adding heavy unsecured objects to upper floors", "Applying appropriate seismic design, retrofitting and construction standards", "Blocking all exits", "Removing structural supports", "B"),
        ("Why can a small landslide become a major disaster in a densely populated area?", "Landslides occur only in empty areas", "Slope movement has no effect on infrastructure", "High exposure and vulnerability can cause extensive damage and casualties", "Population density prevents slope failure", "C"),
        ("What is a cascading disaster effect?", "A hazard that affects only one person", "A warning that has no consequences", "A natural event that ends before any secondary impact", "An initial event triggers further failures, such as an earthquake causing fires or infrastructure outages", "D"),
        ("Which combination best supports effective drought management?", "Monitoring rainfall and water supplies, demand management and sustainable water allocation", "Waiting until all reservoirs are empty", "Increasing water waste", "Ignoring crop and groundwater conditions", "A"),
        ("Why is a single evacuation route risky in a hazard-prone area?", "It guarantees faster evacuation in all circumstances", "It can become blocked, so alternative routes and accessible plans are important", "It removes the need for warnings", "It prevents people from reaching shelters", "B"),
        ("What is the main advantage of risk-based land-use zoning?", "It makes hazard maps unnecessary", "It guarantees that no property will ever be damaged", "It can steer development away from areas with unacceptable hazard exposure", "It prevents all extreme weather", "C"),
        ("Why can an earthquake cause a tsunami when it occurs beneath the ocean?", "All underwater earthquakes produce identical waves", "The ocean floor cannot move", "Tsunamis are caused only by tides", "Sudden vertical displacement of the seafloor can displace a large volume of water", "D"),
        ("Which action best supports safe recovery after a major flood?", "Assess damage, restore essential services safely and rebuild with reduced future risk", "Rebuild all structures exactly as before without assessing risk", "Ignore contamination of drinking water", "Remove every warning system", "A"),
        ("What is the purpose of a multi-hazard early warning system?", "To predict every event with perfect certainty", "To monitor different hazards and deliver actionable warnings to exposed people", "To replace local emergency services", "To prevent all natural events from occurring", "B"),
        ("Why can unplanned urbanisation increase disaster risk?", "It always improves drainage", "It removes all exposure to hazards", "It can increase exposure through unsafe construction and inadequate infrastructure", "It guarantees that slopes remain stable", "C"),
        ("Which factor is most relevant when estimating disaster risk?", "Only the name of the hazard", "Only the date of the last disaster", "Only the number of emergency vehicles", "The interaction of hazard, exposure, vulnerability and capacity", "D"),
        ("Why is redundancy important in emergency communication systems?", "Backup channels can help maintain communication if one system fails", "It ensures every network fails together", "It prevents all power outages", "It removes the need for accurate messages", "A"),
        ("What is a limitation of relying only on historical disaster records?", "Past records contain no useful information", "Future conditions and exposure may change, so past events cannot describe every possible risk", "Historical events never occurred", "It makes hazard mapping impossible", "B"),
        ("During a wildfire, why can wind direction and speed be important for evacuation decisions?", "Wind never affects fire behaviour", "Wind always extinguishes flames", "Wind can change the speed and direction of fire spread", "Wind prevents smoke from travelling", "C"),
        ("Why should shelters account for sanitation and safe water after disasters?", "Shelters do not need water", "Sanitation has no relationship to public health", "Unsafe water is harmless if boiled once in every situation", "Poor sanitation and contaminated water can increase disease risk", "D"),
        ("What is an example of nature-based disaster risk reduction?", "Restoring mangroves and wetlands to help buffer certain coastal and flood impacts", "Removing all natural vegetation from riverbanks", "Building directly across every drainage channel", "Filling wetlands without assessment", "A"),
        ("Why is community participation important in disaster planning?", "It makes expert advice unnecessary", "Local knowledge can reveal vulnerabilities, needs and practical evacuation barriers", "It guarantees hazards will not occur", "It prevents emergency agencies from communicating", "B"),
        ("A warning is issued, but residents do not evacuate because they distrust it. What should future planning improve?", "The colour of official vehicles only", "The number of warning sirens without any explanation", "Trust, accessible communication, warning credibility and clear action guidance", "The length of unrelated reports", "C"),
        ("Which action is most appropriate immediately after an earthquake if the building appears damaged?", "Use damaged lifts to leave quickly", "Return inside to collect nonessential items", "Stand beside damaged walls", "Move to a safe area, watch for aftershocks and follow official instructions", "D"),
        ("Why can flood risk increase when drainage channels are blocked by waste?", "Blocked channels can reduce flow capacity and cause water to back up", "Waste makes rainfall disappear", "Blocked drains increase soil infiltration everywhere", "Floodwater cannot enter streets", "A"),
        ("What is the key objective of the 'Build Back Better' approach?", "Reconstruct rapidly without assessing damage", "Use recovery to improve resilience and reduce future disaster risk", "Rebuild only the most exposed structures", "Remove preparedness plans after recovery", "B"),
        ("Why should disaster plans be reviewed and practised regularly?", "Hazard information and community needs never change", "Plans are effective even if no one knows them", "People, infrastructure, risks and procedures can change over time", "Practice increases every hazard", "C"),
        ("Which is a realistic limitation of earthquake prediction?", "Earthquakes can always be predicted to the exact minute", "Every earthquake occurs on a fixed schedule", "Seismic monitoring eliminates all uncertainty", "Scientists can assess seismic hazards, but precise time-and-place prediction is not currently reliable", "D"),
        ("Why can prolonged power failure complicate disaster response?", "It can disrupt communication, water pumping, medical equipment and other essential services", "It automatically restores roads", "It prevents all secondary hazards", "It makes emergency coordination unnecessary", "A"),
        ("Which set of actions best represents an all-hazards preparedness approach?", "Prepare only for one previously experienced event", "Identify local risks, plan protective actions, maintain supplies and practise communication and evacuation", "Wait for officials to arrive before identifying any exits", "Rely entirely on social media rumours", "B"),
    ],
}


def normalize(text):
    return " ".join(text.lower().split())


def main():
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DATABASE_PATH}")

    conn = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM lessons WHERE LOWER(TRIM(title)) = LOWER(TRIM(?))",
            (LESSON_TITLE,),
        )
        lesson_rows = cursor.fetchall()

        if len(lesson_rows) != 1:
            raise RuntimeError(
                f"Expected exactly one lesson named '{LESSON_TITLE}', "
                f"but found {len(lesson_rows)}."
            )

        lesson_id = lesson_rows[0][0]
        total_added = 0

        for difficulty in ("Easy", "Medium", "Hard"):
            cursor.execute(
                """
                SELECT id FROM quizzes
                WHERE lesson_id = ?
                  AND LOWER(TRIM(difficulty)) = LOWER(TRIM(?))
                """,
                (lesson_id, difficulty),
            )
            quiz_rows = cursor.fetchall()

            if len(quiz_rows) != 1:
                raise RuntimeError(
                    f"Expected exactly one {difficulty} quiz for "
                    f"'{LESSON_TITLE}', but found {len(quiz_rows)}."
                )

            quiz_id = quiz_rows[0][0]

            cursor.execute(
                "SELECT question FROM questions WHERE quiz_id = ?",
                (quiz_id,),
            )
            existing = {normalize(row[0]) for row in cursor.fetchall()}

            cursor.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                (quiz_id,),
            )
            current_count = cursor.fetchone()[0]
            needed = max(0, TARGET_QUESTIONS - current_count)

            candidates = []
            seen = set()

            for item in QUESTION_BANK[difficulty]:
                key = normalize(item[0])
                if key not in existing and key not in seen:
                    candidates.append(item)
                    seen.add(key)

            if len(candidates) < needed:
                raise RuntimeError(
                    f"{difficulty}: need {needed} new questions, "
                    f"but only {len(candidates)} unique candidates are available. "
                    "No changes have been committed."
                )

            to_insert = candidates[:needed]

            cursor.executemany(
                """
                INSERT INTO questions
                (quiz_id, question, option_a, option_b, option_c,
                 option_d, correct_answer)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (quiz_id, q, a, b, c, d, answer)
                    for q, a, b, c, d, answer in to_insert
                ],
            )

            total_added += len(to_insert)

            cursor.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                (quiz_id,),
            )
            final_count = cursor.fetchone()[0]

            print(
                f"{difficulty}: started with {current_count}, "
                f"added {len(to_insert)}, final total {final_count}"
            )

        conn.commit()
        print(
            f"\nSuccess! Added {total_added} questions "
            f"to '{LESSON_TITLE}'."
        )
        print("Other lessons and Social Science were not modified.")

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    main()
