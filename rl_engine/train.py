"""Offline training entry point for the Aegis Q-learning engine.

Usage (from the project root)::

    python -m rl_engine.train                 # default: 20000 episodes, seed 2026
    python -m rl_engine.train --episodes 5000 --seed 1 --output some.json

Steps:

1. Train a fresh ``QLearningAgent`` on simulated students (``Trainer``).
2. Save it to ``q_table.candidate.json`` next to the live table.
3. Validate the candidate on 1000 held-out simulated students (a seed range
   never used in training) against the pre-Phase-4 rule policy and a
   random policy. The candidate must
   * achieve a higher mean return than the random policy,
   * achieve a mean return at least as high as the legacy rule policy,
   * never select an action blocked by the safety constraints, and
   * have learned at least 50% of the 1944 possible states.
4. Only if validation passes: copy the current live table to
   ``rl_engine/archive/q_table_<timestamp>.json`` and replace it with the
   candidate. On failure the live table is left untouched and the process
   exits with status 1.

Training is offline only. The running backend does not update the
Q-table; real outcomes are recorded in ``reward_history`` for evaluation.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Final

from .core.config import RLConfig
from .core.state_encoding import STATE_KEY_VERSION, STATE_SPACE_SIZE
from .evaluation.baselines import legacy_rule_policy, make_random_policy
from .evaluation.evaluate import evaluate_policy, greedy_policy
from .training.rewards import REWARD_VERSION
from .training.trainer import Trainer

ENGINE_DIR: Final[Path] = Path(__file__).resolve().parent
Q_TABLE_PATH: Final[Path] = ENGINE_DIR / "q_table.json"
ARCHIVE_DIR: Final[Path] = ENGINE_DIR / "archive"

DEFAULT_SEED: Final[int] = 2026
VALIDATION_SEED: Final[int] = 900_000  # disjoint from training seeds
VALIDATION_EPISODES: Final[int] = 1000
MIN_STATE_COVERAGE: Final[float] = 0.5


def validate(agent, episodes: int = VALIDATION_EPISODES) -> tuple[bool, dict]:
    import random

    learned = evaluate_policy("learned_q_table", greedy_policy(agent), episodes=episodes, seed=VALIDATION_SEED)
    legacy = evaluate_policy("legacy_rules", legacy_rule_policy, episodes=episodes, seed=VALIDATION_SEED)
    rand = evaluate_policy(
        "random_permitted", make_random_policy(random.Random(VALIDATION_SEED)), episodes=episodes, seed=VALIDATION_SEED
    )
    coverage = len(agent.q_table) / STATE_SPACE_SIZE

    checks = {
        "beats_random": learned.mean_return > rand.mean_return,
        "not_worse_than_legacy_rules": learned.mean_return >= legacy.mean_return,
        "no_constraint_violations": learned.constraint_violations == 0,
        "state_coverage_ok": coverage >= MIN_STATE_COVERAGE,
    }
    report = {
        "checks": checks,
        "state_coverage": round(coverage, 4),
        "policies": {r.name: r.as_dict() for r in (learned, legacy, rand)},
    }
    return all(checks.values()), report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Train the Aegis Q-learning agent offline.")
    parser.add_argument("--episodes", type=int, default=None)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--output", type=Path, default=Q_TABLE_PATH)
    parser.add_argument("--validation-episodes", type=int, default=VALIDATION_EPISODES)
    args = parser.parse_args(argv)

    config = RLConfig() if args.episodes is None else RLConfig(training_episodes=args.episodes)
    output: Path = args.output.resolve()
    candidate = output.with_name(output.stem + ".candidate.json")

    print(f"Training {config.training_episodes} episodes (seed {args.seed}) ...", flush=True)
    started = time.time()
    trainer = Trainer(config, seed=args.seed)
    agent = trainer.train()
    seconds = round(time.time() - started, 1)

    print(f"Validating on {args.validation_episodes} held-out simulated students ...", flush=True)
    passed, report = validate(agent, args.validation_episodes)

    last = trainer.episode_rewards[-1000:]
    metadata = {
        "trained_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "state_key_version": STATE_KEY_VERSION,
        "reward_version": REWARD_VERSION,
        "seed": args.seed,
        "training_seconds": seconds,
        "config": {
            k: getattr(config, k)
            for k in (
                "learning_rate",
                "discount_factor",
                "epsilon",
                "epsilon_decay",
                "min_epsilon",
                "training_episodes",
                "max_steps_per_episode",
            )
        },
        "final_epsilon": round(agent.epsilon, 4),
        "mean_reward_all_episodes": round(trainer.average_reward, 3),
        "mean_reward_last_1000": round(sum(last) / len(last), 3),
        "states_learned": len(agent.q_table),
        "validation": report,
    }
    agent.save_q_table(candidate, metadata)

    print(json.dumps({"checks": report["checks"], "state_coverage": report["state_coverage"]}, indent=2))
    for name, policy in report["policies"].items():
        print(
            f"  {name:18s} return {policy['mean_return']:8.2f}  lessons {policy['mean_lessons_completed']:5.2f}  "
            f"premature {policy['premature_advance_rate']:.1%}  drowsy-steps {policy['drowsy_step_rate']:.1%}"
        )

    if not passed:
        print(f"Validation FAILED. Live Q-table unchanged; candidate kept at {candidate}", file=sys.stderr)
        return 1

    if output.exists():
        ARCHIVE_DIR.mkdir(exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = ARCHIVE_DIR / f"{output.stem}_{stamp}.json"
        shutil.copy2(output, backup)
        print(f"Previous table backed up to {backup}")

    candidate.replace(output)
    print(f"Validation passed. Q-table written to {output} ({len(agent.q_table)} states, {seconds}s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
