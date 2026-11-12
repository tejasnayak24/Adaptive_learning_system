from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Progress(Base):
    """One graded quiz attempt by a student."""

    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False,
        index=True,
    )

    lesson_id = Column(
        Integer,
        ForeignKey("lessons.id"),
        nullable=False,
    )

    # The quiz that was attempted. Nullable only so that a quiz can be
    # removed without destroying the student's history.
    quiz_id = Column(
        Integer,
        ForeignKey("quizzes.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Percentage (0-100), computed by the server from the stored answers.
    quiz_score = Column(
        Float,
        nullable=False,
    )

    correct_count = Column(Integer, nullable=True)
    total_questions = Column(Integer, nullable=True)
    hints_used = Column(Integer, nullable=True)

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

    # Whether yawning / looking away / drowsiness were observed during the
    # attempt. NULL means unknown (no valid camera telemetry).
    yawning = Column(
        Boolean,
        nullable=True,
    )

    looking_away = Column(
        Boolean,
        nullable=True,
    )

    drowsy = Column(
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

    # When the attempt was submitted. NULL only for attempts recorded
    # before timestamps existed.
    created_at = Column(
        DateTime,
        nullable=True,
        default=datetime.utcnow,
    )

    student = relationship(
        "Student",
        back_populates="progress",
    )

    lesson = relationship(
        "Lesson",
        back_populates="progress",
    )

    quiz = relationship("Quiz")

    answers = relationship(
        "AttemptAnswer",
        back_populates="progress",
        cascade="all, delete-orphan",
    )
