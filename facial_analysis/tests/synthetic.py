"""Synthetic MediaPipe-style face landmarks with known geometry.

Coordinates are normalised (0-1) like MediaPipe Face Mesh output. Only the
landmark indices used by the detectors are positioned deliberately; all
others sit at the frame centre.

Neutral face: eyes open (EAR 0.30), irises centred (gaze ratio 0.5),
head forward (yaw 0, pitch 0) and mouth closed (MAR 0.10).
"""

from dataclasses import dataclass

NUM_LANDMARKS = 478


@dataclass
class Point:
    x: float
    y: float
    z: float = 0.0


class Landmarks:
    """Mimics ``results.multi_face_landmarks[0]`` (has ``.landmark``)."""

    def __init__(self, points):
        self.landmark = points


def face(
    eye_opening=0.03,
    iris_offset=0.0,
    yaw_offset=0.0,
    pitch_offset=0.0,
    mouth_opening=0.01,
):
    """Build a synthetic face.

    eye_opening:   vertical eyelid gap (0.03 -> EAR 0.30 open, 0.01 -> 0.10 closed)
    iris_offset:   horizontal iris shift in eye-width fractions (-0.2 -> looks "Left")
    yaw_offset:    nose x shift (> 0.03 -> head "Left", < -0.03 -> "Right")
    pitch_offset:  nose y shift (> 0.04 -> head "Down")
    mouth_opening: lip gap (0.01 -> MAR 0.10, 0.08 -> MAR 0.80 yawn)
    """
    pts = [Point(0.5, 0.5) for _ in range(NUM_LANDMARKS)]
    half = eye_opening / 2

    def eye(corner_a, top_a, top_b, corner_b, bottom_b, bottom_a, x0, iris_index):
        width = 0.10
        y = 0.40
        pts[corner_a] = Point(x0, y)
        pts[corner_b] = Point(x0 + width, y)
        pts[top_a] = Point(x0 + 0.025, y - half)
        pts[bottom_a] = Point(x0 + 0.025, y + half)
        pts[top_b] = Point(x0 + 0.075, y - half)
        pts[bottom_b] = Point(x0 + 0.075, y + half)
        pts[iris_index] = Point(x0 + width * (0.5 + iris_offset), y)

    # EyeTracker order: [p1, p2, p3, p4, p5, p6] = corner, top, top, corner, bottom, bottom
    eye(33, 160, 158, 133, 153, 144, 0.35, 468)
    eye(362, 385, 387, 263, 373, 380, 0.55, 473)

    # Head pose
    pts[234] = Point(0.30, 0.50)
    pts[454] = Point(0.70, 0.50)
    pts[10] = Point(0.50, 0.20)
    pts[152] = Point(0.50, 0.80)
    pts[1] = Point(0.50 + yaw_offset, 0.50 + pitch_offset)

    # Mouth
    pts[61] = Point(0.45, 0.70)
    pts[291] = Point(0.55, 0.70)
    pts[13] = Point(0.50, 0.70)
    pts[14] = Point(0.50, 0.70 + mouth_opening)

    return Landmarks(pts)


class ScriptedDetector:
    """Stands in for FaceDetector: returns a scripted face (or none)."""

    def __init__(self, landmarks=None):
        self.landmarks = landmarks if landmarks is not None else face()
        self.face_visible = True

    def detect(self, frame):
        if not self.face_visible:
            return False, None, frame
        return True, self.landmarks, frame
