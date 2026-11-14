from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_student
from app.database.connection import get_db
from app.models.student import Student
from app.schemas.quiz import (
    AttemptAnswersRequest,
    AttemptEventsRequest,
    QuizStartRequest,
    QuizSubmitRequest,
)
from app.services import curriculum_service as cs
from app.services import monitoring_service as ms
from app.services import quiz_attempt_service as qa
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


def _attempt_error(db: Session, exc: qa.AttemptError) -> HTTPException:
    # Keep any state change made before the error (e.g. an expired grace
    # period becoming "unverified").
    db.commit()
    headers = {"Retry-After": str(exc.retry_after)} if exc.retry_after else None
    return HTTPException(status_code=exc.status_code, detail=exc.detail, headers=headers)


@router.post("/quiz/start")
def start_quiz(
    request: QuizStartRequest,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student),
) -> dict[str, Any]:
    """Start a server-side attempt, or resume the open one (e.g. after a reload).

    Returns the questions (never the correct answers) and the attempt,
    including any answers saved so far. 429 while the 5-minute cooldown
    after a terminated or abandoned attempt applies.
    """
    payload = _quiz_payload_or_404(db, request.quiz_id, student)
    quiz = QuizService.get_quiz_by_id(db, request.quiz_id)

    if request.monitoring_session_id is not None:
        try:
            ms.owned_session(db, student, request.monitoring_session_id)
        except ms.MonitoringError as exc:
            raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc

    try:
        attempt, created = qa.start_or_resume(
            db, student, quiz, request.mode, request.monitoring_session_id
        )
    except qa.AttemptError as exc:
        raise _attempt_error(db, exc) from exc
    db.commit()
    db.refresh(attempt)

    return {
        "success": True,
        "message": "Quiz started successfully" if created else "Quiz attempt resumed",
        "data": {**payload, "attempt": qa.view(attempt), "resumed": not created},
    }


def _owned_attempt_or_error(db: Session, student: Student, attempt_id: int):
    try:
        return qa.owned_attempt(db, student, attempt_id)
    except qa.AttemptError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc


@router.get("/quiz/attempts/{attempt_id}")
def get_attempt(
    attempt_id: int,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student),
) -> dict[str, Any]:
    """Current state of the student's own attempt (decided by the server)."""
    attempt = _owned_attempt_or_error(db, student, attempt_id)
    qa.refresh(db, attempt)
    db.commit()
    return {"success": True, "message": "Quiz attempt", "data": qa.view(attempt)}


@router.put("/quiz/attempts/{attempt_id}/answers")
def save_attempt_answers(
    attempt_id: int,
    request: AttemptAnswersRequest,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student),
) -> dict[str, Any]:
    """Save in-progress answers. 409 once the attempt has ended (answers frozen)."""
    attempt = _owned_attempt_or_error(db, student, attempt_id)
    try:
        qa.save_answers(db, attempt, request.answers, request.draft_state)
    except qa.AttemptError as exc:
        raise _attempt_error(db, exc) from exc
    db.commit()
    return {"success": True, "message": "Answers saved", "data": qa.view(attempt)}


@router.post("/quiz/attempts/{attempt_id}/events")
def report_attempt_events(
    attempt_id: int,
    request: AttemptEventsRequest,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student),
) -> dict[str, Any]:
    """Page visibility/focus events observed by the browser.

    The server applies the two-strike rule and returns its decision.
    Duplicate or replayed events (same page id and sequence) are ignored.
    """
    attempt = _owned_attempt_or_error(db, student, attempt_id)
    events = [qa.ReportedEvent(**e.model_dump()) for e in request.events]
    qa.report_events(db, attempt, request.page_id, events)
    db.commit()
    return {"success": True, "message": "Events recorded", "data": qa.view(attempt)}


@router.post("/quiz/attempts/{attempt_id}/abandon")
def abandon_attempt(
    attempt_id: int,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student),
) -> dict[str, Any]:
    """The student confirmed leaving the quiz: answers kept, not graded, no violation."""
    attempt = _owned_attempt_or_error(db, student, attempt_id)
    qa.abandon(db, attempt)
    db.commit()
    return {"success": True, "message": "Quiz attempt abandoned", "data": qa.view(attempt)}


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

    # The server-side attempt: only an open attempt that is not away or
    # locked can be graded (the tab-switch rule is enforced here).
    try:
        attempt = qa.attempt_for_submit(db, student, quiz, request.attempt_id)
    except qa.AttemptError as exc:
        raise _attempt_error(db, exc) from exc

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

    qa.mark_submitted(attempt, progress.id, request.answers)

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
            "attempt": qa.view(attempt),
        },
    }
