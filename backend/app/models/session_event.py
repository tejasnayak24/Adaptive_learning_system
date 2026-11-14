"""Camera-observed episodes during a monitored learning session.

One row per *episode* (not per heartbeat): currently ``multiple_faces`` --
the camera agent saw two or more faces for a sustained period. Only the
kind, server timestamps and the peak face count are stored; never images.
An episode is information, not evidence of misconduct (a parent helping
is normal).
"""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base

MULTIPLE_FACES = "multiple_faces"


class SessionEvent(Base):
    __tablename__ = "session_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    monitoring_session_id: Mapped[str] = mapped_column(
        ForeignKey("monitoring_sessions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True
    )
    kind: Mapped[str] = mapped_column(String(32), nullable=False)

    # Server receive times of the heartbeats that opened / closed the episode.
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    # cleared | not_measured | heartbeats_stopped | session_ended
    end_reason: Mapped[str | None] = mapped_column(String(32), nullable=True)
    peak_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
