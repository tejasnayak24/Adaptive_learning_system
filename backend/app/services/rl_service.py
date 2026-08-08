"""Integration layer between the backend and the Reinforcement Learning engine.

This module exposes ``RLService``, the single point of contact the
backend uses to obtain adaptive learning recommendations. It loads the
trained Q-learning agent once and reuses it for every request, translates
plain backend data into the RL engine's ``StudentState`` type, and
returns the RL engine's own ``Recommendation`` object unchanged.

This service contains no FastAPI router code, no API endpoint
definitions, and no database access -- it only knows how to talk to the
RL engine. The RL engine itself remains completely independent of this
module; nothing here modifies, subclasses, or duplicates any logic from
``rl_engine``.
"""

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from rl_engine.core.config import RLConfig
from rl_engine.models.recommendation import Recommendation
from rl_engine.models.student_state import Difficulty, StudentState
from rl_engine.training.agent import QLearningAgent


class RLService:
    """Loads a trained Q-learning agent once and serves recommendations from it.

    The agent and its Q-table are loaded a single time, at construction,
    and held in memory for the lifetime of this service. No request
    handled by ``get_recommendation`` ever retrains the agent or reloads
    the Q-table from disk.

    Attributes:
        None (the loaded agent is kept as a private attribute; the
        backend is only expected to call ``get_recommendation``).
    """

    def __init__(self, q_table_path: str | Path, config: RLConfig | None = None) -> None:
        """Load the trained agent once and keep it in memory.

        Args:
            q_table_path: Path to the trained ``q_table.json`` file.
            config: The hyperparameters and state-discretization
                thresholds the agent should use. Defaults to
                ``RLConfig()`` (the RL engine's own default values) if
                not provided.

        Raises:
            TypeError: If ``q_table_path`` is not a ``str`` or ``Path``,
                or if ``config`` is provided but is not an ``RLConfig``.
            FileNotFoundError: If no file exists at ``q_table_path``.
            RuntimeError: If the Q-table file exists but cannot be
                loaded into a ``QLearningAgent`` for any other reason
                (e.g. it is corrupted or not valid JSON).
        """
        if not isinstance(q_table_path, (str, Path)):
            raise TypeError("q_table_path must be a str or Path.")
        if config is not None and not isinstance(config, RLConfig):
            raise TypeError("config must be an instance of RLConfig.")

        resolved_path = Path(q_table_path).expanduser().resolve()
        resolved_config = config if config is not None else RLConfig()

        if not resolved_path.exists():
            raise FileNotFoundError(f"Q-table file not found at '{resolved_path}'.")

        try:
            self._agent = QLearningAgent.load_q_table(resolved_path, resolved_config)
        except FileNotFoundError:
            raise
        except Exception as exc:
            raise RuntimeError(
                f"Failed to load Q-table from '{resolved_path}': {exc}"
            ) from exc

    def get_recommendation(self, student_data: Mapping[str, Any]) -> Recommendation:
        """Return the agent's recommendation for a student described by ``student_data``.

        Builds a ``StudentState`` from the given backend data and asks
        the already-loaded agent for a recommendation. No training,
        Q-value updates, or file I/O occur here.

        Args:
            student_data: A mapping containing every field required to
                construct a ``StudentState`` (``subject``, ``topic``,
                ``lesson``, ``previous_quiz_score``,
                ``current_quiz_score``, ``attention_score``,
                ``yawning``, ``looking_away``, ``difficulty``,
                ``response_time``, ``hints_used``, ``lesson_attempts``,
                and ``completed_lessons``). ``difficulty`` may be either
                a ``Difficulty`` instance or a string matching one of
                its member names (case-insensitive), since backend data
                typically arrives as plain, JSON-compatible values.

        Returns:
            The ``Recommendation`` produced by the RL engine.

        Raises:
            TypeError: If ``student_data`` is not a mapping, or if
                ``difficulty`` is not a ``Difficulty`` instance or a
                string.
            KeyError: If ``student_data`` is missing a required field.
            ValueError: If a field's value is invalid, including an
                unrecognized ``difficulty`` string or a value rejected
                by ``StudentState``'s own validation (e.g. an
                out-of-range score).
        """
        if not isinstance(student_data, Mapping):
            raise TypeError("student_data must be a mapping of StudentState fields.")

        student_state = self._build_student_state(student_data)
        return self._agent.recommend(student_state)

    def _build_student_state(self, data: Mapping[str, Any]) -> StudentState:
        """Convert plain backend data into a ``StudentState``.

        Each required field is retrieved into a local variable first, so
        a missing field is easy to trace back to this block, and only
        the ``difficulty`` value receives any conversion (into a
        ``Difficulty`` member) before being passed on. All range and
        value validation is left to ``StudentState.__post_init__``, so
        that validation logic is not duplicated here.

        Args:
            data: The raw student data supplied by the backend.

        Returns:
            A validated ``StudentState`` instance.

        Raises:
            KeyError: If a required field is missing from ``data``.
            TypeError: If ``difficulty`` is not a ``Difficulty`` or a
                string.
            ValueError: If ``difficulty`` is a string that does not
                match a known ``Difficulty`` member, or if any field
                fails ``StudentState``'s own validation.
        """
        try:
            subject = data["subject"]
            topic = data["topic"]
            lesson = data["lesson"]
            previous_quiz_score = data["previous_quiz_score"]
            current_quiz_score = data["current_quiz_score"]
            attention_score = data["attention_score"]
            yawning = data["yawning"]
            looking_away = data["looking_away"]
            difficulty = data["difficulty"]
            response_time = data["response_time"]
            hints_used = data["hints_used"]
            lesson_attempts = data["lesson_attempts"]
            completed_lessons = data["completed_lessons"]
        except KeyError as exc:
            raise KeyError(f"Missing required student data field: {exc}") from exc

        return StudentState(
            subject=subject,
            topic=topic,
            lesson=lesson,
            previous_quiz_score=previous_quiz_score,
            current_quiz_score=current_quiz_score,
            attention_score=attention_score,
            yawning=yawning,
            looking_away=looking_away,
            difficulty=self._to_difficulty(difficulty),
            response_time=response_time,
            hints_used=hints_used,
            lesson_attempts=lesson_attempts,
            completed_lessons=completed_lessons,
        )

    @staticmethod
    def _to_difficulty(value: Difficulty | str) -> Difficulty:
        """Convert a raw difficulty value into a ``Difficulty`` member.

        Args:
            value: Either a ``Difficulty`` instance already, or a string
                matching a member name (e.g. ``"medium"``, ``"MEDIUM"``).

        Returns:
            The corresponding ``Difficulty`` member.

        Raises:
            TypeError: If ``value`` is neither a ``Difficulty`` nor a
                string.
            ValueError: If ``value`` is a string that does not match
                any ``Difficulty`` member.
        """
        if isinstance(value, Difficulty):
            return value
        if isinstance(value, str):
            try:
                return Difficulty[value.strip().upper()]
            except KeyError as exc:
                raise ValueError(f"Unknown difficulty level: {value!r}") from exc
        raise TypeError("difficulty must be a Difficulty instance or a string.")