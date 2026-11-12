"""Baseline policies used only to evaluate the learned Q-table policy.

``legacy_rule_policy`` is the hand-written rule set that decided every
recommendation before Phase 4 (``QLearningAgent._policy_action`` at
commit a98023d), copied unchanged so the old and new behaviour can be
compared on the same simulated students. It is **not** used at runtime.
"""

from __future__ import annotations

import random

from ..core.actions import Action
from ..core.constraints import permitted_actions
from ..models.student_state import Difficulty, StudentState

REPEAT_SCORE_THRESHOLD = 70
PRACTICE_SCORE_THRESHOLD = 80
HIGH_SCORE_THRESHOLD = 80
LOW_ATTENTION_THRESHOLD = 0.40


def legacy_rule_policy(state: StudentState) -> Action:
    """The pre-Phase-4 rules (always returned an action; Q-table never used)."""
    score = state.current_quiz_score
    attention = state.attention_score

    if score < REPEAT_SCORE_THRESHOLD:
        return Action.REPEAT_LESSON

    if attention < LOW_ATTENTION_THRESHOLD or state.yawning or state.looking_away:
        if score >= REPEAT_SCORE_THRESHOLD:
            return Action.FOCUS_RECOVERY

    if score < PRACTICE_SCORE_THRESHOLD:
        return Action.PRACTICE_QUIZ

    if state.difficulty in (Difficulty.EASY, Difficulty.MEDIUM):
        return Action.INCREASE_DIFFICULTY
    return Action.NEXT_LESSON


def make_random_policy(rng: random.Random):
    """Uniformly random choice among the permitted actions."""

    def policy(state: StudentState) -> Action:
        return rng.choice(permitted_actions(state))

    return policy
