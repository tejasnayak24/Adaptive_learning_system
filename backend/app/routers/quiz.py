from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_student
from app.database.connection import get_db
from app.models.student import Student
from app.schemas.quiz import QuizStartRequest, QuizSubmitRequest
from app.services import curriculum_service as cs
from app.services import monitoring_service as ms
from app.services import telemetry_service
from app.services.grading_service import GradingError
from app.services.quiz_service import QuizService, quiz_to_dict
from app.services.recommendation_service import (
    recommend_for_attempt,
    recommendation_to_dict,
    record_outcome_of_previous,
)
from app.services.rl_service import get_rl_service
from app.utils.response import progress_to_dict

router = APIRouter(tags=["Quiz"])


def _quiz_payload_or_404(db: Session, quiz_id: int, student: Student) -> dict[str, Any]:
    quiz = QuizService.get_quiz_by_id(db, quiz_id)
    if quiz is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found",
        )
    cs.check_lesson_access(student, quiz.lesson)

    return QuizService.start_quiz(db, quiz_id)


@router.post("/quiz/start")
def start_quiz(
    request: QuizStartRequest,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student),
) -> dict[str, Any]:
    return {
        "success": True,
        "message": "Quiz started successfully",
        "data": _quiz_payload_or_404(db, request.quiz_id, student),
    }


@router.get("/quiz/lesson/{lesson_id}")
def get_quizzes_by_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student),
) -> dict[str, Any]:
    from app.models.lesson import Lesson

    lesson = db.get(Lesson, lesson_id)
    if lesson is not None:
        cs.check_lesson_access(student, lesson)
    quizzes = QuizService.get_quizzes_by_lesson(db, lesson_id)

    return {
        "success": True,
        "message": "Quizzes fetched successfully",
        "data": [quiz_to_dict(quiz) for quiz in quizzes],
    }


@router.get("/quiz/{quiz_id}")
def get_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student),
) -> dict[str, Any]:
    """Quiz questions for answering. Correct answers are never included."""
    return {
        "success": True,
        "message": "Quiz fetched successfully",
        "data": _quiz_payload_or_404(db, quiz_id, student),
    }


@router.post("/quiz/submit")
def submit_quiz(
    request: QuizSubmitRequest,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student),
) -> dict[str, Any]:
    """Grade the submitted answers on the server and store the attempt.

    The response contains the server-computed result, the per-question
    review (correct answers are revealed only now, after submission) and
    the adaptive recommendation -- or ``None`` when the attempt had no
    camera telemetry.
    """
    # The attempt always belongs to the authenticated student.
    if request.student_id is not None and request.student_id != student.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot submit a quiz for another student",
        )

    quiz = QuizService.get_quiz_by_id(db, request.quiz_id)
    if quiz is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found",
        )
    cs.check_lesson_access(student, quiz.lesson)

    # Camera monitoring is mandatory: the attempt must belong to one of the
    # student's own monitored sessions that has not ended.
    try:
        monitoring = ms.owned_session(db, student, request.monitoring_session_id)
    except ms.MonitoringError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc
    if monitoring.status == ms.ENDED:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The monitoring session has ended; restart camera monitoring and retake the quiz",
        )

    # Measured by the paired camera agent during this attempt (None when
    # nothing was measured). Never taken from the browser.
    camera = telemetry_service.attempt_metrics(student.id, monitoring.id)

    try:
        progress, grading = QuizService.grade_and_record(
            db,
            student_id=student.id,
            quiz=quiz,
            answers=request.answers,
            response_time=request.response_time,
            hints_used=request.hints_used,
            attention_score=camera["attention_score"],
            yawning=camera["yawning"],
            looking_away=camera["looking_away"],
            drowsy=camera["drowsy"],
            monitoring_session_id=monitoring.id,
            attempt_mode=request.mode,
        )
    except GradingError as exc:
        db.rollback()
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    # This attempt is the observed outcome of the previous recommendation.
    record_outcome_of_previous(db, progress)

    recommendation = recommend_for_attempt(db, get_rl_service(), progress)

    db.commit()
    db.refresh(progress)
    if recommendation is not None:
        db.refresh(recommendation)

    explanations = {
        q.id: q.explanation for q in QuizService.get_questions_by_quiz(db, quiz.id)
    }

    return {
        "success": True,
        "message": "Quiz submitted successfully",
        "data": {
            "progress": progress_to_dict(progress),
            "grading": {
                "score": grading.score,
                "correct_count": grading.correct_count,
                "total_questions": grading.total_questions,
                "results": [
                    {
                        "question_id": r.question_id,
                        "selected_answer": r.selected_answer,
                        "correct_answer": r.correct_answer,
                        "is_correct": r.is_correct,
                        # Revealed only now, after submission.
                        "explanation": explanations.get(r.question_id),
                    }
                    for r in grading.results
                ],
            },
            "recommendation": recommendation_to_dict(recommendation),
            # Where the recommended action leads, within this grade and subject.
            "next_step": cs.recommendation_next_step(
                db, quiz.lesson, quiz, recommendation.action if recommendation else None
            ),
            "recommendation_status": (
                "available" if recommendation is not None else "telemetry_unavailable"
            ),
        },
    }
