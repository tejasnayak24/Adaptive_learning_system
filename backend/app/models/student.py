from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    age: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    # One Student -> Many Progress Records
    progress_records = relationship(
        "StudentProgress",
        back_populates="student",
        cascade="all, delete-orphan"
    )

    # One Student -> Many Learning Sessions
    learning_sessions = relationship(
        "LearningSession",
        back_populates="student",
        cascade="all, delete-orphan"
    )

    # One Student -> Many Reward History Records
    reward_history = relationship(
        "RewardHistory",
        back_populates="student",
        cascade="all, delete-orphan"
    )