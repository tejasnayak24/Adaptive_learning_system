"""Configuration for the Reinforcement Learning Engine.

This module centralizes the hyperparameters used by the Q-learning agent
during training. Keeping these values in a single, frozen configuration
object allows training behavior to be tuned without touching the RL
algorithm's implementation.

In addition to the core Q-learning hyperparameters, this module also
holds the state-discretization thresholds used to convert a student's
continuous signals (quiz score, attention score) and unbounded counters
(hints used, lesson attempts) into the small, finite set of buckets the
tabular ``QLearningAgent`` needs for its Q-table keys. Keeping these
thresholds here, rather than as constants inside the agent, means the
discretization scheme can be tuned the same way as any other
hyperparameter, without touching the agent's algorithmic code.

This file defines only the configuration data itself. It has no
dependency on FastAPI, Flask, PostgreSQL, any database, or any frontend
or UI code, and contains no training logic or RL algorithm code.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class RLConfig:
    """Hyperparameters controlling the Q-learning agent's training.

    Instances are immutable (``frozen=True``) so that a configuration
    cannot be accidentally mutated once it has been used to start a
    training run, keeping training runs reproducible. This class is
    intended to be imported and reused by both ``trainer.py`` and
    ``agent.py``.

    Beyond the core learning hyperparameters, ``RLConfig`` also carries
    the thresholds ``QLearningAgent`` uses to discretize a
    ``StudentState`` into a Q-table key: a quiz score and an attention
    score are each split into low/medium/high buckets by a pair of
    thresholds, while hint and attempt counts are each collapsed into a
    "many or not" boolean by a single threshold. Centralizing these here
    means the agent's discretization behavior is configuration-driven
    rather than hardcoded, and can be tuned without editing
    ``agent.py``.

    Attributes:
        learning_rate: The step size used when updating Q-values, in the
            range [0.0, 1.0]. Higher values make the agent adopt new
            information more aggressively; lower values make learning
            more gradual and stable.
        discount_factor: The weight given to future rewards relative to
            immediate rewards, in the range [0.0, 1.0]. Values closer to
            1.0 make the agent favor long-term outcomes over immediate
            ones.
        epsilon: The initial probability of taking a random (exploratory)
            action rather than the agent's current best-known action, in
            the range [0.0, 1.0].
        epsilon_decay: The multiplicative factor applied to ``epsilon``
            after each episode, in the range [0.0, 1.0], gradually
            shifting the agent from exploration toward exploitation.
        min_epsilon: The lower bound below which ``epsilon`` will not
            decay further, in the range [0.0, 1.0], ensuring the agent
            always retains some minimal exploration.
        training_episodes: The total number of episodes to run during
            training. Must be greater than 0.
        max_steps_per_episode: The maximum number of steps allowed within
            a single training episode before it is terminated. Must be
            greater than 0.
        score_low_threshold: The quiz score (on a 0-100 scale) below
            which a student's current quiz score is discretized into the
            "low" bucket of the Q-table state key. Must be greater than
            or equal to 0, and less than ``score_high_threshold``.
        score_high_threshold: The quiz score at or above which a
            student's current quiz score is discretized into the "high"
            bucket; scores in between fall into the "medium" bucket.
            Must be less than or equal to 100, and greater than
            ``score_low_threshold``.
        attention_low_threshold: The attention score (in [0.0, 1.0])
            below which a student's attention score is discretized into
            the "low" bucket of the Q-table state key. Must be greater
            than or equal to 0.0, and less than
            ``attention_high_threshold``.
        attention_high_threshold: The attention score at or above which a
            student's attention score is discretized into the "high"
            bucket; scores in between fall into the "medium" bucket.
            Must be less than or equal to 1.0, and greater than
            ``attention_low_threshold``.
        many_hints_threshold: The number of hints used at or above which
            a student is discretized as having used "many" hints, rather
            than "few", in the Q-table state key. Must be greater than
            0.
        many_attempts_threshold: The number of lesson attempts at or
            above which a student is discretized as having made "many"
            attempts, rather than "few", in the Q-table state key. Must
            be greater than 0.
    """

    learning_rate: float = 0.1
    discount_factor: float = 0.9
    epsilon: float = 1.0
    epsilon_decay: float = 0.995
    min_epsilon: float = 0.01
    training_episodes: int = 1000
    max_steps_per_episode: int = 100
    score_low_threshold: int = 50
    score_high_threshold: int = 80
    attention_low_threshold: float = 0.4
    attention_high_threshold: float = 0.6
    many_hints_threshold: int = 2
    many_attempts_threshold: int = 3

    def __post_init__(self) -> None:
        """Validate that all hyperparameters hold sensible values.

        Beyond the original hyperparameter checks, this also validates
        the state-discretization thresholds: each low/high threshold
        pair (score, attention) must stay within its natural range and
        keep its low bound strictly below its high bound, since a
        reversed or overlapping pair would make the "medium" bucket
        ill-defined or unreachable. The two "many" thresholds must be
        positive, since a zero or negative count threshold would make
        every student register as having used "many" hints or attempts.

        Raises:
            ValueError: If any hyperparameter falls outside its valid
                range, if ``min_epsilon`` is greater than ``epsilon``, if
                ``score_low_threshold`` or ``score_high_threshold`` falls
                outside [0, 100] or is out of order, if
                ``attention_low_threshold`` or
                ``attention_high_threshold`` falls outside [0.0, 1.0] or
                is out of order, or if ``many_hints_threshold`` or
                ``many_attempts_threshold`` is not greater than 0.
        """
        if not 0.0 <= self.learning_rate <= 1.0:
            raise ValueError("learning_rate must be between 0.0 and 1.0.")
        if not 0.0 <= self.discount_factor <= 1.0:
            raise ValueError("discount_factor must be between 0.0 and 1.0.")
        if not 0.0 <= self.epsilon <= 1.0:
            raise ValueError("epsilon must be between 0.0 and 1.0.")
        if not 0.0 <= self.epsilon_decay <= 1.0:
            raise ValueError("epsilon_decay must be between 0.0 and 1.0.")
        if not 0.0 <= self.min_epsilon <= 1.0:
            raise ValueError("min_epsilon must be between 0.0 and 1.0.")
        if self.training_episodes <= 0:
            raise ValueError("training_episodes must be greater than 0.")
        if self.max_steps_per_episode <= 0:
            raise ValueError("max_steps_per_episode must be greater than 0.")
        if self.min_epsilon > self.epsilon:
            raise ValueError("min_epsilon cannot be greater than epsilon.")
        if not 0 <= self.score_low_threshold <= 100:
            raise ValueError("score_low_threshold must be between 0 and 100.")
        if not 0 <= self.score_high_threshold <= 100:
            raise ValueError("score_high_threshold must be between 0 and 100.")
        if self.score_low_threshold >= self.score_high_threshold:
            raise ValueError("score_low_threshold must be less than score_high_threshold.")
        if not 0.0 <= self.attention_low_threshold <= 1.0:
            raise ValueError("attention_low_threshold must be between 0.0 and 1.0.")
        if not 0.0 <= self.attention_high_threshold <= 1.0:
            raise ValueError("attention_high_threshold must be between 0.0 and 1.0.")
        if self.attention_low_threshold >= self.attention_high_threshold:
            raise ValueError(
                "attention_low_threshold must be less than attention_high_threshold."
            )
        if self.many_hints_threshold <= 0:
            raise ValueError("many_hints_threshold must be greater than 0.")
        if self.many_attempts_threshold <= 0:
            raise ValueError("many_attempts_threshold must be greater than 0.")