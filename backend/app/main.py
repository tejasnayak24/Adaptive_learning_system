import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

# Validate required environment variables before anything touches the
# database or signs tokens, so a misconfiguration fails with a clear
# message instead of an obscure SQLAlchemy/JWT error.
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

# Import all models so SQLAlchemy registers them. The schema itself is
# managed by Alembic migrations (backend/migrations); run
# `alembic upgrade head` from backend/ before starting the API.
from app.models.student import Student  # noqa: E402,F401
from app.models.lesson import Lesson  # noqa: E402,F401
from app.models.quiz import Quiz  # noqa: E402,F401
from app.models.question import Question  # noqa: E402,F401
from app.models.progress import Progress  # noqa: E402,F401
from app.models.session import LearningSession  # noqa: E402,F401
from app.models.reward import RewardHistory  # noqa: E402,F401

from app.routers import (  # noqa: E402
    auth,
    lesson,
    progress,
    quiz,
    integration,
    rl,
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


# Include routers
app.include_router(auth.router)
app.include_router(lesson.router)
app.include_router(quiz.router)
app.include_router(progress.router)
app.include_router(integration.router)
app.include_router(rl.router)
