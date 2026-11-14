import random

from conftest import make_state
from rl_engine.core.actions import Action
from rl_engine.core.constraints import NEVER_BLOCKED, blocked_actions, permitted_actions
from rl_engine.models.student_state import Difficulty


def test_difficulty_bounds():
    assert Action.INCREASE_DIFFICULTY in blocked_actions(make_state(difficulty=Difficulty.HARD, current_quiz_score=95))
    assert Action.DECREASE_DIFFICULTY in blocked_actions(make_state(difficulty=Difficulty.EASY, current_quiz_score=20))


def test_failing_student_cannot_advance_or_get_harder():
    blocked = blocked_actions(make_state(current_quiz_score=30, difficulty=Difficulty.EASY))
    assert {Action.NEXT_LESSON, Action.INCREASE_DIFFICULTY, Action.SKIP_TO_ADVANCED_TOPIC} <= blocked.keys()
    assert all(isinstance(reason, str) and reason for reason in blocked.values())


def test_mastery_blocks_decrease_and_skip_needs_90():
    s = make_state(current_quiz_score=85, difficulty=Difficulty.MEDIUM)
    assert Action.DECREASE_DIFFICULTY in blocked_actions(s)
    assert Action.SKIP_TO_ADVANCED_TOPIC in blocked_actions(s)
    assert Action.SKIP_TO_ADVANCED_TOPIC not in blocked_actions(make_state(current_quiz_score=95))


def test_drowsiness_blocks_challenging_actions():
    s = make_state(current_quiz_score=95, drowsy=True)
    assert {Action.QUICK_CHALLENGE, Action.INCREASE_DIFFICULTY, Action.SKIP_TO_ADVANCED_TOPIC} <= blocked_actions(s).keys()
    assert Action.FOCUS_RECOVERY in permitted_actions(s)


def test_constraints_only_filter_and_never_decide():
    rng = random.Random(0)
    for _ in range(2000):
        s = make_state(
            current_quiz_score=rng.randint(0, 100),
            previous_quiz_score=rng.randint(0, 100),
            attention_score=rng.random(),
            yawning=rng.random() < 0.5,
            looking_away=rng.random() < 0.5,
            drowsy=rng.random() < 0.5,
            difficulty=rng.choice(list(Difficulty)),
        )
        permitted = set(permitted_actions(s))
        assert NEVER_BLOCKED <= permitted
        assert len(permitted) >= 6


def test_every_action_is_permitted_somewhere():
    excellent = make_state(current_quiz_score=95, previous_quiz_score=90, difficulty=Difficulty.MEDIUM)
    struggling = make_state(current_quiz_score=55, difficulty=Difficulty.MEDIUM)
    allowed = set(permitted_actions(excellent)) | set(permitted_actions(struggling))
    assert allowed == set(Action)
