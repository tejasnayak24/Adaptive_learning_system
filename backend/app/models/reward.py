from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class RewardHistory(Base):
    __tablename__ = "reward_history"

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

    reward: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    state: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    action: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    # The recommendation this reward evaluates, and the attempt whose
    # result produced it. Nullable for any rows recorded before linking.
    recommendation_id: Mapped[int | None] = mapped_column(
        ForeignKey("recommendation_history.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    progress_id: Mapped[int | None] = mapped_column(
        ForeignKey("progress.id", ondelete="SET NULL"),
        nullable=True,
    )

    student = relationship(
        "Student",
        back_populates="reward_history"
    )