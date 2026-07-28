"""Training orchestration for the Reinforcement Learning Engine.

This module is responsible only for orchestrating the tabular Q-learning
training process: constructing the environment and agent, running
training episodes, and collecting basic monitoring metrics along the
way. It contains no reward logic (that lives in ``rewards.py``, used
internally by ``LearningEnvironment``), no environment transition logic
(that lives in ``environment.py``), and no recommendation logic (that
lives in ``agent.py``'s ``recommend`` method). It has no dependency on
FastAPI, any database, any API framework, or any frontend or UI code.
"""

from ..core.config import RLConfig
from .agent import QLearningAgent
from .environment import LearningEnvironment
from .simulation import create_initial_state


class Trainer:
    """Orchestrates tabular Q-learning training for the RL engine.

    A ``Trainer`` owns one ``LearningEnvironment`` and one
    ``QLearningAgent`` for the lifetime of a training run, and drives
    the standard Q-learning training loop: for each episode, reset the
    environment to a fresh starting state, repeatedly let the agent
    choose an action and observe the resulting transition, update the
    agent's Q-table from that transition, and decay the agent's
    exploration rate once the episode ends. It has no opinion on how the
    environment computes rewards, how the agent selects actions or
    computes Q-values, or how a simulated student's starting state is
    constructed -- those behaviors are entirely encapsulated in
    ``LearningEnvironment``, ``QLearningAgent``, and
    ``training.simulation`` respectively, and ``Trainer`` only
    coordinates calls between them.

    Attributes:
        config: The ``RLConfig`` supplied at construction, governing the
            number of training episodes, the per-episode step limit, and
            (indirectly, via the agent) all Q-learning hyperparameters.
        episode_rewards: The total reward accumulated in each completed
            training episode, in the order the episodes ran. Intended
            for monitoring only.
        epsilon_history: The agent's exploration rate (``epsilon``)
            recorded immediately after each episode's decay step, in the
            order the episodes ran. Intended for monitoring only.
        average_reward: The mean of ``episode_rewards`` so far, updated
            after every completed episode. ``0.0`` before any episode
            has completed. Intended for monitoring only.
    """

    def __init__(self, config: RLConfig) -> None:
        """Initialize the trainer, and the agent and environment it drives.

        Args:
            config: The training configuration. Used directly to build
                the ``QLearningAgent`` and to control how many episodes
                ``train`` runs and how many steps each episode may take.

        Raises:
            TypeError: If ``config`` is not an instance of ``RLConfig``.
            ValueError: If ``config.training_episodes`` is not positive,
                or if ``config.max_steps_per_episode`` is not positive.
        """
        if not isinstance(config, RLConfig):
            raise TypeError("config must be an instance of RLConfig.")

        if config.training_episodes <= 0:
            raise ValueError(
                "config.training_episodes must be greater than 0, got "
                f"{config.training_episodes!r}."
            )

        if config.max_steps_per_episode <= 0:
            raise ValueError(
                "config.max_steps_per_episode must be greater than 0, got "
                f"{config.max_steps_per_episode!r}."
            )

        self.config = config
        self._agent = QLearningAgent(config)
        self._environment = LearningEnvironment(create_initial_state())

        self.episode_rewards: list[float] = []
        self.epsilon_history: list[float] = []
        self.average_reward: float = 0.0
        self._total_reward: float = 0.0

    def train(self) -> QLearningAgent:
        """Run the full training process and return the trained agent.

        Executes ``config.training_episodes`` episodes, each capped at
        ``config.max_steps_per_episode`` steps, updating the agent's
        Q-table after every step and decaying its exploration rate at
        the end of every episode. Monitoring metrics are accumulated on
        ``self`` as training proceeds.

        Returns:
            The same ``QLearningAgent`` instance this trainer has been
            updating throughout training, now reflecting everything it
            learned over all episodes.
        """
        for _ in range(self.config.training_episodes):
            episode_reward = self._run_episode()
            self._record_episode(episode_reward)

        return self._agent

    def _run_episode(self) -> float:
        """Run a single training episode to completion or the step limit.

        Resets the environment to a fresh starting state (built by
        ``training.simulation.create_initial_state``), then repeatedly
        lets the agent choose an action, applies it to the environment,
        and updates the agent's Q-table from the observed transition,
        until the environment reports the episode is done or
        ``config.max_steps_per_episode`` steps have been taken.

        Returns:
            The sum of the rewards received over every step of the
            episode.
        """
        state = self._environment.reset(create_initial_state())
        total_reward = 0.0
        done = False
        steps_taken = 0

        while not done and steps_taken < self.config.max_steps_per_episode:
            action = self._agent.choose_action(state)
            next_state, reward, done = self._environment.step(action)
            self._agent.update(state, action, reward, next_state, done)

            state = next_state
            total_reward += reward
            steps_taken += 1

        return total_reward

    def _record_episode(self, episode_reward: float) -> None:
        """Update monitoring metrics and decay epsilon after an episode.

        Maintains ``_total_reward`` as a running sum so that
        ``average_reward`` can be recomputed in constant time each
        episode, rather than re-summing all of ``episode_rewards`` every
        time.

        Args:
            episode_reward: The total reward accumulated over the
                episode that just finished.

        Raises:
            TypeError: If ``episode_reward`` is not a real number.
        """
        if not isinstance(episode_reward, (int, float)):
            raise TypeError("episode_reward must be a real number.")

        self._agent.decay_epsilon()

        self.episode_rewards.append(episode_reward)
        self.epsilon_history.append(self._agent.epsilon)

        self._total_reward += episode_reward
        self.average_reward = self._total_reward / len(self.episode_rewards)