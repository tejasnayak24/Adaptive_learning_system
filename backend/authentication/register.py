from flask import Blueprint, request, jsonify

from database.database import SessionLocal
from database.models import Student

from werkzeug.security import generate_password_hash


register_bp = Blueprint(
    "register",
    __name__
)


@register_bp.route("/register", methods=["POST"])
def register():

    db = SessionLocal()

    try:

        data = request.json

        name = data["name"]
        email = data["email"]
        password = data["password"]
        age = data["age"]
        grade = data["grade"]


        existing_student = db.query(Student).filter(
            Student.email == email
        ).first()


        if existing_student:

            return jsonify({
                "message": "Email already registered"
            }), 400



        hashed_password = generate_password_hash(password)


        student = Student(

            name=name,
            email=email,
            password=hashed_password,
            age=age,
            grade=grade

        )


        db.add(student)
        db.commit()
        db.refresh(student)


        return jsonify({

            "message": "Registration successful",
            "student_id": student.id

        }), 201


    finally:

        db.close()