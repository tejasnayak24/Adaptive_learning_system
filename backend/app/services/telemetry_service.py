"""In-memory store for the latest facial-analysis telemetry per student.

Every update is timestamped. A reading older than ``STALE_AFTER_SECONDS``
is reported as unavailable: an old value is never presented as current.

Between a reset (start of a quiz) and the next reset, the store also keeps
a running average of the attention samples actually received, plus
whether yawning / looking away was observed at any point. When no sample
has been received the values are ``None`` -- the store never invents an
attention score.
"""

import time
from typing import Any

# A reading older than this is stale. The camera agent sends once per
# second, so a few missed beats are tolerated before declaring it stale.
STALE_AFTER_SECONDS = 5.0

_latest_telemetry: dict[int, dict[str, Any]] = {}


def _empty_record() -> dict[str, Any]:
    return {
        "attention_score": None,
        "yawning": None,
        "looking_away": None,
        "updated_at": None,
        # Aggregates since the last reset.
        "attention_sum": 0.0,
        "samples": 0,
        "yawning_observed": False,
        "looking_away_observed": False,
    }


def update_telemetry(
    student_id: int,
    attention_score: float,
    yawning: bool,
    looking_away: bool,
    now: float | None = None,
) -> None:
    record = _latest_telemetry.setdefault(student_id, _empty_record())
    now = time.time() if now is None else now

    record["attention_score"] = float(attention_score)
    record["yawning"] = bool(yawning)
    record["looking_away"] = bool(looking_away)
    record["updated_at"] = now

    record["attention_sum"] += float(attention_score)
    record["samples"] += 1
    record["yawning_observed"] = record["yawning_observed"] or bool(yawning)
    record["looking_away_observed"] = (
        record["looking_away_observed"] or bool(looking_away)
    )


def get_telemetry(student_id: int, now: float | None = None) -> dict[str, Any]:
    """Return the public telemetry view for a student.

    ``available`` is true only when a reading arrived within
    ``STALE_AFTER_SECONDS``. When unavailable, every measurement is
    ``None`` so callers cannot mistake missing data for low attention.
    """
    record = _latest_telemetry.get(student_id) or _empty_record()
    now = time.time() if now is None else now

    updated_at = record["updated_at"]
    age = None if updated_at is None else max(0.0, now - updated_at)
    available = age is not None and age <= STALE_AFTER_SECONDS

    if updated_at is None:
        status = "no_data"
    elif available:
        status = "live"
    else:
        status = "stale"

    samples = record["samples"]
    average = (record["attention_sum"] / samples) if samples else None

    return {
        "available": available,
        "status": status,
        "age_seconds": None if age is None else round(age, 1),
        "attention_score": record["attention_score"] if available else None,
        "yawning": record["yawning"] if available else None,
        "looking_away": record["looking_away"] if available else None,
        "session_samples": samples,
        "session_average_attention": (
            round(average, 4) if (available and average is not None) else None
        ),
        "yawning_observed": record["yawning_observed"] if available else None,
        "looking_away_observed": (
            record["looking_away_observed"] if available else None
        ),
    }


def reset_telemetry(student_id: int) -> None:
    """Start a new aggregation window (e.g. a new quiz attempt).

    The latest reading and its timestamp are kept so a live camera stays
    "live" across the reset; only the session aggregates are cleared.
    """
    record = _latest_telemetry.setdefault(student_id, _empty_record())
    record["attention_sum"] = 0.0
    record["samples"] = 0
    record["yawning_observed"] = False
    record["looking_away_observed"] = False


def clear_all() -> None:
    """Remove all telemetry (used by tests)."""
    _latest_telemetry.clear()
