from sqlalchemy.orm import Session

from app.auth.password import hash_password, verify_password
from app.models.student import Student
from app.schemas.auth import LoginRequest, RegisterRequest


class StudentService:

    @staticmethod
    def get_student_by_email(
        db: Session,
        email: str,
    ):
        return (
            db.query(Student)
            .filter(Student.email == email)
            .first()
        )

    @staticmethod
    def get_student_by_id(
        db: Session,
        student_id: int,
    ):
        return (
            db.query(Student)
            .filter(Student.id == student_id)
            .first()
        )

    @staticmethod
    def register_student(
        db: Session,
        student: RegisterRequest,
    ):
        existing = StudentService.get_student_by_email(
            db,
            student.email,
        )

        if existing:
            return None

        new_student = Student(
            name=student.name,
            email=student.email,
            password_hash=hash_password(student.password),
            age=student.age,
        )

        db.add(new_student)
        db.commit()
        db.refresh(new_student)

        return new_student

    @staticmethod
    def authenticate_student(
        db: Session,
        login: LoginRequest,
    ):
        student = StudentService.get_student_by_email(
            db,
            login.email,
        )

        if not student:
            return None

        if not verify_password(
            login.password,
            student.password_hash,
        ):
            return None

        return student