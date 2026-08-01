# 🎓 Adaptive Learning System using Reinforcement Learning

> An Intelligent Adaptive Learning Platform that personalizes learning content using Reinforcement Learning and Facial Attention Analysis.

---

# 📖 Overview

Traditional e-learning platforms provide the same learning path to every student regardless of their understanding, learning speed, or attention level.

Our project builds an intelligent adaptive learning platform that continuously analyzes student performance and engagement to recommend the most suitable learning content.

The system combines:

- Reinforcement Learning
- Facial Attention Analysis
- Quiz Performance
- Student Progress Tracking
- AI-driven Content Recommendation

The objective is to create a personalized learning experience for every student.

---

# 🎯 Objectives

- Personalize learning for every student
- Adapt content difficulty automatically
- Detect student attention using computer vision
- Improve learning outcomes using Reinforcement Learning
- Provide teachers with learning analytics

---

# 👨‍💻 Team Members

| Name | Responsibility |
|------|----------------|
| Tejas Nayak | Team Lead • Reinforcement Learning • Integration |
| Rohan | Facial Analysis Module |
| Roshwin | Frontend Development |
| Rishika | Backend Development |

---

# 🛠 Tech Stack

## Frontend

- React
- Tailwind CSS
- Axios
- React Router

---

## Backend

- FastAPI
- Python

---

## Database

- PostgreSQL

---

## AI / Machine Learning

- OpenCV
- MediaPipe
- Reinforcement Learning (Q-Learning initially)

---

## Tools

- Git
- GitHub
- VS Code
- Postman

---

# 📂 Project Structure

```
adaptive-learning-system/

README.md

TEAM/
PROMPTS/

frontend/
backend/
rl_engine/
facial_analysis/
```

---

# 🏗 System Architecture

```
                Student

                    │

                    ▼

             React Frontend

                    │

                    ▼

              FastAPI Backend

        ┌───────────┼───────────┐

        ▼           ▼           ▼

Database      RL Engine     Facial Analysis

        │           │

        └──────► Recommendation
```

---

# 🧠 Project Modules

## 1. Frontend

Responsible for

- Login
- Dashboard
- Lessons
- Quiz
- Progress
- Reports

---

## 2. Backend

Responsible for

- Authentication
- Database
- APIs
- Student Management
- Quiz Management

---

## 3. Reinforcement Learning

Responsible for

- Student State
- Reward Calculation
- Action Selection
- Difficulty Recommendation

---

## 4. Facial Analysis

Responsible for

- Face Detection
- Attention Detection
- Head Pose
- Eye Tracking

---

# 🔄 Data Flow

Student

↓

Frontend

↓

Backend

↓

RL Engine

↓

Recommendation

↓

Frontend

↓

Student

Facial Analysis continuously updates attention score.

---

# 🔗 API Contracts

These APIs are fixed.

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

## Reinforcement Learning

POST /recommend

Input

- Student ID
- Current Topic
- Accuracy
- Attention Score
- Difficulty
- Response Time

Output

- Recommended Content
- Difficulty Level
- Suggested Action

---

## Facial Analysis

POST /attention

Output

- Attention Score
- Looking At Screen
- Head Direction

---

## Progress

GET /progress

---

# 🗄 Database Tables

Student

Lesson

Quiz

Question

Progress

Learning Session

Reward History

---

# 🌿 Git Workflow

Every member works only on their own branch.

Example

Tejas

tejas/rl-engine

Rohan

rohan/facial-analysis

Roshwin

roshwin/frontend

Rishika

rishika/backend

Nobody commits directly to **main**.

Workflow

1. Pull latest changes

2. Work on your branch

3. Commit

4. Push

5. Inform Team Lead

6. Team Lead reviews

7. Merge into main

---

# 📋 Coding Rules

- Write clean and readable code
- Comment important logic
- Never modify another member's folder
- Keep commits meaningful
- Test before pushing
- Ask before changing shared APIs

---

# 📅 Development Roadmap

Phase 1

- Repository Setup
- Project Structure
- Documentation

Phase 2

- Backend
- Frontend
- Facial Analysis
- RL Module

Phase 3

- Integration

Phase 4

- Testing

Phase 5

- Final Demo

---

# 🚀 Setup

Clone Repository

git clone <repository-url>

Create your branch

git checkout -b your-name/module

Start Development

Commit regularly

Push your branch

Inform Team Lead

---

# 📌 Important Rules

✅ Work only in your assigned module.

✅ Never push directly to main.

✅ Do not modify another teammate's code without discussion.

✅ Follow API contracts.

✅ Commit regularly.

---

Developed as a Major Project by the Department of Information Science & Engineering.