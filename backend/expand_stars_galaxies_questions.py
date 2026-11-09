
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"
LESSON_TITLE = "Stars and Galaxies"
TARGET_QUESTIONS = 30

# Each question: question, option A, option B, option C, option D, correct answer
QUESTION_BANK = {
    "Easy": [
        ("What is a star?", "A hot ball of gases that produces its own light", "A rocky planet", "A natural satellite", "A cloud of water vapour", "A"),
        ("Which star is closest to Earth?", "Sirius", "The Sun", "Polaris", "Alpha Centauri", "B"),
        ("What is the name of our galaxy?", "Andromeda", "Whirlpool", "Milky Way", "Sombrero", "C"),
        ("Which object orbits Earth naturally?", "Mars", "The Sun", "Venus", "The Moon", "D"),
        ("What gives stars their energy?", "Nuclear fusion", "Burning coal", "Electric batteries", "Chemical reactions with oxygen", "A"),
        ("Which planet is known as the Red Planet?", "Jupiter", "Mars", "Mercury", "Neptune", "B"),
        ("What is a galaxy?", "A single planet", "A type of telescope", "A large collection of stars, gas and dust held together by gravity", "A small asteroid", "C"),
        ("Which galaxy contains our Solar System?", "Andromeda Galaxy", "Whirlpool Galaxy", "Sombrero Galaxy", "Milky Way Galaxy", "D"),
        ("Which star is commonly used to locate north in the Northern Hemisphere?", "Polaris", "Sirius", "Betelgeuse", "Vega", "A"),
        ("What is the Sun?", "A planet", "A star", "A comet", "A galaxy", "B"),
        ("Which instrument helps us observe distant stars?", "Microscope", "Thermometer", "Telescope", "Barometer", "C"),
        ("What is the apparent pattern formed by stars in the sky called?", "Orbit", "Galaxy", "Nebula", "Constellation", "D"),
        ("Which is the largest object among these?", "A galaxy", "A planet", "A moon", "A small asteroid", "A"),
        ("What is a light-year used to measure?", "Time taken by a planet to rotate", "Distance", "Temperature", "Brightness only", "B"),
        ("Which object is at the centre of our Solar System?", "Earth", "The Moon", "The Sun", "Jupiter", "C"),
        ("What is a group of stars forming a recognisable pattern called?", "An asteroid belt", "A solar system", "A comet trail", "A constellation", "D"),
        ("Which colour generally indicates a hotter star?", "Blue", "Red", "Orange", "Dark brown", "A"),
        ("What is a nebula?", "A rocky planet", "A cloud of gas and dust in space", "A natural satellite", "A type of orbit", "B"),
        ("Which galaxy is the nearest large galaxy to the Milky Way?", "Sombrero Galaxy", "Whirlpool Galaxy", "Andromeda Galaxy", "Pinwheel Galaxy", "C"),
        ("Why do stars appear to twinkle when viewed from Earth?", "They switch on and off", "They change size rapidly", "They orbit Earth every second", "Earth's atmosphere bends their light irregularly", "D"),
        ("What is a planet?", "An object that orbits a star and does not produce its own light through fusion", "A collection of galaxies", "A star that has cooled slightly", "A cloud of dust", "A"),
        ("Which planet is famous for its prominent ring system?", "Earth", "Saturn", "Mars", "Mercury", "B"),
        ("What is the name of the galaxy closest to the Milky Way among these?", "Whirlpool Galaxy", "Sombrero Galaxy", "Andromeda Galaxy", "Cartwheel Galaxy", "C"),
        ("What is the main source of visible light from the Sun?", "Reflected light from Earth", "Burning gases in oxygen", "Light from distant galaxies", "Energy released by fusion in its core", "D"),
        ("What do astronomers study?", "Celestial objects and the universe", "Only rocks on Earth", "Only ocean currents", "Only living organisms", "A"),
        ("Which object is made mainly of ice, dust and rocky material and may form a tail near the Sun?", "A star", "A comet", "A galaxy", "A planet", "B"),
        ("What is the Solar System?", "A single constellation", "A group of unrelated galaxies", "The Sun and the objects gravitationally bound to it", "A cluster of stars with no central star", "C"),
        ("Which star is at the centre of our Solar System?", "Polaris", "Sirius", "Vega", "The Sun", "D"),
        ("What is the shape of the Milky Way generally classified as?", "Barred spiral", "Perfect cube", "Flat triangle", "Straight line", "A"),
        ("Why can we see stars at night?", "They reflect all the light from the Moon", "Their light reaches Earth and the Sun's glare is reduced", "They are inside Earth's atmosphere", "They are closer than the Moon", "B"),
    ],
    "Medium": [
        ("Why does the Sun appear much brighter than other stars?", "It is the hottest star in the universe", "It produces more energy than every other star combined", "It is much closer to Earth than other stars", "Other stars do not produce light", "C"),
        ("What does a light-year represent?", "The time a star takes to form", "The distance Earth travels in one day", "The age of a galaxy", "The distance light travels in one year", "D"),
        ("What force holds stars together within a galaxy?", "Gravity", "Magnetism alone", "Friction", "Air pressure", "A"),
        ("What is nuclear fusion in a star's core?", "Splitting large atoms to release energy", "Combining light atomic nuclei and releasing energy", "Burning fuel using oxygen", "Reflecting energy from nearby planets", "B"),
        ("What is a main-sequence star?", "A star that has become a black hole", "A star with no nuclear reactions", "A star that fuses hydrogen into helium in its core", "A star made entirely of solid rock", "C"),
        ("Which factor most directly determines a star's main-sequence lifetime?", "Its distance from Earth", "The number of planets around it", "Its apparent colour in a photograph only", "Its mass", "D"),
        ("What can happen when a massive star reaches the end of its life?", "It may explode as a supernova", "It always becomes a planet", "It turns into a comet", "It immediately disappears without any change", "A"),
        ("What is a black hole?", "A planet with no atmosphere", "A region where gravity is so strong that light cannot escape from within the event horizon", "A dark cloud that absorbs all starlight in the universe", "A star that reflects no light but has ordinary gravity", "B"),
        ("Which type of galaxy has a roughly spherical or ellipsoidal shape and little organised spiral structure?", "Spiral", "Irregular", "Elliptical", "Ring-shaped only", "C"),
        ("What is the main difference between a star and a planet?", "Planets are always larger", "Stars always orbit planets", "Planets produce more energy through fusion", "Stars generate energy through fusion; planets generally do not", "D"),
        ("Why do astronomers use spectroscopy to study stars?", "To infer their composition, temperature and motion", "To measure only their physical distance by touch", "To stop their light from reaching Earth", "To determine the exact number of planets in every galaxy", "A"),
        ("What is a supernova?", "The birth of a small moon", "A powerful explosion associated with certain stages in a star's life", "A type of constellation", "A planet passing in front of a star", "B"),
        ("What is the approximate age of the universe?", "About 4.6 million years", "About 100 billion years", "About 13.8 billion years", "About 1,000 years", "C"),
        ("What does the redshift of light from a distant galaxy often indicate?", "The galaxy is definitely moving toward Earth", "The galaxy has no stars", "The galaxy is becoming colder only", "Its light has shifted toward longer wavelengths, often indicating recession due to cosmic expansion", "D"),
        ("What is a globular cluster?", "A dense, roughly spherical collection of stars", "A group of planets around one star", "A cloud of water droplets", "A single very large asteroid", "A"),
        ("What is an exoplanet?", "A planet inside Earth's atmosphere", "A planet orbiting a star beyond our Solar System", "A moon orbiting Earth", "A planet that has no gravity", "B"),
        ("Why do stars have different colours?", "Because they are made of completely different elements only", "Because they are at different distances only", "Their surface temperatures differ", "Because all stars reflect the colours of nearby planets", "C"),
        ("What is the event horizon of a black hole?", "Its visible solid surface", "The point where its gravity becomes zero", "The outer edge of the Milky Way", "The boundary beyond which escape is impossible", "D"),
        ("What is an astronomical unit approximately equal to?", "The average distance between Earth and the Sun", "The distance light travels in a year", "The diameter of the Milky Way", "The distance between Earth and the Moon", "A"),
        ("What is the role of gravity in star formation?", "It prevents gas from moving", "It pulls gas and dust together so a protostar can form", "It turns planets into galaxies instantly", "It stops all nuclear reactions", "B"),
        ("Which observation provides strong evidence that the universe is expanding?", "All stars have exactly the same temperature", "The Moon moves around Earth", "The redshift of many distant galaxies", "The presence of rings around Saturn", "C"),
        ("What is a white dwarf?", "A newly formed galaxy", "A massive star before its first fusion reaction", "A planet made of ice", "The compact remnant of a low- or intermediate-mass star", "D"),
        ("What is the Milky Way's central region thought to contain?", "A supermassive black hole", "The Solar System's largest planet", "A second Sun identical to ours", "A giant solid sphere of iron", "A"),
        ("Which statement about constellations is correct?", "Their stars are always physically close together", "They are apparent patterns viewed from Earth", "They are all galaxies", "Their shapes never change over very long times", "B"),
        ("What is a binary star system?", "A system containing two galaxies only", "A planet with two moons", "Two stars gravitationally bound and orbiting a common centre of mass", "A star that emits light in two colours only", "C"),
        ("What is a protostar?", "A star that has already become a black hole", "A dead star made of iron", "A planet forming in a ring", "A developing star formed as gas and dust collapse", "D"),
        ("What is cosmic microwave background radiation?", "Radiation left over from the early universe", "Radio waves emitted only by Earth", "Light reflected by the Moon", "Heat produced by the Sun's surface", "A"),
        ("Why are distant galaxies useful for studying the early universe?", "They are all older than nearby galaxies", "Their light has taken a long time to reach us", "They contain no stars", "They are outside the universe", "B"),
        ("What does a star's apparent magnitude describe?", "Its chemical composition", "Its exact mass", "How bright it appears from Earth", "Its age in years", "C"),
        ("What is an irregular galaxy?", "A galaxy that contains no matter", "A galaxy with a perfectly circular orbit", "A galaxy consisting of one star", "A galaxy without a well-defined spiral or elliptical shape", "D"),
    ],
    "Hard": [
        ("A star is 4 light-years away. What does this tell us about the light we observe from it?", "The light took about 4 years to reach Earth", "The star formed exactly 4 years ago", "The star is 4 kilometres away", "The star's surface temperature is 4 degrees", "A"),
        ("Why do more massive main-sequence stars generally have shorter lifetimes?", "They contain no hydrogen", "They consume their nuclear fuel at a much higher rate", "Their gravity is zero", "They cannot fuse hydrogen", "B"),
        ("A star's spectral lines are shifted toward longer wavelengths. What is this commonly called?", "Blueshift", "Parallax", "Redshift", "Diffraction", "C"),
        ("Which sequence best describes the early formation of a star?", "Planet → comet → galaxy → star", "Black hole → planet → nebula → star", "White dwarf → asteroid → star → nebula", "Gas and dust cloud → gravitational collapse → protostar → star with sustained fusion", "D"),
        ("What is the approximate relationship between a star's luminosity, its radius and surface temperature?", "Luminosity is proportional to radius squared and the fourth power of temperature", "Luminosity depends only on distance from Earth", "Luminosity is proportional only to its number of planets", "Luminosity is independent of radius and temperature", "A"),
        ("A star's parallax angle is measured to be 0.1 arcsecond. Using distance in parsecs = 1 / parallax in arcseconds, how far away is it?", "0.1 parsec", "10 parsecs", "1 parsec", "100 parsecs", "B"),
        ("Which remnant is most likely to form after a sufficiently massive stellar core collapses?", "A small asteroid", "A normal main-sequence star immediately", "A neutron star or black hole, depending on the core and conditions", "A new planet with no heat", "C"),
        ("Why can a black hole be detected even though light cannot escape from inside its event horizon?", "It is always surrounded by a visible solid shell", "It reflects all nearby starlight perfectly", "It blocks gravity from acting on nearby objects", "Its effects on nearby matter and light can be observed", "D"),
        ("If a galaxy is moving away from us and its recession speed is small compared with the speed of light, what does a larger redshift generally suggest?", "A larger recession speed", "A lower number of stars in the galaxy", "That the galaxy has no gravity", "That it is necessarily closer to Earth", "A"),
        ("Which observation is used in the standard method of stellar parallax?", "Measuring a star's colour once", "Comparing its apparent position against distant background objects from different points in Earth's orbit", "Counting its planets directly", "Measuring only the temperature of its core", "B"),
        ("Why are Cepheid variable stars useful in astronomy?", "They never change brightness", "They exist only in the Solar System", "Their pulsation period is related to intrinsic luminosity, helping estimate distance", "Their colour directly gives the age of every galaxy", "C"),
        ("What is the approximate Schwarzschild radius of a non-rotating black hole proportional to?", "The square of its temperature", "The inverse of its mass", "The distance to the nearest star", "Its mass", "D"),
        ("Which process supports a stable main-sequence star against gravitational collapse?", "Pressure from hot gas and energy transport balancing gravity", "The push of sunlight from nearby planets alone", "The absence of gravity in the core", "The star's rotation alone in every case", "A"),
        ("What does the Hertzsprung–Russell diagram primarily compare?", "Galaxy distance and age only", "Stellar luminosity and surface temperature or spectral type", "Planet mass and orbital period", "Black-hole radius and event date", "B"),
        ("What is a supermassive black hole?", "A black hole with the mass of a small asteroid", "A star that has no gravity", "A black hole with millions to billions of solar masses, often found in galactic centres", "A galaxy with no dark matter", "C"),
        ("What is the main evidence for dark matter in galaxies?", "Every galaxy emits only blue light", "Dark matter can be seen as a bright surface", "Stars in galaxies never move", "Gravitational effects, including rotation curves, exceed what visible matter alone explains", "D"),
        ("What is the cosmological principle, in simplified form?", "On sufficiently large scales, the universe is approximately homogeneous and isotropic", "Earth is the centre of every galaxy", "All stars have the same mass", "Every galaxy is identical in shape", "A"),
        ("What does the cosmic microwave background tell us?", "That the universe has always had the same temperature", "It is relic radiation from the hot, early universe", "That the Sun existed before the Big Bang", "That galaxies do not move", "B"),
        ("If a star has a parallax of 0.05 arcsecond, what is its distance in parsecs?", "5 parsecs", "10 parsecs", "20 parsecs", "50 parsecs", "C"),
        ("Which factor primarily determines the evolutionary path of an isolated star?", "The number of constellations visible nearby", "Its distance from Earth", "The planet with the shortest orbit around it", "Its initial mass", "D"),
        ("Why do stars near the main sequence have a relatively stable size for much of their lives?", "Hydrostatic equilibrium balances inward gravity with outward pressure", "Gravity stops acting inside stars", "Their cores contain no energy", "Their surfaces are solid", "A"),
        ("What is gravitational lensing?", "The bending of sound around a star", "The bending of light by gravity as it travels near massive objects", "The reflection of light from planets only", "The absorption of all light by Earth's atmosphere", "B"),
        ("What does a galaxy's rotation curve show?", "The chemical composition of each planet", "The number of moons around its stars", "Orbital speed as a function of distance from the galactic centre", "The colour of every star in sequence", "C"),
        ("Why is the Andromeda Galaxy expected to interact strongly with the Milky Way in the distant future?", "It is a planet orbiting Earth", "It has no gravitational attraction", "It is moving away at the speed of light", "It is approaching the Milky Way under their mutual gravitational attraction", "D"),
        ("What does the term 'metallicity' mean in stellar astronomy?", "The abundance of elements heavier than helium", "The percentage of a star made of liquid metal", "The number of planets around a star", "The star's distance measured in kilometres", "A"),
        ("Which statement about a neutron star is correct?", "It is a large cloud of hydrogen gas", "It is an extremely dense remnant of a massive star's collapsed core", "It is a planet made entirely of ice", "It has no gravitational field", "B"),
        ("What is the approximate escape velocity from a black hole's event horizon equal to in the idealised non-rotating case?", "The speed of sound", "Half the speed of light", "The speed of light", "Zero", "C"),
        ("What is the primary difference between apparent magnitude and absolute magnitude?", "Both always describe the same measured brightness", "Absolute magnitude measures distance directly", "Apparent magnitude is only used for planets", "Apparent magnitude is observed brightness; absolute magnitude standardises brightness at 10 parsecs", "D"),
        ("Why can gravitational waves be produced by a pair of orbiting black holes?", "Their accelerating, asymmetric mass distribution changes the gravitational field and radiates waves", "Black holes emit ordinary sound waves into space", "Their event horizons are made of vibrating air", "They reflect radio waves like mirrors", "A"),
        ("Which observation most directly supports the idea that the universe is expanding?", "The phases of Venus", "The systematic redshift of distant galaxies, together with distance measurements", "The daily rotation of Earth", "The existence of Earth's seasons", "B"),
    ],
}


def normalize(text):
    return " ".join(text.lower().split())


def main():
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DATABASE_PATH}\n"
            "Run this script from your project setup after checking the database path."
        )

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
        added_total = 0

        for difficulty in ("Easy", "Medium", "Hard"):
            cursor.execute(
                """
                SELECT id FROM quizzes
                WHERE lesson_id = ? AND LOWER(TRIM(difficulty)) = LOWER(TRIM(?))
                """,
                (lesson_id, difficulty),
            )
            quiz_rows = cursor.fetchall()

            if len(quiz_rows) != 1:
                raise RuntimeError(
                    f"Expected exactly one {difficulty} quiz for '{LESSON_TITLE}', "
                    f"but found {len(quiz_rows)}."
                )

            quiz_id = quiz_rows[0][0]

            cursor.execute(
                "SELECT question FROM questions WHERE quiz_id = ?",
                (quiz_id,),
            )
            existing = {normalize(row[0]) for row in cursor.fetchall()}

            candidates = QUESTION_BANK[difficulty]
            unique_candidates = []
            seen_candidates = set()

            for item in candidates:
                key = normalize(item[0])
                if key not in existing and key not in seen_candidates:
                    unique_candidates.append(item)
                    seen_candidates.add(key)

            cursor.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                (quiz_id,),
            )
            current_count = cursor.fetchone()[0]
            needed = max(0, TARGET_QUESTIONS - current_count)

            if len(unique_candidates) < needed:
                raise RuntimeError(
                    f"{difficulty}: need {needed} new questions, "
                    f"but only {len(unique_candidates)} unique candidates are available. "
                    "No changes have been committed."
                )

            to_insert = unique_candidates[:needed]

            cursor.executemany(
                """
                INSERT INTO questions
                (quiz_id, question, option_a, option_b, option_c, option_d, correct_answer)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (quiz_id, question, a, b, c, d, answer)
                    for question, a, b, c, d, answer in to_insert
                ],
            )

            added_total += len(to_insert)

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
        print(f"\nSuccess! Added {added_total} questions to '{LESSON_TITLE}'.")
        print("Other lessons and Social Science were not modified.")

    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
