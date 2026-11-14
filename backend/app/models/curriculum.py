"""Curriculum hierarchy: Grade -> Subject -> Unit -> Topic -> Lesson.

Grade and subject are attributes of a unit (and copied onto each lesson
for fast filtering); units and topics are rows so the curriculum is fully
database-driven. Content is imported by ``backend/scripts/import_curriculum.py``
from ``backend/curriculum/content/*.json``; ``slug`` makes the import
idempotent.
"""

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base

GRADES = (6, 7, 8, 9, 10)
SUBJECTS = ("Mathematics", "Science", "Social Science", "English")


class CurriculumUnit(Base):
    __tablename__ = "curriculum_units"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    grade: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    subject: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    topics = relationship(
        "CurriculumTopic",
        back_populates="unit",
        order_by="CurriculumTopic.position",
        cascade="all, delete-orphan",
    )


class CurriculumTopic(Base):
    __tablename__ = "curriculum_topics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    unit_id: Mapped[int] = mapped_column(
        ForeignKey("curriculum_units.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    unit = relationship("CurriculumUnit", back_populates="topics")
    lessons = relationship("Lesson", back_populates="curriculum_topic", order_by="Lesson.position")
