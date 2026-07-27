from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LessonBase(BaseModel):
    title: str
    topic: str
    difficulty: str
    content: str


class LessonCreate(LessonBase):
    pass


class LessonUpdate(BaseModel):
    title: str | None = None
    topic: str | None = None
    difficulty: str | None = None
    content: str | None = None

    model_config = ConfigDict(from_attributes=True)


class LessonResponse(LessonBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)