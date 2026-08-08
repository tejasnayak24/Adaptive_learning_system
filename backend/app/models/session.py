from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class LearningSession(Base):
    __tablename__ = "learning_sessions"

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

    start_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    end_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    average_attention: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    average_score: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    student = relationship(
        "Student",
        back_populates="learning_sessions"
    )