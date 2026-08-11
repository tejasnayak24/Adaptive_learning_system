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

    attention_score = Column(
        Float,
        nullable=False,
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