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
    0.3,
    0.4,
    0.5,
    0.6,
    0.75,
    0.9,
    1.0,
)


DIFFICULTIES: Final[tuple[Difficulty, ...]] = (
    Difficulty.EASY,
    Difficulty.MEDIUM,
    Difficulty.HARD,
)


SCORE_VALUES: Final[tuple[int, ...]] = (
    30,
    40,
    50,
    60,
    70,
    80,
    90,
    95,
)


def create_initial_state() -> StudentState:
    subject = random.choice(list(CURRICULUM.keys()))
    topic = random.choice(list(CURRICULUM[subject].keys()))
    lesson = random.choice(CURRICULUM[subject][topic])

    current_score = random.choice(SCORE_VALUES)

    score_change = random.choice(
        (-15, -10, -5, 0, 5, 10, 15)
    )

    previous_score = max(
        0,
        min(100, current_score - score_change)
    )

    attention = random.choice(ATTENTION_VALUES)

    yawning = False
    looking_away = False

    if attention < 0.4:
        yawning = random.random() < 0.7
        looking_away = random.random() < 0.7
    elif attention < 0.6:
        yawning = random.random() < 0.2
        looking_away = random.random() < 0.2
    else:
        yawning = random.random() < 0.03
        looking_away = random.random() < 0.03

    difficulty = random.choice(DIFFICULTIES)

    return StudentState(
        subject=subject,
        topic=topic,
        lesson=lesson,
        previous_quiz_score=previous_score,
        current_quiz_score=current_score,
        attention_score=attention,
        yawning=yawning,
        looking_away=looking_away,
        difficulty=difficulty,
        response_time=random.choice(
            (5.0, 10.0, 15.0, 25.0, 40.0, 60.0)
        ),
        hints_used=random.randint(0, 3),
        lesson_attempts=random.randint(0, 4),
        completed_lessons=random.randint(0, 5),
    )