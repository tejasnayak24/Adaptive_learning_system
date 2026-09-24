"""
Drowsiness detection built on top of the per-frame eye, yawn and
face-presence results.

This module only decides *when* an alert should fire. Playing the
alert (beep / speech) is handled by voice_alert.VoiceAlert.
"""

import time

from config import (
    EYES_CLOSED_ALERT_SECONDS,
    DROWSY_ALERT_REPEAT_SECONDS,
    NO_FACE_ALERT_SECONDS,
    NO_FACE_ALERT_REPEAT_SECONDS,
    YAWN_ALERT_COOLDOWN_SECONDS,
    WAKE_UP_MESSAGE,
    NO_FACE_MESSAGE,
    YAWN_MESSAGE,
)


# Alert identifiers returned in result["alerts"]
ALERT_EYES_CLOSED = "eyes_closed"
ALERT_NO_FACE = "no_face"
ALERT_YAWN = "yawn"

# Alert -> (spoken message, play beep first)
ALERT_MESSAGES = {
    ALERT_EYES_CLOSED: (WAKE_UP_MESSAGE, True),
    ALERT_NO_FACE: (NO_FACE_MESSAGE, False),
    ALERT_YAWN: (YAWN_MESSAGE, False),
}


class DrowsinessDetector:

    def __init__(self):

        self.eyes_closed_start = None
        self.face_missing_start = None

        self.last_eyes_alert = None
        self.last_no_face_alert = None
        self.last_yawn_alert = None

        self.was_yawning = False

    def update(self, face_found, eyes_open=True, yawning=False, now=None):
        """
        Call once per frame. Eye and yawn state are ignored when no
        face is found. `now` can be passed in for testing.
        """

        if now is None:
            now = time.time()

        alerts = []

        # -----------------------------
        # Face Presence
        # -----------------------------

        if face_found:
            self.face_missing_start = None
            self.last_no_face_alert = None

        else:
            if self.face_missing_start is None:
                self.face_missing_start = now

            # Eye / mouth state is unknown without a face
            eyes_open = True
            yawning = False

        # -----------------------------
        # Eyes Closed (time based, so it
        # does not depend on the FPS)
        # -----------------------------

        if eyes_open:
            self.eyes_closed_start = None
            self.last_eyes_alert = None
            eyes_closed_duration = 0.0

        else:
            if self.eyes_closed_start is None:
                self.eyes_closed_start = now

            eyes_closed_duration = now - self.eyes_closed_start

        drowsy = eyes_closed_duration >= EYES_CLOSED_ALERT_SECONDS

        if drowsy and self._due(
            self.last_eyes_alert, DROWSY_ALERT_REPEAT_SECONDS, now
        ):
            alerts.append(ALERT_EYES_CLOSED)
            self.last_eyes_alert = now

        # -----------------------------
        # No Face
        # -----------------------------

        absent_duration = 0.0

        if self.face_missing_start is not None:
            absent_duration = now - self.face_missing_start

        absent = absent_duration >= NO_FACE_ALERT_SECONDS

        if absent and self._due(
            self.last_no_face_alert, NO_FACE_ALERT_REPEAT_SECONDS, now
        ):
            alerts.append(ALERT_NO_FACE)
            self.last_no_face_alert = now

        # -----------------------------
        # Yawning (only on the start of a
        # yawn, with a cooldown so it
        # doesn't nag)
        # -----------------------------

        yawn_started = yawning and not self.was_yawning

        if yawn_started and self._due(
            self.last_yawn_alert, YAWN_ALERT_COOLDOWN_SECONDS, now
        ):
            alerts.append(ALERT_YAWN)
            self.last_yawn_alert = now

        self.was_yawning = yawning

        return {
            "drowsy": drowsy,
            "eyes_closed_time": round(eyes_closed_duration, 1),
            "absent": absent,
            "alerts": alerts
        }

    @staticmethod
    def _due(last_alert, interval, now):

        return last_alert is None or now - last_alert >= interval
