"""Summarise or export the observed outcomes of real recommendations.

This is evaluation, not online learning: nothing here changes the Q-table.
Each ``reward_history`` row pairs a stored recommendation with the
student's next attempt. Run from the project root:

    python backend/scripts/rl_outcome_report.py
    python backend/scripts/rl_outcome_report.py --export outcomes.jsonl

The export writes one JSON object per observed transition
(state, state_key, action, policy, model_version, reward, reward_version,
followed, reward components) without names or e-mail addresses, as input
for future offline analysis or retraining. Student ids are replaced by a
per-export pseudonym.
"""

import argparse
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
for path in (BACKEND_DIR, BACKEND_DIR.parent):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from app.database.connection import SessionLocal  # noqa: E402
import app.models  # noqa: E402,F401  (registers every model)
from app.models.recommendation import RecommendationHistory  # noqa: E402
from app.models.reward import RewardHistory  # noqa: E402


def _rows(db):
    return (
        db.query(RewardHistory, RecommendationHistory)
        .outerjoin(RecommendationHistory, RewardHistory.recommendation_id == RecommendationHistory.id)
        .order_by(RewardHistory.id)
        .all()
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--export", type=Path, help="write observed transitions as JSON lines")
    args = parser.parse_args()

    db = SessionLocal()
    try:
        rows = _rows(db)
        groups = defaultdict(list)
        for reward, rec in rows:
            policy = rec.policy if rec is not None else "unknown"
            groups[(reward.reward_version or 1, policy, reward.action)].append(reward)

        print(f"{len(rows)} observed outcome(s) in reward_history\n")
        print(f"{'reward v':>8}  {'policy':26} {'action':28} {'n':>4} {'mean reward':>12} {'followed':>9}")
        for (version, policy, action), items in sorted(groups.items()):
            mean = statistics.fmean(r.reward for r in items)
            known = [r.followed for r in items if r.followed is not None]
            followed = f"{sum(known)}/{len(known)}" if known else "n/a"
            print(f"{version:>8}  {policy:26} {action:28} {len(items):>4} {mean:>12.2f} {followed:>9}")
        print("\nRewards with different versions use different formulas; compare like with like.")

        if args.export:
            pseudonyms: dict[int, int] = {}
            with args.export.open("w", encoding="utf-8") as out:
                for reward, rec in rows:
                    out.write(
                        json.dumps(
                            {
                                "learner": pseudonyms.setdefault(reward.student_id, len(pseudonyms) + 1),
                                "action": reward.action,
                                "state_key": json.loads(reward.state) if reward.state else None,
                                "state": json.loads(rec.state) if rec is not None and rec.state else None,
                                "policy": rec.policy if rec is not None else None,
                                "model_version": rec.model_version if rec is not None else None,
                                "reward": reward.reward,
                                "reward_version": reward.reward_version,
                                "followed": reward.followed,
                                "reward_detail": json.loads(reward.reward_detail) if reward.reward_detail else None,
                            },
                            default=str,
                        )
                        + "\n"
                    )
            print(f"Exported {len(rows)} transition(s) to {args.export}")
    finally:
        db.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
