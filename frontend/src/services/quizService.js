import api from './api'

export const quizService = {
  async getQuiz(quizId) {
    return await api.get(`/quiz/${quizId}`)
  },

  async submitQuiz({ studentId, lessonId, quizScore, responseTime, attentionScore, difficulty }) {
    return await api.post('/quiz/submit', {
      student_id: parseInt(studentId, 10),
      lesson_id: parseInt(lessonId, 10),
      quiz_score: parseFloat(quizScore),
      response_time: parseFloat(responseTime),
      attention_score: Number.isFinite(Number(attentionScore)) ? Number(attentionScore) : 0,
      difficulty: difficulty
    })
  }
}

