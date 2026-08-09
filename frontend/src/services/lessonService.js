import api from './api'

export const lessonService = {
  async getLessons() {
    return await api.get('/lessons')
  },

  async getLesson(lessonId) {
    return await api.get(`/lesson/${lessonId}`)
  }
}
