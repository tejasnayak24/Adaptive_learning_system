"""Session integrity: server-side quiz attempts and page-visibility events.

Additive only: two new tables, no change to existing tables or rows.

* ``quiz_attempts`` -- one row per started quiz; answers are saved on it
  while the student works. Only a submitted attempt is graded (it then
  points at its ``progress`` row).
* ``quiz_attempt_events`` -- page visibility / focus events reported by the
  browser for an attempt, with the server's conclusion.

Revision ID: 0007_quiz_attempts
Revises: 0006_curriculum
Create Date: 2026-11-14
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0007_quiz_attempts"
down_revision: Union[str, None] = "0006_curriculum"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_OPEN_SQL = "status IN ('in_progress', 'away', 'unverified')"


def upgrade() -> None:
    op.create_table(
        "quiz_attempts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "student_id",
            sa.Integer(),
            sa.ForeignKey("students.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "quiz_id",
            sa.Integer(),
            sa.ForeignKey("quizzes.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "monitoring_session_id",
            sa.String(length=64),
            sa.ForeignKey("monitoring_sessions.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("mode", sa.String(length=16), nullable=False),
        sa.Column("protected", sa.Boolean(), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("strikes", sa.Integer(), nullable=False),
        sa.Column("answers", sa.JSON(), nullable=False),
        sa.Column("draft_state", sa.JSON(), nullable=True),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("last_seen_at", sa.DateTime(), nullable=True),
        sa.Column("away_started_at", sa.DateTime(), nullable=True),
        sa.Column("away_page_id", sa.String(length=64), nullable=True),
        sa.Column("away_kind", sa.String(length=16), nullable=True),
        sa.Column("unverified_since", sa.DateTime(), nullable=True),
        sa.Column("page_sequences", sa.JSON(), nullable=False),
        sa.Column("ended_at", sa.DateTime(), nullable=True),
        sa.Column("end_reason", sa.String(length=32), nullable=True),
        sa.Column(
            "progress_id",
            sa.Integer(),
            sa.ForeignKey("progress.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )
    op.create_index("ix_quiz_attempts_id", "quiz_attempts", ["id"])
    op.create_index("ix_quiz_attempts_student_id", "quiz_attempts", ["student_id"])
    op.create_index("ix_quiz_attempts_quiz_id", "quiz_attempts", ["quiz_id"])
    op.create_index(
        "uq_quiz_attempts_open",
        "quiz_attempts",
        ["student_id", "quiz_id"],
        unique=True,
        postgresql_where=sa.text(_OPEN_SQL),
        sqlite_where=sa.text(_OPEN_SQL),
    )

    op.create_table(
        "quiz_attempt_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "attempt_id",
            sa.Integer(),
            sa.ForeignKey("quiz_attempts.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("page_id", sa.String(length=64), nullable=False),
        sa.Column("seq", sa.Integer(), nullable=False),
        sa.Column("kind", sa.String(length=16), nullable=False),
        sa.Column("client_ms", sa.Float(), nullable=True),
        sa.Column("hidden_ms", sa.Float(), nullable=True),
        sa.Column("delivery_failures", sa.Integer(), nullable=True),
        sa.Column("queued_ms", sa.Float(), nullable=True),
        sa.Column("received_at", sa.DateTime(), nullable=False),
        sa.Column("outcome", sa.String(length=32), nullable=True),
        sa.UniqueConstraint("attempt_id", "page_id", "seq", name="uq_quiz_attempt_events_page_seq"),
    )
    op.create_index("ix_quiz_attempt_events_id", "quiz_attempt_events", ["id"])
    op.create_index("ix_quiz_attempt_events_attempt_id", "quiz_attempt_events", ["attempt_id"])


def downgrade() -> None:
    op.drop_index("ix_quiz_attempt_events_attempt_id", table_name="quiz_attempt_events")
    op.drop_index("ix_quiz_attempt_events_id", table_name="quiz_attempt_events")
    op.drop_table("quiz_attempt_events")
    op.drop_index("uq_quiz_attempts_open", table_name="quiz_attempts")
    op.drop_index("ix_quiz_attempts_quiz_id", table_name="quiz_attempts")
    op.drop_index("ix_quiz_attempts_student_id", table_name="quiz_attempts")
    op.drop_index("ix_quiz_attempts_id", table_name="quiz_attempts")
    op.drop_table("quiz_attempts")
