import sys

import cv2

from config import CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT

# Camera failure codes reported to the frontend.
CAMERA_OK = "ok"
CAMERA_BLOCKED_BY_PRIVACY = "blocked_by_privacy_settings"
CAMERA_UNAVAILABLE = "unavailable"  # not found, or in use by another app
CAMERA_DISCONNECTED = "disconnected"

CAMERA_HELP = {
    CAMERA_UNAVAILABLE: (
        "The webcam could not be opened. Check that it is connected, close "
        "other apps that may be using it (Teams, Zoom, Camera, browser tabs), "
        "then press Retry."
    ),
    CAMERA_DISCONNECTED: (
        "The webcam stopped sending images. Reconnect it or close other apps "
        "using it; Aegis will reconnect automatically."
    ),
}


class CameraError(RuntimeError):
    """Raised when the webcam cannot be opened."""

    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message


def _backend():
    # DirectShow opens quickly on Windows; elsewhere let OpenCV choose.
    return cv2.CAP_DSHOW if sys.platform.startswith("win") else cv2.CAP_ANY


class Camera:
    def __init__(self, index=CAMERA_INDEX):
        self.cap = cv2.VideoCapture(index, _backend())

        if not self.cap.isOpened():
            self.cap.release()
            raise self._open_failure()

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    @staticmethod
    def _open_failure():
        from windows_privacy import HELP_TEXT, camera_privacy_status

        privacy = camera_privacy_status()
        if privacy["blocked"]:
            return CameraError(
                CAMERA_BLOCKED_BY_PRIVACY,
                f"{privacy['reason']}. {HELP_TEXT}",
            )

        return CameraError(CAMERA_UNAVAILABLE, CAMERA_HELP[CAMERA_UNAVAILABLE])

    def read_frame(self):
        success, frame = self.cap.read()

        if not success:
            return None

        return frame

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
