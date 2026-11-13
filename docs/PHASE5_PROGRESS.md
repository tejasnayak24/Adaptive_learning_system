# Phase 5 progress checkpoint

Branch: `final/project-completion` (never `main`).

## Milestones

| Milestone | Status | Commit |
|---|---|---|
| A. Curriculum architecture and grade support | Done | `ccc0a01` |
| B. Curriculum content (20 grade-subject files) | Done; imported into live DB | 571827c |
| C. Quiz and practice integration (hints, explanations, modes) | Backend partly done in A; UI pending | — |
| D. Frontend curriculum experience | Pending | — |
| E. Curriculum and RL integration | Pending | — |

## Content files (`backend/curriculum/content/`)

Validate with `python backend/scripts/check_curriculum_file.py backend/curriculum/content/*.json`.

| Grade | Mathematics | Science | Social Science | English |
|---|---|---|---|---|
| 6 | ✅ | ✅ | ✅ | ✅ |
| 7 | ✅ | ✅ | ✅ | ✅ |
| 8 | ✅ | ✅ | ✅ | ✅ |
| 9 | ✅ | ✅ (adopts 3 original lessons) | ✅ | ✅ |
| 10 | ✅ | ✅ (adopts 2 original lessons) | ✅ | ✅ |

Each file: ≥ 3 topics × 2 lessons, full material, Easy/Medium/Hard quizzes
(4 questions each, hint + explanation, balanced answer key).

## Planned syllabus for remaining files

- G7 Social Science: Medieval India (Delhi Sultanate, Mughal Empire); Our Environment (Components; Air and Water); Democracy and Equality (Equality; State Government).
- G7 English: Verbs and Tenses (Present/Past; Continuous/Perfect); Words in Context (Prefixes/Suffixes; Context clues); Letters and Notices (Informal letter; Notice).
- G8 Maths: Exponents and Squares; Algebraic Expressions and Identities; Mensuration.
- G8 Science: Microorganisms; Metals and Non-metals; Force and Pressure.
- G8 Social Science: Colonialism and National Movement; Resources; Constitution and Parliament.
- G8 English: Voice and Modals; Comprehension (Inference; Fact/Opinion); Formal Writing (Formal letter; Report).
- G9 Maths: Polynomials; Coordinate Geometry and Linear Equations; Triangles (Congruence; Heron's formula).
- G9 Science: Motion and Force (new "Describing Motion" + original "Force and Motion"); Matter (original "Matter and Its Properties" + new "Atoms and Molecules"); The Cell (original "Cell Biology" + new "Tissues"). Original lessons use `legacy_title` + `legacy_notes` (hints/explanations for their existing questions, answers unchanged).
- G9 Social Science: French Revolution; India: Location and Climate; Democracy and Elections.
- G9 English: Reported Speech and Agreement; Poetry; Descriptive and Story Writing.
- G10 Maths: Quadratic Equations; Arithmetic Progressions; Trigonometry.
- G10 Science: Life Processes (original "Human Body Systems" + Control and Coordination); Our Environment (original "Ecosystems" + Managing Natural Resources); Chemical Reactions (2 new); Electricity (2 new).
- G10 Social Science: Nationalism in India; Federalism; Development and Sectors of the Economy.
- G10 English: Conditionals and Clauses; Analytical Reading; Persuasive Writing.

## Exact next task

Milestone B is complete: 20 files, 122 lessons (117 new + 5 original Science),
1,404 new questions plus hints/explanations for the 75 original ones. Imported into
the live DB on 2026-11-13 after backup `backups/aegis_pre_phase5_import_*.dump`
(rehearsed on aegis_test; second run created nothing; progress and original
questions byte-identical).

Next: milestone C (quiz UI: hints from the database, explanations in the answer
review, practice/hints/challenge modes recorded via `mode`, challenge timer),
then D (curriculum browser by grade/subject/unit/topic, lesson material pages with
diagrams, worked examples, practice and navigation), then E (RL next-step resolver
using `navigation`, simulator curriculum aligned with content files).
