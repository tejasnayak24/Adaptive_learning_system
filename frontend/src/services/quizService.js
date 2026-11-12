import api from './api'

const nullable = (value) => (value === undefined ? null : value)

export const quizService = {
  /** Quiz questions for answering. The server never includes correct answers. */
  async getQuiz(id) {
    return await api.get(`/quiz/${id}`)
  },

  async getQuizzesByLesson(lessonId) {
    return await api.get(`/quiz/lesson/${lessonId}`)
  },

  /**
   * Submit the selected answers. The server grades them, stores the attempt
   * for the signed-in student and returns the result, the per-question
   * review and the adaptive recommendation (null without camera telemetry).
   */
  async submitQuiz(data) {
    return await api.post('/quiz/submit', {
      quiz_id: data.quizId,
      answers: data.answers,
      response_time: data.responseTime,
      hints_used: data.hintsUsed ?? 0,
      attention_score: nullable(data.attentionScore),
      yawning: nullable(data.yawning),
      looking_away: nullable(data.lookingAway),
      drowsy: nullable(data.drowsy),
    })
  },
}
