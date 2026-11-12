"""Per-frame facial analysis, shared by the camera agent and preview mode.

This wraps the existing detectors (face mesh, eye tracker, gaze, head
pose, looking away, yawning, attention engine, face presence) and the
drowsiness detector into one call per frame. It contains no camera, HTTP
or UI code, so it can be tested with synthetic landmarks.

"Possible drowsiness" is an attention heuristic (eyes closed for a
sustained period); it is not a medical assessment of sleep.
"""

import time
from collections import deque

from attention_engine import AttentionEngine
from config import FACE_STABILITY_MIN_RATIO, FACE_STABILITY_WINDOW_SECONDS, LOW_LIGHT_BRIGHTNESS
from drowsiness_detector import DrowsinessDetector
from eye_tracker import EyeTracker
from face_presence import FacePresence
from gaze_tracker import GazeTracker
from head_pose import HeadPoseEstimator
from looking_away import LookingAwayDetector
from yawn_detector import YawnDetector


def frame_brightness(frame):
    """Mean grey level (0-255) of a BGR frame."""
    import cv2

    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return float(grey.mean())


class FrameProcessor:

    def __init__(self, face_detector=None, brightness_fn=frame_brightness):
        if face_detector is None:
            from face_detector import FaceDetector

            face_detector = FaceDetector()

        self.detector = face_detector
        self.brightness_fn = brightness_fn

        self.eye_tracker = EyeTracker()
        self.gaze_tracker = GazeTracker()
        self.head_pose = HeadPoseEstimator()
        self.looking_detector = LookingAwayDetector()
        self.yawn_detector = YawnDetector()
        self.attention = AttentionEngine()
        self.presence = FacePresence()
        self.drowsiness = DrowsinessDetector()

        self._face_history = deque()

    def _face_stable(self, face_found, now):
        self._face_history.append((now, face_found))
        while self._face_history and now - self._face_history[0][0] > FACE_STABILITY_WINDOW_SECONDS:
            self._face_history.popleft()

        seen = len(self._face_history)
        found = sum(1 for _, ok in self._face_history if ok)
        span = now - self._face_history[0][0] if seen else 0.0

        # Require most of a full window of history before calling it stable.
        return (
            span >= FACE_STABILITY_WINDOW_SECONDS * 0.75
            and found / seen >= FACE_STABILITY_MIN_RATIO
        )

    def process(self, frame, now=None):
        """Analyse one frame. Returns a result dict (see keys below)."""
        if now is None:
            now = time.time()

        brightness = self.brightness_fn(frame)
        face_found, landmarks, frame = self.detector.detect(frame)

        presence = self.presence.update(face_found)
        stable = self._face_stable(face_found, now)

        result = {
            "frame": frame,
            "timestamp": now,
            "face_detected": bool(face_found),
            "face_stable": bool(stable),
            "presence": presence,
            "brightness": round(brightness, 1),
            "lighting_ok": brightness >= LOW_LIGHT_BRIGHTNESS,
            "eye": None,
            "gaze": None,
            "head": None,
            "looking": None,
            "yawn": None,
            "attention": None,
        }

        if face_found:
            eye = self.eye_tracker.process(landmarks)
            gaze = self.gaze_tracker.process(landmarks)
            head = self.head_pose.process(landmarks)
            looking = self.looking_detector.process(head["direction"], gaze["gaze"], now=now)
            yawn = self.yawn_detector.process(landmarks)

            attention = self.attention.update(
                face=True,
                eyes_open=eye["eyes_open"],
                head_direction=head["direction"],
                blink_rate=eye["blink_rate"],
                looking_away=looking["looking_away"],
                yawning=yawn["yawning"],
            )

            drowsy = self.drowsiness.update(
                face_found=True,
                eyes_open=eye["eyes_open"],
                yawning=yawn["yawning"],
                now=now,
            )

            result.update(eye=eye, gaze=gaze, head=head, looking=looking, yawn=yawn, attention=attention)
        else:
            self.looking_detector.reset()
            drowsy = self.drowsiness.update(face_found=False, now=now)

        result["drowsy"] = drowsy
        return result


def telemetry_from_result(result):
    """The measurement fields sent to the backend for one frame result.

    When no face is visible the attention-derived measurements are None:
    the camera is working, but there is nothing to measure.
    """
    face = result["face_detected"]
    attention = result["attention"]

    score = None
    if face and attention is not None:
        score = float(attention["score"])
        if score > 1:
            score = score / 100.0
        score = max(0.0, min(1.0, score))

    return {
        "face_detected": face,
        "face_stable": result["face_stable"],
        "lighting_ok": result["lighting_ok"],
        "brightness": result["brightness"],
        "attention_score": score,
        "yawning": bool(result["yawn"]["yawning"]) if face else None,
        "looking_away": bool(result["looking"]["looking_away"]) if face else None,
        "eyes_closed": (not result["eye"]["eyes_open"]) if face else None,
        "possible_drowsiness": bool(result["drowsy"]["drowsy"]) if face else None,
        "eyes_closed_seconds": result["drowsy"]["eyes_closed_time"],
        "head_direction": result["head"]["direction"] if face else None,
        "gaze": result["gaze"]["gaze"] if face else None,
        "yawn_count": result["drowsy"]["yawn_count"],
    }
