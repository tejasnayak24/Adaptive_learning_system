def __post_init__(self) -> None:
    """Perform lightweight sanity checks on the recommendation.

    This validation only guards against structurally invalid output
    (an out-of-range confidence value or a missing explanation) that
    would indicate a bug in the policy or agent code producing this
    recommendation.
    """
    if not isinstance(self.action, Action):
        raise TypeError("action must be an instance of Action.")

    if not 0.0 <= self.confidence <= 1.0:
        raise ValueError("confidence must be between 0.0 and 1.0.")

    if not self.explanation.strip():
        raise ValueError("explanation must not be empty.")