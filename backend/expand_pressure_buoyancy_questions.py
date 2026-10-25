
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"
LESSON_TITLE = "Pressure and Buoyancy"
TARGET_QUESTIONS = 30

QUESTIONS = {
    "Easy": [
        ("What is the SI unit of pressure?", "Newton", "Pascal", "Joule", "Watt", "B"),
        ("How is pressure calculated?", "Force multiplied by area", "Area divided by force", "Force divided by area", "Mass multiplied by volume", "C"),
        ("What is the SI unit of force?", "Newton", "Pascal", "Kilogram", "Metre", "A"),
        ("What is buoyancy?", "The force that always pulls objects downward", "The force that stops all motion", "The pressure inside a solid", "The upward force exerted by a fluid on an immersed object", "D"),
        ("Which instrument measures atmospheric pressure?", "Thermometer", "Barometer", "Ammeter", "Speedometer", "B"),
        ("Why does a sharp knife cut more easily than a blunt knife when the same force is applied?", "It has a larger contact area", "It has no friction", "Its smaller contact area produces greater pressure", "It removes gravity", "C"),
        ("What happens to liquid pressure as depth increases?", "It increases", "It decreases to zero", "It remains constant in all circumstances", "It becomes negative", "A"),
        ("Which object is most likely to float in water?", "A solid iron block", "A stone", "A piece of dense metal", "A piece of dry wood", "D"),
        ("What is the SI unit of density?", "kg/m", "kg/m³", "N/m", "Pa/m", "B"),
        ("What is the approximate atmospheric pressure at sea level?", "100 Pa", "1000 Pa", "101,325 Pa", "1 Pa", "C"),
        ("What is the formula for density?", "Mass divided by volume", "Volume divided by mass", "Force divided by area", "Mass multiplied by volume", "A"),
        ("Which force helps a boat float on water?", "Friction only", "Magnetic force", "Electrostatic force", "Buoyant force", "D"),
        ("Why are broad shoulder straps more comfortable when carrying a heavy bag?", "They increase the bag's weight", "They reduce pressure by spreading the force over a larger area", "They increase gravity", "They eliminate the load", "B"),
        ("In which direction does buoyant force act on an immersed object?", "Downward", "Horizontally only", "Upward", "In the direction of motion only", "C"),
        ("What is the pressure exerted by a force of 20 N on an area of 4 m²?", "5 Pa", "80 Pa", "24 Pa", "0.2 Pa", "A"),
        ("Which property mainly determines whether an object floats in a fluid?", "Its colour", "Its shape alone", "Its temperature alone", "Its average density compared with the fluid's density", "D"),
        ("What happens to atmospheric pressure as altitude increases?", "It always doubles", "It generally decreases", "It remains exactly constant", "It becomes infinite", "B"),
        ("Which of these is a fluid?", "Glass only", "Iron only", "Water", "Wood only", "C"),
        ("What causes liquid pressure at a point below the surface?", "The weight of the liquid above that point", "Only the colour of the liquid", "The container's temperature alone", "The absence of gravity", "A"),
        ("What is the pressure due to a 100 N force acting over 2 m²?", "200 Pa", "50 Pa", "102 Pa", "0.02 Pa", "B"),
        ("What happens to an object that is less dense than the fluid in which it is placed, assuming it can reach equilibrium at the surface?", "It must sink completely", "It disappears", "It always remains fully submerged", "It tends to float", "D"),
        ("Which principle explains why a liquid exerts pressure in all directions?", "Newton's law of cooling", "Reflection of light", "Fluid pressure acts in all directions", "Conservation of charge", "C"),
        ("What is the buoyant force on an object equal to, according to Archimedes' principle?", "The weight of fluid displaced", "The object's volume in kilograms", "The atmospheric pressure only", "The object's temperature", "A"),
        ("Which change increases pressure when the applied force remains constant?", "Increasing the area", "Reducing the area", "Removing the force", "Increasing the object's colour", "B"),
        ("Why can a large steel ship float even though steel is denser than water?", "Steel has no mass when in a ship", "Water does not exert an upward force", "The ship's average density, including the air-filled hull, can be less than water's density", "Gravity does not act on ships", "C"),
        ("Which quantity is measured in pascals?", "Mass", "Volume", "Energy", "Pressure", "D"),
        ("What happens to the buoyant force when the volume of fluid displaced increases in the same fluid?", "It generally increases", "It always becomes zero", "It decreases to zero", "It is unaffected in every case", "A"),
        ("What is the weight of a 2 kg object on Earth if g = 10 m/s²?", "2 N", "20 N", "12 N", "200 N", "B"),
        ("Which statement about pressure in a liquid at rest is correct?", "It depends only on the container's colour", "It is always zero below the surface", "It generally increases with depth", "It acts only downward", "C"),
        ("Why does a life jacket help a person float?", "It increases the person's mass greatly", "It removes gravity", "It stops water from exerting pressure", "It increases displaced water volume and helps reduce average density", "D"),
    ],

    "Medium": [
        ("A force of 120 N acts on an area of 3 m². What pressure is produced?", "40 Pa", "360 Pa", "123 Pa", "0.025 Pa", "A"),
        ("A pressure of 500 Pa acts on an area of 2 m². What force is exerted?", "250 N", "1000 N", "502 N", "100 N", "B"),
        ("A 600 N person stands on an area of 0.03 m². What pressure is exerted?", "18 Pa", "200 Pa", "20,000 Pa", "600.03 Pa", "C"),
        ("A liquid has density 1000 kg/m³. Taking g = 10 m/s², what is the gauge pressure 2 m below its surface?", "2000 Pa", "5000 Pa", "10,000 Pa", "20,000 Pa", "D"),
        ("An object displaces 0.02 m³ of water. Taking water density as 1000 kg/m³ and g = 10 m/s², what is the buoyant force?", "200 N", "20 N", "2 N", "2000 N", "A"),
        ("An object weighs 50 N in air and experiences a buoyant force of 15 N in water. What is its apparent weight in water?", "65 N", "35 N", "15 N", "50 N", "B"),
        ("A block has mass 4 kg and volume 0.002 m³. What is its average density?", "200 kg/m³", "500 kg/m³", "2000 kg/m³", "8000 kg/m³", "C"),
        ("A pressure of 2000 Pa acts on a surface of area 0.5 m². What is the force?", "1000 N", "4000 N", "2000.5 N", "400 N", "A"),
        ("A body floats at rest in water. What is the relationship between its weight and the buoyant force?", "Weight is always twice the buoyant force", "Buoyant force is zero", "Weight is greater than buoyant force", "They are equal", "D"),
        ("What is the gauge pressure 5 m below the surface of water if density is 1000 kg/m³ and g = 9.8 m/s²?", "4900 Pa", "49,000 Pa", "9800 Pa", "50,000 Pa", "B"),
        ("A force of 80 N acts on an area of 0.2 m². What is the pressure?", "16 Pa", "40 Pa", "400 Pa", "800 Pa", "C"),
        ("A body displaces 0.005 m³ of a liquid of density 800 kg/m³. Taking g = 10 m/s², what is the buoyant force?", "40 N", "4 N", "400 N", "0.4 N", "B"),
        ("An object weighs 100 N in air and 70 N when fully immersed in water. What is the buoyant force?", "170 N", "70 N", "30 N", "100 N", "C"),
        ("A liquid has density 1200 kg/m³. What is the gauge pressure at a depth of 3 m if g = 10 m/s²?", "3600 Pa", "12,000 Pa", "24,000 Pa", "36,000 Pa", "D"),
        ("An object has mass 600 g and volume 200 cm³. What is its density?", "3 g/cm³", "0.33 g/cm³", "120 g/cm³", "800 g/cm³", "A"),
        ("A force of 150 N acts over an area of 0.5 m². What is the pressure?", "75 Pa", "300 Pa", "150.5 Pa", "3 Pa", "B"),
        ("A block floats with 60% of its volume submerged in water. What is the block's average density?", "6000 kg/m³", "1000 kg/m³", "600 kg/m³", "400 kg/m³", "C"),
        ("A fully immersed object displaces 0.01 m³ of water. Taking water density as 1000 kg/m³ and g = 9.8 m/s², what buoyant force acts on it?", "98 N", "9.8 N", "100 N", "0.98 N", "A"),
        ("Why does liquid pressure at the same depth generally not depend on the shape of the container?", "It depends only on the container's colour", "It is zero in a narrow container", "It depends only on surface area", "It depends on depth, fluid density, and gravitational acceleration", "D"),
        ("An object has a weight of 40 N and experiences a buoyant force of 50 N while fully immersed. What will it tend to do when released?", "Sink", "Rise toward the surface", "Remain suspended without acceleration", "Lose all its mass", "B"),
        ("A hydraulic press has a small piston area of 0.01 m² and a large piston area of 0.5 m². If 20 N is applied to the small piston, what ideal force acts on the large piston?", "20 N", "100 N", "1000 N", "500 N", "C"),
        ("A liquid exerts gauge pressure of 15,000 Pa at a depth of 1.5 m. Taking g = 10 m/s², what is its density?", "1000 kg/m³", "500 kg/m³", "1500 kg/m³", "2000 kg/m³", "A"),
        ("A block of volume 0.004 m³ is fully immersed in oil of density 800 kg/m³. Taking g = 10 m/s², what is the buoyant force?", "3.2 N", "32 N", "320 N", "800 N", "B"),
        ("A body weighs 80 N in air and 60 N in a liquid. What is the magnitude of the buoyant force?", "140 N", "80 N", "60 N", "20 N", "D"),
        ("A 5 kg object has a volume of 0.004 m³. Is it likely to float in water of density 1000 kg/m³?", "Yes, because its density is 500 kg/m³", "Yes, because all objects float", "No, because its density is 1250 kg/m³", "No, because water has no buoyancy", "C"),
        ("The same force acts on two surfaces. Surface X has area 2 m² and surface Y has area 0.5 m². How does pressure on Y compare with pressure on X?", "Four times as large", "Half as large", "One-fourth as large", "Equal", "A"),
        ("A hydraulic system has piston areas of 0.02 m² and 0.4 m². What output force is produced by an input force of 50 N ideally?", "100 N", "1000 N", "500 N", "2000 N", "B"),
        ("A body displaces 0.003 m³ of water. Taking g = 10 m/s², what weight of water is displaced?", "3 N", "0.3 N", "300 N", "30 N", "D"),
        ("A liquid has density 900 kg/m³. Calculate gauge pressure at a depth of 4 m using g = 10 m/s².", "3600 Pa", "9000 Pa", "36,000 Pa", "90,000 Pa", "C"),
        ("An object has a mass of 2 kg and volume 0.001 m³. Taking g = 10 m/s², what is its weight?", "20 N", "2 N", "200 N", "0.2 N", "A"),
    ],

    "Hard": [
        ("A solid weighs 100 N in air and 60 N when fully immersed in water. What is its relative density?", "1.5", "2.5", "0.6", "4", "B"),
        ("A hydraulic press has piston areas of 0.02 m² and 0.4 m². What input force is needed to support a 2000 N load ideally?", "100 N", "200 N", "400 N", "50 N", "A"),
        ("A floating object has 75% of its volume submerged in water of density 1000 kg/m³. What is its average density?", "1333 kg/m³", "1000 kg/m³", "750 kg/m³", "250 kg/m³", "C"),
        ("A 2 kg object of volume 0.001 m³ is fully immersed in water. Taking g = 10 m/s² and water density as 1000 kg/m³, what is its apparent weight?", "20 N", "10 N", "5 N", "10 N", "D"),
        ("A diver is 8 m below the surface of water. Using density = 1000 kg/m³ and g = 9.8 m/s², what is the gauge pressure?", "78,400 Pa", "9800 Pa", "8000 Pa", "98,000 Pa", "A"),
        ("A solid has mass 3 kg and volume 0.002 m³. Taking g = 10 m/s², what is its weight?", "15 N", "30 N", "60 N", "300 N", "B"),
        ("A block of volume 0.01 m³ is fully submerged in a liquid of density 1200 kg/m³. Taking g = 10 m/s², what buoyant force acts on it?", "12 N", "120 N", "1200 N", "10 N", "B"),
        ("A body weighs 60 N in air and 45 N in a liquid. If the body displaces 0.0015 m³ of that liquid and g = 10 m/s², what is the liquid's density?", "500 kg/m³", "1000 kg/m³", "1500 kg/m³", "2000 kg/m³", "C"),
        ("A hydraulic press has a small piston area of 0.005 m² and a large piston area of 0.25 m². What force on the small piston can ideally support a 5000 N load?", "100 N", "250 N", "500 N", "50 N", "D"),
        ("A body has density 800 kg/m³ and volume 0.02 m³. It is placed in water of density 1000 kg/m³. What volume will be submerged when it floats?", "0.016 m³", "0.02 m³", "0.008 m³", "0.025 m³", "A"),
        ("A liquid produces gauge pressure of 24,000 Pa at a depth of 3 m. Taking g = 10 m/s², what is its density?", "800 kg/m³", "1000 kg/m³", "1200 kg/m³", "2400 kg/m³", "C"),
        ("An object weighs 200 N in air and 150 N when fully submerged in a liquid of density 1000 kg/m³. Taking g = 10 m/s², what is the object's volume?", "0.005 m³", "0.05 m³", "0.5 m³", "0.02 m³", "B"),
        ("A 100 N force is applied to a hydraulic piston's area of 0.01 m². What pressure is transmitted by the fluid ideally?", "100 Pa", "1000 Pa", "10,000 Pa", "1,000,000 Pa", "C"),
        ("A cube of side 0.2 m is completely submerged in water. Taking water density as 1000 kg/m³ and g = 10 m/s², what is the buoyant force?", "8 N", "40 N", "80 N", "800 N", "A"),
        ("A block floats in a liquid with 40% of its volume submerged. If the liquid density is 1200 kg/m³, what is the block's density?", "480 kg/m³", "720 kg/m³", "1200 kg/m³", "300 kg/m³", "A"),
        ("A body displaces 0.005 m³ of water and has a weight of 40 N. Taking water density as 1000 kg/m³ and g = 10 m/s², what happens when it is released while fully submerged?", "It sinks because its weight is greater", "It rises because buoyant force is greater than its weight", "It remains neutrally buoyant", "It has no buoyant force", "B"),
        ("A force of 500 N acts on an area of 0.025 m². What pressure is produced?", "20,000 Pa", "12,500 Pa", "2000 Pa", "500 Pa", "A"),
        ("A hydraulic lift has a large piston area 25 times the small piston area. If 80 N is applied to the small piston, what ideal output force is produced?", "320 N", "2000 N", "25 N", "80 N", "B"),
        ("An object weighs 120 N in air and 90 N when immersed. If g = 10 m/s² and the fluid density is 1000 kg/m³, what volume of fluid is displaced?", "0.003 m³", "0.03 m³", "0.3 m³", "0.0003 m³", "A"),
        ("A 4 kg object has volume 0.005 m³. What is its density?", "200 kg/m³", "500 kg/m³", "800 kg/m³", "1250 kg/m³", "C"),
        ("A body of volume 0.004 m³ and density 1500 kg/m³ is fully submerged in water. Taking g = 10 m/s², what is the net downward force?", "20 N", "40 N", "60 N", "10 N", "B"),
        ("A liquid has density 850 kg/m³. What is its gauge pressure at a depth of 6 m if g = 10 m/s²?", "5100 Pa", "8500 Pa", "51,000 Pa", "85,000 Pa", "C"),
        ("A block floats in water with 90% of its volume submerged. What is its density, assuming water density is 1000 kg/m³?", "900 kg/m³", "1000 kg/m³", "1100 kg/m³", "90 kg/m³", "A"),
        ("A hydraulic press has piston areas 0.01 m² and 0.2 m². A 100 N force is applied to the smaller piston. What load can be supported ideally?", "200 N", "1000 N", "500 N", "2000 N", "D"),
        ("A metal object has a mass of 5 kg and a volume of 0.002 m³. Taking g = 10 m/s², what is its weight?", "25 N", "50 N", "100 N", "500 N", "B"),
        ("A fully submerged object displaces 0.008 m³ of a liquid with density 750 kg/m³. Taking g = 10 m/s², what is the buoyant force?", "60 N", "6 N", "75 N", "600 N", "A"),
        ("A body weighs 50 N in air and experiences a buoyant force of 20 N in water. What is its apparent weight in water?", "70 N", "20 N", "30 N", "50 N", "C"),
        ("A force of 250 N produces a pressure of 5000 Pa. What is the area over which it acts?", "0.02 m²", "2 m²", "20 m²", "0.05 m²", "D"),
        ("A block has density 600 kg/m³ and volume 0.01 m³. If it floats in water of density 1000 kg/m³, what volume is submerged?", "0.01 m³", "0.006 m³", "0.004 m³", "0.016 m³", "B"),
        ("A 3 kg object of volume 0.002 m³ is completely submerged in water. Taking g = 10 m/s² and water density = 1000 kg/m³, what is the net force on it?", "10 N downward", "30 N downward", "20 N upward", "Zero", "A"),
    ],
}


def normalize(text):
    return " ".join(text.strip().lower().split())


def main():
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DATABASE_PATH}")

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, title FROM lessons WHERE LOWER(TRIM(title)) = LOWER(TRIM(?))",
            (LESSON_TITLE,),
        )
        lessons = cursor.fetchall()

        if len(lessons) != 1:
            raise RuntimeError(
                f"Expected exactly one lesson titled '{LESSON_TITLE}', found {len(lessons)}."
            )

        lesson_id = lessons[0][0]

        cursor.execute(
            "SELECT id, difficulty FROM quizzes WHERE lesson_id = ?",
            (lesson_id,),
        )
        quiz_by_difficulty = {}

        for quiz_id, difficulty in cursor.fetchall():
            key = str(difficulty).strip().capitalize()
            if key in {"Easy", "Medium", "Hard"}:
                if key in quiz_by_difficulty:
                    raise RuntimeError(f"Multiple {key} quizzes found.")
                quiz_by_difficulty[key] = quiz_id

        missing = {"Easy", "Medium", "Hard"} - set(quiz_by_difficulty)
        if missing:
            raise RuntimeError(f"Missing quizzes: {sorted(missing)}")

        total_added = 0

        for difficulty in ("Easy", "Medium", "Hard"):
            quiz_id = quiz_by_difficulty[difficulty]

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

            print(f"\n{difficulty}: currently {current_count} questions")

            if current_count >= TARGET_QUESTIONS:
                print(f"Already has at least {TARGET_QUESTIONS}; skipping.")
                continue

            added = 0

            for item in QUESTIONS[difficulty]:
                if current_count + added >= TARGET_QUESTIONS:
                    break

                question, option_a, option_b, option_c, option_d, answer = item
                normalized_question = normalize(question)

                if normalized_question in existing:
                    continue

                if answer not in {"A", "B", "C", "D"}:
                    raise ValueError(f"Invalid answer key for: {question}")

                cursor.execute(
                    """
                    INSERT INTO questions
                    (quiz_id, question, option_a, option_b, option_c, option_d, correct_answer)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (quiz_id, question, option_a, option_b, option_c, option_d, answer),
                )
                existing.add(normalized_question)
                added += 1

            final_count = current_count + added
            print(f"Added {added}; final total: {final_count}")

            if final_count < TARGET_QUESTIONS:
                raise RuntimeError(
                    f"{difficulty} has only {final_count} questions; "
                    "transaction will be rolled back."
                )

            total_added += added

        connection.commit()
        print(f"\nSuccess! Added {total_added} questions to '{LESSON_TITLE}'.")
        print("Other lessons and Social Science were not modified.")

    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


if __name__ == "__main__":
    main()
