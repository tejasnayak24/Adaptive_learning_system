"""
Configuration settings for the Facial Analysis module and camera agent.
"""

# -------------------------------
# Camera Configuration
# -------------------------------
CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FPS = 30

# Consecutive failed frame reads before the camera is treated as
# disconnected (it is then reopened automatically while a session runs).
CAMERA_READ_FAILURE_LIMIT = 15
CAMERA_REOPEN_INTERVAL_SECONDS = 2.0

# -------------------------------
# MediaPipe Configuration
# -------------------------------
MAX_NUM_FACES = 1
REFINE_LANDMARKS = True
MIN_DETECTION_CONFIDENCE = 0.6
MIN_TRACKING_CONFIDENCE = 0.6

# -------------------------------
# Attention / Presence Thresholds
# -------------------------------
EYE_CLOSED_THRESHOLD = 1.0
FACE_MISSING_THRESHOLD = 5.0

# Looking away must persist this long before it counts (a quick glance
# at the keyboard is not "looking away").
LOOK_AWAY_THRESHOLD = 2.0

# A face is "stable" when detected in at least this fraction of the
# frames seen during the last FACE_STABILITY_WINDOW_SECONDS.
FACE_STABILITY_WINDOW_SECONDS = 2.0
FACE_STABILITY_MIN_RATIO = 0.8

# Mean grey level (0-255) below which lighting is reported as too dark.
LOW_LIGHT_BRIGHTNESS = 45

# -------------------------------
# Multiple-face detection (separate from the attention pipeline)
# -------------------------------
# MediaPipe Face Detection on a downscaled copy of a frame, about twice a
# second, in its own thread. Only the face count and a yes/no signal are
# sent; frames are never stored or transmitted.
MULTI_FACE_DETECTION_ENABLED = True
MULTI_FACE_INTERVAL_SECONDS = 0.5
MULTI_FACE_WORK_WIDTH = 320            # pixels; frames are downscaled to this width
MULTI_FACE_MIN_CONFIDENCE = 0.6        # detection score needed to count a face
# A face counts only if at least this fraction of the largest face's width,
# so small faces far behind the student (posters, a TV) are ignored.
MULTI_FACE_MIN_RELATIVE_SIZE = 0.4
# Sustained detection: 2+ faces in 5 of the last 6 samples (~3 s) starts a
# "multiple faces" episode; 4 samples in a row below 2 (~2 s) clears it.
MULTI_FACE_WINDOW_SAMPLES = 6
MULTI_FACE_REQUIRED_SAMPLES = 5
MULTI_FACE_CLEAR_SAMPLES = 4
# A face-count result older than this is not sent as current.
MULTI_FACE_RESULT_MAX_AGE_SECONDS = 2.0

# -------------------------------
# Backend / Local Agent
# -------------------------------

API_BASE_URL = "http://127.0.0.1:8000"

# The local agent listens only on the loopback interface.
AGENT_HOST = "127.0.0.1"
AGENT_PORT = 8765

# Browser origins allowed to control the agent (the Aegis frontend).
AGENT_ALLOWED_ORIGINS = (
    "http://localhost:5173",
    "http://127.0.0.1:5173",
)

# Seconds between heartbeats sent to the backend.
HEARTBEAT_INTERVAL = 1.0

# Retained for the legacy preview mode; the agent never trusts or sends
# a configured student id (the backend derives it from the session token).
STUDENT_ID = None

SEND_INTERVAL = 1

# -------------------------------
# Drowsiness Detection (possible drowsiness, not a medical assessment)
# -------------------------------
EYES_CLOSED_ALERT_SECONDS = 2.0      # eyes closed this long -> wake-up alert
DROWSY_ALERT_REPEAT_SECONDS = 5.0    # repeat wake-up alert while eyes stay closed
NO_FACE_ALERT_SECONDS = 10.0         # no face this long -> "are you still there?"
NO_FACE_ALERT_REPEAT_SECONDS = 30.0  # repeat while the face is still missing
WAKE_UP_ESCALATE_AFTER = 3           # wake-up alerts in a row before escalating

# -------------------------------
# Yawn Alerts
# -------------------------------
YAWN_ALERT_MIN_GAP_SECONDS = 15.0        # minimum gap between spoken yawn alerts
FREQUENT_YAWN_COUNT = 3                  # this many yawns ...
FREQUENT_YAWN_WINDOW_SECONDS = 300.0     # ... within 5 minutes -> break message
FREQUENT_YAWN_COOLDOWN_SECONDS = 120.0   # minimum gap between break messages

# -------------------------------
# Voice Alerts
# -------------------------------
VOICE_ALERTS_ENABLED = True
VOICE_RATE = 150                     # words per minute (pyttsx3 default is 200)
VOICE_VOLUME = 1.0                   # 0.0 - 1.0
PREFERRED_VOICE_LANGUAGES = ["en-IN", "en-US", "en-GB"]  # first match wins
BEEP_FREQUENCY = 1000                # Hz
BEEP_DURATION_MS = 400
ESCALATED_BEEP_DURATION_MS = 700     # each beep of the escalated double beep
BEEP_GAP_MS = 150                    # pause between beeps

WAKE_UP_MESSAGE = "Hey, wake up!"
ESCALATED_WAKE_UP_MESSAGE = "Wake up now! Please open your eyes and sit up straight."
NO_FACE_MESSAGE = "Are you still there?"
YAWN_MESSAGES = [
    "You seem a little tired. Maybe take a short break.",
    "Feeling sleepy? Try stretching for a moment.",
    "A sip of water might help you stay fresh.",
]
FREQUENT_YAWN_MESSAGE = "You've yawned several times. Let's take a five minute break."

# -------------------------------
# On-screen Dashboard (HUD)
# -------------------------------
SHOW_HUD = True
ALERT_BANNER_SECONDS = 3.0           # how long an alert banner stays on screen

# -------------------------------
# Debug Options
# -------------------------------
SHOW_FPS = True
SHOW_LANDMARKS = False
SHOW_HEAD_DIRECTION = True
SHOW_ATTENTION_SCORE = True
