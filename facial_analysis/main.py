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
- Drowsiness Detection (Voice Alerts)
- On-screen Dashboard (HUD)
- Session Logging
- FPS Counter
"""

import argparse
import cv2
import time

from api_client import APIClient
from config import STUDENT_ID as DEFAULT_STUDENT_ID, SEND_INTERVAL, SHOW_HUD
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
from drowsiness_detector import DrowsinessDetector
from voice_alert import VoiceAlert
from hud import HUD


# ---------------------------------------------------
# Student Configuration
# ---------------------------------------------------

parser = argparse.ArgumentParser(
    description="Adaptive Learning System - Facial Analysis"
)

parser.add_argument(
    "--student-id",
    type=int,
    default=DEFAULT_STUDENT_ID,
    help="Student ID to associate with facial telemetry",
)

args = parser.parse_args()
student_id = args.student_id


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
drowsiness = DrowsinessDetector()
voice = VoiceAlert()
hud = HUD(student_id)
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

    # Per-frame results (stay None while no face is detected)
    eye_result = gaze_result = head_result = attention_result = None

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
        # Drowsiness Detection
        # -----------------------------

        drowsy_result = drowsiness.update(
            face_found=True,
            eyes_open=eye_result["eyes_open"],
            yawning=yawn_result["yawning"]
        )

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
                    student_id=student_id,
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

    else:

        drowsy_result = drowsiness.update(face_found=False)

    # ---------------------------------------------------
    # Voice Alerts (played on a background thread)
    # ---------------------------------------------------

    for alert in drowsy_result["alerts"]:

        voice.say(
            alert["message"],
            beeps=alert["beeps"],
            beep_ms=alert["beep_ms"]
        )

        hud.show_alert(alert["type"], alert["message"])

    # ---------------------------------------------------
    # FPS
    # ---------------------------------------------------

    current_time = time.time()

    elapsed = current_time - prev_time

    fps = 1 / elapsed if elapsed > 0 else 0

    prev_time = current_time

    # ---------------------------------------------------
    # Dashboard
    # ---------------------------------------------------

    if SHOW_HUD:

        hud.draw(
            frame,
            fps=fps,
            backend_connected=backend_status == "Connected",
            presence=presence_result,
            drowsy=drowsy_result,
            eye=eye_result,
            head=head_result,
            gaze=gaze_result,
            attention=attention_result
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

    if key == ord("h"):
        hud.toggle_compact()


# ---------------------------------------------------
# Cleanup
# ---------------------------------------------------

voice.shutdown()
camera.release()
cv2.destroyAllWindows()
