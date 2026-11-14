"""Session integrity: camera-observed episodes (multiple faces).

Additive only: one new table. Rows are episodes with server timestamps and
a peak face count; no images are stored.

Revision ID: 0008_session_events
Revises: 0007_quiz_attempts
Create Date: 2026-11-14
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0008_session_events"
down_revision: Union[str, None] = "0007_quiz_attempts"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "session_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "monitoring_session_id",
            sa.String(length=64),
            sa.ForeignKey("monitoring_sessions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "student_id",
            sa.Integer(),
            sa.ForeignKey("students.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("kind", sa.String(length=32), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("ended_at", sa.DateTime(), nullable=True),
        sa.Column("end_reason", sa.String(length=32), nullable=True),
        sa.Column("peak_count", sa.Integer(), nullable=True),
    )
    op.create_index("ix_session_events_id", "session_events", ["id"])
    op.create_index("ix_session_events_monitoring_session_id", "session_events", ["monitoring_session_id"])
    op.create_index("ix_session_events_student_id", "session_events", ["student_id"])


def downgrade() -> None:
    op.drop_index("ix_session_events_student_id", table_name="session_events")
    op.drop_index("ix_session_events_monitoring_session_id", table_name="session_events")
    op.drop_index("ix_session_events_id", table_name="session_events")
    op.drop_table("session_events")
