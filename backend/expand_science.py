
"""
Expand the Science curriculum.

Target:
- 40 Science lessons
- 3 quizzes per lesson: Easy, Medium, Hard
- 90 questions per lesson (implemented in the question-bank stage)

Existing Social Science lessons and questions are preserved.
seed_science.py is not modified.
"""

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
DATABASE_PATH = PROJECT_ROOT / "adaptive_learning.db"

os.environ["DATABASE_URL"] = (
    f"sqlite:///{DATABASE_PATH.as_posix()}"
)

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


# Import all models so SQLAlchemy can resolve relationships.
import app.models.student
import app.models.lesson
import app.models.quiz
import app.models.question
import app.models.progress
import app.models.session
import app.models.reward

from app.database.connection import SessionLocal
from app.models.lesson import Lesson
from app.models.quiz import Quiz


# The existing five Science lessons are retained.
NEW_SCIENCE_LESSONS = [
    (
        "Introduction to Plants",
        "Plant Biology",
        "Learn about plant structures, roots, stems, leaves, and their functions.",
    ),
    (
        "Photosynthesis",
        "Plant Biology",
        "Understand how plants use sunlight, water, and carbon dioxide to produce food.",
    ),
    (
        "Plant Reproduction",
        "Plant Biology",
        "Explore pollination, fertilization, seeds, and plant reproduction.",
    ),
    (
        "Nutrition in Animals",
        "Biology",
        "Study different modes of nutrition and the human digestive system.",
    ),
    (
        "Respiration in Organisms",
        "Biology",
        "Learn about respiration, breathing, and energy release in organisms.",
    ),
    (
        "Transportation in Plants and Animals",
        "Biology",
        "Explore blood circulation and the transport of water and nutrients in plants.",
    ),
    (
        "Reproduction in Animals",
        "Biology",
        "Understand sexual and asexual reproduction in animals.",
    ),
    (
        "Microorganisms",
        "Biology",
        "Study bacteria, fungi, protozoa, viruses, and their effects on life.",
    ),
    (
        "Food Chains and Food Webs",
        "Ecology",
        "Understand producers, consumers, decomposers, and energy flow in ecosystems.",
    ),
    (
        "Adaptations in Living Organisms",
        "Biology",
        "Explore how organisms adapt to their environments.",
    ),
    (
        "Natural Resources",
        "Environmental Science",
        "Learn about renewable and non-renewable natural resources.",
    ),
    (
        "Pollution and Its Control",
        "Environmental Science",
        "Study air, water, soil, and noise pollution and their prevention.",
    ),
    (
        "Conservation of Biodiversity",
        "Environmental Science",
        "Understand biodiversity and methods for conserving species and habitats.",
    ),
    (
        "Acids, Bases and Salts",
        "Chemistry",
        "Identify acids, bases, indicators, neutralization, and salts.",
    ),
    (
        "Atoms and Molecules",
        "Chemistry",
        "Explore atoms, molecules, chemical symbols, and chemical formulas.",
    ),
    (
        "Elements, Compounds and Mixtures",
        "Chemistry",
        "Compare pure substances, elements, compounds, and mixtures.",
    ),
    (
        "Physical and Chemical Changes",
        "Chemistry",
        "Distinguish physical changes from chemical reactions.",
    ),
    (
        "Metals and Non-Metals",
        "Chemistry",
        "Compare the properties and uses of metals and non-metals.",
    ),
    (
        "Separation of Substances",
        "Chemistry",
        "Learn filtration, evaporation, distillation, sieving, and other methods.",
    ),
    (
        "Structure of the Atom",
        "Chemistry",
        "Study protons, neutrons, electrons, and atomic structure.",
    ),
    (
        "Heat and Temperature",
        "Physics",
        "Understand heat transfer, temperature, and thermal expansion.",
    ),
    (
        "Light and Shadows",
        "Physics",
        "Explore light sources, opaque objects, transparent objects, and shadows.",
    ),
    (
        "Reflection of Light",
        "Physics",
        "Understand reflection and the behavior of light on different surfaces.",
    ),
    (
        "Sound and Its Properties",
        "Physics",
        "Study sound production, vibrations, pitch, loudness, and propagation.",
    ),
    (
        "Electricity and Circuits",
        "Physics",
        "Learn about electric current, cells, conductors, and simple circuits.",
    ),
    (
        "Magnetism",
        "Physics",
        "Explore magnetic poles, magnetic materials, and magnetic fields.",
    ),
    (
        "Work, Energy and Power",
        "Physics",
        "Understand work, kinetic energy, potential energy, and power.",
    ),
    (
        "Simple Machines",
        "Physics",
        "Learn how levers, pulleys, inclined planes, and other machines help us.",
    ),
    (
        "Pressure and Buoyancy",
        "Physics",
        "Explore pressure in solids and fluids, buoyancy, and floating.",
    ),
    (
        "Waves and Vibrations",
        "Physics",
        "Understand vibrations, wave motion, and the transfer of energy.",
    ),
    (
        "Solar System",
        "Astronomy",
        "Explore the Sun, planets, moons, asteroids, and comets.",
    ),
    (
        "Stars and Galaxies",
        "Astronomy",
        "Learn about stars, constellations, galaxies, and the universe.",
    ),
    (
        "Rocks and Minerals",
        "Earth Science",
        "Study the properties, formation, and uses of rocks and minerals.",
    ),
    (
        "Water Cycle",
        "Earth Science",
        "Understand evaporation, condensation, precipitation, and collection.",
    ),
    (
        "Natural Disasters and Preparedness",
        "Earth Science",
        "Learn about earthquakes, floods, cyclones, and disaster preparedness.",
    ),
]


def main():
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DATABASE_PATH}"
        )

    db = SessionLocal()

    try:
        # Identify Social Science using the existing topic convention.
        existing_lessons = db.query(Lesson).all()

        social_science_lessons = [
            lesson
            for lesson in existing_lessons
            if (lesson.topic or "").strip().lower()
            == "social science"
        ]

        # Existing Science lessons are all lessons not marked Social Science.
        science_lessons = [
            lesson
            for lesson in existing_lessons
            if (lesson.topic or "").strip().lower()
            != "social science"
        ]

        print(f"Database: {DATABASE_PATH}")
        print(f"Existing Science lessons: {len(science_lessons)}")
        print(
            f"Existing Social Science lessons: "
            f"{len(social_science_lessons)}"
        )

        if len(science_lessons) != 5:
            raise RuntimeError(
                "Expected exactly 5 existing Science lessons. "
                "No changes have been committed. Check the lesson topics."
            )

        # Refuse to create duplicate titles.
        existing_titles = {
            (lesson.title or "").strip().casefold()
            for lesson in existing_lessons
        }

        duplicates = [
            title
            for title, _, _ in NEW_SCIENCE_LESSONS
            if title.strip().casefold() in existing_titles
        ]

        if duplicates:
            raise RuntimeError(
                "Some proposed Science lesson titles already exist: "
                + ", ".join(duplicates)
                + ". No changes have been committed."
            )

        if len(NEW_SCIENCE_LESSONS) != 35:
            raise RuntimeError(
                "Expected exactly 35 new Science lessons."
            )

        # Create all lessons and quizzes inside one transaction.
        try:
            for title, topic, content in NEW_SCIENCE_LESSONS:
                lesson = Lesson(
                    title=title,
                    topic=topic,
                    difficulty="Easy",
                    content=content,
                )

                db.add(lesson)
                db.flush()

                for difficulty in ("Easy", "Medium", "Hard"):
                    quiz = Quiz(
                        lesson_id=lesson.id,
                        title=f"{title} - {difficulty}",
                        difficulty=difficulty,
                    )
                    db.add(quiz)

            db.flush()

            # Validate counts before committing.
            db.expire_all()

            final_lessons = db.query(Lesson).all()

            final_science = [
                lesson
                for lesson in final_lessons
                if (lesson.topic or "").strip().lower()
                != "social science"
            ]

            if len(final_science) != 40:
                raise RuntimeError(
                    f"Expected 40 Science lessons, found "
                    f"{len(final_science)}."
                )

            db.commit()

        except Exception:
            db.rollback()
            raise

        print("\nScience lesson expansion completed.")
        print(f"Science lessons: {len(final_science)}")
        print("New lessons added: 35")
        print("New quizzes added: 105")
        print("Existing Social Science lessons preserved.")
        print("Existing questions preserved.")
        print(
            "\nNote: question insertion is not included in this stage."
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()
