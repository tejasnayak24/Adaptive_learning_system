# Phase 3 — real-webcam acceptance checklist

Run on the Windows laptop with a real webcam. Automated tests cover the
protocol with synthetic landmarks; **these checks are the only proof the real
camera works.** Mark each line ✅ / ❌ and note anything odd.

## Setup

1. Backend: `uvicorn backend.app.main:app --port 8000` (from the repo root,
   `$env:PYTHONPATH = "$PWD\backend"`).
2. Frontend: `npm run dev` in `frontend/`, open http://localhost:5173.
3. Camera agent: in `facial_analysis/`, `.\venv\Scripts\Activate.ps1`, then
   `python main.py`. Confirm it prints *"ready on http://127.0.0.1:8765"* and the
   webcam light is **off**.
4. Log in with a student account.

## A. Consent and pairing

| # | Step | Expected |
|---|---|---|
| A1 | Open any lesson | Consent screen. Minor account shows guardian + school checkboxes; button disabled until all ticked |
| A2 | Give consent | Checklist appears; webcam light turns **on**; "Aegis Camera Agent" window opens |
| A3 | Sit normally facing the camera | Within ~3 s all four checklist items turn ✓ and the lesson content becomes readable |
| A4 | Dashboard/Progress pages | Usable without the camera |

## B. Detection features

| # | Step | Expected |
|---|---|---|
| B1 | Look straight at the screen | Agent window: Head *Forward*, Gaze *Center*, attention high (green) |
| B2 | Turn head left, then right | Head direction changes; brief turns don't flag *looking away* |
| B3 | Look away (head or eyes) for 3+ s | *Looking away* shows Yes after ~2 s |
| B4 | Yawn (mouth wide ~1 s) | *Yawning* Yes; spoken reminder ("You seem a little tired…") |
| B5 | Yawn 3 times within 5 min | Break suggestion is spoken |
| B6 | Blink normally | Blink count rises; **no** wake-up alert |
| B7 | Close eyes for 3 s | Beep + spoken "Hey, wake up!"; red pulsing border; *possible drowsiness* |
| B8 | Keep eyes closed 20 s | Alert repeats ~every 5 s; after 3 alerts a firmer message with double beep |
| B9 | Talk/move while an alert is speaking | Video keeps updating smoothly (speech does not freeze the camera) |
| B10 | Dim the room lights strongly | Website shows "The room looks dark" hint |

## C. Pausing and recovery during a quiz

| # | Step | Expected |
|---|---|---|
| C1 | Start a quiz, answer 2 questions | Timer runs |
| C2 | Leave the camera view for 5 s | Quiz blurs, "Learning paused — your place and answers are saved", checklist shows *Face*; **timer stops** |
| C3 | Return | Resumes automatically; previous answers still selected; timer continues from where it stopped |
| C4 | Press `Q` in the agent window | Brief pause, then the website re-pairs automatically within ~5 s (monitoring cannot be switched off during a lesson) |
| C5 | Unplug the USB webcam (or disable it in Device Manager) | "Webcam unavailable" with instructions; plug back in → resumes automatically |
| C6 | Stop the agent (Ctrl+C) | "Start the Aegis camera agent"; run `python main.py` again → reconnects to the **same** session, quiz answers intact |
| C7 | Stop the backend for 10 s | "Camera data is not reaching Aegis"; restart backend → recovers |
| C8 | Open the Windows Camera app first, then start a lesson | "Webcam unavailable … close other apps"; close Camera app, Retry → works |
| C9 | Settings → Privacy & security → Camera → turn off "Let desktop apps access your camera" | Website shows the Windows privacy instructions; turn back on, Retry → works |
| C10 | Submit the quiz | Results show measured attention, yawning, gaze, possible drowsiness; recommendation generated |
| C11 | Refresh the browser mid-quiz | Answers and timer restored; monitoring reconnects without login |

## D. Session end

| # | Step | Expected |
|---|---|---|
| D1 | Go back to the Dashboard | Within ~5 s the webcam light turns **off**; agent window closes |
| D2 | Close the browser tab during a lesson | Within ~60 s the webcam light turns off |
| D3 | Log out | Webcam off |

## E. Privacy

| # | Check | Expected |
|---|---|---|
| E1 | `facial_analysis/` and `logs/` after testing | No image or video files created |
| E2 | Backend terminal output | No tokens or passwords printed |

Report results (✅/❌ with notes) back so failures can be fixed before Phase 4.

## Results

**2026-11-12: real-webcam acceptance run on the team lead's Windows laptop.**

Reported outcome: the facial-analysis system, the voice alerts and camera
recovery worked correctly on the real webcam, and Phase 4 was approved to
start. Results for the individual check IDs above were not reported one by
one, so no single line is marked ✅ here. The overall outcome covers the
detection (B), voice-alert (B4–B8) and recovery (C) areas as reported.

The database contains two quiz attempts from a student account during the
testing window (progress rows 62–63, 2026-11-12 09:01 UTC) with camera
attention values and a monitoring session. This is consistent with real
camera telemetry reaching the backend during the run.
