"""Simulation utilities for Reinforcement Learning training."""

from __future__ import annotations

import random
from typing import Final

from ..models.student_state import Difficulty, StudentState


CURRICULUM: Final[dict[str, dict[str, list[str]]]] = {
    "Mathematics": {
        "Algebra": [
            "Introduction to Algebra",
            "Linear Equations",
        ],
        "Geometry": [
            "Triangles",
            "Circles",
        ],
    },
    "Science": {
        "Physics": [
            "Motion",
            "Force",
        ],
        "Chemistry": [
            "Atoms",
            "Molecules",
        ],
    },
    "English": {
        "Grammar": [
            "Parts of Speech",
            "Tenses",
        ],
        "Reading": [
            "Comprehension",
            "Vocabulary",
        ],
    },
}


ATTENTION_VALUES: Final[tuple[float, ...]] = (
    0.2,
    0.35,
    0.5,
    0.7,
    0.9,
)


DIFFICULTIES: Final[tuple[Difficulty, ...]] = (
    Difficulty.EASY,
    Difficulty.MEDIUM,
    Difficulty.HARD,
)


def create_initial_state() -> StudentState:
    """Create a varied simulated student state for a training episode."""

    subject = random.choice(list(CURRICULUM.keys()))
    topic = random.choice(list(CURRICULUM[subject].keys()))
    lesson = random.choice(CURRICULUM[subject][topic])

    current_score = random.choice(
        (30, 45, 55, 65, 75, 85, 90, 95)
    )

    previous_score = random.choice(
        (30, 45, 55, 65, 75, 85, 90, 95)
    )

    attention = random.choice(ATTENTION_VALUES)

    yawning = (
        attention <= 0.35
        and random.random() < 0.65
    )

    looking_away = (
        attention <= 0.35
        and random.random() < 0.65
    )

    if not yawning and random.random() < 0.08:
        yawning = True

    if not looking_away and random.random() < 0.08:
        looking_away = True

    return StudentState(
        subject=subject,
        topic=topic,
        lesson=lesson,
        previous_quiz_score=previous_score,
        current_quiz_score=current_score,
        attention_score=attention,
        yawning=yawning,
        looking_away=looking_away,
        difficulty=random.choice(DIFFICULTIES),
        response_time=random.choice(
            (5.0, 10.0, 15.0, 25.0)
        ),
        hints_used=random.randint(0, 3),
        lesson_attempts=random.randint(0, 4),
        completed_lessons=random.randint(0, 5),
    )