from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.jwt_handler import create_access_token
from app.database.connection import get_db
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.services.student_service import StudentService

router = APIRouter(tags=["Authentication"])


@router.post("/register")
def register(
    student: RegisterRequest,
    db: Session = Depends(get_db),
):
    new_student = StudentService.register_student(db, student)

    if new_student is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    return {
        "success": True,
        "message": "Student registered successfully",
        "data": {
            "id": new_student.id,
            "name": new_student.name,
            "email": new_student.email,
        },
    }


@router.post("/login", response_model=TokenResponse)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db),
):
    student = StudentService.authenticate_student(
        db,
        login_data,
    )

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        {
            "sub": str(student.id),
            "email": student.email,
        }
    )

    return TokenResponse(
        success=True,
        message="Login successful",
        access_token=access_token,
    )


@router.get("/profile")
def profile(
    current_user=Depends(get_current_user),
):
    return {
        "success": True,
        "message": "Profile fetched successfully",
        "data": current_user,
    }