"""Simulation utilities for Reinforcement Learning training.

This module provides simulated student states for offline Reinforcement
Learning training. It is responsible only for creating realistic initial
student states for each training episode.

During production, ``StudentState`` instances should be constructed from
real learner data received from the backend rather than from this module.
"""

from __future__ import annotations

import random
from typing import Final

from ..core.actions import Difficulty
from ..models.student_state import StudentState


# ---------------------------------------------------------------------
# Simulated curriculum
# ---------------------------------------------------------------------

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


# ---------------------------------------------------------------------
# Default values for a newly simulated learner
# ---------------------------------------------------------------------

INITIAL_QUIZ_SCORE: Final[int] = 0
INITIAL_ATTENTION_SCORE: Final[float] = 1.0
INITIAL_RESPONSE_TIME: Final[float] = 0.0
INITIAL_HINTS_USED: Final[int] = 0
INITIAL_LESSON_ATTEMPTS: Final[int] = 0
INITIAL_COMPLETED_LESSONS: Final[int] = 0


def create_initial_state() -> StudentState:
    """Create the initial simulated student state for a training episode.

    A subject, topic, and lesson are selected randomly from the simulated
    curriculum. All learner-related metrics begin with sensible default
    values representing a student starting a new lesson.

    Returns:
        A ``StudentState`` representing the initial state of a simulated
        learner.
    """
    subject = random.choice(list(CURRICULUM.keys()))
    topic = random.choice(list(CURRICULUM[subject].keys()))
    lesson = random.choice(CURRICULUM[subject][topic])

    return StudentState(
        subject=subject,
        topic=topic,
        lesson=lesson,
        previous_quiz_score=INITIAL_QUIZ_SCORE,
        current_quiz_score=INITIAL_QUIZ_SCORE,
        attention_score=INITIAL_ATTENTION_SCORE,
        yawning=False,
        looking_away=False,
        difficulty=Difficulty.EASY,
        response_time=INITIAL_RESPONSE_TIME,
        hints_used=INITIAL_HINTS_USED,
        lesson_attempts=INITIAL_LESSON_ATTEMPTS,
        completed_lessons=INITIAL_COMPLETED_LESSONS,
    )