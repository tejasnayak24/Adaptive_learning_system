import api from './api'

/**
 * fetch() for requests that must survive the page being hidden or closed
 * (``keepalive``), which axios cannot do. Same /api prefix and bearer token
 * as api.js; the token goes in a header, never in the URL.
 */
async function sendJson(path, body, { method = 'POST', keepalive = false } = {}) {
  const headers = { 'Content-Type': 'application/json' }
  const token = localStorage.getItem('token')
  if (token) headers.Authorization = `Bearer ${token}`
  let response
  try {
    response = await fetch(`/api${path}`, {
      method,
      headers,
      body: body === undefined ? undefined : JSON.stringify(body),
      keepalive,
      credentials: 'same-origin',
    })
  } catch (networkError) {
    const failure = new Error(networkError?.message || 'Network error')
    failure.status = null
    throw failure
  }
  const data = await response.json().catch(() => null)
  if (!response.ok) {
    const detail = data?.detail
    const failure = new Error(
      typeof detail === 'string' ? detail : detail?.message || `Request failed (${response.status})`
    )
    failure.status = response.status
    failure.detail = detail ?? null
    throw failure
  }
  return data
}

export const quizService = {
  /** Quiz questions for answering. The server never includes correct answers. */
  async getQuiz(id) {
    return await api.get(`/quiz/${id}`)
  },

  /**
   * Start a server-side attempt, or resume the open one (after a reload).
   * Rejects with status 429 (and ``detail.retry_after_seconds``) during the
   * cooldown after a terminated or abandoned attempt.
   */
  async startAttempt({ quizId, mode, monitoringSessionId }) {
    return await api.post('/quiz/start', {
      quiz_id: Number(quizId),
      mode: mode || 'standard',
      ...(monitoringSessionId ? { monitoring_session_id: monitoringSessionId } : {}),
    })
  },

  async getAttempt(attemptId) {
    return await api.get(`/quiz/attempts/${attemptId}`)
  },

  /** Save in-progress answers (partial) and resumable UI state. */
  async saveAnswers(attemptId, answers, draftState, { keepalive = false } = {}) {
    const data = await sendJson(
      `/quiz/attempts/${attemptId}/answers`,
      { answers, draft_state: draftState },
      { method: 'PUT', keepalive }
    )
    return data?.data
  },

  /** Page events for the tab-switch rule; returns the server's attempt view. */
  async sendAttemptEvents(attemptId, pageId, events, { keepalive = false } = {}) {
    const data = await sendJson(`/quiz/attempts/${attemptId}/events`, { page_id: pageId, events }, { keepalive })
    return data?.data
  },

  /** The student confirmed leaving the quiz: kept, not graded, no violation. */
  async abandonAttempt(attemptId, { keepalive = false } = {}) {
    const data = await sendJson(`/quiz/attempts/${attemptId}/abandon`, undefined, { keepalive })
    return data?.data
  },

  async getQuizzesByLesson(lessonId) {
    return await api.get(`/quiz/lesson/${lessonId}`)
  },

  /**
   * Submit the selected answers for a monitored session. The server grades
   * them and takes camera measurements from its paired agent's telemetry
   * for that session -- the browser never sends attention values.
   */
  async submitQuiz(data) {
    return await api.post('/quiz/submit', {
      quiz_id: data.quizId,
      attempt_id: data.attemptId,
      monitoring_session_id: data.monitoringSessionId,
      answers: data.answers,
      response_time: data.responseTime,
      hints_used: data.hintsUsed ?? 0,
      mode: data.mode || 'standard',
    })
  },
}
