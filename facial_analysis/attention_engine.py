from collections import deque


class AttentionEngine:

    def __init__(self):

        self.history = deque(maxlen=30)

    def update(
        self,
        face,
        eyes_open,
        head_direction,
        blink_rate,
    ):

        score = 100

        if not face:
            score -= 40

        if not eyes_open:
            score -= 20

        if head_direction != "Forward":
            score -= 20

        if blink_rate > 30:
            score -= 10

        score = max(0, min(score, 100))

        self.history.append(score)

        average = sum(self.history) / len(self.history)

        if average >= 85:
            status = "Highly Attentive"

        elif average >= 70:
            status = "Attentive"

        elif average >= 50:
            status = "Slightly Distracted"

        else:
            status = "Distracted"

        return {
            "score": round(average),
            "status": status
        }