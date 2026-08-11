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
    const parsedStudentId = parseInt(studentId, 10)
    const parsedLessonId = parseInt(lessonId, 10)
    const parsedQuizScore = parseFloat(quizScore)
    const parsedResponseTime = parseFloat(responseTime)

    const parsedAttentionScore =
      attentionScore !== undefined &&
      attentionScore !== null &&
      Number.isFinite(Number(attentionScore))
        ? parseFloat(attentionScore)
        : 0.5

    return await api.post('/quiz/submit', {
      student_id: parsedStudentId,
      lesson_id: parsedLessonId,
      quiz_score: parsedQuizScore,
      response_time: parsedResponseTime,
      attention_score: parsedAttentionScore,
      difficulty: String(difficulty || '').toUpperCase()
    })
  }
}