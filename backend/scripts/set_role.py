"""Grant or revoke curriculum-management roles.

Roles are deliberately not changeable through the public API, so a student
can never promote themselves. Run from the project root:

    python backend/scripts/set_role.py teacher@example.com teacher
    python backend/scripts/set_role.py teacher@example.com student
"""

import argparse
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.database.connection import SessionLocal  # noqa: E402
from app.models.student import Student  # noqa: E402

ROLES = ("student", "teacher", "admin")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("email")
    parser.add_argument("role", choices=ROLES)
    args = parser.parse_args()

    db = SessionLocal()
    try:
        student = db.query(Student).filter(Student.email == args.email).first()
        if student is None:
            print(f"No account with e-mail {args.email!r}.", file=sys.stderr)
            return 1

        previous = student.role
        student.role = args.role
        db.commit()
        print(f"{student.email}: {previous} -> {student.role}")
        return 0
    finally:
        db.close()


if __name__ == "__main__":
    raise SystemExit(main())
