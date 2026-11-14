from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    topic: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    difficulty: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    # -- Phase 5 curriculum placement (nullable for lessons created by hand) --
    slug: Mapped[str | None] = mapped_column(String(120), unique=True, nullable=True)
    grade: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    subject: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    topic_id: Mapped[int | None] = mapped_column(
        ForeignKey("curriculum_topics.id", ondelete="SET NULL"), nullable=True, index=True
    )
    position: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # JSON: objectives, sections, definitions, examples, worked examples,
    # diagram, real-world application, key takeaways, practice exercises.
    material: Mapped[str | None] = mapped_column(Text, nullable=True)

    curriculum_topic = relationship("CurriculumTopic", back_populates="lessons")

    # One Lesson -> Many Quizzes
    quizzes = relationship(
        "Quiz",
        back_populates="lesson",
        cascade="all, delete-orphan",
    )

    # One Lesson -> Many Progress Records
    progress = relationship(
        "Progress",
        back_populates="lesson",
        cascade="all, delete-orphan",
    )