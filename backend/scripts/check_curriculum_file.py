"""Validate one or more curriculum files and print a short summary.

    python backend/scripts/check_curriculum_file.py backend/curriculum/content/g06_mathematics.json
"""

import sys
from collections import Counter
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from curriculum.loader import iter_lessons, load_file  # noqa: E402
from curriculum.validate import validate_file  # noqa: E402

status = 0
for name in sys.argv[1:]:
    data = load_file(Path(name))
    problems = validate_file(data)
    lessons = list(iter_lessons(data))
    answers = Counter(q[2] for _, _, l in lessons for qs in l.get("quiz", {}).values() for q in qs)
    words = [len(l["intro"].split()) + sum(len(s[1].split()) for s in l["sections"]) for _, _, l in lessons]
    print(f"{data['_file']}: {len(lessons)} lessons, {sum(answers.values())} questions, answers {dict(sorted(answers.items()))}, words {min(words)}-{max(words)}")
    for p in problems:
        print("  PROBLEM:", p)
    status |= bool(problems)
sys.exit(status)
