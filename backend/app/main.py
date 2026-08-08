import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from app.database.connection import Base, engine

# Import all models so SQLAlchemy registers them
from app.models.student import Student
from app.models.lesson import Lesson
from app.models.quiz import Quiz
from app.models.question import Question
from app.models.progress import Progress
from app.models.session import LearningSession
from app.models.reward import RewardHistory

from app.routers import (
    auth,
    lesson,
    progress,
    quiz,
    integration,
    rl,
)


# Create database tables
Base.metadata.create_all(bind=engine)


# Validate required environment variables
required_env_vars = [
    "DATABASE_URL",
    "SECRET_KEY",
    "ALGORITHM",
    "ACCESS_TOKEN_EXPIRE_MINUTES",
]

for var in required_env_vars:
    if not os.getenv(var):
        raise RuntimeError(
            f"Required environment variable '{var}' is not set."
        )


app = FastAPI(
    title="Adaptive Learning System API",
    version="1.0.0",
    description="Backend API for the Intelligent Adaptive Learning System",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://127.0.0.1:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "success": True,
        "message": "Adaptive Learning System API is running",
        "data": {},
    }


# Include routers
app.include_router(auth.router)
app.include_router(lesson.router)
app.include_router(quiz.router)
app.include_router(progress.router)
app.include_router(integration.router)
app.include_router(rl.router)






