# Testing

Aegis has four automated test suites, plus content and migration checks.
**None of them uses your PostgreSQL database:** the backend and camera-agent
tests build throwaway SQLite databases, and the other suites need no
database at all.

## Running the suites

| Suite | Run in | Command | Needs |
|---|---|---|---|
| Backend API (194 tests) | `backend/` | `python -m pytest` | `pip install -r requirements-dev.txt` |
| Recommendation engine (68) | `rl_engine/` | `python -m pytest` | pytest only (installed by the backend's `requirements-dev.txt`) |
| Camera agent (51) | `facial_analysis/` | `.\venv\Scripts\python.exe -m pytest` | `.\venv\Scripts\python.exe -m pip install -r requirements-dev.txt`; see the integration test below |
| Frontend unit tests (46) | `frontend/` | `npm test` | `npm ci` |
| Frontend lint | `frontend/` | `npm run lint` | `npm ci` |
| Frontend production build | `frontend/` | `npm run build` | `npm ci` (output in `frontend/dist/`, git-ignored) |
| Curriculum content | project root | `python backend/scripts/import_curriculum.py --check` | backend requirements; never opens a database connection |
| One curriculum file | project root | `python backend/scripts/check_curriculum_file.py backend/curriculum/content/g08_science.json` | backend requirements |
| Migrations vs models | `backend/` | covered by `tests/test_migrations.py`; see below for PostgreSQL | — |

On macOS or Linux, use `./venv/bin/python` instead of `.\venv\Scripts\python.exe`.

### What each suite uses

- **Backend.** `backend/tests/conftest.py` points `DATABASE_URL` at a
  throwaway SQLite file and sets a test `SECRET_KEY` *before* the app is
  imported, and each test gets an in-memory SQLite database built from the
  models. `backend/.env` cannot override these (`load_dotenv` never
  replaces variables that are already set).
- **Migrations.** `tests/test_migrations.py` runs the real Alembic
  migrations on a fresh SQLite file: `upgrade head`, `alembic check`, the
  Science seed (twice, to prove it never duplicates), then a downgrade and
  a second upgrade.
- **Camera agent.** Synthetic face landmarks replace the webcam, so no
  camera is needed. `tests/test_integration_backend.py` also starts the
  real backend in a separate process on a throwaway SQLite database and
  pairs the real agent with it. It runs only when `AEGIS_BACKEND_PYTHON`
  names a Python interpreter that has the backend requirements installed;
  otherwise it is skipped:

  ```powershell
  $env:AEGIS_BACKEND_PYTHON = (Get-Command python).Source   # or your backend venv's python.exe
  .\venv\Scripts\python.exe -m pytest
  ```

- **Manual webcam scripts** in `facial_analysis/tests/manual/` open the
  real camera and are deliberately not collected by pytest.

### Checking migrations against PostgreSQL

`alembic check` compares the models with the database it is pointed at and
changes nothing. To test the migrations themselves on PostgreSQL, use an
empty scratch database, never one with real data:

```powershell
& "C:\Program Files\PostgreSQL\18\bin\createdb.exe" -U postgres aegis_scratch
cd backend
$env:DATABASE_URL = "postgresql://postgres:<password>@localhost:5432/aegis_scratch"
python -m alembic upgrade head
python -m alembic check          # expect "No new upgrade operations detected."
Remove-Item Env:DATABASE_URL     # back to backend/.env
```

A `DATABASE_URL` set in the shell takes precedence over `backend/.env`.

## Results for this release (2026-11-14)

All suites were run on Windows 11 with Python 3.10 and Node.js 24, from
**fresh installs**: new virtual environments created from
`backend/requirements-dev.txt` and `facial_analysis/requirements-dev.txt`,
and `npm ci` on the tracked frontend files.

| Check | Result |
|---|---|
| Backend tests | 194 passed |
| Recommendation-engine tests | 68 passed |
| Camera-agent tests, including the backend integration test | 51 passed |
| Frontend unit tests | 46 passed |
| Frontend lint | clean |
| Frontend production build | succeeds |
| Curriculum content | 20 files, 122 lessons, no problems |
| Fresh PostgreSQL 18 database | 8 migrations to `0008_session_events (head)`; `alembic check` clean; curriculum import creates 122 lessons, 366 quizzes and 1,479 questions, and a second import creates nothing |
| API smoke test on that database (the README's start command) | 19/19: health, Swagger UI, 43 endpoints listed, registration, login, wrong password refused, grade selection, Grade 8 curriculum (4 subjects, 24 lessons), lesson material, no answers in quiz questions, consent required, monitoring refused without consent, model info (offline training, no online updates) |

## Acceptance evidence

Browser runs used Google Chrome (headless) driven by Playwright, the real
backend on an **isolated copy** of the database, and the **real camera-agent
code with a synthetic camera** (scripted landmarks for a normal face, no
face, yawning, looking away, closed eyes and camera failure). The
automation scripts were run from a separate working folder and are not part
of the repository; the manual checklists below cover the same ground.

| Date | What | Result |
|---|---|---|
| 2026-11-12 | Real webcam on the team lead's Windows laptop ([checklist](WEBCAM_ACCEPTANCE_CHECKLIST.md)) | Reported as passed overall (detection, voice alerts, recovery); not ticked line by line |
| 2026-11-13 | Full learning journey in the browser | 38/38 journey checks, 9/9 extra checks, 7/7 production-build checks |
| 2026-11-13 | API regression on the database copy: 20 grade-subject combinations, 366 quizzes with no answer leaks, camera-agent authentication, stale telemetry, ownership | 34/34; the earlier curriculum and analytics checks re-run: 11/11 and 23/23 |
| 2026-11-14 | Session integrity in the browser: tab switching (warning, second switch, more than 10 s, blur ignored, cancelled and confirmed reloads, network loss, leave confirmation, cooldown) | 27/27 |
| 2026-11-14 | Multiple-face detection: brief face ignored, warning after about 3 s, clears, quiz never ended | 11/11 |
| 2026-11-14 | Session Activity page and consent v2 | 13/13 |
| 2026-11-14 | Full learning journey re-run after the session-integrity changes | 38/38 and 9/9 |
| 2026-11-14 | Session integrity with real Chrome and a real webcam ([checklist](SESSION_INTEGRITY_CHECKLIST.md)) | Reported as passed by the project team |
| 2026-11-14 | Redesigned frontend: sign-in and app shell 11/11; learning flow and quiz dialogs 18/18 (repeated on the production build); insight pages 15/15; every page at 1440, 1280, 768 and 390 px without horizontal overflow 37/37; quiz and results at 390 px 2/2; behaviour (camera gate, multiple-face banner, reduced motion, keyboard focus, skip link) 11/11; production smoke 3/3; results scroll 1/1 | 98/98, no console errors |

Bugs these runs found, all fixed before release:
- a false "Webcam unavailable" flash about 1.5 s after consent;
- a lesson from another grade asked for camera verification before
  showing the refusal;
- the registration success message was missing on the sign-in page;
- quiz dialogs did not dim the whole window, and quiz results opened
  mid-page;
- two version-less entries in `frontend/package-lock.json` broke
  `npm install`.

### What automation cannot prove

- **Hiding a real tab.** Headless Chrome, and Chrome launched by test
  tools, never hid a background tab on the development laptop, so the
  page-visibility change was simulated. Real-Chrome checks are in
  [SESSION_INTEGRITY_CHECKLIST.md](SESSION_INTEGRITY_CHECKLIST.md).
- **A real webcam and real faces.** Automated runs use synthetic landmarks;
  see [WEBCAM_ACCEPTANCE_CHECKLIST.md](WEBCAM_ACCEPTANCE_CHECKLIST.md).
- **Other browsers and systems.** Only Chrome on Windows 11 was tested.

## Manual visual pass

About 10 minutes in Chrome or Edge, signed in as a student with a few quizzes.

| ✓ | Page | Look for |
|---|---|---|
| ☐ | Sign in / Register | Password show/hide toggle; errors shown next to the field; the grade choice on registration |
| ☐ | Dashboard | Greeting and grade, completion ring, stat cards, *Continue learning* and *Latest activity*, subject progress, AI coach card; no overlapping text |
| ☐ | My Learning | Four subject cards; search and status filter; units → topics → lessons with Easy, Medium and Hard |
| ☐ | Lesson | Readable sections; *In this lesson* chips jump to sections; the diagram renders; no raw JSON or `undefined` |
| ☐ | Quiz | Selected option highlighted; hint readable; timer running; question navigator; *Review and submit* asks for confirmation |
| ☐ | Results | Score, *Your AI coach's next step*, answer review with "Why:" explanations |
| ☐ | Progress | The filter row changes the charts and the quiz history; "No quizzes match these filters" for an empty range; every chart has a table view |
| ☐ | AI Coach | Advice, *Based on your quiz*, history with outcomes, the 11 actions with the current one marked *Current advice* |
| ☐ | Session Activity | One timeline per attempt; no score or verdict anywhere |
| ☐ | Phone width (DevTools, 390 px) | The menu button opens the navigation drawer; cards stack; tables become lists of cards; no sideways scrolling |
| ☐ | Console (DevTools) | No red errors, except a 401 after a deliberately wrong password |
