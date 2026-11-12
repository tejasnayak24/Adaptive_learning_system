"""Shared response serializers."""

from typing import Any


def progress_to_dict(progress) -> dict[str, Any]:
    """Serialize a Progress row into the public API shape."""
    return {
        "id": progress.id,
        "student_id": progress.student_id,
        "lesson_id": progress.lesson_id,
        "quiz_score": progress.quiz_score,
        "response_time": progress.response_time,
        "attention_score": progress.attention_score,
        "yawning": progress.yawning,
        "looking_away": progress.looking_away,
        "telemetry_available": progress.attention_score is not None,
        "difficulty": progress.difficulty,
        "completed": progress.completed,
    }
