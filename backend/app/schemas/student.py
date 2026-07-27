from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class StudentBase(BaseModel):
    name: str
    email: EmailStr
    age: int


class StudentCreate(StudentBase):
    password: str


class StudentUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    age: int | None = None

    model_config = ConfigDict(from_attributes=True)


class StudentResponse(StudentBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)