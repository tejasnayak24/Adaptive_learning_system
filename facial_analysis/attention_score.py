"""
Attention score calculator.
Combines outputs from face detection, eye tracking, and head pose.
"""


class AttentionScorer:

    def __init__(self):
        self.score = 0

    def calculate(
        self,
        face_detected,
        eyes_open,
        head_direction,
    ):

        score = 0

        # Face detected
        if face_detected:
            score += 30

        # Eyes open
        if eyes_open:
            score += 20

        # Looking forward
        if head_direction == "Forward":
            score += 25

        # Head stable
        if head_direction == "Forward":
            score += 15

        # Face continuously visible
        if face_detected:
            score += 10

        self.score = score

        return {
            "score": score,
            "status": self.get_status(score)
        }

    def get_status(self, score):

        if score >= 85:
            return "Highly Attentive"

        elif score >= 60:
            return "Attentive"

        elif score >= 40:
            return "Slightly Distracted"

        else:
            return "Distracted"