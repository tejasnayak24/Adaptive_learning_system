"""The shipped Grade 6-10 curriculum is complete, valid and imports idempotently."""

import json
from collections import Counter

import pytest

from curriculum import load_all, validate_curriculum
from curriculum.importer import import_curriculum
from curriculum.validate import GRADES, SUBJECTS

FILES = load_all()


def test_all_twenty_grade_subject_pairs_are_present_and_valid():
    assert {(f["grade"], f["subject"]) for f in FILES} == {(g, s) for g in GRADES for s in SUBJECTS}
    assert validate_curriculum(FILES) == []


@pytest.mark.parametrize("data", FILES, ids=lambda d: d["_file"])
def test_each_pair_meets_minimum_coverage(data):
    topics = [t for u in data["units"] for t in u["topics"]]
    assert len(topics) >= 3
    for topic in topics:
        assert len(topic["lessons"]) >= 2
        for lesson in topic["lessons"]:
            if lesson.get("legacy_title"):
                continue
            for level in ("EASY", "MEDIUM", "HARD"):
                assert len(lesson["quiz"][level]) >= 4


def test_answer_keys_are_balanced_overall():
    answers = Counter(
        q[2]
        for f in FILES
        for u in f["units"]
        for t in u["topics"]
        for l in t["lessons"]
        for qs in l.get("quiz", {}).values()
        for q in qs
    )
    total = sum(answers.values())
    assert total >= 1400
    assert max(answers.values()) / total < 0.3


def test_full_import_preserves_science_and_is_idempotent(db_session):
    from app.models.curriculum import CurriculumTopic, CurriculumUnit
    from app.models.lesson import Lesson
    from app.models.question import Question
    from app.models.quiz import Quiz
    from seed_science import seed_into

    seed_into(db_session)
    db_session.commit()
    original = {l.title: l.id for l in db_session.query(Lesson)}
    original_questions = {q.id: (q.question, q.correct_answer) for q in db_session.query(Question)}
    assert len(original) == 5 and len(original_questions) == 75

    first = import_curriculum(db_session, FILES)
    db_session.commit()
    assert first.adopted_legacy_lessons == 5
    assert first.created["lessons"] == 117

    # Original Science lessons keep their ids and are placed in Grades 9 and 10.
    for title, lesson_id in original.items():
        lesson = db_session.get(Lesson, lesson_id)
        assert lesson.title == title and lesson.subject == "Science" and lesson.grade in (9, 10)
        assert json.loads(lesson.material)["objectives"]
    for qid, (text, answer) in original_questions.items():
        q = db_session.get(Question, qid)
        assert (q.question, q.correct_answer) == (text, answer)
        assert q.hint and q.explanation

    counts = (
        db_session.query(CurriculumUnit).count(),
        db_session.query(CurriculumTopic).count(),
        db_session.query(Lesson).count(),
        db_session.query(Quiz).count(),
        db_session.query(Question).count(),
    )
    assert counts[2] == 122
    assert counts[4] == 75 + 1404

    second = import_curriculum(db_session, FILES)
    db_session.commit()
    assert second.total_created == 0 and sum(second.updated.values()) == 0
    assert (
        db_session.query(CurriculumUnit).count(),
        db_session.query(CurriculumTopic).count(),
        db_session.query(Lesson).count(),
        db_session.query(Quiz).count(),
        db_session.query(Question).count(),
    ) == counts

    # Every grade-subject pair is reachable through the hierarchy.
    for grade in GRADES:
        for subject in SUBJECTS:
            n = (
                db_session.query(CurriculumTopic)
                .join(CurriculumUnit)
                .filter(CurriculumUnit.grade == grade, CurriculumUnit.subject == subject)
                .count()
            )
            assert n >= 3, (grade, subject)
