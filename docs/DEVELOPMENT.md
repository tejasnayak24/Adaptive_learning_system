# Development guide

How to work on Aegis after the first-time setup in the
[README](../README.md#installation-and-setup). For the design, see
[ARCHITECTURE.md](ARCHITECTURE.md); for every endpoint, see
[API_REFERENCE.md](API_REFERENCE.md); for the test suites, see
[TESTING.md](TESTING.md).

## Running the services one by one

`start-all.ps1` starts everything on Windows. To run a single service (for
example, to watch its log), use one terminal per service. The commands
below are what `start-all.ps1` runs.

| Service | Run from | Windows (PowerShell) |
|---|---|---|
| Backend API, port 8000 | project root | `$env:PYTHONPATH = "$PWD\backend"; python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000` |
| Camera agent, port 8765 | `facial_analysis/` | `.\venv\Scripts\python.exe main.py` |
| Frontend, port 5173 | `frontend/` | `npm run dev` |

The backend must start from the project root with `backend/` on
`PYTHONPATH`: the API is imported as `app.*` and it also imports the
recommendation engine from `rl_engine/`.

Camera agent options:

| Command (in `facial_analysis/`) | Purpose |
|---|---|
| `python main.py` | Normal agent; the webcam stays off until a lesson starts |
| `python main.py --no-window` | Agent without the "Aegis Camera Agent" preview window |
| `python main.py --preview` | Local preview of all detectors, without the backend |
| `python tests/manual/check_face_detector.py` | Manual webcam checks (see `tests/manual/`) |

The frontend dev server reads three optional environment variables, set in
the shell before `npm run dev` (see the
[README](../README.md#environment-variables)). The camera agent only accepts
requests from the frontend on port 5173, so keep that port.

## Database migrations

The schema is managed by Alembic (`backend/migrations/versions/`). Never
change tables by hand.

```powershell
cd backend
python -m alembic current                            # revision of the configured database
python -m alembic upgrade head                       # apply pending migrations
python -m alembic check                              # models and migrations agree (read only)
python -m alembic revision --autogenerate -m "short description"   # new migration
```

- The database URL comes from `DATABASE_URL` in `backend/.env`. A
  `DATABASE_URL` set in the shell takes precedence, which is the safe way
  to point a command at a scratch database.
- Review every generated migration before using it, run it on a copy of
  the database first, and **back up before migrating a database with real
  data** (`pg_dump -Fc -f backup.dump <database>`).
- `backend/tests/test_migrations.py` upgrades a fresh SQLite database to
  head, runs `alembic check`, downgrades and upgrades again.

**A database created before Alembic was introduced** (no `alembic_version`
table) must be stamped once: back it up, then run
`python -m alembic stamp 0001_baseline` and `python -m alembic upgrade head`.

## Curriculum content

Lessons and quizzes live in JSON files, one per grade and subject:
`backend/curriculum/content/g<grade>_<subject>.json` (20 files, Grades 6–10 ×
Mathematics, Science, Social Science and English; 122 lessons). Each file
holds units → topics → lessons. A lesson has objectives, an introduction,
sections, definitions, examples, worked examples, a diagram, a real-world
application, takeaways, practice and Easy, Medium and Hard quizzes. The
exact format is enforced by `backend/curriculum/validate.py`.

```powershell
# from the project root
python backend\scripts\check_curriculum_file.py backend\curriculum\content\g08_science.json   # one file: summary and problems
python backend\scripts\import_curriculum.py --check                                           # validate all files (no database access)
python backend\scripts\import_curriculum.py                                                   # import into the configured database
```

The importer is idempotent: rows are matched by slug, so re-running it never
duplicates or deletes anything. It first creates the five original Science
lessons if they are missing (`backend/seed_science.py`) and adopts them into
Grades 9 and 10 with their ids, questions and progress unchanged.

## Recommendation engine

The backend loads `rl_engine/q_table.json` once at start-up and never
changes it. To retrain it offline on simulated students (about a minute):

```powershell
python -m rl_engine.train          # from the project root
```

The new table replaces the current one only if it passes validation against
held-out simulated students (it must beat a random policy, be no worse than
the old rule policy, make no safety-constraint violations and cover at least
half of the states). The previous table is archived in `rl_engine/archive/`.
Restart the backend afterwards. To summarise how real recommendations
turned out, run `python backend\scripts\rl_outcome_report.py`
(`--export file.jsonl` writes pseudonymised transitions). See
[RL_ENGINE.md](RL_ENGINE.md).

## Teacher and admin roles

Teachers and admins can create, edit and delete lessons and correct quiz
attempts through the API. There is no role management in the API or the
website:

```powershell
python backend\scripts\set_role.py teacher@example.com teacher   # student | teacher | admin
```

## Rules that keep the system honest

Changes must keep these properties; the tests check most of them.

- **Grading is server-side.** Correct answers and explanations are never
  sent before a quiz is submitted, and a score sent by the browser is
  ignored.
- **Camera values come from the agent, never the browser.** A missing
  measurement is stored as `NULL` ("unavailable"), never as a guessed or
  low value. Without valid camera telemetry no recommendation is made.
- **No images or video leave the camera agent.** It sends numbers and
  yes/no signals only.
- **The Q-table decides.** Safety constraints may only remove unsuitable
  actions; the learned Q-values choose among the rest. The runtime never
  updates the table.
- **Session integrity is decided by the server**, and a hidden tab or a
  second face is never presented as proof of misconduct. The quiz-integrity
  wording is relied on by
  [SESSION_INTEGRITY_CHECKLIST.md](SESSION_INTEGRITY_CHECKLIST.md); change
  both together.
- **Students only see their own records.** New endpoints must check
  ownership or derive the student from the token.
- **Frontend:** build pages from the shared components described in
  [frontend/DESIGN_SYSTEM.md](../frontend/DESIGN_SYSTEM.md). Keep in-app
  navigation as links and do not wrap the quiz page in transformed or
  animated containers; the quiz leave-guard and dialogs rely on both.

## Code style and Git workflow

- **Python:** type hints, Pydantic schemas for request bodies, SQLAlchemy
  models, routers kept thin with the logic in `app/services/`. Successful
  responses use the `{success, message, data}` envelope.
- **Frontend:** React function components, API calls only in
  `src/services/`, Tailwind classes using the design tokens.
- **Branches:** create a branch from an up-to-date `main` for each change
  (`feature/<topic>` or `fix/<topic>`) and open a pull request into `main`.
  Do not commit directly to `main`.
- **Commits:** one logical change per commit, with a message that says what
  changed and why ("Add multiple-face episode report", not "update").
- **Before opening a pull request**, run the suites in
  [TESTING.md](TESTING.md) that cover what you changed, and update the
  documentation when behaviour, commands or endpoints change.
- **Never commit** `.env` files, virtual environments, `node_modules`,
  build output, logs, database dumps or webcam recordings. The root
  `.gitignore` covers these.

## Dependencies

| Component | Manifest | Notes |
|---|---|---|
| Backend | `backend/requirements.txt`, `backend/requirements-dev.txt` (adds pytest and httpx) | Pinned to the tested versions |
| Camera agent | `facial_analysis/requirements.txt`, `facial_analysis/requirements-dev.txt` (adds pytest) | Its own virtual environment. Keep `mediapipe==0.10.21`, `numpy==1.26.4` and `opencv-contrib-python==4.11.0.86` together: they are a known-working set |
| Recommendation engine | none | Standard library only; its tests use the backend's pytest |
| Frontend | `frontend/package.json`, `frontend/package-lock.json` | Install with `npm ci` to get exactly the locked versions |

When you add or upgrade a package, update the manifest and the lockfile in
the same commit and rerun the affected test suites.
