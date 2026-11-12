from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    age: int
    # School grade 6-10. Optional so older clients keep working; students
    # without a grade are asked to choose one before browsing lessons.
    grade: int | None = Field(default=None, ge=6, le=10)


class GradeUpdate(BaseModel):
    grade: int = Field(ge=6, le=10)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    success: bool
    message: str
    access_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(from_attributes=True)