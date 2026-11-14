"""Session lifecycle of the camera agent, with a fake camera and backend."""

import threading
import time

import pytest

from backend_client import SessionRevoked
from camera import CAMERA_BLOCKED_BY_PRIVACY, CameraError
from frame_processor import FrameProcessor
from monitor import CAMERA_UNAVAILABLE, IDLE, RUNNING, MonitoringController
from synthetic import ScriptedDetector, face


class FakeClient:
    def __init__(self):
        self.heartbeats = []
        self.claims = []
        self.ended = []
        self.revoke_after = None
        self.heartbeat_interval = 0.05
        self.student_label = "Test Student"
        self._paired = False

    def forget(self):
        self._paired = False

    def claim(self, session_id, token):
        self.claims.append((session_id, token))
        self._paired = True
        return {"agent_token": "x"}

    def heartbeat(self, payload):
        self.heartbeats.append(payload)
        if self.revoke_after is not None and len(self.heartbeats) >= self.revoke_after:
            raise SessionRevoked("Session ended")
        return {"state": "verified"}

    def end(self, reason="agent_stopped"):
        self.ended.append(reason)


class FakeCamera:
    instances = []

    def __init__(self, frames_ok=True):
        self.frames_ok = frames_ok
        self.released = False
        FakeCamera.instances.append(self)

    def read_frame(self):
        time.sleep(0.01)
        return "frame" if self.frames_ok else None

    def release(self):
        self.released = True


def _processor_factory():
    return FrameProcessor(face_detector=ScriptedDetector(face()), brightness_fn=lambda f: 120.0)


@pytest.fixture()
def running():
    FakeCamera.instances = []
    client = FakeClient()
    state = {"camera_factory": FakeCamera}

    controller = MonitoringController(
        client=client,
        camera_factory=lambda: state["camera_factory"](),
        processor_factory=_processor_factory,
        display=False,
    )
    thread = threading.Thread(target=controller.run_forever, daemon=True)
    thread.start()
    yield controller, client, state
    controller.shutdown()
    thread.join(timeout=3)


def _wait(predicate, timeout=4.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if predicate():
            return True
        time.sleep(0.02)
    return False


def test_camera_stays_closed_until_session_starts(running):
    controller, _, _ = running
    time.sleep(0.2)
    assert FakeCamera.instances == []
    assert controller.status()["state"] == IDLE


def test_session_start_opens_camera_and_sends_heartbeats(running):
    controller, client, _ = running
    controller.start_session("sess_ABCDEFGH12345678", "token")

    assert client.claims == [("sess_ABCDEFGH12345678", "token")]
    assert _wait(lambda: controller.status()["state"] == RUNNING)
    assert _wait(lambda: any(h["face_detected"] for h in client.heartbeats))

    beats = list(client.heartbeats)
    sequences = [h["sequence"] for h in beats]
    assert sequences == sorted(sequences) and len(set(sequences)) == len(sequences)

    live = [h for h in beats if h["face_detected"]][-1]
    assert live["camera_ok"] is True
    assert live["captured_at"] is not None
    assert 0.0 <= live["attention_score"] <= 1.0
    assert "student_id" not in live  # the agent never asserts an identity

    status = controller.status()
    assert status["face"]["detected"] is True
    assert status["backend"]["connected"] is True


def test_stop_session_releases_camera(running):
    controller, client, _ = running
    controller.start_session("sess_ABCDEFGH12345678", "token")
    assert _wait(lambda: controller.status()["state"] == RUNNING)

    controller.stop_session("sess_ABCDEFGH12345678")
    assert _wait(lambda: FakeCamera.instances[-1].released)
    assert controller.status()["state"] == IDLE
    assert _wait(lambda: client.ended == ["stopped_by_student"])


def test_server_side_end_stops_camera(running):
    controller, client, _ = running
    client.revoke_after = 3
    controller.start_session("sess_ABCDEFGH12345678", "token")

    assert _wait(lambda: controller.status()["state"] == IDLE)
    assert _wait(lambda: FakeCamera.instances and FakeCamera.instances[-1].released)
    assert "session_ended_by_server" in controller.status()["last_end_reason"]


def test_camera_blocked_by_privacy_is_reported_without_measurements(running):
    controller, client, state = running

    def blocked():
        raise CameraError(CAMERA_BLOCKED_BY_PRIVACY, "Desktop apps are not allowed to use the camera")

    state["camera_factory"] = blocked
    controller.start_session("sess_ABCDEFGH12345678", "token")

    assert _wait(lambda: controller.status()["state"] == CAMERA_UNAVAILABLE)
    status = controller.status()
    assert status["camera"]["error_code"] == CAMERA_BLOCKED_BY_PRIVACY
    assert "Desktop apps" in status["camera"]["message"]

    assert _wait(lambda: any(h["camera_error"] == CAMERA_BLOCKED_BY_PRIVACY for h in client.heartbeats))
    beat = [h for h in client.heartbeats if h["camera_error"] == CAMERA_BLOCKED_BY_PRIVACY][-1]
    assert beat["camera_ok"] is False
    assert beat["camera_error"] == CAMERA_BLOCKED_BY_PRIVACY
    assert beat["attention_score"] is None and beat["captured_at"] is None


def test_disconnected_camera_is_detected_and_reopened(running, monkeypatch):
    import monitor

    monkeypatch.setattr(monitor, "CAMERA_READ_FAILURE_LIMIT", 3)
    monkeypatch.setattr(monitor, "CAMERA_REOPEN_INTERVAL_SECONDS", 0.1)
    controller, client, state = running

    state["camera_factory"] = lambda: FakeCamera(frames_ok=False)
    controller.start_session("sess_ABCDEFGH12345678", "token")
    assert _wait(lambda: controller.status()["camera"]["error_code"] == "disconnected")
    assert FakeCamera.instances[0].released

    # Plugging the camera back in resumes monitoring automatically.
    state["camera_factory"] = FakeCamera
    assert _wait(lambda: controller.status()["state"] == RUNNING)
    assert _wait(lambda: client.heartbeats[-1]["camera_ok"] is True)


def test_stale_measurement_is_not_sent_as_current(running):
    controller, client, _ = running
    controller.start_session("sess_ABCDEFGH12345678", "token")
    assert _wait(lambda: controller.status()["state"] == RUNNING)

    # Simulate a frozen camera loop: the last measurement ages past the limit.
    with controller._lock:
        controller._measurement_at = time.time() - 10
        controller._camera_state = "ok"
    payload = controller._build_heartbeat()
    assert payload["camera_ok"] is False
    assert payload["attention_score"] is None


def test_rejected_start_does_not_disturb_running_session(running):
    controller, client, _ = running
    controller.start_session("sess_ABCDEFGH12345678", "token")
    assert _wait(lambda: controller.status()["state"] == RUNNING)

    def reject(session_id, token):
        raise SessionRevoked("Pairing token already used")

    client.claim = reject
    with pytest.raises(SessionRevoked):
        controller.start_session("sess_ABCDEFGH12345678", "replayed-token")

    beats = len(client.heartbeats)
    assert _wait(lambda: len(client.heartbeats) > beats + 2)  # still heartbeating
    assert controller.status()["state"] == RUNNING
    assert client._paired is True
