import api from './api'

const toNullableNumber = (value) =>
  value === undefined || value === null || Number.isNaN(Number(value)) ? null : Number(value)

const toNullableBool = (value) => (value === true || value === false ? value : null)

export const rlService = {
  /**
   * Request an adaptive recommendation.
   *
   * Camera-derived fields (attention_score, yawning, looking_away) are sent
   * as null when unknown. The backend then answers with
   * `telemetry_available: false` and no action instead of guessing.
   */
  async getRecommendation(data) {
    const payload = {
      subject: data.subject,
      topic: data.topic,
      lesson: data.lesson,
      previous_quiz_score: Math.round(Number(data.previous_quiz_score) || 0),
      current_quiz_score: Math.round(Number(data.current_quiz_score) || 0),
      difficulty: String(data.difficulty || '').toUpperCase(),
      response_time: Number(data.response_time) || 0,
      hints_used: parseInt(data.hints_used ?? 0, 10) || 0,
      lesson_attempts: parseInt(data.lesson_attempts ?? 0, 10) || 0,
      completed_lessons: parseInt(data.completed_lessons ?? 0, 10) || 0,
      attention_score: toNullableNumber(data.attention_score),
      yawning: toNullableBool(data.yawning),
      looking_away: toNullableBool(data.looking_away),
    }

    return await api.post('/rl/recommend', payload)
  },

  /**
   * The signed-in student's most recent stored recommendation.
   * Resolves to { status, recommendation, attempt } where status is
   * "available", "telemetry_unavailable", "not_generated" or "no_attempts".
   */
  async getLatest() {
    const response = await api.get('/recommendations/latest')
    return response?.data ?? { status: 'no_attempts', recommendation: null, attempt: null }
  },

  async getHistory() {
    const response = await api.get('/recommendations')
    return response?.data ?? []
  },
}
