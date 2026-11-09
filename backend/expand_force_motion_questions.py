import sqlite3
from pathlib import Path

DATABASE_PATH = (
    Path(__file__).resolve().parent.parent
    / "adaptive_learning.db"
)

TARGET_QUESTIONS = 30

QUESTION_BANK = {
    "Easy": [
        ("What is a force?", "A push or pull", "A type of energy only", "A unit of time", "A form of matter", "A"),
        ("What is the SI unit of force?", "Joule", "Newton", "Watt", "Pascal", "B"),
        ("Which instrument measures force?", "Thermometer", "Barometer", "Spring balance", "Stopwatch", "C"),
        ("What is the SI unit of speed?", "Kilogram", "Newton", "Joule", "Metre per second", "D"),
        ("What is the formula for speed?", "Distance divided by time", "Time divided by distance", "Mass multiplied by acceleration", "Distance multiplied by time", "A"),
        ("Which quantity describes how fast an object changes position?", "Force", "Speed", "Mass", "Pressure", "B"),
        ("What is the SI unit of acceleration?", "Metre", "Second", "Metre per second squared", "Kilogram", "C"),
        ("Which force pulls objects towards Earth?", "Friction", "Magnetic force", "Muscular force", "Gravity", "D"),
        ("What force opposes motion between surfaces in contact?", "Friction", "Gravity", "Buoyancy", "Electrostatic force", "A"),
        ("What is the SI unit of mass?", "Newton", "Kilogram", "Metre", "Watt", "B"),
        ("Which of these is a contact force?", "Gravitational force", "Magnetic force", "Frictional force", "Electrostatic force", "C"),
        ("Which quantity measures the amount of matter in an object?", "Speed", "Acceleration", "Force", "Mass", "D"),
        ("What happens when balanced forces act on a stationary object?", "It remains stationary", "It must accelerate", "Its mass doubles", "Its weight becomes zero", "A"),
        ("What does a speedometer measure?", "Distance", "Speed", "Force", "Acceleration", "B"),
        ("What is the SI unit of distance?", "Kilogram", "Newton", "Metre", "Joule", "C"),
        ("What can an unbalanced force do to an object?", "Only change its colour", "Always reduce its mass", "Never change its motion", "Change its motion", "D"),
        ("Which quantity has both magnitude and direction?", "Velocity", "Distance", "Speed", "Time", "A"),
        ("What is the formula for acceleration?", "Distance divided by time", "Change in velocity divided by time", "Mass divided by volume", "Force multiplied by distance", "B"),
        ("Which law states that an object remains at rest or in uniform motion unless acted on by a net external force?", "Newton's third law", "Law of gravitation only", "Newton's first law", "Law of conservation of mass", "C"),
        ("What is inertia?", "The ability to create energy", "The force of friction", "The speed of an object", "The tendency to resist changes in motion", "D"),
        ("Which force helps a person walk without slipping on the ground?", "Friction", "Magnetism", "Buoyancy", "Electrostatic force", "A"),
        ("What is the SI unit of work?", "Watt", "Joule", "Newton", "Pascal", "B"),
        ("Which quantity is calculated by multiplying mass by velocity?", "Acceleration", "Force", "Momentum", "Power", "C"),
        ("What happens to the velocity of an object moving at constant speed in a straight line?", "It continuously increases", "It continuously decreases", "It becomes zero immediately", "It remains constant", "D"),
        ("Which force acts without direct physical contact?", "Gravitational force", "Friction between surfaces", "Normal contact force", "Tension in a rope", "A"),
        ("What is displacement?", "The total path travelled", "Change in position in a specified direction", "The time taken for a journey", "The mass of an object", "B"),
        ("Which graph can show distance travelled against time?", "A pie chart only", "A periodic table", "A distance-time graph", "A food chain", "C"),
        ("What is the approximate acceleration due to gravity near Earth's surface?", "1.0 m/s²", "3.0 m/s²", "5.0 m/s²", "9.8 m/s²", "D"),
        ("What is the formula for force according to Newton's second law?", "Force = mass × acceleration", "Force = distance ÷ time", "Force = mass ÷ volume", "Force = speed × time", "A"),
        ("When is mechanical work done by a force?", "Whenever an object has mass", "When the force causes displacement with a component along its direction", "Whenever an object is stationary", "Whenever time passes", "B"),
    ],

    "Medium": [
        ("A car travels 100 metres in 5 seconds. What is its average speed?", "10 m/s", "15 m/s", "20 m/s", "25 m/s", "C"),
        ("A 4 kg object accelerates at 3 m/s². What net force acts on it?", "7 N", "1 N", "9 N", "12 N", "D"),
        ("A runner's velocity changes from 2 m/s to 10 m/s in 4 seconds. What is the acceleration?", "2 m/s²", "3 m/s²", "4 m/s²", "8 m/s²", "A"),
        ("What is the momentum of a 5 kg object moving at 4 m/s?", "9 kg·m/s", "20 kg·m/s", "1.25 kg·m/s", "25 kg·m/s", "B"),
        ("A force of 10 N moves an object 3 m in the direction of the force. How much work is done?", "13 J", "7 J", "30 J", "3.3 J", "C"),
        ("A machine performs 100 J of work in 5 seconds. What is its average power?", "5 W", "10 W", "15 W", "20 W", "D"),
        ("Which statement describes Newton's third law?", "Every action has an equal and opposite reaction", "Force always equals mass", "Objects cannot accelerate", "Energy is always destroyed", "A"),
        ("Why do passengers move forward when a moving bus stops suddenly?", "Gravity suddenly disappears", "Their bodies tend to maintain their previous motion", "Their mass increases", "Friction becomes zero everywhere", "B"),
        ("A 2 kg object accelerates at 5 m/s². What is the net force?", "2.5 N", "7 N", "10 N", "15 N", "C"),
        ("A cyclist travels 60 metres in 10 seconds. What is the average speed?", "3 m/s", "5 m/s", "10 m/s", "6 m/s", "D"),
        ("Which factor increases the friction between two dry surfaces in many ordinary situations?", "Increasing the normal force", "Removing all contact", "Eliminating the surfaces", "Reducing the normal force", "A"),
        ("What does the slope of a velocity-time graph represent?", "Distance", "Acceleration", "Mass", "Momentum", "B"),
        ("What does the area under a velocity-time graph represent?", "Acceleration", "Force", "Displacement", "Power", "C"),
        ("A 2 kg object moves at 6 m/s. What is its kinetic energy?", "12 J", "18 J", "24 J", "36 J", "D"),
        ("An object is lifted 2 metres against gravity. If its weight is 50 N, how much work is done against gravity?", "100 J", "25 J", "52 J", "200 J", "A"),
        ("What happens to the momentum of an isolated system when no net external force acts on it?", "It always doubles", "It remains constant", "It becomes zero immediately", "It always decreases", "B"),
        ("Why is it easier to push an empty shopping cart than a fully loaded one?", "The empty cart has more inertia", "Gravity does not act on the empty cart", "The loaded cart generally has greater mass and inertia", "The empty cart has no friction", "C"),
        ("A force of 20 N acts on an object for 3 seconds. What impulse does the force provide if it is constant?", "6 N·s", "17 N·s", "23 N·s", "60 N·s", "D"),
        ("A vehicle slows from 20 m/s to 5 m/s in 3 seconds. What is its acceleration?", "-5 m/s²", "5 m/s²", "-15 m/s²", "15 m/s²", "A"),
        ("Which quantity is a scalar?", "Velocity", "Speed", "Displacement", "Acceleration", "B"),
        ("A 10 kg object has a weight of approximately how much on Earth, taking g = 9.8 m/s²?", "10 N", "49 N", "98 N", "980 N", "C"),
        ("What is the net force when two opposite forces of 12 N and 7 N act on an object?", "19 N", "84 N", "0 N", "5 N towards the 12 N force", "D"),
        ("Why does a sharp knife cut more easily than a blunt knife under the same applied force?", "Its smaller contact area produces greater pressure", "Its mass becomes zero", "It eliminates gravity", "It produces energy from nothing", "A"),
        ("What is the relationship between mass and acceleration for a fixed net force?", "They are directly proportional", "Acceleration is inversely proportional to mass", "They are always equal", "Mass has no effect", "B"),
        ("A 2 kg object is raised through 5 metres. Taking g = 10 m/s², what is the gain in gravitational potential energy?", "10 J", "25 J", "100 J", "50 J", "C"),
        ("A body moves at a constant velocity in a straight line. What is its net acceleration?", "9.8 m/s²", "1 m/s²", "Its velocity divided by mass", "0 m/s²", "D"),
        ("Which quantity describes how quickly velocity changes?", "Acceleration", "Distance", "Mass", "Work", "A"),
        ("What is the momentum of a 3 kg object at rest?", "3 kg·m/s", "0 kg·m/s", "9 kg·m/s", "1 kg·m/s", "B"),
        ("A 100 N force acts over a displacement of 4 m in its direction. What is the work done?", "25 J", "104 J", "400 J", "0 J", "C"),
        ("What does a horizontal line on a velocity-time graph indicate?", "Increasing acceleration", "Increasing speed", "Increasing displacement per second", "Constant velocity", "D"),
    ],

    "Hard": [
        ("A 2 kg object initially at rest experiences a net force of 6 N for 4 seconds. What is its final speed?", "12 m/s", "6 m/s", "8 m/s", "24 m/s", "A"),
        ("A car travelling at 20 m/s stops uniformly in 5 seconds. What is its acceleration?", "4 m/s²", "-4 m/s²", "-5 m/s²", "5 m/s²", "B"),
        ("A 1,000 kg car accelerates at 2 m/s². What is the net force?", "500 N", "1,002 N", "2,000 N", "2 N", "C"),
        ("A 4 kg object moving at 3 m/s collides with a stationary 2 kg object. They stick together. What is their final velocity, assuming no external impulse?", "1 m/s", "3 m/s", "4 m/s", "2 m/s", "D"),
        ("A 10 N force acts at 60 degrees to a displacement of 4 m. What work does it perform?", "20 J", "40 J", "10 J", "0 J", "A"),
        ("A 2 kg object speeds up from 3 m/s to 7 m/s. What is its change in kinetic energy?", "20 J", "40 J", "49 J", "10 J", "B"),
        ("A 1,500 kg car travels at 10 m/s. What is its kinetic energy?", "7,500 J", "15,000 J", "75,000 J", "150,000 J", "C"),
        ("A 5 kg object falls through 4 m. Taking g = 10 m/s² and ignoring air resistance, how much gravitational potential energy is lost?", "20 J", "50 J", "100 J", "200 J", "D"),
        ("A 2 kg object moving at 8 m/s is brought to rest. What is the magnitude of its change in momentum?", "16 kg·m/s", "8 kg·m/s", "4 kg·m/s", "0 kg·m/s", "A"),
        ("A constant net force of 15 N acts for 2 seconds. What is the impulse?", "7.5 N·s", "30 N·s", "17 N·s", "45 N·s", "B"),
        ("A 60 kg person stands in an elevator accelerating upward at 2 m/s². Taking g = 10 m/s², what is the apparent weight?", "480 N", "600 N", "720 N", "120 N", "C"),
        ("A 60 kg person stands in an elevator accelerating downward at 2 m/s². Taking g = 10 m/s², what is the apparent weight?", "720 N", "600 N", "480 N", "120 N", "C"),
        ("A 10 kg block rests on a horizontal surface with coefficient of kinetic friction 0.2. Taking g = 10 m/s², what is the kinetic friction force while it slides horizontally?", "2 N", "10 N", "20 N", "200 N", "C"),
        ("A 4 kg object experiences a net force of 12 N. What is its acceleration?", "48 m/s²", "16 m/s²", "8 m/s²", "3 m/s²", "D"),
        ("An object moves in a circle at constant speed. Why is it accelerating?", "Its velocity direction continuously changes", "Its mass continuously increases", "Its speed must increase", "No force acts on it", "A"),
        ("A 2 kg object moves at 5 m/s. What is its momentum?", "2.5 kg·m/s", "10 kg·m/s", "25 kg·m/s", "7 kg·m/s", "B"),
        ("A 1,000 kg vehicle travelling at 20 m/s is stopped in 4 seconds. What is the magnitude of the average net braking force?", "1,000 N", "2,500 N", "5,000 N", "10,000 N", "C"),
        ("A force of 50 N moves an object 10 m in 5 seconds in the force direction. What is the average power?", "50 W", "100 W", "200 W", "100 W", "B"),
        ("A projectile is launched horizontally at 10 m/s from a height of 20 m. Taking g = 10 m/s² and ignoring air resistance, how long does it take to hit the ground?", "1 s", "4 s", "2 s", "10 s", "C"),
        ("For the projectile in the previous question, how far horizontally does it travel before hitting the ground?", "10 m", "15 m", "40 m", "20 m", "D"),
        ("A 2 kg object moving at 4 m/s collides with a 2 kg object at rest. They stick together. What is their final velocity?", "2 m/s", "4 m/s", "1 m/s", "8 m/s", "A"),
        ("A 5 kg object has a momentum of 20 kg·m/s. What is its speed?", "100 m/s", "4 m/s", "15 m/s", "25 m/s", "B"),
        ("A net force of 8 N acts on a 2 kg object initially at rest for 3 seconds. What is its final momentum?", "12 kg·m/s", "8 kg·m/s", "24 kg·m/s", "6 kg·m/s", "C"),
        ("An object travels 10 m east and then 10 m west to its starting point. What is its total displacement?", "20 m east", "20 m west", "10 m", "0 m", "D"),
        ("A 2 kg object is moving at 3 m/s. What is its kinetic energy?", "9 J", "6 J", "18 J", "3 J", "A"),
        ("A 100 N force acts perpendicular to an object's displacement. How much work does this force perform?", "100 J", "0 J", "50 J", "200 J", "B"),
        ("A 1 kg object is dropped from rest and falls for 3 seconds. Taking g = 10 m/s² and ignoring air resistance, what is its final speed?", "10 m/s", "15 m/s", "30 m/s", "90 m/s", "C"),
        ("A 3 kg object accelerates at 4 m/s². What net force acts on it?", "7 N", "1 N", "9 N", "12 N", "D"),
        ("A 20 kg object is pulled with a horizontal force of 100 N while friction opposes motion with 40 N. What is its acceleration?", "3 m/s²", "5 m/s²", "7 m/s²", "2 m/s²", "A"),
        ("A 2 kg object moving at 10 m/s is stopped by a constant force over 5 m. What is the magnitude of the stopping force?", "10 N", "20 N", "25 N", "40 N", "B"),
    ],
}


def normalize(text):
    return " ".join(text.casefold().split())


def main():
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DATABASE_PATH}"
        )

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        connection.execute("PRAGMA foreign_keys = ON")

        lesson = connection.execute(
            """
            SELECT id
            FROM lessons
            WHERE lower(trim(title)) = lower(trim(?))
            """,
            ("Force and Motion",),
        ).fetchone()

        if lesson is None:
            raise RuntimeError(
                "Force and Motion lesson was not found in the database."
            )

        lesson_id = lesson[0]
        total_inserted = 0

        # Commit all three difficulty levels together.
        with connection:
            for difficulty, candidates in QUESTION_BANK.items():
                quiz = connection.execute(
                    """
                    SELECT id
                    FROM quizzes
                    WHERE lesson_id = ?
                      AND lower(trim(difficulty)) = lower(trim(?))
                    """,
                    (lesson_id, difficulty),
                ).fetchone()

                if quiz is None:
                    raise RuntimeError(
                        f"Missing {difficulty} quiz for Force and Motion."
                    )

                quiz_id = quiz[0]

                existing_rows = connection.execute(
                    """
                    SELECT question
                    FROM questions
                    WHERE quiz_id = ?
                    """,
                    (quiz_id,),
                ).fetchall()

                existing_questions = {
                    normalize(row[0]) for row in existing_rows
                }
                current_count = len(existing_rows)

                if current_count > TARGET_QUESTIONS:
                    raise RuntimeError(
                        f"{difficulty} already has {current_count} "
                        f"questions; target is {TARGET_QUESTIONS}."
                    )

                added = 0

                for item in candidates:
                    if current_count >= TARGET_QUESTIONS:
                        break

                    question, a, b, c, d, answer = item
                    normalized_question = normalize(question)

                    if normalized_question in existing_questions:
                        print(
                            f"Skipping duplicate ({difficulty}): {question}"
                        )
                        continue

                    if answer not in {"A", "B", "C", "D"}:
                        raise ValueError(
                            f"Invalid correct answer: {question}"
                        )

                    if not all(
                        option.strip() for option in (a, b, c, d)
                    ):
                        raise ValueError(
                            f"Empty answer option: {question}"
                        )

                    connection.execute(
                        """
                        INSERT INTO questions (
                            quiz_id,
                            question,
                            option_a,
                            option_b,
                            option_c,
                            option_d,
                            correct_answer
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (quiz_id, question, a, b, c, d, answer),
                    )

                    existing_questions.add(normalized_question)
                    current_count += 1
                    added += 1
                    total_inserted += 1

                if current_count != TARGET_QUESTIONS:
                    raise RuntimeError(
                        f"{difficulty} has {current_count} questions, "
                        f"not {TARGET_QUESTIONS}. Add more unique questions. "
                        "The transaction will roll back."
                    )

                print(
                    f"{difficulty}: added {added}; "
                    f"final count = {current_count}"
                )

        print("\nForce and Motion expansion completed!")
        print(f"Total new questions inserted: {total_inserted}")
        print("Easy: 30 questions")
        print("Medium: 30 questions")
        print("Hard: 30 questions")
        print("Other lessons and Social Science were not modified.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()