import json
from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator



class QuizBase(BaseModel):
    lesson_id: int
    title: str
    difficulty: str


class QuizCreate(QuizBase):
    pass


class QuizUpdate(QuizBase):
    pass


class QuizResponse(QuizBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


_MODE_PATTERN = "^(standard|practice|hints|challenge)$"


class QuizStartRequest(BaseModel):
    """Start (or resume) a server-side attempt at a quiz."""

    quiz_id: int
    mode: str = Field(default="standard", pattern=_MODE_PATTERN)
    monitoring_session_id: str | None = Field(default=None, min_length=8, max_length=64)


class QuizSubmitRequest(BaseModel):
    """Answers submitted by the authenticated student for one quiz.

    The server grades ``answers`` (question id -> option letter A-D); a
    client-computed score is never accepted. ``student_id`` is optional
    and only checked against the access token.

    Camera measurements are never accepted from the browser: the server
    takes them from the telemetry its paired camera agent reported for
    ``monitoring_session_id`` (which must belong to the student). Values
    the client might send for attention, yawning etc. are ignored.
    """

    student_id: int | None = None
    quiz_id: int
    # The attempt being submitted (from /quiz/start). If omitted, the
    # student's open attempt at this quiz is used.
    attempt_id: int | None = None
    monitoring_session_id: str = Field(min_length=8, max_length=64)
    answers: dict[int, str] = Field(min_length=1)
    response_time: float = Field(ge=0)
    hints_used: int = Field(default=0, ge=0)
    # How the attempt was taken: standard, practice (recommended retake),
    # hints (retry with hints) or challenge (timed).
    mode: str = Field(default="standard", pattern=_MODE_PATTERN)

    @field_validator("answers")
    @classmethod
    def _normalize_answers(cls, value: dict[int, str]) -> dict[int, str]:
        normalized = {}
        for question_id, option in value.items():
            letter = str(option).strip().upper()
            if letter not in ("A", "B", "C", "D"):
                raise ValueError(
                    f"answer for question {question_id} must be A, B, C or D"
                )
            normalized[question_id] = letter
        return normalized


def _letters(value: dict[int, str]) -> dict[int, str]:
    normalized = {}
    for question_id, option in value.items():
        letter = str(option).strip().upper()
        if letter not in ("A", "B", "C", "D"):
            raise ValueError(f"answer for question {question_id} must be A, B, C or D")
        normalized[question_id] = letter
    return normalized


class AttemptAnswersRequest(BaseModel):
    """In-progress answers (may be partial) and resumable UI state."""

    answers: dict[int, str] = Field(default_factory=dict, max_length=200)
    # Current question, hints revealed, elapsed seconds. Not used for grading.
    draft_state: dict | None = None

    @field_validator("answers")
    @classmethod
    def _normalize(cls, value: dict[int, str]) -> dict[int, str]:
        return _letters(value)

    @field_validator("draft_state")
    @classmethod
    def _small(cls, value: dict | None) -> dict | None:
        if value is not None and len(json.dumps(value)) > 4000:
            raise ValueError("draft_state is too large")
        return value


class AttemptEventIn(BaseModel):
    """One page event observed by the browser.

    ``hidden_ms`` and ``client_ms`` come from the browser's monotonic clock
    (``performance.now()``); for a reloaded page ``hidden_ms`` is measured
    from the moment the previous page was hidden.
    """

    seq: int = Field(ge=1, le=10_000_000)
    kind: Literal[
        "hidden", "visible", "pagehide", "resume", "hidden_tick", "blur", "focus", "online", "offline"
    ]
    client_ms: float | None = Field(default=None, ge=0, le=1e10)
    hidden_ms: float | None = Field(default=None, ge=0, le=1e10)
    delivery_failures: int | None = Field(default=None, ge=0, le=100_000)
    queued_ms: float | None = Field(default=None, ge=0, le=1e10)
    reload: bool = False


class AttemptEventsRequest(BaseModel):
    page_id: str = Field(min_length=8, max_length=64, pattern=r"^[A-Za-z0-9_-]+$")
    events: list[AttemptEventIn] = Field(min_length=1, max_length=50)


class QuestionResponse(BaseModel):
    id: int
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str

    model_config = ConfigDict(from_attributes=True)


class QuizStartResponse(BaseModel):
    quiz: QuizResponse
    questions: List[QuestionResponse]


class QuizSubmitResponse(BaseModel):
    success: bool
    message: str
