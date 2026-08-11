"""
Head pose estimation using MediaPipe Face Mesh landmarks.
"""

import math


class HeadPoseEstimator:

    # MediaPipe landmark indices
    NOSE_TIP = 1
    LEFT_CHEEK = 234
    RIGHT_CHEEK = 454
    FOREHEAD = 10
    CHIN = 152

    def process(self, landmarks):

        lm = landmarks.landmark

        nose = lm[self.NOSE_TIP]
        left = lm[self.LEFT_CHEEK]
        right = lm[self.RIGHT_CHEEK]
        forehead = lm[self.FOREHEAD]
        chin = lm[self.CHIN]

        # Horizontal rotation (Yaw)
        yaw = nose.x - ((left.x + right.x) / 2)

        # Vertical rotation (Pitch)
        pitch = nose.y - ((forehead.y + chin.y) / 2)

        direction = "Forward"

        if yaw > 0.03:
            direction = "Left"

        elif yaw < -0.03:
            direction = "Right"

        elif pitch > 0.04:
            direction = "Down"

        elif pitch < -0.04:
            direction = "Up"                 

        return {
            "yaw": round(yaw, 3),
            "pitch": round(pitch, 3),
            "direction": direction
        }