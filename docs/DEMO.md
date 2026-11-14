# Aegis demonstration guide

A complete demonstration takes about 15 minutes. Part A is the main
learning loop. Part B shows drowsiness detection and the voice alerts on
their own.

## Before the demonstration (10 minutes earlier)

| ✓ | Check |
|---|---|
| ☐ | Laptop on mains power; webcam not covered; room well lit (face detection needs light) |
| ☐ | Close Teams, Zoom, the Windows Camera app and anything else that may hold the webcam |
| ☐ | Settings → Privacy & security → Camera → "Let desktop apps access your camera" is **On** |
| ☐ | Speakers on, volume about 50 % (for the voice alerts in Part B) |
| ☐ | PostgreSQL service running |
| ☐ | `powershell -ExecutionPolicy Bypass -File .\start-all.ps1 -CheckOnly` reports **All checks passed** |
| ☐ | Run `.\start-all.ps1`: three windows open (backend, camera agent, frontend) and the browser opens http://localhost:5173 |
| ☐ | Have a fresh e-mail address ready for a new demo student (for example `demo.student.<date>@example.com`) |
| ☐ | Optional: a second browser tab with http://localhost:8000/docs to show the API |

If something fails, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

## Part A — main learning loop

| # | Do | Point out |
|---|---|---|
| A1 | **Register.** Name, the demo e-mail, age **13**, Grade **8**, a password of 8 or more characters. You land on *Sign in* with "Registration successful" | Grade decides the curriculum. Passwords are stored as bcrypt hashes |
| A2 | **Sign in.** The Dashboard shows *Grade 8*, 0 of 24 lessons, *Average score —* and "No advice yet" | A new student sees honest empty values, not sample numbers |
| A3 | **My Learning.** Click through Mathematics, Science, Social Science and English | Grade 8 curriculum: subject → unit → topic → lesson, each with Easy, Medium and Hard quizzes |
| A4 | **Choose a lesson.** Mathematics → *Laws of Exponents* → **Start** | The camera consent screen appears; it is mandatory |
| A5 | **Consent.** Tick the three boxes (under 18: guardian and school too) → *Give consent and continue* | The webcam light turns on only now. The checklist runs: agent → webcam → face → live data |
| A6 | **Study the lesson** once it unlocks. Scroll through objectives, explanation, worked examples, diagram, real-world use and practice | Content is generated for each grade and subject |
| A7 | **Camera pause (optional).** Lean out of view for 5 s, then come back | Learning pauses and resumes automatically. The camera cannot be skipped |
| A8 | **Take the quiz.** *Take quiz* (Easy). Use **💡 Need a hint?** on one question, answer the rest, **Submit quiz** | Answers were never sent to the browser before submitting |
| A9 | **Results.** Score, then *Answer review* with the correct answer and a "Why:" explanation for each question. Then the camera summary (average attention, yawning, gaze, drowsiness) | The server graded the quiz and took the camera values from the agent's measurements |
| A10 | **Reinforcement Learning Policy Decision** panel | The action, the reason in plain words, and "Decided by: Learned Q-table". Decision strength is not a probability |
| A11 | **Follow the recommendation** (the button under it). It may be a lesson section, an easier or harder quiz, a retry with hints, a timed challenge or a short break | All 11 actions lead to a real next step, always within the student's grade and subject |
| A12 | **Second quiz.** Complete the quiz the recommendation leads to, or the lesson's quiz | This attempt becomes the recorded *outcome* of the first recommendation, and its reward is stored |
| A13 | **AI Coach.** Shows the new advice, "Based on your quiz", and *Earlier advice and what happened next* with the score change | Advice comes from the Q-learning service. The page has no recommendation rules of its own |
| A14 | **Progress Log.** Tiles, score trend with the pass line (filter by subject or date), subject and topic performance, camera section, weekly activity, milestones and the attempt log | Untried topics are never "weak". Missing camera data is never counted as low attention |
| A15 | **Dashboard again.** Updated counts, latest activity, the coach card and recent activity | All figures come from this student's saved records |

## Part B — drowsiness detection and voice alerts

Do this in a lesson or quiz with monitoring verified. The agent window
("Aegis Camera Agent") shows the live measurements.

| # | Do | Expected |
|---|---|---|
| B1 | Look at the screen normally | Head *Forward*, gaze *Center*, attention high (green) |
| B2 | **Yawn** (mouth wide open for about 1 s) | *Yawning: Yes* and a spoken reminder ("You seem a little tired…") |
| B3 | **Look away** (turn your head or eyes away for 3+ s) | *Looking away: Yes* after about 2 s |
| B4 | **Close your eyes for about 3 s** | Beep and spoken **"Hey, wake up!"**; red pulsing border; *possible drowsiness* |
| B5 | Keep your eyes closed for about 20 s | The alert repeats about every 5 s; after 3 alerts a firmer message with a double beep |
| B6 | Open your eyes and finish the quiz | The results show *Possible drowsiness: Observed* (plus yawning or looking away if they happened during this quiz). The coach usually suggests a **Focus-recovery break** with a countdown |

Say during Part B:
- These are estimates to support learning, not a medical or sleep
  assessment.
- The agent never stores or sends images or video, only numbers and yes/no
  signals.

## After the demonstration

- Run `.\stop-all.ps1`: it stops the three services and closes their
  windows.
- The demo student and its attempts stay in the database. Nothing is
  deleted automatically. Remove test accounts only if your supervisor
  asks; see [TROUBLESHOOTING.md](TROUBLESHOOTING.md#test-accounts).

## If something goes wrong during the demo

| Symptom | Quick fix |
|---|---|
| "Start the Aegis camera agent" | The agent window was closed. Run `facial_analysis\venv\Scripts\python.exe facial_analysis\main.py` |
| "Webcam unavailable" | Close other camera apps; check Windows camera privacy; press **Retry** |
| Checklist stuck on *Face detected* | More light; face the camera; remove strong backlight |
| "Camera data is not reaching Aegis" | The backend window was closed or crashed. Restart it (`.\stop-all.ps1`, then `.\start-all.ps1`) |
| No recommendation after a quiz | The quiz had no valid camera reading (the page says so). Take another quiz with the face visible |
