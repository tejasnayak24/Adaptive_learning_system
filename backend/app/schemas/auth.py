from pydantic import BaseModel, ConfigDict, EmailStr


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    age: int


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    success: bool
    message: str
    access_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(from_attributes=True)