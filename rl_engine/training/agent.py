"""Tabular Q-learning agent for the Aegis Reinforcement Learning Engine.

Training (offline, simulator only)
    ``choose_action`` is epsilon-greedy over the *permitted* actions
    (``core.constraints``); ``update`` applies the Q-learning rule

        Q(s,a) <- Q(s,a) + alpha * [ r + gamma * max_{a' in P(s')} Q(s',a') - Q(s,a) ]

    (target = r when the episode ends), with alpha = ``learning_rate`` and
    gamma = ``discount_factor``. Visit counts are kept per (s, a).

Runtime (real students)
    ``decide`` is purely greedy and read-only: it never explores, never
    updates Q-values and never adds states to the table. It

    1. encodes the student's state (``core.state_encoding``, version 3);
    2. removes unsuitable actions (safety constraints);
    3. keeps only permitted actions that were tried at least
       ``min_action_visits`` times in training (no untested actions on
       real students);
    4. picks the one with the highest learned Q-value;
    5. if this exact state was never learned, uses the most-visited
       learned state that differs in exactly one feature ("nearest
       learned state"); if there is none, falls back to REPEAT_LESSON,
       the lowest-risk action, and says so (``policy = "fallback"``).

Confidence is a *heuristic decision-strength indicator* in [0, 1], not a
calibrated probability:

    confidence = (1 - exp(-margin / confidence_scale)) * support

``margin`` is the Q-value gap between the chosen and the next-best
eligible action; ``support = min(1, visits(s, a*) / full_support_visits)``.
When only one eligible action exists, the separation term is 0.5 (no
alternative to compare with). Confidence is halved for a nearest-state
decision and 0 for the fallback.
"""

from __future__ import annotations

import json
import math
import random
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Final

from ..core.actions import Action
from ..core.config import RLConfig
from ..core.constraints import blocked_actions
from ..core.state_encoding import (
    STATE_FEATURES,
    STATE_KEY_VERSION,
    StateKey,
    encode_state,
    is_valid_key,
)
from ..models.recommendation import Recommendation
from ..models.student_state import StudentState
from .rewards import REWARD_VERSION

FILE_FORMAT: Final[str] = "aegis-q-table"
FALLBACK_ACTION: Final[Action] = Action.REPEAT_LESSON
NEAREST_STATE_CONFIDENCE_FACTOR: Final[float] = 0.5
SINGLE_CANDIDATE_SEPARATION: Final[float] = 0.5

POLICY_Q_LEARNING: Final[str] = "q_learning"
POLICY_NEAREST: Final[str] = "q_learning_nearest_state"
POLICY_FALLBACK: Final[str] = "fallback"

ACTION_LABELS: Final[dict[Action, str]] = {
    Action.NEXT_LESSON: "Next lesson",
    Action.REPEAT_LESSON: "Repeat lesson",
    Action.INCREASE_DIFFICULTY: "Increase difficulty",
    Action.DECREASE_DIFFICULTY: "Decrease difficulty",
    Action.PRACTICE_QUIZ: "Practice quiz",
    Action.QUICK_CHALLENGE: "Quick challenge",
    Action.SHOW_WORKED_EXAMPLE: "Worked example",
    Action.PROVIDE_HINT: "Retry with hints",
    Action.FOCUS_RECOVERY: "Focus-recovery break",
    Action.SHOW_REAL_WORLD_APPLICATION: "Real-world application",
    Action.SKIP_TO_ADVANCED_TOPIC: "Skip to advanced topic",
}


@dataclass(frozen=True)
class PolicyDecision:
    """Everything about one runtime decision, for storage and display."""

    action: Action
    confidence: float
    explanation: str
    policy: str
    state_key: StateKey
    source_state_key: StateKey | None
    q_values: dict[str, float]
    blocked: dict[str, str]
    untested: tuple[str, ...]
    margin: float | None
    state_visits: int
    action_visits: int
    runner_up: str | None = None
    detail: dict[str, Any] = field(default_factory=dict)

    def to_recommendation(self) -> Recommendation:
        return Recommendation(
            action=self.action,
            confidence=self.confidence,
            explanation=self.explanation,
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "action": self.action.name,
            "confidence": self.confidence,
            "confidence_kind": "heuristic_decision_strength",
            "policy": self.policy,
            "state_key": list(self.state_key),
            "state_features": list(STATE_FEATURES),
            "source_state_key": list(self.source_state_key) if self.source_state_key else None,
            "q_values": self.q_values,
            "runner_up": self.runner_up,
            "margin": self.margin,
            "blocked_actions": self.blocked,
            "untested_actions": list(self.untested),
            "state_visits": self.state_visits,
            "action_visits": self.action_visits,
        }


class QLearningAgent:
    """Tabular Q-learning agent with safety-constrained action selection."""

    def __init__(self, config: RLConfig, rng: random.Random | None = None) -> None:
        if not isinstance(config, RLConfig):
            raise TypeError("config must be an instance of RLConfig.")

        self.config = config
        self.rng = rng or random.Random()
        self.epsilon: float = config.epsilon
        self.q_table: dict[StateKey, dict[Action, float]] = {}
        self.visits: dict[StateKey, dict[Action, int]] = {}
        self.metadata: dict[str, Any] = {}

    # ------------------------------------------------------------------
    # State helpers
    # ------------------------------------------------------------------
    def state_key(self, state: StudentState) -> StateKey:
        return encode_state(state, self.config)

    # Kept for callers/tests written against the v2 API.
    def _state_to_key(self, state: StudentState) -> StateKey:
        return self.state_key(state)

    def _ensure_state(self, key: StateKey) -> None:
        if key not in self.q_table:
            self.q_table[key] = {action: 0.0 for action in Action}
            self.visits[key] = {action: 0 for action in Action}

    # ------------------------------------------------------------------
    # Training
    # ------------------------------------------------------------------
    def choose_action(self, state: StudentState) -> Action:
        """Epsilon-greedy choice among permitted actions (training only)."""
        key = self.state_key(state)
        self._ensure_state(key)
        permitted = [a for a in Action if a not in blocked_actions(state)]

        if self.rng.random() < self.epsilon:
            return self.rng.choice(permitted)

        values = self.q_table[key]
        best_value = max(values[a] for a in permitted)
        tied = [a for a in permitted if values[a] == best_value]
        return self.rng.choice(tied)

    def update(
        self,
        state: StudentState,
        action: Action,
        reward: float,
        next_state: StudentState,
        done: bool,
    ) -> None:
        if not isinstance(action, Action):
            raise TypeError("action must be an instance of Action.")
        if isinstance(reward, bool) or not isinstance(reward, (int, float)):
            raise TypeError("reward must be a real number.")
        if not isinstance(done, bool):
            raise TypeError("done must be a bool.")

        key = self.state_key(state)
        self._ensure_state(key)
        current_q = self.q_table[key][action]

        if done:
            target = float(reward)
        else:
            next_key = self.state_key(next_state)
            self._ensure_state(next_key)
            next_values = self.q_table[next_key]
            next_blocked = blocked_actions(next_state)
            best_next = max(v for a, v in next_values.items() if a not in next_blocked)
            target = float(reward) + self.config.discount_factor * best_next

        self.q_table[key][action] = current_q + self.config.learning_rate * (target - current_q)
        self.visits[key][action] += 1

    def decay_epsilon(self) -> None:
        self.epsilon = max(self.epsilon * self.config.epsilon_decay, self.config.min_epsilon)

    # ------------------------------------------------------------------
    # Runtime decision (greedy, read-only)
    # ------------------------------------------------------------------
    def decide(self, state: StudentState) -> PolicyDecision:
        if not isinstance(state, StudentState):
            raise TypeError("state must be an instance of StudentState.")

        key = self.state_key(state)
        blocked = blocked_actions(state)
        permitted = [a for a in Action if a not in blocked]

        source_key: StateKey | None = key
        eligible = self._eligible(key, permitted)
        policy = POLICY_Q_LEARNING

        if not eligible:
            source_key = self._nearest_learned_state(key, permitted)
            if source_key is not None:
                eligible = self._eligible(source_key, permitted)
                policy = POLICY_NEAREST

        blocked_named = {a.name: reason for a, reason in blocked.items()}

        if not eligible:
            return PolicyDecision(
                action=FALLBACK_ACTION,
                confidence=0.0,
                explanation=(
                    _action_sentence(state, FALLBACK_ACTION)
                    + " This learning situation was not covered during training, "
                    "so Aegis chose the lowest-risk action instead of a learned one."
                ),
                policy=POLICY_FALLBACK,
                state_key=key,
                source_state_key=None,
                q_values={},
                blocked=blocked_named,
                untested=tuple(a.name for a in permitted),
                margin=None,
                state_visits=0,
                action_visits=0,
            )

        assert source_key is not None
        values = self.q_table[source_key]
        counts = self.visits[source_key]
        # Highest Q first; ties broken by the fixed action index (deterministic).
        ranked = sorted(eligible, key=lambda a: (-values[a], a.value))
        best = ranked[0]
        runner_up = ranked[1] if len(ranked) > 1 else None
        margin = values[best] - values[runner_up] if runner_up is not None else None

        support = min(1.0, counts[best] / self.config.full_support_visits)
        if margin is not None:
            separation = 1.0 - math.exp(-margin / self.config.confidence_scale)
        else:
            # Only one action is sufficiently tested here: nothing to compare
            # it with, so it cannot be a clear-cut decision.
            separation = SINGLE_CANDIDATE_SEPARATION
        confidence = separation * support
        if policy == POLICY_NEAREST:
            confidence *= NEAREST_STATE_CONFIDENCE_FACTOR
        confidence = round(max(0.0, min(1.0, confidence)), 4)

        untested = tuple(a.name for a in permitted if a not in eligible)
        explanation = self._explain(state, best, runner_up, len(eligible), policy)

        return PolicyDecision(
            action=best,
            confidence=confidence,
            explanation=explanation,
            policy=policy,
            state_key=key,
            source_state_key=source_key if source_key != key else None,
            q_values={a.name: round(values[a], 4) for a in ranked},
            blocked=blocked_named,
            untested=untested,
            margin=round(margin, 4) if margin is not None else None,
            state_visits=sum(counts.values()),
            action_visits=counts[best],
            runner_up=runner_up.name if runner_up is not None else None,
        )

    def recommend(self, state: StudentState) -> Recommendation:
        return self.decide(state).to_recommendation()

    def _eligible(self, key: StateKey, permitted: Iterable[Action]) -> list[Action]:
        counts = self.visits.get(key)
        if not counts or key not in self.q_table:
            return []
        return [a for a in permitted if counts.get(a, 0) >= self.config.min_action_visits]

    def _nearest_learned_state(self, key: StateKey, permitted: list[Action]) -> StateKey | None:
        best_key, best_visits = None, 0
        for other, counts in self.visits.items():
            if sum(1 for x, y in zip(other, key) if x != y) != 1:
                continue
            if not self._eligible(other, permitted):
                continue
            total = sum(counts.values())
            if total > best_visits:
                best_key, best_visits = other, total
        return best_key

    def _explain(
        self,
        state: StudentState,
        action: Action,
        runner_up: Action | None,
        n_eligible: int,
        policy: str,
    ) -> str:
        text = _action_sentence(state, action)
        basis = (
            "the learned Q-table"
            if policy == POLICY_Q_LEARNING
            else "the learned Q-table for the most similar trained situation"
        )
        text += f" Chosen by {basis} as the best of {n_eligible} suitable actions"
        if runner_up is not None:
            text += f" (next best: {ACTION_LABELS[runner_up].lower()})"
        return text + "."

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------
    def save_q_table(self, path: str | Path, metadata: dict[str, Any] | None = None) -> None:
        payload = {
            "format": FILE_FORMAT,
            "state_key_version": STATE_KEY_VERSION,
            "state_features": list(STATE_FEATURES),
            "actions": [a.name for a in Action],
            "reward_version": REWARD_VERSION,
            "epsilon": self.epsilon,
            "metadata": metadata if metadata is not None else self.metadata,
            "entries": [
                {
                    "state_key": list(key),
                    "values": {a.name: v for a, v in values.items()},
                    "visits": {a.name: self.visits.get(key, {}).get(a, 0) for a in values},
                }
                for key, values in sorted(self.q_table.items())
            ],
        }
        with open(path, "w", encoding="utf-8") as file:
            json.dump(payload, file)

    @classmethod
    def load_q_table(cls, path: str | Path, config: RLConfig) -> "QLearningAgent":
        """Load a saved table, refusing anything not built for this engine."""
        with open(path, encoding="utf-8") as file:
            payload = json.load(file)

        saved_version = payload.get("state_key_version", 1)
        if saved_version != STATE_KEY_VERSION:
            raise ValueError(
                f"Saved state_key_version {saved_version} does not match current "
                f"STATE_KEY_VERSION {STATE_KEY_VERSION}; retrain with `python -m rl_engine.train`."
            )
        if payload.get("format") != FILE_FORMAT:
            raise ValueError("File is not an Aegis Q-table.")
        if payload.get("state_features") != list(STATE_FEATURES):
            raise ValueError("Saved state features do not match this engine's state encoding.")
        if payload.get("actions") != [a.name for a in Action]:
            raise ValueError("Saved action list does not match the current Action enum.")

        agent = cls(config)
        agent.epsilon = float(payload["epsilon"])
        agent.metadata = payload.get("metadata") or {}

        for entry in payload["entries"]:
            key = tuple(entry["state_key"])
            if not is_valid_key(key):
                raise ValueError(f"Invalid state key in Q-table: {entry['state_key']!r}")
            values = {Action[name]: float(v) for name, v in entry["values"].items()}
            if set(values) != set(Action):
                raise ValueError(f"State {key} does not have a value for every action.")
            agent.q_table[key] = values
            visits = entry.get("visits") or {}
            agent.visits[key] = {a: int(visits.get(a.name, 0)) for a in Action}

        return agent


# ----------------------------------------------------------------------
# Student-facing explanation of each action (facts from the state only).
# ----------------------------------------------------------------------
def _engagement_note(state: StudentState) -> str:
    notes = []
    if state.drowsy:
        notes.append("possible drowsiness was observed")
    elif state.yawning:
        notes.append("yawning was observed")
    if state.looking_away:
        notes.append("you looked away from the screen for a while")
    return " and ".join(notes)


def _action_sentence(state: StudentState, action: Action) -> str:
    score = state.current_quiz_score
    level = state.difficulty.name
    engagement = _engagement_note(state)
    builders: dict[Action, Callable[[], str]] = {
        Action.NEXT_LESSON: lambda: f"You scored {score}% at {level} difficulty, so moving on to the next lesson is suggested.",
        Action.REPEAT_LESSON: lambda: f"You scored {score}% at {level} difficulty; studying the lesson again should strengthen the basics.",
        Action.INCREASE_DIFFICULTY: lambda: f"You scored {score}% at {level} difficulty, so a harder quiz is suggested.",
        Action.DECREASE_DIFFICULTY: lambda: f"You scored {score}% at {level} difficulty; an easier quiz should help you rebuild confidence.",
        Action.PRACTICE_QUIZ: lambda: f"You scored {score}% at {level} difficulty; another practice attempt should consolidate what you learned.",
        Action.QUICK_CHALLENGE: lambda: f"You scored {score}% at {level} difficulty; a short challenge is suggested to keep things engaging.",
        Action.SHOW_WORKED_EXAMPLE: lambda: f"You scored {score}% after {state.lesson_attempts} attempt(s); working through solved examples should help.",
        Action.PROVIDE_HINT: lambda: f"You scored {score}% at {level} difficulty; retrying with hints should help you close the gap.",
        Action.FOCUS_RECOVERY: lambda: (
            f"You scored {score}%"
            + (f", and {engagement}" if engagement else f" with attention at {state.attention_score:.0%}")
            + "; a short focus-recovery break is suggested before continuing."
        ),
        Action.SHOW_REAL_WORLD_APPLICATION: lambda: f"You scored {score}% with attention at {state.attention_score:.0%}; seeing how this topic is used in real life may help it stick.",
        Action.SKIP_TO_ADVANCED_TOPIC: lambda: f"You scored {score}% at {level} difficulty, so you can skip ahead to more advanced material.",
    }
    return builders[action]()


_missing = set(Action) - set(ACTION_LABELS)
if _missing:  # pragma: no cover - guards future enum additions
    raise ValueError(f"Missing labels for: {_missing}")
