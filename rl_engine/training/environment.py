"""Simulated learning environment for offline Q-learning training.

``LearningEnvironment`` wraps one ``SimulatedStudent`` (see
``simulation.py``) behind the usual ``reset`` / ``step`` interface. The
agent only ever sees observable ``StudentState`` objects; the student's
hidden traits and mastery stay inside the environment.

Each ``step(action)`` applies the action, lets the student take the next
quiz, and returns ``(next_state, reward, done)`` where the reward comes
from ``RewardCalculator`` (reward version 2, outcome based). An episode
ends when the student has completed the whole simulated curriculum (the
trainer also stops at ``max_steps_per_episode``).
"""

from __future__ import annotations

import random

from ..core.actions import Action
from ..models.student_state import StudentState
from .rewards import RewardBreakdown, RewardCalculator
from .simulation import TOTAL_LESSONS, SimulatedStudent


class LearningEnvironment:
    def __init__(self, rng: random.Random | None = None) -> None:
        self.rng = rng or random.Random()
        self.reward_calculator = RewardCalculator()
        self.student: SimulatedStudent = SimulatedStudent.sample(self.rng)
        self.current_state: StudentState = self.student.observe()
        self.last_breakdown: RewardBreakdown | None = None

    def reset(self, student: SimulatedStudent | None = None) -> StudentState:
        """Start a new episode with ``student`` (or a freshly sampled one)."""
        self.student = student or SimulatedStudent.sample(self.rng)
        self.current_state = self.student.observe()
        self.last_breakdown = None
        return self.current_state

    def step(self, action: Action) -> tuple[StudentState, float, bool]:
        if not isinstance(action, Action):
            raise TypeError("action must be an instance of Action.")

        before = self.current_state
        self.student.apply(action)
        after = self.student.observe()

        self.last_breakdown = self.reward_calculator.breakdown(before, action, after)
        self.current_state = after
        done = after.completed_lessons >= TOTAL_LESSONS
        return after, self.last_breakdown.total, done
