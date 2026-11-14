"""Phase 5: grade-based curriculum hierarchy, lesson material, hints.

Additive only. Existing lessons, quizzes, questions and progress keep their
ids and values; the new columns are nullable. Curriculum content is loaded
separately by ``backend/scripts/import_curriculum.py`` (idempotent), which
also places the five original Science lessons into the hierarchy.

* ``students.grade`` (6-10, NULL until the student chooses it)
* ``curriculum_units``, ``curriculum_topics``
* ``lessons.slug/grade/subject/topic_id/position/material``
* ``questions.hint/explanation``
* ``progress.attempt_mode``

Revision ID: 0006_curriculum
Revises: 0005_rl_decision_audit
Create Date: 2026-11-12
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0006_curriculum"
down_revision: Union[str, None] = "0005_rl_decision_audit"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("students") as batch:
        batch.add_column(sa.Column("grade", sa.Integer(), nullable=True))

    op.create_table(
        "curriculum_units",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("slug", sa.String(length=120), nullable=False, unique=True),
        sa.Column("grade", sa.Integer(), nullable=False),
        sa.Column("subject", sa.String(length=50), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
    )
    op.create_index("ix_curriculum_units_id", "curriculum_units", ["id"])
    op.create_index("ix_curriculum_units_grade", "curriculum_units", ["grade"])
    op.create_index("ix_curriculum_units_subject", "curriculum_units", ["subject"])

    op.create_table(
        "curriculum_topics",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("slug", sa.String(length=120), nullable=False, unique=True),
        sa.Column(
            "unit_id",
            sa.Integer(),
            sa.ForeignKey("curriculum_units.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("position", sa.Integer(), nullable=False),
    )
    op.create_index("ix_curriculum_topics_id", "curriculum_topics", ["id"])
    op.create_index("ix_curriculum_topics_unit_id", "curriculum_topics", ["unit_id"])

    with op.batch_alter_table("lessons") as batch:
        batch.add_column(sa.Column("slug", sa.String(length=120), nullable=True))
        batch.add_column(sa.Column("grade", sa.Integer(), nullable=True))
        batch.add_column(sa.Column("subject", sa.String(length=50), nullable=True))
        batch.add_column(sa.Column("topic_id", sa.Integer(), nullable=True))
        batch.add_column(sa.Column("position", sa.Integer(), nullable=True))
        batch.add_column(sa.Column("material", sa.Text(), nullable=True))
        batch.create_unique_constraint("uq_lessons_slug", ["slug"])
        batch.create_foreign_key(
            "fk_lessons_topic_id", "curriculum_topics", ["topic_id"], ["id"], ondelete="SET NULL"
        )
        batch.create_index("ix_lessons_grade", ["grade"])
        batch.create_index("ix_lessons_subject", ["subject"])
        batch.create_index("ix_lessons_topic_id", ["topic_id"])

    with op.batch_alter_table("questions") as batch:
        batch.add_column(sa.Column("hint", sa.Text(), nullable=True))
        batch.add_column(sa.Column("explanation", sa.Text(), nullable=True))

    with op.batch_alter_table("progress") as batch:
        batch.add_column(sa.Column("attempt_mode", sa.String(length=16), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table("progress") as batch:
        batch.drop_column("attempt_mode")

    with op.batch_alter_table("questions") as batch:
        batch.drop_column("explanation")
        batch.drop_column("hint")

    with op.batch_alter_table("lessons") as batch:
        batch.drop_index("ix_lessons_topic_id")
        batch.drop_index("ix_lessons_subject")
        batch.drop_index("ix_lessons_grade")
        batch.drop_constraint("fk_lessons_topic_id", type_="foreignkey")
        batch.drop_constraint("uq_lessons_slug", type_="unique")
        batch.drop_column("material")
        batch.drop_column("position")
        batch.drop_column("topic_id")
        batch.drop_column("subject")
        batch.drop_column("grade")
        batch.drop_column("slug")

    op.drop_index("ix_curriculum_topics_unit_id", table_name="curriculum_topics")
    op.drop_index("ix_curriculum_topics_id", table_name="curriculum_topics")
    op.drop_table("curriculum_topics")
    op.drop_index("ix_curriculum_units_subject", table_name="curriculum_units")
    op.drop_index("ix_curriculum_units_grade", table_name="curriculum_units")
    op.drop_index("ix_curriculum_units_id", table_name="curriculum_units")
    op.drop_table("curriculum_units")

    with op.batch_alter_table("students") as batch:
        batch.drop_column("grade")
