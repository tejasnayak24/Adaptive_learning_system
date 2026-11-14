"""Aegis curriculum content (Grades 6-10).

Content lives in ``content/g<grade>_<subject>.json`` -- one file per
grade-subject pair -- and is loaded into the database by
``backend/scripts/import_curriculum.py``. Nothing here touches the database.

File format::

    {
      "grade": 6, "subject": "Mathematics",
      "units": [{
        "slug": "...", "title": "...",
        "topics": [{
          "slug": "...", "title": "...", "description": "...",
          "lessons": [LESSON, ...]
        }]
      }]
    }

LESSON::

    {
      "slug", "title",
      "legacy_title":  (optional) adopt an existing lesson with this title,
                       keeping its id, quizzes, questions and progress,
      "objectives":    ["..."],
      "intro":         "...",
      "sections":      [["heading", "body"], ...],
      "definitions":   [["term", "meaning"], ...],
      "examples":      ["..."],
      "worked":        [{"problem": "...", "steps": ["..."], "answer": "..."}],
      "diagram":       {"type": "flow"|"cycle"|"table"|"labelled"|"number_line"|"bar", ...} or null,
      "real_world":    "...",
      "takeaways":     ["..."],
      "practice":      [["question", "answer"], ...],
      "quiz": {"EASY": [Q, ...], "MEDIUM": [...], "HARD": [...]},
      "legacy_notes":  (legacy lessons) {"<existing question text>": ["hint", "explanation"]}
    }

Q = ["question", ["option A", "option B", "option C", "option D"], "B", "hint", "explanation"]
"""

from .loader import CONTENT_DIR, load_all, load_file  # noqa: F401
from .validate import validate_curriculum, validate_file  # noqa: F401
