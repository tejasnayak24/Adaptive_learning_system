# Troubleshooting and known limitations

## Troubleshooting

### Start-up

| Problem | Fix |
|---|---|
| `start-all.ps1` "cannot be loaded because running scripts is disabled" | Run it as `powershell -ExecutionPolicy Bypass -File .\start-all.ps1` |
| `[FAIL] backend\.env exists` | Copy `backend\.env.example` to `backend\.env`, then set `DATABASE_URL` and a new `SECRET_KEY` |
| Backend window: `SECRET_KEY is a placeholder or too short` | Generate a key: `python -c "import secrets; print(secrets.token_urlsafe(48))"` and put it in `backend\.env` |
| `[FAIL] PostgreSQL reachable` | Start the PostgreSQL service (Services → postgresql-x64-18). Check the user, password, port and database name in `DATABASE_URL`. Create the database if needed (README §2) |
| `[FAIL] Database schema up to date` | Back up, then `cd backend; python -m alembic upgrade head` (README §2) |
| `[FAIL] Port 8000/5173/8765 free` | An old copy is still running. Run `.\stop-all.ps1`. If another program uses the port, close it |
| Frontend window: `Port 5173 is in use` | Same as above. The camera agent only accepts the website from port 5173, so the port cannot change |
| Lessons show no content / empty curriculum | Import the curriculum: `python backend\scripts\import_curriculum.py` (README §2). It is safe to re-run |
| Want to open the site from another device on the LAN | Not needed for normal use, because the camera agent only pairs on the same computer. To do it anyway: `$env:AEGIS_DEV_HOST = "0.0.0.0"` before `npm run dev` |

### Camera

| Problem | Fix |
|---|---|
| "Start the Aegis camera agent" | Start it: `cd facial_analysis; .\venv\Scripts\python.exe main.py` (or rerun `start-all.ps1`) |
| "Webcam unavailable" | Close Teams, Zoom or the Camera app. Windows Settings → Privacy & security → Camera → allow desktop apps. Press **Retry** |
| Stuck on "Checking face detection…" | Improve lighting, face the camera, avoid a bright window behind you |
| "Camera data is not reaching Aegis" | The backend stopped or is unreachable from the agent. Restart the backend; the agent reconnects automatically |
| Quiz results say camera data was unavailable and no recommendation appeared | No valid live reading arrived during that quiz. This is reported honestly rather than guessed. Keep your face in view during the next quiz |
| No voice alerts | Check speaker volume. Alerts come from the agent (pyttsx3), not the browser |

### Tests

| Problem | Fix |
|---|---|
| `test_integration_backend.py` is skipped | Set `$env:AEGIS_BACKEND_PYTHON = (Get-Command python).Source` before running the facial-analysis tests |
| Backend tests touch my database? | They never do; they use a throwaway SQLite database |

## Test accounts

Testing created student accounts in the live database. They were **not**
deleted automatically:
- `phase1.e2e.*@example.com` (id 12, Grade 9);
- `phase6.e2e.*@example.com` (id 14, Grade 7).

Later browser and regression runs used an isolated copy of the database
(`aegis_phase7`), not the live one. To list test accounts:

```sql
SELECT id, email, grade, created_at FROM students WHERE email LIKE '%e2e%@example.com' ORDER BY id;
```

Remove them only if you decide to. Back up first (`pg_dump`). Deleting a
student also deletes their attempts, recommendations and monitoring records.

## Known limitations

### Security (accepted for this local, single-computer deployment)

- **JWT in `localStorage`.** The login token is kept in `localStorage`, so
  any script injected into the page could read it.
  - **Mitigations now:** React escapes all rendered content and no third-party
    scripts are loaded. Tokens expire after 30 minutes, are never put in
    URLs, and are not logged.
  - **Proper fix:** an HttpOnly, SameSite cookie with CSRF protection. That
    changes authentication and was deliberately not attempted in the final
    phase.
- **No login rate limiting or account lockout.** Passwords are bcrypt-hashed,
  and new passwords need at least 8 characters.
- **No refresh tokens.** Students sign in again after 30 minutes. The
  answers of a quiz in progress are kept in that browser tab
  (`sessionStorage`, no tokens) and restored.
- **Plain HTTP.** Everything runs on `localhost`. A server deployment would
  need HTTPS, a production web server and secret management.
- **Teacher/admin roles are set with `backend/scripts/set_role.py`.** There
  is no admin UI.

### Camera and analytics

- **Per-quiz camera data.** The database stores one camera summary per quiz
  attempt (average attention; whether yawning, looking away or drowsiness
  was seen). Continuous recordings are never stored, so there are no
  minute-by-minute statistics.
- **Detection is approximate.** It is based on face landmarks, not a medical
  or sleep assessment, and depends on light, camera angle and glasses.
- **Real-webcam acceptance was reported as a whole.** It passed on
  2026-11-12 on the team lead's laptop but was not ticked line by line (see
  [WEBCAM_ACCEPTANCE_CHECKLIST.md](WEBCAM_ACCEPTANCE_CHECKLIST.md)).
  Automated tests use a synthetic camera.
- **Streaks use UTC days.** For students in India (UTC+5:30), a quiz taken
  just after midnight local time counts on the previous day.

### Reinforcement learning

- **Offline training only.** The Q-table was trained offline on simulated
  students and is read-only at runtime. Real outcomes are recorded
  (`reward_history`) for analysis and future retraining, but the policy does
  not learn online.
- **Decision strength is not a probability.** It describes how clearly the
  learned values favour the chosen action.
- **"Followed" can't always be checked.** It is inferred from the next quiz
  and is unknown for actions like a break or reading a real-world example.

### Curriculum and content

- **Not teacher-reviewed.** All curriculum text and questions were written
  for this project. They are checked by a validator and were spot-checked by
  hand, but have not been reviewed by a teacher.
- **Uneven original answer key.** The 75 original Science questions keep
  their original answer key, which is heavily "A". It is kept because
  stored attempts refer to those letters.
- **Diagrams are generated.** They are charts, tables and flows, not drawn
  illustrations.
- **Challenge mode is not enforced.** It shows a time target but does not
  force submission.

### Other

- **Tested on Windows only.** Tested on Windows 11 with Python 3.10,
  Node.js 24 and PostgreSQL 18. The start/stop scripts are PowerShell.
  The camera agent uses DirectShow and the Windows camera-privacy checks on
  Windows; other systems would need their own testing.
- **Lint warning exception.** `npm run lint` is clean with one documented
  exception in `QuizView.jsx`, plus the React-Compiler advisory rules turned
  off (see `frontend/eslint.config.js`).
