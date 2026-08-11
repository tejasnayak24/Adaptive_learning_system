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

STUDENT_ID = 1

SEND_INTERVAL = 1

# -------------------------------
# Debug Options
# -------------------------------
SHOW_FPS = True
SHOW_LANDMARKS = False
SHOW_HEAD_DIRECTION = True
SHOW_ATTENTION_SCORE = True