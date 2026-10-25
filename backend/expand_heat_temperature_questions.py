
import sqlite3
from pathlib import Path
import re

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

LESSON_TITLE = "Heat and Temperature"
TARGET_QUESTIONS = 30

QUESTIONS = {
    "Easy": [
        ("What is heat?",
         "A form of energy transferred because of a temperature difference",
         "The amount of matter in an object",
         "The space occupied by an object",
         "The force acting on an object", "A"),
        ("What does a thermometer measure?",
         "Mass", "Temperature", "Volume", "Density", "B"),
        ("Which is the SI unit of temperature?",
         "Celsius", "Fahrenheit", "Kelvin", "Joule", "C"),
        ("Which instrument is commonly used to measure body temperature?",
         "Barometer", "Ammeter", "Speedometer", "Clinical thermometer", "D"),
        ("Which material is generally a good conductor of heat?",
         "Copper", "Wood", "Rubber", "Plastic", "A"),
        ("Which material is generally a poor conductor of heat?",
         "Iron", "Wood", "Aluminium", "Copper", "B"),
        ("Heat normally flows spontaneously from:",
         "A colder object to a hotter object", "A smaller object to a larger object",
         "A hotter object to a colder object", "A heavier object to a lighter object", "C"),
        ("What is the usual unit of heat energy?",
         "Metre", "Kelvin", "Kilogram", "Joule", "D"),
        ("Which of these is a source of natural heat and light for Earth?",
         "The Sun", "The Moon", "A mirror", "A thermometer", "A"),
        ("What happens to most substances when heated?",
         "They always shrink", "They generally expand", "Their mass doubles",
         "They stop containing particles", "B"),
        ("Which method of heat transfer can occur through a vacuum?",
         "Conduction", "Convection", "Radiation", "None of these", "C"),
        ("Which method of heat transfer mainly occurs through direct particle interactions in solids?",
         "Radiation", "Evaporation", "Convection", "Conduction", "D"),
        ("Which method of heat transfer occurs through the movement of fluids?",
         "Convection", "Conduction only", "Reflection", "Condensation", "A"),
        ("Which colour generally absorbs more radiant heat?",
         "White", "Black", "Silver", "Pale yellow", "B"),
        ("Which colour generally reflects more radiant heat?",
         "Black", "Dark blue", "White", "Dark brown", "C"),
        ("What happens to the temperature of melting pure ice at normal atmospheric pressure while it melts?",
         "It rises continuously", "It falls continuously", "It becomes 100°C",
         "It remains approximately constant until melting is complete", "D"),
        ("Which state of matter usually expands to fill its container?",
         "Gas", "Solid", "Only crystalline solids", "None of these", "A"),
        ("What is temperature a measure of in an introductory particle model?",
         "The total mass of an object", "How hot or cold something is, related to average particle kinetic energy",
         "The object's colour", "The number of objects present", "B"),
        ("Which of these is commonly used as a thermal insulator?",
         "Copper", "Aluminium", "Wool", "Iron", "C"),
        ("Why are cooking-pan handles often made from materials such as wood or heat-resistant plastic?",
         "They produce heat rapidly", "They increase the boiling point of food",
         "They are always magnetic", "They reduce heat transfer to the hand", "D"),
        ("Which temperature is approximately equal to 0°C?",
         "273 K", "100 K", "373 K", "0 K", "A"),
        ("Which temperature is approximately equal to 100°C?",
         "273 K", "373 K", "100 K", "0 K", "B"),
        ("What is the freezing point of pure water at normal atmospheric pressure?",
         "100°C", "50°C", "0°C", "−100°C", "C"),
        ("What is the boiling point of pure water at normal atmospheric pressure?",
         "0°C", "50°C", "75°C", "100°C", "D"),
        ("Which process transfers heat from the Sun to Earth?",
         "Radiation", "Conduction through air alone", "Convection through space",
         "Direct contact", "A"),
        ("Why do metal spoons become hot when left in hot soup?",
         "The spoon creates energy from nothing", "Heat is conducted through the metal",
         "The spoon stops all heat transfer", "The soup becomes a solid", "B"),
        ("What is thermal expansion?",
         "A decrease in temperature only", "A change in colour caused by light",
         "An increase in dimensions due to heating", "A change in mass caused by gravity", "C"),
        ("Which device is designed to reduce unwanted heat transfer?",
         "A bare metal plate", "A blackened steel rod", "An uncovered hot pan",
         "A thermos flask", "D"),
        ("What is the normal freezing point of water on the Celsius scale?",
         "0°C", "32°C", "100°C", "273°C", "A"),
        ("Which statement is correct?",
         "Heat and temperature mean exactly the same thing",
         "Heat is energy transferred due to a temperature difference",
         "Temperature is measured in joules",
         "Heat always flows from cold to hot spontaneously", "B"),
    ],

    "Medium": [
        ("Convert 27°C to kelvin using K = °C + 273.",
         "246 K", "273 K", "300 K", "310 K", "C"),
        ("Convert 300 K to degrees Celsius using °C = K − 273.",
         "27°C", "300°C", "573°C", "−27°C", "A"),
        ("Which statement best distinguishes heat from temperature?",
         "Heat and temperature are both measured only in kilograms",
         "Temperature is energy transferred, while heat is the degree of hotness",
         "Heat and temperature always have identical numerical values",
         "Heat is energy transferred, while temperature indicates thermal state", "D"),
        ("Why does a metal chair often feel colder than a wooden chair in the same room?",
         "The metal is always at a lower temperature",
         "Metal conducts heat away from the skin faster",
         "Wood has no temperature",
         "Metal contains no particles", "B"),
        ("Why does warm air usually rise?",
         "It becomes heavier", "It loses all its energy",
         "It expands and becomes less dense than surrounding cooler air",
         "It turns into a solid", "C"),
        ("Which is an example of convection?",
         "Heat moving along a metal rod", "Sunlight warming the ground",
         "A spoon warming in tea", "Circulation of water while it is heated in a pot", "D"),
        ("Which is an example of conduction?",
         "Heat travelling along a metal rod", "Sea breezes caused by air circulation",
         "Sunlight reaching Earth", "Warm air rising in a room", "A"),
        ("Which is an example of radiation?",
         "Heat moving through a metal spoon", "Feeling warmth from a fire without touching it",
         "Water circulating in a heated pan", "Warm air moving upwards", "B"),
        ("Why are gaps sometimes left between railway tracks or bridge sections?",
         "To reduce their mass", "To make them magnetic",
         "To allow expansion in hot weather", "To prevent all heat transfer", "C"),
        ("Why can water remain at its boiling temperature while continuing to boil at constant pressure?",
         "It stops absorbing energy", "Its particles stop moving",
         "Its mass becomes zero", "Energy is used for the change of state", "D"),
        ("Which statement about evaporation is correct?",
         "It can occur at the surface of a liquid below its boiling point",
         "It occurs only at the boiling point", "It occurs only in solids",
         "It always requires the liquid to freeze first", "A"),
        ("Why does evaporation generally cause cooling?",
         "The liquid gains all the energy from its surroundings",
         "Higher-energy particles escape, reducing the average energy of those remaining",
         "The liquid's mass increases", "The surrounding air stops moving", "B"),
        ("Which factor generally increases the rate of evaporation?",
         "Higher humidity", "Smaller exposed surface area",
         "Higher temperature", "Still air in every situation", "C"),
        ("Why are light-coloured clothes often preferred in hot sunny weather?",
         "They absorb all incident radiation", "They generate cold energy",
         "They prevent sweat from evaporating completely",
         "They generally reflect more solar radiation than dark clothes", "D"),
        ("Which surface is generally a good emitter of thermal radiation?",
         "A dull black surface", "A shiny silver surface", "A polished mirror",
         "A highly reflective white surface in all conditions", "A"),
        ("Why does a vacuum layer in a thermos flask reduce heat transfer?",
         "It increases convection", "It greatly reduces conduction and prevents convection across the vacuum",
         "It creates a continuous solid path", "It makes the liquid lose all energy", "B"),
        ("A 2 kg object receives 4,000 J of heat. What is the heat received per kilogram?",
         "500 J/kg", "1,000 J/kg", "2,000 J/kg", "8,000 J/kg", "C"),
        ("What is the SI unit of specific heat capacity?",
         "J", "K", "W", "J/(kg·K)", "D"),
        ("Which material usually has a higher specific heat capacity: water or copper?",
         "Water", "Copper", "They are always equal", "Neither has specific heat capacity", "A"),
        ("Why are coastal areas often cooler during the day than inland areas?",
         "Sea water has no heat capacity", "Water has a relatively high specific heat capacity and warms more slowly",
         "Land cannot absorb sunlight", "Air near the sea contains no energy", "B"),
        ("What happens to the average kinetic energy of particles when a substance is heated without a phase change?",
         "It always becomes zero", "It never changes",
         "It generally increases", "It becomes negative", "C"),
        ("Which statement about the Celsius and Kelvin scales is correct?",
         "Kelvin values are always smaller than Celsius values",
         "0 K equals 0°C", "A temperature difference of 1 K is larger than 1°C",
         "A temperature difference of 1 K equals a difference of 1°C", "D"),
        ("Why does a liquid-in-glass thermometer work?",
         "The liquid expands and contracts with temperature changes",
         "The glass creates new liquid when heated", "The liquid becomes magnetic",
         "The thermometer measures mass directly", "A"),
        ("What is the approximate Celsius equivalent of 310 K?",
         "310°C", "37°C", "583°C", "−37°C", "B"),
        ("Which transfer method is most important in moving heat through the vacuum of space?",
         "Conduction", "Convection", "Radiation", "Direct contact", "C"),
        ("Why is air trapped in woollen clothing useful in cold weather?",
         "Air is an excellent conductor", "Air produces heat continuously",
         "Air increases the body's mass", "Trapped air reduces heat loss because it is a poor conductor and limits convection", "D"),
        ("Which process explains the formation of convection currents in a heated liquid?",
         "Warmer, less-dense liquid rises while cooler, denser liquid sinks",
         "All liquid particles stop moving", "The liquid becomes uniformly solid",
         "Heat travels only by radiation", "A"),
        ("What happens to most metals when heated, assuming no phase change?",
         "They always shrink", "They expand",
         "They lose all their mass", "They become non-metallic elements", "B"),
        ("Which instrument measures atmospheric pressure rather than temperature?",
         "Thermometer", "Calorimeter", "Barometer", "Thermostat", "C"),
        ("What is the role of a thermostat in a temperature-controlled system?",
         "To measure mass", "To remove all thermal energy",
         "To convert temperature into length only",
         "To regulate a system around a set temperature", "D"),
    ],

    "Hard": [
        ("A temperature rises from 20°C to 45°C. What is the temperature increase in kelvin?",
         "25 K", "45 K", "293 K", "318 K", "A"),
        ("A substance has a mass of 2 kg and specific heat capacity of 500 J/(kg·K). How much energy is needed to raise its temperature by 10 K, ignoring losses?",
         "1,000 J", "10,000 J", "5,000 J", "25,000 J", "B"),
        ("How much energy is required to raise the temperature of 0.5 kg of water by 4°C? Use c = 4,200 J/(kg·°C).",
         "2,100 J", "4,200 J", "8,400 J", "16,800 J", "C"),
        ("Two objects of equal mass receive equal amounts of heat. Object X has a lower specific heat capacity than object Y. Assuming no phase changes or losses, which warms more?",
         "Object Y", "Both warm by the same amount in all cases",
         "Neither warms", "Object X", "D"),
        ("A 1 kg substance with specific heat capacity 400 J/(kg·K) absorbs 2,000 J. What is its temperature increase?",
         "5 K", "2 K", "8 K", "20 K", "A"),
        ("Which equation calculates heat energy for a temperature change when no phase change occurs?",
         "Q = m/cΔT", "Q = mcΔT", "Q = m + c + ΔT", "Q = c/(mΔT)", "B"),
        ("A 0.2 kg sample with specific heat capacity 900 J/(kg·K) cools by 10 K. How much heat does it release in magnitude?",
         "180 J", "900 J", "1,800 J", "18,000 J", "C"),
        ("Why can a black surface cool by radiation more effectively than a shiny surface under otherwise similar conditions?",
         "Black surfaces contain no energy", "Shiny surfaces cannot have a temperature",
         "Black surfaces always have lower mass",
         "Dull black surfaces are generally better emitters of thermal radiation", "D"),
        ("Why does a metal pan heat quickly but water inside it may take longer to warm?",
         "Metal generally has a lower specific heat capacity than water",
         "Water cannot absorb heat", "Metal has no particles",
         "Water is always a perfect insulator", "A"),
        ("During the melting of a pure substance at constant pressure, what happens to the supplied energy?",
         "It always raises temperature rapidly", "It is used to change state while temperature remains approximately constant",
         "It destroys the particles", "It changes the atomic number", "B"),
        ("What is latent heat?",
         "Heat needed only to increase mass", "Heat transferred only by conduction",
         "Energy transferred during a change of state without a temperature change in the idealised phase-change process",
         "The temperature of a vacuum", "C"),
        ("Why does steam at 100°C often cause more severe burns than water at 100°C?",
         "Steam has no energy", "Water at 100°C is always frozen",
         "Steam cannot condense on skin", "Steam releases additional latent heat when it condenses", "D"),
        ("Which statement about thermal equilibrium is correct?",
         "Objects in thermal equilibrium have the same temperature and no net heat flows between them",
         "Objects must have equal masses", "Both objects must be made of the same material",
         "One object must be at absolute zero", "A"),
        ("A metal rod is heated at one end. Which process transfers energy along the rod most directly?",
         "Convection", "Conduction", "Evaporation", "Condensation", "B"),
        ("Why can convection occur in liquids and gases but not in a rigid solid in the usual bulk-flow sense?",
         "Liquids and gases contain no particles", "Solids cannot transfer heat at all",
         "Fluids can flow and carry thermal energy with their bulk motion",
         "Convection requires a vacuum", "C"),
        ("Which statement about absolute zero is correct?",
         "It is 0°C", "It is 100 K", "It is the boiling point of water",
         "It is 0 K, approximately −273.15°C", "D"),
        ("A temperature is 68°F. What is its Celsius equivalent using C = (F − 32) × 5/9?",
         "20°C", "36°C", "68°C", "100°C", "A"),
        ("A temperature is 25°C. What is its Fahrenheit equivalent using F = (9/5)C + 32?",
         "25°F", "77°F", "57°F", "45°F", "B"),
        ("Why is the inside of a greenhouse warmed by sunlight?",
         "The glass creates heat from nothing", "Sunlight cannot pass through glass",
         "Solar radiation enters, and the greenhouse reduces some heat loss and alters heat exchange with the surroundings",
         "Convection in outer space heats the greenhouse", "C"),
        ("A 3 kg object with specific heat capacity 200 J/(kg·K) warms by 5 K. How much heat does it absorb?",
         "200 J", "600 J", "1,000 J", "3,000 J", "D"),
        ("Which statement about heat capacity and specific heat capacity is correct?",
         "Heat capacity applies to an entire object, while specific heat capacity is per unit mass",
         "They are always measured in kilograms", "Specific heat capacity is independent of mass by definition but has unit joules",
         "Heat capacity and temperature are identical", "A"),
        ("Why does a thermometer need to reach thermal equilibrium with an object for a reliable reading?",
         "To make the object's mass increase",
         "So the thermometer's temperature matches the object's temperature",
         "To cause the object to change chemical identity",
         "To stop all particle motion", "B"),
        ("A 0.4 kg object absorbs 3,600 J and warms by 20 K. What is its specific heat capacity?",
         "180 J/(kg·K)", "360 J/(kg·K)", "450 J/(kg·K)", "900 J/(kg·K)", "D"),
        ("Which combination reduces heat transfer through a building wall most effectively?",
         "Use a thick layer of good thermal insulation",
         "Use a thin layer of highly conductive metal only",
         "Increase air leakage", "Remove all insulating materials", "A"),
        ("Why does sweating cool the human body?",
         "Sweat releases heat when it freezes on the skin in all conditions",
         "Evaporation of sweat requires energy taken from the skin",
         "Sweat blocks all radiation", "Sweat raises the skin's mass indefinitely", "B"),
        ("Which change generally increases heat transfer by conduction through a flat slab, all else equal?",
         "Increasing slab thickness", "Reducing the temperature difference",
         "Increasing the thermal conductivity of the material",
         "Reducing the cross-sectional area", "C"),
        ("Why are shiny, reflective surfaces used in some thermal insulation designs?",
         "They increase convection through the vacuum",
         "They absorb all incident radiation",
         "They increase the object's specific heat capacity",
         "They reduce the absorption and emission of radiant heat compared with dull black surfaces", "D"),
        ("A 2 kg object cools from 80°C to 30°C. Its specific heat capacity is 400 J/(kg·K). How much heat does it release in magnitude?",
         "40,000 J", "20,000 J", "4,000 J", "100,000 J", "A"),
        ("Which statement best explains why water is used in many central heating systems?",
         "It has no mass", "It has a relatively high specific heat capacity and can transport substantial thermal energy",
         "It cannot expand when heated", "It never changes temperature", "B"),
        ("A 1.5 kg sample with specific heat capacity 800 J/(kg·K) absorbs 12,000 J. What is its temperature increase?",
         "5 K", "8 K", "10 K", "15 K", "C"),
    ],
}


def normalize(text):
    return re.sub(r"\s+", " ", text.strip().lower())


def main():
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DATABASE_PATH}")

    conn = sqlite3.connect(DATABASE_PATH)
    try:
        cur = conn.cursor()

        cur.execute(
            "SELECT id FROM lessons WHERE LOWER(TRIM(title)) = LOWER(TRIM(?))",
            (LESSON_TITLE,),
        )
        lesson_rows = cur.fetchall()

        if len(lesson_rows) != 1:
            raise RuntimeError(
                f"Expected exactly one lesson titled '{LESSON_TITLE}', "
                f"but found {len(lesson_rows)}."
            )

        lesson_id = lesson_rows[0][0]
        inserted_total = 0

        for difficulty, question_bank in QUESTIONS.items():
            cur.execute(
                """
                SELECT id FROM quizzes
                WHERE lesson_id = ? AND LOWER(TRIM(difficulty)) = LOWER(TRIM(?))
                """,
                (lesson_id, difficulty),
            )
            quiz_rows = cur.fetchall()

            if len(quiz_rows) != 1:
                raise RuntimeError(
                    f"Expected exactly one {difficulty} quiz for "
                    f"'{LESSON_TITLE}', but found {len(quiz_rows)}."
                )

            quiz_id = quiz_rows[0][0]

            cur.execute(
                "SELECT question FROM questions WHERE quiz_id = ?",
                (quiz_id,),
            )
            existing = {normalize(row[0]) for row in cur.fetchall()}

            cur.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                (quiz_id,),
            )
            current_count = cur.fetchone()[0]
            needed = max(0, TARGET_QUESTIONS - current_count)

            added = 0
            for item in question_bank:
                question, a, b, c, d, answer = item
                key = normalize(question)

                if key in existing:
                    continue

                if answer not in {"A", "B", "C", "D"}:
                    raise ValueError(f"Invalid answer key for: {question}")

                if added >= needed:
                    break

                cur.execute(
                    """
                    INSERT INTO questions
                    (quiz_id, question, option_a, option_b, option_c,
                     option_d, correct_answer)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (quiz_id, question, a, b, c, d, answer),
                )

                existing.add(key)
                added += 1

            cur.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                (quiz_id,),
            )
            final_count = cur.fetchone()[0]

            if final_count < TARGET_QUESTIONS:
                raise RuntimeError(
                    f"{difficulty} has only {final_count} questions after "
                    f"expansion. Add more unique questions to the bank."
                )

            inserted_total += added
            print(
                f"{difficulty}: started with {current_count}, "
                f"added {added}, final total {final_count}"
            )

        conn.commit()
        print(f"\nSuccess! Added {inserted_total} questions to '{LESSON_TITLE}'.")
        print("Each difficulty now has at least 30 questions.")
        print("Other lessons and Social Science were not modified.")

    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
