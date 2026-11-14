"""Phase 4: audit columns for Q-learning decisions and observed rewards.

Additive only (all new columns are nullable):

* ``recommendation_history.model_version`` -- which Q-table produced it;
* ``recommendation_history.decision_detail`` -- JSON: Q-values of the
  eligible actions, blocked actions and reasons, margin, visit counts;
* ``reward_history.reward_version`` -- reward formula version (existing
  rows were computed with the Phase 2 formula and are marked 1);
* ``reward_history.followed`` -- whether the next attempt shows the
  student followed the recommendation (NULL when not observable);
* ``reward_history.reward_detail`` -- JSON breakdown of the reward.

Revision ID: 0005_rl_decision_audit
Revises: 0004_monitoring_sessions
Create Date: 2026-11-12
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0005_rl_decision_audit"
down_revision: Union[str, None] = "0004_monitoring_sessions"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("recommendation_history") as batch:
        batch.add_column(sa.Column("model_version", sa.String(length=64), nullable=True))
        batch.add_column(sa.Column("decision_detail", sa.Text(), nullable=True))

    with op.batch_alter_table("reward_history") as batch:
        batch.add_column(sa.Column("reward_version", sa.Integer(), nullable=True))
        batch.add_column(sa.Column("followed", sa.Boolean(), nullable=True))
        batch.add_column(sa.Column("reward_detail", sa.Text(), nullable=True))

    op.execute("UPDATE reward_history SET reward_version = 1 WHERE reward_version IS NULL")


def downgrade() -> None:
    with op.batch_alter_table("reward_history") as batch:
        batch.drop_column("reward_detail")
        batch.drop_column("followed")
        batch.drop_column("reward_version")

    with op.batch_alter_table("recommendation_history") as batch:
        batch.drop_column("decision_detail")
        batch.drop_column("model_version")
