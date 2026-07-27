from pydantic import BaseModel, ConfigDict


class ProgressUpdateRequest(BaseModel):
    lesson_id: int
    quiz_score: float
    response_time: float
    attention_score: float
    difficulty: str
    completed: bool


class ProgressResponse(BaseModel):
    id: int
    student_id: int
    lesson_id: int
    quiz_score: float
    response_time: float
    attention_score: float
    difficulty: str
    completed: bool

    model_config = ConfigDict(from_attributes=True)