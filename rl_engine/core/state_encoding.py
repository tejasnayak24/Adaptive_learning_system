"""Discretisation of a ``StudentState`` into a tabular Q-learning key.

State-key version 3 (introduced in Phase 4) encodes eight features:

=====  ================  ======================================  ======
Index  Feature           Values                                  Count
=====  ================  ======================================  ======
0      score_level       0 low (<50), 1 medium (50-79),          3
                         2 high (>=80) -- current quiz score
1      attention_level   0 low (<0.40), 1 medium (0.40-0.59),    3
                         2 high (>=0.60) -- camera attention
2      difficulty        0 EASY, 1 MEDIUM, 2 HARD                3
3      many_hints        1 if hints used >= 2                    2
4      many_attempts     1 if lesson attempts >= 3               2
5      fatigue           0 none, 1 yawning, 2 possible           3
                         drowsiness (drowsiness dominates)
6      looking_away      1 if sustained looking away observed    2
7      trend             0 declining (<= -5 points vs previous   3
                         attempt), 1 steady, 2 improving (>= +5)
=====  ================  ======================================  ======

Total: 3*3*3*2*2*3*2*3 = 1944 states.

Changes from version 2 (432 states, 7 features):

* ``drowsy`` added. It is merged with ``yawning`` into one ordered
  *fatigue* feature because both describe tiredness, and possible
  drowsiness (sustained eye closure) is the stronger signal; keeping two
  independent booleans would double the table for a combination
  (drowsy *and* yawning) that calls for the same response.
* ``trend`` added from ``previous_quiz_score``: whether the student is
  improving or declining on this lesson changes what helps next (a
  declining student needs a different explanation; an improving one may
  only need more practice).
* ``response_time`` is deliberately **not** encoded: it depends on the
  number of questions and on reading speed, and in the collected data it
  mostly duplicates information already in the score. Adding even a
  3-level feature would triple the table (5832 states) for little gain.

``lesson``, ``topic``, ``subject`` and ``completed_lessons`` are also not
encoded: the policy is meant to generalise across curriculum content.
"""

from typing import Final

from ..models.student_state import StudentState
from .config import RLConfig

STATE_KEY_VERSION: Final[int] = 3

STATE_FEATURES: Final[tuple[str, ...]] = (
    "score_level",
    "attention_level",
    "difficulty",
    "many_hints",
    "many_attempts",
    "fatigue",
    "looking_away",
    "trend",
)

# Number of values each feature can take, in STATE_FEATURES order.
FEATURE_CARDINALITY: Final[tuple[int, ...]] = (3, 3, 3, 2, 2, 3, 2, 3)

STATE_SPACE_SIZE: Final[int] = 1
for _n in FEATURE_CARDINALITY:
    STATE_SPACE_SIZE *= _n

StateKey = tuple[int, int, int, int, int, int, int, int]

FATIGUE_NONE: Final[int] = 0
FATIGUE_YAWNING: Final[int] = 1
FATIGUE_DROWSY: Final[int] = 2

TREND_DECLINING: Final[int] = 0
TREND_STEADY: Final[int] = 1
TREND_IMPROVING: Final[int] = 2


def bucket_score(score: int, config: RLConfig) -> int:
    if score < config.score_low_threshold:
        return 0
    if score < config.score_high_threshold:
        return 1
    return 2


def bucket_attention(attention: float, config: RLConfig) -> int:
    if attention < config.attention_low_threshold:
        return 0
    if attention < config.attention_high_threshold:
        return 1
    return 2


def fatigue_level(state: StudentState) -> int:
    if state.drowsy:
        return FATIGUE_DROWSY
    if state.yawning:
        return FATIGUE_YAWNING
    return FATIGUE_NONE


def score_trend(state: StudentState, config: RLConfig) -> int:
    delta = state.current_quiz_score - state.previous_quiz_score
    if delta <= -config.trend_threshold:
        return TREND_DECLINING
    if delta >= config.trend_threshold:
        return TREND_IMPROVING
    return TREND_STEADY


def encode_state(state: StudentState, config: RLConfig) -> StateKey:
    """Return the version-3 Q-table key for ``state``."""
    if not isinstance(state, StudentState):
        raise TypeError("state must be an instance of StudentState.")

    return (
        bucket_score(state.current_quiz_score, config),
        bucket_attention(state.attention_score, config),
        state.difficulty.value,
        int(state.hints_used >= config.many_hints_threshold),
        int(state.lesson_attempts >= config.many_attempts_threshold),
        fatigue_level(state),
        int(state.looking_away),
        score_trend(state, config),
    )


def is_valid_key(key: tuple) -> bool:
    """True if ``key`` is a well-formed version-3 state key."""
    if len(key) != len(FEATURE_CARDINALITY):
        return False
    return all(
        isinstance(v, int) and not isinstance(v, bool) and 0 <= v < n
        for v, n in zip(key, FEATURE_CARDINALITY)
    )


def describe_key(key: StateKey) -> dict[str, int]:
    """Map a key to ``{feature_name: value}`` for logs and documentation."""
    return dict(zip(STATE_FEATURES, key))
