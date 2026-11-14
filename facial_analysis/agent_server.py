"""Loopback HTTP interface of the Aegis camera agent.

Endpoints (all on http://127.0.0.1:8765):

* ``GET  /status``          -- agent / camera / face / backend state.
* ``POST /session/start``   -- ``{session_id, pairing_token}``; claims the
  learning session at the backend and starts the camera.
* ``POST /session/stop``    -- ``{session_id}``; stops the camera.

Protections:

* The socket is bound to 127.0.0.1 only (not reachable from the network).
* ``Host`` must be ``127.0.0.1:<port>`` or ``localhost:<port>``; this
  defeats DNS-rebinding attacks from malicious web pages.
* Cross-origin access is limited to the configured Aegis frontend origins.
  POST requests must come from an allowed ``Origin`` and carry the custom
  ``X-Aegis-Client`` header with ``Content-Type: application/json``; a
  browser can only send these after a CORS preflight that the agent
  approves solely for allowed origins, so other sites cannot forge
  requests (CSRF).
* Request bodies are size-limited and never logged; tokens are held in
  memory only.
"""

import json
import re
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from backend_client import BackendUnavailable, SessionRevoked
from config import AGENT_ALLOWED_ORIGINS, AGENT_HOST, AGENT_PORT

CLIENT_HEADER = "X-Aegis-Client"
CLIENT_HEADER_VALUE = "aegis-web"
MAX_BODY_BYTES = 4096
_SESSION_ID_RE = re.compile(r"^[A-Za-z0-9_-]{8,64}$")
_TOKEN_RE = re.compile(r"^[A-Za-z0-9_-]{20,128}$")


def make_handler(controller, allowed_origins=AGENT_ALLOWED_ORIGINS):
    allowed_origins = tuple(allowed_origins)

    class AgentHandler(BaseHTTPRequestHandler):
        server_version = "AegisCameraAgent/1.0"
        sys_version = ""

        # -- helpers ---------------------------------------------------

        def log_message(self, fmt, *args):
            # Only method, path and status are ever logged (no bodies).
            pass

        def _origin(self):
            return self.headers.get("Origin")

        def _origin_allowed(self):
            return self._origin() in allowed_origins

        def _send(self, status, body=None, cors=True):
            payload = b"" if body is None else json.dumps(body).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            if cors and self._origin_allowed():
                self.send_header("Access-Control-Allow-Origin", self._origin())
                self.send_header("Vary", "Origin")
            self.end_headers()
            if payload:
                self.wfile.write(payload)

        def _error(self, status, code, message):
            self._send(status, {"ok": False, "error": code, "message": message})

        def _host_ok(self):
            port = self.server.server_address[1]
            allowed_hosts = {f"127.0.0.1:{port}", f"localhost:{port}"}
            if self.headers.get("Host") not in allowed_hosts:
                self._send(421, {"ok": False, "error": "bad_host", "message": "Unexpected Host header"}, cors=False)
                return False
            return True

        def _read_json(self):
            if (self.headers.get("Content-Type") or "").split(";")[0].strip().lower() != "application/json":
                self._error(415, "unsupported_media_type", "Content-Type must be application/json")
                return None
            try:
                length = int(self.headers.get("Content-Length") or 0)
            except ValueError:
                length = -1
            if length < 0 or length > MAX_BODY_BYTES:
                self._error(413, "body_too_large", "Request body too large")
                return None
            try:
                body = json.loads(self.rfile.read(length) or b"{}")
            except (ValueError, UnicodeDecodeError):
                self._error(400, "invalid_json", "Body must be valid JSON")
                return None
            if not isinstance(body, dict):
                self._error(400, "invalid_json", "Body must be a JSON object")
                return None
            return body

        def _post_allowed(self):
            if not self._origin_allowed():
                self._send(403, {"ok": False, "error": "origin_not_allowed", "message": "Origin not allowed"}, cors=False)
                return False
            if self.headers.get(CLIENT_HEADER) != CLIENT_HEADER_VALUE:
                self._error(403, "missing_client_header", f"{CLIENT_HEADER} header required")
                return False
            return True

        # -- verbs -----------------------------------------------------

        def do_OPTIONS(self):
            if not self._host_ok():
                return
            if not self._origin_allowed():
                self._send(403, None, cors=False)
                return
            self.send_response(204)
            self.send_header("Access-Control-Allow-Origin", self._origin())
            self.send_header("Vary", "Origin")
            self.send_header("Access-Control-Allow-Methods", "GET, POST")
            self.send_header("Access-Control-Allow-Headers", f"Content-Type, {CLIENT_HEADER}")
            self.send_header("Access-Control-Max-Age", "600")
            if self.headers.get("Access-Control-Request-Private-Network") == "true":
                self.send_header("Access-Control-Allow-Private-Network", "true")
            self.send_header("Content-Length", "0")
            self.end_headers()

        def do_GET(self):
            if not self._host_ok():
                return
            if self._origin() is not None and not self._origin_allowed():
                self._send(403, {"ok": False, "error": "origin_not_allowed", "message": "Origin not allowed"}, cors=False)
                return
            if self.path != "/status":
                self._error(404, "not_found", "Not found")
                return
            self._send(200, {"ok": True, **controller.status()})

        def do_POST(self):
            if not self._host_ok() or not self._post_allowed():
                return

            body = self._read_json()
            if body is None:
                return

            session_id = body.get("session_id")
            if not isinstance(session_id, str) or not _SESSION_ID_RE.match(session_id):
                self._error(400, "invalid_session_id", "session_id is missing or malformed")
                return

            if self.path == "/session/start":
                token = body.get("pairing_token")
                if not isinstance(token, str) or not _TOKEN_RE.match(token):
                    self._error(400, "invalid_pairing_token", "pairing_token is missing or malformed")
                    return
                try:
                    status = controller.start_session(session_id, token)
                except SessionRevoked as exc:
                    self._error(409, "pairing_rejected", f"The backend rejected the pairing: {exc}")
                    return
                except BackendUnavailable:
                    self._error(502, "backend_unreachable", "The camera agent cannot reach the Aegis backend")
                    return
                self._send(200, {"ok": True, **status})
                return

            if self.path == "/session/stop":
                self._send(200, {"ok": True, **controller.stop_session(session_id)})
                return

            self._error(404, "not_found", "Not found")

    return AgentHandler


class AgentServer:
    """Runs the loopback HTTP server on a background thread."""

    def __init__(self, controller, host=AGENT_HOST, port=AGENT_PORT, allowed_origins=AGENT_ALLOWED_ORIGINS):
        if host not in ("127.0.0.1", "::1"):
            raise ValueError("The camera agent may only listen on the loopback interface")
        self.httpd = ThreadingHTTPServer((host, port), make_handler(controller, allowed_origins))
        self.httpd.daemon_threads = True
        self.port = self.httpd.server_address[1]
        self._thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)

    def start(self):
        self._thread.start()
        return self

    def stop(self):
        self.httpd.shutdown()
        self.httpd.server_close()
