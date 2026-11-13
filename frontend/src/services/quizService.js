import api from './api'

export const quizService = {
  /** Quiz questions for answering. The server never includes correct answers. */
  async getQuiz(id) {
    return await api.get(`/quiz/${id}`)
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
      monitoring_session_id: data.monitoringSessionId,
      answers: data.answers,
      response_time: data.responseTime,
      hints_used: data.hintsUsed ?? 0,
      mode: data.mode || 'standard',
    })
  },
}
