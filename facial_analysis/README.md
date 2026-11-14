# Aegis facial analysis — local camera agent

The camera agent runs on the student's own computer. It analyses the webcam
with OpenCV + MediaPipe Face Mesh and sends **only numbers and yes/no
signals** (attention 0–1, face present, yawning, sustained looking away,
possible drowsiness) to the Aegis backend. No images or video are stored or
transmitted.

## Run

```powershell
cd C:\Users\tejas\Adaptive_learning_system\facial_analysis
.\venv\Scripts\Activate.ps1
python main.py
```

The webcam stays **off** until you start a lesson on the Aegis website. The
website pairs with the agent automatically through `http://127.0.0.1:8765`.
An "Aegis Camera Agent" window shows what the camera sees, the attention
score and alerts (`H` = compact view, `Q` = stop monitoring).

Other modes:

| Command | Purpose |
|---|---|
| `python main.py --no-window` | Agent without the on-screen window |
| `python main.py --preview` | Local preview of all detectors, no backend |
| `python tests\manual\check_face_detector.py` | Manual webcam checks (see `tests/manual`) |

First-time setup:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Pinned, known-working versions: `mediapipe==0.10.21`, `numpy==1.26.4`,
`opencv-contrib-python==4.11.0.86`. Voice alerts use `pyttsx3` (Windows SAPI5).

## How pairing works

1. The student logs in and gives camera-monitoring consent (minors also confirm
   parent/guardian and school authorisation).
2. Opening a lesson creates a monitoring session. The backend returns a random
   **single-use pairing token** (valid 2 minutes; only its hash is stored).
3. The browser POSTs it to the agent on `127.0.0.1:8765`. The agent exchanges it
   at the backend for an **agent token** bound to that student and session.
4. The agent opens the webcam and sends one timestamped heartbeat per second.
   The backend derives the student from the token — the agent never sends a
   student id.
5. The lesson unlocks only when the **backend** reports *verified* (fresh
   heartbeat, camera working, face detected and stable).
6. If anything fails the lesson and quiz timer pause; answers and position are
   kept. Reconnecting issues a new pairing token for the same session — no new
   login needed.
7. Ending the lesson (or closing the tab for 60 s) ends the session; the agent's
   next heartbeat is rejected and it releases the webcam.

## Security of the local agent

* Listens on `127.0.0.1` only; refuses any other bind address.
* `Host` must be `127.0.0.1:8765` or `localhost:8765` (blocks DNS rebinding).
* Only the Aegis frontend origins may call it (CORS allow-list). POSTs need an
  allowed `Origin`, the `X-Aegis-Client: aegis-web` header and a JSON body, so
  other websites cannot forge requests (CSRF).
* Tokens travel only in JSON bodies / `Authorization` headers — never in URLs —
  are kept in memory only and are never printed or logged.

## Status states

`GET http://127.0.0.1:8765/status` → `state`:

| Agent state | Meaning |
|---|---|
| `idle` | Running, no session, camera off |
| `starting` | Session claimed, opening the camera |
| `camera_unavailable` | Camera blocked / missing / in use / disconnected (`camera.error_code`, `camera.message`) |
| `running` | Camera active (see `face`, `backend.connected`) |

The website combines this with the backend's view into: agent not running →
camera unavailable → no face → backend disconnected → verified.

## Camera blocked on Windows

If the agent reports `blocked_by_privacy_settings`: open **Settings → Privacy &
security → Camera**, turn on **Camera access** and **Let desktop apps access
your camera**, then press *Retry* on the website. On school-managed laptops
these switches may be controlled by IT. If the camera is "unavailable", close
other apps that use it (Teams, Zoom, Camera app, browser tabs).

## Possible drowsiness and voice alerts

Ported from PR #10. Eyes closed for 2 s → beep and spoken "Hey, wake up!"
(repeats every 5 s, firmer after 3); no face for 10 s → "Are you still there?";
yawns → gentle spoken reminder (15 s gap) and a break suggestion after 3 yawns
in 5 minutes. Speech runs on its own thread with a small queue, so it never
blocks the camera loop. **This is an attention aid, not a medical sleep
assessment.**

## Multiple-face detection

`face_counter.py` counts faces with MediaPipe **Face Detection** (BlazeFace,
already installed).
- **When and where:** on a 320-px copy of a frame, about twice a second, in its own thread.
- **Unchanged:** Face Mesh and all attention, gaze, yawning and drowsiness measurements.

The rules for counting and warning:
- **What counts as a face:** a score of at least 0.6, and at least 40% as wide as the largest face (posters and TVs are ignored).
- **When the warning starts:** "multiple faces" is raised after 2+ faces in 5 of 6 samples (about 3 s).
- **When it clears:** about 2 s after the extra face leaves.

Only `face_count` and `multiple_faces` go in the heartbeat; frames are never
stored or sent. Overhead on the development laptop is about 2.5 ms per count,
about 4% of one core, +9 MB, and the camera loop stays at 30 fps. Turn it off with
`MULTI_FACE_DETECTION_ENABLED = False` in `config.py`. See
[docs/SESSION_INTEGRITY.md](../docs/SESSION_INTEGRITY.md).

## Tests

```powershell
pip install -r requirements-dev.txt
python -m pytest
```

Synthetic-landmark, protocol and lifecycle tests run without a webcam. The
cross-process test also starts the real backend:

```powershell
$env:AEGIS_BACKEND_PYTHON = "C:\Users\tejas\AppData\Local\Programs\Python\Python310\python.exe"
python -m pytest tests\test_integration_backend.py
```
