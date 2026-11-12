from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False,
    )

    lesson_id = Column(
        Integer,
        ForeignKey("lessons.id"),
        nullable=False,
    )

    quiz_score = Column(
        Float,
        nullable=False,
    )

    response_time = Column(
        Float,
        nullable=False,
    )

    # Average attention (0.0-1.0) measured by the camera during the attempt.
    # NULL means valid camera telemetry was unavailable -- it is never a
    # stand-in for low attention.
    attention_score = Column(
        Float,
        nullable=True,
    )

    # Whether yawning / looking away were observed during the attempt.
    # NULL means unknown (no valid camera telemetry).
    yawning = Column(
        Boolean,
        nullable=True,
    )

    looking_away = Column(
        Boolean,
        nullable=True,
    )

    difficulty = Column(
        String,
        nullable=False,
    )

    completed = Column(
        Boolean,
        default=False,
    )

    student = relationship(
        "Student",
        back_populates="progress",
    )

    lesson = relationship(
        "Lesson",
        back_populates="progress",
    )