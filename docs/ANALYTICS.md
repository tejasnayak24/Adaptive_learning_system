# Dashboard and analytics (Phase 6)

The Dashboard, Progress & Analytics and AI Coach pages show only the
signed-in student's own saved records. Nothing is hard-coded, sampled or
estimated in the browser.

## Data sources

| Source | What it holds | Used for |
|---|---|---|
| `progress` | One row per graded quiz attempt: score, difficulty, mode, time, hints, and the camera measurements taken during that attempt | Every score, completion, trend, activity and attention figure |
| `lessons`, `curriculum_units`, `curriculum_topics` | The grade → subject → unit → topic → lesson hierarchy | Subject and topic grouping, lesson totals |
| `recommendation_history` | Each Q-learning recommendation, with the state, policy and model version behind it | AI Coach (latest advice and history) |
| `reward_history` | The observed outcome of a recommendation once the next quiz is graded | AI Coach outcome column |

No new tables or migrations were needed. The analytics are computed when
the page is requested:

- **Database aggregation:** `COUNT`, `SUM`, `MAX` grouped by lesson, plus
  `AVG` and `COUNT(column)` for attention, which skip NULLs.
- **One query for the ordered attempts:** used for the trend, the activity
  feed and topic status.

Endpoints: `GET /analytics/summary`, `GET /recommendations`,
`GET /recommendations/latest`. All require sign-in and use the caller's id
from the token.

## Definitions

| Metric | Calculation |
|---|---|
| **Lesson completed** | At least one quiz of the lesson scored **≥ 50%**, the same pass mark the RL safety rules use before allowing *Next lesson*. `progress.completed` is **not** used, because it is set on every submitted quiz and only means "quiz finished". |
| Lessons started | Lessons with at least one attempt. |
| Curriculum completion | Completed lessons in the student's grade ÷ lessons in that grade. |
| Quiz attempts | All of the student's attempts, every grade and mode. |
| Average quiz score / accuracy | Mean score of all attempts. Shown as "—" when there are none, never 0%. |
| Subject progress | Completed lessons in the subject ÷ lessons in the subject (student's grade only). The subject average uses every attempt in that subject. |
| Topic status | Uses the last 3 attempts in the topic. **Not started:** no attempts. **Not enough attempts:** only one attempt. **Strong:** recent average ≥ 80% and the latest attempt passed. **Weak:** recent average < 50%. **Needs revision:** everything in between, including a high average with a failed latest attempt. A topic with no attempts is never marked weak. |
| Quiz trend | Every attempt in order; the browser filters it by subject and by date range. Attempts with no recorded date are kept only when no date filter is set. |
| Trend summary | Mean of the last 3 attempts compared with the first 3. Needs at least 6 attempts. |
| Learning activity over time | Attempts per week (weeks start on Monday). Weeks with no attempts show as 0. |
| Days active, streak | Distinct UTC days with at least one quiz. The current streak counts back from today, or from yesterday if there is no quiz today. |
| Activity feed | Quiz attempts, first passes of a lesson ("completed"), and subjects where every lesson is passed. |
| Milestones | First quiz; 1/5/10/25/50/100 lessons completed; first score ≥ 80%; first 100%; each completed subject. Each is dated by the attempt that earned it. |

## Camera (facial-analysis) analytics: limitations

- **Per quiz, not continuous.** The camera agent sends heartbeats during a
  quiz, but the server keeps only the attempt's averages: the attention
  average, and whether yawning, looking away or drowsiness was seen at all.
  Live heartbeats are held in memory and are not stored. The page says this
  next to the figures.
- **Missing is not low.** `attention_score IS NULL` means there was no
  valid measurement, and it is left out of every average. Attempts fall
  into three groups:
  - **Camera measured:** an attention value was stored.
  - **Camera data unavailable:** a monitoring session existed, but no
    valid live reading arrived. The camera was off, no face was found, or
    the readings were stale (captured more than the allowed age before
    they reached the server).
  - **Not monitored:** the attempt predates camera monitoring.
- **Observations** are reported as "seen in X of Y measured quizzes". Y
  counts only quizzes with a measurement.
- **Insufficient history:** with fewer than 3 measured quizzes the page
  says the trend is not yet meaningful. The attention line chart appears
  only once at least 2 quizzes have a measurement.

## AI Coach integration

- **Where advice comes from.** Recommendations are produced on the server
  by the Phase 4 Q-learning policy when a quiz is graded. The Q-table was
  trained offline on simulated students and is not updated online. The
  frontend only displays the stored recommendation and turns its action
  into a link. It has no recommendation rules of its own.
- **What the page shows:**
  - the action, its plain-language meaning, and the policy's explanation;
  - the subject, topic, lesson, score, level and attention of the attempt
    that produced the advice;
  - the decision strength, which is not a probability, and the runner-up
    action;
  - a link to the next step.
- **Next step.** The link stays within the student's grade and subject,
  using the lesson's curriculum navigation. All 11 actions are handled.
- **History and outcomes.** Each recommendation shows "Waiting for your
  next quiz" until the next attempt is graded. After that it shows that
  attempt's score and change. "Followed" is inferred from the next attempt
  where the quiz records allow it. For example, *Increase difficulty* is
  followed if the next quiz is harder on the same lesson. For actions like
  *Focus-recovery break* it is left unknown.
- **No camera, no advice.** When the latest quiz had no valid camera
  reading, no recommendation is generated and the page explains why.

## Browser acceptance checklist

These checks have **not** been performed in a browser yet. The API and the
unit-tested helper functions are verified (see the Phase 6 commit).

Start PostgreSQL, the backend (`README.md` §2) and the frontend
(`npm run dev`). Then:

1. **New account.** Register without a grade.
   - The grade picker appears. Choose Grade 7.
   - The Dashboard shows 0/24 lessons, 0 quizzes, average score "—",
     4 subjects and "No quizzes yet".
   - The AI Coach card says "No advice yet".
   - There are no charts with fake data.
2. **Progress page with no quizzes.**
   - Only the overview tiles and "No analytics yet" are shown, with a
     *Start your first lesson* link.
3. **Take a quiz with the camera agent running**, then open the
   Dashboard.
   - The "Latest activity" card shows the lesson, score, ✓/✗ and
     *Camera measured*.
   - The quiz count is 1 and the coach card shows an action with its
     subject and topic.
4. **Progress page after a few quizzes.**
   - The score chart shows the dashed pass line, and its tooltip shows the
     lesson, subject, level and date.
   - The subject and date filters change the points. *Clear* resets them.
   - A filter that matches nothing shows "No quizzes match these filters".
   - Subject cards show only your grade's subjects, in fixed colours.
   - Clicking a subject card opens My Learning on that subject.
   - Topic groups show a status label and icon, not colour alone.
   - Untried topics say *Not started*, and a topic with one quiz says *Not
     enough attempts*.
   - The *Revise* / *Continue* buttons open the right lesson.
5. **Camera section.**
   - Close the camera agent mid-quiz (or block the camera) and submit.
   - The attempt log shows *Camera data unavailable*, and the attention
     average does not drop.
   - The section warns about limited history while fewer than 3 quizzes
     were measured.
6. **AI Coach page.**
   - It shows the action, a plain explanation, the "Based on your quiz"
     panel and a next-step button that opens the right lesson or quiz.
   - The history lists earlier advice. The newest says "Waiting for your
     next quiz" and older items show the score change.
   - The 11-step guide shows a description for every step and highlights
     the current one.
7. **Errors.**
   - Stop the backend and reload the Dashboard and Progress pages. A clear
     error with *Try again* appears, not a blank page.
8. **Layouts.**
   - At about 1366×768, tiles sit in rows of 4–5 and the charts are
     readable.
   - At about 375 px wide, everything stacks into one column, the attempt
     table scrolls sideways inside its card, and the page itself has no
     horizontal scroll.
9. **Navigation.**
   - Dashboard *Full analytics →* opens Progress.
   - *All activity →* scrolls to Recent activity.
   - Activity items open their lesson.
