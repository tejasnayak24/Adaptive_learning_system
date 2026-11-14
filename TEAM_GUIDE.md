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

## Health

`GET /` — returns `{success: true}` when the API is running (used by `start-all.ps1`).

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
| GET | `/lessons` 🔒 | Lessons of the student's grade in curriculum order (all grades for teachers/admins; empty until a grade is chosen) |
| GET | `/lesson/{id}` 🔒 | Lesson, its quizzes, structured `material` (objectives, sections, definitions, examples, worked examples, diagram, real world, takeaways, practice), `grade`, `subject`, `unit`, `curriculum_topic` and `navigation` (previous/next/skip within the grade and subject). 403 for another grade, 409 `grade_required` if the student has no grade |
| POST | `/lesson` 🔒🎓 | Create a lesson |
| PUT | `/lesson/{id}` 🔒🎓 | Partial update (only sent fields change) |
| DELETE | `/lesson/{id}` 🔒🎓 | Delete a lesson |

## Curriculum (Phase 5)

Hierarchy: Grade (6–10) → Subject (Mathematics, Science, Social Science,
English) → Unit → Topic → Lesson → Material → Quizzes (EASY/MEDIUM/HARD).
Content is imported from `backend/curriculum/content/*.json` with
`python backend/scripts/import_curriculum.py` (idempotent).

| Method | Path | Notes |
|---|---|---|
| PUT | `/profile/grade` 🔒 | `{grade: 6..10}` — choose or change the student's grade (progress kept). `GET /profile` and `POST /register` include `grade` |
| GET | `/curriculum` 🔒 | `?subject=` optional. The student's grade: subjects → units → topics → lessons (quizzes, attempts, best score). Teachers/admins may pass `?grade=` |
| GET | `/curriculum/grades` 🔒 | Lesson counts per grade and subject |
| GET | `/curriculum/lessons/{id}/navigation` 🔒 | Previous / next / skip / next topic within the grade and subject |

## Quiz

| Method | Path | Notes |
|---|---|---|
| GET | `/quiz/lesson/{lesson_id}` 🔒 | Quizzes of a lesson |
| GET | `/quiz/{id}` 🔒 | Quiz + questions with a topic-specific `hint` each. **Never includes correct answers or explanations.** |
| POST | `/quiz/start` 🔒 | `{quiz_id}` → same payload as `GET /quiz/{id}` |
| POST | `/quiz/submit` 🔒 | See below |

`POST /quiz/submit` body:

```json
{
  "quiz_id": 3,
  "answers": { "11": "B", "12": "A" },
  "response_time": 42.0,
  "hints_used": 1,
  "monitoring_session_id": "ms_…"
}
```

* The **server grades** the answers; a client-sent score is ignored.
* Every question of the quiz must be answered once (else **422**).
* `monitoring_session_id` (the student's own, not ended) is required.
  Camera measurements are taken by the server from that session's agent
  telemetry; any camera values sent by the browser are ignored. They are
  `null` when nothing was measured — never guessed.
* Response `data`: `progress` (stored attempt), `grading`
  (`score`, `correct_count`, `total_questions`, per-question `results`
  including the correct answer — revealed only after submission),
  `recommendation` (or `null`) and `recommendation_status`
  (`available` | `telemetry_unavailable`).

## Adaptive recommendations (RL)

| Method | Path | Notes |
|---|---|---|
| GET | `/recommendations/latest` 🔒 | `{status, recommendation, next_step, attempt}`; status is `available`, `telemetry_unavailable`, `not_generated` or `no_attempts`. `attempt` includes `subject`, `grade` and `curriculum_topic` |
| GET | `/recommendations` 🔒 | `?limit=1..200` (default 20). The student's recommendations, newest first, each with `context` (lesson, subject, topic, score of the attempt that produced it) and `outcome` (`{status: "pending"}` until the next quiz, then that quiz's score, `score_change`, `followed` (true/false/null = not observable) and `reward`) |
| POST | `/rl/recommend` 🔒 | Stateless recommendation for a supplied state (13 fields + optional `drowsy`, see `/docs`). Returns `{action, confidence, confidence_kind, explanation, policy, model_version, state_key, q_values, runner_up, margin, blocked_actions, untested_actions, state_visits, telemetry_available}`; `action` is `null` when any camera field is `null`. |
| GET | `/rl/model` 🔒 | Loaded Q-table: `model_version`, `trained_at`, `states_learned`, `state_key_version` (3), `training: "offline_simulation"`, `online_updates: false` |

Recommendations are generated **by the server when a quiz is graded**, from
the stored attempt, and saved to `recommendation_history` (with
`model_version` and `decision_detail`). When the student's next attempt
arrives, its observed reward (reward version 2, same formula as training) is
recorded in `reward_history` with `followed` and `reward_detail`.

`policy` is `q_learning` (learned Q-table chose among the permitted actions),
`q_learning_nearest_state` (state not learned; most similar learned state
used) or `fallback` (nothing learned applies; `REPEAT_LESSON`, confidence 0).
Rows from before Phase 4 say `rules`. `confidence` is a heuristic decision
strength, **not a probability**. Safety constraints only remove unsuitable
actions; they never choose one. Full details: `docs/RL_ENGINE.md`.

Retrain offline with `python -m rl_engine.train` (validates before replacing
`rl_engine/q_table.json`); the running backend never changes the table.

The old `POST /recommend` placeholder has been removed.

## Camera monitoring (local agent)

Lessons and quizzes require a verified monitored session. The camera agent
(`facial_analysis/main.py`) listens on `http://127.0.0.1:8765` (see
`facial_analysis/README.md`).

| Method | Path | Caller | Notes |
|---|---|---|---|
| GET | `/monitoring/consent` 🔒 | browser | `{required_version, is_minor, valid, consent}` |
| POST | `/monitoring/consent` 🔒 | browser | `{accept: true, guardian_authorization_confirmed, school_authorization_confirmed}`; both confirmations required when age < 18 |
| DELETE | `/monitoring/consent` 🔒 | browser | Withdraw; ends open sessions |
| POST | `/monitoring/sessions` 🔒 | browser | `{lesson_id}` → `{session_id, pairing_token, …}` (403 without consent). Ends the student's other open sessions |
| POST | `/monitoring/sessions/{id}/pairing` 🔒👤 | browser | Reconnect: new single-use pairing token, old agent token revoked |
| GET | `/monitoring/sessions/{id}` 🔒👤 | browser | `{state, verified, camera_error, lighting_ok, …}`; also keeps the session alive |
| POST | `/monitoring/sessions/{id}/end` 🔒👤 | browser | End the session (agent releases the camera) |
| POST | `/monitoring/sessions/{id}/claim` | agent | `{pairing_token}` → `{agent_token, heartbeat_interval}`; single use, 2-minute TTL |
| POST | `/monitoring/heartbeat` | agent (Bearer agent token) | Once per second: `{sequence, captured_at, camera_ok, face_detected, face_stable, attention_score, yawning, looking_away, possible_drowsiness, …}` |
| POST | `/monitoring/agent/end` | agent (Bearer agent token) | Agent shutting down; session waits for reconnection |

`state` is `awaiting_agent`, `stale` (no heartbeat within 5 s),
`camera_unavailable`, `no_face`, `verifying`, `verified` or `ended`.
Only `verified` permits learning. A session the browser stops polling for
60 s is ended automatically.

Tokens are never put in URLs, never logged, and only their SHA-256 hashes are
stored. The agent never sends a student id: the backend derives it from the
token. Out-of-order heartbeats (409) and measurements captured more than 3 s
earlier are rejected as not live.

## Facial-analysis telemetry (read-only)

| Method | Path | Notes |
|---|---|---|
| GET | `/attention/{student_id}` 🔒👤 | Live view: `{available, status, age_seconds, attention_score, possible_drowsiness, …, session_average_attention}` |
| POST | `/attention/{student_id}/reset` 🔒👤 | Start a new per-quiz measurement window |

`status` is `live`, `no_face`, `camera_unavailable`, `stale` or `no_data`;
when not live, measurements are `null`. The old unauthenticated
`POST /attention` was removed.

## Student progress

| Method | Path | Notes |
|---|---|---|
| GET | `/progress/{student_id}` 🔒👤 | All attempts, oldest first |
| GET | `/progress/{student_id}/{lesson_id}` 🔒👤 | Latest attempt for a lesson |
| PUT | `/progress/{progress_id}` 🔒🎓 | Teachers/admins only: correct an attempt. Students cannot edit attempts (scores are graded by the server, camera values come from the agent) |

## Learning analytics (Phase 6)

| Method | Path | Notes |
|---|---|---|
| GET | `/analytics/summary` 🔒 | The signed-in student's own analytics (no student id parameter, so no cross-student access): `student`, `overview`, `subjects`, `topics`, `topic_status_counts`, `trend`, `attention`, `activity`, `milestones`, `definitions`. See [docs/ANALYTICS.md](docs/ANALYTICS.md) for every calculation |

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