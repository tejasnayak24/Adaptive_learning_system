import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cv2

from camera import Camera
from face_detector import FaceDetector
from eye_tracker import EyeTracker
from head_pose import HeadPoseEstimator
from attention_score import AttentionScorer

camera = Camera()
detector = FaceDetector()
eye = EyeTracker()
head = HeadPoseEstimator()
attention = AttentionScorer()

while True:

    frame = camera.read_frame()

    if frame is None:
        break

    found, landmarks, frame = detector.detect(frame)

    if found:

        eye_result = eye.process(landmarks)
        head_result = head.process(landmarks)

        result = attention.calculate(
            face_detected=True,
            eyes_open=eye_result["eyes_open"],
            head_direction=head_result["direction"]
        )

        cv2.putText(
            frame,
            f"Attention : {result['score']}",
            (20,40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,255,0),
            2
        )

        cv2.putText(
            frame,
            result["status"],
            (20,80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255,0,0),
            2
        )

    cv2.imshow("Attention Score", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()