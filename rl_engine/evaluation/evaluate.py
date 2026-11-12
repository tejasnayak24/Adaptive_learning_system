"""Evaluate policies on the same set of simulated students.

Every policy is run on identical students (episode *i* always samples its
student from ``Random(seed + i)``), so differences come from the policy,
not from easier students. Metrics:

* ``mean_return`` -- average total reward (reward version 2) per episode;
* ``mean_lessons_completed`` -- lessons finished within the step limit;
* ``mean_score_at_advance`` -- quiz score when the policy moved on;
* ``mean_difficulty_at_advance`` -- 0 EASY .. 2 HARD when moving on;
* ``premature_advance_rate`` -- share of advancements below the pass level
  (difficulty-adjusted score < 70, i.e. 70% EASY / 60% MEDIUM / 50% HARD);
* ``drowsy_step_rate`` -- share of steps that ended with possible drowsiness;
* ``mean_final_mastery`` -- hidden mastery of the last lesson reached;
* ``action_share`` -- how often each action was chosen.
"""

from __future__ import annotations

import random
import statistics
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from ..core.actions import Action
from ..core.constraints import blocked_actions
from ..models.student_state import StudentState
from ..training.environment import LearningEnvironment
from ..training.rewards import PASS_ADJUSTED_SCORE, adjusted_score
from ..training.simulation import SimulatedStudent

Policy = Callable[[StudentState], Action]


@dataclass(frozen=True)
class PolicyReport:
    name: str
    episodes: int
    mean_return: float
    return_stdev: float
    mean_lessons_completed: float
    mean_score_at_advance: float | None
    mean_difficulty_at_advance: float | None
    premature_advance_rate: float
    drowsy_step_rate: float
    mean_final_mastery: float
    constraint_violations: int
    action_share: dict[str, float]

    def as_dict(self) -> dict[str, Any]:
        return {k: getattr(self, k) for k in self.__dataclass_fields__}


def evaluate_policy(
    name: str,
    policy: Policy,
    *,
    episodes: int = 1000,
    seed: int = 12345,
    max_steps: int = 60,
) -> PolicyReport:
    returns: list[float] = []
    completed: list[int] = []
    advance_scores: list[int] = []
    advance_difficulty: list[int] = []
    final_mastery: list[float] = []
    actions: Counter[str] = Counter()
    steps = drowsy_steps = premature = violations = 0

    for episode in range(episodes):
        env = LearningEnvironment(random.Random(seed + episode))
        student = SimulatedStudent.sample(random.Random(seed + episode))
        state = env.reset(student)
        start_completed = state.completed_lessons
        total = 0.0

        for _ in range(max_steps):
            action = policy(state)
            if action in blocked_actions(state):
                violations += 1
            actions[action.name] += 1
            next_state, reward, done = env.step(action)

            if next_state.completed_lessons > state.completed_lessons:
                advance_scores.append(state.current_quiz_score)
                advance_difficulty.append(state.difficulty.value)
                if adjusted_score(state.current_quiz_score, state.difficulty) < PASS_ADJUSTED_SCORE:
                    premature += 1
            steps += 1
            drowsy_steps += int(next_state.drowsy)
            total += reward
            state = next_state
            if done:
                break

        returns.append(total)
        completed.append(state.completed_lessons - start_completed)
        final_mastery.append(env.student.mastery)

    n_actions = sum(actions.values()) or 1
    return PolicyReport(
        name=name,
        episodes=episodes,
        mean_return=round(statistics.fmean(returns), 3),
        return_stdev=round(statistics.pstdev(returns), 3),
        mean_lessons_completed=round(statistics.fmean(completed), 3),
        mean_score_at_advance=round(statistics.fmean(advance_scores), 2) if advance_scores else None,
        mean_difficulty_at_advance=round(statistics.fmean(advance_difficulty), 3) if advance_difficulty else None,
        premature_advance_rate=round(premature / len(advance_scores), 4) if advance_scores else 0.0,
        drowsy_step_rate=round(drowsy_steps / max(steps, 1), 4),
        mean_final_mastery=round(statistics.fmean(final_mastery), 4),
        constraint_violations=violations,
        action_share={a.name: round(actions[a.name] / n_actions, 4) for a in Action},
    )


def greedy_policy(agent) -> Policy:
    """The runtime decision rule of a trained ``QLearningAgent``."""

    def policy(state: StudentState) -> Action:
        return agent.decide(state).action

    return policy
