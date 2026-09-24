"""
Configuration settings for the Facial Analysis module.
"""

# -------------------------------
# Camera Configuration
# -------------------------------
CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FPS = 30

# -------------------------------
# MediaPipe Configuration
# -------------------------------
MAX_NUM_FACES = 1
REFINE_LANDMARKS = True
MIN_DETECTION_CONFIDENCE = 0.6
MIN_TRACKING_CONFIDENCE = 0.6

# -------------------------------
# Attention Thresholds
# -------------------------------
EYE_CLOSED_THRESHOLD = 1.0
FACE_MISSING_THRESHOLD = 5.0
LOOK_AWAY_THRESHOLD = 2.0

# -------------------------------
# API Configuration
# -------------------------------

API_BASE_URL = "http://127.0.0.1:8000"

ATTENTION_ENDPOINT = "/attention"

API_URL = API_BASE_URL + ATTENTION_ENDPOINT

STUDENT_ID = 10

SEND_INTERVAL = 1

# -------------------------------
# Drowsiness Detection
# -------------------------------
EYES_CLOSED_ALERT_SECONDS = 2.0      # eyes closed this long -> wake-up alert
DROWSY_ALERT_REPEAT_SECONDS = 5.0    # repeat wake-up alert while eyes stay closed
NO_FACE_ALERT_SECONDS = 10.0         # no face this long -> "are you still there?"
NO_FACE_ALERT_REPEAT_SECONDS = 30.0  # repeat while the face is still missing
YAWN_ALERT_COOLDOWN_SECONDS = 60.0   # minimum gap between break reminders

# -------------------------------
# Voice Alerts
# -------------------------------
VOICE_ALERTS_ENABLED = True
VOICE_RATE = 170                     # words per minute
VOICE_VOLUME = 1.0                   # 0.0 - 1.0
BEEP_FREQUENCY = 1000                # Hz
BEEP_DURATION_MS = 400

WAKE_UP_MESSAGE = "Hey, wake up!"
NO_FACE_MESSAGE = "Are you still there?"
YAWN_MESSAGE = "You seem a little tired. Maybe take a short break."

# -------------------------------
# Debug Options
# -------------------------------
SHOW_FPS = True
SHOW_LANDMARKS = False
SHOW_HEAD_DIRECTION = True
SHOW_ATTENTION_SCORE = True