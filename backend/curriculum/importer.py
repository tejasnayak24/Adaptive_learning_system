"""Idempotent import of curriculum content into the database.

Rows are matched by stable keys, so running the import any number of times
gives the same database:

* units / topics / lessons by ``slug``;
* a lesson with ``legacy_title`` adopts the existing lesson of that title
  (the original Science lessons). Its id, title, content, quizzes,
  questions, answers and progress are kept; it only gains its place in the
  hierarchy, structured material, and hints/explanations for its questions;
* quizzes by (lesson, difficulty);
* questions by (quiz, question text).

Nothing is ever deleted.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from sqlalchemy.orm import Session

from app.models.curriculum import CurriculumTopic, CurriculumUnit
from app.models.lesson import Lesson
from app.models.question import Question
from app.models.quiz import Quiz

from .validate import LEVELS, validate_curriculum

MATERIAL_KEYS = (
    "objectives",
    "intro",
    "sections",
    "definitions",
    "examples",
    "worked",
    "diagram",
    "real_world",
    "takeaways",
    "practice",
)


@dataclass
class ImportStats:
    created: dict[str, int] = field(default_factory=lambda: {k: 0 for k in ("units", "topics", "lessons", "quizzes", "questions")})
    updated: dict[str, int] = field(default_factory=lambda: {k: 0 for k in ("units", "topics", "lessons", "quizzes", "questions")})
    adopted_legacy_lessons: int = 0

    @property
    def total_created(self) -> int:
        return sum(self.created.values())


class CurriculumError(ValueError):
    pass


def _set(row: Any, values: dict[str, Any]) -> bool:
    changed = False
    for key, value in values.items():
        if getattr(row, key) != value:
            setattr(row, key, value)
            changed = True
    return changed


def _material(lesson: dict[str, Any]) -> str:
    return json.dumps({k: lesson.get(k) for k in MATERIAL_KEYS}, ensure_ascii=False, sort_keys=True)


def _plain_content(lesson: dict[str, Any]) -> str:
    parts = [lesson["intro"]] + [f"{heading}\n{body}" for heading, body in lesson["sections"]]
    return "\n\n".join(parts)


def _level_label(level: str) -> str:
    return level.capitalize()


def import_curriculum(db: Session, files: list[dict[str, Any]], *, require_complete: bool = True) -> ImportStats:
    """Import ``files`` (from ``curriculum.load_all``) into ``db``; no commit.

    With ``require_complete`` all 20 grade-subject pairs must be present.
    """
    problems = validate_curriculum(files)
    if not require_complete:
        problems = [p for p in problems if not p.startswith("missing grade")]
    if problems:
        raise CurriculumError("Curriculum content is invalid:\n  " + "\n  ".join(problems[:50]))

    stats = ImportStats()
    for data in files:
        grade, subject = data["grade"], data["subject"]
        lesson_position = 0
        for u_pos, unit_data in enumerate(data["units"]):
            unit = db.query(CurriculumUnit).filter_by(slug=unit_data["slug"]).one_or_none()
            values = {"grade": grade, "subject": subject, "title": unit_data["title"], "position": u_pos}
            if unit is None:
                unit = CurriculumUnit(slug=unit_data["slug"], **values)
                db.add(unit)
                db.flush()
                stats.created["units"] += 1
            elif _set(unit, values):
                stats.updated["units"] += 1

            for t_pos, topic_data in enumerate(unit_data["topics"]):
                topic = db.query(CurriculumTopic).filter_by(slug=topic_data["slug"]).one_or_none()
                values = {
                    "unit_id": unit.id,
                    "title": topic_data["title"],
                    "description": topic_data.get("description"),
                    "position": t_pos,
                }
                if topic is None:
                    topic = CurriculumTopic(slug=topic_data["slug"], **values)
                    db.add(topic)
                    db.flush()
                    stats.created["topics"] += 1
                elif _set(topic, values):
                    stats.updated["topics"] += 1

                for lesson_data in topic_data["lessons"]:
                    lesson_position += 1
                    _import_lesson(db, stats, lesson_data, grade, subject, topic, lesson_position)
    db.flush()
    return stats


def _import_lesson(db, stats, data, grade, subject, topic, position) -> None:
    lesson = db.query(Lesson).filter_by(slug=data["slug"]).one_or_none()
    legacy_title = data.get("legacy_title")

    if lesson is None and legacy_title:
        lesson = db.query(Lesson).filter(Lesson.title == legacy_title, Lesson.slug.is_(None)).first()
        if lesson is None:
            raise CurriculumError(
                f"Legacy lesson {legacy_title!r} not found; run backend/seed_science.py first."
            )
        stats.adopted_legacy_lessons += 1

    placement = {
        "slug": data["slug"],
        "grade": grade,
        "subject": subject,
        "topic_id": topic.id,
        "position": position,
        "material": _material(data),
    }

    if lesson is None:
        lesson = Lesson(
            title=data["title"],
            topic=topic.title,
            difficulty="MIXED",
            content=_plain_content(data),
            **placement,
        )
        db.add(lesson)
        db.flush()
        stats.created["lessons"] += 1
    else:
        values = dict(placement)
        if not legacy_title:
            # Legacy lessons keep their original title, topic and text.
            values.update(title=data["title"], topic=topic.title, content=_plain_content(data))
        if _set(lesson, values):
            stats.updated["lessons"] += 1

    if legacy_title:
        _apply_legacy_notes(db, stats, lesson, data.get("legacy_notes") or {})

    for level in LEVELS:
        questions = data.get("quiz", {}).get(level)
        if not questions:
            continue
        quiz = db.query(Quiz).filter_by(lesson_id=lesson.id, difficulty=level).one_or_none()
        title = f"{lesson.title} - {_level_label(level)} Quiz"
        if quiz is None:
            quiz = Quiz(lesson_id=lesson.id, title=title, difficulty=level)
            db.add(quiz)
            db.flush()
            stats.created["quizzes"] += 1
        elif _set(quiz, {"title": title}):
            stats.updated["quizzes"] += 1

        for text, options, answer, hint, explanation in questions:
            values = {
                "option_a": options[0],
                "option_b": options[1],
                "option_c": options[2],
                "option_d": options[3],
                "correct_answer": answer,
                "hint": hint,
                "explanation": explanation,
            }
            row = db.query(Question).filter_by(quiz_id=quiz.id, question=text).one_or_none()
            if row is None:
                db.add(Question(quiz_id=quiz.id, question=text, **values))
                stats.created["questions"] += 1
            elif _set(row, values):
                stats.updated["questions"] += 1


def _apply_legacy_notes(db, stats, lesson: Lesson, notes: dict[str, list[str]]) -> None:
    """Add hints/explanations to the original questions; never change answers."""
    for quiz in lesson.quizzes:
        for question in db.query(Question).filter_by(quiz_id=quiz.id):
            note = notes.get(question.question)
            if note and _set(question, {"hint": note[0], "explanation": note[1]}):
                stats.updated["questions"] += 1
