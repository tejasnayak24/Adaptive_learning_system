import api from './api'

export const quizService = {
  async startQuiz(quizId) {
    return await api.post('/quiz/start', { quiz_id: parseInt(quizId, 10) })
  },

  async getQuiz(quizId) {
    return await api.get(`/quiz/${quizId}`)
  },

  async submitQuiz({ studentId, lessonId, quizScore, responseTime, attentionScore, difficulty }) {
    return await api.post('/quiz/submit', {
      student_id: parseInt(studentId, 10),
      lesson_id: parseInt(lessonId, 10),
      quiz_score: parseFloat(quizScore),
      response_time: parseFloat(responseTime),
      attention_score: parseFloat(attentionScore),
      difficulty: difficulty
    })
  }
}
