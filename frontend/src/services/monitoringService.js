import api from './api'

/** Backend endpoints for camera-monitoring consent and sessions. */
export const monitoringService = {
  async getConsent() {
    return (await api.get('/monitoring/consent')).data
  },

  async giveConsent({ guardianConfirmed = false, schoolConfirmed = false }) {
    return (
      await api.post('/monitoring/consent', {
        accept: true,
        guardian_authorization_confirmed: guardianConfirmed,
        school_authorization_confirmed: schoolConfirmed,
      })
    ).data
  },

  async withdrawConsent() {
    return (await api.delete('/monitoring/consent')).data
  },

  /** Returns { session_id, pairing_token, ...status }. Keep the token in memory only. */
  async createSession(lessonId) {
    return (await api.post('/monitoring/sessions', { lesson_id: lessonId ?? null })).data
  },

  /** New single-use pairing token for reconnecting the same session. */
  async reissuePairing(sessionId) {
    return (await api.post(`/monitoring/sessions/${sessionId}/pairing`)).data
  },

  async getStatus(sessionId) {
    return (await api.get(`/monitoring/sessions/${sessionId}`)).data
  },

  async endSession(sessionId) {
    return (await api.post(`/monitoring/sessions/${sessionId}/end`)).data
  },
}
