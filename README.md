# Aegis — Adaptive Learning System

Aegis is an adaptive learning platform for school students in Grades 6–10.
Students study Mathematics, Science, Social Science and English lessons,
then take Easy, Medium or Hard quizzes. During lessons and quizzes, a local
camera agent measures attention and notices yawning, looking away and
possible drowsiness; it can speak a short alert. After each quiz, the server
grades the answers and an offline-trained **Q-learning** policy recommends
one of 11 next steps. Dashboards show each student's own progress.

Quizzes are **protected**:
- **Tab switching:** leaving the quiz page gives one warning if the student is back within 10 seconds. A second time, or a longer absence, ends the quiz without grading.
- **Multiple faces:** the camera agent shows a warning while more than one face is visible.
- **Session Activity:** this page shows the student exactly what was recorded, with no score.

See [docs/SESSION_INTEGRITY.md](docs/SESSION_INTEGRITY.md).

| Service | Folder | Address |
|---|---|---|
| Backend API (FastAPI + PostgreSQL) | `backend/` | http://127.0.0.1:8000 (docs at `/docs`) |
| Frontend (React + Vite) | `frontend/` | http://localhost:5173 |
| Camera agent (OpenCV + MediaPipe) | `facial_analysis/` | http://127.0.0.1:8765 (local only) |
| Recommendation engine (Q-learning) | `rl_engine/` | loaded by the backend |

Architecture diagram: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Quick start (already set up)

```powershell
cd C:\Users\tejas\Adaptive_learning_system
powershell -ExecutionPolicy Bypass -File .\start-all.ps1
```

The script checks everything first. It looks for Python, Node, `.env`, the
virtual environment, `node_modules` and free ports, and confirms that
PostgreSQL is reachable and migrated. It then opens three windows
(backend, camera agent, frontend) and the browser.
- `-CheckOnly` runs only the checks.
- `-NoAgent` skips the camera agent.
- `-NoBrowser` doesn't open the browser.

Stop everything with `.\stop-all.ps1`.

## First-time setup on Windows

### 1. Install

| Tool | Version used | Notes |
|---|---|---|
| Python | 3.10 | Tick "Add python.exe to PATH" |
| Node.js | 20 LTS or newer (tested with 24) | Includes npm |
| PostgreSQL | 14 or newer (tested with 18) | Remember the `postgres` password |
| A webcam | — | Lessons and quizzes require camera monitoring |

### 2. Database

Create an empty database. Use pgAdmin, or run the following (the tools live
in `C:\Program Files\PostgreSQL\<version>\bin`):

```powershell
& "C:\Program Files\PostgreSQL\18\bin\createdb.exe" -U postgres adaptive_learning_db
```

Configure the backend:

```powershell
cd C:\Users\tejas\Adaptive_learning_system\backend
copy .env.example .env
python -c "import secrets; print(secrets.token_urlsafe(48))"   # paste as SECRET_KEY
notepad .env                                                   # set DATABASE_URL and SECRET_KEY
pip install -r requirements.txt
python -m alembic upgrade head
```

`.env` is git-ignored; never commit it. The backend refuses to start with the
placeholder secret. All variables are explained in
[`backend/.env.example`](backend/.env.example).

Load the curriculum: 20 grade-subject combinations, 122 lessons, Easy,
Medium and Hard quizzes. It is safe to re-run. Rows are matched by slug and
never duplicated or deleted, and the original Science lessons keep their
ids and progress.

```powershell
cd C:\Users\tejas\Adaptive_learning_system
python backend\scripts\import_curriculum.py --check   # validate only
python backend\scripts\import_curriculum.py           # import
```

> **Existing database from before Alembic?** Back up first
> (`pg_dump -Fc -f backup.dump <database>`), then
> `python -m alembic stamp 0001_baseline` and `python -m alembic upgrade head`.
> Always back up before running migrations on a database with real data.

### 3. Camera agent

```powershell
cd C:\Users\tejas\Adaptive_learning_system\facial_analysis
python -m venv venv
.\venv\Scripts\pip install -r requirements.txt
```

### 4. Frontend

```powershell
cd C:\Users\tejas\Adaptive_learning_system\frontend
npm install
```

Then run `start-all.ps1` (Quick start above).

### Optional: teacher/admin role

Teachers and admins can edit lessons and correct quiz attempts. Roles can't
be changed through the API:

```powershell
python backend\scripts\set_role.py teacher@example.com teacher
```

## Starting services by hand

Use one PowerShell window per service, all from the project root.

```powershell
# Backend (start from the project root: it imports rl_engine)
$env:PYTHONPATH = "$PWD\backend"
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000

# Camera agent (webcam stays off until a lesson starts)
cd facial_analysis; .\venv\Scripts\python.exe main.py

# Frontend (forwards /api/* to the backend)
cd frontend; npm run dev
```

Open http://localhost:5173. The first lesson asks for camera-monitoring
consent. Students under 18 also confirm parent/guardian and school
authorisation. Lessons and quizzes unlock only while monitoring is verified.

## Tests

| Suite | Command | Database |
|---|---|---|
| Backend (192) | `cd backend; pip install -r requirements-dev.txt; python -m pytest` | throwaway SQLite |
| Recommendation engine (68) | `python -m pytest rl_engine` | — |
| Camera agent (51) | `$env:AEGIS_BACKEND_PYTHON = (Get-Command python).Source; python -m pytest facial_analysis` | throwaway SQLite (the integration test starts its own backend) |
| Frontend unit tests (44) | `cd frontend; npm test` | — |
| Frontend lint / build | `npm run lint`, `npm run build` | — |
| Curriculum content | `python backend\scripts\import_curriculum.py --check` | — |
| Migrations vs models | `cd backend; python -m alembic check` | the configured database (read only) |

Results for the final release are in
[docs/PHASE7_PROGRESS.md](docs/PHASE7_PROGRESS.md) and
[docs/BROWSER_ACCEPTANCE.md](docs/BROWSER_ACCEPTANCE.md).

## Recommendation engine

The backend loads the trained Q-table `rl_engine/q_table.json`. It was
trained **offline** on simulated students and is not updated while the app
runs. To retrain it (about a minute):

```powershell
python -m rl_engine.train
```

The new table only replaces the old one if it beats the previous rule policy
and a random policy. The old table is archived in `rl_engine/archive/`.
Restart the backend afterwards. To summarise the outcomes of real
recommendations, run `python backend\scripts\rl_outcome_report.py`. The
design is described in [docs/RL_ENGINE.md](docs/RL_ENGINE.md).

## Documentation

| Document | Contents |
|---|---|
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Diagram, request flow, trust boundaries, code map |
| [TEAM_GUIDE.md](TEAM_GUIDE.md#-api-contracts) | API reference (every endpoint), team workflow |
| [docs/DEMO.md](docs/DEMO.md) | Demonstration checklist and script, including drowsiness and voice alerts |
| [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Fixes for common problems; **known limitations** |
| [docs/BROWSER_ACCEPTANCE.md](docs/BROWSER_ACCEPTANCE.md) | What was tested in the browser, and the manual checklist |
| [docs/WEBCAM_ACCEPTANCE_CHECKLIST.md](docs/WEBCAM_ACCEPTANCE_CHECKLIST.md) | Real-webcam test plan |
| [docs/ANALYTICS.md](docs/ANALYTICS.md) | How every dashboard metric is calculated |
| [docs/SESSION_INTEGRITY.md](docs/SESSION_INTEGRITY.md) | Tab-switch rule, multiple-face detection, activity report, privacy, limits |
| [docs/SESSION_INTEGRITY_CHECKLIST.md](docs/SESSION_INTEGRITY_CHECKLIST.md) | Real-Chrome and real-webcam acceptance checks |
| [docs/RL_ENGINE.md](docs/RL_ENGINE.md) | Q-learning state, actions, rewards, training and evaluation |
| [facial_analysis/README.md](facial_analysis/README.md) | Camera agent details |

## Privacy and security in brief

- **Camera data:**
  - The camera agent never stores or sends images or video, only numbers
    and yes/no signals.
  - A quiz with no valid camera reading is stored as "unknown", never as
    low attention.
  - Multiple-face detection records only how many faces and when, never
    who; tab checks record when the quiz page was hidden, never which tab,
    site or app.
- **Accounts and access:**
  - Passwords are bcrypt-hashed.
  - Each student can only read their own records.
  - Quiz answers are never sent before submission, and quizzes are graded
    on the server.
- **Known limitation:** the login token is kept in the browser's
  `localStorage`. See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md#known-limitations)
  for this and the other known limitations.
