# Aegis reinforcement-learning engine

This document describes the recommendation engine as implemented on branch
`final/project-completion` (Phase 4). Every number below is taken from the
code or from the metadata of the shipped Q-table
(`rl_engine/q_table.json`, trained 2026-11-12, seed 2026).

| Item | Where |
|---|---|
| State encoding | `rl_engine/core/state_encoding.py` |
| Actions | `rl_engine/core/actions.py` |
| Safety constraints | `rl_engine/core/constraints.py` |
| Reward | `rl_engine/training/rewards.py` |
| Agent (training + runtime decision) | `rl_engine/training/agent.py` |
| Simulator | `rl_engine/training/simulation.py`, `environment.py` |
| Training entry point | `rl_engine/train.py` (`python -m rl_engine.train`) |
| Evaluation / baselines | `rl_engine/evaluation/` |
| Backend integration | `backend/app/services/rl_service.py`, `recommendation_service.py` |

---

## 1. What reinforcement learning does in Aegis

After every graded quiz, Aegis recommends one of 11 next steps (repeat the
lesson, raise difficulty, take a break, …). Choosing a teaching action is a
sequential decision problem: an action changes the student's next state
(knowledge, attention, fatigue), and its value only shows up over several
future quizzes. Aegis models this as a Markov decision process and learns a
policy with **tabular Q-learning**.

* **Training is offline**, on simulated students (section 9). The learned
  table `Q(s, a)` estimates the long-term (discounted) reward of taking action
  `a` in observable state `s`.
* **At runtime** the backend builds the student's real state from the
  database and the camera agent, removes unsuitable actions (safety
  constraints) and recommends the permitted action with the highest learned
  Q-value. The running system **does not update the Q-table** (no online
  learning).
* Real outcomes are recorded in `reward_history` with the same reward formula
  used in training, so the deployed policy can be evaluated on real students
  and the data can feed a future offline retraining.

Before Phase 4, `QLearningAgent._policy_action()` returned a hand-written
rule for *every* state, so the Q-table never influenced a recommendation.
That rule set is kept only as an evaluation baseline
(`rl_engine/evaluation/baselines.py::legacy_rule_policy`).

## 2. State representation (state-key version 3)

The backend supplies a full `StudentState` (`rl_engine/models/student_state.py`).
The agent discretises it into an 8-feature key:

| # | Feature | Values | Source |
|---|---|---|---|
| 0 | `score_level` | 0: < 50 %, 1: 50–79 %, 2: ≥ 80 % | current quiz score (graded on the server) |
| 1 | `attention_level` | 0: < 0.40, 1: 0.40–0.59, 2: ≥ 0.60 | mean camera attention during the attempt |
| 2 | `difficulty` | 0 EASY, 1 MEDIUM, 2 HARD | quiz difficulty |
| 3 | `many_hints` | 1 if hints ≥ 2 | hints used in the attempt |
| 4 | `many_attempts` | 1 if attempts ≥ 3 | attempts on this lesson |
| 5 | `fatigue` | 0 none, 1 yawning, 2 possible drowsiness | camera agent (drowsiness dominates) |
| 6 | `looking_away` | 1 if sustained looking away (≥ 2 s) | camera agent |
| 7 | `trend` | 0 declining (≤ −5 points), 1 steady, 2 improving (≥ +5) | current − previous score on this lesson |

State space: 3·3·3·2·2·3·2·3 = **1944 states**. The shipped table has learned
1571 of them (80.8 %).

Design decisions:

* **Drowsiness** (new from the Phase 3 camera agent) is merged with yawning
  into one ordered *fatigue* feature. Both describe tiredness, and possible
  drowsiness (sustained eye closure) is the stronger signal. Two separate
  booleans would double the table for a combination that needs the same
  response.
* **Previous quiz score** enters as the 3-level `trend`. An improving and a
  declining student at the same score need different help.
* **Response time is not encoded.** It depends on the number of questions and
  on reading speed, and largely duplicates the score. A 3-level feature would
  triple the table to 5832 states.
* Subject, topic, lesson and completed-lesson count are not encoded, so the
  policy generalises across curriculum content.

Version 2 (432 states, 7 features, no drowsiness or trend) is **refused by
the loader**: `load_q_table` checks `state_key_version`, the feature list, the
action list, every key's range and that every state has a value for all 11
actions. The old table is archived at `rl_engine/archive/q_table_v2.json`.

## 3. Actions

Indices are fixed in `Action` (`rl_engine/core/actions.py`):

| # | Action | What the website does |
|---|---|---|
| 0 | `NEXT_LESSON` | Opens the next lesson |
| 1 | `REPEAT_LESSON` | Re-opens the lesson with study guidance |
| 2 | `INCREASE_DIFFICULTY` | Opens the next harder quiz of the lesson |
| 3 | `DECREASE_DIFFICULTY` | Opens the next easier quiz |
| 4 | `PRACTICE_QUIZ` | Restarts the same quiz as a practice attempt |
| 5 | `QUICK_CHALLENGE` | Restarts the quiz as a timed challenge |
| 6 | `SHOW_WORKED_EXAMPLE` | Scrolls to the answer review (correct answer beside each answer) |
| 7 | `PROVIDE_HINT` | Restarts the quiz, prompting use of hints |
| 8 | `FOCUS_RECOVERY` | Shows a 60-second guided break |
| 9 | `SHOW_REAL_WORLD_APPLICATION` | Re-opens the lesson with a real-world prompt |
| 10 | `SKIP_TO_ADVANCED_TOPIC` | Opens the lesson two ahead |

The mapping lives in `frontend/src/utils/recommendationActions.js`. A test
checks that all 11 actions resolve to a specific step; unknown actions are
shown explicitly, never as a generic button.

### Safety constraints (filter only)

`core/constraints.py` removes unsuitable actions **before** Q-values are
compared, during training and at runtime alike:

| Blocked action | When |
|---|---|
| `INCREASE_DIFFICULTY` | already HARD; or score < 50 %; or possible drowsiness |
| `DECREASE_DIFFICULTY` | already EASY; or score ≥ 80 % |
| `NEXT_LESSON` | score < 50 % (lesson not passed) |
| `SKIP_TO_ADVANCED_TOPIC` | score < 90 %; or possible drowsiness |
| `QUICK_CHALLENGE` | possible drowsiness |

Six actions are never blocked (`REPEAT_LESSON`, `PRACTICE_QUIZ`,
`SHOW_WORKED_EXAMPLE`, `PROVIDE_HINT`, `FOCUS_RECOVERY`,
`SHOW_REAL_WORLD_APPLICATION`). At least six candidates therefore always
remain, and the choice among them is always made by the Q-table.

## 4. Reward and penalty mechanism (reward version 2)

The reward judges **what happened after** an action, using only quantities
that can be observed both in simulation and in real data (two consecutive
attempts). One reward unit is roughly a 10-point quiz improvement.

| Component | Value | Justification |
|---|---|---|
| Learning gain | +0.1 per point of *difficulty-adjusted* score change on the same lesson, clipped to ±3 | Improvement is the main goal. Adjusted score = score + 0 (EASY) / +10 (MEDIUM) / +20 (HARD), so moving up a level and scoring 10 points lower is neutral. The clip stops one lucky or unlucky quiz from dominating. |
| Lesson completion | per lesson advanced: +3 if mastered (adjusted ≥ 90, i.e. 90 % EASY / 80 % MEDIUM / 70 % HARD); otherwise −0.1 per point still missing to 90 | Finishing a lesson properly is worth a 30-point gain. Leaving with gaps charges the unlearned points at the same rate learning is rewarded, so abandoning a lesson for cheap early progress elsewhere does not pay. |
| Frustration | −1 if the new score < 40 % on MEDIUM/HARD | The content is too hard for the student right now. |
| Engagement change | +2 × Δattention (0–1 scale) | Rewards *recovery* of attention. A student with low but unchanged attention adds nothing, so low attention alone never makes an action bad. |
| Drowsiness | +1 if possible drowsiness is gone after the action, −1 while it persists | Makes a break worthwhile exactly when fatigue is observed. |
| Step cost | −0.5 per action | Study time is limited, so actions that teach nothing (e.g. repeated breaks for an alert student) have a net cost. |

Examples (from the tests):

| Situation | Reward |
|---|---|
| Same quiz 60 % → 80 % | +2.0 − 0.5 = **+1.5** |
| 80 % EASY → 70 % MEDIUM (harder, same adjusted level) | **−0.5** (step cost only) |
| Move on after 92 % on EASY | +3 − 0.5 = **+2.5** |
| Move on after 50 % on EASY | −4.0 − 0.5 = **−4.5** |
| Break when possibly drowsy, attention 0.3 → 0.6, drowsiness clears | +0.6 + 1 − 0.5 = **+1.1** |
| Break for an alert student (nothing changes) | **−0.5** |

Missing camera values (NULL) drop the engagement and drowsiness terms; nothing
is guessed.

## 5. Q-learning algorithm

Tabular, model-free, off-policy temporal-difference control:

```
initialise Q(s, a) = 0 for every state seen
for episode = 1 .. 20000:
    sample a new simulated student, observe s
    repeat up to 60 steps:
        P(s) = actions permitted by the safety constraints
        a = epsilon-greedy over P(s)
        apply a, simulated student takes the next quiz -> r, s'
        Q(s, a) <- Q(s, a) + alpha [ r + gamma * max_{a' in P(s')} Q(s', a') - Q(s, a) ]
        s <- s'; stop if the curriculum is finished
    epsilon <- max(epsilon * 0.9997, 0.05)
```

Visit counts `N(s, a)` are stored with the Q-values and used at runtime.

## 6. Update equation

```
Q(s,a) ← Q(s,a) + α · [ r + γ · max_{a′ ∈ P(s′)} Q(s′,a′) − Q(s,a) ]
```

* `r + γ·max Q(s′,·)` is the TD target; at a terminal state (curriculum
  finished) the target is just `r`.
* The max is taken **only over permitted actions** in `s′`, so learned values
  are values under the same constraints the system runs with.
* `test_q_learning_update_matches_the_equation` checks this numerically,
  including that a blocked action's value is ignored.

## 7. Learning rate and discount factor

| Parameter | Value | Reason |
|---|---|---|
| α (`learning_rate`) | 0.1 | Rewards are noisy (simulated quiz noise ~6 points). A small step averages over many outcomes. |
| γ (`discount_factor`) | 0.95 (0.9 before Phase 4) | One step = one recommendation + quiz, and a lesson takes ~5–15 steps. A horizon of ~1/(1−γ) = 20 steps lets the agent value finishing a lesson properly over short-term gains. With 0.9 the agent was measurably more short-sighted in experiments. |

## 8. Epsilon-greedy exploration and exploitation

* **Training:** with probability ε a random *permitted* action, otherwise
  the permitted action with the highest Q (ties broken at random).
  ε starts at 1.0 and is multiplied by 0.9997 after each episode, down to a
  floor of 0.05, which it reaches after ~10,000 episodes. The first half of
  training explores broadly; the second half refines the greedy policy.
* **Runtime:** **purely greedy, no exploration.** Real students are never
  experimented on. In addition, an action is only eligible if it was tried
  at least 5 times in training for that state (`min_action_visits`), so an
  untested action with an untouched value of 0 can never be recommended.

## 9. Training simulation

Each episode samples a `SimulatedStudent` with hidden traits:

| Trait | Range | Effect |
|---|---|---|
| ability | 0.6–1.4 | multiplies learning gains |
| focus | 0.35–0.95 | baseline attention |
| fatigue_rate | 0.01–0.07 per step | how fast the student tires |
| distractibility | 0–0.5 | chance of looking away |

Hidden state per step: mastery of the current lesson (0–1), fatigue (0–1)
and a short-lived attention boost. The agent only sees the observable state.

* **Quiz score** = 100 × (mastery − offset + 0.1 × (attention − 0.6) + noise),
  with offset −0.05 / +0.05 / +0.15 for EASY / MEDIUM / HARD and noise
  N(0, 0.06). Scores can go down as well as up.
* **Learning gain** = base(action, mastery band) × ability × effectiveness ×
  difficulty-fit × (1 − mastery) + N(0, 0.02).
  * Effectiveness is (0.35 + 0.65 × attention), halved when possibly drowsy.
  * The (1 − mastery) term gives diminishing returns.
* **Mastery bands** are < 0.4 / < 0.7 / ≥ 0.7. Base gains per band:
  * worked example 0.30 / 0.14 / 0.02 (helps novices most);
  * repeat lesson 0.18 / 0.20 / 0.06;
  * practice quiz 0.04 / 0.18 / 0.10 (helps once the idea is understood);
  * hint 0.08 / 0.12 / 0.03, halved after 2 hints.
* **Difficulty fit:** the ideal level is EASY below 0.45 mastery, MEDIUM
  below 0.75 and HARD above that. Gains are ×1.2 at the right level, ×0.6
  one level off and ×0.3 two levels off.
* **Fatigue** grows every step except breaks:
  * possible drowsiness appears with probability clip((fatigue − 0.45) × 1.6, 0, 0.9);
  * yawning with probability fatigue × 0.7;
  * `FOCUS_RECOVERY` cuts fatigue to 30% and clears drowsiness with probability 0.85.
* **Attention boosts** come from quick challenges (0.25), real-world
  applications (0.35) and breaks (0.20).
  * Each boost is scaled by the attention deficit and cut to 30% when the same action is repeated back-to-back.
  * Boosts halve every step and do not stack.
* **Advancing** starts the next lesson at EASY. Mastery restarts at
  0.25–0.45, plus 0.3 × (previous mastery − 0.7), so moving on with weak
  understanding makes the next lesson harder. Skipping two lessons uses a
  carry-over of 0.6 × (mastery − 0.85).

The curriculum has 12 lessons across Mathematics, Science (the five seeded
Science topics), Social Science and English. An episode ends when the
curriculum is finished or after 60 steps.

While designing the simulator, profiling the learned policy exposed three
exploits, which were fixed before shipping:

1. Attention boosts stacked, so the agent spammed real-world applications.
2. Mastery was judged on the raw score, so the agent kept everyone on EASY.
3. A flat penalty for advancing let the agent abandon lessons to harvest
   cheap gains elsewhere.

## 10. Q-table generation and loading

`python -m rl_engine.train` (about 45 s):

1. Trains 20,000 episodes with seed 2026 (reproducible: same seed gives the
   same table).
2. Writes `q_table.candidate.json`.
3. **Validates** on 1000 held-out simulated students (seeds from 900000,
   never used in training). The candidate must:
   * beat a random permitted-action policy;
   * be no worse than the legacy rules;
   * make zero constraint violations;
   * cover at least 50% of the states.
4. Only if every check passes, archives the current table to
   `rl_engine/archive/` and replaces `q_table.json`. Otherwise the live table
   is untouched and the command exits with status 1.

The JSON file stores the format name, `state_key_version` 3, the feature
list, the action list, `reward_version` 2, the training configuration, the
validation report, and per state the Q-values and visit counts. The backend
loads it once (`get_rl_service()`), identifies it as
`model_version = v3-<first 12 hex of SHA-256>` and reports this at
`GET /rl/model`.

## 11. How real student data reaches the RL engine

1. The student takes a quiz while the camera agent sends heartbeats once per
   second (Phase 3). Only numbers and yes/no signals are sent, no images.
2. `POST /quiz/submit`: the server grades the answers. It takes attention,
   yawning, looking away and possible drowsiness from the heartbeats of
   that monitoring session (`telemetry_service.attempt_metrics`), never
   from the browser.
3. `recommendation_service.build_state` assembles the state from the
   database:
   * the score, difficulty and hints of this attempt;
   * the previous score and the number of attempts on this lesson;
   * the count of completed lessons;
   * the camera values.
4. Without camera telemetry, no recommendation is generated
   (`telemetry_unavailable`).

## 12. How the final recommendation is selected

`QLearningAgent.decide(state)` (read-only):

1. Encode the state (version 3 key).
2. Remove blocked actions (section 3), keeping the reasons.
3. Keep permitted actions with ≥ 5 training visits in this state.
4. Choose the highest Q-value. Ties are broken by the fixed action index, so
   the choice is deterministic. `policy = "q_learning"`.
5. If the exact state was never learned, use the most-visited learned state
   that differs in exactly one feature (`policy = "q_learning_nearest_state"`,
   confidence halved).
6. If none exists, recommend `REPEAT_LESSON`, the lowest-risk action, with
   confidence 0 and an explanation saying the situation was not learned
   (`policy = "fallback"`).

**Confidence is a heuristic decision-strength indicator, not a calibrated
probability:**

```
confidence = (1 − e^(−margin / 1.0)) × min(1, N(s, a*) / 30)
```

* `margin` is the Q-value gap to the next-best eligible action.
* If only one action is eligible, the first factor is 0.5.
* The UI labels it "decision strength (not a probability)".

The explanation states the facts used and the next-best action, e.g. *"You
scored 20%, and possible drowsiness was observed; a short focus-recovery
break is suggested before continuing. Chosen by the learned Q-table as the
best of 5 suitable actions (next best: real-world application)."*

Each recommendation is stored in `recommendation_history` with:

* the full state and the state key;
* the policy path and the model version;
* `decision_detail`: Q-values of the eligible actions, blocked actions with
  reasons, untested actions, margin and visit counts.

## 13. How recommendation outcomes are evaluated

When the student's next attempt is graded,
`record_outcome_of_previous` closes the most recent open recommendation:

* `reward` is computed with the **same** `observed_reward` function as
  training, from the two real attempts. Moving to a different lesson counts as
  an advancement.
* `reward_version` = 2. The 3 rows recorded before Phase 4 are marked 1
  (old formula).
* `followed` is inferred where quiz records can show it:
  * advance: True if the lesson changed;
  * difficulty actions: True if the level moved in the right direction;
  * repeat, practice, worked example and hint: True if the same lesson was
    attempted;
  * break, real-world application and challenge: NULL (not observable).
* `reward_detail`: JSON of the components.

`python backend/scripts/rl_outcome_report.py` summarises the mean observed
reward per policy, action and reward version. `--export file.jsonl` writes
pseudonymised transitions for future offline analysis or retraining.
**These records do not update the deployed Q-table.** Retraining is a
deliberate offline step. Real outcomes are not yet used in training because
there are only a handful of them, and they come from a different policy
(off-policy data would need importance weighting or a model of real
students).

### Offline comparison with the previous rule policy

The validation run above uses 1000 held-out simulated students, the same
students for each policy:

| Metric | Learned Q-table | Legacy rules (pre-Phase 4) | Random permitted |
|---|---|---|---|
| Mean return (reward v2) | **−3.79** (sd 10.3) | −23.83 (sd 22.0) | −29.57 (sd 10.3) |
| Lessons completed in 60 steps | 3.41 | 1.53 | 4.16 |
| Advanced before passing (adj. < 70) | **0 %** | 0 % | 53 % |
| Mean score when advancing | 83.1 % | 83.4 % | 65.2 % |
| Mean difficulty when advancing (0 = EASY … 2 = HARD) | 0.97 | 2.00 | 0.44 |
| Steps ending with possible drowsiness | **4.8 %** | 14.9 % | 11.6 % |
| Hidden mastery of the last lesson reached | 0.63 | 0.74 | 0.52 |
| Safety-constraint violations | 0 | 51 | 0 |
| Actions used (> 1 % share) | 10 of 11 | 5 of 11 | 11 of 11 |

How to read this:

* The legacy rules repeat the lesson in 59% of steps whenever the score is
  below 70%. Their students reach high mastery on few lessons but progress
  slowly, and the rules ignore fatigue (51 times they raised difficulty for a
  possibly drowsy student).
* The random policy moves on early and often, so it covers many lessons
  with gaps.
* The learned policy keeps students moving at a mastery level. It raises
  difficulty when they are ready, sends tired students on breaks, and uses
  worked examples for low scores.

Same-state comparison on the shipped table (`decide` vs `legacy_rule_policy`):

| Student situation | Legacy rules | Learned policy (next best, decision strength) |
|---|---|---|
| 35 % EASY, 3rd attempt, 2 hints | REPEAT_LESSON | REPEAT_LESSON (quick challenge, 0.16) |
| 38 % MEDIUM, declining | REPEAT_LESSON | REPEAT_LESSON (real-world, 0.38) |
| 60 % EASY, improving | REPEAT_LESSON | **INCREASE_DIFFICULTY** (practice, 0.58) |
| 65 % MEDIUM, steady | REPEAT_LESSON | **SHOW_WORKED_EXAMPLE** (hint, 0.03) |
| 75 % EASY, looking away, attention 0.35 | FOCUS_RECOVERY | **SHOW_REAL_WORLD_APPLICATION** (practice, 0.00) |
| 85 % MEDIUM, attentive | INCREASE_DIFFICULTY | **NEXT_LESSON** (practice, 0.89) |
| 85 % MEDIUM, yawning | FOCUS_RECOVERY | **NEXT_LESSON** (mastered at that level) |
| 90 % EASY, possible drowsiness | INCREASE_DIFFICULTY | **FOCUS_RECOVERY** (nearest learned state) |
| 95 % HARD, attentive | NEXT_LESSON | NEXT_LESSON |

### Limitations (stated honestly)

* All learned values come from a **simulated** student model whose
  parameters are design assumptions, not fitted to real learners. The
  comparison shows the policy is better *in that model*. Whether it helps
  real students has to be measured with `reward_history` over time.
* Some decisions are near-ties (decision strength ≈ 0). One example is
  "85% on EASY → repeat the lesson rather than raise difficulty"
  (strength 0.46), because the simulator does not treat 85% on EASY as
  mastery.
* `followed` cannot be observed for breaks, real-world applications and
  challenges.
* No online learning: the deployed table changes only when
  `python -m rl_engine.train` is run and passes validation.

## Tests

| Suite | Command | Covers |
|---|---|---|
| RL engine (68) | `cd rl_engine; python -m pytest` | state encoding incl. drowsiness, rewards (positive and negative), constraints, update equation, exploration and exploitation, greedy read-only runtime, **Q-values change the decision**, all 11 actions selectable, unseen states, confidence, save/load, version refusal, simulator realism, training reproducibility, shipped policy beats legacy and random |
| Backend (64) | `cd backend; python -m pytest` | API decision driven by the loaded table (swapping tables changes the answer), blocked actions never returned, fallback, drowsiness in the state, `/rl/model`, stored decision detail, reward v2 and `followed` |
| Frontend (17) | `cd frontend; npm test` | every action maps to a specific next step, plus the monitoring state tests |
