"""Student state representation for the Reinforcement Learning Engine.

This module defines the complete snapshot of a student's academic and
engagement status at the moment the RL agent is asked to make a decision.

The backend is responsible for constructing this object from whatever
sources it has (database records, the facial analysis module, the quiz
service, etc.) and passing it into the RL engine.

The RL engine itself has no knowledge of where these values came from —
it only consumes the state.

The numeric/categorical encoding used for Q-learning (e.g. one-hot
encoding, normalization, feature vectors) is a concern of the training
and inference layers, not of this module.

This file exists solely to define the state itself.
"""

from dataclasses import dataclass
from enum import Enum


class Difficulty(Enum):
    """Difficulty level of the content currently being presented."""

    EASY = 0
    MEDIUM = 1
    HARD = 2


@dataclass(frozen=True)
class StudentState:
    """A complete snapshot of a student's learning state.

    This represents everything the RL agent is allowed to know about
    a student when deciding the next learning action.

    It intentionally contains only academic, performance, and engagement
    information — nothing related to how the state was produced or stored.
    """

    # -- Academic Information --
    subject: str
    topic: str
    lesson: str

    # -- Performance --
    previous_quiz_score: int
    current_quiz_score: int

    # -- Engagement --
    # None means attention data is unavailable.
    attention_score: float | None
    yawning: bool
    looking_away: bool

    # -- Learning Context --
    difficulty: Difficulty
    response_time: float
    hints_used: int
    lesson_attempts: int
    completed_lessons: int

    def __post_init__(self) -> None:
        """Validate the structure and values of the student state."""

        if not self.subject.strip():
            raise ValueError("subject must not be empty.")

        if not self.topic.strip():
            raise ValueError("topic must not be empty.")

        if not self.lesson.strip():
            raise ValueError("lesson must not be empty.")

        if not 0 <= self.previous_quiz_score <= 100:
            raise ValueError(
                "previous_quiz_score must be between 0 and 100."
            )

        if not 0 <= self.current_quiz_score <= 100:
            raise ValueError(
                "current_quiz_score must be between 0 and 100."
            )

        # Validate attention only when telemetry is available.
        if self.attention_score is not None:
            if not isinstance(self.attention_score, (int, float)):
                raise TypeError(
                    "attention_score must be a number or None."
                )

            if not 0.0 <= self.attention_score <= 1.0:
                raise ValueError(
                    "attention_score must be between 0.0 and 1.0."
                )

        if not isinstance(self.yawning, bool):
            raise TypeError("yawning must be a bool.")

        if not isinstance(self.looking_away, bool):
            raise TypeError("looking_away must be a bool.")

        if not isinstance(self.difficulty, Difficulty):
            raise TypeError(
                "difficulty must be an instance of Difficulty."
            )

        if self.response_time < 0.0:
            raise ValueError(
                "response_time must not be negative."
            )

        if self.hints_used < 0:
            raise ValueError(
                "hints_used must not be negative."
            )

        if self.lesson_attempts < 0:
            raise ValueError(
                "lesson_attempts must not be negative."
            )

        if self.completed_lessons < 0:
            raise ValueError(
                "completed_lessons must not be negative."
            )