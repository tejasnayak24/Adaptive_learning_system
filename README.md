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

Seed the Science curriculum (safe to re-run; existing rows are kept):

```powershell
cd C:\Users\tejas\Adaptive_learning_system
python backend\seed_science.py
```

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

## 5. Use the app

Keep all three services running, then open http://localhost:5173.
The first lesson asks for camera-monitoring consent (students under 18 also
confirm parent/guardian and school authorisation).
