import test from 'node:test'
import assert from 'node:assert/strict'

import {
  SUBJECT_COLORS,
  SUBJECT_ORDER,
  TOPIC_STATUS,
  TOPIC_STATUS_ORDER,
  activityText,
  attentionSummary,
  continueTarget,
  filterTrend,
  formatPercent,
  observationText,
  outcomeText,
  parseDate,
  trendDirection,
  trendRows,
  weeklyActivity
} from '../src/utils/analytics.js'

const point = (subject, at, score, extra = {}) => ({ subject, at, score, lesson_title: 'L', difficulty: 'EASY', ...extra })

const TREND = [
  point('Mathematics', '2026-10-01T09:00:00', 40),
  point('Science', '2026-10-05T09:00:00', 60),
  point('Mathematics', '2026-10-09T09:00:00', 80),
  point('Science', null, 70)
]

test('every subject has a fixed colour and order', () => {
  assert.deepEqual(Object.keys(SUBJECT_COLORS), SUBJECT_ORDER)
  assert.equal(new Set(Object.values(SUBJECT_COLORS)).size, 4)
})

test('topic statuses cover the backend classification and never colour-only', () => {
  assert.deepEqual([...TOPIC_STATUS_ORDER].sort(), ['insufficient_data', 'needs_revision', 'not_started', 'strong', 'weak'])
  for (const status of TOPIC_STATUS_ORDER) {
    assert.ok(TOPIC_STATUS[status].label && TOPIC_STATUS[status].icon && TOPIC_STATUS[status].help)
  }
  assert.doesNotMatch(TOPIC_STATUS.not_started.label, /weak/i)
  assert.doesNotMatch(TOPIC_STATUS.insufficient_data.label, /weak/i)
})

test('formatPercent keeps missing values missing', () => {
  assert.equal(formatPercent(72.4), '72%')
  assert.equal(formatPercent(0), '0%')
  assert.equal(formatPercent(null), '—')
  assert.equal(formatPercent(undefined, 'No quizzes'), 'No quizzes')
})

test('API timestamps are read as UTC', () => {
  assert.equal(parseDate('2026-10-01T09:00:00').toISOString(), '2026-10-01T09:00:00.000Z')
  assert.equal(parseDate(null), null)
  assert.equal(parseDate('not a date'), null)
})

test('trend filters by subject and date; undated points only without a date filter', () => {
  assert.equal(filterTrend(TREND).length, 4)
  assert.deepEqual(filterTrend(TREND, { subject: 'Mathematics' }).map((p) => p.score), [40, 80])
  assert.deepEqual(filterTrend(TREND, { subject: 'Science' }).map((p) => p.score), [60, 70])
  assert.deepEqual(filterTrend(TREND, { from: '2026-10-04' }).map((p) => p.score), [60, 80])
  assert.deepEqual(filterTrend(TREND, { to: '2026-10-05' }).map((p) => p.score), [40, 60])
  assert.deepEqual(filterTrend(TREND, { subject: 'Mathematics', from: '2026-10-02', to: '2026-10-31' }).map((p) => p.score), [80])
  assert.deepEqual(filterTrend([], { subject: 'English' }), [])
})

test('trend rows are numbered in order and keep null attention as null', () => {
  const rows = trendRows([point('Science', '2026-10-01T00:00:00', 50, { attention: null }), point('Science', '2026-10-02T00:00:00', 70, { attention: 81 })])
  assert.deepEqual(rows.map((r) => r.label), ['#1', '#2'])
  assert.equal(rows[0].attention, null)
  assert.equal(rows[1].attention, 81)
})

test('trend direction needs six attempts and compares first and last three', () => {
  assert.equal(trendDirection(TREND), null)
  const up = [30, 40, 50, 70, 80, 90].map((s) => ({ score: s }))
  assert.deepEqual(trendDirection(up), { first: 40, last: 80, change: 40, direction: 'up' })
  const flat = [60, 60, 60, 61, 60, 60].map((s) => ({ score: s }))
  assert.equal(trendDirection(flat).direction, 'flat')
  assert.equal(trendDirection([...up].reverse()).direction, 'down')
})

test('weekly activity fills empty weeks with zero and counts undated attempts separately', () => {
  const { weeks, undated } = weeklyActivity([
    point('Science', '2026-10-05T10:00:00', 1), // Monday
    point('Science', '2026-10-07T10:00:00', 1),
    point('Science', '2026-10-21T10:00:00', 1),
    point('Science', null, 1)
  ])
  assert.equal(undated, 1)
  assert.deepEqual(weeks.map((w) => w.attempts), [2, 0, 1])
  assert.equal(weeks[0].week, '2026-10-05')
  assert.deepEqual(weeklyActivity([]), { weeks: [], undated: 0 })
})

test('attention summary distinguishes no data, limited history and enough history', () => {
  assert.equal(attentionSummary(null).level, 'none')
  assert.equal(attentionSummary({ attempts_total: 0 }).level, 'none')
  const none = attentionSummary({ attempts_total: 4, measured_attempts: 0, sufficient_history: false })
  assert.equal(none.level, 'none')
  assert.match(none.message, /no attention average/)
  const limited = attentionSummary({ attempts_total: 4, measured_attempts: 1, sufficient_history: false, min_measured_attempts: 3 })
  assert.equal(limited.level, 'limited')
  assert.match(limited.message, /Only 1 quiz had/)
  assert.equal(attentionSummary({ attempts_total: 5, measured_attempts: 4, sufficient_history: true }).level, 'ok')
})

test('observations are stated out of measured quizzes only', () => {
  assert.equal(observationText({ observed_in: 2, measured_attempts: 5 }), '2 of 5 measured quizzes')
  assert.equal(observationText({ observed_in: 0, measured_attempts: 1 }), '0 of 1 measured quiz')
  assert.equal(observationText({ observed_in: 0, measured_attempts: 0 }), 'No camera data')
})

test('continue target prefers the most recently studied subject', () => {
  const summary = {
    overview: { latest_activity: { subject: 'Science' } },
    topics: [
      { subject: 'Mathematics', topic: 'Fractions', next_lesson: { lesson_id: 1, lesson_title: 'A' } },
      { subject: 'Science', topic: 'Cells', next_lesson: null },
      { subject: 'Science', topic: 'Forces', next_lesson: { lesson_id: 9, lesson_title: 'B' } }
    ]
  }
  assert.deepEqual(continueTarget(summary), { lesson_id: 9, lesson_title: 'B', topic: 'Forces', subject: 'Science' })
  assert.equal(continueTarget({ overview: {}, topics: [{ next_lesson: null }] }), null)
  assert.equal(continueTarget(null), null)
})

test('activity text for each event type', () => {
  assert.match(activityText({ type: 'quiz_attempt', passed: true, difficulty: 'HARD', score: 90, lesson_title: 'X', subject: 'Science' }).title, /Passed the hard quiz — 90%/)
  assert.match(activityText({ type: 'quiz_attempt', passed: false, difficulty: 'EASY', score: 20 }).title, /Tried/)
  assert.match(activityText({ type: 'lesson_completed', lesson_title: 'Cells' }).title, /Completed “Cells”/)
  assert.match(activityText({ type: 'subject_completed', grade: 8, subject: 'English' }).title, /Grade 8 English/)
})

test('recommendation outcome text is honest about pending and unobservable outcomes', () => {
  assert.match(outcomeText({ status: 'pending' }).text, /Waiting/)
  const up = outcomeText({ status: 'recorded', score: 80, score_change: 30, same_lesson: true, followed: true })
  assert.equal(up.tone, 'emerald')
  assert.match(up.text, /followed.*up 30 points/)
  const down = outcomeText({ status: 'recorded', score: 40, score_change: -10, same_lesson: false, lesson_title: 'Y', followed: null })
  assert.equal(down.tone, 'rose')
  assert.doesNotMatch(down.text, /followed/)
  assert.match(down.text, /“Y”.*down 10 points/)
})
