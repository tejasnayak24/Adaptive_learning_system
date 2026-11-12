import itertools

from conftest import make_state
from rl_engine.core.config import RLConfig
from rl_engine.core.state_encoding import (
    FEATURE_CARDINALITY,
    STATE_FEATURES,
    STATE_KEY_VERSION,
    STATE_SPACE_SIZE,
    encode_state,
    is_valid_key,
)
from rl_engine.models.student_state import Difficulty

CFG = RLConfig()


def key(**kw):
    return dict(zip(STATE_FEATURES, encode_state(make_state(**kw), CFG)))


def test_version_and_size():
    assert STATE_KEY_VERSION == 3
    assert len(STATE_FEATURES) == len(FEATURE_CARDINALITY) == 8
    assert STATE_SPACE_SIZE == 1944


def test_score_and_attention_buckets():
    scores = [key(current_quiz_score=s, previous_quiz_score=s)["score_level"] for s in (0, 49, 50, 79, 80, 100)]
    assert scores == [0, 0, 1, 1, 2, 2]
    attention = [key(attention_score=a)["attention_level"] for a in (0.0, 0.39, 0.4, 0.59, 0.6, 1.0)]
    assert attention == [0, 0, 1, 1, 2, 2]


def test_difficulty_hints_attempts():
    assert [key(difficulty=d)["difficulty"] for d in Difficulty] == [0, 1, 2]
    assert key(hints_used=1)["many_hints"] == 0 and key(hints_used=2)["many_hints"] == 1
    assert key(lesson_attempts=2)["many_attempts"] == 0 and key(lesson_attempts=3)["many_attempts"] == 1


def test_drowsiness_encoding():
    assert key()["fatigue"] == 0
    assert key(yawning=True)["fatigue"] == 1
    assert key(drowsy=True)["fatigue"] == 2
    # Possible drowsiness is the stronger signal and dominates yawning.
    assert key(drowsy=True, yawning=True)["fatigue"] == 2
    assert key(looking_away=True)["looking_away"] == 1


def test_trend_uses_previous_score():
    assert key(previous_quiz_score=70, current_quiz_score=60)["trend"] == 0
    assert key(previous_quiz_score=62, current_quiz_score=60)["trend"] == 1
    assert key(previous_quiz_score=55, current_quiz_score=60)["trend"] == 2


def test_response_time_and_curriculum_position_do_not_change_key():
    base = encode_state(make_state(), CFG)
    assert encode_state(make_state(response_time=2.0), CFG) == base
    assert encode_state(make_state(response_time=500.0), CFG) == base
    assert encode_state(make_state(lesson="Ecosystems", completed_lessons=9), CFG) == base


def test_every_key_in_the_space_is_valid():
    keys = list(itertools.product(*(range(n) for n in FEATURE_CARDINALITY)))
    assert len(keys) == STATE_SPACE_SIZE
    assert all(is_valid_key(k) for k in keys)
    assert not is_valid_key((0, 0, 0, 0, 0, 0, 0))  # version-2 length
    assert not is_valid_key((3, 0, 0, 0, 0, 0, 0, 0))
    assert not is_valid_key((True, 0, 0, 0, 0, 0, 0, 0))
