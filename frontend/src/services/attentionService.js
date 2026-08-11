import api from './api'

export const quizService = {
  async getQuiz(quizId) {
    return await api.get(`/quiz/${quizId}`)
  },

  async submitQuiz({
    studentId,
    lessonId,
    quizScore,
    responseTime,
    attentionScore,
    difficulty
  }) {
    const score = Number.isFinite(Number(attentionScore))
      ? parseFloat(attentionScore)
      : 0.5

    return await api.post('/quiz/submit', {
      student_id: parseInt(studentId, 10),
      lesson_id: parseInt(lessonId, 10),
      quiz_score: parseFloat(quizScore),
      response_time: parseFloat(responseTime),
      attention_score: score,
      difficulty: String(difficulty).toUpperCase()
    })
  }
}