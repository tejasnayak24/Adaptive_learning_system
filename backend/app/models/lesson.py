from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    topic: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )

    difficulty: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    # One Lesson -> Many Quizzes
    quizzes = relationship(
        "Quiz",
        back_populates="lesson",
        cascade="all, delete-orphan"
    )

    # One Lesson -> Many Student Progress Records
    progress_records = relationship(
        "StudentProgress",
        back_populates="lesson",
        cascade="all, delete-orphan"
    )