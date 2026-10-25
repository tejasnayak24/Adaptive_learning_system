
import sqlite3
from pathlib import Path
import re

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"
LESSON_TITLE = "Sound and Its Properties"
TARGET_QUESTIONS = 30

QUESTIONS = {
    "Easy": [
        ("What produces sound?", "Vibrating objects", "Objects that never move", "Shadows", "Only magnets", "A"),
        ("Which organ helps humans hear sounds?", "Lungs", "Ears", "Eyes", "Nose", "B"),
        ("Can sound travel through a vacuum?", "Yes, easily", "Only at night", "No, it requires a material medium", "Only if light is present", "C"),
        ("Which of these is a unit of frequency?", "Metre", "Joule", "Newton", "Hertz", "D"),
        ("What is the approximate frequency range of human hearing for a healthy young person?", "20 Hz to 20,000 Hz", "0 Hz to 5 Hz", "100,000 Hz to 1,000,000 Hz", "Only 500 Hz to 1,000 Hz", "A"),
        ("What determines the pitch of a sound most directly?", "Amplitude", "Frequency", "Distance alone", "Echo duration", "B"),
        ("A sound with a higher frequency generally has:", "Lower pitch", "No pitch", "Higher pitch", "No vibration", "C"),
        ("What is the amplitude of a sound wave associated with?", "Its colour", "Its speed only", "Its direction only", "Its loudness", "D"),
        ("Which part of a vibrating guitar produces sound initially?", "The vibrating string", "The guitar's shadow", "The stationary floor", "The guitar case's colour", "A"),
        ("What is an echo?", "A sound absorbed completely", "A reflected sound heard separately from the original", "A sound with zero frequency", "A sound that travels only through a vacuum", "B"),
        ("Which material is generally a good sound absorber?", "Polished steel", "A smooth mirror", "Thick acoustic foam", "A hard metal plate", "C"),
        ("Which of these is an example of a source of sound?", "A silent shadow", "A stationary photograph", "An unstruck, motionless bell", "A ringing bell", "D"),
        ("What is the unit of sound intensity level commonly used in everyday contexts?", "Decibel", "Kilogram", "Metre", "Kelvin", "A"),
        ("Which wave type describes sound in air under ordinary conditions?", "Transverse electromagnetic wave", "Longitudinal mechanical wave", "A wave that needs no medium", "A stationary light wave", "B"),
        ("In a longitudinal sound wave, particles of the medium vibrate:", "Only perpendicular to wave travel", "In circles only", "Back and forth approximately parallel to wave travel", "Not at all", "C"),
        ("What is a compression in a longitudinal sound wave?", "A region with no particles", "A region where particles are farther apart", "A region with zero pressure", "A region where particles are closer together", "D"),
        ("What is a rarefaction?", "A region where particles are farther apart", "A region where all particles stop", "A region with the greatest compression", "A source of light", "A"),
        ("Which factor affects the speed of sound in a material?", "The object's colour only", "The properties of the medium and its conditions", "The listener's height only", "The sound's loudness alone in every case", "B"),
        ("Which travels faster in air under ordinary conditions?", "Sound always travels faster than light", "They travel at identical speeds", "Light", "Neither can travel in air", "C"),
        ("Why does thunder usually arrive after the lightning flash is seen?", "Thunder occurs on another day", "Light cannot travel through air", "Sound is faster than light", "Light reaches us much faster than sound", "D"),
        ("What is noise commonly described as?", "Unwanted or unpleasant sound", "A sound that must be musical", "A sound with no vibrations", "Light reflected from a surface", "A"),
        ("Which of these can help reduce noise inside a room?", "Adding more hard reflective surfaces", "Using sound-absorbing curtains and panels", "Opening a loudspeaker at maximum volume", "Removing all soft furnishings", "B"),
        ("What is ultrasound?", "Sound below 20 Hz", "Sound audible to every human", "Sound with frequency above about 20,000 Hz", "Sound that travels only in space", "C"),
        ("What is infrasound?", "Sound above 20,000 Hz", "Sound that cannot travel through solids", "A type of light", "Sound with frequency below about 20 Hz", "D"),
        ("Which device commonly uses ultrasound to form images inside the body?", "Medical ultrasound scanner", "Ordinary mirror", "Thermometer", "Barometer", "A"),
        ("What happens when the amplitude of a sound wave increases, with other factors comparable?", "Its frequency must become zero", "The sound is generally louder", "Its pitch must always rise", "It stops travelling", "B"),
        ("What is the time taken for one complete vibration called?", "Frequency", "Wavelength", "Time period", "Amplitude", "C"),
        ("What is frequency?", "Distance travelled", "Maximum displacement only", "Energy per kilogram", "Number of complete vibrations per second", "D"),
        ("Which instrument can produce sound by vibrating a stretched string?", "Guitar", "Thermometer", "Compass", "Barometer", "A"),
        ("Why can we hear a ringing bell through air?", "Air permanently stores the sound", "Vibrations travel through air to the ear", "The bell sends light into the ear", "The sound travels without any medium", "B"),
    ],

    "Medium": [
        ("A source makes 200 vibrations in 2 seconds. What is its frequency?", "50 Hz", "200 Hz", "100 Hz", "400 Hz", "C"),
        ("A sound wave has a frequency of 500 Hz. What is its time period?", "0.5 s", "0.02 s", "2 s", "0.002 s", "D"),
        ("If the frequency of a sound increases while amplitude stays comparable, what is perceived to increase?", "Pitch", "Loudness only", "Speed in every medium", "Echo distance", "A"),
        ("If the amplitude of a sound wave increases while frequency remains unchanged, what generally changes?", "Pitch only", "Loudness", "Frequency", "The medium's density", "B"),
        ("A sound wave travels at 340 m/s and has frequency 170 Hz. What is its wavelength?", "0.5 m", "4 m", "2 m", "510 m", "C"),
        ("What is the relationship between wave speed, frequency, and wavelength?", "v = f/λ", "v = λ/f", "v = f + λ", "v = fλ", "D"),
        ("Why is sound generally faster in solids than in gases?", "Many solids transmit mechanical disturbances more rapidly because of their elastic properties", "Solids contain no particles", "Sound travels through solids as light", "Gas particles never move", "A"),
        ("An echo is heard 2 seconds after a shout. If the speed of sound is 340 m/s, approximately how far away is the reflecting surface?", "680 m", "340 m", "170 m", "1,360 m", "B"),
        ("Why is the distance to a reflecting surface divided by two when calculating it from an echo time?", "Sound travels only one way", "The sound stops at the surface", "The sound travels to the surface and back", "The speed of sound doubles on return", "C"),
        ("What is reverberation?", "The complete absence of sound", "A sound's frequency measured in hertz", "A change from sound to light", "Persistence of sound due to repeated reflections", "D"),
        ("Why are concert halls designed with acoustic treatment?", "To manage reflections and improve sound clarity", "To make all sound travel in a vacuum", "To remove every vibration from instruments", "To increase all frequencies equally without limit", "A"),
        ("Which change can increase the frequency of a vibrating string?", "Increasing its length while keeping other conditions fixed", "Increasing its tension while keeping other conditions fixed", "Adding mass per unit length while keeping other conditions fixed", "Stopping its vibration", "B"),
        ("What is the approximate minimum time gap usually needed for a distinct echo to be heard by a human listener?", "0.001 s", "0.01 s", "0.1 s", "10 s", "C"),
        ("A wave has wavelength 0.85 m and frequency 400 Hz. What is its speed?", "340 m/s", "400 m/s", "470 m/s", "85 m/s", "A"),
        ("Which property distinguishes ultrasound from ordinary audible sound?", "It cannot reflect", "Its frequency is above the normal upper limit of human hearing", "It travels only through air", "It has no wavelength", "B"),
        ("Why can ultrasound be useful for detecting flaws inside metal components?", "It always passes through every defect unchanged", "It produces visible colours", "It does not interact with matter", "Reflections from boundaries or defects can reveal internal structure", "D"),
        ("What happens to the frequency of a sound when it travels from air into water, assuming the source frequency remains fixed?", "It becomes zero", "It always doubles", "It remains the same at the boundary", "It becomes equal to the speed", "C"),
        ("When sound enters a new medium and its speed changes while frequency stays fixed, what happens to its wavelength?", "Its wavelength changes in proportion to the speed", "Its wavelength must stay fixed", "Its frequency becomes zero", "It ceases to be a wave", "A"),
        ("Which situation is an example of noise pollution?", "A quiet library", "Continuous loud construction noise near homes", "A soft conversation at a suitable level", "A clock in an empty room", "B"),
        ("Which measure is most suitable for protecting workers exposed to loud industrial sound?", "Increasing the exposure duration", "Removing all hearing protection", "Using appropriate hearing protection and reducing exposure", "Standing closer to the machine", "C"),
        ("Why can a vibrating tuning fork produce sound in air?", "Its prongs never move", "It creates sound without disturbing air", "It converts air into a solid", "Its vibrations cause nearby air pressure variations", "D"),
        ("What happens to the speed of sound in air as temperature generally increases?", "It generally increases", "It always becomes zero", "It decreases to zero", "It remains exactly constant under all conditions", "A"),
        ("A sound source has a frequency of 250 Hz. How many vibrations does it make in 4 seconds?", "250", "1,000", "500", "62.5", "B"),
        ("What is the time period of a wave with frequency 50 Hz?", "50 s", "5 s", "0.02 s", "0.2 s", "C"),
        ("Which statement about sound in a vacuum is correct?", "It travels faster than in solids", "It travels at the speed of light", "It travels only at night", "It cannot propagate because there are no material particles to transmit the vibration", "D"),
        ("Why can sound be heard around a doorway even when the source is not directly visible?", "Sound can diffract around openings and obstacles", "Sound always travels in a perfect vacuum", "The doorway creates the original sound", "Sound changes into a solid", "A"),
        ("Which change generally increases the loudness of sound produced by plucking a string?", "Reducing the amplitude of vibration", "Plucking the string with greater amplitude", "Reducing the vibration to zero", "Changing only the string's colour", "B"),
        ("Which instrument is commonly used to measure sound level in decibels?", "Thermometer", "Ammeter", "Sound level meter", "Hydrometer", "C"),
        ("What is the primary role of the eardrum?", "To produce light", "To measure air temperature", "To block all sound permanently", "To vibrate in response to sound waves and transmit vibrations to the middle ear", "D"),
        ("Why is the speed of sound different in different materials?", "The material's elastic properties and density affect wave propagation", "All materials have identical particles and properties", "Sound speed depends only on colour", "Sound speed is always 3 × 10^8 m/s", "A"),
    ],

    "Hard": [
        ("A sound wave travels at 330 m/s and has frequency 660 Hz. What is its wavelength?", "0.25 m", "0.5 m", "2 m", "990 m", "B"),
        ("A source produces 720 vibrations in 3 seconds. What are its frequency and time period?", "120 Hz and 0.12 s", "240 Hz and 2.4 s", "240 Hz and approximately 0.00417 s", "720 Hz and 3 s", "C"),
        ("An echo returns 0.8 seconds after a sound is emitted. If sound travels at 340 m/s, what is the distance to the reflecting surface?", "136 m", "272 m", "340 m", "680 m", "A"),
        ("A sound wave has speed 300 m/s and wavelength 0.75 m. What is its frequency?", "225 Hz", "300 Hz", "400 Hz", "450 Hz", "C"),
        ("A wave has frequency 2,000 Hz and speed 340 m/s. What is its wavelength?", "1.7 m", "0.17 m", "0.017 m", "6.8 m", "B"),
        ("A listener hears an echo after 1.5 seconds. If the reflecting surface is 255 m away, what is the implied speed of sound?", "170 m/s", "255 m/s", "510 m/s", "340 m/s", "D"),
        ("A sound travels from air into another medium. Its speed rises from 340 m/s to 1,360 m/s while its frequency remains 680 Hz. What is its new wavelength?", "2 m", "0.5 m", "4 m", "1 m", "A"),
        ("Which statement about frequency and pitch is most accurate?", "Pitch depends only on amplitude", "Pitch is primarily associated with frequency", "Pitch is measured in metres", "Pitch is independent of frequency", "B"),
        ("Two sounds have the same frequency but different amplitudes. What is the most direct difference between them?", "Their pitches must differ", "Their frequencies differ", "Their loudness levels can differ", "Their propagation speeds must differ", "C"),
        ("Why is a sound heard as an echo only when the reflected sound is sufficiently separated in time from the original?", "The reflected sound must be louder than the original", "Sound must travel through a vacuum", "The listener must be underwater", "The auditory system needs sufficient time separation to distinguish the reflection", "D"),
        ("A sound wave has a time period of 0.004 seconds. What is its frequency?", "250 Hz", "400 Hz", "40 Hz", "4 Hz", "A"),
        ("A wave of frequency 500 Hz travels through air at 350 m/s. What is its wavelength?", "1.4 m", "0.7 m", "7 m", "0.14 m", "B"),
        ("A source's frequency doubles while sound speed in the same medium remains constant. What happens to the wavelength?", "It doubles", "It remains unchanged", "It becomes half as large", "It becomes four times as large", "C"),
        ("A sound wave's wavelength doubles while its speed remains constant. What happens to its frequency?", "It doubles", "It becomes four times as large", "It remains unchanged", "It becomes half as large", "D"),
        ("Why can sound not travel from the Sun to Earth through outer space directly?", "Outer space is nearly a vacuum and lacks enough material medium for sound propagation", "The Sun produces no vibrations", "Sound travels only downward", "Earth absorbs all sound at its surface", "A"),
        ("Which statement about sound waves in air is correct?", "They are transverse electromagnetic waves", "They propagate as longitudinal pressure variations", "They need no medium", "Air particles travel all the way from the source to the listener", "B"),
        ("A wave completes 150 cycles in 0.5 seconds. What is its frequency?", "75 Hz", "150 Hz", "300 Hz", "600 Hz", "C"),
        ("A sound wave has frequency 850 Hz and wavelength 0.4 m. What is its speed?", "212.5 m/s", "340 m/s", "1,250 m/s", "340 m/s", "D"),
        ("Why does the sound from a distant explosion reach a listener after the light from it?", "Light travels much faster than sound in air", "Sound is not a wave", "Light must travel through a material medium", "The explosion emits light only later", "A"),
        ("Which factor most directly determines the energy carried by a sound wave in a given setup?", "The colour of the source", "The wave amplitude and the properties of the medium", "The listener's height only", "The source's name", "B"),
        ("Why can an ultrasound scan produce an image of internal tissues?", "Ultrasound is visible to the naked eye", "It travels only through empty space", "Echoes from tissue boundaries are processed to form an image", "It has no frequency", "C"),
        ("A sonar pulse returns after 2.4 seconds. If sound travels through the water at 1,500 m/s, how far away is the reflecting object?", "1,500 m", "3,600 m", "7,200 m", "1,800 m", "D"),
        ("A sound level increases substantially when a source is moved closer to a listener. Which factor is most directly responsible in a typical open environment?", "The sound intensity reaching the listener increases as distance decreases", "The sound frequency must become zero", "The source becomes a different element", "Sound no longer needs a medium", "A"),
        ("What is the main difference between ultrasound and infrasound?", "Ultrasound has lower frequency than infrasound", "Ultrasound is above the upper human hearing range, while infrasound is below the lower range", "Infrasound is electromagnetic radiation", "Ultrasound cannot travel through liquids", "B"),
        ("A sound wave travels at 340 m/s and has a time period of 0.01 s. What is its wavelength?", "0.34 m", "3.4 m", "34 m", "0.034 m", "A"),
        ("Why can noise-cancelling headphones reduce some unwanted sounds?", "They remove the need for hearing", "They convert all sound into light", "They generate sound waves that can destructively interfere with incoming sound", "They block every frequency perfectly in all environments", "C"),
        ("A wave has wavelength 1.2 m and speed 360 m/s. How many cycles occur in 2 seconds?", "300", "600", "720", "900", "B"),
        ("A person stands 170 m from a reflecting cliff. Using a sound speed of 340 m/s, approximately how long does the echo take to return?", "0.25 s", "0.5 s", "2 s", "1 s", "D"),
        ("Which change would generally lower the pitch of a vibrating string, if other factors remain comparable?", "Reducing its tension", "Increasing its frequency", "Reducing its vibrating length", "Increasing its frequency and tension together in every case", "A"),
        ("A sound wave travels 1,020 m in 3 seconds. If its frequency is 600 Hz, what is its wavelength?", "0.57 m", "1.7 m", "3.4 m", "340 m", "B"),
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