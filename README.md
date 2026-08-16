Aegis — Adaptive Learning System

An adaptive learning platform that uses quiz performance, facial attention telemetry, and reinforcement learning to personalize the learning experience.

🚀 Quick Setup

1. Clone the Repository

git clone <YOUR_GITHUB_REPO_URL>
cd Adaptive_learning_system

2. Backend Setup

cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

Create a backend/.env file with your own PostgreSQL credentials.

Then from the project root:

cd ..
alembic upgrade head
python backend/seed_science.py

The seed populates the database with 5 lessons, 15 quizzes, and 75 questions.

Start the backend:

uvicorn backend.app.main:app --reload --port 8000

Backend API:

http://127.0.0.1:8000

3. Facial Analysis Setup

Open a new terminal:

cd facial_analysis
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py

Allow camera/webcam access when prompted.

4. Frontend Setup

Open another terminal:

cd frontend
npm install
npm run dev

Open:

http://localhost:5173

🧩 Running the Project

Keep these three services running:

Service

Address

Backend

http://127.0.0.1:8000

Facial Analysis

Webcam + telemetry

Frontend

http://localhost:5173

🗄️ Database

Each teammate should use their own local PostgreSQL database and .env.

Run:

alembic upgrade head
python backend/seed_science.py

This provides the common Science lessons, quizzes, and questions, so teammates do not need access to anyone else's database.

Each teammate should create their own .env using their local PostgreSQL credentials.