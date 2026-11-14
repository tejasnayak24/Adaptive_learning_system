# Session integrity

Three features help keep a monitored learning session honest:

- **Tab-switch protection:** a two-strike rule during quizzes.
- **Multiple-face detection:** in the camera agent.
- **Session activity report:** shows the student what was recorded.

None of them produces a score, a probability or a verdict. A hidden tab or a
second face is not proof of misconduct, and Aegis never says it is.

| Feature | How reliable | What it cannot see |
|---|---|---|
| Tab-switch protection | **Reliable** for "the quiz page was hidden" (browser Page Visibility API) | Which tab, site or app was used. A second device. A student who disables the page's scripts. |
| Multiple-face detection | **Approximate.** Good for two clear, frontal faces at a similar distance | Faces in profile, partly out of frame, far away, behind the student or in poor light. People out of the camera's view. |
| Activity report | As reliable as its inputs; every value says how it was measured | — |

## 1. Tab-switch protection (two-strike rule)

Protected attempts are all graded quiz modes: standard, practice, hints and
challenge. There is no ungraded practice mode yet. The attempt flag
`protected` (`PROTECTED_MODES` in `quiz_attempt_service.py`) makes room for one.

| Situation | Result |
|---|---|
| Quiz page hidden the first time | A 10-second grace period starts, measured by the **server** from when the report arrives |
| Back within 10 s | Quiz continues. A warning dialog says another switch will end the quiz, and a warning banner stays visible |
| Not back within 10 s (reliable evidence) | **Terminated** (`grace_expired`) |
| Hidden again after the warning | **Terminated immediately** (`second_tab_switch`) |
| Terminated | Answers kept and frozen. **Not graded**: no `progress` row, so it never counts towards completion, averages, analytics, recommendations or Q-learning rewards. A new attempt is possible after a **5-minute cooldown** |
| Window blur/focus (e.g. the camera agent's window, an OS dialog) | Recorded for diagnostics only. **Never a strike** |
| Confirmed reload (the student accepts the browser's "Reload site?" prompt) | **Counts as a tab-switch incident.** First incident: strike 1 and the warning, once the reloaded page is back within 10 s. After strike 1: **terminated immediately** (`second_tab_switch`). The attempt, its answers and its strike history are kept across the reload |
| Cancelled reload (the student dismisses the prompt and stays) | Not an incident: nothing is reported |
| Leaving for another Aegis page (link or Back button) | Asks first. Confirming makes the attempt **abandoned** (answers kept, not graded, not a violation, 5-minute cooldown) |
| Network interruption | **Never a violation.** If nothing can be verified, the attempt is locked as `unverified` until a report resolves it |

### How it is enforced (server-authoritative)

```text
browser (reports only)                 server (decides)
--------------------------------       -----------------------------------------------
page hidden -> "hidden" (keepalive)    away_started_at = receive time, status "away"
still hidden -> "hidden_tick" / 2 s    hidden_ms > 10 000 -> terminated (grace_expired)
visible -> "visible" + hidden_ms       hidden_ms > 10 000                  -> terminated
                                       arrived <= 10 + 2 s after the hide  -> strike 1
                                       arrived later, network delay shown  -> strike 1
                                       arrived later, sent promptly        -> terminated
nothing at all after 10 + 2 s          status "unverified" (locked, not a violation)
```

- **Throttled timers do not matter.**
  - The `hidden` report is sent the moment the page is hidden, with `fetch(..., {keepalive: true})`, before Chrome throttles anything.
  - The deadline is on the server and is evaluated lazily on the next request. A frozen tab cannot extend it.
- **Measured absence.** `hidden_ms` is the larger of the monotonic-clock and wall-clock gaps, so a sleeping laptop (which can pause `performance.now()`) or a clock change cannot shorten it.
- **The 2-second allowance never adds grace.** The 10 s limit is applied to the measured absence. The 2 s only covers the time the "visible" report takes to reach the server.
- **Network vs leaving.**
  - Undeliverable reports are queued and retried, and carry `delivery_failures` and `queued_ms`. A return measured at 10 s or less but delayed by the network is a warning, never a termination.
  - With no report at all, the attempt is `unverified`. A later report resolves it. If it can never be measured (e.g. the tab was closed and reopened), the attempt is **abandoned**, not terminated.
  - No contact for 30 minutes also abandons it.
- **Reload.**
  - `beforeunload` shows the browser's prompt. If the student cancels, the page never unloads and nothing is sent.
  - A confirmed reload unloads the page: `pagehide` is sent with `keepalive`. After strike 1 the server terminates at once. Otherwise the incident is open and the 10-second rule applies.
  - The reloaded page reports the measured gap (from `sessionStorage`) with `reload: true`. It is judged exactly like any other return (within 10 s: strike 1; network-delayed: strike 1; longer: terminated). It is labelled "page reloaded" in the report.
  - The reloaded page resumes the same attempt with its saved answers. If the attempt has already ended, it shows the reason and the cooldown.
- **Duplicates.** Every event has `(page_id, seq)`. Replays are ignored.
- **Concurrency.** A partial unique index allows one open attempt per student and quiz. Two simultaneous starts resume the same attempt.
- **Lock.** After a return, the questions stay hidden behind "Checking your quiz…" (or "Reconnecting…") until the server answers.

Code:
- **Backend:** `app/services/quiz_attempt_service.py`, `app/models/quiz_attempt.py`, `app/routers/quiz.py`.
- **Frontend:** `src/services/quizIntegrity.js` (pure, unit-tested), `src/hooks/useQuizIntegrity.js`, `src/components/QuizIntegrity.jsx`, `src/pages/QuizView.jsx`.

### Trust limits

- The reports come from the student's own browser. They are accurate unless the page is tampered with; a student can block them with developer tools.
- Gaps show as "not recorded" or `unverified`, never as zero.
- The rule cannot see a second device or a printed sheet.

## 2. Multiple-face detection

The camera agent (`facial_analysis/face_counter.py`) runs **MediaPipe Face
Detection** (BlazeFace, short-range model, already part of the installed
`mediapipe`).
- **How often:** on a 320-px copy of a frame, about twice a second.
- **Where:** in its own thread, separate from Face Mesh.
- **Unchanged:** the attention, eye, gaze, head-pose, yawning and drowsiness measurements.

| Rule | Value (`config.py`) |
|---|---|
| A face counts if its detection score is at least | `MULTI_FACE_MIN_CONFIDENCE = 0.6` |
| …and it is at least this fraction of the largest face's width (ignores posters, TVs, people far behind) | `MULTI_FACE_MIN_RELATIVE_SIZE = 0.4` |
| Warning starts after 2+ faces in | 5 of the last 6 samples (about 3 s) |
| Warning clears after | 4 samples below 2 (about 2 s) |
| Switch off | `MULTI_FACE_DETECTION_ENABLED = False` |

What happens with the result:
- **Heartbeat:** only `face_count` and `multiple_faces` are sent. If the model cannot load, both are `null` (not measured).
- **Records:** the backend keeps each **episode** in `session_events`: server start and end times, peak face count, and how it ended (`cleared`, `not_measured`, `heartbeats_stopped`, `session_ended`).
- **Student's view:** one informational banner while the signal lasts. No popup, no lock, and never a quiz termination.

**Measured overhead** (this laptop: AMD Ryzen 7 250, 16 logical cores; noise
frames at 640×480, because BlazeFace's cost does not depend on frame content):

| Measure | Value |
|---|---|
| One face count | 2.5 ms median (95th percentile 3.2 ms) |
| CPU at 2 counts per second, including the frame copies | about 4% of one core (0.24% of the whole CPU) |
| Extra memory | about 9 MB |
| Camera loop rate | 30 fps with or without it |

Normal situations it will report (and that are fine): a parent or guardian
helping, a sibling, a teacher at school. The report says "more than one face
visible" and nothing more.

## 3. Session activity report

`GET /integrity/report` and the **Session Activity** page (`/activity`) show
the signed-in student's own records only:

- **Tab-switch incidents:**
  - time;
  - time away, as measured by the browser, or "not measured";
  - outcome;
  - whether the return was unverified;
  - confirmed reloads are counted as incidents and labelled "page reloaded".
- **Attempt outcome:** graded, ended (terminated) or closed (abandoned), with the reason.
- **Unverified periods** and **reports delayed by the network**.
- **Multiple-face episodes:** times, duration, peak count.
- **Window focus changes,** marked as diagnostic.
- **Measurement notes.**

There is no teacher view in this phase; teacher-student relationships do not
exist yet.

## 4. Consent and privacy

- **Consent version `2026-11-v2`.** Students who agreed to v1 are asked again. The consent text says:
  - tab visibility is monitored during protected quizzes (never which tab, site or app);
  - the camera may notice more than one face (how many and when, never who);
  - only event metadata and numbers are stored;
  - webcam images and video are never stored or transmitted.
- **Minors.** The guardian and school confirmations now name both checks explicitly.
- **Stored data.**
  - `quiz_attempts` holds answers, status and server timestamps.
  - `quiz_attempt_events` holds the kind of each page event, browser-measured times and the server outcome.
  - `session_events` holds face-episode times and peak counts.
  - No images, crops, boxes or landmarks are stored.
- **Access.** Every endpoint is the student's own (404 for another student's attempt). The agent token can only send heartbeats.

## 5. Tests

| Suite | What it covers |
|---|---|
| `backend/tests/test_quiz_attempts.py` (31) | Every timing rule with a controlled clock (9.9 s / 10.1 s, 2 s allowance, hidden ticks, second switch, lost reports, unverified, network delay, confirmed reload as first and second incident, cancelled reload, slow and network-delayed reload, duplicates, cooldown, abandonment, privacy, ungraded results, concurrent starts) |
| `backend/tests/test_multiple_faces.py` (9) | Episodes open/close, peak count, stale/unmeasured data, heartbeat gaps, session end, no effect on grading |
| `backend/tests/test_integrity_report.py` (6) | Report contents, privacy, no score wording, consent v2 re-consent |
| `facial_analysis/tests/test_face_counter.py` (14) | Counting rules, sustained signal, worker thread, real MediaPipe model loads |
| `frontend/tests/quizIntegrity.test.mjs` (14) | Tracker: keepalive hide, ticks, measured absence, offline retry, confirmed reload reported by both pages, cancelled reload sends nothing, blur ignored, ordering |
| Browser (headless Chrome, isolated database copy) | Tab switching 27/27, multiple faces 11/11, report and consent 13/13, Phase 7 journey 38/38 |

**Limits of the automated tests:**
- Headless Chrome never hides a background tab. A windowed Chrome launched from the test tools also kept every tab "visible" on this machine. In the browser tests the page-visibility change was therefore **simulated**, and everything else was real.
- The real-Chrome and real-webcam checks are in
  [SESSION_INTEGRITY_CHECKLIST.md](SESSION_INTEGRITY_CHECKLIST.md).

## 6. Known limitations

- The tab-switch rule relies on the browser. A determined student can block it, and a second device is invisible to it.
- Some assistive tools (on-screen keyboards, screen readers, the Snipping Tool) can hide or cover the page. There is no teacher reinstatement yet; a retake after the cooldown is the remedy.
- Multiple-face detection is approximate: see the table at the top. It needs reasonable lighting, and BlazeFace's short-range model is designed for faces within about 2 m.
- Episode times are server receive times. The agent requires about 3 s of detection before reporting, so an episode really began about 3 s earlier.
- Phone detection, a teacher dashboard and teacher-student relationships are not part of this phase.
