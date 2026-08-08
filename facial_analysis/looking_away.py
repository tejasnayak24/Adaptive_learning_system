class LookingAwayDetector:

    def process(self, head_direction, gaze):

        looking_away = (
            head_direction != "Forward"
            or gaze != "Center"
        )

        return {
            "looking_away": looking_away
        }