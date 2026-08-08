import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cv2

from camera import Camera
from face_detector import FaceDetector
from eye_tracker import EyeTracker

camera = Camera()
detector = FaceDetector()
tracker = EyeTracker()

while True:

    frame = camera.read_frame()

    if frame is None:
        break

    found, landmarks, frame = detector.detect(frame)

    if found:

        result = tracker.process(landmarks)

        cv2.putText(
            frame,
            f"EAR : {result['ear']:.3f}",
            (20,40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,255,0),
            2
        )

        status = "Eyes Open" if result["eyes_open"] else "Eyes Closed"

        cv2.putText(
            frame,
            status,
            (20,80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255,0,0),
            2
        )

    cv2.imshow("Eye Tracker", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()