
import sqlite3
from pathlib import Path
import re

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

LESSON_TITLE = "Light and Shadows"
TARGET_QUESTIONS = 30

QUESTIONS = {
    "Easy": [
        ("What is light?", "A form of energy that enables us to see objects", "A type of sound", "A form of matter", "A magnetic force", "A"),
        ("Which of these is a natural source of light?", "Moon", "Sun", "Mirror", "Book", "B"),
        ("Which object is a luminous object?", "Moon", "Wooden table", "Burning candle", "Stone", "C"),
        ("Which object allows most light to pass through it?", "Wood", "Cardboard", "Metal sheet", "Clear glass", "D"),
        ("Which material is opaque?", "Wood", "Clear glass", "Clean water", "Transparent plastic", "A"),
        ("Which material is translucent?", "A thick metal plate", "Frosted glass", "A wooden board", "A brick", "B"),
        ("What is a shadow?", "A bright reflection", "A source of light", "A dark region formed when light is blocked", "A type of transparent material", "C"),
        ("What is needed to form a shadow?", "Only a mirror", "Only a transparent object", "Only a screen", "A light source, an object, and a surface or screen", "D"),
        ("In which direction does light travel in a uniform medium?", "In straight lines", "Only in circles", "Only downward", "In random zigzags", "A"),
        ("Which object is non-luminous?", "The Sun", "The Moon", "A lit bulb", "A burning candle", "B"),
        ("Why can we see the Moon?", "It produces its own visible light like the Sun", "It is always transparent", "It reflects sunlight toward Earth", "It absorbs all light", "C"),
        ("Which object usually produces a sharp shadow?", "Clear glass", "Clean water", "A transparent sheet", "An opaque object", "D"),
        ("What happens when an opaque object blocks light?", "A shadow can form behind it", "Light passes through completely", "The object becomes luminous", "Light changes into sound", "A"),
        ("Which of these is a man-made source of light?", "Sun", "Electric bulb", "Stars", "Lightning", "B"),
        ("Which property of light helps explain the formation of shadows?", "Light always bends around every object", "Light cannot travel through space", "Light travels approximately in straight lines in a uniform medium", "Light travels only through solids", "C"),
        ("Which object is transparent?", "Brick", "Wooden door", "Thick cardboard", "Clear window glass", "D"),
        ("What is a screen used for in a simple shadow experiment?", "To receive the shadow", "To create electricity", "To make the object transparent", "To produce sound", "A"),
        ("What happens to a shadow when an object is moved closer to a nearby light source, with the screen fixed farther away?", "It always disappears", "It generally becomes larger", "It always becomes smaller", "It becomes transparent", "B"),
        ("Which object can form a shadow even though it does not produce light?", "A lit candle", "The Sun", "A book", "A glowing bulb", "C"),
        ("Which of these is a natural luminous object?", "Moon", "Mirror", "Planet seen by reflected sunlight", "A star", "D"),
        ("What is a ray of light commonly used to represent?", "The direction in which light travels", "The mass of a light source", "The temperature of an object", "The colour of a shadow", "A"),
        ("Which object is most likely to cast a faint shadow?", "A thick wooden plank", "A translucent sheet", "A metal wall", "A stone block", "B"),
        ("Can a shadow form in a completely dark room with no light source?", "Yes, always", "Only behind transparent objects", "No, a light source is needed", "Only at noon", "C"),
        ("Which source produces light when switched on?", "A cold metal spoon", "A book", "An unlit mirror", "An electric lamp", "D"),
        ("What happens to the size of a shadow if the object is moved closer to the screen while the light source stays fixed?", "It generally becomes smaller", "It always becomes larger", "It changes into a reflection", "It disappears in every case", "A"),
        ("Which of these objects is opaque?", "Clear plastic film", "A stone", "Clear glass", "Clean air", "B"),
        ("Which statement about shadows is correct?", "Shadows always have the same colour as the object", "Shadows are sources of light", "Shadows are formed where light is blocked", "Shadows can form only outdoors", "C"),
        ("Which object can be used to redirect light by reflection?", "A black cloth", "A brick", "A piece of opaque wood", "A plane mirror", "D"),
        ("What is the dark region behind an opaque object called?", "Shadow", "Spectrum", "Beam", "Reflection", "A"),
        ("Which of these is an example of light travelling through a transparent material?", "Light hitting a brick wall", "Light passing through a clear window", "Light blocked by a book", "Light absorbed by black paper", "B"),
    ],
    "Medium": [
        ("Why does a small hole in a card produce a narrow beam of sunlight in a suitable setup?", "Light always travels in circles", "Light changes into sound", "Light travels approximately in straight lines", "The card produces new light", "C"),
        ("A student stands between a lamp and a screen. What forms on the screen if the student blocks the lamp's light?", "A reflection only", "A rainbow", "A transparent region", "A shadow", "D"),
        ("Why is the shadow of a person usually longer in the early morning than around noon on a clear day?", "The Sun is lower in the sky in the morning", "People become taller in the morning", "Light travels more slowly in the morning", "The ground becomes transparent", "A"),
        ("Which arrangement can produce the largest shadow on a screen?", "Object close to screen and far from source", "Object close to source and farther from screen", "Source very far away and object touching screen", "No light source", "B"),
        ("What happens when an opaque object is placed directly in the path of a narrow beam of light?", "The light passes through unchanged", "The object becomes transparent", "The object blocks the beam and may cast a shadow", "The beam becomes sound", "C"),
        ("Why does a transparent glass sheet generally produce a less distinct shadow than an opaque board?", "It absorbs all incident light", "It reflects all light", "It produces its own light", "It transmits most of the light", "D"),
        ("Which factor affects the size of a shadow in a simple lamp-object-screen setup?", "The relative positions of the lamp, object, and screen", "Only the object's colour", "Only the object's name", "The mass of the screen alone", "A"),
        ("What is a point source of light in an idealised model?", "A source spread over a large area", "A source treated as having negligible size", "A source that produces no light", "A source that only reflects light", "B"),
        ("Why can an extended light source produce a penumbra?", "Light cannot travel in straight lines", "The object becomes transparent", "Some parts of the source are blocked while others remain visible", "The screen produces light", "C"),
        ("What is the umbra of a shadow?", "The brightly lit region around an object", "The region where all light passes through", "The reflected image of an object", "The region where the light source is completely blocked", "D"),
        ("What is the penumbra?", "A partially shaded region where some light from an extended source is blocked", "A region of complete transparency", "The surface of a mirror", "A luminous object", "A"),
        ("Why does the Sun appear to move across the sky during the day?", "The Sun revolves around Earth every day", "Earth rotates on its axis", "The Moon blocks sunlight continuously", "Light bends around Earth once a day", "B"),
        ("Which arrangement is needed to observe a shadow on a wall?", "Wall alone in total darkness", "Object alone without light", "Light source, blocking object, and wall in a suitable arrangement", "Two transparent sheets only", "C"),
        ("An object is moved closer to a point-like lamp while the screen stays in place. What usually happens to its shadow size?", "It always disappears", "It becomes smaller in every setup", "It does not change in any setup", "It becomes larger", "D"),
        ("What is the main difference between a shadow and a reflection?", "A shadow is a region where light is blocked, while a reflection is light redirected from a surface", "A shadow always produces light", "A reflection is always completely black", "They are exactly the same phenomenon", "A"),
        ("Why does an opaque object have a dark region behind it?", "It generates extra light", "It prevents light from reaching that region directly", "It converts all light into sound", "It makes the screen disappear", "B"),
        ("Which condition usually makes a shadow sharper?", "Using a very large nearby light source", "Using several light sources from different directions", "Using a small light source and a suitable screen arrangement", "Using only transparent objects", "C"),
        ("Why can shadows of the same object change shape during the day outdoors?", "The object's mass changes", "The ground stops reflecting light", "Light becomes a solid", "The direction of sunlight changes", "D"),
        ("Which statement about the Moon's own light is correct?", "The Moon mostly reflects sunlight", "The Moon is a star", "The Moon creates sunlight", "The Moon is always transparent", "A"),
        ("Why is a shadow not usually as colourful as the object casting it?", "The shadow produces every colour equally", "The shadow region receives less direct light, so the object's surface colours are not seen there in the same way", "The object changes its chemical composition", "The screen becomes luminous", "B"),
        ("Which object is most likely to transmit light diffusely and form a blurred shadow?", "A thick metal plate", "A brick", "Frosted glass", "A wooden block", "C"),
        ("What happens when two opaque objects overlap in the path of a light source?", "Both become transparent", "No shadow can form", "Only the brighter object casts a shadow", "Their shadows may overlap on the screen", "D"),
        ("Which factor does NOT directly determine the geometric size of a shadow in an ideal point-source setup?", "The relative distances between source, object, and screen", "The object's position", "The screen's position", "The object's chemical composition by itself", "D"),
        ("A lamp is placed to the left of an opaque ball, with a screen to the right. On which side of the ball is its shadow formed?", "On the side away from the lamp, toward the screen", "On the lamp-facing side only", "Inside the lamp", "Nowhere", "A"),
        ("Why does an object cast a shadow in sunlight?", "Sunlight passes completely through every object", "The object blocks some sunlight from reaching the ground", "The ground produces the object", "The object absorbs the ground", "B"),
        ("Which setup best demonstrates rectilinear propagation of light?", "A magnet attracting iron filings", "Water flowing down a slope", "Aligning several holes in cards so a candle is visible only when the holes line up", "Heating a metal rod", "C"),
        ("What is the effect of moving a screen farther from an opaque object while a nearby point source remains fixed?", "The shadow always vanishes", "The object becomes luminous", "The shadow changes into a reflection", "The shadow generally becomes larger", "D"),
        ("Which is the best explanation for the dark patch formed by a book under a lamp?", "The book blocks light from reaching that part of the surface", "The book creates a hole in the surface", "The book removes gravity", "The lamp stops producing light everywhere", "A"),
        ("What does a translucent object do to incident light?", "It blocks all light", "It transmits some light but scatters it", "It emits light without a source", "It reflects every ray perfectly", "B"),
        ("Which event is caused by the Moon coming between the Sun and Earth and blocking sunlight from part of Earth?", "Lunar eclipse", "Seasons", "Solar eclipse", "Tides only", "C"),
    ],
    "Hard": [
        ("In a point-source model, an opaque object is moved closer to the source while the screen remains fixed. What happens to the shadow's size?", "It generally becomes larger", "It always becomes smaller", "It always disappears", "It remains the same for every position", "A"),
        ("Why does a small, distant light source tend to produce a sharper shadow than a large nearby source?", "It produces no light", "It creates less variation in the directions from which light reaches the object", "It makes opaque objects transparent", "It changes the screen's colour", "B"),
        ("What causes the umbra during an eclipse?", "Light passing through the Moon", "Reflection from Earth's atmosphere only", "Complete blockage of the light source from that region", "The Sun switching off", "C"),
        ("What causes the penumbra during an eclipse?", "Complete blockage of every ray from the source", "The absence of an object", "The source producing no light", "Partial blockage of light from an extended source", "D"),
        ("A light source, an opaque object, and a screen are aligned. If the object is moved toward the screen, what generally happens to the shadow's size for a fixed point source?", "It becomes smaller", "It becomes infinitely large", "It always becomes brighter than the screen", "It cannot be observed", "A"),
        ("Which statement correctly describes rectilinear propagation of light?", "Light always follows curved paths in air", "Light travels in straight lines through a uniform medium", "Light can travel only through solids", "Light needs sound to travel", "B"),
        ("Why can a large extended source produce a less sharp shadow edge than a small source?", "The object becomes luminous", "The screen absorbs all light", "Different parts of the source illuminate different parts of the region around the object", "Light stops travelling in straight lines", "C"),
        ("An opaque ball is illuminated by two lamps from different directions. What is likely to happen?", "There will never be a shadow", "The ball becomes transparent", "Only one lamp can illuminate the ball", "Overlapping or multiple shadow regions may form", "D"),
        ("During a solar eclipse, why is a total solar eclipse visible only from a limited region of Earth?", "The Moon's umbra covers only a limited area of Earth's surface", "The Sun's light reaches only one country", "Earth becomes transparent", "The Moon emits no gravity", "A"),
        ("What distinguishes a lunar eclipse from a solar eclipse?", "A lunar eclipse occurs when the Moon is between the Sun and Earth", "A lunar eclipse occurs when Earth is between the Sun and Moon", "A lunar eclipse requires the Moon to produce light", "A lunar eclipse happens every day", "B"),
        ("Why can a transparent glass object still produce a faint shadow under some conditions?", "Glass is always opaque", "Glass absorbs every ray", "Some light may be reflected or absorbed, and imperfections can scatter light", "Glass produces no interaction with light", "C"),
        ("Which statement about the colour of a shadow is most accurate?", "A shadow is always pure black under every condition", "A shadow has the exact colour of the object", "A shadow is a separate material", "A shadow is a region receiving less direct light and can still be illuminated by other sources", "D"),
        ("In a simple setup, the object is 20 cm from a point source and the screen is 80 cm from the source. What is the approximate ratio of shadow height to object height?", "4:1", "1:4", "2:1", "1:1", "A"),
        ("In the same point-source model, the object is 30 cm from the source and the screen is 90 cm from the source. What is the ratio of shadow height to object height?", "1:3", "3:1", "2:1", "1:1", "B"),
        ("A 5 cm object is 10 cm from a point source. A screen is 30 cm from the source. What is the approximate shadow height?", "5 cm", "10 cm", "15 cm", "20 cm", "C"),
        ("A 4 cm object is 20 cm from a point source, and a screen is 100 cm from the source. What is the approximate shadow height?", "4 cm", "8 cm", "16 cm", "20 cm", "D"),
        ("Which change would most likely make the penumbra wider for an extended source?", "Increasing the angular size of the source as seen from the object", "Replacing the source with an ideal point source", "Making the source infinitely small", "Removing the object", "A"),
        ("Why does a pinhole camera form an inverted image in the ideal ray model?", "Light changes into sound at the hole", "Light rays from opposite parts of the object cross at the small aperture", "The screen rotates the image", "The object becomes transparent", "B"),
        ("Which principle explains why the Sun can cast shadows of objects on Earth?", "Light travels only through opaque matter", "Light must travel in circles", "Light travels approximately in straight lines through a uniform medium", "Shadows attract sunlight", "C"),
        ("What is the main reason the Moon has phases?", "Earth's shadow covers the Moon every night", "The Moon produces changing amounts of its own light", "Clouds cover different parts of the Moon", "We see different portions of the Moon's sunlit half as it orbits Earth", "D"),
        ("Which statement correctly compares a solar eclipse with a lunar eclipse?", "A solar eclipse involves the Moon's shadow falling on Earth; a lunar eclipse involves Earth's shadow falling on the Moon", "Both require Earth to be between the Sun and Moon", "Both occur every new moon", "Neither involves shadows", "A"),
        ("Why are shadows at noon often shorter than shadows in early morning at the same location?", "The Sun becomes smaller at noon", "The Sun is generally higher in the sky around noon", "Objects lose height at noon", "Light stops travelling in straight lines at noon", "B"),
        ("A shadow appears on a screen even though the object itself is not luminous. What is the best explanation?", "The object creates light inside the screen", "The screen absorbs all light in the room", "The object blocks light from the source from reaching part of the screen", "The object changes into a source of light", "C"),
        ("In an ideal point-source setup, which change would leave the shadow-to-object size ratio unchanged?", "Moving the object while keeping the source and screen fixed", "Moving the screen without changing any other distance", "Changing the source position relative to the object", "Scaling all source-object-screen distances by the same factor", "D"),
        ("Which statement about light and opaque materials is correct?", "Opaque materials do not transmit visible light through them in the ordinary sense", "Opaque materials always emit visible light", "Opaque materials allow all visible light through", "Opaque materials have no surface", "A"),
        ("Why can a shadow edge become blurry when a light source has a large apparent size?", "The object has no shape", "Partial illumination occurs near the edge because some source points are blocked and others are visible", "The screen stops existing", "The source becomes a mirror", "B"),
        ("An object casts a 12 cm shadow when the source-screen distance is 60 cm and source-object distance is 20 cm. What is the object's height in the point-source model?", "2 cm", "3 cm", "4 cm", "6 cm", "C"),
        ("Which arrangement is most likely to produce a total solar eclipse for an observer?", "Earth between the Sun and Moon during a full moon", "Moon at a right angle to the Sun-Earth line", "The Sun between Earth and the Moon", "Observer located in the Moon's umbra on Earth when the Sun, Moon, and observer align", "D"),
        ("Why do multiple lights in a room often make a shadow appear less dark?", "Light from other directions can illuminate the region shadowed by one source", "The object stops blocking light", "All sources switch off", "The screen becomes transparent", "A"),
        ("What happens to the shadow of an object if the light source is removed completely?", "It becomes larger", "No new source-cast shadow can form in the absence of illumination", "It becomes a reflection", "It becomes luminous", "B"),
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
