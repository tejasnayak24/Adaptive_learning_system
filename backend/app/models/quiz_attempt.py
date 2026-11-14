"""Server-side quiz attempts and the page-visibility events reported for them.

A ``QuizAttempt`` exists from the moment a student starts a quiz until it is
submitted, terminated by the tab-switch rule, or abandoned. Answers are
saved on it as the student works, so they survive reloads and are kept
when an attempt ends without being graded.

Only a submitted attempt is graded: grading creates the ``progress`` row
(``progress_id``). Terminated and abandoned attempts never create one, so
they are excluded from lesson completion, quiz averages, analytics,
recommendations and Q-learning rewards, which all read ``progress``.

All times are naive UTC, measured by the server, except ``client_ms`` and
``hidden_ms`` on events, which the browser measured with its monotonic clock.
"""

from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Index, Integer, String, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base

# Attempt states. "away" = the quiz page is hidden and the grace period runs;
# "unverified" = no report arrived to say how the absence ended (locked).
IN_PROGRESS = "in_progress"
AWAY = "away"
UNVERIFIED = "unverified"
SUBMITTED = "submitted"
TERMINATED = "terminated"
ABANDONED = "abandoned"

OPEN_STATUSES = (IN_PROGRESS, AWAY, UNVERIFIED)
ENDED_STATUSES = (SUBMITTED, TERMINATED, ABANDONED)

_OPEN_SQL = "status IN ('in_progress', 'away', 'unverified')"


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    __table_args__ = (
        # At most one open attempt per student and quiz: a reload resumes it.
        Index(
            "uq_quiz_attempts_open",
            "student_id",
            "quiz_id",
            unique=True,
            postgresql_where=text(_OPEN_SQL),
            sqlite_where=text(_OPEN_SQL),
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True
    )
    quiz_id: Mapped[int | None] = mapped_column(
        ForeignKey("quizzes.id", ondelete="SET NULL"), nullable=True, index=True
    )
    monitoring_session_id: Mapped[str | None] = mapped_column(
        ForeignKey("monitoring_sessions.id", ondelete="SET NULL"), nullable=True
    )

    # standard | practice | hints | challenge (as on progress.attempt_mode)
    mode: Mapped[str] = mapped_column(String(16), nullable=False, default="standard")
    # Whether the two-strike tab rule applies. True for every graded mode.
    protected: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    status: Mapped[str] = mapped_column(String(16), nullable=False, default=IN_PROGRESS)
    strikes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # question id (as a string) -> option letter, saved as the student works.
    answers: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    # Non-graded UI state needed to resume: current question, hints revealed,
    # elapsed seconds. Never trusted for grading.
    draft_state: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # The open absence (status "away" or "unverified").
    away_started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    away_page_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    # "hidden" (tab hidden) or "unload" (the page was closed or reloaded)
    away_kind: Mapped[str | None] = mapped_column(String(16), nullable=True)
    unverified_since: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Last sequence number seen per page (page id -> seq), to drop duplicates.
    page_sequences: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

    ended_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    # submitted | grace_expired | second_tab_switch | left_quiz |
    # no_contact | unverified_no_measurement | monitoring_ended
    end_reason: Mapped[str | None] = mapped_column(String(32), nullable=True)

    progress_id: Mapped[int | None] = mapped_column(
        ForeignKey("progress.id", ondelete="SET NULL"), nullable=True
    )


class QuizAttemptEvent(Base):
    """One page event reported by the browser (or noted by the server)."""

    __tablename__ = "quiz_attempt_events"
    __table_args__ = (
        UniqueConstraint("attempt_id", "page_id", "seq", name="uq_quiz_attempt_events_page_seq"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    attempt_id: Mapped[int] = mapped_column(
        ForeignKey("quiz_attempts.id", ondelete="CASCADE"), nullable=False, index=True
    )
    # Random id of one page load, and the event's sequence number within it.
    # Server-generated notes (e.g. "deadline_passed") use page_id "server".
    page_id: Mapped[str] = mapped_column(String(64), nullable=False)
    seq: Mapped[int] = mapped_column(Integer, nullable=False)

    # hidden | visible | pagehide | resume | hidden_tick | blur | focus |
    # online | offline | deadline_passed | abandon
    kind: Mapped[str] = mapped_column(String(16), nullable=False)

    client_ms: Mapped[float | None] = mapped_column(Float, nullable=True)
    hidden_ms: Mapped[float | None] = mapped_column(Float, nullable=True)
    delivery_failures: Mapped[int | None] = mapped_column(Integer, nullable=True)
    queued_ms: Mapped[float | None] = mapped_column(Float, nullable=True)

    received_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    # What the server concluded: strike | warning_network_delayed |
    # terminated | unverified | diagnostic | ignored ...
    outcome: Mapped[str | None] = mapped_column(String(32), nullable=True)
