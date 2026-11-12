"""End-to-end: real backend process + real camera agent (synthetic camera).

Runs only when AEGIS_BACKEND_PYTHON points at the Python interpreter that
has the backend's dependencies (the facial venv deliberately does not):

    $env:AEGIS_BACKEND_PYTHON = (Get-Command python).Source   # backend Python
    .\\venv\\Scripts\\python.exe -m pytest tests\\test_integration_backend.py

The backend uses a throwaway SQLite database (migrated + seeded), never
PostgreSQL. The webcam is replaced by a fake camera whose frames are
analysed by the real FrameProcessor with synthetic face landmarks.
"""

import os
import socket
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

import pytest
import requests

from agent_server import AgentServer
from backend_client import BackendClient
from camera import CAMERA_UNAVAILABLE, CameraError
from frame_processor import FrameProcessor
from monitor import MonitoringController
from synthetic import ScriptedDetector, face

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
ORIGIN = "http://localhost:5173"
AGENT_HEADERS = {"Origin": ORIGIN, "X-Aegis-Client": "aegis-web", "Content-Type": "application/json"}

BACKEND_PYTHON = os.environ.get("AEGIS_BACKEND_PYTHON")
pytestmark = pytest.mark.skipif(not BACKEND_PYTHON, reason="set AEGIS_BACKEND_PYTHON to run")


def _free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="module")
def backend_url():
    tmp = Path(tempfile.mkdtemp(prefix="aegis-e2e-"))
    port = _free_port()
    env = {
        **os.environ,
        "DATABASE_URL": f"sqlite:///{(tmp / 'e2e.db').as_posix()}",
        "SECRET_KEY": "e2e-secret-not-for-production",
        "ALGORITHM": "HS256",
        "ACCESS_TOKEN_EXPIRE_MINUTES": "30",
        "PYTHONPATH": str(BACKEND),
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    subprocess.run([BACKEND_PYTHON, "-m", "alembic", "upgrade", "head"], cwd=BACKEND, env=env, check=True, capture_output=True)
    subprocess.run([BACKEND_PYTHON, str(BACKEND / "seed_science.py")], cwd=ROOT, env=env, check=True, capture_output=True)

    log = open(tmp / "backend.log", "w")
    proc = subprocess.Popen(
        [BACKEND_PYTHON, "-m", "uvicorn", "backend.app.main:app", "--port", str(port)],
        cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT,
    )
    url = f"http://127.0.0.1:{port}"
    for _ in range(100):
        try:
            if requests.get(url + "/", timeout=0.5).status_code == 200:
                break
        except requests.RequestException:
            time.sleep(0.2)
    else:
        proc.terminate()
        pytest.fail("backend did not start")

    yield url
    proc.terminate()
    proc.wait(timeout=10)
    log.close()


class Camera:
    """Fake webcam. ``state["fail"]`` simulates an unplugged / blocked camera."""

    state = {"fail": False}

    def __init__(self):
        if Camera.state["fail"]:
            raise CameraError(CAMERA_UNAVAILABLE, "The webcam could not be opened.")

    def read_frame(self):
        time.sleep(0.03)
        return None if Camera.state["fail"] else "frame"

    def release(self):
        pass


class Agent:
    """A real agent (HTTP server + controller) on its own port."""

    def __init__(self, backend_url, detector):
        self.controller = MonitoringController(
            client=BackendClient(base_url=backend_url),
            camera_factory=Camera,
            processor_factory=lambda: FrameProcessor(face_detector=detector, brightness_fn=lambda f: 120.0),
            display=False,
        )
        self.server = AgentServer(self.controller, port=0, allowed_origins=(ORIGIN,)).start()
        self.url = f"http://127.0.0.1:{self.server.port}"
        self.thread = threading.Thread(target=self.controller.run_forever, daemon=True)
        self.thread.start()

    def crash(self):
        """Simulate the agent process dying (no goodbye to the backend)."""
        self.controller._shutdown.set()
        with self.controller._lock:
            self.controller._active = False
            self.controller._generation += 1
        self.server.stop()
        self.thread.join(timeout=3)


def _wait_for_state(get_state, expected, timeout=12):
    deadline = time.time() + timeout
    seen = None
    while time.time() < deadline:
        seen = get_state()
        if seen in expected:
            return seen
        time.sleep(0.25)
    raise AssertionError(f"expected {expected}, last state {seen!r}")


def test_full_monitored_learning_session(backend_url):
    http = requests.Session()
    email = f"e2e.{int(time.time() * 1000)}@example.com"
    assert http.post(f"{backend_url}/register", json={"name": "Ira Test", "email": email, "password": "E2e-Pass-123", "age": 13}).status_code == 200
    token = http.post(f"{backend_url}/login", json={"email": email, "password": "E2e-Pass-123"}).json()["access_token"]
    auth = {"Authorization": f"Bearer {token}"}
    me = http.get(f"{backend_url}/profile", headers=auth).json()["data"]

    # Consent (minor: guardian + school confirmations) then a monitored session.
    assert http.post(f"{backend_url}/monitoring/sessions", json={}, headers=auth).status_code == 403
    http.post(
        f"{backend_url}/monitoring/consent",
        json={"accept": True, "guardian_authorization_confirmed": True, "school_authorization_confirmed": True},
        headers=auth,
    ).raise_for_status()
    created = http.post(f"{backend_url}/monitoring/sessions", json={"lesson_id": 1}, headers=auth).json()["data"]
    sid = created["session_id"]

    def backend_state():
        return http.get(f"{backend_url}/monitoring/sessions/{sid}", headers=auth).json()["data"]["state"]

    detector = ScriptedDetector(face())
    agent = Agent(backend_url, detector)

    # 1. Agent idle, camera closed; browser hands over the pairing token.
    assert requests.get(f"{agent.url}/status", headers={"Origin": ORIGIN}).json()["state"] == "idle"
    started = requests.post(f"{agent.url}/session/start", json={"session_id": sid, "pairing_token": created["pairing_token"]}, headers=AGENT_HEADERS)
    assert started.status_code == 200, started.text
    assert _wait_for_state(backend_state, {"verified"}) == "verified"

    # The pairing token is single use.
    replay = requests.post(f"{agent.url}/session/start", json={"session_id": sid, "pairing_token": created["pairing_token"]}, headers=AGENT_HEADERS)
    assert replay.status_code == 409
    # ...and a rejected (replayed / duplicate) start never disturbs the running session.
    time.sleep(2)
    assert backend_state() == "verified"

    # 2. A monitored quiz: camera values come from the server's telemetry.
    quiz = http.get(f"{backend_url}/quiz/1", headers=auth).json()["data"]
    http.post(f"{backend_url}/attention/{me['id']}/reset", headers=auth).raise_for_status()
    time.sleep(2.5)
    answers = {str(q["id"]): "A" for q in quiz["questions"]}
    submitted = http.post(
        f"{backend_url}/quiz/submit",
        json={"quiz_id": 1, "monitoring_session_id": sid, "answers": answers, "response_time": 30, "attention_score": 0.01},
        headers=auth,
    )
    assert submitted.status_code == 200, submitted.text
    result = submitted.json()["data"]
    assert result["progress"]["attention_score"] is not None and result["progress"]["attention_score"] > 0.5
    assert result["progress"]["drowsy"] is False
    assert result["recommendation"] is not None

    # 3. Student leaves the frame -> no_face (learning pauses), back -> verified.
    detector.face_visible = False
    _wait_for_state(backend_state, {"no_face"})
    detector.face_visible = True
    _wait_for_state(backend_state, {"verified"})

    # 4. Sustained eye closure -> possible drowsiness reaches the backend.
    detector.landmarks = face(eye_opening=0.01)
    deadline = time.time() + 8
    drowsy = False
    while time.time() < deadline and not drowsy:
        drowsy = bool(http.get(f"{backend_url}/attention/{me['id']}", headers=auth).json()["data"]["possible_drowsiness"])
        time.sleep(0.25)
    assert drowsy
    detector.landmarks = face()

    # 5. Webcam unplugged -> camera_unavailable; plugged back -> verified.
    Camera.state["fail"] = True
    _wait_for_state(backend_state, {"camera_unavailable"})
    Camera.state["fail"] = False
    _wait_for_state(backend_state, {"verified"}, timeout=15)

    # 6. Agent crashes -> heartbeats stop -> stale (never treated as verified).
    agent.crash()
    _wait_for_state(backend_state, {"stale"}, timeout=10)

    # 7. Agent restarted -> browser re-pairs the SAME session, no new login.
    agent = Agent(backend_url, detector)
    data = http.post(f"{backend_url}/monitoring/sessions/{sid}/pairing", headers=auth).json()["data"]
    assert data["session_id"] == sid
    requests.post(f"{agent.url}/session/start", json={"session_id": sid, "pairing_token": data["pairing_token"]}, headers=AGENT_HEADERS).raise_for_status()
    _wait_for_state(backend_state, {"verified"})

    # 8. Learning session ends -> agent stops the camera.
    http.post(f"{backend_url}/monitoring/sessions/{sid}/end", headers=auth).raise_for_status()
    _wait_for_state(lambda: requests.get(f"{agent.url}/status").json()["state"], {"idle"}, timeout=6)
    assert backend_state() == "ended"
    agent.crash()
