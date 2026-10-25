
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"
LESSON_TITLE = "Work, Energy and Power"
TARGET_QUESTIONS = 30

QUESTIONS = {
    "Easy": [
        ("What is the SI unit of work?", "Newton", "Joule", "Watt", "Pascal", "B"),
        ("What is the SI unit of energy?", "Joule", "Watt", "Newton", "Ampere", "A"),
        ("What is the SI unit of power?", "Joule", "Newton", "Watt", "Metre", "C"),
        ("When is mechanical work done on an object by a force?", "Whenever the object exists", "Only when the force is zero", "Only when the object has mass", "When the force causes displacement with a component along its direction", "D"),
        ("Which of these is a form of kinetic energy?", "Energy stored in a stretched spring", "Energy possessed by a moving car", "Energy stored in a battery", "Energy stored in food", "B"),
        ("Which object has gravitational potential energy because of its height?", "A book on a high shelf", "A stationary book on the floor", "A stone at ground level", "A ball rolling on a level floor", "A"),
        ("What does power measure?", "Total distance travelled", "Mass of an object", "Rate of doing work", "Amount of matter", "C"),
        ("Which expression gives average power?", "Work × time", "Work + time", "Time ÷ work", "Work ÷ time", "D"),
        ("What is the kinetic energy of an object at rest?", "Zero", "Maximum", "Equal to its mass", "Always negative", "A"),
        ("Which energy source stores chemical energy?", "A raised stone", "A moving bicycle", "Food", "A spinning wheel", "C"),
        ("What happens to an object's kinetic energy when its speed increases, with mass unchanged?", "It decreases", "It increases", "It becomes zero", "It remains unchanged", "B"),
        ("Which of these is an example of mechanical work being done?", "Holding a heavy bag stationary", "Pushing a wall that does not move", "Standing still with a book", "Lifting a box from the floor", "D"),
        ("What is the formula for kinetic energy?", "mv", "mgh", "½mv²", "F ÷ d", "C"),
        ("What is the formula for gravitational potential energy near Earth's surface?", "mgh", "½mv²", "Fd²", "m ÷ g", "A"),
        ("What is the SI unit of force?", "Joule", "Newton", "Watt", "Kilogram", "B"),
        ("If a force acts on an object but causes no displacement, how much work does that force do?", "Maximum work", "Negative infinite work", "Work equal to the object's mass", "Zero work", "D"),
        ("Which object has kinetic energy?", "A stationary chair", "A book resting on a table", "A moving train", "A fixed wall", "C"),
        ("What is the commercial unit commonly used to measure electrical energy consumption?", "Kilowatt-hour", "Newton", "Watt per second", "Kilogram", "A"),
        ("One joule of work is done when a force of 1 N moves an object how far in the force's direction?", "10 m", "1 m", "1 km", "0.1 m", "B"),
        ("What happens to gravitational potential energy when an object is lifted higher?", "It always becomes zero", "It becomes negative in every case", "It remains unchanged", "It increases", "D"),
        ("Which quantity is measured in watts?", "Power", "Force", "Work", "Distance", "A"),
        ("Which type of energy does a stretched elastic band store?", "Sound energy only", "Nuclear energy only", "Elastic potential energy", "Electrical current", "C"),
        ("Which statement about energy is correct?", "Energy can be created from nothing", "Energy can neither be created nor destroyed in an isolated system", "Energy always disappears", "Energy has no units", "B"),
        ("What is the work done by a 10 N force moving an object 2 m in the same direction as the force?", "5 J", "12 J", "20 J", "100 J", "C"),
        ("A machine performs 100 J of work in 5 seconds. What is its average power?", "20 W", "50 W", "500 W", "5 W", "A"),
        ("Which of these has gravitational potential energy relative to the ground?", "A stone moving horizontally at ground level", "A stationary stone on the ground", "A stationary stone raised above the ground", "A stone buried at the chosen reference level", "C"),
        ("What is the kinetic energy of a 2 kg object moving at 3 m/s?", "6 J", "9 J", "12 J", "18 J", "B"),
        ("What happens to kinetic energy if an object's speed doubles while its mass stays constant?", "It doubles", "It becomes half", "It becomes four times as large", "It becomes eight times as large", "C"),
        ("Which unit is equivalent to one watt?", "Joule × second", "Newton per metre", "Kilogram per second", "Joule per second", "D"),
        ("A person carries a bag horizontally at constant height. In the ideal physics model, what work does the upward supporting force do on the bag?", "Zero, because the force is perpendicular to the displacement", "Positive work equal to the bag's weight", "Negative work equal to the distance", "Work equal to the bag's mass", "A"),
    ],

    "Medium": [
        ("A 20 N force moves an object 5 m in the direction of the force. How much work is done?", "4 J", "25 J", "100 J", "200 J", "C"),
        ("A machine does 600 J of work in 20 seconds. What is its average power?", "30 W", "120 W", "580 W", "12 W", "A"),
        ("Calculate the kinetic energy of a 4 kg object moving at 5 m/s.", "20 J", "40 J", "100 J", "50 J", "D"),
        ("A 3 kg object is raised 2 m. Taking g = 10 m/s², what is its gain in gravitational potential energy?", "6 J", "60 J", "30 J", "15 J", "B"),
        ("A 10 N force acts at 60° to a displacement of 4 m. What work does the force do?", "40 J", "20 J", "10 J", "0 J", "B"),
        ("A 2 kg object moves at 6 m/s. What is its kinetic energy?", "12 J", "18 J", "36 J", "72 J", "C"),
        ("A motor lifts a 100 N load through 5 m in 10 seconds. What is the useful average power output?", "50 W", "100 W", "500 W", "250 W", "A"),
        ("A force of 15 N acts opposite to an object's displacement of 3 m. What work does the force do?", "45 J", "18 J", "0 J", "−45 J", "D"),
        ("A 5 kg object is moving at 4 m/s. If its speed doubles, what is its new kinetic energy?", "40 J", "80 J", "160 J", "20 J", "B"),
        ("A 2 kW motor runs for 3 minutes. How much energy does it transfer at constant rated power?", "600 J", "6000 J", "360,000 J", "36,000 J", "C"),
        ("A 50 kg student climbs a staircase 4 m high. Taking g = 10 m/s², how much gravitational potential energy is gained?", "200 J", "500 J", "1000 J", "2000 J", "D"),
        ("A 200 W device runs for 10 seconds. How much energy does it transfer?", "2000 J", "20 J", "200 J", "20000 J", "A"),
        ("A 30 N force moves an object 6 m, making an angle of 90° with the displacement. What work does this force do?", "180 J", "30 J", "0 J", "6 J", "C"),
        ("A 1000 kg car moves at 10 m/s. What is its kinetic energy?", "10,000 J", "50,000 J", "100,000 J", "5000 J", "B"),
        ("A 4 kg object is raised by 5 m. Taking g = 9.8 m/s², what is the increase in potential energy?", "19.6 J", "98 J", "196 J", "49 J", "C"),
        ("A machine does 2400 J of work in 60 seconds. What is its average power?", "40 W", "60 W", "144 W", "240 W", "A"),
        ("A 10 kg object falls through a vertical height of 3 m. Ignoring air resistance and taking g = 10 m/s², how much gravitational potential energy does it lose?", "30 J", "100 J", "3000 J", "300 J", "D"),
        ("A 2 kg object has 100 J of kinetic energy. What is its speed?", "5 m/s", "10 m/s", "20 m/s", "50 m/s", "B"),
        ("A force of 8 N moves an object 10 m at an angle of 60° to the displacement. What is the work done by this force?", "80 J", "20 J", "40 J", "0 J", "C"),
        ("A machine receives 500 J of energy and produces 350 J of useful output energy. What is its efficiency?", "70%", "35%", "50%", "85%", "A"),
        ("A 60 kg person climbs 5 m in 10 seconds. Taking g = 10 m/s², what is the average power developed against gravity?", "300 W", "600 W", "30 W", "150 W", "B"),
        ("A 1 kg object is dropped from a height of 20 m. Ignoring air resistance and taking g = 10 m/s², what is its speed just before impact?", "10 m/s", "14.1 m/s", "20 m/s", "200 m/s", "C"),
        ("A force of 25 N acts along a displacement of 4 m. If the force and displacement are in opposite directions, what is the work done?", "100 J", "29 J", "0 J", "−100 J", "D"),
        ("A 3 kg object moves at 4 m/s. What work must the net force do to bring it to rest?", "−24 J", "24 J", "−12 J", "12 J", "A"),
        ("A 500 W motor operates for 2 minutes. How much energy does it use?", "1000 J", "10,000 J", "60,000 J", "120,000 J", "C"),
        ("A 20 kg object is lifted vertically at constant speed through 2 m. Taking g = 10 m/s², what work is done by the lifting force?", "40 J", "400 J", "200 J", "800 J", "B"),
        ("An object has 50 J of kinetic energy and 150 J of gravitational potential energy. What is its total mechanical energy?", "100 J", "150 J", "200 J", "7500 J", "C"),
        ("A 1000 W motor performs 8000 J of useful work in 10 seconds. What is its useful output power?", "800 W", "1000 W", "80 W", "8000 W", "A"),
        ("A 2 kg object moving at 3 m/s is accelerated to 7 m/s. What is the net work done on it?", "20 J", "29 J", "40 J", "40 J", "D"),
        ("A 100 N force moves an object 10 m, and the angle between force and displacement is 60°. What work is done?", "1000 J", "500 J", "250 J", "0 J", "B"),
    ],

    "Hard": [
        ("A 2 kg object speeds up from 3 m/s to 7 m/s. What is the net work done on it?", "20 J", "40 J", "58 J", "40 J", "B"),
        ("A 1000 kg car travels at 20 m/s. What is its kinetic energy?", "20,000 J", "100,000 J", "200,000 J", "400,000 J", "C"),
        ("A 5 kg object is lifted 8 m in 4 seconds at constant speed. Taking g = 10 m/s², what is the average useful power?", "100 W", "50 W", "400 W", "200 W", "D"),
        ("A machine receives 2000 J of energy and has an efficiency of 75%. How much useful energy does it output?", "1500 J", "500 J", "2000 J", "2667 J", "A"),
        ("A 4 kg object falls from rest through 5 m. Ignoring air resistance and taking g = 10 m/s², what is its speed just before impact?", "5 m/s", "10 m/s", "20 m/s", "50 m/s", "B"),
        ("A 10 kg object moves at 8 m/s. What constant net opposing force would stop it over 16 m?", "10 N", "40 N", "20 N", "80 N", "C"),
        ("A 50 N force acts at 37° to a displacement of 10 m. Using cos 37° ≈ 0.8, calculate the work done by the force.", "500 J", "300 J", "400 J", "40 J", "C"),
        ("A motor lifts a 200 kg load through 15 m in 30 seconds. Taking g = 10 m/s², what is its useful output power?", "1000 W", "1500 W", "2000 W", "1000 W", "D"),
        ("An object of mass 2 kg is moving at 10 m/s. A net opposing force does 64 J of work. What is its final kinetic energy?", "36 J", "100 J", "64 J", "164 J", "A"),
        ("A 1500 kg car increases its speed from 10 m/s to 20 m/s. How much net work is done on it?", "75,000 J", "225,000 J", "300,000 J", "150,000 J", "B"),
        ("A 60 kg climber ascends 12 m in 8 seconds. Taking g = 10 m/s², what is the average power used to gain gravitational potential energy?", "600 W", "720 W", "900 W", "1200 W", "D"),
        ("A 1000 W machine is 80% efficient. How much useful energy does it produce in 60 seconds?", "60,000 J", "48,000 J", "80,000 J", "12,000 J", "B"),
        ("A 2 kg object is projected vertically upward at 20 m/s. Ignoring air resistance and taking g = 10 m/s², what maximum height does it reach?", "10 m", "40 m", "20 m", "2 m", "C"),
        ("A 5 kg object has 250 J of kinetic energy. What is its speed?", "10 m/s", "5 m/s", "25 m/s", "50 m/s", "A"),
        ("A 40 N force acts on an object over 5 m at an angle of 60° to the displacement. What work does it do?", "200 J", "100 J", "40 J", "0 J", "B"),
        ("A machine receives 5000 J and delivers 3500 J of useful energy. What percentage of the input energy is lost to other forms?", "70%", "35%", "15%", "30%", "D"),
        ("A 1200 kg vehicle moving at 15 m/s is brought to rest. What is the work done by the net braking force?", "135,000 J", "−13,500 J", "−135,000 J", "0 J", "C"),
        ("A 4 kg object is lifted 6 m in 3 seconds at constant speed. Taking g = 10 m/s², what is the average power?", "80 W", "40 W", "240 W", "120 W", "D"),
        ("A 2 kg object falls from a height of 45 m. Ignoring air resistance and taking g = 10 m/s², what is its speed after falling 20 m?", "20 m/s", "10 m/s", "30 m/s", "40 m/s", "A"),
        ("A 3 kg object moving at 4 m/s is accelerated to 12 m/s. What is the increase in kinetic energy?", "48 J", "192 J", "240 J", "144 J", "C"),
        ("A motor takes 2 kW of input power and delivers 1.5 kW of useful output power. What is its efficiency?", "50%", "75%", "80%", "25%", "B"),
        ("A 10 kg object is raised 2 m and then raised another 3 m. Taking g = 10 m/s², what is its total gain in gravitational potential energy from the starting point?", "200 J", "300 J", "500 J", "50 J", "C"),
        ("A 5 kg object moving at 6 m/s is stopped by a constant net force over 3 m. What is the magnitude of that force?", "15 N", "20 N", "25 N", "30 N", "D"),
        ("A 2 kW motor runs for 15 minutes. How much energy does it consume in kWh?", "0.5 kWh", "2 kWh", "0.25 kWh", "30 kWh", "A"),
        ("A 100 kg load is raised 10 m by a motor that is 50% efficient. Taking g = 10 m/s², how much input energy is required?", "5000 J", "10,000 J", "20,000 J", "2000 J", "C"),
        ("A 4 kg object has 200 J of kinetic energy. What is its speed?", "5 m/s", "10 m/s", "20 m/s", "100 m/s", "B"),
        ("A force does 600 J of work in moving an object 12 m in the direction of the force. What is the force magnitude?", "50 N", "72 N", "12 N", "25 N", "A"),
        ("A 75 kg person climbs 4 m in 5 seconds. Taking g = 10 m/s², what is the average power against gravity?", "150 W", "300 W", "750 W", "600 W", "D"),
        ("A 3 kg object is dropped from 20 m. Ignoring air resistance and taking g = 10 m/s², how much kinetic energy does it have after falling 12 m?", "240 J", "360 J", "600 J", "60 J", "B"),
        ("A 1000 kg car slows from 25 m/s to 15 m/s. What is the net work done on the car?", "200,000 J", "−50,000 J", "−200,000 J", "50,000 J", "C"),
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
            raise RuntimeError(f"Missing difficulty quizzes: {sorted(missing)}")

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
                    raise ValueError(f"Invalid answer key for question: {question}")

                cursor.execute(
                    """
                    INSERT INTO questions
                    (quiz_id, question, option_a, option_b, option_c, option_d, correct_answer)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        quiz_id,
                        question,
                        option_a,
                        option_b,
                        option_c,
                        option_d,
                        answer,
                    ),
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
