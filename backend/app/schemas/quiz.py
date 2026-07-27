from pydantic import BaseModel, ConfigDict


class QuizStartRequest(BaseModel):
    lesson_id: int


class QuizSubmitRequest(BaseModel):
    quiz_id: int
    answers: dict[int, str]
    response_time: float


class QuizResponse(BaseModel):
    id: int
    lesson_id: int
    title: str
    difficulty: str

    model_config = ConfigDict(from_attributes=True)


class QuizResultResponse(BaseModel):
    success: bool
    message: str
    score: float

    model_config = ConfigDict(from_attributes=True)