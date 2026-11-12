# 👨‍💻 Adaptive Learning System - Team Guide

Welcome to the Adaptive Learning System project.

This guide explains how our team will collaborate, our responsibilities, Git workflow, API contracts, coding standards, and project expectations.

---

# 👥 Team Members

| Member | Role |
|---------|------|
| Tejas Nayak | Team Lead • Reinforcement Learning • Integration |
| Rohan | Facial Analysis |
| Roshwin | Frontend |
| Rishika | Backend |

---

# 📂 Project Structure

```
adaptive-learning-system/

README.md

TEAM_GUIDE.md

PROMPTS/

frontend/

backend/

rl_engine/

facial_analysis/
```

---

# 🏗 Module Responsibilities

## 🧠 Tejas (Team Lead)

Responsible for

- Reinforcement Learning
- Recommendation Engine
- Project Integration
- API Contracts
- Code Reviews
- Final Testing
- GitHub Repository Management

Folder

```
rl_engine/
```

---

## 👁 Rohan

Responsible for

- Face Detection
- Eye Tracking
- Head Pose Estimation
- Attention Score
- Camera Integration

Folder

```
facial_analysis/
```

---

## 💻 Roshwin

Responsible for

- React Frontend
- Dashboard
- Student Interface
- Teacher Interface
- API Integration
- Charts
- UI Design

Folder

```
frontend/
```

---

## ⚙ Rishika

Responsible for

- FastAPI Backend
- Authentication
- Database
- CRUD APIs
- Student Management
- Lesson Management
- Quiz APIs

Folder

```
backend/
```

---

# 🚫 Folder Ownership Rules

Each member owns only their assigned folder.

Do NOT modify another member's folder without discussing it first.

Example

Rohan should never modify

backend/

frontend/

Tejas should avoid changing frontend code unless integration requires it.

---

# 🔌 API Contracts

These are the endpoints the backend actually serves (source of truth:
`backend/app/routers/`; interactive docs at `http://localhost:8000/docs`).
All responses use `{ "success", "message", "data" }` unless noted.

🔒 = requires `Authorization: Bearer <token>`. 👤 = owner only (a student
can only access their own records; others get **403**).
🎓 = teacher or admin role only.

## Authentication

| Method | Path | Notes |
|---|---|---|
| POST | `/register` | `{name, email, password, age}` → new account (role `student`) |
| POST | `/login` | `{email, password}` → `{access_token, token_type}` |
| POST | `/token` | OAuth2 form login (used by the Swagger "Authorize" button) |
| GET | `/profile` 🔒 | The signed-in student: `{id, name, email, age, role, created_at}` |

Roles are changed only with `python backend/scripts/set_role.py <email> <role>`.

## Lessons

| Method | Path | Notes |
|---|---|---|
| GET | `/lessons` | All lessons |
| GET | `/lesson/{id}` | Lesson content + its quizzes |
| POST | `/lesson` 🔒🎓 | Create a lesson |
| PUT | `/lesson/{id}` 🔒🎓 | Partial update (only sent fields change) |
| DELETE | `/lesson/{id}` 🔒🎓 | Delete a lesson |

## Quiz

| Method | Path | Notes |
|---|---|---|
| GET | `/quiz/lesson/{lesson_id}` 🔒 | Quizzes of a lesson |
| GET | `/quiz/{id}` 🔒 | Quiz + questions. **Never includes correct answers.** |
| POST | `/quiz/start` 🔒 | `{quiz_id}` → same payload as `GET /quiz/{id}` |
| POST | `/quiz/submit` 🔒 | See below |

`POST /quiz/submit` body:

```json
{
  "quiz_id": 3,
  "answers": { "11": "B", "12": "A" },
  "response_time": 42.0,
  "hints_used": 1,
  "attention_score": 0.82,
  "yawning": false,
  "looking_away": false,
  "drowsy": null
}
```

* The **server grades** the answers; a client-sent score is ignored.
* Every question of the quiz must be answered once (else **422**).
* Camera fields are `null` when telemetry was unavailable — never guessed.
* Response `data`: `progress` (stored attempt), `grading`
  (`score`, `correct_count`, `total_questions`, per-question `results`
  including the correct answer — revealed only after submission),
  `recommendation` (or `null`) and `recommendation_status`
  (`available` | `telemetry_unavailable`).

## Adaptive recommendations (RL)

| Method | Path | Notes |
|---|---|---|
| GET | `/recommendations/latest` 🔒 | `{status, recommendation, attempt}`; status is `available`, `telemetry_unavailable`, `not_generated` or `no_attempts` |
| GET | `/recommendations` 🔒 | The student's recommendation history |
| POST | `/rl/recommend` 🔒 | Stateless recommendation for a supplied state (13 fields, see `/docs`). Returns `{action, confidence, explanation, policy, telemetry_available}`; `action` is `null` when any camera field is `null`. |

Recommendations are generated **by the server when a quiz is graded**, from
the stored attempt, and saved to `recommendation_history`. When the
student's next attempt arrives, its outcome is recorded in `reward_history`.
`policy` reports whether a rule (`rules`) or the learned Q-table
(`q_learning`) chose the action.

The old `POST /recommend` placeholder has been removed.

## Facial-analysis telemetry

| Method | Path | Notes |
|---|---|---|
| POST | `/attention` | Camera agent → `{student_id, attention_score (0–1), yawning, looking_away}` once per second |
| GET | `/attention/{student_id}` 🔒👤 | `{available, status, age_seconds, attention_score, …, session_average_attention}` |
| POST | `/attention/{student_id}/reset` 🔒👤 | Start a new per-quiz aggregation window |

`status` is `live`, `stale` (no reading for more than 5 s) or `no_data`.
When not `live`, every measurement is `null`.

## Student progress

| Method | Path | Notes |
|---|---|---|
| GET | `/progress/{student_id}` 🔒👤 | All attempts, oldest first |
| GET | `/progress/{student_id}/{lesson_id}` 🔒👤 | Latest attempt for a lesson |
| PUT | `/progress/{progress_id}` 🔒👤 | Update an attempt |

## Database changes

The schema is managed with Alembic (`backend/migrations`). Never change
tables by hand: add a migration (`python -m alembic revision -m "..."`),
test it on a copy of the database, then run `python -m alembic upgrade head`.

---

# 🌿 Git Workflow

Every member works only on their own branch.

Example

```
tejas/rl-engine

rohan/facial-analysis

roshwin/frontend

rishika/backend
```

Never work directly on main.

---

## First Time Setup

Clone repository

```
git clone <repo-url>
```

Create your branch

Example

```
git checkout -b rohan/facial-analysis
```

Push branch

```
git push -u origin rohan/facial-analysis
```

---

## Daily Workflow

Pull latest changes

```
git checkout main

git pull origin main
```

Switch to your branch

```
git checkout rohan/facial-analysis
```

Work

Commit

```
git add .

git commit -m "Implemented attention score"
```

Push

```
git push
```

Inform Team Lead.

Team Lead reviews.

Merge to main.

---

# 📌 Commit Message Format

Use meaningful commit messages.

Good

```
Added login API

Implemented Q-Learning

Created dashboard UI

Integrated facial analysis API
```

Avoid

```
Update

Changes

Done

Fixed
```

---

# 🧪 Before Asking for Review

Make sure

- Code runs
- No syntax errors
- No unnecessary files
- API format unchanged
- No merge conflicts
- Code is commented
- README updated if necessary

---

# 📝 Coding Standards

Use meaningful variable names.

Write modular code.

Comment important logic.

Avoid duplicate code.

Follow folder structure.

Keep functions small.

---

# 🤝 Communication Rules

If changing an API,

Inform the team first.

If changing database schema,

Inform the backend developer.

If changing recommendation format,

Inform frontend developer.

Never surprise teammates with breaking changes.

---

# 🏁 Development Order

Phase 1

Repository Setup

↓

Backend APIs

↓

Frontend Screens

↓

Facial Analysis

↓

RL Engine

↓

Integration

↓

Testing

↓

Final Demo

---

# 🎯 Project Goal

Our objective is not just to complete a college project.

We aim to build a clean, modular, scalable Adaptive Learning System where every module integrates seamlessly.

Every contribution should improve the overall quality of the system.

Let's build something we are proud to present.