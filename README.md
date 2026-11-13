# Aegis — Adaptive Learning System

Aegis has three services that run side by side:

| Service | Folder | URL / command |
|---|---|---|
| Backend API (FastAPI + PostgreSQL) | `backend/` | http://localhost:8000 |
| Frontend (React + Vite) | `frontend/` | http://localhost:5173 |
| Facial analysis (OpenCV + MediaPipe) | `facial_analysis/` | `python main.py` |

## 1. Database

PostgreSQL must be running. Copy `backend/.env.example` to `backend/.env`
and fill in your own `DATABASE_URL` and `SECRET_KEY` (never commit `.env`).

The schema is managed with **Alembic**. From `backend/`:

```powershell
cd C:\Users\tejas\Adaptive_learning_system\backend
python -m alembic upgrade head
```

> Upgrading a database that was created **before** Alembic was introduced?
> Take a backup first (`pg_dump -Fc -f backup.dump <database>`), then mark it
> as matching the original schema and upgrade:
>
> ```powershell
> python -m alembic stamp 0001_baseline
> python -m alembic upgrade head
> ```

Load the Grade 6–10 curriculum (Mathematics, Science, Social Science and
English). It is safe to re-run: rows are matched by slug and never duplicated
or deleted, and the original Science lessons keep their ids and progress.

```powershell
cd C:\Users\tejas\Adaptive_learning_system
python backend\scripts\import_curriculum.py --check   # validate content only
python backend\scripts\import_curriculum.py           # import
```

Content lives in `backend/curriculum/content/g<grade>_<subject>.json`.

## 2. Backend

```powershell
cd C:\Users\tejas\Adaptive_learning_system
$env:PYTHONPATH = "$PWD\backend"
uvicorn backend.app.main:app --reload --port 8000
```

Start it from the project root: the backend imports the `rl_engine` package.

Run the backend tests (they use a throwaway SQLite database, never PostgreSQL):

```powershell
cd C:\Users\tejas\Adaptive_learning_system\backend
pip install -r requirements-dev.txt
python -m pytest
```

## 3. Frontend

```powershell
cd C:\Users\tejas\Adaptive_learning_system\frontend
npm install
npm run dev
```

The Vite dev server forwards `/api/*` to the backend on port 8000.

## 4. Facial analysis (camera agent — required for lessons)

```powershell
cd C:\Users\tejas\Adaptive_learning_system\facial_analysis
.\venv\Scripts\Activate.ps1
python main.py
```

If the venv does not exist:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

The agent listens on `http://127.0.0.1:8765` and keeps the webcam **off**
until a lesson starts. The website pairs with it automatically using a
single-use token — no student id is configured anywhere. Lessons and quizzes
unlock only after camera monitoring is verified, and pause if it fails.
See `facial_analysis/README.md` for details and troubleshooting, and
`docs/WEBCAM_ACCEPTANCE_CHECKLIST.md` for the real-webcam test plan.

## 5. Recommendation engine (offline Q-learning)

The backend loads the trained Q-table `rl_engine/q_table.json` (state-key
version 3). To retrain it offline (about a minute) and run the RL tests:

```powershell
cd C:\Users\tejas\Adaptive_learning_system
python -m rl_engine.train
cd rl_engine
python -m pytest
```

Training only replaces the table if the new one passes validation against
the previous rule policy and a random policy; the old table is archived in
`rl_engine/archive/`. Restart the backend afterwards. See
`docs/RL_ENGINE.md` for the full design (state, actions, rewards, update
rule, simulator, evaluation). Real outcomes can be summarised with
`python backend\scripts\rl_outcome_report.py`.

## 6. Use the app

Keep all three services running, then open http://localhost:5173.
The first lesson asks for camera-monitoring consent (students under 18 also
confirm parent/guardian and school authorisation).
