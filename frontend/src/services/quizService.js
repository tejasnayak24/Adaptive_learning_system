import api from './api'

const nullable = (value) => (value === undefined ? null : value)

export const quizService = {
  async getQuiz(id) {
    return await api.get(`/quiz/${id}`)
  },

  async getQuizzesByLesson(lessonId) {
    return await api.get(`/quiz/lesson/${lessonId}`)
  },

  /**
   * Submit a quiz attempt. The backend records it for the authenticated
   * student. Camera fields are sent as null when telemetry is unavailable.
   */
  async submitQuiz(data) {
    return await api.post('/quiz/submit', {
      lesson_id: data.lessonId,
      quiz_score: data.quizScore,
      response_time: data.responseTime,
      attention_score: nullable(data.attentionScore),
      yawning: nullable(data.yawning),
      looking_away: nullable(data.lookingAway),
      difficulty: String(data.difficulty || '').toUpperCase(),
    })
  },
}
