"""Shared response serializers."""

from typing import Any


def progress_to_dict(progress) -> dict[str, Any]:
    """Serialize a Progress row into the public API shape."""
    return {
        "id": progress.id,
        "student_id": progress.student_id,
        "lesson_id": progress.lesson_id,
        "quiz_id": progress.quiz_id,
        "quiz_score": progress.quiz_score,
        "correct_count": progress.correct_count,
        "total_questions": progress.total_questions,
        "hints_used": progress.hints_used,
        "response_time": progress.response_time,
        "attention_score": progress.attention_score,
        "yawning": progress.yawning,
        "looking_away": progress.looking_away,
        "drowsy": progress.drowsy,
        "attempt_mode": progress.attempt_mode,
        "monitoring_session_id": progress.monitoring_session_id,
        "telemetry_available": progress.attention_score is not None,
        "difficulty": progress.difficulty,
        "completed": progress.completed,
        "created_at": progress.created_at,
    }
