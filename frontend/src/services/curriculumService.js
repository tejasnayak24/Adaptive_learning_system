import api from './api'

export const SUBJECTS = ['Mathematics', 'Science', 'Social Science', 'English']

export const curriculumService = {
  /** The signed-in student's grade curriculum (optionally one subject). */
  async getCurriculum(subject) {
    const query = subject ? `?subject=${encodeURIComponent(subject)}` : ''
    return await api.get(`/curriculum${query}`)
  },

  async getGrades() {
    return await api.get('/curriculum/grades')
  },

  async getNavigation(lessonId) {
    return await api.get(`/curriculum/lessons/${lessonId}/navigation`)
  }
}
