"""Outcome-based reward for the Aegis Q-learning agent (reward version 2).

The reward judges what *happened after* an action, not whether the action
matched a hand-written rule. It is computed from quantities that can be
observed both in the training simulator and in real student data (two
consecutive quiz attempts), so the same function is used for

* offline training (``LearningEnvironment.step``), and
* evaluating real recommendations (``reward_history`` in the backend).

Reward components (one "reward unit" ~ a 10-point quiz improvement):

====================  =====================================================
Component             Value and justification
====================  =====================================================
learning_gain         +0.1 per point of *difficulty-adjusted* score change on
                      the same lesson, clipped to [-3, +3]. A score at MEDIUM
                      counts 10 points more than the same score at EASY, HARD
                      20 more (``DIFFICULTY_CREDIT``), so moving up a level and
                      scoring 10 points lower is neutral rather than punished.
                      Clipping stops one lucky/unlucky quiz from dominating.
lesson_completion     Per lesson advanced, judged on the difficulty-adjusted
                      score before moving on. Mastered (adjusted >= 90, i.e.
                      90% EASY / 80% MEDIUM / 70% HARD): +3, the value of a
                      30-point improvement -- finishing a lesson properly is
                      the main goal but must not outweigh learning it.
                      Otherwise: -0.1 per point still missing to mastery
                      (e.g. 75% on EASY -> -1.5, 50% on EASY -> -4.0). The
                      unlearned material is charged at the same rate as
                      learning is rewarded, so the policy cannot gain by
                      abandoning a lesson to collect cheap early progress on
                      the next one. Using the adjusted score stops it from
                      "mastering" lessons only on EASY.
frustration           -1 if the new score is below 40% on MEDIUM/HARD content
                      (the difficulty is too high for the student right now).
engagement_change     +2 x change in attention (0-1 scale), so +0.25 attention
                      = +0.5. Only the *change* is rewarded: a student with low
                      attention is not penalised for being tired; an action
                      that restores attention is credited.
drowsiness            +1 when possible drowsiness observed before the action
                      is gone afterwards; -1 while it is still present. This is
                      what makes a break worthwhile only when it is needed.
step_cost             -0.5 per action. Study time is limited, so actions that
                      do not lead to learning (e.g. repeated breaks for an
                      alert student) have a net cost.
====================  =====================================================

Unknown camera values (``None``) simply drop the engagement/drowsiness
terms; nothing is guessed.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Final

from ..core.actions import Action
from ..models.student_state import Difficulty, StudentState

REWARD_VERSION: Final[int] = 2

LEARNING_GAIN_PER_POINT: Final[float] = 0.1
LEARNING_GAIN_CLIP: Final[float] = 3.0
DIFFICULTY_CREDIT: Final[dict[int, int]] = {0: 0, 1: 10, 2: 20}

MASTERY_ADJUSTED_SCORE: Final[int] = 90
PASS_ADJUSTED_SCORE: Final[int] = 70  # used for reporting premature advancement
MASTERED_ADVANCE_BONUS: Final[float] = 3.0
UNMASTERED_POINT_COST: Final[float] = 0.1

FRUSTRATION_SCORE: Final[int] = 40
FRUSTRATION_PENALTY: Final[float] = -1.0

ENGAGEMENT_WEIGHT: Final[float] = 2.0
DROWSINESS_CLEARED_BONUS: Final[float] = 1.0
DROWSINESS_PERSISTS_PENALTY: Final[float] = -1.0

STEP_COST: Final[float] = -0.5


@dataclass(frozen=True)
class RewardBreakdown:
    learning_gain: float = 0.0
    lesson_completion: float = 0.0
    frustration: float = 0.0
    engagement_change: float = 0.0
    drowsiness: float = 0.0
    step_cost: float = STEP_COST

    @property
    def total(self) -> float:
        return round(
            self.learning_gain
            + self.lesson_completion
            + self.frustration
            + self.engagement_change
            + self.drowsiness
            + self.step_cost,
            4,
        )

    def as_dict(self) -> dict[str, float]:
        data = {k: round(v, 4) for k, v in asdict(self).items()}
        data["total"] = self.total
        return data


def _difficulty_index(value: Difficulty | int | str) -> int:
    if isinstance(value, Difficulty):
        return value.value
    if isinstance(value, str):
        return Difficulty[value.strip().upper()].value
    if isinstance(value, int) and 0 <= value <= 2:
        return value
    raise ValueError(f"Unknown difficulty: {value!r}")


def adjusted_score(score: float, difficulty: Difficulty | int | str) -> float:
    return float(score) + DIFFICULTY_CREDIT[_difficulty_index(difficulty)]


def observed_reward(
    *,
    score_before: float,
    score_after: float,
    difficulty_before: Difficulty | int | str,
    difficulty_after: Difficulty | int | str,
    lessons_advanced: int = 0,
    attention_before: float | None = None,
    attention_after: float | None = None,
    drowsy_before: bool | None = None,
    drowsy_after: bool | None = None,
) -> RewardBreakdown:
    """Reward for one learning step, from observable before/after values."""
    if lessons_advanced < 0:
        raise ValueError("lessons_advanced must not be negative.")

    learning_gain = 0.0
    lesson_completion = 0.0

    if lessons_advanced == 0:
        delta = adjusted_score(score_after, difficulty_after) - adjusted_score(
            score_before, difficulty_before
        )
        learning_gain = max(
            -LEARNING_GAIN_CLIP,
            min(LEARNING_GAIN_CLIP, LEARNING_GAIN_PER_POINT * delta),
        )
    else:
        # The new score belongs to a different lesson, so it is not compared
        # with the old one; the quality of the advancement is judged instead.
        readiness = adjusted_score(score_before, difficulty_before)
        if readiness >= MASTERY_ADJUSTED_SCORE:
            per_lesson = MASTERED_ADVANCE_BONUS
        else:
            per_lesson = -UNMASTERED_POINT_COST * (MASTERY_ADJUSTED_SCORE - readiness)
        lesson_completion = per_lesson * lessons_advanced

    frustration = 0.0
    if score_after < FRUSTRATION_SCORE and _difficulty_index(difficulty_after) > 0:
        frustration = FRUSTRATION_PENALTY

    engagement_change = 0.0
    if attention_before is not None and attention_after is not None:
        engagement_change = ENGAGEMENT_WEIGHT * (attention_after - attention_before)

    drowsiness = 0.0
    if drowsy_after is not None:
        if drowsy_after:
            drowsiness = DROWSINESS_PERSISTS_PENALTY
        elif drowsy_before:
            drowsiness = DROWSINESS_CLEARED_BONUS

    return RewardBreakdown(
        learning_gain=learning_gain,
        lesson_completion=lesson_completion,
        frustration=frustration,
        engagement_change=engagement_change,
        drowsiness=drowsiness,
    )


class RewardCalculator:
    """Reward for a simulated transition ``state --action--> next_state``."""

    def calculate_reward(
        self,
        state: StudentState,
        action: Action,
        next_state: StudentState,
    ) -> float:
        return self.breakdown(state, action, next_state).total

    def breakdown(
        self,
        state: StudentState,
        action: Action,
        next_state: StudentState,
    ) -> RewardBreakdown:
        if not isinstance(state, StudentState) or not isinstance(next_state, StudentState):
            raise TypeError("state and next_state must be StudentState instances.")
        if not isinstance(action, Action):
            raise TypeError("action must be an instance of Action.")

        return observed_reward(
            score_before=state.current_quiz_score,
            score_after=next_state.current_quiz_score,
            difficulty_before=state.difficulty,
            difficulty_after=next_state.difficulty,
            lessons_advanced=max(0, next_state.completed_lessons - state.completed_lessons),
            attention_before=state.attention_score,
            attention_after=next_state.attention_score,
            drowsy_before=state.drowsy,
            drowsy_after=next_state.drowsy,
        )
