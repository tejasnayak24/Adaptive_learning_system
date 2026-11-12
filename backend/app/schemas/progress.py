from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.utils.constants import normalize_difficulty


class ProgressBase(BaseModel):
    student_id: int
    lesson_id: int
    quiz_score: float
    response_time: float
    attention_score: float | None = None
    yawning: bool | None = None
    looking_away: bool | None = None
    difficulty: str
    completed: bool


class ProgressCreate(ProgressBase):
    pass


class ProgressUpdate(BaseModel):
    quiz_score: float = Field(ge=0, le=100)
    response_time: float = Field(ge=0)
    attention_score: float | None = Field(default=None, ge=0.0, le=1.0)
    yawning: bool | None = None
    looking_away: bool | None = None
    difficulty: str
    completed: bool

    @field_validator("difficulty")
    @classmethod
    def _normalize_difficulty(cls, value: str) -> str:
        return normalize_difficulty(value)


class ProgressResponse(ProgressBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )
