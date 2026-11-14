"""Import the Grade 6-10 curriculum into the database (safe to re-run).

Run from the project root, after ``python -m alembic upgrade head``:

    python backend/scripts/import_curriculum.py            # import
    python backend/scripts/import_curriculum.py --check    # validate only

The original Science lessons are created first if missing (seed_science),
then adopted into the hierarchy with their ids, questions and progress kept.
Re-running reports zero created rows.
"""

import argparse
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

import app.models  # noqa: E402,F401
from app.database.connection import SessionLocal  # noqa: E402
from curriculum import load_all, validate_curriculum  # noqa: E402
from curriculum.importer import CurriculumError, import_curriculum  # noqa: E402
from seed_science import seed_into  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="validate content without touching the database")
    args = parser.parse_args()

    files = load_all()
    problems = validate_curriculum(files)
    lessons = sum(len(t["lessons"]) for d in files for u in d["units"] for t in u["topics"])
    print(f"{len(files)} grade-subject files, {lessons} lessons")
    if problems:
        print("Content problems:\n  " + "\n  ".join(problems))
        return 1
    if args.check:
        print("Content is valid.")
        return 0

    db = SessionLocal()
    try:
        seeded = seed_into(db)
        stats = import_curriculum(db, files)
        db.commit()
    except CurriculumError as exc:
        db.rollback()
        print(exc)
        return 1
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

    print(f"Original Science rows created (lessons, quizzes, questions): {seeded}")
    print(f"Created: {stats.created}")
    print(f"Updated: {stats.updated}")
    print(f"Legacy lessons adopted this run: {stats.adopted_legacy_lessons}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
