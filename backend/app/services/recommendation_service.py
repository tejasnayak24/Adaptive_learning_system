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
from app.utils.constants import normalize_difficulty
from rl_engine.training.rewards import REWARD_VERSION, RewardBreakdown, observed_reward

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
        "drowsy": bool(progress.drowsy),
        "difficulty": progress.difficulty,
        "response_time": float(progress.response_time),
        "hints_used": int(progress.hints_used or 0),
        "lesson_attempts": len([p for p in same_lesson if p.id <= progress.id]),
        "completed_lessons": completed_lessons,
    }


def outcome_breakdown(previous: Progress, outcome: Progress) -> RewardBreakdown:
    """Observed reward of a recommendation, from the student's next attempt.

    Uses the same outcome-based reward as offline training
    (``rl_engine.training.rewards.observed_reward``, reward version 2):
    difficulty-adjusted score change on the same lesson, or the quality of
    the advancement when the next attempt is on a different lesson, plus
    the change in measured attention and possible drowsiness. Camera
    values that were not measured (NULL) are left out, never guessed.
    """
    advanced = 1 if outcome.lesson_id != previous.lesson_id else 0
    return observed_reward(
        score_before=previous.quiz_score,
        score_after=outcome.quiz_score,
        difficulty_before=normalize_difficulty(previous.difficulty),
        difficulty_after=normalize_difficulty(outcome.difficulty),
        lessons_advanced=advanced,
        attention_before=previous.attention_score,
        attention_after=outcome.attention_score,
        drowsy_before=previous.drowsy,
        drowsy_after=outcome.drowsy,
    )


def outcome_reward(previous: Progress, outcome: Progress) -> float:
    return outcome_breakdown(previous, outcome).total


_DIFFICULTY_ORDER = {"EASY": 0, "MEDIUM": 1, "HARD": 2}
_SAME_LESSON_ACTIONS = {
    "REPEAT_LESSON",
    "PRACTICE_QUIZ",
    "SHOW_WORKED_EXAMPLE",
    "PROVIDE_HINT",
}


def infer_followed(action: str, previous: Progress, outcome: Progress) -> bool | None:
    """Whether the next attempt is consistent with following ``action``.

    Returns None when quiz records cannot show it (e.g. whether the student
    actually took a break or read a real-world example).
    """
    same_lesson = outcome.lesson_id == previous.lesson_id
    before = _DIFFICULTY_ORDER.get(normalize_difficulty(previous.difficulty))
    after = _DIFFICULTY_ORDER.get(normalize_difficulty(outcome.difficulty))

    if action in ("NEXT_LESSON", "SKIP_TO_ADVANCED_TOPIC"):
        return not same_lesson
    if action == "INCREASE_DIFFICULTY":
        return same_lesson and before is not None and after is not None and after > before
    if action == "DECREASE_DIFFICULTY":
        return same_lesson and before is not None and after is not None and after < before
    if action in _SAME_LESSON_ACTIONS:
        return same_lesson
    return None


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

    breakdown = outcome_breakdown(previous, new_progress)
    reward_row = RewardHistory(
        student_id=new_progress.student_id,
        reward=breakdown.total,
        state=pending.state_key,
        action=pending.action,
        recommendation_id=pending.id,
        progress_id=new_progress.id,
        reward_version=REWARD_VERSION,
        followed=infer_followed(pending.action, previous, new_progress),
        reward_detail=json.dumps(breakdown.as_dict(), sort_keys=True),
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
        model_version=decision.model_version or None,
        decision_detail=json.dumps(decision.detail, sort_keys=True),
    )
    db.add(row)
    return row


def _load_json(text: str | None) -> Any:
    if not text:
        return None
    try:
        return json.loads(text)
    except ValueError:
        return None


def recommendation_to_dict(row: RecommendationHistory | None) -> dict[str, Any] | None:
    if row is None:
        return None
    detail = _load_json(row.decision_detail) or {}
    return {
        "id": row.id,
        "progress_id": row.progress_id,
        "action": row.action,
        "confidence": row.confidence,
        "explanation": row.explanation,
        "confidence_kind": "heuristic_decision_strength",
        "policy": row.policy,
        "model_version": row.model_version,
        "q_values": detail.get("q_values"),
        "runner_up": detail.get("runner_up"),
        "blocked_actions": detail.get("blocked_actions"),
        "state_visits": detail.get("state_visits"),
        "created_at": row.created_at,
        "outcome_progress_id": row.outcome_progress_id,
        "telemetry_available": True,
    }
