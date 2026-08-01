"""Action space definition for the Reinforcement Learning Engine.

This module defines the complete set of pedagogical actions the RL agent
can recommend to a student, based on their academic performance and
engagement signals. The action space is intentionally richer than a simple
"increase/decrease difficulty" toggle, allowing the agent to reason about
pacing, remediation, motivation, and engagement recovery independently of
difficulty adjustment.
"""

from enum import Enum


class Action(Enum):
    """The set of learning strategies the RL agent may recommend.

    Each member is assigned an explicit integer value, starting from 0,
    via ``.value``. These integers are used as the stable index for the
    RL agent's action space (e.g. policy/value network output positions,
    action sampling, and Q-value lookups).

    Values are assigned explicitly rather than with ``auto()`` so the
    action-to-index mapping stays fixed regardless of how members are
    reordered or regrouped in this file. A trained policy's output layer
    is order-dependent: if an index silently shifted, the model would
    keep producing the same integers, but they would now point to
    different actions with no error raised anywhere.

    Members are grouped below by pedagogical intent (pacing, difficulty,
    practice, instructional support, engagement, acceleration) purely for
    human readability; the grouping has no effect on behavior.
    """

    # -- Pacing: controls whether the student moves forward or repeats --
    NEXT_LESSON = 0
    # Advance the student to the next lesson in the curriculum sequence.

    REPEAT_LESSON = 1
    # Have the student redo the current lesson, typically after a poor
    # or inconsistent result suggesting the material wasn't retained.

    # -- Difficulty calibration --
    INCREASE_DIFFICULTY = 2
    # Raise the difficulty of upcoming content, typically in response to
    # high performance combined with sustained engagement.

    DECREASE_DIFFICULTY = 3
    # Lower the difficulty of upcoming content, typically in response to
    # repeated struggle at the current difficulty level.

    # -- Practice and assessment --
    PRACTICE_QUIZ = 4
    # Assign a low-stakes practice quiz to reinforce recent material
    # without advancing the curriculum.

    QUICK_CHALLENGE = 5
    # Offer a short, time-boxed challenge to re-engage a student and
    # add variety without the weight of a full quiz.

    # -- Instructional support --
    SHOW_WORKED_EXAMPLE = 6
    # Present a fully worked example before the student attempts the
    # problem again, typically after repeated incorrect attempts.

    PROVIDE_HINT = 7
    # Give a targeted hint for the current problem rather than a full
    # worked example, for a student who is close to the correct approach.

    # -- Engagement and motivation --
    FOCUS_RECOVERY = 8
    # Interrupt the current task with a short attention-recovery
    # activity, triggered by engagement signals such as yawning or
    # looking away rather than by academic performance alone.

    SHOW_REAL_WORLD_APPLICATION = 9
    # Present a real-world application of the current topic to rebuild
    # motivation and relevance for a disengaged but not struggling student.

    # -- Acceleration --
    SKIP_TO_ADVANCED_TOPIC = 10
    # Bypass remaining lessons in the current topic and move the student
    # directly to advanced material, reserved for consistently high
    # performance with strong engagement.

    @classmethod
    def count(cls) -> int:
        """Return the total number of available actions."""
        return len(cls)