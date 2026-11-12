from typing import List

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.utils.constants import normalize_difficulty


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


class QuizStartRequest(BaseModel):
    quiz_id: int


class QuizSubmitRequest(BaseModel):
    """Quiz result submitted by the authenticated student.

    ``student_id`` is accepted only for backward compatibility; the
    backend always records the attempt against the student in the access
    token and rejects a mismatching value.

    Camera fields are optional: ``None`` means valid telemetry was not
    available for this attempt. They must never be filled with guesses.
    """

    student_id: int | None = None
    lesson_id: int
    quiz_score: float = Field(ge=0, le=100)
    response_time: float = Field(ge=0)
    attention_score: float | None = Field(default=None, ge=0.0, le=1.0)
    yawning: bool | None = None
    looking_away: bool | None = None
    difficulty: str

    @field_validator("difficulty")
    @classmethod
    def _normalize_difficulty(cls, value: str) -> str:
        return normalize_difficulty(value)


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
