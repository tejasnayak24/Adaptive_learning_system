from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class RecommendationHistory(Base):
    """An adaptive recommendation produced for a graded attempt.

    ``state`` is the JSON-encoded learning state the policy saw, and
    ``state_key`` the discretised Q-table key, so every decision can be
    audited and later paired with its observed outcome (see
    ``RewardHistory``).
    """

    __tablename__ = "recommendation_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    progress_id: Mapped[int | None] = mapped_column(
        ForeignKey("progress.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    action: Mapped[str] = mapped_column(String(64), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)

    state: Mapped[str] = mapped_column(Text, nullable=False)
    state_key: Mapped[str] = mapped_column(String(255), nullable=False)

    # Which policy produced the decision: "q_learning",
    # "q_learning_nearest_state" or "fallback" (Phase 4), or "rules" for
    # rows recorded before Phase 4 when hand-written rules decided.
    policy: Mapped[str] = mapped_column(String(32), nullable=False)

    # Phase 4: the Q-table that produced the decision, and a JSON record
    # of the Q-values, blocked actions and visit counts behind it.
    model_version: Mapped[str | None] = mapped_column(String(64), nullable=True)
    decision_detail: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    # Filled in when the student's next attempt reveals the outcome.
    outcome_progress_id: Mapped[int | None] = mapped_column(
        ForeignKey("progress.id", ondelete="SET NULL"),
        nullable=True,
    )
    outcome_recorded_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    student = relationship("Student", back_populates="recommendations")
