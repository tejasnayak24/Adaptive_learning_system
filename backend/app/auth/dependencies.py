from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.jwt_handler import verify_access_token
from app.database.connection import get_db
from app.models.student import Student

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def _unauthorized(detail: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_user(
    token: str = Depends(oauth2_scheme),
):
    """Return the decoded JWT payload (kept for backward compatibility)."""
    payload = verify_access_token(token)

    if payload is None:
        raise _unauthorized("Invalid or expired token")

    return payload


def get_current_student(
    payload: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Student:
    """Resolve the token's subject to the authenticated Student record.

    The token's ``sub`` claim holds the student's integer id as a string.
    A token whose student no longer exists is treated as invalid.
    """
    try:
        student_id = int(payload.get("sub"))
    except (TypeError, ValueError):
        raise _unauthorized("Invalid token subject")

    student = db.get(Student, student_id)

    if student is None:
        raise _unauthorized("Student account not found")

    return student


def require_curriculum_manager(
    student: Student = Depends(get_current_student),
) -> Student:
    """Allow only teachers and admins (e.g. to change lessons)."""
    if not student.can_manage_curriculum:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only teachers or admins can modify the curriculum",
        )

    return student
