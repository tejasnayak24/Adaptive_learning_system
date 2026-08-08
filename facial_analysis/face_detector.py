"""
Face detection module using MediaPipe Face Mesh.
"""

import cv2
import mediapipe as mp

from config import (
    MAX_NUM_FACES,
    REFINE_LANDMARKS,
    MIN_DETECTION_CONFIDENCE,
    MIN_TRACKING_CONFIDENCE,
    SHOW_LANDMARKS,
)


class FaceDetector:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils

        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=MAX_NUM_FACES,
            refine_landmarks=REFINE_LANDMARKS,
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
        )

    def detect(self, frame):
        """
        Detect face and return:
        - face_detected (bool)
        - landmarks
        - processed_frame
        """

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb)

        if not results.multi_face_landmarks:
            return False, None, frame

        landmarks = results.multi_face_landmarks[0]

        if SHOW_LANDMARKS:
            self.mp_drawing.draw_landmarks(
                frame,
                landmarks,
                self.mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=self.mp_drawing.DrawingSpec(
                    thickness=1,
                    circle_radius=1,
                ),
            )

        return True, landmarks, frame