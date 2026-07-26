"""Configuration for the Reinforcement Learning Engine.

This module centralizes the hyperparameters used by the Q-learning agent
during training. Keeping these values in a single, frozen configuration
object allows training behavior to be tuned without touching the RL
algorithm's implementation.

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
    """

    learning_rate: float = 0.1
    discount_factor: float = 0.9
    epsilon: float = 1.0
    epsilon_decay: float = 0.995
    min_epsilon: float = 0.01
    training_episodes: int = 1000
    max_steps_per_episode: int = 100

    def __post_init__(self) -> None:
        """Validate that all hyperparameters hold sensible values.

        Raises:
            ValueError: If any hyperparameter falls outside its valid
                range, or if ``min_epsilon`` is greater than ``epsilon``.
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