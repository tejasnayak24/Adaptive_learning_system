from fer import FER
import cv2


class EmotionDetector:

    def __init__(self):
        # Use MTCNN for better face detection
        self.detector = FER(mtcnn=True)

    def process(self, frame):

        result = self.detector.detect_emotions(frame)

        if len(result) == 0:
            return {
                "emotion": "Unknown",
                "confidence": 0
            }

        emotions = result[0]["emotions"]

        emotion = max(emotions, key=emotions.get)

        confidence = emotions[emotion]

        return {
            "emotion": emotion.capitalize(),
            "confidence": round(confidence * 100, 1)
        }