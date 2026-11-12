"""Baseline schema (as created by the original create_all).

This mirrors the existing production schema exactly, so a database that
was created before Alembic was introduced can be marked as up to date
with ``alembic stamp 0001_baseline`` without altering any data. A brand
new database gets the same tables by running ``alembic upgrade head``.

Revision ID: 0001_baseline
Revises:
Create Date: 2026-11-12
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0001_baseline"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "students",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_students_id", "students", ["id"])
    op.create_index("ix_students_email", "students", ["email"], unique=True)

    op.create_table(
        "lessons",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("topic", sa.String(length=100), nullable=False),
        sa.Column("difficulty", sa.String(length=20), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_lessons_id", "lessons", ["id"])
    op.create_index("ix_lessons_topic", "lessons", ["topic"])

    op.create_table(
        "quizzes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "lesson_id",
            sa.Integer(),
            sa.ForeignKey("lessons.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("difficulty", sa.String(length=20), nullable=False),
    )
    op.create_index("ix_quizzes_id", "quizzes", ["id"])
    op.create_index("ix_quizzes_lesson_id", "quizzes", ["lesson_id"])

    op.create_table(
        "questions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "quiz_id",
            sa.Integer(),
            sa.ForeignKey("quizzes.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("option_a", sa.String(length=255), nullable=False),
        sa.Column("option_b", sa.String(length=255), nullable=False),
        sa.Column("option_c", sa.String(length=255), nullable=False),
        sa.Column("option_d", sa.String(length=255), nullable=False),
        sa.Column("correct_answer", sa.String(length=1), nullable=False),
    )
    op.create_index("ix_questions_id", "questions", ["id"])
    op.create_index("ix_questions_quiz_id", "questions", ["quiz_id"])

    op.create_table(
        "progress",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "student_id",
            sa.Integer(),
            sa.ForeignKey("students.id"),
            nullable=False,
        ),
        sa.Column(
            "lesson_id",
            sa.Integer(),
            sa.ForeignKey("lessons.id"),
            nullable=False,
        ),
        sa.Column("quiz_score", sa.Float(), nullable=False),
        sa.Column("response_time", sa.Float(), nullable=False),
        sa.Column("attention_score", sa.Float(), nullable=False),
        sa.Column("difficulty", sa.String(), nullable=False),
        sa.Column("completed", sa.Boolean(), nullable=True),
    )
    op.create_index("ix_progress_id", "progress", ["id"])

    op.create_table(
        "learning_sessions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "student_id",
            sa.Integer(),
            sa.ForeignKey("students.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("start_time", sa.DateTime(), nullable=False),
        sa.Column("end_time", sa.DateTime(), nullable=False),
        sa.Column("average_attention", sa.Float(), nullable=False),
        sa.Column("average_score", sa.Float(), nullable=False),
    )
    op.create_index("ix_learning_sessions_id", "learning_sessions", ["id"])
    op.create_index(
        "ix_learning_sessions_student_id", "learning_sessions", ["student_id"]
    )

    op.create_table(
        "reward_history",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "student_id",
            sa.Integer(),
            sa.ForeignKey("students.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("reward", sa.Float(), nullable=False),
        sa.Column("state", sa.String(length=255), nullable=False),
        sa.Column("action", sa.String(length=255), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_reward_history_id", "reward_history", ["id"])
    op.create_index(
        "ix_reward_history_student_id", "reward_history", ["student_id"]
    )


def downgrade() -> None:
    # Downgrading the baseline would drop every table and all data, so it
    # is deliberately not supported.
    raise RuntimeError(
        "Refusing to downgrade the baseline: it would drop all tables."
    )
