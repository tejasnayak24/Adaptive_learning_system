"""Grade-aware access to the curriculum hierarchy.

Students see only lessons of their own grade (``students.grade``). Accounts
created before Phase 5 have no grade yet; they get 409 ``grade_required``
until they choose one. Teachers and admins can view every grade.
"""

from __future__ import annotations

import json
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.curriculum import GRADES, SUBJECTS, CurriculumTopic, CurriculumUnit
from app.models.lesson import Lesson
from app.models.progress import Progress
from app.models.student import Student

MANAGER_ROLES = ("teacher", "admin")
GRADE_REQUIRED = "grade_required"


def is_manager(student: Student) -> bool:
    return (student.role or "student") in MANAGER_ROLES


def require_grade(student: Student) -> int:
    if student.grade is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=GRADE_REQUIRED)
    return student.grade


def visible_grade(student: Student, requested: int | None) -> int:
    """The grade whose curriculum ``student`` may browse."""
    if requested is not None and requested not in GRADES:
        raise HTTPException(status_code=422, detail=f"grade must be one of {list(GRADES)}")
    if is_manager(student):
        return requested if requested is not None else (student.grade or GRADES[0])
    grade = require_grade(student)
    if requested is not None and requested != grade:
        raise HTTPException(status_code=403, detail=f"Your curriculum is Grade {grade}")
    return grade


def check_lesson_access(student: Student, lesson: Lesson) -> None:
    if lesson.grade is None or is_manager(student):
        return
    grade = require_grade(student)
    if lesson.grade != grade:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"This lesson belongs to the Grade {lesson.grade} curriculum (you are in Grade {grade})",
        )


def lesson_material(lesson: Lesson) -> dict[str, Any] | None:
    if not lesson.material:
        return None
    try:
        return json.loads(lesson.material)
    except ValueError:
        return None


def subject_sequence(db: Session, grade: int, subject: str) -> list[Lesson]:
    """Lessons of one grade and subject in curriculum order."""
    return (
        db.query(Lesson)
        .filter(Lesson.grade == grade, Lesson.subject == subject)
        .order_by(Lesson.position, Lesson.id)
        .all()
    )


def _lesson_ref(lesson: Lesson | None) -> dict[str, Any] | None:
    if lesson is None:
        return None
    return {"id": lesson.id, "title": lesson.title, "topic": lesson.topic}


def navigation(db: Session, lesson: Lesson) -> dict[str, Any] | None:
    """Previous / next / skip-ahead lessons within the lesson's grade and subject.

    ``skip`` is the lesson two places ahead (or the last one), matching the
    RL action SKIP_TO_ADVANCED_TOPIC; ``next_topic`` is the first lesson of
    the following topic.
    """
    if lesson.grade is None or lesson.subject is None:
        return None
    sequence = subject_sequence(db, lesson.grade, lesson.subject)
    ids = [item.id for item in sequence]
    if lesson.id not in ids:
        return None
    index = ids.index(lesson.id)
    nxt = sequence[index + 1] if index + 1 < len(sequence) else None
    skip = sequence[min(index + 2, len(sequence) - 1)] if index + 1 < len(sequence) else None
    next_topic = next((item for item in sequence[index + 1 :] if item.topic_id != lesson.topic_id), None)
    return {
        "index": index,
        "total": len(sequence),
        "previous": _lesson_ref(sequence[index - 1] if index > 0 else None),
        "next": _lesson_ref(nxt),
        "skip": _lesson_ref(skip),
        "next_topic": _lesson_ref(next_topic),
        "sequence": [_lesson_ref(item) for item in sequence],
    }


def placement(lesson: Lesson) -> dict[str, Any]:
    topic = lesson.curriculum_topic
    unit = topic.unit if topic is not None else None
    return {
        "grade": lesson.grade,
        "subject": lesson.subject,
        "unit": {"id": unit.id, "title": unit.title} if unit else None,
        "curriculum_topic": {"id": topic.id, "title": topic.title, "description": topic.description}
        if topic
        else None,
        "position": lesson.position,
    }


def _best_scores(db: Session, student: Student) -> dict[int, dict[str, Any]]:
    best: dict[int, dict[str, Any]] = {}
    for row in db.query(Progress).filter(Progress.student_id == student.id):
        entry = best.setdefault(row.lesson_id, {"attempts": 0, "best_score": None, "completed": False})
        entry["attempts"] += 1
        if entry["best_score"] is None or row.quiz_score > entry["best_score"]:
            entry["best_score"] = row.quiz_score
        entry["completed"] = entry["completed"] or bool(row.completed)
    return best


def curriculum_tree(db: Session, student: Student, grade: int, subject: str | None = None) -> dict[str, Any]:
    if subject is not None and subject not in SUBJECTS:
        raise HTTPException(status_code=422, detail=f"subject must be one of {list(SUBJECTS)}")

    query = db.query(CurriculumUnit).filter(CurriculumUnit.grade == grade)
    if subject is not None:
        query = query.filter(CurriculumUnit.subject == subject)
    units = query.order_by(CurriculumUnit.subject, CurriculumUnit.position).all()
    progress = _best_scores(db, student)

    subjects: dict[str, dict[str, Any]] = {}
    for unit in units:
        entry = subjects.setdefault(
            unit.subject, {"subject": unit.subject, "units": [], "lesson_count": 0, "lessons_attempted": 0}
        )
        topics = []
        for topic in unit.topics:
            lessons = []
            for lesson in topic.lessons:
                stats = progress.get(lesson.id, {"attempts": 0, "best_score": None, "completed": False})
                lessons.append(
                    {
                        "id": lesson.id,
                        "title": lesson.title,
                        "position": lesson.position,
                        "quizzes": [
                            {"id": q.id, "difficulty": q.difficulty, "title": q.title}
                            for q in sorted(lesson.quizzes, key=lambda q: ("EASY", "MEDIUM", "HARD").index(q.difficulty) if q.difficulty in ("EASY", "MEDIUM", "HARD") else 9)
                        ],
                        **stats,
                    }
                )
                entry["lesson_count"] += 1
                entry["lessons_attempted"] += 1 if stats["attempts"] else 0
            topics.append(
                {"id": topic.id, "title": topic.title, "description": topic.description, "lessons": lessons}
            )
        entry["units"].append({"id": unit.id, "title": unit.title, "topics": topics})

    ordered = [subjects[s] for s in SUBJECTS if s in subjects]
    return {"grade": grade, "subjects": ordered}


def grade_overview(db: Session) -> list[dict[str, Any]]:
    """Lesson counts per grade and subject (for grade selection)."""
    rows = db.query(Lesson.grade, Lesson.subject).filter(Lesson.grade.isnot(None)).all()
    counts: dict[tuple[int, str], int] = {}
    for grade, subject in rows:
        counts[(grade, subject)] = counts.get((grade, subject), 0) + 1
    return [
        {"grade": g, "subjects": [{"subject": s, "lessons": counts.get((g, s), 0)} for s in SUBJECTS]}
        for g in GRADES
    ]


def topic_count(db: Session, grade: int, subject: str) -> int:
    return (
        db.query(CurriculumTopic)
        .join(CurriculumUnit)
        .filter(CurriculumUnit.grade == grade, CurriculumUnit.subject == subject)
        .count()
    )
