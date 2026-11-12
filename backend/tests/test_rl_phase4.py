"""Phase 4: the learned Q-table, not hand-written rules, drives recommendations."""

import pytest

from app.routers import rl as rl_router
from app.services.recommendation_service import infer_followed, outcome_breakdown
from app.services.rl_service import RLService, get_rl_service
from rl_engine.core.actions import Action
from rl_engine.core.config import RLConfig
from rl_engine.models.student_state import Difficulty, StudentState
from rl_engine.training.agent import QLearningAgent

STATE = {
    "subject": "Science",
    "topic": "Force and Motion",
    "lesson": "Force and Motion",
    "previous_quiz_score": 60,
    "current_quiz_score": 62,
    "attention_score": 0.8,
    "yawning": False,
    "looking_away": False,
    "drowsy": False,
    "difficulty": "MEDIUM",
    "response_time": 30.0,
    "hints_used": 0,
    "lesson_attempts": 1,
    "completed_lessons": 1,
}


def _table(tmp_path, name, preferred: Action, extra: dict | None = None):
    """Write a Q-table whose only learned state is STATE, preferring ``preferred``."""
    agent = QLearningAgent(RLConfig())
    state = StudentState(**{**STATE, "difficulty": Difficulty.MEDIUM})
    key = agent.state_key(state)
    agent._ensure_state(key)
    for action in Action:
        agent.q_table[key][action] = 0.0
        agent.visits[key][action] = 40
    agent.q_table[key][preferred] = 2.0
    for action, value in (extra or {}).items():
        agent.q_table[key][action] = value
    path = tmp_path / name
    agent.save_q_table(path, {"trained_at": "test"})
    return path


@pytest.fixture()
def use_table(monkeypatch):
    def install(path):
        service = RLService(path)
        monkeypatch.setattr(rl_router, "get_rl_service", lambda: service)
        return service

    return install


def test_changing_the_q_table_changes_the_api_recommendation(client, auth, tmp_path, use_table):
    headers, _ = auth
    use_table(_table(tmp_path, "a.json", Action.PRACTICE_QUIZ))
    first = client.post("/rl/recommend", json=STATE, headers=headers).json()

    use_table(_table(tmp_path, "b.json", Action.SHOW_WORKED_EXAMPLE))
    second = client.post("/rl/recommend", json=STATE, headers=headers).json()

    assert first["action"] == "PRACTICE_QUIZ"
    assert second["action"] == "SHOW_WORKED_EXAMPLE"
    assert first["policy"] == second["policy"] == "q_learning"
    assert first["blocked_actions"] == second["blocked_actions"]  # same permitted set
    assert first["q_values"]["PRACTICE_QUIZ"] == 2.0


def test_api_never_returns_a_blocked_action(client, auth, tmp_path, use_table):
    headers, _ = auth
    failing = {**STATE, "current_quiz_score": 30, "previous_quiz_score": 30}
    agent = QLearningAgent(RLConfig())
    state = StudentState(**{**failing, "difficulty": Difficulty.MEDIUM})
    key = agent.state_key(state)
    agent._ensure_state(key)
    for action in Action:
        agent.visits[key][action] = 40
    agent.q_table[key][Action.NEXT_LESSON] = 99.0
    agent.q_table[key][Action.SHOW_WORKED_EXAMPLE] = 1.0
    path = tmp_path / "blocked.json"
    agent.save_q_table(path)
    use_table(path)

    body = client.post("/rl/recommend", json=failing, headers=headers).json()
    assert body["action"] == "SHOW_WORKED_EXAMPLE"
    assert "NEXT_LESSON" in body["blocked_actions"]


def test_unseen_state_is_handled_safely(client, auth, tmp_path, use_table):
    headers, _ = auth
    use_table(_table(tmp_path, "one-state.json", Action.PRACTICE_QUIZ))
    far = {**STATE, "current_quiz_score": 10, "previous_quiz_score": 40, "attention_score": 0.1,
           "drowsy": True, "difficulty": "HARD", "hints_used": 5, "lesson_attempts": 6}
    body = client.post("/rl/recommend", json=far, headers=headers).json()
    assert body["policy"] == "fallback"
    assert body["action"] == "REPEAT_LESSON"
    assert body["confidence"] == 0.0


def test_drowsiness_reaches_the_rl_state(client, auth):
    headers, _ = auth
    alert = client.post("/rl/recommend", json=STATE, headers=headers).json()
    drowsy = client.post("/rl/recommend", json={**STATE, "drowsy": True}, headers=headers).json()
    assert alert["state_key"][5] == 0 and drowsy["state_key"][5] == 2  # fatigue feature
    assert "QUICK_CHALLENGE" in drowsy["blocked_actions"]


def test_model_info_reports_offline_training(client, auth):
    headers, _ = auth
    data = client.get("/rl/model", headers=headers).json()["data"]
    assert data["state_key_version"] == 3
    assert data["model_version"].startswith("v3-")
    assert data["training"] == "offline_simulation"
    assert data["online_updates"] is False
    assert client.get("/rl/model").status_code == 401


def test_shipped_table_is_loaded_and_drives_decisions():
    service = get_rl_service()
    decision = service.decide(STATE)
    assert decision.policy in ("q_learning", "q_learning_nearest_state")
    assert decision.detail["q_values"]  # learned values were compared
    assert decision.recommendation.action.name in decision.detail["q_values"]


class _P:
    def __init__(self, lesson_id, difficulty, score, attention=None, drowsy=None):
        self.lesson_id = lesson_id
        self.difficulty = difficulty
        self.quiz_score = score
        self.attention_score = attention
        self.drowsy = drowsy


def test_observed_reward_matches_engine_and_handles_missing_camera_values():
    before, after = _P(1, "Easy", 50), _P(1, "Easy", 70)
    b = outcome_breakdown(before, after)
    assert b.learning_gain == 2.0 and b.engagement_change == 0.0 and b.total == 1.5

    advanced = outcome_breakdown(_P(1, "Medium", 85), _P(2, "Easy", 40))
    assert advanced.lesson_completion == 3.0  # 85% on MEDIUM counts as mastered


@pytest.mark.parametrize(
    "action, before, after, expected",
    [
        ("NEXT_LESSON", _P(1, "Easy", 80), _P(2, "Easy", 60), True),
        ("NEXT_LESSON", _P(1, "Easy", 80), _P(1, "Easy", 60), False),
        ("INCREASE_DIFFICULTY", _P(1, "Easy", 80), _P(1, "Medium", 70), True),
        ("DECREASE_DIFFICULTY", _P(1, "Hard", 30), _P(1, "Hard", 40), False),
        ("REPEAT_LESSON", _P(1, "Easy", 40), _P(1, "Easy", 60), True),
        ("FOCUS_RECOVERY", _P(1, "Easy", 40), _P(1, "Easy", 60), None),
    ],
)
def test_followed_is_inferred_only_when_observable(action, before, after, expected):
    assert infer_followed(action, before, after) is expected
