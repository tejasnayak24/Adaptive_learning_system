"""HTTP protocol and security checks for the loopback camera agent."""

import http.client
import json

import pytest

from agent_server import AgentServer
from backend_client import BackendUnavailable, SessionRevoked

ORIGIN = "http://localhost:5173"
SESSION = "sess_ABCDEFGH12345678"
TOKEN = "pairing_token_ABCDEFGHIJKLMNOPQRSTUVWX"


class FakeController:
    def __init__(self):
        self.started = []
        self.stopped = []
        self.start_error = None

    def status(self):
        return {"state": "idle", "session_id": None}

    def start_session(self, session_id, token):
        if self.start_error:
            raise self.start_error
        self.started.append((session_id, token))
        return {"state": "starting", "session_id": session_id}

    def stop_session(self, session_id=None, reason="stopped_by_student"):
        self.stopped.append(session_id)
        return {"state": "idle", "session_id": None}


@pytest.fixture()
def agent():
    controller = FakeController()
    server = AgentServer(controller, port=0, allowed_origins=(ORIGIN,)).start()
    yield controller, server.port
    server.stop()


def _request(port, method, path, body=None, headers=None, host=None):
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
    payload = None if body is None else (body if isinstance(body, bytes) else json.dumps(body).encode())
    all_headers = {"Host": host or f"127.0.0.1:{port}"}
    if payload is not None:
        all_headers["Content-Length"] = str(len(payload))
    all_headers.update(headers or {})
    conn.putrequest(method, path, skip_host=True, skip_accept_encoding=True)
    for key, value in all_headers.items():
        conn.putheader(key, value)
    conn.endheaders(payload)
    response = conn.getresponse()
    raw = response.read()
    conn.close()
    data = json.loads(raw) if raw else None
    return response.status, dict(response.getheaders()), data


GOOD_POST = {"Origin": ORIGIN, "X-Aegis-Client": "aegis-web", "Content-Type": "application/json"}


def test_status_from_frontend_origin_has_cors_header(agent):
    _, port = agent
    status, headers, body = _request(port, "GET", "/status", headers={"Origin": ORIGIN})
    assert status == 200
    assert body["ok"] is True and body["state"] == "idle"
    assert headers["Access-Control-Allow-Origin"] == ORIGIN
    assert headers["Cache-Control"] == "no-store"


def test_foreign_origin_is_refused(agent):
    _, port = agent
    status, headers, _ = _request(port, "GET", "/status", headers={"Origin": "https://evil.example"})
    assert status == 403
    assert "Access-Control-Allow-Origin" not in headers


def test_dns_rebinding_host_is_refused(agent):
    _, port = agent
    status, _, body = _request(port, "GET", "/status", host=f"evil.example:{port}")
    assert status == 421
    assert body["error"] == "bad_host"


def test_preflight_only_for_allowed_origin(agent):
    _, port = agent
    ok, headers, _ = _request(
        port,
        "OPTIONS",
        "/session/start",
        headers={
            "Origin": ORIGIN,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type,x-aegis-client",
            "Access-Control-Request-Private-Network": "true",
        },
    )
    assert ok == 204
    assert headers["Access-Control-Allow-Origin"] == ORIGIN
    assert "X-Aegis-Client" in headers["Access-Control-Allow-Headers"]
    assert headers["Access-Control-Allow-Private-Network"] == "true"

    bad, headers, _ = _request(port, "OPTIONS", "/session/start", headers={"Origin": "https://evil.example"})
    assert bad == 403
    assert "Access-Control-Allow-Origin" not in headers


def test_post_requires_origin_client_header_and_json(agent):
    controller, port = agent
    body = {"session_id": SESSION, "pairing_token": TOKEN}

    no_origin = {k: v for k, v in GOOD_POST.items() if k != "Origin"}
    assert _request(port, "POST", "/session/start", body, no_origin)[0] == 403

    foreign = {**GOOD_POST, "Origin": "https://evil.example"}
    assert _request(port, "POST", "/session/start", body, foreign)[0] == 403

    no_header = {k: v for k, v in GOOD_POST.items() if k != "X-Aegis-Client"}
    assert _request(port, "POST", "/session/start", body, no_header)[0] == 403

    form = {**GOOD_POST, "Content-Type": "text/plain"}
    assert _request(port, "POST", "/session/start", body, form)[0] == 415

    huge = {"session_id": SESSION, "pairing_token": TOKEN, "pad": "x" * 5000}
    assert _request(port, "POST", "/session/start", huge, GOOD_POST)[0] == 413

    assert controller.started == []


def test_start_and_stop_session(agent):
    controller, port = agent
    status, _, body = _request(port, "POST", "/session/start", {"session_id": SESSION, "pairing_token": TOKEN}, GOOD_POST)
    assert status == 200
    assert body["state"] == "starting"
    assert controller.started == [(SESSION, TOKEN)]

    status, _, body = _request(port, "POST", "/session/stop", {"session_id": SESSION}, GOOD_POST)
    assert status == 200
    assert controller.stopped == [SESSION]


def test_malformed_ids_rejected(agent):
    controller, port = agent
    assert _request(port, "POST", "/session/start", {"session_id": "../etc", "pairing_token": TOKEN}, GOOD_POST)[0] == 400
    assert _request(port, "POST", "/session/start", {"session_id": SESSION, "pairing_token": "short"}, GOOD_POST)[0] == 400
    assert _request(port, "POST", "/session/start", b"not json", GOOD_POST)[0] == 400
    assert controller.started == []


def test_backend_rejection_and_outage_are_reported(agent):
    controller, port = agent
    body = {"session_id": SESSION, "pairing_token": TOKEN}

    controller.start_error = SessionRevoked("Pairing token already used")
    status, _, data = _request(port, "POST", "/session/start", body, GOOD_POST)
    assert status == 409 and data["error"] == "pairing_rejected"
    assert TOKEN not in json.dumps(data)

    controller.start_error = BackendUnavailable("down")
    status, _, data = _request(port, "POST", "/session/start", body, GOOD_POST)
    assert status == 502 and data["error"] == "backend_unreachable"


def test_agent_refuses_non_loopback_bind():
    with pytest.raises(ValueError):
        AgentServer(FakeController(), host="0.0.0.0", port=0)
