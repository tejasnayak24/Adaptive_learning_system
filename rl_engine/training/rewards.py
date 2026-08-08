from ..core.actions import Action
from ..models.student_state import Difficulty, StudentState

HIGH_SCORE = 80
LOW_SCORE = 50
HIGH_ATTENTION = 0.6
LOW_ATTENTION = 0.4
MANY_HINTS = 2
MANY_ATTEMPTS = 3

ADVANCED_SKIP_SCORE_THRESHOLD = HIGH_SCORE + 10

EXCELLENT_REWARD = 10.0
GOOD_REWARD = 5.0
NEUTRAL_REWARD = 0.0
POOR_REWARD = -5.0
VERY_POOR_REWARD = -10.0


class RewardCalculator:

    def calculate_reward(self, state: StudentState, action: Action) -> float:

        if not isinstance(state, StudentState):
            raise TypeError("state must be an instance of StudentState.")

        if not isinstance(action, Action):
            raise TypeError("action must be an instance of Action.")

        if action == Action.NEXT_LESSON:
            if (
                state.difficulty == Difficulty.HARD
                and state.attention_score >= HIGH_ATTENTION
                and state.current_quiz_score >= HIGH_SCORE
                and state.lesson_attempts < MANY_ATTEMPTS
            ):
                return EXCELLENT_REWARD

            return POOR_REWARD

        if action == Action.REPEAT_LESSON:
            if (
                state.current_quiz_score < LOW_SCORE
                and state.lesson_attempts < MANY_ATTEMPTS
            ):
                return GOOD_REWARD

            return POOR_REWARD

        if action == Action.INCREASE_DIFFICULTY:
            if state.difficulty == Difficulty.HARD:
                return NEUTRAL_REWARD

            if (
                state.current_quiz_score >= HIGH_SCORE
                and state.attention_score >= HIGH_ATTENTION
                and not state.yawning
                and not state.looking_away
            ):
                return EXCELLENT_REWARD

            return POOR_REWARD

        if action == Action.DECREASE_DIFFICULTY:
            if state.difficulty == Difficulty.EASY:
                return NEUTRAL_REWARD

            if state.current_quiz_score < LOW_SCORE:
                return EXCELLENT_REWARD

            return POOR_REWARD

        if action == Action.PRACTICE_QUIZ:
            if (
                state.current_quiz_score < LOW_SCORE
                or state.current_quiz_score < state.previous_quiz_score
            ):
                return GOOD_REWARD

            return POOR_REWARD

        if action == Action.QUICK_CHALLENGE:
            if state.difficulty == Difficulty.HARD:
                return POOR_REWARD

            if (
                state.attention_score >= HIGH_ATTENTION
                and state.current_quiz_score >= HIGH_SCORE
            ):
                return GOOD_REWARD

            return POOR_REWARD

        if action == Action.SHOW_WORKED_EXAMPLE:
            if (
                state.hints_used >= MANY_HINTS
                or state.lesson_attempts >= MANY_ATTEMPTS
            ):
                return EXCELLENT_REWARD

            return POOR_REWARD

        if action == Action.PROVIDE_HINT:
            if (
                state.hints_used < MANY_HINTS
                and (
                    state.current_quiz_score < LOW_SCORE
                    or state.current_quiz_score < state.previous_quiz_score
                )
            ):
                return GOOD_REWARD

            return POOR_REWARD

        if action == Action.FOCUS_RECOVERY:
            if (
                state.attention_score < LOW_ATTENTION
                or state.yawning
                or state.looking_away
            ):
                return EXCELLENT_REWARD

            return POOR_REWARD

        if action == Action.SHOW_REAL_WORLD_APPLICATION:
            if (
                LOW_ATTENTION <= state.attention_score < HIGH_ATTENTION
                and state.current_quiz_score >= LOW_SCORE
            ):
                return GOOD_REWARD

            return POOR_REWARD

        if action == Action.SKIP_TO_ADVANCED_TOPIC:
            return VERY_POOR_REWARD

        raise ValueError(f"Unrecognized action: {action}")