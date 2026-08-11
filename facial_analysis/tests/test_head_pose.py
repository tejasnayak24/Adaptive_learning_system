import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cv2

from camera import Camera
from face_detector import FaceDetector
from head_pose import HeadPoseEstimator

camera = Camera()
detector = FaceDetector()
head = HeadPoseEstimator()

while True:

    frame = camera.read_frame()

    if frame is None:
        break

    found, landmarks, frame = detector.detect(frame)

    if found:

        result = head.process(landmarks)

        cv2.putText(
            frame,
            f"Yaw : {result['yaw']}",
            (20,40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0,255,0),
            2
        )

        cv2.putText(
            frame,
            f"Pitch : {result['pitch']}",
            (20,80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0,255,0),
            2
        )

        cv2.putText(
            frame,
            result["direction"],
            (20,120),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255,0,0),
            2
        )

    cv2.imshow("Head Pose", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()