"""Phase 3: camera-monitoring consent and learning-session monitoring.

Additive only: new ``monitoring_consents`` and ``monitoring_sessions``
tables and a nullable ``progress.monitoring_session_id``.

Revision ID: 0004_monitoring_sessions
Revises: 0003_grading_roles_history
Create Date: 2026-11-12
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0004_monitoring_sessions"
down_revision: Union[str, None] = "0003_grading_roles_history"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "monitoring_consents",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "student_id",
            sa.Integer(),
            sa.ForeignKey("students.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("consent_version", sa.String(length=32), nullable=False),
        sa.Column("accepted_at", sa.DateTime(), nullable=False),
        sa.Column("is_minor", sa.Boolean(), nullable=False),
        sa.Column("guardian_authorization_confirmed", sa.Boolean(), nullable=False),
        sa.Column("school_authorization_confirmed", sa.Boolean(), nullable=False),
        sa.Column("withdrawn_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_monitoring_consents_id", "monitoring_consents", ["id"])
    op.create_index("ix_monitoring_consents_student_id", "monitoring_consents", ["student_id"])

    op.create_table(
        "monitoring_sessions",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column(
            "student_id",
            sa.Integer(),
            sa.ForeignKey("students.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "lesson_id",
            sa.Integer(),
            sa.ForeignKey("lessons.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("claimed_at", sa.DateTime(), nullable=True),
        sa.Column("first_verified_at", sa.DateTime(), nullable=True),
        sa.Column("last_heartbeat_at", sa.DateTime(), nullable=True),
        sa.Column("last_client_seen_at", sa.DateTime(), nullable=True),
        sa.Column("ended_at", sa.DateTime(), nullable=True),
        sa.Column("end_reason", sa.String(length=64), nullable=True),
        sa.Column("pairing_token_hash", sa.String(length=64), nullable=True),
        sa.Column("pairing_expires_at", sa.DateTime(), nullable=True),
        sa.Column("agent_token_hash", sa.String(length=64), nullable=True),
        sa.Column("agent_token_expires_at", sa.DateTime(), nullable=True),
        sa.Column("last_sequence", sa.Integer(), nullable=False),
        sa.Column("heartbeat_count", sa.Integer(), nullable=False),
        sa.Column("reconnect_count", sa.Integer(), nullable=False),
    )
    op.create_index("ix_monitoring_sessions_student_id", "monitoring_sessions", ["student_id"])
    op.create_index("ix_monitoring_sessions_agent_token_hash", "monitoring_sessions", ["agent_token_hash"])

    with op.batch_alter_table("progress") as batch:
        batch.add_column(sa.Column("monitoring_session_id", sa.String(length=64), nullable=True))
        batch.create_foreign_key(
            "fk_progress_monitoring_session_id",
            "monitoring_sessions",
            ["monitoring_session_id"],
            ["id"],
            ondelete="SET NULL",
        )


def downgrade() -> None:
    with op.batch_alter_table("progress") as batch:
        batch.drop_constraint("fk_progress_monitoring_session_id", type_="foreignkey")
        batch.drop_column("monitoring_session_id")

    op.drop_table("monitoring_sessions")
    op.drop_table("monitoring_consents")
