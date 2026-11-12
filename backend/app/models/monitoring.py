"""Camera-monitoring consent and learning-session monitoring records.

Tokens are never stored in clear text: only SHA-256 hashes of the
single-use pairing token and of the agent token are kept.
"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class MonitoringConsent(Base):
    """A student's (and, for minors, guardian/school) consent to camera use."""

    __tablename__ = "monitoring_consents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True
    )
    consent_version: Mapped[str] = mapped_column(String(32), nullable=False)
    accepted_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    # Recorded for minors (age < 18): the student confirms that a parent or
    # guardian and their school have authorised camera-based monitoring.
    is_minor: Mapped[bool] = mapped_column(Boolean, nullable=False)
    guardian_authorization_confirmed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    school_authorization_confirmed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    withdrawn_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class MonitoringSession(Base):
    """One monitored learning session, paired with the local camera agent."""

    __tablename__ = "monitoring_sessions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True
    )
    lesson_id: Mapped[int | None] = mapped_column(
        ForeignKey("lessons.id", ondelete="SET NULL"), nullable=True
    )

    # pending (waiting for the agent) | active (agent paired) | ended
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="pending")

    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    claimed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    first_verified_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    last_heartbeat_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    last_client_seen_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    end_reason: Mapped[str | None] = mapped_column(String(64), nullable=True)

    pairing_token_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    pairing_expires_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    agent_token_hash: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    agent_token_expires_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    last_sequence: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    heartbeat_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    reconnect_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    student = relationship("Student")
