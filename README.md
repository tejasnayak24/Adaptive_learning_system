# Run Instructions

## Backend

```powershell
cd C:\Users\tejas\Adaptive_learning_system
$env:PYTHONPATH = "$PWD\backend"
uvicorn backend.app.main:app --reload --port 8000
Frontend

Open a new terminal:

cd C:\Users\tejas\Adaptive_learning_system\frontend
npm install
npm run dev
Facial Analysis

Open another terminal:

cd C:\Users\tejas\Adaptive_learning_system\facial_analysis
.\venv\Scripts\Activate.ps1
python main.py

If venv does not exist:

python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py

Make sure STUDENT_ID in facial_analysis/config.py matches the student account being tested.

Database

Make sure PostgreSQL is running and the .env file is configured in backend/.

If the database needs to be seeded:

python backend\seed_science.py
Application

Keep all three services running:

Backend: http://localhost:8000
Frontend: http://localhost:5173
Facial Analysis: python main.py

Then open:

http://localhost:5173