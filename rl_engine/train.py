"""Offline training entry point for the tabular Q-learning RL engine.

Running this module trains a ``QLearningAgent`` via ``Trainer`` on the
configuration in ``RLConfig``, persists the learned Q-table to disk, and
prints a summary of the completed run. It contains no API, web,
database, or frontend code, and no training, reward, or environment
logic of its own -- all of that is delegated to ``Trainer`` and
``QLearningAgent``. This module only orchestrates: build config, train,
save, report.

Usage:
    python -m rl_engine.train
"""

import sys
from pathlib import Path
from typing import Final

from .core.config import RLConfig
from .training.trainer import Trainer

Q_TABLE_FILENAME: Final[str] = "q_table.json"
Q_TABLE_PATH: Final[Path] = Path(__file__).resolve().parent / Q_TABLE_FILENAME

BANNER_TITLE: Final[str] = "EduAdapt Reinforcement Learning Training"
BANNER_RULE: Final[str] = "=" * len(BANNER_TITLE)
SUMMARY_LABEL_WIDTH: Final[int] = 19


def _row(label: str, value: str) -> str:
    """Format a single aligned "label: value" line for the summary.

    Args:
        label: The field name to display.
        value: The already-formatted field value to display.

    Returns:
        A single line with the label left-padded to a fixed width.
    """
    return f"{label:<{SUMMARY_LABEL_WIDTH}}: {value}"


def _print_summary(trainer: Trainer, q_table_path: Path) -> None:
    """Print a concise, human-readable summary of a completed training run.

    Args:
        trainer: The ``Trainer`` that has just finished ``train()``,
            used to read ``episode_rewards``, ``average_reward``, and
            ``epsilon_history`` for reporting.
        q_table_path: The filesystem path the Q-table was saved to.
    """
    episodes_run = len(trainer.episode_rewards)
    final_epsilon = trainer.epsilon_history[-1] if trainer.epsilon_history else 0.0

    print(BANNER_RULE)
    print(BANNER_TITLE)
    print(BANNER_RULE)
    print()
    print("Training completed successfully.")
    print()
    print(_row("Episodes", str(episodes_run)))
    print(_row("Average Reward", f"{trainer.average_reward:.2f}"))
    print(_row("Final Epsilon", f"{final_epsilon:.2f}"))
    print()
    print("Q-table saved to:")
    print(str(q_table_path))


def main() -> None:
    """Train the Q-learning agent once and persist its learned Q-table.

    Builds an ``RLConfig``, runs a full training pass through
    ``Trainer.train()``, saves the resulting agent's Q-table to
    ``rl_engine/q_table.json``, and prints a training summary. Exits
    the process with a non-zero status and a descriptive message if
    initialization, training, or saving fails, distinguishing which
    stage failed.
    """
    try:
        config = RLConfig()
        trainer = Trainer(config)
    except Exception as error:
        print(f"Failed to initialize training: {error}", file=sys.stderr)
        sys.exit(1)

    try:
        agent = trainer.train()
    except Exception as error:
        print(f"Training failed: {error}", file=sys.stderr)
        sys.exit(1)

    try:
        agent.save_q_table(Q_TABLE_PATH)
    except Exception as error:
        print(f"Failed to save Q-table: {error}", file=sys.stderr)
        sys.exit(1)

    _print_summary(trainer, Q_TABLE_PATH)


if __name__ == "__main__":
    main()