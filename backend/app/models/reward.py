from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
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

    # Phase 4: reward formula version (1 = Phase 2 formula, 2 = shared
    # rl_engine outcome reward), whether the next attempt shows the
    # recommendation was followed (None = not observable), and the JSON
    # breakdown of the reward components.
    reward_version: Mapped[int | None] = mapped_column(Integer, nullable=True)
    followed: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    reward_detail: Mapped[str | None] = mapped_column(Text, nullable=True)

    student = relationship(
        "Student",
        back_populates="reward_history"
    )