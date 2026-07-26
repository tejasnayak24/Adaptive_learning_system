def __post_init__(self) -> None:
        """Perform lightweight sanity checks on the configuration.

        This validation only guards against structurally invalid values
        (out-of-range rates or non-positive counts) that would indicate a
        misconfiguration, catching them at construction time rather than
        deep inside a training loop.
        """
        if not 0.0 <= self.learning_rate <= 1.0:
            raise ValueError("learning_rate must be between 0.0 and 1.0.")
        if not 0.0 <= self.discount_factor <= 1.0:
            raise ValueError("discount_factor must be between 0.0 and 1.0.")
        if not 0.0 <= self.epsilon <= 1.0:
            raise ValueError("epsilon must be between 0.0 and 1.0.")
        if not 0.0 <= self.epsilon_decay <= 1.0:
            raise ValueError("epsilon_decay must be between 0.0 and 1.0.")
        if not 0.0 <= self.min_epsilon <= 1.0:
            raise ValueError("min_epsilon must be between 0.0 and 1.0.")
        if self.training_episodes <= 0:
            raise ValueError("training_episodes must be greater than 0.")
        if self.max_steps_per_episode <= 0:
            raise ValueError("max_steps_per_episode must be greater than 0.")
        if self.min_epsilon > self.epsilon:
            raise ValueError("min_epsilon cannot be greater than epsilon.")