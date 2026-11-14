"""HTTP client the camera agent uses to talk to the Aegis backend.

Security notes:
* The single-use pairing token is sent once, in a JSON body, to claim the
  session; the backend answers with an agent token bound to that student
  and session.
* The agent token is kept only in memory and sent in the Authorization
  header. Tokens are never put in URLs and never printed or logged.
* The agent never supplies a student id: the backend derives it from the
  token.
"""

import requests

from config import API_BASE_URL


class SessionRevoked(Exception):
    """The backend no longer accepts this session (ended, expired, revoked)."""


class BackendUnavailable(Exception):
    """The backend could not be reached or answered with an error."""


class BackendClient:

    def __init__(self, base_url=API_BASE_URL, timeout=3.0, http=None):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.http = http or requests.Session()
        self._agent_token = None
        self.session_id = None
        self.student_label = None
        self.heartbeat_interval = 1.0

    @property
    def paired(self):
        return self._agent_token is not None

    def claim(self, session_id, pairing_token):
        """Exchange a single-use pairing token for an agent token."""
        try:
            response = self.http.post(
                f"{self.base_url}/monitoring/sessions/{session_id}/claim",
                json={"pairing_token": pairing_token},
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise BackendUnavailable(f"Backend unreachable: {type(exc).__name__}") from exc

        if response.status_code in (400, 401, 403, 404, 409, 410):
            raise SessionRevoked(_detail(response))
        if response.status_code != 200:
            raise BackendUnavailable(f"Backend error {response.status_code}")

        data = response.json()["data"]
        # Only now replace the previous token: a failed claim leaves an
        # already-running session untouched.
        self._agent_token = data["agent_token"]
        self.session_id = session_id
        self.student_label = data.get("student_name")
        self.heartbeat_interval = float(data.get("heartbeat_interval", 1.0))
        return data

    def heartbeat(self, payload):
        """Send one heartbeat. Returns the backend's session view."""
        if not self.paired:
            raise SessionRevoked("Not paired")

        try:
            response = self.http.post(
                f"{self.base_url}/monitoring/heartbeat",
                json=payload,
                headers={"Authorization": f"Bearer {self._agent_token}"},
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise BackendUnavailable(f"Backend unreachable: {type(exc).__name__}") from exc

        if response.status_code in (401, 403, 409, 410):
            self.forget()
            raise SessionRevoked(_detail(response))
        if response.status_code != 200:
            raise BackendUnavailable(f"Backend error {response.status_code}")

        return response.json().get("data", {})

    def end(self, reason="agent_stopped"):
        """Tell the backend the agent stopped. Best effort."""
        if not self.paired:
            return
        try:
            self.http.post(
                f"{self.base_url}/monitoring/agent/end",
                json={"reason": reason},
                headers={"Authorization": f"Bearer {self._agent_token}"},
                timeout=self.timeout,
            )
        except requests.RequestException:
            pass
        finally:
            self.forget()

    def forget(self):
        self._agent_token = None


def _detail(response):
    try:
        detail = response.json().get("detail")
        if isinstance(detail, str):
            return detail
    except ValueError:
        pass
    return f"HTTP {response.status_code}"
