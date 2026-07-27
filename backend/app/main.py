import os

from fastapi import FastAPI
from app.routers import auth, lesson, progress, quiz

# Validate required environment variables
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY environment variable is not set."
    )

app = FastAPI(
    title="Adaptive Learning System API",
    version="1.0.0",
    description="Backend API for the Intelligent Adaptive Learning System",
)


@app.get("/")
def root():
    return {
        "success": True,
        "message": "Adaptive Learning System API is running",
        "data": {},
    }


app.include_router(auth.router)
app.include_router(lesson.router)
app.include_router(quiz.router)
app.include_router(progress.router)




