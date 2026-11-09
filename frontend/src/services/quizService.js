import api from './api'

export const quizService = {
  async getQuiz(id) {
    return await api.get(`/quiz/${id}`)
  },

  async getQuizzesByLesson(lessonId) {
    return await api.get(`/quiz/lesson/${lessonId}`)
  },

  async submitQuiz(data) {
    return await api.post('/quiz/submit', {
      student_id: Number(data.studentId),
      lesson_id: Number(data.lessonId),
      quiz_score: Number(data.quizScore),
      response_time: Number(data.responseTime),
      attention_score: Number(data.attentionScore ?? 0),
      difficulty: String(data.difficulty || 'EASY').toUpperCase(),
    })
  },
}