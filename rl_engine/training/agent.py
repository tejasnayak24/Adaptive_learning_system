"""Tabular Q-learning agent for the EduAdapt Reinforcement Learning Engine."""

import json
import math
import random
from collections.abc import Callable
from typing import Final

from ..core.actions import Action
from ..core.config import RLConfig
from ..models.recommendation import Recommendation
from ..models.student_state import Difficulty, StudentState


StateKey = tuple[int, int, int, bool, bool, bool, bool]

_ALL_ACTIONS: Final[tuple[Action, ...]] = tuple(Action)

STATE_KEY_VERSION: Final[int] = 2

REPEAT_SCORE_THRESHOLD: Final[int] = 70
PRACTICE_SCORE_THRESHOLD: Final[int] = 80
HIGH_SCORE_THRESHOLD: Final[int] = 80

LOW_ATTENTION_THRESHOLD: Final[float] = 0.40
MEDIUM_ATTENTION_THRESHOLD: Final[float] = 0.60


class QLearningAgent:
    """Tabular Q-learning agent with educational policy constraints."""

    def __init__(self, config: RLConfig) -> None:
        if not isinstance(config, RLConfig):
            raise TypeError("config must be an instance of RLConfig.")

        self.config = config
        self.epsilon: float = config.epsilon
        self.q_table: dict[StateKey, dict[Action, float]] = {}

    def choose_action(self, state: StudentState) -> Action:
        """Choose an action during training using epsilon-greedy exploration."""

        state_key = self._prepare_state_key(state)

        if random.random() < self.epsilon:
            return random.choice(_ALL_ACTIONS)

        return self._best_action(
            state_key,
            break_ties_randomly=True,
        )

    def update(
        self,
        state: StudentState,
        action: Action,
        reward: float,
        next_state: StudentState,
        done: bool,
    ) -> None:
        """Update Q-value using the standard Q-learning update."""

        if not isinstance(action, Action):
            raise TypeError("action must be an instance of Action.")

        if isinstance(reward, bool) or not isinstance(reward, (int, float)):
            raise TypeError("reward must be a real number.")

        if not isinstance(done, bool):
            raise TypeError("done must be a bool.")

        state_key = self._prepare_state_key(state)
        current_q = self.q_table[state_key][action]

        if done:
            target = float(reward)
        else:
            next_state_key = self._prepare_state_key(
                next_state,
                param_name="next_state",
            )
            best_next_q = max(self.q_table[next_state_key].values())
            target = (
                reward
                + self.config.discount_factor * best_next_q
            )

        self.q_table[state_key][action] = (
            current_q
            + self.config.learning_rate * (target - current_q)
        )

    def decay_epsilon(self) -> None:
        """Decay exploration rate after an episode."""

        self.epsilon = max(
            self.epsilon * self.config.epsilon_decay,
            self.config.min_epsilon,
        )

    def recommend(self, state: StudentState) -> Recommendation:
        """
        Produce a recommendation for a student.

        Educational policy rules are applied first to prevent the learned
        Q-table from producing logically invalid recommendations.

        The Q-table is still used for situations where multiple actions
        are educationally appropriate.
        """

        state_key = self._prepare_state_key(state)

        policy_action = self._policy_action(state)

        if policy_action is not None:
            best_action = policy_action
            confidence = 1.0
        else:
            best_action = self._best_action(state_key)
            confidence = self._compute_confidence(
                state_key,
                best_action,
            )

        explanation = self._build_explanation(
            state,
            best_action,
        )

        return Recommendation(
            action=best_action,
            confidence=confidence,
            explanation=explanation,
        )

    def save_q_table(self, path: str) -> None:
        """Persist Q-table and epsilon to JSON."""

        payload = {
            "state_key_version": STATE_KEY_VERSION,
            "epsilon": self.epsilon,
            "entries": [
                {
                    "state_key": list(state_key),
                    "values": {
                        action.name: value
                        for action, value in action_values.items()
                    },
                }
                for state_key, action_values in self.q_table.items()
            ],
        }

        with open(path, "w", encoding="utf-8") as file:
            json.dump(payload, file)

    @classmethod
    def load_q_table(
        cls,
        path: str,
        config: RLConfig,
    ) -> "QLearningAgent":
        """Load a previously saved Q-table."""

        with open(path, encoding="utf-8") as file:
            payload = json.load(file)

        saved_version = payload.get("state_key_version", 1)

        if saved_version != STATE_KEY_VERSION:
            raise ValueError(
                f"Saved state_key_version {saved_version} does not "
                f"match current STATE_KEY_VERSION {STATE_KEY_VERSION}."
            )

        agent = cls(config)
        agent.epsilon = payload["epsilon"]

        for entry in payload["entries"]:
            state_key: StateKey = tuple(entry["state_key"])

            agent.q_table[state_key] = {
                Action[name]: value
                for name, value in entry["values"].items()
            }

        return agent

    def _prepare_state_key(
        self,
        state: StudentState,
        *,
        param_name: str = "state",
    ) -> StateKey:
        """Validate and initialize a state key."""

        if not isinstance(state, StudentState):
            raise TypeError(
                f"{param_name} must be an instance of StudentState."
            )

        state_key = self._state_to_key(state)
        self._initialize_state(state_key)

        return state_key

    def _state_to_key(
        self,
        state: StudentState,
    ) -> StateKey:
        """Convert StudentState into a compact Q-learning state key."""

        return (
            self._bucket_score(state.current_quiz_score),
            self._bucket_attention(state.attention_score),
            state.difficulty.value,
            state.hints_used >= self.config.many_hints_threshold,
            state.lesson_attempts >= self.config.many_attempts_threshold,
            state.yawning,
            state.looking_away,
        )

    def _bucket_score(self, score: int) -> int:
        """Convert score into low, medium, or high bucket."""

        if score < self.config.score_low_threshold:
            return 0

        if score < self.config.score_high_threshold:
            return 1

        return 2

    def _bucket_attention(self, attention: float) -> int:
        """Convert attention into low, medium, or high bucket."""

        if attention < self.config.attention_low_threshold:
            return 0

        if attention < self.config.attention_high_threshold:
            return 1

        return 2

    def _initialize_state(
        self,
        state_key: StateKey,
    ) -> None:
        """Initialize an unseen Q-table state."""

        if state_key not in self.q_table:
            self.q_table[state_key] = {
                action: 0.0
                for action in Action
            }

    def _policy_action(
        self,
        state: StudentState,
    ) -> Action | None:
        """
        Apply deterministic educational rules.

        Returns None when the Q-learning policy should decide.
        """

        score = state.current_quiz_score
        attention = state.attention_score

        # ---------------------------------------------------------
        # 1. Very poor performance:
        #    Study/repeat the lesson before attempting more quizzes.
        # ---------------------------------------------------------

        if score < REPEAT_SCORE_THRESHOLD:
            return Action.REPEAT_LESSON

        # ---------------------------------------------------------
        # 2. Attention problems:
        #    Only use focus recovery when academic performance is
        #    already acceptable.
        # ---------------------------------------------------------

        if (
            attention < LOW_ATTENTION_THRESHOLD
            or state.yawning
            or state.looking_away
        ):
            if score >= REPEAT_SCORE_THRESHOLD:
                return Action.FOCUS_RECOVERY

        # ---------------------------------------------------------
        # 3. Medium performance:
        #    Practice the concept after studying it.
        # ---------------------------------------------------------

        if score < PRACTICE_SCORE_THRESHOLD:
            return Action.PRACTICE_QUIZ

        # ---------------------------------------------------------
        # 4. Excellent performance:
        #    Never decrease difficulty.
        # ---------------------------------------------------------

        if score >= HIGH_SCORE_THRESHOLD:

            if state.difficulty == Difficulty.EASY:
                return Action.INCREASE_DIFFICULTY

            if state.difficulty == Difficulty.MEDIUM:
                return Action.INCREASE_DIFFICULTY

            if state.difficulty == Difficulty.HARD:
                return Action.NEXT_LESSON

        return None

    def _best_action(
        self,
        state_key: StateKey,
        *,
        break_ties_randomly: bool = False,
    ) -> Action:
        """Return the highest-value learned action."""

        q_values = self.q_table[state_key]

        if not break_ties_randomly:
            return max(
                Action,
                key=lambda action: q_values[action],
            )

        best_value = max(q_values.values())

        tied_actions = [
            action
            for action in Action
            if q_values[action] == best_value
        ]

        return random.choice(tied_actions)

    def _compute_confidence(
        self,
        state_key: StateKey,
        best_action: Action,
    ) -> float:
        """Calculate softmax confidence from Q-values."""

        q_values = self.q_table[state_key]

        max_value = max(q_values.values())

        exponentials = {
            action: math.exp(value - max_value)
            for action, value in q_values.items()
        }

        total = sum(exponentials.values())

        return exponentials[best_action] / total

    def _build_explanation(
        self,
        state: StudentState,
        action: Action,
    ) -> str:
        """Build a human-readable recommendation explanation."""

        builder = _EXPLANATION_BUILDERS.get(action)

        if builder is None:
            raise ValueError(
                f"Unrecognized action: {action}"
            )

        return builder(state)


_EXPLANATION_BUILDERS: dict[
    Action,
    Callable[[StudentState], str],
] = {

    Action.NEXT_LESSON: lambda state: (
        f"Quiz score is strong at {state.current_quiz_score}% "
        f"with {state.attention_score:.2f} attention; "
        "recommending the next lesson."
    ),

    Action.REPEAT_LESSON: lambda state: (
        f"Quiz score is {state.current_quiz_score}%, "
        "so the student should study the lesson again "
        "before attempting more practice."
    ),

    Action.INCREASE_DIFFICULTY: lambda state: (
        f"Quiz score is {state.current_quiz_score}% with "
        f"attention at {state.attention_score:.2f}; "
        f"the current difficulty is {state.difficulty.name}. "
        "Recommending a higher difficulty level."
    ),

    Action.DECREASE_DIFFICULTY: lambda state: (
        f"Quiz score is {state.current_quiz_score}%; "
        "recommending lower difficulty to support learning."
    ),

    Action.PRACTICE_QUIZ: lambda state: (
        f"Quiz score is {state.current_quiz_score}%, "
        "so additional practice is recommended."
    ),

    Action.QUICK_CHALLENGE: lambda state: (
        f"Student is attentive at {state.attention_score:.2f} "
        f"and performing well with a score of "
        f"{state.current_quiz_score}%; recommending a quick challenge."
    ),

    Action.SHOW_WORKED_EXAMPLE: lambda state: (
        f"The student has used {state.hints_used} hint(s) "
        f"across {state.lesson_attempts} attempt(s); "
        "recommending a worked example."
    ),

    Action.PROVIDE_HINT: lambda state: (
        f"Quiz score is {state.current_quiz_score}% with "
        f"{state.hints_used} hint(s) used; recommending a targeted hint."
    ),

    Action.FOCUS_RECOVERY: lambda state: (
        f"Attention is {state.attention_score:.2f}"
        + (
            " and the student is yawning"
            if state.yawning
            else ""
        )
        + (
            " and looking away"
            if state.looking_away
            else ""
        )
        + "; recommending a short focus recovery activity."
    ),

    Action.SHOW_REAL_WORLD_APPLICATION: lambda state: (
        f"Attention is {state.attention_score:.2f} while "
        f"performance is acceptable at {state.current_quiz_score}%; "
        "recommending a real-world application."
    ),

    Action.SKIP_TO_ADVANCED_TOPIC: lambda state: (
        f"Quiz score is {state.current_quiz_score}% with "
        f"previous score {state.previous_quiz_score}% and strong "
        f"attention ({state.attention_score:.2f}); "
        "recommending advanced material."
    ),
}


_missing_explanations = (
    set(Action) - _EXPLANATION_BUILDERS.keys()
)

if _missing_explanations:
    raise ValueError(
        "Missing explanations for: "
        f"{_missing_explanations}"
    )