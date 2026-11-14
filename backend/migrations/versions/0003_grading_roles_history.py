"""Phase 2: server-side grading, roles, recommendation and reward history.

Additive only -- no table or row is dropped:

* ``students.role`` (default ``student``).
* ``progress``: ``quiz_id`` (back-filled for existing rows from the unique
  lesson + difficulty quiz), ``correct_count``, ``total_questions``,
  ``hints_used``, ``drowsy``, ``created_at`` and an index on
  ``student_id``. Existing attempts keep NULL for values that were never
  recorded (they are not invented).
* New ``attempt_answers`` and ``recommendation_history`` tables.
* ``reward_history`` gains ``recommendation_id`` and ``progress_id``.

Revision ID: 0003_grading_roles_history
Revises: 0002_nullable_attention
Create Date: 2026-11-12
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0003_grading_roles_history"
down_revision: Union[str, None] = "0002_nullable_attention"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("students") as batch:
        batch.add_column(
            sa.Column(
                "role",
                sa.String(length=20),
                nullable=False,
                server_default="student",
            )
        )

    with op.batch_alter_table("progress") as batch:
        batch.add_column(sa.Column("quiz_id", sa.Integer(), nullable=True))
        batch.add_column(sa.Column("correct_count", sa.Integer(), nullable=True))
        batch.add_column(sa.Column("total_questions", sa.Integer(), nullable=True))
        batch.add_column(sa.Column("hints_used", sa.Integer(), nullable=True))
        batch.add_column(sa.Column("drowsy", sa.Boolean(), nullable=True))
        batch.add_column(sa.Column("created_at", sa.DateTime(), nullable=True))
        batch.create_foreign_key(
            "fk_progress_quiz_id_quizzes",
            "quizzes",
            ["quiz_id"],
            ["id"],
            ondelete="SET NULL",
        )
        batch.create_index("ix_progress_quiz_id", ["quiz_id"])
        batch.create_index("ix_progress_student_id", ["student_id"])

    # Each lesson has exactly one quiz per difficulty, so the attempted quiz
    # of a legacy row is determined by (lesson_id, difficulty). Rows without
    # a unique match are left NULL rather than guessed.
    op.execute(
        sa.text(
            """
            UPDATE progress
            SET quiz_id = (
                SELECT q.id FROM quizzes q
                WHERE q.lesson_id = progress.lesson_id
                  AND q.difficulty = progress.difficulty
            )
            WHERE quiz_id IS NULL
              AND (
                SELECT COUNT(*) FROM quizzes q
                WHERE q.lesson_id = progress.lesson_id
                  AND q.difficulty = progress.difficulty
              ) = 1
            """
        )
    )

    op.create_table(
        "attempt_answers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "progress_id",
            sa.Integer(),
            sa.ForeignKey("progress.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "question_id",
            sa.Integer(),
            sa.ForeignKey("questions.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("selected_answer", sa.String(length=1), nullable=False),
        sa.Column("correct_answer", sa.String(length=1), nullable=False),
        sa.Column("is_correct", sa.Boolean(), nullable=False),
    )
    op.create_index("ix_attempt_answers_id", "attempt_answers", ["id"])
    op.create_index("ix_attempt_answers_progress_id", "attempt_answers", ["progress_id"])
    op.create_index("ix_attempt_answers_question_id", "attempt_answers", ["question_id"])

    op.create_table(
        "recommendation_history",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "student_id",
            sa.Integer(),
            sa.ForeignKey("students.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "progress_id",
            sa.Integer(),
            sa.ForeignKey("progress.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("action", sa.String(length=64), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False),
        sa.Column("state", sa.Text(), nullable=False),
        sa.Column("state_key", sa.String(length=255), nullable=False),
        sa.Column("policy", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column(
            "outcome_progress_id",
            sa.Integer(),
            sa.ForeignKey("progress.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("outcome_recorded_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_recommendation_history_id", "recommendation_history", ["id"])
    op.create_index(
        "ix_recommendation_history_student_id", "recommendation_history", ["student_id"]
    )
    op.create_index(
        "ix_recommendation_history_progress_id", "recommendation_history", ["progress_id"]
    )

    with op.batch_alter_table("reward_history") as batch:
        batch.add_column(sa.Column("recommendation_id", sa.Integer(), nullable=True))
        batch.add_column(sa.Column("progress_id", sa.Integer(), nullable=True))
        batch.create_foreign_key(
            "fk_reward_history_recommendation_id",
            "recommendation_history",
            ["recommendation_id"],
            ["id"],
            ondelete="SET NULL",
        )
        batch.create_foreign_key(
            "fk_reward_history_progress_id",
            "progress",
            ["progress_id"],
            ["id"],
            ondelete="SET NULL",
        )
        batch.create_index("ix_reward_history_recommendation_id", ["recommendation_id"])


def downgrade() -> None:
    with op.batch_alter_table("reward_history") as batch:
        batch.drop_index("ix_reward_history_recommendation_id")
        batch.drop_constraint("fk_reward_history_progress_id", type_="foreignkey")
        batch.drop_constraint("fk_reward_history_recommendation_id", type_="foreignkey")
        batch.drop_column("progress_id")
        batch.drop_column("recommendation_id")

    op.drop_table("recommendation_history")
    op.drop_table("attempt_answers")

    with op.batch_alter_table("progress") as batch:
        batch.drop_index("ix_progress_student_id")
        batch.drop_index("ix_progress_quiz_id")
        batch.drop_constraint("fk_progress_quiz_id_quizzes", type_="foreignkey")
        batch.drop_column("created_at")
        batch.drop_column("drowsy")
        batch.drop_column("hints_used")
        batch.drop_column("total_questions")
        batch.drop_column("correct_count")
        batch.drop_column("quiz_id")

    with op.batch_alter_table("students") as batch:
        batch.drop_column("role")
