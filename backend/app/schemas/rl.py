"""Request schema for the Reinforcement Learning recommendation endpoint.

This module defines the Pydantic model used to validate the request
body the backend receives when asking for an adaptive learning
recommendation. It performs input validation only -- it has no
knowledge of the RL engine's internal types and does not convert,
construct, or reference any of them.
"""

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator

# The set of accepted difficulty values, kept as plain string literals
# (mirroring the RL engine's Difficulty member names) rather than an
# import, so this schema has no dependency on the RL engine.
_ALLOWED_DIFFICULTIES = {"EASY", "MEDIUM", "HARD"}


class RecommendationRequest(BaseModel):
    """The request body for requesting a learning recommendation.

    Contains exactly the fields required to describe a student's current
    academic and engagement state. This model is intentionally decoupled
    from the RL engine: it does not import, construct, or reference
    ``StudentState`` or any other RL engine type, so it can be validated,
    documented, and evolved independently of the RL engine's internals.

    Attributes:
        subject: The subject currently being studied.
        topic: The topic within the subject.
        lesson: The specific lesson within the topic.
        previous_quiz_score: Score (0-100) from the student's previous
            quiz attempt.
        current_quiz_score: Score (0-100) from the student's most recent
            quiz attempt.
        attention_score: Normalized engagement score in [0.0, 1.0].
        yawning: Whether the student was observed yawning.
        looking_away: Whether the student was observed looking away
            from the screen.
        difficulty: The difficulty level of the content currently being
            presented to the student.
        response_time: Time in seconds the student took to respond to
            the current question or lesson interaction.
        hints_used: Number of hints the student has used on the current
            lesson or question.
        lesson_attempts: Number of times the student has attempted the
            current lesson.
        completed_lessons: Total number of lessons the student has
            completed so far.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "subject": "Mathematics",
                "topic": "Quadratic Equations",
                "lesson": "Factoring",
                "previous_quiz_score": 60,
                "current_quiz_score": 75,
                "attention_score": 0.8,
                "yawning": False,
                "looking_away": False,
                "difficulty": "MEDIUM",
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
        description="Score (0-100) from the student's previous quiz attempt.",
    )
    current_quiz_score: int = Field(
        ge=0,
        le=100,
        description="Score (0-100) from the student's most recent quiz attempt.",
    )
    attention_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Normalized engagement score in the range [0.0, 1.0].",
    )
    yawning: bool = Field(
        description="Whether the student was observed yawning.",
    )
    looking_away: bool = Field(
        description="Whether the student was observed looking away from the screen.",
    )
    difficulty: str = Field(
        min_length=1,
        description="The difficulty level of the content currently being presented.",
    )
    response_time: float = Field(
        ge=0.0,
        description="Time in seconds the student took to respond to the current interaction.",
    )
    hints_used: int = Field(
        ge=0,
        description="Number of hints the student has used on the current lesson or question.",
    )
    lesson_attempts: int = Field(
        ge=0,
        description="Number of times the student has attempted the current lesson.",
    )
    completed_lessons: int = Field(
        ge=0,
        description="Total number of lessons the student has completed so far.",
    )

    @field_validator("subject", "topic", "lesson", "difficulty")
    @classmethod
    def _strip_and_require_non_blank(cls, value: str, info: ValidationInfo) -> str:
        """Strip leading/trailing whitespace and reject blank strings.

        Args:
            value: The raw string value supplied for the field.
            info: Validation context identifying which field is being
                validated, used to produce a field-specific message.

        Returns:
            The stripped string.

        Raises:
            ValueError: If the stripped string is empty.
        """
        stripped = value.strip()
        if not stripped:
            raise ValueError(f"{info.field_name} must not be blank.")
        return stripped

    @field_validator("difficulty")
    @classmethod
    def _validate_difficulty(cls, value: str) -> str:
        """Normalize ``difficulty`` to uppercase and validate it.

        Args:
            value: The (already stripped) difficulty string.

        Returns:
            The difficulty string normalized to uppercase.

        Raises:
            ValueError: If the normalized value is not one of "EASY",
                "MEDIUM", or "HARD".
        """
        normalized = value.upper()
        if normalized not in _ALLOWED_DIFFICULTIES:
            raise ValueError(
                f"difficulty must be one of {sorted(_ALLOWED_DIFFICULTIES)}, got {value!r}."
            )
        return normalized