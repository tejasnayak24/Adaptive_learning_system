import sys
from pathlib import Path

# Add facial_analysis directory to Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cv2

from camera import Camera
from face_detector import FaceDetector

camera = Camera()
detector = FaceDetector()

while True:
    frame = camera.read_frame()

    if frame is None:
        break

    face_found, landmarks, frame = detector.detect(frame)

    if face_found:
        cv2.putText(
            frame,
            "Face Detected",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )
    else:
        cv2.putText(
            frame,
            "No Face",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2,
        )

    cv2.imshow("Face Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()