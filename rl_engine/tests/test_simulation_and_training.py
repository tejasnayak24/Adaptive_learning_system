import random
import statistics
from pathlib import Path

from rl_engine.core.actions import Action
from rl_engine.core.config import RLConfig
from rl_engine.evaluation.baselines import legacy_rule_policy, make_random_policy
from rl_engine.evaluation.evaluate import evaluate_policy, greedy_policy
from rl_engine.models.student_state import Difficulty
from rl_engine.training.agent import QLearningAgent
from rl_engine.training.environment import LearningEnvironment
from rl_engine.training.simulation import SimulatedStudent
from rl_engine.training.trainer import Trainer

ENGINE = Path(__file__).resolve().parents[1]


def student(seed, **overrides):
    s = SimulatedStudent.sample(random.Random(seed))
    for k, v in overrides.items():
        setattr(s, k, v)
    return s


def test_repeating_a_lesson_can_improve_scores():
    gains = []
    for seed in range(300):
        s = student(seed, mastery=0.3, fatigue=0.0, drowsy=False, difficulty=Difficulty.EASY)
        before = s._take_quiz()
        s.apply(Action.REPEAT_LESSON)
        gains.append(s.current_score - before)
    assert statistics.fmean(gains) > 3
    assert max(gains) > 10


def test_scores_can_also_decline():
    changes = []
    for seed in range(300):
        s = student(seed)
        before = s.current_score
        s.apply(Action.PRACTICE_QUIZ)
        changes.append(s.current_score - before)
    assert min(changes) < 0 < max(changes)


def test_students_differ_and_the_simulator_is_stochastic():
    traits = {(round(s.ability, 3), round(s.focus, 3)) for s in (student(i) for i in range(50))}
    assert len(traits) == 50
    a, b = student(1), student(1)
    a.apply(Action.PRACTICE_QUIZ)
    b.apply(Action.PRACTICE_QUIZ)
    assert a.current_score == b.current_score  # same seed -> reproducible
    runs = set()
    for seed in range(20):
        s = student(seed, mastery=0.5)
        s.apply(Action.PRACTICE_QUIZ)
        runs.add(s.current_score)
    assert len(runs) > 5


def test_attention_and_distraction_change_across_steps():
    s = student(3)
    attention, away = [], []
    for _ in range(30):
        s.apply(Action.PRACTICE_QUIZ)
        attention.append(s.attention)
        away.append(s.looking_away)
    assert max(attention) - min(attention) > 0.1


def test_difficulty_changes_outcomes():
    def mean_score(difficulty):
        return statistics.fmean(
            student(seed, mastery=0.7, difficulty=difficulty)._take_quiz() for seed in range(300)
        )

    assert mean_score(Difficulty.EASY) > mean_score(Difficulty.MEDIUM) > mean_score(Difficulty.HARD)


def test_drowsiness_slows_learning_and_breaks_help():
    def gain(drowsy):
        total = []
        for seed in range(300):
            s = student(seed, mastery=0.5, drowsy=drowsy, fatigue=0.8 if drowsy else 0.0, difficulty=Difficulty.MEDIUM)
            s.apply(Action.PRACTICE_QUIZ)
            total.append(s.mastery - 0.5)
        return statistics.fmean(total)

    assert gain(drowsy=True) < gain(drowsy=False)

    cleared = 0
    for seed in range(200):
        s = student(seed, drowsy=True, fatigue=0.9)
        s.apply(Action.FOCUS_RECOVERY)
        cleared += not s.drowsy
    assert cleared > 150


def test_environment_step_returns_outcome_reward():
    env = LearningEnvironment(random.Random(0))
    state = env.reset(student(0, mastery=0.9, difficulty=Difficulty.HARD))
    next_state, reward, done = env.step(Action.NEXT_LESSON)
    assert next_state.completed_lessons == state.completed_lessons + 1
    assert reward == env.last_breakdown.total
    assert isinstance(done, bool)


def test_short_training_run_learns_better_than_random_and_is_reproducible():
    cfg = RLConfig(training_episodes=1500, epsilon_decay=0.997)
    agent = Trainer(cfg, seed=11).train()
    again = Trainer(cfg, seed=11).train()
    assert agent.q_table == again.q_table

    learned = evaluate_policy("learned", greedy_policy(agent), episodes=150, seed=500_000)
    rand = evaluate_policy("random", make_random_policy(random.Random(0)), episodes=150, seed=500_000)
    assert learned.mean_return > rand.mean_return
    assert learned.constraint_violations == 0


def test_shipped_policy_beats_legacy_rules_and_random():
    agent = QLearningAgent.load_q_table(ENGINE / "q_table.json", RLConfig())
    learned = evaluate_policy("learned", greedy_policy(agent), episodes=200, seed=700_000)
    legacy = evaluate_policy("legacy", legacy_rule_policy, episodes=200, seed=700_000)
    rand = evaluate_policy("random", make_random_policy(random.Random(0)), episodes=200, seed=700_000)
    assert learned.mean_return > legacy.mean_return
    assert learned.mean_return > rand.mean_return
    assert learned.constraint_violations == 0
    # The learned policy actually uses a range of actions, not one rule.
    assert sum(1 for share in learned.action_share.values() if share > 0.01) >= 6
