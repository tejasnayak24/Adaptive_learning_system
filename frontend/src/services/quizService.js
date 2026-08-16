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
      student_id: data.studentId,
      lesson_id: data.lessonId,
      quiz_score: data.quizScore,
      response_time: data.responseTime,
      attention_score: data.attentionScore,
      difficulty: data.difficulty
    })
  }
}