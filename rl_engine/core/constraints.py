"""Safety constraints: remove unsuitable actions before Q-values are compared.

These rules never *choose* an action. They only take actions out of the
candidate set when recommending them would be clearly inappropriate or
impossible. The learned Q-table then picks among the remaining actions.

The same mask is applied during training (exploration and the
``max_a' Q(s', a')`` term) and at runtime, so the Q-values the agent
learns are always values *under* the constraints it will run with.

Six actions are never blocked (REPEAT_LESSON, PRACTICE_QUIZ,
SHOW_WORKED_EXAMPLE, PROVIDE_HINT, FOCUS_RECOVERY,
SHOW_REAL_WORLD_APPLICATION), so at least six candidates always remain
and the decision is always left to the Q-table.
"""

from typing import Final

from ..models.student_state import Difficulty, StudentState
from .actions import Action

PASS_SCORE: Final[int] = 50          # below this the lesson is not passed
MASTERY_SCORE: Final[int] = 80       # at/above this the lesson is mastered
ADVANCED_SCORE: Final[int] = 90      # required before skipping lessons

NEVER_BLOCKED: Final[frozenset[Action]] = frozenset(
    {
        Action.REPEAT_LESSON,
        Action.PRACTICE_QUIZ,
        Action.SHOW_WORKED_EXAMPLE,
        Action.PROVIDE_HINT,
        Action.FOCUS_RECOVERY,
        Action.SHOW_REAL_WORLD_APPLICATION,
    }
)


def blocked_actions(state: StudentState) -> dict[Action, str]:
    """Return ``{action: reason}`` for every action unsuitable in ``state``."""
    if not isinstance(state, StudentState):
        raise TypeError("state must be an instance of StudentState.")

    score = state.current_quiz_score
    blocked: dict[Action, str] = {}

    # Difficulty can only move within EASY..HARD.
    if state.difficulty == Difficulty.HARD:
        blocked[Action.INCREASE_DIFFICULTY] = "already at the highest difficulty"
    elif score < PASS_SCORE:
        blocked[Action.INCREASE_DIFFICULTY] = (
            f"score below {PASS_SCORE}%: harder content would add frustration"
        )
    elif state.drowsy:
        blocked[Action.INCREASE_DIFFICULTY] = (
            "possible drowsiness: not the moment to raise difficulty"
        )

    if state.difficulty == Difficulty.EASY:
        blocked[Action.DECREASE_DIFFICULTY] = "already at the easiest difficulty"
    elif score >= MASTERY_SCORE:
        blocked[Action.DECREASE_DIFFICULTY] = (
            f"score of {MASTERY_SCORE}%+ shows the current level is not too hard"
        )

    # Never advance a student who has not passed the lesson.
    if score < PASS_SCORE:
        blocked[Action.NEXT_LESSON] = f"lesson not passed yet (below {PASS_SCORE}%)"

    # Skipping lessons needs excellent performance and an alert student.
    if score < ADVANCED_SCORE:
        blocked[Action.SKIP_TO_ADVANCED_TOPIC] = (
            f"skipping ahead requires at least {ADVANCED_SCORE}%"
        )
    elif state.drowsy:
        blocked[Action.SKIP_TO_ADVANCED_TOPIC] = (
            "possible drowsiness: not the moment to skip ahead"
        )

    if state.drowsy:
        blocked[Action.QUICK_CHALLENGE] = (
            "possible drowsiness: a timed challenge is not suitable"
        )

    assert not (NEVER_BLOCKED & blocked.keys())
    return blocked


def permitted_actions(state: StudentState) -> tuple[Action, ...]:
    """Actions the Q-table may choose from in ``state``, in index order."""
    blocked = blocked_actions(state)
    return tuple(a for a in Action if a not in blocked)
