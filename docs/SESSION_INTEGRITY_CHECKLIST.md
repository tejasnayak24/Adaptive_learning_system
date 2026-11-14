# Session integrity: manual acceptance checklist

These checks need a person, real Chrome and a real webcam. Automated tests
covered the rules, but they could not hide a real tab or show real faces
(see [SESSION_INTEGRITY.md §5](SESSION_INTEGRITY.md#5-tests)).

## Before you start

1. Back up the live database:
   ```powershell
   & "C:\Program Files\PostgreSQL\18\bin\pg_dump.exe" -U postgres -Fc -f backups\before_0008.dump adaptive_learning_db1
   ```
2. Apply the migrations:
   ```powershell
   cd backend
   python -m alembic upgrade head
   ```
   Check that `python -m alembic current` shows `0008_session_events`.
3. Start everything with `.\start-all.ps1`. Sign in as a test student (not a
   real one).
4. The first lesson asks for consent again (version 2). Check the new
   wording, then accept.

Record each result as **Pass / Fail / Note**.

## A. Tab switching in real Chrome (protected quiz)

Use a different quiz for each group. A terminated or closed quiz needs a
5-minute wait before a new attempt.

| # | Step | Expected | Result |
|---|---|---|---|
| A1 | Open a quiz and wait for the camera to verify | "Protected quiz" rules banner above the questions | |
| A2 | Answer a question, press Ctrl+T, wait about 5 s, go back to the quiz tab | "You left the quiz" dialog; quiz continues; the amber warning banner stays | |
| A3 | Press F5 and **cancel** the browser's "Reload site?" prompt | Nothing changes: still one warning, quiz continues | |
| A4 | Switch to another tab again for 1 s | "This quiz has ended": hidden or reloaded a second time; answers kept; not graded; retake countdown | |
| A4b | New quiz: answer a question, press F5 and **accept** the prompt | Same attempt, same answer selected, and the "You left the quiz" warning (the reload is the first incident) | |
| A4c | Same quiz: press F5 and accept again | The quiz ends at once ("hidden or reloaded a second time"); the cooldown screen states the reason | |
| A5 | New quiz: switch tabs and stay away about 15 s | Ended: hidden for more than 10 seconds | |
| A6 | New quiz: minimise Chrome for about 3 s, restore | Warning (first incident) | |
| A7 | Same quiz: click the "Aegis Camera Agent" preview window, then click back in Chrome | **No** warning or termination (focus change only) | |
| A8 | Same quiz: press Alt+Tab to another app while Chrome stays visible (e.g. side by side), wait 15 s, come back | **No** termination (the page was not hidden) | |
| A9 | Same quiz: click "Abort to Lesson", then "Stay on the quiz" | Quiz continues | |
| A10 | Click "Abort to Lesson", then "Leave quiz" | Lesson page; reopening the quiz shows the 5-minute wait | |
| A11 | New quiz: press the browser's Back button | "Leave this quiz?" dialog appears first | |
| A12 | Lock the screen (Win+L) for about 20 s during a quiz, unlock | Ended: hidden for more than 10 seconds | |

## B. Network interruption and recovery

| # | Step | Expected | Result |
|---|---|---|---|
| B1 | During a quiz, stop the backend window ("Aegis backend"), answer a question | "Answers saved" changes to an offline note; no termination | |
| B2 | With the backend still stopped, switch tabs for about 3 s and come back | Quiz locks: "Reconnecting…" | |
| B3 | Start the backend again in a new PowerShell window from the project root (README, "Starting services by hand": `$env:PYTHONPATH = "$PWD\backend"; python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000`) | Within a few seconds: warning dialog (one strike), quiz continues, answers intact. The camera gate may also pause briefly while the backend is down; that is expected | |
| B4 | Turn Wi-Fi off and on during a quiz (no tab switch) | No warning, no termination | |

## C. Multiple-face detection with the real webcam

Have a second person (a family member or classmate) help. The warning is
an information banner only.

| # | Condition | Expected | Result |
|---|---|---|---|
| C1 | Only you, good light, normal sitting position, 2 minutes | No warning | |
| C2 | Second person sits next to you, both facing the camera, 10 s | Banner after about 3 s; clears about 2 s after they leave | |
| C3 | Second person walks behind you without stopping | Usually no warning (brief) | |
| C4 | Second person in profile or half out of frame | May not be detected: note what happened | |
| C5 | Dim room (lamp only) | Note whether C2 still works; lighting warnings may appear | |
| C6 | Laptop on your lap / camera tilted / sitting further back (about 1.5 m) | Note detection; the short-range model is for faces within about 2 m | |
| C7 | A photo or poster with a face in view behind you | Small background faces should be ignored | |
| C8 | During a protected quiz, repeat C2 | Banner appears; the quiz is **not** ended or locked | |
| C9 | Open **Session Activity** | Episodes listed with times, duration and peak count; tab incidents from part A listed with times away; no score anywhere | |

## D. Existing features still work

| # | Check | Result |
|---|---|---|
| D1 | A normal quiz without switching is graded; the AI Coach recommendation appears | |
| D2 | Dashboard and Progress show only graded quizzes (terminated/closed ones are not counted) | |
| D3 | Yawning, looking away and the drowsiness voice alert still work as in [DEMO.md](DEMO.md) Part B | |
| D4 | Agent CPU: open Task Manager during a lesson; the agent's CPU use is similar to before | |
