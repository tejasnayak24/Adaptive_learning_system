"""SQLAlchemy models.

Importing any ``app.models.<module>`` first runs this package initialiser,
which registers every model. Relationships refer to other models by name,
so all of them must be registered before the first query -- otherwise a
script that imports only a few models (e.g. the seed script) fails.
"""

from app.models.student import Student  # noqa: F401
from app.models.curriculum import CurriculumTopic, CurriculumUnit  # noqa: F401
from app.models.lesson import Lesson  # noqa: F401
from app.models.quiz import Quiz  # noqa: F401
from app.models.question import Question  # noqa: F401
from app.models.progress import Progress  # noqa: F401
from app.models.attempt_answer import AttemptAnswer  # noqa: F401
from app.models.session import LearningSession  # noqa: F401
from app.models.recommendation import RecommendationHistory  # noqa: F401
from app.models.reward import RewardHistory  # noqa: F401
from app.models.monitoring import MonitoringConsent, MonitoringSession  # noqa: F401
from app.models.quiz_attempt import QuizAttempt, QuizAttemptEvent  # noqa: F401
from app.models.session_event import SessionEvent  # noqa: F401
