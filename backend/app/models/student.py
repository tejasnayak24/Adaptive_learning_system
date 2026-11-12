from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    age: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    # Authorization role: "student" (default), "teacher" or "admin".
    # Only teachers and admins may create, edit or delete curriculum.
    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="student",
        server_default="student",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    # School grade (6-10). NULL for accounts created before Phase 5; the
    # student chooses it on first sign-in. Curriculum is filtered by it.
    grade: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    # One Student -> Many Progress Records
    progress = relationship(
        "Progress",
        back_populates="student",
        cascade="all, delete-orphan",
    )

    # One Student -> Many Learning Sessions
    learning_sessions = relationship(
        "LearningSession",
        back_populates="student",
        cascade="all, delete-orphan",
    )

    # One Student -> Many Reward History Records
    reward_history = relationship(
        "RewardHistory",
        back_populates="student",
        cascade="all, delete-orphan",
    )

    # One Student -> Many Recommendations
    recommendations = relationship(
        "RecommendationHistory",
        back_populates="student",
        cascade="all, delete-orphan",
    )

    @property
    def can_manage_curriculum(self) -> bool:
        return self.role in ("teacher", "admin")