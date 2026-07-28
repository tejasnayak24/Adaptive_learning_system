"""Reward calculation for the Reinforcement Learning Engine.

This module defines how appropriate a chosen learning action was for a
given student state, expressed as a single numerical reward. The reward
signal is what teaches the Q-learning agent which actions are
pedagogically sound in which situations — it is the only place in the
system where "good teaching" is encoded as a number.

The reward logic here is deliberately simple, explicit, and rule-based
so that it is easy to read, reason about, and adjust as the project's
understanding of good pedagogy evolves.

Reward scale:
    +10.0  Excellent decision
     +5.0  Good decision
      0.0  Neutral
     -5.0  Poor decision
    -10.0  Very poor decision
"""

from ..core.actions import Action
from ..models.student_state import Difficulty, StudentState

HIGH_SCORE = 80
LOW_SCORE = 50
HIGH_ATTENTION = 0.6
LOW_ATTENTION = 0.4
MANY_HINTS = 2
MANY_ATTEMPTS = 3

# Stricter than HIGH_SCORE: skipping ahead is a larger, harder-to-reverse
# jump than a normal difficulty increase, so it demands stronger evidence
# of mastery.
ADVANCED_SKIP_SCORE_THRESHOLD = HIGH_SCORE + 10

EXCELLENT_REWARD = 10.0
GOOD_REWARD = 5.0
NEUTRAL_REWARD = 0.0
POOR_REWARD = -5.0
VERY_POOR_REWARD = -10.0


class RewardCalculator:
    """Computes a deterministic reward for a (state, action) pair.

    The calculator holds no internal state and performs no randomness —
    calling ``calculate_reward`` twice with the same arguments always
    produces the same result. It reads the given ``StudentState`` only;
    it never modifies it.
    """

    def calculate_reward(self, state: StudentState, action: Action) -> float:
        """Return the reward for taking ``action`` given ``state``.

        Args:
            state: The student's state at the time the action was taken.
            action: The learning action that was recommended.

        Returns:
            A float reward on the scale [-10.0, 10.0]: strongly positive
            for excellent decisions, strongly negative for very poor
            ones, and smaller in magnitude for less clear-cut cases.

        Raises:
            TypeError: If ``state`` is not an instance of
                ``StudentState``, or if ``action`` is not an instance of
                ``Action``.
        """
        if not isinstance(state, StudentState):
            raise TypeError("state must be an instance of StudentState.")
        if not isinstance(action, Action):
            raise TypeError("action must be an instance of Action.")

        if action == Action.NEXT_LESSON:
            if (
                state.attention_score >= HIGH_ATTENTION
                and state.current_quiz_score >= LOW_SCORE
                and state.lesson_attempts < MANY_ATTEMPTS
            ):
                return EXCELLENT_REWARD
            return POOR_REWARD

        if action == Action.REPEAT_LESSON:
            if state.current_quiz_score < LOW_SCORE and state.lesson_attempts < MANY_ATTEMPTS:
                return GOOD_REWARD
            return POOR_REWARD

        if action == Action.INCREASE_DIFFICULTY:
            # Difficulty is clamped at HARD by the environment, so this
            # would be a no-op; reward NEUTRAL rather than POOR since
            # the choice itself wasn't wrong, just ineffective here.
            if state.difficulty == Difficulty.HARD:
                return NEUTRAL_REWARD
            if state.current_quiz_score >= HIGH_SCORE and state.attention_score >= HIGH_ATTENTION:
                return EXCELLENT_REWARD
            return POOR_REWARD

        if action == Action.DECREASE_DIFFICULTY:
            # Symmetric no-op case at the EASY floor.
            if state.difficulty == Difficulty.EASY:
                return NEUTRAL_REWARD
            # Performance-based only; low attention is FOCUS_RECOVERY's
            # signal to own, so the two actions don't compete for the
            # same trigger.
            if state.current_quiz_score < LOW_SCORE:
                return EXCELLENT_REWARD
            return POOR_REWARD

        if action == Action.PRACTICE_QUIZ:
            if state.current_quiz_score < LOW_SCORE or state.current_quiz_score < state.previous_quiz_score:
                return GOOD_REWARD
            return NEUTRAL_REWARD

        if action == Action.QUICK_CHALLENGE:
            # GOOD rather than EXCELLENT for the same trigger as
            # INCREASE_DIFFICULTY: a difficulty increase is a lasting
            # change, while a quick challenge is a lighter, one-off action.
            if state.attention_score >= HIGH_ATTENTION and state.current_quiz_score >= HIGH_SCORE:
                return GOOD_REWARD
            return POOR_REWARD

        if action == Action.SHOW_WORKED_EXAMPLE:
            if state.hints_used >= MANY_HINTS or state.lesson_attempts >= MANY_ATTEMPTS:
                return EXCELLENT_REWARD
            return POOR_REWARD

        if action == Action.PROVIDE_HINT:
            if state.hints_used < MANY_HINTS and (
                state.current_quiz_score < LOW_SCORE
                or state.current_quiz_score < state.previous_quiz_score
            ):
                return GOOD_REWARD
            return POOR_REWARD

        if action == Action.FOCUS_RECOVERY:
            # Owns the attention/engagement signal exclusively, distinct
            # from DECREASE_DIFFICULTY's performance-based trigger above.
            if state.attention_score < LOW_ATTENTION or state.yawning or state.looking_away:
                return EXCELLENT_REWARD
            return POOR_REWARD

        if action == Action.SHOW_REAL_WORLD_APPLICATION:
            if state.attention_score < HIGH_ATTENTION and state.current_quiz_score >= LOW_SCORE:
                return GOOD_REWARD
            return POOR_REWARD

        if action == Action.SKIP_TO_ADVANCED_TOPIC:
            if (
                state.current_quiz_score >= ADVANCED_SKIP_SCORE_THRESHOLD
                and state.previous_quiz_score >= HIGH_SCORE
                and state.attention_score >= HIGH_ATTENTION
            ):
                return EXCELLENT_REWARD
            return VERY_POOR_REWARD

        raise ValueError(f"Unrecognized action: {action}")