import api from './api'

/**
 * Facial-analysis telemetry for the signed-in student.
 *
 * The backend reports `available: false` (with null measurements) when no
 * fresh camera reading exists. Callers must treat that as "camera data
 * unavailable" -- never as low attention.
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

  /**
   * Convert a telemetry snapshot into the camera fields stored with a quiz
   * attempt. Returns nulls when telemetry is unavailable.
   */
  toAttemptMetrics(telemetry) {
    if (!telemetry || telemetry.available !== true) {
      return { attentionScore: null, yawning: null, lookingAway: null, available: false }
    }

    const attention =
      telemetry.session_average_attention ?? telemetry.attention_score ?? null

    return {
      attentionScore: attention === null ? null : Number(attention),
      yawning: telemetry.yawning_observed ?? telemetry.yawning ?? null,
      lookingAway: telemetry.looking_away_observed ?? telemetry.looking_away ?? null,
      available: attention !== null,
    }
  },
}
