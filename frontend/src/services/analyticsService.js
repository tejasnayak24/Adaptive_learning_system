import api from './api'

export const analyticsService = {
  /** Dashboard / progress analytics for the signed-in student only. */
  async getSummary() {
    const response = await api.get('/analytics/summary')
    return response?.data ?? null
  }
}
