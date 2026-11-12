import time

from config import LOOK_AWAY_THRESHOLD


class LookingAwayDetector:
    """Reports looking away only once it has lasted ``LOOK_AWAY_THRESHOLD``.

    A single frame of off-centre gaze (e.g. a glance at the keyboard) is
    reported as ``looking_away_instant`` but does not set ``looking_away``.
    """

    def __init__(self, threshold_seconds=LOOK_AWAY_THRESHOLD):
        self.threshold_seconds = threshold_seconds
        self.away_since = None

    def process(self, head_direction, gaze, now=None):

        if now is None:
            now = time.time()

        instant = (
            head_direction != "Forward"
            or gaze != "Center"
        )

        if instant:
            if self.away_since is None:
                self.away_since = now
            away_for = now - self.away_since
        else:
            self.away_since = None
            away_for = 0.0

        return {
            "looking_away": instant and away_for >= self.threshold_seconds,
            "looking_away_instant": instant,
            "away_seconds": round(away_for, 1),
        }

    def reset(self):
        self.away_since = None
