from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class Quiz(Base):
    __tablename__ = "quizzes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    lesson_id: Mapped[int] = mapped_column(
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    difficulty: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    lesson = relationship(
        "Lesson",
        back_populates="quizzes"
    )

    questions = relationship(
        "Question",
        back_populates="quiz",
        cascade="all, delete-orphan"
    )