"""In-memory store for live facial-analysis telemetry, one record per student.

Readings arrive as heartbeats from the paired camera agent of the
student's active monitoring session. Every reading is stamped with the
server's receive time; a reading older than ``STALE_AFTER_SECONDS`` is
reported as unavailable, so an old value is never presented as current.

Between window resets (the start of a quiz attempt) the store keeps
aggregates of the measurements actually received:

* attention is averaged over samples in which a face was visible;
* samples in which the camera worked but no face was visible are counted
  separately (``face_absent_samples``) -- they are not missing data, but
  there is no attention to measure;
* yawning, sustained looking away and possible drowsiness are recorded if
  observed at any point.

When nothing was measured the values are ``None``; nothing is invented.
"""

import time
from typing import Any

# The agent sends once per second; a few missed beats are tolerated.
STALE_AFTER_SECONDS = 5.0


def _now() -> float:
    return time.time()


_latest_telemetry: dict[int, dict[str, Any]] = {}


def _empty_aggregates() -> dict[str, Any]:
    return {
        "attention_sum": 0.0,
        "samples": 0,
        "face_absent_samples": 0,
        "camera_error_samples": 0,
        "yawning_observed": False,
        "looking_away_observed": False,
        "drowsy_observed": False,
    }


def _empty_record(session_id: str | None = None) -> dict[str, Any]:
    return {
        "session_id": session_id,
        "updated_at": None,
        "camera_ok": None,
        "camera_error": None,
        "face_detected": None,
        "face_stable": None,
        "lighting_ok": None,
        "attention_score": None,
        "yawning": None,
        "looking_away": None,
        "possible_drowsiness": None,
        "face_count": None,
        "multiple_faces": None,
        **_empty_aggregates(),
    }


def record_heartbeat(student_id: int, session_id: str, sample: dict[str, Any], now: float | None = None) -> None:
    """Store one heartbeat from the student's paired camera agent."""
    now = _now() if now is None else now

    record = _latest_telemetry.get(student_id)
    if record is None or record["session_id"] != session_id:
        record = _empty_record(session_id)
        _latest_telemetry[student_id] = record

    camera_ok = bool(sample.get("camera_ok"))
    face = camera_ok and bool(sample.get("face_detected"))
    attention = sample.get("attention_score") if face else None

    record.update(
        updated_at=now,
        camera_ok=camera_ok,
        camera_error=None if camera_ok else (sample.get("camera_error") or "unavailable"),
        face_detected=face,
        face_stable=face and bool(sample.get("face_stable")),
        lighting_ok=sample.get("lighting_ok") if camera_ok else None,
        attention_score=None if attention is None else float(attention),
        yawning=bool(sample.get("yawning")) if face else None,
        looking_away=bool(sample.get("looking_away")) if face else None,
        possible_drowsiness=bool(sample.get("possible_drowsiness")) if face else None,
        # Independent of the student's own face: only needs a working camera.
        face_count=sample.get("face_count") if camera_ok else None,
        multiple_faces=sample.get("multiple_faces") if camera_ok else None,
    )

    if not camera_ok:
        record["camera_error_samples"] += 1
    elif not face:
        record["face_absent_samples"] += 1
    else:
        if attention is not None:
            record["attention_sum"] += float(attention)
            record["samples"] += 1
        record["yawning_observed"] |= bool(sample.get("yawning"))
        record["looking_away_observed"] |= bool(sample.get("looking_away"))
        record["drowsy_observed"] |= bool(sample.get("possible_drowsiness"))


def update_telemetry(
    student_id: int,
    attention_score: float,
    yawning: bool,
    looking_away: bool,
    now: float | None = None,
    session_id: str = "direct",
    possible_drowsiness: bool = False,
) -> None:
    """Record a face-present measurement (used by tests and tools)."""
    record_heartbeat(
        student_id,
        session_id,
        {
            "camera_ok": True,
            "face_detected": True,
            "face_stable": True,
            "attention_score": attention_score,
            "yawning": yawning,
            "looking_away": looking_away,
            "possible_drowsiness": possible_drowsiness,
        },
        now=now,
    )


def _age(record: dict[str, Any], now: float) -> float | None:
    updated_at = record["updated_at"]
    return None if updated_at is None else max(0.0, now - updated_at)


def get_telemetry(student_id: int, now: float | None = None) -> dict[str, Any]:
    """Return the public live-telemetry view for a student.

    ``available`` is true only when a reading arrived within
    ``STALE_AFTER_SECONDS`` and the camera was working. When unavailable,
    every measurement is ``None`` so missing data cannot be mistaken for
    low attention.
    """
    record = _latest_telemetry.get(student_id) or _empty_record()
    now = _now() if now is None else now

    age = _age(record, now)
    fresh = age is not None and age <= STALE_AFTER_SECONDS
    available = fresh and bool(record["camera_ok"])

    if record["updated_at"] is None:
        status = "no_data"
    elif not fresh:
        status = "stale"
    elif not record["camera_ok"]:
        status = "camera_unavailable"
    elif not record["face_detected"]:
        status = "no_face"
    else:
        status = "live"

    samples = record["samples"]
    average = (record["attention_sum"] / samples) if samples else None

    def live(key):
        return record[key] if available else None

    return {
        "available": available,
        "status": status,
        "session_id": record["session_id"],
        "age_seconds": None if age is None else round(age, 1),
        "camera_ok": record["camera_ok"] if fresh else None,
        "camera_error": record["camera_error"] if fresh else None,
        "face_detected": live("face_detected"),
        "face_stable": live("face_stable"),
        "lighting_ok": live("lighting_ok"),
        "attention_score": live("attention_score"),
        "yawning": live("yawning"),
        "looking_away": live("looking_away"),
        "possible_drowsiness": live("possible_drowsiness"),
        "face_count": live("face_count"),
        "multiple_faces": live("multiple_faces"),
        "session_samples": samples,
        "face_absent_samples": record["face_absent_samples"],
        "session_average_attention": (
            round(average, 4) if (available and average is not None) else None
        ),
        "yawning_observed": live("yawning_observed"),
        "looking_away_observed": live("looking_away_observed"),
        "drowsy_observed": live("drowsy_observed"),
    }


def attempt_metrics(student_id: int, session_id: str) -> dict[str, Any]:
    """Camera measurements gathered during the current window of a session.

    Used when a quiz is submitted. Values are what was actually measured
    in this window (even if the camera has since dropped); ``None`` when
    nothing was measured, or when the store holds a different session.
    """
    record = _latest_telemetry.get(student_id)
    if record is None or record["session_id"] != session_id or record["samples"] == 0:
        return {
            "attention_score": None,
            "yawning": None,
            "looking_away": None,
            "drowsy": None,
            "samples": 0 if record is None or record["session_id"] != session_id else record["samples"],
        }

    return {
        "attention_score": round(record["attention_sum"] / record["samples"], 4),
        "yawning": record["yawning_observed"],
        "looking_away": record["looking_away_observed"],
        "drowsy": record["drowsy_observed"],
        "samples": record["samples"],
    }


def reset_telemetry(student_id: int) -> None:
    """Start a new aggregation window (e.g. a new quiz attempt).

    The latest reading and its timestamp are kept so a live camera stays
    "live" across the reset; only the window aggregates are cleared.
    """
    record = _latest_telemetry.setdefault(student_id, _empty_record())
    record.update(_empty_aggregates())


def forget_student(student_id: int) -> None:
    _latest_telemetry.pop(student_id, None)


def clear_all() -> None:
    """Remove all telemetry (used by tests)."""
    _latest_telemetry.clear()
