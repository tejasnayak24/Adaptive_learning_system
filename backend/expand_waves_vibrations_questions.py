
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"
LESSON_TITLE = "Waves and Vibrations"
TARGET_QUESTIONS = 30

QUESTIONS = {
    "Easy": [
        ("What is a vibration?", "A repeated to-and-fro motion about a position", "A permanent change in mass", "A type of chemical reaction", "A stationary object with no motion", "A"),
        ("What produces sound in most everyday cases?", "Light rays", "Vibrating objects", "Magnetic poles only", "Static objects", "B"),
        ("Which type of wave requires a material medium to travel?", "Radio wave", "Visible light wave", "Sound wave", "X-ray", "C"),
        ("What is one complete vibration called?", "Amplitude", "Wavelength", "Wave speed", "One oscillation", "D"),
        ("What is frequency?", "The number of complete oscillations per second", "The maximum displacement only", "The distance travelled by an object", "The mass of a vibrating object", "A"),
        ("What is the SI unit of frequency?", "Metre", "Hertz", "Second", "Newton", "B"),
        ("What is amplitude in an oscillation?", "The time for one cycle", "The number of cycles per second", "The maximum displacement from the equilibrium position", "The distance between two crests", "C"),
        ("What is the time period of an oscillation?", "The number of cycles per second", "The wave's height only", "The wave's speed", "The time taken for one complete oscillation", "D"),
        ("Which formula relates frequency f and time period T?", "f = 1/T", "f = T", "f = T²", "f = 1 + T", "A"),
        ("Which unit is used for wavelength?", "Hertz", "Metre", "Second", "Decibel", "B"),
        ("What is the highest point of a transverse wave called?", "Trough", "Rarefaction", "Crest", "Compression", "C"),
        ("What is the lowest point of a transverse wave called?", "Crest", "Compression", "Equilibrium", "Trough", "D"),
        ("In a longitudinal wave, what is a compression?", "A region where particles are closer together", "A region where particles are farther apart", "A point where particles disappear", "A place with no energy transfer", "A"),
        ("In a longitudinal wave, what is a rarefaction?", "A region of maximum particle crowding", "A region where particles are farther apart", "A complete vibration", "The highest point of a transverse wave", "B"),
        ("Which wave property is measured in hertz?", "Wavelength", "Amplitude", "Frequency", "Wave speed", "C"),
        ("Can sound travel through a perfect vacuum?", "Yes, at the speed of light", "Yes, but only at low frequency", "Only if it is loud", "No, sound needs a material medium", "D"),
        ("Which of these is a transverse wave?", "A wave on a stretched string", "Sound travelling through air", "A compression wave in a spring", "A pressure wave in a gas", "A"),
        ("Which of these is generally a longitudinal wave in air?", "A light wave", "A sound wave", "A radio wave", "An X-ray wave", "B"),
        ("What does a wave transfer from one place to another?", "Matter permanently in every case", "The source itself", "Energy", "The medium's entire mass", "C"),
        ("What happens when the frequency of a sound increases, under ordinary listening conditions?", "Its pitch generally becomes higher", "Its pitch always becomes lower", "Its speed in air doubles", "It becomes inaudible in every case", "A"),
        ("What is the usual approximate range of human hearing for a healthy young person?", "0–100 Hz", "20 Hz to 20,000 Hz", "2000 Hz to 200,000 Hz", "Only above 20,000 Hz", "B"),
        ("What is ultrasound?", "Sound below 20 Hz", "Sound that cannot travel through solids", "Sound above approximately 20,000 Hz", "Any sound with zero amplitude", "C"),
        ("What is infrasound?", "Sound above 20,000 Hz", "Sound with a frequency of exactly 1000 Hz", "Sound that travels only in water", "Sound below approximately 20 Hz", "D"),
        ("What is the approximate speed of sound in air at room temperature?", "About 343 m/s", "About 3 × 10⁸ m/s", "About 30 m/s", "About 1500 m/s", "A"),
        ("What determines the pitch of a sound?", "Amplitude alone", "Frequency", "Distance alone", "The object's mass alone", "B"),
        ("What mainly determines how loud a sound seems, for a given listener and frequency?", "Wavelength alone", "Time period alone", "Amplitude and sound intensity", "The colour of the source", "C"),
        ("What is a wave's wavelength?", "The time taken for one cycle", "The number of oscillations per second", "The maximum displacement only", "The distance between successive points in the same phase", "D"),
        ("What is the equilibrium position of an oscillator?", "Its central position where the net restoring force is zero in a simple oscillator", "Its position of maximum displacement", "The position where its speed must always be zero", "The farthest point of the wave", "A"),
        ("What is a mechanical wave?", "A wave that always travels in vacuum", "A wave that requires a material medium", "A wave that carries matter permanently", "A wave with no energy", "B"),
        ("Which property is calculated using wave speed = frequency × wavelength?", "Mass", "Force", "Wave speed", "Pressure", "C"),
    ],
    "Medium": [
        ("A wave has frequency 5 Hz. What is its time period?", "5 s", "0.2 s", "2.5 s", "10 s", "B"),
        ("An oscillator completes 40 cycles in 8 seconds. What is its frequency?", "5 Hz", "8 Hz", "32 Hz", "0.2 Hz", "A"),
        ("A wave has frequency 10 Hz and wavelength 3 m. What is its speed?", "13 m/s", "3.3 m/s", "30 m/s", "0.3 m/s", "C"),
        ("A sound wave travels at 340 m/s and has frequency 170 Hz. What is its wavelength?", "0.5 m", "1 m", "4 m", "2 m", "D"),
        ("A vibrating object has a time period of 0.04 s. What is its frequency?", "25 Hz", "40 Hz", "0.04 Hz", "4 Hz", "A"),
        ("A wave travels at 24 m/s and has a frequency of 6 Hz. What is its wavelength?", "4 Hz", "4 m", "18 m", "144 m", "B"),
        ("A wave has wavelength 0.5 m and speed 200 m/s. What is its frequency?", "100 Hz", "200 Hz", "400 Hz", "50 Hz", "C"),
        ("A tuning fork vibrates at 256 Hz. How many complete vibrations does it make in 2 seconds?", "128", "256", "64", "512", "D"),
        ("A wave has frequency 20 Hz. How many cycles occur in 3 seconds?", "60", "23", "6.7", "40", "A"),
        ("A wave travels 120 m in 4 seconds. What is its speed?", "30 Hz", "30 m/s", "480 m/s", "0.033 m/s", "B"),
        ("A wave travels at 12 m/s and has wavelength 2 m. What is its frequency?", "24 Hz", "6 m", "6 Hz", "10 Hz", "C"),
        ("A sound wave has a frequency of 500 Hz and travels at 340 m/s. What is its wavelength?", "0.34 m", "1.47 m", "170 m", "0.68 m", "B"),
        ("What happens to the frequency of a wave if its period doubles?", "It doubles", "It remains the same", "It becomes half", "It becomes four times as large", "C"),
        ("Two waves travel through the same medium at the same speed. Wave A has twice the frequency of wave B. How do their wavelengths compare?", "A has twice B's wavelength", "A has four times B's wavelength", "They have equal wavelengths", "A has half B's wavelength", "D"),
        ("A wave has a wavelength of 4 m and frequency 3 Hz. What is its speed?", "12 m/s", "7 m/s", "1.33 m/s", "0.75 m/s", "A"),
        ("A source completes 150 oscillations in 30 seconds. What is its frequency?", "30 Hz", "5 Hz", "150 Hz", "0.2 Hz", "B"),
        ("A wave has a period of 0.01 s. What is its frequency?", "10 Hz", "0.01 Hz", "100 Hz", "1000 Hz", "C"),
        ("A wave travels at 15 m/s and has a wavelength of 0.75 m. What is its frequency?", "11.25 Hz", "15 Hz", "0.05 Hz", "20 Hz", "D"),
        ("A sound wave travels at 330 m/s and has a wavelength of 1.1 m. What is its frequency?", "300 Hz", "330 Hz", "363 Hz", "30 Hz", "A"),
        ("If a wave's frequency remains constant but its speed doubles in a different medium, what happens to its wavelength?", "It halves", "It doubles", "It remains constant", "It becomes zero", "B"),
        ("A vibrating object has a frequency of 4 Hz. How long does it take to complete 20 vibrations?", "0.2 s", "4 s", "5 s", "80 s", "C"),
        ("A wave has speed 50 m/s and frequency 25 Hz. What is its wavelength?", "1250 m", "2.5 m", "0.5 m", "2 m", "D"),
        ("Which change increases the energy carried by a wave on a string, assuming other conditions are comparable?", "Increasing its amplitude", "Making its amplitude zero", "Stopping the vibration", "Removing the medium", "A"),
        ("What happens to the speed of sound when it moves from air into water?", "It always becomes zero", "It generally increases", "It always decreases to half", "It becomes the speed of light", "B"),
        ("An echo is heard 2 seconds after a sound is produced. If sound speed is 340 m/s, how far away is the reflecting surface?", "680 m", "170 m", "340 m", "85 m", "C"),
        ("A wave has frequency 50 Hz and period 0.02 s. Which statement is correct?", "Its period should be 50 s", "Its frequency should be 0.02 Hz", "The values contradict each other", "The frequency and period are consistent", "D"),
        ("A wave travels 600 m in 2 seconds. If its frequency is 100 Hz, what is its wavelength?", "3 m", "6 m", "300 m", "0.3 m", "A"),
        ("A sound wave has wavelength 0.85 m and speed 340 m/s. What is its frequency?", "289 Hz", "400 Hz", "340 Hz", "200 Hz", "B"),
        ("What is the main difference between a transverse and a longitudinal mechanical wave?", "Only transverse waves transfer energy", "Only longitudinal waves require a medium", "Particle vibration is perpendicular to propagation in transverse waves and parallel in longitudinal waves", "Longitudinal waves cannot travel through solids", "C"),
        ("A wave's frequency is 8 Hz. How many cycles occur in 0.5 seconds?", "16", "8", "2", "4", "D"),
    ],
    "Hard": [
        ("A wave travels at 360 m/s with frequency 240 Hz. What is its wavelength?", "1.5 m", "0.67 m", "600 m", "120 m", "A"),
        ("A sound wave has wavelength 0.8 m and speed 320 m/s. What is its frequency?", "256 Hz", "400 Hz", "40 Hz", "0.0025 Hz", "B"),
        ("A source vibrates at 50 Hz. How many oscillations occur in 2.4 minutes?", "120", "2400", "7200", "720", "D"),
        ("A wave has frequency 25 Hz and wavelength 12 m. What is its speed?", "37 m/s", "2.08 m/s", "300 m/s", "0.48 m/s", "C"),
        ("A sound echo returns after 1.5 seconds. If the speed of sound is 340 m/s, how far away is the reflecting surface?", "255 m", "510 m", "340 m", "170 m", "A"),
        ("A wave travels at 48 m/s and has a wavelength of 0.6 m. What is its frequency?", "28.8 Hz", "80 Hz", "48 Hz", "0.0125 Hz", "B"),
        ("A wave has frequency 200 Hz and speed 1500 m/s in a liquid. What is its wavelength?", "0.075 m", "3 m", "7.5 m", "0.133 m", "C"),
        ("A source makes 900 oscillations in 3 minutes. What is its frequency?", "300 Hz", "5 Hz", "15 Hz", "0.2 Hz", "B"),
        ("A wave has frequency 60 Hz and wavelength 2.5 m. What is its speed?", "24 m/s", "62.5 m/s", "150 m/s", "1500 m/s", "C"),
        ("A wave's speed is 20 m/s and its frequency is 4 Hz. If the frequency is increased to 8 Hz in the same medium, what is the new wavelength?", "10 m", "5 m", "2.5 m", "40 m", "B"),
        ("A sound travels 1020 m in 3 seconds. What is its speed?", "340 m/s", "3060 m/s", "1023 m/s", "300 m/s", "A"),
        ("A wave has a time period of 0.005 s and wavelength 1.7 m. What is its speed?", "170 m/s", "34 m/s", "850 m/s", "340 m/s", "D"),
        ("A sound wave has frequency 250 Hz. If sound speed is 350 m/s, what is its wavelength?", "0.7 m", "1.4 m", "87,500 m", "600 m", "A"),
        ("A wave travels at 100 m/s and has frequency 20 Hz. How many wavelengths fit into a 50 m distance?", "10", "5", "20", "40", "B"),
        ("A source vibrates at 12.5 Hz. What is its period?", "12.5 s", "0.08 s", "0.8 s", "1.25 s", "B"),
        ("A wave has wavelength 3 m and frequency 15 Hz. How far does it travel in 4 seconds?", "45 m", "60 m", "180 m", "12 m", "C"),
        ("A sound wave travels at 330 m/s with frequency 1100 Hz. What is its wavelength?", "3 m", "0.3 m", "0.03 m", "330 m", "B"),
        ("An echo is heard 0.8 seconds after a sound is made. If sound travels at 340 m/s, how far away is the reflecting wall?", "136 m", "272 m", "340 m", "170 m", "A"),
        ("A wave has a frequency of 75 Hz and wavelength 4 m. What is its speed?", "18.75 m/s", "79 m/s", "300 m/s", "150 m/s", "C"),
        ("A vibrating object completes 240 cycles in 8 seconds. What is its period?", "30 s", "8 s", "0.3 s", "1/30 s", "D"),
        ("A wave has speed 600 m/s and wavelength 2 m. What is its frequency?", "300 Hz", "1200 Hz", "30 Hz", "600 Hz", "A"),
        ("If the amplitude of a wave is doubled, what happens to its energy in an idealized wave model where energy is proportional to amplitude squared?", "It doubles", "It becomes four times as large", "It halves", "It remains unchanged", "B"),
        ("A sound source emits a 500 Hz tone. If the sound travels at 340 m/s, how long is one wavelength?", "0.34 m", "1.47 m", "0.68 m", "170 m", "C"),
        ("A wave has speed 24 m/s and wavelength 3 m. How long does it take to travel 120 m?", "5 s", "10 s", "15 s", "20 s", "A"),
        ("A sound travels from a source to a wall 255 m away and back. If its speed is 340 m/s, how long until the echo returns?", "0.75 s", "1.5 s", "2 s", "3 s", "B"),
        ("A wave has a period of 0.02 s and speed 15 m/s. What is its wavelength?", "0.3 m", "75 m", "7.5 m", "30 m", "A"),
        ("A source emits 1200 vibrations in 20 seconds. What is its frequency?", "24 Hz", "60 Hz", "120 Hz", "600 Hz", "B"),
        ("A wave travels at 200 m/s with wavelength 5 m. How many complete cycles pass a point in 10 seconds?", "40", "100", "200", "400", "C"),
        ("A wave has frequency 125 Hz and speed 500 m/s. What is its wavelength?", "0.25 m", "2 m", "4 m", "625 m", "B"),
        ("A wave travels 900 m in 5 seconds. If its wavelength is 3 m, what is its frequency?", "30 Hz", "60 Hz", "90 Hz", "300 Hz", "B"),
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
                    f"{difficulty} has only {final_count} questions; transaction will roll back."
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
