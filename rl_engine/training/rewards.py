from ..core.actions import Action
from ..models.student_state import Difficulty, StudentState


HIGH_SCORE = 80
LOW_SCORE = 50
ADVANCED_SCORE = 90

HIGH_ATTENTION = 0.6
LOW_ATTENTION = 0.4

MANY_HINTS = 2
MANY_ATTEMPTS = 3

EXCELLENT_REWARD = 15.0
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

        score = state.current_quiz_score
        attention = state.attention_score

        distracted = (
            attention < LOW_ATTENTION
            or state.yawning
            or state.looking_away
        )

        highly_attentive = (
            attention >= HIGH_ATTENTION
            and not state.yawning
            and not state.looking_away
        )

        improving = score >= state.previous_quiz_score

        # ---------------------------------------------------------
        # FOCUS RECOVERY
        # ---------------------------------------------------------
        if action == Action.FOCUS_RECOVERY:
            if distracted:
                return EXCELLENT_REWARD

            return VERY_POOR_REWARD

        # ---------------------------------------------------------
        # DISTRACTED STUDENT
        # Focus recovery should take priority over academic actions.
        # ---------------------------------------------------------
        if distracted:
            if action in (
                Action.PRACTICE_QUIZ,
                Action.NEXT_LESSON,
                Action.INCREASE_DIFFICULTY,
                Action.QUICK_CHALLENGE,
                Action.SKIP_TO_ADVANCED_TOPIC,
            ):
                return VERY_POOR_REWARD

        # ---------------------------------------------------------
        # DECREASE DIFFICULTY
        # ---------------------------------------------------------
        if action == Action.DECREASE_DIFFICULTY:

            if state.difficulty == Difficulty.EASY:
                return VERY_POOR_REWARD

            if score < LOW_SCORE:
                return EXCELLENT_REWARD

            if score < 60:
                return GOOD_REWARD

            return POOR_REWARD

        # ---------------------------------------------------------
        # REPEAT LESSON
        #
        # 0-49%  -> strongly recommend reviewing the lesson
        # 50-69% -> still below mastery, so review the lesson
        # ---------------------------------------------------------
        if action == Action.REPEAT_LESSON:

            if score < LOW_SCORE:
                return EXCELLENT_REWARD

            if 50 <= score < 70:
                return EXCELLENT_REWARD

            return POOR_REWARD

        # ---------------------------------------------------------
        # PRACTICE QUIZ
        #
        # 70-79% -> practice to reinforce understanding
        # ---------------------------------------------------------
        if action == Action.PRACTICE_QUIZ:

            if (
                70 <= score < HIGH_SCORE
                and not distracted
            ):
                return EXCELLENT_REWARD

            if (
                score >= LOW_SCORE
                and score < HIGH_SCORE
                and improving
                and not distracted
            ):
                return GOOD_REWARD

            return POOR_REWARD

        # ---------------------------------------------------------
        # PROVIDE HINT
        # ---------------------------------------------------------
        if action == Action.PROVIDE_HINT:

            if (
                score < LOW_SCORE
                and state.hints_used < MANY_HINTS
            ):
                return GOOD_REWARD

            if (
                score < HIGH_SCORE
                and not improving
                and state.hints_used < MANY_HINTS
            ):
                return GOOD_REWARD

            return POOR_REWARD

        # ---------------------------------------------------------
        # SHOW WORKED EXAMPLE
        #
        # Used when the student has repeatedly struggled with
        # genuinely low performance.
        # ---------------------------------------------------------
        if action == Action.SHOW_WORKED_EXAMPLE:

            if (
                score < LOW_SCORE
                and state.lesson_attempts >= MANY_ATTEMPTS
            ):
                return EXCELLENT_REWARD

            if (
                score < LOW_SCORE
                and state.hints_used >= MANY_HINTS
            ):
                return EXCELLENT_REWARD

            if score < LOW_SCORE:
                return GOOD_REWARD

            return POOR_REWARD

        # ---------------------------------------------------------
        # NEXT LESSON
        # ---------------------------------------------------------
        if action == Action.NEXT_LESSON:

            if (
                score >= HIGH_SCORE
                and highly_attentive
            ):
                return EXCELLENT_REWARD

            if (
                score >= HIGH_SCORE
                and attention >= HIGH_ATTENTION
            ):
                return GOOD_REWARD

            return POOR_REWARD

        # ---------------------------------------------------------
        # INCREASE DIFFICULTY
        #
        # Never increase difficulty when already HARD.
        # ---------------------------------------------------------
        if action == Action.INCREASE_DIFFICULTY:

            if state.difficulty == Difficulty.HARD:
                return VERY_POOR_REWARD

            if (
                score >= HIGH_SCORE
                and highly_attentive
            ):
                return EXCELLENT_REWARD

            return POOR_REWARD

        # ---------------------------------------------------------
        # QUICK CHALLENGE
        # ---------------------------------------------------------
        if action == Action.QUICK_CHALLENGE:

            if state.difficulty == Difficulty.HARD:
                return POOR_REWARD

            if (
                score >= HIGH_SCORE
                and highly_attentive
            ):
                return GOOD_REWARD

            return POOR_REWARD

        # ---------------------------------------------------------
        # REAL-WORLD APPLICATION
        #
        # Appropriate for moderate attention with acceptable
        # performance, but not during strong distraction.
        # ---------------------------------------------------------
        if action == Action.SHOW_REAL_WORLD_APPLICATION:

            if (
                LOW_ATTENTION <= attention < HIGH_ATTENTION
                and score >= LOW_SCORE
                and not state.yawning
                and not state.looking_away
            ):
                return GOOD_REWARD

            return POOR_REWARD

        # ---------------------------------------------------------
        # SKIP TO ADVANCED TOPIC
        #
        # Only appropriate for excellent performance and strong
        # attention.
        # ---------------------------------------------------------
        if action == Action.SKIP_TO_ADVANCED_TOPIC:

            if (
                score >= ADVANCED_SCORE
                and highly_attentive
                and state.difficulty == Difficulty.HARD
            ):
                return EXCELLENT_REWARD

            if (
                score >= ADVANCED_SCORE
                and highly_attentive
            ):
                return GOOD_REWARD

            return VERY_POOR_REWARD

        raise ValueError(f"Unrecognized action: {action}")