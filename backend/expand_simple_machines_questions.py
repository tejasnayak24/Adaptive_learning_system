
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"
LESSON_TITLE = "Simple Machines"
TARGET_QUESTIONS = 30

QUESTIONS = {
    "Easy": [
        ("What is a simple machine?", "A device that helps make work easier", "A device that creates energy", "A type of fuel", "A living organism", "A"),
        ("Which of these is a simple machine?", "Battery", "Lever", "Bulb", "Thermometer", "B"),
        ("How many basic types of simple machines are commonly identified?", "Three", "Four", "Six", "Ten", "C"),
        ("Which simple machine consists of a rigid bar that turns around a fixed point?", "Pulley", "Screw", "Wedge", "Lever", "D"),
        ("What is the fixed point about which a lever turns called?", "Fulcrum", "Load", "Effort", "Axle", "A"),
        ("Which simple machine is commonly used to raise a flag on a flagpole?", "Wedge", "Pulley", "Screw", "Inclined plane", "B"),
        ("Which simple machine is a sloping surface used to move objects to a different height?", "Lever", "Wheel and axle", "Inclined plane", "Pulley", "C"),
        ("Which simple machine is commonly used to split wood?", "Pulley", "Wheel and axle", "Lever only", "Wedge", "D"),
        ("Which simple machine is used in a doorknob?", "Wheel and axle", "Wedge", "Inclined plane", "Pulley", "A"),
        ("A screw is most closely related to which simple machine?", "Lever", "Inclined plane wrapped around a cylinder", "Pulley", "Wedge only", "B"),
        ("What is the force applied to a machine called?", "Load", "Friction", "Effort", "Fulcrum", "C"),
        ("What is the object or resistance that a machine moves called?", "Effort", "Fulcrum", "Axle", "Load", "D"),
        ("Which simple machine is commonly used in a seesaw?", "Lever", "Screw", "Pulley", "Wedge", "A"),
        ("Which of these is an example of an inclined plane?", "Bottle opener", "Ramp", "Door handle", "Flagpole pulley", "B"),
        ("What is the main purpose of a simple machine?", "To destroy energy", "To eliminate all forces", "To change the size or direction of a force", "To create energy from nothing", "C"),
        ("Which simple machine is found in an axe blade?", "Pulley", "Wheel and axle", "Lever", "Wedge", "D"),
        ("Which part of a pulley system supports the pulley wheel and its axle?", "The frame or support", "The load itself in every case", "The effort only", "The rope's free end only", "A"),
        ("Which simple machine is used in a traditional well to lift a bucket with a rope?", "Wedge", "Pulley", "Inclined plane", "Screw", "B"),
        ("Which simple machine is a ramp an example of?", "Lever", "Pulley", "Inclined plane", "Wheel and axle", "C"),
        ("Which of these is an example of a lever?", "Nail", "Ramp", "Screw cap", "Crowbar", "D"),
        ("What does a machine's load generally represent?", "The resistance or weight being moved", "The distance travelled by effort only", "The machine's colour", "The amount of friction alone", "A"),
        ("Which simple machine is commonly used in a wheelbarrow?", "Fixed pulley only", "Lever and wheel-and-axle arrangement", "Wedge only", "Screw only", "B"),
        ("Which simple machine is used in a knife?", "Pulley", "Wheel and axle", "Wedge", "Lever", "C"),
        ("What is mechanical advantage?", "The machine's mass", "The speed of sound", "The machine's temperature", "The ratio of load to effort", "D"),
        ("What does an ideal machine do with input work and output work?", "Output work equals input work", "Output work is always zero", "Output work is always greater than input work", "Input work is always zero", "A"),
        ("Which simple machine helps turn a small force applied over a longer distance into a larger force over a shorter distance?", "Thermometer", "Lever", "Light bulb", "Battery", "B"),
        ("Which part of a lever is the point where the effort is applied?", "Fulcrum", "Load", "Effort point", "Axle", "C"),
        ("Which simple machine is used in a bottle opener?", "Pulley", "Inclined plane", "Wheel and axle", "Lever", "D"),
        ("What is friction in a machine?", "A force that opposes relative motion between contacting surfaces", "A type of stored energy", "The load divided by effort", "The fixed turning point", "A"),
        ("Which statement about simple machines is correct?", "They always eliminate the need for effort", "They can make a task easier but do not create energy", "They produce energy without input", "They always reduce both force and distance", "B"),
    ],

    "Medium": [
        ("A machine lifts a load of 200 N using an effort of 50 N. What is its mechanical advantage?", "2", "3", "4", "5", "C"),
        ("A lever has a load arm of 20 cm and an effort arm of 80 cm. What is its ideal mechanical advantage?", "4", "2", "0.25", "100", "A"),
        ("A machine has an input work of 500 J and useful output work of 400 J. What is its efficiency?", "50%", "80%", "90%", "125%", "B"),
        ("An ideal pulley system has a mechanical advantage of 3. Ideally, how much effort is required to lift a 300 N load?", "900 N", "150 N", "100 N", "75 N", "C"),
        ("A lever lifts a 600 N load with an effort of 150 N. What is its mechanical advantage?", "2", "3", "5", "4", "D"),
        ("A machine receives 1000 J of work and produces 700 J of useful work. How much energy is lost to other forms?", "300 J", "700 J", "1000 J", "1700 J", "A"),
        ("A ramp is 5 m long and rises 1 m vertically. What is its ideal mechanical advantage?", "1", "5", "4", "6", "B"),
        ("An effort of 40 N moves through 2 m while lifting a load through 0.5 m. If the machine is ideal, what is the load?", "40 N", "80 N", "160 N", "20 N", "C"),
        ("A machine has a load of 240 N and an effort of 80 N. What is its mechanical advantage?", "2", "4", "5", "3", "D"),
        ("A machine has a mechanical advantage of 4 and an efficiency of 75%. What is its velocity ratio?", "16/3, approximately 5.33", "3", "4", "1", "A"),
        ("A lever has an effort arm of 60 cm and a load arm of 15 cm. What is its ideal mechanical advantage?", "2", "4", "5", "0.25", "B"),
        ("A machine's input work is 600 J and its efficiency is 50%. What is its useful output work?", "1200 J", "600 J", "300 J", "50 J", "C"),
        ("A load of 500 N is raised using an effort of 125 N. What is the mechanical advantage?", "2", "3", "5", "4", "D"),
        ("A machine has a velocity ratio of 5 and a mechanical advantage of 4. What is its efficiency?", "80%", "20%", "125%", "40%", "A"),
        ("A 200 N load is raised by 2 m. Ignoring losses, how much useful work is done against gravity?", "100 J", "400 J", "200 J", "800 J", "B"),
        ("A pulley system has an ideal mechanical advantage of 4. What effort is ideally needed to lift a 600 N load?", "2400 N", "300 N", "200 N", "150 N", "D"),
        ("A machine has an efficiency of 60% and receives 1000 J of work. What is its useful output work?", "400 J", "600 J", "1000 J", "1600 J", "B"),
        ("A lever's effort arm is 1.2 m and its load arm is 0.3 m. What is the ideal mechanical advantage?", "0.25", "2", "4", "3", "C"),
        ("A machine moves an effort through 4 m while a load moves through 1 m. What is its velocity ratio?", "4", "1/4", "3", "5", "A"),
        ("A machine lifts a 400 N load using an effort of 100 N. If its velocity ratio is 5, what is its efficiency?", "20%", "80%", "125%", "100%", "B"),
        ("A 300 N load is lifted 2 m. What is the gain in gravitational potential energy, assuming the load's weight remains constant?", "150 J", "300 J", "600 J", "900 J", "C"),
        ("A machine has mechanical advantage 2 and velocity ratio 4. What is its efficiency?", "200%", "100%", "75%", "50%", "D"),
        ("A ramp is 6 m long and raises an object by 2 m. What is its ideal mechanical advantage?", "3", "2", "4", "8", "A"),
        ("A machine delivers 900 J of useful work from 1200 J of input work. What is its efficiency?", "25%", "75%", "80%", "133%", "B"),
        ("A lever has a 100 cm effort arm and a 25 cm load arm. If the effort is 40 N, what load can it balance ideally?", "40 N", "80 N", "160 N", "200 N", "C"),
        ("A machine has an input power of 500 W and an output power of 350 W. What is its efficiency?", "30%", "50%", "85%", "70%", "D"),
        ("A 100 N effort raises a load of 300 N. What is the machine's mechanical advantage?", "3", "2", "4", "0.33", "A"),
        ("A machine has an efficiency of 40%. If input work is 250 J, what is the useful output work?", "1000 J", "100 J", "150 J", "40 J", "B"),
        ("An ideal wheel and axle has a wheel radius of 40 cm and axle radius of 10 cm. What is its ideal mechanical advantage?", "2", "5", "4", "0.25", "C"),
        ("Why is the efficiency of a real simple machine usually less than 100%?", "It creates energy", "It has no moving parts", "It always stores all input energy", "Some input energy is dissipated, often by friction", "D"),
    ],

    "Hard": [
        ("A machine lifts a 600 N load with an effort of 150 N. Its velocity ratio is 5. What is its efficiency?", "80%", "50%", "75%", "125%", "A"),
        ("A lever has an effort arm of 1.5 m and a load arm of 0.3 m. What effort is ideally needed to balance a 500 N load?", "500 N", "100 N", "250 N", "50 N", "B"),
        ("A machine receives 2000 J of input work and has an efficiency of 65%. How much useful work does it produce?", "2000 J", "1300 J", "700 J", "3077 J", "B"),
        ("A pulley system has a velocity ratio of 6 and an efficiency of 80%. What is its mechanical advantage?", "6.8", "4.8", "7.5", "0.75", "B"),
        ("A machine raises a 400 N load by 3 m while the effort moves 12 m. If the effort is 150 N, what is its efficiency?", "50%", "60%", "66.7%", "80%", "C"),
        ("A lever's effort arm is 90 cm and its load arm is 30 cm. If the effort is 80 N, what load can be balanced ideally?", "80 N", "120 N", "160 N", "240 N", "D"),
        ("A machine has mechanical advantage 3 and velocity ratio 4. What is its efficiency?", "75%", "133%", "25%", "100%", "A"),
        ("A machine operates at 70% efficiency and delivers 350 J of useful work. What is its input work?", "245 J", "500 J", "420 J", "700 J", "B"),
        ("An ideal inclined plane is 8 m long and raises a load by 2 m. What effort is needed to raise a 400 N load at constant speed?", "400 N", "200 N", "100 N", "50 N", "C"),
        ("A wheel and axle has a wheel radius of 0.5 m and axle radius of 0.1 m. If its efficiency is 80%, what is its mechanical advantage?", "4", "5", "6.25", "4.8", "D"),
        ("A machine has input power 800 W and useful output power 600 W. How much energy is lost in 10 seconds?", "2000 J", "6000 J", "8000 J", "200 J", "A"),
        ("A 1000 N load is lifted by a machine with mechanical advantage 5. What effort is required?", "5000 N", "200 N", "100 N", "50 N", "B"),
        ("A machine has a velocity ratio of 8 and efficiency of 75%. What is its mechanical advantage?", "8", "10.67", "6", "4", "C"),
        ("A 250 N effort moves 4 m while a load of 500 N moves 1.5 m. What is the efficiency?", "75%", "50%", "100%", "75%", "A"),
        ("A lever balances a 600 N load with a 150 N effort. If the effort arm is 1.2 m, what is the load arm for ideal balance?", "0.2 m", "0.3 m", "0.6 m", "0.4 m", "D"),
        ("A machine's efficiency is 60%. If the input work is 1500 J, how much energy is not delivered as useful output work?", "900 J", "600 J", "1500 J", "2400 J", "B"),
        ("A pulley system has a velocity ratio of 5. The effort moves 10 m while lifting a load. How far does the load move?", "50 m", "10 m", "2 m", "5 m", "C"),
        ("A machine lifts a 300 N load through 2 m using a 100 N effort that moves 8 m. What is its efficiency?", "75%", "50%", "100%", "25%", "A"),
        ("A wheel and axle has a wheel radius of 30 cm and an axle radius of 5 cm. What is the ideal mechanical advantage?", "5", "6", "25", "1/6", "B"),
        ("A machine has efficiency 80% and velocity ratio 10. What is its mechanical advantage?", "10", "12.5", "8", "80", "C"),
        ("A machine receives 5 kJ of input energy and produces 3.5 kJ of useful work. What percentage of input energy is lost?", "30%", "70%", "35%", "15%", "A"),
        ("A 400 N load is lifted by an effort of 100 N. The load moves 2 m while the effort moves 10 m. What is the efficiency?", "40%", "50%", "80%", "20%", "D"),
        ("A lever has an effort arm of 2 m and a load arm of 0.5 m. If the load is 800 N, what effort is required ideally?", "800 N", "200 N", "400 N", "100 N", "B"),
        ("A machine delivers 1200 W of useful power at 75% efficiency. What is its input power?", "900 W", "1600 W", "1500 W", "2400 W", "B"),
        ("A machine has mechanical advantage 4 and efficiency 50%. What is its velocity ratio?", "2", "4", "8", "0.5", "C"),
        ("A 600 N load is raised by a machine using a 200 N effort. If the effort moves 6 m and the load moves 1.5 m, what is its efficiency?", "75%", "50%", "100%", "25%", "A"),
        ("An ideal screw jack advances 0.5 cm per turn. The handle radius is 25 cm. Using π ≈ 3.14, what is its approximate velocity ratio?", "31.4", "50", "100", "157", "D"),
        ("A machine is 80% efficient and has an input energy of 2500 J. How much useful energy is produced?", "500 J", "2000 J", "2500 J", "3125 J", "B"),
        ("A lever's load arm is 20 cm and effort arm is 100 cm. If the load is 500 N, what effort is needed ideally?", "500 N", "250 N", "100 N", "50 N", "D"),
        ("A machine performs 1800 J of useful work in 12 seconds. If its efficiency is 60%, what is its input power?", "150 W", "250 W", "300 W", "360 W", "C"),
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

        cursor.execute("SELECT id, difficulty FROM quizzes WHERE lesson_id = ?", (lesson_id,))
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

            cursor.execute("SELECT question FROM questions WHERE quiz_id = ?", (quiz_id,))
            existing = {normalize(row[0]) for row in cursor.fetchall()}

            cursor.execute("SELECT COUNT(*) FROM questions WHERE quiz_id = ?", (quiz_id,))
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
                    f"{difficulty} has only {final_count} questions. "
                    "Transaction will be rolled back."
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
