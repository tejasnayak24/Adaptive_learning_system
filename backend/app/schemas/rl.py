"""Request schema for the Reinforcement Learning recommendation endpoint.

This module defines the Pydantic model used to validate the request
body the backend receives when asking for an adaptive learning
recommendation. It performs input validation only -- it has no
knowledge of the RL engine's internal types and does not convert,
construct, or reference any of them.
"""

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationInfo,
    field_validator,
)

# Accepted difficulty values.
_ALLOWED_DIFFICULTIES = {"EASY", "MEDIUM", "HARD"}


class RecommendationRequest(BaseModel):
    """Request body for an adaptive learning recommendation."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "subject": "Social Science",
                "topic": "Indian Constitution",
                "lesson": "Indian Constitution",
                "previous_quiz_score": 60,
                "current_quiz_score": 80,
                "attention_score": 0.8,
                "yawning": False,
                "looking_away": False,
                "difficulty": "EASY",
                "response_time": 12.5,
                "hints_used": 1,
                "lesson_attempts": 2,
                "completed_lessons": 10,
            }
        }
    )

    subject: str = Field(
        min_length=1,
        description="The subject currently being studied.",
    )

    topic: str = Field(
        min_length=1,
        description="The topic within the subject.",
    )

    lesson: str = Field(
        min_length=1,
        description="The specific lesson within the topic.",
    )

    previous_quiz_score: int = Field(
        ge=0,
        le=100,
        description="Score from the previous quiz attempt (0-100).",
    )

    current_quiz_score: int = Field(
        ge=0,
        le=100,
        description="Score from the most recent quiz attempt (0-100).",
    )

    # Attention telemetry is optional because webcam data
    # may not be available for every student or quiz attempt.
    attention_score: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description=(
            "Normalized attention score between 0.0 and 1.0, "
            "or None when attention telemetry is unavailable."
        ),
    )

    yawning: bool = Field(
        description="Whether yawning was observed.",
    )

    looking_away: bool = Field(
        description="Whether the student was observed looking away.",
    )

    difficulty: str = Field(
        min_length=1,
        description="The current content difficulty.",
    )

    response_time: float = Field(
        ge=0.0,
        description="Response time in seconds.",
    )

    hints_used: int = Field(
        ge=0,
        description="Number of hints used.",
    )

    lesson_attempts: int = Field(
        ge=0,
        description="Number of attempts for the current lesson.",
    )

    completed_lessons: int = Field(
        ge=0,
        description="Number of lessons completed so far.",
    )

    @field_validator("subject", "topic", "lesson", "difficulty")
    @classmethod
    def _strip_and_require_non_blank(
        cls,
        value: str,
        info: ValidationInfo,
    ) -> str:
        """Remove surrounding whitespace and reject blank values."""

        stripped = value.strip()

        if not stripped:
            raise ValueError(
                f"{info.field_name} must not be blank."
            )

        return stripped

    @field_validator("difficulty")
    @classmethod
    def _validate_difficulty(cls, value: str) -> str:
        """Normalize difficulty and allow only supported levels."""

        normalized = value.upper()

        if normalized not in _ALLOWED_DIFFICULTIES:
            raise ValueError(
                f"difficulty must be one of "
                f"{sorted(_ALLOWED_DIFFICULTIES)}, "
                f"got {value!r}."
            )

        return normalized