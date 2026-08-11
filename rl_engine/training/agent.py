"""Tabular Q-learning agent for the Reinforcement Learning Engine.

This module implements the core decision-making algorithm of the RL
engine: a tabular Q-learning agent that learns which learning action is
most appropriate for a given student state through repeated interaction
with a training environment.

The agent has no knowledge of databases, web frameworks, or frontend
code. It operates entirely on ``StudentState``, ``Action``, and
``Recommendation`` objects, and is driven externally by a training loop
(implemented separately in ``trainer.py``) that supplies states, chosen
actions, and observed rewards.
"""

import json
import math
import random
from collections.abc import Callable
from typing import Final

from ..core.actions import Action
from ..core.config import RLConfig
from ..models.recommendation import Recommendation
from ..models.student_state import StudentState

# The exact shape of a Q-table key, as produced by ``_state_to_key``:
# (quiz score bucket, attention bucket, difficulty level,
#  many hints used, many attempts made, yawning, looking away).
StateKey = tuple[int, int, int, bool, bool, bool, bool]

# All actions, cached once as a tuple rather than rebuilding a list from
# the ``Action`` enum on every exploration step.
_ALL_ACTIONS: Final[tuple[Action, ...]] = tuple(Action)

# Bumped whenever _state_to_key's shape or field order changes, so a
# saved Q-table produced by an incompatible encoding is rejected on load
# instead of silently producing wrong lookups.
STATE_KEY_VERSION: Final[int] = 1


class QLearningAgent:
    """A tabular Q-learning agent that recommends adaptive learning actions.

    The agent maintains a Q-table mapping discretized student states to a
    value for every possible ``Action``, and updates those values using
    the standard Q-learning (Bellman) update rule. It selects actions
    using an epsilon-greedy strategy, balancing exploration of untried
    actions against exploitation of the best-known action for a state.

    Attributes:
        config: The ``RLConfig`` this agent was constructed with. It
            holds every learning hyperparameter and discretization
            threshold (learning rate, discount factor, epsilon schedule,
            and the score/attention/hints/attempts bucket thresholds) as
            a single source of truth, rather than the agent copying each
            value into its own attributes.
        epsilon: The current probability of choosing a random action
            instead of the best-known action. Unlike the rest of
            ``config``, this is kept as a separate mutable attribute
            because, unlike the fixed hyperparameters, it is actually
            *changed* at runtime (by ``decay_epsilon``) over the course
            of training. ``config`` itself is treated as immutable
            configuration, so runtime state that evolves independently
            of it -- like the live exploration rate -- doesn't belong
            on it.
        q_table: A mapping from a discretized state key to a mapping from
            each ``Action`` to its learned Q-value.
    """

    def __init__(self, config: RLConfig) -> None:
        """Initialize the agent from a training configuration.

        Args:
            config: The hyperparameters governing this agent's learning
                rate, discount factor, exploration schedule, and
                state-discretization thresholds.

        Raises:
            TypeError: If ``config`` is not an instance of ``RLConfig``.
        """
        if not isinstance(config, RLConfig):
            raise TypeError("config must be an instance of RLConfig.")

        self.config = config
        self.epsilon: float = config.epsilon
        self.q_table: dict[StateKey, dict[Action, float]] = {}

    def choose_action(self, state: StudentState) -> Action:
        """Select an action for ``state`` using an epsilon-greedy policy.

        With probability ``epsilon``, a random action is chosen to
        encourage exploration. Otherwise, the action with the highest
        learned Q-value for this state is chosen, with ties among
        equally-valued actions broken uniformly at random so exploitation
        doesn't systematically favor whichever action happens to be
        declared first in the ``Action`` enum.

        Args:
            state: The student's current state.

        Returns:
            The action chosen by the epsilon-greedy policy.

        Raises:
            TypeError: If ``state`` is not an instance of ``StudentState``.
        """
        state_key = self._prepare_state_key(state)

        if random.random() < self.epsilon:
            return random.choice(_ALL_ACTIONS)

        return self._best_action(state_key, break_ties_randomly=True)

    def update(
        self,
        state: StudentState,
        action: Action,
        reward: float,
        next_state: StudentState,
        done: bool,
    ) -> None:
        """Update the Q-value for ``(state, action)`` using the observed outcome.

        Applies the Q-learning update rule:
        ``Q(s,a) <- Q(s,a) + learning_rate * (target - Q(s,a))``, where
        ``target`` is ``reward`` alone if the episode has ended, or
        ``reward + discount_factor * max(Q(s', a'))`` otherwise.

        Args:
            state: The state the action was taken in.
            action: The action that was taken.
            reward: The reward received for taking ``action`` in ``state``.
            next_state: The state the environment transitioned to.
            done: Whether the episode ended after this transition.

        Raises:
            TypeError: If ``state`` or ``next_state`` is not a
                ``StudentState``, if ``action`` is not an ``Action``, if
                ``reward`` is not a real number (``bool`` is rejected even
                though it is technically an ``int`` subtype), or if
                ``done`` is not a ``bool``.
        """
        if not isinstance(action, Action):
            raise TypeError("action must be an instance of Action.")
        if isinstance(reward, bool) or not isinstance(reward, (int, float)):
            raise TypeError("reward must be a real number.")
        if not isinstance(done, bool):
            raise TypeError("done must be a bool.")

        state_key = self._prepare_state_key(state)
        current_q = self.q_table[state_key][action]

        if done:
            # No future to bootstrap from, so the next state's Q-values
            # are never read here -- skip preparing/initializing
            # next_state_key entirely rather than populating Q-table
            # entries for a terminal state that will never be queried
            # again.
            target = float(reward)
        else:
            next_state_key = self._prepare_state_key(next_state, param_name="next_state")
            best_next_q = max(self.q_table[next_state_key].values())
            target = reward + self.config.discount_factor * best_next_q

        self.q_table[state_key][action] = current_q + self.config.learning_rate * (
            target - current_q
        )

    def decay_epsilon(self) -> None:
        """Decay the exploration rate after an episode.

        Multiplies ``epsilon`` by the configured decay factor, never
        letting it fall below the configured minimum, gradually shifting
        the agent from exploration toward exploitation over training.
        """
        self.epsilon = max(
            self.epsilon * self.config.epsilon_decay, self.config.min_epsilon
        )

    def recommend(self, state: StudentState) -> Recommendation:
        """Produce a recommendation for a student without exploration.

        Unlike ``choose_action``, this always selects the best-known
        action for the state (no random exploration), since it is meant
        to be called at inference time rather than during training. Ties
        among equally-valued actions are broken deterministically (by
        enum declaration order) rather than randomly, so the same state
        always yields the same recommendation.

        Args:
            state: The student's current state.

        Returns:
            A ``Recommendation`` containing the best-known action, a
            confidence score, and a human-readable explanation.

        Raises:
            TypeError: If ``state`` is not an instance of ``StudentState``.
        """
        state_key = self._prepare_state_key(state)

        best_action = self._best_action(state_key)
        confidence = self._compute_confidence(state_key, best_action)
        explanation = self._build_explanation(state, best_action)

        return Recommendation(action=best_action, confidence=confidence, explanation=explanation)

    def save_q_table(self, path: str) -> None:
        """Persist this agent's learned Q-table and epsilon to a JSON file.

        The state-key version is saved alongside the data so that
        ``load_q_table`` can detect and reject a file produced by an
        incompatible ``_state_to_key`` encoding, rather than silently
        loading Q-values under the wrong keys.

        Args:
            path: The filesystem path to write the JSON file to.
        """
        payload = {
            "state_key_version": STATE_KEY_VERSION,
            "epsilon": self.epsilon,
            "entries": [
                {
                    "state_key": list(state_key),
                    "values": {action.name: value for action, value in action_values.items()},
                }
                for state_key, action_values in self.q_table.items()
            ],
        }

        with open(path, "w", encoding="utf-8") as file:
            json.dump(payload, file)

    @classmethod
    def load_q_table(cls, path: str, config: RLConfig) -> "QLearningAgent":
        """Reconstruct a previously saved agent from a JSON file.

        Uses plain JSON (no ``pickle``) so loading a Q-table never
        executes arbitrary code, even if the file's origin isn't fully
        trusted.

        Args:
            path: The filesystem path to read the JSON file from.
            config: The configuration to construct the new agent with.
                Hyperparameters and thresholds come from this argument,
                not from the saved file, so a saved Q-table can be
                reloaded against a deliberately adjusted configuration.

        Returns:
            A new ``QLearningAgent`` with its Q-table and epsilon
            restored from ``path``.

        Raises:
            ValueError: If the file's ``state_key_version`` does not
                match the current ``STATE_KEY_VERSION``.
        """
        with open(path, encoding="utf-8") as file:
            payload = json.load(file)

        if payload["state_key_version"] != STATE_KEY_VERSION:
            raise ValueError(
                f"Saved state_key_version {payload['state_key_version']} does not "
                f"match current STATE_KEY_VERSION {STATE_KEY_VERSION}."
            )

        agent = cls(config)
        agent.epsilon = payload["epsilon"]

        for entry in payload["entries"]:
            state_key: StateKey = tuple(entry["state_key"])
            agent.q_table[state_key] = {
                Action[name]: value for name, value in entry["values"].items()
            }

        return agent

    def _prepare_state_key(self, state: StudentState, *, param_name: str = "state") -> StateKey:
        """Validate a state and return its initialized Q-table key.

        Consolidates the validate -> encode -> ensure-initialized
        sequence that every public method needs before touching the
        Q-table, so that sequence is defined in exactly one place.

        Args:
            state: The student state to validate and encode.
            param_name: The parameter name to use in the error message,
                so callers with more than one state argument (``update``'s
                ``state`` and ``next_state``) get an accurate message.

        Returns:
            The state's key, guaranteed to have a corresponding entry in
            ``q_table``.

        Raises:
            TypeError: If ``state`` is not an instance of ``StudentState``.
        """
        if not isinstance(state, StudentState):
            raise TypeError(f"{param_name} must be an instance of StudentState.")

        state_key = self._state_to_key(state)
        self._initialize_state(state_key)
        return state_key

    def _state_to_key(self, state: StudentState) -> StateKey:
        """Convert a ``StudentState`` into a hashable Q-table key.

        Continuous values (quiz score, attention) are discretized into
        low/medium/high buckets, and counts (hints used, lesson attempts)
        are collapsed into a small/large boolean, keeping the number of
        distinct states the agent must learn small enough for tabular
        Q-learning to converge in a practical number of episodes. With
        the fields currently used, the state space has an exact, fixed
        size of 3 (score) x 3 (attention) x 3 (difficulty) x 2 (hints)
        x 2 (attempts) x 2 (yawning) x 2 (looking away) = 432 distinct
        states, small enough for every state to be visited many times
        over a few thousand training episodes.

        ``subject``, ``topic``, and ``lesson`` are intentionally
        excluded. They are free-text curriculum identifiers with
        effectively unbounded cardinality: every distinct lesson in the
        curriculum would fragment the Q-table into its own disconnected
        copy of the entire 432-state space above, multiplying the total
        state count by the number of lessons in the system. Because none
        of ``RewardCalculator``'s rules depend on which subject, topic,
        or lesson is active, this would add pure noise -- more distinct
        states to independently discover via epsilon-greedy exploration,
        with no corresponding gain in learning signal -- and would
        prevent the agent from generalizing a learned pattern (e.g. "low
        attention with yawning warrants a focus recovery activity") from
        one lesson to another.

        ``completed_lessons`` is excluded for the same reason: it is a
        monotonically increasing progress counter with roughly one value
        per lesson in the curriculum, and no reward rule currently
        depends on it, so including it would multiply the state space by
        the curriculum length without improving the policy the agent
        learns.

        Should curriculum-aware personalization become a real
        requirement later (e.g. a subject that genuinely warrants a
        different policy), the cleaner extension is composing multiple
        ``QLearningAgent`` instances -- one per subject -- rather than
        expanding this key, since that keeps each individual Q-table
        small and keeps this class's responsibility unchanged.

        Args:
            state: The student state to convert.

        Returns:
            A hashable tuple summarizing the state for the Q-table.
        """
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
        """Discretize a quiz score into a low/medium/high bucket.

        Args:
            score: The quiz score to bucket, on a 0-100 scale.

        Returns:
            ``0`` for a low score, ``1`` for a medium score, or ``2``
            for a high score.
        """
        if score < self.config.score_low_threshold:
            return 0
        if score < self.config.score_high_threshold:
            return 1
        return 2

    def _bucket_attention(self, attention: float) -> int:
        """Discretize an attention score into a low/medium/high bucket.

        Args:
            attention: The attention score to bucket, in [0.0, 1.0].

        Returns:
            ``0`` for low attention, ``1`` for medium attention, or ``2``
            for high attention.
        """
        if attention < self.config.attention_low_threshold:
            return 0
        if attention < self.config.attention_high_threshold:
            return 1
        return 2

    def _initialize_state(self, state_key: StateKey) -> None:
        """Ensure ``state_key`` has an entry in the Q-table.

        Unseen states are populated with a Q-value of ``0.0`` for every
        possible action, representing "no information yet" rather than
        any particular preference.

        Args:
            state_key: The Q-table key to ensure is initialized.
        """
        if state_key not in self.q_table:
            self.q_table[state_key] = {action: 0.0 for action in Action}

    def _best_action(self, state_key: StateKey, *, break_ties_randomly: bool = False) -> Action:
        """Return the highest-value action for a given state key.

        Args:
            state_key: The Q-table key to look up.
            break_ties_randomly: If True, ties among equally-valued
                actions are broken uniformly at random, avoiding a
                systematic bias toward whichever action happens to be
                declared first in the ``Action`` enum -- important
                during training, where many states start with all
                Q-values equal at ``0.0``. If False (the default), ties
                are broken deterministically by enum declaration order
                (``max`` scans actions in iteration order and only
                replaces its current pick on a strictly greater
                Q-value), so the same state always yields the same
                recommendation.

        Returns:
            The action with the highest learned Q-value for this state.
        """
        q_values = self.q_table[state_key]

        if not break_ties_randomly:
            return max(Action, key=lambda action: q_values[action])

        best_value = max(q_values.values())
        tied_actions = [action for action in Action if q_values[action] == best_value]
        return random.choice(tied_actions)

    def _compute_confidence(self, state_key: StateKey, best_action: Action) -> float:
        """Compute a confidence score for the best action at a state.

        The confidence is the softmax probability of ``best_action``
        among all actions' Q-values for this state. This naturally
        yields low confidence for a freshly initialized state (all
        Q-values equal, so the softmax is close to uniform) and rises as
        the agent learns a stronger preference for one action over the
        others.

        Args:
            state_key: The Q-table key to compute confidence for.
            best_action: The action to compute the confidence of.

        Returns:
            A confidence value in the range (0.0, 1.0].
        """
        q_values = self.q_table[state_key]
        max_value = max(q_values.values())
        exponentials = {action: math.exp(value - max_value) for action, value in q_values.items()}
        total = sum(exponentials.values())
        return exponentials[best_action] / total

    def _build_explanation(self, state: StudentState, action: Action) -> str:
        """Generate a human-readable explanation for a recommended action.

        Dispatches to a per-action explanation builder via
        ``_EXPLANATION_BUILDERS``, keeping the mapping from action to
        wording in one place and making it a one-line change to support
        a newly added ``Action`` in the future.

        Args:
            state: The student state the recommendation was based on.
            action: The action being explained.

        Returns:
            A short explanation referencing the relevant state values
            that motivated the recommendation.

        Raises:
            ValueError: If ``action`` is not a recognized ``Action``.
        """
        builder = _EXPLANATION_BUILDERS.get(action)
        if builder is None:
            raise ValueError(f"Unrecognized action: {action}")
        return builder(state)


# Maps each Action to a function that renders a human-readable
# explanation from a StudentState. Defined at module level, rather than
# inline in _build_explanation, since the mapping depends only on the
# student state (not on the agent instance) and only needs to be built
# once.
_EXPLANATION_BUILDERS: dict[Action, Callable[[StudentState], str]] = {
    Action.NEXT_LESSON: lambda state: (
        f"Attention is high ({state.attention_score:.2f}) and the quiz "
        f"score ({state.current_quiz_score}) is solid; recommending the "
        "next lesson."
    ),
    Action.REPEAT_LESSON: lambda state: (
        f"Quiz score is low ({state.current_quiz_score}) after "
        f"{state.lesson_attempts} attempt(s); recommending the lesson be "
        "repeated."
    ),
    Action.INCREASE_DIFFICULTY: lambda state: (
        f"Quiz score ({state.current_quiz_score}) and attention "
        f"({state.attention_score:.2f}) are both high; recommending "
        "increased difficulty."
    ),
    Action.DECREASE_DIFFICULTY: lambda state: (
        f"Quiz score is {state.current_quiz_score} with attention at "
        f"{state.attention_score:.2f}; recommending decreased difficulty."
    ),
    Action.PRACTICE_QUIZ: lambda state: (
        f"Current quiz score ({state.current_quiz_score}) trails the "
        f"previous score ({state.previous_quiz_score}); recommending "
        "additional practice."
    ),
    Action.QUICK_CHALLENGE: lambda state: (
        f"Student is attentive ({state.attention_score:.2f}) and scoring "
        f"well ({state.current_quiz_score}); recommending a quick "
        "challenge."
    ),
    Action.SHOW_WORKED_EXAMPLE: lambda state: (
        f"Student has used {state.hints_used} hint(s) across "
        f"{state.lesson_attempts} attempt(s); recommending a fully "
        "worked example."
    ),
    Action.PROVIDE_HINT: lambda state: (
        f"Quiz score is {state.current_quiz_score} with only "
        f"{state.hints_used} hint(s) used so far; recommending a "
        "targeted hint."
    ),
    Action.FOCUS_RECOVERY: lambda state: (
        f"Attention score is {state.attention_score:.2f}, indicating "
        "fatigue or distraction; recommending a focus recovery activity."
    ),
    Action.SHOW_REAL_WORLD_APPLICATION: lambda state: (
        f"Attention is moderate ({state.attention_score:.2f}) while "
        "performance remains acceptable; recommending a real-world "
        "application to rebuild motivation."
    ),
    Action.SKIP_TO_ADVANCED_TOPIC: lambda state: (
        f"Quiz scores are consistently high (previous "
        f"{state.previous_quiz_score}, current {state.current_quiz_score}) "
        f"with strong attention ({state.attention_score:.2f}); "
        "recommending a skip to advanced material."
    ),
}

# Fail fast at import time if a new Action is ever added without a
# matching explanation, rather than discovering the gap only at runtime
# when recommend() happens to select that specific action.
_missing_explanations = set(Action) - _EXPLANATION_BUILDERS.keys()
if _missing_explanations:
    raise ValueError(f"_EXPLANATION_BUILDERS is missing entries for: {_missing_explanations}")