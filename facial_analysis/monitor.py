"""Monitoring session controller for the local camera agent.

The controller owns one learning-session monitor at a time:

* ``start_session`` (called by the local HTTP server when the browser asks)
  claims the session at the backend with the single-use pairing token and
  then activates the camera loop.
* ``run_forever`` runs on the main thread: it opens the webcam only while a
  session is active, analyses frames, plays alerts and draws the HUD.
* A heartbeat thread sends one timestamped measurement per interval. When
  the backend reports the session ended (or the token is rejected) the
  camera is released immediately.

The camera is never opened while no session is active.
"""

import threading
import time

from backend_client import BackendClient, BackendUnavailable, SessionRevoked
from camera import CAMERA_DISCONNECTED, CAMERA_HELP, CAMERA_OK, Camera, CameraError
from config import (
    CAMERA_READ_FAILURE_LIMIT,
    CAMERA_REOPEN_INTERVAL_SECONDS,
    HEARTBEAT_INTERVAL,
    MULTI_FACE_DETECTION_ENABLED,
)
from frame_processor import telemetry_from_result

AGENT_VERSION = "1.0"

# Agent-level states reported by GET /status.
IDLE = "idle"
STARTING = "starting"
CAMERA_UNAVAILABLE = "camera_unavailable"
RUNNING = "running"

# A measurement older than this is not sent as current.
MEASUREMENT_MAX_AGE = 2.0


class MonitoringController:

    def __init__(
        self,
        client=None,
        camera_factory=Camera,
        processor_factory=None,
        voice=None,
        display=True,
        clock=time.time,
        face_worker_factory=None,
    ):
        self.client = client or BackendClient()
        self.camera_factory = camera_factory
        self.processor_factory = processor_factory or _default_processor_factory
        # Multiple-face counting runs in its own thread, separate from the
        # attention pipeline. None from the factory = feature off.
        self.face_worker_factory = face_worker_factory or _default_face_worker_factory
        self.voice = voice
        self.display = display
        self.clock = clock

        self._lock = threading.RLock()
        self._active = False
        self._session_id = None
        self._generation = 0  # bumps on every start/stop so stale threads exit

        self._camera_state = "off"
        self._camera_error = None
        self._camera_message = None

        self._measurement = None
        self._measurement_at = None
        self._possible_drowsiness = False

        self._backend_connected = False
        self._backend_last_ok = None
        self._backend_error = None
        self._backend_view = None
        self._last_end_reason = None

        self._sequence = 0
        self._heartbeat_thread = None
        self._shutdown = threading.Event()

    # ------------------------------------------------------------------
    # Called from the HTTP thread
    # ------------------------------------------------------------------

    def start_session(self, session_id, pairing_token):
        """Claim ``session_id`` at the backend and start monitoring.

        Raises ``SessionRevoked`` (invalid/expired/used token) or
        ``BackendUnavailable``; the camera is not opened in that case.
        """
        # Claim first: a rejected or duplicate start request must never
        # disturb a session that is already running. The client only
        # replaces its agent token once the backend accepts the new claim.
        self.client.claim(session_id, pairing_token)

        with self._lock:
            if self._active and self._session_id != session_id:
                self._stop_locked("replaced_by_new_session", notify_backend=False)

            self._generation += 1
            self._active = True
            self._session_id = session_id
            self._sequence = 0
            self._camera_state = "starting"
            self._camera_error = None
            self._camera_message = None
            self._measurement = None
            self._measurement_at = None
            self._backend_connected = True
            self._backend_last_ok = self.clock()
            self._backend_error = None
            self._last_end_reason = None

            generation = self._generation
            self._heartbeat_thread = threading.Thread(
                target=self._heartbeat_loop, args=(generation,), daemon=True
            )
            self._heartbeat_thread.start()

        return self.status()

    def stop_session(self, session_id=None, reason="stopped_by_student"):
        with self._lock:
            if not self._active:
                return self.status()
            if session_id is not None and session_id != self._session_id:
                return self.status()
            self._stop_locked(reason)
        return self.status()

    def _stop_locked(self, reason, notify_backend=True):
        self._active = False
        self._generation += 1
        self._last_end_reason = reason
        self._camera_state = "off"
        self._measurement = None
        self._measurement_at = None
        if notify_backend:
            threading.Thread(target=self.client.end, args=(reason,), daemon=True).start()

    def status(self):
        now = self.clock()
        with self._lock:
            measurement = self._measurement if self._measurement_fresh(now) else None

            if not self._active:
                state = IDLE
            elif self._camera_state in ("starting",):
                state = STARTING
            elif self._camera_state != CAMERA_OK:
                state = CAMERA_UNAVAILABLE
            else:
                state = RUNNING

            face_detected = bool(measurement and measurement["face_detected"])
            face_stable = bool(measurement and measurement["face_stable"])

            return {
                "agent": "aegis-camera-agent",
                "version": AGENT_VERSION,
                "state": state,
                "session_id": self._session_id if self._active else None,
                "camera": {
                    "state": self._camera_state,
                    "error_code": self._camera_error,
                    "message": self._camera_message,
                },
                "face": {"detected": face_detected, "stable": face_stable},
                "lighting": {
                    "ok": None if measurement is None else measurement["lighting_ok"],
                    "brightness": None if measurement is None else measurement["brightness"],
                },
                "possible_drowsiness": bool(measurement and measurement["possible_drowsiness"]),
                "backend": {
                    "connected": self._backend_connected if self._active else False,
                    "last_ok_seconds_ago": (
                        None if self._backend_last_ok is None else round(now - self._backend_last_ok, 1)
                    ),
                    "error": self._backend_error,
                },
                "last_end_reason": self._last_end_reason,
            }

    def _measurement_fresh(self, now):
        return self._measurement_at is not None and now - self._measurement_at <= MEASUREMENT_MAX_AGE

    # ------------------------------------------------------------------
    # Heartbeat thread
    # ------------------------------------------------------------------

    def _build_heartbeat(self):
        now = self.clock()
        with self._lock:
            self._sequence += 1
            camera_ok = self._camera_state == CAMERA_OK
            measurement = self._measurement if self._measurement_fresh(now) else None

            payload = {
                "sequence": self._sequence,
                "sent_at": now,
                "captured_at": self._measurement_at if measurement else None,
                "camera_ok": camera_ok and measurement is not None,
                "camera_error": None if camera_ok else (self._camera_error or self._camera_state),
            }

            fields = (
                "face_detected", "face_stable", "lighting_ok", "brightness",
                "attention_score", "yawning", "looking_away", "eyes_closed",
                "possible_drowsiness", "eyes_closed_seconds", "head_direction", "gaze",
                "face_count", "multiple_faces",
            )
            for name in fields:
                payload[name] = measurement[name] if measurement else None
            if payload["face_detected"] is None:
                payload["face_detected"] = False
                payload["face_stable"] = False

            return payload

    def _heartbeat_loop(self, generation):
        while not self._shutdown.is_set():
            with self._lock:
                if not self._active or generation != self._generation:
                    return

            payload = self._build_heartbeat()

            try:
                view = self.client.heartbeat(payload)
                with self._lock:
                    if generation != self._generation:
                        return
                    self._backend_connected = True
                    self._backend_last_ok = self.clock()
                    self._backend_error = None
                    self._backend_view = view
            except SessionRevoked as exc:
                with self._lock:
                    if generation == self._generation and self._active:
                        self._active = False
                        self._generation += 1
                        self._camera_state = "off"
                        self._last_end_reason = f"session_ended_by_server: {exc}"
                return
            except BackendUnavailable as exc:
                with self._lock:
                    self._backend_connected = False
                    self._backend_error = str(exc)

            time.sleep(self.client.heartbeat_interval or HEARTBEAT_INTERVAL)

    # ------------------------------------------------------------------
    # Camera loop (main thread)
    # ------------------------------------------------------------------

    def run_forever(self, max_iterations=None):
        """Run until ``shutdown()``. Opens the camera only while active."""
        camera = None
        processor = None
        hud = None
        face_worker = None
        active_generation = None
        read_failures = 0
        next_open_attempt = 0.0
        iterations = 0

        try:
            while not self._shutdown.is_set():
                iterations += 1
                if max_iterations is not None and iterations > max_iterations:
                    break

                with self._lock:
                    active = self._active
                    generation = self._generation

                if not active or generation != active_generation:
                    if camera is not None:
                        camera.release()
                        camera = None
                    face_worker = _stop_worker(face_worker)
                    processor = None
                    hud = None
                    self._close_window()
                    if not active:
                        active_generation = None
                        time.sleep(0.05)
                        continue
                    active_generation = generation
                    read_failures = 0
                    next_open_attempt = 0.0

                if camera is None:
                    if self.clock() < next_open_attempt:
                        time.sleep(0.05)
                        continue
                    try:
                        camera = self.camera_factory()
                        processor = self.processor_factory()
                        hud = self._make_hud()
                        if face_worker is None:
                            face_worker = self.face_worker_factory()
                        read_failures = 0
                        self._set_camera(CAMERA_OK, None, None)
                    except CameraError as exc:
                        self._set_camera(exc.code, exc.code, exc.message)
                        next_open_attempt = self.clock() + CAMERA_REOPEN_INTERVAL_SECONDS
                        continue

                frame = camera.read_frame()
                if frame is None:
                    read_failures += 1
                    if read_failures >= CAMERA_READ_FAILURE_LIMIT:
                        camera.release()
                        camera = None
                        self._set_camera(
                            CAMERA_DISCONNECTED, CAMERA_DISCONNECTED, CAMERA_HELP[CAMERA_DISCONNECTED]
                        )
                        next_open_attempt = self.clock() + CAMERA_REOPEN_INTERVAL_SECONDS
                    else:
                        time.sleep(0.01)
                    continue

                read_failures = 0
                now = self.clock()
                if face_worker is not None:
                    face_worker.offer(frame)  # copies the frame only when a sample is due
                result = processor.process(frame, now=now)
                measurement = telemetry_from_result(result)
                measurement.update(_face_fields(face_worker))

                with self._lock:
                    if generation != self._generation:
                        continue
                    self._measurement = measurement
                    self._measurement_at = now

                self._play_alerts(result, hud)
                if self._show(result, hud):
                    self.stop_session(reason="closed_by_student")
        finally:
            if camera is not None:
                camera.release()
            _stop_worker(face_worker)
            self._close_window()

    def _set_camera(self, state, error, message):
        with self._lock:
            self._camera_state = state
            self._camera_error = error
            self._camera_message = message
            if state != CAMERA_OK:
                self._measurement = None
                self._measurement_at = None

    def _play_alerts(self, result, hud):
        for alert in result["drowsy"]["alerts"]:
            if self.voice is not None:
                self.voice.say(alert["message"], beeps=alert["beeps"], beep_ms=alert["beep_ms"])
            if hud is not None:
                hud.show_alert(alert["type"], alert["message"])

    def _make_hud(self):
        if not self.display:
            return None
        from hud import HUD

        return HUD(self.client.student_label or "signed in")

    def _show(self, result, hud):
        """Draw the HUD window. Returns True when the student pressed Q."""
        if not self.display or hud is None:
            return False
        import cv2

        frame = result["frame"]
        status = self.status()
        hud.draw(
            frame,
            fps=_fps(result),
            backend_connected=status["backend"]["connected"],
            presence=result["presence"],
            drowsy=result["drowsy"],
            eye=result["eye"],
            head=result["head"],
            gaze=result["gaze"],
            attention=result["attention"],
        )
        cv2.imshow("Aegis Camera Agent", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("h"):
            hud.toggle_compact()
        return key == ord("q")

    def _close_window(self):
        if not self.display:
            return
        try:
            import cv2

            cv2.destroyAllWindows()
        except Exception:
            pass

    def shutdown(self):
        self.stop_session(reason="agent_shutdown")
        self._shutdown.set()


_last_frame_time = [None]


def _fps(result):
    now = result["timestamp"]
    previous = _last_frame_time[0]
    _last_frame_time[0] = now
    if previous is None or now <= previous:
        return 0.0
    return 1.0 / (now - previous)


def _default_processor_factory():
    from frame_processor import FrameProcessor

    return FrameProcessor()


def _default_face_worker_factory():
    if not MULTI_FACE_DETECTION_ENABLED:
        return None
    from face_counter import FaceCountWorker

    return FaceCountWorker()


def _stop_worker(worker):
    if worker is not None:
        worker.stop()
    return None


def _face_fields(worker):
    """Multiple-face fields for a measurement: None = not measured."""
    latest = worker.latest() if worker is not None and worker.error is None else None
    if latest is None:
        return {"face_count": None, "multiple_faces": None}
    return {"face_count": latest["face_count"], "multiple_faces": latest["multiple_faces"]}
