"""Simulated learning environment for the Reinforcement Learning Engine.

This module implements a lightweight, deterministic simulation the
Q-learning agent can interact with during training. It plays the role a
real backend would eventually play: given a student's current state and
a chosen action, it produces the student's next state and a reward,
without any of the agent's or trainer's code needing to know whether the
student behind those transitions is simulated or real.

The simulation intentionally models only small, predictable effects for
each action. It is not meant to be a realistic model of human learning —
it exists to give the agent a consistent signal to learn from during
development, ahead of real student interaction data becoming available.
"""

from dataclasses import replace
from typing import Final

from ..core.actions import Action
from ..models.student_state import Difficulty, StudentState
from .rewards import RewardCalculator
from .simulation import CURRICULUM

# The single source of truth for the curriculum's shape (subjects, their
# topics, and each topic's lessons, in deterministic iteration order) is
# ``training.simulation.CURRICULUM``. The total lesson count is derived
# from it rather than hardcoded, so this module never has its own
# opinion about how large the curriculum is.
TOTAL_LESSONS: Final[int] = sum(
    len(lessons) for topics in CURRICULUM.values() for lessons in topics.values()
)
QUIZ_SCORE_IMPROVEMENT: Final[int] = 5
ATTENTION_IMPROVEMENT: Final[float] = 0.1
LESSONS_PER_SKIP: Final[int] = 2


class LearningEnvironment:
    """A simulated environment in which the RL agent trains.

    The environment owns the student's current state and advances it one
    action at a time, mirroring the ``reset``/``step`` interface common
    to reinforcement learning environments. Every state produced by
    ``step`` is a new ``StudentState`` instance built with
    ``dataclasses.replace`` — the previous state is never mutated.
    """

    def __init__(self, initial_state: StudentState) -> None:
        """Create the environment with the student's starting state.

        Args:
            initial_state: The state the environment begins in.
        """
        self.current_state = initial_state
        self.reward_calculator = RewardCalculator()

    def reset(self, initial_state: StudentState) -> StudentState:
        """Reset the environment to a new starting state.

        Args:
            initial_state: The state to reset the environment to.

        Returns:
            The state the environment was reset to.
        """
        self.current_state = initial_state
        return self.current_state

    def step(self, action: Action) -> tuple[StudentState, float, bool]:
        """Apply an action to the current state and advance the episode.

        Args:
            action: The learning action chosen by the agent.

        Returns:
            A tuple of (next_state, reward, done):
                next_state: The new ``StudentState`` after the action.
                reward: The reward for taking ``action`` in the state the
                    environment was in before this call.
                done: Whether the episode has finished, i.e. the student
                    has reached the end of the curriculum.
        """
        if not isinstance(action, Action):
            raise TypeError("action must be an instance of Action.")

        reward = self.reward_calculator.calculate_reward(self.current_state, action)
        next_state = self._apply_action(action)

        self.current_state = next_state
        done = next_state.completed_lessons >= TOTAL_LESSONS

        return next_state, reward, done

    def _apply_action(self, action: Action) -> StudentState:
        """Compute the state that results from applying ``action``.

        This holds all of the simulation's state-transition logic. It is
        the only place that knows *how* each action changes a
        ``StudentState`` — ``step`` just orchestrates validation,
        reward calculation, and bookkeeping around it.

        Args:
            action: The learning action chosen by the agent.

        Returns:
            The ``StudentState`` that results from applying ``action`` to
            ``self.current_state``.
        """
        state = self.current_state

        if action == Action.NEXT_LESSON:
            completed_lessons = state.completed_lessons + 1
            subject, topic, lesson = self._curriculum_position(completed_lessons)
            return replace(
                state,
                completed_lessons=completed_lessons,
                subject=subject,
                topic=topic,
                lesson=lesson,
                lesson_attempts=0,
                hints_used=0,
            )

        elif action == Action.REPEAT_LESSON:
            return replace(state, lesson_attempts=state.lesson_attempts + 1)

        elif action == Action.INCREASE_DIFFICULTY:
            new_level = min(state.difficulty.value + 1, Difficulty.HARD.value)
            return replace(state, difficulty=Difficulty(new_level))

        elif action == Action.DECREASE_DIFFICULTY:
            new_level = max(state.difficulty.value - 1, Difficulty.EASY.value)
            return replace(state, difficulty=Difficulty(new_level))

        elif action == Action.PRACTICE_QUIZ:
            improved_score = min(state.current_quiz_score + QUIZ_SCORE_IMPROVEMENT, 100)
            return replace(
                state,
                previous_quiz_score=state.current_quiz_score,
                current_quiz_score=improved_score,
                lesson_attempts=state.lesson_attempts + 1,
            )

        elif action == Action.QUICK_CHALLENGE:
            return replace(state, attention_score=self._improve_attention(state.attention_score))

        elif action == Action.SHOW_WORKED_EXAMPLE:
            improved_score = min(state.current_quiz_score + QUIZ_SCORE_IMPROVEMENT, 100)
            return replace(
                state,
                attention_score=self._improve_attention(state.attention_score),
                current_quiz_score=improved_score,
            )

        elif action == Action.PROVIDE_HINT:
            return replace(
                state,
                hints_used=state.hints_used + 1,
                attention_score=self._improve_attention(state.attention_score),
            )

        elif action == Action.FOCUS_RECOVERY:
            return replace(
                state,
                attention_score=self._improve_attention(state.attention_score),
                yawning=False,
                looking_away=False,
            )

        elif action == Action.SHOW_REAL_WORLD_APPLICATION:
            return replace(state, attention_score=self._improve_attention(state.attention_score))

        elif action == Action.SKIP_TO_ADVANCED_TOPIC:
            completed_lessons = state.completed_lessons + LESSONS_PER_SKIP
            subject, topic, lesson = self._curriculum_position(completed_lessons)
            return replace(
                state,
                completed_lessons=completed_lessons,
                subject=subject,
                topic=topic,
                lesson=lesson,
                lesson_attempts=0,
                hints_used=0,
            )

        else:
            raise ValueError(f"Unrecognized action: {action}")

    def _curriculum_position(self, completed_lessons: int) -> tuple[str, str, str]:
        """Translate a completed-lesson count into a curriculum position.

        The curriculum's shape and ordering come entirely from the
        shared ``training.simulation.CURRICULUM`` mapping (subject ->
        topic -> ordered list of lesson names), so this environment
        holds no independent opinion about how many subjects, topics, or
        lessons exist -- it only walks ``CURRICULUM`` in order and picks
        out the entry at ``completed_lessons``.

        Once ``completed_lessons`` reaches or exceeds ``TOTAL_LESSONS``
        the position is clamped to the final lesson of the final topic
        of the final subject, since there is nothing further to advance
        to.

        Args:
            completed_lessons: How many lessons the student has finished.

        Returns:
            A ``(subject, topic, lesson)`` tuple of the actual names from
            ``CURRICULUM`` at that position in the curriculum.
        """
        position = min(completed_lessons, TOTAL_LESSONS - 1)

        index = 0
        for subject, topics in CURRICULUM.items():
            for topic, lessons in topics.items():
                for lesson in lessons:
                    if index == position:
                        return subject, topic, lesson
                    index += 1

        raise RuntimeError("Curriculum traversal failed. Check CURRICULUM consistency.")

    def _improve_attention(self, current: float) -> float:
        """Apply the standard attention bump, capped at the max score.

        Several actions (quick challenges, worked examples, hints, focus
        recovery, real-world applications) nudge attention up by the same
        fixed amount. Centralizing that here avoids repeating the same
        ``min(...)`` calculation in every branch of ``_apply_action``.

        Args:
            current: The student's current attention score.

        Returns:
            The new attention score, capped at 1.0.
        """
        return min(current + ATTENTION_IMPROVEMENT, 1.0)