"""Student state representation for the Reinforcement Learning Engine.

This module defines the complete snapshot of a student's academic and
engagement status at the moment the RL agent is asked to make a decision.
The backend is responsible for constructing this object from whatever
sources it has (database records, the facial analysis module, the quiz
service, etc.) and passing it into the RL engine. The RL engine itself
has no knowledge of where these values came from — it only consumes the
state.

The numeric/categorical encoding used for Q-learning (e.g. one-hot
encoding, normalization, feature vectors) is a concern of the training
and inference layers, not of this module. This file exists solely to
define the state itself.
"""

from dataclasses import dataclass
from enum import Enum


class Difficulty(Enum):
    """The difficulty level of the content currently being presented.

    An explicit integer value is assigned to each member, starting from 0,
    so the difficulty level can be used consistently as a feature when the
    RL engine encodes ``StudentState`` into a numeric representation.
    """

    EASY = 0
    MEDIUM = 1
    HARD = 2


@dataclass
class StudentState:
    """A complete snapshot of a student's learning state.

    This represents everything the RL agent is allowed to know about a
    student when deciding the next learning action. It intentionally
    contains only academic, performance, and engagement information —
    nothing related to how the state was produced or stored (no database
    IDs, timestamps, session tokens, or backend-specific fields).

    Attributes:
        subject: The subject currently being studied (e.g. "Mathematics").
        topic: The topic within the subject (e.g. "Quadratic Equations").
        lesson: The specific lesson within the topic.
        previous_quiz_score: Score (0-100) from the student's previous
            quiz attempt, used to detect trends in performance.
        current_quiz_score: Score (0-100) from the student's most recent
            quiz attempt.
        attention_score: Normalized engagement score in the range
            [0.0, 1.0], typically derived from the facial analysis module,
            where 1.0 represents full attention.
        yawning: Whether the student was observed yawning, an indicator
            of fatigue.
        looking_away: Whether the student was observed looking away from
            the screen, an indicator of distraction.
        difficulty: The difficulty level of the content currently being
            presented to the student.
        response_time: Time in seconds the student took to respond to the
            current question or lesson interaction.
        hints_used: Number of hints the student has used on the current
            lesson or question.
        lesson_attempts: Number of times the student has attempted the
            current lesson.
        completed_lessons: Total number of lessons the student has
            completed so far, used as a broader progress indicator.
    """

    # -- Academic Information --
    subject: str
    topic: str
    lesson: str

    # -- Performance --
    previous_quiz_score: int
    current_quiz_score: int

    # -- Engagement --
    attention_score: float
    yawning: bool
    looking_away: bool

    # -- Learning Context --
    difficulty: Difficulty
    response_time: float
    hints_used: int
    lesson_attempts: int
    completed_lessons: int

    def __post_init__(self) -> None:
        """Perform lightweight sanity checks on the student state.

        This validation only guards against structurally invalid data
        (e.g. negative counts, out-of-range scores) that would indicate a
        bug in the caller. It intentionally does not enforce
        domain-specific business rules, which belong outside this module.
        """
        if not self.subject:
            raise ValueError("subject must not be empty.")
        if not self.topic:
            raise ValueError("topic must not be empty.")
        if not self.lesson:
            raise ValueError("lesson must not be empty.")

        if not 0 <= self.previous_quiz_score <= 100:
            raise ValueError("previous_quiz_score must be between 0 and 100.")
        if not 0 <= self.current_quiz_score <= 100:
            raise ValueError("current_quiz_score must be between 0 and 100.")

        if not 0.0 <= self.attention_score <= 1.0:
            raise ValueError("attention_score must be between 0.0 and 1.0.")

        if self.response_time < 0.0:
            raise ValueError("response_time must not be negative.")
        if self.hints_used < 0:
            raise ValueError("hints_used must not be negative.")
        if self.lesson_attempts < 0:
            raise ValueError("lesson_attempts must not be negative.")
        if self.completed_lessons < 0:
            raise ValueError("completed_lessons must not be negative.")