from typing import List

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


class QuizStartRequest(BaseModel):
    quiz_id: int


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
    monitoring_session_id: str = Field(min_length=8, max_length=64)
    answers: dict[int, str] = Field(min_length=1)
    response_time: float = Field(ge=0)
    hints_used: int = Field(default=0, ge=0)
    # How the attempt was taken: standard, practice (recommended retake),
    # hints (retry with hints) or challenge (timed).
    mode: str = Field(default="standard", pattern="^(standard|practice|hints|challenge)$")

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
