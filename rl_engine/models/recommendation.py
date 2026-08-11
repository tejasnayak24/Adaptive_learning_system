"""Recommendation output for the Reinforcement Learning Engine.

This module defines the single output type produced by the RL engine.
Given a student's current learning state, the RL agent evaluates its
policy and returns a ``Recommendation`` describing which learning action
to take next, how confident the policy is in that choice, and a
human-readable explanation of the decision.

This class is completely independent of FastAPI, Flask, PostgreSQL, any
database, and any frontend or UI code. It is intended to be returned by
the RL agent and consumed by the backend, which is solely responsible
for resolving the recommended action into concrete lesson, topic, or UI
content.
"""

from dataclasses import dataclass

from rl_engine.core.actions import Action


@dataclass(frozen=True)
class Recommendation:
    """The RL agent's recommended next learning action for a student.

    This is the sole output of the RL agent's decision-making process.
    Instances are immutable (``frozen=True``), so a recommendation
    cannot be altered after it has been produced by the agent and
    handed off to the backend. The class contains only the
    recommendation itself; it has no awareness of how the backend will
    store, render, or act on it.

    Attributes:
        action: The learning action recommended by the RL policy.
        confidence: The policy's confidence in this recommendation, in
            the range [0.0, 1.0], where 1.0 indicates full confidence.
        explanation: A short, human-readable justification for the
            recommendation, suitable for logging or display to an
            instructor or student.
    """

    action: Action
    confidence: float
    explanation: str

    def __post_init__(self) -> None:
        """Validate the recommendation's fields.

        Raises:
            TypeError: If ``action`` is not an instance of ``Action``,
                or if ``explanation`` is not a string.
            ValueError: If ``confidence`` is outside the range
                [0.0, 1.0], or if ``explanation`` is empty or contains
                only whitespace.
        """
        if not isinstance(self.action, Action):
            raise TypeError("action must be an instance of Action.")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0.")
        if not isinstance(self.explanation, str):
            raise TypeError("explanation must be a string.")
        if not self.explanation.strip():
            raise ValueError("explanation must not be empty or whitespace-only.")