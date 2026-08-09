import api from './api'

export const progressService = {
  async getStudentProgress(studentId) {
    return await api.get(`/progress/${studentId}`)
  },

  async getLessonProgress(studentId, lessonId) {
    return await api.get(`/progress/${studentId}/${lessonId}`)
  },

  async updateProgress(progressId, data) {
    return await api.put(`/progress/${progressId}`, data)
  }
}
