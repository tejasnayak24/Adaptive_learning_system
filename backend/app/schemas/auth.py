from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    # New accounts only (login does not re-check, so existing accounts keep
    # working). 72 is bcrypt's input limit.
    password: str = Field(min_length=8, max_length=72)
    age: int = Field(ge=5, le=100)
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