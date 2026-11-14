// Pure helpers for the dashboard, progress and AI Coach pages. All values
// come from the backend's /analytics/summary and /recommendations
// responses; nothing here invents data. Unit-tested with `npm test`.

export const SUBJECT_ORDER = ['Mathematics', 'Science', 'Social Science', 'English']

// Categorical subject colours (violet, teal, amber, rose in this fixed order),
// validated with the dataviz palette validator against the card surface
// #151C2D: all inside the dark lightness band, chroma above the floor, >= 3:1
// contrast, adjacent colour-vision separation >= 8 and normal-vision >= 15.
// Rose and teal are close under deuteranopia when not adjacent, so a
// subject's name is always shown next to its colour. Colour follows the
// subject, never its rank, so a filter never repaints a subject.
export const SUBJECT_COLORS = {
  Mathematics: '#8875ff',
  Science: '#26a68b',
  'Social Science': '#c98500',
  English: '#d55181'
}

export const SCORE_COLOR = '#8875ff'
export const ATTENTION_COLOR = '#43cdb0'

export const TOPIC_STATUS = {
  strong: {
    label: 'Strong',
    icon: '✓',
    tone: 'emerald',
    help: 'Your recent quiz scores here are 80% or more.'
  },
  needs_revision: {
    label: 'Needs revision',
    icon: '↻',
    tone: 'amber',
    help: 'You are passing, but your recent scores are below 80% or your last quiz dropped. A quick revision will help.'
  },
  weak: {
    label: 'Weak',
    icon: '!',
    tone: 'rose',
    help: 'Your recent scores here are below the 50% pass mark. Go back over the lesson before the next quiz.'
  },
  insufficient_data: {
    label: 'Not enough attempts',
    icon: '…',
    tone: 'slate',
    help: 'One quiz is not enough to judge a topic. Try another quiz here.'
  },
  not_started: {
    label: 'Not started',
    icon: '○',
    tone: 'slate',
    help: 'No quizzes taken in this topic yet.'
  }
}

export const TOPIC_STATUS_ORDER = ['weak', 'needs_revision', 'strong', 'insufficient_data', 'not_started']

export const TELEMETRY_LABELS = {
  measured: 'Camera measured',
  unavailable: 'Camera data unavailable',
  not_monitored: 'Not monitored'
}

export const TELEMETRY_HELP = {
  measured: 'Attention was measured by the camera agent during this quiz.',
  unavailable:
    'Camera monitoring was on, but no valid live reading arrived during this quiz (camera off, face not found or the readings were out of date). This is not low attention.',
  not_monitored: 'This quiz was taken before camera monitoring was added, so attention was not recorded.'
}

export function topicStatusInfo(status) {
  return TOPIC_STATUS[status] || TOPIC_STATUS.not_started
}

export function subjectColor(subject) {
  return SUBJECT_COLORS[subject] || '#64748b'
}

/** "72%" or the fallback for null/undefined. */
export function formatPercent(value, fallback = '—') {
  if (value === null || value === undefined || Number.isNaN(Number(value))) return fallback
  return `${Math.round(Number(value))}%`
}

/** Parse an API timestamp (naive UTC ISO) to a Date, or null. */
export function parseDate(value) {
  if (!value) return null
  const text = /[zZ]|[+-]\d\d:?\d\d$/.test(value) ? value : `${value}Z`
  const date = new Date(text)
  return Number.isNaN(date.getTime()) ? null : date
}

export function formatDate(value, { withTime = false } = {}) {
  const date = parseDate(value)
  if (!date) return 'Date not recorded'
  return date.toLocaleString(undefined, {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    ...(withTime ? { hour: '2-digit', minute: '2-digit' } : {})
  })
}

/** "today", "3 days ago" … relative to `now`. */
export function relativeDay(value, now = new Date()) {
  const date = parseDate(value)
  if (!date) return 'date not recorded'
  const days = Math.floor((startOfDay(now) - startOfDay(date)) / 86400000)
  if (days <= 0) return 'today'
  if (days === 1) return 'yesterday'
  if (days < 30) return `${days} days ago`
  return formatDate(value)
}

function startOfDay(date) {
  const d = new Date(date)
  d.setHours(0, 0, 0, 0)
  return d.getTime()
}

/**
 * Filter quiz-trend points by subject and date range.
 * filters: { subject: 'all' | name, from: 'YYYY-MM-DD' | '', to: 'YYYY-MM-DD' | '' }
 * Points with no recorded date are kept only when no date filter is set.
 */
export function filterTrend(points, { subject = 'all', from = '', to = '' } = {}) {
  const fromTime = from ? new Date(`${from}T00:00:00`).getTime() : null
  const toTime = to ? new Date(`${to}T23:59:59.999`).getTime() : null
  return (points || []).filter((p) => {
    if (subject !== 'all' && p.subject !== subject) return false
    if (fromTime === null && toTime === null) return true
    const date = parseDate(p.at)
    if (!date) return false
    const t = date.getTime()
    return (fromTime === null || t >= fromTime) && (toTime === null || t <= toTime)
  })
}

/** Chart rows for the score trend: attempt number, score, and labels. */
export function trendRows(points) {
  return (points || []).map((p, index) => ({
    n: index + 1,
    label: `#${index + 1}`,
    score: p.score,
    attention: p.attention,
    subject: p.subject,
    lesson: p.lesson_title,
    difficulty: p.difficulty,
    mode: p.mode,
    at: p.at,
    telemetry: p.telemetry
  }))
}

/**
 * Average score of the first and last `size` attempts, for a plain-language
 * "are my scores going up?" summary. Null when there are too few attempts.
 */
export function trendDirection(points, size = 3) {
  const scores = (points || []).map((p) => p.score).filter((s) => typeof s === 'number')
  if (scores.length < size * 2) return null
  const mean = (xs) => xs.reduce((a, b) => a + b, 0) / xs.length
  const first = mean(scores.slice(0, size))
  const last = mean(scores.slice(-size))
  const change = Math.round(last - first)
  return { first: Math.round(first), last: Math.round(last), change, direction: change > 2 ? 'up' : change < -2 ? 'down' : 'flat' }
}

/** ISO week start (Monday, local time) as YYYY-MM-DD. */
function weekStart(date) {
  const d = new Date(date)
  d.setHours(0, 0, 0, 0)
  const day = (d.getDay() + 6) % 7
  d.setDate(d.getDate() - day)
  const pad = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`
}

/**
 * Quiz attempts per week (only weeks between the first and last dated
 * attempt; empty weeks are shown as 0, not hidden). Undated attempts are
 * counted separately.
 */
export function weeklyActivity(points) {
  const counts = new Map()
  let undated = 0
  for (const p of points || []) {
    const date = parseDate(p.at)
    if (!date) {
      undated += 1
      continue
    }
    const key = weekStart(date)
    counts.set(key, (counts.get(key) || 0) + 1)
  }
  const keys = [...counts.keys()].sort()
  const weeks = []
  if (keys.length) {
    const cursor = new Date(`${keys[0]}T00:00:00`)
    const end = new Date(`${keys[keys.length - 1]}T00:00:00`)
    while (cursor <= end) {
      const key = weekStart(cursor)
      weeks.push({ week: key, attempts: counts.get(key) || 0 })
      cursor.setDate(cursor.getDate() + 7)
    }
  }
  return { weeks, undated }
}

/** Plain-language summary of the camera analytics. */
export function attentionSummary(attention) {
  if (!attention || attention.attempts_total === 0) {
    return { level: 'none', message: 'No quizzes yet, so there is no camera data.' }
  }
  if (attention.measured_attempts === 0) {
    return {
      level: 'none',
      message:
        'None of your quizzes has a valid camera measurement yet, so there is no attention average. Keep the camera agent running during quizzes.'
    }
  }
  if (!attention.sufficient_history) {
    return {
      level: 'limited',
      message: `Only ${attention.measured_attempts} quiz${attention.measured_attempts === 1 ? '' : 'zes'} had a camera measurement. At least ${attention.min_measured_attempts} are needed before the trend means much.`
    }
  }
  return {
    level: 'ok',
    message: `Based on ${attention.measured_attempts} quizzes with a camera measurement.`
  }
}

/** "observed in 2 of 5 measured quizzes" or "no camera data". */
export function observationText(obs) {
  if (!obs || !obs.measured_attempts) return 'No camera data'
  return `${obs.observed_in} of ${obs.measured_attempts} measured quiz${obs.measured_attempts === 1 ? '' : 'zes'}`
}

/** Next lesson to continue: first unfinished lesson of the most recent subject. */
export function continueTarget(summary) {
  if (!summary) return null
  const topics = summary.topics || []
  const latest = summary.overview?.latest_activity
  const ordered = latest?.subject
    ? [...topics.filter((t) => t.subject === latest.subject), ...topics.filter((t) => t.subject !== latest.subject)]
    : topics
  const topic = ordered.find((t) => t.next_lesson)
  if (!topic) return null
  return { ...topic.next_lesson, topic: topic.topic, subject: topic.subject }
}

/** Student-friendly text for an activity event. */
export function activityText(event) {
  switch (event.type) {
    case 'quiz_attempt':
      return {
        icon: event.passed ? '📝' : '🔁',
        title: `${event.passed ? 'Passed' : 'Tried'} the ${String(event.difficulty || '').toLowerCase()} quiz — ${formatPercent(event.score)}`,
        detail: `${event.lesson_title} · ${event.subject}`
      }
    case 'lesson_completed':
      return { icon: '✅', title: `Completed “${event.lesson_title}”`, detail: `${event.topic} · ${event.subject}` }
    case 'subject_completed':
      return { icon: '🏆', title: `Finished Grade ${event.grade} ${event.subject}`, detail: 'Every lesson passed' }
    default:
      return { icon: '•', title: 'Activity', detail: '' }
  }
}

/** Plain-language description of a recorded recommendation outcome. */
export function outcomeText(outcome) {
  if (!outcome || outcome.status !== 'recorded') {
    return { tone: 'slate', text: 'Waiting for your next quiz to see how this went.' }
  }
  const change = outcome.score_change
  const where = outcome.same_lesson ? 'the same lesson' : `“${outcome.lesson_title}”`
  const followed =
    outcome.followed === true ? 'You followed this advice. ' : outcome.followed === false ? 'You chose a different step. ' : ''
  if (change === null || change === undefined) {
    return { tone: 'slate', text: `${followed}Next quiz: ${formatPercent(outcome.score)} on ${where}.` }
  }
  const delta = Math.round(change)
  const tone = delta > 0 ? 'emerald' : delta < 0 ? 'rose' : 'slate'
  const movement = delta > 0 ? `up ${delta} points` : delta < 0 ? `down ${Math.abs(delta)} points` : 'the same score'
  return { tone, text: `${followed}Next quiz: ${formatPercent(outcome.score)} on ${where} (${movement}).` }
}
