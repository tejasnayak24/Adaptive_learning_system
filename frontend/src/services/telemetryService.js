import api from './api'

/**
 * Facial-analysis telemetry for the signed-in student.
 *
 * Measurements come only from the paired camera agent's heartbeats. The
 * backend reports `available: false` (with null measurements) when no fresh
 * reading exists -- that means "camera data unavailable", never low attention.
 */
export const telemetryService = {
  async getTelemetry(studentId) {
    const response = await api.get(`/attention/${studentId}`)
    return response?.data ?? null
  },

  async resetSession(studentId) {
    const response = await api.post(`/attention/${studentId}/reset`)
    return response?.data ?? null
  },
}
