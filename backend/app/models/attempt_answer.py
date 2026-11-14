from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class AttemptAnswer(Base):
    """The answer a student gave to one question in a graded attempt."""

    __tablename__ = "attempt_answers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    progress_id: Mapped[int] = mapped_column(
        ForeignKey("progress.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Kept nullable so editing a question bank never erases history.
    question_id: Mapped[int | None] = mapped_column(
        ForeignKey("questions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    selected_answer: Mapped[str] = mapped_column(String(1), nullable=False)
    correct_answer: Mapped[str] = mapped_column(String(1), nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)

    progress = relationship("Progress", back_populates="answers")
