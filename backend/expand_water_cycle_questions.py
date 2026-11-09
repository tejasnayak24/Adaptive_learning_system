
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"
LESSON_TITLE = "Water Cycle"
TARGET_QUESTIONS = 30

# Format: question, option A, option B, option C, option D, correct answer
QUESTION_BANK = {
    "Easy": [
        ("What is the water cycle?", "The continuous movement of water between Earth's surface and atmosphere", "The movement of rocks inside Earth", "The daily rotation of Earth", "The formation of stars", "A"),
        ("What is evaporation?", "Water vapour changing into liquid water", "Liquid water changing into water vapour", "Water freezing into ice", "Ice changing directly into liquid water", "B"),
        ("What is condensation?", "Water flowing downhill", "Ice melting into water", "Water vapour changing into liquid droplets", "Water soaking into soil", "C"),
        ("What is precipitation?", "Water vapour rising from oceans", "Water entering plant roots", "Water freezing underground", "Water falling from clouds as rain, snow, sleet or hail", "D"),
        ("What is the main energy source driving the water cycle?", "The Sun", "The Moon", "Earth's magnetic field", "Ocean tides alone", "A"),
        ("What happens during collection in the water cycle?", "Water becomes sunlight", "Water gathers in rivers, lakes, oceans and other reservoirs", "Clouds turn into rocks", "Water disappears permanently", "B"),
        ("What is transpiration?", "Water flowing from mountains", "Water freezing in lakes", "Water vapour released by plants, mainly through their leaves", "Rain falling from clouds", "C"),
        ("Which process forms clouds from water vapour?", "Infiltration", "Runoff", "Melting", "Condensation", "D"),
        ("Where does much of Earth's evaporation occur?", "From oceans and other water bodies", "Only from deserts", "Only from glaciers", "Only from underground rocks", "A"),
        ("What is runoff?", "Water changing into vapour", "Water flowing over the land surface toward streams and other water bodies", "Water vapour forming clouds", "Water freezing in the atmosphere", "B"),
        ("What is infiltration?", "Water falling as snow", "Water leaving plant leaves", "Water entering the soil from the surface", "Water vapour turning into ice only", "C"),
        ("Which of these is a form of precipitation?", "Fog", "Dew", "Water vapour", "Rain", "D"),
        ("What happens when water freezes?", "Liquid water changes into solid ice", "Water vapour changes into liquid", "Ice changes into vapour directly", "Liquid water becomes oxygen", "A"),
        ("What is groundwater?", "Water floating in clouds", "Water stored beneath Earth's surface in soil and rock", "Water found only in oceans", "Water falling from clouds", "B"),
        ("Which process returns water vapour to the atmosphere from plant leaves?", "Collection", "Runoff", "Transpiration", "Precipitation", "C"),
        ("Which reservoir stores the largest share of Earth's water?", "Rivers", "Lakes", "Atmospheric clouds", "Oceans", "D"),
        ("What is a cloud mainly made of?", "Tiny water droplets and/or ice crystals", "Smoke only", "Pure oxygen", "Solid rock particles only", "A"),
        ("What can happen to rainwater after it reaches the ground?", "It all immediately becomes clouds", "It may run off, infiltrate the soil or evaporate", "It permanently disappears", "It always becomes ice", "B"),
        ("What is melting in the water cycle?", "Water vapour becoming liquid", "Liquid water becoming gas", "Solid ice changing into liquid water", "Water entering the ground", "C"),
        ("What is the term for ice changing directly into water vapour?", "Condensation", "Freezing", "Evaporation", "Sublimation", "D"),
        ("Which process causes liquid water to enter the atmosphere as vapour?", "Evaporation", "Precipitation", "Collection", "Infiltration", "A"),
        ("Why does rain often fall from clouds?", "Clouds become heavier than Earth", "Droplets or ice particles grow large enough to fall", "The Sun pulls clouds downward", "Wind turns clouds into liquid oceans", "B"),
        ("Which of these is a natural water reservoir?", "A metal spoon", "A plastic bag", "A lake", "A light bulb", "C"),
        ("What is the atmosphere's role in the water cycle?", "It stops all evaporation", "It stores all Earth's water", "It prevents clouds from forming", "It carries water vapour and clouds through the air", "D"),
        ("How does the Sun help water evaporate?", "It supplies heat energy", "It freezes ocean water", "It converts water into soil", "It removes gravity", "A"),
        ("Which process can replenish rivers and lakes directly?", "Transpiration only", "Precipitation", "Sublimation only", "Freezing only", "B"),
        ("What is dew?", "Rain falling from high clouds", "Water flowing underground", "Liquid water droplets formed on cool surfaces", "Snow falling from clouds", "C"),
        ("What is the water table?", "The top of a cloud", "The depth of the ocean only", "The height of a mountain", "The upper level of the saturated zone underground", "D"),
        ("Why is the water cycle important for living organisms?", "It helps distribute and renew available freshwater", "It removes all water from Earth", "It prevents plant growth", "It stops rivers from flowing", "A"),
        ("Which statement about Earth's water cycle is correct?", "It happens only during the rainy season", "Water continually changes state and moves between reservoirs", "Water is created from nothing each day", "It occurs only in oceans", "B"),
    ],
    "Medium": [
        ("Why does evaporation generally increase when temperature rises, if other conditions are similar?", "Water molecules stop moving", "The air becomes solid", "More water molecules have enough energy to escape into the vapour phase", "Condensation becomes impossible", "C"),
        ("What usually happens when moist air rises and cools to its dew point?", "All water immediately freezes", "The air loses all oxygen", "Evaporation stops forever", "Water vapour can condense into droplets", "D"),
        ("How do plants contribute to atmospheric moisture?", "Through transpiration", "By preventing evaporation everywhere", "By converting clouds into groundwater", "Through runoff alone", "A"),
        ("Which condition generally favours faster evaporation from an exposed water surface?", "Low temperature and still air", "Higher temperature and moving, relatively dry air", "A sealed container with no air exchange", "Freezing conditions", "B"),
        ("What is the difference between evaporation and boiling?", "Evaporation occurs only at 100°C", "Boiling occurs only at the water surface", "Evaporation occurs at the surface and can happen below boiling point; boiling occurs throughout the liquid", "They are exactly the same process", "C"),
        ("What role does condensation play in cloud formation?", "It turns clouds into groundwater directly", "It creates sunlight", "It makes all water freeze instantly", "It changes water vapour into tiny liquid droplets or ice crystals", "D"),
        ("How can forests influence the water cycle?", "They can increase transpiration and affect infiltration and runoff", "They eliminate all precipitation", "They prevent groundwater recharge in every case", "They stop the Sun from heating oceans", "A"),
        ("What is groundwater recharge?", "Water leaving the atmosphere", "Water entering underground aquifers", "Water changing into snow", "Water flowing from clouds into space", "B"),
        ("Why can paved urban areas increase surface runoff?", "Pavement absorbs more water than soil", "Pavement creates more groundwater", "Impervious surfaces reduce infiltration", "Pavement stops rainfall", "C"),
        ("What is an aquifer?", "A type of cloud", "A river flowing above ground", "A frozen ocean", "A permeable geological formation that stores and transmits groundwater", "D"),
        ("How does condensation release energy into the surroundings?", "Water vapour releases latent heat when it changes to liquid", "Liquid water absorbs no energy under any conditions", "Ice creates energy from nothing", "Condensation destroys heat", "A"),
        ("What is one effect of excessive groundwater extraction?", "A permanent increase in rainfall", "A falling water table and possible depletion of wells", "An immediate increase in all river levels", "The end of evaporation", "B"),
        ("How can wetlands affect the movement of water?", "They prevent all infiltration", "They turn water into minerals", "They can store water, slow runoff and support groundwater exchange", "They eliminate the water cycle", "C"),
        ("What is sublimation?", "Liquid changing into solid", "Gas changing into liquid", "Liquid changing into gas", "Solid ice changing directly into water vapour", "D"),
        ("What is deposition in the context of changes of state?", "Water vapour changing directly into ice", "Ice changing into liquid water", "Liquid water changing into vapour", "Rainwater entering soil", "A"),
        ("Why can warm air often contain more water vapour before becoming saturated than cold air?", "Warm air has no molecules", "The saturation vapour pressure of water increases with temperature", "Cold air cannot contain any water vapour", "Water vapour only forms at freezing temperatures", "B"),
        ("Which process moves water from land to rivers without requiring it to enter the atmosphere first?", "Condensation", "Transpiration", "Surface runoff", "Sublimation", "C"),
        ("What does relative humidity compare?", "Rainfall with river flow", "Air temperature with ocean depth", "Groundwater with surface water", "Actual water vapour content with the saturation amount at that temperature", "D"),
        ("How can mountain ranges influence precipitation?", "Rising air may cool, condense and produce orographic precipitation", "They stop all clouds permanently", "They prevent air from moving", "They convert all rain into groundwater instantly", "A"),
        ("What is a watershed or drainage basin?", "A reservoir used only for drinking", "An area of land whose water drains to a common outlet", "A cloud that produces snow", "A layer of impermeable metal", "B"),
        ("Why can deforestation increase the risk of flooding in some areas?", "Trees always prevent rainfall", "Tree roots create oceans", "Reduced interception and altered infiltration can increase rapid runoff", "Deforestation stops all rivers", "C"),
        ("How does water from melting snow enter the water cycle?", "It becomes a mineral", "It permanently leaves Earth", "It cannot enter rivers", "It can flow as runoff or infiltrate the ground", "D"),
        ("What is the main difference between a water cycle reservoir and a water cycle flux?", "A reservoir stores water; a flux is the movement of water between reservoirs", "A reservoir is always a cloud; a flux is always a river", "A reservoir measures temperature only", "A flux is a permanent storage location", "A"),
        ("How can a prolonged drought affect the water cycle locally?", "It guarantees higher groundwater levels", "It can reduce soil moisture, streamflow and groundwater recharge", "It stops the global water cycle", "It increases rainfall every day", "B"),
        ("What happens when air reaches saturation and cools further under suitable conditions?", "It loses all nitrogen", "Water vapour cannot condense", "Condensation may occur if suitable particles are present", "All cloud droplets become salt", "C"),
        ("Why is precipitation not always followed by immediate river flow?", "Rain cannot reach the ground", "Rivers only receive water from oceans", "Water cannot move through soil", "Some water infiltrates, is stored, evaporates or is used by organisms", "D"),
        ("How can dams affect the local water cycle?", "They can alter storage, evaporation and downstream flow", "They stop evaporation from the entire planet", "They remove all groundwater", "They prevent condensation in the atmosphere", "A"),
        ("What is the significance of the latent heat of vaporisation?", "It measures the colour of water", "It is the energy absorbed per unit mass during liquid-to-vapour change at a specified condition", "It is the weight of a cloud", "It is the speed of river water", "B"),
        ("Which human activity can reduce groundwater recharge?", "Protecting permeable open land", "Restoring wetlands", "Covering large areas with impermeable surfaces", "Collecting rainwater for infiltration", "C"),
        ("Why is the water cycle described as a system with multiple pathways?", "All water follows the same route at the same speed", "Only oceans participate", "Water never enters living organisms", "Water can move through evaporation, transpiration, runoff, infiltration and other processes", "D"),
    ],
    "Hard": [
        ("If the air temperature rises while actual water vapour content stays constant, what generally happens to relative humidity?", "It decreases because saturation vapour pressure increases", "It always becomes 100%", "It increases without limit", "It remains exactly 100%", "A"),
        ("Which statement best describes the global water cycle's water balance over a sufficiently long period?", "All water must remain in the atmosphere", "Total evaporation and precipitation are approximately balanced globally over long periods", "Precipitation is always greater than evaporation over the entire ocean-land system", "Groundwater never exchanges with surface water", "B"),
        ("Why can intense rainfall on dry, compacted soil produce substantial runoff?", "Dry soil always absorbs unlimited water", "Rainfall cannot interact with soil", "Infiltration capacity may be lower than the rainfall intensity", "Evaporation immediately removes all rain", "C"),
        ("What is the likely effect of increasing vegetation cover on a degraded catchment, if other factors are comparable?", "It guarantees no rainfall", "It eliminates groundwater", "It makes every storm more severe", "It may increase interception and infiltration while reducing rapid runoff", "D"),
        ("A water body loses 120 mm of water by evaporation in a month and receives 80 mm of precipitation. Ignoring other exchanges, what is its net change in water depth?", "A decrease of 40 mm", "An increase of 40 mm", "An increase of 200 mm", "No change", "A"),
        ("What is the main reason clouds form when moist air rises over a mountain?", "Air pressure always increases upward", "Rising air expands and cools, potentially reaching saturation", "Mountains create water from rocks", "The Sun stops heating the atmosphere", "B"),
        ("Why can groundwater contamination persist for a long time?", "Groundwater always moves faster than sound", "All pollutants are removed instantly", "Groundwater may move slowly, and some contaminants can persist or be released from aquifer materials", "Aquifers contain no water", "C"),
        ("Which statement about the residence time of water in reservoirs is correct?", "All water remains in every reservoir for exactly one year", "Ocean water never leaves the ocean", "Groundwater always has a shorter residence time than atmospheric water", "Residence time varies greatly; atmospheric water is usually much shorter-lived than deep groundwater", "D"),
        ("How can warming influence the atmosphere's potential to hold water vapour?", "It increases saturation vapour pressure, allowing more water vapour when moisture is available", "It makes evaporation physically impossible", "It prevents condensation at every temperature", "It stops all precipitation globally", "A"),
        ("Why does condensation commonly occur on tiny aerosol particles in the atmosphere?", "Aerosols destroy all water molecules", "They can provide surfaces on which water droplets form", "They turn water directly into rock", "They remove gravity", "B"),
        ("What does a hydrograph typically show?", "The mineral content of a rock", "The temperature of the Sun", "Stream discharge or river flow over time", "The age of a galaxy", "C"),
        ("A watershed receives 500 mm of precipitation. Over the period, 150 mm is lost through evapotranspiration and 250 mm leaves as streamflow. Ignoring storage change and other exchanges, what is the remaining amount?", "100 mm", "250 mm", "500 mm", "600 mm", "A"),
        ("Why is the water cycle important in regulating Earth's climate?", "Water never absorbs heat", "Phase changes and water transport redistribute energy through the atmosphere and surface", "It prevents any temperature variation", "It stops all sunlight from reaching Earth", "B"),
        ("What can happen to the water table during prolonged pumping from a well that exceeds local recharge?", "It must rise indefinitely", "It becomes the cloud base", "It can decline, potentially creating a cone of depression around the well", "It immediately turns into surface runoff", "C"),
        ("What is capillary rise in soil?", "Water vapour escaping from clouds", "The movement of rain through rivers only", "The direct freezing of groundwater", "Upward movement of water through small pores due to capillary forces", "D"),
        ("Why can irrigation increase local evaporation and transpiration?", "It supplies additional water to soil and plants", "It stops plant growth", "It removes all solar energy", "It prevents water from changing state", "A"),
        ("Which combination most directly favours fog formation near the ground?", "Very dry air warming rapidly", "Air near the surface cooling to its dew point with sufficient moisture", "A complete absence of water vapour", "Extremely hot rock melting into clouds", "B"),
        ("How can urban stormwater harvesting help manage the water cycle?", "By stopping all precipitation", "By converting runoff into sunlight", "By collecting runoff for use or infiltration, reducing some drainage pressure", "By preventing all groundwater recharge", "C"),
        ("Which statement about water in the atmosphere is correct?", "All atmospheric water exists as visible clouds", "Water vapour is the same as liquid rain", "Atmospheric water never condenses", "Water can be present as invisible vapour as well as droplets and ice crystals", "D"),
        ("Why can a warmer climate intensify some heavy precipitation events?", "Warmer air can hold more water vapour, which can provide more moisture for precipitation when conditions support it", "Warm air always produces no clouds", "Rainfall depends only on the Moon", "Water vapour disappears as temperature rises", "A"),
        ("What is the difference between infiltration and percolation?", "They both mean only cloud formation", "Infiltration is water entering the soil; percolation is its movement through soil or rock", "Infiltration is evaporation from leaves", "Percolation is rain falling from clouds", "B"),
        ("Why can groundwater discharge help sustain streams during dry weather?", "Groundwater cannot interact with rivers", "Streams receive water only during storms", "Groundwater can slowly flow into streams as baseflow", "Dry weather immediately removes all groundwater", "C"),
        ("What does evapotranspiration combine?", "Precipitation and snowmelt only", "Runoff and erosion only", "Condensation and freezing only", "Evaporation from surfaces and transpiration from plants", "D"),
        ("A catchment has precipitation of 900 mm, evapotranspiration of 550 mm and runoff of 300 mm. If other exchanges are ignored, what is the change in storage?", "An increase of 50 mm", "A decrease of 50 mm", "An increase of 300 mm", "No change", "A"),
        ("How can a permeable surface help reduce flash-flood risk compared with an impermeable surface?", "It makes rainfall stop", "It allows more water to infiltrate and can reduce rapid surface runoff", "It increases runoff in every case", "It prevents water from entering soil", "B"),
        ("Why can snowpack be considered a seasonal water reservoir?", "Snow is never converted into liquid", "Snow cannot influence river flow", "It stores precipitation and may release water during melting", "It exists only in the atmosphere", "C"),
        ("Which change is most likely to reduce recharge to an unconfined aquifer in a developed area?", "Restoring wetlands", "Using permeable paving", "Protecting vegetated infiltration zones", "Increasing impermeable cover and diverting runoff away from infiltration areas", "D"),
        ("Why does the global water cycle not mean that every region receives the same amount of freshwater?", "Water transport, atmospheric circulation, geography and local climate differ", "All regions have identical rainfall", "The oceans contain no water", "Groundwater is distributed uniformly everywhere", "A"),
        ("What is one potential consequence of melting glaciers for downstream water availability?", "River flow must increase forever", "Runoff may increase initially, but long-term meltwater contributions can decline as ice reserves shrink", "Glaciers do not store water", "Melting glaciers stop the water cycle", "B"),
        ("Which statement best explains why conserving freshwater is important even though Earth continually recycles water?", "The water cycle creates unlimited clean water instantly", "All Earth's water is safe to drink", "Usable freshwater is unevenly distributed and can be polluted or depleted faster than it is replenished locally", "Freshwater never enters the oceans", "C"),
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
                (quiz_id, question, option_a, option_b, option_c, option_d, correct_answer)
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
        print(f"\nSuccess! Added {total_added} questions to '{LESSON_TITLE}'.")
        print("Other lessons and Social Science were not modified.")

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    main()
