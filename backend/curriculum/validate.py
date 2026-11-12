"""Quality gate for curriculum content.

``validate_file`` returns a list of problems (empty = valid). The importer
refuses invalid files and a test runs it over every file, so a lesson with
only a title and a paragraph, a quiz missing a level, a question without a
hint, or a lopsided answer key cannot be committed unnoticed.
"""

from collections import Counter
from typing import Any

from .loader import iter_lessons

GRADES = (6, 7, 8, 9, 10)
SUBJECTS = ("Mathematics", "Science", "Social Science", "English")
LEVELS = ("EASY", "MEDIUM", "HARD")
DIAGRAM_TYPES = ("flow", "cycle", "table", "labelled", "number_line", "bar")

MIN_TOPICS = 3
MIN_LESSONS_PER_TOPIC = 2
MIN_QUESTIONS_PER_LEVEL = 4
MIN_EXPLANATION_WORDS = 250
MAX_ANSWER_SHARE = 0.40


def _words(text: str) -> int:
    return len(str(text).split())


def _check_question(q: Any, where: str, problems: list[str]) -> str | None:
    if not (isinstance(q, list) and len(q) == 5):
        problems.append(f"{where}: question must be [text, options, answer, hint, explanation]")
        return None
    text, options, answer, hint, explanation = q
    if not str(text).strip():
        problems.append(f"{where}: empty question text")
    if not (isinstance(options, list) and len(options) == 4 and all(str(o).strip() for o in options)):
        problems.append(f"{where}: needs four non-empty options")
    elif len({str(o).strip().lower() for o in options}) != 4:
        problems.append(f"{where}: duplicate options")
    if answer not in ("A", "B", "C", "D"):
        problems.append(f"{where}: answer must be A-D")
    if not str(hint).strip() or not str(explanation).strip():
        problems.append(f"{where}: hint and explanation are required")
    if isinstance(options, list) and answer in ("A", "B", "C", "D") and len(options) == 4:
        correct = str(options["ABCD".index(answer)]).lower()
        if str(hint).strip().lower() == correct:
            problems.append(f"{where}: hint gives away the answer")
    return answer


def _check_lesson(lesson: dict, where: str, problems: list[str], answers: Counter) -> None:
    legacy = bool(lesson.get("legacy_title"))
    for key in ("slug", "title", "intro", "real_world"):
        if not str(lesson.get(key, "")).strip():
            problems.append(f"{where}: missing {key}")
    if len(lesson.get("objectives", [])) < 2:
        problems.append(f"{where}: at least 2 learning objectives")
    sections = lesson.get("sections", [])
    if len(sections) < 2 or not all(isinstance(s, list) and len(s) == 2 for s in sections):
        problems.append(f"{where}: at least 2 [heading, body] sections")
    words = _words(lesson.get("intro", "")) + sum(_words(s[1]) for s in sections if isinstance(s, list) and len(s) == 2)
    if words < MIN_EXPLANATION_WORDS:
        problems.append(f"{where}: explanation too short ({words} words < {MIN_EXPLANATION_WORDS})")
    if len(lesson.get("definitions", [])) < 2:
        problems.append(f"{where}: at least 2 definitions")
    if len(lesson.get("examples", [])) < 1:
        problems.append(f"{where}: at least 1 example")
    worked = lesson.get("worked", [])
    if len(worked) < 1 or not all(w.get("problem") and w.get("steps") and w.get("answer") for w in worked):
        problems.append(f"{where}: at least 1 complete worked example")
    if len(lesson.get("takeaways", [])) < 3:
        problems.append(f"{where}: at least 3 key takeaways")
    if len(lesson.get("practice", [])) < 3:
        problems.append(f"{where}: at least 3 practice exercises")
    diagram = lesson.get("diagram")
    if diagram is not None and diagram.get("type") not in DIAGRAM_TYPES:
        problems.append(f"{where}: unknown diagram type {diagram.get('type')!r}")

    quiz = lesson.get("quiz", {})
    if legacy and not quiz:
        if not lesson.get("legacy_notes"):
            problems.append(f"{where}: legacy lesson needs legacy_notes (hints/explanations)")
        return
    for level in LEVELS:
        questions = quiz.get(level, [])
        if len(questions) < MIN_QUESTIONS_PER_LEVEL:
            problems.append(f"{where}: {level} needs at least {MIN_QUESTIONS_PER_LEVEL} questions")
        seen = set()
        for i, q in enumerate(questions):
            answer = _check_question(q, f"{where} {level}[{i}]", problems)
            if answer:
                answers[answer] += 1
            if isinstance(q, list) and q:
                if q[0] in seen:
                    problems.append(f"{where} {level}: duplicate question {q[0]!r}")
                seen.add(q[0])


def validate_file(data: dict) -> list[str]:
    problems: list[str] = []
    name = data.get("_file", "?")
    if data.get("grade") not in GRADES:
        problems.append(f"{name}: grade must be one of {GRADES}")
    if data.get("subject") not in SUBJECTS:
        problems.append(f"{name}: subject must be one of {SUBJECTS}")

    topics = [t for u in data.get("units", []) for t in u.get("topics", [])]
    if len(topics) < MIN_TOPICS:
        problems.append(f"{name}: at least {MIN_TOPICS} topics (has {len(topics)})")
    for topic in topics:
        if len(topic.get("lessons", [])) < MIN_LESSONS_PER_TOPIC:
            problems.append(f"{name}/{topic.get('slug')}: at least {MIN_LESSONS_PER_TOPIC} lessons")
        if not topic.get("slug") or not topic.get("title"):
            problems.append(f"{name}: topic missing slug/title")
    for unit in data.get("units", []):
        if not unit.get("slug") or not unit.get("title"):
            problems.append(f"{name}: unit missing slug/title")

    answers: Counter = Counter()
    for _, topic, lesson in iter_lessons(data):
        _check_lesson(lesson, f"{name}/{lesson.get('slug', '?')}", problems, answers)

    total = sum(answers.values())
    if total:
        letter, count = answers.most_common(1)[0]
        if count / total > MAX_ANSWER_SHARE:
            problems.append(f"{name}: answer key unbalanced ({letter} is {count}/{total})")
    return problems


def validate_curriculum(files: list[dict]) -> list[str]:
    problems: list[str] = []
    for data in files:
        problems.extend(validate_file(data))

    slugs: Counter = Counter()
    for data in files:
        for unit in data.get("units", []):
            slugs[unit.get("slug")] += 1
            for topic in unit.get("topics", []):
                slugs[topic.get("slug")] += 1
                for lesson in topic.get("lessons", []):
                    slugs[lesson.get("slug")] += 1
    problems.extend(f"duplicate slug {s!r}" for s, n in slugs.items() if n > 1)

    combos = {(d.get("grade"), d.get("subject")) for d in files}
    missing = [(g, s) for g in GRADES for s in SUBJECTS if (g, s) not in combos]
    problems.extend(f"missing grade {g} {s}" for g, s in missing)
    return problems
