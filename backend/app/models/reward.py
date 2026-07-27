from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


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

    student = relationship(
        "Student",
        back_populates="reward_history"
    )