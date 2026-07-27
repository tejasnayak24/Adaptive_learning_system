from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class StudentProgress(Base):
    __tablename__ = "student_progress"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    lesson_id: Mapped[int] = mapped_column(
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    quiz_score: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    response_time: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    attention_score: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    difficulty: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    student = relationship(
        "Student",
        back_populates="progress_records"
    )

    lesson = relationship(
        "Lesson",
        back_populates="progress_records"
    )