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
- Looking Away Detection
- Yawning Detection
- Face Presence Detection
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
from looking_away import LookingAwayDetector
from yawn_detector import YawnDetector
from face_presence import FacePresence


# ---------------------------------------------------
# Initialize Modules
# ---------------------------------------------------

camera = Camera()
detector = FaceDetector()
eye_tracker = EyeTracker()
head_pose = HeadPoseEstimator()
gaze_tracker = GazeTracker()
looking_detector = LookingAwayDetector()
yawn_detector = YawnDetector()
attention = AttentionEngine()
logger = SessionLogger()
presence = FacePresence()
api = APIClient()

backend_status = "Disconnected"


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

    face_found, landmarks, frame = detector.detect(frame)

    presence_result = presence.update(face_found)

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
        # Looking At Screen
        # -----------------------------

        looking_at_screen = (
            gaze_result["gaze"] == "Center"
            and head_result["direction"] == "Forward"
        )

        # -----------------------------
        # Looking Away Detection
        # -----------------------------

        looking_result = looking_detector.process(
            head_result["direction"],
            gaze_result["gaze"]
        )

        # -----------------------------
        # Yawn Detection
        # -----------------------------

        yawn_result = yawn_detector.process(landmarks)

        # -----------------------------
        # Attention Engine
        # -----------------------------

        attention_result = attention.update(
            face=face_found,
            eyes_open=eye_result["eyes_open"],
            head_direction=head_result["direction"],
            blink_rate=eye_result["blink_rate"],
            looking_away=looking_result["looking_away"],
            yawning=yawn_result["yawning"]
        )

        # -----------------------------
        # Log Once Every Second
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
        # Send Data To Backend
        # -----------------------------

        current_time = time.time()

        if current_time - last_api_time >= SEND_INTERVAL:

            try:

                api.send_attention_data(
                    student_id=STUDENT_ID,
                    attention_score=attention_result["score"],
                    status=attention_result["status"],
                    eyes_open=eye_result["eyes_open"],
                    head_direction=head_result["direction"],
                    looking_away=looking_result["looking_away"],
                    yawning=yawn_result["yawning"]
                )

                backend_status = "Connected"

            except Exception:

                backend_status = "Disconnected"

            last_api_time = current_time

        # -----------------------------
        # Display Information
        # -----------------------------

        cv2.putText(
            frame,
            f"Attention : {attention_result['score']}%",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Status : {attention_result['status']}",
            (20, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 0, 0),
            2
        )

        cv2.putText(
            frame,
            f"Head : {head_result['direction']}",
            (20, 110),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Looking : {'YES' if looking_at_screen else 'NO'}",
            (20, 145),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0) if looking_at_screen else (0, 0, 255),
            2
        )

        cv2.putText(
            frame,
            f"Gaze : {gaze_result['gaze']}",
            (20, 180),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"EAR : {eye_result['ear']:.3f}",
            (20, 215),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Blinks : {eye_result['blink_count']}",
            (20, 250),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Blink Rate : {eye_result['blink_rate']:.1f}/min",
            (20, 285),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Looking Away : {'Yes' if looking_result['looking_away'] else 'No'}",
            (20, 320),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"MAR : {yawn_result['mar']:.2f}",
            (20, 355),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Yawning : {'Yes' if yawn_result['yawning'] else 'No'}",
            (20, 390),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

    else:

        cv2.putText(
            frame,
            "No Face Detected",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

    # ---------------------------------------------------
    # FPS
    # ---------------------------------------------------

    current_time = time.time()

    elapsed = current_time - prev_time

    fps = 1 / elapsed if elapsed > 0 else 0

    prev_time = current_time

    cv2.putText(
        frame,
        f"FPS : {int(fps)}",
        (20, 425),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )

    # ---------------------------------------------------
    # Face Presence
    # ---------------------------------------------------

    cv2.putText(
        frame,
        f"Face : {presence_result['status']}",
        (20, 460),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0)
        if presence_result["status"] == "Present"
        else (0, 0, 255),
        2
    )

    cv2.putText(
        frame,
        f"Absent : {presence_result['absent_time']} sec",
        (20, 495),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )

    # ---------------------------------------------------
    # Backend Status
    # ---------------------------------------------------

    cv2.putText(
        frame,
        f"Backend : {backend_status}",
        (20, 530),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0)
        if backend_status == "Connected"
        else (0, 0, 255),
        2
    )

    # ---------------------------------------------------
    # Show Window
    # ---------------------------------------------------

    cv2.imshow(
        "Adaptive Learning System - Facial Analysis",
        frame
    )

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break


# ---------------------------------------------------
# Cleanup
# ---------------------------------------------------

camera.release()
cv2.destroyAllWindows()