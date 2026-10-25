
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"
LESSON_TITLE = "Electricity and Circuits"
TARGET_QUESTIONS = 30

QUESTIONS = {
    "Easy": [
        ("What is the SI unit of electric current?", "Volt", "Ampere", "Ohm", "Watt", "B"),
        ("Which device supplies electrical energy in a simple circuit?", "Bulb", "Switch", "Cell", "Wire", "C"),
        ("Which material is a good conductor of electricity?", "Copper", "Rubber", "Plastic", "Wood", "A"),
        ("What is the main function of a switch?", "Store charge", "Produce light", "Measure current", "Open or close a circuit", "D"),
        ("Which instrument measures electric current?", "Voltmeter", "Ammeter", "Thermometer", "Barometer", "B"),
        ("Which component converts electrical energy into light?", "Fuse", "Cell", "Electric bulb", "Switch", "C"),
        ("What is the SI unit of potential difference?", "Volt", "Ampere", "Ohm", "Joule", "A"),
        ("Which material is commonly used to cover electric wires?", "Copper", "Aluminium", "Iron", "Plastic", "D"),
        ("When does a bulb glow in a simple circuit?", "When the circuit is open", "When the circuit is complete", "When a wire is disconnected", "When there is no cell", "B"),
        ("What is the SI unit of electrical resistance?", "Watt", "Volt", "Ohm", "Ampere", "C"),
        ("Which of these is an electrical insulator?", "Rubber", "Copper", "Iron", "Aluminium", "A"),
        ("What is the purpose of a cell in a circuit?", "Interrupt current", "Measure resistance", "Insulate wires", "Provide electrical energy", "D"),
        ("Which symbol is commonly used to represent a cell in a circuit diagram?", "A circle with a cross", "Two parallel lines of unequal length", "A zigzag line only", "A triangle", "B"),
        ("What happens when a circuit is broken?", "Current increases automatically", "The cell becomes a bulb", "Current stops flowing through the broken path", "Resistance becomes zero", "C"),
        ("Which quantity is measured in watts?", "Power", "Current", "Resistance", "Charge", "A"),
        ("Which particle carries a negative electric charge?", "Proton", "Neutron", "Nucleus", "Electron", "D"),
        ("Which device protects a circuit from excessive current by melting?", "Voltmeter", "Fuse", "Bulb", "Ammeter", "B"),
        ("What is the conventional direction of current in an external circuit?", "Negative to positive", "From the bulb to the switch only", "Positive to negative", "In no fixed direction", "C"),
        ("What is a circuit with a complete conducting path called?", "Closed circuit", "Open circuit", "Broken circuit", "Insulated circuit", "A"),
        ("Which metal is commonly used for electrical wiring?", "Sulfur", "Rubber", "Glass", "Copper", "D"),
        ("What does a battery contain?", "Only plastic", "One or more electrochemical cells", "Only a switch", "Only a resistor", "B"),
        ("Which instrument measures potential difference?", "Ammeter", "Compass", "Voltmeter", "Stopwatch", "C"),
        ("Which component is used to limit current in a circuit?", "Resistor", "Cell holder", "Connecting wire only", "Switch cover", "A"),
        ("What is the unit of electric charge?", "Volt", "Watt", "Ohm", "Coulomb", "D"),
        ("Which combination is required for a simple working bulb circuit?", "Bulb and disconnected wire only", "Cell, bulb, and complete conducting path", "Switch alone", "Bulb without a power source", "B"),
        ("What is the main role of connecting wires?", "Generate electricity", "Measure voltage", "Provide a conducting path", "Store electrical energy", "C"),
        ("Which material is a poor conductor under ordinary conditions?", "Glass", "Copper", "Silver", "Aluminium", "A"),
        ("What is the SI unit of electrical energy?", "Ampere", "Ohm", "Volt", "Joule", "D"),
        ("What happens when a closed switch is changed to an open switch in a simple series circuit?", "Current doubles", "The conducting path is interrupted", "The cell gains energy", "Resistance must become zero", "B"),
        ("Which household device converts electrical energy mainly into heat?", "Electric heater", "Dry cell", "Switch", "Connecting wire", "A"),
    ],

    "Medium": [
        ("A current of 2 A flows for 5 seconds. How much charge passes a point?", "2 C", "5 C", "10 C", "20 C", "C"),
        ("A 12 V potential difference is applied across a 4 ohm resistor. What current flows?", "3 A", "4 A", "8 A", "48 A", "A"),
        ("A resistor has 6 V across it and carries 0.5 A. What is its resistance?", "3 ohms", "6 ohms", "12 ohms", "0.083 ohms", "C"),
        ("Two 2 ohm resistors are connected in series. What is their total resistance?", "1 ohm", "4 ohms", "2 ohms", "8 ohms", "B"),
        ("Two 6 ohm resistors are connected in parallel. What is the equivalent resistance?", "12 ohms", "6 ohms", "3 ohms", "36 ohms", "C"),
        ("A device operates at 10 V and draws 2 A. What is its electrical power?", "5 W", "12 W", "8 W", "20 W", "D"),
        ("A 60 W lamp operates for 2 hours. How much electrical energy does it use?", "120 Wh", "30 Wh", "60 Wh", "240 Wh", "A"),
        ("What happens to the total resistance when resistors are added in series?", "It always becomes zero", "It decreases", "It increases", "It stays equal to the smallest resistor", "C"),
        ("In a parallel circuit, what is the same across each branch?", "Current through every branch", "Potential difference", "Resistance", "Power in every branch", "B"),
        ("An ammeter should be connected how in a circuit to measure current through a component?", "In parallel with the component", "Across the cell only", "Without connecting it to the circuit", "In series with the component", "D"),
        ("A voltmeter should be connected how to measure the potential difference across a resistor?", "In parallel", "In series", "Only to the switch", "In place of the cell", "A"),
        ("If the voltage across a fixed resistor doubles, what happens to the current?", "It becomes half", "It becomes zero", "It doubles", "It remains unchanged", "C"),
        ("A 4 ohm resistor carries 3 A. What is the potential difference across it?", "7 V", "12 V", "1.33 V", "24 V", "B"),
        ("A 100 W appliance operates at 200 V. What current does it draw?", "0.5 A", "2 A", "20 A", "0.05 A", "A"),
        ("A 5 ohm resistor and a 7 ohm resistor are connected in series. What is their total resistance?", "2 ohms", "35 ohms", "12 ohms", "1.7 ohms", "C"),
        ("Two 4 ohm resistors are connected in parallel. What is their equivalent resistance?", "8 ohms", "4 ohms", "16 ohms", "2 ohms", "D"),
        ("A current of 0.25 A flows for 20 seconds. How much charge is transferred?", "80 C", "5 C", "20 C", "0.0125 C", "B"),
        ("Which statement describes conventional current correctly?", "It is the movement of neutrons through a wire", "It always flows from low to high potential in an external circuit", "It is defined in the direction positive charges would move", "It is identical to the motion direction of electrons in a metal", "C"),
        ("Why are household appliances generally connected in parallel?", "Each appliance can receive the supply voltage and operate independently", "The current must be identical in every appliance", "The total resistance must always increase", "One switch must control every appliance", "A"),
        ("What is the main purpose of earthing a metal-bodied appliance?", "Increase its normal operating voltage", "Make its casing a source of current", "Prevent all current from flowing in the appliance", "Provide a safer path for fault current", "D"),
        ("A 2 ohm resistor and an 8 ohm resistor are connected in series to a 20 V source. What current flows?", "10 A", "2 A", "4 A", "0.5 A", "B"),
        ("A 12 V battery is connected across a 6 ohm resistor. What power is dissipated?", "2 W", "18 W", "24 W", "72 W", "C"),
        ("Which change reduces the resistance of a uniform metal wire, assuming temperature stays constant?", "Increasing its length", "Reducing its cross-sectional area", "Increasing its cross-sectional area", "Replacing it with an insulator", "C"),
        ("A fuse is rated at 5 A. What does this rating primarily indicate?", "The approximate current rating it is designed to protect around", "The voltage it always produces", "The resistance of every household wire", "The power consumed when switched off", "A"),
        ("A circuit has a 9 V supply and a 3 ohm resistor. What is the current?", "0.33 A", "6 A", "27 A", "3 A", "D"),
        ("If three identical bulbs are connected in series and one bulb is removed, what happens to the other bulbs in an ideal circuit?", "They become brighter", "They go out because the circuit is broken", "They remain at the same brightness", "They change into resistors of zero resistance", "B"),
        ("A 2 A current flows through a component with a 5 V potential difference. What power is used?", "2.5 W", "7 W", "10 W", "25 W", "C"),
        ("What is the equivalent resistance of 3 ohms and 6 ohms connected in parallel?", "2 ohms", "3 ohms", "9 ohms", "18 ohms", "A"),
        ("An appliance uses 500 W for 30 minutes. How much energy does it use in kilowatt-hours?", "0.25 kWh", "1 kWh", "15 kWh", "0.5 kWh", "D"),
        ("A 10 ohm resistor carries 0.4 A. What is the voltage across it?", "4 V", "25 V", "10.4 V", "0.04 V", "A"),
    ],

    "Hard": [
        ("A 6 ohm resistor is connected in series with a parallel combination of 6 ohm and 3 ohm resistors. What is the total resistance?", "9 ohms", "8 ohms", "12 ohms", "15 ohms", "B"),
        ("A 12 V source is connected across 4 ohms and 8 ohms in series. What is the voltage across the 8 ohm resistor?", "4 V", "6 V", "8 V", "12 V", "C"),
        ("A 4 ohm resistor and an 8 ohm resistor are connected in parallel across 12 V. What is the total current supplied?", "1.5 A", "3 A", "4.5 A", "6 A", "C"),
        ("A 100 W lamp is used for 5 hours each day for 30 days. How much energy does it use?", "15 kWh", "150 kWh", "5 kWh", "30 kWh", "A"),
        ("A wire has resistance R. If its length is doubled while its material, temperature, and cross-sectional area remain constant, what is its new resistance?", "R/2", "R", "4R", "2R", "D"),
        ("A wire has resistance R. If its length stays the same and its cross-sectional area is doubled, what is its new resistance?", "2R", "R/2", "4R", "R", "B"),
        ("A 12 V battery is connected to two 6 ohm resistors in parallel. What is the total current?", "2 A", "1 A", "4 A", "6 A", "C"),
        ("A 4 ohm resistor carries 2 A for 3 minutes. How much electrical energy is converted to heat?", "2880 J", "960 J", "1440 J", "480 J", "A"),
        ("A 60 W, 120 V lamp is operated at its rated voltage. What is its approximate resistance?", "2 ohms", "120 ohms", "240 ohms", "60 ohms", "C"),
        ("Two resistors of 3 ohms and 6 ohms are connected in series across 18 V. What current flows?", "6 A", "2 A", "3 A", "9 A", "B"),
        ("The 3 ohm and 6 ohm resistors in the previous type of series circuit are instead connected in parallel across 18 V. What is the total current?", "3 A", "6 A", "9 A", "12 A", "C"),
        ("A 10 ohm resistor and a 15 ohm resistor are connected in parallel. What is their equivalent resistance?", "6 ohms", "25 ohms", "12.5 ohms", "5 ohms", "A"),
        ("A device uses 2400 J of energy in 2 minutes. What is its average power?", "1200 W", "40 W", "20 W", "12 W", "B"),
        ("A 24 V supply delivers 3 A to a circuit. What is the circuit's equivalent resistance?", "72 ohms", "8 ohms", "21 ohms", "0.125 ohms", "B"),
        ("A 5 ohm resistor and a 10 ohm resistor are in series across 30 V. What is the power dissipated by the 10 ohm resistor?", "20 W", "30 W", "40 W", "60 W", "D"),
        ("A 6 ohm resistor is connected in parallel with a 3 ohm resistor across 6 V. What current flows through the 3 ohm resistor?", "1 A", "2 A", "3 A", "6 A", "B"),
        ("A circuit has a 12 V source and two series resistors of 2 ohms and 4 ohms. What is the power dissipated by the 2 ohm resistor?", "2 W", "4 W", "8 W", "16 W", "C"),
        ("A 2 ohm resistor, a 3 ohm resistor, and a 6 ohm resistor are connected in parallel. What is the equivalent resistance?", "1 ohm", "2 ohms", "3 ohms", "11 ohms", "A"),
        ("An appliance rated 1000 W operates at 250 V. What current does it draw at its rated operating point?", "0.25 A", "2 A", "5 A", "4 A", "D"),
        ("A current of 0.5 A flows through a 20 ohm resistor for 10 seconds. How much heat energy is generated?", "10 J", "50 J", "100 J", "200 J", "C"),
        ("A 12 V source is connected across a 2 ohm resistor in series with a 4 ohm parallel 12 ohm combination. What is the total resistance?", "5 ohms", "6 ohms", "8 ohms", "14 ohms", "C"),
        ("A 12 V battery is connected to a 2 ohm resistor in series with a parallel combination of 6 ohms and 3 ohms. What is the total current?", "2 A", "3 A", "4 A", "6 A", "B"),
        ("A 12 V supply is connected across 4 ohms and 12 ohms in parallel. What is the current through the 4 ohm resistor?", "1 A", "2 A", "3 A", "4 A", "C"),
        ("A resistor dissipates 18 W when 3 A flows through it. What is its resistance?", "2 ohms", "6 ohms", "9 ohms", "54 ohms", "A"),
        ("A 2 kW heater operates for 45 minutes. What energy does it consume?", "0.75 kWh", "1.5 kWh", "2 kWh", "90 kWh", "B"),
        ("A 4 ohm resistor is connected across 8 V. If the voltage is increased to 16 V and resistance remains constant, what is the new power?", "16 W", "32 W", "64 W", "8 W", "C"),
        ("A 3 ohm resistor and a 6 ohm resistor are in parallel. This combination is connected in series with a 2 ohm resistor. What is the total resistance?", "2 ohms", "4 ohms", "5 ohms", "8 ohms", "B"),
        ("A 12 V source is connected to a 4 ohm resistor. If the resistor is replaced with an 8 ohm resistor, what happens to the current?", "It doubles", "It stays the same", "It becomes zero", "It halves", "D"),
        ("A 6 ohm resistor carries 2 A. How much energy does it dissipate in 1 minute?", "720 J", "1440 J", "360 J", "120 J", "B"),
        ("A 12 V supply is connected across a 6 ohm resistor. What is the power dissipated?", "2 W", "12 W", "24 W", "72 W", "C"),
    ],
}


def normalize(text):
    return " ".join(text.strip().lower().split())


def main():
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DATABASE_PATH}\n"
            "Run this script from your project setup with adaptive_learning.db in the project root."
        )

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
            """
            SELECT id, difficulty
            FROM quizzes
            WHERE lesson_id = ?
            """,
            (lesson_id,),
        )
        quizzes = cursor.fetchall()

        quiz_by_difficulty = {}
        for quiz_id, difficulty in quizzes:
            key = str(difficulty).strip().capitalize()
            if key in {"Easy", "Medium", "Hard"}:
                if key in quiz_by_difficulty:
                    raise RuntimeError(
                        f"Multiple {key} quizzes found for '{LESSON_TITLE}'."
                    )
                quiz_by_difficulty[key] = quiz_id

        missing = {"Easy", "Medium", "Hard"} - set(quiz_by_difficulty)
        if missing:
            raise RuntimeError(
                f"Missing difficulty quizzes for '{LESSON_TITLE}': {sorted(missing)}"
            )

        inserted_total = 0

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
            for question in QUESTIONS[difficulty]:
                if current_count + added >= TARGET_QUESTIONS:
                    break

                text, option_a, option_b, option_c, option_d, answer = question
                normalized_question = normalize(text)

                if normalized_question in existing:
                    continue

                if answer not in {"A", "B", "C", "D"}:
                    raise ValueError(f"Invalid answer key: {answer!r} for {text!r}")

                cursor.execute(
                    """
                    INSERT INTO questions
                    (quiz_id, question, option_a, option_b, option_c, option_d, correct_answer)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        quiz_id,
                        text,
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
                    f"{difficulty} has only {final_count} questions. "
                    "More unique questions are needed; transaction will be rolled back."
                )

            inserted_total += added

        connection.commit()
        print(f"\nSuccess! Added {inserted_total} questions to '{LESSON_TITLE}'.")
        print("Other lessons and Social Science were not modified.")

    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


if __name__ == "__main__":
    main()
