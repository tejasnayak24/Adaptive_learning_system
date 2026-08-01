"""
Adaptive Learning System
Facial Analysis Module

Features:
- Face Detection
- Eye Tracking (EAR)
- Blink Detection
- Gaze Detection
- Head Pose Estimation
- Attention Scoring
- Session Logging
- FPS Counter
"""

import cv2
import time

from api_client import APIClient
from config import STUDENT_ID, SEND_INTERVAL
from camera import Camera
from face_detector import FaceDetector
from eye_tracker import EyeTracker
from head_pose import HeadPoseEstimator
from gaze_tracker import GazeTracker
from attention_engine import AttentionEngine
from logger import SessionLogger


# ---------------------------------------------------
# Initialize Modules
# ---------------------------------------------------

camera = Camera()

detector = FaceDetector()

eye_tracker = EyeTracker()

head_pose = HeadPoseEstimator()

gaze_tracker = GazeTracker()

attention = AttentionEngine()

logger = SessionLogger()
api = APIClient()

# ---------------------------------------------------
# Timers
# ---------------------------------------------------

prev_time = time.time()

last_log_time = time.time()
last_api_time = time.time()

# ---------------------------------------------------
# Main Loop
# ---------------------------------------------------

while True:

    frame = camera.read_frame()

    if frame is None:
        break

    # Detect face
    face_found, landmarks, frame = detector.detect(frame)

    if face_found:

        # -----------------------------
        # Eye Tracking
        # -----------------------------

        eye_result = eye_tracker.process(landmarks)

        # -----------------------------
        # Gaze Detection
        # -----------------------------

        gaze_result = gaze_tracker.process(landmarks)

        # -----------------------------
        # Head Pose
        # -----------------------------

        head_result = head_pose.process(landmarks)

        # -----------------------------
        # Attention Engine
        # -----------------------------

        attention_result = attention.update(
            face=face_found,
            eyes_open=eye_result["eyes_open"],
            head_direction=head_result["direction"],
            blink_rate=eye_result["blink_rate"]
        )

        # -----------------------------
        # Log once every second
        # -----------------------------

        current_time = time.time()

        if current_time - last_log_time >= 1:

            logger.log(
                attention=attention_result["score"],
                status=attention_result["status"],
                head_direction=head_result["direction"],
                eyes_open=eye_result["eyes_open"],
                blink_count=eye_result["blink_count"],
                blink_rate=eye_result["blink_rate"]
            )

            last_log_time = current_time

        # -----------------------------
        # Display Information
        # -----------------------------
        current_time = time.time()

     
        if current_time - last_api_time >= SEND_INTERVAL:
            api.send_attention_data(
            student_id=STUDENT_ID,
            attention_score=attention_result["score"],
            status=attention_result["status"],
            eyes_open=eye_result["eyes_open"],
            head_direction=head_result["direction"]
            )

            last_api_time = current_time    

        cv2.putText(
            frame,
            f"Attention : {attention_result['score']}%",
            (20,40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0,255,0),
            2
        )

        cv2.putText(
            frame,
            f"Status : {attention_result['status']}",
            (20,75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255,0,0),
            2
        )

        cv2.putText(
            frame,
            f"Head : {head_result['direction']}",
            (20,110),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0,255,255),
            2
        )

        cv2.putText(
            frame,
            f"Gaze : {gaze_result['gaze']}",
            (20,145),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255,255,0),
            2
        )

        cv2.putText(
            frame,
            f"EAR : {eye_result['ear']:.3f}",
            (20,180),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255,255,255),
            2
        )

        cv2.putText(
            frame,
            f"Blinks : {eye_result['blink_count']}",
            (20,215),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255,255,255),
            2
        )

        cv2.putText(
            frame,
            f"Blink Rate : {eye_result['blink_rate']:.1f}/min",
            (20,250),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255,255,255),
            2
        )

    else:

        cv2.putText(
            frame,
            "No Face Detected",
            (20,40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,0,255),
            2
        )

    # ---------------------------------------------------
    # FPS
    # ---------------------------------------------------

    current_time = time.time()

    fps = 1 / (current_time - prev_time)

    prev_time = current_time

    cv2.putText(
        frame,
        f"FPS : {int(fps)}",
        (20,285),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0,255,255),
        2
    )

    # ---------------------------------------------------
    # Show Window
    # ---------------------------------------------------

    cv2.imshow("Adaptive Learning System - Facial Analysis", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break


# ---------------------------------------------------
# Cleanup
# ---------------------------------------------------

camera.release()

cv2.destroyAllWindows()