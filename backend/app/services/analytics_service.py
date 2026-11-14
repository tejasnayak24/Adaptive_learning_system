"""Student learning analytics (Phase 6).

Every figure is computed from the signed-in student's own stored records:

* ``progress`` -- one row per graded quiz attempt (score, difficulty, mode,
  time, and the camera measurements taken *during that attempt*);
* the curriculum tables (grade -> subject -> unit -> topic -> lesson);
* ``recommendation_history`` / ``reward_history`` -- the Q-learning
  recommendations and their recorded outcomes.

Definitions (documented in TEAM_GUIDE.md):

* A lesson is **completed** when at least one of its quizzes was passed
  (score >= ``PASS_SCORE``, the same pass mark the RL safety rules use
  before allowing the student to move on). ``progress.completed`` is not
  used: it is set on every submitted attempt, so it means "quiz finished",
  not "lesson learned".
* Attention is only averaged over attempts with a real camera measurement.
  ``attention_score IS NULL`` means no valid measurement (camera missing,
  face not found or readings stale) and is never treated as low attention.
* Camera analytics are per quiz attempt: the server stores the average of
  the heartbeats received during the attempt, not a continuous recording.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime, timedelta
from typing import Any, Iterable

from sqlalchemy import case, func
from sqlalchemy.orm import Session, joinedload

from app.models.curriculum import SUBJECTS, CurriculumTopic, CurriculumUnit
from app.models.lesson import Lesson
from app.models.progress import Progress
from app.models.recommendation import RecommendationHistory
from app.models.reward import RewardHistory
from app.models.student import Student
from app.services.recommendation_service import recommendation_to_dict
from rl_engine.core.constraints import MASTERY_SCORE, PASS_SCORE

# A topic needs at least this many quiz attempts before it is called
# strong, weak or in need of revision.
MIN_ATTEMPTS_TO_EVALUATE = 2
# Topic status uses the student's most recent attempts on that topic.
RECENT_ATTEMPTS_FOR_STATUS = 3
# Fewer camera-measured attempts than this is reported as insufficient
# monitoring history (averages are still shown, but flagged).
MIN_MEASURED_ATTEMPTS = 3
TREND_LIMIT = 500
ACTIVITY_LIMIT = 30
LESSON_MILESTONES = (1, 5, 10, 25, 50, 100)


def _pct(value: float | None) -> float | None:
    return None if value is None else round(float(value), 1)


def _avg(total: float, count: int) -> float | None:
    return round(total / count, 1) if count else None


def _iso(value: datetime | None) -> str | None:
    return value.isoformat() if value is not None else None


def telemetry_status(progress: Progress) -> str:
    """``measured`` | ``unavailable`` (monitored, but no valid camera
    reading during the attempt) | ``not_monitored`` (recorded before
    camera monitoring existed)."""
    if progress.attention_score is not None:
        return "measured"
    if progress.monitoring_session_id is not None:
        return "unavailable"
    return "not_monitored"


def topic_status(scores_oldest_first: list[float]) -> str:
    """Classify a topic from its quiz scores (oldest first).

    ``not_started`` with no attempts and ``insufficient_data`` with fewer
    than ``MIN_ATTEMPTS_TO_EVALUATE`` -- a topic is never called weak just
    because it has not been attempted.
    """
    if not scores_oldest_first:
        return "not_started"
    if len(scores_oldest_first) < MIN_ATTEMPTS_TO_EVALUATE:
        return "insufficient_data"
    recent = scores_oldest_first[-RECENT_ATTEMPTS_FOR_STATUS:]
    recent_avg = sum(recent) / len(recent)
    latest = scores_oldest_first[-1]
    if recent_avg >= MASTERY_SCORE and latest >= PASS_SCORE:
        return "strong"
    if recent_avg < PASS_SCORE:
        return "weak"
    return "needs_revision"


def _ordered(attempts: Iterable[Progress]) -> list[Progress]:
    # Attempts without a timestamp predate timestamps; ids are monotonic.
    return sorted(attempts, key=lambda p: p.id)


def _streaks(days: set[date], today: date) -> dict[str, Any]:
    if not days:
        return {"days_active": 0, "current_streak_days": 0, "longest_streak_days": 0, "timezone": "UTC"}
    ordered = sorted(days)
    longest = run = 1
    for prev, cur in zip(ordered, ordered[1:]):
        run = run + 1 if cur - prev == timedelta(days=1) else 1
        longest = max(longest, run)
    current = 0
    day = today if today in days else today - timedelta(days=1)
    while day in days:
        current += 1
        day -= timedelta(days=1)
    return {
        "days_active": len(days),
        "current_streak_days": current,
        "longest_streak_days": longest,
        "timezone": "UTC",
    }


def _lesson_ref(lesson: Lesson | None) -> dict[str, Any]:
    if lesson is None:
        return {"lesson_id": None, "lesson_title": None, "subject": None, "grade": None, "topic": None}
    topic = lesson.curriculum_topic
    return {
        "lesson_id": lesson.id,
        "lesson_title": lesson.title,
        "subject": lesson.subject or "Science",
        "grade": lesson.grade,
        "topic": topic.title if topic is not None else lesson.topic,
        "topic_id": topic.id if topic is not None else None,
    }


def _attempt_point(p: Progress) -> dict[str, Any]:
    return {
        "progress_id": p.id,
        "at": _iso(p.created_at),
        **_lesson_ref(p.lesson),
        "quiz_id": p.quiz_id,
        "difficulty": p.difficulty,
        "mode": p.attempt_mode or "standard",
        "score": _pct(p.quiz_score),
        "passed": p.quiz_score >= PASS_SCORE,
        "correct_count": p.correct_count,
        "total_questions": p.total_questions,
        "response_time": p.response_time,
        "hints_used": p.hints_used,
        "attention": _pct(p.attention_score * 100) if p.attention_score is not None else None,
        "yawning": p.yawning,
        "looking_away": p.looking_away,
        "drowsy": p.drowsy,
        "telemetry": telemetry_status(p),
    }


def _attention_block(db: Session, student_id: int, attempts: list[Progress]) -> dict[str, Any]:
    # Database aggregation: AVG and COUNT(column) ignore NULLs, so attempts
    # without a camera measurement never pull the average down.
    def observed(column):
        return func.sum(case((column.is_(True), 1), else_=0))

    row = (
        db.query(
            func.count(Progress.id),
            func.count(Progress.attention_score),
            func.avg(Progress.attention_score),
            func.min(Progress.attention_score),
            func.max(Progress.attention_score),
            func.count(Progress.yawning),
            observed(Progress.yawning),
            func.count(Progress.looking_away),
            observed(Progress.looking_away),
            func.count(Progress.drowsy),
            observed(Progress.drowsy),
        )
        .filter(Progress.student_id == student_id)
        .one()
    )
    (total, measured, avg, low, high, yawn_n, yawn_k, away_n, away_k, drowsy_n, drowsy_k) = row

    unavailable = sum(1 for p in attempts if telemetry_status(p) == "unavailable")
    not_monitored = sum(1 for p in attempts if telemetry_status(p) == "not_monitored")

    by_subject: dict[str, list[float]] = defaultdict(list)
    for p in attempts:
        if p.attention_score is not None and p.lesson is not None:
            by_subject[p.lesson.subject or "Science"].append(p.attention_score)

    def observation(measured_n: int, observed_k: int | None) -> dict[str, Any]:
        return {"observed_in": int(observed_k or 0), "measured_attempts": int(measured_n or 0)}

    return {
        "granularity": "per_quiz_attempt",
        "attempts_total": int(total or 0),
        "measured_attempts": int(measured or 0),
        "unavailable_attempts": unavailable,
        "not_monitored_attempts": not_monitored,
        "average_attention": _pct(avg * 100) if avg is not None else None,
        "lowest_attention": _pct(low * 100) if low is not None else None,
        "highest_attention": _pct(high * 100) if high is not None else None,
        "sufficient_history": int(measured or 0) >= MIN_MEASURED_ATTEMPTS,
        "min_measured_attempts": MIN_MEASURED_ATTEMPTS,
        "yawning": observation(yawn_n, yawn_k),
        "looking_away": observation(away_n, away_k),
        "drowsiness": observation(drowsy_n, drowsy_k),
        "by_subject": [
            {"subject": s, "average_attention": _pct(sum(v) / len(v) * 100), "measured_attempts": len(v)}
            for s, v in sorted(by_subject.items())
        ],
    }


def student_summary(db: Session, student: Student, now: datetime | None = None) -> dict[str, Any]:
    """Everything the dashboard and progress pages show, in one response."""
    now = now or datetime.utcnow()

    attempts = _ordered(
        db.query(Progress)
        .options(joinedload(Progress.lesson).joinedload(Lesson.curriculum_topic))
        .filter(Progress.student_id == student.id)
        .all()
    )

    # Per-lesson aggregates in the database.
    lesson_rows = (
        db.query(
            Progress.lesson_id,
            func.count(Progress.id),
            func.sum(Progress.quiz_score),
            func.max(Progress.quiz_score),
        )
        .filter(Progress.student_id == student.id)
        .group_by(Progress.lesson_id)
        .all()
    )
    per_lesson = {
        lid: {"attempts": int(n), "score_sum": float(s or 0), "best": float(b) if b is not None else None}
        for lid, n, s, b in lesson_rows
    }
    passed_lessons = {lid for lid, v in per_lesson.items() if v["best"] is not None and v["best"] >= PASS_SCORE}

    total_attempts = len(attempts)
    average_score = _avg(sum(p.quiz_score for p in attempts), total_attempts)

    grade = student.grade
    grade_lessons: list[Lesson] = []
    if grade is not None:
        grade_lessons = (
            db.query(Lesson)
            .options(joinedload(Lesson.curriculum_topic).joinedload(CurriculumTopic.unit))
            .filter(Lesson.grade == grade)
            .order_by(Lesson.subject, Lesson.position, Lesson.id)
            .all()
        )
    grade_lesson_ids = {l.id for l in grade_lessons}

    # ---- subjects -------------------------------------------------------
    attempts_by_lesson: dict[int, list[Progress]] = defaultdict(list)
    for p in attempts:
        attempts_by_lesson[p.lesson_id].append(p)

    subjects = []
    for subject in SUBJECTS:
        lessons = [l for l in grade_lessons if l.subject == subject]
        if not lessons:
            continue
        ids = [l.id for l in lessons]
        n = sum(per_lesson.get(i, {}).get("attempts", 0) for i in ids)
        s = sum(per_lesson.get(i, {}).get("score_sum", 0.0) for i in ids)
        done = sum(1 for i in ids if i in passed_lessons)
        attempted = sum(1 for i in ids if i in per_lesson)
        subject_attempts = [p for i in ids for p in attempts_by_lesson.get(i, [])]
        last = max((p.created_at for p in subject_attempts if p.created_at), default=None)
        subjects.append(
            {
                "subject": subject,
                "lessons_total": len(lessons),
                "lessons_completed": done,
                "lessons_attempted": attempted,
                "quiz_attempts": n,
                "average_score": _avg(s, n),
                "progress_percent": round(done / len(lessons) * 100, 1),
                "completed": done == len(lessons),
                "last_activity_at": _iso(last),
            }
        )

    # ---- topics ---------------------------------------------------------
    topics = []
    topic_order: dict[int, list[Lesson]] = defaultdict(list)
    topic_obj: dict[int, CurriculumTopic] = {}
    for l in grade_lessons:
        if l.curriculum_topic is not None:
            topic_order[l.curriculum_topic.id].append(l)
            topic_obj[l.curriculum_topic.id] = l.curriculum_topic
    for topic_id, lessons in topic_order.items():
        topic = topic_obj[topic_id]
        topic_attempts = _ordered(p for l in lessons for p in attempts_by_lesson.get(l.id, []))
        scores = [p.quiz_score for p in topic_attempts]
        recent = scores[-RECENT_ATTEMPTS_FOR_STATUS:]
        weakest = None
        attempted_lessons = [l for l in lessons if l.id in per_lesson]
        if attempted_lessons:
            weakest_lesson = min(attempted_lessons, key=lambda l: per_lesson[l.id]["best"] or 0)
            weakest = {"lesson_id": weakest_lesson.id, "lesson_title": weakest_lesson.title}
        first_unpassed = next((l for l in lessons if l.id not in passed_lessons), None)
        topics.append(
            {
                "topic_id": topic_id,
                "topic": topic.title,
                "unit": topic.unit.title if topic.unit else None,
                "subject": topic.unit.subject if topic.unit else None,
                "lessons_total": len(lessons),
                "lessons_completed": sum(1 for l in lessons if l.id in passed_lessons),
                "quiz_attempts": len(scores),
                "average_score": _avg(sum(scores), len(scores)),
                "recent_average": _avg(sum(recent), len(recent)),
                "latest_score": _pct(scores[-1]) if scores else None,
                "best_score": _pct(max(scores)) if scores else None,
                "status": topic_status(scores),
                "revise_lesson": weakest,
                "next_lesson": {"lesson_id": first_unpassed.id, "lesson_title": first_unpassed.title}
                if first_unpassed
                else None,
                "first_lesson_id": lessons[0].id,
            }
        )
    status_rank = {"weak": 0, "needs_revision": 1, "strong": 2, "insufficient_data": 3, "not_started": 4}
    topics.sort(key=lambda t: (SUBJECTS.index(t["subject"]) if t["subject"] in SUBJECTS else 9, t["topic_id"]))

    # ---- activity and milestones ---------------------------------------
    events: list[dict[str, Any]] = []
    milestones: list[dict[str, Any]] = []
    first_pass: dict[int, Progress] = {}
    for p in attempts:
        events.append({"type": "quiz_attempt", **_attempt_point(p)})
        if p.quiz_score >= PASS_SCORE and p.lesson_id not in first_pass:
            first_pass[p.lesson_id] = p
            events.append({"type": "lesson_completed", "progress_id": p.id, "at": _iso(p.created_at), **_lesson_ref(p.lesson)})
            count = len(first_pass)
            if count in LESSON_MILESTONES:
                milestones.append(
                    {
                        "key": f"lessons_completed_{count}",
                        "title": "First lesson completed" if count == 1 else f"{count} lessons completed",
                        "at": _iso(p.created_at),
                    }
                )
    if attempts:
        milestones.insert(0, {"key": "first_quiz", "title": "First quiz submitted", "at": _iso(attempts[0].created_at)})
    first_mastery = next((p for p in attempts if p.quiz_score >= MASTERY_SCORE), None)
    if first_mastery:
        milestones.append({"key": "first_mastery", "title": f"First score of {MASTERY_SCORE}% or more", "at": _iso(first_mastery.created_at)})
    first_perfect = next((p for p in attempts if p.quiz_score >= 100), None)
    if first_perfect:
        milestones.append({"key": "first_perfect", "title": "First perfect score", "at": _iso(first_perfect.created_at)})
    for subject in subjects:
        if subject["completed"]:
            ids = [l.id for l in grade_lessons if l.subject == subject["subject"]]
            finishing = max((first_pass[i] for i in ids), key=lambda p: p.id)
            at = _iso(finishing.created_at)
            milestones.append({"key": f"subject_completed_{subject['subject']}", "title": f"Grade {grade} {subject['subject']} completed", "at": at})
            events.append({"type": "subject_completed", "progress_id": finishing.id, "at": at, "subject": subject["subject"], "grade": grade})
    events.sort(key=lambda e: (e["progress_id"], {"quiz_attempt": 0, "lesson_completed": 1, "subject_completed": 2}[e["type"]]), reverse=True)

    days = {p.created_at.date() for p in attempts if p.created_at is not None}
    latest = attempts[-1] if attempts else None
    completed_in_grade = len(passed_lessons & grade_lesson_ids)

    return {
        "student": {"id": student.id, "name": student.name, "grade": grade},
        "grade_required": grade is None,
        "definitions": {
            "pass_score": PASS_SCORE,
            "mastery_score": MASTERY_SCORE,
            "min_attempts_to_evaluate_topic": MIN_ATTEMPTS_TO_EVALUATE,
            "recent_attempts_for_topic_status": RECENT_ATTEMPTS_FOR_STATUS,
        },
        "overview": {
            "subjects_available": len(subjects),
            "lessons_total": len(grade_lessons),
            "lessons_completed": completed_in_grade,
            "lessons_attempted": len(set(per_lesson) & grade_lesson_ids),
            "completion_percent": round(completed_in_grade / len(grade_lessons) * 100, 1) if grade_lessons else 0.0,
            "quiz_attempts": total_attempts,
            "average_score": average_score,
            "best_score": _pct(max((p.quiz_score for p in attempts), default=None)),
            "attempts_outside_grade": sum(1 for p in attempts if p.lesson_id not in grade_lesson_ids),
            "latest_activity": _attempt_point(latest) if latest else None,
            **_streaks(days, now.date()),
        },
        "subjects": subjects,
        "topics": topics,
        "topic_status_counts": {k: sum(1 for t in topics if t["status"] == k) for k in status_rank},
        "trend": [_attempt_point(p) for p in attempts[-TREND_LIMIT:]],
        "attention": _attention_block(db, student.id, attempts),
        "activity": events[:ACTIVITY_LIMIT],
        "milestones": milestones,
        "generated_at": _iso(now),
    }


def coach_history(db: Session, student: Student, limit: int = 20) -> list[dict[str, Any]]:
    """Recommendations, newest first, with the attempt that produced each
    one and -- once the student's next attempt arrived -- its outcome."""
    rows = (
        db.query(RecommendationHistory)
        .filter(RecommendationHistory.student_id == student.id)
        .order_by(RecommendationHistory.id.desc())
        .limit(limit)
        .all()
    )
    if not rows:
        return []

    progress_ids = {r.progress_id for r in rows if r.progress_id} | {
        r.outcome_progress_id for r in rows if r.outcome_progress_id
    }
    attempts = {
        p.id: p
        for p in db.query(Progress)
        .options(joinedload(Progress.lesson).joinedload(Lesson.curriculum_topic))
        .filter(Progress.id.in_(progress_ids), Progress.student_id == student.id)
        .all()
    }
    rewards = {
        r.recommendation_id: r
        for r in db.query(RewardHistory).filter(
            RewardHistory.student_id == student.id,
            RewardHistory.recommendation_id.in_([r.id for r in rows]),
        )
    }

    items = []
    for row in rows:
        source = attempts.get(row.progress_id)
        outcome_attempt = attempts.get(row.outcome_progress_id)
        reward = rewards.get(row.id)
        outcome = None
        if outcome_attempt is not None:
            outcome = {
                "status": "recorded",
                "progress_id": outcome_attempt.id,
                **_lesson_ref(outcome_attempt.lesson),
                "difficulty": outcome_attempt.difficulty,
                "score": _pct(outcome_attempt.quiz_score),
                "score_change": _pct(outcome_attempt.quiz_score - source.quiz_score) if source else None,
                "same_lesson": source is not None and source.lesson_id == outcome_attempt.lesson_id,
                "followed": reward.followed if reward else None,
                "reward": round(reward.reward, 3) if reward else None,
                "at": _iso(outcome_attempt.created_at),
            }
        items.append(
            {
                **recommendation_to_dict(row),
                "context": {
                    **_lesson_ref(source.lesson if source else None),
                    "score": _pct(source.quiz_score) if source else None,
                    "difficulty": source.difficulty if source else None,
                    "attention": _pct(source.attention_score * 100)
                    if source is not None and source.attention_score is not None
                    else None,
                    "at": _iso(source.created_at) if source else None,
                },
                "outcome": outcome or {"status": "pending"},
            }
        )
    return items
