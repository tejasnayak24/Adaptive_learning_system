"""Builds the learning state from stored data and records recommendations.

The RL state for a recommendation is assembled on the server from the
database (the graded attempt and the student's history), not from values
supplied by the browser. Each recommendation is stored in
``recommendation_history`` so it can be audited and, once the student's
next attempt arrives, paired with its outcome in ``reward_history``.
"""

import json
from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from app.models.lesson import Lesson
from app.models.progress import Progress
from app.models.recommendation import RecommendationHistory
from app.models.reward import RewardHistory
from app.services.rl_service import RLService

# Until the multi-subject curriculum stores a subject per lesson, every
# seeded lesson belongs to the Science curriculum.
DEFAULT_SUBJECT = "Science"


def lesson_subject(lesson: Lesson) -> str:
    return getattr(lesson, "subject", None) or DEFAULT_SUBJECT


def has_camera_telemetry(progress: Progress) -> bool:
    return (
        progress.attention_score is not None
        and progress.yawning is not None
        and progress.looking_away is not None
    )


def build_state(db: Session, progress: Progress) -> dict[str, Any] | None:
    """Return the RL state for a stored attempt, or None without telemetry."""
    if not has_camera_telemetry(progress):
        return None

    lesson = progress.lesson

    history = (
        db.query(Progress)
        .filter(Progress.student_id == progress.student_id)
        .order_by(Progress.id)
        .all()
    )

    same_lesson = [p for p in history if p.lesson_id == progress.lesson_id]
    earlier_same_lesson = [p for p in same_lesson if p.id < progress.id]
    previous_score = (
        earlier_same_lesson[-1].quiz_score if earlier_same_lesson else progress.quiz_score
    )

    completed_lessons = len({p.lesson_id for p in history if p.completed})

    return {
        "subject": lesson_subject(lesson),
        "topic": lesson.topic,
        "lesson": lesson.title,
        "previous_quiz_score": int(round(previous_score)),
        "current_quiz_score": int(round(progress.quiz_score)),
        "attention_score": float(progress.attention_score),
        "yawning": bool(progress.yawning),
        "looking_away": bool(progress.looking_away),
        "difficulty": progress.difficulty,
        "response_time": float(progress.response_time),
        "hints_used": int(progress.hints_used or 0),
        "lesson_attempts": len([p for p in same_lesson if p.id <= progress.id]),
        "completed_lessons": completed_lessons,
    }


def outcome_reward(previous: Progress, outcome: Progress) -> float:
    """Reward observed after a recommendation, from the next real attempt.

    * score change between the attempts, scaled to [-5, +5];
    * +3 when the new attempt reaches mastery (>= 80%), -3 when it is
      poor (< 50%);
    * when both attempts have camera telemetry, +2 x the change in
      attention (so a recovery from distraction is rewarded).

    The formula is intentionally simple and transparent; it only uses
    values that were actually measured.
    """
    delta = (outcome.quiz_score - previous.quiz_score) / 10.0
    reward = max(-5.0, min(5.0, delta))

    if outcome.quiz_score >= 80:
        reward += 3.0
    elif outcome.quiz_score < 50:
        reward -= 3.0

    if previous.attention_score is not None and outcome.attention_score is not None:
        reward += 2.0 * (outcome.attention_score - previous.attention_score)

    return round(reward, 4)


def record_outcome_of_previous(db: Session, new_progress: Progress) -> RewardHistory | None:
    """Close the student's most recent open recommendation with this attempt."""
    pending = (
        db.query(RecommendationHistory)
        .filter(
            RecommendationHistory.student_id == new_progress.student_id,
            RecommendationHistory.outcome_progress_id.is_(None),
            RecommendationHistory.progress_id.isnot(None),
            RecommendationHistory.progress_id < new_progress.id,
        )
        .order_by(RecommendationHistory.id.desc())
        .first()
    )

    if pending is None:
        return None

    previous = db.get(Progress, pending.progress_id)
    if previous is None:
        return None

    reward_row = RewardHistory(
        student_id=new_progress.student_id,
        reward=outcome_reward(previous, new_progress),
        state=pending.state_key,
        action=pending.action,
        recommendation_id=pending.id,
        progress_id=new_progress.id,
    )

    pending.outcome_progress_id = new_progress.id
    pending.outcome_recorded_at = datetime.utcnow()
    db.add(reward_row)
    return reward_row


def recommend_for_attempt(
    db: Session,
    rl_service: RLService,
    progress: Progress,
) -> RecommendationHistory | None:
    """Generate, store and return the recommendation for a graded attempt.

    Returns None when the attempt has no camera telemetry: no
    recommendation is produced from guessed engagement values.
    """
    state = build_state(db, progress)
    if state is None:
        return None

    decision = rl_service.decide(state)

    row = RecommendationHistory(
        student_id=progress.student_id,
        progress_id=progress.id,
        action=decision.recommendation.action.name,
        confidence=float(decision.recommendation.confidence),
        explanation=decision.recommendation.explanation,
        state=json.dumps(state, sort_keys=True),
        state_key=json.dumps(list(decision.state_key)),
        policy=decision.policy,
    )
    db.add(row)
    return row


def recommendation_to_dict(row: RecommendationHistory | None) -> dict[str, Any] | None:
    if row is None:
        return None
    return {
        "id": row.id,
        "progress_id": row.progress_id,
        "action": row.action,
        "confidence": row.confidence,
        "explanation": row.explanation,
        "policy": row.policy,
        "created_at": row.created_at,
        "outcome_progress_id": row.outcome_progress_id,
        "telemetry_available": True,
    }
