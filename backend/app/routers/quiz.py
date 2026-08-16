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
        "data": {
            "quiz": quiz_data["quiz"],
            "questions": quiz_data["questions"],
        },
    }


@router.get("/quiz/lesson/{lesson_id}")
def get_quizzes_by_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    quizzes = QuizService.get_quizzes_by_lesson(
        db,
        lesson_id,
    )

    return {
        "success": True,
        "message": "Quizzes fetched successfully",
        "data": [
            {
                "id": quiz.id,
                "lesson_id": quiz.lesson_id,
                "title": quiz.title,
                "difficulty": quiz.difficulty,
            }
            for quiz in quizzes
        ],
    }


@router.get("/quiz/{quiz_id}")
def get_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    quiz_data = QuizService.start_quiz(
        db,
        quiz_id,
    )

    if quiz_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found",
        )

    quiz = quiz_data["quiz"]
    questions = quiz_data["questions"]

    return {
        "success": True,
        "message": "Quiz fetched successfully",
        "data": {
            "quiz": {
                "id": quiz.id,
                "lesson_id": quiz.lesson_id,
                "title": quiz.title,
                "difficulty": quiz.difficulty,
            },
            "questions": [
                {
                    "id": question.id,
                    "quiz_id": question.quiz_id,
                    "question": question.question,
                    "option_a": question.option_a,
                    "option_b": question.option_b,
                    "option_c": question.option_c,
                    "option_d": question.option_d,
                    "correct_answer": question.correct_answer,
                }
                for question in questions
            ],
        },
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
        "data": {
            "id": progress.id,
            "student_id": progress.student_id,
            "lesson_id": progress.lesson_id,
            "quiz_score": progress.quiz_score,
            "response_time": progress.response_time,
            "attention_score": progress.attention_score,
            "difficulty": progress.difficulty,
            "completed": progress.completed,
        },
    }