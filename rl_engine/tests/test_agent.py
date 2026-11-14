import math
import random

import pytest

from conftest import make_state
from rl_engine.core.actions import Action
from rl_engine.core.config import RLConfig
from rl_engine.core.constraints import blocked_actions, permitted_actions
from rl_engine.evaluation.baselines import legacy_rule_policy
from rl_engine.models.recommendation import Recommendation
from rl_engine.models.student_state import Difficulty
from rl_engine.training.agent import (
    POLICY_FALLBACK,
    POLICY_NEAREST,
    POLICY_Q_LEARNING,
    QLearningAgent,
)


def agent_with(state, values: dict[Action, float], visits: int = 50, config: RLConfig | None = None):
    agent = QLearningAgent(config or RLConfig(), rng=random.Random(0))
    key = agent.state_key(state)
    agent._ensure_state(key)
    for action in Action:
        agent.q_table[key][action] = values.get(action, -1.0)
        agent.visits[key][action] = visits
    return agent


# ---------------------------------------------------------------------------
# The core Phase 4 property: the Q-table decides.
# ---------------------------------------------------------------------------
def test_changing_q_values_changes_the_recommendation():
    state = make_state(current_quiz_score=65, previous_quiz_score=60)
    permitted = permitted_actions(state)
    assert Action.PRACTICE_QUIZ in permitted and Action.SHOW_WORKED_EXAMPLE in permitted

    a = agent_with(state, {Action.PRACTICE_QUIZ: 2.0, Action.SHOW_WORKED_EXAMPLE: 1.0})
    b = agent_with(state, {Action.PRACTICE_QUIZ: 1.0, Action.SHOW_WORKED_EXAMPLE: 2.0})

    assert a.decide(state).action == Action.PRACTICE_QUIZ
    assert b.decide(state).action == Action.SHOW_WORKED_EXAMPLE
    # Same state, same permitted actions -- only the learned values differ.
    assert permitted_actions(state) == permitted


def test_decision_differs_from_legacy_rules_when_q_table_prefers_another_action():
    # Legacy rules always said REPEAT_LESSON below 70%.
    state = make_state(current_quiz_score=55, previous_quiz_score=55)
    assert legacy_rule_policy(state) == Action.REPEAT_LESSON
    agent = agent_with(state, {Action.SHOW_WORKED_EXAMPLE: 3.0, Action.REPEAT_LESSON: 1.0})
    decision = agent.decide(state)
    assert decision.action == Action.SHOW_WORKED_EXAMPLE
    assert decision.policy == POLICY_Q_LEARNING


@pytest.mark.parametrize("action", list(Action))
def test_every_one_of_the_11_actions_can_be_selected(action):
    if action in (Action.SKIP_TO_ADVANCED_TOPIC, Action.QUICK_CHALLENGE, Action.INCREASE_DIFFICULTY):
        state = make_state(current_quiz_score=95, previous_quiz_score=90, difficulty=Difficulty.MEDIUM)
    else:
        state = make_state(current_quiz_score=55, previous_quiz_score=55, difficulty=Difficulty.MEDIUM)
    assert action in permitted_actions(state)
    decision = agent_with(state, {action: 5.0}).decide(state)
    assert decision.action == action
    assert isinstance(decision.to_recommendation(), Recommendation)
    assert decision.explanation.strip()


# ---------------------------------------------------------------------------
# Safety constraints filter, they do not choose.
# ---------------------------------------------------------------------------
def test_blocked_action_is_never_chosen_even_with_highest_q():
    state = make_state(current_quiz_score=30, difficulty=Difficulty.EASY)
    agent = agent_with(state, {Action.NEXT_LESSON: 100.0, Action.SHOW_WORKED_EXAMPLE: 1.0})
    decision = agent.decide(state)
    assert decision.action == Action.SHOW_WORKED_EXAMPLE
    assert "NEXT_LESSON" in decision.blocked
    assert "NEXT_LESSON" not in decision.q_values


def test_training_exploration_never_picks_blocked_actions():
    state = make_state(current_quiz_score=30, difficulty=Difficulty.HARD, drowsy=True)
    agent = QLearningAgent(RLConfig(), rng=random.Random(1))
    agent.epsilon = 1.0
    chosen = {agent.choose_action(state) for _ in range(500)}
    assert chosen == set(permitted_actions(state))
    assert not chosen & blocked_actions(state).keys()


# ---------------------------------------------------------------------------
# Exploration vs exploitation
# ---------------------------------------------------------------------------
def test_epsilon_greedy_explores_and_exploits():
    state = make_state(current_quiz_score=65)
    agent = agent_with(state, {Action.PRACTICE_QUIZ: 5.0})
    agent.epsilon = 0.0
    assert {agent.choose_action(state) for _ in range(200)} == {Action.PRACTICE_QUIZ}
    agent.epsilon = 1.0
    assert len({agent.choose_action(state) for _ in range(500)}) > 5


def test_epsilon_decay_stops_at_minimum():
    agent = QLearningAgent(RLConfig(epsilon=1.0, epsilon_decay=0.5, min_epsilon=0.1))
    for _ in range(10):
        agent.decay_epsilon()
    assert agent.epsilon == 0.1


def test_runtime_decision_is_greedy_and_read_only():
    state = make_state(current_quiz_score=65)
    agent = agent_with(state, {Action.PRACTICE_QUIZ: 2.0, Action.REPEAT_LESSON: 1.9})
    snapshot = {k: dict(v) for k, v in agent.q_table.items()}
    unseen = make_state(current_quiz_score=10, attention_score=0.1, drowsy=True, difficulty=Difficulty.HARD)
    results = {agent.decide(state).action for _ in range(100)}
    agent.decide(unseen)
    assert results == {Action.PRACTICE_QUIZ}
    assert {k: dict(v) for k, v in agent.q_table.items()} == snapshot  # nothing learned or added


# ---------------------------------------------------------------------------
# Q-learning update rule
# ---------------------------------------------------------------------------
def test_q_learning_update_matches_the_equation():
    cfg = RLConfig(learning_rate=0.1, discount_factor=0.9)
    s = make_state(current_quiz_score=65)
    s2 = make_state(current_quiz_score=85, previous_quiz_score=65)
    agent = QLearningAgent(cfg)
    k, k2 = agent.state_key(s), agent.state_key(s2)
    agent._ensure_state(k)
    agent._ensure_state(k2)
    agent.q_table[k][Action.PRACTICE_QUIZ] = 1.0
    agent.q_table[k2][Action.NEXT_LESSON] = 4.0
    # DECREASE_DIFFICULTY is blocked in s2 (score >= 80); its value must be ignored.
    agent.q_table[k2][Action.DECREASE_DIFFICULTY] = 50.0

    agent.update(s, Action.PRACTICE_QUIZ, 2.0, s2, done=False)
    expected = 1.0 + 0.1 * (2.0 + 0.9 * 4.0 - 1.0)
    assert agent.q_table[k][Action.PRACTICE_QUIZ] == pytest.approx(expected)
    assert agent.visits[k][Action.PRACTICE_QUIZ] == 1

    agent.update(s, Action.PRACTICE_QUIZ, 2.0, s2, done=True)
    assert agent.q_table[k][Action.PRACTICE_QUIZ] == pytest.approx(expected + 0.1 * (2.0 - expected))


# ---------------------------------------------------------------------------
# Unseen states and confidence
# ---------------------------------------------------------------------------
def test_untested_actions_are_not_tried_on_students():
    state = make_state(current_quiz_score=65)
    agent = agent_with(state, {Action.PRACTICE_QUIZ: 1.0, Action.REPEAT_LESSON: 0.5})
    key = agent.state_key(state)
    agent.q_table[key][Action.QUICK_CHALLENGE] = 10.0
    agent.visits[key][Action.QUICK_CHALLENGE] = 0
    decision = agent.decide(state)
    assert decision.action == Action.PRACTICE_QUIZ
    assert "QUICK_CHALLENGE" in decision.untested


def test_unseen_state_uses_nearest_learned_state():
    learned = make_state(current_quiz_score=65, attention_score=0.8)
    agent = agent_with(learned, {Action.PROVIDE_HINT: 3.0})
    neighbour = make_state(current_quiz_score=65, attention_score=0.5)  # differs in one feature
    decision = agent.decide(neighbour)
    assert decision.policy == POLICY_NEAREST
    assert decision.action == Action.PROVIDE_HINT
    assert decision.source_state_key == agent.state_key(learned)
    assert decision.confidence <= 0.5


def test_completely_unseen_state_falls_back_safely():
    agent = QLearningAgent(RLConfig())
    decision = agent.decide(make_state(current_quiz_score=20))
    assert decision.policy == POLICY_FALLBACK
    assert decision.action == Action.REPEAT_LESSON
    assert decision.confidence == 0.0
    assert "not covered during training" in decision.explanation


def test_confidence_is_a_bounded_heuristic():
    state = make_state(current_quiz_score=65)
    close = agent_with(state, {Action.PRACTICE_QUIZ: 1.0, Action.REPEAT_LESSON: 0.95}).decide(state)
    clear = agent_with(state, {Action.PRACTICE_QUIZ: 3.0, Action.REPEAT_LESSON: 0.0}).decide(state)
    rare = agent_with(state, {Action.PRACTICE_QUIZ: 3.0, Action.REPEAT_LESSON: 0.0}, visits=6).decide(state)
    assert 0.0 <= close.confidence < clear.confidence <= 1.0
    assert rare.confidence < clear.confidence  # less training support
    # margin 3.0 (3.0 vs 0.0), confidence_scale 1.0, full support (50 >= 30 visits)
    assert clear.margin == pytest.approx(3.0)
    assert clear.confidence == pytest.approx(round(1 - math.exp(-3.0), 4))
    assert close.margin == pytest.approx(0.05)
    assert close.as_dict()["confidence_kind"] == "heuristic_decision_strength"


def test_single_tested_action_is_not_reported_as_certain():
    state = make_state(current_quiz_score=65)
    agent = agent_with(state, {Action.PRACTICE_QUIZ: 3.0})
    key = agent.state_key(state)
    for action in Action:
        if action != Action.PRACTICE_QUIZ:
            agent.visits[key][action] = 0
    decision = agent.decide(state)
    assert decision.action == Action.PRACTICE_QUIZ and decision.runner_up is None
    assert decision.confidence == 0.5


def test_recommend_returns_recommendation():
    state = make_state(current_quiz_score=65)
    rec = agent_with(state, {Action.PRACTICE_QUIZ: 1.0}).recommend(state)
    assert rec.action == Action.PRACTICE_QUIZ and 0.0 <= rec.confidence <= 1.0
