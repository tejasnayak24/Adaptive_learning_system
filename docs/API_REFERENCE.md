# API reference

The Aegis backend is a FastAPI application. This page describes every
endpoint it serves. The source of truth is `backend/app/routers/`, and the
interactive documentation generated from it is always up to date:

| What | Address (backend running locally) |
|---|---|
| Swagger UI (try requests in the browser) | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |
| OpenAPI schema | http://127.0.0.1:8000/openapi.json |

The frontend reaches the same API through the Vite dev server: a request to
`http://localhost:5173/api/<path>` is forwarded to `http://127.0.0.1:8000/<path>`.

## Conventions

- **Response envelope.** Successful responses use
  `{ "success": true, "message": "...", "data": { ... } }`. The exceptions
  are `POST /login` and `POST /token`, which return the OAuth2 shape
  `{ "access_token": "...", "token_type": "bearer" }`.
- **Errors.** FastAPI's standard format: an HTTP status code and a `detail`
  field: a message, a list of validation problems (**422**), or, for some
  quiz-attempt conflicts, an object with a `message` and the server's view
  of the attempt (noted below).
- **Authentication.** Send the token from `POST /login` as
  `Authorization: Bearer <token>`. Tokens are signed JWTs (HS256) that
  expire after `ACCESS_TOKEN_EXPIRE_MINUTES` (30 minutes by default). In
  Swagger UI, use **Authorize** (it calls `POST /token`).
- **Access column** in the tables below:

  | Value | Meaning |
  |---|---|
  | Public | No token needed |
  | Student | Any signed-in user |
  | Owner | Signed in, and only for the student's own records (another student's records give **403**, or **404** for quiz attempts) |
  | Teacher/admin | Signed in with the `teacher` or `admin` role |
  | Agent | The local camera agent, with its own short-lived agent token (never a student's login token) |

Roles are set only from the command line, never through the API:
`python backend/scripts/set_role.py <email> <student|teacher|admin>`.

## Health

| Method | Path | Access | Notes |
|---|---|---|---|
| GET | `/` | Public | `{success: true}` while the API is running (used by `start-all.ps1`) |

## Authentication

| Method | Path | Access | Notes |
|---|---|---|---|
| POST | `/register` | Public | `{name, email, password, age, grade?}` creates a `student` account. Name 1–100 characters, password 8–72 characters, age 5–100, grade 6–10 (optional; asked for later if missing) |
| POST | `/login` | Public | `{email, password}` → `{access_token, token_type}` |
| POST | `/token` | Public | The same login as an OAuth2 form (used by Swagger's **Authorize** button) |
| GET | `/profile` | Student | `{id, name, email, age, role, grade, created_at}` |
| PUT | `/profile/grade` | Student | `{grade: 6..10}` chooses or changes the grade. Progress is kept |

## Curriculum

The hierarchy is Grade (6–10) → Subject (Mathematics, Science, Social
Science, English) → Unit → Topic → Lesson → Easy, Medium and Hard quizzes.
Content is imported from `backend/curriculum/content/*.json` (see
[DEVELOPMENT.md](DEVELOPMENT.md#curriculum-content)).

| Method | Path | Access | Notes |
|---|---|---|---|
| GET | `/curriculum` | Student | `?subject=` optional. The student's grade: subjects → units → topics → lessons, with quizzes, attempts and best score. Teachers and admins may pass `?grade=` |
| GET | `/curriculum/grades` | Student | Lesson counts per grade and subject |
| GET | `/curriculum/lessons/{lesson_id}/navigation` | Student | Previous, next, skip and next-topic lessons within the grade and subject |

## Lessons

| Method | Path | Access | Notes |
|---|---|---|---|
| GET | `/lessons` | Student | Lessons of the student's grade in curriculum order (all grades for teachers and admins; empty until a grade is chosen) |
| GET | `/lesson/{lesson_id}` | Student | The lesson, its quizzes, structured `material` (objectives, sections, definitions, examples, worked examples, diagram, real-world use, takeaways, practice), `grade`, `subject`, `unit`, `curriculum_topic` and `navigation`. **403** for a lesson of another grade; **409** `grade_required` if the student has no grade yet |
| POST | `/lesson` | Teacher/admin | Create a lesson: `{title, topic, difficulty, content}` |
| PUT | `/lesson/{lesson_id}` | Teacher/admin | Partial update: only the fields sent change |
| DELETE | `/lesson/{lesson_id}` | Teacher/admin | Delete a lesson |

## Quizzes and attempts

| Method | Path | Access | Notes |
|---|---|---|---|
| GET | `/quiz/lesson/{lesson_id}` | Student | Quizzes of a lesson |
| GET | `/quiz/{quiz_id}` | Student | The quiz and its questions, each with a topic-specific `hint`. **Never includes correct answers or explanations** |
| POST | `/quiz/start` | Student | `{quiz_id, mode?, monitoring_session_id?}` → the questions, the server-side `attempt` and `resumed`. Resumes the open attempt after a reload. **429** with a `Retry-After` header during the 5-minute cooldown after a terminated or abandoned attempt; `detail` then holds `message`, `cooldown_until`, `retry_after_seconds` and `previous_attempt` |
| GET | `/quiz/attempts/{attempt_id}` | Owner | The attempt as the server sees it: `status`, `strikes`, `warning`, `end_reason`, `retry_after_seconds` and the saved `answers` |
| PUT | `/quiz/attempts/{attempt_id}/answers` | Owner | Save in-progress answers (partial allowed) and `draft_state`. **409** once the attempt has ended (answers are frozen) |
| POST | `/quiz/attempts/{attempt_id}/events` | Owner | Page events for the tab-switch rule: `{page_id, events: [{seq, kind, client_ms, hidden_ms?, delivery_failures?, queued_ms?, reload?}]}`. `kind` is `hidden`, `visible`, `pagehide`, `resume`, `hidden_tick`, `blur`, `focus`, `online` or `offline`. A repeated `(page_id, seq)` is ignored. Returns the attempt |
| POST | `/quiz/attempts/{attempt_id}/abandon` | Owner | Confirmed departure: the attempt becomes `abandoned` (answers kept, not graded, not a violation) |
| POST | `/quiz/submit` | Student | Grade an attempt (below) |

### `POST /quiz/submit`

```json
{
  "quiz_id": 3,
  "attempt_id": 41,
  "answers": { "11": "B", "12": "A" },
  "response_time": 42.0,
  "hints_used": 1,
  "monitoring_session_id": "ms_…"
}
```

- **The server grades the answers.** A score sent by the browser is ignored.
- Every question of the quiz must be answered exactly once (otherwise **422**).
- An open attempt from `/quiz/start` is required (`attempt_id`, or the
  student's open attempt at that quiz). **409** if the attempt has ended,
  is waiting for a return to be confirmed (`away`) or is `unverified`;
  `detail.attempt` then holds the server's view.
- `monitoring_session_id` must be the student's own session that has not
  ended. The camera measurements are taken by the server from that
  session's agent telemetry; camera values sent by the browser are ignored.
  They are `null` when nothing was measured, never guessed.
- Response `data`:
  - `progress`: the stored attempt;
  - `grading`: `score`, `correct_count`, `total_questions` and per-question
    `results`, including the correct answer and explanation (revealed only
    after submission);
  - `recommendation` (or `null`) and `recommendation_status`
    (`available` or `telemetry_unavailable`);
  - `attempt`: now `submitted`.

### Attempt status (tab-switch rule)

The server decides everything; [SESSION_INTEGRITY.md](SESSION_INTEGRITY.md)
explains the rules in full.

| Status | Meaning |
|---|---|
| `in_progress` | Being answered |
| `away` | The quiz page was hidden; a 10-second grace period is running |
| `submitted` | Graded |
| `terminated` | Ended by the rule (`end_reason` `grace_expired` or `second_tab_switch`). Not graded |
| `unverified` | No report arrived after the grace period. Locked, but not a violation |
| `abandoned` | Left the quiz (`left_quiz`), no contact (`no_contact`) or an absence that could not be measured (`unverified_no_measurement`). Not graded, not a violation |

A return within 10 seconds sets `strikes: 1` and a warning. A confirmed
reload (`pagehide`, then `resume` with `reload: true` from the reloaded
page) is a tab-switch incident like any other; a cancelled reload sends
nothing. Terminated and abandoned attempts never create a `progress` row,
so they count nowhere: not in completion, averages, analytics,
recommendations or rewards.

## Session integrity

| Method | Path | Access | Notes |
|---|---|---|---|
| GET | `/integrity/report` | Student | `?limit=1..50` (default 20). The signed-in student's own factual activity summary: `totals`, per-attempt `incidents` (time away as measured by the browser, outcome), `unverified_periods`, `multiple_face_episodes` and `notes`. No score or probability |

## Camera monitoring

Lessons and quizzes require a verified monitoring session. The camera agent
([facial_analysis/README.md](../facial_analysis/README.md)) listens on
`http://127.0.0.1:8765`; the browser hands it a pairing token, and the
agent then talks to these endpoints itself.

| Method | Path | Access | Notes |
|---|---|---|---|
| GET | `/monitoring/consent` | Student | `{required_version, is_minor, valid, consent}` |
| POST | `/monitoring/consent` | Student | `{accept: true, guardian_authorization_confirmed, school_authorization_confirmed}`. Both confirmations are required when the student is under 18 |
| DELETE | `/monitoring/consent` | Student | Withdraw consent; open sessions end |
| POST | `/monitoring/sessions` | Student | `{lesson_id}` → `{session_id, pairing_token, …}`. **403** without valid consent. Ends the student's other open sessions |
| POST | `/monitoring/sessions/{session_id}/pairing` | Owner | Reconnect: a new single-use pairing token; the old agent token is revoked |
| GET | `/monitoring/sessions/{session_id}` | Owner | `{state, verified, camera_error, lighting_ok, multiple_faces, …}`. Polling it also keeps the session alive |
| POST | `/monitoring/sessions/{session_id}/end` | Owner | End the session (the agent releases the webcam) |
| POST | `/monitoring/sessions/{session_id}/claim` | Agent | `{pairing_token}` → `{agent_token, heartbeat_interval}`. The pairing token is single use and valid for 2 minutes |
| POST | `/monitoring/heartbeat` | Agent | About once per second: `{sequence, captured_at, camera_ok, face_detected, face_stable, attention_score, yawning, looking_away, possible_drowsiness, face_count, multiple_faces, …}`. A sustained `multiple_faces` signal opens and closes a `session_events` episode |
| POST | `/monitoring/agent/end` | Agent | The agent is shutting down; the session waits for it to reconnect |

`state` is one of `awaiting_agent`, `stale` (no heartbeat within 5
seconds), `camera_unavailable`, `no_face`, `verifying`, `verified` or
`ended`. Only `verified` permits learning. A session the browser stops
polling for 60 seconds is ended automatically.

Tokens are never put in URLs and never logged; only their SHA-256 hashes
are stored. The agent never sends a student id: the backend derives the
student from the token. Out-of-order heartbeats (**409**) and measurements
captured more than 3 seconds earlier are rejected as not live. The consent
version is `2026-11-v2`; students who accepted an older version are asked
again.

## Facial-analysis telemetry (read only)

| Method | Path | Access | Notes |
|---|---|---|---|
| GET | `/attention/{student_id}` | Owner | Live view: `{available, status, age_seconds, attention_score, possible_drowsiness, …, session_average_attention}` |
| POST | `/attention/{student_id}/reset` | Owner | Start a new per-quiz measurement window |

`status` is `live`, `no_face`, `camera_unavailable`, `stale` or `no_data`.
When it is not `live`, the measurements are `null`.

## Student progress

| Method | Path | Access | Notes |
|---|---|---|---|
| GET | `/progress/{student_id}` | Owner | All graded attempts, oldest first |
| GET | `/progress/{student_id}/{lesson_id}` | Owner | The latest attempt for a lesson |
| PUT | `/progress/{progress_id}` | Teacher/admin | Correct an attempt. Students cannot edit attempts: scores are graded by the server and camera values come from the agent |

## Learning analytics

| Method | Path | Access | Notes |
|---|---|---|---|
| GET | `/analytics/summary` | Student | The signed-in student's own analytics: `student`, `overview`, `subjects`, `topics`, `topic_status_counts`, `trend`, `attention`, `activity`, `milestones` and `definitions`. There is no student-id parameter, so no cross-student access. Every calculation is defined in [ANALYTICS.md](ANALYTICS.md) |

## Recommendations (Q-learning)

| Method | Path | Access | Notes |
|---|---|---|---|
| GET | `/recommendations/latest` | Student | `{status, recommendation, next_step, attempt}`. `status` is `available`, `telemetry_unavailable`, `not_generated` or `no_attempts`; `attempt` includes `subject`, `grade` and `curriculum_topic` |
| GET | `/recommendations` | Student | `?limit=1..200` (default 20). The student's recommendations, newest first, each with `context` (lesson, subject, topic and score of the attempt that produced it) and `outcome` (`{status: "pending"}` until the next quiz; then that quiz's score, `score_change`, `followed` (true, false or null when not observable) and `reward`) |
| POST | `/rl/recommend` | Student | A stateless recommendation for a supplied state: `subject`, `topic`, `lesson`, `previous_quiz_score`, `current_quiz_score`, `attention_score`, `yawning`, `looking_away`, `difficulty`, `response_time`, `hints_used`, `lesson_attempts`, `completed_lessons` and optional `drowsy`. Returns `{action, confidence, confidence_kind, explanation, policy, model_version, state_key, q_values, runner_up, margin, blocked_actions, untested_actions, state_visits, telemetry_available}`. `action` is `null` when any camera field is `null` |
| GET | `/rl/model` | Student | The loaded Q-table: `model_version`, `trained_at`, `states_learned`, `state_key_version` (3), `training: "offline_simulation"` and `online_updates: false` |

Recommendations are generated **by the server when a quiz is graded**, from
the stored attempt, and saved to `recommendation_history` with the model
version and the decision detail. When the student's next attempt is graded,
the observed reward (reward version 2, the same formula as in training) is
recorded in `reward_history` with `followed` and `reward_detail`.

`policy` is `q_learning` (the learned Q-table chose among the permitted
actions), `q_learning_nearest_state` (the exact state was not learned; the
most similar learned state was used) or `fallback` (nothing learned
applies; `REPEAT_LESSON` with confidence 0). Older rows may say `rules`.
`confidence` is a heuristic decision strength, **not a probability**.
Safety constraints only remove unsuitable actions; they never choose one.
The running backend never changes the Q-table. Details:
[RL_ENGINE.md](RL_ENGINE.md).
