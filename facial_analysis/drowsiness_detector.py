"""
Drowsiness detection built on top of the per-frame eye, yawn and
face-presence results.

This module only decides *when* an alert should fire and what it
should say. Playing the alert (beep / speech) is handled by
voice_alert.VoiceAlert and showing it by hud.HUD.
"""

import time
from collections import deque

from config import (
    EYES_CLOSED_ALERT_SECONDS,
    DROWSY_ALERT_REPEAT_SECONDS,
    NO_FACE_ALERT_SECONDS,
    NO_FACE_ALERT_REPEAT_SECONDS,
    WAKE_UP_ESCALATE_AFTER,
    YAWN_ALERT_MIN_GAP_SECONDS,
    FREQUENT_YAWN_COUNT,
    FREQUENT_YAWN_WINDOW_SECONDS,
    FREQUENT_YAWN_COOLDOWN_SECONDS,
    BEEP_DURATION_MS,
    ESCALATED_BEEP_DURATION_MS,
    WAKE_UP_MESSAGE,
    ESCALATED_WAKE_UP_MESSAGE,
    NO_FACE_MESSAGE,
    YAWN_MESSAGES,
    FREQUENT_YAWN_MESSAGE,
)


# Alert types (alert["type"])
ALERT_EYES_CLOSED = "eyes_closed"
ALERT_NO_FACE = "no_face"
ALERT_YAWN = "yawn"
ALERT_FREQUENT_YAWN = "frequent_yawn"


class DrowsinessDetector:

    def __init__(self):

        self.eyes_closed_start = None
        self.face_missing_start = None

        self.last_eyes_alert = None
        self.last_no_face_alert = None

        # Wake-up alerts fired during the current eyes-closed episode
        self.wake_alert_count = 0

        self.was_yawning = False
        self.yawn_count = 0
        self.recent_yawns = deque()
        self.last_yawn_alert = None
        self.last_frequent_yawn_alert = None
        self.yawn_message_index = 0

    def update(self, face_found, eyes_open=True, yawning=False, now=None):
        """
        Call once per frame. Eye and yawn state are ignored when no
        face is found. `now` can be passed in for testing.

        Each entry in result["alerts"] is a dict with
        type, message, beeps and beep_ms.
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
            self.wake_alert_count = 0
            eyes_closed_duration = 0.0

        else:
            if self.eyes_closed_start is None:
                self.eyes_closed_start = now

            eyes_closed_duration = now - self.eyes_closed_start

        drowsy = eyes_closed_duration >= EYES_CLOSED_ALERT_SECONDS

        if drowsy and self._due(
            self.last_eyes_alert, DROWSY_ALERT_REPEAT_SECONDS, now
        ):
            alerts.append(self._wake_up_alert())
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
            alerts.append(self._alert(ALERT_NO_FACE, NO_FACE_MESSAGE))
            self.last_no_face_alert = now

        # -----------------------------
        # Yawning (counted once, at the
        # start of each yawn)
        # -----------------------------

        if yawning and not self.was_yawning:

            yawn_alert = self._on_yawn_start(now)

            if yawn_alert is not None:
                alerts.append(yawn_alert)

        self.was_yawning = yawning

        return {
            "drowsy": drowsy,
            "eyes_closed_time": round(eyes_closed_duration, 1),
            "absent": absent,
            "yawn_count": self.yawn_count,
            "alerts": alerts
        }

    def _wake_up_alert(self):
        """Normal wake-up alert, or a firmer one if the student slept through the last few."""

        self.wake_alert_count += 1

        if self.wake_alert_count > WAKE_UP_ESCALATE_AFTER:
            return self._alert(
                ALERT_EYES_CLOSED,
                ESCALATED_WAKE_UP_MESSAGE,
                beeps=2,
                beep_ms=ESCALATED_BEEP_DURATION_MS
            )

        return self._alert(ALERT_EYES_CLOSED, WAKE_UP_MESSAGE, beeps=1)

    def _on_yawn_start(self, now):
        """Count the yawn and return an alert to play, or None."""

        self.yawn_count += 1
        self.recent_yawns.append(now)

        while now - self.recent_yawns[0] > FREQUENT_YAWN_WINDOW_SECONDS:
            self.recent_yawns.popleft()

        # Several yawns in a short time -> stronger break message
        if len(self.recent_yawns) >= FREQUENT_YAWN_COUNT and self._due(
            self.last_frequent_yawn_alert, FREQUENT_YAWN_COOLDOWN_SECONDS, now
        ):
            self.last_frequent_yawn_alert = now
            self.last_yawn_alert = now
            return self._alert(ALERT_FREQUENT_YAWN, FREQUENT_YAWN_MESSAGE)

        # Otherwise a gentle reminder, rotating through the messages
        if self._due(self.last_yawn_alert, YAWN_ALERT_MIN_GAP_SECONDS, now):
            self.last_yawn_alert = now
            message = YAWN_MESSAGES[self.yawn_message_index % len(YAWN_MESSAGES)]
            self.yawn_message_index += 1
            return self._alert(ALERT_YAWN, message)

        return None

    @staticmethod
    def _alert(alert_type, message, beeps=0, beep_ms=BEEP_DURATION_MS):

        return {
            "type": alert_type,
            "message": message,
            "beeps": beeps,
            "beep_ms": beep_ms
        }

    @staticmethod
    def _due(last_alert, interval, now):

        return last_alert is None or now - last_alert >= interval
