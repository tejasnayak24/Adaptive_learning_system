import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rl_engine.models.student_state import Difficulty, StudentState  # noqa: E402

BASE = dict(
    subject="Science",
    topic="Force and Motion",
    lesson="Force and Motion",
    previous_quiz_score=60,
    current_quiz_score=60,
    attention_score=0.8,
    yawning=False,
    looking_away=False,
    difficulty=Difficulty.MEDIUM,
    response_time=30.0,
    hints_used=0,
    lesson_attempts=1,
    completed_lessons=2,
    drowsy=False,
)


def make_state(**overrides) -> StudentState:
    return StudentState(**{**BASE, **overrides})
