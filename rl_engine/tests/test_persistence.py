import json
from pathlib import Path

import pytest

from conftest import make_state
from rl_engine.core.actions import Action
from rl_engine.core.config import RLConfig
from rl_engine.core.state_encoding import STATE_KEY_VERSION
from rl_engine.training.agent import QLearningAgent

ENGINE = Path(__file__).resolve().parents[1]


def trained_agent():
    agent = QLearningAgent(RLConfig())
    s = make_state(current_quiz_score=65)
    s2 = make_state(current_quiz_score=75, previous_quiz_score=65)
    for _ in range(10):
        agent.update(s, Action.PRACTICE_QUIZ, 1.5, s2, done=False)
    return agent, s


def test_save_and_load_round_trip(tmp_path):
    agent, state = trained_agent()
    path = tmp_path / "q.json"
    agent.save_q_table(path, {"note": "test"})

    loaded = QLearningAgent.load_q_table(path, RLConfig())
    assert loaded.q_table == agent.q_table
    assert loaded.visits == agent.visits
    assert loaded.metadata == {"note": "test"}
    assert loaded.decide(state).action == agent.decide(state).action

    payload = json.loads(path.read_text())
    assert payload["state_key_version"] == STATE_KEY_VERSION == 3
    assert payload["actions"] == [a.name for a in Action]


def test_old_version_2_table_is_refused():
    with pytest.raises(ValueError, match="state_key_version 2"):
        QLearningAgent.load_q_table(ENGINE / "archive" / "q_table_v2.json", RLConfig())


def _tamper(tmp_path, change):
    agent, _ = trained_agent()
    path = tmp_path / "q.json"
    agent.save_q_table(path)
    payload = json.loads(path.read_text())
    change(payload)
    path.write_text(json.dumps(payload))
    return path


@pytest.mark.parametrize(
    "change, message",
    [
        (lambda p: p.update(actions=p["actions"][:-1]), "action list"),
        (lambda p: p.update(state_features=p["state_features"][::-1]), "state features"),
        (lambda p: p.update(format="other"), "not an Aegis Q-table"),
        (lambda p: p["entries"][0].update(state_key=[9, 0, 0, 0, 0, 0, 0, 0]), "Invalid state key"),
        (lambda p: p["entries"][0]["values"].pop("NEXT_LESSON"), "every action"),
    ],
)
def test_incompatible_tables_are_refused(tmp_path, change, message):
    with pytest.raises(ValueError, match=message):
        QLearningAgent.load_q_table(_tamper(tmp_path, change), RLConfig())


def test_shipped_q_table_is_version_3_and_validated():
    agent = QLearningAgent.load_q_table(ENGINE / "q_table.json", RLConfig())
    meta = agent.metadata
    assert meta["state_key_version"] == 3 and meta["reward_version"] == 2
    assert all(meta["validation"]["checks"].values())
    assert len(agent.q_table) >= 0.5 * 1944
