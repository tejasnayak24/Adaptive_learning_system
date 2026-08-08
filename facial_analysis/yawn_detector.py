import math


class YawnDetector:

    def __init__(self):
        self.threshold = 0.60
        self.required_frames = 15
        self.yawn_frames = 0

    def distance(self, p1, p2):
        return math.sqrt(
            (p1.x - p2.x) ** 2 +
            (p1.y - p2.y) ** 2
        )

    def process(self, landmarks):

        points = landmarks.landmark

        upper_lip = points[13]
        lower_lip = points[14]

        left_mouth = points[61]
        right_mouth = points[291]

        vertical = self.distance(upper_lip, lower_lip)
        horizontal = self.distance(left_mouth, right_mouth)

        mar = vertical / horizontal if horizontal != 0 else 0

        if mar > self.threshold:
            self.yawn_frames += 1
        else:
            self.yawn_frames = 0

        yawning = self.yawn_frames >= self.required_frames

        return {
            "mar": round(mar, 3),
            "yawning": yawning
        }