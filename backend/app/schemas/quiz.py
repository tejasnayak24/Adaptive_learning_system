from pydantic import BaseModel
from typing import List


class QuizBase(BaseModel):
    lesson_id: int
    title: str
    total_questions: int
    difficulty: str


class QuizCreate(QuizBase):
    pass


class QuizUpdate(QuizBase):
    pass


class QuizResponse(QuizBase):
    id: int

    class Config:
        from_attributes = True


class QuizStartRequest(BaseModel):
    quiz_id: int


class QuizSubmitRequest(BaseModel):
    student_id: int
    lesson_id: int
    quiz_score: float
    response_time: float
    attention_score: float
    difficulty: str


class QuestionResponse(BaseModel):
    id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str

    class Config:
        from_attributes = True


class QuizStartResponse(BaseModel):
    quiz: QuizResponse
    questions: List[QuestionResponse]


class QuizSubmitResponse(BaseModel):
    success: bool
    message: str