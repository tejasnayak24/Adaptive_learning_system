"""Stochastic simulated students for offline Q-learning training.

Each episode samples a new ``SimulatedStudent`` with its own hidden traits:

=================  ===========  =========================================
Trait              Range        Effect
=================  ===========  =========================================
ability            0.6 - 1.4    multiplies every learning gain
focus              0.35 - 0.95  baseline attention level
fatigue_rate       0.01 - 0.07  fatigue added per study step
distractibility    0.0 - 0.5    chance of sustained looking away
=================  ===========  =========================================

Hidden (latent) variables evolve over the episode: ``mastery`` of the
current lesson (0-1), ``fatigue`` (0-1) and a short-lived attention
``boost``. The agent never sees them -- it only sees the observable
``StudentState`` (quiz score, camera signals, difficulty, counters), just
as in the real system.

Model of learning (all numbers below are the simulator's assumptions):

* **Quiz score** = 100 x (mastery - difficulty offset + 0.1 x (attention -
  0.6) + noise), noise ~ N(0, 0.06), clipped to 0-100. Difficulty offsets
  are -0.05 / +0.05 / +0.15 for EASY / MEDIUM / HARD, i.e. each level
  costs ~10 points at equal mastery (matching the reward's difficulty
  credit). Scores can therefore go **down** as well as up.
* **Learning gain** = base(action, mastery) x ability x effectiveness x
  zone-of-proximal-development factor x (1 - mastery), plus noise. The
  ``(1 - mastery)`` term gives diminishing returns; gains can be negative
  (forgetting/confusion) when the noise is unfavourable.
* **Effectiveness** = (0.35 + 0.65 x attention), halved when the student
  is possibly drowsy, so tired or distracted students learn less from
  the same action.
* **Difficulty fit**: learning is fastest when difficulty matches mastery
  (EASY < 0.45 <= MEDIUM < 0.75 <= HARD): x1.2 at the right level, x0.6
  one level too easy or too hard, x0.3 two levels off. Practising only
  easy material therefore cannot build deep mastery quickly, and content
  far above the student's level is just as unproductive.
* **Action-specific bases** (low / mid / high mastery bands
  < 0.4 / < 0.7 / >= 0.7): worked examples help novices most (0.30 /
  0.14 / 0.02, the "expertise-reversal" effect); repeating the lesson
  helps low and mid mastery (0.18 / 0.20 / 0.06); practice quizzes help
  once the idea is understood (0.04 / 0.18 / 0.10); hints help mid
  mastery (0.08 / 0.12 / 0.03) and lose half their effect after two
  hints (dependence); quick challenges and real-world applications
  mainly raise attention.
* **Fatigue** grows every step (except breaks) at the student's
  ``fatigue_rate``. Possible drowsiness appears with probability
  ``clip((fatigue - 0.45) x 1.6, 0, 0.9)``; yawning with ``fatigue x
  0.7``. ``FOCUS_RECOVERY`` (a short break) cuts fatigue to 30% and clears
  drowsiness with probability 0.85.
* **Attention boosts** from quick challenges (0.25), real-world
  applications (0.35) and breaks (0.20) are multiplied by the attention
  deficit (1 - attention), cut to 30% when the same action is repeated
  back-to-back, halve every step and do not stack -- so novelty helps a
  distracted student but cannot be farmed.
* **Advancing** to the next lesson starts it at EASY difficulty and at
  mastery 0.25-0.45 (scaled by ability) plus 0.3 x (previous mastery - 0.7): moving on with weak
  understanding makes the next lesson harder. Skipping two lessons uses
  a stronger carry-over (0.6 x (mastery - 0.85)), so it only pays off for
  students who have truly mastered the material.

Because outcomes are noisy and depend on hidden traits, the same action
can help one student and not another; the agent has to learn which
actions work *on average* for each observable state.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Final

from ..core.actions import Action
from ..models.student_state import Difficulty, StudentState

# Shape of the simulated curriculum (subject -> topic -> lessons). Topic
# names do not affect the Q-table key; only the number of lessons matters
# (it bounds an episode). Science topics match the seeded Science lessons.
CURRICULUM: Final[dict[str, dict[str, list[str]]]] = {
    "Mathematics": {
        "Number System": ["Integers", "Fractions and Decimals"],
        "Algebra": ["Linear Equations in One Variable"],
    },
    "Science": {
        "Cell Biology": ["Cell Biology"],
        "Human Body Systems": ["Human Body Systems"],
        "Force and Motion": ["Force and Motion"],
        "Matter and Its Properties": ["Matter and Its Properties"],
        "Ecosystems": ["Ecosystems"],
    },
    "Social Science": {
        "Geography": ["Maps and Globes"],
        "Civics": ["Local Government"],
    },
    "English": {
        "Grammar": ["Parts of Speech", "Tenses"],
    },
}

LESSON_SEQUENCE: Final[tuple[tuple[str, str, str], ...]] = tuple(
    (subject, topic, lesson)
    for subject, topics in CURRICULUM.items()
    for topic, lessons in topics.items()
    for lesson in lessons
)
TOTAL_LESSONS: Final[int] = len(LESSON_SEQUENCE)

DIFFICULTY_OFFSET: Final[dict[Difficulty, float]] = {
    Difficulty.EASY: -0.05,
    Difficulty.MEDIUM: 0.05,
    Difficulty.HARD: 0.15,
}
SCORE_NOISE_SD: Final[float] = 0.06
GAIN_NOISE_SD: Final[float] = 0.02
ATTENTION_NOISE_SD: Final[float] = 0.05

# Mastery band -> base gain, per action: (mastery < 0.4, < 0.7, >= 0.7)
BASE_GAIN: Final[dict[Action, tuple[float, float, float]]] = {
    Action.REPEAT_LESSON: (0.18, 0.20, 0.06),
    Action.SHOW_WORKED_EXAMPLE: (0.30, 0.14, 0.02),
    Action.PRACTICE_QUIZ: (0.04, 0.18, 0.10),
    Action.PROVIDE_HINT: (0.08, 0.12, 0.03),
    Action.QUICK_CHALLENGE: (0.01, 0.04, 0.10),
    Action.SHOW_REAL_WORLD_APPLICATION: (0.04, 0.04, 0.03),
    Action.INCREASE_DIFFICULTY: (0.04, 0.04, 0.04),
    Action.DECREASE_DIFFICULTY: (0.04, 0.04, 0.04),
    Action.FOCUS_RECOVERY: (0.0, 0.0, 0.0),
    Action.NEXT_LESSON: (0.0, 0.0, 0.0),
    Action.SKIP_TO_ADVANCED_TOPIC: (0.0, 0.0, 0.0),
}

# Short-lived attention boost per action, multiplied by the attention
# deficit (1 - attention); it halves every step and does not stack.
ATTENTION_BOOST: Final[dict[Action, float]] = {
    Action.QUICK_CHALLENGE: 0.25,
    Action.SHOW_REAL_WORLD_APPLICATION: 0.35,
    Action.FOCUS_RECOVERY: 0.20,
}


def _clip(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def _band(mastery: float) -> int:
    if mastery < 0.4:
        return 0
    if mastery < 0.7:
        return 1
    return 2


def ideal_difficulty(mastery: float) -> Difficulty:
    if mastery < 0.45:
        return Difficulty.EASY
    if mastery < 0.75:
        return Difficulty.MEDIUM
    return Difficulty.HARD


def difficulty_fit(mastery: float, difficulty: Difficulty) -> float:
    gap = difficulty.value - ideal_difficulty(mastery).value
    return {0: 1.2, -1: 0.6, -2: 0.3, 1: 0.6, 2: 0.3}[gap]


@dataclass
class SimulatedStudent:
    """One simulated learner: hidden traits plus hidden and observable state."""

    rng: random.Random
    ability: float
    focus: float
    fatigue_rate: float
    distractibility: float

    lesson_index: int = 0
    mastery: float = 0.3
    fatigue: float = 0.0
    boost: float = 0.0
    difficulty: Difficulty = Difficulty.EASY
    hints_used: int = 0
    lesson_attempts: int = 1
    completed_lessons: int = 0

    attention: float = 0.6
    yawning: bool = False
    looking_away: bool = False
    drowsy: bool = False
    previous_score: int = 0
    current_score: int = 0
    response_time: float = 30.0

    history: list[str] = field(default_factory=list)

    # ------------------------------------------------------------------
    @classmethod
    def sample(cls, rng: random.Random) -> "SimulatedStudent":
        student = cls(
            rng=rng,
            ability=rng.uniform(0.6, 1.4),
            focus=rng.uniform(0.35, 0.95),
            fatigue_rate=rng.uniform(0.01, 0.07),
            distractibility=rng.uniform(0.0, 0.5),
        )
        student.lesson_index = rng.randrange(0, TOTAL_LESSONS - 3)
        student.completed_lessons = student.lesson_index
        student.mastery = rng.uniform(0.1, 0.9)
        student.fatigue = rng.uniform(0.0, 0.5)
        student.difficulty = rng.choice(tuple(Difficulty))
        student.hints_used = rng.randint(0, 2)
        student.lesson_attempts = rng.randint(1, 3)
        student._observe_engagement()
        first = student._take_quiz()
        # A previous attempt on the same lesson, close to the current one.
        student.previous_score = int(_clip(first + rng.choice((-15, -10, -5, 0, 5, 10)), 0, 100))
        student.current_score = first
        return student

    # ------------------------------------------------------------------
    def observe(self) -> StudentState:
        subject, topic, lesson = LESSON_SEQUENCE[min(self.lesson_index, TOTAL_LESSONS - 1)]
        return StudentState(
            subject=subject,
            topic=topic,
            lesson=lesson,
            previous_quiz_score=self.previous_score,
            current_quiz_score=self.current_score,
            attention_score=round(self.attention, 3),
            yawning=self.yawning,
            looking_away=self.looking_away,
            difficulty=self.difficulty,
            response_time=self.response_time,
            hints_used=self.hints_used,
            lesson_attempts=self.lesson_attempts,
            completed_lessons=self.completed_lessons,
            drowsy=self.drowsy,
        )

    @property
    def finished(self) -> bool:
        return self.completed_lessons >= TOTAL_LESSONS

    # ------------------------------------------------------------------
    def apply(self, action: Action) -> None:
        """Advance the hidden and observable state by one action + quiz."""
        rng = self.rng
        self.history.append(action.name)
        effectiveness = (0.35 + 0.65 * self.attention) * (0.5 if self.drowsy else 1.0)

        if action in (Action.NEXT_LESSON, Action.SKIP_TO_ADVANCED_TOPIC):
            step = 1 if action == Action.NEXT_LESSON else 2
            carry = 0.3 * (self.mastery - 0.7) if step == 1 else 0.6 * (self.mastery - 0.85)
            self.lesson_index = min(self.lesson_index + step, TOTAL_LESSONS - 1)
            self.completed_lessons = min(self.completed_lessons + step, TOTAL_LESSONS)
            start = rng.uniform(0.25, 0.45) * (0.7 + 0.3 * self.ability)
            self.mastery = _clip(start + carry, 0.05, 0.95)
            self.difficulty = Difficulty.EASY  # a new lesson starts with its EASY quiz
            self.hints_used = 0
            self.lesson_attempts = 1
        else:
            if action == Action.INCREASE_DIFFICULTY:
                self.difficulty = Difficulty(min(self.difficulty.value + 1, 2))
            elif action == Action.DECREASE_DIFFICULTY:
                self.difficulty = Difficulty(max(self.difficulty.value - 1, 0))

            base = BASE_GAIN[action][_band(self.mastery)]
            if action == Action.PROVIDE_HINT:
                if self.hints_used >= 2:
                    base *= 0.5
                self.hints_used += 1
            gain = (
                base
                * self.ability
                * effectiveness
                * difficulty_fit(self.mastery, self.difficulty)
                * (1.0 - self.mastery)
            )
            if base > 0:
                gain += rng.gauss(0.0, GAIN_NOISE_SD)
            self.mastery = _clip(self.mastery + gain, 0.0, 1.0)

            if action in (
                Action.REPEAT_LESSON,
                Action.PRACTICE_QUIZ,
                Action.SHOW_WORKED_EXAMPLE,
                Action.INCREASE_DIFFICULTY,
                Action.DECREASE_DIFFICULTY,
                Action.QUICK_CHALLENGE,
            ):
                self.lesson_attempts += 1

        # Fatigue: a break restores, everything else tires the student.
        if action == Action.FOCUS_RECOVERY:
            self.fatigue *= 0.3
            if self.drowsy and rng.random() < 0.85:
                self.drowsy = False
            self.looking_away = False
        else:
            self.fatigue = _clip(self.fatigue + self.fatigue_rate * rng.uniform(0.5, 1.5))

        # Novelty/refocus boost: proportional to how much attention was
        # missing, weaker when repeated back-to-back (habituation), and it
        # does not stack -- the larger of the fading old boost and the new
        # one applies.
        boost = ATTENTION_BOOST.get(action, 0.0) * (1.0 - self.attention)
        if self.drowsy and action != Action.FOCUS_RECOVERY:
            boost *= 0.25  # novelty barely helps a drowsy student
        if len(self.history) >= 2 and self.history[-2] == action.name:
            boost *= 0.3
        self.boost = max(self.boost * 0.5, boost)

        self._observe_engagement(after_break=action == Action.FOCUS_RECOVERY)
        self.previous_score = self.current_score
        self.current_score = self._take_quiz()

    # ------------------------------------------------------------------
    def _observe_engagement(self, after_break: bool = False) -> None:
        rng = self.rng
        if not after_break:  # after a break, apply() already decided drowsiness
            p_drowsy = _clip((self.fatigue - 0.45) * 1.6, 0.0, 0.9)
            self.drowsy = rng.random() < p_drowsy
        self.yawning = (not self.drowsy) and rng.random() < self.fatigue * 0.7
        self.looking_away = rng.random() < self.distractibility * (1.1 - self.focus)
        attention = (
            self.focus
            - 0.35 * self.fatigue
            + self.boost
            - (0.2 if self.looking_away else 0.0)
            - (0.15 if self.drowsy else 0.0)
            + rng.gauss(0.0, ATTENTION_NOISE_SD)
        )
        self.attention = _clip(attention)

    def _take_quiz(self) -> int:
        raw = (
            self.mastery
            - DIFFICULTY_OFFSET[self.difficulty]
            + 0.1 * (self.attention - 0.6)
            + self.rng.gauss(0.0, SCORE_NOISE_SD)
        )
        self.response_time = round(self.rng.uniform(10.0, 60.0) * (1.4 - self.mastery * 0.6), 1)
        return int(round(_clip(raw) * 100))


def create_initial_state(rng: random.Random | None = None) -> StudentState:
    """Observable state of a freshly sampled simulated student."""
    return SimulatedStudent.sample(rng or random.Random()).observe()
