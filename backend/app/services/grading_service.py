"""Server-side quiz grading.

The client only ever sends the options the student selected. Correct
answers stay on the server until the attempt has been graded and stored.
"""

from dataclasses import dataclass, field

from app.models.question import Question

VALID_OPTIONS = ("A", "B", "C", "D")


class GradingError(ValueError):
    """Raised when submitted answers do not match the quiz's questions."""


@dataclass
class QuestionResult:
    question_id: int
    selected_answer: str
    correct_answer: str
    is_correct: bool


@dataclass
class GradingResult:
    correct_count: int
    total_questions: int
    results: list[QuestionResult] = field(default_factory=list)

    @property
    def score(self) -> float:
        """Percentage score rounded to two decimals."""
        if self.total_questions == 0:
            return 0.0
        return round(self.correct_count * 100.0 / self.total_questions, 2)


def grade_answers(questions: list[Question], answers: dict[int, str]) -> GradingResult:
    """Grade ``answers`` (question id -> option letter) against ``questions``.

    Every question of the quiz must be answered exactly once, and no
    answer may refer to a question outside the quiz.
    """
    if not questions:
        raise GradingError("This quiz has no questions.")

    question_ids = {question.id for question in questions}
    submitted_ids = set(answers)

    unknown = submitted_ids - question_ids
    if unknown:
        raise GradingError(
            f"Answers refer to questions not in this quiz: {sorted(unknown)}"
        )

    missing = question_ids - submitted_ids
    if missing:
        raise GradingError(f"Unanswered questions: {sorted(missing)}")

    results: list[QuestionResult] = []
    correct = 0

    for question in sorted(questions, key=lambda q: q.id):
        selected = str(answers[question.id]).strip().upper()
        if selected not in VALID_OPTIONS:
            raise GradingError(
                f"Answer for question {question.id} must be one of {list(VALID_OPTIONS)}"
            )

        expected = str(question.correct_answer).strip().upper()
        is_correct = selected == expected
        correct += int(is_correct)

        results.append(
            QuestionResult(
                question_id=question.id,
                selected_answer=selected,
                correct_answer=expected,
                is_correct=is_correct,
            )
        )

    return GradingResult(
        correct_count=correct,
        total_questions=len(questions),
        results=results,
    )
