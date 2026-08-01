from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.connection import get_db
from app.schemas.quiz import QuizStartRequest, QuizSubmitRequest
from app.services.quiz_service import QuizService

router = APIRouter(tags=["Quiz"])


@router.post("/quiz/start")
def start_quiz(
    request: QuizStartRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    quiz_data = QuizService.start_quiz(
        db,
        request.quiz_id,
    )

    if quiz_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found",
        )

    return {
        "success": True,
        "message": "Quiz started successfully",
        "data": quiz_data,
    }


@router.get("/quiz/{quiz_id}")
def get_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    quiz = QuizService.get_quiz_by_id(
        db,
        quiz_id,
    )

    if quiz is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found",
        )

    return {
        "success": True,
        "message": "Quiz fetched successfully",
        "data": quiz,
    }


@router.post("/quiz/submit")
def submit_quiz(
    request: QuizSubmitRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    progress = QuizService.submit_quiz(
        db=db,
        student_id=request.student_id,
        lesson_id=request.lesson_id,
        quiz_score=request.quiz_score,
        response_time=request.response_time,
        attention_score=request.attention_score,
        difficulty=request.difficulty,
    )

    return {
        "success": True,
        "message": "Quiz submitted successfully",
        "data": progress,
    }