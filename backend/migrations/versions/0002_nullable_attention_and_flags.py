"""Phase 1: honest telemetry and canonical difficulty values.

* ``progress.attention_score`` becomes nullable: NULL means camera
  telemetry was unavailable for the attempt (never "zero attention").
* ``progress.yawning`` / ``progress.looking_away`` (nullable booleans)
  record whether they were observed during the attempt (NULL = unknown).
* Difficulty values in ``progress`` and ``quizzes`` are normalised to
  uppercase (EASY / MEDIUM / HARD). No rows are added or removed.

Revision ID: 0002_nullable_attention
Revises: 0001_baseline
Create Date: 2026-11-12
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0002_nullable_attention"
down_revision: Union[str, None] = "0001_baseline"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_DIFFICULTY_TABLES = ("progress", "quizzes")


def upgrade() -> None:
    with op.batch_alter_table("progress") as batch:
        batch.alter_column(
            "attention_score",
            existing_type=sa.Float(),
            nullable=True,
        )
        batch.add_column(sa.Column("yawning", sa.Boolean(), nullable=True))
        batch.add_column(sa.Column("looking_away", sa.Boolean(), nullable=True))

    for table in _DIFFICULTY_TABLES:
        op.execute(
            sa.text(
                f"UPDATE {table} SET difficulty = UPPER(TRIM(difficulty)) "
                "WHERE UPPER(TRIM(difficulty)) IN ('EASY', 'MEDIUM', 'HARD') "
                "AND difficulty <> UPPER(TRIM(difficulty))"
            )
        )


def downgrade() -> None:
    bind = op.get_bind()
    null_rows = bind.execute(
        sa.text("SELECT COUNT(*) FROM progress WHERE attention_score IS NULL")
    ).scalar()

    if null_rows:
        raise RuntimeError(
            f"Cannot downgrade: {null_rows} progress row(s) have no attention "
            "score, and the old schema cannot represent missing telemetry. "
            "Downgrading would require fabricating values."
        )

    with op.batch_alter_table("progress") as batch:
        batch.drop_column("looking_away")
        batch.drop_column("yawning")
        batch.alter_column(
            "attention_score",
            existing_type=sa.Float(),
            nullable=False,
        )
    # Difficulty casing is left uppercase: the values are equivalent and
    # the original mixed casing carried no meaning.
