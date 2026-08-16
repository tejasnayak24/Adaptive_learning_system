from typing import Any

_latest_telemetry: dict[int, dict[str, Any]] = {}


def update_telemetry(
    student_id: int,
    attention_score: float,
    yawning: bool,
    looking_away: bool,
) -> None:
    previous = _latest_telemetry.get(student_id, {})

    _latest_telemetry[student_id] = {
        "attention_score": float(attention_score),
        "yawning": bool(yawning),
        "looking_away": bool(looking_away),
        "yawning_observed": bool(
            previous.get("yawning_observed", False) or yawning
        ),
        "looking_away_observed": bool(
            previous.get("looking_away_observed", False) or looking_away
        ),
    }


def get_telemetry(student_id: int) -> dict[str, Any]:
    return _latest_telemetry.get(
        student_id,
        {
            "attention_score": None,
            "yawning": False,
            "looking_away": False,
            "yawning_observed": False,
            "looking_away_observed": False,
        },
    )


def reset_telemetry(student_id: int) -> None:
    _latest_telemetry[student_id] = {
        "attention_score": None,
        "yawning": False,
        "looking_away": False,
        "yawning_observed": False,
        "looking_away_observed": False,
    }