# Phase 7 progress (final testing and delivery)

Branch: `final/project-completion` (never `main`). Phase 6 commit: `5060646`.

## Done

- Backup of the live database: `backups/aegis_pre_phase7_20261113_215937.dump`.
  All live testing used the isolated copy `aegis_phase7`. The live database
  was only read.
- Browser journey: headless Chrome with the real camera-agent code and a
  synthetic camera. Results: journey 38/38, extra checks 9/9, production
  build 7/7. See [BROWSER_ACCEPTANCE.md](BROWSER_ACCEPTANCE.md).
- Live API regression on the copy: 34/34. It covered:
  - 20 grade-subject combinations;
  - 366 quizzes, none leaking answers;
  - camera-agent authentication and stale telemetry;
  - ownership.

  Phase 5 and Phase 6 live checks were rerun on the copy: 11/11 and 23/23.
- Migrations: `alembic check` clean on a fresh database and on the copy.
  Curriculum validator: 20 files, 122 lessons valid.
- Fixes:
  - false "Webcam unavailable" flash at camera start;
  - a lesson from another grade is refused before the camera starts (also
    enforced by the server for monitoring sessions);
  - registration success message shown on sign-in;
  - results-page wording;
  - students can no longer edit their own quiz attempts (teachers and
    admins only);
  - registration validation (password 8–72 characters, name, age);
  - backend refuses the placeholder `SECRET_KEY`;
  - dev server bound to 127.0.0.1;
  - `.gitignore` safety net;
  - sidebar no longer remounts on every render.
- Frontend:
  - route-level code splitting; the initial download fell from 796 kB to
    about 312 kB;
  - ESLint config; `eslint .` is clean.
- `start-all.ps1` / `stop-all.ps1`: written and tested for real.
- Docs:
  - README (setup from scratch, start scripts, tests, docs index);
  - [ARCHITECTURE.md](ARCHITECTURE.md);
  - [DEMO.md](DEMO.md);
  - [TROUBLESHOOTING.md](TROUBLESHOOTING.md);
  - [BROWSER_ACCEPTANCE.md](BROWSER_ACCEPTANCE.md);
  - `backend/.env.example`;
  - TEAM_GUIDE API updates.

## Commits

- `0aafa45`: Phase 7A (fixes, security, scripts, docs).
- Phase 7B: README update (this commit).

## Remaining

- Final pull request `final/project-completion` → `main`. It is opened for
  review and **not merged**.

## Needs the team lead (physical testing)

- Real-webcam checklist: [WEBCAM_ACCEPTANCE_CHECKLIST.md](WEBCAM_ACCEPTANCE_CHECKLIST.md).
- Visual pass: [BROWSER_ACCEPTANCE.md §2](BROWSER_ACCEPTANCE.md).
- Rehearse the demonstration: [DEMO.md](DEMO.md).
