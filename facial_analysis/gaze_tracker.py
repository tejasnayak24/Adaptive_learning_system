"""
Simple gaze estimation using iris landmarks.
"""

class GazeTracker:

    LEFT_IRIS = [474, 475, 476, 477]
    RIGHT_IRIS = [469, 470, 471, 472]

    LEFT_EYE = [33, 133]
    RIGHT_EYE = [362, 263]

    def process(self, landmarks):

        lm = landmarks.landmark

        left_iris = lm[468]
        right_iris = lm[473]

        left_eye_left = lm[self.LEFT_EYE[0]]
        left_eye_right = lm[self.LEFT_EYE[1]]

        right_eye_left = lm[self.RIGHT_EYE[0]]
        right_eye_right = lm[self.RIGHT_EYE[1]]

        left_ratio = (
            (left_iris.x - left_eye_left.x) /
            (left_eye_right.x - left_eye_left.x)
        )

        right_ratio = (
            (right_iris.x - right_eye_left.x) /
            (right_eye_right.x - right_eye_left.x)
        )

        ratio = (left_ratio + right_ratio) / 2

        if ratio < 0.40:
            gaze = "Left"

        elif ratio > 0.60:
            gaze = "Right"

        else:
            gaze = "Center"

        return {
            "ratio": round(ratio,3),
            "gaze": gaze
        }