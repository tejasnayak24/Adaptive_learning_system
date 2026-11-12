import pytest

from conftest import make_state
from rl_engine.core.actions import Action
from rl_engine.training.rewards import (
    REWARD_VERSION,
    STEP_COST,
    RewardCalculator,
    observed_reward,
)


def r(**kw):
    base = dict(score_before=60, score_after=60, difficulty_before="EASY", difficulty_after="EASY")
    return observed_reward(**{**base, **kw})


def test_version():
    assert REWARD_VERSION == 2


def test_no_change_costs_one_step():
    assert r().total == STEP_COST == -0.5


def test_score_improvement_is_positive_and_decline_negative():
    assert r(score_after=80).learning_gain == pytest.approx(2.0)
    assert r(score_after=80).total > 0
    assert r(score_after=40).learning_gain == pytest.approx(-2.0)
    assert r(score_after=40).total < 0


def test_learning_gain_is_clipped():
    assert r(score_before=0, score_after=100).learning_gain == 3.0
    assert r(score_before=100, score_after=0).learning_gain == -3.0


def test_harder_level_with_slightly_lower_score_is_not_punished():
    # 80% on EASY -> 70% on MEDIUM is the same difficulty-adjusted result.
    b = r(score_before=80, score_after=70, difficulty_before="EASY", difficulty_after="MEDIUM")
    assert b.learning_gain == 0.0


def test_lesson_completion_rewards_mastery_and_penalises_premature_advance():
    mastered = r(score_before=92, score_after=40, lessons_advanced=1)
    assert mastered.lesson_completion == 3.0 and mastered.learning_gain == 0.0
    assert mastered.total > 0
    # Not mastered: 0.1 per point still missing to the mastery level.
    assert r(score_before=75, lessons_advanced=1).lesson_completion == pytest.approx(-1.5)
    premature = r(score_before=50, lessons_advanced=1)
    assert premature.lesson_completion == pytest.approx(-4.0) and premature.total < 0
    # Judged on the difficulty-adjusted score: 70% on HARD is mastered,
    # 82% on EASY is not.
    assert r(score_before=70, difficulty_before="HARD", lessons_advanced=1).lesson_completion == 3.0
    assert r(score_before=82, difficulty_before="EASY", lessons_advanced=1).lesson_completion == pytest.approx(-0.8)
    assert r(score_before=92, lessons_advanced=2).lesson_completion == 6.0


def test_frustration_penalty_only_above_easy():
    hard = r(score_before=30, score_after=30, difficulty_before="HARD", difficulty_after="HARD")
    assert hard.frustration == -1.0
    assert r(score_before=30, score_after=30).frustration == 0.0


def test_engagement_rewards_change_not_level():
    # Low but unchanged attention is not penalised.
    assert r(attention_before=0.2, attention_after=0.2).engagement_change == 0.0
    assert r(attention_before=0.3, attention_after=0.7).engagement_change == pytest.approx(0.8)
    assert r(attention_before=0.8, attention_after=0.5).engagement_change == pytest.approx(-0.6)


def test_drowsiness_cleared_vs_persisting():
    assert r(drowsy_before=True, drowsy_after=False).drowsiness == 1.0
    assert r(drowsy_before=True, drowsy_after=True).drowsiness == -1.0
    assert r(drowsy_before=False, drowsy_after=False).drowsiness == 0.0


def test_unknown_camera_values_are_left_out():
    b = r(attention_before=None, attention_after=0.9, drowsy_before=None, drowsy_after=None)
    assert b.engagement_change == 0.0 and b.drowsiness == 0.0


def test_break_pays_off_only_when_needed():
    calc = RewardCalculator()
    tired = make_state(drowsy=True, attention_score=0.3)
    recovered = make_state(drowsy=False, attention_score=0.6)
    alert = make_state(attention_score=0.9)
    assert calc.calculate_reward(tired, Action.FOCUS_RECOVERY, recovered) > 0
    assert calc.calculate_reward(alert, Action.FOCUS_RECOVERY, alert) < 0


def test_breakdown_dict_contains_total():
    d = r(score_after=70).as_dict()
    assert d["total"] == pytest.approx(0.5)
    assert {"learning_gain", "lesson_completion", "step_cost"} <= set(d)


def test_negative_lessons_rejected():
    with pytest.raises(ValueError):
        r(lessons_advanced=-1)
