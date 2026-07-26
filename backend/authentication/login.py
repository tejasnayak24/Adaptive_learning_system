from flask import Blueprint, request, jsonify

from database.database import SessionLocal
from database.models import Student

from werkzeug.security import check_password_hash


login_bp = Blueprint(
    "login",
    __name__
)



@login_bp.route("/login", methods=["POST"])
def login():

    db = SessionLocal()

    try:

        data = request.json

        email = data["email"]

        password = data["password"]


        student = db.query(Student).filter(
            Student.email == email
        ).first()



        if not student:

            return jsonify({

                "message": "Student not found"

            }),404



        if check_password_hash(
            student.password,
            password
        ):


            return jsonify({

                "message": "Login successful",
                "student_id": student.id,
                "name": student.name

            })


        else:

            return jsonify({

                "message": "Invalid password"

            }),401


    finally:

        db.close()