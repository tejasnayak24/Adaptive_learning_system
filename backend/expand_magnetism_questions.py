
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"
LESSON_TITLE = "Magnetism"
TARGET_QUESTIONS = 30

QUESTIONS = {
    "Easy": [
        ("Which material is strongly attracted to a magnet?", "Wood", "Iron", "Plastic", "Glass", "B"),
        ("What are the two poles of a magnet?", "Left and right", "Top and bottom", "North and south", "Positive and negative", "C"),
        ("What happens when two north poles are brought together?", "They repel", "They attract", "They disappear", "They become neutral immediately", "A"),
        ("Which material is generally not attracted to an ordinary magnet?", "Iron", "Nickel", "Cobalt", "Wood", "D"),
        ("Where is the magnetic force of a bar magnet usually strongest?", "At its center", "At its poles", "Equally everywhere", "Only outside the magnet", "B"),
        ("Which instrument uses a magnetized needle to show direction?", "Thermometer", "Barometer", "Compass", "Ammeter", "C"),
        ("What happens when a north pole and a south pole are brought together?", "They attract", "They repel", "They lose all their magnetism", "They become electric charges", "A"),
        ("Which of these is a natural magnet?", "Plastic", "Copper wire", "Glass", "Lodestone", "D"),
        ("What is the region around a magnet where magnetic force acts called?", "Electric circuit", "Magnetic field", "Friction zone", "Sound field", "B"),
        ("Can a single isolated magnetic pole normally be obtained by cutting a bar magnet in half?", "Yes, the north pole separates completely", "Yes, the south pole separates completely", "No, each piece has both poles", "Only by using a compass", "C"),
        ("Which device helps identify the direction of a magnetic field at a point?", "Small compass", "Stopwatch", "Thermometer", "Measuring cylinder", "A"),
        ("Which of the following is a magnetic material?", "Paper", "Rubber", "Dry wood", "Nickel", "D"),
        ("What are magnetic field lines around a bar magnet conventionally directed outside the magnet?", "South to north", "North to south", "East to west only", "In random directions", "B"),
        ("What happens when a magnet is freely suspended?", "It always points east", "It points vertically down", "It tends to align north-south", "It stops having poles", "C"),
        ("Which object can be attracted by a magnet?", "Iron nail", "Plastic ruler", "Paper sheet", "Wooden stick", "A"),
        ("What is the usual shape of a common school-lab bar magnet?", "Circular sheet only", "Long rectangular bar", "Hollow glass tube", "Flexible rubber strip", "B"),
        ("What do like magnetic poles do?", "Attract", "Merge", "Repel", "Cancel gravity", "C"),
        ("Which of these is commonly used to make a permanent magnet?", "Soft cotton", "Paper", "Plain wood", "Hardened steel", "D"),
        ("What is the magnetic compass needle made to respond to?", "Magnetic field", "Sound waves", "Water pressure", "Light intensity", "A"),
        ("Which statement about magnetic field lines is correct?", "They cross each other at every pole", "They never intersect one another", "They exist only inside iron", "They are always straight", "B"),
        ("What happens if a bar magnet is broken into two pieces?", "Only one piece remains magnetic", "Both pieces lose all magnetism", "Each piece has a north and a south pole", "Each piece has only a north pole", "C"),
        ("Which pair of poles will repel each other?", "North and south", "South and north", "Opposite poles", "North and north", "D"),
        ("Which metal is attracted to a magnet?", "Aluminium foil is always strongly attracted", "Iron", "Copper", "Silver", "B"),
        ("What is the purpose of a magnetic compass?", "To determine direction", "To measure mass", "To measure temperature", "To measure current directly", "A"),
        ("Which of these can weaken a permanent magnet?", "Keeping it away from heat", "Using a protective case", "Excessive heating", "Storing it carefully", "C"),
        ("What is the name of the end of a freely suspended magnet that points approximately toward geographic north?", "South-seeking pole", "Neutral pole", "Center pole", "North-seeking pole", "D"),
        ("Which arrangement can show the pattern of a bar magnet's field?", "Iron filings on paper above the magnet", "Sugar dissolved in water", "A thermometer in air", "A ruler beside a bulb", "A"),
        ("What is a temporary magnet?", "A magnet that must be made of plastic", "A material that becomes magnetic under suitable conditions and may lose magnetism afterward", "A magnet with only one pole", "A magnet that never responds to fields", "B"),
        ("Which material is commonly used as a core in an electromagnet?", "Glass", "Wood", "Soft iron", "Rubber", "C"),
        ("What happens to a compass needle near a strong magnet?", "It may deflect", "It always melts", "It becomes a battery", "It loses its mass", "A"),
    ],

    "Medium": [
        ("Why do magnetic field lines never cross one another?", "They have no direction", "The magnetic field at a point has a unique direction", "They exist only at the poles", "They always form squares", "B"),
        ("Which change generally makes an electromagnet stronger?", "Removing the current", "Removing its core in every case", "Increasing the current through its coil", "Cutting the wire into disconnected pieces", "C"),
        ("What happens to a compass needle when it is placed in a magnetic field?", "It tends to align with the local field direction", "It always points vertically", "It stops responding to magnetic forces", "It becomes permanently demagnetized immediately", "A"),
        ("Why is soft iron often used in electromagnets?", "It is a perfect insulator", "It cannot become magnetized", "It is always permanently magnetized", "It magnetizes and demagnetizes relatively easily", "D"),
        ("What is the direction of magnetic field lines inside a bar magnet?", "North to south", "South to north", "They have no direction", "They run only outside the magnet", "B"),
        ("What happens when the current through an electromagnet's coil is reversed?", "The magnet becomes nonmagnetic permanently", "Its strength must become infinite", "Its magnetic poles reverse", "Its coil stops conducting electricity", "C"),
        ("Which factor can increase the strength of an electromagnet?", "Increasing the number of coil turns, with other factors suitably controlled", "Removing all turns of wire", "Disconnecting the power supply", "Replacing the iron core with paper", "A"),
        ("Why should a compass be kept away from large magnets when finding geographic direction?", "Magnets make the compass measure temperature", "A magnet can deflect its needle", "A compass works only underwater", "The needle becomes a source of light", "B"),
        ("Which statement best describes magnetic field strength around a typical bar magnet?", "It is always zero near the poles", "It is identical at every point", "It is generally stronger near the poles", "It exists only at the center", "C"),
        ("What happens to an iron nail placed inside a current-carrying coil?", "It may become magnetized", "It turns into copper", "It loses all mass", "It blocks every electric current", "A"),
        ("Which is a practical use of an electromagnet?", "A wooden ruler", "A glass lens", "A paper notebook", "A scrapyard lifting crane", "D"),
        ("What is the main difference between a permanent magnet and a typical electromagnet?", "A permanent magnet needs current continuously", "An electromagnet's field can be controlled by its current", "A permanent magnet has no poles", "An electromagnet cannot attract iron", "B"),
        ("Which change is most likely to weaken an electromagnet?", "Increasing its coil turns", "Increasing its current within safe limits", "Switching off the current", "Using a suitable magnetic core", "C"),
        ("What do iron filings reveal around a bar magnet?", "An approximate pattern of the magnetic field", "The electric current in amperes", "The magnet's exact temperature", "The magnet's mass in kilograms", "A"),
        ("Two bar magnets attract each other. Which conclusion is definitely consistent with this observation?", "Both facing poles must be north", "The magnets must have identical poles facing", "Magnetic force cannot act between them", "The facing poles are opposite poles", "D"),
        ("What is the role of the core in many electromagnets?", "To prevent the coil from carrying current", "To strengthen the magnetic field", "To convert the coil into a permanent insulator", "To remove both magnetic poles", "B"),
        ("Why can a magnet attract an unmagnetized iron object?", "Iron contains no magnetic domains", "Iron is always positively charged", "The magnet can induce magnetic alignment in the iron", "Gravity disappears between them", "C"),
        ("What is the effect of increasing the distance from a small bar magnet?", "Its magnetic influence generally becomes weaker", "Its field always becomes stronger", "Its poles exchange places automatically", "Its field becomes identical everywhere", "A"),
        ("Which statement about magnetic poles is correct?", "A north pole can exist alone in an ordinary broken magnet", "South poles do not produce fields", "Every magnet must have exactly four poles", "Magnetic poles occur in north-south pairs in ordinary magnets", "D"),
        ("What happens when a current-carrying wire is placed near a compass?", "The compass always points straight down", "The magnetic field from the current may deflect the needle", "The wire becomes a permanent magnet in every case", "The compass stops measuring direction forever", "B"),
        ("Which setup is most suitable for testing whether current creates a magnetic field?", "A ruler and a glass of water", "A thermometer beside a battery", "A compass near a current-carrying wire", "A paper clip placed on wood only", "C"),
        ("Why are magnetic materials attracted to some regions near a magnet?", "Their magnetic domains can respond to the external field", "All materials contain free north poles", "The magnet removes their electrons completely", "The material must be electrically charged", "A"),
        ("What is the effect of adding more turns to an electromagnet's coil while keeping current and core conditions comparable?", "It always removes the field", "It makes the coil an insulator", "It reverses current automatically", "It generally increases the field strength", "D"),
        ("Which action is most appropriate to reduce interference when using a compass?", "Place it directly against a strong magnet", "Move it away from magnetic objects and current-carrying wires", "Surround it with iron filings", "Put it beside a loudspeaker with a strong magnet", "B"),
        ("What happens to the magnetic field of a simple electromagnet when its power supply is disconnected?", "It generally disappears or becomes much weaker", "It becomes infinitely strong", "Its poles become electric charges", "It always remains as strong as before", "A"),
        ("Which material is commonly used for making strong permanent magnets?", "Soft paper", "Wet clay", "Suitable hard magnetic alloys", "Pure rubber", "C"),
        ("How can the poles of a solenoid be identified?", "By measuring its temperature only", "By checking its weight only", "By looking at the wire's colour", "By using a compass or the current direction and coil winding", "D"),
        ("Which statement about magnetic field lines is correct?", "They terminate at random points in space", "Outside a bar magnet, they run from north to south", "They always point toward the north pole everywhere", "They cannot form closed loops", "B"),
        ("Why is a horseshoe magnet often useful for lifting iron objects?", "It has no magnetic field", "It is made from wood", "Its poles are close together, concentrating a strong field in the gap", "It works only when connected to a battery", "C"),
        ("What happens if an electromagnet's coil has no current flowing through it?", "Its current-produced magnetic field is absent, apart from any residual magnetism", "Its magnetic field must double", "It becomes a battery", "Its resistance becomes negative", "A"),
    ],

    "Hard": [
        ("An ideal electromagnet has 200 turns and carries 2 A. If the turns are doubled and current remains unchanged, how does its ampere-turn value change?", "It halves", "It doubles", "It remains the same", "It becomes zero", "B"),
        ("A solenoid's current is reversed while its winding stays unchanged. What happens to its north and south poles?", "They both disappear permanently", "They remain unchanged in all cases", "They interchange", "They turn into electric charges", "C"),
        ("A coil has 300 turns and carries 0.5 A. What is its ampere-turn value?", "150 ampere-turns", "600 ampere-turns", "300.5 ampere-turns", "30 ampere-turns", "A"),
        ("Why does inserting a suitable soft-iron core usually strengthen a solenoid's field?", "It stops the current completely", "It removes the coil turns", "It changes iron into a permanent battery", "The core's magnetic response increases the field", "D"),
        ("A compass is placed at different points around a bar magnet. What does the needle indicate at each point?", "The electric resistance at that point", "The local direction of the magnetic field", "The magnet's mass", "The local sound frequency", "B"),
        ("A coil has 100 turns and carries 3 A. A second comparable coil has 150 turns and carries 2 A. Which has the greater ampere-turn value?", "The first coil", "The second coil", "Both have the same ampere-turn value", "Neither produces a field", "C"),
        ("Why should an electromagnet's coil wire be insulated between adjacent turns?", "To reduce unwanted short circuits between turns", "To make all turns electrically disconnected from the supply", "To prevent any magnetic field", "To make the core nonmagnetic", "A"),
        ("An iron core is removed from a powered solenoid. What is the most likely effect?", "The magnetic field becomes infinitely strong", "The current must reverse", "The solenoid becomes a permanent magnet in every case", "The field generally becomes weaker", "D"),
        ("A magnetic field is represented by closely spaced field lines in a diagram. What does this convention indicate?", "Lower temperature", "A stronger magnetic field", "A greater electric resistance", "A lower mass density", "B"),
        ("Two identical solenoids have the same core and number of turns. One carries 1 A and the other 3 A. Under comparable unsaturated conditions, what is expected?", "The 1 A solenoid has three times the field", "Both fields must be zero", "The 3 A solenoid has a stronger field, roughly proportional to current", "Both fields must be exactly identical", "C"),
        ("Why is it incorrect to say that cutting a bar magnet produces an isolated north pole and an isolated south pole?", "Each fragment ordinarily forms its own north and south poles", "Magnetism is destroyed by any cut", "Only the longer fragment remains magnetic", "Magnetic poles are electrical insulators", "A"),
        ("A coil's number of turns is tripled while its current is reduced to one-third. In an ideal long-solenoid model, what happens to its field strength?", "It triples", "It becomes one-third", "It becomes nine times greater", "It remains approximately unchanged", "D"),
        ("Which change is most likely to demagnetize an ordinary permanent magnet?", "Storing it carefully with keepers where appropriate", "Strong heating or severe mechanical shocks", "Keeping it away from strong fields", "Cleaning its surface with a cloth", "B"),
        ("A current-carrying solenoid is viewed from one end. The current around that end appears anticlockwise. Which pole is that end, using the right-hand rule?", "South pole", "Neither pole", "North pole", "Both north and south simultaneously", "C"),
        ("A solenoid has 500 turns and carries 0.4 A. What is its ampere-turn value?", "200 ampere-turns", "1250 ampere-turns", "500.4 ampere-turns", "20 ampere-turns", "A"),
        ("Which statement about the magnetic field inside an ideal long solenoid is most accurate?", "It is zero everywhere", "It points in random directions", "It is strongest only at one end", "It is approximately uniform away from the ends", "D"),
        ("A powered electromagnet attracts iron clips. The power is switched off, and the clips fall away. What best explains this?", "Gravity has stopped acting", "The coil's current-produced magnetic field has largely disappeared", "The clips have lost their mass", "The circuit has generated extra current", "B"),
        ("Two coils have equal ampere-turn values but different shapes and cores. Must their magnetic fields be identical?", "Yes, ampere-turns alone determine every field exactly", "Yes, regardless of core material", "No, geometry and core properties also affect the field", "No, because coils cannot create magnetic fields", "C"),
        ("Which action can reverse an electromagnet's poles without changing its physical winding?", "Reverse the current through the coil", "Increase the wire's length only", "Paint the core", "Remove the switch label", "A"),
        ("Why can magnetic field lines not intersect in a standard magnetic field diagram?", "They only exist in a vacuum", "They always form triangles", "They carry electric charge", "An intersection would assign two directions to the field at one point", "D"),
        ("A coil has 250 turns and carries 1.2 A. What is its ampere-turn value?", "120 ampere-turns", "300 ampere-turns", "250 ampere-turns", "500 ampere-turns", "B"),
        ("A solenoid's turns and core remain unchanged, but current increases from 0.5 A to 1.5 A. In the linear operating range, how does the field strength change?", "It becomes one-third", "It remains unchanged", "It becomes approximately three times as strong", "It becomes zero", "C"),
        ("Which description of a magnetic keeper is correct?", "A piece of soft iron placed across magnet poles to help reduce demagnetization during storage", "A battery used to reverse current", "A plastic cover that generates a field", "A device that measures electric power", "A"),
        ("A bar magnet is brought near an unmagnetized iron nail. Why can the nail be attracted even without an initial permanent magnetization?", "The nail produces no magnetic response", "The nail must already have a north pole only", "The nail's electric charge always causes attraction", "The external field induces magnetic alignment in the nail", "D"),
        ("Two comparable electromagnets have the same current and core material, but one has twice as many turns. What is generally expected if other conditions remain comparable?", "The one with fewer turns must be stronger", "The one with twice as many turns generally produces a stronger field", "Both fields must be zero", "The field is independent of turns in all cases", "B"),
        ("Which rule is commonly used to determine the magnetic field direction around a straight current-carrying wire?", "Newton's third law", "Snell's law", "Right-hand thumb rule", "Ohm's law", "C"),
        ("A solenoid has 400 turns and carries 0.25 A. What is its ampere-turn value?", "100 ampere-turns", "1600 ampere-turns", "400.25 ampere-turns", "25 ampere-turns", "A"),
        ("What is the most accurate reason that an electromagnet is useful in a relay?", "It must stay magnetized forever", "It does not need electric current", "It cannot exert force on iron", "Its magnetic action can be switched by controlling current", "D"),
        ("A magnet attracts one end of an object. Does this alone prove that the object is itself a permanent magnet?", "Yes, every attracted object is a permanent magnet", "No, an unmagnetized ferromagnetic object can also be attracted", "Yes, attraction occurs only between permanent magnets", "No, because magnets never attract objects", "B"),
        ("Which combination is most likely to produce a stronger electromagnet, within safe operating limits and comparable geometry?", "Fewer turns, lower current, and no suitable core", "No current and a plastic core", "More coil turns, greater current, and a suitable magnetic core", "A disconnected coil with broken wire", "C"),
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
        quiz_rows = cursor.fetchall()

        quiz_by_difficulty = {}
        for quiz_id, difficulty in quiz_rows:
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

                question, a, b, c, d, answer = item
                key = normalize(question)

                if key in existing:
                    continue

                if answer not in {"A", "B", "C", "D"}:
                    raise ValueError(f"Invalid answer key: {answer} for {question}")

                cursor.execute(
                    """
                    INSERT INTO questions
                    (quiz_id, question, option_a, option_b, option_c, option_d, correct_answer)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (quiz_id, question, a, b, c, d, answer),
                )

                existing.add(key)
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
