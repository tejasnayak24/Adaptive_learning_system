"""Shared constants and small normalisation helpers for the backend."""

# Canonical quiz/progress difficulty values. Stored and returned in
# uppercase so the backend, frontend and RL engine agree on one spelling.
DIFFICULTIES: tuple[str, ...] = ("EASY", "MEDIUM", "HARD")


def normalize_difficulty(value: str) -> str:
    """Return the canonical uppercase difficulty, or raise ValueError."""
    if not isinstance(value, str):
        raise ValueError("difficulty must be a string")

    normalized = value.strip().upper()

    if normalized not in DIFFICULTIES:
        raise ValueError(
            f"difficulty must be one of {list(DIFFICULTIES)}, got {value!r}"
        )

    return normalized
