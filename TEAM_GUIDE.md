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

These API names are fixed.

## Authentication

POST /login

POST /register

---

## Lessons

GET /lessons

GET /lesson/{id}

---

## Quiz

POST /quiz/start

POST /quiz/submit

---

## RL Recommendation

POST /recommend

Returns

- Recommended Content
- Difficulty
- Next Action

---

## Facial Analysis

POST /attention

Returns

- Attention Score
- Looking At Screen
- Head Direction

---

## Student Progress

GET /progress

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