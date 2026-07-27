from pydantic import BaseModel


class ProgressBase(BaseModel):
    student_id: int
    lesson_id: int
    quiz_score: float
    response_time: float
    attention_score: float
    difficulty: str
    completed: bool


class ProgressCreate(ProgressBase):
    pass


class ProgressUpdate(BaseModel):
    quiz_score: float
    response_time: float
    attention_score: float
    difficulty: str
    completed: bool


class ProgressResponse(ProgressBase):
    id: int

    class Config:
        from_attributes = True