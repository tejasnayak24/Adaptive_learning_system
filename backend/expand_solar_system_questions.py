
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"
LESSON_TITLE = "Solar System"
TARGET_QUESTIONS = 30

QUESTIONS = {
    "Easy": [
        ("Which star is at the center of our solar system?", "Sirius", "The Sun", "Polaris", "Alpha Centauri", "B"),
        ("Which planet is closest to the Sun?", "Venus", "Earth", "Mercury", "Mars", "C"),
        ("Which planet is known as the Red Planet?", "Mars", "Jupiter", "Saturn", "Neptune", "A"),
        ("Which is the largest planet in our solar system?", "Earth", "Venus", "Mars", "Jupiter", "D"),
        ("Which planet is famous for its prominent ring system?", "Mercury", "Saturn", "Earth", "Mars", "B"),
        ("Which planet do we live on?", "Venus", "Mars", "Earth", "Jupiter", "C"),
        ("How many planets are officially recognized in our solar system?", "Eight", "Seven", "Nine", "Ten", "A"),
        ("Which planet is farthest from the Sun among the eight planets?", "Uranus", "Saturn", "Jupiter", "Neptune", "D"),
        ("What is Earth's natural satellite?", "The Sun", "The Moon", "Mars", "Venus", "B"),
        ("What force keeps planets in orbit around the Sun?", "Friction", "Magnetism alone", "Gravity", "Air resistance", "C"),
        ("Which planet is often called Earth's sister planet because of its similar size?", "Venus", "Jupiter", "Mercury", "Neptune", "A"),
        ("Which planet is best known for its Great Red Spot?", "Mars", "Saturn", "Venus", "Jupiter", "D"),
        ("What is an asteroid?", "A type of star", "A small rocky body orbiting the Sun", "A galaxy", "A planet's atmosphere", "B"),
        ("Where is the main asteroid belt located?", "Beyond Neptune", "Between Earth and Mars", "Between Mars and Jupiter", "Inside the Sun", "C"),
        ("What is a comet mainly made of?", "Ice, dust, and rocky material", "Only liquid water", "Pure iron", "Hot plasma only", "A"),
        ("What causes day and night on Earth?", "Earth's revolution around the Sun", "The Moon's revolution", "Changes in the Sun's size", "Earth's rotation on its axis", "D"),
        ("What causes Earth's seasons mainly?", "Changes in Earth's distance from the Sun alone", "Earth's axial tilt as it revolves around the Sun", "The Moon blocking sunlight every day", "The Sun orbiting Earth", "B"),
        ("Which planet is known for its very prominent rings made largely of ice and rocky particles?", "Mercury", "Earth", "Saturn", "Mars", "C"),
        ("What is the path followed by a planet around the Sun called?", "Orbit", "Axis", "Equator", "Crater", "A"),
        ("Which planet has the most massive planetary system of moons and is the largest planet?", "Venus", "Mercury", "Earth", "Jupiter", "D"),
        ("What is the Sun?", "A planet", "A star", "A moon", "An asteroid", "B"),
        ("Which object is classified as a dwarf planet and lies in the Kuiper Belt?", "Earth", "Mars", "Pluto", "Venus", "C"),
        ("What is the natural satellite of Earth called?", "Moon", "Phobos", "Europa", "Titan", "A"),
        ("Which planet rotates on its side with an extreme axial tilt?", "Mars", "Earth", "Jupiter", "Uranus", "D"),
        ("What is the Milky Way?", "A planet", "The galaxy containing our solar system", "A comet", "A constellation inside Earth", "B"),
        ("Which planet is known for having a very thick carbon-dioxide atmosphere and extremely high surface temperatures?", "Mars", "Neptune", "Venus", "Mercury", "C"),
        ("What is a meteor?", "A streak of light caused by a space object entering Earth's atmosphere", "A star orbiting Earth", "A planet's ring", "A type of galaxy", "A"),
        ("Which planet is known for its blue appearance and strong winds?", "Mercury", "Venus", "Earth", "Neptune", "D"),
        ("What is the main source of energy for Earth?", "The Moon", "The Sun", "Jupiter", "Earth's core alone", "B"),
        ("What is a natural satellite?", "A man-made spacecraft only", "A star that produces light", "A natural object that orbits a planet or another smaller body", "A cloud in the atmosphere", "C"),
    ],

    "Medium": [
        ("Approximately how long does Earth take to complete one revolution around the Sun?", "365.25 days", "24 hours", "30 days", "12 hours", "A"),
        ("Approximately how long does Earth take to rotate once relative to distant stars?", "12 hours", "24 hours", "23 hours 56 minutes", "365 days", "C"),
        ("Why does the Moon shine in the night sky?", "It produces light through nuclear fusion", "It reflects sunlight", "It is a star", "It reflects only Earth's core heat", "B"),
        ("Which planet has the shortest orbital period around the Sun?", "Venus", "Earth", "Mars", "Mercury", "D"),
        ("Which planet has the longest orbital period among the eight planets?", "Neptune", "Saturn", "Uranus", "Jupiter", "A"),
        ("What is the main reason Pluto is classified as a dwarf planet rather than one of the eight planets?", "It does not orbit the Sun", "It has no gravity", "It has not cleared its orbital neighbourhood", "It produces no reflected sunlight", "C"),
        ("What is the Kuiper Belt?", "A region containing many icy bodies beyond Neptune", "The layer at the center of the Sun", "A ring around Earth", "A belt of clouds around Venus", "A"),
        ("What is the Oort Cloud hypothesized to be?", "A ring around Saturn", "A distant, roughly spherical reservoir of icy bodies surrounding the solar system", "The surface of the Sun", "A region between Earth and Mars", "B"),
        ("Why do planets generally appear to move across the sky against the background stars?", "They are fixed in space", "The stars orbit each planet daily", "They are moons of the Sun", "They orbit the Sun and are observed from a moving Earth", "D"),
        ("What causes a lunar eclipse?", "The Moon moves between Earth and the Sun", "The Sun moves behind Jupiter", "Earth comes between the Sun and the Moon", "Mars blocks the Moon", "C"),
        ("What causes a solar eclipse?", "The Moon passes between Earth and the Sun", "Earth passes between Mars and Jupiter", "The Sun passes behind the Moon in its orbit around Earth", "Jupiter blocks sunlight from Earth", "A"),
        ("Why do we see different phases of the Moon?", "Earth's shadow covers the Moon every night", "We see different portions of its sunlit half as it orbits Earth", "The Moon changes its actual shape", "The Moon produces different amounts of light", "B"),
        ("Which planet has the shortest day, approximately, because of its rapid rotation?", "Earth", "Mars", "Jupiter", "Mercury", "C"),
        ("Which planet has the highest average surface temperature, largely because of its strong greenhouse effect?", "Mercury", "Mars", "Jupiter", "Venus", "D"),
        ("What is the main component of the Sun by mass?", "Hydrogen", "Oxygen", "Iron", "Carbon dioxide", "A"),
        ("What process powers the Sun?", "Chemical combustion", "Nuclear fusion", "Nuclear fission of uranium only", "Burning coal", "B"),
        ("What is the approximate average distance from Earth to the Sun, known as one astronomical unit?", "1 million km", "15 million km", "150 million km", "1 billion km", "C"),
        ("Why do planets remain in orbit rather than moving in straight lines away from the Sun?", "Their engines continuously push them", "Air resistance slows them", "Magnetic attraction alone holds them", "Their forward motion combines with the Sun's gravitational pull", "D"),
        ("Which of these is an example of a gas giant?", "Jupiter", "Mercury", "Venus", "Mars", "A"),
        ("Which pair consists of the solar system's ice giants?", "Earth and Mars", "Uranus and Neptune", "Jupiter and Saturn", "Mercury and Venus", "B"),
        ("What is the Great Red Spot on Jupiter?", "A solid mountain", "A giant impact crater", "A long-lasting storm", "A frozen ocean", "C"),
        ("Which planet has the most prominent ring system visible through telescopes?", "Earth", "Mars", "Venus", "Saturn", "D"),
        ("What is a light-year?", "The distance light travels in one year", "The time Earth takes to orbit the Sun", "The distance from Earth to the Moon", "The age of a star in days", "A"),
        ("What is the main difference between a planet and a star?", "Planets always have rings", "Stars generate energy through internal processes such as fusion, while planets generally reflect starlight", "Planets are always larger than stars", "Stars cannot have planets around them", "B"),
        ("Why are craters common on the surfaces of many airless bodies, such as the Moon?", "Water continuously carves them", "They are formed by plants", "Impacts from space objects create them and there is little weathering to erase them", "They are caused by Earth's seasons", "C"),
        ("What is a constellation?", "A group of stars that form a recognized apparent pattern in the sky", "A group of planets physically attached together", "A type of asteroid", "A satellite orbiting Earth", "A"),
        ("Why do we always see nearly the same side of the Moon from Earth?", "The Moon does not rotate", "The Moon's rotation period is approximately equal to its orbital period around Earth", "Earth's atmosphere hides the other side", "The Sun illuminates only one side permanently", "B"),
        ("What is the solar wind?", "Rain in the Sun's atmosphere", "A wind blowing through Earth's forests", "A stream of charged particles emitted by the Sun", "A current of liquid water in space", "C"),
        ("Which spacecraft was the first to fly past Pluto in 2015?", "Voyager 1", "Pioneer 10", "Juno", "New Horizons", "D"),
        ("What is the heliosphere?", "The region of space influenced by the solar wind and the Sun's magnetic environment", "The core of Earth", "The atmosphere of Jupiter", "The ring system of Saturn", "A"),
    ],

    "Hard": [
        ("A planet orbits a star at four times Earth's orbital radius. Using Kepler's third law, approximately how many Earth years is its orbital period?", "4 years", "8 years", "16 years", "2 years", "B"),
        ("If a planet's orbital radius is 9 astronomical units, approximately how long is its orbital period in Earth years, assuming a Sun-like central mass?", "9 years", "18 years", "27 years", "81 years", "C"),
        ("Why does a planet move faster near perihelion than near aphelion in an elliptical orbit?", "Its angular momentum is conserved, so it moves faster when closer to the Sun", "The Sun's gravity becomes zero near perihelion", "Its mass increases near the Sun", "It receives a push from the solar wind only", "A"),
        ("Which statement best describes Kepler's first law?", "Planets move in perfect circles with the Sun at the center", "A planet's speed is always constant", "The orbital period is proportional to the orbital radius", "Planets move in ellipses with the Sun at one focus", "D"),
        ("According to Kepler's second law, a line joining a planet and the Sun sweeps out what over equal time intervals?", "Equal distances", "Equal areas", "Equal angles", "Equal speeds", "B"),
        ("A planet's orbital period is 8 Earth years around a Sun-like star. What is its approximate orbital radius in astronomical units?", "2 AU", "4 AU", "8 AU", "16 AU", "B"),
        ("Which factor mainly determines the orbital speed of a planet in a nearly circular orbit around the Sun?", "The planet's colour", "The planet's surface temperature only", "The Sun's mass and the orbital radius", "The planet's number of moons only", "C"),
        ("Why do inner planets generally have shorter orbital periods than outer planets?", "They orbit at smaller radii and have higher orbital speeds", "They have no gravity", "The Sun pulls only on inner planets", "They are all made of gas", "A"),
        ("What is escape velocity?", "The speed needed to orbit Earth once", "The speed at which a planet rotates", "The speed of light in a vacuum", "The minimum speed needed to escape a body's gravitational influence without further propulsion, under ideal conditions", "D"),
        ("What is the approximate escape velocity from Earth's surface, ignoring atmosphere and Earth's rotation?", "3.0 km/s", "11.2 km/s", "30 km/s", "42 km/s", "B"),
        ("Why is a geostationary satellite useful for communication?", "It passes over every latitude each hour", "It is stationary relative to the Sun", "It appears nearly fixed above the same point on Earth's equator", "It does not experience gravity", "C"),
        ("What orbital period must a geostationary satellite have?", "Approximately one sidereal day", "Exactly 12 hours", "Exactly 365 days", "One lunar month", "A"),
        ("Why do astronauts in orbit experience apparent weightlessness?", "Gravity is absent in space", "They are beyond Earth's gravitational field", "Their mass becomes zero", "They and their spacecraft are in continuous free fall together", "D"),
        ("Which statement about the asteroid belt is correct?", "It contains more mass than all planets combined", "It lies mainly between Mars and Jupiter", "It is located between Earth and Venus", "It is a solid ring with no gaps", "B"),
        ("What is the Roche limit in planetary science?", "The distance at which sunlight becomes zero", "The distance where a satellite's orbital period is one year", "A distance within which tidal forces can disrupt a satellite held together mainly by gravity", "The maximum distance a comet can travel", "C"),
        ("Why do comets often develop tails when they approach the Sun?", "Solar heating releases gas and dust, which are pushed away by sunlight and the solar wind", "They collide with Earth's atmosphere", "Their solid cores melt completely into stars", "Their tails are made of liquid oceans", "A"),
        ("Which statement distinguishes a meteor from a meteoroid?", "A meteor is a planet", "A meteoroid is always larger than Earth", "A meteor is a star", "A meteor is the visible atmospheric phenomenon caused by a meteoroid or related debris entering the atmosphere", "D"),
        ("What is the approximate orbital speed of Earth around the Sun?", "3 km/s", "30 km/s", "300 km/s", "3000 km/s", "B"),
        ("A planet is twice as far from a Sun-like star as Earth. Approximately what is its orbital period?", "2 years", "4 years", "2√2 years", "8 years", "C"),
        ("Which observation provides strong evidence that the universe is expanding?", "The systematic redshift of light from distant galaxies", "The daily rising of the Sun", "The phases of Earth's Moon", "The existence of Earth's seasons", "A"),
        ("What is the main difference between a meteoroid and an asteroid in common astronomical usage?", "Meteoroids are stars and asteroids are planets", "Asteroids are always made of ice only", "Meteoroids orbit Earth only", "Asteroids are generally larger rocky or metallic bodies, while meteoroids are smaller space objects", "D"),
        ("Why is the Sun's gravitational influence important to the solar system?", "It creates all matter from nothing", "It keeps planets and many smaller bodies in gravitationally bound orbits", "It stops all objects from moving", "It removes the need for orbital velocity", "B"),
        ("What does a planet's orbital eccentricity measure?", "Its mass", "Its surface gravity", "How much its orbit deviates from a perfect circle", "Its number of moons", "C"),
        ("What is the approximate orbital period of Mars?", "687 Earth days", "365 Earth days", "88 Earth days", "29.5 Earth days", "A"),
        ("Which planet has an axial tilt so extreme that it rotates almost on its side?", "Mercury", "Mars", "Saturn", "Uranus", "D"),
        ("What is the main source of the Sun's energy over billions of years?", "Chemical reactions", "Nuclear fusion of hydrogen into helium", "Burning oxygen", "Gravitational friction alone", "B"),
        ("Why are the inner planets generally rocky while Jupiter and Saturn are gas giants?", "The inner planets formed only after all gas vanished", "The Sun has no gravity in the outer solar system", "Temperature and early solar-system conditions influenced which materials could condense and how planets grew", "Rocky material cannot exist beyond Mars", "C"),
        ("What is the approximate time taken by sunlight to reach Earth?", "About 8 minutes 20 seconds", "About 8 seconds", "About 1 hour", "About 24 hours", "A"),
        ("What is the main reason an artificial satellite remains in orbit rather than falling straight to Earth?", "There is no gravity acting on it", "It is supported by air", "It has no mass", "Its sideways velocity and Earth's gravitational pull combine to produce continuous free fall around Earth", "D"),
        ("If a planet's distance from a Sun-like star increases from 1 AU to 4 AU, what is its approximate orbital period according to Kepler's third law?", "4 years", "8 years", "16 years", "64 years", "B"),
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
                "SELECT question FROM questions WHERE quiz_id = ?", (quiz_id,)
            )
            existing = {normalize(row[0]) for row in cursor.fetchall()}

            cursor.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?", (quiz_id,)
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
