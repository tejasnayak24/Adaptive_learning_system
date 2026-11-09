
import sqlite3
from pathlib import Path
import re

DATABASE_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"
LESSON_TITLE = "Reflection of Light"
TARGET_QUESTIONS = 30

QUESTIONS = {
    "Easy": [
        ("What is reflection of light?", "Bending of light when entering water", "Bouncing back of light from a surface", "Splitting of light into colours", "Production of sound by light", "B"),
        ("Which object is commonly used as a plane mirror?", "A polished mirror", "A piece of rough wood", "A brick", "A sheet of cardboard", "A"),
        ("What is the incident ray?", "The ray leaving a mirror", "The ray absorbed by an object", "The ray that strikes a surface", "The ray that forms a shadow only", "C"),
        ("What is the reflected ray?", "The ray travelling toward the mirror", "A ray that cannot be seen", "The ray passing through an opaque wall", "The ray that bounces off a surface", "D"),
        ("What is the normal at a point on a reflecting surface?", "A line perpendicular to the surface at that point", "A line parallel to the surface", "The reflected ray itself", "The incident ray itself", "A"),
        ("The angle of incidence is measured between the incident ray and the:", "Reflecting surface", "Normal", "Mirror edge", "Reflected image", "B"),
        ("According to the law of reflection, the angle of incidence is:", "Always twice the angle of reflection", "Always zero", "Equal to the angle of reflection", "Always 90 degrees", "C"),
        ("The incident ray, reflected ray, and normal at the point of incidence lie in:", "Three unrelated planes", "A circle", "Different parallel planes", "The same plane", "D"),
        ("Which surface generally produces regular reflection?", "A smooth, polished surface", "A very rough wall", "Crinkled paper", "Uneven soil", "A"),
        ("Which surface commonly produces diffuse reflection?", "A clean plane mirror", "A rough wall", "A polished steel sheet", "A smooth mirror", "B"),
        ("What type of image does a plane mirror normally form?", "Real and inverted", "Real and enlarged", "Virtual and upright", "Virtual and upside down", "C"),
        ("In a plane mirror, the image is generally:", "Smaller than the object", "Larger than the object", "Always inverted vertically", "The same size as the object", "D"),
        ("If an object is 2 m in front of a plane mirror, how far behind the mirror is its image?", "2 m", "1 m", "4 m", "0.5 m", "A"),
        ("An object is 3 m in front of a plane mirror. What is the distance between the object and its image?", "3 m", "6 m", "9 m", "1.5 m", "B"),
        ("What is lateral inversion?", "An image becoming larger", "An image becoming darker", "The apparent left-right reversal in a plane mirror", "The bending of light in water", "C"),
        ("Which device uses multiple reflections to form many images?", "Thermometer", "Barometer", "Ammeter", "Kaleidoscope", "D"),
        ("Which type of mirror is commonly used as a rear-view mirror in vehicles?", "Convex mirror", "Plane mirror only", "Concave mirror only", "A transparent glass sheet", "A"),
        ("Which mirror can produce a magnified upright image when the object is close to it?", "Convex mirror", "Concave mirror", "Plane mirror", "A rough wall", "B"),
        ("Which mirror always forms a virtual, upright, diminished image of a real object placed in front of it?", "Concave mirror", "Plane mirror", "Convex mirror", "None of these", "C"),
        ("What is the principal axis of a spherical mirror?", "A line along the mirror's curved edge", "A line tangent to the mirror", "A line perpendicular to every ray", "The line passing through the pole and centre of curvature", "D"),
        ("What is the pole of a spherical mirror?", "The centre point of its reflecting surface", "The centre of curvature", "The principal focus", "The edge of the mirror only", "A"),
        ("What is the centre of curvature of a spherical mirror?", "The point where all reflected rays meet", "The centre of the sphere of which the mirror is a part", "The pole of the mirror", "The image position", "B"),
        ("What is the principal focus of a concave mirror for rays parallel to its principal axis?", "The pole", "The centre of curvature", "The point where the reflected rays converge approximately", "The edge of the mirror", "C"),
        ("What is the focal length of a spherical mirror?", "The distance between the object and image", "The diameter of the mirror", "The distance from the pole to the edge", "The distance between the pole and principal focus", "D"),
        ("For a spherical mirror of small aperture, the radius of curvature is approximately how related to focal length?", "R = 2f", "R = f/2", "R = 3f", "R = f", "A"),
        ("Which mirror is often used by dentists to view enlarged images of teeth at close range?", "Convex mirror", "Concave mirror", "Plane mirror only", "A rough mirror", "B"),
        ("Which mirror provides a wide field of view for security and traffic observation?", "Concave mirror", "Plane mirror", "Convex mirror", "A transparent lens", "C"),
        ("What happens to the angle of reflection if the angle of incidence is 35 degrees?", "70 degrees", "55 degrees", "90 degrees", "35 degrees", "D"),
        ("A ray strikes a plane mirror along the normal. What is its angle of incidence?", "0 degrees", "45 degrees", "90 degrees", "180 degrees", "A"),
        ("Which statement about a virtual image is correct?", "It can always be projected onto a screen", "It appears to come from a point where light rays do not actually meet", "It is always larger than the object", "It is always upside down", "B"),
    ],

    "Medium": [
        ("A ray strikes a plane mirror at an angle of incidence of 40 degrees. What is its angle of reflection?", "20 degrees", "50 degrees", "40 degrees", "80 degrees", "C"),
        ("A ray makes an angle of 30 degrees with the mirror surface. What is its angle of incidence?", "30 degrees", "60 degrees", "90 degrees", "150 degrees", "B"),
        ("A ray makes an angle of incidence of 25 degrees. What angle does the reflected ray make with the mirror surface?", "25 degrees", "90 degrees", "115 degrees", "65 degrees", "D"),
        ("An object is placed 4 cm in front of a plane mirror. What is the distance between the object and its image?", "8 cm", "4 cm", "2 cm", "16 cm", "A"),
        ("A person walks 1 m toward a stationary plane mirror. By how much does the distance between the person and the image decrease?", "1 m", "2 m", "0.5 m", "4 m", "B"),
        ("If a plane mirror is rotated by 10 degrees while the incident ray remains fixed, by how much does the reflected ray rotate?", "5 degrees", "10 degrees", "20 degrees", "40 degrees", "C"),
        ("Why can a plane mirror form a clear image while a rough wall usually does not?", "A wall absorbs all light", "A mirror creates light", "A wall has no reflecting surface", "A smooth mirror produces regular reflection, while a rough surface scatters reflected light in many directions", "D"),
        ("An object is 5 cm in front of a plane mirror. If the mirror is moved 2 cm farther from the stationary object, where is the image relative to the object's original position?", "7 cm behind the mirror's new position, or 9 cm from the original object position", "5 cm from the object", "2 cm in front of the mirror", "10 cm from the object regardless of mirror movement", "A"),
        ("Which image characteristic is associated with a plane mirror?", "Real, inverted, and smaller", "Virtual, upright, and same size", "Real, upright, and enlarged", "Virtual, inverted, and smaller", "B"),
        ("What happens when two plane mirrors are placed at an angle to each other?", "They cannot reflect light", "They always form exactly one image", "They may form multiple images", "They always form a real image", "C"),
        ("Which mirror is suitable for concentrating sunlight at a point?", "Plane mirror", "Convex mirror", "A rough wall", "Concave mirror", "D"),
        ("Why are convex mirrors useful at road bends?", "They provide a wider field of view", "They always magnify distant objects", "They form real images on the road", "They absorb reflected light", "A"),
        ("For a concave mirror, what happens to rays parallel to the principal axis after reflection, approximately?", "They spread out as if from the centre of curvature", "They converge near the principal focus", "They travel through the pole only", "They become parallel to the mirror surface", "B"),
        ("For a convex mirror, parallel rays reflected from the mirror:", "Meet at a real focus in front of the mirror", "Pass through the centre of curvature in every case", "Diverge and appear to originate from a virtual focus behind the mirror", "Are completely absorbed", "C"),
        ("A spherical mirror has a radius of curvature of 40 cm. What is the magnitude of its focal length under the paraxial approximation?", "40 cm", "80 cm", "10 cm", "20 cm", "D"),
        ("A concave mirror has a focal length magnitude of 15 cm. What is its radius of curvature magnitude?", "30 cm", "15 cm", "7.5 cm", "45 cm", "A"),
        ("Which mirror can form a real, inverted image of a real object?", "Plane mirror", "Concave mirror", "Convex mirror", "All mirrors in all positions", "B"),
        ("When does a concave mirror form a virtual, upright, magnified image?", "When the object is beyond the centre of curvature", "When the object is at the centre of curvature", "When the object is between the pole and principal focus", "When the object is infinitely far away", "C"),
        ("What type of image does a convex mirror form for a real object?", "Real and enlarged", "Real and inverted", "Virtual and enlarged", "Virtual, upright, and diminished", "D"),
        ("An object is placed at the centre of curvature of a concave mirror. In the ideal ray model, where is its image formed?", "At the centre of curvature", "At the pole", "At infinity", "Behind the mirror", "A"),
        ("What happens to the image formed by a concave mirror when the object is at its principal focus?", "It is virtual and diminished", "Reflected rays are parallel, so the image is at infinity in the ideal model", "It forms at the pole", "It is always upright and same size", "B"),
        ("Which statement about the image formed by a plane mirror is correct?", "It is always real", "It can be caught directly on a screen", "Its image distance behind the mirror equals the object's distance in front", "Its image is always diminished", "C"),
        ("A ray makes an angle of 60 degrees with the normal. What angle does it make with the mirror surface?", "60 degrees", "120 degrees", "90 degrees", "30 degrees", "D"),
        ("What is the angle between the incident and reflected rays when the angle of incidence is 30 degrees?", "60 degrees", "30 degrees", "90 degrees", "120 degrees", "A"),
        ("A person stands 2 m in front of a plane mirror. How far must they move toward the mirror to reduce the person-image distance to 2 m?", "2 m", "1 m", "0.5 m", "1.5 m", "B"),
        ("Why is the image in a plane mirror described as laterally inverted?", "It is always upside down", "It has no depth", "The left and right sides appear interchanged", "It is smaller than the object", "C"),
        ("Which statement about the principal focus of a convex mirror is correct?", "It is a real point in front of the mirror", "It is always at the pole", "It is the point where all rays physically meet behind the mirror", "It is a virtual point from which reflected parallel rays appear to diverge", "D"),
        ("Which surface produces diffuse reflection even though it obeys the law of reflection locally?", "A rough surface with differently oriented microscopic regions", "A perfect plane mirror", "A perfectly smooth polished metal surface only", "A transparent vacuum", "A"),
        ("A ray makes 20 degrees with the normal at incidence. What is the angle between the incident and reflected rays?", "20 degrees", "40 degrees", "70 degrees", "160 degrees", "B"),
        ("Which quantity is measured from the pole of a spherical mirror to its principal focus?", "Radius of curvature", "Object distance", "Focal length", "Image height", "C"),
    ],

    "Hard": [
        ("A ray strikes a plane mirror at 37 degrees to the normal. What is the angle between the incident and reflected rays?", "74 degrees", "37 degrees", "53 degrees", "90 degrees", "A"),
        ("A ray makes 20 degrees with the mirror surface. The mirror is rotated by 5 degrees while the incident ray stays fixed. By how much does the reflected ray rotate?", "5 degrees", "10 degrees", "15 degrees", "20 degrees", "B"),
        ("A person is 3 m from a plane mirror. The person moves 0.5 m toward it. What is the new distance between the person and the image?", "2 m", "2.5 m", "5 m", "6 m", "C"),
        ("A plane mirror is moved 1 m away from a stationary object. How far does the image move relative to its original position?", "0.5 m", "1 m", "3 m", "2 m", "D"),
        ("A concave mirror has a radius of curvature of 60 cm. What is its focal length magnitude?", "30 cm", "60 cm", "120 cm", "15 cm", "A"),
        ("An object is placed 30 cm in front of a concave mirror with focal length magnitude 15 cm. Where is the image formed in the ideal mirror model?", "At infinity", "30 cm in front of the mirror", "15 cm behind the mirror", "At the pole", "B"),
        ("An object is placed between the pole and focus of a concave mirror. Which image is formed?", "Real, inverted, and diminished", "Real, upright, and enlarged", "Virtual, upright, and enlarged", "Virtual, inverted, and diminished", "C"),
        ("Which statement about a convex mirror is correct for a real object in front of it?", "It always forms a real image", "It forms an inverted enlarged image", "It forms a virtual image at infinity for every object", "It forms a virtual, upright, diminished image", "D"),
        ("A concave mirror produces an image at the centre of curvature when the object is at the centre of curvature. What is the image's orientation and size?", "Inverted and same size", "Upright and magnified", "Upright and diminished", "Virtual and infinitely large", "A"),
        ("A ray strikes a plane mirror at an incidence angle of 0 degrees. What is the angle between the incident and reflected rays as measured between their propagation directions?", "0 degrees", "180 degrees", "90 degrees", "45 degrees", "B"),
        ("Two plane mirrors are parallel and face each other. What is the idealised result for an object placed between them?", "No images form", "Exactly two images form", "Repeated multiple images can form", "Only one real image forms", "C"),
        ("A plane mirror forms an image 2.5 m behind it. How far is the object in front of the mirror?", "1.25 m", "5 m", "0 m", "2.5 m", "D"),
        ("An object is 4 m from a plane mirror. What is the separation between the object and its image?", "8 m", "4 m", "2 m", "16 m", "A"),
        ("The angle between an incident ray and the mirror surface is 35 degrees. What is the angle of reflection measured from the normal?", "35 degrees", "55 degrees", "70 degrees", "145 degrees", "B"),
        ("A concave mirror has a focal length magnitude of 20 cm. An object is placed 60 cm in front of it. Using the mirror formula with the usual Cartesian sign convention, where is the image formed?", "20 cm behind the mirror", "60 cm behind the mirror", "30 cm in front of the mirror", "30 cm behind the mirror", "C"),
        ("A concave mirror has focal length magnitude 10 cm. An object is placed 5 cm in front of it. What is the image nature in the ideal mirror model?", "Real and inverted", "Real and diminished", "At infinity", "Virtual and upright", "D"),
        ("What is the magnification of a plane mirror in the usual signed convention for a real object?", "+1", "−1", "0", "Depends on object colour", "A"),
        ("Which statement correctly compares regular and diffuse reflection?", "Only regular reflection obeys the law of reflection", "Both obey the law of reflection, but diffuse reflection scatters rays due to surface irregularities", "Diffuse reflection occurs only in a vacuum", "Regular reflection cannot form images", "B"),
        ("A ray is incident at 42 degrees to the normal. What angle does the reflected ray make with the mirror surface?", "42 degrees", "48 degrees", "90 degrees", "48 degrees", "D"),
        ("An object is 10 cm in front of a plane mirror. The mirror is moved 3 cm away from the object. What is the new object-image separation?", "26 cm", "20 cm", "13 cm", "6 cm", "A"),
        ("A concave mirror forms a real image twice the object's height in magnitude. Which statement about magnification is correct?", "The signed magnification is +2", "The signed magnification is −2 for an inverted real image", "The signed magnification is always zero", "The image must be virtual", "B"),
        ("A spherical mirror has radius of curvature 50 cm. What is the magnitude of its focal length?", "50 cm", "100 cm", "25 cm", "12.5 cm", "C"),
        ("Which condition is most important for the simple relation R = 2f to be a good approximation for a spherical mirror?", "The mirror must be transparent", "The object must touch the mirror", "The surface must be rough", "The mirror has a small aperture and paraxial rays are considered", "D"),
        ("An object is placed 20 cm in front of a concave mirror of focal length magnitude 10 cm. What is the image position?", "20 cm in front of the mirror", "10 cm behind the mirror", "At infinity", "At the pole", "A"),
        ("Which mirror is most appropriate for producing a wide field of view in a shop security system?", "Concave mirror", "Convex mirror", "Plane mirror with no curvature", "A rough black surface", "B"),
        ("A plane mirror is rotated through 12 degrees while the incident ray direction remains fixed. Through what angle does the reflected ray rotate?", "6 degrees", "12 degrees", "24 degrees", "48 degrees", "C"),
        ("An object and its image in a plane mirror are 14 m apart. How far is the object from the mirror?", "14 m", "28 m", "3.5 m", "7 m", "D"),
        ("A ray makes an angle of 15 degrees with a plane mirror surface. What is the angle between the incident and reflected rays?", "150 degrees", "30 degrees", "15 degrees", "75 degrees", "A"),
        ("A concave mirror forms an image at infinity when the object is placed at which position?", "At the centre of curvature", "At the principal focus", "At the pole", "Behind the mirror", "B"),
        ("Why can a plane mirror not form a real image of an ordinary real object placed in front of it?", "It absorbs all incident light", "It has no reflecting surface", "The reflected rays diverge and only appear to come from behind the mirror", "It always focuses parallel rays at the pole", "C"),
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
